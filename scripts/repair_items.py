#!/usr/bin/env python3
"""repair_items.py — book-based repair of the FLIP_REVIEW_LOG needs-review items.

For each flagged qid: retrieve OFFICIAL book passages (topic-matched), ask the model
whether the marked answer is correct and — if not — what the book-correct answer text
is, whether it is offered, and the verbatim passage. Output review JSON; apply manually.

Usage:
  python3 scripts/repair_items.py                 # run the batch (deepseek, books-only)
  python3 scripts/repair_items.py --review        # print staged repairs with passages
"""
from __future__ import annotations

import json
import re
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
Q_JS = ROOT / "sdle-prep" / "data" / "questions.js"
CORPUS = ROOT / "sdle-prep" / "data" / "raw" / "books" / "text"
OUT = ROOT / "sdle-prep" / "data" / "generated" / "uncertain"
OUT.mkdir(parents=True, exist_ok=True)

API = {"url": "https://api.deepseek.com/chat/completions",
       "key": "sk-ba41aeb17e7641c99cd24c4ee2e57098", "model": "deepseek-chat"}

# qids still flagged in FLIP_REVIEW_LOG (verified current state 2026-08-06)
FLAGGED = ("ab2_7710e019d9 ab2_f71be23273 fr_boost_033 ab2_2f241b10b7 ab2_9fe3fc238b "
           "rafi_01_1e7372f945 ab2_5c94fb585c rafi_01_6b9539a6a5 rafi_01_716334486e "
           "rafi_10_520feb3b96 rafi_14_b4b8982575 rafi_06_0d311c408f rafi_08_8b7dbb6ea6 "
           "rafi_17_46df219c7b rafi_17_f8f45558ed rafi_18_9793f334c2 "
           "rafi_04_381c1e1f81 rafi_04_0d96b8c5fe rafi_12_68bc391e9d rafi_15_8564eb49ec "
           "rafi_20_bfd4d592dd rafi_08_6dfb9d2845 rafi_15_e2981fe47b ab2_2b6d04a4a1 "
           "rafi_03_bc3dfe851b rafi_04_d4958735c5 rafi_08_43a5bf4c8c rafi_04_4f8e77ae69 "
           "rafi_07_d94477dd31 rafi_06_3c40385fd0 rafi_16_5591d0a9de rafi_18_89b6f2d029").split()

TOPIC_DIRS = {
    "endo": ["Endo"], "perio": ["perio"],
    "restorative": ["Resto", "Fixed", "Removable"], "operative": ["Resto", "Fixed", "Removable"],
    "fixed": ["Fixed"], "rpd": ["Removable"], "materials": ["Resto", "Fixed"],
    "oms": ["Oral surgary"], "ortho_pedo": ["ortho", "pedo"],
    "ethics": ["Ethics + infection control + local anasthesia"], "mixed": None,
}
STOP = {"which", "following", "what", "with", "that", "this", "from", "have", "would", "should",
        "patient", "treatment", "correct", "answer", "best", "most", "about", "their", "there",
        "these", "those", "because", "during", "after", "before", "between", "when", "where",
        "than", "then", "they", "them", "into", "over", "under", "used", "use", "not", "all",
        "one", "can", "may", "are", "was", "were", "has", "had", "its", "also", "other"}

SYSTEM = """You are a dental board examiner REPAIRING exam questions using OFFICIAL TEXTBOOK PASSAGES ONLY.
You are given verbatim passages from official dental textbooks, then one exam question (options + marked answer).

For EACH question output a JSON object:
{"qid":"...",
 "marked_correct": true|false,            # is the marked answer right per the passage?
 "correct_text": "the correct answer text",   # book-supported correct answer (exact wording)
 "offered": true|false,                   # is correct_text already among the options?
 "offered_index": 0-3 or null,            # if offered, which index
 "passage": "short verbatim quote",
 "book": "book title",
 "repair": "what to change: fix answer index, replace option N, hide question, or keep with new evidence"}
Passages are the ONLY evidence. Never invent. If no passage decides it, say marked_correct: null and repair: "unresolvable".
Reply with ONLY the JSON array, no markdown, no commentary."""


def load_bank():
    raw = Q_JS.read_text(encoding="utf-8")
    m = re.search(r"QUESTION_BANK\s*=\s*(\[.*\])", raw, re.S)
    return json.loads(m.group(1))


def load_corpus():
    idx = {}
    for d in sorted(CORPUS.iterdir()):
        if not d.is_dir() or "FACTPACK" in d.name:
            continue
        passages = []
        for f in sorted(d.glob("*.txt")):
            try:
                txt = f.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            if txt.count("(cid:") > 50:
                continue
            for i in range(0, len(txt), 600):
                chunk = txt[i:i + 600]
                if len(chunk.strip()) >= 60:
                    passages.append((f.stem, chunk))
        idx[d.name] = passages
    return idx


def keywords(q):
    text = " ".join([q.get("q", ""), *(q.get("options") or []), q.get("explanation", "")])
    words = re.findall(r"[A-Za-z][A-Za-z\-]{3,}", text.lower())
    return [w for w in words if w not in STOP and len(w) > 3][:18]


def retrieve(pool, kws, k=8):
    scored = []
    for name, p in pool:
        low = p.lower()
        s = sum(1 for kw in kws if kw in low)
        if s:
            scored.append((s, name, p))
    scored.sort(key=lambda x: -x[0])
    return scored[:k]


def topic_pool(corpus, topic):
    dirs = TOPIC_DIRS.get(topic)
    if dirs is None:
        return [p for ps in corpus.values() for p in ps]
    pool = []
    for d in dirs:
        pool.extend(corpus.get(d, []))
    return pool


def call_api(prompt, timeout=180):
    body = json.dumps({"model": API["model"],
                       "messages": [{"role": "system", "content": SYSTEM},
                                    {"role": "user", "content": prompt}],
                       "max_tokens": 9000, "temperature": 0.1}).encode()
    req = urllib.request.Request(API["url"], data=body, headers={
        "Content-Type": "application/json", "Authorization": f"Bearer {API['key']}"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                data = json.loads(resp.read().decode())
            return (data.get("choices", [{}])[0].get("message", {}).get("content") or "").strip()
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(12 * (attempt + 1)); continue
            if e.code in (500, 502, 503):
                time.sleep(6); continue
            return f"__HTTP {e.code}"
        except Exception as e:
            return f"__ERR {type(e).__name__}"
    return "__RATE"


def parse(resp, qids):
    t = re.sub(r"```(?:json)?", "", resp).strip()
    arr = None
    start = t.find("[")
    if start >= 0:
        end, depth, in_str, esc = -1, 0, False, False
        for i in range(start, len(t)):
            c = t[i]
            if in_str:
                if esc: esc = False
                elif c == "\\": esc = True
                elif c == '"': in_str = False
                continue
            if c == '"': in_str = True
            elif c == "[": depth += 1
            elif c == "]":
                depth -= 1
                if depth == 0:
                    end = i; break
        if end > 0:
            try:
                arr = json.loads(t[start:end + 1])
            except Exception:
                arr = None
    if arr is None:
        # bare object (model returns {...} for a single item)
        s0 = t.find("{")
        if s0 >= 0:
            end, depth, in_str, esc = -1, 0, False, False
            for i in range(s0, len(t)):
                c = t[i]
                if in_str:
                    if esc: esc = False
                    elif c == "\\": esc = True
                    elif c == '"': in_str = False
                    continue
                if c == '"': in_str = True
                elif c == "{": depth += 1
                elif c == "}":
                    depth -= 1
                    if depth == 0:
                        end = i; break
            if end > 0:
                try:
                    obj = json.loads(t[s0:end + 1])
                    if isinstance(obj, dict) and obj.get("qid"):
                        arr = [obj]
                except Exception:
                    arr = None
    if arr is None:
        return None
    by = {a.get("qid"): a for a in arr if isinstance(a, dict) and a.get("qid")}
    return [by.get(q) for q in qids]


def main():
    review = "--review" in sys.argv
    bank = load_bank()
    by_id = {q["id"]: q for q in bank}
    qs = [by_id[i] for i in FLAGGED if i in by_id]
    print(f"repairing {len(qs)} flagged items")

    corpus = load_corpus()
    results = []
    for i, q in enumerate(qs):
        topic = q.get("department") or q.get("topic") or "mixed"
        kws = keywords(q)
        hits = retrieve(topic_pool(corpus, topic), kws, 8)
        passages = "\n".join(f"({name}) {p.strip()[:500]}" for _, name, p in hits) or "(no passages found)"
        opts = "\n".join(f"{j+1}. {o}" for j, o in enumerate(q["options"]))
        prompt = (f"PASSAGES:\n{passages}\n\n"
                  f"QID:{q['id']}\nQ: {q['q'][:250]}\nOPTIONS:\n{opts}\n"
                  f"MARKED ANSWER ({q['answer']}): {q['options'][q['answer']]}\n"
                  f"NOTE: marked answer may be wrong or missing; verify against the passages.")
        resp = call_api(prompt)
        arr = parse(resp, [q["id"]])
        v = arr[0] if arr and arr[0] else {"qid": q["id"], "marked_correct": None, "repair": "parse-fail " + resp[:100]}
        results.append(v)
        print(f"[{i+1}/{len(qs)}] {q['id']}: marked_correct={v.get('marked_correct')} offered={v.get('offered')} repair={str(v.get('repair'))[:60]}", flush=True)
        time.sleep(0.8)

    with open(OUT / "repairs.json", "w", encoding="utf-8") as fh:
        json.dump(results, fh, ensure_ascii=False, indent=1)

    if review:
        print("\n=== REVIEW ===")
        for v in results:
            q = by_id.get(v.get("qid"), {})
            print(f"\n{v.get('qid')} | marked_correct={v.get('marked_correct')} offered={v.get('offered')} idx={v.get('offered_index')}")
            print(f"  correct_text: {v.get('correct_text')}")
            print(f"  repair: {v.get('repair')}")
            print(f"  passage: {str(v.get('passage'))[:200]}")
            print(f"  book: {v.get('book')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

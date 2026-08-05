#!/usr/bin/env python3
"""verify_uncertain.py — re-verify the 2,020 'uncertain' verdicts against the OFFICIAL
book corpus ONLY (data/raw/books/text/*.txt — extracted from /data/prometric/books PDFs).
Factpacks (.md) and community banks are NEVER used as evidence here.

Parallel: shard by qid crc32 % N, per-shard checkpoints, merge, then --apply.
Usage:
  python3 scripts/verify_uncertain.py --shard 0/4 --checkpoint data/generated/uncertain/s0.jsonl
  python3 scripts/verify_uncertain.py --merge
  python3 scripts/verify_uncertain.py --apply   (supported -> real book_support; contradicted -> review log)
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.request
import urllib.error
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
Q_JS = ROOT / "sdle-prep" / "data" / "questions.js"
CORPUS = ROOT / "sdle-prep" / "data" / "raw" / "books" / "text"
OUT = ROOT / "sdle-prep" / "data" / "generated" / "uncertain"
OUT.mkdir(parents=True, exist_ok=True)
VERDICTS = ROOT / "sdle-prep" / "data" / "generated" / "bank_verification" / "verdicts.jsonl"

API = {"url": "https://api.deepseek.com/chat/completions",
       "key": "sk-ba41aeb17e7641c99cd24c4ee2e57098", "model": "deepseek-chat"}

SYSTEM = """You are a dental board examiner verifying MCQ answers against OFFICIAL TEXTBOOK PASSAGES ONLY.
You are given verbatim passages from official dental textbooks, then a list of exam questions (options + the bank's marked answer).

For EVERY question decide:
- supported: the marked answer is CORRECT and a passage supports it (quote the passage verbatim).
- contradicted: the marked answer is WRONG (a passage contradicts it). Give the correct option index if offered.
- uncertain: no passage supports or contradicts it — say so honestly. Do NOT guess.

Passages are the ONLY evidence. Never invent citations. Never claim support without quoting.
Reply with ONLY a JSON array, one object per question, in order:
[{"qid":"...","verdict":"supported|contradicted|uncertain","correct_option":0-3 or null,"passage":"short verbatim quote","book":"book title","reason":"one sentence"}]
No markdown fences, no commentary."""


def load_bank():
    raw = Q_JS.read_text(encoding="utf-8")
    m = re.search(r"QUESTION_BANK\s*=\s*(\[.*\])", raw, re.S)
    return json.loads(m.group(1))


def uncertain_qids():
    ids = []
    for line in open(VERDICTS, encoding="utf-8"):
        try:
            r = json.loads(line)
            if r.get("verdict") == "uncertain":
                ids.append(r["qid"])
        except Exception:
            pass
    return ids


def load_corpus():
    """topic -> passages (600-char chunks). OFFICIAL books only:
    data/raw/books/text/*.txt + sdle-ref/books/*.md (both from the book PDFs).
    Factpacks and community files are NEVER used."""
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
    # supplement: sdle-ref/books/*.md (book markdown conversions)
    ref = ROOT / "sdle-ref" / "books"
    if ref.exists():
        for f in sorted(ref.glob("*.md")):
            try:
                txt = f.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            topic = str(f.name).split("_")[0].lower()
            topic = {"endo": "Endo", "perio": "perio", "fixed": "Fixed",
                     "resto": "Resto", "removable": "Removable",
                     "ortho": "ortho", "pedo": "pedo", "oral": "Oral surgary",
                     "oms": "Oral surgary", "ethics": "Ethics + infection control + local anasthesia"}.get(topic)
            if topic is None:
                continue
            for i in range(0, len(txt), 600):
                chunk = txt[i:i + 600]
                if len(chunk.strip()) >= 60:
                    idx.setdefault(topic, []).append((f.stem, chunk))
    return idx


STOP = {"which", "following", "what", "with", "that", "this", "from", "have", "would", "should",
        "patient", "treatment", "correct", "answer", "best", "most", "about", "their", "there",
        "these", "those", "because", "during", "after", "before", "between", "when", "where",
        "than", "then", "they", "them", "into", "over", "under", "used", "use", "not", "all",
        "one", "can", "may", "are", "was", "were", "has", "had", "its", "also", "other"}


def keywords(q):
    text = " ".join([q.get("q", ""), *(q.get("options") or []), q.get("explanation", "")])
    words = re.findall(r"[A-Za-z][A-Za-z\-]{3,}", text.lower())
    kws = [w for w in words if w not in STOP and len(w) > 3][:20]
    # also add the marked-answer distinctive words (the fact is often stated in books)
    ans = str(q.get("options", [""])[q.get("answer")]) if q.get("options") else ""
    for w in re.findall(r"[A-Za-z][A-Za-z\-]{3,}", ans.lower()):
        if w not in STOP and len(w) > 3 and w not in kws:
            kws.append(w)
    return kws[:22]


def retrieve(passages, kws, k=5):
    scored = []
    for name, p in passages:
        low = p.lower()
        s = sum(1 for kw in kws if kw in low)
        if s:
            scored.append((s, name, p))
    scored.sort(key=lambda x: -x[0])
    return scored[:k]


def call_api(prompt, timeout=180):
    body = json.dumps({"model": API["model"],
                       "messages": [{"role": "system", "content": SYSTEM},
                                    {"role": "user", "content": prompt}],
                       "max_tokens": 8000, "temperature": 0.1}).encode()
    req = urllib.request.Request(API["url"], data=body, headers={
        "Content-Type": "application/json", "Authorization": f"Bearer {API['key']}"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                data = json.loads(resp.read().decode())
            msg = data.get("choices", [{}])[0].get("message", {})
            return (msg.get("content") or "").strip()
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
    start = t.find("[")
    if start < 0:
        return None
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
    if end < 0:
        return None
    try:
        arr = json.loads(t[start:end + 1])
    except Exception:
        return None
    return arr


TOPIC_DIRS = {
    "endo": ["Endo"],
    "perio": ["perio"],
    "restorative": ["Resto", "Fixed", "Removable"],
    "operative": ["Resto", "Fixed", "Removable"],
    "fixed": ["Fixed"],
    "rpd": ["Removable"],
    "materials": ["Resto", "Fixed"],
    "oms": ["Oral surgary"],
    "ortho_pedo": ["ortho", "pedo"],
    "ethics": ["Ethics + infection control + local anasthesia"],
    "mixed": None,  # all folders
}


def topic_pool(corpus, topic):
    dirs = TOPIC_DIRS.get(topic)
    if dirs is None:
        return [p for ps in corpus.values() for p in ps]
    pool = []
    for d in dirs:
        pool.extend(corpus.get(d, []))
    return pool


def build_prompt(batch, corpus):
    parts = ["TEXTBOOK PASSAGES (verbatim, official books only):"]
    for q in batch:
        topic = q.get("department") or q.get("topic") or "mixed"
        pool = topic_pool(corpus, topic)
        kws = keywords(q)
        hits = retrieve(pool, kws, 5)
        if not hits:
            continue
        parts.append(f"[{q['id']}]")
        for _, name, p in hits:
            parts.append(f"({name}) {p.strip()[:450]}")
    parts.append("\nQUESTIONS:")
    for q in batch:
        opts = "\n".join(f"{i+1}. {o}" for i, o in enumerate(q["options"]))
        parts.append(f"QID:{q['id']}\nQ: {q['q'][:220]}\nOPTIONS:\n{opts}\nMARKED ANSWER ({q['answer']}): {q['options'][q['answer']]}\n---")
    return "\n".join(parts)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shard", default="0/1")
    ap.add_argument("--checkpoint", default=str(OUT / "s0.jsonl"))
    ap.add_argument("--batch", type=int, default=20)
    ap.add_argument("--merge", action="store_true")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--stats", action="store_true")
    args = ap.parse_args()

    if args.merge:
        merged = {}
        for f in sorted(OUT.glob("s*.jsonl")):
            for line in open(f, encoding="utf-8"):
                try:
                    r = json.loads(line)
                    if r.get("qid") and r.get("verdict"):
                        merged[r["qid"]] = r
                except Exception:
                    pass
        with open(OUT / "final.jsonl", "w", encoding="utf-8") as fh:
            for r in merged.values():
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
        from collections import Counter
        print("merged:", len(merged), dict(Counter(v["verdict"] for v in merged.values())))
        return 0

    if args.apply:
        bank = load_bank()
        by_id = {q["id"]: q for q in bank}
        final = OUT / "final.jsonl"
        if not final.exists():
            print("run --merge first")
            return 1
        applied = 0
        review = []
        for line in open(final, encoding="utf-8"):
            try:
                r = json.loads(line)
            except Exception:
                continue
            q = by_id.get(r.get("qid"))
            if not q or q.get("usable") is False:
                continue
            v = r.get("verdict")
            if v == "supported" and r.get("passage"):
                q["book_support"] = f"[Book: {r.get('book') or 'textbook'}] {r['passage'][:400]}"
                q["book_verified"] = True
                applied += 1
            elif v == "contradicted":
                review.append(r)
        raw = Q_JS.read_text(encoding="utf-8")
        m = re.search(r"(QUESTION_BANK\s*=\s*)(\[.*\])(\s*;?)", raw, re.S)
        if not m:
            raise SystemExit("could not parse questions.js for apply — NOTHING WAS WRITTEN")
        new_content = m.group(1) + json.dumps(bank, ensure_ascii=False) + m.group(3)
        tmp = Q_JS.with_suffix(".js.tmp")
        tmp.write_text(new_content, encoding="utf-8")
        tmp.replace(Q_JS)  # atomic
        with open(OUT / "contradicted_review.jsonl", "w", encoding="utf-8") as fh:
            for r in review:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
        print(f"applied supported: {applied} | contradicted (review only, NOT auto-applied): {len(review)}")
        return 0

    bank = load_bank()
    by_id = {q["id"]: q for q in bank}
    # skip qids already resolved in a previous pass (final.jsonl has a non-uncertain verdict)
    resolved = set()
    fin = OUT / "final.jsonl"
    if fin.exists():
        for line in open(fin, encoding="utf-8"):
            try:
                r = json.loads(line)
                if r.get("verdict") != "uncertain":
                    resolved.add(r["qid"])
            except Exception:
                pass
    todo = [by_id[i] for i in uncertain_qids() if i in by_id and by_id[i].get("usable") is not False
            and i not in resolved]
    k, n = (int(x) for x in args.shard.split("/"))
    todo = [q for q in todo if zlib.crc32(q["id"].encode()) % n == k]
    CHECK = Path(args.checkpoint)
    done = set()
    if CHECK.exists():
        for line in open(CHECK, encoding="utf-8"):
            try:
                done.add(json.loads(line)["qid"])
            except Exception:
                pass
    todo = [q for q in todo if q["id"] not in done]
    print(f"shard {k}/{n}: {len(todo)} uncertain to check", flush=True)

    if args.stats:
        return 0

    corpus = load_corpus()
    ok = err = 0
    t0 = time.time()
    with open(CHECK, "a", encoding="utf-8") as ck:
        for start in range(0, len(todo), args.batch):
            batch = todo[start:start + args.batch]
            prompt = build_prompt(batch, corpus)
            resp = call_api(prompt)
            if resp.startswith("__"):
                err += 1
                print(f"[batch {start//args.batch}] FAILED {resp}", flush=True)
                time.sleep(8)
                continue
            arr = parse(resp, [q["id"] for q in batch])
            if not arr:
                err += 1
                print(f"[batch {start//args.batch}] parse failed", flush=True)
                time.sleep(3)
                continue
            for v in arr:
                if isinstance(v, dict) and v.get("qid") and v.get("verdict"):
                    ck.write(json.dumps(v, ensure_ascii=False) + "\n")
            ck.flush()
            ok += 1
            print(f"[batch {start//args.batch}] +{len(batch)}Q ok={ok} err={err} {time.time()-t0:.0f}s", flush=True)
            time.sleep(1.0)
    print(f"SHARD DONE ok={ok} err={err}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

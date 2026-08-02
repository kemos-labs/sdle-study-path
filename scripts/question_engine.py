#!/usr/bin/env python3
"""question_engine.py — generate examiner-style MCQs from the official textbooks.

Design goals (user mandate):
  * Questions that separate students who UNDERSTAND from those who only memorized
    old recall questions — scenario-based, "best answer" traps, clinical reasoning.
  * Grounded in the official books: every question ships with a verbatim
    supporting passage (the "why") so it is verifiable, not invented.
  * Focus on the ~70% of the exam: endo + perio + prostho + restorative.
  * Batch generation: MANY questions per API call (never 1 per call).

Pipeline:
  1. Pick target topics + subtopics (blueprint-weighted).
  2. Retrieve the most fact-dense passages from the book corpus for each topic.
  3. Ask the model to write N exam-style MCQs from those passages (open-book,
     batched) — one JSON array per call.
  4. Validate each generated question (4 unique options, answer index valid,
     passage present, stem not junk) → staging file data/generated/engine_out/.
  5. NEVER auto-merge into the bank — human/AI review first (like the old
     agent's mistake of shipping unverified volume).

Usage:
  python3 scripts/question_engine.py --topics endo,perio --count 40 --batch 10
  python3 scripts/question_engine.py --review            # print staged questions
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORPUS = ROOT / "sdle-prep" / "data" / "raw" / "books" / "text"
OUT = ROOT / "sdle-prep" / "data" / "generated" / "engine_out"
OUT.mkdir(parents=True, exist_ok=True)

TOPIC_DIRS = {
    "endo": ["Endo"],
    "perio": ["perio"],
    "restorative": ["Resto", "Fixed", "Removable"],
    "oms": ["Oral surgary"],
    "ortho_pedo": ["ortho", "pedo"],
    "ethics": ["Ethics + infection control + local anasthesia"],
}

PROVIDERS = [
    {"name": "deepseek", "url": "https://api.deepseek.com/chat/completions",
     "key": "sk-ba41aeb17e7641c99cd24c4ee2e57098", "model": "deepseek-chat"},
    {"name": "zai", "url": "https://api.z.ai/api/paas/v4/chat/completions",
     "key": "4ea3822302844e2ca6837e1db7c85e55.IAd0YoFVPgKwYcCC", "model": "glm-4.5-flash"},
]

SYSTEM = """You are a senior dental board examiner who writes SDLE-style multiple-choice questions.
You are given textbook passages. Write questions that:
1. Test UNDERSTANDING, not recall of the passage words — use clinical scenarios,
   patient cases, "best first step", "most likely diagnosis", compare/contrast traps.
2. Have exactly 4 plausible options (ONE clearly best answer).
3. Are exam-realistic: a good student who studied gets it right; a student who only
   memorized old questions gets the trap options.
4. Cover the kind of high-yield facts that actually appear on the SDLE
   (endo/perio/prostho/resto are ~70% of the exam).
Reply with ONLY a JSON array (no markdown):
[{"q": "...", "options": ["A","B","C","D"], "answer": 0-3, "passage": "verbatim supporting passage from the textbook (short)", "why": "one-sentence clinical explanation"}, ...]
Each question must cite its supporting passage verbatim from the given text."""


def load_passages(topic: str) -> list[str]:
    out = []
    for d in TOPIC_DIRS.get(topic, []):
        dd = CORPUS / d
        if not dd.exists():
            continue
        for f in sorted(dd.glob("*.txt")):
            if "DECODED" in f.name:
                continue
            try:
                txt = f.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            if txt.count("(cid:") > 50:
                continue
            body = txt[5000:] if txt[:5000].count("\x03") > 50 else txt
            for i in range(0, len(body), 700):
                chunk = body[i:i + 700].strip()
                if len(chunk) > 120:
                    out.append(chunk)
    return out


def fact_dense(passages: list[str], k: int = 12) -> list[str]:
    """Score passages by fact-density heuristics (numbers, %%, 'is/are', clinical terms)."""
    score = []
    clinical = re.compile(r"\b(diagnos|treat|indicated|contraindicat|increased|decreased|risk|%|mg|mm|ml|pH|degree|C\b|F\b|first|most|common|rare|gold standard)\b", re.I)
    for p in passages:
        hits = len(clinical.findall(p))
        words = len(p.split())
        density = hits / max(1, words)
        score.append((density, len(p), p))
    score.sort(key=lambda x: (-x[0], -x[1]))
    return [p for _, _, p in score[:k]]


def call_api(provider, prompt: str, timeout: int = 240) -> str:
    body = json.dumps({
        "model": provider["model"],
        "messages": [{"role": "system", "content": SYSTEM},
                     {"role": "user", "content": prompt}],
        "max_tokens": 6000,
        "temperature": 0.7,
    }).encode()
    req = urllib.request.Request(provider["url"], data=body, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {provider['key']}",
    })
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                data = json.loads(resp.read().decode())
            msg = data.get("choices", [{}])[0].get("message", {})
            return (msg.get("content") or msg.get("reasoning_content") or "").strip()
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(12)
                continue
            if e.code in (500, 502, 503):
                time.sleep(5)
                continue
            return f"__HTTP__ {e.code}"
        except Exception as e:
            return f"__ERR__ {str(e)[:100]}"
    return "__HTTP__ rate_limited"


def parse_json(resp: str):
    """Extract the first balanced JSON array (forward scan, string/escape aware)."""
    t = re.sub(r"```(?:json)?", "", resp or "").strip()
    start = t.find("[")
    if start < 0:
        return None
    depth = 0
    in_str = False
    esc = False
    for i in range(start, len(t)):
        c = t[i]
        if in_str:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
                in_str = False
            continue
        if c == '"':
            in_str = True
        elif c == "[":
            depth += 1
        elif c == "]":
            depth -= 1
            if depth == 0:
                try:
                    return json.loads(t[start:i + 1])
                except Exception:
                    return None
    return None

def validate(q: dict) -> str | None:
    """Return error string if invalid, else None."""
    stem = (q.get("q") or "").strip()
    opts = q.get("options") or []
    ans = q.get("answer")
    passage = (q.get("passage") or "").strip()
    if len(stem) < 30:
        return "stem too short"
    if not isinstance(opts, list) or len(opts) != 4:
        return "need 4 options"
    if any(not o or len(str(o).strip()) < 2 for o in opts):
        return "empty option"
    if len(set(str(o).strip().lower() for o in opts)) < 4:
        return "duplicate options"
    if not isinstance(ans, int) or not (0 <= ans <= 3):
        return "bad answer index"
    if len(passage) < 40:
        return "missing passage"
    # the answer must appear supported by the passage (loose check: keyword overlap)
    opt_txt = str(opts[ans]).lower()
    pass_low = passage.lower()
    keyw = [w for w in re.findall(r"[a-z]{4,}", opt_txt) if w not in ("that", "with", "this", "from")]
    if keyw and not any(w in pass_low for w in keyw):
        return "answer not in passage"
    # passage must be VERBATIM from the corpus (honesty: no paraphrase citations)
    if not CORPUS_PASSAGES:
        build_corpus_passages()
    norm = re.sub(r"[^a-z0-9 ]+", " ", passage.lower())
    if len(norm.split()) >= 12 and norm not in CORPUS_PASSAGES:
        return "passage not verbatim (paraphrased)"
    return None


CORPUS_PASSAGES: set[str] = set()


def build_corpus_passages() -> None:
    """Index normalized ~700-char chunks so we can verify verbatim citations."""
    global CORPUS_PASSAGES
    if CORPUS_PASSAGES:
        return
    seen: set[str] = set()
    for d in TOPIC_DIRS.values():
        dd = CORPUS / d[0]
        if not dd.exists():
            continue
        for f in sorted(dd.glob("*.txt")):
            if "DECODED" in f.name:
                continue
            try:
                txt = f.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            if txt.count("(cid:") > 50:
                continue
            body = txt[5000:] if txt[:5000].count("\x03") > 50 else txt
            for i in range(0, len(body), 700):
                chunk = body[i:i + 700].strip()
                if len(chunk) > 120:
                    seen.add(re.sub(r"[^a-z0-9 ]+", " ", chunk.lower()))
    CORPUS_PASSAGES = seen


def norm_stem(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--topics", default="endo,perio,restorative")
    ap.add_argument("--count", type=int, default=40)
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--review", action="store_true")
    ap.add_argument("--out", default="engine_questions.jsonl")
    args = ap.parse_args()

    # load existing staged rows so re-runs append (never overwrite)
    staged = OUT / args.out
    existing = []
    if staged.exists():
        for line in staged.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                try:
                    existing.append(json.loads(line))
                except Exception:
                    pass
    seen_stems = {norm_stem(r["q"]["q"]) for r in existing}

    if args.review:
        p = OUT / args.out
        if not p.exists():
            print("no staged questions")
            return 0
        rows = [json.loads(l) for l in p.read_text().splitlines()]
        ok = [r for r in rows if r.get("valid") is True]
        print(f"staged: {len(rows)} | valid: {len(ok)}")
        for r in ok[:10]:
            print(f"  [{r['topic']}] {r['q']['q'][:90]}")
            print(f"      ans={r['q']['answer']} {r['q']['options'][r['q']['answer']][:60]}")
        return 0

    topics = args.topics.split(",")
    per_topic = max(1, args.count // len(topics))
    all_out = []
    pi = 0
    for topic in topics:
        passages = fact_dense(load_passages(topic))
        print(f"[{topic}] {len(passages)} fact-dense passages selected")
        for start in range(0, per_topic, args.batch):
            n = min(args.batch, per_topic - start)
            # give the model a rotating window of passages
            window = passages[(start // args.batch) * 4: (start // args.batch) * 4 + 8]
            if not window:
                window = passages[:8]
            ctx = "\n---\n".join(window)[:8000]
            prompt = (f"Write {n} exam-style MCQ questions for the SDLE from these "
                      f"textbook passages (topic: {topic}).\n\nPASSAGES:\n{ctx}")
            resp = ""
            for _ in range(3):
                prov = PROVIDERS[pi % len(PROVIDERS)]
                pi += 1
                resp = call_api(prov, prompt)
                if not resp.startswith("__"):
                    break
            if resp.startswith("__"):
                print(f"  [{topic}] provider failed: {resp[:60]}")
                time.sleep(8)
                continue
            arr = parse_json(resp)
            if not arr:
                print(f"  [{topic}] bad JSON — retrying later (skipping)")
                continue
            for item in arr:
                err = validate(item)
                ns = norm_stem(item.get("q"))
                if ns and ns in seen_stems:
                    err = err or "duplicate stem (seen)"
                if ns:
                    seen_stems.add(ns)
                all_out.append({
                    "topic": topic,
                    "q": item,
                    "valid": err is None,
                    "invalid_reason": err,
                    "provider": prov["name"],
                })
            nv = sum(1 for x in all_out if x.get("valid"))
            print(f"  [{topic}] batch → {len(arr)} generated, {nv} valid so far")
            time.sleep(1.5)

    # append new rows to the staging file (resumable)
    new_rows = all_out
    all_rows = existing + new_rows
    with staged.open("w", encoding="utf-8") as f:
        for r in all_rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    valid = [r for r in all_rows if r["valid"]]
    new_valid = sum(1 for r in new_rows if r["valid"])
    print(f"\n✅ wrote {staged} — total {len(all_rows)} ({len(new_rows)} new), valid {len(valid)} (+{new_valid})")
    print(f"valid by topic: { {t: sum(1 for r in valid if r['topic'] == t) for t in set(r['topic'] for r in valid)} }")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

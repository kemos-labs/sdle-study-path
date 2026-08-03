#!/usr/bin/env python3
"""verify_bank_batch.py — batched deep book-verification of the MCQ bank.

Per user mandate: MAXIMUM questions per API call (never 1 call per question).
Pipeline:
  1. Load usable MCQs from data/questions.js (priority topics first).
  2. Build a per-topic passage index from the canonical book .txt corpus
     (data/raw/books/text/), chunked into ~600-char passages.
  3. For each batch of questions, retrieve top relevant passages by keyword
     scoring and send ONE API call: passages + N questions → JSON verdicts.
  4. Verdict: supported (book passage backs the answer) / contradicted
     (book contradicts) / uncertain (no evidence found).
  5. Checkpoint after every batch (resumable). Staging output only — the
     merge into questions.js happens via --apply after human/AI review.

Usage:
  python3 scripts/verify_bank_batch.py --limit 200 --topics endo,perio --batch 20
  python3 scripts/verify_bank_batch.py --resume --batch 40          # continue
  python3 scripts/verify_bank_batch.py --stats                      # progress
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
Q_JS = ROOT / "sdle-prep" / "data" / "questions.js"
CORPUS = ROOT / "sdle-prep" / "data" / "raw" / "books" / "text"
OUT = ROOT / "sdle-prep" / "data" / "generated" / "bank_verification"
OUT.mkdir(parents=True, exist_ok=True)
CHECKPOINT = OUT / "verdicts.jsonl"

# Topic -> corpus folders / keywords
TOPIC_DIRS = {
    "endo": ["Endo"],
    "perio": ["perio"],
    "restorative": ["Resto", "Fixed", "Removable"],
    "oms": ["Oral surgary"],
    "ortho_pedo": ["ortho", "pedo"],
    "ethics": ["Ethics + infection control + local anasthesia"],
    "mixed": ["Resto", "Fixed", "Removable", "Endo", "perio", "Oral surgary", "ortho", "pedo", "Ethics + infection control + local anasthesia"],
}
PRIORITY = ["restorative", "endo", "perio"]

# ── working APIs (tested 2026-08-02) ────────────────────────────────
# kilo is unreliable on big batches (times out) — demoted to last resort.
PROVIDERS = [
    {"name": "deepseek", "url": "https://api.deepseek.com/chat/completions",
     "key": "sk-ba41aeb17e7641c99cd24c4ee2e57098",
     "model": "deepseek-chat"},
    {"name": "zai", "url": "https://api.z.ai/api/paas/v4/chat/completions",
     "key": "4ea3822302844e2ca6837e1db7c85e55.IAd0YoFVPgKwYcCC",
     "model": "glm-4.5-flash"},
    {"name": "kilo", "url": "https://api.kilo.ai/api/gateway/chat/completions",
     "key": "placeholder",
     "model": "kilo-auto/free"},
]

SYSTEM = """You are a dental board examiner verifying MCQ answer keys against official textbook evidence.
You are given: (1) textbook passages (may be from multiple books), (2) a list of exam questions, each with options and the bank's marked answer.

For EVERY question decide:
- supported: the marked answer is CORRECT (a passage supports it, or it is uncontroversial dental knowledge).
- contradicted: the marked answer is WRONG (a passage or solid dental knowledge contradicts it). If so, say which option is correct.
- uncertain: you cannot determine correctness from the passages or general knowledge.

Use the passages as PRIMARY evidence. Do not force "supported" — it is better to say uncertain than to guess.
Reply with ONLY a valid JSON array, one object per question, in order:
[{"qid": "...", "verdict": "supported|contradicted|uncertain", "correct_option": 0-3 or null, "passage": "the exact supporting/contradicting passage (verbatim, short)", "reason": "one sentence"}]
No markdown, no commentary."""


def load_questions() -> list[dict]:
    raw = Q_JS.read_text(encoding="utf-8")
    m = re.search(r"QUESTION_BANK\s*=\s*(\[.*\])", raw, re.S)
    if not m:
        raise SystemExit("could not parse questions.js")
    return json.loads(m.group(1))


def load_corpus() -> dict[str, list[str]]:
    """topic -> list of clean passages."""
    idx = {}
    for topic, dirs in TOPIC_DIRS.items():
        passages = []
        for d in dirs:
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
                # skip junk: cid-garbage / shifted front matter (first 5k chars)
                if txt.count("(cid:") > 50:
                    continue
                body = txt[5000:] if txt[:5000].count("\x03") > 50 else txt
                # chunk
                for i in range(0, len(body), 600):
                    chunk = body[i:i + 600]
                    if len(chunk.strip()) < 60:
                        continue
                    passages.append(chunk)
        idx[topic] = passages
    return idx


def keywords(q: dict) -> list[str]:
    text = " ".join([q.get("q", ""), *(q.get("options") or []), q.get("explanation", "")])
    words = re.findall(r"[A-Za-z][A-Za-z\-]{3,}", text.lower())
    stop = {"which", "following", "what", "with", "that", "this", "from", "have", "would", "should",
            "patient", "patient's", "treatment", "correct", "answer", "best", "most", "about",
            "their", "there", "these", "those", "because", "during", "after", "before", "between",
            "when", "where", "than", "then", "they", "them", "into", "over", "under", "used", "use"}
    return [w for w in words if w not in stop and len(w) > 3][:14]


def retrieve(passages: list[str], kws: list[str], k: int = 6) -> str:
    """Return top-k passages by keyword overlap (BM25-ish), joined."""
    scored = []
    for p in passages:
        low = p.lower()
        s = sum(1 for kw in kws if kw in low)
        if s == 0:
            continue
        scored.append((s, p))
    scored.sort(key=lambda x: -x[0])
    top = [p for _, p in scored[:k]]
    return "\n---\n".join(top)


def call_api(provider, prompt: str, timeout: int = 90) -> str:
    body = json.dumps({
        "model": provider["model"],
        "messages": [{"role": "system", "content": SYSTEM},
                     {"role": "user", "content": prompt}],
        "max_tokens": 8000,
        "temperature": 0.1,
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
                time.sleep(10 * (attempt + 1))
                continue
            if e.code in (500, 502, 503):
                time.sleep(5)
                continue
            return f"__HTTP__ {e.code}"
        except Exception as e:
            return f"__ERR__ {str(e)[:120]}"
    return "__HTTP__ rate_limited"


def parse_verdicts(resp: str, qids: list[str]) -> list[dict]:
    """Extract JSON array robustly (handles ```json fences, trailing text, truncation)."""
    # strip fences
    t = re.sub(r"```(?:json)?", "", resp).strip()
    start = t.find("[")
    if start < 0:
        return [{"qid": q, "verdict": "error", "reason": resp[:120]} for q in qids]
    # find the balanced ']' (forward scan, string/escape aware)
    end = -1
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
                end = i
                break
    if end < 0:
        return [{"qid": q, "verdict": "error", "reason": "no balanced json"} for q in qids]
    try:
        arr = json.loads(t[start:end + 1])
    except Exception:
        # fallback: try first [ ... ]
        m = re.search(r"\[.*?\]", t, re.S)
        if not m:
            return [{"qid": q, "verdict": "error", "reason": "bad json"} for q in qids]
        try:
            arr = json.loads(m.group(0))
        except Exception:
            return [{"qid": q, "verdict": "error", "reason": "bad json"} for q in qids]
    out = []
    for i, q in enumerate(qids):
        v = arr[i] if i < len(arr) else {}
        out.append({
            "qid": q,
            "verdict": v.get("verdict", "error"),
            "correct_option": v.get("correct_option"),
            "passage": (v.get("passage") or "")[:400],
            "reason": (v.get("reason") or "")[:200],
        })
    return out


def _lock() -> None:
    import fcntl
    LOCK = ROOT / "sdle-prep" / "data" / "generated" / "bank_verification" / ".verify.lock"
    LOCK.parent.mkdir(parents=True, exist_ok=True)
    fd = open(LOCK, "w")
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        print("another verifier holds the lock — exiting")
        raise SystemExit(2)
    global _LOCK_FD
    _LOCK_FD = fd


def done_ids() -> set:
    if not CHECKPOINT.exists():
        return set()
    ids = set()
    for line in CHECKPOINT.read_text(encoding="utf-8").splitlines():
        try:
            ids.add(json.loads(line)["qid"])
        except Exception:
            pass
    return ids


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--topics", default="")
    ap.add_argument("--batch", type=int, default=25)
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--stats", action="store_true")
    args = ap.parse_args()

    if args.stats:
        d = done_ids()
        print(f"verified so far: {len(d)}")
        return 0

    bank = load_questions()
    usable = [q for q in bank if q.get("usable") is not False]
    topics = args.topics.split(",") if args.topics else PRIORITY
    # order: priority topics first, then others
    ordered = sorted(usable, key=lambda q: (q["topic"] not in PRIORITY, PRIORITY.index(q["topic"]) if q["topic"] in PRIORITY else 9))
    if topics:
        ordered = [q for q in ordered if q["topic"] in topics]
    if args.limit:
        ordered = ordered[:args.limit]

    _lock()
    done = done_ids() if args.resume else set()
    todo = [q for q in ordered if q["id"] not in done]
    print(f"bank usable: {len(usable)} | target: {len(ordered)} | already: {len(done)} | todo: {len(todo)}")

    corpus = load_corpus()
    print(f"corpus passages: { {k: len(v) for k, v in corpus.items()} }")

    # round-robin providers; on error retry with the next provider
    pi = 0
    ok = err = 0
    t0 = time.time()
    with open(CHECKPOINT, "a", encoding="utf-8") as ckpt:
        for start in range(0, len(todo), args.batch):
            batch = todo[start:start + args.batch]
            topic = batch[0]["topic"]
            passages = corpus.get(topic) or corpus["mixed"]
            # per-question retrieval
            parts = []
            for q in batch:
                kws = keywords(q)
                ctx = retrieve(passages, kws)
                opts = "\n".join(f"{i}. {o}" for i, o in enumerate(q.get("options", [])))
                ans_txt = q["options"][q["answer"]] if q["answer"] is not None and q["answer"] < len(q.get("options", [])) else "?"
                parts.append(
                    f"QID:{q['id']}\nQ: {q['q']}\nOPTIONS:\n{opts}\nMARKED ANSWER: {q['answer']} ({ans_txt})\nPASSAGES:\n{ctx[:2400]}\n=====")
            prompt = "\n".join(parts)
            # try providers in order until one works
            resp = ""
            for _ in range(len(PROVIDERS)):
                provider = PROVIDERS[pi % len(PROVIDERS)]
                pi += 1
                resp = call_api(provider, prompt)
                if not resp.startswith("__"):
                    break
                print(f"  [{provider['name']}] failed {resp[:40]} — trying next provider")
            if resp.startswith("__"):
                err += 1
                print(f"[batch {start // args.batch}] ALL PROVIDERS FAILED {resp[:60]}")
                time.sleep(8)
                continue
            verdicts = parse_verdicts(resp, [q["id"] for q in batch])
            nerr = sum(1 for v in verdicts if v["verdict"] == "error")
            if nerr == len(batch):
                err += 1
                print(f"[batch {start // args.batch}] parse failed: {resp[:100]!r}")
                time.sleep(3)
                continue
            for v in verdicts:
                if v["verdict"] != "error":  # don't checkpoint errors → they retry
                    ckpt.write(json.dumps(v, ensure_ascii=False) + "\n")
            ckpt.flush()
            vc = {}
            for v in verdicts:
                vc[v["verdict"]] = vc.get(v["verdict"], 0) + 1
            ok += 1
            print(f"[batch {start // args.batch}] {provider['name']} {len(batch)}Q → {json.dumps(vc)} | total {len(done_ids())} | {time.time() - t0:.0f}s")
            time.sleep(1.5)  # polite rate limit
    print(f"DONE. batches ok={ok} err={err} | total verdicts: {len(done_ids())}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

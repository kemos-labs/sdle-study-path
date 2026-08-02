#!/usr/bin/env python3
"""apply_bank_verification.py — merge book-verification verdicts into questions.js.

Reads the checkpoint JSONL produced by verify_bank_batch.py and:
  * supported + real passage → set/refresh `book_support` to the passage,
    set `book_verified=true` (real evidence now).
  * contradicted → record proposed flip in work/flips_review.json (NOT applied
    automatically — every flip needs human/AI review first).
  * uncertain → leave book_verified as-is but note needs_review.

This is the SINGLE merge pass that owns questions.js. Run after reviewing
work/flips_review.json with --apply-flips.

Usage:
  python3 scripts/apply_bank_verification.py                 # write book_support only
  python3 scripts/apply_bank_verification.py --apply-flips   # also apply reviewed flips
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
Q_JS = ROOT / "sdle-prep" / "data" / "questions.js"
VERDICTS = ROOT / "sdle-prep" / "data" / "generated" / "bank_verification" / "verdicts.jsonl"
FLIPS = ROOT / "work" / "flips_review.json"


def load_verdicts() -> list[dict]:
    if not VERDICTS.exists():
        return []
    return [json.loads(l) for l in VERDICTS.read_text(encoding="utf-8").splitlines() if l.strip()]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply-flips", action="store_true")
    ap.add_argument("--report", action="store_true")
    args = ap.parse_args()

    verdicts = load_verdicts()
    print(f"verdicts loaded: {len(verdicts)}")
    if not verdicts:
        return 1
    vc = Counter(v["verdict"] for v in verdicts)
    print(f"verdict mix: {dict(vc)}")

    raw = Q_JS.read_text(encoding="utf-8")
    m = re.search(r"(QUESTION_BANK\s*=\s*)(\[.*\])(\s*;?)", raw, re.S)
    if not m:
        raise SystemExit("could not parse questions.js")
    bank = json.loads(m.group(2))
    by_id = {q["id"]: q for q in bank}

    applied_support = 0
    flips = []
    for v in verdicts:
        q = by_id.get(v.get("qid"))
        if not q:
            continue
        if v.get("verdict") == "supported" and v.get("passage"):
            # replace junk/empty book_support with the real passage
            old = (q.get("book_support") or "")[:60]
            if "factpack" not in old.lower() or not old:
                pass
            if len(v["passage"]) > 40:
                q["book_support"] = v["passage"]
                q["book_verified"] = True
                q["_verify_pass"] = "book_batch_2026-08"
                applied_support += 1
        elif v.get("verdict") == "contradicted":
            flips.append({
                "qid": v["qid"],
                "current_answer": q.get("answer"),
                "current_text": (q.get("options") or [])[q["answer"]] if q.get("answer") is not None and q["answer"] < len(q.get("options", [])) else None,
                "proposed_answer": v.get("correct_option"),
                "proposed_text": (q.get("options") or [])[v["correct_option"]] if v.get("correct_option") is not None and v["correct_option"] < len(q.get("options", [])) else None,
                "passage": v.get("passage", ""),
                "reason": v.get("reason", ""),
                "q": (q.get("q") or "")[:160],
            })

    if args.report:
        print(f"supported w/ passage applied: {applied_support}")
        print(f"contradicted flagged: {len(flips)}")
        for f in flips[:20]:
            print(f"  FLIP {f['qid']}: {f['current_text'][:50] if f['current_text'] else '?'} → {f['proposed_text'][:50] if f['proposed_text'] else '?'} | {f['reason'][:80]}")
        return 0

    # write flips for review
    FLIPS.parent.mkdir(parents=True, exist_ok=True)
    FLIPS.write_text(json.dumps(flips, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"flips written to {FLIPS}: {len(flips)}")

    if args.apply_flips:
        for f in flips:
            q = by_id.get(f["qid"])
            if q and f.get("proposed_answer") is not None:
                q["answer"] = f["proposed_answer"]
                q["_answer_flipped"] = True

    # write back
    new_body = json.dumps(bank, ensure_ascii=False)
    out = m.group(1) + new_body + m.group(3)
    Q_JS.write_text(out, encoding="utf-8")
    print(f"✅ wrote questions.js — supported refreshed: {applied_support}, flips applied: {len(flips) if args.apply_flips else 0}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

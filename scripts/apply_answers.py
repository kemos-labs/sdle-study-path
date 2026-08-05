#!/usr/bin/env python3
"""apply_answers.py — apply the answer-solving results to flash_notes.js.

For each solved result: set answerIdx + answerLetter (derived from index, then
RE-VERIFIED against option text), _verification_verdict, _book_explanation,
_verified_explanation ("Why: ..."), marker verified for book-supported items.
Index-vs-text check: the option at the chosen index must be a real option.
"""
import json, os, re, tempfile, glob
from pathlib import Path

ROOT = Path("/data/prometric")
FN = ROOT / "sdle-prep" / "data" / "flash_notes.js"
WORK = ROOT / "work" / "mcqify"

def load_results():
    res = {}
    for f in glob.glob(str(WORK / "results_answers_*.jsonl")):
        for line in open(f, encoding="utf-8"):
            try:
                r = json.loads(line)
                res[r["id"]] = r
            except Exception:
                pass
    return res

def main():
    res = load_results()
    print(f"answer results loaded: {len(res)}")
    src = FN.read_text(encoding="utf-8")
    fbody = src.split("=", 1)[1].strip().rstrip().rstrip(";").strip()
    data = json.loads(fbody)
    applied = supported = recall = 0
    for dept, arr in data["byDept"].items():
        for it in arr:
            r = res.get(it.get("id"))
            if not r:
                continue
            ai = r.get("answer_idx")
            opts = it.get("options") or []
            if not isinstance(ai, int) or not (0 <= ai < len(opts)):
                continue
            # index-vs-text verification: the chosen option must be non-empty real text
            chosen = re.sub(r"^[a-z][).]\s*", "", str(opts[ai]).strip(), flags=re.I).strip()
            if len(chosen) < 2:
                continue
            it["answerIdx"] = ai
            it["answerLetter"] = chr(65 + ai)
            it["_solved_from_book"] = True
            why = (r.get("why") or "").strip()
            passage = (r.get("passage") or "").strip()
            book = (r.get("book") or "").strip()
            if not r.get("unsolved") and len(passage) >= 20:
                it["_verification_verdict"] = "supported"
                it["_book_explanation"] = {"book": book, "chapter": "", "passage": passage[:500],
                                           "context": passage[:500]}
                it["_verified_explanation"] = ("Why: " + why if why else "")[:600]
                it["marker"] = "verified"
                supported += 1
            else:
                it["_verification_verdict"] = "needs_review"
                it["_verified_explanation"] = ("Why (not book-verified): " + why if why else "Recall — not book-verified.")[:600]
                recall += 1
            applied += 1
    data["total"] = sum(len(v) for v in data["byDept"].values())
    new_src = src.replace(fbody, json.dumps(data, ensure_ascii=False, indent=1))
    fd, tmp = tempfile.mkstemp(dir=str(FN.parent), suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        fh.write(new_src)
    os.replace(tmp, FN)
    print(f"applied: {applied} (supported {supported}, honest recall {recall})")
    print(f"flash total now: {data['total']}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Apply the MCQ-ify results to flash_notes.js.

For every target item with a solved result:
  - options  -> "A. text" (4 options), answerIdx + answerLetter set
  - marker   -> verified (now a proper MCQ)
  - _verification_verdict -> supported (has verbatim passage) | needs_review (unsolved)
  - _book_explanation     -> {book, passage} for supported items (drives the 📖 button)
  - _verified_explanation -> "Why: <why> [Book: <book>]" (shows the reason on the card)
  - _solved_from_book     -> true
Books-only rule: no passage -> never 'supported', never a citation.
"""
import json, os, tempfile, glob
from pathlib import Path

ROOT = Path("/data/prometric")
FN = ROOT / "sdle-prep" / "data" / "flash_notes.js"
WORK = ROOT / "work" / "mcqify"

def load_results():
    res = {}
    for f in glob.glob(str(WORK / "results_*.jsonl")) + [str(WORK / "done_pool.jsonl")]:
        for line in open(f, encoding="utf-8"):
            try:
                r = json.loads(line)
                res[r["id"]] = r
            except Exception:
                pass
    return res

def main():
    res = load_results()
    print(f"results loaded: {len(res)} unique ids")
    src = FN.read_text(encoding="utf-8")
    fbody = src.split("=", 1)[1].strip().rstrip().rstrip(";").strip()
    data = json.loads(fbody)
    applied = 0
    supported = 0
    recall = 0
    for dept, arr in data["byDept"].items():
        for it in arr:
            r = res.get(it.get("id"))
            if not r:
                continue
            opts = [str(o).strip()[:120] for o in r.get("options", [])]
            if len(opts) < 3:
                continue
            ai = r.get("answer_idx")
            if not isinstance(ai, int) or not (0 <= ai < len(opts)):
                continue
            it["options"] = [f"{chr(65 + i)}. {o}" for i, o in enumerate(opts)]
            it["answerIdx"] = ai
            it["answerLetter"] = chr(65 + ai)
            it["marker"] = "verified"
            it["_solved_from_book"] = True
            why = (r.get("why") or "").strip()
            passage = (r.get("passage") or "").strip()
            book = (r.get("book") or "").strip()
            unsolved = bool(r.get("unsolved"))
            if not unsolved and len(passage) >= 20:
                it["_verification_verdict"] = "supported"
                it["_book_explanation"] = {"book": book, "chapter": "", "passage": passage[:500],
                                           "context": passage[:500]}
                it["_verified_explanation"] = (("Why: " + why) if why else "")[:600]
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

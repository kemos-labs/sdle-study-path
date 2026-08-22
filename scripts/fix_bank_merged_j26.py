#!/usr/bin/env python3
"""
fix_bank_merged_j26.py — repair the 5 merged-option monsters in the bank.

Source docx merged consecutive questions' option blocks (work/parsed_new_mcqs.json
shows the same glued lists). Four items keep their clean 4-option prefix — each
bank answer index was re-verified against the option TEXT after trimming:

  j26_0116 -> [Complex odontoma, Compound odontoma, Cementoblastoma,
               Ameloblastic fibro-odontoma]              ans=1 Compound odontoma
  j26_0118 -> [MIH, AI, Dental caries, DI]             ans=0 MIH
  j26_0119 -> [Flap debridement+Bone graft+CG, SRP+re-evaluate,
               Extract incisors, Non-surgical endo]    ans=1 SRP + re-evaluate
  j26_0134 -> [Cervical HG, Reverse-pull HG, High-pull HG, Twin block]
                                                       ans=2 High-pull headgear

j26_0120 has duplicated/junk option lines even in the source parse -> demoted.

Usage: python3 scripts/fix_bank_merged_j26.py [--apply]
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
Q_JS = ROOT / "data" / "questions.js"

TRIM = {
    "j26_0116": ["Complex odontoma", "Compound odontoma", "Cementoblastoma", "Ameloblastic fibro-odontoma"],
    "j26_0118": ["MIH", "AI", "Dental caries", "DI"],
    "j26_0119": [
        "Flap debridement + bone graft + connective tissue graft",
        "Scaling and root planing + re-evaluate in 6 weeks",
        "Extract all incisors",
        "Non-surgical endodontics for the incisor",
    ],
    "j26_0134": ["Cervical headgear", "Reverse pull headgear", "High-pull headgear", "Twin block"],
}
EXPECT_ANS = {"j26_0116": 1, "j26_0118": 0, "j26_0119": 1, "j26_0134": 2}

DEMOTE = {
    "j26_0120": "source option block is merged junk ('crown' duplicated, scenario sentences inside options); no clean option set recoverable from the source docx",
}


def load() -> list:
    m = re.search(r"QUESTION_BANK\s*=\s*(\[.*\]);?\s*$", Q_JS.read_text(encoding="utf-8"), re.DOTALL)
    return json.loads(m.group(1))


def save(bank: list) -> None:
    bak = Q_JS.with_suffix(".js.bak-merged")
    bak.write_text(Q_JS.read_text(encoding="utf-8"), encoding="utf-8")
    Q_JS.write_text("QUESTION_BANK = " + json.dumps(bank, ensure_ascii=False, indent=1) + ";\n", encoding="utf-8")
    print(f"backup written: {bak.name}")


def main() -> int:
    apply = "--apply" in sys.argv
    bank = load()
    by_id = {q.get("id"): q for q in bank}
    ok = True

    for qid, opts in TRIM.items():
        q = by_id.get(qid)
        if not q:
            print(f"MISSING {qid}"); ok = False; continue
        ans = q.get("answer")
        if ans != EXPECT_ANS[qid]:
            print(f"ABORT {qid}: answer {ans} != expected {EXPECT_ANS[qid]}"); ok = False; continue
        correct_text = opts[ans]
        print(f"TRIM {qid}: ans={ans} -> {correct_text!r}")
        if apply:
            q["options"] = opts
            q["_merged_options_repaired"] = True

    for qid, reason in DEMOTE.items():
        q = by_id.get(qid)
        if not q:
            print(f"MISSING {qid}"); ok = False; continue
        if q.get("usable") is False:
            continue
        print(f"DEMOTE {qid}: {reason[:70]}")
        if apply:
            q["usable"] = False
            q["exclude_reason"] = reason

    if not ok:
        return 1
    if not apply:
        print("DRY RUN \u2014 rerun with --apply.")
        return 0
    save(bank)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

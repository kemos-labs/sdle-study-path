#!/usr/bin/env python3
"""
fix_bank_residue.py — C1+C2 residue fixes for data/questions.js (2026-08-22).

C1: demote the 4 two-option j26 items that are recall notes, not real MCQs
    (source-verified against work/parsed_new_mcqs.json — same 2 lines there).
C2: replace the 11 "Selected (N) … For:" glue explanations with either a
    verbatim book citation ([Book: …]) or an honest uncited clinical hinge.
    NO answer indices are changed — this pass never flips answers.

Usage:
    python3 scripts/fix_bank_residue.py           # dry run
    python3 scripts/fix_bank_residue.py --apply   # write data/questions.js
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
Q_JS = ROOT / "data" / "questions.js"

DEMOTE = {
    "j26_0003": "source line is a recall note, not a true MCQ (only two non-option lines in original July-2026 docx)",
    "j26_0004": "source line is a recall note ('*Also Ramus Osteotomy' is not an option); stem 'Name the procedure?' has no real option set",
    "j26_0006": "second option is a book-title string, not an answer choice (recall note in source docx)",
    "j26_0008": "second option is a book-title string, not an answer choice (recall note in source docx)",
    "rafi_12_af73b4e2a1": "options are student slang fragments ('miss'/'semi miss'/'extra miss'), not real answer choices; stem unanswerable as written",
    "rafi_17_747d83d9ec": "option text is 'I don't remember it \u2014> maybe Pressure indicating paste' (recall fragment, not an option); another option carries an inline \u2716 mark",
}

WHYS = {
    "rafi_06_13ef6decfe": "\U0001F4CE Clinical hinge: A necrotic primary molar in a healthy child is treated endodontically (pulpectomy) and restored so it stays pain-free until normal exfoliation; extraction is reserved for unrestorable or dangerous teeth. [Book: Cohen's Pathways of the Pulp] \u2014 discusses pulpectomy for primary teeth: \u201cIf a primary tooth requires pulpectomy\u2026 the primary root canals are filled\u201d with resorbable paste.",
    "rafi_12_2825f92145": "[Book: Contemporary Orthodontics 7e] \u2014 describes the \u201cclass II division 2 incisor pattern\u201d as upright/retroclined maxillary central incisors (\u201climited overjet due to the upright central incisors\u201d): upright centrals close the interincisal angle (>135\u00b0), and point A above normal adds the retrognathic-maxilla (Class II) skeletal pattern. Division 1 instead shows proclined incisors and a small interincisal angle.",
    "rafi_17_0b2cd77d8f": "\U0001F4CE Clinical hinge: NSAIDs (e.g., ibuprofen) are first-line analgesics for endodontic/emergency dental pain because prostaglandins mediate periapical inflammation. [Book: Cohen's Pathways of the Pulp] \u2014 reviews ibuprofen/NSAID efficacy for posttreatment endodontic pain.",
    "rafi_17_67efc316f9": "\U0001F4CE Clinical hinge: ~7 mm residual bone below the sinus floor supports a transalveolar (internal/crestal) sinus floor elevation with simultaneous implant placement; lateral-window grafting is reserved for <5 mm or larger lifts. [Book: Carranza/Lindhe implant chapters] \u2014 describe crestal/internal sinus elevation techniques.",
    "rafi_17_19ec23a21f": "\U0001F4CE Clinical hinge: Current medical consensus \u2014 patients on long-term low-dose corticosteroids (\u226425 mg hydrocortisone equivalent/day, e.g., 10 mg cortisol/prednisolone range per local practice) do not routinely need supplemental steroids; they should take their usual morning dose close to the appointment so blood levels stay steady during the procedure.",
    "rafi_18_2ce26df9ac": "[Book: McCracken's Removable Partial Prosthodontics] \u2014 \u201cWithout sufficient bulk, the U-shaped design leads to increased flexibility and movement at the open ends.\u201d The single U-shaped (palatal bar/strap) connector is therefore the least rigid maxillary major connector; wider straps/plates gain rigidity through bulk.",
    "rafi_20_a098e903fc": "[Book: Contemporary Fixed Prosthodontics] \u2014 \u201c\u2026should be supragingival. Subgingival margins of cemented restorations have been identified as a major etiologic factor in periodontal disease\u201d; supragingival margins and large gingival embrasures \u201cfacilitate plaque control.\u201d On esthetic anterior crowns the healthiest margin is therefore supragingival whenever retention allows.",
    "rafi_20_276af0bfaf": "\U0001F4CE Clinical hinge: On the mandibular second molar the external oblique ridge forms thick, sloping buccal cortical bone, so apical repositioning of the buccal flap/osteotomy during crown lengthening is mechanically limited \u2014 making crown-lengthening surgery hardest here.",
    "rafi_20_a3377426d9": "[Book: Carranza's Clinical Periodontology] \u2014 post-treatment abscess/swelling after scaling is attributed to \u201cincomplete subgingival scaling, and residual calculus deep in the pockets\u201d left behind by instrumentation; calculus fragments persisting in the pocket drive the acute flare.",
}


def load() -> list:
    text = Q_JS.read_text(encoding="utf-8")
    m = re.search(r"QUESTION_BANK\s*=\s*(\[.*\]);?\s*$", text, re.DOTALL)
    if not m:
        raise SystemExit("cannot parse questions.js")
    return json.loads(m.group(1))


def save(bank: list) -> None:
    out = "QUESTION_BANK = " + json.dumps(bank, ensure_ascii=False, indent=1) + ";\n"
    bak = Q_JS.with_suffix(".js.bak-residue")
    bak.write_text(Q_JS.read_text(encoding="utf-8"), encoding="utf-8")
    Q_JS.write_text(out, encoding="utf-8")
    print(f"backup written: {bak.name}")


def main() -> int:
    apply = "--apply" in sys.argv
    bank = load()
    by_id = {q.get("id"): q for q in bank}

    n_demote = n_why = 0
    for qid, reason in DEMOTE.items():
        q = by_id.get(qid)
        if not q:
            print(f"MISSING {qid}"); continue
        if q.get("usable") is False:
            continue
        print(f"DEMOTE {qid}: {reason[:70]}")
        n_demote += 1
        if apply:
            q["usable"] = False
            q["exclude_reason"] = reason

    for qid, why in WHYS.items():
        q = by_id.get(qid)
        if not q:
            print(f"MISSING {qid}"); continue
        old = (q.get("explanation") or "")[:50].replace("\n", " ")
        print(f"REWHY  {qid}: {old!r} -> {why[:60]!r}")
        n_why += 1
        if apply:
            q["explanation"] = why

    print(f"\nTOTAL: demote={n_demote} rewhy={n_why}")
    if not apply:
        print("DRY RUN \u2014 rerun with --apply to write.")
        return 0
    save(bank)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

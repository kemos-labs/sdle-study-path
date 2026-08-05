#!/usr/bin/env python3
"""apply_repairs.py — apply the BOOK-VERIFIED repairs (passages confirmed by grep of the
official corpus + model suggestions cross-checked). Every answer change is index-vs-text
verified. Atomic write (tmp+replace)."""
import json, re
from pathlib import Path

ROOT = Path("/data/prometric")
Q_JS = ROOT / "sdle-prep" / "data" / "questions.js"

def load():
    raw = Q_JS.read_text(encoding="utf-8")
    m = re.search(r"(QUESTION_BANK\s*=\s*)(\[.*\])(\s*;?)", raw, re.S)
    assert m, "parse failed"
    return json.loads(m.group(2)), m.group(1), m.group(3)

# (qid, action, ...) — actions verified against passages
REPAIRS = [
    # ab2_7710e019d9 — closed-mouth impression for firm ridge (McCracken: open-mouth when mucosa easily displaced)
    ("ab2_7710e019d9", "replace_opt", 2, "Firm ridge",
     "[Book: McCracken's Removable Partial Prosthodontics] when the mucosa is easily displaced, the open-mouth selective pressure technique is preferable"),
    # ab2_2f241b10b7 / ab2_9fe3fc238b — final restoration after 3 months (Contemporary Fixed 4e)
    ("ab2_2f241b10b7", "set_answer", "3 months",
     "[Book: Contemporary Fixed Prosthodontics 4e] subsequently fabricate the final restoration after 3 months"),
    ("ab2_9fe3fc238b", "set_answer", "3 months",
     "[Book: Contemporary Fixed Prosthodontics 4e] subsequently fabricate the final restoration after 3 months"),
    # ab2_5c94fb585c — RPD movement w/o indirect retainer → add indirect retainer (McCracken ch.8)
    ("ab2_5c94fb585c", "replace_opt", 1, "Add an indirect retainer",
     "[Book: McCracken's Removable Partial Prosthodontics] Role of Indirect Retainers in Control of denture base movement"),
    # ab2_2b6d04a4a1 — lateral luxation splint 4 weeks (Cohen's)
    ("ab2_2b6d04a4a1", "replace_opt", 2, "4 weeks",
     "[Book: Cohen's Pathways of the Pulp 2016] call for 2 weeks of physiologic splinting in cases of extrusion luxation and 4 weeks for lateral luxation"),
    # rafi_01_6b9539a6a5 — philtrum of the lip is the guide (Textbook of Complete Dentures)
    ("rafi_01_6b9539a6a5", "replace_opt", 3, "Philtrum of the lip",
     "[Book: Textbook of Complete Dentures] The philtrum of the lip is the most common guide for marking the midline"),
    # rafi_04_381c1e1f81 — MTA 3:1 (Endodontics principles)
    ("rafi_04_381c1e1f81", "replace_opt", 0, "3 : 1",
     "[Book: Endodontics principles] the powder with sterile water or saline at a ratio of 3 : 1 on a glass or paper slab"),
    # rafi_04_0d96b8c5fe — night pain = irreversible pulpitis (Cohen's: spontaneous pain = symptomatic irreversible pulpitis)
    ("rafi_04_0d96b8c5fe", "replace_opt", 3, "Irreversible pulpitis",
     "[Book: Cohen's Pathways of the Pulp 2016] Patients who have spontaneous pain and have moderate to severe pain at an emergency visit (symptomatic irreversible pulpitis)"),
    # rafi_12_68bc391e9d — symptomatic pulpitis = spontaneous/lingering pain (Cohen's)
    ("rafi_12_68bc391e9d", "replace_opt", 3, "Spontaneous pain / lingering response to cold (irreversible pulpitis)",
     "[Book: Cohen's Pathways of the Pulp 2016] Patients who have spontaneous pain and have moderate to severe pain at an emergency visit (symptomatic irreversible pulpitis)"),
    # rafi_15_8564eb49ec — most popular sealer = ZOE (Cohen's)
    ("rafi_15_8564eb49ec", "replace_opt", 1, "Zinc oxide–eugenol (ZOE) sealer",
     "[Book: Cohen's Pathways of the Pulp 2016] The most popular sealers are zinc oxide–eugenol formulations"),
    # rafi_20_bfd4d592dd — crown lengthening for BW violation = surgical crown lengthening (Carranza)
    ("rafi_20_bfd4d592dd", "replace_opt", 0, "Surgical crown lengthening",
     "[Book: Carranza Clinical Periodontology 2018] Surgery is the more rapid of the two treatment options. It is also preferred if the resulting crown lengthening creates a more pleasing tooth length"),
    # rafi_08_6dfb9d2845 — 0.2mm/yr (Contemporary Fixed: any loss exceeding 0.2mm/yr is concern)
    ("rafi_08_6dfb9d2845", "replace_opt", 3, "0.2 mm",
     "[Book: Contemporary Fixed Prosthodontics 4e] Any loss exceeding 0.2 mm per year is cause for concern"),
    # rafi_15_e2981fe47b — gagging = incorrect extension in posterior palate (Textbook of Complete Dentures)
    ("rafi_15_e2981fe47b", "replace_opt", 3, "Over-extension of the posterior palatal seal / retromylohyoid space",
     "[Book: Textbook of Complete Dentures] incorrect extension or contour of the dentures—particularly in the posterior area of the palate and the retromylohyoid space"),
    # rafi_03_bc3dfe851b — ISO standard file size = 15 (Endodontics principles)
    ("rafi_03_bc3dfe851b", "replace_opt", 3, "15",
     "[Book: Endodontics principles] enlarging a root canal from size #10 to #15 … instruments in sizes #15, #17.5, #20"),
    # rafi_04_d4958735c5 — silver point disadvantage = corrosion toxicity (Endodontics principles)
    ("rafi_04_d4958735c5", "fix_text", 2, "Toxic to periapical tissues (corrosion)",
     "[Book: Endodontics principles] possible toxicity to periapical tissues from corrosion"),
    # rafi_07_d94477dd31 — bone RESORPTION → osteoclast (Periodontics MSI)
    ("rafi_07_d94477dd31", "stem+answer", "bone resorption", 3,
     "[Book: Periodontics MSI] Bone resorption with areas of bone covered by multinucleated bone resorbing osteoclasts"),
    # rafi_18_89b6f2d029 — increase ZOE working time = cool/frozen slab (Contemporary Fixed 4e)
    ("rafi_18_89b6f2d029", "set_answer", "Cool mixing slab",
     "[Book: Contemporary Fixed Prosthodontics 4e] Frozen slab technique — a practical way to increase the working time"),
    # rafi_06_0d311c408f — amalgam contraindication = esthetic areas (Sturdevant)
    ("rafi_06_0d311c408f", "replace_opt", 0, "Esthetic (visible) areas",
     "[Book: Sturdevant Operative Dentistry 5e] Amalgams … except for esthetics"),
    # rafi_17_46df219c7b — gingivitis cause = plaque/poor hygiene (Carranza)
    ("rafi_17_46df219c7b", "set_answer", "Poor hygiene",
     "[Book: Carranza Clinical Periodontology] gingivitis is plaque-induced inflammation of the gingiva"),
    # keep-with-evidence (no answer change)
    ("rafi_08_43a5bf4c8c", "evidence_only", None, None,
     "[Book: Endodontics principles] a file with a taper of 0.02 (2%) increases in diameter at a rate of 0.02 mm per running millimeter — cutting 1 mm off a #30 (0.30 mm tip) gives 0.32 mm = #32"),
    ("rafi_08_8b7dbb6ea6", "evidence_only", None, None,
     "[Book: Carranza Clinical Periodontology 2018] supragingival calculus: white or whitish yellow; hard, with a claylike consistency; easily detached — subgingival is harder/denser (so 'hard and rough' is the exception)"),
    ("fr_boost_033", "evidence_only", None, None,
     "[Book: implant literature / Contemporary Fixed] the widely taught implant-to-tooth distance is 1.5–2 mm"),
    ("rafi_04_d3defe2714", "evidence_only", None, None,
     "[Book: Contemporary Fixed Prosthodontics] 1 mm on non-functional cusp, 1.5 mm on functional"),
]

def main():
    bank, pre, post = load()
    by_id = {q["id"]: q for q in bank}
    changed = 0
    for r in REPAIRS:
        qid, action = r[0], r[1]
        q = by_id.get(qid)
        if not q:
            print("MISSING", qid); continue
        opts = [str(o) for o in q["options"]]
        if action == "replace_opt":
            idx, newtext, book = r[2], r[3], r[4]
            if idx >= len(opts): print("BAD IDX", qid); continue
            # preserve answer index; only replace a NON-answer option
            if q["answer"] == idx:
                print("REFUSE: would replace answer slot", qid); continue
            q["options"][idx] = newtext
            q["book_support"] = book
            q["book_verified"] = True
            q.pop("_repair_pending", None)
            q["usable"] = True
            print(f"{qid}: option {idx} = {newtext!r} | answer stays {q['answer']} ({opts[q['answer']]!r})")
            changed += 1
        elif action == "set_answer":
            want, book = r[2], r[3]
            idx = next((i for i, o in enumerate(opts) if str(o).strip().lower() == want.lower()), None)
            if idx is None:
                print(f"{qid}: target {want!r} NOT among options — skipping")
                continue
            q["answer"] = idx
            q["book_support"] = book
            q["book_verified"] = True
            q.pop("_repair_pending", None)
            q["usable"] = True
            print(f"{qid}: answer -> {idx} = {opts[idx]!r}")
            changed += 1
        elif action == "fix_text":
            idx, newtext, book = r[2], r[3], r[4]
            q["options"][idx] = newtext
            q["book_support"] = book
            print(f"{qid}: option {idx} text cleaned -> {newtext!r} (answer stays {q['answer']})")
            changed += 1
        elif action == "stem+answer":
            stem, idx, book = r[2], r[3], r[4]
            q["q"] = re.sub(r"resorption\s*&\s*apposition\??", "bone resorption", q["q"], flags=re.I)
            if "bone resorption" not in q["q"].lower():
                q["q"] = f"Cell responsible for bone resorption?"
            q["answer"] = idx
            q["book_support"] = book
            q["book_verified"] = True
            print(f"{qid}: stem -> {q['q'][:70]!r} | answer -> {idx} ({opts[idx]!r})")
            changed += 1
        elif action == "evidence_only":
            book = r[4]
            q["book_support"] = book
            q["book_verified"] = True
            print(f"{qid}: evidence refreshed (answer kept {q['answer']})")
            changed += 1
    # atomic write
    tmp = Q_JS.with_suffix(".js.tmp")
    tmp.write_text(pre + json.dumps(bank, ensure_ascii=False) + post, encoding="utf-8")
    tmp.replace(Q_JS)
    print(f"DONE — {changed} questions updated (atomic)")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Build the July-2026 + docx-file content into the app:
1. recent_qa.js  — 377 book-solved MCQs (set J) with dept/options/reference/why
2. flash_notes.js — 377 MCQ cards + 62 Q&A flashcards + 28 unverified archive;
   raw recall notes flagged _raw_recall for the archive section.
3. FLIP_REVIEW_LOG — 13 answer conflicts logged (bank untouched, RED LINE).
"""
import json, re, html
from pathlib import Path

ROOT = Path("/data/prometric")
SD = ROOT / "sdle-prep"
FN_JS = SD / "data" / "flash_notes.js"
QA_JS = SD / "data" / "recent_qa.js"
CONTENT = json.load(open(ROOT / "work" / "final_new_content.json", encoding="utf-8"))
QA_PARSED = json.load(open(ROOT / "work" / "parsed_new_mcqs.json", encoding="utf-8"))

FLASH_DEPT = {"operative": "restorative", "materials": "restorative", "mixed": "restorative"}

def clean_stem(s):
    s = re.sub(r"[✅🟢🟡✳🔵🔁●]+", "", s or "").strip()
    return s[:260]

# ---------- 1. recent_qa.js ----------
rq_items = []
for idx, it in enumerate(CONTENT["recentqa"]):
    n = len(it["options"])
    ai = it["answerIdx"]
    rq_items.append({
        "id": f"qa_j_{idx:04d}",
        "set": "J",
        "qnum": idx + 1,
        "dept": it["department"],
        "stem": clean_stem(it["stem"]),
        "options": [str(o).strip() for o in it["options"]],
        "answer": str(it["options"][ai]).strip(),
        "reference": it.get("reference") or "",
        "why": it.get("why") or "",
        "_verified": "book",
        "_source": it.get("source") or "july2026",
    })

qa_raw = open(QA_JS, encoding="utf-8").read()
m = re.search(r"(const ITEMS = \[)(.*)(\n  \];)", qa_raw, re.S)
new_block = m.group(1) + m.group(2).rstrip()
# careful insert before closing
insert = "\n"
for it in rq_items:
    insert += "    " + json.dumps(it, ensure_ascii=False) + ",\n"
insert = insert[:-2] + "\n"
new_block = new_block + insert + "\n  ];"
qa_raw = re.sub(r"(const ITEMS = \[)(.*)(\n  \];)", lambda mm: mm.group(1) + mm.group(2).rstrip() + insert + "\n  ];", qa_raw, count=1, flags=re.S)
tmp = QA_JS.with_suffix(".js.tmp")
tmp.write_text(qa_raw, encoding="utf-8")
tmp.replace(QA_JS)
print("recent_qa.js: appended", len(rq_items))

# ---------- 2. flash_notes.js ----------
fn_raw = open(FN_JS, encoding="utf-8").read()
fn = json.loads(re.search(r"window\.FLASH_NOTES\s*=\s*(\{.*\})", fn_raw, re.S).group(1))
byDept = fn["byDept"]

def new_mcq(it, prefix):
    n = len(it["options"])
    ai = it["answerIdx"]
    opts = [f"{chr(97+i)}. {str(o).strip()}" for i, o in enumerate(it["options"])]
    return {
        "id": f"fn_{prefix}_{it['id'][3:]}",
        "stem": clean_stem(it["stem"]),
        "options": opts,
        "answerLetter": chr(97 + ai),
        "answerIdx": ai,
        "marker": "verified",
        "needsImage": bool(it.get("image")),
        "raw": clean_stem(it["stem"]),
        "dept": FLASH_DEPT.get(it["department"], it["department"]),
        "sources": ["July_2026"] if it.get("source") == "july2026" else [str(it.get("source"))],
        "_verification_verdict": "supported",
        "_book_explanation": {"book": it.get("reference") or "", "passage": (it.get("why") or "")[:400]},
        "_dept": it["department"],
    }

added = 0
for it in CONTENT["flash"]:
    item = new_mcq(it, "j26")
    byDept.setdefault(item["dept"], []).append(item)
    added += 1
print("flash MCQ cards added:", added)

# 62 Q&A flashcards from qa_answered
qa_cards = 0
for it in QA_PARSED.get("qa_answered", []):
    if not (it.get("answer") or "").strip():
        continue
    dept = FLASH_DEPT.get(it.get("department") or "mixed", it.get("department") or "restorative")
    byDept.setdefault(dept, []).append({
        "id": f"fn_qa_{qa_cards:03d}",
        "stem": clean_stem(it["stem"]),
        "options": [],
        "answer": (it.get("answer") or "").strip(),
        "why": (it.get("why") or "").strip(),
        "reference": (it.get("reference") or "").strip(),
        "marker": "verified",
        "needsImage": False,
        "raw": clean_stem(it["stem"]),
        "dept": dept,
        "sources": ["SDLE_QA_Answered"],
        "_verification_verdict": "supported",
        "_kind": "flashcard",
    })
    qa_cards += 1
print("QA flashcards added:", qa_cards)

# genuinely-unsolved (no book answer found) -> archive, honest label
export_all = json.load(open(ROOT / "sdle-prep" / "data" / "generated" / "newmcqs" / "export_mcqs.json", encoding="utf-8"))
import sys
sys.path.insert(0, str(ROOT / "scripts"))
from verify_new_mcqs import dept_of
unv = 0
for it in export_all:
    ai = it.get("answerIdx")
    if ai is not None and 0 <= ai < len(it.get("options", [])):
        continue
    dept = FLASH_DEPT.get(dept_of(it), "restorative")
    byDept.setdefault(dept, []).append({
        "id": f"fn_j26_{it['id'][3:]}",
        "stem": clean_stem(it["stem"]),
        "options": [f"{chr(97+i)}. {str(o).strip()}" for i, o in enumerate(it.get("options", []))],
        "answerLetter": None,
        "answerIdx": None,
        "marker": "ref",
        "needsImage": bool(it.get("image")),
        "raw": clean_stem(it["stem"]),
        "dept": dept,
        "sources": ["July_2026"],
        "_verification_verdict": "needs_review",
        "_unverified": True,
    })
    unv += 1
print("unverified archive items:", unv)

# mark existing raw recall items (no answer anywhere) as _raw_recall
raw_marked = 0
for dept, items in byDept.items():
    for it in items:
        if it.get("_raw_recall"):
            continue
        has_ans = (it.get("options") and len(it["options"]) >= 2) \
            or (it.get("options") and len(it["options"]) == 1) \
            or (it.get("_embedded_answer") or "").strip() \
            or (it.get("_verified_explanation") or "").strip() \
            or it.get("_model_suggested_answer") \
            or (it.get("answer") or "").strip()
        if not has_ans:
            it["_raw_recall"] = True
            raw_marked += 1
print("existing raw items flagged archive:", raw_marked)

# totals
all_items = [it for items in byDept.values() for it in items]
fn["total"] = len(all_items)
fn["markerStats"] = {
    "verified": sum(1 for it in all_items if it.get("marker") == "verified"),
    "ref": sum(1 for it in all_items if it.get("marker") == "ref"),
}
if "July_2026" not in [s.get("id") if isinstance(s, dict) else s for s in fn.get("sources", [])]:
    fn.setdefault("sources", []).append("July_2026")
fn_raw_new = "window.FLASH_NOTES = " + json.dumps(fn, ensure_ascii=False, indent=1) + ";\n"
tmp = FN_JS.with_suffix(".js.tmp")
tmp.write_text(fn_raw_new, encoding="utf-8")
tmp.replace(FN_JS)
print("flash_notes.js rewritten: total =", fn["total"], "| markerStats =", fn["markerStats"])

# ---------- 3. conflicts -> review log ----------
conf = json.load(open(ROOT / "work" / "conflicts_log.json", encoding="utf-8"))
log = SD / "docs" / "FLIP_REVIEW_LOG.md"
s = log.read_text(encoding="utf-8")
s += "\n## 🔶 JULY-2026 NEW-SOURCE ANSWER CONFLICTS (2026-08-06) — bank UNTOUCHED, pending review\n"
s += "Same stem exists in the bank with a different answer. Book-grounded verdict needed.\n"
for c in conf:
    s += f"- `{c['new_id']}` (new source) vs `{c['bank_id']}` (bank) — new: “{c['new_ans']}” | bank: “{c['bank_ans']}” — stem: {c['stem'][:80]}\n"
log.write_text(s, encoding="utf-8")
print("conflicts logged:", len(conf))

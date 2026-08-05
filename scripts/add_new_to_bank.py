#!/usr/bin/env python3
"""Add the 377 new book-verified MCQs (Set J) to the PRACTICE bank (questions.js).
349 usable+book_verified (real [Book:] passages); 28 honest-hidden (no passage).
Schema matches existing bank items. Atomic write via tmp+replace.
"""
import json, re, os
from pathlib import Path

SD = Path("/data/prometric/sdle-prep")
Q_JS = SD / "data" / "questions.js"
PAGES = json.load(open("/data/prometric/sdle-prep/data/generated/book_pages/index.json", encoding="utf-8"))

TOPIC = {"fixed": "restorative", "operative": "restorative", "materials": "restorative",
         "rpd": "restorative", "endo": "endo", "perio": "perio", "ortho_pedo": "ortho_pedo",
         "oms": "oms", "ethics": "ethics", "mixed": "mixed"}

raw = Q_JS.read_text(encoding="utf-8")
bank = json.loads(re.search(r"QUESTION_BANK\s*=\s*(\[.*\])", raw, re.S).group(1))
have = {q.get("id") for q in bank}
existing = {re.sub(r"[^a-z0-9]+", " ", str(q.get("q", "")).lower()).strip()[:60] for q in bank}

qa_raw = (SD / "data" / "recent_qa.js").read_text(encoding="utf-8")
m = re.search(r"const ITEMS = \[(.*)\n  \];", qa_raw, re.S)
qa_items = json.loads("[" + m.group(1) + "]")
j_items = [i for i in qa_items if i.get("set") == "J"]

added, skipped = 0, 0
for idx, it in enumerate(j_items):
    ns = re.sub(r"[^a-z0-9]+", " ", str(it["stem"]).lower()).strip()[:60]
    if ns in existing:
        skipped += 1
        continue
    qid = f"j26_{idx:04d}"
    if qid in have:
        continue
    opts = [str(o).strip() for o in (it.get("options") or [])]
    ai = it.get("answer")
    if not isinstance(ai, int) or not (0 <= ai < len(opts)):
        continue
    ref = it.get("reference") or ""
    why = it.get("why") or ""
    verified = it.get("_verified") == "book" and bool(ref)
    pg = PAGES.get(it.get("id")) or {}
    item = {
        "id": qid,
        "topic": TOPIC.get(it.get("dept"), "mixed"),
        "difficulty": "medium",
        "q": str(it["stem"]),
        "options": opts,
        "answer": ai,
        "explanation": why,
        "source": "july2026_files",
        "subtopics": [it.get("dept", "mixed")],
        "truth_pass": "book" if verified else None,
        "truth_confidence": 0.9 if verified else None,
        "truth_wave": 3 if verified else None,
        "read_audit": "book" if verified else None,
        "audit_confidence": 0.9 if verified else None,
        "book_support": f"[Book: {ref}] {why[:400]}" if verified else "",
        "truth_judge": "supported" if verified else "needs_review",
        "usable": verified,
        "book_verified": verified,
        "_verify_pass": "book" if verified else "unverified",
        "_page": pg.get("page"),
        "_book_file": pg.get("file"),
        "_context": pg.get("context", ""),
    }
    bank.append(item)
    have.add(qid)
    existing.add(ns)
    added += 1

print(f"added {added} to bank | skipped {skipped} (dup stems) | bank total now {len(bank)}")
raw_new = re.sub(r"(QUESTION_BANK\s*=\s*)(\[.*\])(\s*;?)",
                 lambda mm: mm.group(1) + json.dumps(bank, ensure_ascii=False) + mm.group(3),
                 raw, count=1, flags=re.S)
tmp = Q_JS.with_suffix(".js.tmp")
tmp.write_text(raw_new, encoding="utf-8")
tmp.replace(Q_JS)
print("questions.js written atomically")

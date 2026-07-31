#!/usr/bin/env python3
"""
reverify_repaired.py — re-verify only the repaired Saud items against books,
merging new verdicts into the existing flash_notes_verdicts_v2.json.

Usage: python3 scripts/reverify_repaired.py [--answers-only]
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import importlib.util

spec = importlib.util.spec_from_file_location("vt", Path(__file__).resolve().parent / "verify_textbook_v2.py")
vt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vt)

PREP = Path("/data/prometric/sdle-prep")
FN_JS = PREP / "data" / "flash_notes.js"
OUT_JSON = PREP / "data" / "flash_notes_verdicts_v2.json"

def main():
    answers_only = "--answers-only" in sys.argv
    content = FN_JS.read_text(encoding="utf-8")
    data = json.loads(re.search(r"window\.FLASH_NOTES\s*=\s*(\{.*);", content, re.DOTALL).group(1))
    items = [it for its in data["byDept"].values() for it in its]
    repaired = [it for it in items if it.get("_repaired_2026")]
    if answers_only:
        repaired = [it for it in repaired if it.get("answerLetter") or it.get("answerIdx") is not None]
    print(f"Repaired items to re-verify: {len(repaired)}")

    # load existing verdicts
    old = json.loads(OUT_JSON.read_text(encoding="utf-8"))
    verdicts = old.get("verdicts", {})

    print("\n📚 Loading all textbooks...")
    global_indices = []
    for cfg in vt.ALL_BOOKS:
        idx = vt.TextbookIndex(cfg)
        if idx.load():
            global_indices.append(idx)
    print(f"   → {len(global_indices)} books loaded")

    new_sup = 0
    for i, it in enumerate(repaired):
        v = vt.verify_item(it, global_indices)
        verdicts[it["id"]] = v
        if v["verdict"] == "supported":
            new_sup += 1
        if (i + 1) % 50 == 0:
            print(f"   [{i+1}/{len(repaired)}] supported so far: {new_sup}")
            OUT_JSON.write_text(json.dumps(old, ensure_ascii=False, indent=2), encoding="utf-8")

    supported_total = sum(1 for v in verdicts.values() if v.get("verdict") == "supported")
    old["verdicts"] = verdicts
    old["totalChecked"] = len(verdicts)
    old["stats"] = {"supported": supported_total, "needs_review": len(verdicts) - supported_total}
    OUT_JSON.write_text(json.dumps(old, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nDone. New supported from repair: {new_sup}")
    print(f"Total supported verdicts now: {supported_total}")

if __name__ == "__main__":
    main()

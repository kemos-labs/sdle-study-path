#!/usr/bin/env python3
"""dedupe_flash.py — dedupe Flash Notes items by normalized stem + option overlap.

Strategy (safe):
  * Group items by full normalized stem.
  * True duplicates = groups where option sets overlap >= 40%.
  * Keep the BEST copy: most options, has answer, 'verified' marker, any dept.
  * Merge `sources` provenance into the kept copy.
  * Mark removed copies `_merged_into: <kept id>` + `_data_quality: "deduped"`
    (the UI already hides `_merged_into` items from study lists).
  * If two copies carry CONFLICTING answers, keep the best copy but stamp
    `_answer_conflict: [{id, answerIdx, answerLetter}]` so book-verification
    (Phase 2) resolves it. Nothing is silently dropped.

Usage:
    python3 scripts/dedupe_flash.py            # dry run
    python3 scripts/dedupe_flash.py --apply    # write changes
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FN_JS = ROOT / "data" / "flash_notes.js"
REPORT = ROOT / "work" / "dedupe_flash_report.json"


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9\u0621-\u064A]", "", (s or "").lower())


def norm_opts(it) -> set:
    return {norm(o) for o in (it.get("options") or []) if len(norm(o)) > 3}


def overlap(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union


def copy_score(it) -> tuple:
    nopts = len(it.get("options") or [])
    has_ans = it.get("answerIdx") is not None or bool(it.get("answerLetter"))
    marker = it.get("marker")
    return (nopts, 1 if has_ans else 0, 1 if marker == "verified" else 0)


def main() -> int:
    text = FN_JS.read_text(encoding="utf-8")
    m = re.search(r"(window\.FLASH_NOTES\s*=\s*)(\{.*\})(\s*;)", text, re.DOTALL)
    if not m:
        raise SystemExit("❌ could not parse flash_notes.js")
    data = json.loads(m.group(2))
    apply = "--apply" in sys.argv

    all_items = [it for its in data["byDept"].values() for it in its]
    groups = {}
    for it in all_items:
        key = norm(it.get("stem", ""))
        if len(key) < 8:
            continue
        groups.setdefault(key, []).append(it)

    stats = {"dup_groups": 0, "merged_away": 0, "conflicts": 0, "false_positives": 0}
    report = []
    for key, g in groups.items():
        if len(g) < 2:
            continue
        sets = [norm_opts(it) for it in g]
        best = 0.0
        for i in range(len(g)):
            for j in range(i + 1, len(g)):
                best = max(best, overlap(sets[i], sets[j]))
        if best < 0.4:
            stats["false_positives"] += 1
            continue  # different questions that share a stem start
        stats["dup_groups"] += 1
        keeper = max(g, key=copy_score)
        # merge sources
        all_src = []
        for it in g:
            for s in (it.get("sources") or []):
                if s not in all_src:
                    all_src.append(s)
        # conflicting answers?
        answers = {(it.get("answerIdx"), it.get("answerLetter")) for it in g if it.get("answerIdx") is not None}
        conflict = len(answers) > 1
        entry = {
            "keeper": keeper["id"],
            "merged": [it["id"] for it in g if it is not keeper],
            "conflict": conflict,
            "sources": all_src,
        }
        if conflict:
            entry["answers"] = [{"id": it["id"], "answerIdx": it.get("answerIdx"),
                                 "answerLetter": it.get("answerLetter")} for it in g]
        report.append(entry)
        if apply:
            keeper["sources"] = all_src
            if conflict:
                keeper["_answer_conflict"] = [{"id": it["id"], "answerIdx": it.get("answerIdx"),
                                               "answerLetter": it.get("answerLetter")}
                                              for it in g if it is not keeper]
            for it in g:
                if it is not keeper:
                    it["_merged_into"] = keeper["id"]
                    if not it.get("_data_quality"):
                        it["_data_quality"] = "deduped"
                    stats["merged_away"] += 1
            if conflict:
                stats["conflicts"] += 1

    print(f"DRY-RUN (no --apply): {json.dumps(stats, ensure_ascii=False)}")
    for e in report[:10]:
        print(f"  keep {e['keeper']} ← {e['merged']} conflict={e['conflict']}")

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps({"stats": stats, "groups": report}, ensure_ascii=False, indent=1),
                      encoding="utf-8")

    if apply:
        data["generated"] = "2026-08-02 (dedupe_flash)"
        out = m.group(1) + json.dumps(data, ensure_ascii=False, indent=1) + m.group(3)
        FN_JS.write_text(out, encoding="utf-8")
        print(f"✅ wrote {FN_JS} — total unchanged: {data['total']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

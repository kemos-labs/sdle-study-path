#!/usr/bin/env python3
"""Repair Flash Notes option structure without changing the item set."""
from __future__ import annotations

import json
import re
from pathlib import Path

from build_flash_notes import extract_options, find_marked_answer


ROOT = Path(__file__).resolve().parents[1]
FLASH_NOTES = ROOT / "data" / "flash_notes.js"


def load() -> dict:
    text = FLASH_NOTES.read_text(encoding="utf-8")
    match = re.search(r"window\.FLASH_NOTES\s*=\s*(\{.*);", text, re.DOTALL)
    if not match:
        raise SystemExit("Could not parse flash_notes.js")
    return json.loads(match.group(1))


def main() -> None:
    data = load()
    repaired = downgraded = reindexed = merged = 0
    all_items = [item for items in data["byDept"].values() for item in items]

    for item in all_items:
        old_options = item.get("options", [])
        parsed = extract_options(item.get("raw", ""))
        if len(parsed) >= 2:
            options = [f"{letter}. {text}" for letter, text in parsed]
            if options != old_options:
                item["options"] = options
                repaired += 1

            letter, index = find_marked_answer(parsed, item.get("raw", ""))
            if letter is not None:
                item["answerLetter"] = letter
                item["answerIdx"] = index
            elif item.get("answerIdx") is not None and item["answerIdx"] >= len(item["options"]):
                item["answerLetter"] = None
                item["answerIdx"] = None
                reindexed += 1

        options = item.get("options", [])
        if item.get("answerIdx") is not None and item["answerIdx"] >= len(options):
            item["answerLetter"] = None
            item["answerIdx"] = None
            reindexed += 1

        item["format"] = "mcq" if len(options) >= 2 else "recall"
        if item.get("marker") == "verified" and len(options) < 2:
            # A source checkmark on a non-MCQ is a community recall lead, not
            # a verified multiple-choice item.
            item["marker"] = "ref"
            downgraded += 1
        if len(options) >= 5:
            item["_data_quality"] = "merged_options_review"
            merged += 1
        else:
            item.pop("_data_quality", None)

    if len(all_items) != data["total"]:
        raise SystemExit("Refusing to write: item count changed")
    markers: dict[str, int] = {}
    for item in all_items:
        markers[item["marker"]] = markers.get(item["marker"], 0) + 1
    data["markerStats"] = markers
    data["dataQuality"] = {"merged_options_review": merged}
    FLASH_NOTES.write_text(
        "/** Flash Notes — source recalls plus canonical-book evidence candidates. */\n"
        "window.FLASH_NOTES = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n",
        encoding="utf-8",
    )
    print(f"Repaired {repaired} option sets; downgraded {downgraded} incomplete MCQs; cleared {reindexed} invalid indexes; flagged {merged} merged-option items.")


if __name__ == "__main__":
    main()

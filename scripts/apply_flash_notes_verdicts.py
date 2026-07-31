#!/usr/bin/env python3
"""Apply canonical-textbook evidence candidates to Flash Notes safely.

This does not mark an answer textbook-verified.  A `supported` result means
only that the deterministic checker found a non-junk canonical-book passage
containing both a stem term and an answer term.  Final clinical correctness
still requires the mandated human/Grok-plus-book review.
"""
from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FLASH_NOTES = ROOT / "data" / "flash_notes.js"
VERDICTS = ROOT / "data" / "flash_notes_verdicts_v2.json"


def load_js(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    match = re.search(r"window\.FLASH_NOTES\s*=\s*(\{.*);", text, re.DOTALL)
    if not match:
        raise SystemExit(f"Could not parse {path}")
    return json.loads(match.group(1))


def main() -> None:
    data = load_js(FLASH_NOTES)
    verdicts = json.loads(VERDICTS.read_text(encoding="utf-8"))["verdicts"]
    applied = supported = missing = 0

    for items in data["byDept"].values():
        for item in items:
            result = verdicts.get(item["id"])
            if not result:
                item["_verification_verdict"] = "needs_review"
                item.pop("_book_explanation", None)
                missing += 1
                continue

            applied += 1
            verdict = result.get("verdict", "needs_review")
            item["_verification_verdict"] = verdict
            if verdict != "supported":
                item.pop("_book_explanation", None)
                continue

            evidence = next(
                (entry for entry in result.get("evidence", [])
                 if entry.get("ans_keywords_hit", 0) > 0
                 and entry.get("stem_keywords_hit", 0) > 0
                 and entry.get("passage", "").strip()),
                None,
            )
            if not evidence:
                item["_verification_verdict"] = "needs_review"
                item.pop("_book_explanation", None)
                continue

            item["_book_explanation"] = {
                "book": evidence.get("book", "Canonical SCFHS text"),
                "chapter": evidence.get("chapter", ""),
                "passage": evidence["passage"],
                "status": "automated_evidence_candidate",
            }
            supported += 1

    all_items = [item for items in data["byDept"].values() for item in items]
    if len(all_items) != data["total"]:
        raise SystemExit(f"Refusing to write: {len(all_items)} items != declared total {data['total']}")

    FLASH_NOTES.write_text(
        "/** Flash Notes — source recalls plus canonical-book evidence candidates. */\n"
        "window.FLASH_NOTES = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n",
        encoding="utf-8",
    )
    print(f"Applied {applied} verdicts; {supported} candidate passages retained; {missing} items defaulted to needs_review.")


if __name__ == "__main__":
    main()

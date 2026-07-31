#!/usr/bin/env python3
"""Gate for Flash Notes — exit 0 only if no-slack red lines are green.

Checks the same invariants as gate_no_slack.py but for data/flash_notes.js.

Usage:
    python3 scripts/gate_flash_notes.py

Exit code:
    0 = all gates green
    1 = one or more gates red (details printed as JSON)
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FN_JS = ROOT / "data" / "flash_notes.js"


def load_flash_notes() -> dict:
    text = FN_JS.read_text(encoding="utf-8")
    m = re.search(r"window\.FLASH_NOTES\s*=\s*(\{.*);", text, re.DOTALL)
    if not m:
        raise SystemExit("❌ Could not parse flash_notes.js")
    return json.loads(m.group(1))


def main() -> int:
    data = load_flash_notes()

    total = data["total"]
    markers = data.get("markerStats", {})

    # Collect all items
    all_items = []
    for dept, items in data.get("byDept", {}).items():
        for it in items:
            all_items.append(it)

    print(f"📊 Flash Notes: {total} items loaded")

    # ── Gate FN-COUNT: total matches expected ────────────────────────────
    found_total = len(all_items)
    count_ok = found_total == total
    if not count_ok:
        print(f"  ❌ FN-COUNT: declared={total} actual={found_total}")

    # ── Gate FN-OPTS: verified items should have ≥2 options ─────────────
    verified_lt2 = []
    for it in all_items:
        if it.get("marker") == "verified" and len(it.get("options", [])) < 2:
            verified_lt2.append(it["id"])
    opts_ok = len(verified_lt2) == 0
    if not opts_ok:
        print(f"  ❌ FN-OPTS: {len(verified_lt2)} verified items have <2 options")
        print(f"     sample: {verified_lt2[:10]}")

    # ── Gate FN-IDX: no answerIdx out of range ──────────────────────────
    oob_items = []
    for it in all_items:
        aidx = it.get("answerIdx")
        opts = it.get("options", [])
        if aidx is not None and aidx >= len(opts):
            oob_items.append({"id": it["id"], "answerIdx": aidx, "options_len": len(opts)})
    idx_ok = len(oob_items) == 0
    if not idx_ok:
        print(f"  ❌ FN-IDX: {len(oob_items)} items have answerIdx OOB")
        print(f"     sample: {oob_items[:10]}")

    # ── Gate FN-CITATION: only supported verdicts may expose evidence ────
    # `supported` is still an automated evidence candidate, not a final
    # correctness judgement. The UI intentionally does not use the phrase
    # "textbook-verified" for either status.
    invalid_supported = []
    for it in all_items:
        book_exp = it.get("_book_explanation")
        verdict = it.get("_verification_verdict", "")
        if verdict != "supported":
            continue
        passage = book_exp.get("passage", "") if isinstance(book_exp, dict) else str(book_exp or "")
        if not passage.strip() or re.match(r"^\s*(?:INDEX|REFERENCES?|BIBLIOGRAPHY|GLOSSARY)\b", passage, re.I):
            invalid_supported.append({"id": it["id"], "verdict": verdict, "passage": passage[:80]})
    citation_ok = len(invalid_supported) == 0
    if not citation_ok:
        print(f"  ❌ FN-CITATION: {len(invalid_supported)} supported items lack a usable non-index passage")
        print(f"     sample: {invalid_supported[:10]}")

    # ── Gate FN-BOOKS: canonical SCFHS textbook extracts exist ──────────
    books_dir = ROOT / "data" / "raw" / "books" / "text"
    txt_files = list(books_dir.rglob("*.txt")) if books_dir.exists() else []
    books_ok = len(txt_files) >= 22
    if not books_ok:
        print(f"  ❌ FN-BOOKS: only {len(txt_files)} canonical .txt extracts found (need ≥22)")

    # ── Gate FN-VERIFIED: verification verdict coverage ──────────────────
    verdict_coverage = sum(1 for it in all_items if "_verification_verdict" in it)
    supported = sum(1 for it in all_items if it.get("_verification_verdict") == "supported")
    needs_review = sum(1 for it in all_items if it.get("_verification_verdict") == "needs_review")
    verified_ok = verdict_coverage == total
    if not verified_ok:
        print(f"  ❌ FN-VERIFIED: only {verdict_coverage}/{total} items have verdicts")

    # ── Gate FN-MERGED: long option lists must be visibly flagged ───────
    merged = [it["id"] for it in all_items if len(it.get("options", [])) >= 5]
    unflagged_merged = [it["id"] for it in all_items if len(it.get("options", [])) >= 5
                        and it.get("_data_quality") != "merged_options_review"]
    merged_ok = not unflagged_merged
    if not merged_ok:
        print(f"  ❌ FN-MERGED: {len(unflagged_merged)} long option lists are not flagged for source review")

    # ── Summary ─────────────────────────────────────────────────────────
    gates = {
        "FN-COUNT": {"ok": count_ok, "declared": total, "actual": found_total},
        "FN-OPTS": {"ok": opts_ok, "verified_lt2_count": len(verified_lt2), "sample": verified_lt2[:20]},
        "FN-IDX": {"ok": idx_ok, "oob_count": len(oob_items), "sample": oob_items[:20]},
        "FN-CITATION": {"ok": citation_ok, "invalid_supported_count": len(invalid_supported), "sample": invalid_supported[:20]},
        "FN-BOOKS": {"ok": books_ok, "canonical_txt_file_count": len(txt_files)},
        "FN-VERIFIED": {"ok": verified_ok, "verdict_coverage": f"{verdict_coverage}/{total}",
                        "supported": supported, "needs_review": needs_review},
        "FN-MERGED": {"ok": merged_ok, "flagged_count": len(merged), "unflagged_count": len(unflagged_merged),
                      "sample": unflagged_merged[:20]},
    }

    all_ok = all(g["ok"] for g in gates.values())
    report = {
        "all_green": all_ok,
        "total": total,
        "markerStats": markers,
        "gates": gates,
        "rule": "docs/RED_LINE_NO_SLACK.md (applied to Flash Notes tab)",
    }

    print(f"\n{'=' * 60}")
    print(f"FLASH NOTES GATE REPORT")
    print(f"{'=' * 60}")
    print(json.dumps(report, indent=2, ensure_ascii=False))

    # Write report
    outp = ROOT / "data" / "generated" / "phase_truth" / "GATE_FLASH_NOTES.json"
    outp.parent.mkdir(parents=True, exist_ok=True)
    outp.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

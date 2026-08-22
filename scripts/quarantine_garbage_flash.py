#!/usr/bin/env python3
"""
quarantine_garbage_flash.py — mark broken-stem "MCQs" in flash_notes.js as garbage.

Conservative rules (only clearly-broken items are touched):
  R1  cleaned stem < 3 chars
  R2  stem contains table pipes "|"
  R3  stem contains newlines (merged multi-line fragments)
  R4  stem starts with a bullet/dash AND has no "?" AND cleaned length < 60
      (answer-fragment class: "- gold", "- Erythema multiform", ...)
  R5  normalized stem equals one of its own option texts (parser put the
      answer line as the stem)

Quarantined items get _data_quality="garbage" + _garbage_reason and stay in
the data file (Review > archive bucket), never deleted.

Usage:
    python3 scripts/quarantine_garbage_flash.py           # dry run
    python3 scripts/quarantine_garbage_flash.py --apply   # write file
"""
from __future__ import annotations
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FN_JS = ROOT / "data" / "flash_notes.js"

MARKERS = re.compile(r"[✅🟢🟡✳🔵🔁●]")
BULLET_PREFIX = re.compile(r"^[\s\u2022\u25CF\u2023\u25AA\u25A0#*>-]+")


def clean(s: str) -> str:
    s = MARKERS.sub("", s or "")
    s = BULLET_PREFIX.sub("", s)
    return s.strip()


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", clean(s)).lower().rstrip("?").strip()


def classify(it: dict) -> str | None:
    if it.get("_kind") == "flashcard":
        return None
    if it.get("_data_quality"):
        return None
    opts = [o for o in (it.get("options") or []) if o]
    if len(opts) < 2:
        return None  # recall/Q&A cards are fine without options
    raw_stem = it.get("stem") or ""
    t = re.sub(r"\s+", " ", clean(raw_stem)).strip()
    if len(t) < 3:
        return "too_short"
    ns = norm(raw_stem)
    if ns and any(ns == norm(o) for o in opts):
        return "stem_equals_option"
    if "?" in t:
        return None  # terse/messy but a real question — keep
    if BULLET_PREFIX.match(raw_stem.strip()) and len(t) < 60:
        return "bullet_fragment_no_question"
    if "|" in raw_stem:
        return "table_fragment_no_question"
    words = t.split()
    if len(words) <= 2 and len(t) < 24:
        return "short_fragment_no_question"
    return None


def main() -> int:
    apply = "--apply" in sys.argv
    text = FN_JS.read_text(encoding="utf-8")
    m = re.search(r"window\.FLASH_NOTES\s*=\s*(\{.*);", text, re.DOTALL)
    if not m:
        raise SystemExit("cannot parse flash_notes.js")
    data = json.loads(m.group(1))

    hits: dict[str, list] = {}
    n_items = 0
    for dept, items in data.get("byDept", {}).items():
        for it in items:
            n_items += 1
            if it.get("_merged_into"):
                continue
            r = classify(it)
            if r:
                hits.setdefault(r, []).append(it)

    total_q = sum(len(v) for v in hits.values())
    print(f"items scanned: {n_items}")
    by_src: Counter = Counter()
    for r, lst in hits.items():
        print(f"\n{r}: {len(lst)}")
        for it in lst[:6]:
            print(f"   {it['id']}  {clean(it.get('stem',''))[:60]!r}")
        for it in lst:
            by_src[(it.get("sources") or ["?"])[0]] += 1
    print("\nby source:", dict(by_src.most_common()))
    print("TOTAL to quarantine:", total_q)

    if not apply:
        print("\nDRY RUN — rerun with --apply to write.")
        return 0

    for r, lst in hits.items():
        for it in lst:
            it["_data_quality"] = "garbage"
            it["_garbage_reason"] = r

    dq = data.setdefault("dataQuality", {})
    dq["garbage_stem_quarantine"] = total_q
    dq["note"] = "garbage stems stay in data, excluded from decks/quizzes, visible in Review>archive"

    out = f"/** Flash Notes — garbage-stem quarantine pass */\nwindow.FLASH_NOTES = {json.dumps(data, ensure_ascii=False, indent=1)};\n"
    bak = FN_JS.with_suffix(".js.bak-quarantine")
    bak.write_text(text, encoding="utf-8")
    FN_JS.write_text(out, encoding="utf-8")
    print(f"\nAPPLIED. backup: {bak.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

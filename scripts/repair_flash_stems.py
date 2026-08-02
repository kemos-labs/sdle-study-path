#!/usr/bin/env python3
"""repair_flash_stems.py — safe, idempotent data repair for data/flash_notes.js.

Safe repairs only (never touch items with real options/answers):
1. Strip leading bullet/dash/●/• prefixes from stems.
2. Recover inline marked answers from stems that have NO structured answer:
   e.g. "- tetracycline\\n🚨\\n| junk |"  -> _embedded_answer="tetracycline"
        "● Calcium 👍🏻"                    -> _embedded_answer="Calcium"
        "crown lengthening ✅"            -> _embedded_answer="crown lengthening"
   Only when the pre-marker text is a short, plausible answer phrase (2-80 chars).
3. Flag clearly broken stems with `_data_quality: "garbage"` (never quizzed).

Usage:
    python3 scripts/repair_flash_stems.py            # dry run (report only)
    python3 scripts/repair_flash_stems.py --apply    # write changes
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FN_JS = ROOT / "data" / "flash_notes.js"

MARKER_RE = re.compile(r"[✅🟢🟡✳🔵🔁🚨👍🏻]")
BULLET_PREFIX_RE = re.compile(r"^[\s\-•●▪▫*#>]+")
EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF\u2600-\u27BF\uFE0F]")

# Table-noise patterns (Saud fragments): "- tetracycline\n🚨\n| | 40 years | ... |"
# The answer is the first line, before any marker or table pipe.
INLINE_MARKED = re.compile(
    r"^\s*(?:[-•●▪▫*#>]+\s*)?([A-Za-z\u0621-\u064A0-9][^✅🟢🟡✳🔵🔁🚨👍🏻\n|]{1,78}?)\s*[✅🟢🟡✳🔵🔁🚨👍🏻]",
    re.M,
)


def strip_bullets(s: str) -> str:
    t = MARKER_RE.sub("", s or "")
    t = BULLET_PREFIX_RE.sub("", t)
    t = EMOJI_RE.sub("", t)
    return t.strip()


def looks_junk(stem: str) -> bool:
    t = strip_bullets(stem)
    if len(t) < 3:
        return True
    # only punctuation / separators / pipes / dashes
    if not re.search(r"[A-Za-z\u0621-\u064A0-9]", t):
        return True
    # pure option-table residue: many pipes + few letters
    letters = len(re.findall(r"[A-Za-z\u0621-\u064A]", t))
    if t.count("|") >= 3 and letters < 8:
        return True
    return False


def recover_answer(stem: str) -> str:
    """Best-effort answer extraction from a marker-bearing stem."""
    m = INLINE_MARKED.match(stem)
    if m:
        ans = m.group(1).strip()
        # drop trailing table noise / repeated dashes
        ans = re.split(r"\s{2,}|\||\n{2,}", ans)[0].strip()
        ans = BULLET_PREFIX_RE.sub("", ans).strip()
        if 2 <= len(ans) <= 80:
            return ans
    return ""


def main() -> int:
    text = FN_JS.read_text(encoding="utf-8")
    m = re.search(r"(window\.FLASH_NOTES\s*=\s*)(\{.*\})(\s*;)", text, re.DOTALL)
    if not m:
        raise SystemExit("❌ could not parse flash_notes.js")
    data = json.loads(m.group(2))

    apply = "--apply" in sys.argv
    stats = {"stem_cleaned": 0, "answer_recovered": 0, "flagged_junk": 0}
    changed = []

    for dept, items in data.get("byDept", {}).items():
        for it in items:
            stem = it.get("stem", "")
            if not isinstance(stem, str):
                continue
            # Orphan option fragments (_is_option) are linked back to parents in
            # the merge phase — don't rewrite them here, just leave them honest.
            if it.get("_is_option"):
                continue
            had_answer = (
                it.get("answerIdx") is not None
                or it.get("answerLetter")
                or it.get("_verified_explanation")
                or it.get("_embedded_answer")
                or it.get("_model_suggested_answer")
            )
            has_options = len(it.get("options", [])) > 0

            # 1) recover inline answer only for answerless, optionless items
            if not had_answer and not has_options:
                ans = recover_answer(stem)
                if ans:
                    if apply:
                        it["_embedded_answer"] = ans
                    stats["answer_recovered"] += 1
                    changed.append((it["id"], "answer_recovered", ans[:40]))

            # 2) flag junk (but keep item in deck, honestly labeled)
            if looks_junk(stem) and not it.get("_data_quality"):
                if apply:
                    it["_data_quality"] = "garbage"
                stats["flagged_junk"] += 1
                changed.append((it["id"], "flagged_junk", stem[:50]))

            # 3) cosmetic bullet-prefix clean (never changes meaning) — only for
            #    stems that still look like a question/statement after cleaning.
            clean = strip_bullets(stem)
            if (
                clean
                and len(clean) >= 5
                and clean != stem
                and BULLET_PREFIX_RE.match(stem)
                and not stem.lstrip().startswith(("a.", "b.", "c.", "d."))
                and "|" not in clean
            ):
                if apply:
                    it["stem"] = clean
                stats["stem_cleaned"] += 1
                changed.append((it["id"], "stem_cleaned", stem[:30]))

    print(f"dry-run stats (no --apply): {json.dumps(stats, ensure_ascii=False)}")
    for cid, kind, detail in changed[:15]:
        print(f"  {kind}: {cid} — {detail!r}")

    if apply:
        data["generated"] = "2026-08-02 (repair_flash_stems)"
        new_body = json.dumps(data, ensure_ascii=False, indent=1)
        out = m.group(1) + new_body + m.group(3)
        FN_JS.write_text(out, encoding="utf-8")
        print(f"✅ wrote {FN_JS} — {json.dumps(stats, ensure_ascii=False)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

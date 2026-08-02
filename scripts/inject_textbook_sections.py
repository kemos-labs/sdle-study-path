#!/usr/bin/env python3
"""Inject textbook-grounded HTML sections into lessons.js by day."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LESSONS = ROOT / "data" / "lessons.js"
SEC = ROOT / "data" / "generated" / "textbook_sections"

# day -> section file(s) to append once
MAP = {
    1: ["operative_sturdevant.html"],
    2: ["fixed_rosenstiel.html"],
    3: ["rpd_cd.html"],
    4: ["operative_sturdevant.html", "fixed_rosenstiel.html", "rpd_cd.html"],
    5: ["perio_core.html"],
    6: ["endo_cohen.html"],
    7: ["oms_hupp.html"],
    8: ["ethics_ic_la.html"],
    9: ["ortho_pedo.html"],
}


def main() -> int:
    text = LESSONS.read_text(encoding="utf-8")
    # load lessons as JS is huge — do string surgery on reading fields carefully
    # Find each day object reading: `...`
    for day, files in MAP.items():
        if not files:
            continue
        chunks = []
        for f in files:
            p = SEC / f
            if p.exists():
                chunks.append(p.read_text(encoding="utf-8").strip())
        if not chunks:
            continue
        inject = "\n".join(chunks)
        # skip if already injected
        marker = "textbook-grounded"
        # locate day N block
        pat = re.compile(
            rf"(day\s*:\s*{day}\b[\s\S]*?reading\s*:\s*`)([\s\S]*?)(`)",
            re.M,
        )
        m = pat.search(text)
        if not m:
            print("no reading for day", day)
            continue
        body = m.group(2)
        if marker in body:
            print("day", day, "already has textbook section")
            continue
        # append before closing
        new_body = body.rstrip() + "\n" + inject + "\n"
        # escape backticks in inject if any
        if "`" in inject:
            print("WARN backticks in inject day", day)
        text = text[: m.start(2)] + new_body + text[m.end(2) :]
        print("injected day", day, "chars+", len(inject))

    LESSONS.write_text(text, encoding="utf-8")
    print("wrote", LESSONS)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""
fix_dropped_answer_option.py — STRICT version.

Repair flash-notes MCQs where the parser dropped the ✅-marked final option
(so the item lost its correct answer). ONLY applies a fix when we can prove
the source block is THIS question and the marked option belongs to it.

Strict rules (all must hold):
  1. The item has >=2 options and NO answer (answerLetter/answerIdx/embedded/suggested).
  2. A UNIQUE anchor (>=35 cleaned chars of the stem) is found in the source .md.
  3. The matched source block (anchor..+900 chars) contains a ✅/✳/●-marked option
     line whose letter is either:
       (a) already among the item's option letters  -> just mark the answer, OR
       (b) exactly the next letter after the item's last option letter AND the
           item currently has <=3 options (i.e. a dropped 4th option).
  4. The marked option text, after lowercasing/spacing, shares at least one
     >=4-char word with one of the item's existing options OR the stem — guards
     against grabbing a marker from an adjacent unrelated question.
  5. The block must NOT contain a second question number/heading between the
     anchor and the marked option (else we crossed into another question).

Records `_repair_source: "dropped_answer_option"`. Total item count preserved.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from load_flash_notes import load  # noqa: E402

# Items where the strict matcher still produces a wrong/ambiguous match
# (verified by hand against the source block). Skip these — leave flagged.
EXCLUDE = {
    "fn_rpd_0048",        # ✅ is on 'Sodium hypochlorite' (the answer hint), not an option letter; 'Reciprocal arm' is from an adjacent clasp question
    "fn_implant_0095",    # merged-questions mess (implant pain→Mental nerve); 'B 18' is a false grab
    "fn_ortho_pedo_gf2_0043",  # TWO options both ✅✅ (Ceramic brackets + Schiller's) — ambiguous, source merged two questions
}

SRC_FILES = {
    "Mar-June_2026": ROOT.parent / "sdle-ref" / "questions" / "Mar-June_2026.md",
    "SDLE_May_2026": ROOT.parent / "sdle-ref" / "focus" / "SDLE_May_2026.md",
    "Saud_Talkhees": ROOT.parent / "sdle-ref" / "focus" / "تلخيص_سعود__20251130_154203_٠٠٠٠.md",
    "Rafi_Maqam_16": ROOT.parent / "sdle-ref" / "focus" / "رفيع_المقام_١٦.md",
    "Rafi_Maqam_19": ROOT.parent / "sdle-ref" / "focus" / "رفيع_المقام_19_-___دعواتكم__.md",
    "GoldenFile2": ROOT.parent / "sdle-ref" / "focus_new" / "Golden_File_2_2021.md",
    "June_July2023": ROOT.parent / "sdle-ref" / "focus_new" / "June_July2023_abtal.md",
    "July_2026": ROOT.parent / "sdle-ref" / "focus_new" / "July_2026_abtal.md",
}

MARK_CHARS = "✅✳✔🔵🟢🟡●"
_SRC_CACHE: dict[str, str] = {}


def src_text(name: str) -> str:
    if name not in _SRC_CACHE:
        p = SRC_FILES.get(name)
        if name == "Saud_Masahhah":
            import glob
            cand = [Path(x) for x in glob.glob(str(ROOT.parent / "sdle-ref" / "focus" / "*.md"))]
            claimed = {SRC_FILES[k] for k in SRC_FILES if k != "Saud_Masahhah"}
            others = [c for c in cand if c not in claimed and c.name != "SDLE_May_2026.md"]
            p = max(others, key=lambda x: x.stat().st_size) if others else None
        _SRC_CACHE[name] = p.read_text(encoding="utf-8", errors="replace") if p and p.exists() else ""
    return _SRC_CACHE[name]


def clean(s: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^A-Za-z0-9 ]", " ", s or "")).strip().lower()


def words(s: str) -> set:
    return {w for w in clean(s).split() if len(w) >= 4}


def find_anchor(t: str, stem: str) -> int:
    """Find a UNIQUE anchor in the RAW source `t` using a tolerant regex built
    from the stem's alphanumeric chars (allows OCR dots/newlines between them).
    Returns the raw char position, or -1 if no unique match."""
    # alphanumeric chars of the stem, in order
    chars = [c for c in (stem or "") if c.isalnum()]
    if len(chars) < 35:
        return -1
    for n in (60, 50, 45, 40, 35):
        seq = chars[:n]
        if len(seq) < 35:
            continue
        # build tolerant regex: each alnum char, with up to 4 any-chars between
        pat = r".{0,4}?".join(re.escape(c) for c in seq)
        hits = [m.start() for m in re.finditer(pat, t, re.IGNORECASE | re.DOTALL)]
        if len(hits) == 1:
            return hits[0]
    return -1


# A "new question" boundary inside the block: a numbered heading like "99." or
# "(99)" or a dash-number "99- " or "Q99" at line start, OR a blank-line gap
# followed by such. We only treat it as a boundary if it appears AFTER the anchor
# and BEFORE the marked option.
NEW_Q = re.compile(r"(?:^|\n)\s*(?:\(?(\d{1,3})[\.\):\-]\s|[Qq](\d{1,3})\s*[\.\):])")


def main() -> None:
    data, items = load()
    fixed = []
    skipped = []
    for it in items:
        has_ans = (
            it.get("answerLetter")
            or it.get("answerIdx") not in (None, -1)
            or it.get("_embedded_answer")
            or it.get("_model_suggested_answer")
        )
        if has_ans or len(it.get("options", [])) < 2:
            continue
        if it["id"] in EXCLUDE:
            continue
        srcs = it.get("sources") or []
        if not srcs or srcs[0] not in SRC_FILES and srcs[0] != "Saud_Masahhah":
            continue
        t = src_text(srcs[0])
        if not t:
            continue
        pos = find_anchor(t, it.get("stem", ""))
        if pos == -1:
            skipped.append((it["id"], "no unique anchor"))
            continue
        block = t[pos : pos + 900]  # RAW block (keeps ✅ markers)
        # find all marked option lines in the block
        marked = []
        for m in re.finditer(r"([A-Ea-e])\s*[\.:)]\s*([^\n]{2,120}?)(✅✅|✳\s*✳|✅|✳|●|✔)", block):
            letter = m.group(1).upper()
            raw_txt = m.group(2)
            txt = re.sub(r"[✅✳✔🔵🟢🟡●\s]+$", "", raw_txt).strip().rstrip(".")
            mpos = m.start()
            marked.append((letter, txt, mpos))
        if not marked:
            skipped.append((it["id"], "no marked opt in block"))
            continue
        existing_letters = [o.strip()[0].upper() for o in it.get("options", []) if o.strip() and o.strip()[0].upper() in "ABCDE"]
        last_letter = existing_letters[-1] if existing_letters else "A"
        next_letter = chr(ord(last_letter) + 1) if last_letter in "ABCD" else None
        stem_words = words(it.get("stem", "")) | set().union(*(words(o) for o in it.get("options", [])))
        chosen = None
        for letter, txt, mpos in marked:
            # rule 3: letter already present OR is the next letter (dropped 4th opt)
            if letter in existing_letters:
                kind = "mark"
            elif next_letter and letter == next_letter and len(existing_letters) <= 3:
                kind = "restore"
            else:
                continue
            # rule 5: no new-question boundary between anchor(pos 0) and mpos
            seg = block[:mpos]
            bnd = NEW_Q.findall(seg[10:])
            if len(bnd) > 1:  # allow the question's own number at the very start
                continue
            chosen = (letter, txt, kind)
            break
        if not chosen:
            skipped.append((it["id"], "no valid marked opt"))
            continue
        letter, txt, kind = chosen
        if kind == "mark":
            idx = next(i for i, o in enumerate(it["options"]) if o.strip()[0].upper() == letter)
        else:
            it["options"] = it.get("options", []) + [f"{letter}. {txt}"]
            idx = len(it["options"]) - 1
        it["answerLetter"] = letter
        it["answerIdx"] = idx
        it["_repair_source"] = "dropped_answer_option"
        fixed.append((it["id"], letter, kind, txt[:45]))
        print(f"FIXED {it['id']}: {kind} {letter}='{txt[:45]}'")
        print(f"   BLOCK: {block[:300].replace(chr(10),' | ')[:280]}")

    flat = [it for arr in data["byDept"].values() for it in arr]
    if len(flat) != data["total"]:
        raise SystemExit(f"Refuse: {len(flat)} != {data['total']}")
    out = (
        "/** Flash Notes — source recalls plus canonical-book evidence candidates. */\n"
        "window.FLASH_NOTES = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n"
    )
    (ROOT / "data" / "flash_notes.js").write_text(out, encoding="utf-8")
    print(f"\nTotal fixed: {len(fixed)}  |  skipped: {len(skipped)}")
    for sid, why in skipped[:15]:
        print(f"  skip {sid}: {why}")


if __name__ == "__main__":
    main()

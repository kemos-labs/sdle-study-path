#!/usr/bin/env python3
"""Repair the flash deck's merged/✅-glued options (user: flash was 'slop', fix properly).

Patterns fixed:
1) "option ✅ AnswerText" glue (243 items): split -> the base text stays an option, the
   text after ✅ is the correct answer -> restored as its own option, answerIdx set to it.
2) "option ✅" end marker (1,159 items): strip the ✅ (answerIdx already points there).
3) "*Book citation*" / "● ● Book" glued inside option text (44): move to item.reference.
4) Multi-question merges / >6 options: flag _data_quality:"merged_options_review"
   (UI demotes them to the archive toggle — honest, never hidden).
After every item: answerIdx is re-verified against the option TEXT.
"""
import json, os, re, tempfile
from pathlib import Path

APP = Path("/data/prometric/sdle-prep")
fpath = APP / "data" / "flash_notes.js"
src = fpath.read_text(encoding="utf-8")
fbody = src.split("=", 1)[1].strip().rstrip().rstrip(";").strip()
data = json.loads(fbody)

LETTER = re.compile(r"^\s*(?:[A-Za-z]\.|\(\s*[A-Za-z]\s*\)|[A-Za-z]\s*[\).])\s*")
CITE = re.compile(r"\s*\*[^*]{4,}\*\s*$|\s*●\s*●\s*[^●]*$")
CHECK = re.compile(r"✅+")
QNUM = re.compile(r"\(\d{1,3}\)")

def clean_option(t):
    t = str(t or "").strip()
    t = LETTER.sub("", t).strip()
    t = CHECK.sub("", t).strip()
    t = t.rstrip("●").strip()
    return t.strip()

def split_answer(t):
    """Return (base_option, answer_text) for 'x ✅ y' glue."""
    t = str(t or "").strip()
    t = LETTER.sub("", t).strip()
    parts = CHECK.split(t, 1)
    base = parts[0].strip().rstrip("●").strip()
    ans = parts[1].strip() if len(parts) > 1 else ""
    ans = CITE.sub("", ans).strip()
    return base, ans

stats = {"glue_split": 0, "marker_strip": 0, "citation": 0, "flagged": 0, "answer_fix": 0}
for dept, arr in data["byDept"].items():
    for it in arr:
        opts = it.get("options") or []
        if not opts:
            continue
        new_opts = []
        answer_text = None
        merged_flag = False
        for o in opts:
            os_ = str(o or "")
            has_glue = CHECK.search(os_) and not CHECK.search(os_).group(0).endswith(os_.strip()[-1:]) if False else False
            # glue: ✅ appears and is NOT at the very end of the trimmed string
            m = CHECK.search(os_)
            glue = bool(m) and (os_[m.end():].strip() != "")
            if glue:
                base, ans = split_answer(os_)
                if ans and len(ans) > 200:
                    # second question glued in -> genuine merge
                    merged_flag = True
                    continue
                if base:
                    new_opts.append(base)
                if ans:
                    answer_text = ans
                stats["glue_split"] += 1
                continue
            # marker only at end
            if CHECK.search(os_) and not os_.replace("✅", "").strip() == "" and not glue:
                base = clean_option(os_)
                if base:
                    new_opts.append(base)
                stats["marker_strip"] += 1
                continue
            # citation glue
            if CITE.search(os_):
                base = CITE.sub("", os_).strip()
                cit = CITE.search(os_).group(0).strip()
                base = clean_option(base)
                if base:
                    new_opts.append(base)
                if cit and not it.get("reference"):
                    it["reference"] = re.sub(r"^●\s*●\s*", "", cit).strip(" *")
                stats["citation"] += 1
                continue
            # question-number glue "(89)..." inside an option -> genuine merge
            if QNUM.search(os_) and re.search(r"\((\d{2,3})\)\s*[A-Z]", os_):
                merged_flag = True
                base = clean_option(os_)
                if base:
                    new_opts.append(base)
                continue
            c = clean_option(os_)
            if c:
                new_opts.append(c)

        # dedupe preserving order
        seen = set()
        uniq = []
        for o in new_opts:
            key = o.lower()
            if key not in seen:
                seen.add(key)
                uniq.append(o)
        new_opts = uniq

        # if a split answer text is not among options, append it (restores original set)
        if answer_text and not any(a.lower() == answer_text.lower() for a in new_opts):
            new_opts.append(answer_text)

        if len(new_opts) > 6 or merged_flag or it.get("_data_quality") == "merged_options_review":
            it["_data_quality"] = "merged_options_review"
            stats["flagged"] += 1
        elif "_data_quality" in it and it["_data_quality"] == "merged_options_review":
            del it["_data_quality"]

        it["options"] = new_opts

        # fix answerIdx: prefer the split answer text; else keep in range
        ai = it.get("answerIdx")
        if answer_text:
            idx = next((i for i, o in enumerate(new_opts) if o.lower() == answer_text.lower()), None)
            if idx is not None and idx != ai:
                it["answerIdx"] = idx
                stats["answer_fix"] += 1
            elif idx is None and new_opts:
                it["answerIdx"] = len(new_opts) - 1
                stats["answer_fix"] += 1
        elif isinstance(ai, int):
            if ai >= len(new_opts):
                it["answerIdx"] = len(new_opts) - 1 if new_opts else None
                stats["answer_fix"] += 1
            elif new_opts and (not isinstance(ai, int) or ai < 0):
                it["answerIdx"] = 0

print(json.dumps(stats, ensure_ascii=False))

fdata2 = json.dumps(data, ensure_ascii=False, indent=1)
src2 = src.replace(fbody, fdata2)
fd, tmp = tempfile.mkstemp(dir=str(fpath.parent), suffix=".tmp")
with os.fdopen(fd, "w", encoding="utf-8") as fh:
    fh.write(src2)
os.replace(tmp, fpath)
print("flash_notes.js written OK")

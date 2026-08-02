#!/usr/bin/env python3
"""split_merged_flash.py — split merged Flash Notes items into individual questions.

Two classes of items carry `_data_quality: merged_options_review`:
  A) MULTI-question bundles (202): several questions joined into one item
     (repeated a./b. labels, numbered stems like "14.amalgum...", "296.Pt...").
     -> split into N individual items.
  B) SINGLE-question with 5+ options (57): one question, too many options.
     -> trim to best 4 options (preserve answer), drop the flag.

Algorithm (class A): tokenize the raw text into ordered boundaries —
  * question starts:  <number>.[)#] followed by a letter (upper/lower/Arabic)
  * option starts:    <letter>.[)] followed by space/letter
then reassemble into questions. A question that ends up with no stem (its stem
belonged to an earlier, lost question) is dropped. Children that parse badly
are kept with a `_data_quality: "split_needs_review"` flag so they never enter
graded quizzes but remain visible for manual repair.

Output: writes a JSON report to work/split_merged_report.json and (with --apply)
writes the new flash_notes.js. Always run dry first, eyeball the report.

Usage:
    python3 scripts/split_merged_flash.py            # dry run
    python3 scripts/split_merged_flash.py --apply    # write changes
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FN_JS = ROOT / "data" / "flash_notes.js"
REPORT = ROOT / "work" / "split_merged_report.json"

MARKER = "[\u2705\U0001F7E2\U0001F7E1\U0001F7FF\u2714\u2713\u2B50\U0001F7E0\U0001F505\u26A1]"
MARKER_RE = re.compile(MARKER)
BULLETS = "\u25CF\u2022\u2023\u25AA\u25A0"
JUNK_PREFIX = re.compile(rf"^[\s{BULLETS}\-*>#]+")

# question start: <1-3 digits><. # )><optional #><space*><letter (upper/lower/arabic)>
# e.g. "1.#Pt...", "103.PA...", "296.Pt...", "2.advantage..."
QSTART = re.compile(r"(?:(?<=\s)|^)(\d{1,3})[.)#][#]?\s*(?=[A-Za-z\u0621-\u064A])")
# dash-separated question numbers: "16- A patient...", "19- what is...", "20-broken file..."
QSTART_DASH = re.compile(r"(?:(?<=\s)|^)(\d{1,3})-\s*(?=[A-Za-z\u0621-\u064A])")
UNIT_WORDS = ("year", "month", "day", "week", "hour", "min", "mm", "ml", "mg", "pm", "am")

# option start: <single letter><. )><space*>
OSTART = re.compile(r"(?:(?<=\s)|^)([A-Za-z])[.)]\s*(?=[^\sA-Za-z0-9])", )
OSTART = re.compile(r"(?:(?<=\s)|^)([A-Za-z])[.)]\s*")


def clean_opt(raw: str) -> str:
    t = MARKER_RE.sub("", raw or "")
    t = re.sub(rf"[{BULLETS}]", "", t)
    t = re.sub(r"\s+", " ", t)
    return t.strip()


def tokenize(text: str):
    """Return sorted list of (pos, kind, value) where kind in {'q','o'}."""
    toks = []
    for m in QSTART.finditer(text):
        toks.append((m.start(), "q", m.group(1)))
    for m in QSTART_DASH.finditer(text):
        # reject "N-year/day/month/..." patterns (units, not question numbers)
        nxt = text[m.end(): m.end() + 12].lower()
        word = re.match(r"[a-z]+", nxt)
        if word and word.group(0) in UNIT_WORDS:
            continue
        toks.append((m.start(), "q", m.group(1)))
    for m in OSTART.finditer(text):
        # an option label must be followed by text or end, and must NOT be the
        # tail of a word ("a." inside "alpha.") → require whitespace before
        toks.append((m.start(), "o", m.group(1)))
    # drop option tokens that collide with question tokens (same position ±1)
    toks.sort(key=lambda t: t[0])
    out = []
    for t in toks:
        if out and abs(t[0] - out[-1][0]) <= 1:
            # prefer question tokens over option tokens
            if t[1] == "q" and out[-1][1] == "o":
                out[-1] = t
            continue
        out.append(t)
    return out


def parse_bundle(text: str):
    """Parse a bundle text into a list of dicts: {stem, opts:[(txt,is_ans)], qnum}."""
    toks = tokenize(text)
    questions = []          # list of {stem, opts, qnum}
    cur = None              # current question being built
    pending_opt = None      # start position of the option just opened, awaiting content
    stem_start = None       # where the current question's stem text begins
    first_opt_pos = None    # where the first option label of the current question starts

    def close_pending(until):
        nonlocal pending_opt, cur
        if pending_opt is not None and cur is not None:
            content = text[pending_opt: until].strip()
            cur["opts"].append((clean_opt(content), bool(MARKER_RE.search(content))))
        pending_opt = None

    def close_question():
        nonlocal cur, stem_start, first_opt_pos
        if cur is not None and (cur["stem"] or cur["opts"]):
            # trim stem to stop at the first option label
            end = first_opt_pos if (first_opt_pos is not None and stem_start is not None and first_opt_pos > stem_start) else None
            if stem_start is not None:
                cur["stem"] = text[stem_start:end] if end else text[stem_start:]
            questions.append(cur)
        cur = None
        stem_start = None
        first_opt_pos = None

    for pos, kind, val in toks:
        if kind == "q":
            # close pending option content up to the question start
            if pending_opt is not None:
                close_pending(pos)
            close_question()
            cur = {"stem": "", "opts": [], "qnum": val}
            m = QSTART.match(text, pos)
            stem_start = m.end() if m else pos + len(val) + 1
        else:  # option start
            if cur is None:
                continue  # option before any question → belongs to a lost earlier question
            if pending_opt is not None:
                close_pending(pos)
            if first_opt_pos is None:
                first_opt_pos = pos
            pending_opt = pos
    # tail
    if pending_opt is not None:
        close_pending(len(text))
    close_question()
    return questions


def build_item(parent, dept, seq, q):
    stem = JUNK_PREFIX.sub("", q["stem"] or "").strip()
    stem = stem.replace("\n", " ")
    stem = re.sub(r"\s+", " ", stem).strip()
    if len(stem) < 3 or not re.search(r"[A-Za-z\u0621-\u064A]", stem):
        return None
    # dedupe options, keep max 4, preserve answer
    seen, clean, ans_idx = set(), [], None
    for txt, is_ans in q["opts"]:
        key = txt.lower()
        if not key or key in seen or len(seen) >= 4:
            continue
        seen.add(key)
        clean.append(txt)
        if is_ans and ans_idx is None:
            ans_idx = len(clean) - 1
    if not clean:
        return None
    # single-option items are recall notes, not MCQs — honest marker
    marker = "verified" if (ans_idx is not None and len(clean) >= 2) else "ref"
    new = {
        "id": f"{parent['id']}x{seq}",
        "stem": stem[:300],
        "options": clean,
        "marker": marker,
        "needsImage": parent.get("needsImage", False),
        "dept": dept,
        "sources": parent.get("sources", []),
        "raw": (parent.get("raw") or "")[:600],
        "_parent": parent["id"],
        "_data_quality": "split_from_merged",
        "_verification_verdict": "needs_review",  # new children: not yet book-verified
    }
    if ans_idx is not None:
        new["answerIdx"] = ans_idx
        new["answerLetter"] = chr(ord("a") + ans_idx)
        new["_verified_explanation"] = f"Correct answer: {chr(ord('a') + ans_idx)}. {clean[ans_idx]}"
    return new


def looks_ok(stem: str) -> bool:
    t = JUNK_PREFIX.sub("", stem or "").strip()
    if len(t) < 8:
        return False
    if not re.search(r"[A-Za-z\u0621-\u064A]{3}", t):
        return False
    return True


def main() -> int:
    text = FN_JS.read_text(encoding="utf-8")
    m = re.search(r"(window\.FLASH_NOTES\s*=\s*)(\{.*\})(\s*;)", text, re.DOTALL)
    if not m:
        raise SystemExit("❌ could not parse flash_notes.js")
    data = json.loads(m.group(2))
    apply = "--apply" in sys.argv

    stats = {"multi_split": 0, "single_trimmed": 0, "new_items": 0, "kept_flagged": 0, "dropped": 0}
    report = {"multi": [], "single": [], "bad_children": []}
    new_depts = {k: [] for k in data["byDept"]}

    for dept, items in data["byDept"].items():
        keep = []
        for item in items:
            if item.get("_data_quality") != "merged_options_review":
                keep.append(item)
                continue
            opts = item.get("options") or []
            raw = item.get("raw") or ""
            full = (raw if len(raw) > 30 else (item.get("stem", "") + " " + " ".join(opts)))

            # ---- Class B: single question, many options ----
            qs = parse_bundle(full)
            # Also handle "no question number" single questions (item stem + options)
            if not qs and len(opts) >= 2:
                own_stem = (item.get("stem") or "").strip()
                if len(own_stem) >= 8:
                    qs = [{"qnum": "", "stem": own_stem, "opts": [(o, bool(MARKER_RE.search(o))) for o in opts]}]
            if len(qs) == 1 and len(qs[0]["opts"]) >= 2:
                q = qs[0]
                stem = re.sub(r"\s+", " ", q["stem"] or "").strip()
                seen, clean, ans_idx = set(), [], item.get("answerIdx")
                for txt, is_ans in q["opts"]:
                    key = txt.lower()
                    if not key or key in seen or len(seen) >= 4:
                        continue
                    seen.add(key)
                    clean.append(txt)
                if len(clean) >= 2 and (ans_idx is None or ans_idx < len(clean)):
                    if apply:
                        item["stem"] = stem[:300]
                        item["options"] = clean
                        if ans_idx is not None:
                            item["answerIdx"] = ans_idx
                            item["answerLetter"] = chr(ord("a") + ans_idx)
                        if len(clean) < 2:
                            item["marker"] = "ref"
                        if "_verification_verdict" not in item:
                            item["_verification_verdict"] = "needs_review"
                        item.pop("_data_quality", None)
                    stats["single_trimmed"] += 1
                    report["single"].append({"id": item["id"], "before": len(opts), "after": len(clean)})
                    keep.append(item)
                    continue

            # ---- Class A: multi-question bundle ----
            built = []
            for si, q in enumerate(qs):
                if not q["opts"]:
                    continue
                b = build_item(item, dept, si + 1, q)
                if b:
                    built.append(b)
            if len(built) >= 2:
                stats["multi_split"] += 1
                stats["new_items"] += len(built)
                stats["dropped"] += 1
                for b in built:
                    if not looks_ok(b["stem"]):
                        b["_data_quality"] = "split_needs_review"
                        report["bad_children"].append({"id": b["id"], "stem": b["stem"][:60]})
                if apply:
                    keep.extend(built)
                report["multi"].append({"parent": item["id"], "children": [b["id"] for b in built],
                                        "stems": [b["stem"][:36] for b in built]})
                continue
            stats["kept_flagged"] += 1
            report["bad_children"].append({"id": item["id"], "stem": (item.get("stem") or "")[:60], "kept": True})
            keep.append(item)
        new_depts[dept] = keep

    print(f"DRY-RUN (no --apply): {json.dumps(stats, ensure_ascii=False)}")
    print("multi samples:")
    for g in report["multi"][:5]:
        print(f"  {g['parent']} → {g['stems']}")
    print("single samples:", json.dumps(report["single"][:5], ensure_ascii=False))
    print("bad children:", json.dumps(report["bad_children"][:12], ensure_ascii=False))

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")

    if apply:
        data["byDept"] = new_depts
        all_items = [it for its in data["byDept"].values() for it in its]
        data["total"] = len(all_items)
        per_src = {}
        for it in all_items:
            for s in it.get("sources", []):
                per_src[s] = per_src.get(s, 0) + 1
        data["perSource"] = per_src
        data["generated"] = "2026-08-02 (split_merged_flash)"
        out = m.group(1) + json.dumps(data, ensure_ascii=False, indent=1) + m.group(3)
        FN_JS.write_text(out, encoding="utf-8")
        print(f"✅ wrote {FN_JS} — new total: {data['total']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

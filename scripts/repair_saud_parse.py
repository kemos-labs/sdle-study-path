#!/usr/bin/env python3
"""
repair_saud_parse.py — repair the Saud_Masahhah fragments in flash_notes.js.

Root cause: build_flash_notes.parse_sectioned treated every "- " bullet as a
new item AND numbered questions use a dash ("31- Q") which didn't match the
numbered-start regex. Result: 1,285 fragment items (bullet answers split from
their questions, question stems contaminated with the previous answer block).

Fix: re-parse the source .md with a corrected parser (dash-numbered questions
start items; "- " bullets become OPTIONS of the current item), then reconcile
in place:
  - parents get real options + clean stems (kept IDs)
  - pure bullet fragments get _merged_into (parent id) + _is_option metadata
  - total item count stays 4,026 (no add/remove)

Dry-run: python3 scripts/repair_saud_parse.py --dry
Apply:    python3 scripts/repair_saud_parse.py --apply
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path
from difflib import SequenceMatcher

ROOT = Path("/data/prometric")
PREP = ROOT / "sdle-prep"
SRC = ROOT / "sdle-ref" / "focus" / "����ملف_سعود_مصحح��.md"
FN_FILE = PREP / "data" / "flash_notes.js"

# --- reused parser pieces from build_flash_notes.py -------------------------
LETTER = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4}
OPTION_RE = re.compile(r"(?i)\b([A-E])\s*[\.:\)]\s*([^\nA-E]+?)(?=\s+[A-E]\s*[\.:\)]\s|\s*$)")
OPTION_START = re.compile(r"(?i)\bA\s*[\.:\)]\s+\S")

def marker_for(text: str) -> str:
    if "✅✅" in text or "✅" in text: return "verified"
    if "✳ ✳" in text or "✳✳" in text: return "ref"
    if "🟢" in text: return "given"
    if "🟡" in text: return "ref"
    if "🔵" in text or "🟦" in text: return "readmore"
    if "🔁" in text: return "unsure"
    return "unknown"

def extract_options(block: str) -> list[tuple[str, str]]:
    opts = [(m.group(1), m.group(2).strip()) for m in OPTION_RE.finditer(block) if m.group(2).strip()]
    if len(opts) >= 2: return opts
    out = []
    for m in re.finditer(r"(?im)^\s*([A-Ea-e])\s*[\.:\)]\s*(\S.+)$", block):
        out.append((m.group(1), m.group(2).strip()))
    return out

def find_marked_answer(opts: list[tuple[str, str]], block: str) -> tuple[str | None, int | None]:
    for letter, txt in opts:
        if "✅✅" in txt or "✅" in txt or "🟢" in txt or "🟡" in txt or "✳" in txt:
            return letter, LETTER.get(letter, -1)
    return None, None

def split_stem_opts(body: str) -> tuple[str, str]:
    m = OPTION_START.search(body)
    if m:
        return body[:m.start()].strip(), body[m.start():].strip()
    m2 = re.search(r"(?m)^\s*([A-Ea-e])\s*[\.:\)]\s+", body)
    if m2:
        return body[:m2.start()].strip(), body[m2.start():].strip()
    return body.strip(), ""

def split_inline_opts(text: str) -> tuple[str, list[tuple[str, str]]]:
    """Split 'A. x B. y C. z' (single line) into stem + [(letter, text)].
    Robust: needs >=2 markers; letters are standalone (word-boundary, followed
    by space). Does NOT rely on the buggy (?i) OPTION_RE."""
    pat = re.compile(r"(?:^|[\s(])([A-E])\s*[\.:)]\s+")
    ms = list(pat.finditer(text))
    if len(ms) < 2:
        return text.strip(), []
    stem = text[:ms[0].start()].strip()
    opts = []
    for i, m in enumerate(ms):
        start = m.end()
        end = ms[i + 1].start() if i + 1 < len(ms) else len(text)
        t = text[start:end].strip()
        if t:
            opts.append((m.group(1), t))
    return stem, opts

# --- fixed parser ------------------------------------------------------------
NUM_HEAD = re.compile(r"^\s*(?:\((\d{1,3})\)|(\d{1,3}))\s*[-\.:\)]\s+(.+)$")
Q_HEAD = re.compile(r"^\s*[Qq]\s*\d+\s*[:\.\)\-]\s*(.+)$")
BULLET = re.compile(r"^\s*[●\-•]\s*(.*)$")

def parse_fixed() -> list[dict]:
    text = SRC.read_text(encoding="utf-8", errors="replace")
    items, cur = [], None
    # question start: line starts with a digit-numbered marker requiring
    # whitespace after the marker ("31- text", "1. text", "2: text"), OR a
    # Qn marker with optional bullet prefix ("Q3: text", "● Q3: text",
    # "- Q2) text").  Plain bullets ("- 5-year-old...") are options, NOT
    # questions.
    QNUM = re.compile(r"^\s*\d{1,3}\s*[-.:)]\s+\S")
    QHEAD = re.compile(r"^\s*(?:[\u25cf\-\u2022]\s*)?Q\s*\d*\s*[:.)\-]\s*\S")
    # bullet/option line: leading dash/star that is NOT a question start
    for ln in text.split("\n"):
        s = ln.strip()
        if not s:
            continue
        if QNUM.match(s) or QHEAD.match(s):
            if cur: items.append(cur)
            # strip the leading bullet marker if present (Qn case)
            s2 = re.sub(r"^[●\-•]\s*", "", s)
            cur = {"stem": s2.strip(), "opts": []}
            continue
        m = BULLET.match(s)
        if m and cur is not None:
            opt = m.group(1).strip()
            if opt:
                cur["opts"].append(opt)
            continue
        if cur is not None:
            cur["stem"] += " " + s
    if cur: items.append(cur)
    return [it for it in items if len(it["stem"]) >= 6]

def norm(s: str) -> str:
    """Normalize for matching: lowercase, strip markers/numbers/punct."""
    s = re.sub(r"[✅🟢🟡✳🔵🟦🔁●•]+", " ", s)
    s = re.sub(r"[^a-z0-9 ]", " ", s.lower())
    s = re.sub(r"\s+", " ", s).strip()
    return s

def ratio(a: str, b: str) -> float:
    na, nb = norm(a), norm(b)
    if not na or not nb: return 0.0
    if na == nb: return 1.0
    return SequenceMatcher(None, na, nb).ratio()

def _tokens(s: str) -> set:
    return set(norm(s).split())

def _quick_ratio(sa: set, sb: set) -> float:
    """Jaccard-ish overlap on token sets — fast prefilter for SequenceMatcher."""
    if not sa or not sb: return 0.0
    inter = len(sa & sb)
    return inter / max(len(sa), len(sb))

def _best_match(target_tokens: set, target_text: str, candidates: list[tuple]) -> tuple[object, float, float]:
    """candidates = list of (tokenset, text, payload). Returns (payload, jaccard, exact).
    Jaccard is the primary score (fast); SequenceMatcher only on top-5."""
    scored = []
    for ts, txt, payload in candidates:
        if not ts or not target_tokens:
            continue
        inter = len(target_tokens & ts)
        j = inter / max(len(target_tokens), len(ts))
        if j >= 0.4:
            scored.append((j, txt, payload))
    scored.sort(key=lambda x: -x[0])
    if not scored:
        return None, 0.0, 0.0
    # refine top-5 with SequenceMatcher
    best_p, best_j, best_e = scored[0][2], scored[0][0], 0.0
    for j, txt, payload in scored[:5]:
        e = ratio(target_text, txt)
        if e > best_e:
            best_p, best_j, best_e = payload, j, e
    return best_p, best_j, best_e

def load_fn() -> dict:
    text = FN_FILE.read_text(encoding="utf-8")
    m = re.search(r"window\.FLASH_NOTES\s*=\s*(\{.*);", text, re.DOTALL)
    return json.loads(m.group(1))

def save_fn(data: dict):
    out = ("/** Flash Notes — source recalls plus canonical-book evidence candidates. */\n"
           "window.FLASH_NOTES = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n")
    FN_FILE.write_text(out, encoding="utf-8")

def _build_output(c: dict) -> tuple[str, list, tuple | None]:
    """Compute final (stem, options, answer) for a consolidated item —
    the exact transforms applied in --apply mode."""
    stem = c["stem"]
    stem = re.sub(r"^[●\-•]\s*", "", stem).strip()
    stem = re.sub(r"^(?:Q\s*\d*\s*[:.)\-]|\d{1,3}\s*[-.:)])\s*", "", stem).strip()
    stem = re.sub(r"\s*[●]\s*$", "", stem).strip()
    # 1) try inline options on the whole stem ("A. x B. y C. z" on one line)
    inline_stem, inline_opts = split_inline_opts(stem)
    if inline_opts:
        stem = re.sub(r"\s+", " ", inline_stem).strip()[:400]
        opts = []
        if c["opts"]:
            ex = extract_options("\n".join(c["opts"]))
            if len(ex) >= 2:
                opts = [f"{l}. {t}" for l, t in ex]
            else:
                opts = [f"{chr(97+i)}. {t}" for i, t in enumerate(c["opts"][:5])]
        for l, t in inline_opts:
            if len(opts) < 5:
                opts.append(f"{l}. {t}")
        block = "\n".join(c["opts"]) + "\n" + stem + "\n" + "\n".join(f"{l}. {t}" for l, t in inline_opts)
        ans = (None, None)
        if opts:
            pairs = [(o.split(". ", 1)[0].lower(), o.split(". ", 1)[-1]) for o in opts]
            ans = find_marked_answer(pairs, block)
        return stem, opts, ans
    # 2) fallback: split_stem_opts (multi-line lettered options)
    s_txt, s_opt = split_stem_opts(stem)
    stem = re.sub(r"\s+", " ", s_txt).strip()[:400]
    opts = []
    if c["opts"]:
        ex = extract_options("\n".join(c["opts"]))
        if len(ex) >= 2:
            opts = [f"{l}. {t}" for l, t in ex]
        else:
            opts = [f"{chr(97+i)}. {t}" for i, t in enumerate(c["opts"][:5])]
    if s_opt:
        ex2 = extract_options(s_opt)
        for l, t in ex2:
            if len(opts) < 5:
                opts.append(f"{l}. {t}")
    block = "\n".join(c["opts"]) + "\n" + s_opt
    ans = (None, None)
    if opts:
        pairs = [(o.split(". ", 1)[0].lower(), o.split(". ", 1)[-1]) for o in opts]
        ans = find_marked_answer(pairs, block)
    return stem, opts, ans

def main():
    dry = "--apply" not in sys.argv
    consolidated = parse_fixed()
    print(f"Fixed parse: {len(consolidated)} questions, "
          f"{sum(len(c['opts']) for c in consolidated)} options absorbed")

    data = load_fn()
    items = [it for items in data["byDept"].values() for it in items]
    saud = [it for it in items if "Saud_Masahhah" in it.get("sources", [])]
    print(f"Existing Saud items: {len(saud)}")

    # --- map consolidated questions to existing items ---------------------
    # ONE fast pass: each existing Saud item finds its best consolidated
    # question (by tail chunk similarity). Accept score >= 0.4.
    cons_cands = []  # (tokenset, text, ci)
    for ci, c in enumerate(consolidated):
        cons_cands.append((_tokens(c["stem"]), c["stem"], ci))

    def _existing_tails(it):
        st = it.get("stem", "")
        tails = [st]
        for sep in ["?", "\n"]:
            if sep in st:
                tails.append(st.rsplit(sep, 1)[-1])
        return tails

    qmap = []  # (consolidated_idx, existing_item)
    used_items = set()
    for it in saud:
        tails = _existing_tails(it)
        best_ci, best_r = None, 0.0
        for t in tails:
            if not norm(t): continue
            payload, j, e = _best_match(_tokens(t), t, cons_cands)
            if payload is not None and e > best_r:
                best_ci, best_r = payload, e
        if best_ci is not None and best_r >= 0.4:
            qmap.append((best_ci, it))
            used_items.add(id(it))

    print(f"Consolidated questions matched to existing items: {len(qmap)} "
          f"(score>=0.4)")

    # --- fragments: bullet-only items that match an option of a parent -----
    opt_cands = []  # (tokenset, text, (ci, oi))
    for ci, c in enumerate(consolidated):
        for oi, o in enumerate(c["opts"]):
            nt = norm(o)
            if len(nt) >= 3:
                opt_cands.append((_tokens(o), o, (ci, oi)))
    frag_merged = 0
    frag_no_match = 0
    for it in saud:
        if id(it) in used_items: continue
        st = norm(it.get("stem", ""))
        if len(st) < 3: continue
        payload, q, r = _best_match(_tokens(it.get("stem", "")), it.get("stem", ""), opt_cands)
        if payload is not None and r >= 0.75:
            ci, oi = payload
            it["_is_option"] = True
            it["_option_of_consolidated"] = ci
            it["_option_text"] = consolidated[ci]["opts"][oi]
            frag_merged += 1
        else:
            frag_no_match += 1

    print(f"Fragments tagged as options: {frag_merged}")
    print(f"Fragments unmatched: {frag_no_match}")

    # --- report what would change ------------------------------------------
    rewritten = 0
    for ci, it in qmap:
        c = consolidated[ci]
        old_opts = len(it.get("options", []))
        stem2, new_opts, ans2 = _build_output(c)
        if new_opts and len(new_opts) != old_opts:
            rewritten += 1
    print(f"Parents that would gain options: {rewritten}")

    if dry:
        print("\n[DRY RUN] no changes written.")
        shown = 0
        for ci, it in qmap:
            if shown >= 6: break
            c = consolidated[ci]
            stem2, new_opts, ans2 = _build_output(c)
            print("\n" + "=" * 70)
            print(f"OLD id={it['id']}: {it['stem'][:90]!r}")
            print(f"NEW stem: {stem2[:90]!r}")
            print(f"NEW opts: {[o[:40] for o in new_opts[:6]]}")
            print(f"NEW answer: {ans2}")
            shown += 1
        return

    # --- apply: rewrite matched parents -------------------------------------
    for ci, it in qmap:
        c = consolidated[ci]
        stem2, new_opts, ans2 = _build_output(c)
        ans_letter, ans_idx = ans2
        # PRESERVE existing good options — the consolidated inline parse can
        # miss options that were already extracted correctly. Only replace when
        # the existing item had <2 options (true fragment).
        old_opts = it.get("options", []) or []
        old_ans_letter = it.get("answerLetter")
        old_ans_idx = it.get("answerIdx")
        old_ans_ok = (old_ans_idx is not None and 0 <= old_ans_idx < len(old_opts))
        if len(old_opts) >= 2 and not new_opts:
            new_opts = list(old_opts)
        elif len(old_opts) >= 2 and new_opts:
            # merge: keep old options, add any new ones not present
            seen = {re.sub(r"^[a-eA-E][.)]\s*", "", o).strip().lower() for o in old_opts}
            merged = list(old_opts)
            for o in new_opts:
                key = re.sub(r"^[a-eA-E][.)]\s*", "", o).strip().lower()
                if key and key not in seen:
                    merged.append(o)
                    seen.add(key)
            new_opts = merged[:5]
            # re-index letters to positions
            new_opts = [f"{chr(97+i)}. {re.sub(r'^[a-eA-E][.)]\s*', '', o).strip()}"
                        for i, o in enumerate(new_opts)]
        it["stem"] = stem2
        it["options"] = new_opts
        # keep old valid answer; otherwise use newly found one
        if old_ans_ok and len(new_opts) > (old_ans_idx if old_ans_idx is not None else 0):
            it["answerLetter"] = old_ans_letter
            it["answerIdx"] = old_ans_idx
        elif ans_letter:
            it["answerLetter"] = ans_letter
            it["answerIdx"] = ans_idx
        it["_repaired_2026"] = True
        it["_repair_source"] = "parse_saud_fixed"

    # fragments: point at the consolidated parent index; resolve to item id
    # after parents are rewritten (build id lookup from CLEANED stems)
    id_by_norm = {}
    for it in items:
        n = norm(it.get("stem", ""))
        if n and n not in id_by_norm:
            id_by_norm[n] = it["id"]
    for it in saud:
        if it.get("_option_of_consolidated") is not None:
            ci = it["_option_of_consolidated"]
            c = consolidated[ci]
            stem2, _, _ = _build_output(c)
            parent_id = id_by_norm.get(norm(stem2))
            if parent_id:
                it["_merged_into"] = parent_id
            del it["_option_of_consolidated"]

    save_fn(data)
    print(f"Saved. Total items: {sum(len(v) for v in data['byDept'].values())}")

if __name__ == "__main__":
    main()

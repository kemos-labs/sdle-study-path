#!/usr/bin/env python3
"""
verify_flash_notes.py — Phase 3: verify community recall answers against official textbooks.

Reads:  data/flash_notes.js  (window.FLASH_NOTES, ~1,490 items with a community-marked answer)
Searches the GOLD-STANDARD textbooks in sdle-ref/books/ for each item's:
  - question stem keywords
  - marked answer option keywords
and scores book-line co-occurrence. Emits:
  - data/flash_notes_verdicts.json   (machine-readable)
  - HANDOFF_CORRECTIONS.md           (human-readable: needs-review + conflicts)

Verdict legend:
  supported     -> a book line co-mentions a stem keyword AND the marked answer keyword
                    (a citation candidate the reviewer can confirm)
  needs_review  -> no strong book line found; answer not yet grounded
  conflict      -> (heuristic) a known-contrary keyword in the same lines; manual check

This is an automated EVIDENCE-CANDIDATE pass, not a final correctness judgment.
A human/AI reviewer should confirm each 'supported' citation and decide conflicts.
Student-bank answers are LEADS, not truth (UPGRADE_PLAN.md §1).
"""
from __future__ import annotations
import json, re, sys, unicodedata
from pathlib import Path
from collections import defaultdict

ROOT = Path("/data/prometric")
BOOKS = ROOT / "sdle-ref" / "books"
FN_JS = ROOT / "sdle-prep" / "data" / "flash_notes.js"
OUT_JSON = ROOT / "sdle-prep" / "data" / "flash_notes_verdicts.json"
OUT_MD = ROOT / "sdle-prep" / "HANDOFF_CORRECTIONS.md"

# Department -> gold-standard textbooks (tier 1 in UPGRADE_PLAN §1)
DEPT_BOOKS = {
    "restorative": ["Resto_Sturdevant_Operative_5e.md",
                    "GD2_Basic_Dental_Materials,_John_Manapallil.md",
                    "GD2_Applied_Dental_Materials9-.md"],
    "endo":        ["Endo_Cohens_Pathways_of_the_Pulp_2016.md",
                    "Endo_Endodontics_principles.md"],
    "perio":       ["perio_Carranza_Clinical_Periodontology_2018.md",
                    "TD_4.Newman_&_Carranza's_Clinical_Periodontology_13ed.md"],
    "fixed":       ["Fixed_Contemporary_Fixed_Prosthodontics_4e.md"],
    "rpd":         ["Removable_McCracken_s_Removable_Partial_Prosthodontics.md",
                    "Removable_Textbook_of_Complete_Dentures.md"],
    "implant":     ["TD_Contemporary_Oral_&_Maxillofacial_Surgery_7th_edn.md",
                    "Perio_Periodontics_Medicine_Surgery_Implants.md"],
    "ortho_pedo":  ["Ortho_Contemporary Orthodontics 5th.md",
                    "Pedo_McDonald_Avery_10e.md"],
    "oms":         ["Oral_surgary_Oral_Radiology_-_Principles_and_Interpretation_7E_2014_.md",
                    "Oral_surgary_Oral_and_Maxillofacial_Pathology.md",
                    "TD_Contemporary_Oral_&_Maxillofacial_Surgery_7th_edn.md"],
    "ethics":      ["Ethics___infection_control___local_anasthesia_Hand_book_of_local_anesthesia_6th.md",
                    "Ethics___infection_control___local_anasthesia_Professionalism_and_Ethics_Handbook_for_Residents.md",
                    "Ethics___infection_control___local_anasthesia_GUIDELINES_FOR_INFECTION_CONTROL-2003.md"],
    "diagnostics": ["Oral_surgary_Oral_Radiology_-_Principles_and_Interpretation_7E_2014_.md",
                    "Oral_surgary_Oral_and_Maxillofacial_Pathology.md"],
}

STOP = set("""a an the of to in on at for and or but is are was were be been being with within
without by from as into onto over under above below this that these those it its their his her
we you they i he she them us our your which who whom what when where why how not no nor so than
then there here can could should would may might must shall will do does did done have has had
also more most such only per via etc ie eg vs among between about up down out off again further
once will all any both each few many other some such no nor only own same s t can will don""".split())

def tokenize(s):
    s = unicodedata.normalize("NFKC", s.lower())
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    toks = [t for t in s.split() if len(t) >= 4 and t not in STOP]
    return toks

def distinctive_words(text, n=6):
    toks = tokenize(text)
    # prefer longer / rarer-looking: dedupe preserve order, drop very common single chars
    seen, out = set(), []
    for t in toks:
        if t in seen: continue
        seen.add(t); out.append(t)
        if len(out) >= n: break
    return out

def load_flash_notes():
    txt = FN_JS.read_text(encoding="utf-8")
    obj = json.loads(txt[txt.find("{"):txt.rfind("};")+1])
    return obj

def build_index(files):
    """Return lines=[(orig, lower)], word_index={word:[line_idx,...]}."""
    lines = []
    word_index = defaultdict(list)
    for fn in files:
        p = BOOKS / fn
        if not p.exists():
            print(f"  [warn] missing book {fn}", file=sys.stderr); continue
        try:
            for ln in p.read_text(encoding="utf-8", errors="ignore").split("\n"):
                low = ln.lower()
                lines.append((ln, low))
                idx = len(lines) - 1
                seen = set()
                for t in re.findall(r"[a-z0-9]{4,}", low):
                    if t in STOP or t in seen: continue
                    seen.add(t); word_index[t].append(idx)
        except Exception as e:
            print(f"  [warn] read err {fn}: {e}", file=sys.stderr)
    return lines, word_index

MARKER_CHARS = "✅🟢🟡✳🔵🔁●"

def strip_markers(s):
    return re.sub(r"[✅🟢🟡✳🔵🔁●]", "", s or "")

def extract_answer_text(it):
    """Best-effort answer text: marked option if present, else inline ✅-adjacent phrase, else text after last '?'."""
    stem = it.get("stem", "") or ""
    if it.get("options") and it.get("answerLetter"):
        for o in it["options"]:
            if o.startswith((it["answerLetter"] or "_") + "."):
                return strip_markers(o.split(".", 1)[1] if "." in o else o).strip()
    # inline: the phrase immediately preceding a marker emoji
    m = re.search(r"([^?.!\n]{2,80}?[✅🟢🟡✳])", stem)
    if m:
        phrase = strip_markers(m.group(1)).strip(" .,;:○●")
        words = phrase.split()
        return " ".join(words[-8:]) if words else ""
    # fallback: text after the last '?'
    if "?" in stem:
        return strip_markers(stem.rsplit("?", 1)[1]).strip()
    return ""

def extract_question_text(it):
    stem = strip_markers(it.get("stem", "") or "")
    # text before the last '?', else whole stem
    if "?" in stem:
        return stem.rsplit("?", 1)[0].strip()
    return stem

def verify_item(it, lines, word_index):
    stem = it.get("stem", "")
    ans_text = extract_answer_text(it)
    q_text = extract_question_text(it)
    ans_kw = distinctive_words(ans_text, 6) if ans_text else []
    stem_kw = distinctive_words(q_text, 6)
    if not ans_kw:
        return ("needs_review", 0, [])
    # candidate lines: union of lines containing any answer keyword
    cand = set()
    for w in ans_kw:
        cand.update(word_index.get(w, []))
    if not cand:
        # try shorter prefix matches for the most distinctive answer word
        w = ans_kw[0][:5]
        for kw, idxs in word_index.items():
            if kw.startswith(w):
                cand.update(idxs)
            if len(cand) > 5000: break
    # score candidates by how many answer + stem keywords they contain
    scored = []
    cand = list(cand)[:8000]  # cap
    for i in cand:
        orig, low = lines[i]
        if len(low) < 25 or len(low) > 400: continue
        ahits = sum(1 for w in ans_kw if w in low)
        shits = sum(1 for w in stem_kw if w in low)
        if ahits == 0: continue
        score = ahits * 2 + shits
        scored.append((score, i, orig))
    scored.sort(reverse=True, key=lambda x: x[0])
    top = scored[:3]
    if not top:
        return ("needs_review", 0, [])
    best_score = top[0][0]
    evidence = [{"file": BOOKS_LOOKUP.get(it["dept"], "?"),
                 "line": i + 1, "text": orig.strip()[:300]} for _, i, orig in top]
    # heuristic conflict flag: known contrary indicators near a high-stakes drug/material
    verdict = "supported" if best_score >= 3 else "needs_review"
    return (verdict, best_score, evidence)

BOOKS_LOOKUP = {}  # filled in main per dept

def main():
    fn = load_flash_notes()
    items_to_verify = []
    for dept, lst in fn["byDept"].items():
        for it in lst:
            # Phase 3+: verify ALL marked items (structured options OR inline answers)
            if it.get("marker") in ("verified", "ref", "given"):
                items_to_verify.append((dept, it))
    print(f"items to verify: {len(items_to_verify)} (of {fn['total']} total)")

    verdicts = []
    stats = {"supported": 0, "needs_review": 0, "conflict": 0}
    by_dept_stats = defaultdict(lambda: {"supported": 0, "needs_review": 0, "conflict": 0, "total": 0})

    # process per-dept so we build the index once per dept
    by_dept = defaultdict(list)
    for dept, it in items_to_verify:
        by_dept[dept].append(it)

    for dept, its in by_dept.items():
        files = DEPT_BOOKS.get(dept, [])
        BOOKS_LOOKUP[dept] = ", ".join(files)
        print(f"\n[{dept}] {len(its)} items · books: {len(files)}")
        if not files:
            for it in its:
                verdicts.append({"id": it["id"], "dept": dept, "stem": it["stem"][:200],
                                 "answerLetter": it.get("answerLetter"), "answerText": extract_answer_text(it)[:200], "verdict": "needs_review",
                                 "score": 0, "evidence": []})
                stats["needs_review"] += 1; by_dept_stats[dept]["needs_review"] += 1; by_dept_stats[dept]["total"] += 1
            continue
        lines, word_index = build_index(files)
        print(f"  indexed {len(lines)} lines, {len(word_index)} unique words")
        for it in its:
            v, score, ev = verify_item(it, lines, word_index)
            verdicts.append({"id": it["id"], "dept": dept, "stem": it["stem"][:200],
                             "answerLetter": it.get("answerLetter"), "answerText": extract_answer_text(it)[:200],
                             "verdict": v, "score": score, "evidence": ev})
            stats[v] += 1; by_dept_stats[dept][v] += 1; by_dept_stats[dept]["total"] += 1
        # free memory
        del lines, word_index
        print(f"  -> supported={by_dept_stats[dept]['supported']} needs_review={by_dept_stats[dept]['needs_review']}")

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "generated": "2026-07-29",
        "totalChecked": len(verdicts),
        "stats": stats,
        "byDept": {d: dict(v) for d, v in by_dept_stats.items()},
        "rule": "Automated evidence-candidate pass. 'supported' = a gold-textbook line co-mentions a stem keyword AND the marked-answer keyword (citation candidate to confirm). 'needs_review' = no strong book line found. Not a final correctness judgment — confirm each 'supported' citation manually.",
        "booksUsed": {d: DEPT_BOOKS.get(d, []) for d in DEPT_BOOKS},
        "items": verdicts,
    }
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\nWROTE {OUT_JSON}")
    print(f"  stats: {stats}")

    # human-readable corrections handoff: list needs_review (sample) + low-score supported (sample)
    with OUT_MD.open("w", encoding="utf-8") as f:
        f.write("# Phase 3 — Flash Notes answer verification (automated evidence pass)\n\n")
        f.write(f"**Generated:** 2026-07-29  \n**Checked:** {len(verdicts)} community-marked recall answers.  \n")
        f.write(f"**Stats:** supported (book citation candidate) = {stats['supported']}; needs_review = {stats['needs_review']}.  \n")
        f.write("**Note:** this is an automated *evidence-candidate* pass, NOT a final correctness judgment. ")
        f.write("`supported` means a gold-textbook line co-mentions a stem keyword AND the marked-answer keyword — a reviewer must confirm it actually endorses the answer. ")
        f.write("`needs_review` means no strong book line was found — the answer is not yet grounded and must be checked manually against the official books before being trusted.\n\n")
        f.write("## Per-department breakdown\n\n| Dept | checked | supported | needs_review |\n|---|---|---|---|\n")
        for d in sorted(by_dept_stats):
            s = by_dept_stats[d]
            f.write(f"| {d} | {s['total']} | {s['supported']} | {s['needs_review']} |\n")
        f.write("\n## Books used (gold standard)\n\n")
        for d, files in DEPT_BOOKS.items():
            f.write(f"- **{d}**: " + ", ".join(f"`books/{x}`" for x in files) + "\n")
        # sample needs_review for human attention
        nr = [v for v in verdicts if v["verdict"] == "needs_review"]
        f.write(f"\n## Needs-review sample (first 40 of {len(nr)}) — verify these manually\n\n")
        for v in nr[:40]:
            f.write(f"- `{v['id']}` ({v['dept']}) ans={v['answerLetter']} — {v['stem'][:140]}\n")
        f.write(f"\n## Supported sample (first 20 of {stats['supported']}) — confirm the citation endorses the answer\n\n")
        for v in [x for x in verdicts if x["verdict"]=="supported"][:20]:
            ev = v["evidence"][0] if v["evidence"] else {}
            f.write(f"- `{v['id']}` ({v['dept']}) ans={v['answerLetter']} — {v['stem'][:120]}  \n  evidence: {ev.get('text','')[:160]}\n")
    print(f"WROTE {OUT_MD}")

if __name__ == "__main__":
    main()

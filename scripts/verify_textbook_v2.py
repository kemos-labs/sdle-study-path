#!/usr/bin/env python3
"""
verify_textbook_v2.py — Honest textbook verification for Flash Notes.

Phase 2 of the Flash Notes pipeline. Uses the stricter approach from
verify_flash_notes.py (July 29): requires BOTH stem keywords AND answer
keywords in the same passage, and classifies results as 'supported' vs
'needs_review' instead of claiming everything is "textbook-verified."

Usage:
    python3 verify_textbook_v2.py --sample 50   # Run on 50 items (5 per dept)
    python3 verify_textbook_v2.py --dept perio   # Run on one department
    python3 verify_textbook_v2.py                # Run on all 4,026 items

Output:
    data/flash_notes_verdicts_v2.json  — Machine-readable verdicts
    Terminal report — supported/needs_review per department
"""
from __future__ import annotations
import json, re, sys, unicodedata
from pathlib import Path
from collections import defaultdict

ROOT = Path("/data/prometric")
# SCFHS Appendix C corpus.  The older sdle-ref/books directory is a broad
# working collection with duplicate and non-canonical files, so it cannot be
# the evidence source for a Flash Notes verdict.
BOOKS_DIR = ROOT / "sdle-prep" / "data" / "raw" / "books" / "text"
DATA_DIR = ROOT / "sdle-prep" / "data"
FN_JS = DATA_DIR / "flash_notes.js"
OUT_JSON = DATA_DIR / "flash_notes_verdicts_v2.json"

# ── Department → canonical SCFHS Appendix C text extracts ───────────────
DEPT_BOOKS = {
    "restorative": [
        {"file": "Resto/Sturdevant_Operative_5e.txt", "short": "Sturdevant 5e"},
    ],
    "endo": [
        {"file": "Endo/Cohens_Pathways_of_the_Pulp_2016.txt", "short": "Cohen 11e"},
    ],
    "perio": [
        {"file": "perio/Carranza_Clinical_Periodontology_2018.txt", "short": "Carranza 13e"},
    ],
    "fixed": [
        {"file": "Fixed/Contemporary_Fixed_Prosthodontics_4e.txt", "short": "Fixed Pros 4e"},
    ],
    "rpd": [
        {"file": "Removable/McCracken_s Removable Partial Prosthodontics.txt", "short": "McCracken RPD"},
    ],
    "implant": [
        {"file": "perio/Carranza_Clinical_Periodontology_2018.txt", "short": "Carranza 13e"},
        {"file": "Fixed/Contemporary_Fixed_Prosthodontics_4e.txt", "short": "Fixed Pros 4e"},
    ],
    "ortho_pedo": [
        {"file": "ortho/Contemporary Orthodontics 5th.txt", "short": "Contemporary Orthodontics 5e"},
        {"file": "pedo/McDonald_Avery_10e.txt", "short": "McDonald & Avery 10e"},
    ],
    "oms": [
        {"file": "Oral surgary/Hupp_Contemporary_OMFS_6e.txt", "short": "Hupp OMFS 6e"},
        {"file": "Oral surgary/White_Pharoah_Oral_Radiology_7e.txt", "short": "White & Pharoah 7e"},
    ],
    "ethics": [
        {"file": "Ethics + infection control + local anasthesia/Stanley_F_Malamed_handbook_of_local_anes.txt", "short": "Malamed"},
        {"file": "Ethics + infection control + local anasthesia/Professionalism and Ethics Handbook for Residents.txt", "short": "SCFHS Ethics"},
    ],
    "diagnostics": [
        {"file": "Oral surgary/White_Pharoah_Oral_Radiology_7e.txt", "short": "White & Pharoah 7e"},
        {"file": "Oral surgary/Hupp_Contemporary_OMFS_6e.txt", "short": "Hupp OMFS 6e"},
    ],
}

# ── Stop words ──────────────────────────────────────────────────────────
STOP = {
    "a", "an", "the", "of", "to", "in", "on", "for", "and", "or", "but",
    "is", "are", "was", "were", "be", "been", "being", "have", "has", "had",
    "do", "does", "did", "doing", "will", "would", "shall", "should", "may",
    "might", "must", "can", "could", "i", "me", "my", "we", "our", "you",
    "your", "he", "she", "it", "they", "this", "that", "these", "those",
    "what", "which", "who", "whom", "when", "where", "why", "how",
    "and", "but", "or", "not", "no", "nor", "so", "for", "yet",
    "at", "by", "in", "on", "to", "of", "from", "with", "about", "into",
    "through", "during", "before", "after", "above", "below", "between",
    "up", "down", "out", "off", "over", "under", "again", "further",
    "then", "once", "here", "there", "when", "where", "why", "how",
    "all", "both", "each", "few", "more", "most", "other", "some", "such",
    "only", "own", "same", "than", "too", "very", "just", "also",
    "if", "as", "its", "am", "been", "doing", "does", "did",
    "patient", "pt", "following", "true", "false", "regarding",
    "one", "two", "three", "use", "used", "using", "etc",
    "without", "within", "often", "among", "whose", "many",
    "well", "much", "see", "per", "due", "along", "less", "even",
    "case", "cases", "clinical", "treatment", "management",
    "commonly", "common", "always", "usually", "typically",
    "associated", "condition", "conditions", "table", "figure", "fig",
}

# ── Junk passage patterns (index pages, bibliography, etc.) ─────────────
JUNK_PATTERNS = [
    r"^\s*INDEX\s+\d+",
    r"^\s*REFERENCES?\s",
    r"^\s*BIBLIOGRAPHY",
    r"^\s*GLOSSARY",
    r"^\s*CONTRIBUTORS?\s",
    r"^\s*ACKNOWLEDGMENTS?\s",
    r"^This page intentionally",
    r"^\d+\s+Westline",
    r"^Library of Congress",
    r"^ISBN",
    r"^Copyright",
    r"reserved\.$",
    r"^\s*Page\s+\d+",
]

def norm(s: str) -> str:
    s = unicodedata.normalize("NFKC", s)
    s = re.sub(r"[\u200b-\u200f\ufeff]", "", s)
    return s.lower()

def tokenize(text: str) -> set[str]:
    """Extract meaningful tokens (≥4 chars, not stop words)."""
    text = norm(text)
    text = re.sub(r"[^a-z0-9\u0600-\u06ff ]", " ", text)
    toks = set()
    for t in text.split():
        t = t.strip()
        if len(t) >= 4 and t not in STOP:
            toks.add(t)
    return toks

def distinctive_words(text: str, n: int = 6) -> list[str]:
    """Pick the most distinctive (longer, rarer) keywords from text."""
    text = norm(text)
    text = re.sub(r"[^a-z0-9 ]", " ", text)
    words = [t for t in text.split() if len(t) >= 4 and t not in STOP]
    seen = set()
    out = []
    for w in words:
        if w in seen:
            continue
        seen.add(w)
        out.append(w)
        if len(out) >= n:
            break
    return out

def strip_markers(s: str) -> str:
    return re.sub(r"[✅🟢🟡✳🔵🔁●]", "", s or "")

def is_junk(text: str) -> bool:
    """Check if a passage is junk (index, bibliography, etc.)."""
    for pat in JUNK_PATTERNS:
        if re.search(pat, text, re.IGNORECASE):
            return True
    # Check for table artifacts: more than 30% pipes or numbers
    pipe_ratio = text.count("|") / max(len(text), 1)
    if pipe_ratio > 0.15:
        return True
    return False


class TextbookIndex:
    """Index a textbook by chunks for fast keyword search."""

    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 100

    def __init__(self, book_config: dict):
        self.config = book_config
        self.chunks: list[tuple[int, str, str]] = []  # (start_pos, chapter, text)
        self.word_index: dict[str, set[int]] = defaultdict(set)
        self.loaded = False

    def load(self) -> bool:
        filepath = BOOKS_DIR / self.config["file"]
        if not filepath.exists():
            print(f"    ⚠️  Missing: {filepath.name}", file=sys.stderr)
            return False

        text = filepath.read_text(encoding="utf-8", errors="replace")

        # Clean table artifacts
        text = re.sub(r'\n\|[-|\s]+\|\s*\n', '\n', text)
        text = re.sub(r'\n\||\|\n', '\n', text)
        text = re.sub(r'\n{3,}', '\n\n', text)

        # Find chapter positions
        chapters = []
        for m in re.finditer(r'(?:CHAPTER|Chapter)\s+(\d+)', text):
            chapters.append((m.start(), f"Ch {m.group(1)}"))
        chapters.sort()

        def get_chapter(pos: int) -> str:
            ch = ""
            for cp, cl in chapters:
                if cp <= pos:
                    ch = cl
            return ch

        # Chunk with overlap
        pos = 0
        while pos < len(text):
            end = min(pos + self.CHUNK_SIZE, len(text))
            chunk = text[pos:end].strip()
            chunk = re.sub(r'\s*\|\s*', ' ', chunk)
            chunk = re.sub(r'\s{2,}', ' ', chunk)

            if len(chunk) > 60 and not is_junk(chunk):
                ch = get_chapter(pos)
                idx = len(self.chunks)
                self.chunks.append((pos, ch, chunk))
                for word in tokenize(chunk):
                    self.word_index[word].add(idx)

            pos += self.CHUNK_SIZE - self.CHUNK_OVERLAP

        self.loaded = True
        print(f"    ✓ {self.config['short']}: {len(self.chunks)} chunks, {len(self.word_index)} terms")
        return True

    def search(self, query_terms: set[str], max_results: int = 5) -> list[tuple[int, str, str]]:
        """Find chunks matching ANY query term. Returns [(score, chapter, text), ...]."""
        candidates = set()
        for term in query_terms:
            candidates |= self.word_index.get(term, set())

        if not candidates:
            return []

        scored = []
        for idx in candidates:
            _, ch, text = self.chunks[idx]
            text_lower = text.lower()
            score = sum(text_lower.count(term) for term in query_terms)
            scored.append((score, ch, text))

        scored.sort(key=lambda x: x[0], reverse=True)
        return scored[:max_results]


def extract_answer_text(item: dict) -> str:
    """Extract the answer text from a flash notes item."""
    # Try _verified_explanation first
    expl = item.get("_verified_explanation", "")
    if expl and expl.startswith("Correct answer:"):
        return expl.replace("Correct answer:", "").strip()

    # Try options + answerLetter
    answer_letter = item.get("answerLetter", "")
    answer_idx = item.get("answerIdx")
    options = item.get("options", [])

    if answer_idx is not None and options and answer_idx < len(options):
        opt_text = options[answer_idx]
        return strip_markers(opt_text).strip()

    if answer_letter and options:
        letter = answer_letter.upper().strip().rstrip(".")
        for opt in options:
            opt_clean = opt.strip()
            if opt_clean.upper().startswith(letter + ".") or opt_clean.upper().startswith(letter + " "):
                return strip_markers(opt_clean).strip()

    # Try from raw text
    raw = item.get("raw", "")
    if raw:
        m = re.search(r"([^✅✳🟢🟡●🔵🟦🔁\n]{10,80}?)\s*[✅✳🟢]", raw)
        if m:
            return m.group(1).strip().rstrip("-•,")

    return ""


def extract_question_text(item: dict) -> str:
    """Extract the question stem text."""
    stem = strip_markers(item.get("stem", "") or "")
    # Text before the last '?', otherwise whole stem
    if "?" in stem:
        return stem.rsplit("?", 1)[0].strip()
    return stem


def verify_item(item: dict, indices: list[TextbookIndex]) -> dict:
    """Verify a single item against a textbook index.

    Returns verdict dict with:
      - verdict: 'supported' | 'needs_review'
      - score: int
      - ans_keywords: list[str]
      - stem_keywords: list[str]
      - evidence: list[dict]
    """
    ans_text = extract_answer_text(item)
    q_text = extract_question_text(item)

    ans_kw = distinctive_words(ans_text, 6) if ans_text else []
    stem_kw = distinctive_words(q_text, 6)

    if not ans_kw:
        return {"verdict": "needs_review", "score": 0, "reason": "no_answer_text",
                "ans_keywords": [], "stem_keywords": stem_kw, "evidence": []}

    # Search canonical textbook passages for both the question and its marked
    # answer.  Shared vocabulary alone is not evidence of the answer.
    query = set(ans_kw + [w for w in stem_kw if len(w) >= 4])
    results = []
    for index in indices:
        results.extend((index.config["short"], chapter, text)
                       for _, chapter, text in index.search(query, max_results=8))

    if not results:
        return {"verdict": "needs_review", "score": 0, "reason": "no_match",
                "ans_keywords": ans_kw, "stem_keywords": stem_kw, "evidence": []}

    # Score each result: +2 per answer keyword hit, +1 per stem keyword hit
    evidence = []
    best_score = 0
    for book, chapter, text in results:
        text_lower = text.lower()
        ans_hits = sum(1 for w in ans_kw if w in text_lower)
        stem_hits = sum(1 for w in stem_kw if w in text_lower)
        combined = ans_hits * 2 + stem_hits

        if combined > best_score:
            best_score = combined

        evidence.append({
            "book": book,
            "passage": text[:300],
            "chapter": chapter,
            "ans_keywords_hit": ans_hits,
            "stem_keywords_hit": stem_hits,
            "score": combined,
        })

    evidence.sort(key=lambda e: e["score"], reverse=True)
    supported = [e for e in evidence if e["ans_keywords_hit"] > 0 and e["stem_keywords_hit"] > 0 and e["score"] >= 3]
    verdict = "supported" if supported else "needs_review"

    return {
        "verdict": verdict,
        "score": best_score,
        "reason": "same_passage_stem_and_answer" if verdict == "supported" else "no_same_passage_match",
        "ans_keywords": ans_kw,
        "stem_keywords": stem_kw,
        "evidence": evidence[:3],  # top 3 pieces of evidence
    }


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Phase 2: Honest textbook verification")
    parser.add_argument("--sample", type=int, default=0, help="Items per department (sample mode)")
    parser.add_argument("--dept", type=str, default="", help="Single department only")
    parser.add_argument("--dry-run", action="store_true", help="Don't write output")
    args = parser.parse_args()

    # ── Load flash_notes.js ─────────────────────────────────────────────
    print("=" * 70)
    print("PHASE 2 — TEXTBOOK VERIFICATION v2 (honest supported/needs_review)")
    print("=" * 70)

    content = FN_JS.read_text(encoding="utf-8")
    match = re.search(r"window\.FLASH_NOTES\s*=\s*(\{.*);", content, re.DOTALL)
    if not match:
        print("❌ Could not parse flash_notes.js")
        sys.exit(1)
    data = json.loads(match.group(1))
    print(f"\n📊 Loaded: {data['total']} items")

    # ── Process each department ─────────────────────────────────────────
    all_verdicts = {}
    total_stats = {"supported": 0, "needs_review": 0, "no_books": 0}
    dept_stats = {}

    for dept in ["restorative", "endo", "perio", "fixed", "rpd", "implant",
                  "ortho_pedo", "oms", "ethics", "diagnostics"]:
        items = data["byDept"].get(dept, [])
        if not items:
            continue
        if args.dept and dept != args.dept:
            continue

        books = DEPT_BOOKS.get(dept, [])
        if not books:
            print(f"\n⚠️  {dept}: No textbooks mapped — skipping {len(items)} items")
            for it in items:
                all_verdicts[it["id"]] = {"verdict": "needs_review", "score": 0, "reason": "no_textbooks"}
                total_stats["needs_review"] += 1
            continue

        # Limit to sample if requested
        if args.sample > 0:
            # Pick items to sample: mix of verified and ref
            verified_items = [it for it in items if it.get("marker") == "verified"]
            ref_items = [it for it in items if it.get("marker") == "ref"]
            sample_size = min(args.sample, len(items))
            n_ver = min(sample_size // 2, len(verified_items))
            n_ref = sample_size - n_ver
            sampled = verified_items[:n_ver] + ref_items[:n_ref]
            print(f"\n📚 {dept.upper()} — sampling {len(sampled)}/{len(items)} items ({n_ver} verified, {n_ref} ref)")
            process_items = sampled
        else:
            print(f"\n📚 {dept.upper()} — {len(items)} items")
            process_items = items

        # Load textbooks
        indices = []
        for cfg in books:
            idx = TextbookIndex(cfg)
            if idx.load():
                indices.append(idx)

        if not indices:
            print(f"   ❌ No textbooks could be loaded for {dept}")
            for it in process_items:
                all_verdicts[it["id"]] = {"verdict": "needs_review", "score": 0, "reason": "no_textbooks_loaded"}
                total_stats["needs_review"] += 1
            continue

        # Verify each item
        dept_supported = 0
        dept_review = 0
        for it in process_items:
            verdict = verify_item(it, indices)
            all_verdicts[it["id"]] = verdict

            if verdict["verdict"] == "supported":
                dept_supported += 1
                total_stats["supported"] += 1
            else:
                dept_review += 1
                total_stats["needs_review"] += 1

        dept_stats[dept] = {"checked": len(process_items), "supported": dept_supported, "needs_review": dept_review}
        print(f"   → {dept_supported} supported, {dept_review} needs_review (of {len(process_items)})")

    # ── Summary ─────────────────────────────────────────────────────────
    print(f"\n{'=' * 70}")
    print(f"📊 SUMMARY")
    print(f"   Total checked: {total_stats['supported'] + total_stats['needs_review']}")
    print(f"   Supported:     {total_stats['supported']}")
    print(f"   Needs review:  {total_stats['needs_review']}")
    print(f"   No books:      {total_stats['no_books']}")
    print(f"{'=' * 70}")

    # ── Show sample of downgraded items (currently have _book_explanation but verdict=needs_review) ──
    downgraded = []
    for dept, items in data["byDept"].items():
        if args.dept and dept != args.dept:
            continue
        for it in items:
            if it["id"] in all_verdicts:
                v = all_verdicts[it["id"]]
                has_book = "_book_explanation" in it and it["_book_explanation"]
                if has_book and v["verdict"] == "needs_review":
                    downgraded.append((it["id"], dept, it.get("stem", "")[:60], v["score"]))

    if downgraded:
        print(f"\n⚠️  Items with CURRENT _book_explanation that are NEES_REVIEW:")
        for iid, dept, stem, score in downgraded[:10]:
            print(f"   {iid} ({dept}) score={score} — {stem}")
        if len(downgraded) > 10:
            print(f"   ... and {len(downgraded)-10} more")
        print(f"   Total: {len(downgraded)} items might be over-claiming 'textbook-verified'")

    # ── Write output ────────────────────────────────────────────────────
    if not args.dry_run:
        output = {
            "generated": "2026-07-30",
            "mode": "sample" if args.sample > 0 else "full",
            "totalChecked": total_stats["supported"] + total_stats["needs_review"],
            "stats": total_stats,
            "byDept": dept_stats,
            "verdicts": all_verdicts,
        }
        OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
        OUT_JSON.write_text(json.dumps(output, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"\n💾 Wrote {OUT_JSON}")

    # ── Show sample items ───────────────────────────────────────────────
    if args.sample > 0:
        print(f"\n{'=' * 70}")
        print(f"📋 SAMPLE RESULTS (first 20)")
        print(f"{'=' * 70}")
        shown = 0
        for dept in ["restorative", "endo", "perio", "fixed", "rpd", "implant",
                      "ortho_pedo", "oms", "ethics", "diagnostics"]:
            items = data["byDept"].get(dept, [])
            for it in items:
                if it["id"] in all_verdicts and shown < 20:
                    v = all_verdicts[it["id"]]
                    has_book = "✓" if "_book_explanation" in it and it["_book_explanation"] else "✗"
                    print(f"\n{it['id']} ({dept}) [{v['verdict']}] score={v['score']} book={has_book}")
                    print(f"  stem: {it.get('stem','')[:80]}")
                    if v['ans_keywords']:
                        print(f"  ans_kw: {v['ans_keywords']}")
                    if v['evidence']:
                        ev = v['evidence'][0]
                        print(f"  evidence: {ev['passage'][:120]}...")
                    shown += 1


if __name__ == "__main__":
    main()

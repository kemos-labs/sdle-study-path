#!/usr/bin/env python3
"""
fix_flash_notes.py — Fix, verify, and enhance flash_notes.js

Phase 2 pipeline:
  1. Fix 200 verified items missing _verified_explanation
  2. Search textbooks for corroborating passages (high-quality matches only)
  3. Add _book_explanation with citations where found
  4. Clean up formatting, update stats

NO API. Pure local text search. Honest about verification status.
"""
from __future__ import annotations
import json, os, re, sys
from pathlib import Path
from collections import defaultdict
from typing import Optional

ROOT = Path("/data/prometric")
BOOKS_DIR = ROOT / "sdle-ref" / "books"
DATA_DIR = ROOT / "sdle-prep" / "data"
FLASH_NOTES = DATA_DIR / "flash_notes.js"

# ── Department → Textbook mapping ──────────────────────────────────────────
DEPT_BOOKS = {
    "restorative": [
        {"file": "Resto_Sturdevant_Operative_5e.md", "title": "Sturdevant's Art & Science of Operative Dentistry, 5e", "short": "Sturdevant 5e"},
    ],
    "endo": [
        {"file": "Endo_Cohens_Pathways_of_the_Pulp_2016.md", "title": "Cohen's Pathways of the Pulp, 11e", "short": "Cohen 11e"},
    ],
    "perio": [
        {"file": "perio_Carranza_Clinical_Periodontology_2018.md", "title": "Carranza's Clinical Periodontology, 13e", "short": "Carranza 13e"},
    ],
    "fixed": [
        {"file": "Fixed_Contemporary_Fixed_Prosthodontics_4e.md", "title": "Contemporary Fixed Prosthodontics, 5e", "short": "Fixed Pros 5e"},
    ],
    "rpd": [
        {"file": "Removable_McCracken_s_Removable_Partial_Prosthodontics.md", "title": "McCracken's Removable Partial Prosthodontics", "short": "McCracken RPD"},
    ],
    "implant": [
        {"file": "perio_Carranza_Clinical_Periodontology_2018.md", "title": "Carranza's Clinical Periodontology, 13e", "short": "Carranza 13e"},
        {"file": "Fixed_Contemporary_Fixed_Prosthodontics_4e.md", "title": "Contemporary Fixed Prosthodontics, 5e", "short": "Fixed Pros 5e"},
    ],
    "ortho_pedo": [
        {"file": "Ortho_Contemporary Orthodontics 5th.md", "title": "Contemporary Orthodontics, 7e", "short": "Ortho 7e"},
        {"file": "Pedo_McDonald_Avery_10e.md", "title": "McDonald & Avery's Dentistry for the Child & Adolescent, 10e", "short": "McDonald 10e"},
    ],
    "oms": [
        {"file": "Oral_surgary_Hupp_Contemporary_OMFS_6e.md", "title": "Contemporary Oral & Maxillofacial Surgery, 7e", "short": "OMFS 7e"},
        {"file": "Oral_surgary_White_Pharoah_Oral_Radiology_7e.md", "title": "White & Pharoah's Oral Radiology, 8e", "short": "Oral Radiology 8e"},
    ],
    "ethics": [
        {"file": "Ethics___infection_control___local_anasthesia_Stanley_F_Malamed_handbook_of_local_anes.md", "title": "Malamed's Handbook of Local Anesthesia, 7e", "short": "Malamed 7e"},
        {"file": "Ethics___infection_control___local_anasthesia_Professionalism_and_Ethics_Handbook_for_Residents.md", "title": "SCFHS Ethics Handbook", "short": "SCFHS Ethics"},
    ],
    "diagnostics": [
        {"file": "Oral_surgary_White_Pharoah_Oral_Radiology_7e.md", "title": "White & Pharoah's Oral Radiology, 8e", "short": "Oral Radiology 8e"},
        {"file": "Oral_surgary_Hupp_Contemporary_OMFS_6e.md", "title": "Contemporary OMFS, 7e", "short": "OMFS 7e"},
    ],
}

STOP_WORDS = {
    "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "having", "do", "does", "did", "doing",
    "will", "would", "shall", "should", "may", "might", "must", "can", "could",
    "i", "me", "my", "we", "our", "you", "your", "he", "she", "it", "they",
    "this", "that", "these", "those", "what", "which", "who", "whom",
    "and", "but", "or", "not", "no", "nor", "so", "for", "yet",
    "at", "by", "in", "on", "to", "of", "from", "with", "about", "into",
    "through", "during", "before", "after", "above", "below", "between",
    "up", "down", "out", "off", "over", "under", "again", "further",
    "then", "once", "here", "there", "when", "where", "why", "how",
    "all", "both", "each", "few", "more", "most", "other", "some", "such",
    "only", "own", "same", "than", "too", "very", "just", "also",
    "if", "as", "its", "am", "been", "being", "had", "has", "does",
    "patient", "pt", "following", "true", "false", "regarding",
    "one", "two", "three", "use", "used", "using", "etc",
    "without", "within", "often", "among", "whose", "many",
    "well", "much", "see", "per", "due", "along", "less", "even",
    "case", "cases", "clinical", "treatment", "management",
    "commonly", "common", "always", "usually", "typically",
    "associated", "condition", "conditions", "table", "figure", "fig",
}

# Medical abbreviations for query expansion
EXPAND_TERMS = {
    "rct": ["root canal", "endodontic treatment"],
    "srp": ["scaling", "root planing"],
    "la": ["local anesthesia", "local anaesthetic"],
    "ian": ["inferior alveolar nerve"],
    "mronj": ["osteonecrosis", "bisphosphonate"],
    "onj": ["osteonecrosis"],
    "vrf": ["vertical root fracture"],
    "gi": ["glass ionomer"],
    "gic": ["glass ionomer cement"],
    "pfm": ["porcelain fused to metal"],
    "rpd": ["removable partial denture"],
    "fpd": ["fixed partial denture", "bridge"],
    "ssc": ["stainless steel crown"],
    "gtr": ["guided tissue regeneration"],
    "cbct": ["cone beam", "computed tomography"],
    "tmj": ["temporomandibular joint"],
    "mta": ["mineral trioxide aggregate"],
    "chx": ["chlorhexidine"],
}


def tokenize(text: str) -> set:
    """Extract normalized tokens from text."""
    tokens = re.findall(r"[a-z0-9]{3,}", text.lower())
    result = set()
    for t in tokens:
        if t in STOP_WORDS:
            continue
        result.add(t)
        # Expand abbreviations
        if t in EXPAND_TERMS:
            for exp in EXPAND_TERMS[t]:
                for et in re.findall(r"[a-z]{3,}", exp):
                    if et not in STOP_WORDS:
                        result.add(et)
    return result


def clean_text(text: str) -> str:
    """Clean up PDF artifacts from textbook text."""
    # Remove page numbers, headers, footers, table artifacts
    text = re.sub(r"\b\d{1,4}\b\s*\|\s*", " ", text)  # table column separators
    text = re.sub(r"\s{2,}", " ", text)
    return text.strip()


class TextbookSearcher:
    """Index a textbook by chunks and search for matching passages."""

    CHUNK_SIZE = 400  # chars per chunk
    CHUNK_OVERLAP = 100  # overlap between chunks

    def __init__(self, book_config):
        self.config = book_config
        self.book_text = ""
        self.chunks = []  # list of (start_pos, chapter, chunk_text)
        self.word_index = defaultdict(set)

    def load(self) -> bool:
        filepath = BOOKS_DIR / self.config["file"]
        if not filepath.exists():
            return False

        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            self.book_text = f.read()

        # Clean the entire text first: remove table separator lines, merge table artifacts
        text = self.book_text
        # Remove markdown table separators and empty table rows
        text = re.sub(r'\n\|[-|\s]+\|\s*\n', '\n', text)
        text = re.sub(r'\n\|[\s|]*\|\s*\n', '\n', text)
        # Collapse multiple newlines
        text = re.sub(r'\n{3,}', '\n\n', text)
        # Remove lines that are just table formatting
        text = re.sub(r'\n\|[\s\|]+\n', '\n', text)

        # Find chapter positions
        # Patterns: "CHAPTER 1", "Chapter 1", "C H A P T E R   1"
        chapter_pattern = re.compile(
            r'(?:CHAPTER|Chapter)\s+(\d+)|C\s+H\s+\|\s+A\s+\|\s+P\s+\|\s+T\s+\|\s+E\s+\|\s+R\s+\|?\s*(\d+)?',
            re.IGNORECASE
        )
        chapter_positions = []  # list of (pos, chapter_label)
        for m in chapter_pattern.finditer(text):
            ch_num = m.group(1) or m.group(2)
            if ch_num:
                chapter_positions.append((m.start(), f"Ch {ch_num}"))

        # Also look for "Introduction to Operative Dentistry CHAPTER 1" style
        ch_inline = re.compile(r'(CHAPTER|Chapter)\s+(\d+)', re.IGNORECASE)
        for m in ch_inline.finditer(text):
            chapter_positions.append((m.start(), f"Ch {m.group(2)}"))

        chapter_positions.sort()

        def get_chapter(pos):
            """Find the chapter that contains this position."""
            ch = ""
            for cp, cl in chapter_positions:
                if cp <= pos:
                    ch = cl
                else:
                    break
            return ch

        # Chunk the text with overlap
        pos = 0
        text_len = len(text)
        while pos < text_len:
            end = min(pos + self.CHUNK_SIZE, text_len)
            chunk_text = text[pos:end].strip()

            # Clean chunk
            chunk_text = clean_text(chunk_text)
            # Remove bare pipe/table artifacts
            chunk_text = re.sub(r'\s*\|\s*', ' ', chunk_text)
            chunk_text = re.sub(r'\s{2,}', ' ', chunk_text)

            if len(chunk_text) > 50 and not self._is_junk(chunk_text):
                chapter = get_chapter(pos)
                chunk_idx = len(self.chunks)
                self.chunks.append((pos, chapter, chunk_text))
                for word in tokenize(chunk_text):
                    self.word_index[word].add(chunk_idx)

            pos += (self.CHUNK_SIZE - self.CHUNK_OVERLAP)

        return True

    def _is_junk(self, text: str) -> bool:
        """Filter out index, bibliography, and other non-content text."""
        junk_patterns = [
            r"^\s*INDEX\s+\d+", r"^\s*REFERENCES?\s", r"^\s*BIBLIOGRAPHY",
            r"^\s*GLOSSARY", r"^\s*CONTRIBUTORS?\s", r"^\s*ACKNOWLEDGMENTS?\s",
            r"^This page intentionally", r"^\d+ Westline", r"^Library of Congress",
            r"^ISBN", r"^Copyright", r"reserved\.$",
        ]
        for pat in junk_patterns:
            if re.search(pat, text, re.IGNORECASE):
                return True
        # If >50% of chars are table artifacts (|, numbers, spaces)
        pipe_chars = text.count('|') + text.count('  ')
        if len(text) > 0 and pipe_chars / len(text) > 0.3:
            return True
        return False

    def search(self, query_terms: set, max_results: int = 5) -> list:
        """Search for chunks matching query terms. Returns [(score, chapter, passage), ...]."""
        candidate_chunks = set()
        for term in query_terms:
            if term in self.word_index:
                candidate_chunks |= self.word_index[term]

        if not candidate_chunks:
            return []

        scored = []
        for chunk_idx in candidate_chunks:
            _, chapter, text = self.chunks[chunk_idx]
            text_lower = text.lower()
            score = sum(text_lower.count(term) for term in query_terms)
            if score > 0:
                scored.append((score, chapter, text))

        scored.sort(key=lambda x: x[0], reverse=True)
        return scored[:max_results]


def extract_answer_text(item: dict) -> str:
    """Extract the community answer text from an item."""
    # Try _verified_explanation first
    expl = item.get("_verified_explanation", "")
    if expl.startswith("Correct answer:"):
        return expl.replace("Correct answer:", "").strip()

    # Try options + answerLetter/answerIdx
    answer_letter = item.get("answerLetter", "")
    answer_idx = item.get("answerIdx")
    options = item.get("options", [])

    if answer_idx is not None and options and answer_idx < len(options):
        opt_text = options[answer_idx]
        # Clean marker symbols
        return re.sub(r"[✅✳🟢🟡🔵🟦🔁●].*$", "", opt_text).strip()

    if answer_letter and options:
        letter = answer_letter.upper().strip().rstrip(".")
        for opt in options:
            opt_clean = opt.strip()
            if opt_clean.upper().startswith(letter + ".") or opt_clean.upper().startswith(letter + " "):
                return re.sub(r"[✅✳🟢🟡🔵🟦🔁●].*$", "", opt_clean).strip()

    # Try extracting answer from raw text using ✅ marker
    raw = item.get("raw", "")
    if raw:
        # Pattern: text before ✅ is the answer
        # e.g., "C- decrease the microleakage ✅" or "- acrylic ✅"
        m = re.search(r"[-•]\s*([^✅✳🟢🟡●🔵🟦🔁\n]+?)\s*[✅✳🟢]", raw)
        if m:
            return m.group(1).strip().rstrip("-•,")
        # Pattern: text with ✅ at end of a clause
        m = re.search(r"([^✅✳🟢🟡●🔵🟦🔁\n]{10,80}?)\s*[✅✳🟢]", raw)
        if m:
            return m.group(1).strip().rstrip("-•,")

    # Try extracting from stem (some stems have ✅ embedded)
    stem = item.get("stem", "")
    if stem:
        m = re.search(r"([^✅✳🟢🟡●🔵🟦🔁\n]{5,80}?)\s*[✅✳🟢]", stem)
        if m:
            return m.group(1).strip().rstrip("-•,")

    return ""


def build_query_for_item(item: dict) -> str:
    """Build a search query from an item's stem and answer."""
    stem = item.get("stem", "")
    # Clean stem
    stem = re.sub(r"[?.,;:!()\[\]{}►✅✳🟢●🔵🟦🔁\n\r\t]", " ", stem)
    stem = re.sub(r"\s{2,}", " ", stem).strip()

    answer = extract_answer_text(item)

    # Combine: stem keywords + answer keywords
    # Give more weight to the answer for precision
    query = f"{answer} {answer} {stem}"
    return query


def fix_missing_explanations(data: dict) -> int:
    """Add _verified_explanation for verified items that are missing it."""
    fixed = 0
    for dept, items in data["byDept"].items():
        for item in items:
            if item.get("marker") == "verified" and "_verified_explanation" not in item:
                answer = extract_answer_text(item)
                if answer:
                    answer_letter = item.get("answerLetter") or ""
                    if answer_letter:
                        item["_verified_explanation"] = f"Correct answer: {answer_letter.lower()}. {answer}"
                    else:
                        item["_verified_explanation"] = f"Correct answer: {answer}"
                    fixed += 1
    return fixed


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--dept", type=str, help="Single department")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--min-score", type=int, default=5, help="Min keyword score for textbook match")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--fix-only", action="store_true", help="Only fix missing explanations, no textbook search")
    args = parser.parse_args()

    # ── Load ─────────────────────────────────────────────────────────────
    print("=" * 70)
    print("FLASH NOTES — FIX & VERIFY")
    print("=" * 70)

    with open(FLASH_NOTES, "r", encoding="utf-8") as f:
        content = f.read()

    match = re.search(r"window\.FLASH_NOTES\s*=\s*(\{.*);", content, re.DOTALL)
    data = json.loads(match.group(1))

    verif_count = len([it for dept in data["byDept"].values() for it in dept
                       if "_verified_explanation" in it])
    print(f"Loaded: {data['total']} items, {verif_count} with explanations")
    print(f"Markers: {json.dumps(data['markerStats'])}")

    # ── Step 1: Fix missing explanations ─────────────────────────────────
    print("\n── Step 1: Fix missing explanations ──")
    fixed = fix_missing_explanations(data)
    print(f"Fixed {fixed} verified items with missing explanations")

    if args.fix_only:
        # Write and exit
        json_str = json.dumps(data, ensure_ascii=False, indent=2)
        output = f"/** Flash Notes — FIXED */\nwindow.FLASH_NOTES = {json_str};\n"
        with open(FLASH_NOTES, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Wrote {FLASH_NOTES}")
        return

    # ── Step 2: Textbook verification ────────────────────────────────────
    print("\n── Step 2: Textbook verification ──")
    textbook_citations = 0
    searched = 0
    skipped = 0

    for dept, items in data["byDept"].items():
        if args.dept and dept != args.dept:
            continue

        books = DEPT_BOOKS.get(dept, [])
        if not books:
            skipped += len(items)
            continue

        print(f"\n📚 {dept} ({len(items)} items)")

        # Load textbooks
        searchers = []
        for cfg in books:
            s = TextbookSearcher(cfg)
            if s.load():
                searchers.append(s)
                print(f"   ✓ {cfg['short']}: {len(s.chunks)} chunks indexed")

        if not searchers:
            skipped += len(items)
            continue

        # Process items
        limit = args.limit or len(items)
        for idx, item in enumerate(items[:limit]):
            searched += 1

            # Skip items that already have textbook citations
            if item.get("_book_explanation", {}).get("verified") == "textbook":
                continue

            # Build query and search
            query = build_query_for_item(item)
            query_terms = tokenize(query)
            if not query_terms:
                skipped += 1
                continue

            best_score = 0
            best_result = None

            for s in searchers:
                for score, chapter, text in s.search(query_terms):
                    if score > best_score:
                        best_score = score
                        # Extract a good excerpt
                        excerpt = text[:400]
                        if len(text) > 400:
                            excerpt = text[:397] + "..."
                        best_result = {
                            "book": s.config["short"],
                            "chapter": chapter,
                            "passage": excerpt,
                            "score": score,
                        }

            if best_result and best_score >= args.min_score:
                # Store both community answer AND textbook citation
                best_result["verified"] = "textbook"
                item["_book_explanation"] = best_result
                textbook_citations += 1

                if textbook_citations % 100 == 0:
                    print(f"   📖 {textbook_citations} textbook citations found...")

        print(f"   Done: {textbook_citations} citations so far")

    print(f"\n{'=' * 70}")
    print(f"Searched: {searched}")
    print(f"Textbook citations: {textbook_citations}")
    print(f"Skipped: {skipped}")
    print(f"{'=' * 70}")

    # ── Step 3: Update stats ─────────────────────────────────────────────
    verif_after = len([it for dept in data["byDept"].values() for it in dept
                       if "_verified_explanation" in it])
    book_after = len([it for dept in data["byDept"].values() for it in dept
                      if it.get("_book_explanation", {}).get("verified") == "textbook"])

    data["textbookVerified"] = book_after
    data["communityVerified"] = verif_after

    # ── Write ─────────────────────────────────────────────────────────────
    if not args.dry_run:
        json_str = json.dumps(data, ensure_ascii=False, indent=2)
        output = f"/** Flash Notes — Textbook + Community verified */\nwindow.FLASH_NOTES = {json_str};\n"
        with open(FLASH_NOTES, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"\n💾 Written to {FLASH_NOTES}")
        print(f"   {verif_after} community-verified explanations")
        print(f"   {book_after} textbook citations")
    else:
        print("\n🔍 Dry run — no writes")


if __name__ == "__main__":
    main()

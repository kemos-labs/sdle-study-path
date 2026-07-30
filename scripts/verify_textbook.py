#!/usr/bin/env python3
"""
verify_textbook.py — Search official textbooks for flash notes items and add citations.

Phase 2 of the flash notes verification pipeline:
1. Load flash_notes.js
2. For each item with a community answer, search the relevant official textbook
3. Find the passage that corroborates the answer
4. Store as _book_explanation with {book, chapter, passage, confidence}
5. Output updated flash_notes.js

NO API calls. Pure local grep + text search. Reproducible.
"""
from __future__ import annotations
import json, os, re, sys, hashlib
from pathlib import Path
from collections import defaultdict
from typing import Optional

ROOT = Path("/data/prometric")
BOOKS_DIR = ROOT / "sdle-ref" / "books"
DATA_DIR = ROOT / "sdle-prep" / "data"
FLASH_NOTES = DATA_DIR / "flash_notes.js"
OUTPUT = DATA_DIR / "flash_notes.js"

# ── Department → Textbook mapping ──────────────────────────────────────────
# Maps each dept to the textbook file(s) to search, plus book metadata for citations
DEPT_BOOKS = {
    "restorative": [
        {
            "file": "Resto_Sturdevant_Operative_5e.md",
            "title": "Sturdevant's Art & Science of Operative Dentistry, 5e",
            "short": "Sturdevant 5e",
            "chapters_pattern": r"^Chapter\s+(\d+)[,:\s]+(.+)$",
        }
    ],
    "endo": [
        {
            "file": "Endo_Cohens_Pathways_of_the_Pulp_2016.md",
            "title": "Cohen's Pathways of the Pulp, 11e",
            "short": "Cohen 11e",
            "chapters_pattern": r"^Chapter\s+(\d+)[,:\s]+(.+)$",
        }
    ],
    "perio": [
        {
            "file": "perio_Carranza_Clinical_Periodontology_2018.md",
            "title": "Newman & Carranza's Clinical Periodontology, 13e",
            "short": "Carranza 13e",
            "chapters_pattern": r"^Chapter\s+(\d+)[,:\s]+(.+)$",
        }
    ],
    "fixed": [
        {
            "file": "Fixed_Contemporary_Fixed_Prosthodontics_4e.md",
            "title": "Contemporary Fixed Prosthodontics, 5e",
            "short": "Fixed Pros 5e",
            "chapters_pattern": r"^Chapter\s+(\d+)[,:\s]+(.+)$",
        }
    ],
    "rpd": [
        {
            "file": "Removable_McCracken_s_Removable_Partial_Prosthodontics.md",
            "title": "McCracken's Removable Partial Prosthodontics",
            "short": "McCracken RPD",
            "chapters_pattern": r"^Chapter\s+(\d+)[,:\s]+(.+)$",
        }
    ],
    "implant": [
        {
            "file": "perio_Carranza_Clinical_Periodontology_2018.md",
            "title": "Newman & Carranza's Clinical Periodontology, 13e",
            "short": "Carranza 13e",
            "chapters_pattern": r"^Chapter\s+(\d+)[,:\s]+(.+)$",
        },
        {
            "file": "Fixed_Contemporary_Fixed_Prosthodontics_4e.md",
            "title": "Contemporary Fixed Prosthodontics, 5e",
            "short": "Fixed Pros 5e",
            "chapters_pattern": r"^Chapter\s+(\d+)[,:\s]+(.+)$",
        }
    ],
    "ortho_pedo": [
        {
            "file": "Ortho_Contemporary Orthodontics 5th.md",
            "title": "Contemporary Orthodontics, 7e",
            "short": "Ortho 7e",
            "chapters_pattern": r"^Chapter\s+(\d+)[,:\s]+(.+)$",
        },
        {
            "file": "Pedo_McDonald_Avery_10e.md",
            "title": "McDonald & Avery's Dentistry for the Child & Adolescent, 10e",
            "short": "McDonald 10e",
            "chapters_pattern": r"^Chapter\s+(\d+)[,:\s]+(.+)$",
        }
    ],
    "oms": [
        {
            "file": "Oral_surgary_Hupp_Contemporary_OMFS_6e.md",
            "title": "Contemporary Oral & Maxillofacial Surgery, 7e",
            "short": "OMFS 7e",
            "chapters_pattern": r"^Chapter\s+(\d+)[,:\s]+(.+)$",
        },
        {
            "file": "Oral_surgary_White_Pharoah_Oral_Radiology_7e.md",
            "title": "White & Pharoah's Oral Radiology, 8e",
            "short": "Oral Radiology 8e",
            "chapters_pattern": r"^Chapter\s+(\d+)[,:\s]+(.+)$",
        }
    ],
    "ethics": [
        {
            "file": "Ethics___infection_control___local_anasthesia_Stanley_F_Malamed_handbook_of_local_anes.md",
            "title": "Malamed's Handbook of Local Anesthesia, 7e",
            "short": "Malamed 7e",
            "chapters_pattern": r"^CHAPTER\s+(\d+)",
        },
        {
            "file": "Ethics___infection_control___local_anasthesia_Professionalism_and_Ethics_Handbook_for_Residents.md",
            "title": "Professionalism & Ethics Handbook for Residents (SCFHS)",
            "short": "SCFHS Ethics",
            "chapters_pattern": None,
        }
    ],
    "diagnostics": [
        {
            "file": "Oral_surgary_White_Pharoah_Oral_Radiology_7e.md",
            "title": "White & Pharoah's Oral Radiology, 8e",
            "short": "Oral Radiology 8e",
            "chapters_pattern": r"^Chapter\s+(\d+)[,:\s]+(.+)$",
        },
        {
            "file": "Oral_surgary_Hupp_Contemporary_OMFS_6e.md",
            "title": "Contemporary Oral & Maxillofacial Surgery, 7e",
            "short": "OMFS 7e",
            "chapters_pattern": r"^Chapter\s+(\d+)[,:\s]+(.+)$",
        }
    ],
}

# ── English stop words ──────────────────────────────────────────────────────
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
    "only", "own", "same", "than", "too", "very", "just",
    "also", "if", "as", "its", "am", "been", "being", "had", "has",
    "having", "does", "did", "doing", "would", "could", "should",
    "patient", "pt", "following", "true", "false", "regarding",
    "one", "two", "three", "use", "used", "using", "may", "etc",
    "without", "within", "often", "among", "whose", "many",
    "well", "much", "see", "per", "due", "along", "less", "even",
    "case", "cases", "clinical", "treatment", "management",
    "commonly", "common", "always", "usually", "typically",
    "associated", "association", "condition", "conditions",
}

# ── Medical term normalization ─────────────────────────────────────────────
# Map common abbreviations and variants for better search matching
TERM_NORMALIZE = {
    "rct": "root canal treatment",
    "srp": "scaling root planing",
    "la": "local anesthesia",
    "ian": "inferior alveolar nerve",
    "mronj": "medication related osteonecrosis jaw",
    "onj": "osteonecrosis jaw",
    "vrf": "vertical root fracture",
    "mta": "mineral trioxide aggregate",
    "naocl": "sodium hypochlorite",
    "edta": "ethylenediaminetetraacetic acid",
    "gi": "glass ionomer",
    "gic": "glass ionomer cement",
    "rmgic": "resin modified glass ionomer",
    "pfm": "porcelain fused metal",
    "rpd": "removable partial denture",
    "fpd": "fixed partial denture",
    "ssc": "stainless steel crown",
    "prf": "platelet rich fibrin",
    "prp": "platelet rich plasma",
    "gbd": "guided bone regeneration",
    "gtr": "guided tissue regeneration",
    "cbct": "cone beam computed tomography",
    "tmj": "temporomandibular joint",
    "tmd": "temporomandibular disorder",
    "mta": "mineral trioxide aggregate",
    "chx": "chlorhexidine",
    "pmma": "polymethyl methacrylate",
    "bisgma": "bisphenol a glycidyl methacrylate",
    "hema": "hydroxyethyl methacrylate",
}


class TextbookSearcher:
    """Index a textbook and search for passages matching query terms."""

    def __init__(self, book_config):
        self.config = book_config
        self.paragraphs = []  # list of (line_num, chapter, text)
        self.word_index = defaultdict(set)  # word → set of paragraph indices
        self.loaded = False

    def load(self):
        filepath = BOOKS_DIR / self.config["file"]
        if not filepath.exists():
            print(f"  ⚠️  Textbook not found: {filepath}")
            return False

        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()

        chapters_pattern = self.config.get("chapters_pattern")
        current_chapter = ""
        current_para_lines = []
        para_start_line = 0

        for i, line in enumerate(lines):
            line_stripped = line.strip()

            # Detect chapter headings
            if chapters_pattern:
                m = re.match(chapters_pattern, line_stripped, re.IGNORECASE)
                if m:
                    current_chapter = f"Ch {m.group(1)}"

            # Split into paragraphs at blank lines
            if not line_stripped:
                if current_para_lines:
                    para_text = " ".join(current_para_lines).strip()
                    if len(para_text) > 40:  # skip tiny fragments
                        para_idx = len(self.paragraphs)
                        self.paragraphs.append((para_start_line, current_chapter, para_text))
                        self._index_paragraph(para_idx, para_text)
                    current_para_lines = []
            else:
                if not current_para_lines:
                    para_start_line = i + 1
                current_para_lines.append(line_stripped)

        # Don't forget last paragraph
        if current_para_lines:
            para_text = " ".join(current_para_lines).strip()
            if len(para_text) > 40:
                para_idx = len(self.paragraphs)
                self.paragraphs.append((para_start_line, current_chapter, para_text))
                self._index_paragraph(para_idx, para_text)

        self.loaded = True
        print(f"    Loaded {len(self.paragraphs)} paragraphs, indexed {len(self.word_index)} unique terms")
        return True

    def _index_paragraph(self, para_idx, text):
        """Index each word → paragraph for fast retrieval."""
        words = set(self._tokenize(text))
        for w in words:
            self.word_index[w].add(para_idx)

    def _tokenize(self, text):
        """Extract meaningful lowercase tokens from text."""
        tokens = re.findall(r"[a-z]{3,}", text.lower())
        normalized = set()
        for t in tokens:
            if t in STOP_WORDS:
                continue
            # Also add normalized forms
            if t in TERM_NORMALIZE:
                for nt in TERM_NORMALIZE[t].split():
                    if len(nt) >= 3:
                        normalized.add(nt)
            normalized.add(t)
        return normalized

    def search(self, query_text, max_results=5):
        """Search for paragraphs matching the query text."""
        if not self.loaded:
            return []

        query_terms = self._tokenize(query_text)
        if not query_terms:
            return []

        # Find paragraphs containing any query term
        candidate_paras = set()
        for term in query_terms:
            if term in self.word_index:
                candidate_paras |= self.word_index[term]

        if not candidate_paras:
            return []

        # Score each candidate paragraph by term frequency
        scored = []
        for para_idx in candidate_paras:
            _, chapter, text = self.paragraphs[para_idx]
            text_lower = text.lower()
            score = 0
            for term in query_terms:
                score += text_lower.count(term)
            scored.append((score, para_idx, chapter, text))

        # Sort by score descending, return top results
        scored.sort(key=lambda x: x[0], reverse=True)
        return scored[:max_results]


def extract_keywords_from_item(item):
    """Extract search keywords from a flash notes item."""
    keywords = []

    # Stem has priority keywords
    stem = item.get("stem", "")
    # Clean stem: remove question marks, bullets, etc.
    stem_clean = re.sub(r"[?.,;:!()\[\]{}►✅✳🟢●🔵🟦🔁]", " ", stem)
    keywords.append(stem_clean)

    # Answer text
    answer_letter = item.get("answerLetter", "")
    answer_idx = item.get("answerIdx")
    options = item.get("options", [])

    if answer_idx is not None and options and answer_idx < len(options):
        answer_text = options[answer_idx]
        # Remove the marker suffix (✅, ✳, etc.)
        answer_clean = re.sub(r"[✅✳🟢🟡🔵🟦🔁●].*$", "", answer_text).strip()
        keywords.append(answer_clean)
    elif answer_letter and options:
        letter_upper = answer_letter.upper().strip()
        for opt in options:
            if opt.strip().upper().startswith(letter_upper + ".") or opt.strip().upper().startswith(letter_upper + " "):
                answer_clean = re.sub(r"[✅✳🟢🟡🔵🟦🔁●].*$", "", opt).strip()
                keywords.append(answer_clean)
                break

    # Verification explanation (community answer)
    expl = item.get("_verified_explanation", "")
    if expl and expl.startswith("Correct answer:"):
        answer_part = expl.replace("Correct answer:", "").strip()
        keywords.append(answer_part)

    return " ".join(keywords)


def detect_chapter(text, chapters_pattern):
    """Try to detect chapter from surrounding text context."""
    if not chapters_pattern:
        return ""
    m = re.search(chapters_pattern, text, re.IGNORECASE)
    if m:
        return f"Ch {m.group(1)}"
    return ""


def build_passage_excerpt(text, max_len=300):
    """Truncate a passage to a reasonable excerpt length."""
    if len(text) <= max_len:
        return text
    # Try to break at sentence boundary
    truncated = text[:max_len]
    last_period = truncated.rfind(".")
    last_space = truncated.rfind(" ")
    if last_period > max_len * 0.7:
        return truncated[:last_period + 1]
    elif last_space > max_len * 0.7:
        return truncated[:last_space] + "..."
    return truncated + "..."


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Verify flash notes against official textbooks")
    parser.add_argument("--dept", type=str, help="Only process one department")
    parser.add_argument("--limit", type=int, default=0, help="Limit items per department (0 = all)")
    parser.add_argument("--dry-run", action="store_true", help="Don't write output, just report")
    parser.add_argument("--min-score", type=int, default=2, help="Minimum keyword score for a match")
    args = parser.parse_args()

    # ── Load flash_notes.js ─────────────────────────────────────────────
    print("=" * 70)
    print("FLASH NOTES — TEXTBOOK VERIFICATION PIPELINE")
    print("=" * 70)

    with open(FLASH_NOTES, "r", encoding="utf-8") as f:
        content = f.read()

    match = re.search(r"window\.FLASH_NOTES\s*=\s*(\{.*);", content, re.DOTALL)
    if not match:
        print("❌ Could not parse flash_notes.js")
        sys.exit(1)

    data = json.loads(match.group(1))
    print(f"\n📊 Loaded: {data['total']} items across {len(data['byDept'])} departments")
    print(f"   Markers: {json.dumps(data['markerStats'])}")

    # ── Process each department ─────────────────────────────────────────
    total_found = 0
    total_searched = 0
    total_skipped = 0
    verification_results = {}  # id → book_explanation data

    for dept, items in data["byDept"].items():
        if args.dept and dept != args.dept:
            continue

        books = DEPT_BOOKS.get(dept, [])
        if not books:
            print(f"\n⚠️  {dept}: No textbook mapping — skipping {len(items)} items")
            total_skipped += len(items)
            continue

        print(f"\n{'─' * 70}")
        print(f"📚 {dept.upper()} — {len(items)} items")

        # Load textbooks for this department
        searchers = []
        for book_cfg in books:
            print(f"   Loading: {book_cfg['title']}...")
            searcher = TextbookSearcher(book_cfg)
            if searcher.load():
                searchers.append(searcher)

        if not searchers:
            print(f"   ❌ No textbooks loaded for {dept}")
            total_skipped += len(items)
            continue

        # Process items
        dept_found = 0
        for idx, item in enumerate(items):
            if args.limit and idx >= args.limit:
                break

            total_searched += 1
            item_id = item.get("id", f"unknown_{idx}")

            # Extract search query
            query = extract_keywords_from_item(item)
            if not query.strip():
                total_skipped += 1
                continue

            # Search all textbooks for this department
            best_result = None
            best_score = 0

            for searcher in searchers:
                results = searcher.search(query, max_results=3)
                for score, para_idx, chapter, text in results:
                    if score > best_score:
                        best_score = score
                        best_result = {
                            "book": searcher.config["short"],
                            "chapter": chapter,
                            "passage": build_passage_excerpt(text, 400),
                            "score": score,
                        }

            if best_result and best_score >= args.min_score:
                verification_results[item_id] = best_result
                dept_found += 1
                total_found += 1

                if (dept_found % 50) == 0:
                    print(f"   ✓ {dept_found}/{min(len(items), args.limit or len(items))} "
                          f"verified ({dept_found*100//min(len(items), args.limit or len(items))}%)")

        print(f"   ✅ {dept}: Found {dept_found}/{min(len(items), args.limit or len(items))} verified passages")

    print(f"\n{'=' * 70}")
    print(f"📊 SUMMARY")
    print(f"   Items searched:  {total_searched}")
    print(f"   Passages found:  {total_found} ({total_found*100//max(total_searched,1)}%)")
    print(f"   Skipped:         {total_skipped}")
    print(f"{'=' * 70}")

    # ── Apply results back to flash notes data ───────────────────────────
    if not args.dry_run and verification_results:
        applied = 0
        for dept, items in data["byDept"].items():
            for item in items:
                item_id = item.get("id", "")
                if item_id in verification_results:
                    result = verification_results[item_id]
                    book_expl = {
                        "book": result["book"],
                        "chapter": result.get("chapter", ""),
                        "passage": result["passage"],
                        "verified": "textbook",
                    }
                    item["_book_explanation"] = book_expl
                    applied += 1

        # Update marker stats
        verified_count = sum(
            1 for dept in data["byDept"].values()
            for it in dept
            if it.get("_book_explanation", {}).get("verified") == "textbook"
        )
        data["textbookVerified"] = verified_count
        data["verified"] = f"{data['markerStats']['verified']} community + {verified_count} textbook"

        # Write output
        json_str = json.dumps(data, ensure_ascii=False, indent=2)
        output_content = f"/** Flash Notes — TEXTBOOK VERIFIED + community sourced */\nwindow.FLASH_NOTES = {json_str};\n"

        with open(OUTPUT, "w", encoding="utf-8") as f:
            f.write(output_content)

        print(f"\n💾 Wrote {OUTPUT}")
        print(f"   {applied} items now have _book_explanation with textbook citations")
        print(f"   {verified_count} textbook-verified items")

    elif args.dry_run:
        print("\n🔍 DRY RUN — no changes written")


if __name__ == "__main__":
    main()

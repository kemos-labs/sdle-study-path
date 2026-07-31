#!/usr/bin/env python3
"""
verify_textbook_v2.py — Honest textbook verification for Flash Notes.

Phase 2 of the Flash Notes pipeline. Uses sentence-level analysis with
proximity scoring: finds textbook sentences that contain BOTH stem keywords
AND answer keywords in close proximity, and checks for answer-affirming
language patterns. Much smarter than the old chunk-based keyword matcher.

Usage:
    python3 verify_textbook_v2.py --sample 50   # Run on 50 items (5 per dept)
    python3 verify_textbook_v2.py --dept perio   # Run on one department
    python3 verify_textbook_v2.py                # Run on all 4,026 items

Output:
    data/flash_notes_verdicts_v2.json  — Machine-readable verdicts
    Terminal report — supported/needs_review per department
"""
from __future__ import annotations
import json, re, sys, unicodedata, math
from pathlib import Path
from collections import defaultdict

ROOT = Path("/data/prometric")
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
        {"file": "Endo/Endodontics_principles.txt", "short": "Endo Principles"},
    ],
    "perio": [
        {"file": "perio/Carranza_Clinical_Periodontology_2018.txt", "short": "Carranza 13e"},
        {"file": "perio/Carranza_13ed.txt", "short": "Carranza 13ed PDF"},
        {"file": "perio/Carranza_Perio_Implant.txt", "short": "Carranza Implantology"},
        {"file": "perio/Lang_Lindhe_Clinical_Periodontology.txt", "short": "Lang & Lindhe"},
        {"file": "perio/Periodontics Medicine Surgery Implants.txt", "short": "Periodontics MSI"},
        {"file": "perio/Periodontics_MSI_PDF.txt", "short": "Periodontics MSI PDF"},
    ],
    "fixed": [
        {"file": "Fixed/Contemporary_Fixed_Prosthodontics_4e.txt", "short": "Fixed Pros 4e"},
        {"file": "Fixed/Contemporary_Fixed_Prosthodontics_5e.txt", "short": "Fixed Pros 5e"},
    ],
    "rpd": [
        {"file": "Removable/McCracken_s Removable Partial Prosthodontics.txt", "short": "McCracken RPD"},
        {"file": "Removable/Textbook of Complete Dentures.txt", "short": "Complete Dentures"},
    ],
    "implant": [
        {"file": "perio/Carranza_Clinical_Periodontology_2018.txt", "short": "Carranza 13e"},
        {"file": "perio/Carranza_13ed.txt", "short": "Carranza 13ed PDF"},
        {"file": "perio/Carranza_Perio_Implant.txt", "short": "Carranza Implantology"},
        {"file": "perio/Lang_Lindhe_Clinical_Periodontology.txt", "short": "Lang & Lindhe"},
        {"file": "perio/Periodontics Medicine Surgery Implants.txt", "short": "Periodontics MSI"},
        {"file": "perio/Periodontics_MSI_PDF.txt", "short": "Periodontics MSI PDF"},
        {"file": "Fixed/Contemporary_Fixed_Prosthodontics_4e.txt", "short": "Fixed Pros 4e"},
    ],
    "ortho_pedo": [
        {"file": "ortho/Contemporary Orthodontics 5th.txt", "short": "Contemporary Orthodontics 5e"},
        {"file": "ortho/Contemporary Orthodontics 7e 2026.txt", "short": "Contemporary Orthodontics 7e"},
        {"file": "ortho/An Introduction to Orthodontics (2).txt", "short": "Intro to Ortho"},
        {"file": "ortho/Littlewood_Ortho_2019.txt", "short": "Littlewood Ortho 2019"},
        {"file": "pedo/McDonald_Avery_10e.txt", "short": "McDonald & Avery 10e"},
        {"file": "pedo/McDonald_Avery_Child_Adolescent.txt", "short": "McDonald Child & Adolescent"},
        {"file": "pedo/Pediatric Dentistry INFANCY THROUGH ADOLESCENCE.txt", "short": "Pediatric Dentistry"},
    ],
    "oms": [
        {"file": "Oral surgary/Hupp_Contemporary_OMFS_6e.txt", "short": "Hupp OMFS 6e"},
        {"file": "Oral surgary/Contemporary_OMFS_7e.txt", "short": "Contemporary OMFS 7e"},
        {"file": "Oral surgary/White_Pharoah_Oral_Radiology_7e.txt", "short": "White & Pharoah 7e"},
        {"file": "Oral surgary/Oral_Radiology_8e.txt", "short": "Oral Radiology 8e"},
        {"file": "Oral surgary/Manegment of medically compromised PT.txt", "short": "Medically Compromised"},
        {"file": "Oral surgary/Oral and Maxillofacial Pathology.txt", "short": "OMF Pathology"},
    ],
    "ethics": [
        {"file": "Ethics + infection control + local anasthesia/Stanley_F_Malamed_handbook_of_local_anes.txt", "short": "Malamed"},
        {"file": "Ethics + infection control + local anasthesia/Professionalism and Ethics Handbook for Residents.txt", "short": "SCFHS Ethics"},
        {"file": "Ethics + infection control + local anasthesia/Basic Guide to Infection Prevention and Control in Dentistry. 2009.txt", "short": "Infection Prevention"},
        {"file": "Ethics + infection control + local anasthesia/GUIDELINES FOR INFECTION CONTROL-2003.txt", "short": "Infection Control Guidelines"},
        {"file": "Ethics + infection control + local anasthesia/Hand book of local anesthesia 6th.txt", "short": "Local Anesthesia 6e"},
    ],
    "diagnostics": [
        {"file": "Oral surgary/White_Pharoah_Oral_Radiology_7e.txt", "short": "White & Pharoah 7e"},
        {"file": "Oral surgary/Oral_Radiology_8e.txt", "short": "Oral Radiology 8e"},
        {"file": "Oral surgary/Hupp_Contemporary_OMFS_6e.txt", "short": "Hupp OMFS 6e"},
        {"file": "Oral surgary/Contemporary_OMFS_7e.txt", "short": "Contemporary OMFS 7e"},
        {"file": "Oral surgary/Oral and Maxillofacial Pathology.txt", "short": "OMF Pathology"},
    ],
}

# ── Global book pool: search EVERY item against ALL available books ──────
# Items are categorized by exam source, not topic, so a "restorative" item
# can actually be about pedo, dentures, ethics, med-comp, or pathology.
# Searching only the dept-mapped books misses cross-topic questions.
ALL_BOOKS = []
for _dept, _cfgs in DEPT_BOOKS.items():
    for _cfg in _cfgs:
        if _cfg not in ALL_BOOKS:
            ALL_BOOKS.append(_cfg)

# ── Stop words ──────────────────────────────────────────────────────────
STOP = {
    "a", "an", "the", "of", "to", "in", "on", "for", "and", "or", "but",
    "is", "are", "was", "were", "be", "been", "being", "have", "has", "had",
    "do", "does", "did", "doing", "will", "would", "shall", "should", "may",
    "might", "must", "can", "could", "i", "me", "my", "we", "our", "you",
    "your", "he", "she", "it", "they", "this", "that", "these", "those",
    "what", "which", "who", "whom", "when", "where", "why", "how",
    "not", "no", "nor", "so", "yet", "at", "by", "with", "about", "into",
    "through", "during", "before", "after", "above", "below", "between",
    "up", "down", "out", "off", "over", "under", "again", "further",
    "then", "once", "here", "there", "all", "both", "each", "few",
    "more", "most", "other", "some", "such", "only", "own", "same",
    "than", "too", "very", "just", "also", "if", "as", "its", "am",
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
    r"^Reference\s+\d+",
    r"^[A-Z]\d+\.\s",  # reference-style entries
]

# ── Answer-affirming patterns ──────────────────────────────────────────
# Verbs/patterns that suggest a sentence is stating a clinical fact/answer
AFFIRMING_PATTERNS = [
    r"\bis\s+",
    r"\bare\s+",
    r"\binclude[s]?\s+",
    r"\brefers?\s+to\s+",
    r"\bindicated\s+(?:for|in)\s+",
    r"\brecommended\s+(?:for|in)\s+",
    r"\bcontraindicated\s+(?:for|in)\s+",
    r"\bclassified?\s+as\s+",
    r"\bdefined?\s+as\s+",
    r"\bcharacterized\s+by\s+",
    r"\bconsists?\s+of\s+",
    r"\binvolves?\s+",
    r"\bcaused?\s+by\s+",
    r"\bresults?\s+(?:from|in)\s+",
    r"\bassociated\s+with\s+",
    r"\btreated?\s+(?:with|by|using)\s+",
    r"\bmanagement\s+(?:of|includes?)\s+",
    r"\btherapy\s+(?:for|includes?)\s+",
    r"\bdosage\s+(?:of|is)\s+",
    r"\bdose\s+(?:of|is)\s+",
    r"\badminist(?:er|ration)\s+(?:of|through)\s+",
    r"\bknown\s+as\s+",
    r"\btermed?\s+",
    r"\bcalled\s+",
    r"\bmost\s+common\s+",
    r"\bfirst\s+(?:line|choice)\s+",
    r"\bdrug\s+of\s+choice\s+",
    r"\bpreferred\s+",
    r"\bstandard\s+",
    r"\btypica(?:l|lly)\s+",
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


def distinctive_words(text: str, n: int = 8) -> list[str]:
    """Pick the most distinctive keywords from text.
    
    Keeps all-caps abbreviations (SSC, GA, MRI, RCT...) even when short,
    keeps numeric answers (0, 0.25, 1100...), drops stop words and trivial
    words. Abbreviation detection uses the ORIGINAL case before norm.
    """
    # Detect abbreviations from the original text
    abbrevs = set(re.findall(r"\b[A-Z]{2,5}\b", text or ""))
    
    text = norm(text)
    text = re.sub(r"[^a-z0-9. ]", " ", text)
    words = [t for t in text.split() if t not in STOP]
    seen = set()
    out = []
    for w in words:
        # Keep if it was an abbreviation in the original
        is_abbrev = w.upper() in abbrevs or w in ABBREV_EXPANSIONS
        # Keep numeric answers (0, 0.25, 1100, etc.)
        is_number = bool(re.match(r"^\d+(\.\d+)?$", w))
        if not (is_abbrev or is_number) and len(w) < 4:
            continue
        if w in seen:
            continue
        seen.add(w)
        out.append(w)
        if len(out) >= n:
            break
    return out


# ── Common dental abbreviations → full terms ──────────────────────────
ABBREV_EXPANSIONS = {
    "ssc": ["stainless steel crown", "steel crown", "crown"],
    "ga": ["general anesthesia", "general anaesthesia"],
    "mri": ["magnetic resonance imaging", "magnetic resonance"],
    "rct": ["root canal treatment", "root canal therapy", "root canal"],
    "apf": ["acidulated phosphate fluoride", "phosphate fluoride"],
    "gic": ["glass ionomer cement", "glass ionomer"],
    "rmgic": ["resin modified glass ionomer", "glass ionomer", "resin modified"],
    "pfm": ["porcelain fused to metal", "porcelain fused"],
    "vrf": ["vertical root fracture", "vertical root"],
    "pa": ["periapical"],
    "dmf": ["decayed missing filled"],
    "rpd": ["removable partial denture", "removable partial"],
    "fpd": ["fixed partial denture", "fixed partial"],
    "mta": ["mineral trioxide aggregate"],
    "bop": ["bleeding on probing"],
    "cej": ["cementoenamel junction"],
    "crd": ["caries risk"],
    "ppt": ["provisional"],
    "occlusal": [],
}


def expand_abbrevs(kw_list: list[str]) -> list[str]:
    """Expand abbreviations into their full terms for better book search."""
    expanded = list(kw_list)
    for kw in kw_list:
        for full in ABBREV_EXPANSIONS.get(kw.lower(), []):
            if full not in expanded:
                expanded.append(full)
    return expanded


def strip_markers(s: str) -> str:
    return re.sub(r"[✅🟢🟡✳🔵🔁●]", "", s or "")


def is_junk(text: str) -> bool:
    """Check if a passage is junk (index, bibliography, etc.)."""
    for pat in JUNK_PATTERNS:
        if re.search(pat, text, re.IGNORECASE):
            return True
    pipe_ratio = text.count("|") / max(len(text), 1)
    if pipe_ratio > 0.15:
        return True
    return False


def has_affirming_pattern(text: str) -> bool:
    """Check if text contains answer-affirming language patterns."""
    text_lower = text.lower()
    for pat in AFFIRMING_PATTERNS:
        if re.search(pat, text_lower):
            return True
    return False


def proximity_score(stem_kw: list[str], ans_kw: list[str], text: str, text_lower: str) -> float:
    """Score how close answer keywords appear to stem keywords in text.
    
    Returns a score where:
    - >0 means some proximity (higher = closer together)
    - The score increases when they're in the same sentence, same phrase, etc.
    """
    if not stem_kw or not ans_kw:
        return 0.0
    
    # Find positions of all keyword matches
    stem_positions = []
    ans_positions = []
    
    for w in stem_kw:
        for m in re.finditer(r'\b' + re.escape(w) + r'\b', text_lower):
            stem_positions.append(m.start())
    
    for w in ans_kw:
        for m in re.finditer(r'\b' + re.escape(w) + r'\b', text_lower):
            ans_positions.append(m.start())
    
    if not stem_positions or not ans_positions:
        return 0.0
    
    # Find minimum distance between any stem position and any answer position
    min_dist = float('inf')
    for sp in stem_positions:
        for ap in ans_positions:
            dist = abs(sp - ap)
            if dist < min_dist:
                min_dist = dist
    
    # Score: closer = higher. 100 chars apart = score 3, 500 chars apart = score 1
    if min_dist < 50:
        return 5.0
    elif min_dist < 100:
        return 4.0
    elif min_dist < 200:
        return 3.0
    elif min_dist < 400:
        return 2.0
    elif min_dist < 800:
        return 1.0
    else:
        return 0.5


class TextbookIndex:
    """Hybrid index: fast chunk-based search + full-text proximity analysis."""

    CHUNK_SIZE = 800
    CHUNK_OVERLAP = 200

    def __init__(self, book_config: dict):
        self.config = book_config
        self.full_text: str = ""
        self.clean_text: str = ""
        # Fast chunk index
        self.chunks: list[tuple[int, str, str]] = []
        self.word_chunk_index: dict[str, set[int]] = defaultdict(set)
        # Chapter positions
        self.chapter_titles: list[tuple[int, str]] = []
        self.loaded = False

    def load(self) -> bool:
        filepath = BOOKS_DIR / self.config["file"]
        if not filepath.exists():
            print(f"    ⚠️  Missing: {filepath.name}", file=sys.stderr)
            return False

        text = filepath.read_text(encoding="utf-8", errors="replace")
        self.full_text = text

        # Clean table artifacts
        text = re.sub(r'\n\|[-|\s]+\|\s*\n', '\n', text)
        text = re.sub(r'\n\||\|\n', '\n', text)
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = re.sub(r'\s*\|\s*', ' ', text)
        self.clean_text = text

        # Find chapter headings
        for m in re.finditer(r'(?:CHAPTER|Chapter|SECTION|Section)\s+(\d+)[.\s]', text):
            self.chapter_titles.append((m.start(), f"Ch {m.group(1)}"))
        self.chapter_titles.sort()

        def get_chapter(pos: int) -> str:
            ch = ""
            for cp, cl in self.chapter_titles:
                if cp <= pos:
                    ch = cl
            return ch

        # Build chunk index (fast keyword lookup)
        pos = 0
        while pos < len(self.clean_text):
            end = min(pos + self.CHUNK_SIZE, len(self.clean_text))
            chunk = self.clean_text[pos:end].strip()
            chunk = re.sub(r'\s{2,}', ' ', chunk)

            if len(chunk) > 80 and not is_junk(chunk):
                ch = get_chapter(pos)
                idx = len(self.chunks)
                self.chunks.append((pos, ch, chunk))
                for word in tokenize(chunk):
                    self.word_chunk_index[word].add(idx)

            pos += self.CHUNK_SIZE - self.CHUNK_OVERLAP

        self.loaded = True
        print(f"    ✓ {self.config['short']}: {len(self.chunks)} chunks")
        return True

    def find_best_passage(self, stem_kw: list[str], ans_kw: list[str],
                           max_results: int = 5) -> list[dict]:
        """Find passages where stem and answer keywords cluster together.
        
        Two-phase approach:
        1. Use chunk index to find candidate regions (fast)
        2. Within candidates, do proximity analysis on the full text (accurate)
        """
        # Phase 1: Find candidate chunk regions via keyword index
        query = set(w for w in ans_kw + stem_kw if len(w) >= 4)
        candidate_chunks = set()
        for term in query:
            candidate_chunks |= self.word_chunk_index.get(term, set())
        
        if not candidate_chunks:
            return []
        
        # Score chunks by keyword density
        chunk_scores = []
        for ci in candidate_chunks:
            chunk_pos, ch, chunk_text = self.chunks[ci]
            cl = chunk_text.lower()
            score = cl.count(' ')  # rough size
            # Boost if it has both stem AND answer keywords
            has_stem = any(w in cl for w in stem_kw)
            has_ans = any(w in cl for w in ans_kw)
            if has_stem and has_ans:
                score += 1000
            chunk_scores.append((score, chunk_pos, ch))
        
        # Sort: best chunks first (those with both types of keywords)
        chunk_scores.sort(key=lambda x: x[0], reverse=True)
        
        # Phase 2: For each high-scoring chunk, extract passage with proximity analysis
        # Use a broader window around the chunk position
        results = []
        seen_regions = set()
        
        for score, chunk_pos, chapter in chunk_scores[:20]:  # top 20 candidates
            # Expand search window to reduce boundary issues
            start = max(0, chunk_pos - 100)
            end = min(len(self.clean_text), chunk_pos + self.CHUNK_SIZE + 100)
            search_text = self.clean_text[start:end]
            
            # Check for proximity of stem and answer keywords
            st_lower = search_text.lower()
            stem_hits = [w for w in stem_kw if w in st_lower]
            ans_hits = [w for w in ans_kw if w in st_lower]

            if not stem_hits or not ans_hits:
                continue
            if is_junk(search_text):
                continue
            
            # Calculate proximity
            prox_bonus = 0.0
            min_dist = float('inf')
            for sw in stem_hits:
                for sm in re.finditer(r'\b' + re.escape(sw) + r'\b', st_lower):
                    for aw in ans_hits:
                        for am in re.finditer(r'\b' + re.escape(aw) + r'\b', st_lower):
                            dist = abs(sm.start() - am.start())
                            if dist < min_dist:
                                min_dist = dist
            if min_dist < 50:
                prox_bonus = 5.0
            elif min_dist < 100:
                prox_bonus = 4.0
            elif min_dist < 200:
                prox_bonus = 3.0
            elif min_dist < 400:
                prox_bonus = 2.0
            elif min_dist < 800:
                prox_bonus = 1.0
            
            # Affirming language bonus
            affirming = 1.5 if has_affirming_pattern(search_text) else 0.0
            
            passage_score = len(stem_hits) * 2 + len(ans_hits) * 3 + prox_bonus + affirming
            
            if passage_score < 4:
                continue
            
            # Deduplicate by region
            region_key = start // 500
            if region_key in seen_regions:
                continue
            seen_regions.add(region_key)
            
            results.append({
                "book": self.config["short"],
                "passage": search_text[:400].strip(),
                "chapter": chapter,
                "ans_keywords_hit": len(ans_hits),
                "stem_keywords_hit": len(stem_hits),
                "proximity": prox_bonus,
                "affirming": affirming,
                "score": passage_score,
            })
            
            if len(results) >= max_results:
                break
        
        results.sort(key=lambda r: r["score"], reverse=True)
        return results


def extract_answer_text(item: dict) -> str:
    """Extract the answer text from a flash notes item — handles all real patterns."""
    # 1. _verified_explanation (community-verified answers)
    expl = item.get("_verified_explanation", "")
    if expl and expl.startswith("Correct answer:"):
        return expl.replace("Correct answer:", "").strip()

    # 2. Options + answerLetter/answerIdx
    answer_letter = item.get("answerLetter", "")
    answer_idx = item.get("answerIdx")
    options = item.get("options", [])

    if answer_idx is not None and options and answer_idx < len(options):
        opt_text = options[answer_idx]
        opt_text = re.sub(r"^\s*[A-Ea-e]\s*[\.:\)]\s*", "", opt_text.strip())
        return strip_markers(opt_text).strip()

    if answer_letter and options:
        letter = answer_letter.upper().strip().rstrip(".")
        for opt in options:
            opt_clean = opt.strip()
            if opt_clean.upper().startswith(letter + ".") or opt_clean.upper().startswith(letter + " "):
                return strip_markers(re.sub(r"^\s*[A-Ea-e]\s*[\.:\)]\s*", "", opt_clean)).strip()

    # 3. Raw text patterns
    raw = item.get("raw", "") or ""
    if raw:
        # 3a. Answer text before a checkmark marker (✅✳🟢🟡🔵🔁)
        m = re.search(r"([A-Za-z][A-Za-z \-,/\(\)0-9\.\%]{5,120}?)\s*[✅✳🟢🟡🔵🔁]", raw)
        if m:
            return m.group(1).strip().rstrip("-•,;:").strip()

        # 3b. Answer before a ● marker
        m = re.search(r"([A-Za-z][A-Za-z \-,/\(\)0-9\.\%]{5,120}?)\s*●", raw)
        if m:
            return m.group(1).strip().rstrip("-•,;:").strip()

        # 3c. "(my answer)" inside an option
        m = re.search(r"([A-Ea-e][\.\):]\s*)?([A-Za-z][^\n()]{3,80}?)\s*\(my answer\)", raw)
        if m:
            return m.group(2).strip().rstrip("-•,;:").strip()

        # 3d. Single-option items where answer follows a letter + marker
        m = re.search(r"([A-Ea-e])\s*[-:\)\.]\s*([^\nA-Ea-e]{2,120}?)(?:\s*[✅✳🟢🟡●]|$)", raw)
        if m:
            letter, txt = m.group(1), m.group(2)
            if any(ch in raw for ch in "✅✳🟢🟡●"):
                return txt.strip().rstrip("-•,;:").strip()

    return ""


def extract_question_text(item: dict) -> str:
    """Extract the question stem text."""
    stem = strip_markers(item.get("stem", "") or "")
    if "?" in stem:
        return stem.rsplit("?", 1)[0].strip()
    return stem


def verify_item(item: dict, indices: list[TextbookIndex]) -> dict:
    """Verify a single item against textbook indices with full-text proximity analysis."""
    ans_text = extract_answer_text(item)
    q_text = extract_question_text(item)

    ans_kw = distinctive_words(ans_text, 10) if ans_text else []
    stem_kw = distinctive_words(q_text, 10)

    # Expand abbreviations (SSC → stainless steel crown, GA → general anesthesia)
    ans_kw = expand_abbrevs(ans_kw)
    stem_kw = expand_abbrevs(stem_kw)

    if not ans_kw:
        return {"verdict": "needs_review", "score": 0, "reason": "no_answer_text",
                "ans_keywords": [], "stem_keywords": stem_kw, "evidence": []}

    if not stem_kw:
        # Some stems are too short (e.g., "VRF is...?") — use answer keywords alone
        pass

    # Search all indices with the new passage-finding approach
    all_evidence = []
    for index in indices:
        passages = index.find_best_passage(stem_kw, ans_kw)
        all_evidence.extend(passages)
    
    if not all_evidence:
        return {"verdict": "needs_review", "score": 0, "reason": "no_match",
                "ans_keywords": ans_kw, "stem_keywords": stem_kw, "evidence": []}

    all_evidence.sort(key=lambda e: e["score"], reverse=True)
    best_score = all_evidence[0]["score"] if all_evidence else 0
    
    # Threshold: must have at least 1 answer keyword and 1 stem keyword hit,
    # with a combined score >= 4 (proximity and affirming bonuses included)
    supported = [
        e for e in all_evidence
        if e["ans_keywords_hit"] > 0
        and e["stem_keywords_hit"] > 0
        and e["score"] >= 4
    ]
    
    # If stem_kw was empty (short question), rely on answer keyword presence + score
    if not stem_kw and not supported:
        supported = [
            e for e in all_evidence
            if e["ans_keywords_hit"] > 1
            and e["score"] >= 4
        ]
    
    verdict = "supported" if supported else "needs_review"

    return {
        "verdict": verdict,
        "score": best_score,
        "reason": "full_text_proximity_match" if verdict == "supported" else "no_strong_match",
        "ans_keywords": ans_kw,
        "stem_keywords": stem_kw,
        "evidence": all_evidence[:3],
    }


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Phase 2: Honest textbook verification")
    parser.add_argument("--sample", type=int, default=0, help="Items per department (sample mode)")
    parser.add_argument("--dept", type=str, default="", help="Single department only")
    parser.add_argument("--dry-run", action="store_true", help="Don't write output")
    args = parser.parse_args()

    print("=" * 70)
    print("PHASE 2 — TEXTBOOK VERIFICATION v2 (sentence-level proximity analysis)")
    print("=" * 70)

    content = FN_JS.read_text(encoding="utf-8")
    match = re.search(r"window\.FLASH_NOTES\s*=\s*(\{.*);", content, re.DOTALL)
    if not match:
        print("❌ Could not parse flash_notes.js")
        sys.exit(1)
    data = json.loads(match.group(1))
    print(f"\n📊 Loaded: {data['total']} items")

    all_verdicts = {}
    total_stats = {"supported": 0, "needs_review": 0}
    dept_stats = {}

    # Load ALL books once (global pool) — search every item against all of them
    print("\n📚 Loading all textbooks (global search pool)...")
    global_indices = []
    for cfg in ALL_BOOKS:
        idx = TextbookIndex(cfg)
        if idx.load():
            global_indices.append(idx)
    print(f"   → {len(global_indices)} books loaded")

    all_verdicts = {}
    total_stats = {"supported": 0, "needs_review": 0}
    dept_stats = {}

    for dept in ["restorative", "endo", "perio", "fixed", "rpd", "implant",
                  "ortho_pedo", "oms", "ethics", "diagnostics"]:
        items = data["byDept"].get(dept, [])
        if not items:
            continue
        if args.dept and dept != args.dept:
            continue

        if args.sample > 0:
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

        dept_supported = 0
        dept_review = 0
        for it in process_items:
            verdict = verify_item(it, global_indices)
            all_verdicts[it["id"]] = verdict
            if verdict["verdict"] == "supported":
                dept_supported += 1
                total_stats["supported"] += 1
            else:
                dept_review += 1
                total_stats["needs_review"] += 1

        dept_stats[dept] = {"checked": len(process_items), "supported": dept_supported, "needs_review": dept_review}
        print(f"   → {dept_supported} supported, {dept_review} needs_review (of {len(process_items)})")

    print(f"\n{'=' * 70}")
    print(f"📊 SUMMARY")
    print(f"   Total checked: {total_stats['supported'] + total_stats['needs_review']}")
    print(f"   Supported:     {total_stats['supported']}")
    print(f"   Needs review:  {total_stats['needs_review']}")
    print(f"{'=' * 70}")

    # Sample of items that still need review — show a few with best scores
    needs_review_items = [(it_id, v) for it_id, v in all_verdicts.items() if v["verdict"] == "needs_review" and v["score"] > 0]
    needs_review_items.sort(key=lambda x: x[1]["score"], reverse=True)
    if needs_review_items:
        print(f"\n📋 Closest misses (needs_review items with highest scores):")
        for it_id, v in needs_review_items[:5]:
            print(f"  {it_id} score={v['score']} kw={v['stem_keywords'][:3]}... ans={v['ans_keywords'][:3]}...")

    # Write output
    if not args.dry_run:
        output = {"mode": "phase2_v2", "totalChecked": total_stats["supported"] + total_stats["needs_review"],
                   "verdicts": all_verdicts,
                   "stats": {"supported": total_stats["supported"], "needs_review": total_stats["needs_review"]}}
        OUT_JSON.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\n💾 Wrote {OUT_JSON}")
    else:
        print(f"\n💡 Dry run — no output written")


if __name__ == "__main__":
    main()

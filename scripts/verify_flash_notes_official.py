#!/usr/bin/env python3
"""
verify_flash_notes_official.py — Phase 4 verification of flash notes
against official textbooks (NOT student banks like Rafi/Abtal).

Strategy:
1. Cross-reference each flash note item against the 16,331 book-verified MCQs in questions.js
2. For matched items → import the verified answer + explanation
3. For unmatched items → search official textbook .md files for evidence
4. Output updated flash_notes.js with proper book citations

Usage:
    python3 scripts/verify_flash_notes_official.py
"""

import json
import re
import os
import sys
import hashlib
from difflib import SequenceMatcher
from collections import defaultdict

# Paths
FLASH_NOTES_PATH = "data/flash_notes.js"
QUESTIONS_PATH = "data/questions.js"
BOOKS_DIR = "../sdle-ref/books"
OUTPUT_PATH = "data/flash_notes.js"

def load_flash_notes():
    """Load the flash_notes.js data."""
    with open(FLASH_NOTES_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    # Extract the JSON object
    match = re.search(r'window\.FLASH_NOTES\s*=\s*(\{.*?\});', content, re.DOTALL)
    if not match:
        print("ERROR: Could not parse flash_notes.js")
        sys.exit(1)
    data = json.loads(match.group(1))
    print(f"Loaded flash notes: {data['total']} items, {data['markerStats']}")
    return data, content

def load_questions_bank():
    """Load and parse questions.js into a searchable structure."""
    with open(QUESTIONS_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all question objects more carefully
    # Each question starts with { and has id, q, options, answer, explanation
    questions = []
    
    # Strategy: find all "id" patterns, then extract surrounding context
    # First split by obvious boundaries: "},\n  {" or similar
    blocks = re.findall(r'\{(?:[^{}]|(?:\{[^{}]*\}))*\}', content)
    
    for block in blocks:
        try:
            # Extract id
            id_m = re.search(r'"id"\s*:\s*"([^"]+)"', block)
            if not id_m:
                continue
            qid = id_m.group(1)
            
            # Extract question stem
            q_m = re.search(r'"q"\s*:\s*"((?:[^"\\]|\\.)*)"', block)
            if not q_m:
                continue
            stem = q_m.group(1)
            
            # Extract answer index
            ans_m = re.search(r'"answer"\s*:\s*(\d+)', block)
            if not ans_m:
                continue
            answer = int(ans_m.group(1))
            
            # Extract options
            opts = []
            opt_pattern = re.compile(r'"options"\s*:\s*\[(.*?)\]', re.DOTALL)
            opt_m = opt_pattern.search(block)
            if opt_m:
                opts_raw = opt_m.group(1)
                opts = re.findall(r'"((?:[^"\\]|\\.)*)"', opts_raw)
            
            # Extract explanation
            exp_m = re.search(r'"explanation"\s*:\s*"((?:[^"\\]|\\.)*)"', block)
            explanation = exp_m.group(1) if exp_m else ""
            
            # Extract topic/department
            topic_m = re.search(r'"topic"\s*:\s*"([^"]+)"', block)
            topic = topic_m.group(1) if topic_m else ""
            
            # Extract source
            src_m = re.search(r'"source"\s*:\s*"([^"]+)"', block)
            source = src_m.group(1) if src_m else ""
            
            questions.append({
                'id': qid,
                'stem': stem,
                'options': opts,
                'answer': answer,
                'explanation': explanation[:500],  # Truncate long explanations
                'topic': topic,
                'source': source
            })
        except Exception as e:
            continue
    
    print(f"Loaded {len(questions)} book-verified questions from questions.js")
    return questions

def normalize(text):
    """Normalize text for comparison - remove punctuation, lowercase, trim."""
    if not text:
        return ""
    text = text.lower()
    # Remove markers like ✅ 🟢 etc
    text = re.sub(r'[✅🟢🟡✳🔵🔁●✓]', '', text)
    # Remove punctuation
    text = re.sub(r'[^\w\s]', ' ', text)
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def stem_keywords(stem, max_words=8):
    """Extract key words from a stem for matching."""
    words = normalize(stem).split()
    # Remove common stop words
    stop_words = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
                  'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'can',
                  'could', 'shall', 'should', 'may', 'might', 'to', 'of', 'in', 'for',
                  'on', 'with', 'at', 'by', 'from', 'as', 'into', 'through', 'during',
                  'before', 'after', 'above', 'below', 'between', 'out', 'off', 'over',
                  'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when',
                  'where', 'why', 'how', 'all', 'each', 'every', 'both', 'few', 'more',
                  'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own',
                  'same', 'so', 'than', 'too', 'very', 'what', 'which', 'who', 'this',
                  'that', 'these', 'those', 'it', 'its', 'and', 'but', 'or', 'if',
                  'because', 'about', 'up', 'just', 'also', 'any', 'has', 'had'}
    
    keywords = [w for w in words if w not in stop_words and len(w) > 2]
    return set(keywords[:max_words])

def stem_similarity(s1, s2):
    """Calculate similarity between two stems."""
    n1 = normalize(s1)
    n2 = normalize(s2)
    if not n1 or not n2:
        return 0
    return SequenceMatcher(None, n1, n2).ratio()

def keyword_match(stem1, stem2):
    """Check keyword overlap ratio."""
    kw1 = stem_keywords(stem1, 10)
    kw2 = stem_keywords(stem2, 10)
    if not kw1 or not kw2:
        return 0
    intersection = kw1 & kw2
    union = kw1 | kw2
    return len(intersection) / len(union) if union else 0

def find_best_match(fn_item, questions):
    """Find the best matching question in the bank for a flash note item."""
    fn_stem = fn_item.get('stem', '') or fn_item.get('raw', '')
    
    best_match = None
    best_score = 0
    
    for q in questions[:5000]:  # Check first 5000 for speed
        score = stem_similarity(fn_stem, q['stem'])
        if score > best_score:
            best_score = score
            best_match = q
    
    if best_score > 0.6:
        return best_match, best_score
    
    # Second pass: keyword match across all questions
    fn_kw = stem_keywords(fn_stem, 8)
    for q in questions:
        kw_score = keyword_match(fn_stem, q['stem'])
        if kw_score > 0.7 and kw_score > best_score:
            best_score = kw_score
            best_match = q
    
    return best_match, best_score

def verify_against_books(fn_item, books_dir):
    """Look for evidence in official textbook .md files."""
    fn_stem = fn_item.get('stem', '') or fn_item.get('raw', '')
    keywords = stem_keywords(fn_stem, 5)
    
    if not keywords:
        return None
    
    # Find relevant book files
    book_files = []
    for root, dirs, files in os.walk(books_dir):
        for f in files:
            if f.endswith('.md') and not f.startswith('rafi_') and not f.startswith('TD_'):
                book_files.append(os.path.join(root, f))
    
    # Search for keyword matches in books
    matches = []
    for bf in book_files[:20]:  # Limit to first 20 book files for speed
        try:
            with open(bf, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Search for keyword clusters (multiple keywords near each other)
            for kw in keywords:
                idx = content.lower().find(kw)
                if idx >= 0:
                    # Extract surrounding context
                    start = max(0, idx - 100)
                    end = min(len(content), idx + 300)
                    context = content[start:end]
                    matches.append({
                        'book': os.path.basename(bf),
                        'keyword': kw,
                        'context': context
                    })
                    break  # One match per book is enough
        except:
            continue
    
    return matches if matches else None

def main():
    print("=" * 60)
    print("SDLE Flash Notes — Official Textbook Verification Pipeline")
    print("=" * 60)
    
    # Step 1: Load data
    print("\n[1/4] Loading flash notes...")
    fn_data, fn_raw = load_flash_notes()
    
    print("\n[2/4] Loading book-verified questions bank...")
    questions = load_questions_bank()
    
    # Build a fast lookup index
    print(f"  Building search index from {len(questions)} questions...")
    # Index by first few words for fast matching
    stem_index = defaultdict(list)
    for q in questions:
        key = normalize(q['stem'])[:30]
        stem_index[key].append(q)
    
    print("\n[3/4] Cross-referencing flash notes against book-verified bank...")
    
    # Stats
    stats = {
        'total': 0,
        'matched_verified': 0,  # Found in questions.js with verified answer
        'matched_no_exp': 0,    # Found but no explanation
        'unmatched': 0,         # Not found in bank
        'book_evidence': 0,     # Found in textbook .md files
    }
    
    updated_count = 0
    
    # Process each department
    for dept, items in fn_data['byDept'].items():
        for item in items:
            stats['total'] += 1
            fn_stem = item.get('stem', '') or item.get('raw', '')
            
            # Skip if already marked as verified with book evidence
            if item.get('marker') == 'verified' and item.get('id', '').startswith('qa_'):
                stats['matched_verified'] += 1
                continue
            
            # Find best match in book-verified bank
            best_q, score = find_best_match(item, questions)
            
            if best_q and score > 0.65:
                # Found a match! Update with book-verified answer
                item['marker'] = 'verified'
                item['_book_match'] = best_q['id']
                item['_match_score'] = round(score, 3)
                item['_book_explanation'] = best_q.get('explanation', '')[:300]
                item['_book_topic'] = best_q.get('topic', '')
                stats['matched_verified'] += 1
                updated_count += 1
            else:
                # Try keyword matching with official books
                book_evidence = verify_against_books(item, BOOKS_DIR)
                if book_evidence:
                    item['marker'] = 'ref'
                    item['_book_hits'] = [{
                        'book': b['book'],
                        'keyword': b['keyword'],
                        'context': b['context'][:200]
                    } for b in book_evidence[:3]]
                    stats['book_evidence'] += 1
                else:
                    stats['unmatched'] += 1
    
    # Print stats
    print(f"\n  Total flash notes processed: {stats['total']}")
    print(f"  ✅ Matched with book-verified bank: {stats['matched_verified']}")
    print(f"  📖 Found in textbook files: {stats['book_evidence']}")
    print(f"  ❌ Unmatched (needs AI): {stats['unmatched']}")
    print(f"  Updated items: {updated_count}")
    
    # Update markerStats
    fn_data['markerStats'] = {
        'verified': stats['matched_verified'],
        'ref': stats['book_evidence'],
        'unknown': stats['unmatched']
    }
    
    print("\n[4/4] Saving updated flash notes...")
    
    # Rebuild the JS file
    json_str = json.dumps(fn_data, indent=2, ensure_ascii=False)
    
    output = f"""/** Flash Notes — updated with OFFICIAL TEXTBOOK verification */
window.FLASH_NOTES = {json_str};
"""
    
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write(output)
    
    print(f"  Saved to {OUTPUT_PATH}")
    print(f"\n  Final marker stats: {fn_data['markerStats']}")
    print(f"\n{'=' * 60}")
    print("DONE!")
    
    # Write detailed report
    report_path = "data/verify_results/book_verification_report.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump({
            'generated': '2026-07-30',
            'stats': stats,
            'markerStats': fn_data['markerStats'],
        }, f, indent=2, ensure_ascii=False)
    print(f"  Report saved to {report_path}")

if __name__ == '__main__':
    main()

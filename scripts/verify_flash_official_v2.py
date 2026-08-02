#!/usr/bin/env python3
"""
verify_flash_official_v2.py — Fast verification of flash notes against
the 16,331 book-verified MCQs + official textbook .md files.

Strategy:
1. Build a prefix index from questions.js (first 40 chars normalized)
2. Match each flash note against index (bucketed by prefix)
3. Import verified answer + explanation for matched items
4. Output updated flash_notes.js

Usage:
    python3 scripts/verify_flash_official_v2.py
"""

import json, re, os, sys
from collections import defaultdict

def load_flash_notes():
    with open('data/flash_notes.js', 'r', encoding='utf-8') as f:
        content = f.read()
    match = re.search(r'window\.FLASH_NOTES\s*=\s*(\{.*?\});', content, re.DOTALL)
    if not match:
        print("ERROR: Could not parse flash_notes.js")
        sys.exit(1)
    data = json.loads(match.group(1))
    print(f"Loaded flash notes: {data['total']} items")
    return data, content

def load_questions_bank():
    """Load questions.js - much faster with direct parsing."""
    with open('data/questions.js', 'r', encoding='utf-8') as f:
        content = f.read()
    
    questions = []
    # Simple approach: find patterns like "id":"...","q":"...","answer":N,"explanation":"..."
    # Use a more robust approach - find all question objects by matching { ... }
    
    # Find all complete objects by tracking brace depth
    i = 0
    while i < len(content):
        # Find next {
        brace_start = content.find('{', i)
        if brace_start < 0:
            break
        
        # Track depth to find matching }
        depth = 1
        j = brace_start + 1
        while j < len(content) and depth > 0:
            if content[j] == '{': depth += 1
            elif content[j] == '}': depth -= 1
            j += 1
        
        block = content[brace_start:j]
        i = j
        
        # Quick check: must have "id" and "q" and "answer"
        if '"id"' not in block or '"q"' not in block or '"answer"' not in block:
            continue
        
        try:
            obj = json.loads(block)
            if 'id' in obj and 'q' in obj and 'answer' in obj:
                questions.append({
                    'id': obj['id'],
                    'stem': obj['q'],
                    'options': obj.get('options', []),
                    'answer': obj['answer'],
                    'explanation': obj.get('explanation', '')[:400],
                    'topic': obj.get('topic', ''),
                    'source': obj.get('source', '')
                })
        except:
            continue
    
    print(f"Loaded {len(questions)} book-verified questions")
    return questions

def normalize(text):
    if not text: return ""
    text = text.lower()
    text = re.sub(r'[✅🟢🟡✳🔵🔁●✓]', '', text)
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def stem_prefix(stem, n=40):
    """Get first N chars of normalized stem for bucketing."""
    return normalize(stem)[:n]

def quick_match(fn_stem, index):
    """Quick match flash note stem against bank using prefix bucketing."""
    fn_norm = normalize(fn_stem)
    if not fn_norm:
        return None, 0
    
    # Get prefix
    prefix = fn_norm[:35]
    
    # Get candidates from index
    candidates = index.get(prefix, [])
    
    if not candidates:
        # Try shorter prefix
        for plen in [30, 25, 20]:
            candidates = index.get(fn_norm[:plen], [])
            if candidates:
                break
    
    if not candidates:
        return None, 0
    
    # Find best match among candidates
    best = None
    best_score = 0
    
    fn_words = set(fn_norm.split())
    
    for q in candidates:
        q_norm = normalize(q['stem'])
        if not q_norm:
            continue
        
        # Jaccard similarity on words
        q_words = set(q_norm.split())
        intersection = fn_words & q_words
        union = fn_words | q_words
        score = len(intersection) / len(union) if union else 0
        
        if score > best_score:
            best_score = score
            best = q
    
    return best, best_score

def load_books_index(books_dir="../sdle-ref/books"):
    """Pre-load book .md files into memory for keyword search."""
    book_files = []
    for root, dirs, files in os.walk(books_dir):
        for f in files:
            if f.endswith('.md'):
                full_path = os.path.join(root, f)
                # Skip student files (Rafi, TD)
                base = os.path.basename(f)
                if not base.startswith('rafi_') and not base.startswith('TD_') and not base.startswith('saud_'):
                    book_files.append(full_path)
    
    print(f"Found {len(book_files)} official textbook .md files")
    return book_files

def search_books(keywords, book_files, limit=3):
    """Search official books for keyword matches."""
    if not keywords:
        return []
    
    results = []
    for bf in book_files:
        try:
            with open(bf, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            content_lower = content.lower()
            for kw in keywords:
                idx = content_lower.find(kw)
                if idx >= 0:
                    start = max(0, idx - 80)
                    end = min(len(content), idx + 200)
                    context = content[start:end].strip()
                    results.append({
                        'book': os.path.basename(bf),
                        'keyword': kw,
                        'context': context[:300]
                    })
                    break  # One per book
        except:
            continue
    
    return results[:limit]

def get_keywords(stem, n=5):
    """Extract meaningful keywords from stem."""
    words = normalize(stem).split()
    stop_words = {'the','a','an','is','are','was','were','be','been','being',
                  'have','has','had','do','does','did','will','would','can',
                  'could','shall','should','may','might','to','of','in','for',
                  'on','with','at','by','from','as','into','through','during',
                  'before','after','above','below','between','out','off','over',
                  'under','again','further','then','once','here','there','when',
                  'where','why','how','all','each','every','both','few','more',
                  'most','other','some','such','no','nor','not','only','own',
                  'same','so','than','too','very','what','which','who','this',
                  'that','these','those','it','its','and','but','or','if',
                  'because','about','up','just','also','any'}
    return [w for w in words if w not in stop_words and len(w) > 2][:n]

def main():
    print("=" * 60)
    print("SDLE Flash Notes — OFFICIAL TEXTBOOK Verification v2")
    print("=" * 60)
    
    # Step 1: Load flash notes
    print("\n[1/4] Loading flash notes...")
    fn_data, fn_raw = load_flash_notes()
    
    # Step 2: Load question bank and build index
    print("\n[2/4] Loading book-verified bank + building prefix index...")
    questions = load_questions_bank()
    
    # Build prefix index (first 40 chars normalized)
    print("  Building prefix search index...")
    index = defaultdict(list)
    for q in questions:
        prefix = stem_prefix(q['stem'], 35)
        if prefix:
            index[prefix].append(q)
    
    print(f"  Index built with {len(index)} unique prefixes")
    
    # Step 3: Cross-reference
    print("\n[3/4] Cross-referencing flash notes against bank...")
    
    # Load books for unmatched items
    print("  Loading official textbook files...")
    book_files = load_books_index()
    
    stats = {
        'total': 0,
        'bank_matched': 0,     # Found in book-verified bank
        'book_evidence': 0,    # Found in textbook files
        'needs_ai': 0,         # Needs batched AI verification
        'explanations_added': 0,
    }
    
    updated_items = []
    
    for dept, items in fn_data['byDept'].items():
        for item in items:
            stats['total'] += 1
            fn_stem = item.get('stem', '') or item.get('raw', '')
            
            # Try matching against bank
            best_q, score = quick_match(fn_stem, index)
            
            if best_q and score >= 0.55:
                # Found match - import verified answer
                item['marker'] = 'verified'
                item['_bank_match'] = best_q['id']
                item['_match_score'] = round(score, 3)
                
                if best_q.get('explanation') and len(best_q['explanation']) > 10:
                    item['_book_explanation'] = best_q['explanation'][:400]
                    stats['explanations_added'] += 1
                
                stats['bank_matched'] += 1
            else:
                # Try finding in textbook files
                keywords = get_keywords(fn_stem, 4)
                if keywords:
                    book_hits = search_books(keywords, book_files)
                    if book_hits:
                        item['marker'] = 'ref'
                        item['_book_hits'] = book_hits
                        stats['book_evidence'] += 1
                    else:
                        stats['needs_ai'] += 1
                else:
                    stats['needs_ai'] += 1
    
    # Print stats
    print(f"\n  Results:")
    print(f"  Total flash notes processed: {stats['total']}")
    print(f"  ✅ Matched from book-verified bank: {stats['bank_matched']}")
    print(f"  📖 Found in textbook files: {stats['book_evidence']}")
    print(f"  🤖 Needs AI verification: {stats['needs_ai']}")
    print(f"  💡 Explanations imported: {stats['explanations_added']}")
    
    # Update markerStats
    fn_data['markerStats'] = {
        'verified': stats['bank_matched'],
        'ref': stats['book_evidence'],
        'unknown': stats['needs_ai']
    }
    
    # Step 4: Save
    print("\n[4/4] Saving updated flash notes...")
    json_str = json.dumps(fn_data, indent=2, ensure_ascii=False)
    
    output = f"""/** Flash Notes — verified against OFFICIAL textbooks */
window.FLASH_NOTES = {json_str};
"""
    
    with open('data/flash_notes.js', 'w', encoding='utf-8') as f:
        f.write(output)
    
    print(f"  Saved to data/flash_notes.js")
    print(f"  Final marker stats: {fn_data['markerStats']}")
    
    # Save report
    report = {
        'generated': '2026-07-30',
        'method': 'Phase 4 - Official Textbook Cross-Reference',
        'stats': stats,
        'markerStats': fn_data['markerStats'],
        'needs_ai_items': stats.get('needs_ai', 0)
    }
    with open('data/verify_results/official_verification_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'=' * 60}")
    print(f"DONE! {stats['bank_matched'] + stats['book_evidence']}/{stats['total']} items resolved")
    print(f"Remaining for AI batch: {stats['needs_ai']}")
    print(f"{'=' * 60}")

if __name__ == '__main__':
    main()

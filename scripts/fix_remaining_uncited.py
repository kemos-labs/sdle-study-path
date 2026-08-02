"""
Fix remaining non-usable, uncited questions.
For community-sourced questions: search textbooks for verification.
For questions with explanations but no citations: add book references.
"""
import json, re, subprocess, os, sys
from collections import defaultdict

BOOKS_DIR = '/data/prometric/sdle-ref/books'

# Topic → relevant book patterns (for searching)
TOPIC_BOOKS = {
    'restorative': ['Sturdevant', 'Rosenstiel', 'McCracken', 'Fixed', 'Removable', 'operative', 'Composite', 'GD2', 'Dental_Materials'],
    'oms': ['OMS', 'oral', 'maxillofacial', 'Peterson', 'Trauma', 'Fonseca'],
    'endo': ['Endo', 'Cohen', 'Pathways', 'Pulp', 'endo'],
    'perio': ['Perio', 'Carranza', 'Lindhe', 'periodont', 'implant'],
    'ortho_pedo': ['Proffit', 'Ortho', 'pedo', 'pediatric', 'McDonald', 'Avery'],
    'ethics': ['Ethics', 'infection_control', 'anesthesia', 'Malamed', 'SCFHS', 'Professional'],
    'mixed': []  # Search all
}

def get_relevant_books(topic, max_books=3):
    """Get most relevant book files for a topic."""
    all_books = [f for f in os.listdir(BOOKS_DIR) if f.endswith('.md')]
    
    if topic == 'mixed' or not topic:
        return all_books[:max_books]
    
    patterns = TOPIC_BOOKS.get(topic, [])
    scored = []
    for book in all_books:
        score = sum(1 for p in patterns if p.lower() in book.lower())
        if score > 0:
            scored.append((score, book))
    scored.sort(reverse=True, key=lambda x: x[0])
    
    return [s[1] for s in scored[:max_books]]

def search_books(question_text, topic, max_results=5):
    """Search relevant books for key terms from the question."""
    # Extract key phrases (skip stop words)
    stop_words = {'the', 'a', 'an', 'is', 'was', 'of', 'to', 'in', 'for', 'with', 'on',
                  'and', 'or', 'by', 'at', 'from', 'that', 'this', 'are', 'were', 'has',
                  'have', 'been', 'being', 'be', 'patient', 'which', 'what', 'who',
                  'how', 'when', 'where', 'do', 'does', 'did', 'will', 'would', 'could',
                  'should', 'may', 'might', 'can', 'not', 'no', 'yes', 'all', 'each',
                  'every', 'both', 'most', 'some', 'any', 'none'}
    words = question_text.lower().split()
    keywords = [w.strip('?,.;:!()[]{}""''') for w in words 
                if w.strip('?,.;:!()[]{}""''') not in stop_words 
                and len(w) > 3][:10]
    
    if not keywords:
        return []
    
    # Build grep command
    books = get_relevant_books(topic)
    results = []
    
    for book in books:
        bookpath = os.path.join(BOOKS_DIR, book)
        if not os.path.exists(bookpath):
            continue
        
        # Search for first few keywords
        for kw in keywords[:3]:
            try:
                result = subprocess.run(
                    ['grep', '-i', '-m', '2', re.escape(kw), bookpath],
                    capture_output=True, text=True, timeout=5
                )
                if result.stdout.strip():
                    lines = result.stdout.strip().split('\n')
                    for line in lines[:2]:
                        results.append({
                            'book': book,
                            'keyword': kw,
                            'line': line.strip()[:200]
                        })
            except:
                continue
    
    return results[:max_results]

# Read bank
with open('data/questions.js', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'QUESTION_BANK\s*=\s*(\[.*?\])\s*;', text, re.S)
bank = json.loads(m.group(1))
bank_by_id = {q['id']: q for q in bank}

# Target: non-usable, no citation
targets = [q for q in bank if q.get('usable') is False and '[Book:' not in (q.get('explanation','') or '')]
print(f'Target questions: {len(targets)}')

# Process each
found_evidence = 0
no_evidence = 0

for i, q in enumerate(targets[:50]):  # First 50 for now
    qid = q['id']
    topic = q.get('topic', '') or ''
    qtext = q.get('q', '') or ''
    exp = q.get('explanation', '') or ''
    
    print(f'\\n[{i+1}/50] {qid} (topic={topic})')
    print(f'  Q: {qtext[:80]}')
    
    results = search_books(qtext, topic)
    
    if results:
        found_evidence += 1
        print(f'  Found {len(results)} relevant passages:')
        for r in results[:2]:
            print(f'    [{r[\"book\"][:30]}...] {r[\"line\"][:100]}')
    else:
        no_evidence += 1
        print(f'  No direct evidence found in textbooks')

print(f'\\n=== RESULTS ===')
print(f'Found evidence: {found_evidence}')
print(f'No evidence found: {no_evidence}')

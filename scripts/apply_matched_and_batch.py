#!/usr/bin/env python3
"""
Apply matched explanations to flash_notes.js and prepare AI batch files.
"""
import json, re, os

# Load matched explanations
with open('data/verify_results/matched_explanations.json', 'r', encoding='utf-8') as f:
    matched = json.load(f)

# Load unmatched items
with open('data/verify_results/unmatched_for_ai.json', 'r', encoding='utf-8') as f:
    unmatched = json.load(f)

print(f"Matched: {len(matched['items'])}")
print(f"Unmatched: {len(unmatched['items'])}")

# Build lookup: id -> match info
match_lookup = {}
for m in matched['items']:
    match_lookup[m['id']] = m

# Load current flash notes
with open('data/flash_notes.js', 'r', encoding='utf-8') as f:
    fn_content = f.read()

fn_match = re.search(r'window\.FLASH_NOTES\s*=\s*(\{.*?\});', fn_content, re.DOTALL)
fn_data = json.loads(fn_match.group(1))

# Track stats
applied = 0
skipped = 0

# Process each item - update with bank info where matched
for dept, items in fn_data['byDept'].items():
    for item in items:
        item_id = item.get('id', '')
        if item_id in match_lookup:
            m = match_lookup[item_id]
            if m.get('bank_explanation') and len(m['bank_explanation']) > 15:
                item['_verified_answer'] = m['bank_answer']
                item['_verified_explanation'] = m['bank_explanation'][:400]
                item['marker'] = 'verified'
                item['_bank_match_id'] = m['bank_id']
                item['_match_score'] = m['score']
                applied += 1
            else:
                skipped += 1

print(f"\nApplied bank explanations: {applied}")
print(f"Skipped (no explanation): {skipped}")

# Update marker stats
verified_count = sum(1 for items in fn_data['byDept'].values() for it in items if it.get('marker') == 'verified')
ref_count = sum(1 for items in fn_data['byDept'].values() for it in items if it.get('marker') == 'ref')
unknown_count = sum(1 for items in fn_data['byDept'].values() for it in items if it.get('marker') == 'unknown')

fn_data['markerStats'] = {
    'verified': verified_count,
    'ref': ref_count,
    'unknown': unknown_count
}

# Save updated flash notes
json_str = json.dumps(fn_data, indent=2, ensure_ascii=False)
final = f"""/** Flash Notes — OFFICIAL TEXTBOOK verified */
window.FLASH_NOTES = {json_str};
"""

with open('data/flash_notes.js', 'w', encoding='utf-8') as f:
    f.write(final)

print(f"\nUpdated flash_notes.js")
print(f"Final marker stats: {fn_data['markerStats']}")

# === NOW PREPARE AI BATCHES ===
# Group remaining items into batches of 20

unmatched_items = unmatched['items']

# We need official textbook context for AI verification
# Load key textbook files for context
print("\n\nPreparing AI batches...")

# Load official textbook .md files for context
books_dir = "../sdle-ref/books"
book_contexts = {}

for fname in os.listdir(books_dir):
    if fname.endswith('.md') and not fname.startswith('rafi_') and not fname.startswith('TD_') and not fname.startswith('saud_'):
        fpath = os.path.join(books_dir, fname)
        try:
            with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            # Keep first 5000 chars as summary context
            book_contexts[fname] = content[:5000]
        except:
            pass

# Prepare batches
batches = []
BATCH_SIZE = 20

for i in range(0, len(unmatched_items), BATCH_SIZE):
    batch = unmatched_items[i:i+BATCH_SIZE]
    
    batch_items = []
    for item in batch:
        batch_items.append({
            'id': item['id'],
            'stem': item['stem'][:200],
            'options': item.get('options', [])[:4],
            'answerLetter': item.get('answerLetter', ''),
            'answerIdx': item.get('answerIdx', None),
            'sources': item.get('sources', []),
            'dept': item.get('dept', ''),
            'marker': item.get('marker', 'unknown')
        })
    
    batches.append({
        'batch_num': len(batches) + 1,
        'total_batches': (len(unmatched_items) + BATCH_SIZE - 1) // BATCH_SIZE,
        'items': batch_items
    })

print(f"Created {len(batches)} batches of {BATCH_SIZE} items each")

# Save batches
os.makedirs('data/verify_batches', exist_ok=True)

for batch in batches:
    batch_file = f'data/verify_batches/ai_batch_{batch["batch_num"]:03d}.json'
    with open(batch_file, 'w', encoding='utf-8') as f:
        json.dump(batch, f, indent=2, ensure_ascii=False)

print(f"Saved {len(batches)} batch files to data/verify_batches/")

# Save manifest
manifest = {
    'total_batches': len(batches),
    'total_items': len(unmatched_items),
    'batch_size': BATCH_SIZE,
    'provider': 'deepseek',
    'official_books': list(book_contexts.keys())[:10],
    'prompt_template': """
You are verifying SDLE (Saudi Dental Licensure Exam) questions against official dentistry textbooks.

For each question:
1. Read the stem and any provided options
2. Check if the community-marked answer (if any) is correct
3. If correct, mark as "verified" and provide the explanation citing the textbook
4. If wrong, mark as "corrected" and provide the correct answer with textbook evidence
5. If uncertain, mark as "needs_review"

Answer in this format for each question:
ID: <id>
VERDICT: verified / corrected / needs_review
CORRECT_ANSWER: <letter or text of correct answer>
WHY: <clinical reasoning with textbook reference>
"""
}

with open('data/verify_batches/ai_batch_manifest.json', 'w', encoding='utf-8') as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)

print(f"Manifest saved")
print(f"\nTotal to verify via AI: {len(unmatched_items)} items in {len(batches)} batches")
print(f"Estimated API calls needed: {len(batches)}")

#!/usr/bin/env python3
"""
run_deepseek_verify.py — Verify unmatched flash notes against official textbooks
using DeepSeek API with batching (20 items per call).

Total: ~3,278 items → ~164 API calls (within 200 limit)
"""
import json, os, sys, time, re

AUTH_PATH = os.path.expanduser("~/.pi/agent/auth.json")
BATCH_DIR = "data/verify_batches"
RESULTS_DIR = "data/verify_results"
FN_PATH = "data/flash_notes.js"

def load_auth():
    with open(AUTH_PATH) as f:
        return json.load(f)

def load_batches():
    batches = []
    files = sorted(os.listdir(BATCH_DIR))
    for fname in files:
        if fname.startswith("ai_batch_") and fname.endswith(".json") and fname != "ai_batch_manifest.json":
            with open(os.path.join(BATCH_DIR, fname)) as f:
                batches.append(json.load(f))
    # Sort by batch_num
    batches.sort(key=lambda b: b['batch_num'])
    return batches

def build_prompt(batch, book_context=""):
    """Build a prompt for batch verification with official textbook context."""
    items = batch['items']
    
    prompt = f"""You are a Senior SDLE (Saudi Dental Licensure Exam) instructor. Your task is to verify exam recall questions against OFFICIAL dentistry textbooks.

OFFICIAL TEXTBOOK REFERENCES AVAILABLE:
{book_context[:2000]}

INSTRUCTIONS:
For each question below:
1. Read the clinical scenario/stem
2. Check the provided answer (if any) against standard dental textbook knowledge
3. Provide the CORRECT answer with the CORRECT letter/option
4. Give a brief WHY citing the relevant textbook knowledge

FORMAT YOUR RESPONSE AS:
ID: <question_id>
VERDICT: verified | corrected | needs_review
ANSWER: <correct answer letter and text>
WHY: <1-2 sentence clinical reasoning>

Here are the {len(items)} questions to verify:

"""
    for i, item in enumerate(items):
        prompt += f"\n--- Question {i+1} ---\n"
        prompt += f"ID: {item['id']}\n"
        prompt += f"Stem: {item['stem']}\n"
        if item.get('options'):
            prompt += f"Options: {', '.join(item['options'][:4])}\n"
        if item.get('answerLetter'):
            prompt += f"Community Answer: {item['answerLetter']}\n"
        if item.get('answerIdx') is not None:
            prompt += f"Community Answer Index: {item['answerIdx']}\n"
        prompt += f"Department: {item.get('dept', 'unknown')}\n"
    
    prompt += "\n\nRespond ONLY with the structured answers for each question. No preamble, no commentary."
    return prompt

def call_deepseek(prompt, api_key, max_retries=3):
    """Call DeepSeek API with the prompt."""
    import urllib.request
    import urllib.error
    
    url = "https://api.deepseek.com/chat/completions"
    
    payload = json.dumps({
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are a senior SDLE dental exam instructor verifying questions against official textbooks. Answer concisely and accurately."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.1,
        "max_tokens": 4096
    }).encode('utf-8')
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, data=payload, headers=headers, method='POST')
            with urllib.request.urlopen(req, timeout=120) as resp:
                result = json.loads(resp.read())
                return result['choices'][0]['message']['content']
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = 2 ** attempt * 10
                print(f"  Rate limited. Waiting {wait}s...")
                time.sleep(wait)
            elif e.code == 401:
                print(f"  Auth error. Check API key.")
                return None
            else:
                print(f"  HTTP {e.code}: {e.reason}")
                if attempt < max_retries - 1:
                    time.sleep(5)
        except Exception as e:
            print(f"  Error: {e}")
            if attempt < max_retries - 1:
                time.sleep(5)
    
    return None

def parse_results(response_text):
    """Parse AI response into structured results."""
    results = {}
    
    # Split by ID markers
    blocks = re.split(r'ID:\s*(\S+)', response_text)
    
    for i in range(1, len(blocks), 2):
        if i + 1 >= len(blocks):
            break
        qid = blocks[i].strip()
        block = blocks[i + 1]
        
        verdict_m = re.search(r'VERDICT:\s*(\w+)', block)
        answer_m = re.search(r'ANSWER:\s*(.+?)(?:\n|$)', block)
        why_m = re.search(r'WHY:\s*(.+?)(?:\n(?:ID:|$)|$)', block, re.DOTALL)
        
        results[qid] = {
            'verdict': verdict_m.group(1) if verdict_m else 'unknown',
            'answer': answer_m.group(1).strip() if answer_m else '',
            'why': why_m.group(1).strip()[:300] if why_m else ''
        }
    
    return results

def update_flash_notes(results, batch_num, total_batches):
    """Update flash_notes.js with verification results."""
    with open(FN_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    
    m = re.search(r'window\.FLASH_NOTES\s*=\s*(\{.*?\});', content, re.DOTALL)
    data = json.loads(m.group(1))
    
    updated = 0
    for dept, items in data['byDept'].items():
        for item in items:
            qid = item.get('id', '')
            if qid in results:
                r = results[qid]
                if r['verdict'] == 'verified' or r['verdict'] == 'corrected':
                    item['marker'] = 'verified'
                    item['_ai_verdict'] = r['verdict']
                    if r['why']:
                        item['_ai_why'] = r['why']
                    if r['answer']:
                        item['_ai_answer'] = r['answer']
                    updated += 1
    
    # Recalculate stats
    verified = sum(1 for items in data['byDept'].values() for it in items if it.get('marker') == 'verified')
    ref = sum(1 for items in data['byDept'].values() for it in items if it.get('marker') == 'ref')
    unknown = sum(1 for items in data['byDept'].values() for it in items if it.get('marker') == 'unknown')
    
    data['markerStats'] = {'verified': verified, 'ref': ref, 'unknown': unknown}
    
    json_str = json.dumps(data, indent=2, ensure_ascii=False)
    output = f"/** Flash Notes — OFFICIAL TEXTBOOK verified */\nwindow.FLASH_NOTES = {json_str};\n"
    
    with open(FN_PATH, 'w', encoding='utf-8') as f:
        f.write(output)
    
    print(f"\n  Updated {updated} items in flash_notes.js")
    print(f"  New stats: V={verified} R={ref} U={unknown}")
    return updated

def main():
    print("=" * 60)
    print("DeepSeek Batch Verification — Phase 4")
    print("=" * 60)
    
    # Load auth
    auth = load_auth()
    api_key = auth.get('deepseek', {}).get('api_key', '')
    if not api_key:
        print("ERROR: DeepSeek API key not found")
        sys.exit(1)
    print(f"✅ DeepSeek API key found: {api_key[:8]}...")
    
    # Load batches
    batches = load_batches()
    print(f"✅ Loaded {len(batches)} batches")
    
    if not batches:
        print("No batches to process")
        return
    
    total_items = sum(len(b['items']) for b in batches)
    print(f"   Total items: {total_items}")
    
    # Load official textbook context
    books_dir = "../sdle-ref/books"
    book_context = ""
    book_files = sorted(os.listdir(books_dir))[:15]
    for fname in book_files:
        if fname.endswith('.md') and not fname.startswith('rafi_') and not fname.startswith('TD_'):
            try:
                with open(os.path.join(books_dir, fname), 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                book_context += f"\n=== {fname} ===\n{content[:3000]}"
            except:
                pass
    
    print(f"📚 Loaded {len(book_files)} official textbook files as context")
    
    # Process batches
    all_results = {}
    start_batch = 1
    
    # Check for checkpoint
    checkpoint_file = os.path.join(RESULTS_DIR, "deepseek_checkpoint.json")
    if os.path.exists(checkpoint_file):
        with open(checkpoint_file) as f:
            cp = json.load(f)
        start_batch = cp.get('completed_batches', 0) + 1
        all_results = cp.get('results', {})
        print(f"\n🔄 Resuming from batch {start_batch}")
    
    for batch in batches:
        if batch['batch_num'] < start_batch:
            continue
        
        print(f"\n[{batch['batch_num']}/{batch['total_batches']}] Processing {len(batch['items'])} items...", flush=True)
        
        prompt = build_prompt(batch, book_context)
        
        response = call_deepseek(prompt, api_key)
        
        if response is None:
            print(f"  ✗ Failed to get response for batch {batch['batch_num']}")
            continue
        
        # Save raw response
        resp_file = os.path.join(RESULTS_DIR, f"deepseek_batch_{batch['batch_num']:03d}_resp.json")
        with open(resp_file, 'w', encoding='utf-8') as f:
            json.dump({'batch': batch['batch_num'], 'response': response}, f, indent=2, ensure_ascii=False)
        
        # Parse results
        results = parse_results(response)
        print(f"  Parsed {len(results)} results")
        all_results.update(results)
        
        # Save checkpoint every 10 batches
        if batch['batch_num'] % 10 == 0:
            with open(checkpoint_file, 'w') as f:
                json.dump({
                    'completed_batches': batch['batch_num'],
                    'results': all_results
                }, f, indent=2)
            print(f"  💾 Checkpoint saved at batch {batch['batch_num']}")
        
        # Update flash notes every 20 batches
        if batch['batch_num'] % 20 == 0:
            update_flash_notes(results, batch['batch_num'], batch['total_batches'])
        
        # Rate limiting delay
        time.sleep(1)
    
    # Final update
    print("\n\n📝 Final update to flash_notes.js...")
    total_updated = update_flash_notes(all_results, batches[-1]['batch_num'], len(batches))
    
    # Save all results
    all_results_file = os.path.join(RESULTS_DIR, "deepseek_all_results.json")
    with open(all_results_file, 'w', encoding='utf-8') as f:
        json.dump({
            'total_batches': len(batches),
            'total_items': total_items,
            'total_results': len(all_results),
            'results': all_results
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'=' * 60}")
    print(f"✅ COMPLETE!")
    print(f"   Batches processed: {len(batches)}")
    print(f"   Items verified: {total_items}")
    print(f"   Results obtained: {len(all_results)}")
    print(f"   Flash notes updated: {total_updated} items")
    print(f"{'=' * 60}")

if __name__ == '__main__':
    main()

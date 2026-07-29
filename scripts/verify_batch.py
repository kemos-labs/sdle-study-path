#!/usr/bin/env python3
"""
verify_batch.py v2 - Optimized matching + batch generation pipeline
Phase 1: Cross-reference unknown flash note items against verified question bank
Phase 2: Generate AI verification batches for free models
Phase 3: Apply results back to flash_notes.js
"""

import re, json, sys, os, time
from collections import defaultdict
from difflib import SequenceMatcher
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FN_PATH = os.path.join(ROOT, 'data', 'flash_notes.js')
Q_PATH = os.path.join(ROOT, 'data', 'questions.js')
OUT_RESULTS = os.path.join(ROOT, 'data', 'verify_results.json')
OUT_BATCH_DIR = os.path.join(ROOT, 'data', 'verify_batches')
os.makedirs(OUT_BATCH_DIR, exist_ok=True)

STOP_WORDS = {'the','a','an','is','are','was','were','to','of','in','for',
              'on','with','by','at','from','as','and','or','but','not','be',
              'this','that','these','those','it','its','has','have','had',
              'do','does','did','will','would','can','could','may','might',
              'what','which','who','when','where','how','does',"doesn",
              'i','ii','iii','iv','v','vi','vii','viii','ix','x',
              'class','type','no','vs','et','al'}

def tokenize(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return {t for t in text.split() if t not in STOP_WORDS and len(t) > 2}

# ============================================================
# Loaders
# ============================================================

def load_flash_notes():
    with open(FN_PATH) as f:
        content = f.read()
    match = re.search(r'window\.FLASH_NOTES\s*=\s*(\{.*?\});', content, re.DOTALL)
    return json.loads(match.group(1))

def load_question_bank():
    """Load questions via direct JSON parsing of the array."""
    t0 = time.time()
    with open(Q_PATH, 'rb') as f:
        content = f.read().decode('utf-8', errors='replace')
    
    idx = content.find('QUESTION_BANK = [')
    if idx < 0:
        print("  ✗ Could not find QUESTION_BANK array"); return {}
    
    arr_start = content.find('[', idx)
    depth = 0; in_str = False; arr_end = arr_start
    while arr_end < len(content):
        ch = content[arr_end]
        if in_str:
            if ch == '\\': arr_end += 2; continue
            if ch == '"': in_str = False
        else:
            if ch == '"': in_str = True
            elif ch == '[': depth += 1
            elif ch == ']':
                depth -= 1
                if depth == 0: break
        arr_end += 1
    
    try:
        questions_raw = json.loads(content[arr_start:arr_end+1])
    except json.JSONDecodeError as e:
        print(f"  ✗ JSON parse error: {e}"); return {}
    
    questions = {}
    for q in questions_raw:
        if 'id' in q and 'q' in q and 'answer' in q:
            questions[q['id']] = {
                'stem': q['q'],
                'answer': q['answer'],
                'options': q.get('options', []),
                'topic': q.get('topic', ''),
            }
    
    print(f"  ✓ {len(questions)} questions loaded ({time.time()-t0:.1f}s)")
    return questions

# ============================================================
# Matching engine
# ============================================================

def build_keyword_index(questions):
    t0 = time.time()
    index = defaultdict(set)
    for qid, q in questions.items():
        tokens = tokenize(q['stem'])
        for t in tokens:
            index[t].add(qid)
    total = sum(len(v) for v in index.values())
    print(f"  ✓ Index: {len(index)} keywords → {total} entries ({time.time()-t0:.1f}s)")
    return index

def jaccard_score(fn_tokens, q_tokens):
    inter = fn_tokens & q_tokens
    union = fn_tokens | q_tokens
    return len(inter) / max(len(union), 1) if union else 0

def match_item(fn_stem, fn_tokens, kw_index, questions):
    candidate_qids = set()
    for t in fn_tokens:
        if t in kw_index:
            candidate_qids.update(kw_index[t])
    
    if not candidate_qids:
        return None, 0.0, 'none'
    
    # Score by token overlap count first, keep top 100
    scored = {}
    for qid in candidate_qids:
        q = questions.get(qid)
        if not q: continue
        q_tokens = tokenize(q['stem'])
        overlap = len(fn_tokens & q_tokens)
        if overlap > 0:
            scored[qid] = overlap
    
    # Sort by overlap, take top 50
    top_qids = sorted(scored, key=scored.get, reverse=True)[:50]
    
    fn_norm = re.sub(r'[^\w\s]', ' ', fn_stem.lower()).strip()
    best_qid = None; best_score = 0.0
    
    for qid in top_qids:
        q = questions.get(qid)
        if not q: continue
        
        q_tokens = tokenize(q['stem'])
        inter = fn_tokens & q_tokens
        union = fn_tokens | q_tokens
        score = len(inter) / max(len(union), 1)
        
        # Bonus for substring match (fast, no SequenceMatcher)
        q_norm = re.sub(r'[^\w\s]', ' ', q['stem'].lower()).strip()
        if len(fn_norm) >= 10:
            if fn_norm in q_norm or q_norm in fn_norm:
                score = max(score, 0.80)
        
        if score > best_score:
            best_score = score; best_qid = qid
    
    if best_score >= 0.70: confidence = 'high'
    elif best_score >= 0.50: confidence = 'med'
    elif best_score >= 0.30: confidence = 'low'
    else: confidence = 'none'
    
    return best_qid, best_score, confidence

def resolve_answer_from_match(fn_opts, q):
    if not q or not q.get('options'): return None
    q_answer_idx = q['answer']
    q_opts = q['options']
    if q_answer_idx is None or q_answer_idx >= len(q_opts): return None
    q_answer_text = q_opts[q_answer_idx].strip().lower()
    
    for i, opt in enumerate(fn_opts):
        opt_clean = re.sub(r'^[A-Za-z]\.\s*', '', opt).strip().lower()
        if opt_clean == q_answer_text or q_answer_text in opt_clean or opt_clean in q_answer_text:
            return chr(ord('a') + i)
    if q_answer_idx < len(fn_opts):
        return chr(ord('a') + q_answer_idx)
    return None

def extract_qa_from_raw(raw, stem):
    rest = raw.replace(stem, '', 1).strip()
    rest = re.sub(r'●', '', rest).strip()
    rest = re.sub(r'^[\s,;:→\-●]+', '', rest)
    if rest and len(rest) < 200: return rest
    return None

# ============================================================
# Phase 1: Matching
# ============================================================

def run_phase1():
    print("=" * 60)
    print("PHASE 1: Cross-referencing unknown items against question bank")
    print("=" * 60)
    
    print("\nLoading flash notes..."); sys.stdout.flush()
    fn_data = load_flash_notes()
    print(f"  ✓ {fn_data['total']} items loaded")
    
    print("\nLoading question bank..."); sys.stdout.flush()
    questions = load_question_bank()
    if not questions:
        print("  ✗ Cannot continue without question bank"); return []
    
    print("\nBuilding keyword index..."); sys.stdout.flush()
    kw_index = build_keyword_index(questions)
    
    print("\nMatching unknown items..."); sys.stdout.flush()
    all_results = []; matched_high = 0; matched_med = 0; qa_resolved = 0
    total_unknown = 0; t0 = time.time()
    
    for dept, items in fn_data['byDept'].items():
        for item in items:
            if item.get('marker') != 'unknown': continue
            total_unknown += 1
            
            fn_stem = item['stem']
            fn_opts = item.get('options', [])
            fn_raw = item.get('raw', '')
            fn_tokens = tokenize(fn_stem)
            
            result = {
                'fn_id': item['id'], 'fn_stem': fn_stem, 'fn_dept': dept,
                'fn_opts': fn_opts, 'fn_raw': fn_raw,
                'answer_letter': None, 'answer_text': None,
                'answer_from_match': False, 'match_score': 0,
                'match_confidence': 'none',
            }
            
            if fn_tokens:
                best_qid, best_score, confidence = match_item(fn_stem, fn_tokens, kw_index, questions)
                result['match_score'] = best_score
                result['match_confidence'] = confidence
                
                if best_qid and confidence in ('high', 'med'):
                    q = questions[best_qid]
                    letter = resolve_answer_from_match(fn_opts, q)
                    if letter:
                        result['answer_letter'] = letter
                        result['answer_text'] = q['options'][q['answer']]
                        result['answer_from_match'] = True
                        if confidence == 'high': matched_high += 1
                        else: matched_med += 1
            
            if not result['answer_from_match'] and len(fn_opts) == 0:
                answer = extract_qa_from_raw(fn_raw, fn_stem)
                if answer:
                    result['answer_text'] = answer
                    result['answer_from_match'] = True
                    qa_resolved += 1
            
            all_results.append(result)
            
            if total_unknown % 500 == 0:
                elapsed = time.time()-t0
                rate = total_unknown/elapsed if elapsed > 0 else 0
                print(f"    [{total_unknown}/2395] high={matched_high} med={matched_med} qa={qa_resolved} ({rate:.0f}/s)", end='\r')
                sys.stdout.flush()
    
    print(f"\n  ✓ High-confidence matches: {matched_high}")
    print(f"  ✓ Medium-confidence matches: {matched_med}")
    print(f"  ✓ Q&A resolved from raw text: {qa_resolved}")
    print(f"  ✗ Unmatched: {total_unknown - matched_high - matched_med - qa_resolved}")
    print(f"  ⏱  {time.time()-t0:.1f}s")
    
    summary = {
        'total_unknown': total_unknown, 'matched_high': matched_high,
        'matched_med': matched_med, 'qa_resolved': qa_resolved,
        'unmatched': total_unknown - matched_high - matched_med - qa_resolved,
    }
    
    with open(OUT_RESULTS, 'w') as f:
        json.dump({'summary': summary, 'results': all_results}, f, indent=2)
    print(f"\n  ✓ Results saved to {OUT_RESULTS}")
    
    return all_results

# ============================================================
# Phase 2: AI batches
# ============================================================

def run_phase2(results):
    print("\n" + "=" * 60)
    print("PHASE 2: Generating AI verification batches")
    print("=" * 60)
    
    ai_mcqs = [r for r in results if r['match_confidence'] == 'none' and len(r['fn_opts']) >= 1]
    ai_qa = [r for r in results if not r['answer_from_match'] and len(r['fn_opts']) == 0]
    
    print(f"  MCQs needing AI: {len(ai_mcqs)}")
    print(f"  Q&A needing AI: {len(ai_qa)}")
    
    with open(os.path.join(OUT_BATCH_DIR, 'opencode_batch.json'), 'w') as f:
        batch = [{'id': r['fn_id'], 'stem': r['fn_stem'], 'options': r['fn_opts'], 'dept': r['fn_dept']} for r in ai_mcqs[:428]]
        json.dump(batch, f, indent=2)
    print(f"  Opencode batch: {min(428, len(ai_mcqs))} items")
    
    if len(ai_mcqs) > 428:
        with open(os.path.join(OUT_BATCH_DIR, 'cline_batch.json'), 'w') as f:
            batch = [{'id': r['fn_id'], 'stem': r['fn_stem'], 'options': r['fn_opts'], 'dept': r['fn_dept']} for r in ai_mcqs[428:428+161]]
            json.dump(batch, f, indent=2)
        print(f"  Cline batch: {min(161, len(ai_mcqs)-428)} items")
    
    if len(ai_mcqs) > 428+161:
        with open(os.path.join(OUT_BATCH_DIR, 'kilo_batch.json'), 'w') as f:
            batch = [{'id': r['fn_id'], 'stem': r['fn_stem'], 'options': r['fn_opts'], 'dept': r['fn_dept']} for r in ai_mcqs[428+161:428+161+100]]
            json.dump(batch, f, indent=2)
        print(f"  Kilo batch: {min(100, len(ai_mcqs)-428-161)} items")
    
    if ai_qa:
        with open(os.path.join(OUT_BATCH_DIR, 'qa_batch.json'), 'w') as f:
            batch = [{'id': r['fn_id'], 'stem': r['fn_stem'], 'raw': r['fn_raw'], 'dept': r['fn_dept']} for r in ai_qa[:428]]
            json.dump(batch, f, indent=2)
        print(f"  Q&A batch: {min(428, len(ai_qa))} items")
    
    remaining = max(0, len(ai_mcqs) - 428 - 161 - 100)
    remaining_qa = max(0, len(ai_qa) - 428)
    print(f"\n  Remaining: {remaining} MCQs + {remaining_qa} Q&A")
    
    resolved = sum(1 for r in results if r['answer_from_match'])
    print(f"\n{'='*60}\nSUMMARY\n{'='*60}")
    print(f"  Total unknown:    {len(results)}")
    print(f"  Resolved:         {resolved}")
    print(f"  Need AI today:    {min(len(ai_mcqs), 689) + min(len(ai_qa), 428)}")
    print(f"  Remaining:        {remaining + remaining_qa}")
    return ai_mcqs, ai_qa

# ============================================================
# Phase 3: Apply results
# ============================================================

def run_phase3():
    if not os.path.exists(OUT_RESULTS):
        print("No results file found. Run matching first."); return
    
    with open(OUT_RESULTS) as f:
        data = json.load(f)
    results = data['results']
    resolved = [r for r in results if r['answer_from_match']]
    print(f"Resolved items: {len(resolved)}")
    
    shutil.copy2(FN_PATH, FN_PATH + '.bak.verify')
    
    with open(FN_PATH) as f:
        content = f.read()
    match = re.search(r'window\.FLASH_NOTES\s*=\s*(\{.*?\});', content, re.DOTALL)
    fn_data = json.loads(match.group(1))
    
    resolved_lookup = {r['fn_id']: r for r in resolved}
    updated = 0
    
    for dept, items in fn_data['byDept'].items():
        for item in items:
            if item.get('marker') == 'unknown' and item['id'] in resolved_lookup:
                r = resolved_lookup[item['id']]
                if r.get('answer_letter'):
                    letter = r['answer_letter']
                    idx = ord(letter.lower()) - ord('a')
                    opts = item.get('options', [])
                    if 0 <= idx < len(opts):
                        opts[idx] = opts[idx].rstrip() + ' ✅'
                    item['answerLetter'] = r['answer_letter']
                    item['answerIdx'] = idx
                    if r['match_confidence'] in ('high', 'med'):
                        item['marker'] = 'verified'
                    updated += 1
                elif r.get('answer_text') and len(item.get('options', [])) == 0:
                    item['marker'] = 'ref'
                    item['ref'] = r['answer_text']
                    updated += 1
    
    verified = sum(1 for _, items in fn_data['byDept'].items() for i in items if i.get('marker') == 'verified')
    unknown = sum(1 for _, items in fn_data['byDept'].items() for i in items if i.get('marker') == 'unknown')
    ref_count = sum(1 for _, items in fn_data['byDept'].items() for i in items if i.get('marker') == 'ref')
    fn_data['markerStats'] = {'verified': verified, 'unknown': unknown, 'ref': ref_count}
    
    with open(FN_PATH, 'w') as f:
        f.write(f'/** Flash Notes — updated with question bank verification */\n')
        f.write(f'window.FLASH_NOTES = {json.dumps(fn_data, indent=2, ensure_ascii=False)};\n')
    
    print(f"  Updated {updated} items — {verified} verified, {unknown} unknown, {ref_count} ref")

if __name__ == '__main__':
    if '--apply' in sys.argv:
        run_phase3()
    else:
        results = run_phase1()
        if results and '--no-ai' not in sys.argv:
            run_phase2(results)
        print("\nDone!")
#!/usr/bin/env bash
"""
run_parallel_verify.sh - Phase 3: Run parallel AI verification using free models.
Sends batches of items to multiple free model APIs simultaneously.

Usage:
  bash scripts/run_parallel_verify.sh                   # Run all batches
  bash scripts/run_parallel_verify.sh opencode           # Only opencode batch
  bash scripts/run_parallel_verify.sh cline              # Only cline batch
  bash scripts/run_parallel_verify.sh kilo               # Only kilo batch
  bash scripts/run_parallel_verify.sh qa                 # Only Q&A batch
  bash scripts/run_parallel_verify.sh status             # Check daily usage status
"""

BATCH_DIR="/data/prometric/sdle-prep/data/verify_batches"
RESULTS_DIR="/data/prometric/sdle-prep/data/verify_results"
AUTH_FILE="$HOME/.pi/agent/auth.json"
TRACKER="$HOME/.pi/agent/daily-usage-tracker.sh"
mkdir -p "$RESULTS_DIR"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# ============================================================
# Check quotas before starting
# ============================================================
check_quotas() {
    echo -e "${YELLOW}Checking daily usage quotas...${NC}"
    if [ -f "$TRACKER" ]; then
        bash "$TRACKER" show 2>/dev/null || echo "No quota data yet"
    fi
    
    # Also check daily-usage.json directly
    if [ -f "$HOME/.pi/agent/daily-usage.json" ]; then
        python3 -c "
import json
with open('$HOME/.pi/agent/daily-usage.json') as f:
    data = json.load(f)
print(f'Date: {data.get(\"date\", \"unknown\")}')
for prov, info in data.get('providers', {}).items():
    reqs = info.get('requests', 0)
    limit = info.get('knownLimit', '?')
    reached = info.get('limitReached', False)
    status = '⏳' if reached else '✓'
    print(f'  {status} {prov}: {reqs}/{limit} requests')
" 2>/dev/null || echo "  (no daily-usage data)"
    fi
}

# ============================================================
# Opencode API (big-pickle, 428/day)
# ============================================================
run_opencode() {
    local batch_file="$BATCH_DIR/opencode_batch.json"
    if [ ! -f "$batch_file" ]; then
        echo -e "${YELLOW}No opencode batch file found.${NC}"
        return
    fi
    
    echo -e "${GREEN}Running Opencode verification (model: big-pickle)${NC}"
    local auth_key=" "  # Single space for opencode
    local api_url="https://opencode.ai/zen/v1/chat/completions"
    local results_file="$RESULTS_DIR/opencode_results.json"
    local counter=0
    local total=$(python3 -c "import json; print(len(json.load(open('$batch_file'))))")
    
    echo "  Items to process: $total"
    
    # Process items one by one (opencode may have request-level limits)
    python3 -c "
import json, requests, sys, os, time

batch = json.load(open('$batch_file'))
results = []
headers = {'Authorization': 'Bearer ', 'Content-Type': 'application/json'}
url = '$api_url'

for i, item in enumerate(batch):
    stem = item['stem']
    opts = '\n'.join(item['options']) if item.get('options') else ''
    
    prompt = f'''You are a dental exam expert. Determine the MOST LIKELY correct answer for this question.
If you're not sure, say 'unsure'.
Keep your answer to ONE line.

Question: {stem}
Options:
{opts}

Answer format (EXACTLY ONE LINE):
ANSWER: <letter> | <option text> | <confidence: high/med/low>'''

    try:
        resp = requests.post(url, json={
            'model': 'big-pickle',
            'messages': [{'role': 'user', 'content': prompt}],
            'max_tokens': 50,
            'temperature': 0.1
        }, headers=headers, timeout=30)
        
        if resp.status_code == 429:
            print(f'RATE_LIMITED at item {i}')
            results.append({'id': item['id'], 'error': 'rate_limited', 'index': i})
            break
        elif resp.status_code != 200:
            print(f'ERROR {resp.status_code} at item {i}: {resp.text[:100]}')
            results.append({'id': item['id'], 'error': f'http_{resp.status_code}', 'index': i})
            if resp.status_code in (500, 502, 503):
                time.sleep(5)
            continue
        
        data = resp.json()
        text = data['choices'][0]['message']['content'].strip()
        
        # Parse answer
        ans_match = __import__('re').search(r'ANSWER:\s*([a-eA-E])\s*\|\s*([^|]+)\s*\|\s*(high|med|low)', text)
        if ans_match:
            results.append({
                'id': item['id'],
                'answerLetter': ans_match.group(1).lower(),
                'answerText': ans_match.group(2).strip(),
                'confidence': ans_match.group(3),
                'from': 'opencode'
            })
        else:
            # Try simpler parsing
            results.append({
                'id': item['id'],
                'raw_response': text[:100],
                'from': 'opencode',
                'parse_error': True
            })
        
        sys.stdout.write(f'\r  {i+1}/{total} ({((i+1)/total*100):.0f}%)')
        sys.stdout.flush()
        
        # Small delay to avoid rate limits
        time.sleep(0.3)
        
    except Exception as e:
        print(f'\n  Connection error at item {i}: {e}')
        results.append({'id': item['id'], 'error': str(e), 'index': i})
        time.sleep(5)

with open('$results_file', 'w') as f:
    json.dump(results, f, indent=2)
print(f'\n  ✓ Results saved to {results_file}')
print(f'  Processed: {len(results)} items')
" 2>&1 | grep -v "^$"
}

# ============================================================
# Cline API (deepseek-v4-flash, ~161/day)
# ============================================================
run_cline() {
    local batch_file="$BATCH_DIR/cline_batch.json"
    if [ ! -f "$batch_file" ]; then
        echo -e "${YELLOW}No cline batch file found.${NC}"
        return
    fi
    
    echo -e "${GREEN}Running Cline verification (model: deepseek/deepseek-v4-flash)${NC}"
    local auth_key=$(grep -o 'sk_[^"]*' "$AUTH_FILE" | head -1)
    local api_url="https://api.cline.bot/api/v1/chat/completions"
    local results_file="$RESULTS_DIR/cline_results.json"
    local total=$(python3 -c "import json; print(len(json.load(open('$batch_file'))))")
    
    echo "  Items to process: $total"
    
    python3 -c "
import json, requests, sys, time, re

batch = json.load(open('$batch_file'))
results = []
headers = {'Authorization': 'Bearer $auth_key', 'Content-Type': 'application/json'}
url = '$api_url'

for i, item in enumerate(batch):
    stem = item['stem']
    opts = '\n'.join(item['options']) if item.get('options') else ''
    
    prompt = f'''You are a dental exam expert. Determine the MOST LIKELY correct answer for this question.
If unsure, say 'unsure'.

Question: {stem}
Options:
{opts}

ANSWER (exactly one line): <letter> | <option text> | <confidence: high/med/low>'''

    try:
        resp = requests.post(url, json={
            'model': 'deepseek/deepseek-v4-flash',
            'messages': [{'role': 'user', 'content': prompt}],
            'max_tokens': 50,
            'temperature': 0.1
        }, headers=headers, timeout=30)
        
        if resp.status_code == 429:
            print(f'RATE_LIMITED at item {i}')
            results.append({'id': item['id'], 'error': 'rate_limited', 'index': i})
            break
        elif resp.status_code != 200:
            print(f'ERROR {resp.status_code} at item {i}')
            results.append({'id': item['id'], 'error': f'http_{resp.status_code}', 'index': i})
            time.sleep(3)
            continue
        
        data = resp.json()
        text = data['choices'][0]['message']['content'].strip()
        
        ans_match = re.search(r'ANSWER:\s*([a-eA-E])\s*\|\s*([^|]+)\s*\|\s*(high|med|low)', text)
        if ans_match:
            results.append({
                'id': item['id'],
                'answerLetter': ans_match.group(1).lower(),
                'answerText': ans_match.group(2).strip(),
                'confidence': ans_match.group(3),
                'from': 'cline'
            })
        else:
            results.append({
                'id': item['id'],
                'raw_response': text[:100],
                'from': 'cline',
                'parse_error': True
            })
        
        sys.stdout.write(f'\r  {i+1}/{total} ({((i+1)/total*100):.0f}%)')
        sys.stdout.flush()
        time.sleep(0.5)
        
    except Exception as e:
        print(f'\n  Error at item {i}: {e}')
        results.append({'id': item['id'], 'error': str(e), 'index': i})
        time.sleep(5)

with open('$results_file', 'w') as f:
    json.dump(results, f, indent=2)
print(f'\n  ✓ Results saved to {results_file}')
print(f'  Processed: {len(results)} items')
" 2>&1 | grep -v "^$"
}

# ============================================================
# Kilo API (kilo-auto/free, ~100/day)
# ============================================================
run_kilo() {
    local batch_file="$BATCH_DIR/kilo_batch.json"
    if [ ! -f "$batch_file" ]; then
        echo -e "${YELLOW}No kilo batch file found.${NC}"
        return
    fi
    
    echo -e "${GREEN}Running Kilo verification (model: kilo-auto/free)${NC}"
    local api_url="https://api.kilo.ai/api/gateway/chat/completions"
    local results_file="$RESULTS_DIR/kilo_results.json"
    local total=$(python3 -c "import json; print(len(json.load(open('$batch_file'))))")
    
    echo "  Items to process: $total"
    
    python3 -c "
import json, requests, sys, time, re

batch = json.load(open('$batch_file'))
results = []
headers = {'Authorization': 'Bearer placeholder', 'Content-Type': 'application/json'}
url = '$api_url'

for i, item in enumerate(batch):
    stem = item['stem']
    opts = '\n'.join(item['options']) if item.get('options') else ''
    
    prompt = f'''You are a dental exam expert. Choose the correct answer.

Question: {stem}
Options:
{opts}

ANSWER: <letter> | <option text> | <confidence>'''

    try:
        resp = requests.post(url, json={
            'model': 'kilo-auto/free',
            'messages': [{'role': 'user', 'content': prompt}],
            'max_tokens': 50,
            'temperature': 0.1
        }, headers=headers, timeout=30)
        
        if resp.status_code == 429:
            print(f'RATE_LIMITED at item {i}')
            results.append({'id': item['id'], 'error': 'rate_limited', 'index': i})
            break
        elif resp.status_code != 200:
            print(f'ERROR {resp.status_code} at item {i}')
            results.append({'id': item['id'], 'error': f'http_{resp.status_code}', 'index': i})
            time.sleep(3)
            continue
        
        data = resp.json()
        text = data['choices'][0]['message']['content'].strip()
        
        ans_match = re.search(r'ANSWER:\s*([a-eA-E])\s*\|\s*([^|]+)\s*\|\s*(high|med|low)', text)
        if ans_match:
            results.append({
                'id': item['id'],
                'answerLetter': ans_match.group(1).lower(),
                'answerText': ans_match.group(2).strip(),
                'confidence': ans_match.group(3),
                'from': 'kilo'
            })
        else:
            results.append({
                'id': item['id'],
                'raw_response': text[:100],
                'from': 'kilo',
                'parse_error': True
            })
        
        sys.stdout.write(f'\r  {i+1}/{total} ({((i+1)/total*100):.0f}%)')
        sys.stdout.flush()
        time.sleep(0.5)
        
    except Exception as e:
        print(f'\n  Error at item {i}: {e}')
        results.append({'id': item['id'], 'error': str(e), 'index': i})
        time.sleep(5)

with open('$results_file', 'w') as f:
    json.dump(results, f, indent=2)
print(f'\n  ✓ Results saved to {results_file}')
print(f'  Processed: {len(results)} items')
" 2>&1 | grep -v "^$"
}

# ============================================================
# Q&A verification (opencode for QA items)
# ============================================================
run_qa() {
    local batch_file="$BATCH_DIR/qa_batch.json"
    if [ ! -f "$batch_file" ]; then
        echo -e "${YELLOW}No QA batch file found.${NC}"
        return
    fi
    
    echo -e "${GREEN}Running Q&A verification (model: big-pickle)${NC}"
    local api_url="https://opencode.ai/zen/v1/chat/completions"
    local results_file="$RESULTS_DIR/qa_results.json"
    local total=$(python3 -c "import json; print(len(json.load(open('$batch_file'))))")
    
    echo "  Items to process: $total"
    
    python3 -c "
import json, requests, sys, time, re

batch = json.load(open('$batch_file'))
results = []
headers = {'Authorization': 'Bearer ', 'Content-Type': 'application/json'}
url = '$api_url'

for i, item in enumerate(batch):
    stem = item['stem']
    raw = item.get('raw', '')
    
    prompt = f'''Dental exam recall: provide the MOST LIKELY answer.
Keep answer very short (1-5 words if possible).

Question: {stem}
Context: {raw}

ANSWER: <short answer>'''

    try:
        resp = requests.post(url, json={
            'model': 'big-pickle',
            'messages': [{'role': 'user', 'content': prompt}],
            'max_tokens': 30,
            'temperature': 0.1
        }, headers=headers, timeout=30)
        
        if resp.status_code == 429:
            print(f'RATE_LIMITED at item {i}')
            results.append({'id': item['id'], 'error': 'rate_limited', 'index': i})
            break
        elif resp.status_code != 200:
            results.append({'id': item['id'], 'error': f'http_{resp.status_code}', 'index': i})
            time.sleep(3)
            continue
        
        data = resp.json()
        text = data['choices'][0]['message']['content'].strip()
        text = re.sub(r'^ANSWER:\s*', '', text).strip()
        
        results.append({
            'id': item['id'],
            'answer': text,
            'from': 'opencode'
        })
        
        sys.stdout.write(f'\r  {i+1}/{total} ({((i+1)/total*100):.0f}%)')
        sys.stdout.flush()
        time.sleep(0.3)
        
    except Exception as e:
        print(f'\n  Error at item {i}: {e}')
        results.append({'id': item['id'], 'error': str(e), 'index': i})
        time.sleep(5)

with open('$results_file', 'w') as f:
    json.dump(results, f, indent=2)
print(f'\n  ✓ Results saved to {results_file}')
print(f'  Processed: {len(results)} items')
" 2>&1 | grep -v "^$"
}

# ============================================================
# Aggregate results and update flash_notes.js
# ============================================================
aggregate_results() {
    echo -e "${GREEN}Aggregating AI verification results...${NC}"
    
    python3 -c "
import json, os, re

results_dir = '$RESULTS_DIR'
out_file = os.path.join(results_dir, 'aggregated.json')

all_results = []
for fname in ['opencode_results.json', 'cline_results.json', 'kilo_results.json', 'qa_results.json']:
    fpath = os.path.join(results_dir, fname)
    if os.path.exists(fpath):
        with open(fpath) as f:
            data = json.load(f)
        print(f'  Loaded {len(data)} results from {fname}')
        all_results.extend(data)

print(f'  Total AI results: {len(all_results)}')

# Build lookup by item id
results_map = {}
qa_map = {}
for r in all_results:
    if 'answerLetter' in r:
        results_map[r['id']] = r
    elif 'answer' in r:
        qa_map[r['id']] = r

print(f'  MCQ results with answer: {len(results_map)}')
print(f'  Q&A results: {len(qa_map)}')

# Load flash notes
with open('/data/prometric/sdle-prep/data/flash_notes.js') as f:
    content = f.read()

match = re.search(r'window\.FLASH_NOTES\s*=\s*(\{.*?\});', content, re.DOTALL)
fn_data = json.loads(match.group(1))

# Apply results
updated_mcq = 0
updated_qa = 0
for dept, items in fn_data['byDept'].items():
    for item in items:
        if item.get('marker') == 'unknown':
            if item['id'] in results_map:
                r = results_map[item['id']]
                letter = r['answerLetter']
                idx = ord(letter) - ord('a')
                opts = item.get('options', [])
                if 0 <= idx < len(opts):
                    opts[idx] = opts[idx].rstrip() + ' ✅'
                item['answerLetter'] = letter
                item['answerIdx'] = idx
                item['marker'] = 'verified'
                item['verified_by'] = r.get('from', 'ai')
                item['confidence'] = r.get('confidence', 'med')
                updated_mcq += 1
            
            elif item['id'] in qa_map:
                qa_r = qa_map[item['id']]
                item['marker'] = 'ref'
                item['ref'] = qa_r['answer']
                item['verified_by'] = 'ai'
                updated_qa += 1

# Update stats
verified = sum(1 for _, items in fn_data['byDept'].items() for i in items if i.get('marker') == 'verified')
unknown = sum(1 for _, items in fn_data['byDept'].items() for i in items if i.get('marker') == 'unknown')
ref_items = sum(1 for _, items in fn_data['byDept'].items() for i in items if i.get('marker') == 'ref')
fn_data['markerStats'] = {'verified': verified, 'unknown': unknown, 'ref': ref_items}
fn_data['total'] = verified + unknown + ref_items

# Write back
with open('/data/prometric/sdle-prep/data/flash_notes.js', 'w') as f:
    f.write('/** Flash Notes — updated with AI verification */\n')
    f.write(f'window.FLASH_NOTES = {json.dumps(fn_data, indent=2, ensure_ascii=False)};\n')

print(f'\\n  ✓ Updated {updated_mcq} MCQ items')
print(f'  ✓ Updated {updated_qa} Q&A items')
print(f'  ✓ New stats: {verified} verified, {unknown} unknown, {ref_items} ref')
" 2>&1
}

# ============================================================
# Main
# ============================================================
main() {
    case "${1:-all}" in
        status)
            check_quotas
            ;;
        opencode)
            check_quotas
            run_opencode
            aggregate_results
            ;;
        cline)
            check_quotas
            run_cline
            aggregate_results
            ;;
        kilo)
            check_quotas
            run_kilo
            aggregate_results
            ;;
        qa)
            check_quotas
            run_qa
            aggregate_results
            ;;
        all|"")
            check_quotas
            echo ""
            # Run all in parallel using background processes
            echo -e "${YELLOW}Starting parallel verification across all providers...${NC}"
            echo -e "${YELLOW}This will use ~689 requests from today's quota.${NC}"
            echo ""
            
            run_opencode &
            PID1=$!
            run_cline &
            PID2=$!
            run_kilo &
            PID3=$!
            
            wait $PID1 $PID2 $PID3
            
            echo ""
            echo -e "${GREEN}All parallel runs complete. Aggregating results...${NC}"
            aggregate_results
            ;;
        aggregate)
            aggregate_results
            ;;
        *)
            echo "Usage: $0 {all|opencode|cline|kilo|qa|aggregate|status}"
            exit 1
            ;;
    esac
}

main "$@"
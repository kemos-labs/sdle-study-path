#!/usr/bin/env bash
# Full re-audit of placeholder hinges — RED LINE: no stop until all batches OK
set -euo pipefail
ROOT="/data/prometric/sdle-prep"
IN_DIR="$ROOT/data/generated/deepseek_in_placeholder"
OUT_DIR="$ROOT/data/generated/deepseek_out_placeholder"
LOG="$ROOT/data/generated/phase_truth/placeholder_wave.log"
MODEL="${DEEPSEEK_MODEL:-deepseek/deepseek-v4-pro}"
PARALLEL="${PARALLEL:-4}"
mkdir -p "$OUT_DIR"
export DEEPSEEK_MODEL="$MODEL"
export ROOT IN_DIR OUT_DIR

run_one() {
  local f="$1"
  local base
  base=$(basename "$f")
  local out="$OUT_DIR/$base"
  if [[ -f "$out" ]] && python3 -c "import json; d=json.load(open('$out')); assert isinstance(d,list) and len(d)>0" 2>/dev/null; then
    echo "skip $base"
    return 0
  fi
  # adapt run_deepseek_batch paths via env
  python3 - <<PY
import json, re, subprocess, sys
from pathlib import Path
IN = Path("$f")
OUT = Path("$out")
MODEL = "$MODEL"
data = json.loads(IN.read_text())
sys_msg = data.get("system", "")
items = data.get("items", [])
prompt = sys_msg + "\n\nTask: Audit every item (" + str(len(items)) + " MCQs). Return ONLY a JSON array.\n"
prompt += "Each object: id, answer_index (0-3), confidence (high|med|low), hinge (2-4 clinical sentences, min 80 chars, NO 'Community mark provisional'), flip (bool), department.\n\n"
prompt += json.dumps(items, ensure_ascii=False)
prompt += "\n\nWrite nothing except the JSON array."
raw_path = OUT.with_suffix(".raw")
err_path = OUT.with_suffix(".err")
cmd = [
  "command-code", "-p", "--yolo", "--skip-onboarding",
  "-m", MODEL, "--max-turns", "10",
  "You are a pure JSON clinical auditor for SDLE. " + prompt,
]
with open(raw_path, "w") as raw, open(err_path, "w") as err:
    r = subprocess.run(cmd, stdout=raw, stderr=err, text=True)
raw = raw_path.read_text(encoding="utf-8", errors="replace") if raw_path.exists() else ""
m = re.search(r"\[[\s\S]*\]", raw)
if not m:
    print("NO_JSON", IN.name, file=sys.stderr)
    sys.exit(2)
try:
    arr = json.loads(m.group(0))
except Exception as e:
    print("JSON_ERR", IN.name, e, file=sys.stderr)
    sys.exit(3)
# reject if hinges are still provisional
ok = 0
for x in arr:
    h = str(x.get("hinge") or "")
    if len(h) >= 60 and "Community mark provisional" not in h:
        ok += 1
if ok < max(1, len(arr) // 2):
    print("WEAK_HINGES", IN.name, ok, len(arr), file=sys.stderr)
    # still write for retry inspection
OUT.write_text(json.dumps(arr, ensure_ascii=False, indent=2), encoding="utf-8")
print("OK", IN.name, "n=", len(arr), "goodish=", ok)
PY
}

export -f run_one
cd "$ROOT"
mapfile -t FILES < <(ls -1 "$IN_DIR"/ph_*.json | sort)
echo "Total batches: ${#FILES[@]} model=$MODEL parallel=$PARALLEL" | tee -a "$LOG"
# run with parallel xargs
printf '%s\n' "${FILES[@]}" | xargs -P "$PARALLEL" -I{} bash -c 'run_one "$@"' _ {}
echo "WAVE_DONE $(date -Iseconds)" | tee -a "$LOG"
# count
python3 - <<'PY'
from pathlib import Path
import json
out=Path("data/generated/deepseek_out_placeholder")
ok=0
for p in out.glob("ph_*.json"):
  try:
    d=json.loads(p.read_text())
    if isinstance(d,list) and d: ok+=1
  except: pass
print("completed_batches", ok)
PY

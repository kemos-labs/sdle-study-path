#!/usr/bin/env bash
# Run one deepseek_in batch through command-code DeepSeek V4 Flash.
# Usage: run_deepseek_batch.sh dept_endo_0000.json
set -euo pipefail
IN_NAME="${1:?batch json name}"
ROOT="/data/prometric/sdle-prep"
IN="$ROOT/data/generated/deepseek_in/$IN_NAME"
OUT="$ROOT/data/generated/deepseek_out/$IN_NAME"
MODEL="${DEEPSEEK_MODEL:-deepseek/deepseek-v4-pro}"

if [[ ! -f "$IN" ]]; then
  echo "missing $IN" >&2
  exit 1
fi
mkdir -p "$(dirname "$OUT")"

# If already good output, skip
if [[ -f "$OUT" ]]; then
  if python3 -c "import json,sys; d=json.load(open(sys.argv[1])); assert isinstance(d,list) and len(d)>0" "$OUT" 2>/dev/null; then
    echo "skip existing $OUT"
    exit 0
  fi
fi

PROMPT=$(python3 - <<PY
import json
from pathlib import Path
p = Path("$IN")
data = json.loads(p.read_text())
sys_msg = data.get("system", "")
items = data.get("items", [])
print(sys_msg)
print()
print(f"Task: Audit every item below ({len(items)} MCQs). Return ONLY a JSON array (no markdown fences).")
print("Each object: id, answer_index (0-3), confidence (high|med|low), hinge (clinical why 1-3 sentences), flip (bool vs answer_index_in), department.")
print()
print(json.dumps(items, ensure_ascii=False))
print()
print(f"Write nothing except the JSON array. Input batch: {p.name}")
PY
)

echo "Running $IN_NAME on $MODEL ..."
# command-code non-interactive
command-code -p --yolo --skip-onboarding -m "$MODEL" --max-turns 8 \
  "You are a pure JSON clinical auditor. $PROMPT" \
  > "$OUT.raw" 2>"$OUT.err" || true

python3 - <<PY
import json, re, sys
from pathlib import Path
raw_path = Path("$OUT.raw")
out_path = Path("$OUT")
raw = raw_path.read_text(encoding="utf-8", errors="replace") if raw_path.exists() else ""
# extract JSON array
m = re.search(r"\[[\s\S]*\]", raw)
if not m:
    print("NO_JSON_ARRAY", file=sys.stderr)
    # keep raw for debug
    sys.exit(2)
try:
    data = json.loads(m.group(0))
except Exception as e:
    print("JSON_ERR", e, file=sys.stderr)
    sys.exit(3)
if not isinstance(data, list) or not data:
    print("EMPTY", file=sys.stderr)
    sys.exit(4)
out_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
print("OK", out_path, "n=", len(data))
PY

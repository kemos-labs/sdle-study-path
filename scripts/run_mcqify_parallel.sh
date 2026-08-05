#!/bin/bash
# Launch the MCQ-ify book-solving pass as parallel sub-agents.
# deepseek PAID = fast main engine (25/call). Free pi models = parallel helpers (5/call).
# Usage: bash scripts/run_mcqify_parallel.sh
set -u
cd /data/prometric
mkdir -p work/mcqify logs
N=8   # total workers (modulo space)

WORKERS=(
  "0|deepseek/deepseek-v4-flash|25"          # paid backbone (fast)
  "1|cline/deepseek/deepseek-v4-flash|5"     # cline free
  "2|cline/cline-free/glm-5.2|5"             # cline free
  "3|cline/poolside/laguna-s-2.1:free|5"     # cline free
  "4|cline/stepfun/step-3.7-flash|5"         # cline free (vision-capable)
  "5|kilo/kilo-auto/free|5"                  # kilo
  "6|opencode/deepseek-v4-flash-free|5"      # opencode
  "7|kilo/cohere/north-mini-code:free|5"     # kilo cohere
)
PIDS=""
for entry in "${WORKERS[@]}"; do
  WID="${entry%%|*}"
  REST="${entry#*|}"
  MODEL="${REST%%|*}"
  B="${REST##*|}"
  echo "[launch] worker $WID -> $MODEL (batch $B)"
  nohup python3 scripts/mcqify_parallel.py "$WID" "$MODEL" "$N" "$B" > "logs/mcqify_$WID.log" 2>&1 &
  PIDS="$PIDS $!"
done
echo "launched:$PIDS"

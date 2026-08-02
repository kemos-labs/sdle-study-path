#!/usr/bin/env bash
# Sequential DeepSeek audit of weak_*.json batches (book-snippet context).
set -euo pipefail
cd /data/prometric/sdle-prep
export DEEPSEEK_MODEL="${DEEPSEEK_MODEL:-deepseek/deepseek-v4-pro}"
LOG=data/generated/phase_truth/weak_wave.log
mkdir -p data/generated/deepseek_out data/generated/phase_truth
echo "START $(date -Iseconds)" | tee -a "$LOG"
for f in data/generated/deepseek_in/weak_*.json; do
  name=$(basename "$f")
  echo "=== $name $(date -Iseconds) ===" | tee -a "$LOG"
  bash scripts/run_deepseek_batch.sh "$name" 2>&1 | tee -a "$LOG" || echo "FAIL $name" | tee -a "$LOG"
done
echo "DONE $(date -Iseconds)" | tee -a "$LOG"
ls data/generated/deepseek_out/weak_*.json 2>/dev/null | wc -l | tee -a "$LOG"

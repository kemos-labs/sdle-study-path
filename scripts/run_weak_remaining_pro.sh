#!/usr/bin/env bash
set -euo pipefail
cd /data/prometric/sdle-prep
export DEEPSEEK_MODEL=deepseek/deepseek-v4-pro
LOG=data/generated/phase_truth/weak_wave_pro.log
echo "START PRO $(date -Iseconds) model=$DEEPSEEK_MODEL" | tee "$LOG"
for f in data/generated/deepseek_in/weak_*.json; do
  name=$(basename "$f")
  out="data/generated/deepseek_out/$name"
  if [[ -f "$out" ]] && python3 -c "import json,sys; d=json.load(open(sys.argv[1])); assert isinstance(d,list) and len(d)>0" "$out" 2>/dev/null; then
    echo "skip $name" | tee -a "$LOG"
    continue
  fi
  echo "=== $name $(date -Iseconds) PRO ===" | tee -a "$LOG"
  bash scripts/run_deepseek_batch.sh "$name" 2>&1 | tee -a "$LOG" || echo "FAIL $name" | tee -a "$LOG"
done
echo "DONE PRO $(date -Iseconds)" | tee -a "$LOG"
ls data/generated/deepseek_out/weak_*.json | wc -l | tee -a "$LOG"

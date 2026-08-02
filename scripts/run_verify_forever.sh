#!/usr/bin/env bash
# Retry-loop wrapper: keeps running verification until the topic list is done.
# Usage: bash scripts/run_verify_forever.sh [topics] [batch]
set -u
cd "$(dirname "$0")/.."
TOPICS="${1:-restorative,endo,perio}"
BATCH="${2:-25}"
MAX_HOURS="${3:-20}"

end=$(( $(date +%s) + MAX_HOURS*3600 ))
while [ "$(date +%s)" -lt "$end" ]; do
  python3 scripts/verify_bank_batch.py --topics "$TOPICS" --batch "$BATCH" --resume
  # stop if no progress: compare checkpoint size before/after
  cp sdle-prep/data/generated/bank_verification/verdicts.jsonl /tmp/bv_before.jsonl 2>/dev/null || true
  sleep 90
  if [ -f /tmp/bv_before.jsonl ] && ! diff -q /tmp/bv_before.jsonl sdle-prep/data/generated/bank_verification/verdicts.jsonl >/dev/null 2>&1; then
    echo "no progress for 90s — retrying"
  fi
done
echo "verification loop finished (time budget exhausted)"

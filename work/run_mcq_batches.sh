#!/bin/bash
# Sequential batches with resume; stop if rate-limited (all ERROR)
cd /data/prometric/sdle-prep
for b in 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18; do
  echo "=== batch $b $(date +%H:%M) ==="
  timeout 500 python3 scripts/verify_with_models.py --only answer-mcq --batch $b --size 25 --models 3 2>&1 | grep -E "BATCH|ERROR:|all models failed|saved|Summary|Saved"
  # Check pending left
  LEFT=$(python3 scripts/verify_with_models.py --only answer-mcq --list-pending 2>/dev/null | grep "^Pending" | awk '{print $2}')
  echo "pending left: $LEFT"
  if [ -n "$LEFT" ] && [ "$LEFT" -le 5 ]; then echo "DONE"; break; fi
  sleep 3
done
echo "ALL BATCHES FINISHED $(date +%H:%M)"

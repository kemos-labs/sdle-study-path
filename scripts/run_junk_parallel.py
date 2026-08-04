#!/usr/bin/env python3
"""run_junk_parallel.py — run the junk-option distractor fix on 8 models in parallel.

Workers:
  1. deepseek (direct API)       5. pi cline/stepfun-3.7-flash
  2. zai glm-4.5-flash (direct)   6. pi opencode/deepseek-v4-flash-free
  3. pi cline/deepseek-v4-flash   7. pi opencode/big-pickle
  4. pi cline/glm-5.2             8. pi opencode/mimo-v2.5-free

Each worker owns a shard (qid crc32 % 8) + its own checkpoint (distractors.S.jsonl).
Dead shards are auto-restarted (max 4 attempts). When all shards finish → merge
into the main checkpoint → ready for --apply.

Run detached:  nohup python3 -u scripts/run_junk_parallel.py > /tmp/junk_parallel.log 2>&1 &
"""
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path("/data/prometric")
OUT = ROOT / "sdle-prep" / "data" / "generated" / "junk_fix"
OUT.mkdir(parents=True, exist_ok=True)
MAIN_CKPT = OUT / "distractors.jsonl"
TARGET = 4150
SHARDS = 8

JOBS = [
    # provider, shard K, checkpoint file — deepseek proved fast+reliable; 8 parallel shards
    ("deepseek", 0, "distractors.s0.jsonl"),
    ("deepseek", 1, "distractors.s1.jsonl"),
    ("deepseek", 2, "distractors.s2.jsonl"),
    ("deepseek", 3, "distractors.s3.jsonl"),
    ("deepseek", 4, "distractors.s4.jsonl"),
    ("deepseek", 5, "distractors.s5.jsonl"),
    ("deepseek", 6, "distractors.s6.jsonl"),
    ("deepseek", 7, "distractors.s7.jsonl"),
]

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)

def shard_count(name):
    f = OUT / name
    if not f.exists():
        return 0
    try:
        return sum(1 for l in open(f, encoding="utf-8") if l.strip())
    except Exception:
        return 0

def total_count():
    return sum(shard_count(n) for _, _, n in JOBS) + (shard_count("distractors.jsonl") if False else 0)

def main():
    procs = {}
    attempts = {k: 0 for _, k, _ in JOBS}   # keyed by shard index
    log(f"parallel junk-fix: {SHARDS} shards · target {TARGET} distractors")
    log(f"models: " + ", ".join(j[0] for j in JOBS))

    while True:
        # reap finished
        for k in list(procs.keys()):
            p = procs[k]
            if p.poll() is not None:
                log(f"shard worker exited ({k}) rc={p.returncode}")
                del procs[k]

        total = total_count()
        if total >= TARGET:
            log(f"ALL SHARDS DONE ({total}/{TARGET}) — merging…")
            subprocess.run([sys.executable, str(ROOT / "scripts/fix_junk_options.py"), "--merge"],
                           cwd=str(ROOT))
            log("merge complete → run: python3 scripts/fix_junk_options.py --apply")
            return 0

        for provider, k, ckpt in JOBS:
            if k in procs:
                continue
            if attempts[k] >= 4:
                continue
            attempts[k] += 1
            cmd = [
                sys.executable, "-u", str(ROOT / "scripts/fix_junk_options.py"),
                "--resume", "--batch", "25",
                "--provider", provider,
                "--shard", f"{k}/{SHARDS}",
                "--checkpoint", str(OUT / ckpt),
            ]
            fh = open(str(OUT / f"worker.{k}.log"), "ab")
            p = subprocess.Popen(cmd, stdout=fh, stderr=subprocess.STDOUT, start_new_session=True)
            procs[k] = p
            log(f"started shard {k} on {provider} (attempt {attempts[k]})")

        if not procs:
            log("all workers exhausted attempts — stopping; resume by rerunning this script")
            return 1
        time.sleep(20)

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("launcher stopped — shard checkpoints are resumable")

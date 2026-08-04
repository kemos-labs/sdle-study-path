#!/usr/bin/env python3
"""watchdog_junk.py — keeps the junk-option distractor fix alive.

- If the worker (fix_junk_options.py) is not running and the job isn't done → start it.
- If the worker is running but the checkpoint has not grown for STALL_MIN minutes → kill + restart.
- Works detached (nohup/setsid) so closing the terminal does NOT stop it.
- Stops when >= TARGET distractors are checkpointed (job complete).
- Requires internet for API calls; offline = no progress, no loss (checkpointed, auto-resumes).
"""
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

CHECKPOINT = Path("/data/prometric/sdle-prep/data/generated/junk_fix/distractors.jsonl")
WORKER = ["python3", "-u", "/data/prometric/scripts/fix_junk_options.py", "--resume", "--batch", "25"]
LOG = open("/tmp/junk_fix.log", "ab")
TARGET = 4150          # total junk-option questions
STALL_MIN = 10         # restart if no checkpoint growth for this long
POLL = 20              # check every N seconds


def done_count() -> int:
    if not CHECKPOINT.exists():
        return 0
    n = 0
    try:
        for line in open(CHECKPOINT, encoding="utf-8"):
            if line.strip():
                n += 1
    except Exception:
        pass
    return n


def worker_running() -> bool:
    try:
        out = subprocess.run(
            ["pgrep", "-f", "fix_junk_options.py --resume"], capture_output=True, text=True
        ).stdout.strip()
        return bool(out)
    except Exception:
        return False


def start_worker():
    # setsid detaches fully from this process + terminal; stdout → junk log
    subprocess.Popen(
        WORKER,
        stdout=LOG,
        stderr=subprocess.STDOUT,
        start_new_session=True,
    )
    log("started worker")


def kill_worker():
    subprocess.run(["pkill", "-f", "fix_junk_options.py --resume"], capture_output=True)
    time.sleep(2)


def log(msg: str):
    line = f"[{time.strftime('%H:%M:%S')}] {msg}\n"
    sys.stdout.write(line)
    sys.stdout.flush()


def main():
    log(f"watchdog up — target {TARGET} distractors · stall threshold {STALL_MIN} min")
    last_count = done_count()
    last_change = time.time()
    restarts = 0

    while True:
        n = done_count()
        if n >= TARGET:
            log(f"COMPLETE: {n}/{TARGET} distractors. Run: python3 scripts/fix_junk_options.py --apply")
            return 0

        now = time.time()
        if n > last_count:
            last_change = now
        last_count = n

        if worker_running():
            stale = (now - last_change) > STALL_MIN * 60
            if stale:
                restarts += 1
                log(f"stall detected (no growth in {STALL_MIN} min, {n}/{TARGET}) — restarting ({restarts})")
                kill_worker()
                start_worker()
                last_change = time.time()
            else:
                log(f"worker ok · {n}/{TARGET}")
        else:
            restarts += 1
            log(f"worker not running ({n}/{TARGET}) — starting ({restarts})")
            start_worker()
            last_change = time.time()

        time.sleep(POLL)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("watchdog stopped by user (worker keeps its checkpoint — resumable)")

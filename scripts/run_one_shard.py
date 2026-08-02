#!/usr/bin/env python3
"""Run one of 10 shards: audit all micro-batches via command-code DeepSeek Pro."""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHARD = int(sys.argv[1]) if len(sys.argv) > 1 else 0
MODEL = os.environ.get("DEEPSEEK_MODEL", "deepseek/deepseek-v4-pro")
IN_DIR = ROOT / "data/generated/shards_10" / f"shard_{SHARD:02d}"
OUT_DIR = ROOT / "data/generated/deepseek_out_shard" / f"shard_{SHARD:02d}"
LOG = ROOT / "data/generated/phase_truth" / f"shard_{SHARD:02d}.log"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def run_batch(in_path: Path) -> str:
    out = OUT_DIR / in_path.name
    if out.exists():
        try:
            d = json.loads(out.read_text(encoding="utf-8"))
            if isinstance(d, list) and len(d) > 0:
                return f"skip {in_path.name}"
        except Exception:
            pass
    data = json.loads(in_path.read_text(encoding="utf-8"))
    items = data.get("items", [])
    sys_msg = data.get("system", "")
    prompt = (
        f"{sys_msg}\n\nTask: Audit every item ({len(items)} MCQs). Return ONLY a JSON array.\n"
        "Each object: id, answer_index (0-3), confidence (high|med|low), "
        "hinge (2-4 clinical sentences min 80 chars; NEVER Community mark provisional), "
        "flip (bool), department.\n\n"
        + json.dumps(items, ensure_ascii=False)
        + "\n\nWrite nothing except the JSON array."
    )
    cmd = [
        "command-code",
        "-p",
        "--yolo",
        "--skip-onboarding",
        "-m",
        MODEL,
        "--max-turns",
        "12",
        "You are a pure JSON clinical auditor for SDLE. " + prompt,
    ]
    raw_path = out.with_suffix(".raw")
    err_path = out.with_suffix(".err")
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=720)
        raw_path.write_text(r.stdout or "", encoding="utf-8")
        err_path.write_text(r.stderr or "", encoding="utf-8")
        raw = r.stdout or ""
    except subprocess.TimeoutExpired:
        return f"TIMEOUT {in_path.name}"
    m = re.search(r"\[[\s\S]*\]", raw)
    if not m:
        return f"NO_JSON {in_path.name} outlen={len(raw)}"
    try:
        arr = json.loads(m.group(0))
    except Exception as e:
        return f"JSON_ERR {in_path.name} {e}"
    if not isinstance(arr, list) or not arr:
        return f"EMPTY {in_path.name}"
    out.write_text(json.dumps(arr, ensure_ascii=False, indent=2), encoding="utf-8")
    good = sum(
        1
        for x in arr
        if isinstance(x, dict)
        and len(str(x.get("hinge") or "")) >= 60
        and "Community mark provisional" not in str(x.get("hinge") or "")
    )
    return f"OK {in_path.name} n={len(arr)} good={good}"


def main() -> int:
    if not IN_DIR.exists():
        print(f"missing {IN_DIR}", file=sys.stderr)
        return 2
    files = sorted(IN_DIR.glob("batch_*.json"))
    LOG.parent.mkdir(parents=True, exist_ok=True)
    start = time.time()
    with LOG.open("w", encoding="utf-8") as log:
        log.write(f"SHARD={SHARD} model={MODEL} batches={len(files)}\n")
        print(f"SHARD={SHARD} batches={len(files)} model={MODEL}", flush=True)
        ok = fail = 0
        for i, f in enumerate(files, 1):
            msg = run_batch(f)
            line = f"[{i}/{len(files)}] {msg}"
            print(line, flush=True)
            log.write(line + "\n")
            log.flush()
            if msg.startswith("OK") or msg.startswith("skip"):
                ok += 1
            else:
                fail += 1
                # one retry on NO_JSON
                if msg.startswith("NO_JSON") or msg.startswith("TIMEOUT"):
                    time.sleep(2)
                    msg2 = run_batch(f)
                    log.write(f"  retry {msg2}\n")
                    print(f"  retry {msg2}", flush=True)
                    if msg2.startswith("OK") or msg2.startswith("skip"):
                        ok += 1
                        fail -= 1
        elapsed = time.time() - start
        summary = {
            "shard": SHARD,
            "batches_total": len(files),
            "ok_or_skip": ok,
            "fail": fail,
            "elapsed_sec": round(elapsed, 1),
            "out_dir": str(OUT_DIR),
            "model": MODEL,
        }
        (OUT_DIR / "SHARD_DONE.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
        log.write(json.dumps(summary) + "\n")
        print("DONE", json.dumps(summary), flush=True)
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Run all placeholder re-audit batches via command-code. Model always explicit."""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IN_DIR = ROOT / "data/generated/deepseek_in_placeholder"
OUT_DIR = ROOT / "data/generated/deepseek_out_placeholder"
LOG = ROOT / "data/generated/phase_truth/placeholder_wave.log"
MODEL = os.environ.get("DEEPSEEK_MODEL", "deepseek/deepseek-v4-pro")
PARALLEL = int(os.environ.get("PARALLEL", "3"))
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
    if not MODEL or MODEL.startswith("-"):
        return f"BAD_MODEL {MODEL}"
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
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
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
    files = sorted(IN_DIR.glob("ph_*.json"))
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as log:
        hdr = f"START n={len(files)} model={MODEL} parallel={PARALLEL} t={time.time()}\n"
        log.write(hdr)
        print(hdr.strip(), flush=True)
        done = 0
        with ThreadPoolExecutor(max_workers=PARALLEL) as ex:
            futs = {ex.submit(run_batch, f): f for f in files}
            for fut in as_completed(futs):
                msg = fut.result()
                done += 1
                line = f"[{done}/{len(files)}] {msg}"
                print(line, flush=True)
                log.write(line + "\n")
                log.flush()
                if done % 10 == 0:
                    subprocess.run(
                        [sys.executable, str(ROOT / "scripts/apply_placeholder_wave.py")],
                        cwd=str(ROOT),
                    )
        subprocess.run(
            [sys.executable, str(ROOT / "scripts/apply_placeholder_wave.py")],
            cwd=str(ROOT),
        )
        log.write(f"WAVE_DONE t={time.time()}\n")
        print("WAVE_DONE", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

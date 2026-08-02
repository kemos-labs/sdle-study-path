#!/usr/bin/env python3
"""Retry failed Drive book downloads SLOWLY (1 worker) to avoid rate-limit.

Google error seen:
  Cannot retrieve the public link... or have had many accesses.

Strategy: 1 at a time, long sleep, multiple attempts, skip good PDFs.
"""
from __future__ import annotations

import json
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FAILS = ROOT / "data/generated/phase_truth/parallel_dl/FAILED_JOBS.json"
# also rebuild pending from tree minus good pdfs
LOG = ROOT / "data/generated/phase_truth/parallel_dl/retry_slow.jsonl"
SLEEP = 4.0
ATTEMPTS = 2


def good(path: Path) -> bool:
    if not path.exists() or path.stat().st_size < 50_000:
        return False
    try:
        return path.read_bytes()[:5] == b"%PDF-"
    except OSError:
        return False


def one(fid: str, dest: Path) -> str:
    if good(dest):
        return "skip"
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".retry.part")
    if tmp.exists():
        try:
            tmp.unlink()
        except OSError:
            pass
    # try both URL forms
    urls = [
        f"https://drive.google.com/uc?id={fid}",
        f"https://drive.google.com/uc?export=download&id={fid}",
    ]
    for url in urls:
        try:
            subprocess.run(
                ["gdown", url, "-O", str(tmp)],
                capture_output=True,
                text=True,
                timeout=1800,
            )
        except subprocess.TimeoutExpired:
            continue
        if tmp.exists() and tmp.stat().st_size > 0:
            head = tmp.read_bytes()[:10]
            if head.startswith(b"%PDF"):
                tmp.replace(dest)
                return "ok"
            try:
                tmp.unlink()
            except OSError:
                pass
    return "fail"


def main() -> None:
    jobs = json.loads(FAILS.read_text(encoding="utf-8"))
    # de-dupe by id
    seen = set()
    uniq = []
    for j in jobs:
        if j["id"] in seen:
            continue
        seen.add(j["id"])
        uniq.append(j)
    print(f"retry queue={len(uniq)} sleep={SLEEP}s", flush=True)
    stats = {"ok": 0, "skip": 0, "fail": 0}
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as logf:
        for i, j in enumerate(uniq, 1):
            dest = Path(j["dest"])
            status = "fail"
            for attempt in range(1, ATTEMPTS + 1):
                status = one(j["id"], dest)
                if status in ("ok", "skip"):
                    break
                time.sleep(SLEEP * attempt)
            stats[status] = stats.get(status, 0) + 1
            row = {
                "i": i,
                "n": len(uniq),
                "status": status,
                "id": j["id"],
                "name": j.get("name"),
                "dest": str(dest),
                "bytes": dest.stat().st_size if dest.exists() else 0,
            }
            logf.write(json.dumps(row, ensure_ascii=False) + "\n")
            logf.flush()
            print(
                f"[{i}/{len(uniq)}] {status} ok={stats['ok']} fail={stats['fail']} skip={stats['skip']} {(j.get('name') or '')[:55]}",
                flush=True,
            )
            time.sleep(SLEEP)
    print(json.dumps(stats, indent=2), flush=True)
    (LOG.parent / "RETRY_SUMMARY.json").write_text(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()

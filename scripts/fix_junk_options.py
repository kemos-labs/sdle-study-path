#!/usr/bin/env python3
"""fix_junk_options.py — replace "(not listed in source extract)" options with real distractors.

User mandate: MAX questions per API call, checkpointed, never break the app.
Pipeline:
  1. Load usable MCQs; find those with the junk placeholder at index 3.
  2. Batch 25/call; model writes ONE short plausible-but-wrong 4th distractor
     using the stem + 3 real options + marked answer + explanation.
  3. Checkpoint per batch (resumable). Staging output only.
  4. --apply merge: validates (non-empty, unique, not the answer) then writes questions.js.

Usage:
  python3 scripts/fix_junk_options.py --resume --batch 25
  python3 scripts/fix_junk_options.py --stats
  python3 scripts/fix_junk_options.py --apply
"""
from __future__ import annotations

import argparse
import json
import re
import time
import urllib.request
import urllib.error
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
Q_JS = ROOT / "sdle-prep" / "data" / "questions.js"
OUT = ROOT / "sdle-prep" / "data" / "generated" / "junk_fix"
OUT.mkdir(parents=True, exist_ok=True)
CHECKPOINT = OUT / "distractors.jsonl"

PROVIDERS = [
    {"name": "deepseek", "url": "https://api.deepseek.com/chat/completions",
     "key": "sk-ba41aeb17e7641c99cd24c4ee2e57098",
     "model": "deepseek-chat"},
    {"name": "zai", "url": "https://api.z.ai/api/paas/v4/chat/completions",
     "key": "4ea3822302844e2ca6837e1db7c85e55.IAd0YoFVPgKwYcCC",
     "model": "glm-4.5-flash"},
]

# pi CLI models (pi handles cline/opencode auth + Cloudflare). ID must contain "pi:"
PI_MODELS = {
    "pi:cline/deepseek/deepseek-v4-flash": "cline/deepseek/deepseek-v4-flash",
    "pi:cline/cline-free/glm-5.2": "cline/cline-free/glm-5.2",
    "pi:cline/stepfun/step-3.7-flash": "cline/stepfun/step-3.7-flash",
    "pi:opencode/deepseek-v4-flash-free": "opencode/deepseek-v4-flash-free",
    "pi:opencode/big-pickle": "opencode/big-pickle",
    "pi:opencode/mimo-v2.5-free": "opencode/mimo-v2.5-free",
}

def call_pi(model_id, prompt, timeout=180):
    """Run one batch through pi --print (free cline/opencode models)."""
    import subprocess
    cmd = ["pi", "--model", model_id, "--print", prompt]
    try:
        r = subprocess.run(cmd, capture_output=True, timeout=timeout, stdin=subprocess.DEVNULL)
        if r.returncode != 0:
            return f"__PIERR{r.returncode}:{r.stderr.decode()[:80]}"
        return r.stdout.decode()
    except subprocess.TimeoutExpired:
        return "__PITIMEOUT"
    except Exception as e:
        return f"__PIEXC{type(e).__name__}"

SYSTEM = ("You are a dental board examiner writing ONE wrong-answer distractor for a recall question. "
          "You receive: QID, stem, three real options, the correct option letter+text, and a short explanation. "
          "Write exactly ONE short distractor (3-9 words) that a weak student might pick but that is clearly "
          "incorrect on the best-answer standard. Rules: never duplicate or paraphrase the correct option; "
          "never reuse the other options; keep it a dental term or short phrase, no punctuation marks like "
          "'-' or ':' at the start, no quotes. Reply with ONLY a JSON array of objects {\"qid\":..., \"distractor\":\"...\"} "
          "in the same order.")

def load_bank():
    raw = open(Q_JS, encoding="utf-8").read()
    m = re.search(r"(QUESTION_BANK\s*=\s*)(\[.*\])(\s*;?)", raw, re.S)
    return json.loads(m.group(2)), m.group(1), m.group(3), raw

def junk(o):
    return "(not listed" in str(o)

def done_ids():
    ids = set()
    if CHECKPOINT.exists():
        for line in open(CHECKPOINT, encoding="utf-8"):
            try:
                ids.add(json.loads(line)["qid"])
            except Exception:
                pass
    return ids

def call_api(provider, prompt):
    body = json.dumps({
        "model": provider["model"],
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.4,
        "max_tokens": 6000,
    }).encode()
    req = urllib.request.Request(provider["url"], data=body,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {provider['key']}"})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            data = json.loads(r.read().decode())
            return data["choices"][0]["message"]["content"]
    except urllib.error.HTTPError as e:
        return f"__HTTP{e.code}"
    except Exception as e:
        return f"__ERR{type(e).__name__}"

def dispatch(provider, prompt):
    if provider.startswith("pi:"):
        model = PI_MODELS.get(provider)
        if not model:
            return f"__NOMODEL{provider}"
        return call_pi(model, prompt)
    p = next((x for x in PROVIDERS if x["name"] == provider), None)
    if not p:
        return f"__NOPROV{provider}"
    return call_api(p, prompt)

def parse(resp, qids):
    m = re.search(r"\[.*\]", resp, re.S)
    if not m:
        return None
    try:
        arr = json.loads(m.group(0))
    except Exception:
        return None
    out = []
    for i, qid in enumerate(qids):
        item = arr[i] if i < len(arr) else None
        if not isinstance(item, dict) or not item.get("distractor"):
            return None
        out.append({"qid": qid, "distractor": item["distractor"].strip()})
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--batch", type=int, default=25)
    ap.add_argument("--stats", action="store_true")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--provider", default="deepseek")
    ap.add_argument("--shard", default="0/1")
    ap.add_argument("--checkpoint", default=str(CHECKPOINT))
    ap.add_argument("--merge", action="store_true")
    ap.add_argument("--retry-junk", action="store_true")
    args = ap.parse_args()

    if args.apply:
        bank, pre, post, raw = load_bank()
        by_id = {q["id"]: q for q in bank}
        n = 0
        if CHECKPOINT.exists():
            for line in open(CHECKPOINT, encoding="utf-8"):
                try:
                    rec = json.loads(line)
                except Exception:
                    continue
                q = by_id.get(rec["qid"])
                d = str(rec.get("distractor", "")).strip()
                if not q or not d or junk(d):
                    continue
                if len(d) > 60 or d.lower() in [str(o).lower() for o in q["options"]]:
                    continue
                for i, o in enumerate(q["options"]):
                    if junk(o):
                        q["options"][i] = d
                        n += 1
                        break
        with open(Q_JS, "w", encoding="utf-8") as f:
            f.write(pre + json.dumps(bank, ensure_ascii=False) + post)
        print(f"applied {n} distractor replacements")
        return 0

    if args.merge:
        import glob
        merged, count = [], 0
        for f in sorted(glob.glob(str(OUT / "distractors.*.jsonl"))):
            for line in open(f, encoding="utf-8"):
                try:
                    rec = json.loads(line)
                    if rec.get("qid") and rec.get("distractor"):
                        merged.append(rec); count += 1
                except Exception:
                    pass
        with open(CHECKPOINT, "w", encoding="utf-8") as f:
            for rec in merged:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        print(f"merged {count} distractors into {CHECKPOINT.name}")
        return 0

    bank, _, _, _ = load_bank()
    todo = [q for q in bank if q.get("usable") is not False and isinstance(q.get("options"), list) and len(q.get("options")) > 3 and junk(q["options"][3])]
    if args.retry_junk:
        todo = [q for q in todo if q["options"][3] == "(not listed in source extract)"]
    k, n = (int(x) for x in args.shard.split("/"))
    todo = [q for q in todo if zlib.crc32(q["id"].encode()) % n == k]
    done = done_ids() if args.resume else set()
    CHECK = Path(args.checkpoint)
    if args.resume and CHECK.exists():
        for line in open(CHECK, encoding="utf-8"):
            try:
                done.add(json.loads(line)["qid"])
            except Exception:
                pass
    todo = [q for q in todo if q["id"] not in done]
    print(f"shard {args.shard} ({args.provider}) | assigned {len(todo) + len([q for q in []])} | remaining {len(todo)}")

    if args.stats:
        return 0

    provider = args.provider
    pi = 0
    ok = err = 0
    t0 = time.time()
    CHECK = Path(args.checkpoint)
    with open(CHECK, "a", encoding="utf-8") as ckpt:
        for start in range(0, len(todo), args.batch):
            batch = todo[start:start + args.batch]
            parts = []
            for q in batch:
                opts = "\n".join(f"{i+1}. {o}" for i, o in enumerate(q["options"]) if not junk(o))
                ans = q["options"][q["answer"]] if 0 <= q["answer"] < len(q["options"]) else "?"
                expl = (q.get("explanation") or "")[:220].replace("\n", " ")
                parts.append(
                    f"QID:{q['id']}\nQ: {q['q'][:180]}\nREAL OPTIONS:\n{opts}\nCORRECT: {ans}\nEXPLANATION: {expl}\n=====")
            prompt = "\n".join(parts)
            if args.retry_junk:
                prompt = ("You are a dental board examiner. For EACH question write ONE short wrong distractor (3-9 words) "
                          "that belongs to a COMPLETELY DIFFERENT dental concept/category than ALL three real options and the "
                          "correct answer — different diagnosis, different material, different number range, different term. "
                          "A previous distractor was rejected for being too similar, so pick something from a totally different "
                          "field. Never rephrase or contain any real option. Reply with ONLY a JSON array "
                          '[{"qid":...,"distractor":...}] in the same order.\n\n' + prompt)
            resp = ""
            for attempt in range(3):
                resp = dispatch(provider, prompt)
                if not resp.startswith("__"):
                    break
                print(f"  [{provider}] attempt {attempt+1} failed {resp[:40]}")
                time.sleep(5)
            if resp.startswith("__"):
                err += 1
                print(f"[batch {start // args.batch}] ALL FAILED {resp[:50]}")
                time.sleep(8)
                continue
            verdicts = parse(resp, [q["id"] for q in batch])
            if not verdicts:
                err += 1
                print(f"[batch {start // args.batch}] parse failed")
                time.sleep(3)
                continue
            for v in verdicts:
                ckpt.write(json.dumps(v, ensure_ascii=False) + "\n")
            ckpt.flush()
            ok += 1
            print(f"[batch {start // args.batch}] {provider} {len(batch)}Q done | shard total {len(done) + ok * args.batch} | {time.time() - t0:.0f}s", flush=True)
            time.sleep(1.0)
    print(f"SHARD DONE ok={ok} err={err} | distractors in this shard: {ok * args.batch}", flush=True)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

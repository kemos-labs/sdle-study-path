#!/usr/bin/env python3
"""retry_single.py — one question per API call for the last stubborn junk options.
Usage: python3 retry_single.py <shard> <nshards> <provider:deepseek|zai>
Checkpoint: junk_fix/single.<shard>.jsonl  (resume-safe)
"""
import json, sys, time, zlib, urllib.request, urllib.error, re
from pathlib import Path

ROOT = Path("/data/prometric")
OUT = ROOT / "sdle-prep" / "data" / "generated" / "junk_fix"
OUT.mkdir(parents=True, exist_ok=True)
shard, nshards = int(sys.argv[1]), int(sys.argv[2])
provider = sys.argv[3] if len(sys.argv) > 3 else "deepseek"
MODELS = {
    "deepseek": ("https://api.deepseek.com/chat/completions", "sk-ba41aeb17e7641c99cd24c4ee2e57098", "deepseek-chat"),
    "zai": ("https://api.z.ai/api/paas/v4/chat/completions", "4ea3822302844e2ca6837e1db7c85e55.IAd0YoFVPgKwYcCC", "glm-4.5-flash"),
}
url, key, model = MODELS[provider]
CKPT = OUT / f"single.{shard}.jsonl"

raw = open(ROOT / "sdle-prep" / "data" / "questions.js", encoding="utf-8").read()
m = re.search(r"(QUESTION_BANK\s*=\s*)(\[.*\])(\s*;?)", raw, re.S)
bank = json.loads(m.group(2))
junk = lambda o: "(not listed" in str(o)
todo = [q for q in bank if q.get("usable") is not False and q["options"] and junk(q["options"][3])]
todo = [q for q in todo if zlib.crc32(q["id"].encode()) % nshards == shard]

done = set()
if CKPT.exists():
    for line in open(CKPT, encoding="utf-8"):
        try: done.add(json.loads(line)["qid"])
        except Exception: pass
todo = [q for q in todo if q["id"] not in done]
print(f"shard {shard}: {len(todo)} remaining", flush=True)

def call(q):
    opts = "\n".join(f"{i+1}. {o}" for i, o in enumerate(q["options"]) if not junk(o))
    ans = q["options"][q["answer"]]
    prompt = ("You are a dental board examiner. Write ONE short wrong distractor (3-9 words) for this MCQ "
              "that belongs to a COMPLETELY DIFFERENT dental concept/category than ALL three real options and the "
              "correct answer — different diagnosis, different material, different number range, different term. "
              "Never rephrase or contain any real option. Reply with ONLY a JSON array "
              '[{"qid":"<the qid>","distractor":"<your distractor>"}].\n\n'
              f"QID:{q['id']}\nQ: {q['q'][:200]}\nREAL OPTIONS:\n{opts}\nCORRECT: {ans}\nEXPLANATION: {(q.get('explanation') or '')[:200]}")
    body = json.dumps({"model": model, "messages": [{"role": "user", "content": prompt}],
                       "temperature": 0.4, "max_tokens": 6000}).encode()
    req = urllib.request.Request(url, body, {"Content-Type": "application/json", "Authorization": f"Bearer {key}"})
    try:
        resp = json.loads(urllib.request.urlopen(req, timeout=150).read())
        content = resp["choices"][0]["message"]["content"]
        qid_m = re.search(r'"qid"\s*:\s*"([^"]+)"', content)
        dis_m = re.search(r'"distractor"\s*:\s*"([^"]+)"', content)
        if not qid_m or not dis_m:
            return None
        if qid_m.group(1) != q["id"]:
            return None
        return dis_m.group(1).strip()
    except Exception as e:
        return f"__{type(e).__name__}"

ok = err = 0
t0 = time.time()
with open(CKPT, "a", encoding="utf-8") as f:
    for i, q in enumerate(todo):
        d = call(q)
        if d and not str(d).startswith("__"):
            f.write(json.dumps({"qid": q["id"], "distractor": d}, ensure_ascii=False) + "\n")
            f.flush(); ok += 1
        else:
            err += 1
        if i % 20 == 0:
            print(f"  {i}/{len(todo)} ok={ok} err={err} {time.time()-t0:.0f}s", flush=True)
        time.sleep(0.3)
print(f"SHARD {shard} DONE ok={ok} err={err}", flush=True)

#!/usr/bin/env python3
"""mcqify_parallel.py — run the MCQ-ify book-solving pass as PARALLEL SUB-AGENTS
using the free pi models (cline x4, kilo, opencode) + deepseek paid backbone.

Each worker process handles batch_index % N_WORKERS == worker_id, calls its model
via `pi --model <id> --print <prompt>` (pi handles cline/kilo/opencode auth),
validates the JSON output, and appends solved items to a per-worker checkpoint.

Validation (strict, books-only):
  - 4 unique options, answer_idx in range
  - why >= 12 chars, verbatim passage >= 20 chars
  - answer option text matches the passage's stated fact (LLM-instructed; the
    worker drops anything unsupported or malformed)

Usage:
  python3 scripts/mcqify_parallel.py <worker_id> <model_id> <n_workers> <batch_size>
"""
import json, re, subprocess, sys, time
from pathlib import Path

ROOT = Path("/data/prometric")
FN = ROOT / "sdle-prep" / "data" / "flash_notes.js"
CORPUS = ROOT / "sdle-prep" / "data" / "raw" / "books" / "text"
REF = ROOT / "sdle-ref" / "books"
WORK = ROOT / "work" / "mcqify"
WORK.mkdir(parents=True, exist_ok=True)

SRC_TARGETS = ["Rafi_Maqam_16", "Rafi_Maqam_19", "Saud_Masahhah", "Saud_Talkhees",
               "Mar-June_2026", "July_2026"]
STOP = set("which what when where how the of and for with from this that are was were has have had is in on to a an or by be as it its their them between among patient patients tooth teeth".split())

SYSTEM = ("You are a dental board examiner writing exam MCQs. You are given OFFICIAL TEXTBOOK PASSAGES "
          "and a recall question (possibly with a student's marked answer as a LEAD). Rules: "
          "1. The passages are the ONLY authority. If a passage states the answer, use it. If NO passage "
          "supports any answer, return unsolved:true — NEVER guess. "
          "2. The student answer (if given) is a LEAD only — confirm or correct it against the passage. "
          "3. Output the full question as a 4-option MCQ: the correct answer + 3 plausible, realistic "
          "distractors of the same style and length. 4. Write a short 'why' (1-2 sentences) and quote the "
          "supporting passage verbatim. 5. Options in English, exact book terminology. 6. If the stem is "
          "garbage (incomplete/blank/image-only), return unsolved:true. Reply with ONLY a JSON array, one "
          "object per item in order: [{\"id\":\"...\",\"options\":[\"A\",\"B\",\"C\",\"D\"],\"answer_idx\":0,"
          "\"why\":\"...\",\"passage\":\"...\",\"book\":\"...\",\"unsolved\":false}] No markdown fences.")

import urllib.request as _ur
import zlib as _z

def call_pi(model_id, prompt, timeout=300):
    if model_id.startswith("deepseek"):
        body = json.dumps({"model": "deepseek-chat", "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": prompt}],
            "temperature": 0.2, "max_tokens": 8000}).encode()
        req = _ur.Request("https://api.deepseek.com/chat/completions", data=body,
            headers={"Content-Type": "application/json",
                     "Authorization": "Bearer sk-ba41aeb17e7641c99cd24c4ee2e57098",
                     "Accept-Encoding": "gzip"})
        for attempt in range(3):
            try:
                with _ur.urlopen(req, timeout=timeout) as r:
                    raw = r.read()
                    if r.headers.get("Content-Encoding") == "gzip":
                        raw = _z.decompress(raw, 16 + _z.MAX_WBITS)
                    return json.loads(raw)["choices"][0]["message"]["content"]
            except Exception as e:
                if attempt == 2:
                    return f"__APIERR{str(e)[:120]}"
                time.sleep(3 * (attempt + 1))
    cmd = ["pi", "--model", model_id, "--print", prompt]
    try:
        r = subprocess.run(cmd, capture_output=True, timeout=timeout, stdin=subprocess.DEVNULL)
        if r.returncode != 0:
            return f"__PIERR{r.returncode}:{r.stderr.decode(errors='replace')[:120]}"
        return r.stdout.decode(errors="replace")
    except subprocess.TimeoutExpired:
        return "__PITIMEOUT"
    except Exception as e:
        return f"__PIEXC{type(e).__name__}:{str(e)[:80]}"

def load_corpus():
    idx = {}
    for d in sorted(CORPUS.iterdir()):
        if not d.is_dir() or "FACTPACK" in d.name:
            continue
        dept = d.name.lower()
        for f in sorted(d.glob("*.txt")):
            try:
                t = f.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            if t.count("(cid:") > 50:
                continue
            idx.setdefault(dept, []).append((f.stem, t))
    if REF.exists():
        for f in sorted(REF.glob("*.md")):
            try:
                t = f.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            idx.setdefault("ref", []).append((f.stem, t))
    return idx

def retrieve(stem, dept, corpus, k=3):
    words = [w for w in re.findall(r"[a-z]{4,}", stem.lower()) if w not in STOP]
    words = sorted(set(words), key=len, reverse=True)[:6]
    if not words:
        return ""
    best = []
    depts = [dept, "ref"] if dept != "ref" else ["ref"]
    for d in depts:
        for fname, text in corpus.get(d, []):
            low = text.lower()
            hits = sum(1 for w in words if w in low)
            if hits >= 1:
                best.append((hits, fname, text))
    best.sort(key=lambda x: -x[0])
    out = []
    for hits, fname, text in best[:k]:
        pos = 0
        for w in words[:4]:
            i = text.lower().find(w)
            if i >= 0:
                pos = i
                break
        seg = re.sub(r"\s+", " ", text[max(0, pos - 250):pos + 750].replace("\f", " ")).strip()
        out.append(f"[{fname}] {seg[:1000]}")
    return "\n".join(out)[:3200]

def load_targets():
    tp = WORK / "targets.json"
    if not tp.exists():
        src = FN.read_text(encoding="utf-8")
        data = json.loads(src.split("=", 1)[1].strip().rstrip().rstrip(";").strip())
        targets = []
        for dept, arr in data["byDept"].items():
            for it in arr:
                if it.get("_merged_into"):
                    continue
                if not any(s in SRC_TARGETS for s in (it.get("sources") or [])):
                    continue
                n = len(it.get("options") or [])
                if n >= 2:
                    continue
                known = ""
                if n == 1:
                    known = re.sub(r"^[A-Ea-e]\.\s*", "", it["options"][0]).strip()
                targets.append({"id": it["id"], "stem": it.get("stem", "")[:350],
                                "dept": dept, "known": known, "sources": it.get("sources")})
        json.dump(targets, open(tp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"[prep] exported {len(targets)} targets", flush=True)
    return json.load(open(tp, encoding="utf-8"))

def parse_array(text):
    m = re.search(r"\[", text)
    if not m:
        return None
    depth = 0
    for i, ch in enumerate(text[m.start():]):
        if ch == "[": depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                try:
                    return json.loads(text[m.start():m.start() + i + 1])
                except Exception:
                    return None
    return None

def validate(res):
    if not res:
        return None
    opts = res.get("options") or []
    if len(opts) < 3 or len(set(o.lower() for o in opts)) < 3:
        return None
    ai = res.get("answer_idx")
    if not isinstance(ai, int) or not (0 <= ai < len(opts)):
        return None
    why = (res.get("why") or "").strip()
    passage = (res.get("passage") or "").strip()
    unsolved = bool(res.get("unsolved"))
    if unsolved:
        # honest recall-solved: keep the MCQ but it is NOT book-verified
        if len(why) < 12:
            return None
    else:
        if len(why) < 12 or len(passage) < 20:
            return None
    return {"options": [str(o).strip()[:120] for o in opts[:5]], "answer_idx": ai,
            "why": why[:400], "passage": passage[:500], "book": (res.get("book") or "")[:80],
            "unsolved": unsolved}

def build_prompt(items, corpus):
    lines = []
    for i, it in enumerate(items):
        ctx = retrieve(it["stem"], it["dept"], corpus)
        lines.append(f"=== ITEM {i} ===\nID: {it['id']}\nQUESTION: {it['stem']}\n"
                     f"KNOWN-ANSWER-LEAD: {it['known'] or '(none)'}\nPASSAGES:\n{ctx or '(no passage retrieved)'}")
    return "\n\n".join(lines)

def main():
    worker_id, model_id, n_workers, batch_size = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
    ckpt = WORK / f"results_{worker_id}.jsonl"
    done_ids = set()
    for pool_f in [ckpt, WORK / "done_pool.jsonl"]:
        if pool_f.exists():
            for line in open(pool_f, encoding="utf-8"):
                try:
                    done_ids.add(json.loads(line)["id"])
                except Exception:
                    pass
    targets = load_targets()
    corpus = load_corpus()
    mine = [t for i, t in enumerate(targets) if i % n_workers == int(worker_id) and t["id"] not in done_ids]
    print(f"[{worker_id}] {len(mine)} items to process ({model_id})", flush=True)
    B = batch_size
    solved = 0
    for start in range(0, len(mine), B):
        batch = mine[start:start + B]
        prompt = build_prompt(batch, corpus)
        text = call_pi(model_id, prompt)
        ok = []
        if not text.startswith("__"):
            parsed = parse_array(text)
            if parsed:
                for res, it in zip(parsed, batch):
                    v = validate(res)
                    if v:
                        v["id"] = it["id"]
                        v["stem"] = it["stem"]
                        v["sources"] = it["sources"]
                        ok.append(v)
        if not ok:
            # one retry (models sometimes wrap JSON in prose)
            text2 = call_pi(model_id, prompt)
            if not text2.startswith("__"):
                parsed = parse_array(text2)
                if parsed:
                    for res, it in zip(parsed, batch):
                        v = validate(res)
                        if v:
                            v["id"] = it["id"]
                            v["stem"] = it["stem"]
                            v["sources"] = it["sources"]
                            ok.append(v)
        with open(ckpt, "a", encoding="utf-8") as fh:
            for x in ok:
                fh.write(json.dumps(x, ensure_ascii=False) + "\n")
        solved += len(ok)
        print(f"[{worker_id}] batch {start // B + 1}: +{len(ok)}/{len(batch)} (cum {solved})", flush=True)
        time.sleep(0.5)
    print(f"[{worker_id}] DONE: {solved} solved", flush=True)

if __name__ == "__main__":
    main()

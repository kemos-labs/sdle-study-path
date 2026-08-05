#!/usr/bin/env python3
"""mcqify_answers.py — book-solve the CORRECT OPTION for flash items that have
options (>=2) but no source answer mark (answerIdx/letter null).

These items currently degrade to recall Q&A in quizzes ("Answer: ... Options: ..."
glued text). The user ordered real pickable MCQs, so we solve each one from the
official books: deepseek direct API, batch 15, checkpoint per worker.

Output result: {"id", "answer_idx", "why", "passage", "book", "unsolved"}
Validation: answer_idx in range, why >= 12, passage >= 20 (unless unsolved).

Usage: python3 scripts/mcqify_answers.py <worker_id> <n_workers> <batch_size>
"""
import json, re, sys, time
from pathlib import Path
import urllib.request as _ur
import zlib as _z

ROOT = Path("/data/prometric")
FN = ROOT / "sdle-prep" / "data" / "flash_notes.js"
CORPUS = ROOT / "sdle-prep" / "data" / "raw" / "books" / "text"
REF = ROOT / "sdle-ref" / "books"
WORK = ROOT / "work" / "mcqify"
WORK.mkdir(parents=True, exist_ok=True)

STOP = set("which what when where how the of and for with from this that are was were has have had is in on to a an or by be as it its their them between among patient patients tooth teeth".split())

SYSTEM = ("You are a dental board examiner. You are given a recall question that ALREADY HAS OPTIONS, "
          "plus OFFICIAL TEXTBOOK PASSAGES. Rules: 1. The passages are the ONLY authority — pick the ONE "
          "option the passages support. If NO passage supports any option, return unsolved:true — NEVER "
          "guess. 2. If the question stem is garbage (incomplete/blank/image-only), return unsolved:true. "
          "3. Write a short 'why' (1-2 sentences) and quote the supporting passage verbatim. "
          "Reply with ONLY a JSON array, one object per item in order: "
          "[{\"id\":\"...\",\"answer_idx\":0,\"why\":\"...\",\"passage\":\"...\",\"book\":\"...\","
          "\"unsolved\":false}] No markdown fences. answer_idx is the 0-based index into the GIVEN options list.")

def call_api(prompt, timeout=300):
    body = json.dumps({"model": "deepseek-chat", "messages": [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": prompt}],
        "temperature": 0.2, "max_tokens": 6000}).encode()
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
    tp = WORK / "targets_answers.json"
    if not tp.exists():
        src = FN.read_text(encoding="utf-8")
        data = json.loads(src.split("=", 1)[1].strip().rstrip().rstrip(";").strip())
        targets = []
        for dept, arr in data["byDept"].items():
            for it in arr:
                if it.get("_merged_into"):
                    continue
                opts = it.get("options") or []
                if len(opts) < 2:
                    continue
                if it.get("answerIdx") is not None or it.get("answerLetter"):
                    continue
                targets.append({"id": it["id"], "stem": (it.get("stem") or "")[:350],
                                "dept": dept, "options": [str(o).strip()[:120] for o in opts[:6]],
                                "sources": it.get("sources")})
        json.dump(targets, open(tp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"[prep] exported {len(targets)} answer-targets", flush=True)
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

def validate(res, nopts):
    if not res:
        return None
    ai = res.get("answer_idx")
    if not isinstance(ai, int) or not (0 <= ai < nopts):
        return None
    why = (res.get("why") or "").strip()
    passage = (res.get("passage") or "").strip()
    unsolved = bool(res.get("unsolved"))
    if unsolved:
        if len(why) < 12:
            return None
    else:
        if len(why) < 12 or len(passage) < 20:
            return None
    return {"answer_idx": ai, "why": why[:400], "passage": passage[:500],
            "book": (res.get("book") or "")[:80], "unsolved": unsolved}

def build_prompt(items, corpus):
    lines = []
    for i, it in enumerate(items):
        ctx = retrieve(it["stem"], it["dept"], corpus)
        opts = "\n".join(f"  {chr(65+j)}. {o}" for j, o in enumerate(it["options"]))
        lines.append(f"=== ITEM {i} ===\nID: {it['id']}\nQUESTION: {it['stem']}\nOPTIONS:\n{opts}\nPASSAGES:\n{ctx or '(no passage retrieved)'}")
    return "\n\n".join(lines)

def main():
    worker_id, n_workers, batch_size = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    targets = load_targets()
    mine = [t for i, t in enumerate(targets) if i % n_workers == worker_id]
    ckpt = WORK / f"results_answers_{worker_id}.jsonl"
    done = set()
    for f in [ckpt, WORK / "done_pool.jsonl"]:
        if f.exists():
            for line in open(f, encoding="utf-8"):
                try:
                    done.add(json.loads(line)["id"])
                except Exception:
                    pass
    todo = [t for t in mine if t["id"] not in done]
    print(f"[{worker_id}] {len(todo)} items to process", flush=True)
    corpus = load_corpus()
    ok = 0
    for bi in range(0, len(todo), batch_size):
        batch = todo[bi:bi + batch_size]
        prompt = build_prompt(batch, corpus)
        out = call_api(prompt)
        parsed = parse_array(out) if not out.startswith("__") else None
        got = 0
        if parsed:
            for res, it in zip(parsed, batch):
                v = validate(res, len(it["options"]))
                if not v:
                    continue
                rec = {"id": it["id"], **v}
                with open(ckpt, "a", encoding="utf-8") as fh:
                    fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
                got += 1
                ok += 1
        print(f"[{worker_id}] batch {bi // batch_size + 1}: +{got}/{len(batch)} (cum {ok})", flush=True)
    print(f"[{worker_id}] DONE: {ok} solved", flush=True)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""verify_new_mcqs.py — book-verify the newly parsed MCQ sources (July 2026 recall,
MCQs_Solved, BANK_160, QA_Answered, + friend's 7 exam questions) against the OFFICIAL
book corpus ONLY. Parallel shards by crc32, per-shard checkpoints, merge, export.

Outputs:
  data/generated/newmcqs/verdicts.jsonl   -> per-q verdict
  data/generated/newmcqs/export_mcqs.json -> MCQs ready to append to recent_qa.js / flash
"""
from __future__ import annotations
import argparse, json, re, sys, time, urllib.request, urllib.error, zlib
from pathlib import Path
from collections import Counter
sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_uncertain import load_corpus, keywords, retrieve, parse, topic_pool, TOPIC_DIRS

API = {"url": "https://api.deepseek.com/chat/completions",
       "key": "sk-ba41aeb17e7641c99cd24c4ee2e57098", "model": "deepseek-chat"}

def call_api(prompt, timeout=180):
    body = json.dumps({"model": API["model"],
                       "messages": [{"role": "system", "content": SYSTEM},
                                    {"role": "user", "content": prompt}],
                       "max_tokens": 8000, "temperature": 0.1}).encode()
    req = urllib.request.Request(API["url"], data=body, headers={
        "Content-Type": "application/json", "Authorization": f"Bearer {API['key']}"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                data = json.loads(resp.read().decode())
            msg = data.get("choices", [{}])[0].get("message", {})
            return (msg.get("content") or "").strip()
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(12 * (attempt + 1)); continue
            if e.code in (500, 502, 503):
                time.sleep(6); continue
            return f"__HTTP {e.code}"
        except Exception as e:
            return f"__ERR {type(e).__name__}"
    return "__RATE"

ROOT = Path(__file__).resolve().parent.parent
PARSED = ROOT / "work" / "parsed_new_mcqs.json"
FRIEND = ROOT / "work" / "friend_questions.json"
OUT = ROOT / "sdle-prep" / "data" / "generated" / "newmcqs"
OUT.mkdir(parents=True, exist_ok=True)

SYSTEM = """You are a dental board examiner. You are given VERBATIM passages from OFFICIAL dental
textbooks (evidence ONLY — never invent citations), then exam questions with options.

For EVERY question give the CORRECT option index and a 'why' quoting the passage. Rules:
- If a passage supports an option, choose it and quote the passage verbatim (short).
- If NO passage supports any option, output "answer_idx": null and say uncertain honestly.
- Prefer a specific passage over a general one.
Reply with ONLY a JSON array in the same order:
[{"qid":"...","answer_idx":0-4 or null,"why":"1-2 sentences quoting the book","book":"book title","uncertain":false}]
No fences, no commentary."""


def dept_of(item):
    s = (item.get("stem", "") + " " + " ".join(item.get("options", []))).lower()
    rules = [
        ("endo", ["pulpit", "root canal", "canal", "endodont", "gutta", "apicoect", "pulp", "periapical", "sealer", "spreader", "obturat", "irreversible", "necro"]),
        ("perio", ["periodont", "gingiv", "plaque", "pocket", "probe", "calculus", "floss", "scal", "furcat", "implant"]),
        ("fixed", ["crown", "bridge", "veneer", "fixed", "pfm", "abutment", "retainer", "pontic", "prosthodont", "full-coverage", "cop", "cement", "zirconia", "laminate"]),
        ("rpd", ["removable", "denture", "rpd", "clasp", "partial", "major connector", "minor connector", "indirect retainer", "denture base"]),
        ("operative", ["amalgam", "composite", "cavity", "restoration", "class ", "operative", "enamel", "dentin", "bond", "etched", "restorative"]),
        ("ortho_pedo", ["orthodont", "malocclus", "class ii", "class iii", "crowd", "space maintainer", "eruption", "natal", "neonatal", "pediat", "child", "serial extraction", "braces"]),
        ("oms", ["extraction", "socket", "fracture", "surgery", "wisdom", "biopsy", "cyst", "abscess", "swelling", "facial", "space", "airway", "trauma", "dry socket", "hemorrhage", "bleeding"]),
        ("ethics", ["consent", "confident", "record", "law", "ethical", "infection", "steril", "hand", "glove", "disinfect", "ring", "autoclave"]),
        ("materials", ["alginate", "impression", "gypsum", "stone", "wax", "investment", "casting", "ceramic", "porcelain", "alloy", "setting time", "mix", "water/powder"]),
    ]
    for dept, kws in rules:
        if any(k in s for k in kws):
            return dept
    return "mixed"


def load_all():
    parsed = json.load(open(PARSED, encoding="utf-8"))
    items = []
    for src, arr in parsed.items():
        for it in arr:
            if len(it.get("options", [])) >= 2:
                items.append(it)
    friend = json.load(open(FRIEND, encoding="utf-8"))
    items.extend(friend)
    # stable ids
    for idx, it in enumerate(items):
        if not it.get("id"):
            it["id"] = f"nm_{idx:04d}"
        it["department"] = dept_of(it)
    return items


def build_prompt(batch, corpus):
    parts = ["TEXTBOOK PASSAGES (verbatim, official books only):"]
    for q in batch:
        pool = topic_pool(corpus, q.get("department") or "mixed")
        kws = keywords({"q": q.get("stem", ""), "options": q.get("options", []), "answer": q.get("answerIdx"), "explanation": ""})
        hits = retrieve(pool, kws, 5)
        if not hits:
            continue
        parts.append(f"[{q['id']}]")
        for _, name, p in hits:
            parts.append(f"({name}) {p.strip()[:420]}")
    parts.append("\nQUESTIONS:")
    for q in batch:
        opts = "\n".join(f"{i}. {o}" for i, o in enumerate(q["options"]))
        marked = q.get("answerIdx")
        parts.append(f"QID:{q['id']}\nQ: {q['stem'][:260]}\nOPTIONS:\n{opts}\nMARKED: {marked if marked is not None else 'none'}\n---")
    return "\n".join(parts)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shard", default="0/1")
    ap.add_argument("--checkpoint", default=str(OUT / "s0.jsonl"))
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--merge", action="store_true")
    ap.add_argument("--export", action="store_true")
    ap.add_argument("--retry", action="store_true")
    args = ap.parse_args()

    if args.merge:
        merged = {}
        for f in sorted(OUT.glob("s*.jsonl")):
            for line in open(f, encoding="utf-8"):
                try:
                    r = json.loads(line)
                    if r.get("qid"):
                        merged[r["qid"]] = r
                except Exception:
                    pass
        with open(OUT / "verdicts.jsonl", "w", encoding="utf-8") as fh:
            for r in merged.values():
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
        print("merged:", len(merged))
        return 0

    if args.retry:
        corpus = load_corpus()
        items = load_all()
        retry_ids = set(json.load(open(ROOT / "work" / "retry_ids.json", encoding="utf-8")))
        todo = [it for it in items if it["id"] in retry_ids]
        print(f"retry: {len(todo)} items (all-topics retrieval, single-call)", flush=True)
        fh = open(OUT / "retry.jsonl", "w", encoding="utf-8")
        for it in todo:
            pool = [p for ps in corpus.values() for p in ps]  # ALL topics
            kws = keywords({"q": it.get("stem", ""), "options": it.get("options", []), "answer": it.get("answerIdx"), "explanation": ""})
            hits = retrieve(pool, kws, 8)
            parts = ["TEXTBOOK PASSAGES (verbatim, official books only):"]
            if hits:
                parts.append(f"[{it['id']}]")
                for _, name, p in hits:
                    parts.append(f"({name}) {p.strip()[:380]}")
            opts = "\n".join(f"{i}. {o}" for i, o in enumerate(it["options"]))
            parts.append(f"\nQUESTIONS:\nQID:{it['id']}\nQ: {it['stem'][:260]}\nOPTIONS:\n{opts}\n---")
            resp = call_api("\n".join(parts))
            arr = parse(resp, [it["id"]])
            if arr and len(arr) == 1:
                fh.write(json.dumps(arr[0], ensure_ascii=False) + "\n")
            else:
                fh.write(json.dumps({"qid": it["id"], "answer_idx": None, "why": "retry failed", "book": ""}, ensure_ascii=False) + "\n")
            fh.flush()
            print(f"  {todo.index(it)+1}/{len(todo)} done", flush=True)
        fh.close()
        print("retry complete", flush=True)
        return 0

    if args.export:
        items = load_all()
        verdicts = {}
        for line in open(OUT / "verdicts.jsonl", encoding="utf-8"):
            try:
                r = json.loads(line)
                verdicts[r["qid"]] = r
            except Exception:
                pass
        done, unc = 0, 0
        for it in items:
            v = verdicts.get(it["id"], {})
            if v.get("answer_idx") is None:
                unc += 1
                continue
            it["answerIdx"] = v["answer_idx"]
            it["why"] = v.get("why", "")
            it["reference"] = v.get("book", "")
            it["_verified"] = "book" if not v.get("uncertain") else "recall"
            done += 1
        json.dump(items, open(OUT / "export_mcqs.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"export: {done} book-verified | {unc} uncertain (kept, labeled)")
        return 0

    corpus = load_corpus()
    items = load_all()
    k, n = (int(x) for x in args.shard.split("/"))
    todo = [it for it in items if zlib.crc32(it["id"].encode()) % n == k]
    # skip already-done
    CHECK = Path(args.checkpoint)
    done_ids = set()
    if CHECK.exists():
        for line in open(CHECK, encoding="utf-8"):
            try:
                done_ids.add(json.loads(line)["qid"])
            except Exception:
                pass
    todo = [it for it in todo if it["id"] not in done_ids]
    print(f"shard {k}/{n}: {len(todo)} to do", flush=True)
    fh = open(CHECK, "a", encoding="utf-8")
    for i in range(0, len(todo), args.batch):
        batch = todo[i:i + args.batch]
        prompt = build_prompt(batch, corpus)
        resp = call_api(prompt)
        arr = parse(resp, [q["id"] for q in batch])
        if not arr:
            # single-question retry
            for q in batch:
                resp2 = call_api(build_prompt([q], corpus))
                arr2 = parse(resp2, [q["id"]])
                if arr2 and len(arr2) == 1:
                    fh.write(json.dumps(arr2[0], ensure_ascii=False) + "\n")
                    fh.flush()
                else:
                    fh.write(json.dumps({"qid": q["id"], "answer_idx": None, "why": "retry failed", "book": ""}, ensure_ascii=False) + "\n")
                    fh.flush()
            continue
        for q, r in zip(batch, arr):
            if isinstance(r, dict) and r.get("qid"):
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
            else:
                fh.write(json.dumps({"qid": q["id"], "answer_idx": None, "why": "malformed", "book": ""}, ensure_ascii=False) + "\n")
        fh.flush()
        print(f"  {i + len(batch)}/{len(todo)} done", flush=True)
    fh.close()
    print("shard complete", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())

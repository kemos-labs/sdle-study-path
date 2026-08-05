#!/usr/bin/env python3
"""Locate book passages in the official corpus and compute PAGE NUMBERS (fast).
Corpus .txt files preserve page breaks as \\f — page = count of \\f before match + 1.
Uses a cached pickle of normalized texts + per-file word sets for candidate filtering.
"""
import json, re, pickle, sys
from pathlib import Path

ROOT = Path("/data/prometric")
CORPUS = ROOT / "sdle-prep" / "data" / "raw" / "books" / "text"
REF = ROOT / "sdle-ref" / "books"
CACHE = ROOT / "work" / "corpus_idx.pkl"

def norm(s):
    return re.sub(r"\s+", " ", s.lower()).strip()

def build_index():
    files = []
    for d in sorted(CORPUS.iterdir()):
        if not d.is_dir() or "FACTPACK" in d.name:
            continue
        for f in sorted(d.glob("*.txt")):
            try:
                t = f.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            if t.count("(cid:") > 50:
                continue
            files.append((d.name, f.stem, t))
    if REF.exists():
        for f in sorted(REF.glob("*.md")):
            try:
                t = f.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            files.append(("ref-md", f.stem, t))
    idx = []
    for book, stem, raw in files:
        low = raw.lower()
        words = set(re.findall(r"[a-z]{5,}", low))
        idx.append((book, stem, raw, low, words))
    with open(CACHE, "wb") as fh:
        pickle.dump(idx, fh)
    return idx

def load():
    try:
        return pickle.load(open(CACHE, "rb"))
    except Exception:
        return build_index()

IDX = None

def locate(phrase):
    global IDX
    if IDX is None:
        IDX = load()
    p = norm(phrase)
    if len(p) < 18:
        return None
    words = re.findall(r"[a-z]{5,}", p)
    cand = None
    for w in sorted(set(words), key=len, reverse=True)[:3]:
        ws = [i for i, (_, _, _, _, fw) in enumerate(IDX) if w in fw]
        cand = set(ws) if cand is None else (cand & set(ws))
        if not cand:
            break
    if cand is None:
        cand = range(len(IDX))
    for L in (60, 40, 30, 24, 18):
        if len(p) < L:
            continue
        sub = p[:L]
        for i in cand:
            book, stem, raw, low, _ = IDX[i]
            j = low.find(sub[:30])
            if j < 0:
                continue
            page = raw.count("\f", 0, j) + 1
            ctx = re.sub(r"\s+", " ", raw[max(0, j - 250):j + 550].replace("\f", " ")).strip()
            return (book, stem, page, ctx)
    return None

def extract_phrase(why, answer):
    if not why:
        return answer or ""
    quotes = re.findall(r"[\"'\u2018\u2019\u201c\u201d]([^\"'\u2018\u2019\u201c\u201d]{25,})[\"'\u2018\u2019\u201c\u201d]", why)
    if quotes:
        return max(quotes, key=len)
    return why

if __name__ == "__main__":
    sys.path.insert(0, str(ROOT / "scripts"))
    items = json.load(open(ROOT / "sdle-prep" / "data" / "generated" / "newmcqs" / "export_mcqs.json", encoding="utf-8"))
    index = {}
    found = 0
    for it in items:
        if it.get("answerIdx") is None:
            continue
        why = it.get("why") or ""
        phrase = extract_phrase(why, it.get("answer", ""))
        r = locate(phrase)
        if r:
            book, stem, page, ctx = r
            index[it["id"]] = {"book": book, "file": stem, "page": page, "context": ctx[:700]}
            found += 1
    bank_raw = (ROOT / "sdle-prep" / "data" / "questions.js").read_text(encoding="utf-8")
    bank = json.loads(re.search(r"QUESTION_BANK\s*=\s*(\[.*\])", bank_raw, re.S).group(1))
    bank_found = 0
    for q in bank:
        bs = q.get("book_support") or ""
        if not bs.startswith("[Book:"):
            continue
        body = re.sub(r"^\[Book: [^\]]*\]\s*", "", bs)[:400]
        r = locate(extract_phrase(body, ""))
        if r:
            book, stem, page, ctx = r
            index[q["id"]] = {"book": book, "file": stem, "page": page, "context": ctx[:700]}
            bank_found += 1
    OUT = ROOT / "sdle-prep" / "data" / "generated" / "book_pages"
    OUT.mkdir(parents=True, exist_ok=True)
    json.dump(index, open(OUT / "index.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"located: {found} new + {bank_found} bank = {len(index)}")

#!/usr/bin/env python3
"""Enhanced page locator pass 2: locate passages by the ANSWER text so the
hover popup can highlight the exact answer with its page number.

Rules (books are the only truth):
- bank: only items with a verbatim [Book: support are located (high precision),
  phrase = the book_support body (strip prefix), fallback = answer option text.
- recentqa: only book-verified items (they were verified against books),
  phrase = answerText / answer, fallback = why-quotes.
- flash: only marker 'verified' MCQs (phrase = options[answerIdx]) and
  flashcards (_kind, phrase = answer). _raw_recall archive is skipped.
Atomic writes via tmp + os.replace.
"""
import json, re, os, sys, tempfile
from pathlib import Path

ROOT = Path("/data/prometric")
sys.path.insert(0, str(ROOT / "scripts"))
import build_book_pages as bb
locate = bb.locate
load = bb.load
norm = bb.norm


def locate_capped(phrase, maxfiles=10):
    """locate() but scan at most maxfiles candidate files (flash stems are generic;
    answer-text phrases are distinctive so capping is safe)."""
    import re as _re
    p = norm(phrase)
    if len(p) < 18:
        return None
    words = _re.findall(r"[a-z]{5,}", p)
    IDX = bb.IDX if bb.IDX is not None else ([locate(p)] and bb.IDX)
    cand = None
    for w in sorted(set(words), key=len, reverse=True)[:3]:
        ws = [i for i, (_, _, _, _, fw) in enumerate(IDX) if w in fw]
        cand = set(ws) if cand is None else (cand & set(ws))
        if not cand:
            break
    if cand is None:
        cand = range(len(IDX))
    scanned = 0
    for L in (60, 40, 30, 24, 18):
        if len(p) < L:
            continue
        sub = p[:L]
        for i in sorted(cand)[:maxfiles]:
            scanned += 1
            book, stem, raw, low, _ = IDX[i]
            j = low.find(sub[:30])
            if j < 0:
                continue
            page = raw.count("\f", 0, j) + 1
            ctx = _re.sub(r"\s+", " ", raw[max(0, j - 250):j + 550].replace("\f", " ")).strip()
            return (book, stem, page, ctx)
    return None

APP = ROOT / "sdle-prep"


def atomic_write(path, text):
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        fh.write(text)
    os.replace(tmp, path)


def parse_js_var(text, varname):
    m = re.search(varname + r"\s*=\s*(\[[\s\S]*?\])\s*;", text, re.S)
    if not m:
        raise ValueError(f"{varname} not found")
    return m.group(1)


def extract_phrase(why, answer):
    if not why:
        return answer or ""
    quotes = re.findall(r"[\"'\u2018\u2019\u201c\u201d]([^\"'\u2018\u2019\u201c\u201d]{25,})[\"'\u2018\u2019\u201c\u201d]", why)
    if quotes:
        return max(quotes, key=len)
    return why


def fill(items, get_phrases, tag):
    n_found = 0
    for it in items:
        if it.get("_page"):
            continue
        phrases = get_phrases(it)
        r = None
        for ph in phrases:
            if not ph or len(re.sub(r"\s+", "", ph)) < 18:
                continue
            r = locate(ph)
            if r:
                break
        if r:
            book, stem, page, ctx = r
            it["_page"] = page
            it["_book_file"] = f"{book}/{stem}"
            it["_context"] = ctx[:700]
            n_found += 1
    print(f"{tag}: +{n_found} pages")
    return n_found


def bank_phrases(q):
    bs = q.get("book_support") or ""
    if bs.startswith("[Book:"):
        body = re.sub(r"^\[Book: [^\]]*\]\s*", "", bs)[:400]
        yield body
    opts = q.get("options") or []
    ans = q.get("answer")
    if isinstance(ans, int) and 0 <= ans < len(opts) and opts[ans]:
        yield str(opts[ans])
    yield q.get("q") or ""


def qa_phrases(it):
    yield it.get("answerText") or it.get("answer") or ""
    yield extract_phrase(it.get("why") or "", it.get("answerText") or "")


def flash_phrases(it):
    # answer-text only (that is what the hover highlights); stems are too generic
    if it.get("_kind") == "flashcard":
        yield it.get("answer") or ""
        return
    opts = it.get("options") or []
    ai = it.get("answerIdx")
    if isinstance(ai, int) and 0 <= ai < len(opts) and opts[ai]:
        yield str(opts[ai])


def main():
    load()  # warm cache

    # ---- bank (verbatim [Book: support only — books are the only truth) ----
    qpath = APP / "data" / "questions.js"
    qsrc = qpath.read_text(encoding="utf-8")
    bank = json.loads(parse_js_var(qsrc, "QUESTION_BANK"))
    verbatim = [q for q in bank if q.get("usable") is not False and (q.get("book_support") or "").startswith("[Book:")]
    n1 = fill(verbatim, bank_phrases, "bank verbatim")
    qsrc2 = qsrc.replace(parse_js_var(qsrc, "QUESTION_BANK"), json.dumps(bank, ensure_ascii=False, indent=1))
    atomic_write(qpath, qsrc2)

    # ---- recentqa ----
    rpath = APP / "data" / "recent_qa.js"
    rsrc = rpath.read_text(encoding="utf-8")
    m = re.search(r"const ITEMS\s*=\s*(\[[\s\S]*?\])\s*;", rsrc, re.S)
    items = json.loads(m.group(1))
    n3 = fill(items, qa_phrases, "recentqa")
    rsrc2 = rsrc.replace(m.group(1), json.dumps(items, ensure_ascii=False, indent=1))
    atomic_write(rpath, rsrc2)

    # ---- flash (whole file is JSON after `window.FLASH_NOTES = `) ----
    fpath = APP / "data" / "flash_notes.js"
    fsrc = fpath.read_text(encoding="utf-8")
    fbody = fsrc.split("=", 1)[1].strip().rstrip().rstrip(";").strip()
    fdata = json.loads(fbody)
    flat = []
    for k, arr in fdata["byDept"].items():
        for it in arr:
            it["_dept"] = k
            flat.append(it)
    eligible = [it for it in flat if it.get("marker") == "verified" and not it.get("_page")]
    # use the capped locator via a wrapper
    _orig = fill
    def fill_capped(items, get_phrases, tag):
        n = 0
        for k, it in enumerate(items):
            if it.get("_page"):
                continue
            for ph in get_phrases(it):
                if not ph or len(re.sub(r"\s+", "", ph)) < 18:
                    continue
                r = locate_capped(ph)
                if r:
                    book, stem, page, ctx = r
                    it["_page"] = page
                    it["_book_file"] = f"{book}/{stem}"
                    it["_context"] = ctx[:700]
                    n += 1
                    break
            if k and k % 300 == 0:
                print(f"  ...flash {k}/{len(items)} found {n}", flush=True)
        print(f"{tag}: +{n} pages", flush=True)
        return n
    n4 = fill_capped(eligible, flash_phrases, "flash verified")
    back = {}
    for it in flat:
        back.setdefault(it.pop("_dept"), []).append(it)
    fdata["byDept"] = back
    fsrc2 = fsrc.replace(fbody, json.dumps(fdata, ensure_ascii=False, indent=1))
    atomic_write(fpath, fsrc2)

    print(f"TOTAL +{n1 + n3 + n4} pages")


if __name__ == "__main__":
    main()

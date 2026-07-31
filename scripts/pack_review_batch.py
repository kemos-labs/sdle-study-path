#!/usr/bin/env python3
"""
pack_review_batch.py — Pack Flash Notes items + candidate textbook passages
into a compact file for AI-assisted review.

Usage:
    python3 pack_review_batch.py --batch 1 --size 40 --only normal
    python3 pack_review_batch.py --list-pending

Output:
    work/review_batch_N.txt  — question + answer + top candidate passages
"""
from __future__ import annotations
import json, re, sys, argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from verify_textbook_v2 import TextbookIndex, DEPT_BOOKS, distinctive_words, extract_answer_text, extract_question_text, strip_markers

FN_JS = ROOT / "data" / "flash_notes.js"
VERDICTS = ROOT / "data" / "flash_notes_verdicts_v2.json"
WORK_DIR = ROOT / "work"
WORK_DIR.mkdir(exist_ok=True)


def load_data():
    text = FN_JS.read_text(encoding="utf-8")
    data = json.loads(text[text.index("{"):text.rindex("};") + 1])
    return data


def load_verdicts():
    return json.loads(VERDICTS.read_text(encoding="utf-8"))["verdicts"]


def categorize_item(it) -> str:
    stem = (it.get("stem") or "").strip()
    clean = re.sub(r"[✅🟢🟡✳🔵🔁●]", "", stem)
    clean = re.sub(r"^\s*\d+[\.\):]\s*", "", clean)
    clean = re.sub(r"^\s*Q\d+\s*[:\)\-]\s*", "", clean, flags=re.I).strip()
    has_cid = "cid:" in clean
    has_table = "|" in clean or "---" in clean
    words = len(clean.split())
    if has_cid or has_table or words < 4:
        return "garbled"
    if words < 8:
        return "short"
    return "normal"


def get_answer(it) -> str:
    ans = extract_answer_text(it)
    if ans:
        return strip_markers(ans).strip()
    # fallback: try option letter from raw
    raw = it.get("raw", "")
    m = re.search(r"([A-Za-z][A-Za-z \-,\(\)/]{5,120}?)\s*[✅✳🟢🟡]", raw)
    if m:
        return m.group(1).strip().rstrip("-•,;:").strip()
    return "(no answer extracted)"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--list-pending", action="store_true")
    parser.add_argument("--batch", type=int, default=1)
    parser.add_argument("--size", type=int, default=40)
    parser.add_argument("--dept", type=str, default="")
    parser.add_argument("--only", choices=["normal", "short", "garbled", "all"], default="normal")
    parser.add_argument("--min-score", type=float, default=0, help="Only items with best candidate score >= N")
    args = parser.parse_args()

    data = load_data()
    verdicts = load_verdicts()
    all_items = [it for items in data["byDept"].values() for it in items]

    # Items still needing review
    pending = [it for it in all_items if verdicts.get(it["id"], {}).get("verdict") != "supported"]
    if args.dept:
        pending = [it for it in pending if it.get("dept") == args.dept]

    if args.list_pending:
        from collections import Counter
        cats = Counter(categorize_item(it) for it in pending)
        depts = Counter(it.get("dept", "?") for it in pending)
        print(f"Total pending: {len(pending)}")
        print(f"Categories: {dict(cats)}")
        print(f"By dept: {dict(depts)}")
        return

    # Filter by category
    if args.only != "all":
        pending = [it for it in pending if categorize_item(it) == args.only]

    # Filter by candidate score if requested
    if args.min_score > 0:
        scored = []
        for it in pending:
            v = verdicts.get(it["id"], {})
            if v.get("score", 0) >= args.min_score:
                scored.append(it)
        pending = scored

    # Sort: highest candidate score first (most likely to have evidence)
    pending.sort(key=lambda it: verdicts.get(it["id"], {}).get("score", 0), reverse=True)

    # Slice batch
    start = (args.batch - 1) * args.size
    batch = pending[start:start + args.size]
    if not batch:
        print(f"No items in batch {args.batch}. Total pending: {len(pending)}")
        return

    # Load relevant textbook indices lazily per dept
    index_cache = {}

    def get_indices(dept):
        if dept not in index_cache:
            indices = []
            for cfg in DEPT_BOOKS.get(dept, []):
                idx = TextbookIndex(cfg)
                if idx.load():
                    indices.append(idx)
            index_cache[dept] = indices
        return index_cache[dept]

    lines = []
    lines.append(f"BATCH {args.batch} — {len(batch)} items (category={args.only}, min_score={args.min_score})")
    lines.append("=" * 80)

    for i, it in enumerate(batch, 1):
        stem = (it.get("stem") or "").strip().replace("\n", " ")
        ans = get_answer(it)
        verdict = verdicts.get(it["id"], {})
        score = verdict.get("score", 0)

        lines.append(f"\n--- ITEM {i} [{it['id']}] dept={it.get('dept')} marker={it.get('marker')} score={score} ---")
        lines.append(f"Q: {stem[:300]}")
        lines.append(f"A: {ans[:200]}")

        # Options if present
        opts = it.get("options", [])
        if opts:
            lines.append("OPTIONS:")
            for o in opts[:8]:
                lines.append(f"  {o[:120]}")

        # Raw text (helps disambiguate)
        raw = (it.get("raw") or "").strip()
        if raw and raw != stem:
            lines.append(f"RAW: {raw[:200]}")

        # Candidate passages
        indices = get_indices(it.get("dept", ""))
        if indices:
            ans_kw = distinctive_words(ans, 10)
            stem_kw = distinctive_words(extract_question_text(it), 10)
            passages = []
            for idx in indices:
                passages.extend(idx.find_best_passage(stem_kw, ans_kw, max_results=3))
            passages.sort(key=lambda p: p["score"], reverse=True)
            if passages:
                lines.append("CANDIDATE PASSAGES:")
                for p in passages[:3]:
                    lines.append(f"  [{p['score']:.1f}] ({p['book']} {p['chapter']}): {p['passage'][:280]}")
            else:
                lines.append("CANDIDATE PASSAGES: none found")
        else:
            lines.append("CANDIDATE PASSAGES: no books mapped")

    out = WORK_DIR / f"review_batch_{args.batch}.txt"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {out} ({len(batch)} items, {start + 1}-{start + len(batch)} of {len(pending)})")
    print(f"  Remaining after this batch: {len(pending) - len(batch)}")


if __name__ == "__main__":
    main()

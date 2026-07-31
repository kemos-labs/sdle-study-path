#!/usr/bin/env python3
"""
merge_model_verdicts.py — Merge free-AI-model judgments into flash_notes.js.

The AI models act as the final judge (replacing the Grok-4.5-plus-books step).
This script records their judgments HONESTLY:

  * `_model_judgment` = {"verdict": "supported"|"contradicted"|"unknown",
                         "confidence": "high"|"low"|"none",
                         "reason": "...", "models": [...]}
    — added to EVERY item the models reviewed. This is AI judgment,
      explicitly NOT labeled as textbook evidence.

  * Items where the model says SUPPORTED **and** the deterministic matcher
    found a real (non-index, non-junk) passage are upgraded to
    `_verification_verdict: supported` with that passage as `_book_explanation`
    — the strongest honest status available (textbook passage + AI confirm).

  * Items where the model says CONTRADICTED get
    `_data_quality: "answer_disputed"` so the UI/user can review them.
    Their `_verification_verdict` is NOT set to supported.

Total item count is preserved (4,026). No answers are silently rewritten.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FN_JS = ROOT / "data" / "flash_notes.js"
MODEL_VERDICTS = ROOT / "data" / "flash_notes_model_verdicts.json"
MODEL_ANSWERS = ROOT / "data" / "flash_notes_model_answers.json"
VERDICTS = ROOT / "data" / "flash_notes_verdicts_v2.json"

sys.path.insert(0, str(ROOT / "scripts"))
from verify_textbook_v2 import TextbookIndex, ALL_BOOKS, distinctive_words, expand_abbrevs, extract_answer_text, strip_markers

JUNK_PAT = re.compile(r"^\s*(?:INDEX|REFERENCES?|BIBLIOGRAPHY|GLOSSARY)\b", re.I)


def load_js(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    m = re.search(r"window\.FLASH_NOTES\s*=\s*(\{.*);", text, re.DOTALL)
    if not m:
        raise SystemExit(f"Could not parse {path}")
    return json.loads(m.group(1))


def load_books() -> list[TextbookIndex]:
    indices = []
    for cfg in ALL_BOOKS:
        idx = TextbookIndex(cfg)
        if idx.load():
            indices.append(idx)
    return indices


def find_passage(item: dict, indices: list[TextbookIndex]):
    """Return a usable passage (or None) from the deterministic matcher."""
    ans = extract_answer_text(item)
    q = strip_markers(item.get("stem") or "")
    ans_kw = expand_abbrevs(distinctive_words(ans, 10)) if ans else []
    stem_kw = expand_abbrevs(distinctive_words(q, 10))
    best = None
    for idx in indices:
        for p in idx.find_best_passage(stem_kw, ans_kw, max_results=1):
            if p["score"] > 0 and p["passage"].strip() and not JUNK_PAT.match(p["passage"]):
                if best is None or p["score"] > best["score"]:
                    best = p
    return best


def main() -> None:
    data = load_js(FN_JS)
    model_verdicts = json.loads(MODEL_VERDICTS.read_text(encoding="utf-8"))
    model_answers = {}
    if MODEL_ANSWERS.exists():
        model_answers = json.loads(MODEL_ANSWERS.read_text(encoding="utf-8"))
    verdicts = json.loads(VERDICTS.read_text(encoding="utf-8"))["verdicts"]

    indices = load_books()
    print(f"Loaded {len(indices)} books")

    upgraded = ai_supported = ai_contradicted = ai_unknown = 0
    passage_upgrades = 0
    answers_written = 0

    for items in data["byDept"].values():
        for item in items:
            mv = model_verdicts.get(item["id"])
            ma = model_answers.get(item["id"])

            # Model-suggested answer for MCQs that had no marked answer
            if ma and ma.get("verdict", "").startswith("ANSWER_"):
                letter = ma["verdict"].replace("ANSWER_", "")
                opts = item.get("options", [])
                if letter in "ABCDE" and letter != "X":
                    idx = "ABCDE".index(letter)
                    if idx < len(opts):
                        item["_model_suggested_answer"] = {
                            "letter": letter,
                            "answerIdx": idx,
                            "confidence": ma.get("confidence", "low"),
                            "reason": ma.get("reason", ""),
                            "models": list(ma.get("detail", {}).keys()),
                        }
                        answers_written += 1

            if not mv:
                continue
            verdict = mv.get("verdict", "UNKNOWN").lower()
            detail = mv.get("detail", {})
            models = [m for m, d in detail.items() if d.get("verdict") not in ("ERROR",) and d.get("verdict") in ("SUPPORTED", "CONTRADICTED", "UNKNOWN")][:8]

            judgment = {
                "verdict": verdict,
                "confidence": mv.get("confidence", "low"),
                "reason": mv.get("reason", ""),
                "models": models,
            }
            item["_model_judgment"] = judgment

            # Record embedded answer (recall-note 'Question? Answer') if present
            from verify_with_models import extract_embedded_answer as _emb
            emb = _emb(item.get("stem", ""))
            if emb:
                item["_embedded_answer"] = emb

            if verdict == "supported":
                ai_supported += 1
                # If a real passage exists, upgrade to supported with citation
                passage = find_passage(item, indices)
                if passage:
                    item["_verification_verdict"] = "supported"
                    item["_book_explanation"] = {
                        "book": passage.get("book", "Canonical SCFHS text"),
                        "chapter": passage.get("chapter", ""),
                        "passage": passage["passage"],
                        "status": "automated_evidence_candidate_ai_confirmed",
                    }
                    upgraded += 1
                    passage_upgrades += 1
                else:
                    # AI says correct but no textbook passage found — keep needs_review
                    # (do not fabricate a citation)
                    pass
            elif verdict == "contradicted":
                ai_contradicted += 1
                # Use a dedicated flag — do not clobber _data_quality (e.g. merged_options_review)
                item["_answer_disputed"] = True
                item["_verification_verdict"] = "needs_review"
                item.pop("_book_explanation", None)
            else:
                ai_unknown += 1

    all_items = [it for items in data["byDept"].values() for it in items]
    if len(all_items) != data["total"]:
        raise SystemExit(f"Refusing to write: {len(all_items)} items != declared total {data['total']}")

    FN_JS.write_text(
        "/** Flash Notes — source recalls plus canonical-book evidence candidates. */\n"
        "window.FLASH_NOTES = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n",
        encoding="utf-8",
    )
    print(f"AI supported (no passage, kept needs_review): {ai_supported - passage_upgrades}")
    print(f"AI supported + real passage → upgraded:       {passage_upgrades}")
    print(f"AI contradicted → flagged answer_disputed:     {ai_contradicted}")
    print(f"AI unknown:                                    {ai_unknown}")
    print(f"Model-suggested answers written:               {answers_written}")
    print(f"Total model-judged items:                      {ai_supported + ai_contradicted + ai_unknown}")


if __name__ == "__main__":
    main()

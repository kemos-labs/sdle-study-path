#!/usr/bin/env python3
"""
verify_with_models.py — Verify Flash Notes answers using free AI models in parallel.

The deterministic matcher (verify_textbook_v2.py) finds candidate book passages.
This script sends each item + its candidate passages to multiple free AI models,
which JUDGE whether the passage supports the marked answer.

The AI models are the "final judge" role (instead of Grok 4.5):
  - SUPPORTED: passage supports the marked answer
  - CONTRADICTED: passage contradicts the marked answer
  - UNKNOWN: no passage, or passage is inconclusive

Usage:
    python3 verify_with_models.py --batch 1 --size 30 --models 4
    python3 verify_with_models.py --list-pending
"""
from __future__ import annotations
import json, re, sys, time, argparse, concurrent.futures, random
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from verify_textbook_v2 import TextbookIndex, ALL_BOOKS, distinctive_words, expand_abbrevs, extract_answer_text, strip_markers, norm

FN_JS = ROOT / "data" / "flash_notes.js"
VERDICTS = ROOT / "data" / "flash_notes_verdicts_v2.json"
OUT_JSON = ROOT / "data" / "flash_notes_model_verdicts.json"
ANSWER_OUT_JSON = ROOT / "data" / "flash_notes_model_answers.json"

# ── Free model pools ──────────────────────────────────────────────────
AUTH = json.loads(Path("/home/kalde/.pi/agent/auth.json").read_text())

KILO_MODELS = [
    "kilo-auto/free",
    "stepfun/step-3.7-flash:free",
    "inclusionai/ling-3.0-flash:free",
    "nvidia/nemotron-3-super-120b-a12b:free",
    "nvidia/nemotron-3-ultra-550b-a55b:free",
    "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
    "cohere/north-mini-code:free",
    "poolside/laguna-s-2.1:free",
    "poolside/laguna-xs-2.1:free",
    "poolside/laguna-m.1:free",
    "openrouter/free",
]

OPENCODE_MODELS = [
    "big-pickle",
    "deepseek-v4-flash-free",
    "ling-3.0-flash-free",
    "mimo-v2.5-free",
    "nemotron-3-ultra-free",
    "north-mini-code-free",
]

# Models that actually returned text in tests
# Decisive (give real SUPPORTED/CONTRADICTED with reasons):
WORKING = [
    ("kilo", "kilo-auto/free"),
    ("kilo", "inclusionai/ling-3.0-flash:free"),
    ("kilo", "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free"),
    ("kilo", "nvidia/nemotron-3-super-120b-a12b:free"),
    ("kilo", "openrouter/free"),
    ("opencode", "nemotron-3-ultra-free"),
]

SYSTEM_PROMPT = """You are a dental board exam verifier. You are given:
1. A question from a dental exam
2. The marked answer (may be absent — then judge based on medical knowledge)
3. Candidate passages from official dental textbooks

Your job: determine whether the marked answer is CORRECT.

IMPORTANT: Your ENTIRE reply must start with exactly this line:
VERDICT: SUPPORTED|CONTRADICTED|UNKNOWN
Then one more line:
REASON: <one short sentence>

- SUPPORTED = the passage or your knowledge confirms the marked answer is correct
- CONTRADICTED = the passage or your knowledge shows the marked answer is wrong
- UNKNOWN = you cannot determine correctness (no passage, ambiguous)

Do NOT explain your reasoning process. Just output the verdict line and the reason line.
If no marked answer is given, still give your best judgment of the correct answer
in the REASON line."""


def call_model(provider: str, model: str, prompt: str, timeout: int = 120,
              system_prompt: str | None = None) -> str:
    """Call a free model API and return the response text."""
    if provider == "kilo":
        url = "https://api.kilo.ai/api/gateway/chat/completions"
        key = "placeholder"
    elif provider == "opencode":
        url = "https://opencode.ai/zen/v1/chat/completions"
        key = " "
    else:
        return ""

    body = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt or SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        "max_tokens": 300,
        "temperature": 0.2,
    }).encode()

    req = Request(url, data=body, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {key}",
    })

    for attempt in range(4):
        try:
            with urlopen(req, timeout=timeout) as resp:
                data = json.loads(resp.read().decode())
            msg = data.get("choices", [{}])[0].get("message", {})
            content = msg.get("content") or ""
            if not content and msg.get("reasoning_content"):
                content = msg.get("reasoning_content", "")
            return content.strip()
        except HTTPError as e:
            if e.code == 429:
                time.sleep(5 * (attempt + 1))
                continue
            if e.code in (500, 502, 503):
                time.sleep(3)
                continue
            # 401/403 = auth/entitlement/rate-limit — fail fast
            return f"__HTTP_ERROR__ {e.code}"
        except Exception as e:
            return f"__ERROR__ {str(e)[:80]}"
    return "__HTTP_ERROR__ rate_limited"


def judge_response(text: str) -> tuple[str, str]:
    """Parse model response into (verdict, reason).
    Searches the whole text for VERDICT:/REASON: lines, robust to
    reasoning-chain prefixes some models emit.
    """
    if text.startswith("__"):
        return "ERROR", text
    # Find VERDICT anywhere in the text
    m = re.search(r"VERDICT\s*[:\-]\s*(\w+)", text, re.IGNORECASE)
    verdict = m.group(1).upper() if m else "UNKNOWN"
    if verdict not in ("SUPPORTED", "CONTRADICTED", "UNKNOWN"):
        verdict = "UNKNOWN"
    m2 = re.search(r"REASON\s*[:\-]\s*(.+?)(?:\n|$)", text, re.IGNORECASE | re.DOTALL)
    reason = m2.group(1).strip()[:200] if m2 else text[-200:].strip()
    return verdict, reason


ANSWER_SYSTEM_PROMPT = """You are a dental board exam expert answering a multiple-choice question.
You are given a question with options (one may be marked "(my answer)" by the student —
ignore that unless you agree; pick the SINGLE best clinical answer).

IMPORTANT: Your ENTIRE reply must start with exactly this line:
ANSWER: <letter>
Then one more line:
REASON: <one short sentence>

Choose only among the option letters given (A, B, C, D, ...).
If you cannot determine the answer, reply: ANSWER: X with reason UNKNOWN.
Do NOT explain your reasoning process beyond the REASON line."""


def judge_answer_response(text: str, opt_count: int) -> tuple[str, str]:
    """Parse model response into (letter, reason)."""
    if text.startswith("__"):
        return "ERROR", text
    letters = "ABCDE"[:opt_count]
    m = re.search(r"ANSWER\s*[:\-]\s*([A-Ea-e])", text)
    letter = m.group(1).upper() if m else "X"
    if letter not in letters:
        m2 = re.search(r"\b([" + letters + r"])\b", text)
        letter = m2.group(1).upper() if m2 and m2.group(1).upper() in letters else "X"
    m3 = re.search(r"REASON\s*[:\-]\s*(.+?)(?:\n|$)", text, re.IGNORECASE | re.DOTALL)
    reason = m3.group(1).strip()[:200] if m3 else text[-200:].strip()
    return letter, reason


def build_answer_prompt(it: dict, passages: list[dict]) -> str:
    """Prompt asking the model to pick the correct option (for MCQs with no marked answer)."""
    stem = (it.get("stem") or "").strip()
    opts = it.get("options", [])
    lines = []
    lines.append(f"QUESTION: {stem[:400]}")
    if opts:
        lines.append("OPTIONS:")
        for i, o in enumerate(opts[:8]):
            lines.append(f"  {chr(65+i)}. {o[:150]}")
    lines.append("")
    if passages:
        lines.append("TEXTBOOK PASSAGES (candidate evidence):")
        for i, p in enumerate(passages[:3], 1):
            lines.append(f"[{i}] ({p.get('book','')} {p.get('chapter','')}):")
            lines.append(p.get("passage", "")[:400])
    else:
        lines.append("TEXTBOOK PASSAGES: (none found — judge from your own knowledge)")
    return "\n".join(lines)


FRAGMENT_SYSTEM_PROMPT = """You are a dental board exam expert answering a recall question from a student's study notes.
The question is a free-text question with NO multiple-choice options (ignore any "A." "B." etc. that appear in the raw OCR text — they are leftovers from unrelated questions).

IMPORTANT: Your ENTIRE reply must be EXACTLY two lines:
ANSWER: <your answer as plain text, one short phrase, NOT a letter>
REASON: <one short sentence>

Example:
ANSWER: stainless steel crown
REASON: standard treatment for multi-surface caries in primary molars

If the question is too garbled to answer, reply: ANSWER: UNKNOWN with reason explaining why."""


def judge_fragment_response(text: str) -> tuple[str, str]:
    """Parse model response into (answer_text, reason)."""
    if text.startswith("__"):
        return "ERROR", text
    m = re.search(r"ANSWER\s*[:\-]\s*(.+?)(?:\n|$)", text, re.IGNORECASE | re.DOTALL)
    answer = m.group(1).strip()[:150] if m else text[-200:].strip()
    # Reject single-letter "answers" (models confusing with MCQ options)
    if re.match(r"^[A-Ea-eX]\s*$", answer):
        answer = "UNKNOWN"
    m2 = re.search(r"REASON\s*[:\-]\s*(.+?)(?:\n|$)", text, re.IGNORECASE | re.DOTALL)
    reason = m2.group(1).strip()[:200] if m2 else ""
    if answer.upper() == "UNKNOWN":
        return "UNKNOWN", reason
    return answer, reason


def build_fragment_prompt(it: dict, passages: list[dict]) -> str:
    """Prompt asking the model to answer a free-text recall fragment."""
    stem = (it.get("stem") or "").strip()
    raw = (it.get("raw") or "").strip()
    lines = []
    lines.append(f"QUESTION: {stem[:400]}")
    if raw and raw != stem:
        lines.append(f"RAW NOTE: {raw[:200]}")
    lines.append("")
    if passages:
        lines.append("TEXTBOOK PASSAGES (candidate evidence):")
        for i, p in enumerate(passages[:3], 1):
            lines.append(f"[{i}] ({p.get('book','')} {p.get('chapter','')}):")
            lines.append(p.get("passage", "")[:400])
    else:
        lines.append("TEXTBOOK PASSAGES: (none found — judge from your own knowledge)")
    return "\n".join(lines)


def extract_embedded_answer(stem: str) -> str:
    """Extract an answer embedded after '?' in recall-note stems.
    e.g. 'Pedo with multi-surface caries? SSC' → 'SSC'
         'Canine with class V, which clamp to use? 212' → '212'
    Returns '' if no reliable answer is embedded.
    """
    stem = (stem or "").strip()
    if "?" not in stem:
        return ""
    qpos = stem.rfind("?")
    after = stem[qpos + 1:].strip()
    # Reject if text after '?' starts with a question number (e.g. "9- Patient...")
    if re.match(r"^\d+[-\\.\)]\s", after):
        return ""
    # Take up to first newline / double space / next numbered question
    ans = re.split(r"\n\s*(?=[A-Z0-9])|\s{2,}|(?=\d+[-\\.\)]\s*[A-Z])", after)[0].strip()
    ans = re.sub(r"^[-•\s]+", "", ans).strip()
    ans = re.split(r"\s+(?=[A-Da-d][\\.\)]\s)", ans)[0].strip()
    if len(ans) < 2 or re.match(r"^(A\.|B\.|C\.|D\.|yes|no|y|n)$", ans, re.I):
        return ""
    return ans


def build_prompt(it: dict, passages: list[dict]) -> str:
    stem = (it.get("stem") or "").strip()
    ans = extract_answer_text(it)
    embedded = extract_embedded_answer(stem)
    opts = it.get("options", [])
    raw = (it.get("raw") or "").strip()

    lines = []
    lines.append(f"QUESTION: {stem[:400]}")
    if opts:
        lines.append("OPTIONS:")
        for o in opts[:8]:
            lines.append(f"  {o[:150]}")
    if ans:
        lines.append(f"MARKED ANSWER: {ans[:150]}")
    elif embedded:
        lines.append(f"MARKED ANSWER (extracted from recall note): {embedded[:150]}")
    else:
        lines.append("MARKED ANSWER: (none — answer the question yourself)")
    lines.append("")
    if passages:
        lines.append("TEXTBOOK PASSAGES (candidate evidence):")
        for i, p in enumerate(passages[:3], 1):
            lines.append(f"[{i}] ({p.get('book','')} {p.get('chapter','')}):")
            lines.append(p.get("passage", "")[:400])
    else:
        lines.append("TEXTBOOK PASSAGES: (none found — judge from your own knowledge)")
    return "\n".join(lines)


def get_passages(it: dict, indices: list[TextbookIndex], n: int = 3) -> list[dict]:
    """Get candidate passages for an item using the deterministic matcher."""
    ans = extract_answer_text(it) or extract_embedded_answer(it.get("stem", ""))
    q = strip_markers(it.get("stem") or "")
    ans_kw = expand_abbrevs(distinctive_words(ans, 10)) if ans else []
    stem_kw = expand_abbrevs(distinctive_words(q, 10))
    passages = []
    for idx in indices:
        passages.extend(idx.find_best_passage(stem_kw, ans_kw, max_results=2))
    passages.sort(key=lambda p: p["score"], reverse=True)
    return passages[:n]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", type=int, default=1)
    parser.add_argument("--size", type=int, default=20)
    parser.add_argument("--models", type=int, default=3, help="Models to call per item")
    parser.add_argument("--list-pending", action="store_true")
    parser.add_argument("--dept", type=str, default="")
    parser.add_argument("--only", choices=["has-ans", "no-ans", "all", "embedded", "answer-mcq", "fragment"], default="all")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--resume", action="store_true", help="skip items already in the output JSON")
    args = parser.parse_args()

    data = json.loads(re.search(r"window\.FLASH_NOTES\s*=\s*(\{.*);", FN_JS.read_text(), re.DOTALL).group(1))
    verdicts = json.loads(VERDICTS.read_text())["verdicts"]
    all_items = [it for items in data["byDept"].values() for it in items]

    pending = [it for it in all_items if verdicts.get(it["id"], {}).get("verdict") != "supported"]
    if args.dept:
        pending = [it for it in pending if it.get("dept") == args.dept]
    if args.only == "has-ans":
        pending = [it for it in pending if extract_answer_text(it)]
    elif args.only == "no-ans":
        pending = [it for it in pending if not extract_answer_text(it)]
    elif args.only == "embedded":
        pending = [it for it in pending if not extract_answer_text(it) and extract_embedded_answer(it.get("stem", ""))]
    elif args.only == "fragment":
        # Answerable fragments: have '?' in stem, <2 options, no extractable embedded answer
        pending = [it for it in pending if not extract_answer_text(it)
                   and len(it.get("options", [])) < 2
                   and "?" in (it.get("stem") or "")
                   and not extract_embedded_answer(it.get("stem", ""))]
    elif args.only == "answer-mcq":
        # Real MCQs (>=2 options) with no marked answer — models pick the answer
        pending = [it for it in pending if not extract_answer_text(it)
                   and len(it.get("options", [])) >= 2
                   and len(it.get("stem", "").strip()) > 5]

    if args.resume and OUT_JSON.exists():
        existing = json.loads(OUT_JSON.read_text())
        before = len(pending)
        pending = [it for it in pending if it["id"] not in existing]
        print(f"Resume: skipping {before - len(pending)} already-verified items")

    if args.list_pending:
        from collections import Counter
        print(f"Pending: {len(pending)}")
        print(f"By dept: {dict(Counter(it.get('dept','?') for it in pending))}")
        print(f"Has answer: {sum(1 for it in pending if extract_answer_text(it))}")
        return

    # Sort by deterministic score desc (best candidates first)
    pending.sort(key=lambda it: verdicts.get(it["id"], {}).get("score", 0), reverse=True)
    start = (args.batch - 1) * args.size
    batch = pending[start:start + args.size]
    if not batch:
        print(f"Batch {args.batch} empty. {len(pending)} pending total.")
        return

    # Load books once
    print("Loading books...", file=sys.stderr)
    indices = []
    for cfg in ALL_BOOKS:
        idx = TextbookIndex(cfg)
        if idx.load():
            indices.append(idx)

    # Shuffle model pool to distribute rate limits
    model_pool = list(WORKING)
    random.shuffle(model_pool)

    results = {}
    model_usage = {}

    # Per-provider concurrency semaphores (opencode throttles under burst)
    _locks = {
        "kilo": __import__("threading").Semaphore(4),
        "opencode": __import__("threading").Semaphore(2),
    }

    def call_limited(prov, mdl, prompt, system_prompt=None):
        with _locks[prov]:
            return call_model(prov, mdl, prompt, system_prompt=system_prompt)

    def verify_one(it):
        answer_mode = (args.only in ("answer-mcq", "fragment"))
        fragment_mode = (args.only == "fragment")
        passages = get_passages(it, indices)
        if answer_mode:
            prompt = build_answer_prompt(it, passages) if not fragment_mode else build_fragment_prompt(it, passages)
            sys_prompt = ANSWER_SYSTEM_PROMPT
        else:
            prompt = build_prompt(it, passages)
            sys_prompt = SYSTEM_PROMPT
        # Prefer a mix of providers
        kilo_pool = [m for m in model_pool if m[0] == "kilo"][:max(args.models, 2)]
        opencode_pool = [m for m in model_pool if m[0] == "opencode"]
        chosen = kilo_pool[:args.models - 1]
        if opencode_pool:
            chosen.append(opencode_pool[0])
        chosen = chosen[:args.models]
        if len(chosen) < args.models:
            chosen = (chosen + kilo_pool + opencode_pool)[:args.models]
        votes = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.models) as ex:
            futures = {ex.submit(call_limited, prov, mdl, prompt, sys_prompt): (prov, mdl) for prov, mdl in chosen}
            for fut in concurrent.futures.as_completed(futures):
                prov, mdl = futures[fut]
                try:
                    text = fut.result()
                    if fragment_mode:
                        verdict, reason = judge_fragment_response(text)
                    elif answer_mode:
                        letter, reason = judge_answer_response(text, len(it.get("options", [])))
                        verdict = letter
                    else:
                        verdict, reason = judge_response(text)
                    votes[f"{prov}/{mdl}"] = {"verdict": verdict, "reason": reason}
                    model_usage[mdl] = model_usage.get(mdl, 0) + 1
                except Exception as e:
                    votes[f"{prov}/{mdl}"] = {"verdict": "ERROR", "reason": str(e)[:80]}

        if answer_mode:
            if fragment_mode:
                # Aggregate free-text answers: pick the most common non-UNKNOWN
                real_votes = [v for v in votes.values() if v["verdict"] not in ("ERROR", "UNKNOWN")]
                if not real_votes:
                    agg = {"verdict": "ERROR", "reason": "all models failed", "detail": votes}
                else:
                    from collections import Counter as _C
                    # Normalize answers for comparison (lowercase, collapse spaces)
                    normed = {}
                    for v in real_votes:
                        key = re.sub(r"\s+", " ", v["verdict"].lower()).strip()[:60]
                        normed.setdefault(key, []).append(v)
                    best = max(normed.values(), key=len)
                    top_votes = best
                    answer_text = top_votes[0]["verdict"]
                    reasons = [v["reason"][:120] for v in top_votes][:2]
                    agg = {
                        "verdict": f"FRAG_ANSWER: {answer_text[:120]}",
                        "confidence": "high" if len(top_votes) >= 2 else "low",
                        "reason": "; ".join(reasons),
                        "votes": {v["verdict"][:40]: 1 for v in real_votes},
                        "detail": votes,
                    }
                return it["id"], agg, passages

            # Aggregate letter votes: majority of non-error, non-X
            real_votes = [v for v in votes.values() if v["verdict"] not in ("ERROR", "X")]
            if not real_votes:
                agg = {"verdict": "ERROR", "reason": "all models failed", "detail": votes}
            else:
                from collections import Counter as _C
                counts = _C(v["verdict"] for v in real_votes)
                top = counts.most_common(1)[0]
                reasons = [v["reason"][:120] for v in real_votes if v["verdict"] == top[0]][:2]
                agg = {
                    "verdict": f"ANSWER_{top[0]}",
                    "confidence": "high" if top[1] >= 2 else "low",
                    "reason": "; ".join(reasons),
                    "votes": dict(counts),
                    "detail": votes,
                }
            return it["id"], agg, passages

        # Aggregate: majority of non-error, non-unknown votes
        decisive = [v for v in votes.values() if v["verdict"] in ("SUPPORTED", "CONTRADICTED")]
        real_votes = [v for v in votes.values() if v["verdict"] != "ERROR"]
        if not real_votes:
            agg = {"verdict": "ERROR", "reason": "all models failed"}
        elif len(decisive) == 1 and len(votes) >= 2:
            # Single decisive vote — needs confirmation
            d = decisive[0]
            agg = {
                "verdict": d["verdict"],
                "confidence": "low",
                "reason": d["reason"][:200],
                "votes": {v["verdict"]: sum(1 for x in votes.values() if x["verdict"] == v["verdict"]) for v in [d]},
                "detail": votes,
            }
        elif decisive:
            counts = {}
            for v in decisive:
                counts[v["verdict"]] = counts.get(v["verdict"], 0) + 1
            agg_verdict = max(counts, key=counts.get)
            if len(set(counts.values())) > 1 and max(counts.values()) >= 2:
                conf = "high"
            else:
                conf = "low"
            reasons = [v["reason"][:120] for v in decisive if v["verdict"] == agg_verdict][:2]
            agg = {
                "verdict": agg_verdict,
                "confidence": conf,
                "reason": "; ".join(reasons),
                "votes": counts,
                "detail": votes,
            }
        else:
            reasons = [v["reason"][:120] for v in real_votes if v.get("reason")][:2]
            agg = {
                "verdict": "UNKNOWN",
                "confidence": "none",
                "reason": "; ".join(reasons) if reasons else "all models abstained",
                "votes": {v["verdict"]: sum(1 for x in real_votes if x["verdict"] == v["verdict"]) for v in real_votes},
                "detail": votes,
            }
        return it["id"], agg, passages

    # Verify batch (limited concurrency to respect rate limits)
    all_results = {}
    out = ANSWER_OUT_JSON if args.only in ("answer-mcq", "fragment") else OUT_JSON
    existing = {}
    if out.exists():
        try:
            existing = json.loads(out.read_text())
        except Exception:
            existing = {}

    # Incremental save: write after every item so timeouts don't lose progress
    def _save(extra=None):
        data_out = dict(existing)
        data_out.update(all_results)
        if extra:
            data_out.update(extra)
        out.write_text(json.dumps(data_out, ensure_ascii=False, indent=2))
        return len(data_out)

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.models) as ex:
        futures = [ex.submit(verify_one, it) for it in batch]
        done = 0
        for fut in concurrent.futures.as_completed(futures):
            it_id, agg, passages = fut.result()
            all_results[it_id] = agg
            done += 1
            status = agg["verdict"]
            print(f"[{done}/{len(batch)}] {it_id}: {status} (votes={agg.get('votes',{})})", flush=True)
            if done % 5 == 0 or done == len(batch):
                total_saved = _save()
                print(f"  → saved ({total_saved} total)", flush=True)

    # Summary
    counts = {}
    for r in all_results.values():
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
    print(f"\n=== BATCH {args.batch} SUMMARY ===")
    print(f"  SUPPORTED:    {counts.get('SUPPORTED', 0)}")
    print(f"  CONTRADICTED: {counts.get('CONTRADICTED', 0)}")
    print(f"  UNKNOWN:      {counts.get('UNKNOWN', 0)}")
    print(f"  ERROR:        {counts.get('ERROR', 0)}")
    print(f"\nModel usage: {dict(model_usage)}")

    # Final save (incremental, resumable)
    total_saved = _save()
    print(f"\nSaved {out} ({total_saved} total results)")

    # Also write a status marker for the current run
    meta = {
        "last_batch": args.batch,
        "size": len(batch),
        "only": args.only,
        "dept": args.dept,
        "updated_at": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
    }
    meta_path = ROOT / "work" / "model_verdict_progress.json"
    meta_path.parent.mkdir(exist_ok=True)
    meta_path.write_text(json.dumps(meta, indent=2))


if __name__ == "__main__":
    main()

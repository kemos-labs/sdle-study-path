# Flash Notes AI Review — Status & Handoff (2026-07-31)

## What was done this sessionThe user provided free AI models at `/home/kalde/Downloads/pi` (kilo + opencode
providers) to replace the missing Grok-4.5-plus-books final-judge step. The
assistant acted as orchestrator/brain: the deterministic textbook matcher finds
candidate passages, then **free AI models judge each question** (open-book
style), and the assistant aggregates/validates.

### New artifacts
- `scripts/verify_with_models.py` — parallel free-model verifier.
  Modes: `has-ans` (verify marked answers), `embedded` (verify recall-note
  "Question? Answer" answers), `answer-mcq` (models pick the correct option
  for MCQs with no marked answer), `fragment` (free-text answering of broken
  stems — **unreliable, do not trust**).
  - Providers: **kilo** (`https://api.kilo.ai/api/gateway`, auth `placeholder`,
    ~100 req/model/day, models reset midnight UTC) and **opencode**
    (`https://opencode.ai/zen/v1`, auth `" "`, 428 req/day shared, midnight UTC).
  - Reliable models (from live testing): `kilo-auto/free`,
    `inclusionai/ling-3.0-flash:free`, `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free`,
    `nvidia/nemotron-3-super-120b-a12b:free`, `openrouter/free` (kilo);
    `nemotron-3-ultra-free`, `ling-3.0-flash-free` (opencode).
  - Unreliable (empty/403): `poolside/*`, `cohere/north-mini-code`,
    `stepfun/step-3.7-flash:free` (empty), opencode under burst (transient 403s).
  - **Cline free API is rate-limited** (`deepseek/deepseek-v4-flash` 429 "try
    again in 20h"); ClinePass needs a $9.99/mo subscription (403
    ENTITLEMENT_ERROR). Do not spend retries on them.
  - Incremental save every 5 items (resumable via `--resume`).
- `scripts/merge_model_verdicts.py` — writes `_model_judgment`,
  `_model_suggested_answer`, `_embedded_answer`, `_answer_disputed` into
  `data/flash_notes.js`. Only upgrades to `supported` when a real non-junk
  textbook passage exists (AI + passage = strongest honest status).
- `data/flash_notes_model_verdicts.json` — 571 raw model judgments.
- `data/flash_notes_model_answers.json` — 78 model-suggested MCQ answers.

### Data integrity fixes
- `verify_textbook_v2.py`: added `is_junk(search_text)` check in
  `find_best_passage` phase 2 — was emitting passages starting with
  "Reference 44." (references-section contamination). Fixed 5 items that were
  `supported` with junk citations (FN-CITATION gate).
- `merge_model_verdicts.py`: uses `_answer_disputed` separate flag — no longer
  clobbers `_data_quality: merged_options_review` (FN-MERGED gate).
- `js/app.js`: fixed pre-existing `sourceChipsHtml is not defined` bug that
  broke the Flash Notes tab entirely; added honest UI badges:
  - `⚠ AI disputes answer` (red) — model judged marked answer wrong
  - `🤖 AI-confirmed` — model judged marked answer correct (no citation)
  - `🤖 AI-suggested` — model picked an answer for MCQs that had none
  - `📖 evidence candidate` (unchanged, only for real passages)
  - Audit stats line: `🤖 N AI-reviewed · ⚠ N answer disputed · 💡 N AI-suggested`
- `index.html`/`sw.js`: version bump `20260731fn1 → 20260731fn2`, cache v41.

## Current state (all gates green, exit 0)
- Total items: **4,026** (unchanged)
- `_verification_verdict: supported` (evidence candidates): **1,897**
- `needs_review`: **2,129**
- AI-judged items: **571** (325 supported, 127 contradicted, 119 unknown)
- AI-suggested MCQ answers: **78**
- Embedded recall answers extracted: **439**
- Answer-disputed flags: **127** (models found these marked answers likely wrong)

## Honest labels (per docs/RED_LINE_NO_SLACK.md)
- `supported` + `_book_explanation` = automated evidence candidate with a real
  passage (never called "textbook-verified").
- `_model_judgment.verdict == supported` without passage = AI judgment only,
  kept `needs_review` — **no fabricated citation**.
- `_answer_disputed` = AI review flagged the marked answer; user must verify.

## Fragment repair (markitdown investigation, 2026-07-31 PM)

**User suggested `microsoft/markitdown` for PDF→text.** Investigation result:
- markitdown (v0.1.6, pdfminer+pdfplumber backend) was ALREADY used for all
  flash-notes source .md files — fresh extractions are byte-identical
  (verified on Saud_Masahhah, SDLE_May_2026, Mar-June_2026).
- The real fragment cause is a **parser bug** in `build_flash_notes.py`:
  `parse_sectioned` starts a new item at every `- ` bullet, so answer options
  became standalone "questions"; dash-numbered questions ("31- text") also
  failed to match the numbered-start regex.

### Repair applied (`scripts/repair_saud_parse.py`)
- Re-parses the Saud_Masahhah source .md with a fixed parser: `- `/`●`
  bullets become OPTIONS of the current question; dash-numbered and Qn lines
  start questions.
- 863 items repaired (clean stems + real options + marked answers where the
  source had ✅). 405 fragments tagged `_merged_into` (hidden from list, shown
  as parent options). No items added/removed (still 4,026).
- `reverify_repaired.py`: re-ran textbook verification on repaired
  answer-bearing items → **105 more items supported** (1921 → 1922 after
  re-apply, 0 regressions: no items lost options, no valid answers changed).
- Fixed `normalize_flash_note_options.py` to skip `_repaired_2026` items
  (was clobbering repaired options by re-deriving from stale `raw`).
- UI: `_merged_into` fragments hidden from study list & flashcard deck;
  "🛠 repaired" badge on repaired cards; aiStats extended with repaired counts.
- Fragments: 1,492 → **788 remaining** (581 Saud orphans + 207 real
  answerless questions from other sources).

## Remaining work (updated)
1. **~788 remaining fragments** — 581 are orphaned Saud bullets (no reliable
   parent match; forcing links risks wrong joins — left flagged honestly);
   207 are real answerless questions (June_July2023, Mar-June, SDLE_May) that
   can be answered by free models (answer-mcq mode) and then verified.
2. Low-confidence model answers (conf: low) should be treated as hints only.
3. Consider a UI filter for "answer disputed" so users can review the 127.
4. The 581 Saud orphans could get a second, looser parent-link pass IF a
   human validates the joins (or accept as flagged recall leads).
5. Run `python3 scripts/repair_saud_parse.py --apply` only if the source
   .md changes — it is idempotent and preserves existing good options/answers.

## Useful commands
```bash
# Re-run model verification (resumes from saved progress)
python3 scripts/verify_with_models.py --batch 1 --size N --models 3 --only embedded --resume

# Answer MCQs without marked answers
python3 scripts/verify_with_models.py --batch 1 --size N --models 3 --only answer-mcq --resume

# Merge model judgments into flash_notes.js
python3 scripts/merge_model_verdicts.py

# Gates
python3 scripts/gate_flash_notes.py   # exit 0 = green

# UI smoke test (playwright)
node /tmp/ui_test4.js   # with server: python3 -m http.server 8765
```

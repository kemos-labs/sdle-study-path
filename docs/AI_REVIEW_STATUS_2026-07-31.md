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
   207 are real answerless questions (June_July2023, Mar-June, SDLE_May).
   **DONE for the answer-mcq subset (commit 99a9522)**: 396 AI-suggested
   answers written (232 high-confidence = 2+ models agree). Fragment
   free-text mode re-confirmed UNRELIABLE (models echo the prompt) — the
   87 non-MCQ recall questions with '?' remain un-answered by design;
   they need a stronger judge or manual review, never auto-write.
2. Low-confidence model answers (conf: low) should be treated as hints only.
3. **DONE (2026-07-31, commit 669337f)** — disputed review flow shipped:
   ⚠ Disputed chip (cross-dept study mode over all 127), dispute reason +
   confidence + models shown on cards, per-item adjudication (✅ source /
   ✏️ AI right) in localStorage (`sdle3_fnDisputeReview`), 📋 export →
   `flash_notes_dispute_review.json`. Next step when the user adjudicates:
   apply the decisions to `data/flash_notes.js` (fix answerLetter/answerIdx
   or add `_answer_disputed` false/keep) via a small script.
4. The 581 Saud orphans could get a second, looser parent-link pass IF a
   human validates the joins (or accept as flagged recall leads).
5. Run `python3 scripts/repair_saud_parse.py --apply` only if the source
   .md changes — it is idempotent and preserves existing good options/answers.
6. **Pipeline order matters**: run `merge_model_verdicts.py` BEFORE
   `apply_flash_notes_verdicts.py` — apply is the citation authority and
   re-applies deterministic v2 evidence (restores correct passages, e.g.
   fn_endo_0468 Lang & Lindhe 'renal osteodystrophy'). Never skip apply
   after merge or citations drift.

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

## Deployed (2026-07-31, commits 99a9522 → 4f335da → 2e5ffe0)
- **Live at https://kemos-labs.github.io/sdle-study-path/** (GitHub Pages,
  legacy build from `main` at repo root; push to main auto-deploys).
- 396 AI-suggested answers, 571 AI-reviewed, 127 disputed, 863 repaired,
  405 merged fragments — all verified live via Playwright against the
  deployed URL (audit stats, disputed chip + 127-row review panel, Recent
  Q&A tab all render; zero page errors).
- Fixed 404s on the live site: `data/recent_qa.js` + `data/book_refs.js`
  were referenced by index.html but never committed → now tracked (2e5ffe0).
- Deploy check: `curl -sI https://kemos-labs.github.io/sdle-study-path/` →
  200; rebuild takes ~60 s after push; verify via
  `gh api repos/kemos-labs/sdle-study-path/pages/builds/latest`.

---

## Continuation pass (2026-07-31 PM → 2026-08-01)

### Verification of the prior session's claims (re-baselined)
- `scripts/gate_flash_notes.py` → **all green, exit 0** (FN-COUNT/OPTS/IDX/
  CITATION/BOOKS/VERIFIED/MERGED all ok; total 4026; supported 1922→1945;
  needs_review 2104→2081).
- `node scripts/flash_notes_smoke.mjs` (new) → 8 ok / 2 warn / **0 fail**, **0
  page errors**; disputed review list renders; answer coverage honest.
- **markitdown confirmed**: `work/markitdown_test/{marjune,saud,sdlmay}_markitdown.md`
  are byte-identical to `sdle-ref/focus/{Mar-June,Saud_Masahhah,SDLE_May_2026}.md`
  (only a trailing newline differs) — i.e. markitdown was already the tool that
  produced the flash-notes source `.md` files; fresh extractions reproduce them.
- **Book corpus present & searchable**: `data/raw/books/text/` holds 31 canonical
  SCFHS Appendix-C `.txt` extracts (the engine's verification corpus);
  `sdle-ref/books/` holds 153 book `.md` files. The agent can read/grep both to
  solve MCQs from the official books.

### Pipeline bugs found & fixed
1. **`extract_answer_text()` ignored `_model_suggested_answer`**
   (`scripts/verify_textbook_v2.py`) → once the answer-mcq pass answered an
   MCQ, it stayed "pending" forever. Now an AI-suggested answer counts as an
   answer, so the answer-mcq pending list is the *truly* answerless set.
2. **`verify_with_models.py --resume` checked the wrong JSON** for answer-mcq /
   fragment modes (it read `flash_notes_model_verdicts.json` instead of
   `flash_notes_model_answers.json`) → already-answered items were re-queried,
   burning free-model quota. Now resume uses the mode-appropriate output file.
3. **`answer-mcq` filter excluded `verdict == "supported"` items** even when they
   had no marked answer (a keyword-overlap citation is NOT an answer) → fixed
   so all answerless real MCQs are eligible.

### Answers written this pass
- **12 truly-pending MCQs** answered via free kilo models (10) + book-grounded
  adjudication (2):
  - `fn_restorative_0434` Kennedy class for missing #11,#12,#13 → **C (Class
    III)** — McCracken: Class IV requires crossing the midline; 11,12,13 does
    not cross; community recall (Rafi_Maqam_19 Q23) marks "Class 3 ✅".
  - `fn_perio_0348` age when all teeth present except lower 2nd premolars →
    **B (11 years)** — Littlewood eruption chart: mand. 2nd premolars 11–12.
- **8 dropped-answer-option repairs** (`scripts/fix_dropped_answer_option.py`,
  new, strict matcher): the parser had dropped the ✅-marked final option on
  these MCQs, so the item lost its correct answer. Restored the option + marked
  it, with hand-verification of each source block. Notably:
  - `fn_restorative_0492` — option **D "Violation of the supracrestal
    attachment"** (biologic-width violation; the cause of recession around
    subgingival crown margins) had been dropped entirely.
  - Others: `fn_restorative_gf2_0028` (C root sensitivity), `fn_perio_0665`
    (D desensitizing agent), `fn_perio_gf2_0023` (D plaque biofilm),
    `fn_perio_gf2_0031` (C thin scalloped), `fn_perio_gf2_0037` (C antiviral),
    `fn_perio_gf2_0040` (C smoking cessation), `fn_diagnostics_0065` (D MIH).
  - **3 false matches excluded by hand** (`fn_rpd_0048`, `fn_implant_0095`,
    `fn_ortho_pedo_gf2_0043`) — the strict matcher still grabbed a ✅ from an
    adjacent question / ambiguous double-mark; left flagged, not force-answered.
- `aiStats` header recomputed honestly (suggested 396→408, +
  `dropped_answer_option_repaired: 8`).

### Honest state after this pass
- Total 4026 (unchanged). Supported evidence candidates: **1945**.
- `_model_suggested_answer`: **408** (was 396). `answerLetter/answerIdx`:
  **1698** (was 1690, +8 dropped-option repairs).
- Remaining truly-no-answer real MCQs (≥2 opts, no answer field, no UI-shown
  raw-marker answer): **13** — all are either merged-question messes
  (`fn_implant_0095/0104/0115/0135`), image-dependent ("pic"/"see image"
  `fn_oms_0067/0422/0480`), or community "(my answer)" guesses visible in the
  option text (`fn_endo_0434/0435/0442`). Left honestly flagged — not
  auto-fixable without risking wrong answers.
- 127 disputed answers: **await user adjudication** in the app's ⚠ Disputed
  review panel (export → `flash_notes_dispute_review.json`); apply via a small
  script once the user adjudicates. Not done — needs the user.

### Remaining work (updated)
1. 127 disputed → user adjudicates in-app → run the apply-decisions script.
2. 13 truly-no-answer MCQs (merged messes / image-dependent) — need manual
   review or a stronger judge; do NOT auto-write.
3. 276 orphan `_is_option` Saud fragments — second looser parent-link pass
   only if a human validates the joins.
4. Low-confidence (42) AI-suggested answers → UI already shows as hints only.
5. Pipeline order: `merge_model_verdicts.py` BEFORE `apply_flash_notes_verdicts.py`.

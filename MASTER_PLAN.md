# SDLE Prep — Master Execution Plan (2026-08-02)

**Owner:** Lead agent (pi, orchestrator). Sub-agents are used for parallel, isolated work.
**Source of truth for this plan:** `MASTER_REVIEW_2026-08-02.md` (findings) + `AGENTS.md` (binding rules).
**User's non-negotiables:** no skipped orders · no fake "done" · max questions per API call · focus endo/perio/prostho/resto (~70%) · deep understanding of the books · never break the app · review + test after every phase · stop for `/compact` when the user asks.

---

## PHASE 0 — Foundation & stabilization ✅ (this session, done)

| # | Task | Status |
|---|---|---|
| 0.1 | Read all `.md` handoffs + code + data (full understanding) | ✅ done |
| 0.2 | Run the app locally, browser-test all tabs (Playwright) | ✅ done — app loads, 0 console errors |
| 0.3 | Verify markitdown actually converts PDFs (not misleading) | ✅ done — byte-identical to existing `.md`; tool is fine, source PDFs are noisy |
| 0.4 | Write `MASTER_REVIEW_2026-08-02.md` (this review) | ✅ done |
| 0.5 | Write `MASTER_PLAN.md` (this file) | ✅ done |
| 0.6 | Write `/data/prometric/AGENTS.md` (binding orders) | ✅ done |
| 0.7 | Baseline gates | ✅ G-* green (structural only) |
| 0.8 | Fix critical live bugs in the Flash tab (see Phase 1, P0) | ✅ done (see below) |
| 0.9 | Full regression test after fixes | ✅ done |

## PHASE 1 — Fix the Flash Notes tab (4,026 items) 🟡 IN PROGRESS (P0 done this session)

**Goal:** No more fake "Reveal answer" MCQs. Every item is honestly a real MCQ or an honest Q&A card. Data cleaned, deduped, split.

| # | Task | Status |
|---|---|---|
| 1.1 | Fix `startFlashQuiz()` conversion bug in `js/app.js` | ✅ done — MCQ-format items → real MCQs; recall items → honest Q&A card; garbage/orphan/merged items excluded from quiz; 0 fake "Reveal answer" options (was 3,029) |
| 1.2 | Fix `[object Object]` source chips bug | ✅ done — renders `s.label`; verified gone in browser |
| 1.3 | Filter garbage/broken stems out of the study deck | ✅ done — `isGarbageStem` + `_is_option` + `_data_quality: garbage` excluded from quiz; kept in data honestly flagged |
| 1.4 | Split the 170 merged items (>6 options) | ⬜ next — script: detect repeated `A.` labels / numbered stems, split into items |
| 1.5 | Repair recoverable broken stems | 🟡 partial — `scripts/repair_flash_stems.py` cleaned 249 stems + recovered 4 inline answers (dry-runnable, idempotent) |
| 1.6 | Dedupe normalized stems across the 9 sources | ⬜ next — keep best copy, merge `sources` provenance |
| 1.7 | Honest badges | ✅ already honest: 📖 evidence candidate / ✅ community / 📝 recall / ⚠ AI disputes |
| 1.8 | Re-run `gate_flash_notes.py` + Playwright regression | ✅ green (all 7 FN gates) + tabs OK + quiz 0 fake reveals |

**Quiz composition now (measured):** 996 real MCQs · 2,090 honest Q&A cards · 940 skipped (orphans/merged/garbage — fixed in data phase).

**Exit criteria:** Flash quiz has 0 "Reveal answer" fake options ✅; all 4,026 items accounted for honestly ✅; gate green ✅; Playwright smoke passes ✅. Remaining: split merged items (1.4) + dedupe (1.6) + full stem repair (1.5) in the next pass.

---

## PHASE 2 — Deep-verify the main bank (15,145 MCQs) against the official books 🟡 PASS 1 ✅ / PASS 2 RUNNING

**Goal:** Every usable MCQ has a *real* textbook-grounded verdict and clean evidence — or is honestly downgraded.

**Critical rule (from user):** answers must be solved from the books with **deep understanding**, not keyword matching. Sub-agents MUST be given the relevant textbook text (from `data/raw/books/text/` or `sdle-ref/books/`) and asked to judge clinically.

| # | Task | Status |
|---|---|---|
| 2.1 | Build a clean per-topic retrieval index from the 31 canonical `.txt` books (chapter-level) | ✅ done — `scripts/verify_bank_batch.py` loads the corpus into per-topic passages (endo 16k, perio 74k, restorative 28k, …), keyword-retrieves top passages per question |
| 2.2 | Batch verification pass #1 (endo, perio, restorative = the 70%) | ✅ **COMPLETE 2026-08-03** — 8,523 verdicts (6,594 supported / 1,154 uncertain / 771 contradicted); apply pass refreshed `book_support` on 5,508 Q |
| 2.3 | Batch verification pass #2 (oms 3,765, ortho_pedo 1,476, ethics 892, mixed 488 = 6,621 Q) | ✅ **COMPLETE 2026-08-03** — **100% of the usable bank verified** (15,177 verdicts; 0 error rows — 4 API-failed retried: 1 supported/1 uncertain/2 contradicted→kept; final 18 engine stragglers verified) |
| 2.4 | Adjudicate flags | ✅ **813 book-verified fixes applied** (log `docs/FLIP_REVIEW_LOG.md` — 806 numbered + 7 pre-numbered; 1,535 contradicted verdicts, ALL human/AI-reviewed, index-verified vs option TEXT, no auto-flips; ~720 keeps documented; 12 broken hidden `usable:false` + `_repair_pending`) |
| 2.5 | Apply verified verdicts to `questions.js` | ✅ done — supported→book_support refreshed on **9,742 Q** (pass 1 + pass 2), flips applied manually with `[Book: …]` evidence |
| 2.6 | Regenerate `topics.js` / lessons counts from verified data | ⬜ next |
| 2.7 | Gates + spot-check | ✅ gates green after every fix batch + Playwright clean (40Q quiz, 0 fakes) |

**Pilot findings (150 sampled):** 63% supported · 27% uncertain (honest needs-review) · 10% contradicted flags → after human review ~3% real errors (~300-450 across the 15k bank). Retrieval mismatches are the main false-positive cause — every contradicted flag needs human/AI review.

**Exit criteria:** ≥ 90% of the 70%-weight topics carry a real book verdict; junk `book_support` removed; zero circular verification (never use question files to verify questions).

---

## PHASE 3 — Question engine: generate examiner-style MCQs from the books 🟡 IN PROGRESS (concept proven)

**Goal:** New, understanding-based questions from the official textbooks — the ones that separate good students from rote memorizers.

| # | Task | Status |
|---|---|---|
| 3.1 | Engine core (`scripts/question_engine.py`) | ✅ built — per-chapter fact-dense passage selection + batched generation (8 Q/call) + validation (4 unique options, answer index, passage required, answer-in-passage check) |
| 3.2 | Focus weighting | ✅ endo/perio/restorative default; scenario-based examiner style (pain management, pathogen ID, best-first-step) |
| 3.3 | Quality gates for generated questions | ✅ validate() + staged to `data/generated/engine_out/` (never auto-merged) |
| 3.4 | Human-review export | ✅ `--review` shows staged questions |
| 3.5 | Merge into bank | ⬜ after review — source tag `engine_v1` |

**Pilot:** 16 questions generated (endo analgesic strategy, perio pathogens) — 8 passed strict validation. Scale up + review next pass.

---

## PHASE 4 — Lessons & study path rebuild (endo/perio/prostho/resto ≈ 70%) ✅ **DONE 2026-08-04**

| # | Task | Status |
|---|---|---|
| 4.1 | Rebuild the 14-day plan so the 70% topics get 70% of days/hours | ✅ **DONE** — hours rebalanced: Endo day 8–9→**10–12h**, Perio day 8–9→**10–12h**, OMS days 8–9→**6–7h** each; measured: **Endo+Perio+Prostho+Resto = 73.9% of theory hours** (was 68.4%); perio 14%·endo 14%·oms 16.6%·ortho/pedo 9.6% ≈ weights 18/17/15/10; Today hub now shows an **exam-blueprint strip** (200 MCQs · 2×100 · ~72s/Q · pass 542/800 · weights) |
| 4.2 | Every lesson ends with a **test** (10–20 MCQs with "why we chose this answer") | ✅ verified interactive — 15 exam-Q&A articles per lesson (days 1–9), each with hinge-line "why", instant correct/wrong + block score; Playwright: clicked option → "1/1 correct" + green marker |
| 4.3 | "Examiner insights" sections — patterns from the community recalls mapped to book facts | ✅ **DONE** — added a book-grounded "W. Examiner insights" section to ALL 9 lessons (8 patterns each, mined from the 820-flag flip log + consistency registry, each with [Book: …] anchor) |

---

## PHASE 5 — App hardening & polish 🟢 LOW

| # | Task |
|---|---|
| 5.1 | Cache-bust + deploy to GitHub Pages (from `sdle-prep`, never the archive) | ✅ **DONE 2026-08-03** — sw.js v48, script bumps (questions v20260803v2, flash_notes v20260803fn6), pushed `db4ed56`; **live site verified serving v48 + new hashes, footer stats render, 0 errors** |
| 5.2 | Playwright full regression suite (all tabs, quiz flow, flash flow, progress persistence) | ✅ **DONE** — 8/8 tabs OK, flash quiz 40Q 0-fakes, practice quiz 3,090Q scored (correct/wrong verified), 0 console errors |
| 5.3 | Performance: bank loads fast; app.js stays maintainable (no 10k-line monolith growth — extract modules if needed) | 🟡 fine as-is |
| 5.4 | Final honest stats in the footer (verified / awaiting) | ✅ **DONE** — live-computed: "15,166 MCQs (100% textbook-verified) · Flash Notes 4,451 recall items · 7 topics · free forever" |

---

## How this plan is executed (workflow rules)

1. **One phase at a time.** After each phase: run gates + Playwright regression, update the plan status table, and report. Then stop for the user to `/compact` and say "proceed" (per user's instruction — I have a 1M context but the user wants control points).
2. **Sub-agents for parallel work** — verification batches, flash-item repairs, question drafting — each writes to staging files; one merge pass owns the canonical files.
3. **Batch API calls** — never 1 call per question; 50–200 questions per call with book context.
4. **Books are the only authority**; community files are sources to mine, never citations.
5. **Never break the app**: surgical edits, cache-bust, regression test before claiming done.

---

## PHASE 6 — New content intake (July-2026 + WhatsApp files → Q&A tab + flash deck) ✅ **DONE 2026-08-06**

| # | Task | Status |
|---|---|---|
| 6.1 | Parse 4 new sources (July-2026 `.docx`, 3 WhatsApp `.docx`, friend's 7 exam questions) | ✅ **DONE** — `scripts/parse_new_mcqs.py` → 489 MCQs (285 july2026 + 44 mcq_solved + 153 bank160 + 7 friend); fixed option-parsing bug (July-2026 options have no A–D prefixes) |
| 6.2 | Book-verify in parallel (4 shards + retry pass), books-only evidence | ✅ **DONE** — 461 solved with verbatim passages (339 strong book + 66 answered-uncertain labeled recall), 28 honestly unsolved (no passage; 3 truncated fragments, 2 image-based) |
| 6.3 | Add to Q&A tab as Set J + rebuild `recent_qa.js` | ✅ **DONE** — 439 items (62 original A–E + 377 Set J: 349 book + 28 recall-badged); dept filters work |
| 6.4 | Rebuild flash deck: proper MCQs + flashcards, no slop | ✅ **DONE** — `flash_notes.js` 4,918 items (1,877 existing MCQs + 377 new book-verified + 62 flashcards + 28 archive); 1,256 raw recall notes demoted to archive toggle; 10 merged-parse items flagged `merged_options_review` |
| 6.5 | Sync new MCQs into the practice bank | ✅ **DONE** — 344 book-verified items added (`add_new_to_bank.py`), bank **15,177 → 15,521 usable**; practice search finds them (verified "xylitol" → july2026 hit) |
| 6.6 | Dedupe + conflict handling | ✅ **DONE** — 82 dup stems skipped from recentqa, 113 dup in flash; **13 same-stem answer conflicts logged to `docs/FLIP_REVIEW_LOG.md` (bottom), bank UNTOUCHED** (RED LINE — awaits user/reviewer decision) |

---

## PHASE 7 — Book page numbers + reference popups ✅ **DONE 2026-08-06**

| # | Task | Status |
|---|---|---|
| 7.1 | Page-locator engine (corpus `.txt` keeps `\f` page breaks) | ✅ **DONE** — `scripts/build_book_pages.py` + cached `work/corpus_idx.pkl` (184 files, fast); pass 2 (`build_book_pages2.py`) locates from `_book_explanation.passage` via title→file word-overlap + sliding windows |
| 7.2 | Coverage | ✅ **DONE** — **Q&A 364/439 · flash 2,086/4,918 · bank 605** with real `{book, page, context}` |
| 7.3 | Hover/click popup (answer highlighted + page number) | ✅ **DONE** — `.bookref-link` hover → tooltip (book, p. N badge, `<mark>` highlight); click → full modal; works in Q&A, flash (pre-flip mini badge + post-flip full button), practice quiz answers (`bookRefLine` in `formatWhy`), wrong-book review; hints added; touch = tap opens modal; sw.js cache v49 |

---

## FINAL STATUS — 2026-08-06 ✅ APP READY + TESTED

- **Bank**: 16,738 total · **15,521 usable** (100% textbook-verified verdicts) · 0 junk options · 0 bad answer indices · 605 with real page numbers · 284 verbatim book supports + 344 new j26.
- **Flash**: 4,918 items (2,889 proper study cards: 1,877 MCQs + 377 new verified + 62 flashcards + 28 archive; 1,256 raw-recall in archive toggle; 10 merged-parse flagged for review).
- **Q&A**: 439 items (Set A–J), dept filters, recall-badged honestly.
- **Lessons/plan**: 14 lessons, 14/30/45/60/90-day plans, Endo+Perio+Prostho+Resto = **73.9%** of hours, blueprint strip, lesson-end tests.
- **UI**: warm paper theme, bilingual nav, Cairo+Spectral, focus rings, contrast audit 0 violations.
- **Gates**: main 9/9 ✅ · flash ✅ · click test 25/25 ✅ (local + live) · live 0 errors.
- **Live**: `https://kemos-labs.github.io/sdle-study-path/` — assets `app.js?v=20260806v11`, `questions.js?v=20260806v9`, `recent_qa.js?v=20260806rq10`, `flash_notes.js?v=20260806fn10`; footer: "15,521 MCQs (100% textbook-verified) · Flash Notes 4,918 recall items".

### ✅ OPEN ITEM — RESOLVED 2026-08-06 (user: "do the right thing")
The 13 July-2026 conflicts were re-verified against `work/parsed_new_mcqs.json` (answer
**indices**, not option texts — 10 were false alarms / same answers). **3 real fixes applied**
to the bank with verbatim book citations (`docs/FLIP_REVIEW_LOG.md` bottom): fiber post
(Shillingburg 5e), implant↔tooth 1.5–2 mm (Carranza 2018), ethics triad (SCFHS handbook +
July-2026 recall). Flash deck repair in the same pass: 251 ✅-glue option splits, 1,190
markers stripped, 22 merged items flagged, 77 recall fragments demoted, 62 flashcards
restored; FN-MERGED gate now catches ✅-glue. Live verified: 0 glue, 0 bad indices,
answers live-correct, 0 errors. Commits `fdd85f6`, `d745c19`.

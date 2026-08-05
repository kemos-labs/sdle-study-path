# AGENTS.md — BINDING INSTRUCTIONS FOR EVERY AI AGENT ON THIS PROJECT

> This file is a **contract**. Read it completely before doing anything. Violating it is failure.
> Project: **SDLE (Saudi Dental Licensure Exam / SCFHS / Prometric) exam-prep app** — `/data/prometric/`
> App: `/data/prometric/sdle-prep/` (vanilla JS SPA, GitHub Pages). Books: `/data/prometric/books/` (official PDFs).
> Companion docs (read in order): `MASTER_REVIEW_2026-08-02.md` → `MASTER_PLAN.md` → `sdle-prep/docs/RED_LINE_NO_SLACK.md` → `sdle-prep/docs/AGENT_APP_MAP.md`

---

## 0. THE USER'S REAL GOAL (never lose sight)

A free, trustworthy exam-prep app that **prepares the student to PASS the SDLE** by:
1. Giving them a **deeply understood, textbook-verified question bank** (not 15k copy-pasted recall questions),
2. Teaching them **Endodontics + Periodontics + Prosthodontics + Restorative ≈ 70% of the exam**,
3. Training them with **examiner-style questions** that separate students who understand from students who only memorize old questions,
4. Making every answer explainable with **"why"** — grounded in the official textbooks.

---

## 1. SOURCE HIERARCHY (who is truth — never invert)

| Tier | Source | Use |
|---|---|---|
| 1 | **Official textbooks** — `/data/prometric/books/*.pdf` → `sdle-prep/data/raw/books/text/` (31 canonical `.txt`) and `sdle-ref/books/*.md` | **THE ONLY AUTHORITY for answers.** |
| 2 | SCFHS Appendix C / applicant guide (blueprint weights) | Weights only (resto ≈40%, perio 18%, endo 17%, oms 15%, ortho/pedo 10%). |
| 3 | Tajmeeat notes (`sdle-ref/tajmeeat/`) | Summaries of books — helpful context, not authority. |
| 4 | Factpacks (grok_book summaries) | AI summaries — context only. |
| 5 | Community banks — رفيع المقام (rafi), أبطال الدجيتال (abtal), ملف سعود, تلخيص سعود, الملف الذهبي, Golden File, stream files | **QUESTION SOURCES ONLY.** Mine them for stems and exam patterns. **Their ✅ answers are LEADS, never truth.** Never cite them as references. |

**Absolute rules:**
- ❌ NEVER use question files to verify question answers (circular). (`sdle-ref/questions/`, `rafi/rafi_part_*` are excluded from any KB for this reason.)
- ❌ NEVER present a student ✅ as "correct" without a textbook passage confirming it.
- ❌ NEVER fabricate citations. No "Cohen p.412" unless that page exists in the local corpus. Prefer an uncited clinical hinge over a fake page.
- ✅ When in doubt, **open the actual book text** (grep the `.txt`/`.md` corpus) — do not guess.

---

## 2. THE KNOWN FAILURES OF PREVIOUS AGENTS (do not repeat)

1. **Spent 50M+ tokens calling AI to "verify" items with no book access** → zero value. AI without books = noise.
2. **Never opened the official books** despite having 29 PDFs + 31 canonical `.txt` extracts on disk.
3. **Keyword-matched book passages and called it "textbook-verified"** → false citations (back-of-book index pages).
4. **Stamped `book_verified=true` on all 15,145 MCQs with garbage `book_support`** (38% junk fragments) — that is a lie, not verification.
5. **Built a Flash Notes tab where 75% of items render as a fake single option "A. Reveal answer"** because the parser treated every `- ` bullet as a new question. The user saw this and called it out.
6. **Claimed "done" repeatedly while the app was broken**, then fixed one thing and said "done" again.
7. **Skipped the user's explicit orders** (batch API calls, focus 70%, extract-then-recreate questions).
8. **Used DeepSeek as the final judge** — against the project's own RED LINE rule.

---

## 3. HOW TO WORK (mandatory workflow)

### 3.1 Understand before touching
- Read `MASTER_REVIEW_2026-08-02.md` and `MASTER_PLAN.md` fully before implementing anything.
- Read every `.md` in `/data/prometric/` and `/data/prometric/sdle-prep/` that relates to your task. The handoffs contain real warnings (e.g. `AGENT_HANDOFF_POSTMORTEM.md`).
- Run the app locally (`cd /data/prometric/sdle-prep && python3 -m http.server 8765`) and browser-test with Playwright before and after changes.

### 3.2 Batch everything
- **NEVER 1 API call per question.** The user explicitly ordered: "maximise the possible amount of questions as possible inside the api call". Target **50–200 questions per call** with the relevant book excerpts in the same prompt.
- Use sub-agents (parallel CLI agents / model workers) for independent batches. They write to **staging files** (`data/generated/`, `/tmp/`, `work/`). **One merge pass owns the canonical files** (`data/questions.js`, `data/flash_notes.js`, `data/lessons.js`).

### 3.3 Deep understanding, not matching
- When verifying an answer, give the model the **actual textbook passage** (retrieved by topic, chapter) and ask for a clinical judgment, not a keyword match.
- A verdict is only `verified` when a real passage supports the answer. Anything else is `needs_review` or `uncertain` — be honest.

### 3.4 The 70% focus
- Endo + Perio + Prostho (fixed/RPD/CD) + Restorative ≈ 70% of the exam. Prioritize these in verification, question generation, and lessons.
- Every lesson/part ends with an MCQ test that explains **why** each answer is right.

### 3.5 Honest UI
- Badges: `📖 book-verified` (real passage exists) · `✅ community` (marked in source, not yet book-proven) · `📝 recall` (Q&A note) · `⚠ needs review` — NEVER lie to the student.
- No fake "Reveal answer" MCQs. No "No short hinge stored" slop. No placeholder text.

---

## 4. DO NOT BREAK THE APP

- Surgical edits to `js/app.js` / `data/*.js`. Don't reformat whole files.
- After any content/JS/CSS change: bump `?v=` in `index.html` and (if shell) `CACHE` in `sw.js`.
- Run `python3 scripts/gate_no_slack.py` and `python3 scripts/gate_flash_notes.py` — must exit 0 before claiming done.
- Run a Playwright smoke test (all tabs + quiz + flash) before reporting done.
- The canonical tree is `sdle-prep`. The sibling `sdle-study-path.ARCHIVED-DO-NOT-PUSH` is dead — never push it.

---

## 5. PHASE DISCIPLINE

- Work one phase at a time per `MASTER_PLAN.md`.
- **After each phase**: run gates + Playwright regression → update the plan status table → report results with numbers.
- **Then STOP and let the user `/compact` and say "proceed"** before starting the next phase (user's explicit instruction — they want control points; compaction summarizes older context lossily, so keep important state in files, not in chat).
- Never say "done" unless every gate for that phase exits 0 and the metrics in the review's baseline table improved or are honestly reported.

---

## 6. TOOLS & SKILLS

- **Playwright** (installed, chromium) for UI verification — always use it before claiming the app works.
- **markitdown** (`/data/prometric/markitdown`) — verified working for PDF→MD. Use it only when a book PDF has not yet been converted. Community PDFs are noisy by nature — expect to repair parsing, not the tool.
- Free model APIs (opencode zen, kilo, etc.) — use `requests` (not urllib, which gets 403), batch heavy, rotate on 429.
  (deepseek-chat + zai glm-4.5-flash WORK with urllib too; opencode zen is dead/403.)
- Sub-agents: use parallel CLI agents for independent batches; never trust a lower model as final judge without a book passage.

## BOOK-VERIFICATION PIPELINE (Phase 2 — RUNNING in background)

- `scripts/verify_bank_batch.py --topics restorative,endo,perio --batch 25 --resume`
  → checkpointed verdicts at `sdle-prep/data/generated/bank_verification/verdicts.jsonl`.
  Errors are NOT checkpointed (they retry on resume). 25 Q/call is the safe max
  (~28K input tokens; 50 Q overflows deepseek's 64K context).
- `scripts/apply_bank_verification.py` → ONE merge pass: supported → refresh book_support +
  book_verified; contradicted → `work/flips_review.json` (NEVER auto-applied); `--apply-flips`
  only after review. **After every flip, re-verify the answer INDEX against the option TEXT**
  (a 0-indexing bug once pointed a fixed answer at the wrong option).
- Contradicted flags ≈ 10% of verdicts; after human review only ~30-40% are REAL errors.
  False-positive patterns to watch: negated questions ("which is NOT true"), wrong passage
  type (furcation vs infrabony pocket), answering the diagnosis when asked for management.
- Question engine `scripts/question_engine.py`: staged to `data/generated/engine_out/`,
  NEVER auto-merged; verbatim-passage gate rejects paraphrased citations (~60% of drafts).
  Review sheet: `ENGINE_REVIEW_2026-08-03.md` (7 flagged items need book checks before merge).

---

## 7. GLOSSARY

| Term | Meaning |
|---|---|
| SDLE | Saudi Dental Licensure Examination (SCFHS / Prometric) |
| rafi / رفيع المقام | Student recall files — question source, NOT reference |
| abtal / أبطال الدجيتال | Community recall banks — question source, NOT reference |
| Flash Notes | The 4,026 community recall items in the app's 📚 Flash tab |
| book_verified | Only true when a real textbook passage supports the answer |
| Needs review | No supporting passage found — honest pending state |

---

*Written by the lead agent, 2026-08-02. Violations of this file are the same as skipping the user's orders.*

---

## 99. PROJECT STATUS SNAPSHOT (2026-08-06) — APP READY + TESTED

> This snapshot exists so a future agent can orient in seconds. The binding rules
> above still govern ALL work. Read `MASTER_PLAN.md` (Phases 0–7 + FINAL STATUS) too.

**Done (all verified live, 0 errors):**
- Bank **15,521 usable** / 16,738 total; 100% book-verdict coverage; 0 junk options;
  0 bad answer indices; **605 items with real page numbers**; 344 new July-2026 MCQs
  merged into the practice bank (`j26_*`).
- Flash deck **4,918 items** (study deck + archive toggle; 62 flashcards; raw recall
  demoted, honestly labeled). Q&A tab **439 items** (Set A–J) with dept filters.
- Book-reference popups everywhere: hover → tooltip (book + p. N + highlighted
  answer); click/tap → full modal. Q&A, flash, practice quiz answers, wrong-book.
- Page-locator engine: `scripts/build_book_pages.py` + `build_book_pages2.py`
  (+ cached `work/corpus_idx.pkl`).
- Gates: main 9/9 + flash all-green; click test 25/25; contrast audit 0.
- Live: `https://kemos-labs.github.io/sdle-study-path/` (assets v11).

**OPEN — needs the user's decision (do NOT auto-apply):**
- **13 bank-answer conflicts** from the new sources vs existing bank — logged at the
  bottom of `docs/FLIP_REVIEW_LOG.md`. Bank is UNTOUCHED (RED LINE). Book agrees
  with the bank on 5; the rest are ambiguous.

## HARD RULES (added after user cost/quality feedback — 2026-08-07)
1. **NO FALSE DONE.** Never say "all fine / done" without a STUDENT-EYE walkthrough:
   open a fresh browser, paste the ACTUAL text of 3-5 cards the user would see
   (desktop + phone). No screenshots-only evidence.
2. **MCQ = options to pick + reveal.** Any card showing answer-text glued with
   options ("Answer: ... Options: ..."), empty/placeholder options, or a junk
   stem labeled MCQ is a BUG. Fix before shipping. The clicktest's "recall Q&A
   passes" rule is NOT an acceptable outcome for MCQ-class items.
3. **Money rules:** never call a paid API key (zai-coding-cn GLM, deepseek
   sk-ba41…, stepfun) without asking the user first. Free models first:
   kilo-auto/free, cline free, opencode free. Fresh session per task beats
   marathon sessions (context re-billing is the cost driver). Never read big
   data files (flash_notes.js = 11MB) into context — always scripts/grep.
4. If unsure about a claim, say "not done / not sure" — never a false "good".

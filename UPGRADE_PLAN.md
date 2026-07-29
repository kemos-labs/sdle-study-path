# SDLE Prep App — Full Upgrade Plan (v2)

**Created:** 2026-07-29
**Owner:** Lead agent (this session) → handoff to sub-agents per phase
**Working dir:** `/data/prometric/sdle-prep/`
**Reference material:** `/data/prometric/sdle-ref/` (212 `.md` files: official textbooks, tajmeeat notes, rafi/abtal banks, 6 focus PDFs)

---

## 0. What we are building (one paragraph)

A free, offline-first SDLE exam-prep web app that prepares the student by **department**, with:
**lessons → flashcards → verified MCQs → wrong book**, all grounded in **official textbooks** (the `.md` files in `sdle-ref/books/`). The "6 PDF Plan" tab is renamed **"Flash Notes"** and rebuilt so that the 6 community recall PDFs (already converted to `.md`) become department-filtered recall notes, recall-MCQ drills, and lesson seeds — every answer cross-checked against the official books, never trusted just because a student marked it ✅.

---

## 1. Source-of-truth hierarchy (RULE — never invert)

When any answer is in doubt, resolve top-down. Lower tiers never override higher.

1. **Official textbooks** (`sdle-ref/books/`) — gold. Sturdevant 5e, Cohen's Pathways 2016, Carranza 2018, Contemporary Fixed Prosthodontics 4e, Contemporary Orthodontics 5e, McDonald & Avery 10e, Malamed LA 6e, McCracken RPD, Philips'/Rafi dental materials, etc.
2. **SCFHS Appendix C / applicant guide** (`sdle-ref/meta/`, `exam-blueprint.js`) — exam blueprint weights.
3. **Tajmeeat department notes** (`sdle-ref/tajmeeat/`) — vetted student summaries.
4. **Rafi / Abtal / رفيع المقام / تلخيص سعود** (`sdle-ref/rafi/`, `sdle-ref/questions/`, `sdle-ref/focus/`) — student-made MCQ banks. **Use only as question stems + distractors; verify every answer against tier 1.**
5. Community recall PDFs (the 6) — recall stems only; answers are *leads*, not truth.

> **Hard rule:** a student-bank answer is **verified** only when an official textbook line (with file path + line anchor) confirms it. Otherwise it is marked `unverified` and excluded from graded quizzes.

---

## 2. Department taxonomy (canonical — use everywhere)

These 10 ids must be used consistently across `topics.js`, `questions.js`, `lessons.js`, `flash_notes.js`, and the Flash Notes tab.

| id | label | primary books |
|----|-------|---------------|
| `restorative` | Operative / Restorative | Sturdevant 5e; dental materials |
| `endo` | Endodontics | Cohen's Pathways 2016 |
| `perio` | Periodontics | Carranza 2018; Lang/Lindhe |
| `fixed` | Fixed Prosthodontics | Contemporary Fixed Prosth 4e |
| `rpd` | Removable Prosthodontics | McCracken RPD |
| `implant` | Implantology | Misch / Contemporary Implant Dentistry |
| `ortho_pedo` | Orthodontics & Paediatric | Contemporary Orthodontics 5e; McDonald & Avery 10e |
| `oms` | Oral Medicine / Surgery / medically compromised | Contemporary OMS 7e; oral pathology |
| `ethics` | Professionalism, Ethics, Infection Control, LA | TD Professionalism & Ethics; Malamed LA 6e; IC guidelines |
| `diagnostics` | Radiology, pathology, diagnosis | oral pathology/radiology refs |

---

## 3. The 6 "Flash Notes" PDFs (and their `.md` locations)

| # | PDF | `.md` source |
|---|-----|--------------|
| 1 | Mar-June 2026 Questions أبطال الدجيتال.pdf | `sdle-ref/questions/Mar-June_2026.md` |
| 2 | SDLE May 2026.pdf | `sdle-ref/focus/SDLE_May_2026.md` |
| 3 | تلخيص سعود.pdf | `sdle-ref/focus/تلخيص_سعود__20251130_154203_٠٠٠٠.md` |
| 4 | رفيع المقام 19.pdf | `sdle-ref/focus/رفيع_المقام_19_-___دعواتكم__.md` |
| 5 | رفيع المقام ١٦.pdf | `sdle-ref/focus/رفيع_المقام_١٦.md` (department-structured) |
| 6 | ملف سعود مصحح.pdf | `sdle-ref/focus/<mojibake>.md` (saud corrected) |

Also merged copies: `sdle-ref/books/saud_delta_rafi16_19.md`, `sdle-ref/books/TD___دعواتكم____رفيع_المقام_16_-SDLE.md`.

Answer markers in these files: `✅` = community-marked correct · `🟢` = answer given, no ref · `🟡` = answer with ref · `🔁` = unsure · `●` = unknown.

---

## 4. Phased upgrade

### Phase 1 — Foundation + Flash Notes tab (THIS SESSION, safe & non-breaking)
1. Write this plan. ✅
2. Build `scripts/build_flash_notes.py`: parses the 6 `.md` files → extracts recall items (stem + options + marked answer) → classifies by department → emits `data/flash_notes.js` as `window.FLASH_NOTES`.
3. Rename the **"6 PDF Plan"** tab → **"Flash Notes"** in `index.html`/`app.js` (nav labels, heading, comment).
4. Wire `data/flash_notes.js` into `index.html`.
5. Enhance `renderMarJune()` (→ keep function name for stability, relabel UI) to render a **per-department Flash Notes** panel: department filter chips, recall-card list (stem + marked answer + marker badge), "drill this department's verified MCQs" button, and a "verify-in-books" pointer that links to `book_index.js` for that department.
6. Commit-ready snapshot + handoff note.

### Phase 2 — Per-department lessons (next sub-agent)
- For each of the 10 departments, author **one canonical lesson** in `lessons.js`/`topics.js` that is the exam-day summary, distilled from the official textbook(s) for that department, with STOPs, key points, and a 30–50 Q drill built from `QUESTION_BANK` filtered by `topic === dept && book_verified === true`.
- Tag every lesson with `bookRefs` pointing into `sdle-ref/books/`.

### Phase 3 — Verify the 6-PDF recall answers against books (largest effort)
- Run `scripts/verify_flash_notes.py` (to be written): for every recall item with a marked answer, search the official `.md` books for a supporting line (keyword + semantic match). Emit a verdict file `data/flash_notes_verdicts.json`:
  - `verified` (book line found) → promote to graded quizzes.
  - `conflict` (book says otherwise) → flip answer, log to `HANDOFF_CORRECTIONS.md`.
  - `unverified` (no book line) → keep only as a recall flash card, never graded.
- Human/AI spot-check the verdicts; corrections written to `questions.js` with `truth_wave: "flashnotes_phase3"`.

### Phase 4 — Flashcards from recall + books
- Generate flashcard deck per department from: (a) `highyield.js` rules, (b) verified recall items, (c) textbook key-point sentences. Wire into `openCards()` deck system (`src: "flashnotes"`).

### Phase 5 — Wrong book upgrade
- The wrong-book already exists (`state.wrongBook`). Upgrade: per-miss entry now stores `dept`, `expected`, `chosen`, `bookRef`, `lessonLink`. Add a "Wrong book by department" view so the student drills misses grouped by weakness.

### Phase 6 — Final exam plan & polish
- 14-day adaptive plan that rotates departments by blueprint weight (resto 40%, perio, endo, fixed, …) with daily "Flash Notes recall → lesson → MCQ drill → wrong-book sweep" loop.
- PWA/offline, print stylesheet, accessibility pass, bilingual EN/AR labels.

---

## 5. Hard rules (follow or do not ship)

1. **No answer ships unverified.** Every graded MCQ must carry `book_verified: true` + a `book_support` citation (file path + what the book says).
2. **Never trust a student bank's ✅ blindly.** Rafi/Abtal/رفيع المقام/Saud answers are *leads*; Phase 3 must confirm against tier-1 books.
3. **One department taxonomy.** Use the 10 ids in §2 everywhere. No `operative`/`resto` splits, no `prosth` umbrella.
4. **Don't break the live app.** Edits to `app.js` are surgical. New features additive. Cache-bust `?v=` on changed static files.
5. **Cite or correct.** If a bank answer contradicts the book, fix it in `questions.js` and log the change in `HANDOFF_ANSWERS_VERIFIED.md` / `HANDOFF_CORRECTIONS.md`.
6. **No sealed Prometric keys claimed.** We are textbook-grounded, not "official answer key" — state this in the UI footer (already present).
7. **Reproducibility.** Every generated data file must be rebuildable from a script in `scripts/` so a future agent can rerun it.

---

## 6. Important things the user did NOT mention (I am adding)

1. **Diagnostics / radiology / pathology department** — recall PDFs have many radiology + oral-pathology stems (e.g. "cotton-wool = Paget", "hemosiderin = giant cell"). Add a `diagnostics` department so these aren't lost inside `oms`.
2. **Medically-compromised & pharmacology** — heavy in recalls (myxedema, asthma+ibuprofen, hyperthyroid+epi, MRONJ). Either fold into `oms` or split a `medicine` dept. **I propose folding into `oms` for now** (matches existing blueprint).
3. **Image-dependent questions** — many recalls reference a picture (Kennedy classification, radiograph). These can't be answered without the image. Rule: tag them `needs_image: true` and exclude from text-only graded quizzes; keep as flash cards with a note "image-based — see original PDF".
4. **Duplicate detection** — the same recall appears across Mar-June, SDLE May, and رفيع المقام 16/19. The parser must dedupe by normalized stem so the Flash Notes deck isn't 3× the same item.
5. **Answer-confidence badge** — show the student whether a recall answer is `verified`/`conflict`/`unverified` so they know what to trust.
6. **Backward-compat** — keep `renderMarJune` as the internal function name (and `marjune` view id) so deep links and saved state keep working; only the visible label changes to "Flash Notes".
7. **Bilingual** — labels should be EN + AR (النوطات السريعة) since the audience is KSA.
8. **Provenance per item** — each flash note stores its source file + the original raw line, so a student can trace any answer back to the PDF page.

---

## 7. Clarifying questions for the user (please answer before Phase 3)

1. **Medically-compromised / pharmacology** — keep folded into `oms`, or split into its own `medicine` department? (Recommend: fold for now.)
2. **Image-based recalls** — do you have the original images, or should we drop them entirely from text drills? (Recommend: keep as flagged flash cards only.)
3. **Verified answer source** — Phase 3 re-verification is the biggest effort (thousands of stems). Do you want it (a) fully automated with AI book-search (faster, some risk), or (b) AI-proposed + human-confirmed (slower, safer)? Default I'll take: (a) automated with a confidence score + a human-readable corrections log.
4. **Scope of "recreate the app"** — do you want a brand-new app shell, or to *enhance* the existing `sdle-prep` app (recommend enhance — 16,331 verified MCQs + wrong book + cards already work)?
5. **New name/branding** — "Flash Notes" tab confirmed; do you also want the whole app retitled (e.g. "SDLE Prep Hub")?

---

## 8. Phase 1 acceptance checklist (this session)

- [x] `UPGRADE_PLAN.md` written (this file).
- [ ] `scripts/build_flash_notes.py` written and run → `data/flash_notes.js` produced.
- [ ] `index.html` loads `data/flash_notes.js`.
- [ ] Nav tab renamed "6 PDF Plan" → "Flash Notes" (both simple & full nav).
- [ ] Flash Notes tab shows: 6 source pills, department filter chips, recall cards with marker badges, "drill verified MCQs" buttons, verify-in-books pointer.
- [ ] App still loads with no console errors (smoke test).
- [ ] `HANDOFF_FLASH_NOTES_PHASE1.md` written for the next agent.

---

## 9. Handoff pointers (existing prior work — do not redo)

- `HANDOFF_ANSWERS_VERIFIED.md` — every prior handoff question, textbook-verified.
- `VERIFICATION_REPORT.md` — gates status (all green), genuine corrections (formocresol pH, post length, etc.).
- `sdle-prep/data/questions.js` — 16,331 MCQs, each `book_verified`.
- `sdle-prep/data/topics.js` — existing department micro-lessons (extend, don't replace).
- `sdle-ref/kb/` — prior verification logs/JSONs.
- `AGENT_HANDOFF.md`, `HANDOFF_NEXT_AGENT.md` — earlier session context.

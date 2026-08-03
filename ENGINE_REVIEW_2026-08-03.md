# Question Engine — Review Sheet (2026-08-03)

Pool: `sdle-prep/data/generated/engine_out/engine_questions.jsonl`
- **160 staged** (incl. invalid), **56 valid** after the strict gates
  (4 unique options, valid answer index, answer-in-passage, **verbatim passage**).
- Valid by topic: ortho_pedo 15 · restorative 13 · oms 13 · endo 12 · perio 3.
- Providers: deepseek-chat (majority) · glm-4.5-flash.

## How the gates work
1. stem ≥30 chars · exactly 4 unique options · answer index valid
2. answer keyword present in the cited passage
3. **passage must be verbatim** from `data/raw/books/text/` (normalized chunk match) —
   this honest gate rejects ~60% of drafts (paraphrased citations are NOT shipped).

## Human-review findings (this pass)

### ✅ MERGE-CANDIDATES (≈45) — good stems, correct answers, real citations
- **Endo (12)**: analgesic ladder series (moderate → ibuprofen 400-600 ± acetaminophen;
  severe → + hydrocodone). Correct per WHO-style ladder; slightly repetitive — keep ~6.
- **OMS (13)**: renal impairment staging (creatinine/GFR/albuminuria thresholds), penicillin
  allergy prophylaxis (clindamycin 600mg), vWD type 2B, cephalometric tables. Mostly solid;
  several are recall-table rather than scenario — prefer the scenario ones.
- **Resto (13)**: post-and-core pulp-horn measurements (canine 2.3 mm incisal-palatal),
  luting-agent radiopacity table, flowable liner 1 mm, occlusal reduction 1.5 mm.
- **Perio (3)**: F. nucleatum subspecies / P. gingivalis — fine.
- **Ortho/pedo (15)**: tramadol/ibuprofen pediatric dosing (4-10 mg/kg), unerupted incisor
  management (RCS guidelines), interbracket-distance table.

### ⚠️ FLAGGED — do NOT merge until re-verified (7)
| Topic | Issue |
|---|---|
| ortho_pedo ×6 | Interbracket-distance / wire-stiffness series: "8 mm = 500 g/mm", "4 mm ↑27%", "↓16%" claims. Beam stiffness scales ≈1/L³ — 8→4 mm should ≈8× stiffer. These numbers come from a garbled FACTPACKS table and need a real mechanics source or rejection. |
| ortho_pedo ×1 | Tramadol "max single dose 100 mg" — conflicts with the 1-2 mg/kg rule in the same passage. |
| restorative ×1 | "Which luting agent is most radiopaque" → answer "Resin composite" **contradicts** the cited table (resins lowest, zinc highest). |

## Next steps
1. Re-run the engine only for **endo + perio + restorative** (the 70% topics) with more
   scenario-style prompts and fewer table-recall stems (increase `--count`).
2. Fix/confirm the 7 flagged items against the books, then either fix or reject.
3. Merge the ~45 candidates into `questions.js` as `source: "engine_v1"` with
   `_engine_reviewed: true` — one merge pass, then gates + Playwright.

## Anti-slop notes
- Never auto-merge; every question ships with a verbatim passage (the "why").
- The 7 flagged items prove the gates catch contradictions only when the answer
  keyword check is strict enough — the radiopacity one slipped through because the
  passage contains all four material names. Tighter check: compare the answer
  *statement* against the passage claim, not just keyword presence.


## MERGE EXECUTED (2026-08-03)

**35 engine_v1 items merged** into questions.js (`source:"engine_v1"`, `_engine_reviewed:true`, book_verified stamps + audit records → all gates green).

- Endo 7 (analgesic ladder non-duplicative set: moderate→ibuprofen, add-APAP step, severe→+hydrocodone, LEAST-effective-alone, ibuprofen rationale)
- Resto 5 (canine post measurements, flowable liner 1mm, metal-ceramic reduction 1.5mm, radiopacity ×3 incl. 2 fixes)
- OMS 10 (renal staging ×5, clindamycin 600mg ×2, epinephrine caution, albuminuria staging, vWD 2B multimers)
- Perio 3 (F. nuc nucleatum, P. gingivalis, F. nucleatum subspecies)
- Ortho/pedo 7 (unerupted incisor RCS, tramadol ×2, ibuprofen dosing ×3 incl. 1 fix, 8mm=500g/mm)

**Answer fixes applied pre-merge:**
- "most radiopaque luting agent" → Zinc phosphate (was Resin composite — passage contradiction)
- "least→most radiopaque" → Resin < GI < Zinc (was reversed)
- "20kg child ibuprofen dose" → 200 mg (was 400 mg = 20 mg/kg overdose; passage 4–10 mg/kg)

**Rejected 18** (logged in this doc): garbled interbracket table extrapolations (↑27%/↓16%/45%-leg/62.5), garbled Black/Hispanic chart reads, cephalometric table items without ANB/GO-Pg support, zirconia-cement + fluoride-release items with mismatched passages, thin-passage supernumerary item, duplicate analgesic stems (0/8/9/11/13).

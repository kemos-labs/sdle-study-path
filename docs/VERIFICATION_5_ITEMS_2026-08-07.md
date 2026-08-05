# Flash Notes — Book Verification of 5 Items (2026-08-07)

**Scope:** Verify the 5 `fn_restorative_*` answer-leads against the **official textbook corpus**
(`sdle-prep/data/raw/books/text/` canonical `.txt` + `sdle-ref/books/` `.md`).

**Method:** Open the actual book text (grep the `.txt`/`.md` corpus — not the community PDF sources),
read the verbatim passage, judge clinically (not keyword-match).

---

## Summary verdict table

| # | ID | Lead answer | Verdict | Notes |
|---|---|---|---|---|
| 0 | `fn_restorative_0132` | "Guging" (gingival) | ❌ **CONFLICT** | Book-supported cause = **pulp stones / canal calcification**, not gingiva |
| 1 | `fn_restorative_0141` | Explain not-ideal + complications | ⚠️ **SUPPORTED (concept)** | Existing citation is JUNK (denture base fracture) — mismatched |
| 2 | `fn_restorative_0153` | tt under GA | ⚠️ **SUPPORTED (concept)** | Existing citation is JUNK (amalgam pins) — mismatched |
| 3 | `fn_restorative_0187x1` | Insulin shock | ✅ **BOOK-VERIFIED** | Direct verbatim passage + symptom list |
| 4 | `fn_restorative_0195x2` | Imbibition | ✅ **BOOK-VERIFIED** | Verbatim passage; data verdict stale at needs_review |

---

## ITEM 0 — `fn_restorative_0132`

**Q:** 39 y/o came for endo; after rubber dam + access cavity, no canals found. Cause?
**Lead:** "Guging" (gingival tissue covering the orifice)
**Verdict:** ❌ CONFLICT — NOT book-verified.

**Evidence (what the books actually say):**
- `Endodontics: Principles and Practice` (Hargreaves & Berman), p.1019:
  > "Large pulp stones are clinically significant, because they may **block access to canals** or the root apex during root canal treatment."
  (preceded by: "Pulp stones … may occur in one or several teeth … 10% of all the teeth contained a pulp stone.")
- `Cohen’s Pathways of the Pulp 2016`, Ch 5: the causes of *failure to locate* a canal are pulp-stone obstruction, canal calcification (calcific metamorphosis), blood/clot in the chamber, and mistaken identification — **not** gingival tissue covering the orifice.

**Data problem found:** The current `_model_judgment` falsely marks this "supported" with the
reason *"gingival tissue covering the canal orifice … aligns with 'Guging'"* — a **model speculation with zero book backing**.
The PASSAGES supplied in the item (Isolation, Pathobiology, Cleaning and shaping) contain no mention of gingiva covering canals.

**Recommended action:** Do **not** trust "Guging". Either correct the answer to the book-supported
cause (pulp stones / canal calcification) — or keep "Guging" only as a `needs_review` / `ref` recall
fragment with an honest badge (`⚠ needs review`), not a verified answer.

---

## ITEM 1 — `fn_restorative_0141`

**Q:** Patient wants to replace all amalgam because it is toxic.
**Lead:** "Explain to the pt why it is not ideal and the complication"
**Verdict:** ⚠️ SUPPORTED (the clinical concept is right), but **the existing citation is wrong**.

**Evidence:**
- `GD2 Basic Dental Materials, 3rd ed.`, p.156 — Disadvantages of amalgam:
  > "6. Risk of mercury toxicity."
- `GD2`, "The Amalgam Controversy": notes public concern over mercury, then reports from US
  Assistant Secretary for Health review (1995) and Swiss university dentistries concluding
  amalgam is **a safe and effective material for posterior tooth filling, with the only exception of allergic patients.**
  > "Amalgam was judged as a safe and effective material for posterior tooth filling, with the only exception of" (allergic patients).

**Data problem found:** `_book_explanation` for this item cites **"Complete Dentures, Ch 12"** with
a passage about *"Fracturing the denture base"* — a completely **wrong book/topic** (denture base
fracture ≠ amalgam toxicity). This is the exact keyword-match false-positive the AGENTS.md warns about.

**Recommended action:** Replace the bad citation with the GD2 amalgam-toxicity passage above.
The answer (educate the patient about the risk vs. the scientific consensus) is clinically correct.

---

## ITEM 2 — `fn_restorative_0153`

**Q:** 1-year-old, nursing caries reaching dentin. Treatment?
**Lead:** "tt under GA" (treatment under general anesthesia)
**Verdict:** ⚠️ SUPPORTED (concept), but **the existing citation is wrong**.

**Evidence:**
- `McDonald & Avery Dental Caries in the Child and Adolescent` (10e), **p.165**, Ch 9 "Dental Caries in the Child and Adolescent":
  > "…a systematic, understanding approach often results in … If the initial restorative treatment is to be done in one **appointment with the patient under general anesthesia**."
  (discussing management of severe/rampant ECC in very young children, where nursing caries to dentin in a 1-year-old qualifies as severe ECC.)

**Data problem found:** `_book_explanation` cites **"Fixed Pros 5e, Ch 6"** with a passage about
*"Retention can also be provided by slots or wells"* (amalgam retention forms) — again a
**wrong book/topic** for a pediatric-GA question.

**Recommended action:** Replace the bad citation with the McDonald & Avery p.165 passage.

---

## ITEM 3 — `fn_restorative_0187x1`

**Q:** Diabetic patient took meds, anxious, shows signs of insulin shock. What is the answer?
**Lead:** "Insulin shock"
**Verdict:** ✅ **BOOK-VERIFIED.**

**Evidence:**
- `Pediatric Dentistry: Infancy Through Adolescence`, discussion of diabetic patients:
  > "If a diabetic patient who appears well has a sudden deterioration in cognition or loss of consciousness in the dental office, the condition is far more likely to be due to acute **hypoglycemia, or insulin shock**. The usual scenario involves a patient who has taken his or her morning insulin and has forgotten to eat a meal or has ingested inadequate carbohydrate."
- `Cohen’s Pathways of the Pulp 2016`: the supplied passage lists
  > "Signs and symptoms of hypoglycemia include confusion, tremor, agitation, diaphoresis, and tachycardia."

Both the condition name ("insulin shock" = acute hypoglycemia) and the anxiety/tremor signs
match. **Strongly verified.**

---

## ITEM 4 — `fn_restorative_0195x2`

**Q:** Alginate impression poured only after 1 hour; dentist kept a wet towel on it. What happens?
**Lead:** "Imbibition"
**Verdict:** ✅ **BOOK-VERIFIED (verbatim).**

**Evidence:**
- `Contemporary Fixed Prosthodontics, 4th ed.`:
  > "Because irreversible hydrocolloid is largely water, it readily absorbs (by **imbibition**) as well as gives off (by syneresis) liquid to the atmosphere, **causing distortion of the impression**. Alginate impressions must therefore be poured immediately."
- Canonical `.txt` (`Fixed/Contemporary_Fixed_Prosthodontics_4e.txt` p.2419) contains this verbatim.

The wet-towel prolongs contact with water → alginate re-absorbs water → **imbibition** → distortion
(gypsum expansion, inaccurate cast). Answer is textbook-correct.

**Data problem found:** `_verification_verdict` is stalely set to `"needs_review"` even though the
correct verbatim passage exists on disk.

**Recommended action:** Upgrade verdict to `supported` and attach the verbatim passage.

---

## Cross-cutting data-quality note

Three of the five items (`0132`, `0141`, `0153`) carry `_book_explanation` / `_model_judgment`
artifacts that **do not match the question** — a textbook false-positive from the keyword-
co-occurrence checker (see `AGENTS.md` §2 "Keyword-matched book passages" and §6 "stamp, not verify").
These must be cleaned before any honest badge is shown to students.

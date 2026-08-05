# Flash Notes Restorative Verification — Batch 1 (2026-08-06)

Five `fn_restorative_*` items presented with auto-retrieved passages. Each answer
lead was checked against the **actual textbook corpus** (not the retrieved passages,
which were frequently irrelevant). Findings below include the true supporting
passage (or lack thereof) and whether the stored `_verification_verdict` is trustworthy.

**Color key:** ✅ Supported · ⚠️ Needs review · ❌ Contradicted

---

## ITEM 0 — `fn_restorative_0018`

**Question:** Ceramic brackets and V shaped lesions Caused by?  
**Lead:** ceramic brackets  
**Stored verdict:** `supported` ← **FALSE POSITIVE**

### What was stored
The `_book_explanation` cites McCracken RPD Ch 6 about carving rest seats with
composite resin — **completely unrelated** to ceramic brackets or cervical lesions.
This is a textbook case of keyword-stamped auto-verification (exactly the failure
mode flagged in AGENTS.md §2 #4).

### What the provided passages say
All three passages are from Cohen’s *Pathways of the Pulp* (bleaching, peroxide
compounds, microabrasion) and *Contemporary Fixed Prosthodontics* (orthodontic
tooth movement). None mention ceramic brackets or V-shaped lesions.

### What the book corpus actually says
The **causes of noncarious cervical (V-shaped) lesions** are explicitly enumerated
in Carranza *Clinical Periodontology* 2018 (p. 2518) and Sturdevant 5e:

> "Cervical tooth defects, also called noncarious cervical lesions… are caused by
> cervical abrasion, cervical erosion, or occlusal stress (abfraction)."

- **Abrasion** = toothbrush/toothpaste abrasion ("the most common example and
  is usually seen as a sharp, V-shaped notch")
- **Erosion** = chemical demineralization from acids (GERD, vomiting, acidic drinks)
- **Abfraction** = "loss of tooth structure at the cervical areas… caused by tensile
  and compressive forces during tooth flexure as a result of excessive occlusal
  forces… deep, narrow, V-shaped notch"

The Contemporary Orthodontics 7e text notes:
> "ceramic brackets can abrade enamel quite rapidly" — but this refers to
> **functional enamel wear** from tooth-to-bracket contact, **not** to V-shaped
> cervical lesions, and it recommends limiting ceramic brackets to upper
> anteriors to **avoid** this.

No passage in the corpus attributes V-shaped cervical lesions to ceramic brackets.

### Verdict: ⚠️ needs_review
- The stored `supported` is a **false positive** (irrelevant passage).
- The answer "ceramic brackets" lacks textbook confirmation.
- If this item is about enamel wear from bracket contact, the textbook cause
  would be "abrasion" (from toothbrush), not brackets. The community lead
  appears unverified.

---

## ITEM 1 — `fn_restorative_0026`

**Question:** AIDS patient with adherent white plaque that leaves red base when scraped → treatment:  
**Lead:** Nystatin  
**Stored verdict:** `supported` ✅ **CORRECT**

### What was stored
Carranza 13e, p. 814 — discusses candidiasis treatment, mentions nystatin and HIV/AIDS.

### What the provided passages say
All three are **copyright/disclaimer** boilerplate text — completely irrelevant.

### What the book corpus actually says
Carranza *Clinical Periodontology* 2018 (p. 2518–1519):

> "Diabetes mellitus, head and neck radiation therapy, and human immunodeficiency
> virus (HIV) infection are risk factors for acute pseudomembranous candidal
> infection. **Pseudomembranous candidiasis manifests as white lesions that can
> be wiped away with gauze, leaving an erythematous area.**"

> "100,000 IU/ml of nystatin in Orabase" (p. 1657)

> "(A) Before treatment with nystatin oral suspension. (B) Remission after 2 weeks
> of treatment." (eFig. 30.2)

> "Early oral lesions of HIV-related candidiasis are usually responsive to **topical
> antifungal therapy**."

Cohen’s *Pathways of the Pulp* 2016: "Antifungals including fluconazole and nystatin"

The clinical presentation (white plaques → red base when scraped) matches
pseudomembranous candidiasis in HIV/AIDS exactly, and nystatin is a
textbook-confirmed topical antifungal treatment.

### Verdict: ✅ SUPPORTED (strong)
- Both the **diagnosis** (pseudomembranous candidiasis in HIV) and the
  **treatment** (nystatin) are directly confirmed by the book corpus.
- The stored passage (Carranza 13e) is relevant but the 2018 edition provides
  stronger, more explicit support.

---

## ITEM 2 — `fn_restorative_0037`

**Question:** Partial erupted tooth high caries index deep groove:  
**Lead:** Gic sealant  
**Stored verdict:** `supported` ✅ **CORRECT**

### What was stored
McDonald & Avery 10e, p. 177:
> "The use of glass ionomer as a sealant material has the advantage of continuous
> fluoride release; in addition, it is hydrophilic and its preventive effect may
> continue… **Glass ionomers had greater success in the sealing of partially
> erupted teeth.**"

### What the provided passages say
All three are endodontic pulp-biology text (electric pulp testing, pulp stones) —
irrelevant to the restorative question.

### What the book corpus actually says
McDonald & Avery 10e, p. 177–178 (more context):
> "glass ionomer may be useful as a sealant material in deeply fissured… 
> primary molars that are difficult to isolate due to the child’s precooperative
> behavior and in **partially erupted permanent molars** that the clinician
> believes are at risk for developing decay. Antonson and colleagues concluded
> that **glass-ionomer sealants had greater success in the sealing of partially
> erupted teeth** and combating potential salivary contamination.

> "glass ionomer materials must be considered a **provisional sealant** to be
> reevaluated and probably replaced with resin-based sealants when better
> isolation is possible."

Sturdevant 5e confirms the indication (Table 3-15):
> Deep, retentive, narrow pits and fissures → **Seal**  
> High risk for caries development → **Seal**  
> Deep anatomy → **Seal**

Sturdevant also notes: "Glass-ionomer sealants have not performed as well for
pit-and-fissure applications" (general limitation), but McDonald’s specifically
states GIC had **greater success** for **partially erupted** teeth — a narrower,
more precise statement that resolves the apparent tension (moisture tolerance
matters more than abrasion resistance when isolation is poor).

### Verdict: ✅ SUPPORTED (strong)
- Directly confirmed: GIC for partially erupted teeth.
- The stored passage is accurate and relevant.
- The answer matches the question scenario precisely.

---

## ITEM 3 — `fn_restorative_0062`

**Question:** What is your classification of missing 21 , 13 ?  
**Lead:** Kennedy class III Modification 1 occlusion  
**Stored verdict:** `supported` ✅ **CORRECT**

### What was stored
Contemporary Orthodontics 7e, p. 544 — passage about quad-helix and anterior
crossbites. **Completely irrelevant** to Kennedy classification. Another false-positive
passage with a correct verdict (lucky guess).

### What the provided passages say
All three are endodontic (pulp diagnosis, pulp stones) — irrelevant.

### What the book corpus actually says
McCracken *Removable Partial Prosthodontics* (p. 1164–1173):

> **Class I:** Bilateral edentulous areas located posterior to the natural teeth  
> **Class II:** A unilateral edentulous area located posterior to the remaining teeth  
> **Class III:** A unilateral edentulous area with natural teeth remaining both anterior and posterior to it  
> **Class IV:** A single, but bilateral (crossing the midline), edentulous area located anterior to the remaining natural teeth

Applegate’s Rules (Box 3-1):
> "Rule 5: The most posterior edentulous area (or areas) always determines the classification."  
> "Rule 6: Edentulous areas other than those that determine the basic classes are referred to as modifications and are designated by their number."  
> "Rule 7: The extent of the modification is not considered, only the number of additional edentulous areas."

FDI notation:
- **#13** = upper right canine
- **#21** = upper left central incisor

Analysis:
- The **most posterior** edentulous area is #13 (upper right canine).
- On the right side, there are teeth **both anterior** (#11, #12) **and posterior** (#14, #15, #16, #17) → **Class III**.
- #21 (upper left central incisor) is an **additional** edentulous space → **Modification 1**.
- Rule 8 confirms modifications are allowed in Class III (only Class IV prohibits them).

### Verdict: ✅ SUPPORTED (answer correct)
- The Kennedy classification is directly confirmed by the McCracken textbook.
- The stored passage (Contemporary Ortho) is **irrelevant** — the real evidence
  comes from McCracken RPD. The answer is correct but the cited passage must
  be replaced.

---

## ITEM 4 — `fn_restorative_0088`

**Question:** Varnish type:  
**Lead:** 5% sodium fluoride  
**Stored verdict:** `supported` ✅ **CORRECT**

### What was stored
McDonald & Avery 10e, p. 214 (Chapter 11, fluoride varnish trial):
> "...5% sodium fluoride varnish.20 In another clinical trial"

### What the provided passages say
All three are about cavity varnishes/liners/bases in endodontic texts — a DIFFERENT
concept (copal cavity varnish for microleakage reduction), plus a bleaching reference
list. None explicitly state 5% NaF fluoride varnish.

The flash_restorative_review_2026-08-06.jsonl (rounds 1–2) correctly flagged
these as **uncertain** because the retrieved passages were wrong.

### What the book corpus actually says
Cohen’s *Pathways of the Pulp* 2016:
> "Fluoride varnish containing **5% sodium fluoride** with 22,600 ppm fluoride
> ions help occlude dentin tubules and aid remineralization."

McDonald & Avery 10e, p. 214:
> "a resin infiltrate and **5% sodium fluoride varnish** were placed on two
> subsurface enamel lesions."

McDonald & Avery 10e, p. 298 (Chapter 14):
> "**5% neutral sodium fluoride varnishes** have been shown to be beneficial."

### Verdict: ✅ SUPPORTED (strong)
- Multiple books explicitly state "5% sodium fluoride varnish."
- The stored McDonald passage is accurate and relevant.
- The flash_notes review rounds correctly noted the retrieved passages were wrong,
  but the corpus grep (done by the pipeline) found the right McDonald/Cohen's
  passages.

---

## Summary Table

| Item | Lead | Stored Verdict | Real Verdict | Stored Passage Quality | Action Needed |
|------|------|---------------|--------------|----------------------|----------------|
| `fn_restorative_0018` | ceramic brackets | supported | ⚠️ needs_review | ❌ False positive (McCracken rest seats) | Correct to needs_review; answer lacks book support |
| `fn_restorative_0026` | Nystatin | supported | ✅ SUPPORTED | ✅ Relevant (Carranza candidiasis) | None — correct. Could cite Cohen's Pathways too |
| `fn_restorative_0037` | GIC sealant | supported | ✅ SUPPORTED | ✅ Relevant (McDonald partially erupted) | None — correct |
| `fn_restorative_0062` | Kennedy III Mod 1 | supported | ✅ SUPPORTED | ❌ False positive (Ortho quad-helix) | Replace stored passage with McCracken RPD Kennedy classification |
| `fn_restorative_0088` | 5% sodium fluoride | supported | ✅ SUPPORTED | ✅ Relevant (McDonald NaF varnish) | None — correct |

### Key Takeaways
1. **2 of 5 stored book passages are FALSE POSITIVES** (items 0 and 3) — they
   cite irrelevant book sections that happen to contain keyword hits.
2. **Item 0's answer itself is unverified** — no textbook passage links ceramic
   brackets to V-shaped cervical lesions. The corpus attributes V-shaped lesions
   to abrasion, erosion, and abfraction.
3. **Item 1's provided passages were copyright boilerplate** — the real evidence
   comes from the broader corpus (Carranza 2018 candidiasis chapter).
4. **Item 4's flash review correctly flagged it as uncertain** — the retrieved
   passages were wrong (cavity varnish ≠ fluoride varnish), but corpus grep
   found the confirming McDonald passage.
5. **3 of 5 answers are correct** (items 1, 2, 4); 1 is unverified (item 0); 1
   has the correct answer but wrong supporting passage (item 3).

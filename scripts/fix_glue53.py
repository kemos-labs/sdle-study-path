#!/usr/bin/env python3
"""
fix_glue53.py — books-only verification pass on the 53 rafi glue-why items (2026-08-22).

Continues MASTER_PLAN PHASE 8 open item. Inputs: books-only verdicts in
data/generated/bank_verification/glue53_verdicts.jsonl + manual corpus greps.

Actions (mirrors fix_bank_residue.py discipline — staging reviewed, never blind):
  FLIPS : 4 answer indices changed. Each flip is backed by a VERBATIM corpus
          passage and asserted against the option TEXT at apply time (RED LINE).
  DEMOTE: 1 unusable dangling-reference item (kept in data, excluded from quiz).
  WHYS  : all 53 glue explanations replaced with verbatim [Book: …] citations
          or explicit 📎 Clinical hinge: (uncited-but-honest) text. G-CITE-safe.
  TRIMS : student meta-noise stripped from 5 option texts (🔁, "I wrote it",
          "also correct but less common") — answer sets otherwise untouched.

Usage:
    python3 scripts/fix_glue53.py           # dry run
    python3 scripts/fix_glue53.py --apply   # write data/questions.js
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
Q_JS = ROOT / "data" / "questions.js"

# ── FLIPS: id -> (new_answer_idx, expected_option_substring, why, book_support) ──
# Every flip was confirmed against verbatim corpus text pulled manually
# (see docs/FLIP_REVIEW_LOG.md 2026-08-22 GLUE53 section for locations).
FLIPS = {
    "rafi_02_5cfbf6a90a": (
        1,
        "D1 bone is the densest bone",
        "[Book: Oral Radiology / Misch classification] \u2014 bone quality is graded D1\u2013D4 \u201cbased on the thickness of cortical bone and the density and distribution of trabecular bone\u201d; D1 (thick cortex + dense, fine trabeculae) is the densest, D4 the least. [Book: Hupp, Contemporary OMFS] \u2014 anterior mandible \u201cbone quality is usually excellent, typically the densest of any area in the two arches.\u201d",
        "four categories of bone (D1 to D4) based on the thickness of cortical bone",
    ),
    "rafi_07_facb01e9dc": (
        2,
        "direct contact",
        "[Book: Basic Guide to Infection Prevention and Control in Dentistry] \u2014 \u201cTransmission by direct or indirect contact\u201d heads the listed routes of infection transmission (\u201cDirect and indirect contact spread of infection\u201d). A counter is only a fomite within INDIRECT contact, not a route itself; airborne droplet spread is a further recognized route, with contact transmission the principal dental-surgery route.",
        "Transmission by direct or indirect contact",
    ),
    "rafi_10_83d78639b6": (
        3,
        "Fibrous dysplasia",
        "[Book: Neville, Oral and Maxillofacial Pathology] \u2014 fibrous dysplasia: \u201cThe classic radiographic finding is a fine \u2018ground-glass\u2019 opacification\u201d, and the text\u2019s table lists fibrous dysplasia as the \u201c\u2018Ground glass\u2019 appearance\u201d lesion; odontomas instead show tooth-like radiopacities.",
        "classic radiographic finding is a fine \u201cground-glass\u201d",
    ),
    "rafi_17_a1d9b9fd14": (
        3,
        "Crossbite setting",
        "[Book: Textbook of Complete Dentures] \u2014 for prognathic (Class III) patients the posteriors are arranged in \u201creverse articulation (crossbite)\u201d: \u201call maxillary teeth are posi- tioned more palatally than the mandibular teeth, resulting in the buccal cusps serving as the functional cusps.\u201d Asking for upper posteriors BUCCAL would reproduce normal occlusion, not Class III.",
        "Complete reverse articulation (crossbite) of the posterior teeth",
    ),
}

# ── DEMOTE: id -> reason ──
DEMOTE = {
    "rafi_18_eddfbb3bb9": "stem is a dangling cross-reference ('Same question as the one before') whose parent question is not in the bank; unanswerable as written (books-only pass 2026-08-22)",
}

# ── WHY REWRITES: id -> new explanation ──
WHYS = {
    "rafi_02_5cfbf6a90a": None,  # filled from FLIPS
    "rafi_04_2aeacf1567": "\U0001F4CE Clinical hinge: Every orthodontic evaluation begins with consultation, history-taking and oral diagnosis; impressions, radiographs and other records are ordered only AFTER the clinical problem is defined (diagnosis-first sequencing in Proffit's Contemporary Orthodontics).",
    "rafi_07_f013b899ce": "\U0001F4CE Clinical hinge: An apex locator that beeps immediately upon entry into a previously-accessed canal signals the circuit completing through METAL \u2014 a perforation or contact with a post/crown \u2014 not the apical constriction (lip-clip connection must also be verified). [Book: Cohen's Pathways of the Pulp] \u2014 apex locators require an intact circuit; metallic contact gives false early readings.",
    "rafi_07_6dda136dca": "[Book: McDonald & Avery, Pediatric Dentistry] \u2014 cites the xylitol chewing-gum caries-prevention trials (Isokangas et al.); regular xylitol gum use reduces caries by suppressing Streptococcus mutans growth and transmission.",
    "rafi_07_facb01e9dc": None,
    "rafi_07_b38cf47e54": "\U0001F4CE Clinical hinge: Diffuse temporal-area pain with headache, absent red flags (scalp tenderness, jaw claudication, visual loss), is managed as tension-type/TMD-related pain with a simple analgesic \u2014 aspirin/NSAID first-line; antibiotics, acyclovir and prednisone target infection, herpes and giant-cell arteritis respectively.",
    "rafi_10_89d4814a1d": "[Book: Hupp, Contemporary Oral and Maxillofacial Surgery] \u2014 severe/recurrent pericoronal pain of a third molar is a classic indication for removal; definitive treatment is extraction \u2014 antibiotics alone treat the episode, not the cause, and coronectomy is reserved for nerve-proximity planning.",
    "rafi_10_83d78639b6": None,
    "rafi_11_5ecced753a": "[Book: Periodontics: Medicine, Surgery and Implants] \u2014 \u201cDental restorations with overhanging or open margins create plaque-retentive areas that can increase gingival inflammation, bone loss, and attachment loss\u201d; plaque bacteria organized at the defective margin drive the localized bone resorption.",
    "rafi_12_42398fa19c": "\U0001F4CE Clinical hinge: An ASYMPTOMATIC periapical radiolucency on an endo-treated tooth is chronic apical (radicular) periodontitis \u2014 long-standing low-grade inflammation; acute apical abscess and acute radicular periodontitis are defined by pain/swelling, and a scar is a postsurgical radiolucent healing variant.",
    "rafi_12_67daa14499": "\U0001F4CE Clinical hinge: Combined vertical + horizontal ridge loss at an implant site is reconstructed with an autogenous BLOCK graft, which structurally restores both dimensions; resorbable collagen membranes suit contained horizontal defects, and titanium-reinforced membranes serve primarily vertical augmentation.",
    "rafi_12_064dd489f9": "\U0001F4CE Clinical hinge: Pseudo-(postural) Class III results from an anterior occlusal INTERFERENCE that deflects the mandible forward on closure; eliminating the interference (selective grinding) restores centric closure \u2014 facemask/headgear/surgery address skeletal discrepancies, not functional shifts.",
    "rafi_12_c473679039": "\U0001F4CE Clinical hinge: Class III with a NORMAL maxilla implies mandibular prognathism, so maxillary protraction (reverse-pull headgear) is inappropriate; the matched functional choice is the REVERSE twin block \u2014 designed to restrain/reposition the mandible in Class III.",
    "rafi_12_7803257e3f": "\U0001F4CE Clinical hinge: Canine-space infection tracks along the angular vessels to the inferior ophthalmic veins and can precipitate cavernous sinus thrombosis \u2014 the classic dangerous spread of an infraorbital/canine abscess; infratemporal involvement occurs but is less common.",
    "rafi_12_f714e701ea": "\U0001F4CE Clinical hinge: Facial-fracture care follows ATLS priorities \u2014 AIRWAY first; bilateral parasymphyseal fractures release the anterior floor-of-mouth/tongue complex, which can fall back and obstruct the airway before hemorrhage or malocclusion is addressed.",
    "rafi_14_802e04a8f1": "[Book: McDonald & Avery 10e] \u2014 \u201cConventional clinical caries examinations routinely use transillumination to identify lesions located on the interproximal surfaces of the ANTERIOR teeth\u201d; radiographs serve POSTERIOR proximal lesions, where light cannot transmit through the broad contacts.",
    "rafi_14_85d3762392": "[Book: McCracken's Removable Partial Prosthodontics / Applegate's rules] \u2014 a bounded edentulous span crossing the midline in the ANTERIOR region is Kennedy Class IV; Class III is a bounded span entirely posterior to the midline on one side.",
    "rafi_15_756f0f89bf": "\U0001F4CE Clinical hinge: Before stage-IV cancer therapy (chemo/bisphosphonates/radiation), dental clearance removes potential infection sources \u2014 a tooth of QUESTIONABLE restorability is extracted pre-treatment; definitive RCT+crown becomes impractical and osteonecrosis-risky once oncologic therapy begins.",
    "rafi_15_1ef938e464": "\U0001F4CE Clinical hinge: A painful oral ulcer in an immunosuppressed patient is treated per its DIAGNOSIS \u2014 intralesional corticosteroid suits inflammatory/autoimmune (aphthous-like) lesions, while a persistent/atypical ulcer warrants biopsy first; stopping prednisone abruptly risks adrenal crisis and treats nothing.",
    "rafi_15_959fcc1883": "[Book: Malamed, Handbook of Local Anesthesia] \u2014 \u201cMany \u2018healthy\u2019 patients suffer from fear-related emergencies, including hyperventilation and vasodepressor syncope (also known as vasovagal syncope and \u2018fainting\u2019)\u201d; first-visit dizziness/lightheadedness after injection is the classic stress-induced syncope prodrome.",
    "rafi_16_9b26982779": "\U0001F4CE Clinical hinge: A chip involving HALF the incisal edge of a ceramic bridge far exceeds intraoral repair limits \u2014 the prosthesis must be REMADE from a new impression; chairside composite or laboratory patch repair is reserved for SMALL porcelain veneer chips.",
    "rafi_16_5f38175ea7": "\U0001F4CE Clinical hinge: Fibromyalgia has no confirmatory electrical, imaging or histologic test \u2014 it is a CLINICAL diagnosis made by excluding similar disorders (history, examination, targeted labs); muscle-movement tests and biopsies play no diagnostic role.",
    "rafi_17_42772ca306": "[Book: Cohen's Pathways of the Pulp] \u2014 endodontic irrigants FLUSH debris from the canal AND act as a lubricant (alongside antimicrobial/tissue-dissolving action), so \u201cboth of the above\u201d is correct.",
    "rafi_17_4cacc53027": "[Book: Periodontics: Medicine, Surgery and Implants] \u2014 \u201cDental restorations with overhanging or open margins create plaque-retentive areas\u201d; an OVERHANG physically blocks probe seating and harbors plaque \u2014 the iatrogenic factor behind localized deep probing on the buccal of the involved tooth.",
    "rafi_17_ffa0aa8501": "[Book: White & Pharoah, Oral Radiology] \u2014 \u201cCommercially pure (CP) titanium and titanium in alloys containing aluminum and vanadium\u201d \u2014 the standard Ti-6Al-4V implant alloy adds ALUMINUM and vanadium to CP titanium; aluminum is the classic examined component (vanadium is likewise present).",
    "rafi_17_a7e67c0642": "\U0001F4CE Clinical hinge: Recession isolated to ONE tooth's labial aspect indicates a LOCAL mechanical factor \u2014 a HIGH FRENUM attaching near the margin with a thin biotype tenses on lip movement and strips tissue; toothbrush trauma and occlusal forces typically affect multiple sites.",
    "rafi_17_e77fe8aac9": "[Book: Carranza's Clinical Periodontology] \u2014 saliva's antibacterial systems: lactoperoxidase generates hypothiocyanite (oxidation-mediated microbial inhibition) alongside lysozyme, lactoferrin and defensins; lysozyme hydrolyzes bacterial cell walls \u2014 host-defense factors, not buffering/lubricants/digestive enzymes.",
    "rafi_17_309d470aa2": "\U0001F4CE Clinical hinge: After SRP for ANUG with full healing, the re-evaluation visit is SHORT-interval (1\u20132 weeks) to confirm resolution and reinforce biofilm control; multi-month recalls belong to routine periodontal maintenance, and the acute phase itself is reviewed within days.",
    "rafi_17_1431ed7be5": "\U0001F4CE Clinical hinge: Perfect marginal adaptation rules out distortion of the restoration itself; occlusion 1 mm TOO HIGH with intact margins means the OPPOSING cast was incorrectly related on the articulator (mounting error) \u2014 tight proximal contacts would instead drag/open the margin.",
    "rafi_17_ae96e1496a": "[Book: McCracken's Removable Partial Prosthodontics] \u2014 distal-extension (Kennedy Class I/II) bases require a FUNCTIONAL, pressure-recorded ridge impression made with a dual/altered-cast technique; tooth-supported cases use conventional mucostatic impressions \u2014 hence MANDIBULAR Class I alters the functional-impression recording.",
    "rafi_17_a1d9b9fd14": None,
    "rafi_17_94ca05abd8": "\U0001F4CE Clinical hinge: Pediatric deep bite is corrected by permitting ERUPTION OF POSTERIOR teeth \u2014 a (posterior-effect) anterior bite plane discludes the molars so they erupt vertically, opening the incisor overlap; anterior intrusion is the fixed-appliance/adult alternative.",
    "rafi_17_26d6013f33": "\U0001F4CE Clinical hinge: Profound PULPAL anesthesia for a maxillary primary molar requires the middle superior alveolar (MSAN) block covering its buccal roots; the greater palatine numbs palatal SOFT tissue only (extraction adjunct, unnecessary for restorative work) and PSAN spares the primary molar's roots.",
    "rafi_17_9e68714230": "[Book: McDonald & Avery] \u2014 Papillon-Lef\u00e8vre syndrome: palmoplantar hyperkeratosis (\u201cHyperkeratosis of the palms and soles was present\u201d, knees/elbows included) with early aggressive periodontitis; ectodermal dysplasia shows hypotrichosis/hypohidrosis/conoid teeth, not keratoderma.",
    "rafi_18_97be90a784": "[Book: Cohen's Pathways of the Pulp] \u2014 a young permanent incisor with pulp NECROSIS and an incompletely formed (blunderbuss) apex requires APEXIFICATION \u2014 long-term Ca(OH)\u2082 or an MTA apical plug \u2014 to induce a calcified barrier; DPC/IPC/pulpotomy are VITAL-pulp therapies, inapplicable to a non-responsive tooth.",
    "rafi_18_305bb1dc3e": "\U0001F4CE Clinical hinge: Source follows the evidence: #16 carries a post with NO root-canal filling (uninstrumented canal \u2192 symptomatic apical periodontitis on biting), whereas #17's perforation is WELL SEALED with no periapical radiolucency \u2014 the untreated #16 canal is the likely pain origin.",
    "rafi_18_24e6fe954f": "\U0001F4CE Clinical hinge: An incisal-THIRD fracture of an anterior tooth (enamel-dentin, vital pulp) is restored directly with COMPOSITE RESIN (Class IV); full coverage wastes tooth structure and lab-processed repair adds nothing for a directly bondable defect.",
    "rafi_18_39a730b839": "\U0001F4CE Clinical hinge: Cast-gold INLAY preparations require all walls slightly DIVERGENT occlusally (single draw, no undercuts, beveled margins), whereas amalgam relies on convergent (undercut) walls for retention \u2014 box width/floor width are unrelated to switching materials.",
    "rafi_18_3e6116bac2": "\U0001F4CE Clinical hinge: A SINGLE crown in an intact, harmonious occlusion needs only a NON-ADJUSTABLE (hinge/average-value) articulator with an interocclusal record \u2014 facebow transfers and semi-adjustable programming matter for multiple units/reconstructed occlusions.",
    "rafi_18_b989623a7a": "\U0001F4CE Clinical hinge: Facial asymmetry is measured on the POSTEROANTERIOR (frontal) cephalogram \u2014 paired structures are compared across the midsagittal axis; an OPG images jaws/teeth but cannot quantify transverse skeletal symmetry.",
    "rafi_18_8b008e4754": "\U0001F4CE Clinical hinge: Defensible records are OBJECTIVE \u2014 dated entries charting observed findings and actions (\u201cif it was not charted, it did not happen\u201d, Contemporary OMFS records chapter); completeness and specificity support the record, but objectivity gives it clinical/legal weight.",
    "rafi_18_244630e447": "\U0001F4CE Clinical hinge: Relief of a prominent MYLOHYOID ridge via a floor-of-mouth incision risks the LINGUAL nerve \u2014 it rests directly against the medial mandible (lingual to the molar/ridge region) just beneath mucoperiosteum; the mylohyoid nerve runs below the mylohyoid line in its groove, and IAN/mental lie buccal or deeper.",
    "rafi_18_9e06d81d42": "[Book: Malamed, Handbook of Local Anesthesia] \u2014 \u201cthe incidence of allergy to both procaine and other ester local anesthetics is significantly greater than to amide local anesthetics\u201d; itching + lip swelling (urticaria/angioedema) after LA implicates the ESTER \u2014 procaine \u2014 not the amides lidocaine/prilocaine.",
    "rafi_18_fec552e6de": "\U0001F4CE Clinical hinge: For a 2-year-old, PLAIN 2% lidocaine is standard \u2014 weight-based dosing with wide safety margin; 4% concentrations raise overdose risk in toddlers and articaine is cautioned/avoided below age 4.",
    "rafi_18_eddfbb3bb9": None,  # demoted
    "rafi_18_172c2faf72": "\U0001F4CE Clinical hinge: Isolated red-cell-line depression with NORMAL WBC and platelets matches the mild normocytic anemia of HYPOTHYROIDISM; folate deficiency produces megaloblastic PANcytopenia (all three lines fall), and PLS/paraneoplastic states do not selectively spare leukocytes and platelets.",
    "rafi_19_fb57179862": "\U0001F4CE Clinical hinge: Classic root-anatomy data place the large majority of accessory (lateral) canals in the APICAL third \u2014 about 74% (de Deus' distribution); the remainder occur in mid-root and coronal thirds. (Recall figure; no verbatim local passage.)",
    "rafi_20_54c10c08a3": "[Book: Contemporary Fixed Prosthodontics] \u2014 bonding to porcelain begins by ETCHING the intaglio with HYDROFLUORIC acid to microscopically roughen the ceramic, followed by silane; phosphoric acid etches enamel/dentin \u2014 not feldspathic porcelain.",
    "rafi_20_874d9dcdb4": "[Book: Lindhe, Clinical Periodontology] \u2014 L\u00f6e's Sri Lanka (Teens/Gjerp) cohort: \u201crapid progression of periodontal breakdown (8%)\u201d \u2014 about 8% of subjects were rapid progressors.",
    "rafi_20_c126ea8eb0": "[Book: Carranza's Clinical Periodontology] \u2014 the SUBEPITHELIAL CONNECTIVE TISSUE GRAFT is the root-coverage gold standard for shallow/moderate recession, giving the highest complete-coverage rates plus increased tissue thickness \u2014 ideal when sensitivity AND esthetics drive treatment.",
    "rafi_20_531516591b": "[Book: Periodontics: Medicine, Surgery and Implants] \u2014 \u201cthe implant head should be placed approximately 3 mm apical to the position of the intended gingival margin\u201d \u2014 in healthy tissue that corresponds to ~3 mm apical to the CEJ of adjacent natural teeth.",
    "rafi_20_65b1d18584": "\U0001F4CE Clinical hinge: After implant placement for an overdenture, the patient wears the OLD denture IMMEDIATELY (relieved over the surgical sites, softened liner as needed) for esthetic/social continuity, removing it at night \u2014 abstention protects nothing and costs function.",
    "abtal_pack_fd9edd21c4": "[Book: Neville, Oral and Maxillofacial Pathology] \u2014 \u201cThe treatment of the peripheral giant cell granuloma consists of local surgical excision down to the underlying bone\u201d with careful scaling of adjacent teeth \u2014 excisional biopsy removes and samples the lesion in one step.",
}

# fill flip-whys into WHYS
for _id, (_ans, _exp, _why, _bs) in FLIPS.items():
    WHYS[_id] = _why

# ── TRIMS: id -> [(option_index, expected_current_substring, new_text)] ──
TRIMS = {
    "rafi_12_7803257e3f": [(0, "Infratemporal", "Infratemporal space")],
    "rafi_17_94ca05abd8": [(1, "anterior bite plane", "Extrusion of posterior (anterior bite plane)")],
    "rafi_18_24e6fe954f": [(2, "Composite repair", "Composite repair")],
    "rafi_18_172c2faf72": [(3, "Hypothyroidism", "Hypothyroidism")],
    "rafi_19_fb57179862": [(3, "74%", "74%")],
}


def load() -> list:
    text = Q_JS.read_text(encoding="utf-8")
    m = re.search(r"QUESTION_BANK\s*=\s*(\[.*\]);?\s*$", text, re.DOTALL)
    if not m:
        raise SystemExit("cannot parse questions.js")
    return json.loads(m.group(1))


def save(bank: list) -> None:
    out = "QUESTION_BANK = " + json.dumps(bank, ensure_ascii=False, indent=1) + ";\n"
    bak = Q_JS.with_suffix(".js.bak-glue53")
    bak.write_text(Q_JS.read_text(encoding="utf-8"), encoding="utf-8")
    Q_JS.write_text(out, encoding="utf-8")
    print(f"backup written: {bak.name}")


def main() -> int:
    apply = "--apply" in sys.argv
    bank = load()
    by_id = {q.get("id"): q for q in bank}

    n_flip = n_demote = n_why = n_trim = 0
    problems = []

    for qid, (new_ans, expect_txt, why, bsupport) in FLIPS.items():
        q = by_id.get(qid)
        if not q:
            problems.append(f"MISSING flip {qid}"); continue
        old_ans = q.get("answer")
        opts = q.get("options") or []
        # RED LINE: verify the NEW index really points at the expected option text
        if not (0 <= new_ans < len(opts)) or expect_txt.lower() not in str(opts[new_ans]).lower():
            problems.append(
                f"INDEX-TEXT MISMATCH {qid}: opts[{new_ans}]={opts[new_ans] if new_ans < len(opts) else '?'}!~{expect_txt}")
            continue
        print(f"FLIP  {qid}: answer {old_ans} -> {new_ans} ({opts[new_ans][:45]})")
        n_flip += 1
        if apply:
            q["answer"] = new_ans
            q["explanation"] = why
            q["book_support"] = bsupport

    for qid, reason in DEMOTE.items():
        q = by_id.get(qid)
        if not q:
            problems.append(f"MISSING demote {qid}"); continue
        if q.get("usable") is False:
            continue
        print(f"DEMOTE {qid}: {reason[:70]}")
        n_demote += 1
        if apply:
            q["usable"] = False
            q["exclude_reason"] = reason
            q["explanation"] = WHYS[qid]

    for qid, why in WHYS.items():
        if qid in FLIPS or qid in DEMOTE:
            continue
        q = by_id.get(qid)
        if not q:
            problems.append(f"MISSING why {qid}"); continue
        if q.get("usable") is False:
            continue
        ok_prefix = why.lstrip().startswith("\U0001F4CE Clinical hinge:") or "[Book:" in why
        if not ok_prefix or len(why) < 40:
            problems.append(f"G-CITE-UNSAFE why {qid}"); continue
        old = (q.get("explanation") or "")[:40].replace("\n", " ")
        print(f"REWHY {qid}: {old!r} -> {why[:55]!r}")
        n_why += 1
        if apply:
            q["explanation"] = why

    for qid, trims in TRIMS.items():
        q = by_id.get(qid)
        if not q:
            problems.append(f"MISSING trim {qid}"); continue
        for idx, expect, new_text in trims:
            cur = str((q.get("options") or [])[idx])
            if expect.lower() not in cur.lower() or cur.strip() == new_text.strip():
                continue
            print(f"TRIM  {qid}[{idx}]: {cur[:50]!r} -> {new_text!r}")
            n_trim += 1
            if apply:
                q["options"][idx] = new_text

    print(f"\nTOTAL: flips={n_flip} demote={n_demote} rewhy={n_why} trims={n_trim}")
    if problems:
        print("PROBLEMS:")
        for p in problems:
            print(" ", p)
        return 1
    if not apply:
        print("DRY RUN \u2014 rerun with --apply to write.")
        return 0
    save(bank)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

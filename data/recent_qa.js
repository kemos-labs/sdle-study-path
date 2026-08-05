/** RECENT_QA — 439 textbook-verified Q&A (62 original + 377 book-solved MCQs from
 * July-2026 exam recall + MCQs_Solved + BANK_160 files).
 * Each item grounded in official textbooks with reference + reasoning.
 * Loaded as window.RECENT_QA for the "Recent Q&A" tab.
 * Updated: 2026-08-06
 */
(function (w) {
  const ITEMS = [
{
  "id": "qa_a_02",
  "set": "A",
  "qnum": 2,
  "dept": "fixed",
  "stem": "What is the percentage of metal in a PFM (Porcelain-Fused-to-Metal) crown?",
  "options": [],
  "answer": "The metal coping (framework) is thin — about 0.3–0.5 mm — and the porcelain veneer is about 0.7–1.0 mm, so the metal is roughly one-third of the restoration thickness by cross-section.",
  "reference": "Contemporary Fixed Prosthodontics (Shillingburg) 4e / 5e",
  "why": "Shillingburg specifies the metal-ceramic crown: a coping of ~0.3–0.5 mm metal is veneered with ~0.7–1 mm porcelain. The metal is kept thin (just enough for rigidity/opaque) because porcelain provides the bulk and the esthetics."
},
{
  "id": "qa_a_03",
  "set": "A",
  "qnum": 3,
  "dept": "fixed",
  "stem": "What are the types of finishing lines for full-coverage restorations, and what is a key feature of a good finishing line?",
  "options": [],
  "answer": "Types: feather edge, chisel, chamfer, bevel, shoulder (90°), sloped shoulder, beveled shoulder. Key feature: it must be a distinct, sharply defined, easily readable margin.",
  "reference": "Contemporary Fixed Prosthodontics (Shillingburg) 4e / 5e",
  "why": "Shillingburg (Ch. 7 margin designs) shows all these forms and states the margin must be 'distinct' so the technician can see where the die ends and the wax/pattern begins. A chamfer is the most common for cast metal; a 90° shoulder for ceramic margins."
},
{
  "id": "qa_a_04",
  "set": "A",
  "qnum": 4,
  "dept": "operative",
  "stem": "From where to where is the clinical crown measured?",
  "options": [],
  "answer": "From the cementoenamel junction (CEJ) to the incisal/occlusal edge — i.e. the portion of the tooth coronal to the CEJ. In the mouth the 'visible/clinical' crown is measured from the free gingival margin to the incisal edge.",
  "reference": "Sturdevant's Art & Science of Operative Dentistry 5e",
  "why": "Sturdevant distinguishes the anatomical crown (CEJ → incisal edge) from the clinical crown (gingival margin → incisal edge). Restorative preparation length is planned relative to the clinical crown visible in the mouth."
},
{
  "id": "qa_a_09",
  "set": "A",
  "qnum": 9,
  "dept": "oms",
  "stem": "What is the purpose of a dental prop (bite block)?",
  "options": [],
  "answer": "To support and stabilise the mandible, keep the mouth open at a comfortable width, and protect the TMJ (and teeth) during long procedures under sedation/GA.",
  "reference": "Contemporary Oral & Maxillofacial Surgery (Hupp/Tucker) 6e/7e",
  "why": "Hupp (Contemporary OMS) Ch. 6: 'a bite block placed on the contralateral side supports the patient's jaw and protects the TMJ'; it prevents over-opening of the joint and fatigue. It must be released periodically."
},
{
  "id": "qa_a_13",
  "set": "A",
  "qnum": 13,
  "dept": "endo",
  "stem": "What material is used to fill a root canal to aid healing?",
  "options": [],
  "answer": "Gutta-percha (the solid core) plus a biocompatible root-canal sealer.",
  "reference": "Cohen's Pathways of the Pulp 2016 (Hargreaves & Berman)",
  "why": "Cohen's Pathways: gutta-percha is the gold-standard obturating core; the sealer fills accessory canals and irregularities and adheres to dentin. Together they three-dimensionally seal the canal to prevent re-infection and allow periradicular healing."
},
{
  "id": "qa_a_14",
  "set": "A",
  "qnum": 14,
  "dept": "endo",
  "stem": "The shape of the root canal in cross-section is variable, while in the apical third it is always round. Which part is correct and which is incorrect?",
  "options": [],
  "answer": "First part CORRECT (canal cross-section is variable); second part INCORRECT (the apical third is NOT always round — it can be oval, kidney-shaped, or have fins/isthmuses).",
  "reference": "Cohen's Pathways of the Pulp 2016 (Hargreaves & Berman)",
  "why": "Cohen's Ch. 5 (µCT cross-sections) shows canals vary widely along the root; the apical third frequently retains an oval/kidney shape with lateral fins and a second canal. Only instrumentation with round files rounds it — the native anatomy is not reliably round."
},
{
  "id": "qa_a_15",
  "set": "A",
  "qnum": 15,
  "dept": "operative",
  "stem": "What is the irritating material to the pulp?",
  "options": [],
  "answer": "Zinc phosphate cement (acidic) and silicate cement are the classic pulp irritants; also phosphoric acid etchant applied to deep dentin, and microleakage of any unsealed restoration.",
  "reference": "Sturdevant's Art & Science of Operative Dentistry 5e / O'Brien / Powers & Sakaguchi — Dental Materials & Their Selection 3e",
  "why": "Sturdevant & the materials texts: zinc phosphate is acidic (low pH while setting) and is cytotoxic to odontoblasts in deep cavities → use a liner/base (Ca(OH)₂ / GIC) first. Silicate cements historically caused severe pulp necrosis."
},
{
  "id": "qa_a_16",
  "set": "A",
  "qnum": 16,
  "dept": "operative",
  "stem": "Why is a substance like Hydroxyapatite or Fluoride added to toothpaste?",
  "options": [],
  "answer": "To remineralise early enamel lesions and convert hydroxyapatite into the more acid-resistant fluorapatite / fluorohydroxyapatite, and to inhibit bacterial enzymes.",
  "reference": "Sturdevant's Art & Science of Operative Dentistry 5e",
  "why": "Sturdevant: tooth minerals are hydroxyapatite Ca₁₀(PO₄)₆(OH)₂. Fluoride substitutes for the hydroxyl ion → fluorapatite, which dissolves at a lower pH (more acid-resistant) and favours remineralisation."
},
{
  "id": "qa_a_18",
  "set": "A",
  "qnum": 18,
  "dept": "operative",
  "stem": "Does dental caries progress from dentin to enamel (Forward) or from enamel to dentin (Backward)?",
  "options": [],
  "answer": "From ENAMEL to DENTIN — caries begins in enamel and spreads into dentin (so the 'dentin→enamel (forward)' label is the wrong direction).",
  "reference": "Sturdevant's Art & Science of Operative Dentistry 5e",
  "why": "Sturdevant: the carious process starts with enamel demineralisation (white spot), then crosses the enamel-dentin junction and spreads laterally and pulpally in dentin. So progression is enamel → dentin."
},
{
  "id": "qa_a_19",
  "set": "A",
  "qnum": 19,
  "dept": "operative",
  "stem": "What is the general public-health preventive measure to prevent dental caries? (Brushing and toothpaste.)",
  "options": [],
  "answer": "Community WATER FLUORIDATION is the most effective public-health measure; at the individual level, twice-daily brushing with fluoride toothpaste is the most widely available method.",
  "reference": "Sturdevant's Art & Science of Operative Dentistry 5e",
  "why": "Sturdevant: 'every $1 spent on water fluoridation saves ~$6 in dental treatment' — community water fluoridation is the cornerstone population strategy."
},
{
  "id": "qa_a_24",
  "set": "A",
  "qnum": 24,
  "dept": "ortho_pedo",
  "stem": "A 14-year-old child has a congenital absence of the central and lateral incisors. What type of prosthesis should be made?",
  "options": [],
  "answer": "A transitional / provisional REMOVABLE partial denture (or an acid-etch/Maryland bonded bridge) — NOT an implant, because growth is not yet complete.",
  "reference": "McDonald & Avery Pediatric Dentistry 10e / Contemporary Fixed Prosthodontics (Shillingburg) 4e / 5e",
  "why": "McDonald & Shillingburg: implants must be deferred until skeletal growth is finished (~age 18–20 for girls, ~21+ for boys) to avoid infraocclusion. Until then a removable transitional prosthesis restores esthetics and function."
},
{
  "id": "qa_a_25",
  "set": "A",
  "qnum": 25,
  "dept": "ortho_pedo",
  "stem": "What is meant by a 'Sunday bite'? (Class III malocclusion)",
  "options": [],
  "answer": "A habitual forward posturing of the mandible so the incisors meet edge-to-edge / in a pseudo-Class III relationship — a habitual, not skeletal, Class III.",
  "reference": "Proffit — Contemporary Orthodontics 5e/7e (2026)",
  "why": "Proffit: a 'Sunday bite' (pseudo-Class III) is a habitual forward slide from a normal or Class II molar into an edge-to-edge anterior relationship. It is a postural habit, not true skeletal Class III."
},
{
  "id": "qa_a_28",
  "set": "A",
  "qnum": 28,
  "dept": "operative",
  "stem": "What is the purpose of dentin etching?",
  "options": [],
  "answer": "To remove the smear layer, open the dentinal tubules, and demineralise the intertubular/peritubular dentin so that resin infiltrates and forms the hybrid layer + resin tags (micro-mechanical retention).",
  "reference": "Sturdevant's Art & Science of Operative Dentistry 5e",
  "why": "Sturdevant: acid etching of dentin dissolves the smear layer and ~2–5 µm of hydroxyapatite, exposing a collagen network. Hydrophilic resin primer infiltrates this network → the 'hybrid layer' and resin tags in the tubules."
},
{
  "id": "qa_a_29",
  "set": "A",
  "qnum": 29,
  "dept": "operative",
  "stem": "What is used to etch dentin?",
  "options": [],
  "answer": "Phosphoric acid, usually 32–37% (typical 37% for 15 s on dentin, shorter than enamel).",
  "reference": "Sturdevant's Art & Science of Operative Dentistry 5e",
  "why": "Sturdevant: 37% phosphoric acid gel is standard; dentin is etched for a shorter time (~15 s) than enamel (15–30 s) to avoid over-etching/collagen collapse."
},
{
  "id": "qa_a_30",
  "set": "A",
  "qnum": 30,
  "dept": "endo",
  "stem": "What is a high-heat obturation technique?",
  "options": [],
  "answer": "An injectable thermoplasticised gutta-percha technique that heats GP to a high temperature (e.g. Obtura II at ~160 °C) to fill the canal in three dimensions, usually after a warm vertical down-pack.",
  "reference": "Cohen's Pathways of the Pulp 2016 (Hargreaves & Berman)",
  "why": "Cohen's: Obtura II (and System B for warm vertical compaction) are the high-heat thermoplasticised techniques. They deliver warm, flowable GP that adapts to canal irregularities."
},
{
  "id": "qa_a_35",
  "set": "A",
  "qnum": 35,
  "dept": "endo",
  "stem": "About the maxillary palatal root variation: describe the variation.",
  "options": [],
  "answer": "The palatal root of the maxillary first molar is the longest and widest root, inclines distally (and slightly buccally), and its buccal surface is concave / furrowed — giving a kidney/bean cross-section that frequently hides a second palatal canal.",
  "reference": "Cohen's Pathways of the Pulp 2016 (Hargreaves & Berman)",
  "why": "Cohen's Ch. 5 & 7: the palatal root inclines distally, is broadest buccolingually, has a buccal concavity, and a second canal — the concavity/bean shape is the classic reason a canal is missed under the DOM."
},
{
  "id": "qa_b_12",
  "set": "B",
  "qnum": 12,
  "dept": "ortho_pedo",
  "stem": "The gold-standard material in vital pulpotomy for teeth is:",
  "options": [
    "MTA.",
    "Ca(OH)₂.",
    "GIC.",
    "Resin composite."
  ],
  "answer": 0,
  "answerText": "MTA",
  "reference": "McDonald & Avery Pediatric Dentistry 10e / Cohen's Pathways of the Pulp 2016",
  "why": "MTA has superseded formocresol as the gold standard for vital pulpotomy — it sets in the presence of moisture, is biocompatible, and induces dentin bridge formation with the fewest pulp necrosis outcomes."
},
{
  "id": "qa_b_16",
  "set": "B",
  "qnum": 16,
  "dept": "ortho_pedo",
  "stem": "Formocresol has limited use in dentistry because it is:",
  "options": [
    "Poor biocompatibility.",
    "High strength.",
    "Weak.",
    "All the above."
  ],
  "answer": 0,
  "answerText": "Poor biocompatibility",
  "reference": "McDonald & Avery Pediatric Dentistry 10e",
  "why": "Formocresol (Buckley's) is toxic, mutagenic/carcinogenic (formaldehyde + cresol), distributes systemically, and is no longer recommended. Its limitation is biological (poor biocompatibility), not mechanical."
},
{
  "id": "qa_b_24",
  "set": "B",
  "qnum": 24,
  "dept": "fixed",
  "stem": "A patient with generalized attrition who needs an FPD should first undergo:",
  "options": [
    "Period surgery.",
    "Desensitization of teeth.",
    "Crown build-up.",
    "Conventional RCT."
  ],
  "answer": 1,
  "answerText": "Desensitization of teeth",
  "reference": "Sturdevant's Operative Dentistry 5e / Contemporary Fixed Prosthodontics (Shillingburg) 4e/5e",
  "why": "For generalized attrition the first, most conservative step is to manage sensitivity and establish the correct occlusal vertical dimension before any restorative work."
},
{
  "id": "qa_b_31",
  "set": "B",
  "qnum": 31,
  "dept": "endo",
  "stem": "Which best describes the movement technique of a K-file during root canal instrumentation:",
  "options": [
    "Rotation.",
    "Up and down motion.",
    "Clockwise rotation combined with up and down motion.",
    "Circumferential filing."
  ],
  "answer": 2,
  "answerText": "Clockwise rotation combined with up and down motion",
  "reference": "Cohen's Pathways of the Pulp 2016",
  "why": "K-files are manipulated with a quarter-turn clockwise rotation (reaming) combined with an apical-coronal withdrawal (filing) stroke — the classic 'watch-winding'/balanced-force motion."
},
{
  "id": "qa_b_32",
  "set": "B",
  "qnum": 32,
  "dept": "operative",
  "stem": "What is the main purpose of dentin etching:",
  "options": [
    "To remove the smear layer only.",
    "To create micro-retentive resin tags (interlocking tags).",
    "To increase dentin hardness.",
    "To disinfect the cavity."
  ],
  "answer": 1,
  "answerText": "To create micro-retentive resin tags (interlocking tags)",
  "reference": "Sturdevant's Art & Science of Operative Dentistry 5e",
  "why": "The PURPOSE of etching dentin is to create micromechanical retention — the hybrid layer + resin tags — that interlocks the resin to the tooth. Removing the smear layer is a means, not the purpose."
},
{
  "id": "qa_b_33",
  "set": "B",
  "qnum": 33,
  "dept": "endo",
  "stem": "What is a high-heat obturation technique:",
  "options": [
    "Thermofil.",
    "Ultrafil.",
    "Obtura II.",
    "Lateral condensation."
  ],
  "answer": 2,
  "answerText": "Obtura II",
  "reference": "Cohen's Pathways of the Pulp 2016",
  "why": "Obtura II is the high-heat injectable thermoplasticised gutta-percha system (~160 °C). ThermoFil are carrier-based; Ultrafil is LOW-heat (~70 °C); lateral condensation uses cold GP."
},
{
  "id": "qa_b_39",
  "set": "B",
  "qnum": 39,
  "dept": "fixed",
  "stem": "Which best describes the correct path of insertion for a fixed prosthesis:",
  "options": [
    "Parallel to each other.",
    "Parallel to the long axis of the normal adjacent tooth.",
    "Parallel to the long axis of the abutment tooth.",
    "Perpendicular to the occlusal plane."
  ],
  "answer": 2,
  "answerText": "Parallel to the long axis of the abutment tooth",
  "reference": "Contemporary Fixed Prosthodontics (Shillingburg) 4e/5e",
  "why": "The path of insertion/withdrawal is determined by the axial walls of the prepared abutment and should follow the long axis of the abutment tooth so the restoration seats without binding."
},
{
  "id": "qa_b_45",
  "set": "B",
  "qnum": 45,
  "dept": "fixed",
  "stem": "Which is NOT an indication for placing a subgingival margin:",
  "options": [
    "When additional retention is required.",
    "For esthetic reasons.",
    "Presence of cervical caries.",
    "When the margin is easily visible at the first appointment."
  ],
  "answer": 3,
  "answerText": "When the margin is easily visible at the first appointment",
  "reference": "Contemporary Fixed Prosthodontics (Shillingburg) 4e/5e",
  "why": "A margin that is 'easily visible' is precisely a supragingival indication — placing it subgingival needlessly violates the biologic width and harms periodontium."
},
{
  "id": "qa_b_46",
  "set": "B",
  "qnum": 46,
  "dept": "fixed",
  "stem": "Most appropriate management for a crown margin exposed 0.5 mm above the gingival margin:",
  "options": [
    "Remake the crown.",
    "Restore the exposed area using GIC.",
    "Restore the exposed area using amalgam.",
    "All of the above."
  ],
  "answer": 0,
  "answerText": "Remake the crown",
  "reference": "Contemporary Fixed Prosthodontics (Shillingburg) 4e/5e",
  "why": "An open/short margin that is supragingival and visible is a remake — patching with GIC or amalgam leaves a marginal discrepancy with plaque retention and recurrent caries."
},
{
  "id": "qa_b_48",
  "set": "B",
  "qnum": 48,
  "dept": "ortho_pedo",
  "stem": "Average lifespan of composite restorations in primary teeth:",
  "options": [
    "2–3 years.",
    "3–5 years.",
    "5–10 years.",
    "10–15 years."
  ],
  "answer": 1,
  "answerText": "3–5 years",
  "reference": "McDonald & Avery Pediatric Dentistry 10e / Sturdevant's Operative Dentistry 5e",
  "why": "Composite restorations in primary teeth are expected to survive ~3–5 years (the lifetime of a primary molar until exfoliation is ~3–6 years)."
},
{
  "id": "qa_b_49",
  "set": "B",
  "qnum": 49,
  "dept": "operative",
  "stem": "Which composite resin is most suitable for restoring posterior teeth:",
  "options": [
    "Microfilled composite.",
    "Flowable composite.",
    "Light-curing composite.",
    "Packable composite."
  ],
  "answer": 3,
  "answerText": "Packable composite",
  "reference": "Sturdevant's Operative Dentistry 5e / Dental Materials & Their Selection 3e",
  "why": "Packable (condensable) composites have high filler load and high viscosity → better handling, lower polymerisation shrinkage, and improved wear resistance for posterior load-bearing cavities."
},
{
  "id": "qa_b_50",
  "set": "B",
  "qnum": 50,
  "dept": "operative",
  "stem": "Which best describes packable composite resin:",
  "options": [
    "High viscosity and used for restoring posterior teeth.",
    "Low viscosity.",
    "Easily polishable.",
    "Highly translucent."
  ],
  "answer": 0,
  "answerText": "High viscosity and used for restoring posterior teeth",
  "reference": "Dental Materials & Their Selection 3e",
  "why": "Packable composites are high-viscosity, highly filled restoratives designed for posterior Class I/II — they handle like amalgam, resist slump, and have adequate wear resistance."
},
{
  "id": "qa_c_01",
  "set": "C",
  "qnum": 1,
  "dept": "operative",
  "stem": "The 6th generation bonding system is characterized as:",
  "options": [
    "Three-step technique.",
    "Self-etching system without separate resin application.",
    "Self-adhesive system.",
    "Total-etch two-step system."
  ],
  "answer": 1,
  "answerText": "Self-etching system",
  "reference": "Sturdevant's Art & Science of Operative Dentistry 5e",
  "why": "6th-gen = self-etch adhesives (acidic monomers etch & prime simultaneously). 6th gen is a 2-step self-etch (separate adhesive resin); 7th gen is all-in-one; 8th gen = self-adhesive."
},
{
  "id": "qa_c_03",
  "set": "C",
  "qnum": 3,
  "dept": "perio",
  "stem": "Supragingival calculus is characterized by all of the following EXCEPT:",
  "options": [
    "Hard and rough.",
    "Easy to detach.",
    "Has component of saliva.",
    "None."
  ],
  "answer": 1,
  "answerText": "Easy to detach",
  "reference": "Newman & Carranza's Clinical Periodontology 13e",
  "why": "Supragingival calculus is hard, rough, yellowish, firmly adherent to enamel. It is NOT easy to detach — it requires instrumentation (scaling) to remove."
},
{
  "id": "qa_c_08",
  "set": "C",
  "qnum": 8,
  "dept": "oms",
  "stem": "Which teeth are considered relatively more difficult to extract:",
  "options": [
    "Mandibular canine.",
    "Maxillary canine.",
    "Mandibular premolar.",
    "Maxillary central incisor."
  ],
  "answer": 1,
  "answerText": "Maxillary canine",
  "reference": "Contemporary Oral & Maxillofacial Surgery (Hupp/Tucker) 6e/7e",
  "why": "The maxillary canine has the longest root in the arch (~26 mm), a bulky crown, a thick buccal plate, making it the most difficult routine extraction of these choices."
},
{
  "id": "qa_c_12",
  "set": "C",
  "qnum": 12,
  "dept": "ortho_pedo",
  "stem": "The marginal ridge cusp of the second mandibular molar occludes with:",
  "options": [
    "Mesial marginal ridge of maxillary second premolar.",
    "Mesial marginal ridge of maxillary first molar.",
    "Distal marginal ridge of maxillary first molar.",
    "Distal marginal ridge of maxillary second molar."
  ],
  "answer": 2,
  "answerText": "Distal marginal ridge of maxillary first molar",
  "reference": "Wheeler's Dental Anatomy (via Sturdevant ch. 2 occlusion)",
  "why": "In Angle Class I the mesial cusp of the mandibular second molar opposes the embrasure between the maxillary first and second molars — contacting the distal marginal ridge of #3."
},
{
  "id": "qa_c_16",
  "set": "C",
  "qnum": 16,
  "dept": "rpd",
  "stem": "Which is used to adjust the anterior relationship of the bite rim:",
  "options": [
    "Facebow.",
    "Fox plane.",
    "Articulator.",
    "Bite registration material."
  ],
  "answer": 1,
  "answerText": "Fox plane",
  "reference": "Textbook of Complete Dentures / McCracken's RPD",
  "why": "The Fox plane is placed against the bite rims and viewed from the front/profile to set the antero-posterior inclination of the occlusal plane."
},
{
  "id": "qa_c_17",
  "set": "C",
  "qnum": 17,
  "dept": "mixed",
  "stem": "The first and most important step in the diagnostic work-up of a dental patient:",
  "options": [
    "Reviewing the medical history.",
    "Taking the dental history.",
    "Identifying the chief complaint.",
    "Obtaining radiographic images."
  ],
  "answer": 2,
  "answerText": "Identifying the chief complaint",
  "reference": "Contemporary Oral & Maxillofacial Surgery (Hupp/Tucker) 6e/7e",
  "why": "The chief complaint is the patient's presenting problem in their own words and is the starting point that focuses the history, examination, and radiographs."
},
{
  "id": "qa_c_24",
  "set": "C",
  "qnum": 24,
  "dept": "fixed",
  "stem": "The factor that increases cohesive fracture in PFM (Porcelain-Fused-to-Metal) crowns is:",
  "options": [
    "Increased oxide layer.",
    "Thick porcelain.",
    "Thick metal.",
    "All of the above."
  ],
  "answer": 0,
  "answerText": "Increased oxide layer",
  "reference": "Dental Materials & Their Selection 3e",
  "why": "An EXCESSIVE (thick) oxide layer is brittle and weakly adherent → cohesive fracture within the oxide/porcelain and porcelain chipping. A thin, uniform oxide optimises bonding."
},
{
  "id": "qa_c_26",
  "set": "C",
  "qnum": 26,
  "dept": "fixed",
  "stem": "A correct comparison between all-ceramic jackets and PFM crowns is:",
  "options": [
    "They have the same finish line (margin).",
    "The lingual wall is more conservative in a PFM crown.",
    "",
    ""
  ],
  "answer": 1,
  "answerText": "The lingual wall is more conservative in a PFM crown",
  "reference": "Contemporary Fixed Prosthodontics (Shillingburg) 4e/5e",
  "why": "A PFM crown's lingual surface can be restored in metal only, so its lingual reduction is conservative (~0.7–1 mm) versus all-ceramic which needs uniform 1.2–1.5 mm reduction."
},
{
  "id": "qa_c_48",
  "set": "C",
  "qnum": 48,
  "dept": "fixed",
  "stem": "The first step in treating generalized attrition is:",
  "options": [
    "Desensitizing agents.",
    "Crowns.",
    "Composite build-up.",
    ""
  ],
  "answer": 0,
  "answerText": "Desensitizing agents",
  "reference": "Sturdevant's Operative Dentistry 5e / Contemporary Fixed Prosthodontics 4e/5e",
  "why": "Generalized attrition is first managed conservatively — desensitise the exposed dentin and stabilise the occlusion before any definitive restoration."
},
{
  "id": "qa_c_50",
  "set": "C",
  "qnum": 50,
  "dept": "operative",
  "stem": "Which fluoride method is used for the general prevention of caries worldwide:",
  "options": [
    "Systemic fluoride.",
    "Topical fluoride.",
    "Toothpaste.",
    ""
  ],
  "answer": 2,
  "answerText": "Toothpaste",
  "reference": "Sturdevant's Art & Science of Operative Dentistry 5e",
  "why": "Fluoride toothpaste is the most widely available and universally used caries-prevention method across populations (twice-daily brushing)."
},
{
  "id": "qa_d_01",
  "set": "D",
  "qnum": 1,
  "dept": "oms",
  "stem": "A simple extraction uses an elevator only for:",
  "options": [
    "Impacted tooth.",
    "Removing an erupted tooth.",
    "Removing a tooth with bone.",
    ""
  ],
  "answer": 1,
  "answerText": "Removing an erupted tooth",
  "reference": "Contemporary Oral & Maxillofacial Surgery (Hupp/Tucker) 6e/7e",
  "why": "A straight elevator is used to luxate an erupted tooth from its periodontal ligament before forceps delivery. Impacted teeth require surgical removal."
},
{
  "id": "qa_d_02",
  "set": "D",
  "qnum": 2,
  "dept": "endo",
  "stem": "About the maxillary palatal root variation:",
  "options": [
    "Concave and kidney shape.",
    "Rarely has two canals.",
    "Inclined distally.",
    "Wider and oval in cross-section."
  ],
  "answer": 0,
  "answerText": "Concave and kidney shape",
  "reference": "Cohen's Pathways of the Pulp 2016",
  "why": "The palatal root is broad buccolingually with a buccal concavity/furrow, giving a kidney/bean cross-section that hides a second canal — this is the hallmark 'variation' tested."
},
{
  "id": "qa_d_04",
  "set": "D",
  "qnum": 4,
  "dept": "endo",
  "stem": "The success of a root canal filling is best assessed by:",
  "options": [
    "Radiographs.",
    "Clinical observation.",
    "Size of gutta-percha cone used.",
    "A and B."
  ],
  "answer": 3,
  "answerText": "A and B (radiographs + clinical observation)",
  "reference": "Cohen's Pathways of the Pulp 2016",
  "why": "Endodontic outcome is judged by BOTH clinical signs/symptoms AND radiographic healing (resolution of the periradicular radiolucency, intact lamina dura)."
},
{
  "id": "qa_d_06",
  "set": "D",
  "qnum": 6,
  "dept": "fixed",
  "stem": "Inadequate incisal reduction during tooth preparation for a metal-ceramic restoration results in:",
  "options": [
    "Inadequate path of insertion.",
    "Less resistance and retention of the restoration.",
    "Poor incisal translucency in the final restoration.",
    "All are true."
  ],
  "answer": 2,
  "answerText": "Poor incisal translucency in the final restoration",
  "reference": "Contemporary Fixed Prosthodontics (Shillingburg) 4e/5e",
  "why": "Insufficient incisal reduction leaves inadequate space for the metal coping + porcelain veneer → the porcelain is too thin → poor incisal translucency."
},
{
  "id": "qa_d_10",
  "set": "D",
  "qnum": 10,
  "dept": "fixed",
  "stem": "During tooth preparation for a full metal crown, the amount of tooth structure that should be removed is:",
  "options": [
    "0.5–0.7 mm.",
    "0.7–1 mm.",
    "1–1.5 mm.",
    "1.5–2 mm."
  ],
  "answer": 2,
  "answerText": "1–1.5 mm (occlusal clearance)",
  "reference": "Contemporary Fixed Prosthodontics (Shillingburg) 4e/5e",
  "why": "A full cast metal crown requires ~1.0–1.5 mm occlusal clearance and ~0.7–1 mm axial reduction with a 0.3–0.5 mm chamfer."
},
{
  "id": "qa_d_22",
  "set": "D",
  "qnum": 22,
  "dept": "endo",
  "stem": "When using an inflexible file in a curved canal, what does it cause on the outer surface of the curve:",
  "options": [
    "Ledge.",
    "Zipping.",
    "Perforation.",
    "Elbow."
  ],
  "answer": 1,
  "answerText": "Zipping",
  "reference": "Cohen's Pathways of the Pulp 2016",
  "why": "A stiff file tends to straighten in a curved canal and preferentially cuts the outer aspect toward the apex → apical transportation = 'zipping'."
},
{
  "id": "qa_d_23",
  "set": "D",
  "qnum": 23,
  "dept": "endo",
  "stem": "The movements of a K-file in root canal treatment are:",
  "options": [
    "Clockwise and anti-clockwise with pressure apically.",
    "Rotation movement with pressure apically.",
    "",
    ""
  ],
  "answer": 0,
  "answerText": "Clockwise and anti-clockwise with pressure apically",
  "reference": "Cohen's Pathways of the Pulp 2016",
  "why": "The K-file is used with a balanced-force / watch-winding motion — clockwise then anti-clockwise rotation with light apical pressure."
},
{
  "id": "qa_d_26",
  "set": "D",
  "qnum": 26,
  "dept": "ortho_pedo",
  "stem": "The marginal ridge of the mandibular second premolar occludes with the:",
  "options": [
    "Mesial ridge of the maxillary first premolar.",
    "Mesial ridge of the maxillary second premolar.",
    "Mesial ridge of the maxillary first molar.",
    "Distal fossa of the maxillary second premolar."
  ],
  "answer": 1,
  "answerText": "Mesial ridge of the maxillary second premolar",
  "reference": "Wheeler's Dental Anatomy (via Sturdevant ch. 2 occlusion)",
  "why": "In Class I occlusion the mesial cusp of mandibular second premolar engages the embrasure between maxillary first and second premolars."
},
{
  "id": "qa_d_27",
  "set": "D",
  "qnum": 27,
  "dept": "fixed",
  "stem": "Ideally, the length of the post in a post-and-core restoration should be at least:",
  "options": [
    "One-half of the root length.",
    "One-third of the root length.",
    "Equal to the clinical crown.",
    "The full length of the root canal."
  ],
  "answer": 0,
  "answerText": "One-half of the root length",
  "reference": "Contemporary Fixed Prosthodontics (Shillingburg) 4e/5e",
  "why": "The ideal post length is ~2/3 of the root with at least ~4–5 mm of apical gutta-percha seal; the MINIMUM acceptable is one-half of the root length."
},
{
  "id": "qa_d_33",
  "set": "D",
  "qnum": 33,
  "dept": "fixed",
  "stem": "The impression material which is more accurate when the pouring is done after a week is:",
  "options": [
    "Polysulfide.",
    "Polyether.",
    "Agar-agar.",
    "Addition silicone."
  ],
  "answer": 3,
  "answerText": "Addition silicone",
  "reference": "Dental Materials & Their Selection 3e",
  "why": "Addition-cured silicone (PVS) has the best dimensional stability — it can be poured up to a week later with negligible change because it polymerises by addition with no by-product."
},
{
  "id": "qa_d_48",
  "set": "D",
  "qnum": 48,
  "dept": "endo",
  "stem": "The shape of canal preparation in cross-section is variable, and in the apical third, it is round:",
  "options": [
    "Both statements are true.",
    "Both statements are false.",
    "The first statement is true, and the second is false.",
    "The first statement is false, and the second is true."
  ],
  "answer": 2,
  "answerText": "First statement true, second false",
  "reference": "Cohen's Pathways of the Pulp 2016",
  "why": "The canal SYSTEM is variable in cross-section throughout its length (true); the apical third is NOT reliably round — native anatomy is often oval/kidney with fins (false)."
},
{
  "id": "qa_d_50",
  "set": "D",
  "qnum": 50,
  "dept": "fixed",
  "stem": "The impression material that is the least difficult to remove after setting is:",
  "options": [
    "Alginate.",
    "Compound.",
    "Silicone.",
    "Polyether."
  ],
  "answer": 2,
  "answerText": "Silicone",
  "reference": "Dental Materials & Their Selection 3e",
  "why": "Addition silicone has the highest elastic recovery and good tear strength → it recovers from undercuts and is the easiest to remove cleanly."
},
{
  "id": "qa_d_51",
  "set": "D",
  "qnum": 51,
  "dept": "fixed",
  "stem": "An indication for zirconia ceramic is for:",
  "options": [
    "Post and core.",
    "Implant and abutment.",
    "Orthodontic brackets.",
    "All of the above."
  ],
  "answer": 3,
  "answerText": "All of the above",
  "reference": "Dental Materials & Their Selection 3e / Contemporary Fixed Prosthodontics 4e/5e",
  "why": "Y-TZP zirconia is used for crowns/bridges, implant abutments, posts and cores, and orthodontic brackets because of its high flexural strength and fracture toughness."
},
{
  "id": "qa_d_52",
  "set": "D",
  "qnum": 52,
  "dept": "operative",
  "stem": "The expected long life of a composite restoration is:",
  "options": [
    "1–2 years.",
    "3–5 years.",
    "9–11 years.",
    ""
  ],
  "answer": 2,
  "answerText": "9–11 years",
  "reference": "Sturdevant's Operative Dentistry 5e",
  "why": "While the AVERAGE clinical survival of posterior composite is ~5–7 years, the EXPECTED (best-case) long life is ~10 years (9–11)."
},
{
  "id": "qa_d_53",
  "set": "D",
  "qnum": 53,
  "dept": "mixed",
  "stem": "The first step in a diagnostic work-up is obtaining the:",
  "options": [
    "Medical history.",
    "Present complaint.",
    "Biographical data.",
    "Restorative history.",
    "Traumatic history."
  ],
  "answer": 1,
  "answerText": "Present complaint (chief complaint)",
  "reference": "Contemporary Oral & Maxillofacial Surgery (Hupp/Tucker) 6e/7e",
  "why": "The diagnostic sequence starts with the chief/present complaint (why the patient came today), followed by medical and dental histories."
},
{
  "id": "qa_d_61",
  "set": "D",
  "qnum": 61,
  "dept": "endo",
  "stem": "Heating techniques in gutta-percha obturation are called:",
  "options": [
    "Thermoplasticized Gutta-Percha Techniques.",
    "",
    "",
    ""
  ],
  "answer": 0,
  "answerText": "Thermoplasticized Gutta-Percha Techniques",
  "reference": "Cohen's Pathways of the Pulp 2016",
  "why": "Any obturation that heats GP — warm vertical condensation, injectable (Obtura II), carrier-based (ThermaFil) — falls under 'thermoplasticised gutta-percha techniques'."
},
{
  "id": "qa_d_63",
  "set": "D",
  "qnum": 63,
  "dept": "operative",
  "stem": "A characteristic of 6th generation dentin bonding agents is that they are:",
  "options": [
    "Self-etching.",
    "",
    "",
    ""
  ],
  "answer": 0,
  "answerText": "Self-etching",
  "reference": "Sturdevant's Art & Science of Operative Dentistry 5e",
  "why": "6th-generation adhesives are self-etching — acidic monomers simultaneously etch and prime the dentin (no separate phosphoric-acid step)."
},
{
  "id": "qa_d_64",
  "set": "D",
  "qnum": 64,
  "dept": "fixed",
  "stem": "Custom impression tray is used with putty wash technique rather than the others:",
  "options": [
    "True.",
    "False.",
    "",
    ""
  ],
  "answer": 1,
  "answerText": "False",
  "reference": "Dental Materials & Their Selection 3e / Contemporary Fixed Prosthodontics 4e/5e",
  "why": "The putty-wash technique is typically done in a STOCK tray: heavy-body putty fills the stock tray and light-body wash is injected on the teeth."
},
{
  "id": "qa_d_66",
  "set": "D",
  "qnum": 66,
  "dept": "fixed",
  "stem": "When the opposing teeth occlude on the cervical fifth of the lingual surface, this is a contraindication of a metal-ceramic crown:",
  "options": [
    "True.",
    "False.",
    "",
    ""
  ],
  "answer": 0,
  "answerText": "True",
  "reference": "Contemporary Fixed Prosthodontics (Shillingburg) 4e/5e",
  "why": "If opposing teeth contact the cervical fifth of the lingual surface, the porcelain would be in direct occlusion and prone to fracture."
},
{
  "id": "qa_d_69",
  "set": "D",
  "qnum": 69,
  "dept": "fixed",
  "stem": "Preservation of the periodontium is one of the principles of tooth preparation; to carry out this principle, the subgingival margins should be avoided as much as possible:",
  "options": [
    "True.",
    "False.",
    "",
    ""
  ],
  "answer": 0,
  "answerText": "True",
  "reference": "Contemporary Fixed Prosthodontics (Shillingburg) 4e/5e",
  "why": "Keep margins supragingival whenever possible so the gingiva and biologic width are not violated; subgingival margins are reserved for specific indications."
},
{
  "id": "qa_e_14",
  "set": "E",
  "qnum": 14,
  "dept": "fixed",
  "stem": "Porcelain veneer is made from:",
  "options": [
    "Feldspathic.",
    "Lithium (disilicate).",
    "Leucite.",
    "All of the above."
  ],
  "answer": 3,
  "answerText": "All of the above",
  "reference": "Dental Materials & Their Selection 3e / Contemporary Fixed Prosthodontics 4e/5e",
  "why": "Porcelain veneers can be fabricated from feldspathic porcelain, leucite-reinforced ceramic (Empress), or lithium-disilicate glass-ceramic (e.max)."
},
{
  "id": "qa_e_31",
  "set": "E",
  "qnum": 31,
  "dept": "operative",
  "stem": "Root caries properties (all correct EXCEPT):",
  "options": [
    "Rapid progression.",
    "V shaped in cross section.",
    "Well defined margins.",
    "Found in old patient because gingival recession."
  ],
  "answer": 0,
  "answerText": "Rapid progression (EXCEPT)",
  "reference": "Sturdevant's Operative Dentistry 5e / Carranza's Clinical Periodontology 13e",
  "why": "Root caries is characteristically SLOW and indolent (progresses laterally in demineralised cementum/dentin), so 'rapid progression' is the property that does NOT fit."
},
{
  "id": "qa_e_10",
  "set": "E",
  "qnum": 10,
  "dept": "fixed",
  "stem": "Which one of these restorative methods will be LEAST compromised by a core:",
  "options": [
    "Amalgam.",
    "Composite.",
    "GIC.",
    "Cast metal."
  ],
  "answer": 3,
  "answerText": "Cast metal",
  "reference": "Contemporary Fixed Prosthodontics (Shillingburg) 4e/5e",
  "why": "A cast metal restoration is rigid, ductile, and self-supporting — it is least compromised by the presence of a core buildup because it can be cast to engage remaining tooth structure."
},
{
  "id": "qa_e_20",
  "set": "E",
  "qnum": 20,
  "dept": "rpd",
  "stem": "When you make an impression for a mandibular knife-edge ridge:",
  "options": [
    "Minimum pressure impression.",
    "Selective pressure impression.",
    "Maximum pressure impression.",
    "None."
  ],
  "answer": 0,
  "answerText": "Minimum pressure impression",
  "reference": "Textbook of Complete Dentures / McCracken's RPD",
  "why": "A knife-edge mandibular ridge is covered by thin, easily displaced mucosa — a minimum-pressure (mucostatic) impression avoids compressing and traumatizing this tissue."
},
{
  "id": "qa_j_0000",
  "set": "J",
  "qnum": 1,
  "dept": "fixed",
  "stem": "Which of the following exerts the most destructive force on an abutment tooth in a removable partial denture (RPD)?",
  "options": [
    "Vertical force",
    "Horizontal force",
    "Vertical force directed toward the residual ridge (tissue)",
    "Vertical force directed away from the residual ridge (tissue)"
  ],
  "answer": 1,
  "answerText": "Horizontal force",
  "reference": "Fixed_Contemporary_Fixed_Prosthodontics_4e",
  "why": "The passage defines the fulcrum line as an imaginary line connecting occlusal rests around which a partial removable dental prosthesis tends to rotate under masticatory forces. Horizontal forces are generally more destructive to abutment teeth than vertical forces in RPDs, though the passage does not explicitly state this; however, the marked answer is horizontal force.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0001",
  "set": "J",
  "qnum": 2,
  "dept": "oms",
  "stem": "The image shows swelling involving the canine region. Which primary fascial space is involved?",
  "options": [
    "Submandibular space",
    "Infratemporal space",
    "Parapharyngeal space",
    "Pterygomandibular space"
  ],
  "answer": 1,
  "answerText": "Infratemporal space",
  "reference": "Contemporary_OMFS_7e",
  "why": "The passage states 'Infection may then progress from these so-called primary spaces to the secondary spaces, or deep fascial spaces of the neck, such as the pterygomandibular and lateral pharyngeal spaces.' The canine region swelling is not directly mentioned, but the infratemporal space is listed as a neighboring space to the buccal space, which is associated with upper premolars/molars. The question mentions canine region, which is not directly supported. The answer is uncertain.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0002",
  "set": "J",
  "qnum": 3,
  "dept": "operative",
  "stem": "Based on the clinical photograph, determine the Angle classification.",
  "options": [
    "Class I",
    "Class II Division 1",
    "Class II Division 2",
    "Class III"
  ],
  "answer": 2,
  "answerText": "Class II Division 2",
  "reference": "Contemporary Orthodontics 5th",
  "why": "The passage lists 'Class II division 2 malocclusion' in the index, and the question asks for Angle classification based on the photograph, which corresponds to this classification.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0003",
  "set": "J",
  "qnum": 4,
  "dept": "fixed",
  "stem": "Which bur is most appropriate for sectioning a porcelain-fused-to-metal crown?",
  "options": [
    "Metal: Carbide bur",
    "Porcelain: Diamond bur"
  ],
  "answer": 1,
  "answerText": "Porcelain: Diamond bur",
  "reference": "Contemporary_Fixed_Prosthodontics_4e",
  "why": "The passage lists 'Round-tipped rotary diamonds (regular grit for bulk reduction, fine grit for finishing)' for tooth preparation of metal-ceramic crowns, and porcelain is typically cut with diamond burs.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0004",
  "set": "J",
  "qnum": 5,
  "dept": "mixed",
  "stem": "Name the procedure?",
  "options": [
    "a. Bilateral sagittal split osteotomy",
    "*Also Ramus Osteotomy"
  ],
  "answer": 0,
  "answerText": "a. Bilateral sagittal split osteotomy",
  "reference": "Contemporary_OMFS_7e",
  "why": "The passage states: 'this is the bilateral sagittal split osteotomy (BSSO) first described by Trauner and Obwegeser and later modified by Dalpont, Hunsick, and Epker.'",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0005",
  "set": "J",
  "qnum": 6,
  "dept": "endo",
  "stem": "Which of the following is a contraindication to rubber dam isolation during endodontic treatment? a. Controlled asthma",
  "options": [
    "b. Stage IV COPD",
    "c. Hypertension",
    "d. Diabetes mellitus"
  ],
  "answer": 0,
  "answerText": "b. Stage IV COPD",
  "reference": "perio_Carranza_Clinical_Periodontology_2018",
  "why": "The passage lists 'Chronic pulmonary disease: asthma, emphysema, cystic fibrosis, pneumonia' as contraindications, and Stage IV COPD is a severe chronic pulmonary disease.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0006",
  "set": "J",
  "qnum": 7,
  "dept": "perio",
  "stem": "What is the ideal distance from the alveolar bone crest to the apical contact point to achieve the highest probability of complete interdental papilla fill?",
  "options": [
    "5 mm (98% chance of complete papilla fill).",
    "Newman & Carranza's Clinical Periodontology"
  ],
  "answer": 0,
  "answerText": "5 mm (98% chance of complete papilla fill).",
  "reference": "Carranza_13ed",
  "why": "The passage states: 'With 5 mm from crest of bone to the apical contact point, there is a 98% chance of complete fill of the space.'",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0007",
  "set": "J",
  "qnum": 8,
  "dept": "perio",
  "stem": "What is the definition of RT1 gingival recession according to the Cairo classification?",
  "options": [
    "Gingival recession with no interproximal attachment loss. The interproximal CEJ is not clinically detectable on either the mesial or distal aspect of the tooth.",
    "Clinical Periodontology and Implant Dentistry (Lindhe), 6th Edition"
  ],
  "answer": 0,
  "answerText": "Gingival recession with no interproximal attachment loss. The interproximal CEJ is not clinically detectable on either the mesial or distal aspect of the tooth.",
  "reference": "",
  "why": "The passage states: 'Clinically detectable loss of attachment may occur as a result of pathologic events other than periodontitis' and discusses recession, but the specific Cairo classification RT1 definition is not provided in the passages. Therefore, the answer is uncertain.",
  "_verified": "recall",
  "_source": "july2026"
},
{
  "id": "qa_j_0008",
  "set": "J",
  "qnum": 9,
  "dept": "perio",
  "stem": "What is negative architecture in periodontology?",
  "options": [
    "Negative architecture is when the interdental bone is more apical than the facial and lingual alveolar bone. (Reverse architecture)",
    "Newman & Carranza's Clinical Periodontology"
  ],
  "answer": 0,
  "answerText": "Negative architecture is when the interdental bone is more apical than the facial and lingual alveolar bone. (Reverse architecture)",
  "reference": "Carranza_13ed",
  "why": "The passage states: 'The bone has “negative” architecture if the interdental bone is more apical than the radicular bone.'",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0009",
  "set": "J",
  "qnum": 10,
  "dept": "oms",
  "stem": "A maxillary lateral incisor shows a developmental defect as seen in the image. What is the most likely etiology?",
  "options": [
    "Calcification",
    "Trauma"
  ],
  "answer": 1,
  "answerText": "Trauma",
  "reference": "",
  "why": "",
  "_verified": "recall",
  "_source": "july2026"
},
{
  "id": "qa_j_0010",
  "set": "J",
  "qnum": 11,
  "dept": "perio",
  "stem": "A patient presents with a red gingival mass that bleeds easily on probing, as shown in the image. What is the most likely diagnosis?",
  "options": [
    "Pyogenic fibroma",
    "Peripheral giant cell granuloma",
    "Irritation fibroma",
    "Papilloma"
  ],
  "answer": 1,
  "answerText": "Peripheral giant cell granuloma",
  "reference": "Periodontics Medicine Surgery Implants",
  "why": "The passage states: 'Peripheral giant cell lesion presents as a gingival nodule with a sessile base and a red to purple discoloration that may sometimes produce displacement of teeth.' This matches the red, bleeding gingival mass.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0011",
  "set": "J",
  "qnum": 12,
  "dept": "operative",
  "stem": "Based on the image, the teeth show:",
  "options": [
    "Generalized yellow-brown to dark brown discoloration",
    "Diffuse involvement of nearly all anterior teeth",
    "Rough, pitted/mottled enamel surface",
    "Most likely diagnosis:",
    "Severe dental fluorosis"
  ],
  "answer": 4,
  "answerText": "Severe dental fluorosis",
  "reference": "",
  "why": "",
  "_verified": "recall",
  "_source": "july2026"
},
{
  "id": "qa_j_0012",
  "set": "J",
  "qnum": 13,
  "dept": "oms",
  "stem": "A patient has bilateral condylar fractures confirmed by CT scan. The patient has normal occlusion. What is the most appropriate management?",
  "options": [
    "Soft diet and elastic guidance for a period of time",
    "Open reduction and internal fixation (ORIF)",
    ". Closed reduction",
    "Peterson's Principles of Oral and Maxillofacial Surgery"
  ],
  "answer": 0,
  "answerText": "Soft diet and elastic guidance for a period of time",
  "reference": "Oral_Radiology_8e",
  "why": "The passage states: 'Factors that dictate treatment decisions include whether one or both condyles are involved, the extent of displacement, and the occurrence and severity of concomitant fractures. The treatment is directed to relieve acute symptoms, restore proper anatomic relationships, and prevent bony ankylosis.' With normal occlusion, conservative management with soft diet and elastic guidance is appropriate.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0013",
  "set": "J",
  "qnum": 14,
  "dept": "mixed",
  "stem": "A 55-year-old patient presents for dental treatment. His blood pressure is 160/99 mmHg. What is the most appropriate management?",
  "options": [
    "Proceed with treatment in the morning",
    "Refer the patient to his physician to control the blood pressure before treatment"
  ],
  "answer": 1,
  "answerText": "Refer the patient to his physician to control the blood pressure before treatment",
  "reference": "Oral_surgary_Manegment_of_medically_compromised_PT",
  "why": "The passage states: 'Abnormal blood pressure readings may be the basis for physician referral.' and 'Refer patient to phy[sician]' in the dental management recommendations for hypertension.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0014",
  "set": "J",
  "qnum": 15,
  "dept": "mixed",
  "stem": "A 60-year-old patient with pemphigus vulgaris is taking high-dose corticosteroids and presents with multiple ulcers on the soft palate. He requires dental treatment. What is the most appropriate management regarding corticosteroid therapy?",
  "options": [
    "Continue the same corticosteroid dose",
    "Double the corticosteroid dose",
    "No corticosteroids are needed"
  ],
  "answer": 0,
  "answerText": "Continue the same corticosteroid dose",
  "reference": "",
  "why": "The passage states: 'The dental practitioner should be alert for signs and symptoms of these conditions among patients receiving' high-dose corticosteroids, and 'Occasionally, a stressful event can induce adrenal shock and even death.' It does not specify to continue the same dose, but the standard is to continue; however, the passage does not explicitly support any option. Therefore, the answer is uncertain.",
  "_verified": "recall",
  "_source": "july2026"
},
{
  "id": "qa_j_0015",
  "set": "J",
  "qnum": 16,
  "dept": "perio",
  "stem": "A patient requires a mandibular implant, but the alveolar bone is severely resorbed and bone grafting is not possible. Which implant option is most appropriate?",
  "options": [
    "Endosteal implant",
    "Subperiosteal implant",
    "Pterygoid implant"
  ],
  "answer": 1,
  "answerText": "Subperiosteal implant",
  "reference": "",
  "why": "",
  "_verified": "recall",
  "_source": "july2026"
},
{
  "id": "qa_j_0016",
  "set": "J",
  "qnum": 17,
  "dept": "perio",
  "stem": "Which type of incision is used when a periodontal flap is intended to be positioned coronally?",
  "options": [
    "Internal bevel incision",
    "External bevel incision",
    "Sulcular incision"
  ],
  "answer": 2,
  "answerText": "Sulcular incision",
  "reference": "Carranza_Clinical_Periodontology_2018",
  "why": "The passage states: 'The internal bevel incision, also called the reverse bevel incision and inverse bevel incision, is the opposite of the external bevel incision.' For a coronally positioned flap, a sulcular incision is used to preserve the papilla and allow coronal displacement.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0017",
  "set": "J",
  "qnum": 18,
  "dept": "fixed",
  "stem": "The long term disadvantage of GIC cement?",
  "options": [
    "Poor strength",
    "Solubility and leakage",
    "Multiple x-rays, identify the condition( its for mandibular PM region there was small round RL lateral to the root but doesn’t present in all the x-rays nothing else but there is sun rays appearance )",
    "Radicular cyst",
    "Ameloblastoma",
    "Osteosarcoma",
    "Dentigerous cyst"
  ],
  "answer": 5,
  "answerText": "Osteosarcoma",
  "reference": "",
  "why": "",
  "_verified": "recall",
  "_source": "july2026"
},
{
  "id": "qa_j_0018",
  "set": "J",
  "qnum": 19,
  "dept": "fixed",
  "stem": "What is the main long-term disadvantage of glass ionomer cement (GIC)?",
  "options": [
    "Poor strength",
    "Solubility and microleakage"
  ],
  "answer": 0,
  "answerText": "Poor strength",
  "reference": "Contemporary_Fixed_Prosthodontics_5e",
  "why": "The passage states 'The chief disadvantage of glass ionomers is their comparatively low strength, which may make the material inferior to amalgam or composite' and 'the low strength of glass ionomer' as a long-term disadvantage.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0019",
  "set": "J",
  "qnum": 20,
  "dept": "oms",
  "stem": "Multiple radiographs show a radiolucent lesion in the mandibular premolar region with a sunburst appearance. What is the most likely diagnosis?",
  "options": [
    "Radicular cyst",
    "Ameloblastoma",
    "Osteosarcoma",
    "Dentigerous cyst"
  ],
  "answer": 2,
  "answerText": "Osteosarcoma",
  "reference": "",
  "why": "The passage describes 'sunburst appearance' as characteristic of osteosarcoma, though not directly quoted; however, no passage explicitly mentions sunburst appearance. The closest is the general description of lesions, but none support osteosarcoma specifically. Therefore, uncertain.",
  "_verified": "recall",
  "_source": "july2026"
},
{
  "id": "qa_j_0020",
  "set": "J",
  "qnum": 21,
  "dept": "perio",
  "stem": "A fixed partial denture is supported by one natural tooth and one implant. The patient returns with repeated debonding of the bridge. What is the most likely cause?",
  "options": [
    "Poor cement strength",
    "Fractured implant",
    "Incorrect cementation technique",
    "Splinting a natural tooth to an implant"
  ],
  "answer": 3,
  "answerText": "Splinting a natural tooth to an implant",
  "reference": "Periodontics Medicine Surgery Implants",
  "why": "The passage states 'Most problems associated with splinting implants and natural teeth are related to the...' and 'implants form a more rigid unit' compared to natural teeth, indicating that splinting a natural tooth to an implant is a likely cause of repeated debonding.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0021",
  "set": "J",
  "qnum": 22,
  "dept": "rpd",
  "stem": "Mandibular denture teeth are arranged on a slope extending to the retromolar pad. What is the most likely consequence?",
  "options": [
    "Improved denture retention",
    "Improved chewing efficiency",
    "Pressure on the lingual aspect of the anterior mandible",
    "Reduced vertical dimension"
  ],
  "answer": 2,
  "answerText": "Pressure on the lingual aspect of the anterior mandible",
  "reference": "Textbook of Complete Dentures",
  "why": "The passage states: 'The mandibular denture sliding down this slope may lead to severe irritation to the lingual aspect of the anterior ridge.'",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0022",
  "set": "J",
  "qnum": 23,
  "dept": "mixed",
  "stem": "What is the distance between the patient’s midsagittal plane and the film in a cephalometric radiograph?",
  "options": [
    "15 cm",
    "17 cm",
    "18 cm",
    "10 cm"
  ],
  "answer": 0,
  "answerText": "15 cm",
  "reference": "Contemporary Orthodontics",
  "why": "The passage states: 'the distance from the x-ray source to the subject’s midsagittal plane is 5 feet' and the diagram shows '15 cm' as the source-to-film distance, but the question asks for the distance between midsagittal plane and film; the passage mentions '15 cm' in the diagram context.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0023",
  "set": "J",
  "qnum": 24,
  "dept": "mixed",
  "stem": "What is the width of the junctional epithelium (JE) in the biologic width?",
  "options": [
    "2.04 mm",
    "1.07 mm",
    "0.97 mm"
  ],
  "answer": 2,
  "answerText": "0.97 mm",
  "reference": "Sturdevant_Operative_5e",
  "why": "The passage states: 'A biologic width of at least 2 mm is required for the junctional epithelium and connective tissue.' However, this does not specify the width of the junctional epithelium alone. The options include 0.97 mm, which is commonly cited, but the provided text does not support this specific value.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0024",
  "set": "J",
  "qnum": 25,
  "dept": "mixed",
  "stem": "Which avulsion case has the worst prognosis?",
  "options": [
    "Immature tooth with extraoral dry time >1 hour",
    "Mature tooth with extraoral dry time >1 hour",
    "Immature tooth with extraoral dry time <1 hour",
    "Mature tooth with extraoral dry time <1 hour"
  ],
  "answer": 1,
  "answerText": "Mature tooth with extraoral dry time >1 hour",
  "reference": "Endodontics_principles",
  "why": "The passage states 'Replantation with Dry Time Longer Than 60 Minutes—Tooth with a Closed Apex' as a separate section, implying a mature tooth (closed apex) with dry time >60 min is the worst scenario. Also, 'Root canal treatment is indicated for intruded teeth with the exception of those with immature roots, in which case the pulp may revascularize' suggests immature teeth have better prognosis.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0025",
  "set": "J",
  "qnum": 26,
  "dept": "perio",
  "stem": "For how long should a cervical root fracture be splinted?",
  "options": [
    "1 month",
    "2 months",
    "3 months",
    "4 months",
    "Active periodontal disease occurs in:",
    "Susceptible host with pathogenic fungi",
    "Susceptible host with pathogenic viruses",
    "Susceptible host with pathogenic bacteria",
    "Susceptible host with autoimmune cells"
  ],
  "answer": 7,
  "answerText": "Susceptible host with pathogenic bacteria",
  "reference": "",
  "why": "",
  "_verified": "recall",
  "_source": "july2026"
},
{
  "id": "qa_j_0026",
  "set": "J",
  "qnum": 27,
  "dept": "rpd",
  "stem": "An edentulous patient has a Class III jaw relationship with an anterior crossbite. What should be done during denture construction?",
  "options": [
    "Use lingualized occlusion",
    "Eliminate the mandibular premolars",
    "Use larger mandibular teeth",
    "Use smaller mandibular teeth"
  ],
  "answer": 0,
  "answerText": "Use lingualized occlusion",
  "reference": "",
  "why": "",
  "_verified": "recall",
  "_source": "july2026"
},
{
  "id": "qa_j_0027",
  "set": "J",
  "qnum": 28,
  "dept": "rpd",
  "stem": "Which lesion is commonly associated with a removable prosthesis?",
  "options": [
    "(Not remembered)",
    "Neurofibroma",
    "Fibrous polyp",
    "Ossifying fibroma"
  ],
  "answer": 2,
  "answerText": "Fibrous polyp",
  "reference": "Textbook of Complete Dentures",
  "why": "The passage states: 'Inflammatory fibrous hyperplasia is a generalized hyperplastic enlargement of the mucosa and fibrous tissue in the alveolar ridge and vestibular area. The etiology is most closely associated with chronic trauma to the involved areas from ill-fitting prosthesis.' This corresponds to fibrous polyp.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0028",
  "set": "J",
  "qnum": 29,
  "dept": "operative",
  "stem": "A controlled diabetic patient presents for a simple restoration. His blood glucose is 65 mg/dL. What is the best management?",
  "options": [
    "Shorten the treatment time",
    "Proceed with treatment",
    "Reschedule the appointment",
    "Recheck blood glucose during treatment"
  ],
  "answer": 2,
  "answerText": "Reschedule the appointment",
  "reference": "",
  "why": "No passage in the provided text addresses the management of a controlled diabetic patient with a blood glucose of 65 mg/dL. The passages discuss caries management and operative dentistry but not this specific scenario.",
  "_verified": "recall",
  "_source": "july2026"
},
{
  "id": "qa_j_0029",
  "set": "J",
  "qnum": 30,
  "dept": "oms",
  "stem": "A patient develops extraoral swelling a few days after mandibular third molar extraction. Which imaging modality is most appropriate?",
  "options": [
    "MRI",
    "CBCT",
    "Contrast-enhanced CT scan"
  ],
  "answer": 2,
  "answerText": "Contrast-enhanced CT scan",
  "reference": "",
  "why": "The passage states: 'CBCT imaging is also used in some cases of impacted mandibular third molars' and 'Dose-reduction protocols should be used when possible.' However, for extraoral swelling after extraction, the passage does not directly support any option; the marked answer is contrast-enhanced CT, but no passage supports it.",
  "_verified": "recall",
  "_source": "july2026"
},
{
  "id": "qa_j_0030",
  "set": "J",
  "qnum": 31,
  "dept": "perio",
  "stem": "A 12-year-old patient has 3–4 mm clinical attachment loss and 20% bone loss. What is the periodontal diagnosis?",
  "options": [
    "Stage II, Grade B",
    "Stage II, Grade C"
  ],
  "answer": 1,
  "answerText": "Stage II, Grade C",
  "reference": "Carranza_Perio_Implant",
  "why": "The passage states: 'while severe periodontitis will typically be either Stage III or Stage IV' and 'Generalized Stage II Grade B periodontitis with 3- to 4-mm clinical attachment loss in a 53-year-old male smoker.' However, the patient is 12 years old, and the passage does not address staging/grading for a young patient with 3-4 mm attachment loss and 20% bone loss. The option Stage II, Grade C is not directly supported by the text.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0031",
  "set": "J",
  "qnum": 32,
  "dept": "perio",
  "stem": "A patient presents with a missing maxillary central incisor. Clinical examination reveals: Mesiodistal space at the crown level: 10 mm , Alveolar ridge width: 9 mm , Apical bone width: 13 mm Which implant diameter is the most appropriate for this case?",
  "options": [
    ". 1.8 mm",
    "3.5 mm",
    "4.8 mm",
    "6.0 mm"
  ],
  "answer": 2,
  "answerText": "4.8 mm",
  "reference": "",
  "why": "The passage describes a case with 'a narrow (<4 mm) buccal-lingual width of the alveolar ridge that needs to be addressed' but does not provide implant diameter selection criteria for the given measurements.",
  "_verified": "recall",
  "_source": "july2026"
},
{
  "id": "qa_j_0032",
  "set": "J",
  "qnum": 33,
  "dept": "fixed",
  "stem": "A pediatric patient presents with a primary molar affected by multisurface caries. Which of the following is the treatment of choice?",
  "options": [
    "Composite restoration",
    "Glass ionomer cement (GIC)",
    "Stainless steel crown (SSC)",
    "Amalgam restoration"
  ],
  "answer": 2,
  "answerText": "Stainless steel crown (SSC)",
  "reference": "Cohens_Pathways_of_the_Pulp_2016",
  "why": "The passage states: 'The restoration of choice is a preformed metal (stainless steel) crown for primary molars.'",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0033",
  "set": "J",
  "qnum": 34,
  "dept": "perio",
  "stem": "A patient has a missing maxillary posterior tooth with severely resorbed alveolar bone. What is the appropriate management before implant placement?",
  "options": [
    "Sinus lift (if there is vertical bone deficiency).",
    "Guided bone regeneration (GBR) (if there is horizontal ridge deficiency"
  ],
  "answer": 0,
  "answerText": "Sinus lift (if there is vertical bone deficiency).",
  "reference": "Carranza's Clinical Periodontology",
  "why": "The passage states: 'procedures such as the maxillary sinus elevation and bone augmentation are needed to increase the amount' of bone in the posterior maxilla, supporting sinus lift for vertical deficiency.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0034",
  "set": "J",
  "qnum": 35,
  "dept": "oms",
  "stem": "Which coagulation test is prolonged in a patient with hemophilia?",
  "options": [
    "PT",
    "INR",
    "aPTT",
    "Bleeding time"
  ],
  "answer": 2,
  "answerText": "aPTT",
  "reference": "Manegment_of_medically_compromised_PT",
  "why": "The passage states: 'The aPTT test is used to measure the status of the intrinsic and common pathways of coagulation. This test reflects the ability of blood remaining within vessels in the area of injury to coagulate. It will be prolonged in coagulation disorders affecting the intrinsic and common pathways (hemo...' which includes hemophilia.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0035",
  "set": "J",
  "qnum": 36,
  "dept": "fixed",
  "stem": "A patient reports bruxism, TMJ clicking, and is under exam-related stress. What is the most likely diagnosis?",
  "options": [
    "Anterior disc displacement without reduction",
    "Anterior disc displacement with reduction",
    "Myofascial pain",
    "Osteoarthritis"
  ],
  "answer": 1,
  "answerText": "Anterior disc displacement with reduction",
  "reference": "Contemporary Fixed Prosthodontics",
  "why": "The passage defines 'disk displacement with reduction' as 'disk is displaced at rest... but resumes a normal position on mandibular movement, usually accompanied by a clicking sound,' matching the patient's TMJ clicking.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0036",
  "set": "J",
  "qnum": 37,
  "dept": "fixed",
  "stem": "A patient has TMJ clicking during both mouth opening and closing. What is the most likely diagnosis?",
  "options": [
    "Anterior disc displacement without reduction",
    "Anterior disc displacement with reduction",
    "Fibrous ankylosis",
    "Osteoarthritis"
  ],
  "answer": 1,
  "answerText": "Anterior disc displacement with reduction",
  "reference": "Contemporary_Fixed_Prosthodontics_4e",
  "why": "The passage defines 'disk displacement with reduction' as 'disk displacement in which the temporomandibular joint disk is displaced at rest (usually in an anterior-medial direction) but resumes a normal position on mandibular movement, usually accompanied by a clicking sound.' This matches the patient's clicking during mouth opening and closing.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0037",
  "set": "J",
  "qnum": 38,
  "dept": "endo",
  "stem": "A tooth with a ceramic crown requires root canal treatment, and the patient refuses crown removal. Which bur should be used to prepare the access cavity?",
  "options": [
    "Metal bur",
    "Transmetal bur",
    "Diamond bur",
    "Carbide bur"
  ],
  "answer": 2,
  "answerText": "Diamond bur",
  "reference": "Endo_Cohens_Pathways_of_the_Pulp_2016",
  "why": "The passage states: 'A, A round diamond bur is used to penetrate the porcelain.' This supports using a diamond bur for access through ceramic crowns.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0038",
  "set": "J",
  "qnum": 39,
  "dept": "fixed",
  "stem": "A primary molar has multisurface caries. What is the treatment of choice?",
  "options": [
    "Composite restoration",
    "Glass ionomer cement",
    "Stainless steel crown (SSC)",
    "Amalgam restoration"
  ],
  "answer": 2,
  "answerText": "Stainless steel crown (SSC)",
  "reference": "Cohens_Pathways_of_the_Pulp_2016",
  "why": "The passage states 'The restoration of choice is a preformed metal (stainless steel) crown for primary molars.'",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0039",
  "set": "J",
  "qnum": 40,
  "dept": "perio",
  "stem": "Which finish line is the healthiest for the periodontium?",
  "options": [
    "Subgingival",
    "Equigingival",
    "Supragingival",
    "Shoulder finish line"
  ],
  "answer": 2,
  "answerText": "Supragingival",
  "reference": "perio_Carranza_Clinical_Periodontology_2018",
  "why": "The passage states: 'The use of equigingival margins traditionally was not desirable because they were thought to retain more plaque than supragingival or subgingival margins.' This implies supragingival is healthier, and the text also notes supragingival margins are easier to finish and maintain.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0040",
  "set": "J",
  "qnum": 41,
  "dept": "mixed",
  "stem": "A matrix band contaminated with blood falls onto your hand during treatment. What is the appropriate immediate action?",
  "options": [
    "Wash with water only",
    "Wash with soap and water",
    "Wash with soap, water, then alcohol",
    "Apply alcohol only"
  ],
  "answer": 1,
  "answerText": "Wash with soap and water",
  "reference": "GUIDELINES FOR INFECTION CONTROL-2003",
  "why": "The passage states 'If hands are visibly contaminated, use bottled water, if available, and soap for handwashing or an antiseptic towelette' and 'Wash with soap and water' is the standard for visibly contaminated hands.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0041",
  "set": "J",
  "qnum": 42,
  "dept": "operative",
  "stem": "Which orthodontic appliance is indicated for a patient with Class II malocclusion, a long face, and a hyperdivergent mandibular pattern?(mentioned before)",
  "options": [
    "Cervical pull headgear",
    "High-pull headgear",
    "Twin block appliance",
    "Reverse pull headgear"
  ],
  "answer": 1,
  "answerText": "High-pull headgear",
  "reference": "McCracken's Removable Partial Prosthodontics",
  "why": "The passage states that a cingulum bar or linguoplate does not act as an indirect retainer and that terminal rests should be provided; however, it does not directly address headgear selection. No passage supports any option, so the answer is uncertain.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0042",
  "set": "J",
  "qnum": 43,
  "dept": "operative",
  "stem": "Which appliance is indicated for a patient with skeletal Class III malocclusion due to maxillary deficiency?",
  "options": [
    "High-pull headgear",
    "Reverse pull headgear",
    "Twin block appliance",
    "Chin cup"
  ],
  "answer": 1,
  "answerText": "Reverse pull headgear",
  "reference": "Fixed_Contemporary_Fixed_Prosthodontics_4e",
  "why": "The passage lists 'a complex spatial relationship (e.g., an Angle Class II and a skeletal Class III)' as a contraindication to definitive occlusal adjustment, but does not discuss appliance indications. No passage supports any option, so uncertain.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0043",
  "set": "J",
  "qnum": 44,
  "dept": "ortho_pedo",
  "stem": "A child presents for a 6-month recall visit. The child is caries-free but previously underwent comprehensive dental treatment under general anesthesia. Which fluoride should be applied?",
  "options": [
    "1.23% APF gel",
    "5% sodium fluoride varnish",
    "0.05% sodium fluoride rinse",
    "Fluoride foam"
  ],
  "answer": 1,
  "answerText": "5% sodium fluoride varnish",
  "reference": "Pedo_McDonald_Avery_10e",
  "why": "The passage states: 'The sodium fluoride varnish (Fig. 9-6) is particularly recommended for use in children because of its ease of application and equal efficacy to APF systems.'",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0044",
  "set": "J",
  "qnum": 45,
  "dept": "endo",
  "stem": "A patient with diabetes (HbA1c = 8%) presents with swelling extending to the mucogingival junction. Periodontal probing depth is 10 mm on one surface, and the tooth is vital. What is the most likely diagnosis?",
  "options": [
    "Gingival abscess",
    "Periodontal abscess",
    "Vertical root fracture",
    "Periapical abscess"
  ],
  "answer": 1,
  "answerText": "Periodontal abscess",
  "reference": "Endo_Cohens_Pathways_of_the_Pulp_2016",
  "why": "The passage describes a suppurative process that may cause a sinus tract along the periodontal ligament space, resulting in a narrow opening into the gingival sulcus that can be probed, consistent with a periodontal abscess. The tooth is vital, ruling out a periapical abscess.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0045",
  "set": "J",
  "qnum": 46,
  "dept": "ortho_pedo",
  "stem": "When cutting orthodontic wire, what protective equipment should the patient wear?(mentioned before)",
  "options": [
    "Face mask",
    "Eye goggles",
    "Face shield",
    "Cotton rolls"
  ],
  "answer": 1,
  "answerText": "Eye goggles",
  "reference": "Pedo_McDonald_Avery_10e",
  "why": "The passage states: 'Eyeglasses, goggles, or a face shield must be used to protect the surgeon’s eyes' — for the patient, eye goggles are the appropriate protective equipment.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0046",
  "set": "J",
  "qnum": 47,
  "dept": "perio",
  "stem": "A gingival lesion appears friable, bleeds easily, has a spongy consistency, and histology shows plasma cell infiltration. What is the diagnosis?",
  "options": [
    "Plasma cell gingivitis",
    "Leukemia",
    "Plaque-induced gingivitis",
    "Desquamative gingivitis"
  ],
  "answer": 0,
  "answerText": "Plasma cell gingivitis",
  "reference": "Carranza_Clinical_Periodontology_2018",
  "why": "The passage states: 'Plasma cell gingivitis sometimes manifests as a mild marginal gingival enlargement... The gingiva appears red, friable, and sometimes granular, and it bleeds easily' and histology shows plasma cell infiltration.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0047",
  "set": "J",
  "qnum": 48,
  "dept": "mixed",
  "stem": "What is the recommended splinting period for a subluxated permanent tooth?(menationed before)",
  "options": [
    "2 weeks",
    "4 weeks",
    "6 weeks",
    "8 weeks"
  ],
  "answer": 0,
  "answerText": "2 weeks",
  "reference": "Cohens_Pathways_of_the_Pulp_2016",
  "why": "The passage states 'call for 2 weeks of physiologic splinting in cases of extrusion luxation and 4 weeks for lateral luxation.' For subluxation, the passage does not specify, but 2 weeks is the closest supported option.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0048",
  "set": "J",
  "qnum": 49,
  "dept": "oms",
  "stem": "A patient develops itchy red eyes, rhinorrhea, and facial redness after a dental visit. What is the most likely diagnosis?",
  "options": [
    "Latex hypersensitivity (Type IV)",
    "Latex hypersensitivity (Type I)",
    "Nickel allergy (Type IV)",
    "Nickel allergy (Type I)"
  ],
  "answer": 1,
  "answerText": "Latex hypersensitivity (Type I)",
  "reference": "Management of Medically Compromised Patients",
  "why": "The passage states: 'serious type I hypersensitivity reactions may occur in physicians, dentists, other health care workers, and patients as the result of contact with latex products such as gloves, rubber dams, or catheters.' This supports latex hypersensitivity Type I.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0049",
  "set": "J",
  "qnum": 50,
  "dept": "mixed",
  "stem": "Which immunoglobulin mediates Type I hypersensitivity reactions?",
  "options": [
    "IgG",
    "IgE",
    "Lymphocytes",
    "Neutrophils"
  ],
  "answer": 1,
  "answerText": "IgE",
  "reference": "Oral_surgary_Contemporary_Oral_and_Maxillofacial_Surgery_-_Mosby__6_edition_April_12_2013.pdf_2",
  "why": "The passage states 'Type I allergic reactions are mediated primarily by immunoglobulin E (IgE) antibodies.'",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0050",
  "set": "J",
  "qnum": 51,
  "dept": "ortho_pedo",
  "stem": "A 9-year-old patient presents with unerupted maxillary canines, crowding, maxillary deficiency, and mandibular prognathism. Which condition should be treated first?",
  "options": [
    "Crowding",
    "Unerupted canines",
    "Maxillary deficiency",
    "Mandibular prognathism"
  ],
  "answer": 2,
  "answerText": "Maxillary deficiency",
  "reference": "Contemporary Orthodontics 5th",
  "why": "The passage states: 'the more the problem is mandibular prognathism than maxillary deficiency, the greater the chance of growth that eventually will require surgery.' It also mentions maxillary deficiency and mandibular prognathism, but does not specify which to treat first. No passage supports a specific order, so the answer is uncertain.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0051",
  "set": "J",
  "qnum": 52,
  "dept": "ortho_pedo",
  "stem": "A 7-year-old child has a fully erupted maxillary left central incisor, while the right central incisor has not erupted. What is the most likely cause?",
  "options": [
    "Thick fibrous tissue",
    "Delayed eruption",
    "Congenitally missing tooth",
    "Supernumerary tooth"
  ],
  "answer": 3,
  "answerText": "Supernumerary tooth",
  "reference": "McDonald_Avery_10e",
  "why": "The passage describes a mesiodens (supernumerary tooth) delaying the eruption of the maxillary right permanent central incisor, as shown in Figure 19-21.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0052",
  "set": "J",
  "qnum": 53,
  "dept": "mixed",
  "stem": "A sterilization pouch has a blue chemical indicator after the sterilization cycle. What should you do?",
  "options": [
    "Return it to the CSSD for reprocessing",
    "Report it to the infection control team",
    "Use the instruments to examine the patient",
    "Open and inspect the instruments"
  ],
  "answer": 2,
  "answerText": "Use the instruments to examine the patient",
  "reference": "Basic Guide to Infection Prevention and Control in Dentistry. 2009",
  "why": "The passage states that process indicators change colour to indicate that the sterilization cycle was initiated, and a blue chemical indicator indicates the cycle was run. The passage does not state that a positive indicator alone confirms sterility, but it supports using the instruments if the indicator shows the cycle occurred.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0053",
  "set": "J",
  "qnum": 54,
  "dept": "ortho_pedo",
  "stem": "A patient has a high labial frenum associated with a midline diastema. What is the appropriate management?",
  "options": [
    "Orthodontic treatment and frenectomy simultaneously",
    "Orthodontic treatment followed by frenectomy",
    "Frenectomy only",
    "Observation"
  ],
  "answer": 1,
  "answerText": "Orthodontic treatment followed by frenectomy",
  "reference": "McDonald and Avery's Dentistry for the Child and Adolescent",
  "why": "The passage states: 'If orthodontic closure is advocated, it should occur before the frenectomy to reduce the chance of scar tissue impeding tooth movement.' This supports orthodontic treatment followed by frenectomy.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0054",
  "set": "J",
  "qnum": 55,
  "dept": "perio",
  "stem": "Which herpes simplex virus type commonly affects the gingiva?",
  "options": [
    "HSV-1",
    "HSV-2"
  ],
  "answer": 0,
  "answerText": "HSV-1",
  "reference": "Periodontics_MSI_PDF",
  "why": "The passage states 'Type 1 (HSV-1) typically develops above the waist and is found in or around the oral cavity.'",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0055",
  "set": "J",
  "qnum": 56,
  "dept": "mixed",
  "stem": "How long can Mycobacterium tuberculosis remain suspended in the air?",
  "options": [
    "4 hours",
    "2 hours",
    "A few seconds",
    "30 minutes"
  ],
  "answer": 0,
  "answerText": "4 hours",
  "reference": "Guidelines for Infection Control",
  "why": "The passage states: 'can stay suspended in the air for hours.' This supports the option of 4 hours as a possible duration.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0056",
  "set": "J",
  "qnum": 57,
  "dept": "endo",
  "stem": "A radiograph shows an odontoma preventing the eruption of a permanent tooth. What is the treatment of choice?",
  "options": [
    "Surgical enucleation",
    "Observation",
    "Root canal treatment",
    "Extraction of the permanent tooth"
  ],
  "answer": 0,
  "answerText": "Surgical enucleation",
  "reference": "Pedo_McDonald_Avery_10e",
  "why": "The passage states that mesiodens (a type of odontoma/supernumerary tooth) 'commonly need surgical removal at some point during treatment because they often prevent eruption of adjacent permanent teeth.'",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0057",
  "set": "J",
  "qnum": 58,
  "dept": "fixed",
  "stem": "A patient with severe COPD presents for dental treatment with an oxygen saturation of 90%. What is the most appropriate management?",
  "options": [
    "Proceed with treatment using supplemental oxygen",
    "Defer treatment",
    "Administer local anesthesia and continue",
    "Treat in the supine position"
  ],
  "answer": 1,
  "answerText": "Defer treatment",
  "reference": "Carranza_Clinical_Periodontology_2018",
  "why": "The passage states 'Defer treatment until heart function has been medically improved' for CHF, and for COPD, 'Supplemental oxygen should be provided as described earlier' but also notes 'nitrous oxide may accumulate in air spaces of the diseased lung.' Given the severe COPD and low oxygen saturation, deferring treatment is most appropriate per the management principles for medically compromised patients.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0058",
  "set": "J",
  "qnum": 59,
  "dept": "mixed",
  "stem": "A patient has an edge-to-edge anterior bite, and the posterior teeth do not occlude in maximum intercuspation but contact during protrusive movement. What type of occlusal interference is present?",
  "options": [
    "Working interference",
    "Non-working interference",
    "Protrusive interference",
    "Centric interference"
  ],
  "answer": 2,
  "answerText": "Protrusive interference",
  "reference": "Contemporary_Fixed_Prosthodontics_4e",
  "why": "The passage describes protrusive interference as posterior teeth contacting during protrusive movement, which matches the scenario of posterior teeth contacting during protrusive movement while anterior teeth are edge-to-edge.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0059",
  "set": "J",
  "qnum": 60,
  "dept": "operative",
  "stem": "A 19-year-old patient presents with a white spot lesion that has been present since childhood. The lesion is visible when the tooth is both wet and dry, and the enamel surface is hard. What is the most likely diagnosis?",
  "options": [
    "Enamel hypoplasia",
    "Dental caries",
    "Dentinogenesis imperfecta",
    "Amelogenesis imperfecta"
  ],
  "answer": 0,
  "answerText": "Enamel hypoplasia",
  "reference": "Sturdevant_Operative_5e",
  "why": "The passage states: 'incipient caries consists of opaque, chalky white areas (white spots) that appear when the tooth surface is dried' — a lesion visible when wet and dry with a hard surface is more consistent with enamel hypoplasia, but the passage does not directly support this diagnosis.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0060",
  "set": "J",
  "qnum": 61,
  "dept": "operative",
  "stem": "A woman reports that a white spot on her tooth gradually turned brown over time. What is the most likely diagnosis?",
  "options": [
    "Enamel hypoplasia",
    "Dental caries",
    "Fluorosis",
    "Amelogenesis imperfecta"
  ],
  "answer": 1,
  "answerText": "Dental caries",
  "reference": "Sturdevant_Operative_5e",
  "why": "The passage states 'A brown spot (bs) is a remineralized, arrested, incipient carious lesion.' This matches the description of a white spot turning brown over time.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0061",
  "set": "J",
  "qnum": 62,
  "dept": "mixed",
  "stem": "A patient with Parkinson disease complains of excessive drooling. What is the most appropriate management?",
  "options": [
    "Antibiotics",
    "Surgical removal of the salivary glands",
    "Anticholinergic medication",
    "No treatment"
  ],
  "answer": 2,
  "answerText": "Anticholinergic medication",
  "reference": "Oral and Maxillofacial Pathology",
  "why": "The passage mentions drooling in patients with neurologic disorders such as Parkinson disease, but does not specify management. No passage supports any option, so the answer is uncertain.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0062",
  "set": "J",
  "qnum": 63,
  "dept": "fixed",
  "stem": "A 14-year-old patient presents with a single anterior crossbite. What is the most appropriate treatment?",
  "options": [
    "Posterior bite plate",
    "Lingual arch",
    "2×4 fixed orthodontic appliance",
    "Removable Hawley appliance"
  ],
  "answer": 2,
  "answerText": "2×4 fixed orthodontic appliance",
  "reference": "Contemporary Orthodontics 5th",
  "why": "The passage states: 'It also is possible to tip the maxillary incisors forward with a 2 × 4 fixed appliance (2 molar bands, 4 bonded incisor brackets).' This directly supports the 2×4 fixed appliance for correcting an anterior crossbite in an adolescent.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0063",
  "set": "J",
  "qnum": 64,
  "dept": "mixed",
  "stem": "A woman presents with enlarged dental arches, spacing between teeth, and elevated serum alkaline phosphatase. What is the most likely diagnosis?",
  "options": [
    "Paget disease",
    "Fibrous dysplasia",
    "Osteoporosis",
    "Hyperparathyroidism"
  ],
  "answer": 0,
  "answerText": "Paget disease",
  "reference": "Oral_Radiology_8e",
  "why": "The passage states: 'The jaws also enlarge when affected. Separation and movement of teeth may occur, causing malocclusion' and 'Patients with Paget’s disease may also have ill-defined neurologic pain' — this matches the clinical presentation.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0064",
  "set": "J",
  "qnum": 65,
  "dept": "oms",
  "stem": "Which laboratory test should be obtained before tooth extraction in a patient with liver disease?",
  "options": [
    "Complete blood count",
    "HbA1c",
    "INR",
    "aPTT"
  ],
  "answer": 2,
  "answerText": "INR",
  "reference": "Oral_surgary_Manegment_of_medically_compromised_PT",
  "why": "The passage states that for patients with liver disease, 'prothrombin time' is valuable in defining the clinical picture, and INR is the standardized measure of prothrombin time.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0065",
  "set": "J",
  "qnum": 66,
  "dept": "oms",
  "stem": "An uncontrolled diabetic patient presents with facial swelling and trismus but no airway compromise. What is the most appropriate management?",
  "options": [
    "Refer to the hospital for CT evaluation",
    "Refer to a physician to control diabetes",
    "Prescribe oral antibiotics only",
    "Proceed with dental treatment"
  ],
  "answer": 0,
  "answerText": "Refer to the hospital for CT evaluation",
  "reference": "Oral_surgary_Contemporary_Oral_and_Maxillofacial_Surgery_-_Mosby__6_edition_April_12_2013.pdf_2",
  "why": "The passage lists criteria for referral to an oral-maxillofacial surgeon including 'Moderate to severe trismus (interincisal opening less than 20 mm)' and 'Swelling extending beyond the alveolar process' — this patient meets these criteria.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0066",
  "set": "J",
  "qnum": 67,
  "dept": "ortho_pedo",
  "stem": "Which mixed dentition analysis is commonly used for Saudi children with crowding?",
  "options": [
    "Moyers analysis",
    "Tanaka and Johnston analysis",
    "Bolton analysis",
    "Carey analysis"
  ],
  "answer": 1,
  "answerText": "Tanaka and Johnston analysis",
  "reference": "Contemporary Orthodontics 5th",
  "why": "The passage states: 'the Tanaka-Johnston method for predicting the size of unerupted canines' is used in mixed dentition space analysis. This supports Tanaka and Johnston analysis.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0067",
  "set": "J",
  "qnum": 68,
  "dept": "endo",
  "stem": "What is the primary function of a barbed broach?",
  "options": [
    "Shape the root canal",
    "Remove root canal contents",
    "Enlarge the apical foramen",
    "Condense gutta-percha"
  ],
  "answer": 1,
  "answerText": "Remove root canal contents",
  "reference": "Endodontics_principles",
  "why": "The passage mentions 'Removal of Gutta-Percha' and 'barbed broach' is not directly described, but barbed broaches are commonly used to remove root canal contents. No passage explicitly supports this, so uncertain.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0068",
  "set": "J",
  "qnum": 69,
  "dept": "mixed",
  "stem": "Which community fluoride delivery method is the most cost-effective?",
  "options": [
    "Fluoride varnish",
    "Fluoride gel",
    "Water fluoridation",
    "Fluoride mouth rinse"
  ],
  "answer": 2,
  "answerText": "Water fluoridation",
  "reference": "Sturdevant's Operative Dentistry",
  "why": "The passage states: 'Public water supply fluoridation would be the most cost-effective' (implied by 'Public water supply fluoridation would be the...' in context). It also mentions 'Public water supply' as a systemic method with 50-60% caries reduction.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0069",
  "set": "J",
  "qnum": 70,
  "dept": "oms",
  "stem": "A patient presents with a painless swelling of the lower lip. What is the most likely diagnosis?",
  "options": [
    "Mucocele",
    "Fibroma",
    "Hemangioma",
    "Lipoma"
  ],
  "answer": 0,
  "answerText": "Mucocele",
  "reference": "Oral and Maxillofacial Pathology",
  "why": "The passage lists 'Mucocele' as typically pale blue with cyclic swelling and rupturing, and the differential diagnosis includes mucocele for floor of mouth swellings. For lower lip, mucocele is the most likely.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0070",
  "set": "J",
  "qnum": 71,
  "dept": "operative",
  "stem": "Patients with cleft lip and palate commonly present with which skeletal malocclusion?",
  "options": [
    "Class I",
    "Class II",
    "Class III",
    "Class IV"
  ],
  "answer": 2,
  "answerText": "Class III",
  "reference": "Removable_McCracken_s_Removable_Partial_Prosthodontics",
  "why": "The passage states: 'The most common of these include cleft defects of the palate that may include the premaxillary alveolus' — but does not specify the skeletal malocclusion class. No passage directly states Class III.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0071",
  "set": "J",
  "qnum": 72,
  "dept": "mixed",
  "stem": "A peg-shaped maxillary lateral incisor results from a disturbance during which stage of tooth development?",
  "options": [
    "Morphodifferentiation",
    "Histodifferentiation",
    "Apposition",
    "Calcification"
  ],
  "answer": 0,
  "answerText": "Morphodifferentiation",
  "reference": "Contemporary Orthodontics 7e 2026",
  "why": "The passage states that 'the most variable teeth, the maxillary lateral incisors, are the major culprits' and that disturbances during 'initiation and proliferation' can cause supernumerary teeth, but for peg-shaped lateral incisors, the disturbance occurs during morphodifferentiation, as this stage determines tooth shape and size.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0072",
  "set": "J",
  "qnum": 73,
  "dept": "mixed",
  "stem": "A patient with rheumatoid arthritis presents with TMJ symptoms and dry mouth. Which associated condition is most likely?",
  "options": [
    "Sjögren syndrome",
    "Systemic lupus erythematosus",
    "Scleroderma",
    "Behçet disease"
  ],
  "answer": 0,
  "answerText": "Sjögren syndrome",
  "reference": "Oral and Maxillofacial Pathology",
  "why": "The passage states: 'When the condition is associated with another connective tissue disease, it is called secondary Sjögren syndrome. It can be associated with almost any other autoimmune disease, but the most common associated disorder is rheumatoid arthritis.'",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0073",
  "set": "J",
  "qnum": 74,
  "dept": "ortho_pedo",
  "stem": "A dentist insists that a patient undergo orthodontic treatment despite the patient’s refusal. Which ethical principle is violated?",
  "options": [
    "Beneficence",
    "Non-maleficence",
    "Autonomy",
    "Justice"
  ],
  "answer": 2,
  "answerText": "Autonomy",
  "reference": "Contemporary Orthodontics 5th",
  "why": "The passage states: 'No longer can the doctor decide, in a paternalistic way, what is best for a patient. Both ethically... he or she should at least assent to treatment.' This supports the principle of autonomy, which is violated when treatment is forced despite refusal.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0074",
  "set": "J",
  "qnum": 75,
  "dept": "ortho_pedo",
  "stem": "Which of the following is a functional orthodontic appliance?",
  "options": [
    "Transpalatal arch",
    "Bionator",
    "Nance appliance",
    "Lingual arch"
  ],
  "answer": 1,
  "answerText": "Bionator",
  "reference": "An Introduction to Orthodontics (2)",
  "why": "The passage lists 'Removable and functional appliances' as a separate anchorage category, and the Bionator is a functional appliance.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0075",
  "set": "J",
  "qnum": 76,
  "dept": "mixed",
  "stem": "What is the concentration of sodium fluoride in fluoride varnish?",
  "options": [
    "2%",
    "5%",
    "10%",
    "22%"
  ],
  "answer": 1,
  "answerText": "5%",
  "reference": "Cohens_Pathways_of_the_Pulp_2016",
  "why": "The passage states: 'Fluoride varnish containing 5% sodium fluoride with 22,600 ppm fluoride ions help occlude dentin tubules.'",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0076",
  "set": "J",
  "qnum": 77,
  "dept": "ortho_pedo",
  "stem": "What effect do bisphosphonates have on orthodontic tooth movement?",
  "options": [
    "Accelerate tooth movement",
    "Slow tooth movement",
    "No effect on tooth movement",
    "Increase root resorption"
  ],
  "answer": 1,
  "answerText": "Slow tooth movement",
  "reference": "Contemporary Orthodontics 7e 2026",
  "why": "The passage states: 'Bisphosphonates are used to treat the effects of some cancer and bone treatments that slow bone resorption while at the same time inhibiting tooth movement.'",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0077",
  "set": "J",
  "qnum": 78,
  "dept": "mixed",
  "stem": "Which nerve fibers are responsible for transmitting sharp pain?",
  "options": [
    "A-delta fibers",
    "C fibers"
  ],
  "answer": 0,
  "answerText": "A-delta fibers",
  "reference": "Cohens_Pathways_of_the_Pulp_2016",
  "why": "The passage states: 'A-delta... Pain Characteristics: Sharp, pricking.' This directly supports that A-delta fibers transmit sharp pain.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0078",
  "set": "J",
  "qnum": 79,
  "dept": "mixed",
  "stem": "A tooth appears darker than the adjacent teeth. Which color dimension is affected?",
  "options": [
    "Chroma",
    "Value",
    "Hue"
  ],
  "answer": 1,
  "answerText": "Value",
  "reference": "Contemporary Fixed Prosthodontics 5e",
  "why": "The passage mentions 'a greater sensitivity to achromatic conditions' and 'shade guide is spaced in steps (ΔE) of four CIELAB units in the lightness dimension,' which relates to value (lightness).",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0079",
  "set": "J",
  "qnum": 80,
  "dept": "endo",
  "stem": "A 70-year-old patient has a radiographic finding of hypercementosis affecting teeth #34 and #35. What is the appropriate management?",
  "options": [
    "Extraction",
    "Root canal treatment",
    "Follow-up",
    "Apicoectomy"
  ],
  "answer": 2,
  "answerText": "Follow-up",
  "reference": "No specific passage",
  "why": "The provided passages do not directly address hypercementosis management. However, hypercementosis is typically a benign, non-inflammatory condition that requires no treatment unless symptomatic, so follow-up is the standard approach. No passage supports extraction, root canal treatment, or apicoectomy for this finding.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0080",
  "set": "J",
  "qnum": 81,
  "dept": "perio",
  "stem": "Inflammation is present around a dental implant without radiographic bone loss. What is the diagnosis?",
  "options": [
    "Peri-implantitis",
    "Peri-implant mucositis",
    "Implant failure",
    "Osteomyelitis"
  ],
  "answer": 1,
  "answerText": "Peri-implant mucositis",
  "reference": "Carranza_Perio_Implant",
  "why": "The passage states: 'peri-implant mucositis is a reversible inflammatory change of the soft tissues around implants without bone loss.'",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0081",
  "set": "J",
  "qnum": 82,
  "dept": "endo",
  "stem": "A patient undergoing root canal treatment with a rubber dam develops wheezing and difficulty breathing after 30 minutes. What is the most likely cause?",
  "options": [
    "Allergic reaction",
    "Asthma attack"
  ],
  "answer": 0,
  "answerText": "Allergic reaction",
  "reference": "Cohens_Pathways_of_the_Pulp_2016",
  "why": "The passage mentions 'Allergic responses to CHX are rare' and 'some allergic reactions such as anaphylaxis... have been reported,' which could cause wheezing and breathing difficulty.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0082",
  "set": "J",
  "qnum": 83,
  "dept": "endo",
  "stem": "A radiograph shows a Stafne bone defect. What is the appropriate management?",
  "options": [
    "Surgical removal",
    "Root canal treatment",
    "No treatment",
    "Biopsy"
  ],
  "answer": 2,
  "answerText": "No treatment",
  "reference": "Cohens_Pathways_of_the_Pulp_2016",
  "why": "The passage mentions 'continuous recall recommended' for osseous defects after root canal treatment, and Stafne bone defect is a developmental bone cavity typically requiring no treatment; however, no passage directly addresses Stafne defect. Based on general dental knowledge, no treatment is appropriate, but the provided text does not support this option.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0083",
  "set": "J",
  "qnum": 84,
  "dept": "mixed",
  "stem": "A lesion contains numerous hemosiderin deposits on histopathologic examination. What is the most likely diagnosis?",
  "options": [
    "Peripheral giant cell granuloma",
    "Peripheral ossifying fibroma",
    "Pyogenic granuloma",
    "Central giant cell granuloma"
  ],
  "answer": 0,
  "answerText": "Peripheral giant cell granuloma",
  "reference": "McDonald Avery 10e",
  "why": "The passage states: 'peripheral giant cell granuloma must be considered in the differential diagnosis of pyogenic granuloma, because these lesions are clinically indistinguishable.' It also lists 'Peripheral Giant Cell Granuloma (Giant Cell Epulis)' as a distinct entity, and giant cell lesions typically contain hemosiderin deposits.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0084",
  "set": "J",
  "qnum": 85,
  "dept": "endo",
  "stem": "What is the prognosis of a separated endodontic file located in the middle third of the root canal?",
  "options": [
    "Good",
    "Fair",
    "Questionable",
    "Poor"
  ],
  "answer": 0,
  "answerText": "Good",
  "reference": "Cohens_Pathways_of_the_Pulp_2016",
  "why": "The passage states that a separated instrument can be incorporated into root canal filling materials and that its presence 'should not affect the prognosis,' indicating a good prognosis.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0085",
  "set": "J",
  "qnum": 86,
  "dept": "oms",
  "stem": "A radiograph of an extracted maxillary lateral incisor shows dens invaginatus. What is the reason for extraction?",
  "options": [
    "Dens invaginatus",
    "Internal resorption",
    "Root fracture",
    "External resorption"
  ],
  "answer": 0,
  "answerText": "Dens invaginatus",
  "reference": "Oral and Maxillofacial Pathology",
  "why": "The passage describes 'Coronal Dens Invaginatus Type III' with a 'Parulis overlying vital maxillary cuspid and lateral incisor. The cuspid contained a dens invaginatus,' indicating dens invaginatus as the reason for extraction.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0086",
  "set": "J",
  "qnum": 87,
  "dept": "endo",
  "stem": "A newly erupted mandibular premolar in a young patient has dens invaginatus but is asymptomatic. What is the appropriate management?",
  "options": [
    "Root canal treatment",
    "Extraction",
    "No treatment",
    "Surgical intervention"
  ],
  "answer": 2,
  "answerText": "No treatment",
  "reference": "Endodontics_principles",
  "why": "The passage states that dens invaginatus is a variation that may render a case difficult to manage, but for an asymptomatic case, no treatment is appropriate; the text does not support immediate intervention for asymptomatic dens invaginatus.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0087",
  "set": "J",
  "qnum": 88,
  "dept": "oms",
  "stem": "A patient presents with exposed bone and pain following extraction of a mandibular third molar. What is the appropriate management?",
  "options": [
    "Surgical debridement",
    "Irrigation of the socket and analgesics",
    "Antibiotics only",
    "Re-suturing"
  ],
  "answer": 1,
  "answerText": "Irrigation of the socket and analgesics",
  "reference": "Contemporary_OMFS_7e",
  "why": "The passage states: 'the tooth socket is gently irrigated with sterile saline' and 'the dressing should be discontinued as soon as the patient is pain free,' indicating irrigation and analgesics as management.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0088",
  "set": "J",
  "qnum": 89,
  "dept": "fixed",
  "stem": "A patient with hypothyroidism becomes anxious during treatment and develops a heart rate of 50 bpm with hypotension. What is the most likely diagnosis?",
  "options": [
    "Thyroid storm",
    "Myxedema coma",
    "Vasovagal syncope",
    "Adrenal crisis"
  ],
  "answer": 2,
  "answerText": "Vasovagal syncope",
  "reference": "",
  "why": "No passage discusses hypothyroidism, heart rate, or hypotension in this context.",
  "_verified": "recall",
  "_source": "july2026"
},
{
  "id": "qa_j_0089",
  "set": "J",
  "qnum": 90,
  "dept": "oms",
  "stem": "A patient is involved in a motorcycle accident and has airway obstruction. Which facial bone should be stabilized first?",
  "options": [
    "Orbital bone",
    "Maxilla",
    "Mandible",
    "Zygomatic bone"
  ],
  "answer": 2,
  "answerText": "Mandible",
  "reference": "Oral_Radiology_8e",
  "why": "The passage states that in Le Fort III fractures, the fracture plane extends from the nasal bone and frontal process of the maxilla, and airway obstruction is a concern; however, the mandible is the key bone to stabilize first for airway management, as it supports the tongue and airway. The passage does not explicitly state this, but the mandible is the correct answer based on standard airway management principles.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0090",
  "set": "J",
  "qnum": 91,
  "dept": "fixed",
  "stem": "A patient is missing teeth #34, #35, #44, and #45. Where should the indirect retainer be placed?",
  "options": [
    "Mesial to the edentulous area",
    "Distal to the edentulous area",
    "No indirect retainer is needed",
    "On the terminal abutment"
  ],
  "answer": 0,
  "answerText": "Mesial to the edentulous area",
  "reference": "McCracken's Removable Partial Prosthodontics",
  "why": "Indirect retainer components should be placed as far as possible from the distal extension base, which provides the best leverage advantage against dislodgment. In a Class III arch with nonsupporting anterior teeth, the adjacent edentulous area is considered to be the tissue-supported end, with a diagonal fulcrum line passing through the two principal abutments, as in a Class II arch.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0091",
  "set": "J",
  "qnum": 92,
  "dept": "rpd",
  "stem": "Which clasp design is indicated for a tooth with a mid-buccal undercut?",
  "options": [
    "Circumferential clasp",
    "I-bar clasp",
    "RPI clasp",
    "Ring clasp"
  ],
  "answer": 1,
  "answerText": "I-bar clasp",
  "reference": "McCracken's Removable Partial Prosthodontics",
  "why": "The passage states: 'the distobuccal undercut on the terminal abutment should be engaged by a bar-type clasp in the absence of a large buccal tissue undercut cervical to the terminal abutment.' An I-bar clasp is a bar-type clasp suitable for a mid-buccal undercut.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0092",
  "set": "J",
  "qnum": 93,
  "dept": "mixed",
  "stem": "Cephalometric analysis shows a normal SNA angle and a decreased SNB angle. What is the diagnosis?",
  "options": [
    "Prognathic maxilla",
    "Retrognathic maxilla",
    "Prognathic mandible",
    "Retrognathic mandible"
  ],
  "answer": 3,
  "answerText": "Retrognathic mandible",
  "reference": "ortho_An_Introduction_to_Orthodontics_(2)",
  "why": "The passage shows cephalometric values: 'SNA = 75°, SNB = 73°, ANB = 2°' with normal SNA and decreased SNB, indicating a retrognathic mandible.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0093",
  "set": "J",
  "qnum": 94,
  "dept": "fixed",
  "stem": "A 25-year-old patient has a normal SNB angle and a decreased SNA angle. What is the appropriate surgical treatment?",
  "options": [
    "Mandibular setback",
    "Maxillary advancement",
    "Maxillary setback",
    "Mandibular advancement"
  ],
  "answer": 1,
  "answerText": "Maxillary advancement",
  "reference": "Contemporary_Fixed_Prosthodontics_4e",
  "why": "The passage describes Angle Class I as normal occlusion; a decreased SNA with normal SNB indicates maxillary retrusion, requiring maxillary advancement, though not explicitly stated.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0094",
  "set": "J",
  "qnum": 95,
  "dept": "perio",
  "stem": "What is a possible consequence of using excessive gingival retraction cord force?",
  "options": [
    "Gingival hyperplasia",
    "Gingival recession",
    "Gingival pigmentation",
    "Increased sulcus depth"
  ],
  "answer": 1,
  "answerText": "Gingival recession",
  "reference": "Carranza_Clinical_Periodontology_2018",
  "why": "The passage states: 'The forceful packing of a gingival retraction cord into the sulcus... may mechanically injure the periodontium' and 'excessive occlusal forces... in some cases to reverse gingival recession,' implying recession as a consequence.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0095",
  "set": "J",
  "qnum": 96,
  "dept": "mixed",
  "stem": "A dentist performs a procedure on a patient with COVID-19 and later tests positive on a home rapid antigen test despite being asymptomatic. What should the dentist do?",
  "options": [
    "Continue working as usual",
    "Return to work after one day",
    "Isolate at home",
    "Continue working while wearing an N95 respirator"
  ],
  "answer": 2,
  "answerText": "Isolate at home",
  "reference": "Basic Guide to Infection Prevention and Control in Dentistry. 2009",
  "why": "The passage emphasizes standard precautions and confidentiality but does not address COVID-19 isolation; however, general infection control principles support isolation.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0096",
  "set": "J",
  "qnum": 97,
  "dept": "fixed",
  "stem": "A patient has a 2 mm oroantral communication following extraction. What is the appropriate management?",
  "options": [
    "Surgical closure",
    "Buccal advancement flap",
    "No intervention is required",
    "Palatal flap"
  ],
  "answer": 2,
  "answerText": "No intervention is required",
  "reference": "Hupp_Contemporary_OMFS_6e",
  "why": "The passage states that for small perforations, 'it may be necessary to cover the extraction site with some type of flap advancement to provide primary closure in an attempt to cover the sinus opening.' However, a 2 mm communication is small and may heal without intervention; the text also mentions that 'small gap between the flaps will heal over the membrane by secondary intention.' No passage explicitly states that a 2 mm communication requires no intervention, but the options for surgical closure (buccal or palatal flap) are described for larger or chronic fistulae, not for a small acute 2 mm communication. Therefore, based on the absence of specific support for surgical closure in this size, no intervention is the most appropriate.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0097",
  "set": "J",
  "qnum": 98,
  "dept": "endo",
  "stem": "A diabetic patient presents with facial swelling and pus associated with a dental infection. What is the initial treatment?",
  "options": [
    "Antibiotics only",
    "Incision and drainage",
    "Extraction only",
    "Root canal treatment"
  ],
  "answer": 1,
  "answerText": "Incision and drainage",
  "reference": "Contemporary_OMFS_7e",
  "why": "Odontogenic infections cause deep-seated abscesses, and they almost always require some form of surgical therapy. Treatments range from endodontic therapy and gingival curettage to extraction, incision, and drainage of the deep fascial spaces of the head and neck. Antibiotic therapy is usually only an adjunctive treatment to the required surgery.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0098",
  "set": "J",
  "qnum": 99,
  "dept": "oms",
  "stem": "A radiograph shows a multilocular radiolucency with a honeycomb appearance. What is the most likely diagnosis?",
  "options": [
    "Odontogenic keratocyst",
    "Ameloblastoma",
    "Dentigerous cyst",
    "Central giant cell granuloma"
  ],
  "answer": 1,
  "answerText": "Ameloblastoma",
  "reference": "Oral_Radiology_8e",
  "why": "The passage states that ameloblastoma can appear as a multilocular radiolucency and mentions 'internal septa' important for identification, consistent with honeycomb appearance.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0099",
  "set": "J",
  "qnum": 100,
  "dept": "oms",
  "stem": "A diabetic patient presents with facial swelling extending unilaterally to the jaw and lower neck. What is the most appropriate management?",
  "options": [
    "Prescribe oral antibiotics",
    "Incision and drainage in the dental clinic",
    "Refer the patient to the hospital",
    "Schedule elective treatment"
  ],
  "answer": 2,
  "answerText": "Refer the patient to the hospital",
  "reference": "Contemporary_OMFS_7e",
  "why": "The passage states: 'require surgical care under general anesthesia, with subsequent monitoring and medical management in a hospital setting. Such patients should be promptly referred to an oral and maxillofacial surgeon.'",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0100",
  "set": "J",
  "qnum": 101,
  "dept": "endo",
  "stem": "What is the recommended use of compomers in pediatric dentistry?",
  "options": [
    "Class II restorations in primary teeth",
    "Class III and Class V restorations in primary teeth",
    "Full-coverage restorations",
    "Endodontic access restoration"
  ],
  "answer": 1,
  "answerText": "Class III and Class V restorations in primary teeth",
  "reference": "Cohen's Pathways of the Pulp",
  "why": "The passage states 'Classically, direct composite restorations have been placed in anterior teeth...' and mentions 'adhesive restorations' in the context of primary teeth, but no specific passage directly addresses compomers. However, the passage 'med on carious coronal amalgam restorations were compared with extracoronal pulpal exposures in primary teeth' and 'Adhesive restorations' suggests adhesive materials are used in primary teeth, and compomers are commonly used for Class III and V restorations in primary teeth. Since no passage explicitly supports this, I am uncertain.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0101",
  "set": "J",
  "qnum": 102,
  "dept": "ortho_pedo",
  "stem": "A 2-year-old child under sedation develops dizziness and difficulty breathing. What is the most likely cause?",
  "options": [
    "Mild sedation",
    "Moderate sedation",
    "Sedation overdose",
    "Allergic reaction"
  ],
  "answer": 2,
  "answerText": "Sedation overdose",
  "reference": "Pedo_McDonald_Avery_10e",
  "why": "The passage states: 'Systemic toxic reactions from anesthetics are rarely observed in adults. However, young children are more likely to experience toxic reactions because of their lower body weight.' Dizziness and difficulty breathing in a sedated child suggest a toxic reaction, consistent with sedation overdose.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0102",
  "set": "J",
  "qnum": 103,
  "dept": "ortho_pedo",
  "stem": "A child returns one week after tooth extraction with swelling of the lower lip. What is the most likely diagnosis?",
  "options": [
    "Hematoma",
    "Masticatory trauma",
    "Cellulitis",
    "Allergic reaction"
  ],
  "answer": 2,
  "answerText": "Cellulitis",
  "reference": "Pediatric Dentistry INFANCY THROUGH ADOLESCENCE",
  "why": "The passage lists 'Cellulitis' as a differential diagnosis for a swelling after tooth extraction, and the clinical findings include 'soft tissue swelling' and 'tender to percussion'.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0103",
  "set": "J",
  "qnum": 104,
  "dept": "mixed",
  "stem": "An 11-year-old patient presents with maxillary constriction. Which appliance is most appropriate?",
  "options": [
    "Haas appliance",
    "Quad helix appliance",
    "Nance appliance",
    "Transpalatal arch"
  ],
  "answer": 1,
  "answerText": "Quad helix appliance",
  "reference": "Pedo_Pediatric Dentistry INFANCY THROUGH ADOLESCENCE",
  "why": "The passage states: 'the quad helix and the W arch for management of maxillary constriction are described. The appliances provide both skeletal and dental movement in the 3- to 6-year-old' and 'Three appliances can be used to correct the constriction, but the appliances are not interchangeable.' The quad helix is specifically mentioned for maxillary constriction.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0104",
  "set": "J",
  "qnum": 105,
  "dept": "perio",
  "stem": "How often should implant maintenance visits be scheduled during the first year for a patient at high risk of periodontitis?",
  "options": [
    "Every month",
    "Every 3 months",
    "Every 6 months",
    "Once a year"
  ],
  "answer": 1,
  "answerText": "Every 3 months",
  "reference": "Carranza_Clinical_Periodontology_2018",
  "why": "The passage states: 'In a study of 25 individuals with aggressive (early-onset) periodontitis followed with maintenance every 3 to 6 months for 5 years, it was concluded that these patients can be effectively maintained.'",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0105",
  "set": "J",
  "qnum": 106,
  "dept": "operative",
  "stem": "A patient has Class II malocclusion with increased overjet. Which orthodontic appliance is indicated?",
  "options": [
    "2×4 appliance with headgear",
    "Reverse pull headgear",
    "Quad helix",
    "Chin cup"
  ],
  "answer": 0,
  "answerText": "2×4 appliance with headgear",
  "reference": "An Introduction to Orthodontics (2)",
  "why": "The passage states 'Functional appliances are also used for Class II malocclusions with increased vertical proportions. A number of designs have been described, but usually they incorporate high-pull headgear and buccal capping.' This supports the use of headgear for Class II malocclusion with increased overjet.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0106",
  "set": "J",
  "qnum": 107,
  "dept": "operative",
  "stem": "A patient has Class II malocclusion with a deep bite. Which type of headgear is indicated?",
  "options": [
    "High-pull headgear",
    "Cervical-pull headgear",
    "Reverse pull headgear",
    "Combination headgear"
  ],
  "answer": 0,
  "answerText": "High-pull headgear",
  "reference": "Pedo_McDonald_Avery_10e",
  "why": "The passage states: 'Extraoral headgear. Directed cervical-pull, high-pull, or protraction reverse-pull headgear applications, with selection dependent on the vertical and sagittal facial growth patterns.' For a deep bite, high-pull headgear is typically indicated to control vertical dimension, and the text mentions 'high-pull headgear as well' in the context of vertical control.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0107",
  "set": "J",
  "qnum": 108,
  "dept": "operative",
  "stem": "A patient has skeletal Class III malocclusion due to maxillary deficiency. Which orthodontic appliance is indicated?",
  "options": [
    "Reverse pull headgear",
    "Cervical-pull headgear",
    "High-pull headgear",
    "Twin block appliance"
  ],
  "answer": 0,
  "answerText": "Reverse pull headgear",
  "reference": "Contemporary Orthodontics 5th",
  "why": "The passage states: 'roaches to maxillary deficiency: Frankel’s FR-III functional appliance, reverse-pull headgear (facemask) to a maxillary splint or skeletal anchors, and Class III elastics to skeletal anchors.'",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0108",
  "set": "J",
  "qnum": 109,
  "dept": "mixed",
  "stem": "A permanent canine is impacted and difficult to expose surgically, while the retained primary canine is healthy and functional. What is the most appropriate management?",
  "options": [
    "Extract the primary canine immediately",
    "Surgically expose the permanent canine",
    "Retain the primary canine",
    "Extract both teeth"
  ],
  "answer": 2,
  "answerText": "Retain the primary canine",
  "reference": "Contemporary Orthodontics",
  "why": "The passage states 'the primary canine was extracted, the crown of the permanent canine was exposed surgically' in a case of resorption, but for a healthy retained primary canine, the passage 'Retained deciduous teeth' is listed as a cause of malocclusion, implying retention may be appropriate. However, no passage directly supports retaining the primary canine in this scenario.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0109",
  "set": "J",
  "qnum": 110,
  "dept": "endo",
  "stem": "A tooth has a fracture involving enamel and dentin without pulp exposure. What is the injury called?",
  "options": [
    "Complicated crown fracture",
    "Uncomplicated crown fracture",
    "Crown-root fracture",
    "Enamel infraction"
  ],
  "answer": 1,
  "answerText": "Uncomplicated crown fracture",
  "reference": "Endo_Endodontics_principles",
  "why": "The passage states: 'Uncomplicated crown fractures involve enamel and dentin without pulpal exposure.'",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0110",
  "set": "J",
  "qnum": 111,
  "dept": "endo",
  "stem": "A radiograph of a root canal-treated tooth shows empty spaces within the root canal filling. What is this finding called?",
  "options": [
    "Ledge",
    "Strip perforation",
    "Void",
    "Transportation"
  ],
  "answer": 2,
  "answerText": "Void",
  "reference": "Endo_Kenneth_M._Hargreaves__Louis_H._Berman_-_Cohen’s_Pathways_of_the_Pulp-Mosby_2016",
  "why": "The passage mentions 'root canal fillings with no voids' as a criterion for success, and 'voids in root canal filling material' as a finding. Empty spaces within the root canal filling are called voids.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0111",
  "set": "J",
  "qnum": 112,
  "dept": "perio",
  "stem": "A patient presents with diffuse white, corrugated plaques on the buccal mucosa. The lesions are bilateral and cannot be scraped off. What is the most likely diagnosis?",
  "options": [
    "Leukoplakia",
    "White sponge nevus",
    "Oral lichen planus",
    "Candidiasis"
  ],
  "answer": 2,
  "answerText": "Oral lichen planus",
  "reference": "Carranza_Clinical_Periodontology_2018",
  "why": "The passage states: 'The typical reticular lesions are asymptomatic and bilateral, and they consist of interlacing white lines on the posterior regio...' and 'One percent of oral lichen planus cases may develop squamous cell carcinoma.'",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0112",
  "set": "J",
  "qnum": 113,
  "dept": "endo",
  "stem": "The radiograph shows inflammation around a dental implant with radiographic bone loss. What is the most likely diagnosis?",
  "options": [
    "Peri-implant mucositis",
    "Peri-implantitis",
    "Implant failure",
    "Periapical abscess"
  ],
  "answer": 1,
  "answerText": "Peri-implantitis",
  "reference": "Endodontics_principles",
  "why": "The passage states: 'gentle probing has been shown to be an effective means to evaluate the stability of the peri-implant attachment and to detect peri-implantitis.' Inflammation around an implant with radiographic bone loss is characteristic of peri-implantitis.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0113",
  "set": "J",
  "qnum": 114,
  "dept": "mixed",
  "stem": "bilateral bony protuberances on the lingual aspect of the mandible. What is the diagnosis?",
  "options": [
    "Mandibular exostosis",
    "Lingual tori",
    "Osteoma",
    "Peripheral ossifying fibroma"
  ],
  "answer": 1,
  "answerText": "Lingual tori",
  "reference": "Hupp_Contemporary_OMFS_6e",
  "why": "The passage states: 'Mandibular tori are bony protuberances on the lingual aspect of the mandible that usually occur in the premolar area.'",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0114",
  "set": "J",
  "qnum": 115,
  "dept": "mixed",
  "stem": "A female patient presents with a bilateral erythematous rash over the cheeks in a butterfly distribution. What is the most likely diagnosis?",
  "options": [
    "Rosacea",
    "Systemic lupus erythematosus (SLE)",
    "Psoriasis",
    "Seborrheic dermatitis"
  ],
  "answer": 1,
  "answerText": "Systemic lupus erythematosus (SLE)",
  "reference": "Carranza's Clinical Periodontology",
  "why": "The passage states 'Systemic lupus erythematosus (SLE) is a severe disease with a 10 : 1 predilection for women compared with men' and describes 'a butterfly-shaped erythematous rash across the nose and cheeks', which matches the patient's presentation.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0115",
  "set": "J",
  "qnum": 116,
  "dept": "operative",
  "stem": "a projection on the occlusal surface of a premolar. What is the most likely diagnosis?",
  "options": [
    "Dens invaginatus",
    "Talon cusp",
    "Dens evaginatus",
    "Enamel pearl"
  ],
  "answer": 2,
  "answerText": "Dens evaginatus",
  "reference": "Oral Radiology: Principles and Interpretation",
  "why": "Dens evaginatus is described as 'a cusplike elevation of enamel located in the ce...' and 'the resultant enamel-covered tubercle usually occurs in or near the middle of the occlusal surface of premolar or occasionally molar teeth.'",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0116",
  "set": "J",
  "qnum": 117,
  "dept": "endo",
  "stem": "The periapical radiograph shows multiple tooth-like radiopaque structures What is the most likely diagnosis?",
  "options": [
    "Complex odontoma",
    "Compound odontoma",
    "Cementoblastoma",
    "Ameloblastic fibro-odontoma",
    "Panorama x-ray ask about age (it was 12 because upper canine erupted )",
    "Pt has pain left side radiating to jaw",
    "Aspirin 325",
    "nitroglycerin 0.4 mg",
    "Pt has lesion in tongue and he has severe epilepsy",
    "chancre",
    "Lichen planes",
    "PV",
    "Esionphilic ulcer",
    "Analgesic for endo",
    "Aspirin",
    "Non steroid",
    "Paracetamol",
    "Pic of analog ask about what it is",
    "central incisors is located at"
  ],
  "answer": 1,
  "answerText": "Compound odontoma",
  "reference": "Oral_surgary_Oral_Radiology_-_Principles_and_Interpretation_7E_2014_",
  "why": "The passage states: 'A toothlike appearance of the radiopaque structures within a well-defined lesion leads to easy recognition of a compound odontoma.' The radiograph shows multiple tooth-like radiopaque structures, which is characteristic of a compound odontoma.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0117",
  "set": "J",
  "qnum": 118,
  "dept": "mixed",
  "stem": "High frenal attachment with diastema, management?",
  "options": [
    "Ortho then Frenectomy",
    "Subluxation splinting"
  ],
  "answer": 0,
  "answerText": "Ortho then Frenectomy",
  "reference": "Contemporary Orthodontics 5th",
  "why": "The passage states: 'If the diastema is relatively small, it is usually possible to bring the central incisors completely together before surgery... The space should be closed at least partially, and the orthodontic...' indicating orthodontic closure before frenectomy.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0118",
  "set": "J",
  "qnum": 119,
  "dept": "operative",
  "stem": "child presents with Chalky white appearance+ all anterior+ molar brown What is the most likely diagnosis?",
  "options": [
    "MIH",
    "AI",
    "Dental caries",
    "DI",
    "Most common occlusion",
    "Class 1",
    "Class malocclusion",
    "serial extraction",
    "BCD4"
  ],
  "answer": 0,
  "answerText": "MIH",
  "reference": "Sturdevant_Operative_5e",
  "why": "The passage describes 'A brown spot (bs) is a remineralized, arrested, incipient carious lesion' and 'Chalky white appearance' is characteristic of MIH, but the passage does not explicitly mention MIH. However, the combination of chalky white and brown spots on molars and incisors is classic for MIH.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0119",
  "set": "J",
  "qnum": 120,
  "dept": "perio",
  "stem": "Pt has pocket depth 5 ,bone loss 50% what to do?",
  "options": [
    "Flap depridment + Bone graft + CG",
    "Scaling and root planning + revaluate 6 weeks",
    "Extract All incisors",
    "Non surgical endo for the incisor",
    "heavy smoking",
    "10 cigarettes per day",
    "20 cigarettes per day",
    "30 cigarettes per day",
    "40 cigarettes per day",
    "There is trauma from occlusion how to asses teeth",
    "Occlusion test",
    "Mobility test",
    "Fremutis test",
    "Occulsion analysis",
    "Staillman recession treatment",
    "how many contact points in centric relation",
    "3",
    "4",
    "5",
    "6",
    "⁠pt have immediate CD from 6-9 months and now he feel continuous ill fit what is best management for him",
    "Remake",
    "lab reline",
    "chairside reline",
    "rebase"
  ],
  "answer": 1,
  "answerText": "Scaling and root planning + revaluate 6 weeks",
  "reference": "Carranza's Clinical Periodontology",
  "why": "The passage describes a case with 'nonsurgical scaling and root planing along with adjunctive systemic antibiotics' and notes 'Probing pocket depths have been maintained in the range of 2 to 5 mm', supporting initial nonsurgical therapy with reevaluation for moderate pocket depth and bone loss.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0120",
  "set": "J",
  "qnum": 121,
  "dept": "endo",
  "stem": "Best restorative treatment for crack tooth?",
  "options": [
    "Full crown",
    "amalgam",
    "composite",
    "Senario pt has attresion and have deep caries and undermind enamel No crown lengthing in choices",
    "crown",
    "composite amalgam",
    "RMGIC",
    "Drug should avoid in pregnancy due to risk of developing malformation",
    "aspirin",
    "Nabroxin",
    "Acetaminophen",
    "ibuprofen",
    "Pic of flap what is the complication",
    "Poor access",
    "Flap necrosis",
    "Cause of Break of gypsum during flasking",
    "Cause of Disdlogment of denture teeth",
    "Muscle posterior to maxillary tuberosity when mandible move from side to side or during open or close the mouth( i forget )",
    "Under cut represntied by red color",
    "Orthodontics what happen to Ankylosed tooth",
    "cannot be moved"
  ],
  "answer": 0,
  "answerText": "Full crown",
  "reference": "Endodontics_principles",
  "why": "The passage states: 'large, deep access preparations should be protected by an onlay or full crown. Large access preparations also require appropriate cusp protection.'",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0121",
  "set": "J",
  "qnum": 122,
  "dept": "oms",
  "stem": "What is the treatment of choice for a condylar fracture?cbct of condyle separated from mandible",
  "options": [
    "Open reduction with internal fixation (ORIF)",
    "Open reduction without fixation",
    "Closed reduction",
    "Conservative treatment"
  ],
  "answer": 0,
  "answerText": "Open reduction with internal fixation (ORIF)",
  "reference": "Contemporary Oral and Maxillofacial Surgery",
  "why": "The passage states 'With rigid fixation techniques, patients can be allowed to heal without undergoing IMF or at least a decreased time of IMF' and 'patients opt to undergo open reduction and internal fixation', supporting ORIF as the treatment of choice for condylar fractures.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0122",
  "set": "J",
  "qnum": 123,
  "dept": "endo",
  "stem": "A maxillary central incisor has a large pulp chamber and a wide root canal. Which description of the pulp chamber shape is correct?",
  "options": [
    "Round triangle on the palatal aspect",
    "Oval from the incisal aspect",
    "trapezoidal access"
  ],
  "answer": 1,
  "answerText": "Oval from the incisal aspect",
  "reference": "Cohens_Pathways_of_the_Pulp_2016",
  "why": "The passage states: 'A single root is oval and wider buccolingually than mesiodistally. The canal or canals remain oval from the pulp chamber floor and taper rapidly to the apex.'",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0123",
  "set": "J",
  "qnum": 124,
  "dept": "perio",
  "stem": "A patient has 4 mm gingival recession on one tooth with the interdental papilla intact. And 1mm of keratinized tissue According to Miller's classification",
  "options": [
    "Miller Class I",
    "Miller Class II",
    "RT1 / Miller Class I",
    "RT2 / Miller Class II"
  ],
  "answer": 0,
  "answerText": "Miller Class I",
  "reference": "Periodontics_MSI_PDF",
  "why": "The passage states: 'Class I: Recession not exte...' and 'The Miller classification allows the clinician to predict the outcome of root coverage by evaluating the height of the interdental bone and gingiva adjacent to the tooth with recession.' With intact interdental papilla, this is Miller Class I.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0124",
  "set": "J",
  "qnum": 125,
  "dept": "mixed",
  "stem": "A patient presents with Oral ulcers Genital ulcers Anal ulcers Which investigation is most helpful?",
  "options": [
    "Direct immunofluorescence",
    "Pathergy test",
    "ESR",
    "schirmer"
  ],
  "answer": 1,
  "answerText": "Pathergy test",
  "reference": "",
  "why": "The passage mentions 'Pemphigus vulgaris' with 'multiple oral blisters and ulcers' and 'Lupus erythematosus' with oral ulcers, but for oral, genital, and anal ulcers, the pathergy test is characteristic of Behçet's disease, though not directly quoted. No passage directly supports any option, so uncertain.",
  "_verified": "recall",
  "_source": "july2026"
},
{
  "id": "qa_j_0125",
  "set": "J",
  "qnum": 126,
  "dept": "mixed",
  "stem": "A patient with a history of reverse smoking presents with trismus and palpable white lesion What is the most appropriate treatment",
  "options": [
    "Intralesional steroid",
    "Surgical excision",
    "Topical steroid"
  ],
  "answer": 1,
  "answerText": "Surgical excision",
  "reference": "Oral_surgary_Oral_and_Maxillofacial_Pathology",
  "why": "The passage states 'In many instances, the diagnostic biopsy is excisional and completely eradicates the problematic mass. In patients with larger lesions, surgical excision ca...' which supports surgical excision as the most appropriate treatment for a palpable white lesion with trismus.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0126",
  "set": "J",
  "qnum": 127,
  "dept": "mixed",
  "stem": "A dentist wearing contact lenses is splashed with blood .What is the first step?",
  "options": [
    "Remove the contact lenses",
    "Irrigate the eyes with eyedrop",
    "clean his eye under running water"
  ],
  "answer": 2,
  "answerText": "clean his eye under running water",
  "reference": "Basic Guide to Infection Prevention and Control in Dentistry. 2009",
  "why": "The passage states: 'Splash to eyes: thoroughly wash eyes with running water or eye wash solution'.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0127",
  "set": "J",
  "qnum": 128,
  "dept": "mixed",
  "stem": "Which adverse effect may occur when digoxin is administered with epinephrine?",
  "options": [
    "Increased blood pressure",
    "Cardiac arrhythmia",
    "decrease INR"
  ],
  "answer": 1,
  "answerText": "Cardiac arrhythmia",
  "reference": "Oral_surgary_Manegment_of_medically_compromised_PT",
  "why": "The passage states: 'Cocaine and methamphetamine abusers are at increased risk for cardiac arrhythmias...' and discusses vasoconstrictors. Digoxin with epinephrine can precipitate cardiac arrhythmias, as epinephrine has positive inotropic and chronotropic effects.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0128",
  "set": "J",
  "qnum": 129,
  "dept": "operative",
  "stem": "A patient has Class I occlusion with a single-tooth anterior crossbite. What is the most appropriate treatment?",
  "options": [
    "2 × 4 appliance",
    "Quad helix",
    "Tiwn block"
  ],
  "answer": 1,
  "answerText": "Quad helix",
  "reference": "An Introduction to Orthodontics (2)",
  "why": "The passage lists 'quadhelix appliance' under 'crossbite management' (pages 165–6), indicating it is used for crossbite treatment.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0129",
  "set": "J",
  "qnum": 130,
  "dept": "mixed",
  "stem": "You accidentally extracted the wrong tooth and did not inform the patient. Which ethical principle was violated?",
  "options": [
    "mal practice",
    "non maleficence",
    "veracity",
    "autonomy"
  ],
  "answer": 3,
  "answerText": "autonomy",
  "reference": "Professionalism and Ethics Handbook for Residents",
  "why": "The passage states: 'Failure to respect patient autonomy rights is a major ethical violation and can lead to prosecution of the physician under malpractice laws.' Withholding information about the wrong tooth violates the patient's autonomy in decision-making.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0130",
  "set": "J",
  "qnum": 131,
  "dept": "oms",
  "stem": "After sustaining a needle-stick injury, what is the first step?",
  "options": [
    "Encourage bleeding from the wound and wash under running water",
    "cover the wound with a bandage",
    "wash under running water"
  ],
  "answer": 0,
  "answerText": "Encourage bleeding from the wound and wash under running water",
  "reference": "Contemporary_OMFS_7e",
  "why": "The passage states 'During an oral surgical procedure, only sterile water or sterile saline solution should be used to irrigate open wounds,' and standard first aid for needle-stick injury includes encouraging bleeding and washing; however, the passage does not explicitly mention needle-stick injury, so this is inferred.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0131",
  "set": "J",
  "qnum": 132,
  "dept": "operative",
  "stem": "A patient has yellow patches affecting all first permanent molars and anterior teeth. What is the most likely diagnosis?",
  "options": [
    "Enamel hypoplasia",
    "Dentinogenesis imperfecta",
    "Fluorosis",
    "Dental caries"
  ],
  "answer": 0,
  "answerText": "Enamel hypoplasia",
  "reference": "Sturdevant_Operative_5e",
  "why": "The passage states 'Nonhereditary enamel hypoplasia occurs when the ameloblasts are injured during enamel formation, resulting in defective enamel' and mentions it 'usually is seen' in such patterns.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0132",
  "set": "J",
  "qnum": 133,
  "dept": "ortho_pedo",
  "stem": "A 7-year-old child presents with diffuse, symmetrical white opacities on the permanent first molars and incisors. The father exhibits similar dental characteristics. The child's history includes a high-carbohydrate diet and consumption of fluoridated water. Wh",
  "options": [
    "Molar Incisor Hypomineralization (MIH)",
    "Early childhood caries",
    "Amelogenesis Imperfecta",
    "Fluorosis"
  ],
  "answer": 2,
  "answerText": "Amelogenesis Imperfecta",
  "reference": "McDonald and Avery's Dentistry for the Child and Adolescent 10e",
  "why": "The passage mentions 'asymmetrical distribution of hypomineralized demarcated opacities in first permanent molars and incisors' and states 'it is a multifactorial genetic condition.' The father exhibiting similar characteristics supports a genetic etiology, consistent with Amelogenesis Imperfecta.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0133",
  "set": "J",
  "qnum": 134,
  "dept": "perio",
  "stem": "What is the minimum distance between an implant and an adjacent natural tooth?",
  "options": [
    "1.0 mm",
    "1.5 mm",
    "2.0 mm",
    "3.0 mm"
  ],
  "answer": 1,
  "answerText": "1.5 mm",
  "reference": "Carranza_Clinical_Periodontology_2018",
  "why": "The text states: 'The implant should be placed at a distance of 1.5 to 2 mm from an adjacent natural tooth.'",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0134",
  "set": "J",
  "qnum": 135,
  "dept": "endo",
  "stem": "What is the appliance of choice for a Class II patient with a high vertical growth pattern?",
  "options": [
    "Cervical headgear",
    "Reverse pull headgear",
    "High-pull headgear",
    "Twin block",
    "Excessive occlusal trauma causing the tooth to become ankylosed to the bone is most likely associated with:",
    "Bone resorption only",
    "PDL widening only",
    "PDL necrosis with bone resorption",
    "Hypercementosis"
  ],
  "answer": 2,
  "answerText": "High-pull headgear",
  "reference": "Pedo_McDonald_Avery_10e",
  "why": "The passage states: 'Extraoral headgear. Directed cervical-pull, high-pull, or protraction reverse-pull headgear applications, with selection dependent on the vertical and sagittal facial growth patterns as well as the stage of development.' For a high vertical growth pattern, high-pull headgear is the appropriate choice.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0135",
  "set": "J",
  "qnum": 136,
  "dept": "rpd",
  "stem": "Which rubber dam clamp is most suitable for a partially erupted molar?",
  "options": [
    "212",
    "W4A",
    "W7",
    "14A"
  ],
  "answer": 3,
  "answerText": "14A",
  "reference": "Pediatric Dentistry INFANCY THROUGH ADOLESCENCE",
  "why": "The passage states 'Partially erupted permanent molars: 14A, 8A*†‡', indicating clamp 14A is suitable for partially erupted molars.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0136",
  "set": "J",
  "qnum": 137,
  "dept": "ortho_pedo",
  "stem": "A child requires RCT, but the mother is unsure and asks the child to decide. What is the most appropriate action?",
  "options": [
    "Let the child decide",
    "Refer to another dentist",
    "Obtain informed consent from the parent before proceeding with treatment (RCT or extraction)",
    "Perform treatment without consent"
  ],
  "answer": 2,
  "answerText": "Obtain informed consent from the parent before proceeding with treatment (RCT or extraction)",
  "reference": "Pedo_Pediatric Dentistry INFANCY THROUGH ADOLESCENCE",
  "why": "The passage emphasizes 'Informing the parent before the extraction and obtaining a written consent' and states 'These issues are shared by dentist and parent.'",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0137",
  "set": "J",
  "qnum": 138,
  "dept": "perio",
  "stem": "A patient has buccal gingival recession with intact interdental attachment. According to the 2017 classification, what is the diagnosis?",
  "options": [
    "Miller Class I",
    "Miller Class II",
    "RT1",
    "RT2"
  ],
  "answer": 2,
  "answerText": "RT1",
  "reference": "Carranza_Clinical_Periodontology_2018",
  "why": "The passage states 'Class I. Marginal tissue recession does not extend to the mucogingival junction. There is no loss of bone or soft tissue in the interdental area,' which matches intact interdental attachment; however, the question asks for the 2017 classification (RT1), and the passage only describes Miller classes, so RT1 is inferred as the equivalent.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0138",
  "set": "J",
  "qnum": 139,
  "dept": "mixed",
  "stem": "A patient presents with a smooth, atrophic tongue. Which investigation is most appropriate?",
  "options": [
    "ESR",
    "Blood glucose",
    "CBC",
    "Liver function test"
  ],
  "answer": 2,
  "answerText": "CBC",
  "reference": "Manegment of medically compromised PT",
  "why": "The passage states: 'Routine testing may include a complete blood count, renal function testing and electrolytes, liver function testing, blood glucose, lipids, and thyroid function testing.' A smooth, atrophic tongue may indicate anemia, making CBC the most appropriate initial investigation.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0139",
  "set": "J",
  "qnum": 140,
  "dept": "rpd",
  "stem": "Which material is commonly used for a functional impression in complete dentures?",
  "options": [
    "a. Impression compound",
    "b. Polyether",
    "c. Alginate",
    "d. ZOE paste"
  ],
  "answer": 1,
  "answerText": "b. Polyether",
  "reference": "Textbook of Complete Dentures",
  "why": "The passage states 'Polyether has an inherent heavy consistency, although there are modifiers that can be used to make it more fluid,' and it is discussed in the context of final impressions for complete dentures, supporting polyether as a functional impression material.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0140",
  "set": "J",
  "qnum": 141,
  "dept": "mixed",
  "stem": "A patient presents with xerostomia and a Schirmer test result of 3–5 mm. What is the most likely diagnosis?",
  "options": [
    "Diabetes mellitus",
    "Sjögren syndrome",
    "Sarcoidosis",
    "Systemic lupus erythematosus"
  ],
  "answer": 1,
  "answerText": "Sjögren syndrome",
  "reference": "Oral_surgary_Oral_and_Maxillofacial_Pathology",
  "why": "The passage lists 'Sjögren syndrome' under 'Systemic Diseases' as a cause of xerostomia and describes primary Sjögren's syndrome with 'xerostomia and exophthalmia.'",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0141",
  "set": "J",
  "qnum": 142,
  "dept": "operative",
  "stem": "A 7-year-old child has generalized sensitivity and brown discoloration affecting the permanent first molars and incisors. What is the most likely diagnosis?",
  "options": [
    "Dentinogenesis imperfecta",
    "Enamel hypoplasia",
    "Molar-incisor hypomineralization (MIH)",
    "Dentin dysplasia"
  ],
  "answer": 2,
  "answerText": "Molar-incisor hypomineralization (MIH)",
  "reference": "McDonald and Avery's Dentistry for the Child and Adolescent 10e",
  "why": "The passage describes 'asymmetrical distribution of hypomineralized demarcated opacities in first permanent molars and incisors' and notes it is 'a multifactorial genetic condition.' Generalized sensitivity and brown discoloration of these teeth is consistent with MIH.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0142",
  "set": "J",
  "qnum": 143,
  "dept": "perio",
  "stem": "An implant with a diameter of 4 mm is planned between two natural teeth. What is the minimum mesiodistal space required?",
  "options": [
    "6 mm",
    "7 mm",
    "8 mm",
    "9 mm"
  ],
  "answer": 1,
  "answerText": "7 mm",
  "reference": "Carranza_Clinical_Periodontology_2018",
  "why": "The text states: 'B. Standard diameter implant (e.g., 4.1 mm) is 7 mm.' A 4 mm implant is standard diameter, requiring 7 mm.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0143",
  "set": "J",
  "qnum": 144,
  "dept": "fixed",
  "stem": "The image shows severe attrition. What is the most appropriate treatment?",
  "options": [
    "Crown lengthening followed by crowns",
    "Refer to Prosthodontics for full-mouth rehabilitation/crowns",
    "Extraction",
    "Composite restoration only"
  ],
  "answer": 1,
  "answerText": "Refer to Prosthodontics for full-mouth rehabilitation/crowns",
  "reference": "Contemporary Fixed Prosthodontics 4e",
  "why": "The passage discusses full-mouth rehabilitation and states 'this treatment approach is preferred because it is much more conservative of tooth structure than is splinting with metalceramic crowns.' Severe attrition typically requires full-mouth rehabilitation.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0144",
  "set": "J",
  "qnum": 145,
  "dept": "rpd",
  "stem": "A partially edentulous arch has missing teeth 11, 12, and 13. What is the Kennedy classification?",
  "options": [
    "Class I",
    "Class II",
    "Class III",
    "Class IV"
  ],
  "answer": 3,
  "answerText": "Class IV",
  "reference": "McCracken_s Removable Partial Prosthodontics",
  "why": "The text states: 'Class IV ... in which only anterior teeth are missing.' Missing teeth 11, 12, and 13 are anterior teeth only.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0145",
  "set": "J",
  "qnum": 146,
  "dept": "operative",
  "stem": "The clinical image shows a melanotic macule. What is the most likely diagnosis?",
  "options": [
    "Amalgam tattoo",
    "Melanoma",
    "Melanotic macule",
    "Oral melanocytic nevus"
  ],
  "answer": 2,
  "answerText": "Melanotic macule",
  "reference": "Pediatric Dentistry INFANCY THROUGH ADOLESCENCE",
  "why": "The passage states 'Oral melanotic macule' is 'the most common oral pigmentation of fair-skinned individuals' and describes it as a 'Brown or black, oval macule with smooth surface' on the 'lower lip vermilion, buccal mucosa'.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0146",
  "set": "J",
  "qnum": 147,
  "dept": "mixed",
  "stem": "While placing a matrix band, the dentist accidentally sustains a needlestick injury. What is the immediate next step?",
  "options": [
    "Apply antiseptic only",
    "Let the wound bleed freely only",
    "Wash immediately with soap and water, then follow the exposure protocol",
    "Cover the wound and continue treatment"
  ],
  "answer": 2,
  "answerText": "Wash immediately with soap and water, then follow the exposure protocol",
  "reference": "Contemporary Oral and Maxillofacial Surgery 6e",
  "why": "The passage emphasizes 'Injuries to teeth and the alveolar process are common and should be considered emergency conditions because a successful outcome depends on prompt attention to the injury.' For a needlestick, immediate washing and following exposure protocol is standard, though not explicitly stated in the provided text.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0147",
  "set": "J",
  "qnum": 148,
  "dept": "perio",
  "stem": "Which adverse oral reaction is associated with thiazide diuretics?",
  "options": [
    "Gingival enlargement",
    "Lichenoid reaction",
    "Xerostomia",
    "Candidiasis"
  ],
  "answer": 1,
  "answerText": "Lichenoid reaction",
  "reference": "Oral_surgary_Manegment_of_medically_compromised_PT",
  "why": "The passage states thiazide diuretics cause 'Dry mouth, lichenoid reactions' as oral adverse effects.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0148",
  "set": "J",
  "qnum": 149,
  "dept": "ortho_pedo",
  "stem": "An older child presents with an avulsed permanent tooth. Which antibiotic is recommended?",
  "options": [
    "Amoxicillin",
    "Penicillin V",
    "Azithromycin",
    "Doxycycline"
  ],
  "answer": 1,
  "answerText": "Penicillin V",
  "reference": "Pediatric Dentistry INFANCY THROUGH ADOLESCENCE",
  "why": "The passage states: 'penicillin V is the antibiotic of choice for children age 8 years and younger.' For an older child with an avulsed permanent tooth, penicillin V is recommended.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0149",
  "set": "J",
  "qnum": 150,
  "dept": "rpd",
  "stem": "A patient complains that the complete denture becomes loose while at rest. What is the most likely cause?",
  "options": [
    "Thick border molding",
    "Poor peripheral seal",
    "Increased vertical dimension",
    "Occlusal discrepancy"
  ],
  "answer": 1,
  "answerText": "Poor peripheral seal",
  "reference": "Textbook of Complete Dentures",
  "why": "The text discusses denture retention and mentions 'border molding' and 'peripheral seal' as factors; a loose denture at rest is most likely due to poor peripheral seal.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0150",
  "set": "J",
  "qnum": 151,
  "dept": "rpd",
  "stem": "What is the most common cause of acrylic denture failure?",
  "options": [
    "Low thermal conductivity",
    "Low modulus of elasticity (MOE)",
    "Low coefficient of thermal expansion",
    "Low water absorption"
  ],
  "answer": 0,
  "answerText": "Low thermal conductivity",
  "reference": "McCracken_s Removable Partial Prosthodontics",
  "why": "The passage states 'denture acrylic resins have insulating properties that prevent int...' and 'The advantages of thermal conductivity are not necessarily lost by covering a portion of the metal base,' indicating low thermal conductivity is a characteristic of acrylic, but the question asks for the most common cause of failure, which is not directly stated.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0151",
  "set": "J",
  "qnum": 152,
  "dept": "mixed",
  "stem": "The image shows a titanium mesh. What is its primary use?",
  "options": [
    "Guided bone regeneration (GBR)",
    "Block bone graft",
    "Sinus lift",
    "Ridge splitting"
  ],
  "answer": 0,
  "answerText": "Guided bone regeneration (GBR)",
  "reference": "Carranza_13ed",
  "why": "The passage mentions 'guided bone regeneration' among strategies to overcome limitations for implant therapy, and titanium mesh is commonly used for GBR.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0152",
  "set": "J",
  "qnum": 153,
  "dept": "mixed",
  "stem": "A dentist fails to inform the operating room staff that an emergency patient has influenza. Which ethical duty has been neglected?",
  "options": [
    "Infection control",
    "Duty to protect colleagues",
    "Duty to protect the community",
    "Duty to report to the infectious disease center"
  ],
  "answer": 1,
  "answerText": "Duty to protect colleagues",
  "reference": "Basic Guide to Infection Prevention and Control in Dentistry. 2009",
  "why": "The passage states 'Everyone working in the practice has a duty of care towards the patients, which includes taking reasonable precautions to protect them from' infection, and the context of occupational health and immunization implies a duty to protect colleagues from infectious diseases like influenza.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0153",
  "set": "J",
  "qnum": 154,
  "dept": "mixed",
  "stem": "A dentist does not inform the referring dentist about the patient’s treatment plan. This represents a breach of:",
  "options": [
    "Professional ethics",
    "Moral values",
    "Veracity",
    "Beneficence"
  ],
  "answer": 0,
  "answerText": "Professional ethics",
  "reference": "Hand book of local anesthesia 6th",
  "why": "The passage discusses HIPAA and professional obligations, but the specific breach of not informing a referring dentist about treatment plan relates to professional ethics, as the dentist must adhere to standards of care and communication.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0154",
  "set": "J",
  "qnum": 155,
  "dept": "mixed",
  "stem": "Why should ibuprofen be avoided in patients with ischemic heart disease or heart failure?",
  "options": [
    "It increases the risk of myocardial infarction.",
    "It increases the risk of arrhythmia.",
    "It increases the risk of tachycardia.",
    "It causes hypotension."
  ],
  "answer": 0,
  "answerText": "It increases the risk of myocardial infarction.",
  "reference": "Oral_surgary_Manegment_of_medically_compromised_PT",
  "why": "The passage states: 'we recommend that NSAIDs be used with caution, if at all, in patients who have had a previous MI' and 'The use of vasoconstrictors in local anesthetics poses potential problems for patients with ischemic heart disease because of the possibility of cardias, arrhythmias, and increases in blood pressure.' However, the specific risk of ibuprofen increasing myocardial infarction is supported by the recommendation to avoid NSAIDs after MI.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0155",
  "set": "J",
  "qnum": 156,
  "dept": "mixed",
  "stem": "What is the standard pressure used in an autoclave operating at 121°C?",
  "options": [
    "15 psi",
    "20 psi",
    "25 psi",
    "30 psi"
  ],
  "answer": 0,
  "answerText": "15 psi",
  "reference": "GUIDELINES FOR INFECTION CONTROL-2003",
  "why": "The passage states that sterilization is performed by 'steam under pressure (autoclaving)' but does not specify the psi at 121°C. However, standard autoclave pressure at 121°C is 15 psi, which is a well-known fact, but since no passage supports this, I must be uncertain.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0156",
  "set": "J",
  "qnum": 157,
  "dept": "endo",
  "stem": "Which finding is least suggestive of pulpal disease?",
  "options": [
    "Physiologic exfoliation with increased mobility",
    "Pathologic mobility",
    "Tooth pain",
    "Percussion tenderness"
  ],
  "answer": 0,
  "answerText": "Physiologic exfoliation with increased mobility",
  "reference": "Cohens_Pathways_of_the_Pulp_2016",
  "why": "The passage states 'mobility can be significant during phases of active physiologic root resorption,' indicating physiologic exfoliation with increased mobility is a normal process, not suggestive of pulpal disease.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0157",
  "set": "J",
  "qnum": 158,
  "dept": "mixed",
  "stem": "What is the most common mode of disease transmission in the dental clinic?",
  "options": [
    "Direct contact",
    "Indirect contact",
    "Airborne transmission",
    "Droplet transmission"
  ],
  "answer": 0,
  "answerText": "Direct contact",
  "reference": "Basic Guide to Infection Prevention and Control in Dentistry. 2009",
  "why": "The passage states 'Contact spread is a direct spread from person to person, or indirectly via equipment...' and 'This is the most obvious and commonly appreciated mode of spread of infection by dental professionals.'",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0158",
  "set": "J",
  "qnum": 159,
  "dept": "perio",
  "stem": "A patient with well-controlled diabetes requires replacement of a missing tooth. What is the most appropriate treatment option?",
  "options": [
    "Removable partial denture",
    "Fixed partial denture",
    "Dental implant",
    "No treatment"
  ],
  "answer": 2,
  "answerText": "Dental implant",
  "reference": "perio_Carranza_Clinical_Periodontology_2018",
  "why": "The passage states 'Replacement of a single missing tooth with an implant-supported crown is a much more conservative approach than preparing two adjacent teeth for the fabrication of a tooth-supported fixed partial denture,' supporting dental implant as the most appropriate option.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0159",
  "set": "J",
  "qnum": 160,
  "dept": "mixed",
  "stem": "A violation of patient privacy.",
  "options": [
    "Patient information disclosure.",
    "Professional communication.",
    "Informed consent."
  ],
  "answer": 0,
  "answerText": "Patient information disclosure.",
  "reference": "Professionalism and Ethics Handbook for Residents",
  "why": "The passage lists 'information disclosure' as part of patients' rights, and a violation of patient privacy would involve improper disclosure of patient information.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0160",
  "set": "J",
  "qnum": 161,
  "dept": "mixed",
  "stem": "The clinical image shows concentric erythematous target lesions associated with oral ulcers. What is the diagnosis?",
  "options": [
    "Pemphigus vulgaris",
    "Lichen planus",
    "Erythema multiforme",
    "Stevens–Johnson syndrome"
  ],
  "answer": 2,
  "answerText": "Erythema multiforme",
  "reference": "perio_Carranza_Clinical_Periodontology_2018",
  "why": "The passage lists 'erythema multiforme' among mucocutaneous disorders that can present as gingival lesions, and the clinical description of concentric target lesions with oral ulcers is characteristic of erythema multiforme.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0161",
  "set": "J",
  "qnum": 162,
  "dept": "endo",
  "stem": "A patient presents with gray-blue teeth and obliterated pulp chambers. What is the most likely diagnosis?",
  "options": [
    "Amelogenesis imperfecta",
    "Dentinogenesis imperfecta",
    "Dentin dysplasia",
    "Dental fluorosis"
  ],
  "answer": 1,
  "answerText": "Dentinogenesis imperfecta",
  "reference": "Cohen's Pathways of the Pulp",
  "why": "The passage mentions 'Dentinogenesis imperfecta' under intrinsic discoloration causes and states it is 'most commonly categorized into three subtypes: DGI type I, DGI type II, and DGI type III', which can present with gray-blue teeth and obliterated pulp chambers.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0162",
  "set": "J",
  "qnum": 163,
  "dept": "mixed",
  "stem": "Which laboratory investigation is most useful in confirming systemic lupus erythematosus (SLE)?",
  "options": [
    "ESR",
    "CRP",
    "Antinuclear antibody (ANA) test",
    "Rheumatoid factor"
  ],
  "answer": 2,
  "answerText": "Antinuclear antibody (ANA) test",
  "reference": "Carranza_Clinical_Periodontology_2018",
  "why": "The passage states 'positive for antinuclear antibodies in 60% to 90%' in patients with lupus erythematosus, indicating ANA is a key confirmatory test.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0163",
  "set": "J",
  "qnum": 164,
  "dept": "oms",
  "stem": "Which imaging modality is most appropriate for evaluating a sublingual abscess?",
  "options": [
    "Panoramic radiograph",
    "Ultrasound",
    "Contrast-enhanced CT scan",
    "MRI"
  ],
  "answer": 2,
  "answerText": "Contrast-enhanced CT scan",
  "reference": "Oral_surgary_Oral_Radiology_-_Principles_and_Interpretation_7E_2014_",
  "why": "The passage states 'MDCT imaging is useful in assessing acute inflammatory processes and abscesses, cysts, mucoceles, and neoplasia,' making contrast-enhanced CT scan the most appropriate for evaluating a sublingual abscess.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0164",
  "set": "J",
  "qnum": 165,
  "dept": "mixed",
  "stem": "A patient complains of a burning sensation in the mouth despite normal oral mucosa and adequate salivary flow. What is the most likely diagnosis?",
  "options": [
    "Oral candidiasis",
    "Xerostomia",
    "Burning mouth syndrome",
    "Geographic tongue"
  ],
  "answer": 2,
  "answerText": "Burning mouth syndrome",
  "reference": "",
  "why": "The passage describes 'atrophic glossitis' with 'tenderness or a burning sensation' in Plummer-Vinson syndrome, but the question specifies normal mucosa and adequate salivary flow, which is not covered. However, burning mouth syndrome is not mentioned in the passages. The closest is the description of dry mouth and burning sensation, but the question states adequate salivary flow, so no passage directly supports burning mouth syndrome.",
  "_verified": "recall",
  "_source": "july2026"
},
{
  "id": "qa_j_0165",
  "set": "J",
  "qnum": 166,
  "dept": "perio",
  "stem": "A patient presents with spontaneous gingival bleeding and tooth mobility. Which vitamin deficiency is the most likely cause?",
  "options": [
    "Scurvy (Vitamin C deficiency)",
    "Beriberi (Vitamin B1 deficiency)",
    "Vitamin D deficiency",
    "Vitamin K deficiency"
  ],
  "answer": 0,
  "answerText": "Scurvy (Vitamin C deficiency)",
  "reference": "Carranza's Clinical Periodontology",
  "why": "The passage states 'severe ascorbic acid (vitamin C) deficiency or scurvy' leads to 'bright red, swollen, and bleeding gingiva' and 'Hemorrhage that occurs spontaneously or on slight provocation', matching the symptoms.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0166",
  "set": "J",
  "qnum": 167,
  "dept": "endo",
  "stem": "A patient presents with necrotic interdental papillae, upper respiratory tract infection, and cervical lymphadenopathy. What is the most likely diagnosis?",
  "options": [
    "Necrotizing ulcerative gingivitis (NUG)",
    "Streptococcal gingivostomatitis",
    "Primary herpetic gingivostomatitis",
    "Acute pericoronitis"
  ],
  "answer": 0,
  "answerText": "Necrotizing ulcerative gingivitis (NUG)",
  "reference": "",
  "why": "The passage mentions 'necrotizing ulcerative gingivitis' is not directly quoted, but the clinical features of necrotic interdental papillae, URTI, and lymphadenopathy are classic for NUG. However, the provided passages do not explicitly describe NUG. The passage lists 'recurrent oral aphthous stomatitis' and 'erythema multiforme' but not NUG.",
  "_verified": "recall",
  "_source": "july2026"
},
{
  "id": "qa_j_0167",
  "set": "J",
  "qnum": 168,
  "dept": "mixed",
  "stem": "A patient has a shiny tongue and dry skin. Which investigation is most appropriate?",
  "options": [
    "Serum ferritin",
    "Complete blood count (CBC)",
    "Blood glucose",
    "Vitamin D level"
  ],
  "answer": 1,
  "answerText": "Complete blood count (CBC)",
  "reference": "Management of Medically Compromised Patients",
  "why": "The passage states 'Minimal blood studies should include complete blood count (CBC)' for evaluating oral lesions, and a shiny tongue and dry skin may indicate anemia, which CBC can help diagnose.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0168",
  "set": "J",
  "qnum": 169,
  "dept": "mixed",
  "stem": "A mother with congenitally missing teeth is concerned that her daughter may have the same condition. Which permanent tooth is most commonly congenitally missing?",
  "options": [
    "Mandibular second premolar",
    "Maxillary lateral incisor",
    "Mandibular canine",
    "Maxillary first premolar"
  ],
  "answer": 0,
  "answerText": "Mandibular second premolar",
  "reference": "pedo_Pediatric_Dentistry_INFANCY_THROUGH_ADOLESCENCE",
  "why": "The passage states 'The most common missing teeth in the permanent dentition, with the exception of the maxillary and mandibular third molars, are the mandibular second premolar, maxillary lateral incisor, and maxillary second premolar in that order,' making mandibular second premolar the most commonly missing.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0169",
  "set": "J",
  "qnum": 170,
  "dept": "oms",
  "stem": "A patient taking warfarin has an INR of 3.0 and requires extraction of a single tooth. What is the most appropriate management?",
  "options": [
    "Stop warfarin before extraction.",
    "Give vitamin K supplementation.",
    "Proceed with extraction using local hemostatic measures.",
    "Replace warfarin with heparin bridging."
  ],
  "answer": 2,
  "answerText": "Proceed with extraction using local hemostatic measures.",
  "reference": "Oral_surgary_Manegment_of_medically_compromised_PT",
  "why": "The passage states 'minor oral surgery, such as simple extractions, can be performed without altering or stopping the warfarin regimen' and 'Surgical wounds should be dressed with thrombogenic substances' for patients with elevated INR.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0170",
  "set": "J",
  "qnum": 171,
  "dept": "fixed",
  "stem": "In a removable partial denture, inadequate relief between the minor connector and the soft tissue may result in:",
  "options": [
    "Poor esthetics",
    "Clasp fracture",
    "Excessive forces on the abutment tooth",
    "Loss of retention"
  ],
  "answer": 2,
  "answerText": "Excessive forces on the abutment tooth",
  "reference": "Contemporary_Fixed_Prosthodontics_4e",
  "why": "The passage defines a clasp assembly and mentions reciprocal clasp, but no passage directly addresses inadequate relief between minor connector and soft tissue. However, based on prosthodontic principles, inadequate relief can lead to excessive forces on the abutment tooth, though this is not directly quoted.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0171",
  "set": "J",
  "qnum": 172,
  "dept": "mixed",
  "stem": "A positive nodule is present on a dental cast. What is the most likely cause?",
  "options": [
    "Impression technique error",
    "Cast pouring error",
    "Dental stone mixing error",
    "Improper trimming"
  ],
  "answer": 1,
  "answerText": "Cast pouring error",
  "reference": "Contemporary_Fixed_Prosthodontics_4e",
  "why": "The passage states 'errors caused by incomplete seating of a removable die' and discusses cast fabrication issues, which relate to pouring errors.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0172",
  "set": "J",
  "qnum": 173,
  "dept": "rpd",
  "stem": "What is the last clinical step before fabrication of a removable partial denture?",
  "options": [
    "Metal framework try-in",
    "Centric relation record",
    "Primary impression",
    "Surveying the cast"
  ],
  "answer": 1,
  "answerText": "Centric relation record",
  "reference": "McCracken's Removable Partial Prosthodontics",
  "why": "The passage describes recording 'maxillomandibular relations' and 'centric relation record' as part of the process before denture fabrication, and this is typically the last clinical step before sending to the lab.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0173",
  "set": "J",
  "qnum": 174,
  "dept": "rpd",
  "stem": "A Kennedy Class I patient returns one day after denture insertion complaining of pain on swallowing without redness over the alveolar ridge. What is the most likely cause?",
  "options": [
    "Overextended lingual flange",
    "Underextended lingual flange",
    "High occlusion",
    "Sharp denture borders"
  ],
  "answer": 0,
  "answerText": "Overextended lingual flange",
  "reference": "Removable_Textbook_of_Complete_Dentures",
  "why": "The passage states: 'Occasionally tongue biting can occur if the horizontal overlap is improper on the lingual cusp areas' and discusses overextended borders causing irritation. Pain on swallowing without redness suggests overextension of the lingual flange, which is supported by the passage on 'irritation caused by a slightly overextended border.'",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0174",
  "set": "J",
  "qnum": 175,
  "dept": "operative",
  "stem": "What is the most common type of malocclusion?",
  "options": [
    "Class I malocclusion",
    "Class II malocclusion",
    "Class III malocclusion",
    "Open bite"
  ],
  "answer": 0,
  "answerText": "Class I malocclusion",
  "reference": "Contemporary_Fixed_Prosthodontics_4e",
  "why": "The passage describes Angle's classification but does not state which is most common. However, Class I malocclusion is generally the most common, but this is not supported by the provided text.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0175",
  "set": "J",
  "qnum": 176,
  "dept": "oms",
  "stem": "Which of the following is the most appropriate method to determine whether craniofacial growth has been completed?",
  "options": [
    "Hand-wrist radiograph",
    "Serial cephalographs",
    "Panoramic radiograph",
    "Cone-beam CT (CBCT)"
  ],
  "answer": 1,
  "answerText": "Serial cephalographs",
  "reference": "Contemporary Orthodontics 5th",
  "why": "The passage states: 'Serial cephalometric radiographs offer the most accurate way to determine whether facial growth has...'",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0176",
  "set": "J",
  "qnum": 177,
  "dept": "operative",
  "stem": "A patient with a constricted maxilla in the early mixed dentition requires maxillary expansion. Which appliance is the most appropriate?",
  "options": [
    "Quad helix",
    "W-arch",
    "Banded palatal expander",
    "Bonded palatal expander"
  ],
  "answer": 0,
  "answerText": "Quad helix",
  "reference": "",
  "why": "No passage in the provided text discusses maxillary expansion appliances or constricted maxilla treatment.",
  "_verified": "recall",
  "_source": "july2026"
},
{
  "id": "qa_j_0177",
  "set": "J",
  "qnum": 178,
  "dept": "operative",
  "stem": "What is the most appropriate treatment for a patient with mild skeletal Class III malocclusion after growth completion?",
  "options": [
    "Orthodontic camouflage with lower premolar extraction",
    "Reverse pull headgear",
    "Functional appliance therapy",
    "Rapid maxillary expansion"
  ],
  "answer": 0,
  "answerText": "Orthodontic camouflage with lower premolar extraction",
  "reference": "Contemporary Fixed Prosthodontics",
  "why": "The passage lists contraindications to occlusal adjustment including 'A complex spatial relationship (e.g., an Angle Class II and a skeletal Class III)', implying that for mild Class III, orthodontic camouflage may be appropriate, but no passage directly supports this option.",
  "_verified": "book",
  "_source": "july2026"
},
{
  "id": "qa_j_0178",
  "set": "J",
  "qnum": 179,
  "dept": "operative",
  "stem": "Ideal temperature of water for alginate mixing:",
  "options": [
    "15°C",
    "20°C",
    "25°C",
    "30°C"
  ],
  "answer": 1,
  "answerText": "20°C",
  "reference": "Contemporary_Fixed_Prosthodontics_4e",
  "why": "The passage states: 'The clinician can control the reaction rate by varying the temperature of the mixing water.' It does not specify an ideal temperature, but 20°C is commonly used. However, the passage does not provide a specific number, so this is uncertain.",
  "_verified": "book",
  "_source": "mcq_solved"
},
{
  "id": "qa_j_0179",
  "set": "J",
  "qnum": 180,
  "dept": "perio",
  "stem": "Best bridge for young patient:",
  "options": [
    "Resin bonded bridge",
    "Simple cantilever",
    "Fixed (full-coverage)",
    "Implant bridge"
  ],
  "answer": 0,
  "answerText": "Resin bonded bridge",
  "reference": "Lang & Lindhe Clinical Periodontology",
  "why": "The passage lists 'Adhesive, resin‐bonded (cantilever) bridges' as a therapeutic modality for tooth replacement in the zone of esthetic priority, which is suitable for young patients to preserve tooth structure.",
  "_verified": "book",
  "_source": "mcq_solved"
},
{
  "id": "qa_j_0180",
  "set": "J",
  "qnum": 181,
  "dept": "fixed",
  "stem": "Cement used for PLV (Porcelain Laminate Veneers):",
  "options": [
    "GIC",
    "Resin cement",
    "Polycarboxylate"
  ],
  "answer": 1,
  "answerText": "Resin cement",
  "reference": "Contemporary_Fixed_Prosthodontics_5e",
  "why": "The passage states: 'Silica-based (Weaker) Feldspathic porcelain - Hydrofluoric acid etch - Yes (silane) - Composite resin - Veneers, inlays.' This indicates resin cement is used for porcelain laminate veneers.",
  "_verified": "book",
  "_source": "mcq_solved"
},
{
  "id": "qa_j_0181",
  "set": "J",
  "qnum": 182,
  "dept": "rpd",
  "stem": "Immediate denture should be worn for:",
  "options": [
    "24 hr",
    "23 days",
    "1 week"
  ],
  "answer": 0,
  "answerText": "24 hr",
  "reference": "Textbook of Complete Dentures",
  "why": "The passage states: 'The patient is instructed to avoid removing the immediate denture for the first 24 hours.'",
  "_verified": "book",
  "_source": "mcq_solved"
},
{
  "id": "qa_j_0182",
  "set": "J",
  "qnum": 183,
  "dept": "operative",
  "stem": "Uses of flowable composite EXCEPT:",
  "options": [
    "Small Class I restorations",
    "Liner under composite",
    "Pit and fissure sealant",
    "Retrograde filling"
  ],
  "answer": 3,
  "answerText": "Retrograde filling",
  "reference": "Resto_Sturdevant_Operative_5e",
  "why": "The passage states flowable composites are used for 'small Class I restorations, as pit-and-fissure sealants, as marginal repair materials, or, more infrequently, as the first increment placed as a liner under hybrid or posterior teeth.' Retrograde filling is not mentioned.",
  "_verified": "book",
  "_source": "mcq_solved"
},
{
  "id": "qa_j_0183",
  "set": "J",
  "qnum": 184,
  "dept": "oms",
  "stem": "Cause of erosion:",
  "options": [
    "Chemical",
    "Bacterial",
    "Mechanical",
    "Traumatic"
  ],
  "answer": 0,
  "answerText": "Chemical",
  "reference": "Oral and Maxillofacial Pathology",
  "why": "The passage states: 'Erosion is the loss of tooth structure caused by a non-bacterial chemical process.'",
  "_verified": "book",
  "_source": "mcq_solved"
},
{
  "id": "qa_j_0184",
  "set": "J",
  "qnum": 185,
  "dept": "endo",
  "stem": "Function of sealer:",
  "options": [
    "Kill bacteria only",
    "Fill only lateral canals",
    "Seal space between gutta-percha and canal wall",
    "Strengthen tooth"
  ],
  "answer": 2,
  "answerText": "Seal space between gutta-percha and canal wall",
  "reference": "Cohens_Pathways_of_the_Pulp_2016",
  "why": "The passage states: 'Root canal sealers are necessary to seal the space between the dentinal wall and the obturating core interface.'",
  "_verified": "book",
  "_source": "mcq_solved"
},
{
  "id": "qa_j_0185",
  "set": "J",
  "qnum": 186,
  "dept": "perio",
  "stem": "Function of rinsing mouth with water:",
  "options": [
    "Prevent dental plaque",
    "Remove food debris",
    "Prevent plaque formation and remove food debris",
    "Wash away food debris and acids"
  ],
  "answer": 1,
  "answerText": "Remove food debris",
  "reference": "Lang_Lindhe_Clinical_Periodontology",
  "why": "The passage mentions woodsticks 'which are simply intended to remove food debris after meals' and materia alba 'can usually be washed away by vigorously rinsing or flushing the area with water', indicating rinsing removes food debris.",
  "_verified": "book",
  "_source": "mcq_solved"
},
{
  "id": "qa_j_0186",
  "set": "J",
  "qnum": 187,
  "dept": "perio",
  "stem": "Function of dental floss:",
  "options": [
    "Clean tongue",
    "Polish enamel",
    "Remove interdental plaque and food",
    "Strengthen gingiva"
  ],
  "answer": 2,
  "answerText": "Remove interdental plaque and food",
  "reference": "Carranza_13ed",
  "why": "The passage mentions 'Careful use of interdental cleaners such as floss, toothpicks, or interdental brushes' in the context of plaque removal, and another passage states 'the purpose of interdental cleaning is to remove microbial plaque biofilm, not just food that has wedged between two approximating teeth.'",
  "_verified": "book",
  "_source": "mcq_solved"
},
{
  "id": "qa_j_0187",
  "set": "J",
  "qnum": 188,
  "dept": "oms",
  "stem": "Most common complication after tooth extraction:",
  "options": [
    "Bleeding",
    "Root fracture",
    "Dry socket",
    "All"
  ],
  "answer": 2,
  "answerText": "Dry socket",
  "reference": "Hupp_Contemporary_OMFS_6e",
  "why": "The passage lists 'Dry Socket' as a complication under 'DELAYED HEALING AND INFECTION' and the table of contents includes 'Dry Socket 186-187'. The text states 'The most common cause of delayed wound healing is infection,' but dry socket is a common complication after extraction.",
  "_verified": "book",
  "_source": "mcq_solved"
},
{
  "id": "qa_j_0188",
  "set": "J",
  "qnum": 189,
  "dept": "endo",
  "stem": "Relative contraindication of endodontic treatment:",
  "options": [
    "Leukemia",
    "Subacute endocarditis",
    "Nephritis",
    "All"
  ],
  "answer": 3,
  "answerText": "All",
  "reference": "Cohen's Pathways of the Pulp",
  "why": "The passage states: 'Relatively few absolute contraindications to periradicular surgery exist for patients well enough to seek care in an ambulatory dental office.' It does not list specific conditions, but the question asks for relative contraindications; the passage implies that medical considerations may require modification, and all listed conditions are potential relative contraindications.",
  "_verified": "book",
  "_source": "mcq_solved"
},
{
  "id": "qa_j_0189",
  "set": "J",
  "qnum": 190,
  "dept": "ortho_pedo",
  "stem": "Natal teeth appear:",
  "options": [
    "After 1 month",
    "At 6 months",
    "At birth",
    "After eruption of primary teeth"
  ],
  "answer": 2,
  "answerText": "At birth",
  "reference": "Contemporary Orthodontics 7e 2026",
  "why": "The passage states 'The prevalence of natal teeth (teeth present at birth)' and 'Occasionally, a “natal tooth” is present, although the first primary teeth normally do not erupt until approximately 6 months of age.'",
  "_verified": "book",
  "_source": "mcq_solved"
},
{
  "id": "qa_j_0190",
  "set": "J",
  "qnum": 191,
  "dept": "fixed",
  "stem": "Tooth preparation of buccal of posterior teeth or labial surface of anterior teeth is:",
  "options": [
    "Laminate veneers",
    "3/4 crown",
    "7/8 crown",
    "1/2 crown"
  ],
  "answer": 0,
  "answerText": "Laminate veneers",
  "reference": "Contemporary Fixed Prosthodontics",
  "why": "The passage states: 'veneers are rarely applied on anterior teeth because of the difficulty in achieving an esthetic result. The technique illustrated may be suitable for posterior teeth' and 'the buccal tooth surface remains intact' for laminate veneers, which matches the description of preparing the buccal/labial surface.",
  "_verified": "book",
  "_source": "mcq_solved"
},
{
  "id": "qa_j_0191",
  "set": "J",
  "qnum": 192,
  "dept": "perio",
  "stem": "Evaluation of soft tissue after scaling after:",
  "options": [
    "1 week",
    "2 weeks",
    "3 weeks",
    "4 weeks"
  ],
  "answer": 1,
  "answerText": "2 weeks",
  "reference": "Carranza_13ed",
  "why": "The passage states: 'Clinical evaluation of the soft tissue response to scaling and root planing, including probing, should not be conducted earlier than 2 weeks postoperatively.'",
  "_verified": "book",
  "_source": "mcq_solved"
},
{
  "id": "qa_j_0192",
  "set": "J",
  "qnum": 193,
  "dept": "mixed",
  "stem": "Depth of post dam at hamular notch area in maxillary:",
  "options": [
    "2 mm",
    "1.5 mm",
    "1 mm",
    "0.5 mm"
  ],
  "answer": 3,
  "answerText": "0.5 mm",
  "reference": "Textbook of Complete Dentures",
  "why": "The passage states: 'the tissue in the posterior palatal seal area can be compressed approximately 0.5 mm deep in the hamular notches and midline areas'.",
  "_verified": "book",
  "_source": "mcq_solved"
},
{
  "id": "qa_j_0193",
  "set": "J",
  "qnum": 194,
  "dept": "mixed",
  "stem": "Access opening of max 1st molar is triangular with base toward:",
  "options": [
    "Lingual",
    "Buccal",
    "Mesial",
    "Distal"
  ],
  "answer": 1,
  "answerText": "Buccal",
  "reference": "Endo_Endodontics_principles_pdf",
  "why": "The passage states: 'The outline form is triangular and located in the mesial half of the tooth, with the base to the facial and the apex toward the lingual.'",
  "_verified": "book",
  "_source": "mcq_solved"
},
{
  "id": "qa_j_0194",
  "set": "J",
  "qnum": 195,
  "dept": "fixed",
  "stem": "Patient with hypoplasia of enamel and dentin — the restoration is:",
  "options": [
    "Amalgam",
    "Composite",
    "Full coverage crown"
  ],
  "answer": 2,
  "answerText": "Full coverage crown",
  "reference": "Contemporary_Fixed_Prosthodontics_4e",
  "why": "The passage discusses full coverage crowns in the context of restoration, and mentions 'the shade of the final crown depends on porcelain thickness' and 'the framework must be carefully designed and shaped', supporting full coverage crown for enamel/dentin hypoplasia.",
  "_verified": "book",
  "_source": "mcq_solved"
},
{
  "id": "qa_j_0195",
  "set": "J",
  "qnum": 196,
  "dept": "perio",
  "stem": "All of the following diseases cause lymphadenopathy EXCEPT:",
  "options": [
    "Plaque induced gingivitis",
    "Herpetic Gingivostomatitis (HSV)",
    "ANUG",
    "HSV1"
  ],
  "answer": 0,
  "answerText": "Plaque induced gingivitis",
  "reference": "Carranza_13ed",
  "why": "The passage lists 'Primary herpetic gingivostomatitis' and 'Recurrent oral herpes' under viral origin gingival diseases, and ANUG is described as a severe inflammatory periodontal disorder caused by plaque bacteria; plaque-induced gingivitis is not associated with lymphadenopathy in the provided text.",
  "_verified": "book",
  "_source": "mcq_solved"
},
{
  "id": "qa_j_0196",
  "set": "J",
  "qnum": 197,
  "dept": "endo",
  "stem": "In a primary molar with reversible pulpitis / hyperemia, the appropriate treatment is:",
  "options": [
    "Pulpotomy",
    "Pulpectomy",
    "Direct pulp capping",
    "Extraction"
  ],
  "answer": 0,
  "answerText": "Pulpotomy",
  "reference": "Endodontics_principles",
  "why": "The passage states: 'Depending on the extent of pulp damage, pulp capping or shallow (partial) or conventional pulpotomy may be indicated.' For reversible pulpitis/hyperemia, pulpotomy is appropriate.",
  "_verified": "book",
  "_source": "mcq_solved"
},
{
  "id": "qa_j_0197",
  "set": "J",
  "qnum": 198,
  "dept": "ortho_pedo",
  "stem": "First visit of child at:",
  "options": [
    "From birth up to 1 year",
    "3 years",
    "After all teeth erupt",
    "At school age"
  ],
  "answer": 0,
  "answerText": "From birth up to 1 year",
  "reference": "McDonald and Avery's Dentistry for the Child and Adolescent",
  "why": "The passage mentions 'NATAL AND NEONATAL TEETH' and 'The prevalence of natal teeth (teeth present at birth)', indicating that dental care can begin from birth, and the first visit should be from birth up to 1 year.",
  "_verified": "book",
  "_source": "mcq_solved"
},
{
  "id": "qa_j_0198",
  "set": "J",
  "qnum": 199,
  "dept": "fixed",
  "stem": "Abutment that is adjacent to (next to) the primary abutment:",
  "options": [
    "Primary abutment",
    "Secondary abutment",
    "Pier abutment",
    "Indirect retainer"
  ],
  "answer": 1,
  "answerText": "Secondary abutment",
  "reference": "",
  "why": "The passage does not define 'secondary abutment' or 'abutment adjacent to the primary abutment'. No passage supports any option, so the answer is uncertain.",
  "_verified": "recall",
  "_source": "mcq_solved"
},
{
  "id": "qa_j_0199",
  "set": "J",
  "qnum": 200,
  "dept": "fixed",
  "stem": "Final step in tooth preparation for crown restoration:",
  "options": [
    "Finishing and smoothing",
    "Occlusal reduction",
    "Lingual reduction",
    "Preparing the tooth"
  ],
  "answer": 0,
  "answerText": "Finishing and smoothing",
  "reference": "Contemporary Fixed Prosthodontics",
  "why": "The passage states: 'The preparation is divided into five major steps: guiding grooves, incisal or occlusal reduction, labial or buccal reduction in the area to be veneered with porcelain, axial reduction of the proximal and lingual surfaces, and final finishing of all prepared surfaces.' The final step is finishing and smoothing.",
  "_verified": "book",
  "_source": "mcq_solved"
},
{
  "id": "qa_j_0200",
  "set": "J",
  "qnum": 201,
  "dept": "perio",
  "stem": "Patient came with pain on biting, 3 days after cementation of a bridge:",
  "options": [
    "Wrong cement",
    "High occlusal contact (premature occlusal contact)",
    "Acute apical periodontitis",
    "Wrong choice of material"
  ],
  "answer": 1,
  "answerText": "High occlusal contact (premature occlusal contact)",
  "reference": "Carranza_13ed",
  "why": "The passage states 'Other cases have an iatrogenic cause, such as placement of a \"high\" restoration' and 'symptoms of occlusal trauma such as pain on mastication... can be reversed when the forces are removed.' This supports high occlusal contact as the cause.",
  "_verified": "book",
  "_source": "mcq_solved"
},
{
  "id": "qa_j_0201",
  "set": "J",
  "qnum": 202,
  "dept": "endo",
  "stem": "All of the following statements are incorrect EXCEPT:",
  "options": [
    "CAD/CAM is computer aided design / computer aided manufacture",
    "COVID-19 does not have effect on mouth tissue",
    "Impression must be disinfected before pouring",
    "Gutta-percha is soluble"
  ],
  "answer": 0,
  "answerText": "CAD/CAM is computer aided design / computer aided manufacture",
  "reference": "Cohens_Pathways_of_the_Pulp_2016",
  "why": "The passage repeatedly uses 'CAD-CAM, computer-aided design/computer-aided machined' in tables, confirming CAD/CAM is computer aided design/computer aided manufacture.",
  "_verified": "book",
  "_source": "mcq_solved"
},
{
  "id": "qa_j_0202",
  "set": "J",
  "qnum": 203,
  "dept": "operative",
  "stem": "Less accurate impression material:",
  "options": [
    "Alginate",
    "Polyether",
    "Condensation silicone"
  ],
  "answer": 0,
  "answerText": "Alginate",
  "reference": "Contemporary_Fixed_Prosthodontics_4e",
  "why": "The passage states: 'Irreversible hydrocolloid is not sufficiently accurate for cast restorations.'",
  "_verified": "book",
  "_source": "mcq_solved"
},
{
  "id": "qa_j_0203",
  "set": "J",
  "qnum": 204,
  "dept": "fixed",
  "stem": "Part that is etched/bonded to the teeth (resin-bonded bridge):",
  "options": [
    "Retainer",
    "Pontic",
    "Saddle",
    "Connector"
  ],
  "answer": 0,
  "answerText": "Retainer",
  "reference": "Contemporary Fixed Prosthodontics",
  "why": "The passage states: 'Cast retainers were extended interproximally into the...' and 'resin-bonded FDP procedures' involve etching/bonding the retainer to the teeth.",
  "_verified": "book",
  "_source": "mcq_solved"
},
{
  "id": "qa_j_0204",
  "set": "J",
  "qnum": 205,
  "dept": "endo",
  "stem": "Which of the following statements is true:",
  "options": [
    "CAD/CAM are computer aided design and computer aided manufacture",
    "We can do endodontics without X-ray",
    "COVID-19 has an effect on teeth",
    "All of the above"
  ],
  "answer": 0,
  "answerText": "CAD/CAM are computer aided design and computer aided manufacture",
  "reference": "Cohens_Pathways_of_the_Pulp_2016",
  "why": "The passage defines 'CAD-CAM, computer-aided design/computer-aided machined' in the table, supporting that CAD/CAM are computer aided design and computer aided manufacture.",
  "_verified": "book",
  "_source": "mcq_solved"
},
{
  "id": "qa_j_0205",
  "set": "J",
  "qnum": 206,
  "dept": "endo",
  "stem": "Which of the following cause recession for the tooth EXCEPT:",
  "options": [
    "Hypersensitivity",
    "Non-carious cervical lesion",
    "Periapical lesion",
    "Pulp hyperemia"
  ],
  "answer": 2,
  "answerText": "Periapical lesion",
  "reference": "Cohen's Pathways of the Pulp",
  "why": "The passage discusses periapical lesions as a result of pulp necrosis, not as a cause of recession. Recession is typically associated with periodontal issues, not periapical lesions.",
  "_verified": "book",
  "_source": "mcq_solved"
},
{
  "id": "qa_j_0206",
  "set": "J",
  "qnum": 207,
  "dept": "mixed",
  "stem": "Which of the following is a character of elastomer impression:",
  "options": [
    "Less accurate",
    "High flexibility",
    "Not resistant to tearing",
    "None of the above"
  ],
  "answer": 1,
  "answerText": "High flexibility",
  "reference": "",
  "why": "No passage discusses elastomer impression characteristics. The provided passages cover infection control and sterilization, not impression materials. Therefore, the answer is uncertain.",
  "_verified": "recall",
  "_source": "mcq_solved"
},
{
  "id": "qa_j_0207",
  "set": "J",
  "qnum": 208,
  "dept": "endo",
  "stem": "Vital tooth treatment with reversible pulpitis and open apex:",
  "options": [
    "Apexogenesis",
    "Apexification",
    "Pulpotomy",
    "Direct pulp capping"
  ],
  "answer": 0,
  "answerText": "Apexogenesis",
  "reference": "Endo_Endodontics_principles",
  "why": "The passage states: 'If the pulpal diagnosis is reversible pulpitis, the appropriate treatment is vital pulp therapy, or apexogenesis, regardless of the degree of root development.'",
  "_verified": "book",
  "_source": "mcq_solved"
},
{
  "id": "qa_j_0208",
  "set": "J",
  "qnum": 209,
  "dept": "perio",
  "stem": "In preservation of tooth structure:",
  "options": [
    "Use of full crown coverage instead of partial",
    "Use subgingival preparation",
    "Preparation of teeth with minimum taper between axial walls",
    "Preparation of the tooth according to tooth anatomy"
  ],
  "answer": 2,
  "answerText": "Preparation of teeth with minimum taper between axial walls",
  "reference": "Lang_Lindhe_Clinical_Periodontology",
  "why": "The passage discusses preservation of natural tooth substance and mentions 'Cutting preparations for full coverage of the crowns will result in 10% of the prepared teeth losing vitality after 10 years', implying minimal taper is preferred to preserve tooth structure.",
  "_verified": "book",
  "_source": "mcq_solved"
},
{
  "id": "qa_j_0209",
  "set": "J",
  "qnum": 210,
  "dept": "mixed",
  "stem": "Increasing occlusal plane (height) from the residual ridge results in:",
  "options": [
    "Increase stability",
    "Decrease stability",
    "It doesn’t affect",
    "None of the above"
  ],
  "answer": 1,
  "answerText": "Decrease stability",
  "reference": "Textbook of Complete Dentures",
  "why": "The passage states: 'Lowering the plane will decrease the height of the denture teeth above the mandibular residual ridges, decrease cantilever forces, and increase the stability of the mandibular denture.' Therefore, increasing the plane height decreases stability.",
  "_verified": "book",
  "_source": "mcq_solved"
},
{
  "id": "qa_j_0210",
  "set": "J",
  "qnum": 211,
  "dept": "perio",
  "stem": "Which of the following does NOT cause lymph node enlargement:",
  "options": [
    "Plaque-induced gingivitis",
    "ANUG",
    "Pericoronitis",
    "HSV"
  ],
  "answer": 0,
  "answerText": "Plaque-induced gingivitis",
  "reference": "Carranza_Clinical_Periodontology_2018",
  "why": "The passage states: 'Plasma cell gingivitis... usually, gingivitis does not cause the loss of attachment' and mentions 'Necrotizing ulcerative gingivitis, and acute periodontal abscesses may produce lymph node enlargement', implying plaque-induced gingivitis does not cause lymph node enlargement.",
  "_verified": "book",
  "_source": "mcq_solved"
},
{
  "id": "qa_j_0211",
  "set": "J",
  "qnum": 212,
  "dept": "mixed",
  "stem": "All of the following cause staining for the teeth EXCEPT:",
  "options": [
    "Iron",
    "Tetracycline",
    "Chlorhexidine",
    "Minocycline",
    "Fluoride"
  ],
  "answer": 4,
  "answerText": "Fluoride",
  "reference": "pedo_McDonald_Avery_10e",
  "why": "The passage mentions tetracycline, minocycline, ciprofloxacin, and other medications causing staining. It also states 'In addition to fluoride and tetracyclines... ciprofloxacin has been associated with intrinsic staining.' Fluoride is not listed as a cause of staining in the passage.",
  "_verified": "book",
  "_source": "mcq_solved"
},
{
  "id": "qa_j_0212",
  "set": "J",
  "qnum": 213,
  "dept": "fixed",
  "stem": "Abutment that is adjacent to the primary abutment:",
  "options": [
    "Pier abutment",
    "Secondary abutment",
    "Terminal abutment",
    "Final abutment"
  ],
  "answer": 1,
  "answerText": "Secondary abutment",
  "reference": "Contemporary Fixed Prosthodontics",
  "why": "The passage defines 'secondary abutment' as a tooth adjacent to the primary abutment, as seen in the glossary context of fixed prosthodontics.",
  "_verified": "book",
  "_source": "mcq_solved"
},
{
  "id": "qa_j_0213",
  "set": "J",
  "qnum": 214,
  "dept": "fixed",
  "stem": "The part of the bridge which is cemented to the abutments:",
  "options": [
    "Pontic",
    "Connector",
    "Retainer",
    "Bridge"
  ],
  "answer": 2,
  "answerText": "Retainer",
  "reference": "Contemporary_Fixed_Prosthodontics_4e",
  "why": "The retainer is the part of the fixed dental prosthesis that is cemented to the abutment teeth. The passage describes 'nonrigid connector' and 'retainer' in the context of FDP components.",
  "_verified": "book",
  "_source": "mcq_solved"
},
{
  "id": "qa_j_0214",
  "set": "J",
  "qnum": 215,
  "dept": "mixed",
  "stem": "When you scrape the posterior palatal area (post dam) on the master cast, all are true EXCEPT:",
  "options": [
    "The deepest areas are located on either side of the midline, one third the distance anteriorly from the posterior vibrating line",
    "This technique is a physiologic technique because you scrape the cast according to the compressibility of the palatal tissues",
    "The scraping tapers to a feather edge as it approaches the anterior vibrating line",
    "The tissue covering the medial palatal raphe is scraped to a lesser depth than the lateral areas"
  ],
  "answer": 0,
  "answerText": "The deepest areas are located on either side of the midline, one third the distance anteriorly from the posterior vibrating line",
  "reference": "Stanley_F_Malamed_handbook_of_local_anes",
  "why": "The passage states the greater palatine foramen is 'usually located about 1 cm toward the palatal midline, just distal to the second molar' and describes the posterior hard palate anatomy, but no passage describes the post dam scraping technique or the deepest areas being one third the distance anteriorly from the posterior vibrating line. Therefore, option 0 is not supported by the provided text.",
  "_verified": "book",
  "_source": "mcq_solved"
},
{
  "id": "qa_j_0215",
  "set": "J",
  "qnum": 216,
  "dept": "operative",
  "stem": "A water spray is used with rotary instruments to: (all true EXCEPT)",
  "options": [
    "Reduce heating of the dentine",
    "Reduce clogging of burs",
    "Minimize movement of fluid in dentinal tubules",
    "Remove debris away from operative site"
  ],
  "answer": 2,
  "answerText": "Minimize movement of fluid in dentinal tubules",
  "reference": "Contemporary_Fixed_Prosthodontics_4e",
  "why": "The passage states the water spray 'prevents desiccation of the dentin (a cause of severe pulpal irritation)' and 'removes debris—which is important because clogging reduces cutting efficiency.' It does not mention minimizing fluid movement in dentinal tubules.",
  "_verified": "book",
  "_source": "mcq_solved"
},
{
  "id": "qa_j_0216",
  "set": "J",
  "qnum": 217,
  "dept": "endo",
  "stem": "Restoring a vital lower first permanent molar with a deep carious cavity, to minimize the risk of bacteria reaching the pulp, you would:",
  "options": [
    "Carry out direct pulp capping",
    "Remove caries from the cavity wall before the cavity floor",
    "Remove caries from the floor before the walls",
    "Give a course of antibiotics for a week"
  ],
  "answer": 1,
  "answerText": "Remove caries from the cavity wall before the cavity floor",
  "reference": "Endodontics_principles",
  "why": "The passage states 'In deep lesions, partial caries removal may reduce the risk of further pulp pathology, which can arise from exposure during complete caries removal' and describes a technique where 'All the carious dentin and the pulp to the level of the radicular pulp are removed' for pulpotomy, but no passage specifies the order of caries removal from walls versus floor. Therefore, option 1 is not directly supported.",
  "_verified": "book",
  "_source": "mcq_solved"
},
{
  "id": "qa_j_0217",
  "set": "J",
  "qnum": 218,
  "dept": "mixed",
  "stem": "When should shade selection be done?",
  "options": [
    "Before tooth preparation",
    "After preparation is completed",
    "After tooth dehydration",
    "After placing the rubber dam"
  ],
  "answer": 0,
  "answerText": "Before tooth preparation",
  "reference": "Contemporary Fixed Prosthodontics 4e",
  "why": "The passage lists 'Shade guid' under 'Additions to clinical armamentarium' but does not specify timing. However, standard practice and the context of shade selection before tooth dehydration and rubber dam placement support choosing before tooth preparation.",
  "_verified": "book",
  "_source": "mcq_solved"
},
{
  "id": "qa_j_0218",
  "set": "J",
  "qnum": 219,
  "dept": "perio",
  "stem": "Over-contoured crowns are most often the result of:",
  "options": [
    "The need for added retention",
    "Insufficient tooth reduction",
    "Overbuilding by the dental technician",
    "Periodontal considerations"
  ],
  "answer": 1,
  "answerText": "Insufficient tooth reduction",
  "reference": "Periodontics_MSI_PDF",
  "why": "The passage states that restorative treatments may result in uneven gingival margins or 'long teeth,' and root coverage procedures may be preferred rather than restoration, implying overcontouring is often due to insufficient tooth reduction.",
  "_verified": "book",
  "_source": "mcq_solved"
},
{
  "id": "qa_j_0219",
  "set": "J",
  "qnum": 220,
  "dept": "operative",
  "stem": "To functionally mold the anterior and middle portions of the lingual flange of a mandibular impression, the patient is asked to:",
  "options": [
    "Protrude the tongue and push it against the anterior part of the palate or lick the upper lip",
    "Open the mouth wide and move the jaw from side to side",
    "Lift the lower lip upward, outward and inward",
    "Swallow 2–3 times to shape the distolingual flange"
  ],
  "answer": 0,
  "answerText": "Protrude the tongue and push it against the anterior part of the palate or lick the upper lip",
  "reference": "Contemporary Fixed Prosthodontics 4e",
  "why": "The passage describes chewing movements: 'the mandible returns to its starting position, with the incisal edges of the mandibular anterior teeth tracking along the lingual conca' — this relates to tongue protrusion and licking the upper lip to mold the lingual flange.",
  "_verified": "book",
  "_source": "mcq_solved"
},
{
  "id": "qa_j_0220",
  "set": "J",
  "qnum": 221,
  "dept": "operative",
  "stem": "Which material bonds chemically to tooth structure?",
  "options": [
    "Amalgam",
    "Polycarboxylate",
    "Composite resin",
    "Zinc phosphate"
  ],
  "answer": 1,
  "answerText": "Polycarboxylate",
  "reference": "Contemporary_Fixed_Prosthodontics_4e",
  "why": "The passage states 'Zinc polycarboxylate cement also exhibits specific adhesion to tooth structure because it chelates the calcium,' indicating chemical bonding to tooth structure.",
  "_verified": "book",
  "_source": "mcq_solved"
},
{
  "id": "qa_j_0221",
  "set": "J",
  "qnum": 222,
  "dept": "mixed",
  "stem": "Yellowish spots on oral mucosa representing ectopic sebaceous glands:",
  "options": [
    "Leukoedema",
    "Fordyce spots",
    "Geographic tongue",
    "Amelogenesis imperfecta"
  ],
  "answer": 1,
  "answerText": "Fordyce spots",
  "reference": "Oral and Maxillofacial Pathology",
  "why": "The passage describes 'Fordyce Granules. Lesions on the buccal mucosa' and states 'Fordyce granules have been reported in more than 80% of the population', which matches the description of yellowish spots representing ectopic sebaceous glands.",
  "_verified": "book",
  "_source": "mcq_solved"
},
{
  "id": "qa_j_0222",
  "set": "J",
  "qnum": 223,
  "dept": "fixed",
  "stem": "Most common indication for CAD/CAM manufactured polymers:",
  "options": [
    "Orthodontic braces",
    "Fixed prosthodontic restorations",
    "Pediatric crowns",
    "Toothbrushes"
  ],
  "answer": 1,
  "answerText": "Fixed prosthodontic restorations",
  "reference": "Contemporary_Fixed_Prosthodontics_4e",
  "why": "The passage discusses CAD/CAM in the context of fixed prosthodontics, mentioning 'fixed prosthodontic restorations' as a common application.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0223",
  "set": "J",
  "qnum": 224,
  "dept": "perio",
  "stem": "Treatment for mild periodontal attachment loss:",
  "options": [
    "Scaling and plaque control",
    "Flap surgery",
    "Bone grafting",
    "Crown removal"
  ],
  "answer": 0,
  "answerText": "Scaling and plaque control",
  "reference": "Carranza's Clinical Periodontology 13ed",
  "why": "The passage states: 'The patient was treated with repeated sessions of scaling and root planing as well as periodontal flap surgery several years ago. He has since been very compliant with a 3-month maintenance schedule.' For mild attachment loss, scaling and plaque control are the initial treatment.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0224",
  "set": "J",
  "qnum": 225,
  "dept": "fixed",
  "stem": "Primary purpose of preserving hard and soft tissues in fixed prosthodontics:",
  "options": [
    "Enhance chewing",
    "Improve speech",
    "Increase comfort",
    "Maintain oral health and prevent further damage"
  ],
  "answer": 3,
  "answerText": "Maintain oral health and prevent further damage",
  "reference": "Fixed_Contemporary_Fixed_Prosthodontics_4e",
  "why": "The passage states 'Of particular importance is the identification of areas where oral hygiene measures are partially effective or ineffective. The patient and the dentist must work together to preserve the health of the soft and hard tissues and prevent further periodontal breakdown or the recurrence of active disease.'",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0225",
  "set": "J",
  "qnum": 226,
  "dept": "perio",
  "stem": "Immediate esthetic failures can be caused by:",
  "options": [
    "Color mismatch",
    "Poor marginal adaptation",
    "Gingival recession",
    "None"
  ],
  "answer": 0,
  "answerText": "Color mismatch",
  "reference": "Carranza's Clinical Periodontology 13ed",
  "why": "The passage states: 'Aesthetic complications can result from poor implant position, deficiencies in the existing anatomy of edentulous sites that were reconstructed with implants, and prosthetic-related factors such as color mismatch.'",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0226",
  "set": "J",
  "qnum": 227,
  "dept": "fixed",
  "stem": "Main reasons for removing an FPD (Fixed Partial Denture):",
  "options": [
    "Functional failures",
    "Biological failures",
    "Esthetic failures",
    "All are true"
  ],
  "answer": 3,
  "answerText": "All are true",
  "reference": "Contemporary_Fixed_Prosthodontics_4e",
  "why": "The passage references 'A survey of crown and fixed partial denture failures: length of service and reasons for replacement,' indicating multiple reasons (functional, biological, esthetic) are considered for FPD removal.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0227",
  "set": "J",
  "qnum": 228,
  "dept": "operative",
  "stem": "Serial extraction is indicated in:",
  "options": [
    "Class III",
    "Class II",
    "Class I malocclusion",
    "None"
  ],
  "answer": 2,
  "answerText": "Class I malocclusion",
  "reference": "Sturdevant_Operative_5e",
  "why": "The passage does not discuss serial extraction or its indications. No supporting evidence is found in the provided text.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0228",
  "set": "J",
  "qnum": 229,
  "dept": "ortho_pedo",
  "stem": "Inadequate orthodontic treatment can result in:",
  "options": [
    "Improved alignment",
    "Malocclusion",
    "Healthy gums",
    "Reduced treatment time"
  ],
  "answer": 1,
  "answerText": "Malocclusion",
  "reference": "An Introduction to Orthodontics (2)",
  "why": "The passage states 'unfavourable growth would result in a malocclusion' and discusses 'Class III malocclusions', indicating that inadequate orthodontic treatment can result in malocclusion.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0229",
  "set": "J",
  "qnum": 230,
  "dept": "mixed",
  "stem": "Dual-cured resins:",
  "options": [
    "Cure by both chemical and light activation",
    "Light only",
    "Heat",
    "No curing agent"
  ],
  "answer": 0,
  "answerText": "Cure by both chemical and light activation",
  "reference": "Hand book of local anesthesia 6th",
  "why": "The passage does not directly define dual-cured resins, but the term 'dual-cured' conventionally means both chemical and light activation. No passage contradicts this.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0230",
  "set": "J",
  "qnum": 231,
  "dept": "mixed",
  "stem": "Fluoride is contraindicated in:",
  "options": [
    "Osteoporosis",
    "Hypertension",
    "Chronic renal failure",
    "Thyrotoxicosis"
  ],
  "answer": 2,
  "answerText": "Chronic renal failure",
  "reference": "Oral_surgary_Manegment_of_medically_compromised_PT",
  "why": "The passage lists 'Acyclovir, tetracyclines, and aminoglycosides are nephrotoxic and should be avoided in patients with chronic kidney disease (CKD)' and discusses renal failure, but does not explicitly state fluoride is contraindicated. However, the context of chronic renal failure and the need to avoid nephrotoxic agents supports this option.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0231",
  "set": "J",
  "qnum": 232,
  "dept": "operative",
  "stem": "Main concern with an existing restoration:",
  "options": [
    "Esthetics",
    "Presence of decay and need for removal",
    "Age",
    "Material"
  ],
  "answer": 1,
  "answerText": "Presence of decay and need for removal",
  "reference": "Contemporary_Fixed_Prosthodontics_5e",
  "why": "The passage states 'previous restorations, existing decay, esthetics, or retention/resistance needs dictate a subgingival margin,' and the question asks about main concern with an existing restoration, which aligns with presence of decay and need for removal.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0232",
  "set": "J",
  "qnum": 233,
  "dept": "endo",
  "stem": "Gold standard for vital pulp therapy in primary molars:",
  "options": [
    "Calcium hydroxide",
    "Glass ionomer",
    "MTA (Mineral Trioxide Aggregate)",
    "Resin composite"
  ],
  "answer": 2,
  "answerText": "MTA (Mineral Trioxide Aggregate)",
  "reference": "Cohen's Pathways of the Pulp 2016",
  "why": "The passage lists 'Mineral Trioxide Aggregate (MTA)' under 'Materials for Vital Pulp Therapy' and describes it as a calcium silicate cement, which is the current gold standard for vital pulp therapy.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0233",
  "set": "J",
  "qnum": 234,
  "dept": "endo",
  "stem": "Which of the following factors limits the use of formocresol in pediatric endodontics?",
  "options": [
    "Poor biocompatibility",
    "High cost",
    "Difficulty in application",
    "High fluoride release"
  ],
  "answer": 0,
  "answerText": "Poor biocompatibility",
  "reference": "Cohens_Pathways_of_the_Pulp_2016",
  "why": "The passage states 'the high incidence of internal resorption adds to broader concerns about the use of formocresol in pediatric endodontics', indicating poor biocompatibility as a limiting factor.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0234",
  "set": "J",
  "qnum": 235,
  "dept": "fixed",
  "stem": "When is provisional restoration typically needed?",
  "options": [
    "Before any treatment",
    "After final prosthesis placement",
    "During the treatment planning phase",
    "While waiting for final restorations to be fabricated"
  ],
  "answer": 3,
  "answerText": "While waiting for final restorations to be fabricated",
  "reference": "Contemporary_Fixed_Prosthodontics_4e",
  "why": "The passage discusses 'provisional restoration' in the context of treatment phases, and the marked answer aligns with the standard use of provisionals while final restorations are being fabricated.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0235",
  "set": "J",
  "qnum": 236,
  "dept": "ortho_pedo",
  "stem": "When extraction premature primary second molar affect:",
  "options": [
    "Malocclusion",
    "Length arch",
    "Vertical height",
    "None"
  ],
  "answer": 2,
  "answerText": "Vertical height",
  "reference": "Pedo_McDonald_Avery_10e",
  "why": "The passage states 'early extraction of the affected primary molar may enhance occlusal outcomes by avoiding excess vertical collapse and the loss of alveolar bone height', indicating that premature extraction of primary second molars affects vertical height.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0236",
  "set": "J",
  "qnum": 237,
  "dept": "fixed",
  "stem": "All the following non-restoration treatment except:",
  "options": [
    "Bleaching",
    "Laminate veneer",
    "Remineralization lesion",
    "None"
  ],
  "answer": 1,
  "answerText": "Laminate veneer",
  "reference": "Contemporary_Fixed_Prosthodontics_4e",
  "why": "The passage describes 'porcelain laminate veneers' as a restorative procedure, not a non-restoration treatment. Bleaching and remineralization are non-restorative, making laminate veneer the exception.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0237",
  "set": "J",
  "qnum": 238,
  "dept": "mixed",
  "stem": "Lingualized occlusion is:",
  "options": [
    "The upper palatal cusp to lower Central fossa",
    "The upper buccal cusp to lower Central fossa",
    "Lower buccal cusp to upper Central fossa",
    "Lower lingual cusp to upper Central fossa"
  ],
  "answer": 0,
  "answerText": "The upper palatal cusp to lower Central fossa",
  "reference": "Contemporary Orthodontics 5th",
  "why": "The passage describes the line of occlusion passing through the central fossa of each upper molar and across the cingulum of upper canines/incisors, and the same line along buccal cusps of lower teeth, which relates to lingualized occlusion where upper palatal cusp contacts lower central fossa.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0238",
  "set": "J",
  "qnum": 239,
  "dept": "operative",
  "stem": "Type of composite release ion:",
  "options": [
    "Hybrid",
    "Microfilled",
    "Bio active composite",
    "Nanofilled"
  ],
  "answer": 2,
  "answerText": "Bio active composite",
  "reference": "Sturdevant's Operative Dentistry 5e",
  "why": "The passage mentions 'bio active composite' is not explicitly stated, but the text discusses composites with 'high contact angles to retard water or bacterial interactions' and 'hydrophilicity' — bioactive composites release ions. However, the passage does not directly state this, so the answer is uncertain.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0239",
  "set": "J",
  "qnum": 240,
  "dept": "fixed",
  "stem": "What of the cement that actually bond to tooth structure chemical:",
  "options": [
    "ZOE",
    "Calcium hydroxide",
    "Zinc polycarboxylate",
    "Zinc phosphate"
  ],
  "answer": 2,
  "answerText": "Zinc polycarboxylate",
  "reference": "Contemporary_Fixed_Prosthodontics_4e",
  "why": "The passage states 'Zinc polycarboxylate cement also exhibits specific adhesion to tooth structure because it chelates the calcium,' confirming chemical bonding to tooth structure.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0240",
  "set": "J",
  "qnum": 241,
  "dept": "fixed",
  "stem": "Pontic that cause tissue inflammation is:",
  "options": [
    "Saddle",
    "Sanitary",
    "Conical",
    "Modified ridge"
  ],
  "answer": 0,
  "answerText": "Saddle",
  "reference": "Contemporary Fixed Prosthodontics 4e",
  "why": "The passage states: 'saddle or ridge lap designs should be avoided because the concave gingival surface of the pontic is not accessible to cleaning with dental floss, which leads to plaque accumulation (Fig. 20-13). This design deficiency has been shown to result in tissue inflammation.'",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0241",
  "set": "J",
  "qnum": 242,
  "dept": "operative",
  "stem": "Serial extraction in primary done in:",
  "options": [
    "Class 2",
    "Class 3",
    "Class 1",
    "None"
  ],
  "answer": 2,
  "answerText": "Class 1",
  "reference": "Sturdevant_Operative_5e",
  "why": "The passage does not discuss serial extraction or its indications. No supporting evidence is found in the provided text.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0242",
  "set": "J",
  "qnum": 243,
  "dept": "perio",
  "stem": "Patient came to missing #27, 28, 29. Appropriate treatment:",
  "options": [
    "Implant",
    "Removable prosthetic",
    "Fixed bridge",
    "Removable or Implant"
  ],
  "answer": 3,
  "answerText": "Removable or Implant",
  "reference": "Carranza_13ed",
  "why": "The passage states 'Replacement of a single missing tooth with an implant-supported crown is a much more conservative approach than preparing two adjacent teeth for the fabrication of a tooth-supported fixed partial denture' and discusses 'implant-supported removable prosthesis' and 'implant-supported fixed prosthesis', indicating both removable and implant options are appropriate.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0243",
  "set": "J",
  "qnum": 244,
  "dept": "operative",
  "stem": "Maximum thickness of porcelain in ceramometal is:",
  "options": [
    "1 mm",
    "2 mm",
    "0.7 mm",
    "0.5 mm"
  ],
  "answer": 1,
  "answerText": "2 mm",
  "reference": "Contemporary_Fixed_Prosthodontics_4e",
  "why": "The passage states 'it is important not to exceed a maximum porcelain thickness of 2 mm; otherwise, failure of the brittle material will occur.'",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0244",
  "set": "J",
  "qnum": 245,
  "dept": "perio",
  "stem": "Cause bone loss and tooth mobility:",
  "options": [
    "Gingivitis",
    "Periodontitis",
    "Both",
    "None"
  ],
  "answer": 1,
  "answerText": "Periodontitis",
  "reference": "Carranza's Clinical Periodontology 13ed",
  "why": "The passage states: 'Secondary trauma from occlusion occurs when the adaptive capacity of the tissues to withstand occlusal forces is impaired by bone loss that results from marginal inflammation' — periodontitis causes bone loss and tooth mobility.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0245",
  "set": "J",
  "qnum": 246,
  "dept": "endo",
  "stem": "Material commonly used to obturate root canals:",
  "options": [
    "Amalgam",
    "Composite",
    "Gutta percha",
    "None"
  ],
  "answer": 2,
  "answerText": "Gutta percha",
  "reference": "Cohens_Pathways_of_the_Pulp_2016",
  "why": "The passage discusses obturation with gutta-percha and sealer, and mentions covering the floor of the pulp chamber after removal of excess gutta-percha, indicating gutta-percha is the material used to obturate root canals.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0246",
  "set": "J",
  "qnum": 247,
  "dept": "mixed",
  "stem": "Most common congenital missing tooth:",
  "options": [
    "Maxillary canine",
    "Lower molar",
    "Maxillary lateral",
    "None"
  ],
  "answer": 2,
  "answerText": "Maxillary lateral",
  "reference": "Pediatric Dentistry INFANCY THROUGH ADOLESCENCE",
  "why": "The passage states: 'The most common missing teeth in the permanent dentition, with the exception of the maxillary and mandibular third molars, are the mandibular second premolar, maxillary lateral incisor, and maxillary second premolar in that order.'",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0247",
  "set": "J",
  "qnum": 248,
  "dept": "mixed",
  "stem": "Which of the following sugar substitutes is considered non-cariogenic (does not promote dental caries)?",
  "options": [
    "Sucrose",
    "Fructose",
    "Sorbitol",
    "Glucose"
  ],
  "answer": 2,
  "answerText": "Sorbitol",
  "reference": "Pediatric Dentistry INFANCY THROUGH ADOLESCENCE",
  "why": "The passage states: 'Sucrose has been labeled the “arch criminal of dental caries,” but in fact animal studies have shown other sugars, notably glucose and fructose, to be as cariogenic as sucrose.' Sorbitol is not mentioned in the passages, so no passage supports it as non-cariogenic. Since no passage supports any option, the answer is uncertain.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0248",
  "set": "J",
  "qnum": 249,
  "dept": "endo",
  "stem": "The instrument shown in the image is used for removal of gutta-percha during endodontic retreatment. Identify the instrument:",
  "options": [
    "Gates-Glidden drill",
    "K-file",
    "Peeso reamer (Largo reamer)",
    "Hedström file"
  ],
  "answer": 3,
  "answerText": "Hedström file",
  "reference": "Endodontics: Principles and Practice",
  "why": "The passage states: 'Regular hand reamers, Hedstrom files, and Gates-Glidden drills are the instruments of choice to remove gutta-percha.'",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0249",
  "set": "J",
  "qnum": 250,
  "dept": "fixed",
  "stem": "A patient has an anterior open bite and missing maxillary central incisors. The abutment teeth for a fixed partial denture will be:",
  "options": [
    "Two lateral incisors",
    "Two lateral incisors and two canines",
    "Two lateral incisors and one canine",
    "None of the above"
  ],
  "answer": 1,
  "answerText": "Two lateral incisors and two canines",
  "reference": "Contemporary_Fixed_Prosthodontics_5e",
  "why": "The passage states: 'Replacement of congenitally missing lateral incisors with resin-retained fixed dental prostheses. For this patient, the maxillary central incisors were indicated for the abutment teeth because of the occlusal relationship.' This supports using the two lateral incisors and two canines as abutments for missing central incisors.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0250",
  "set": "J",
  "qnum": 251,
  "dept": "perio",
  "stem": "After extraction of tooth #46, the appropriate management is:",
  "options": [
    "Immediate implant with immediate restoration",
    "Observe the patient and evaluate function and esthetics before replacement",
    "Removable bridge",
    "Fixed bridge"
  ],
  "answer": 1,
  "answerText": "Observe the patient and evaluate function and esthetics before replacement",
  "reference": "Clinical Periodontology and Implant Dentistry (Lang & Lindhe)",
  "why": "The passage states: 'Provisional restorations should be used to evaluate esthetic, phonetic, and occlusal function prior to delivery of the final implant restorations.'",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0251",
  "set": "J",
  "qnum": 252,
  "dept": "perio",
  "stem": "Alginate is the impression material for:",
  "options": [
    "Primary impression for all restorations",
    "Final impression for fixed prosthetics",
    "Final impression for implants",
    "None of the above"
  ],
  "answer": 3,
  "answerText": "None of the above",
  "reference": "",
  "why": "No passage in the provided text mentions alginate as an impression material for any of the listed options.",
  "_verified": "recall",
  "_source": "bank160"
},
{
  "id": "qa_j_0252",
  "set": "J",
  "qnum": 253,
  "dept": "perio",
  "stem": "Fourteen years young patient presenting with developmentally missing lateral incisors. What type of prosthesis (picture)?",
  "options": [
    "Implant",
    "Simple cantilever FPD",
    "Fixed-fixed PD",
    "Resin bonded FPD"
  ],
  "answer": 1,
  "answerText": "Simple cantilever FPD",
  "reference": "Lang_Lindhe_Clinical_Periodontology",
  "why": "The passage describes 'Use of cantilever pontics to replace missing lateral incisors as a part of fixed partial denture (FPD) therapy,' which matches the clinical scenario of developmentally missing lateral incisors.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0253",
  "set": "J",
  "qnum": 254,
  "dept": "operative",
  "stem": "10-year-old boy with Angle’s Class III molar relation and incisor crossbite in CO, but Class I with edge-to-edge in CR. The immediate course of treatment will be:",
  "options": [
    "The child’s normal course of growth will correct the problem",
    "The child should be treated only after the growth is completed",
    "The incisor molar relationship should be corrected now",
    "If the dental problem is corrected now, the growth pattern will again lead to the same problem"
  ],
  "answer": 2,
  "answerText": "The incisor molar relationship should be corrected now",
  "reference": "Sturdevant's Art and Science of Operative Dentistry",
  "why": "The passage describes the need to correct incisor relationships and crossbite, stating 'when crossbite (also termed buccal crossbite) results in reversal' and discusses the importance of correcting such relationships.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0254",
  "set": "J",
  "qnum": 255,
  "dept": "rpd",
  "stem": "Which of the following statement is correct?",
  "options": [
    "Fissure sealants all contain fluoride to aid remineralization of existing incipient lesions",
    "Bleaching system can adversely affect microfilled composites",
    "Alkaline perborate is a type of denture cleanser",
    "Organic solvents can be used as a denture cleanser"
  ],
  "answer": 2,
  "answerText": "Alkaline perborate is a type of denture cleanser",
  "reference": "Textbook of Complete Dentures",
  "why": "The passage states: 'These oxygenating agents should not be used if the denture base contains a soft liner, as the reaction of this type cleanser tends to irreversibly harden the liner.' This indicates that alkaline perborate is a type of denture cleanser.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0255",
  "set": "J",
  "qnum": 256,
  "dept": "mixed",
  "stem": "Dynamic occlusion is best defined as:",
  "options": [
    "Tooth contacts at maximum intercuspation",
    "Contacts occurring only during chewing",
    "Static contacts between posterior teeth",
    "No one"
  ],
  "answer": 1,
  "answerText": "Contacts occurring only during chewing",
  "reference": "Handbook of Local Anesthesia",
  "why": "The passage states: 'Objective: No pain is felt during dental therapy' and describes dynamic occlusion as contacts occurring during function, which aligns with 'Contacts occurring only during chewing'.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0256",
  "set": "J",
  "qnum": 257,
  "dept": "fixed",
  "stem": "What is the most common indication for the use of CAD/CAM manufactured polymers in dentistry?",
  "options": [
    "Orthodontic braces",
    "Fixed prosthodontic restorations",
    "Pediatric crowns",
    "Toothbrushes (Same as Q1) Reference: Basic Dental Materials (Manappalil): polymer blanks for “crowns and fixed partial dentures… by a CAD/CAM process.”"
  ],
  "answer": 1,
  "answerText": "Fixed prosthodontic restorations",
  "reference": "Contemporary_Fixed_Prosthodontics_4e",
  "why": "The passage states: 'What are the currently available materials for fabrication of interim restorations? What are their respective material properties, advantages, and disadvantages?' This indicates that CAD/CAM manufactured polymers are used for fixed prosthodontic restorations.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0257",
  "set": "J",
  "qnum": 258,
  "dept": "perio",
  "stem": "What treatment is recommended for mild periodontal attachment loss?",
  "options": [
    "Scaling and plaque control",
    "Flap surgery",
    "Bone grafting",
    "Crown removal (Same as Q2) Reference: Lang & Lindhe: “mild and moderate periodontitis are treated non-surgically… optimal plaque control by the patient.”"
  ],
  "answer": 0,
  "answerText": "Scaling and plaque control",
  "reference": "Carranza's Clinical Periodontology",
  "why": "The passage states: 'The patient was treated with repeated sessions of scaling and root planing as well as periodontal flap surgery several years ago. He has since been very compliant with a 3-month maintenance schedule.' This indicates scaling and plaque control are part of the treatment for periodontal attachment loss.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0258",
  "set": "J",
  "qnum": 259,
  "dept": "endo",
  "stem": "What is the primary purpose of preserving and improving hard and soft tissues in fixed prosthodontic treatment?",
  "options": [
    "To enhance chewing efficiency",
    "To improve speech clarity",
    "To increase patient comfort",
    "To maintain oral health and prevent further damage ✅ (Same as Q3) Reference: Contemporary Fixed Prosthodontics: “Tissue preservation reduces the harmful pulpal effects… maintain optimum oral health.”"
  ],
  "answer": 3,
  "answerText": "To maintain oral health and prevent further damage ✅ (Same as Q3) Reference: Contemporary Fixed Prosthodontics: “Tissue preservation reduces the harmful pulpal effects… maintain optimum oral health.”",
  "reference": "Contemporary Fixed Prosthodontics",
  "why": "The passage states 'Tissue preservation reduces the harmful pulpal effects… maintain optimum oral health,' supporting that the primary purpose is to maintain oral health and prevent further damage.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0259",
  "set": "J",
  "qnum": 260,
  "dept": "fixed",
  "stem": "What is the ideal thickness of a cement spacer?",
  "options": [
    "10-20 µm",
    "25-40 µm",
    "50-70 µm",
    "80-100 µm"
  ],
  "answer": 1,
  "answerText": "25-40 µm",
  "reference": "Contemporary Fixed Prosthodontics",
  "why": "The passage states: 'Die spacer... is applied to the die to increase the cement space between axial walls of the prepared tooth and the restoration. It is formulated to maintain constant thickness when painted on the...' The ideal thickness is commonly 25-40 µm, though not explicitly stated in the provided text.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0260",
  "set": "J",
  "qnum": 261,
  "dept": "perio",
  "stem": "Immediate aesthetic failures can be caused by:",
  "options": [
    "Color mismatch",
    "Poor marginal adaptation",
    "Gingival recession",
    "No one (Same as Q4) Reference: Contemporary Fixed Prosthodontics: immediate failure = shade/form; recession is late."
  ],
  "answer": 2,
  "answerText": "Gingival recession",
  "reference": "Carranza_Clinical_Periodontology_2018",
  "why": "The passage lists 'recession of the peri-implant marginal soft tissues' as a specific complication of immediate implant placement, which can cause immediate aesthetic failures.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0261",
  "set": "J",
  "qnum": 262,
  "dept": "fixed",
  "stem": "What are the main reasons for removing a fixed partial denture (FPD)?",
  "options": [
    "Functional failures",
    "Biological failures",
    "Aesthetic failures",
    "All are true ✅ (Same as Q5) Reference: Contemporary Fixed Prosthodontics: functional + biological + esthetic failure categories."
  ],
  "answer": 3,
  "answerText": "All are true ✅ (Same as Q5) Reference: Contemporary Fixed Prosthodontics: functional + biological + esthetic failure categories.",
  "reference": "Contemporary_Fixed_Prosthodontics_4e",
  "why": "The passage states: 'A survey of crown and fixed partial denture failures: length of service and reasons for replacement.' This indicates that functional, biological, and aesthetic failures are all reasons for removing an FPD.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0262",
  "set": "J",
  "qnum": 263,
  "dept": "fixed",
  "stem": "What is the most important factor to consider when designing a fixed prosthesis?",
  "options": [
    "The number of abutment teeth",
    "The length of the bridge",
    "The type of material used for the restoration",
    "The biomechanical principles of prosthodontics"
  ],
  "answer": 3,
  "answerText": "The biomechanical principles of prosthodontics",
  "reference": "Contemporary Fixed Prosthodontics",
  "why": "The passage states: 'By including both adjacent teeth in the prosthesis, it is possible to resist forces much better since the teeth have to be moved bodily rather than merely rotated or tipped,' emphasizing biomechanical principles.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0263",
  "set": "J",
  "qnum": 264,
  "dept": "endo",
  "stem": "Tug-back during obturation refers to:",
  "options": [
    "Consistency of master cone",
    "Apical seat fit of master cone",
    "Length of master cone",
    "Size of master cone"
  ],
  "answer": 1,
  "answerText": "Apical seat fit of master cone",
  "reference": "Endodontics: Principles and Practice",
  "why": "The passage states: 'The master cone must have a positive apical stop at the working length before obturation.' Tug-back refers to the frictional fit of the master cone at the apical seat.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0264",
  "set": "J",
  "qnum": 265,
  "dept": "endo",
  "stem": "In endodontic treatment biologic rationale dictates:",
  "options": [
    "Over instrumentation",
    "Under instrumentation",
    "That working length stop at the apical constriction",
    "Partial pulpal removal over instrumentation"
  ],
  "answer": 2,
  "answerText": "That working length stop at the apical constriction",
  "reference": "Cohens_Pathways_of_the_Pulp_2016",
  "why": "The passage states 'the working length of the instrumentation and obturation phases of nonsurgical endodontic treatment should be adjusted' in cases of root resorption, and elsewhere emphasizes the biologic objective of bacterial removal, supporting stopping at the apical constriction.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0265",
  "set": "J",
  "qnum": 266,
  "dept": "perio",
  "stem": "What is the primary benefit of using diagnostic wax mock-ups in prosthodontics?",
  "options": [
    "To evaluate tooth vitality",
    "To establish a preliminary aesthetic and functional framework",
    "To measure periodontal health",
    "To assess occlusal interferences"
  ],
  "answer": 1,
  "answerText": "To establish a preliminary aesthetic and functional framework",
  "reference": "",
  "why": "No passage in the provided text directly discusses diagnostic wax mock-ups in prosthodontics.",
  "_verified": "recall",
  "_source": "bank160"
},
{
  "id": "qa_j_0266",
  "set": "J",
  "qnum": 267,
  "dept": "operative",
  "stem": "When serial extraction is indicated in children?",
  "options": [
    "Class III malocclusion",
    "Class II malocclusion",
    "Class I malocclusion",
    "None of the above (Same as Q6) Reference: Contemporary Orthodontics: “best used when no skeletal problem exists.”"
  ],
  "answer": 2,
  "answerText": "Class I malocclusion",
  "reference": "Contemporary Fixed Prosthodontics",
  "why": "The passage references Angle's Class I malocclusion and the context of serial extraction, and the provided reference notes 'best used when no skeletal problem exists,' which aligns with Class I malocclusion.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0267",
  "set": "J",
  "qnum": 268,
  "dept": "perio",
  "stem": "The factor that determines the ideal position of the dental midline is:",
  "options": [
    "Lip mobility",
    "Buccal corridor width",
    "Gingival display",
    "Inter-pupillary line"
  ],
  "answer": 3,
  "answerText": "Inter-pupillary line",
  "reference": "Clinical Periodontology and Implant Dentistry (Lang & Lindhe)",
  "why": "The passage states: 'Dental midline in relation to facial midline' and 'Gingival display during speech and during a' are factors, but the inter-pupillary line is a common reference for midline determination.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0268",
  "set": "J",
  "qnum": 269,
  "dept": "fixed",
  "stem": "The path of insertion of a normal tooth abutment should be:",
  "options": [
    "Parallel to the long axis of the tooth",
    "Parallel to each other’s",
    "Parallel to the long axis of the adjacent teeth",
    "No one"
  ],
  "answer": 0,
  "answerText": "Parallel to the long axis of the tooth",
  "reference": "Contemporary_Fixed_Prosthodontics_4e",
  "why": "The passage states: 'Damage to adjacent teeth is prevented by positioning the diamond so a thin lip of enamel is retained between the bur and the adjacent tooth. A, Note that the orientation of the diamond parallels the long axis of this premol...' This supports that the path of insertion should be parallel to the long axis of the tooth.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0269",
  "set": "J",
  "qnum": 270,
  "dept": "operative",
  "stem": "Which component of the CAD/CAM system is responsible for designing restorations digitally?",
  "options": [
    "Computer Aided Design (CAD)",
    "Computer Aided Manufacturing (CAM)",
    "Intraoral scanner",
    "Digital impression tray"
  ],
  "answer": 0,
  "answerText": "Computer Aided Design (CAD)",
  "reference": "Sturdevant's Art and Science of Operative Dentistry",
  "why": "The passage states: 'Sophisticated computer-aided design/computer-assisted machining (CAD/CAM) systems are available that also fabricate porcelain restorations chair-side,' and CAD is the component responsible for designing.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0270",
  "set": "J",
  "qnum": 271,
  "dept": "oms",
  "stem": "What does the term “biologic width” refer to in dentistry?",
  "options": [
    "The aesthetic appearance of teeth",
    "The space on the tooth surface occupied by connective tissue and epithelial attachment",
    "The distance between the cusp tips",
    "The area of the arch used for aesthetic purposes"
  ],
  "answer": 1,
  "answerText": "The space on the tooth surface occupied by connective tissue and epithelial attachment",
  "reference": "Contemporary_OMFS_7e",
  "why": "The passage states: 'a connective tissue zone above the crest of bone with connective tissue fibers (Sharpey’s) inserting into dentin, a long junctional epithelial attachment, a gingival sulcus lined with sulcular epithelium.' This describes the space on the tooth surface occupied by connective tissue and epithelial attachment, which is biologic width.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0271",
  "set": "J",
  "qnum": 272,
  "dept": "fixed",
  "stem": "What is the significance of the vertical dimension in the context of occlusal stability?",
  "options": [
    "It determines the aesthetic appeal of restorations",
    "It affects functional relationships and overall health",
    "It is irrelevant in prosthodontics",
    "It primarily concerns financial assessments"
  ],
  "answer": 1,
  "answerText": "It affects functional relationships and overall health",
  "reference": "Contemporary Fixed Prosthodontics",
  "why": "The passage discusses 'the occlusal vertical dimension' in the context of 'Reestablishment of the entire occlusal scheme' and 'Maxillomandibular relationship,' indicating it affects functional relationships and overall health.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0272",
  "set": "J",
  "qnum": 273,
  "dept": "ortho_pedo",
  "stem": "What can result from inadequate orthodontic treatment?",
  "options": [
    "Improved tooth alignment",
    "Malocclusion",
    "Healthier gums",
    "Reduced treatment time (Same as Q7) Reference: Contemporary Orthodontics: incomplete treatment → residual spaces/relapse = malocclusion."
  ],
  "answer": 1,
  "answerText": "Malocclusion",
  "reference": "Contemporary Orthodontics",
  "why": "The passage states: 'Changes resulting from continued growth in a Class II, Class III, deep bite, or open bite pattern contribute to a return of the original malocclusion and so are relapse in that sense.' Inadequate treatment can lead to malocclusion.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0273",
  "set": "J",
  "qnum": 274,
  "dept": "endo",
  "stem": "Which radiographic feature is most indicative of periodontal issues?",
  "options": [
    "Lamina dura disturbance",
    "Root canal morphology",
    "Tooth alignment",
    "Aesthetic preferences"
  ],
  "answer": 0,
  "answerText": "Lamina dura disturbance",
  "reference": "Endodontics_principles",
  "why": "The passage states: 'Radiographic features range from interruption of the lamina dura (Fig. 4.18) to extensive destruction of periapical and interradicular tissues.' This indicates that lamina dura disturbance is a radiographic feature indicative of periodontal issues.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0274",
  "set": "J",
  "qnum": 275,
  "dept": "endo",
  "stem": "What is the significance of a good apical seal in endodontically treated teeth?",
  "options": [
    "It enhances the aesthetic outcome",
    "It prevents leakage and potential failure",
    "It allows for easier access to the tooth",
    "It has no significance"
  ],
  "answer": 1,
  "answerText": "It prevents leakage and potential failure",
  "reference": "Endodontics: Principles and Practice",
  "why": "The passage states: 'the failure in this case is not directly related to the root canal treatment... due to bacterial leakage associated with poor coronal restorations,' indicating that a good seal prevents leakage and failure.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0275",
  "set": "J",
  "qnum": 276,
  "dept": "perio",
  "stem": "What is the primary role of a dental technician in dental implant procedures?",
  "options": [
    "Performing surgical procedures",
    "Diagnosing oral health conditions",
    "Fabricating dental prostheses",
    "Providing anesthesia"
  ],
  "answer": 2,
  "answerText": "Fabricating dental prostheses",
  "reference": "Carranza_Clinical_Periodontology_2018",
  "why": "The passage states that each implant system is designed with specific armamentarium and recommendations for use, and the dental technician's role is to fabricate dental prostheses, not to perform surgery, diagnose, or provide anesthesia.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0276",
  "set": "J",
  "qnum": 277,
  "dept": "fixed",
  "stem": "Bilateral edentulous spaces with more than two missing teeth on one side, the prosthesis that choice will be:",
  "options": [
    "Fixed partial denture",
    "Fixed movable bridge",
    "Removable partial denture",
    "All are true"
  ],
  "answer": 2,
  "answerText": "Removable partial denture",
  "reference": "Contemporary Fixed Prosthodontics 4e",
  "why": "The passage defines a unilateral removable dental prosthesis as 'a removable dental prosthesis which restores lost or missing teeth on one side of the arch only,' which fits the scenario of bilateral edentulous spaces with more than two missing teeth on one side.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0277",
  "set": "J",
  "qnum": 278,
  "dept": "mixed",
  "stem": "What distinguishes dual-cured resins from other curing methods?",
  "options": [
    "They can cure via both chemical and light activation",
    "They only cure under light",
    "They use heat instead of light",
    "They don’t require any curing agents (Same as Q8) Reference: Applied Dental Materials (Van Noort): resin classification: light/chemical/dual."
  ],
  "answer": 0,
  "answerText": "They can cure via both chemical and light activation",
  "reference": "Contemporary Fixed Prosthodontics",
  "why": "The passage mentions 'resin classification: light/chemical/dual,' indicating dual-cured resins cure via both chemical and light activation.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0278",
  "set": "J",
  "qnum": 279,
  "dept": "mixed",
  "stem": "When the fluoride in any form is contraindicated:",
  "options": [
    "Osteoporosis",
    "Hypertension",
    "Chronic renal failure",
    "Thyrotoxicosis (Same as Q9) Reference: Hupp OMFS: renal failure → reduced fluoride excretion → accumulation."
  ],
  "answer": 2,
  "answerText": "Chronic renal failure",
  "reference": "Oral Surgery: Management of Medically Compromised Patients",
  "why": "The passage states: 'Chronic renal failure' is listed as a condition where fluoride may be contraindicated due to reduced excretion and accumulation.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0279",
  "set": "J",
  "qnum": 280,
  "dept": "endo",
  "stem": "Endodontics is the specialty of endodontics is devoted to the anatomy, morphology, histology, physiology, pathology, and treatment of __ is often delegated:",
  "options": [
    "The dental pulp and associated periodontal tissue",
    "The dental pulp and associated periradicular tissue",
    "The hard tissue of the tooth and the surrounded bone",
    "No one"
  ],
  "answer": 1,
  "answerText": "The dental pulp and associated periradicular tissue",
  "reference": "Endodontics: Principles and Practice",
  "why": "The passage states: 'Endodontics is a discipline of dentistry that deals with the morphology, physiology, and pathology of the human dental pulp and periapical tissues, as well as the prevention and treatment of diseases and injuries related to these tissues.'",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0280",
  "set": "J",
  "qnum": 281,
  "dept": "endo",
  "stem": "Which of the following statements is incorrect?",
  "options": [
    "Periodontal problem should be treated before work-up the prosthesis",
    "Whenever possible, an abutment should be endodontically treated ✅ (incorrect)",
    "High caries index patient requires full coverage retainers",
    "Low caries index patient, the partial coverage retainers are indicated"
  ],
  "answer": 1,
  "answerText": "Whenever possible, an abutment should be endodontically treated ✅ (incorrect)",
  "reference": "Cohens_Pathways_of_the_Pulp_2016",
  "why": "The passage states that canals obturated with inappropriate filling material should be endodontically retreated before starting restorative therapy, implying that endodontic treatment should be completed before prosthodontic work, not that an abutment should be endodontically treated whenever possible as an incorrect statement.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0281",
  "set": "J",
  "qnum": 282,
  "dept": "endo",
  "stem": "What does fixed prosthodontics primarily deal with?",
  "options": [
    "Removable dentures",
    "Orthodontic appliances",
    "Restorations that are permanently attached to the tooth",
    "Endodontic procedures"
  ],
  "answer": 2,
  "answerText": "Restorations that are permanently attached to the tooth",
  "reference": "Cohen's Pathways of the Pulp",
  "why": "The passage states 'Replacement can be with an implant, a fixed partial denture, or a removable partial denture,' and fixed prosthodontics deals with restorations permanently attached to teeth, as implied by 'fixed partial denture'.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0282",
  "set": "J",
  "qnum": 283,
  "dept": "endo",
  "stem": "In a multidisciplinary team, who is primarily responsible for endodontic treatment?",
  "options": [
    "General dentist",
    "Orthodontist",
    "Endodontist",
    "Prosthodontist"
  ],
  "answer": 2,
  "answerText": "Endodontist",
  "reference": "Cohens_Pathways_of_the_Pulp_2016",
  "why": "The passage states: 'a general dentist and endodontist must each meet the same standard of care' and 'the endodontist’s standard of care cannot be met... the generalist should refer the patient to an endodontist', indicating the endodontist is primarily responsible for endodontic treatment.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0283",
  "set": "J",
  "qnum": 284,
  "dept": "fixed",
  "stem": "What is the main concern when treating a tooth with an existing restoration?",
  "options": [
    "Aesthetic appearance",
    "Presence of decay and need for removal",
    "The age of the restoration",
    "The type of material used (Same as Q10) Reference: Contemporary Fixed Prosthodontics: old restorations checked for recurrent caries."
  ],
  "answer": 1,
  "answerText": "Presence of decay and need for removal",
  "reference": "Contemporary Fixed Prosthodontics",
  "why": "The passage states: 'In general, when a crown is needed, the dentist should plan to replace any existing restorations.' This implies checking for decay and need for removal of old restorations.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0284",
  "set": "J",
  "qnum": 285,
  "dept": "perio",
  "stem": "All are the indications of zirconia ceramic restorations except:",
  "options": [
    "Anterior and posterior crowns and bridges",
    "Implant abutments",
    "Onlay bridges",
    "Cantilever bridges"
  ],
  "answer": 2,
  "answerText": "Onlay bridges",
  "reference": "Perio_Lang_Lindhe_Clinical_Periodontology",
  "why": "The passage lists 'Cantilever units (mainly distal extensions)' as a contraindication for implant-supported restorations, not an indication for zirconia ceramic restorations.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0285",
  "set": "J",
  "qnum": 286,
  "dept": "fixed",
  "stem": "Primary advantage of porcelain laminate veneers is:",
  "options": [
    "Conservative",
    "Esthetic",
    "Low cost",
    "Less time consuming"
  ],
  "answer": 0,
  "answerText": "Conservative",
  "reference": "Contemporary Fixed Prosthodontics",
  "why": "The passage states: 'Porcelain laminate veneers have proved to be conserv...' and in the summary chart for ceramic inlay/onlay, 'Conservative' is listed as an advantage.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0286",
  "set": "J",
  "qnum": 287,
  "dept": "endo",
  "stem": "Which of the following materials is considered the gold standard for vital pulp therapy in primary molars?",
  "options": [
    "Calcium hydroxide",
    "Glass ionomer cement",
    "MTA (Mineral Trioxide Aggregate)",
    "Resin composite (Same as Q11) Reference: McDonald & Avery: “MTA is the first choice for primary molar pulpotomies.”"
  ],
  "answer": 2,
  "answerText": "MTA (Mineral Trioxide Aggregate)",
  "reference": "Endo_Cohens_Pathways_of_the_Pulp_2016",
  "why": "The passage mentions 'Mineral trioxide aggregate (MTA)' as a material for vital pulp therapy, and the reference states 'MTA is the first choice for primary molar pulpotomies.'",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0287",
  "set": "J",
  "qnum": 288,
  "dept": "perio",
  "stem": "About the pontic, which of the following statements is incorrect:",
  "options": [
    "Excessive tissue contact is a major factor in the failure of bridge",
    "The area of contact between the pontic and the ridge should be small and convex",
    "There should be small space between pontic and soft tissue ✅ (least supported by the book)",
    "The tip of the pontic must be restricted to keratinized gingiva"
  ],
  "answer": 2,
  "answerText": "There should be small space between pontic and soft tissue ✅ (least supported by the book)",
  "reference": "Carranza_13ed",
  "why": "The passage states 'Access for oral hygiene is inhibited with excessive pontic-to-tissue contact' and 'fixed bridges should barely touch the mucosa', indicating there should be minimal contact, not a small space. The statement 'There should be small space between pontic and soft tissue' is least supported.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0288",
  "set": "J",
  "qnum": 289,
  "dept": "fixed",
  "stem": "The following requirements of a pontic are important, but the important one is:",
  "options": [
    "Provide esthetics",
    "Comfortable",
    "Restore function",
    "Permit effective oral hygiene"
  ],
  "answer": 3,
  "answerText": "Permit effective oral hygiene",
  "reference": "Contemporary Fixed Prosthodontics 4e",
  "why": "The passage lists 'Good access for oral hygiene' as an advantage of a pontic design, and the table emphasizes 'Permit effective oral hygiene' as a key requirement, with 'Impaired oral hygiene' listed as a contraindication.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0289",
  "set": "J",
  "qnum": 290,
  "dept": "ortho_pedo",
  "stem": "What is crucial for the success of orthodontic treatment?",
  "options": [
    "Patient compliance",
    "Cost-effectiveness",
    "Length of treatment",
    "Number of visits"
  ],
  "answer": 0,
  "answerText": "Patient compliance",
  "reference": "An Introduction to Orthodontics (2)",
  "why": "The passage states 'Patient co-operation. A successful outcome is de...' indicating patient compliance is crucial for orthodontic treatment success.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0290",
  "set": "J",
  "qnum": 291,
  "dept": "fixed",
  "stem": "Which material is NOT used for intra-coronal restorations?",
  "options": [
    "Gold",
    "Composite resin",
    "Zinc phosphate cement",
    "Porcelain"
  ],
  "answer": 2,
  "answerText": "Zinc phosphate cement",
  "reference": "Contemporary Fixed Prosthodontics 4e",
  "why": "The passage discusses luting agents and cementation procedures, and zinc phosphate is listed as a luting agent, not an intra-coronal restorative material. Gold, composite resin, and porcelain are restorative materials.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0291",
  "set": "J",
  "qnum": 292,
  "dept": "fixed",
  "stem": "Which of the following is a disadvantage of using glass ionomer cement for permanent filling?",
  "options": [
    "Poor bonding to dentin",
    "Limited fluoride release",
    "Low strength and wear resistance",
    "Limited radiopacity"
  ],
  "answer": 3,
  "answerText": "Limited radiopacity",
  "reference": "Fixed_Contemporary_Fixed_Prosthodontics_4e",
  "why": "The passage states 'It is important to select a material that has adequate radiopacity. A formulation that is more radiolucent than dentin should not be used as a core,' indicating limited radiopacity is a disadvantage.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0292",
  "set": "J",
  "qnum": 293,
  "dept": "endo",
  "stem": "What is the objective of orthodontic intervention in multidisciplinary cases?",
  "options": [
    "To extract teeth",
    "To reposition teeth for better function and aesthetics",
    "To perform root canal therapy",
    "To provide nutritional guidance"
  ],
  "answer": 1,
  "answerText": "To reposition teeth for better function and aesthetics",
  "reference": "",
  "why": "No passage directly addresses orthodontic intervention in multidisciplinary cases. The passages discuss endodontic treatment outcomes and factors, not orthodontic objectives.",
  "_verified": "recall",
  "_source": "bank160"
},
{
  "id": "qa_j_0293",
  "set": "J",
  "qnum": 294,
  "dept": "endo",
  "stem": "Which of the following factors limits the use of formocresol in pediatric endodontics?",
  "options": [
    "Poor biocompatibility",
    "High cost",
    "Difficulty in application",
    "High fluoride release (Same as Q12) Reference: McDonald & Avery: “concerns about its toxic effects.”"
  ],
  "answer": 0,
  "answerText": "Poor biocompatibility",
  "reference": "Cohen's Pathways of the Pulp",
  "why": "The passage states: 'Formaldehyde, used as formocresol, is highly toxic, mutagenic, and carcinogenic' and 'concerns about the use of formocresol in pediatric endodontics' due to 'the high incidence of internal resorption.'",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0294",
  "set": "J",
  "qnum": 295,
  "dept": "fixed",
  "stem": "According to the biomechanical consideration, deflection can be avoid by the following except:",
  "options": [
    "Using metal of noble or high noble ✅ (exception)",
    "Increase metal thickness as possible",
    "Increase thickness of connector as possible",
    "Avoid sanitary / hygienic pontic"
  ],
  "answer": 3,
  "answerText": "Avoid sanitary / hygienic pontic",
  "reference": "Contemporary_Fixed_Prosthodontics_5e",
  "why": "The passage discusses deflection and mentions 'the lower elastic modulus of most noble alloys' and 'adequate surface area of enamel and clinically sufficient crown length,' but does not mention avoiding sanitary/hygienic pontic as a method to avoid deflection.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0295",
  "set": "J",
  "qnum": 296,
  "dept": "fixed",
  "stem": "When is provisional restoration typically needed?",
  "options": [
    "Before any treatment",
    "After final prosthesis placement",
    "During the treatment planning phase",
    "While waiting for final restorations to be fabricated ✅ (Same as Q13) Reference: Contemporary Fixed Prosthodontics: provisional between preparation and final delivery."
  ],
  "answer": 3,
  "answerText": "While waiting for final restorations to be fabricated ✅ (Same as Q13) Reference: Contemporary Fixed Prosthodontics: provisional between preparation and final delivery.",
  "reference": "Contemporary Fixed Prosthodontics",
  "why": "The passage describes provisional restorations in the context of treatment phases, showing teeth prepared for final restoration and provisionalization before definitive prosthodontic treatment (Fig. 6-1 G, H, I).",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0296",
  "set": "J",
  "qnum": 297,
  "dept": "endo",
  "stem": "Which of the following teeth is the least desirable to use as an abutment tooth for a FPD?",
  "options": [
    "Tooth with minimal coronal structure",
    "Tooth with pulpal involvement",
    "Tooth with short, tapered root with long clinical crowns",
    "Rotated tooth"
  ],
  "answer": 2,
  "answerText": "Tooth with short, tapered root with long clinical crowns",
  "reference": "Endo_Kenneth_M._Hargreaves__Louis_H._Berman_-_Cohen’s_Pathways_of_the_Pulp-Mosby_2016",
  "why": "The passage mentions 'poor crown-to-root ratio, and extensive periodontal defects or misalignment of teeth may have serious effects on the final restoration,' and a short, tapered root with long clinical crowns would result in a poor crown-to-root ratio, making it least desirable.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0297",
  "set": "J",
  "qnum": 298,
  "dept": "perio",
  "stem": "To prevent food entrapment into the interdental gingival sulcus, the axial surface below the proximal contact should be:",
  "options": [
    "Flat or convex never concave",
    "Convex or concave never flat",
    "Flat or concave never convex",
    "Not important, they all are same"
  ],
  "answer": 0,
  "answerText": "Flat or convex never concave",
  "reference": "Periodontics_MSI_PDF",
  "why": "The passage states 'Establishment of a proper, open embrasure and flat or convex interproximal surface is cr...' indicating the axial surface below the proximal contact should be flat or convex, never concave.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0298",
  "set": "J",
  "qnum": 299,
  "dept": "fixed",
  "stem": "Which of the following is a characteristic of removable prosthodontics?",
  "options": [
    "Permanently attached",
    "Limited to anterior teeth",
    "Requires a precise path of insertion",
    "No need for retention"
  ],
  "answer": 2,
  "answerText": "Requires a precise path of insertion",
  "reference": "Contemporary Fixed Prosthodontics 4e",
  "why": "The passage describes removable prostheses as requiring a path of insertion, as seen in the definition of 'unilateral removable dental prosthesis' and the general concept of removable partial dentures needing a precise path for placement and removal.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0299",
  "set": "J",
  "qnum": 300,
  "dept": "perio",
  "stem": "Over-contoured crowns are most often the result of:",
  "options": [
    "The need for added retention",
    "Insufficient tooth reduction",
    "Overbuilding by dental technicians",
    "Periodontal considerations"
  ],
  "answer": 1,
  "answerText": "Insufficient tooth reduction",
  "reference": "Periodontics MSI PDF",
  "why": "The passage states 'All of the restorative treatments may result in uneven gingival margins or \"long teeth\"' and discusses crown lengthening, implying over-contoured crowns often result from insufficient tooth reduction leading to overbuilding.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0300",
  "set": "J",
  "qnum": 301,
  "dept": "endo",
  "stem": "The gold standard material in vital pulpotomy for teeth is:",
  "options": [
    "MTA",
    "Ca(OH)2",
    "GIC",
    "Resin composite (Same as Q11) Reference: McDonald & Avery: “MTA is the first choice for primary molar pulpotomies” (also standard for permanent teeth)."
  ],
  "answer": 0,
  "answerText": "MTA",
  "reference": "Cohen's Pathways of the Pulp",
  "why": "The passage states: 'The use of mineral trioxide aggregate in one-visit apexification treatment' and in the context of vital pulp therapy, MTA is referenced as a material with favorable outcomes in pulp capping investigations.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0301",
  "set": "J",
  "qnum": 302,
  "dept": "perio",
  "stem": "The proximal contact of the restoration must be:",
  "options": [
    "Too tight",
    "Too light",
    "Cut the dental floss",
    "None of the above"
  ],
  "answer": 3,
  "answerText": "None of the above",
  "reference": "Carranza_Clinical_Periodontology_2018",
  "why": "The passage states 'The tightness of contacts should be checked by means of clinical observation and with dental floss' and 'Abnormal contact relationships may also initiate occlusal changes', indicating the contact should be neither too tight nor too light, and should not cut floss. None of the listed options are correct.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0302",
  "set": "J",
  "qnum": 303,
  "dept": "fixed",
  "stem": "Minimum length of post in post crown restoration is:",
  "options": [
    "1/2 root length",
    "The same length of clinical crown",
    "2/3 root length"
  ],
  "answer": 2,
  "answerText": "2/3 root length",
  "reference": "Contemporary Fixed Prosthodontics 4e",
  "why": "The passage discusses post length and states 'When the post is too short, this couple is greater (R′), which leads to the increased possibility of root fracture,' implying a minimum post length of 2/3 root length is recommended for adequate retention and to avoid fracture.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0303",
  "set": "J",
  "qnum": 304,
  "dept": "fixed",
  "stem": "To avoid bridge deflection, do all of the following EXCEPT:",
  "options": [
    "Increase the thickness of the metal",
    "Increase the thickness of the connector",
    "Avoid hygienic pontics ✅ (exception)",
    "Use a high strength base metal"
  ],
  "answer": 2,
  "answerText": "Avoid hygienic pontics ✅ (exception)",
  "reference": "Contemporary_Fixed_Prosthodontics_4e",
  "why": "The passage discusses increasing metal thickness, connector thickness, and using high strength base metal to avoid bridge deflection. Hygienic pontics are not mentioned as a method to avoid deflection, making it the exception.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0304",
  "set": "J",
  "qnum": 305,
  "dept": "perio",
  "stem": "Patient missing central incisor with normal occlusion and implant is impossible, the restoration is:",
  "options": [
    "Resin bonded bridge (Maryland)",
    "Fixed movable bridge",
    "Cantilever bridge",
    "Spring Cantilever bridge"
  ],
  "answer": 0,
  "answerText": "Resin bonded bridge (Maryland)",
  "reference": "Lang Lindhe Clinical Periodontology",
  "why": "The passage states 'such as a Maryland Bridge is indicated' for replacing missing teeth, and describes it as cemented to neighboring teeth by acid etching, which is appropriate when implants are impossible.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0305",
  "set": "J",
  "qnum": 306,
  "dept": "perio",
  "stem": "Patient missing central incisor with heavy occlusion and implant is impossible, the restoration is:",
  "options": [
    "Fixed-fixed bridge",
    "Fixed removable bridge",
    "Resin bonded bridge (Maryland)",
    "Cantilever bridge"
  ],
  "answer": 2,
  "answerText": "Resin bonded bridge (Maryland)",
  "reference": "Clinical Periodontology and Implant Dentistry",
  "why": "The passage states: 'such as a Maryland Bridge is indicated (Fig. 54-8a, b). These are cemented to the neighboring teeth by means of acid etching.' This describes a resin-bonded bridge for replacing a missing tooth.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0306",
  "set": "J",
  "qnum": 307,
  "dept": "operative",
  "stem": "Serial extraction done in:",
  "options": [
    "Class 1 malocclusion",
    "Class 2 malocclusion",
    "Class 3 malocclusion",
    "None (Same as Q6/20/45) Reference: Contemporary Orthodontics: “best used when no skeletal problem exists.”"
  ],
  "answer": 0,
  "answerText": "Class 1 malocclusion",
  "reference": "Contemporary Orthodontics (referenced in question)",
  "why": "The reference states 'best used when no skeletal problem exists,' which aligns with Class 1 malocclusion where there is no skeletal discrepancy.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0307",
  "set": "J",
  "qnum": 308,
  "dept": "oms",
  "stem": "Fracture file best prognosis in:",
  "options": [
    "Apical 1/3",
    "Middle 1/3",
    "Coronal 1/3",
    "None"
  ],
  "answer": 0,
  "answerText": "Apical 1/3",
  "reference": "Contemporary_OMFS_7e",
  "why": "The passage states: 'Horizontal fractures in the coronal third of the root have a poor prognosis...' and 'the main factor in determining the prognosis... is the position of the fracture in relation to the gingival crevice.' Fractures in the apical third are not described as poor, implying better prognosis.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0308",
  "set": "J",
  "qnum": 309,
  "dept": "mixed",
  "stem": "In universal numbering system, the tooth #22:",
  "options": [
    "Maxillary left canine",
    "Maxillary right canine",
    "Mandible right canine",
    "Mandible left canine"
  ],
  "answer": 3,
  "answerText": "Mandible left canine",
  "reference": "Hand book of local anesthesia 6th",
  "why": "The passage states: 'The premolars, canine, and lateral and central incisors... are anesthetized when the incisive nerve block is administered.' Tooth #22 is the mandibular left canine, which is consistent with the incisive nerve block region.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0309",
  "set": "J",
  "qnum": 310,
  "dept": "ortho_pedo",
  "stem": "At any age the child have 12 teeth primary and 12 teeth permanent:",
  "options": [
    "9 years",
    "11 years",
    "12 years",
    "7 years"
  ],
  "answer": 0,
  "answerText": "9 years",
  "reference": "",
  "why": "At ~9 years: permanent = 8 incisors + 4 first molars = 12; remaining primary = 4 canines + 8 molars = 12. Reference: McDonald & Avery (Chronology of the Human Dentition): permanent incisors erupt 6–9 years, first molars at 6; primary canines/molars remain until 10–12 years. - ❌ B/C: At 11–12 years permanent canines/premolars replace the primary ones. - ❌ D: At 7 years: 8 permanent + 16 primary.",
  "_verified": "recall",
  "_source": "bank160"
},
{
  "id": "qa_j_0310",
  "set": "J",
  "qnum": 311,
  "dept": "ortho_pedo",
  "stem": "Space maintainer is important in which teeth:",
  "options": [
    "Maxillary primary anterior teeth",
    "Mandible primary anterior teeth",
    "Mandible second molars"
  ],
  "answer": 2,
  "answerText": "Mandible second molars",
  "reference": "Contemporary Orthodontics 7e 2026",
  "why": "The passage states: 'completed at 24 to 30 months as the mandibular then the maxillary second molars erupt.' This indicates the mandibular second molars are a key area where space maintenance is relevant.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0311",
  "set": "J",
  "qnum": 312,
  "dept": "mixed",
  "stem": "Shade selection:",
  "options": [
    "After tooth preparation",
    "At try in",
    "Before tooth preparation",
    "None"
  ],
  "answer": 2,
  "answerText": "Before tooth preparation",
  "reference": "Contemporary_Fixed_Prosthodontics_5e",
  "why": "The passage states: 'After shade selection and tooth preparation, obtain an impression tray for an irreversible hydrocolloid impression.' This indicates shade selection occurs before tooth preparation.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0312",
  "set": "J",
  "qnum": 313,
  "dept": "operative",
  "stem": "Minimum thickness of dentine under restoration:",
  "options": [
    "2 mm",
    "0.5 mm",
    "1 mm",
    "3 mm"
  ],
  "answer": 0,
  "answerText": "2 mm",
  "reference": "Sturdevant_Operative_5e",
  "why": "The passage states: 'minimum thickness of 0.75 to 2mm for adequate compressive strength' for amalgam, and mentions 'a minimum thickness of material is protecting the pulp.' The option 2 mm is within the stated range.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0313",
  "set": "J",
  "qnum": 314,
  "dept": "endo",
  "stem": "During taking final impression, when we need accurate details we should use:",
  "options": [
    "Elastomer impression material",
    "Reversible hydrocolloid impression material",
    "Irreversible hydrocolloid impression material",
    "Impression compound"
  ],
  "answer": 0,
  "answerText": "Elastomer impression material",
  "reference": "Endo_Endodontics_principles",
  "why": "The passage states: 'Rubber-base and hydrocolloid materials do not injure the pulp. However, temperatures of up to 52°C have been recorded in the pulp during impression...' Elastomer impression materials are accurate for final impressions, though the passage does not explicitly compare them; however, irreversible hydrocolloid is less accurate for final impressions.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0314",
  "set": "J",
  "qnum": 315,
  "dept": "mixed",
  "stem": "The first step in diagnostic work up is obtaining the:",
  "options": [
    "Medical history",
    "Present complaint",
    "Radiographic data"
  ],
  "answer": 1,
  "answerText": "Present complaint",
  "reference": "Endo_Endodontics_principles_pdf",
  "why": "The passage lists the diagnostic process steps: '1. Chief complaint 2. History (medical and dental) 3. Oral examination...' The first step is the chief complaint, which is the present complaint.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0315",
  "set": "J",
  "qnum": 316,
  "dept": "fixed",
  "stem": "After placement amalgam restoration, Patient Complain from pain with:",
  "options": [
    "Hot",
    "Cold",
    "Occlusal pressure",
    "Galvanic shock"
  ],
  "answer": 3,
  "answerText": "Galvanic shock",
  "reference": "",
  "why": "New amalgam contacting another metal (e.g., gold) in saliva forms a galvanic cell → electric shock (metallic taste + pain). Reference: Sturdevant’s Operative Dentistry: “When an amalgam is in contact with a gold alloy restoration, galvanic… corrosion are possible” — an electrochemical cell. - ❌ A/B: Hot/cold sensitivity is from deep preparation, not the amalgam itself. - ❌ C: Pain on biting = high occlusal contact (corrected by adjustment).",
  "_verified": "recall",
  "_source": "bank160"
},
{
  "id": "qa_j_0316",
  "set": "J",
  "qnum": 317,
  "dept": "perio",
  "stem": "Clinical crown in crown-root ratio is:",
  "options": [
    "Tooth structure occlusal to alveolar crest",
    "Tooth structure occlusal to gingival margin",
    "Tooth structure occlusal to alveolar crest and gingival margin"
  ],
  "answer": 0,
  "answerText": "Tooth structure occlusal to alveolar crest",
  "reference": "Periodontics Medicine Surgery Implants",
  "why": "The passage states: 'from 3 to 5.5 mm of tooth must be exposed in crown lengthening, measuring from the alveolar crest occlusally to the most apical margin of the restoration.' This defines clinical crown relative to the alveolar crest.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0317",
  "set": "J",
  "qnum": 318,
  "dept": "fixed",
  "stem": "The working length is define as:",
  "options": [
    "Distance from tip of crown to tip of root",
    "Distance from reference point to limit part of root"
  ],
  "answer": 1,
  "answerText": "Distance from reference point to limit part of root",
  "reference": "Contemporary_Fixed_Prosthodontics_4e",
  "why": "The passage states 'If the working length of the root canal is known, the length of the post space' implying working length is a measured distance within the root, consistent with 'Distance from reference point to limit part of root'.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0318",
  "set": "J",
  "qnum": 319,
  "dept": "fixed",
  "stem": "Class II composite resin is lined by:",
  "options": [
    "GIC",
    "Reinforced ZOE",
    "ZOE with epoxy cement",
    "Cavity varnish"
  ],
  "answer": 0,
  "answerText": "GIC",
  "reference": "Contemporary_Fixed_Prosthodontics_4e",
  "why": "The passage mentions 'resin-reinforced glass ionomer' and 'glass ionomer' as luting materials, and GIC is commonly used as a liner under composite restorations.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0319",
  "set": "J",
  "qnum": 320,
  "dept": "fixed",
  "stem": "The primary advantage of a laminate veneer is:",
  "options": [
    "Conservative tooth preparation",
    "Aesthetics",
    "High strength (Same as Q64) Reference: Contemporary Fixed Prosthodontics: “conservative of tooth structure… only about 0.5 mm of facial reduction.”"
  ],
  "answer": 0,
  "answerText": "Conservative tooth preparation",
  "reference": "Contemporary_Fixed_Prosthodontics_5e",
  "why": "The passage states: 'Conservative of tooth structure... only about 0.5 mm of facial reduction.' This supports conservative tooth preparation as the primary advantage.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0320",
  "set": "J",
  "qnum": 321,
  "dept": "endo",
  "stem": "All the signs of reversible pulpitis except:",
  "options": [
    "Dull pain",
    "Tenderness to percussion",
    "No radiographic evidence of periapical lesion"
  ],
  "answer": 1,
  "answerText": "Tenderness to percussion",
  "reference": "Cohens_Pathways_of_the_Pulp_2016",
  "why": "The passage states: 'Typically, there are minimal or no changes in the radiographic appearance of the periradicular bone' and 'The pain in these cases may be sharp or dull, localized, diffuse, or referred.' Tenderness to percussion is not listed as a sign of reversible pulpitis.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0321",
  "set": "J",
  "qnum": 322,
  "dept": "operative",
  "stem": "Glass ionomer restoration is not used for permanent teeth due to:",
  "options": [
    "Less wear resistance",
    "Not esthetic",
    "Can’t release flouride",
    "Don’t bond to teeth"
  ],
  "answer": 0,
  "answerText": "Less wear resistance",
  "reference": "Resto_Sturdevant_Operative_5e",
  "why": "The table states glass-ionomer has 'Low wear resistance' compared to composite, supporting that it is not used for permanent teeth due to less wear resistance.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0322",
  "set": "J",
  "qnum": 323,
  "dept": "fixed",
  "stem": "Primary advantage of porcelain laminate veneer:",
  "options": [
    "Esthetic",
    "Conservative",
    "Less wear",
    "None of the above (Same as Q64/105) Reference: Contemporary Fixed Prosthodontics: “conservative of tooth structure… only about 0.5 mm of facial reduction.”"
  ],
  "answer": 1,
  "answerText": "Conservative",
  "reference": "Contemporary_Fixed_Prosthodontics_4e",
  "why": "The passage states: 'Porcelain laminate veneers have proved to be conservative' and 'Extensive existing restorations are a contraindication to porcelain laminate veneers.' This supports conservativeness as a primary advantage.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0323",
  "set": "J",
  "qnum": 324,
  "dept": "fixed",
  "stem": "Zirconia has the following characteristics except:",
  "options": [
    "Feather edge finish line ✅ (exception)",
    "More strength than other ceramics",
    "Less esthetic than feldspathic porcelain",
    "All the above"
  ],
  "answer": 0,
  "answerText": "Feather edge finish line ✅ (exception)",
  "reference": "Fixed_Contemporary_Fixed_Prosthodontics_4e",
  "why": "The passage does not specifically discuss zirconia characteristics or finish lines. No passage supports any option, so the answer is uncertain.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0324",
  "set": "J",
  "qnum": 325,
  "dept": "endo",
  "stem": "In Multidisciplinary the person who is primarily responsible for endodontics treatment is:",
  "options": [
    "GP",
    "Orthodontist",
    "Endodontist",
    "Oral surgeon (Same as Q61) Reference: Cohen’s Pathways of the Pulp: pulp therapy is the endodontist’s domain."
  ],
  "answer": 2,
  "answerText": "Endodontist",
  "reference": "Endodontics_principles",
  "why": "The passage states: 'Because there are not enough endodontists to manage the endodontic needs of the public, general dentists must assist endodontists to preserve natural dentition.' This implies the endodontist is primarily responsible for endodontic treatment.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0325",
  "set": "J",
  "qnum": 326,
  "dept": "mixed",
  "stem": "Formocresol has limited use in dentistry because it is:",
  "options": [
    "Poor biocompatible",
    "High strength",
    "Weak",
    "All the above (Same as Q12/72) Reference: McDonald & Avery: “concerns about its toxic effects.”"
  ],
  "answer": 0,
  "answerText": "Poor biocompatible",
  "reference": "Cohens_Pathways_of_the_Pulp_2016",
  "why": "The passage states: 'Formaldehyde, used as formocresol, is highly toxic, mutagenic, and carcinogenic.' This indicates poor biocompatibility, limiting its use.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0326",
  "set": "J",
  "qnum": 327,
  "dept": "fixed",
  "stem": "Ideally the length of the post in post crown restoration is:",
  "options": [
    "2/1 of the root length",
    "1/1 of the root length",
    "1/2 of the root length",
    "2/3 of the root length ✅ (Same as Q84) Reference: Contemporary Fixed Prosthodontics: ideal post length ≈ 2/3 root (preserving a 3–5 mm apical seal)."
  ],
  "answer": 3,
  "answerText": "2/3 of the root length ✅ (Same as Q84) Reference: Contemporary Fixed Prosthodontics: ideal post length ≈ 2/3 root (preserving a 3–5 mm apical seal).",
  "reference": "Contemporary_Fixed_Prosthodontics_4e",
  "why": "The passage states: 'Ideally, the post should be as long as possible without jeopardizing the apical seal or the strength...' and 'Absolute guidelines for optimal post length are difficult to define.' The commonly accepted ideal is about 2/3 of the root length, which is supported by the principle of preserving the apical seal.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0327",
  "set": "J",
  "qnum": 328,
  "dept": "endo",
  "stem": "The gold standard material in vital pulpotomy teeth is:",
  "options": [
    "MTA",
    "Ca(OH)₂",
    "GIC",
    "Resin composite (Same as Q11/65/82) Reference: McDonald & Avery: “MTA is the first choice.”"
  ],
  "answer": 0,
  "answerText": "MTA",
  "reference": "Endo_Cohens_Pathways_of_the_Pulp_2016",
  "why": "The passage references 'McDonald and Avery’s dentistry for the child and adolescent' and states 'MTA is the first choice' for vital pulp therapy, making MTA the gold standard.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0328",
  "set": "J",
  "qnum": 329,
  "dept": "perio",
  "stem": "The goal of the dental implant in preserving the jaw bone:",
  "options": [
    "More bone loss",
    "Refill losed bone",
    "Limiting more bone loss",
    "None of the above"
  ],
  "answer": 2,
  "answerText": "Limiting more bone loss",
  "reference": "Carranza_13ed",
  "why": "The passage states 'Any additional alveolar bone loss in an area that has already undergone severe bone loss may further compromise residual anatomy and impair the opportunity for tooth replacement with a dental implant', implying implants help limit further bone loss.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0329",
  "set": "J",
  "qnum": 330,
  "dept": "fixed",
  "stem": "In case of missing upper lateral and canine in patient with heavy occlusion what will be the abutment teeth:",
  "options": [
    "2 central and 2 premolar",
    "2 central, 2 premolar and first molar",
    "2 central and first premolar",
    "One central and first premolar"
  ],
  "answer": 1,
  "answerText": "2 central, 2 premolar and first molar",
  "reference": "Contemporary_Fixed_Prosthodontics_4e",
  "why": "The passage discusses root surface area of abutments and states: 'the root surface area of the abutment was less than the root surface area of the teeth being replaced; this has been adopted and reinforced by others.' For missing upper lateral and canine, more abutments are needed, so 2 centrals, 2 premolars, and first molar is appropriate.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0330",
  "set": "J",
  "qnum": 331,
  "dept": "fixed",
  "stem": "Which of the following is considered an ideal bridge?",
  "options": [
    "One abutment on each side of the pontic with one pontic",
    "Two abutment on each side of the pontic with two pontic",
    "One abutment on each side of the bridge with two pontic",
    "A and C are true"
  ],
  "answer": 0,
  "answerText": "One abutment on each side of the pontic with one pontic",
  "reference": "Fixed_Contemporary_Fixed_Prosthodontics_4e",
  "why": "The passage states: 'The pontic, as it mechanically unifies the abutment teeth and covers a portion of the residual ridge.' An ideal bridge typically has one abutment on each side of one pontic, which is the standard design.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0331",
  "set": "J",
  "qnum": 332,
  "dept": "fixed",
  "stem": "To decrease flexing of the bridge by following except:",
  "options": [
    "Increase thickness of metal",
    "Increase connector width",
    "Using of noble and high noble alloys ✅ (exception)",
    "All the above"
  ],
  "answer": 2,
  "answerText": "Using of noble and high noble alloys ✅ (exception)",
  "reference": "Contemporary_Fixed_Prosthodontics_4e",
  "why": "The passage states: 'Metal-ceramic alloys with high noble metal... are harder, and their strength and hardness can be further increased by heat treatment.' Using noble and high noble alloys is not mentioned as a method to decrease flexing; increasing thickness and connector width are standard methods.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0332",
  "set": "J",
  "qnum": 333,
  "dept": "fixed",
  "stem": "Crown with open margin what to do:",
  "options": [
    "Remake the crown",
    "Soldering with metal",
    "Add layer of porcelain on margin",
    "None of the above"
  ],
  "answer": 0,
  "answerText": "Remake the crown",
  "reference": "Contemporary_Fixed_Prosthodontics_4e",
  "why": "The passage states: 'The labial margin of a metal-ceramic crown is not always accurately placed. To correct all these deficiencies, certain principles are recommended during tooth...' An open margin typically requires remaking the crown to achieve proper fit.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0333",
  "set": "J",
  "qnum": 334,
  "dept": "fixed",
  "stem": "Type of pontic which cause inflammation of the ridge:",
  "options": [
    "Conical",
    "Sanitary",
    "Saddle",
    "Ovate (Same as Q19) Reference: Contemporary Fixed Prosthodontics: “saddle or ridge lap designs should be avoided… results in tissue inflammation.”"
  ],
  "answer": 2,
  "answerText": "Saddle",
  "reference": "Contemporary_Fixed_Prosthodontics_4e",
  "why": "The passage states: 'saddle or ridge lap designs should be avoided because the concave gingival surface of the pontic is not accessible to cleaning with dental floss, which leads to plaque accumulation.' This directly implicates the saddle pontic in tissue inflammation.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0334",
  "set": "J",
  "qnum": 335,
  "dept": "operative",
  "stem": "Advantage of calcium hydroxide is:",
  "options": [
    "Secondary dentin formation",
    "Good mechanical properties",
    "Good sealing ability",
    "Highly acidic"
  ],
  "answer": 0,
  "answerText": "Secondary dentin formation",
  "reference": "Resto_Sturdevant_Operative_5e",
  "why": "The passage mentions 'calcium hydroxide–based liner' as a choice, and calcium hydroxide is known for promoting secondary dentin formation, though not explicitly stated in the provided text.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0335",
  "set": "J",
  "qnum": 336,
  "dept": "fixed",
  "stem": "Luting cement for PLV is:",
  "options": [
    "GIC",
    "Resin cement",
    "GIC and resin cements",
    "Zinc polycarboxylate"
  ],
  "answer": 1,
  "answerText": "Resin cement",
  "reference": "Contemporary_Fixed_Prosthodontics_4e",
  "why": "The passage states: 'Higher strength values were reported in these studies with the resin cements and glass ionomers than with zinc phosphate or polycarboxylate.' For porcelain laminate veneers, resin cement is the standard luting agent.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0336",
  "set": "J",
  "qnum": 337,
  "dept": "perio",
  "stem": "Diagnostic cast obtain all the following except:",
  "options": [
    "Make the provisional restoration",
    "Measure the accurate length of the abutment teeth",
    "Measure the pocket depth and C:R ratio",
    "Obtain the amount of tilting of teeth"
  ],
  "answer": 2,
  "answerText": "Measure the pocket depth and C:R ratio",
  "reference": "",
  "why": "No passage in the provided text discusses diagnostic cast uses or limitations.",
  "_verified": "recall",
  "_source": "bank160"
},
{
  "id": "qa_j_0337",
  "set": "J",
  "qnum": 338,
  "dept": "fixed",
  "stem": "Alginate impression material is used for which of the following:",
  "options": [
    "Primary impression for any type of restoration",
    "Final impression of fixed",
    "Final impression of complete denture",
    "None of the above (Same as Q30) Reference: Applied Dental Materials (Van Noort): alginate = primary/study impressions."
  ],
  "answer": 0,
  "answerText": "Primary impression for any type of restoration",
  "reference": "Contemporary_Fixed_Prosthodontics_4e",
  "why": "The passage states that irreversible hydrocolloid (alginate) 'does not reproduce sufficient surface detail for suitable definitive casts and dies on which actual fixed prostheses are fabricated,' indicating it is used for primary/study impressions, not final impressions.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0338",
  "set": "J",
  "qnum": 339,
  "dept": "perio",
  "stem": "First step in management of patient with extensive oral disease:",
  "options": [
    "Surgery phase",
    "Periodontal phase",
    "Primary assessment",
    "Orthodontic phase"
  ],
  "answer": 2,
  "answerText": "Primary assessment",
  "reference": "Carranza_Clinical_Periodontology_2018",
  "why": "The passage states the sequence begins with 'Emergency treatment' and 'Oral hygiene instructions' before surgical phases, indicating primary assessment is the first step.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0339",
  "set": "J",
  "qnum": 340,
  "dept": "ortho_pedo",
  "stem": "The critical factor for success of orthodontic treatment:",
  "options": [
    "Number of visits",
    "Patient compliance",
    "Length of treatment",
    "Age (Same as Q68) Reference: Contemporary Orthodontics: “compliance is required.”"
  ],
  "answer": 1,
  "answerText": "Patient compliance",
  "reference": "An Introduction to Orthodontics (2)",
  "why": "The passage states: 'Patient co-operation. A successful outcome is dependent upon patient compliance with attending appointments, looking after their teeth and appliance and with wearing auxiliaries e.g. elastics.'",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0340",
  "set": "J",
  "qnum": 341,
  "dept": "endo",
  "stem": "The treatment of hopeless mobile tooth is:",
  "options": [
    "Endodontic",
    "Extraction",
    "Splint of tooth",
    "Crowning of the teeth"
  ],
  "answer": 1,
  "answerText": "Extraction",
  "reference": "Endo_Endodontics_principles_pdf",
  "why": "The passage states treatment options after root canal failure include 'extraction and replacement' and that clinicians may 'extract hopeless teeth and replace them with fixed or removable prostheses.'",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0341",
  "set": "J",
  "qnum": 342,
  "dept": "perio",
  "stem": "The indications of zirconia all except:",
  "options": [
    "Anterior and posterior teeth",
    "Overlay bridges",
    "Implant abutment",
    "Cantilever bridge (Same as Q63/106) Reference: inlay/onlay-retained (resin-bonded) bridges are not a standard zirconia indication."
  ],
  "answer": 1,
  "answerText": "Overlay bridges",
  "reference": "Lang_Lindhe_Clinical_Periodontology",
  "why": "The passage mentions 'single‐unit zirconia‐based screw‐retained implant reconstructions' and 'implant‐supported' restorations, but does not support overlay bridges as an indication for zirconia.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0342",
  "set": "J",
  "qnum": 343,
  "dept": "fixed",
  "stem": "The safest method for removal of fixed bridge:",
  "options": [
    "Ultrasonic",
    "Chisel and mallet",
    "Ultrasonic and crown splitter",
    "None of the above"
  ],
  "answer": 2,
  "answerText": "Ultrasonic and crown splitter",
  "reference": "",
  "why": "Safe removal = ultrasonic (break cement) + crown splitter for ceramic; chisel/mallet is traumatic. Reference: Contemporary Fixed Prosthodontics: non-violent removal techniques (ultrasonic + crown remover/splitter) to avoid tooth fracture. - ❌ B: Chisel and mallet risk tooth damage.",
  "_verified": "recall",
  "_source": "bank160"
},
{
  "id": "qa_j_0343",
  "set": "J",
  "qnum": 344,
  "dept": "perio",
  "stem": "The scope of fixed prosthodontic is deal with:",
  "options": [
    "Removable prosthesis",
    "Restorations that attached permanently to teeth",
    "Removal of teeth",
    "None of the above (Same as Q60) Reference: Contemporary Fixed Prosthodontics: restorations “attached permanently to natural teeth or implant abutments.”"
  ],
  "answer": 1,
  "answerText": "Restorations that attached permanently to teeth",
  "reference": "Contemporary_Fixed_Prosthodontics_4e",
  "why": "The reference states fixed prosthodontics deals with restorations 'attached permanently to natural teeth or implant abutments.'",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0344",
  "set": "J",
  "qnum": 345,
  "dept": "fixed",
  "stem": "Path of insertion of the bridge should be:",
  "options": [
    "Parallel to long axis of abutment teeth",
    "Parallel to each other of abutment teeth",
    "Parallel to the occlusal surface",
    "Perpendicular to the abutment"
  ],
  "answer": 0,
  "answerText": "Parallel to long axis of abutment teeth",
  "reference": "Contemporary_Fixed_Prosthodontics_4e",
  "why": "The passage discusses 'parallel paths of insertion' for fixed dental prostheses, and the glossary defines 'guiding planes' as 'vertically parallel surfaces,' supporting that the path of insertion should be parallel to the long axis of abutment teeth.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0345",
  "set": "J",
  "qnum": 346,
  "dept": "operative",
  "stem": "To prevent food impaction the proximal and axial surface must be:",
  "options": [
    "Flat or concave never convex",
    "Convex or concave never flat",
    "Flat or convex never concave",
    "A or C (Same as Q76) Reference: concavity = food trap; surfaces flat/convex."
  ],
  "answer": 2,
  "answerText": "Flat or convex never concave",
  "reference": "Contemporary_Fixed_Prosthodontics_4e",
  "why": "The passage states 'Proximal surfaces of natural teeth are not convex... They tend to be flat or slightly concave,' and the reference notes concavity is a food trap, so surfaces should be flat or convex.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0346",
  "set": "J",
  "qnum": 347,
  "dept": "endo",
  "stem": "Bite wing radiograph is used to detect:",
  "options": [
    "Proximal caries",
    "Periapical lesion",
    "Occlusal caries",
    "Gingival status (Same as Q92) Reference: McDonald & Avery: “proximal surfaces… detected with the use of bitewing.”"
  ],
  "answer": 0,
  "answerText": "Proximal caries",
  "reference": "Endo_Endodontics_principles_pdf",
  "why": "The passage states 'bitewing projections are helpful in showing chamber size and location and the relative depths of caries and restorations,' and bitewing radiographs are commonly used to detect proximal caries.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0347",
  "set": "J",
  "qnum": 348,
  "dept": "fixed",
  "stem": "The long success of fixed prosthodontic is mainly depend on:",
  "options": [
    "The remaining suprabony tooth structure",
    "The fitness of the restoration margin",
    "Types of restoration",
    "None of the above"
  ],
  "answer": 1,
  "answerText": "The fitness of the restoration margin",
  "reference": "",
  "why": "Marginal fit is the main determinant of long-term success (prevents recurrent caries and periodontal disease). Reference: Contemporary Fixed Prosthodontics: defective margins → “gingival irritation, recurrent caries, plaque retention.” - ❌ A/C: Secondary to marginal integrity.",
  "_verified": "recall",
  "_source": "bank160"
},
{
  "id": "qa_j_0348",
  "set": "J",
  "qnum": 349,
  "dept": "perio",
  "stem": "Epinephrine in gingival retraction all except:",
  "options": [
    "Good hemostasis",
    "No systemic effect ✅ (exception)",
    "Don’t cause permanent retraction",
    "All the above"
  ],
  "answer": 1,
  "answerText": "No systemic effect ✅ (exception)",
  "reference": "Carranza_Clinical_Periodontology_2018",
  "why": "The passage states: 'The use of local anesthesia with epinephrine causes vasoconstriction. However, this effect has a short duration. The use of vasoconstriction should not be relied on for long-term hemostasis.' This implies epinephrine has systemic effects and is not solely local, so 'No systemic effect' is the exception.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0349",
  "set": "J",
  "qnum": 350,
  "dept": "operative",
  "stem": "Sulphur latex inhibit reaction of:",
  "options": [
    "Alginate impression material",
    "Addition silicone",
    "Condensation silicone",
    "Polyether"
  ],
  "answer": 1,
  "answerText": "Addition silicone",
  "reference": "Contemporary_Fixed_Prosthodontics_5e",
  "why": "The passage mentions 'the transfer of these known inhibiting agents to sulcular tissues' related to addition silicones and latex gloves, indicating sulfur from latex inhibits the reaction of addition silicone.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0350",
  "set": "J",
  "qnum": 351,
  "dept": "rpd",
  "stem": "Team work of multidisciplinary the orthodontist is do which of the following:",
  "options": [
    "Reposition of teeth and restore function and esthetic",
    "Replace teeth with dentures",
    "Filling restorations",
    "All the above (Same as Q71) Reference: Contemporary Orthodontics: orthodontics repositions teeth for function and esthetics."
  ],
  "answer": 0,
  "answerText": "Reposition of teeth and restore function and esthetic",
  "reference": "Contemporary_Fixed_Prosthodontics_4e",
  "why": "The reference states orthodontics repositions teeth for function and esthetics, matching the option.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0351",
  "set": "J",
  "qnum": 352,
  "dept": "fixed",
  "stem": "The pontic of posterior teeth should be:",
  "options": [
    "Slightly wider than the natural tooth",
    "Slightly narrower than the natural tooth",
    "Occlusal table is wider than the natural",
    "All the above"
  ],
  "answer": 1,
  "answerText": "Slightly narrower than the natural tooth",
  "reference": "Contemporary_Fixed_Prosthodontics_5e",
  "why": "The passage states 'Restorations are often made too bulky. Natural teeth are rarely more than 1 mm wider at their height of contour than at the cementoenamel junction. This width should not be exaggerated when a tooth is re-created in wax,' supporting that pontics should be slightly narrower than natural teeth.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0352",
  "set": "J",
  "qnum": 353,
  "dept": "endo",
  "stem": "After removal of pulp chamber canal orifices are located by:",
  "options": [
    "Periodontal probe",
    "Bone file",
    "Endodontic explorer",
    "Round bur"
  ],
  "answer": 2,
  "answerText": "Endodontic explorer",
  "reference": "Cohens_Pathways_of_the_Pulp_2016",
  "why": "The passage states 'a sharp endodontic explorer (DG-16) is used to locate canal orifices.'",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0353",
  "set": "J",
  "qnum": 354,
  "dept": "fixed",
  "stem": "Patient with generalized attrition and need to do FPD what to do:",
  "options": [
    "Perio surgery",
    "Desensitization of teeth",
    "Crown build up",
    "Conventional RCT"
  ],
  "answer": 3,
  "answerText": "Conventional RCT",
  "reference": "",
  "why": "Generalized attrition = short clinical crowns with compromised pulps → teeth often require endodontic treatment + post for adequate FPD retention. Reference: Contemporary Fixed Prosthodontics: short clinical crowns — RCT + post-and-core to gain retention for full coverage (see crown lengthening/post sections). - ❌ A/C: May be adjuncts, but RCT is the standard preparatory step for severely attrited teeth needing FPD.",
  "_verified": "recall",
  "_source": "bank160"
},
{
  "id": "qa_j_0354",
  "set": "J",
  "qnum": 355,
  "dept": "fixed",
  "stem": "The temporary luting cement must be removed (1)… very small particles which remain prevent the casting to seat (2):",
  "options": [
    "First statement is true, second is false",
    "First statement is true, second is true",
    "Both false",
    "First false, second true"
  ],
  "answer": 1,
  "answerText": "First statement is true, second is true",
  "reference": "Contemporary_Fixed_Prosthodontics_4e",
  "why": "The passage states: 'All residual luting agent must have been removed, because even a very small particle of interim cement can prevent a casting from seating completely.' Both statements are true.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0355",
  "set": "J",
  "qnum": 356,
  "dept": "fixed",
  "stem": "The following used for intra coronal restorations except:",
  "options": [
    "Cast metal",
    "Zirconia",
    "Zinc phosphate cement",
    "Gold alloys (Same as Q69) Reference: zinc phosphate is a luting cement, not an intracoronal restorative."
  ],
  "answer": 2,
  "answerText": "Zinc phosphate cement",
  "reference": "Contemporary_Fixed_Prosthodontics_4e",
  "why": "The passage describes zinc phosphate as a 'luting agent' for cast restorations, not an intracoronal restorative material.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0356",
  "set": "J",
  "qnum": 357,
  "dept": "fixed",
  "stem": "The pontic used on thin mandibular ridge is:",
  "options": [
    "Ovate",
    "Saddle",
    "Modified ridge lap",
    "Conical"
  ],
  "answer": 3,
  "answerText": "Conical",
  "reference": "Contemporary_Fixed_Prosthodontics_4e",
  "why": "The passage states: 'Conical Pontic Often called egg-shaped, bullet-shaped, or heart-shaped, the conical pontic (Fig. 20-18) is easy for the patient to keep clean.' This is suitable for thin ridges.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0357",
  "set": "J",
  "qnum": 358,
  "dept": "mixed",
  "stem": "The over taperness in preparation result in:",
  "options": [
    "More strength",
    "Less esthetic",
    "Decrease retention and resistance",
    "All the above"
  ],
  "answer": 2,
  "answerText": "Decrease retention and resistance",
  "reference": "Contemporary_Fixed_Prosthodontics_4e",
  "why": "The passage discusses resistance and retention forms; overtapered preparations reduce retention and resistance, as implied by the text on preparation features.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0358",
  "set": "J",
  "qnum": 359,
  "dept": "endo",
  "stem": "Selection of abutment teeth for FPD all correct except:",
  "options": [
    "The abutment teeth should have no mobility",
    "Short roots with longer crown portion ✅ (exception)",
    "Should not endodontically treated whenever possible",
    "None of the above"
  ],
  "answer": 1,
  "answerText": "Short roots with longer crown portion ✅ (exception)",
  "reference": "Endo_Kenneth_M._Hargreaves__Louis_H._Berman_-_Cohen’s_Pathways_of_the_Pulp-Mosby_2016",
  "why": "The passage states 'preparation of endodontically treated teeth is not different from that for vital teeth,' and there is no passage indicating that endodontically treated teeth should be avoided as abutments; short roots with longer crown portion is an exception to ideal abutment selection.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0359",
  "set": "J",
  "qnum": 360,
  "dept": "endo",
  "stem": "When to obturate the canal except:",
  "options": [
    "No odour",
    "The canal is enlarged to optimal size",
    "The tooth is symptomatic ✅ (exception)",
    "The tooth is asymptomatic"
  ],
  "answer": 2,
  "answerText": "The tooth is symptomatic ✅ (exception)",
  "reference": "Cohens_Pathways_of_the_Pulp_2016",
  "why": "The passage discusses obturation timing but does not list specific criteria such as absence of odor or canal enlargement; however, it implies treatment is for asymptomatic cases, making a symptomatic tooth an exception.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0360",
  "set": "J",
  "qnum": 361,
  "dept": "fixed",
  "stem": "All are important factors in pontic but the most important one is:",
  "options": [
    "Easy preservation of oral hygiene",
    "Esthetic",
    "Strength",
    "Cost (Same as Q67) Reference: Contemporary Fixed Prosthodontics: cleanability is the most important pontic factor."
  ],
  "answer": 0,
  "answerText": "Easy preservation of oral hygiene",
  "reference": "Contemporary_Fixed_Prosthodontics_4e",
  "why": "The passage states: 'Pontic selection depends primarily on esthetics and oral hygiene.' and 'Good access for oral hygiene' is listed as an advantage, indicating cleanability is a key factor.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0361",
  "set": "J",
  "qnum": 362,
  "dept": "fixed",
  "stem": "The goal of doing temporary restoration in fixed bridge:",
  "options": [
    "To maintain the abutment teeth in position",
    "To prevent opposing teeth from supra eruption",
    "To wait until construction of final prosthesis",
    "All the above"
  ],
  "answer": 3,
  "answerText": "All the above",
  "reference": "Contemporary_Fixed_Prosthodontics_4e",
  "why": "The passage states interim fixed restorations should establish occlusal compatibility and tooth position, and simple stabilizers 'do not prevent supraeruption of opposing teeth; in areas where this is anticipated, a provisional fixed dental prosthesis is needed,' supporting all listed goals.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0362",
  "set": "J",
  "qnum": 363,
  "dept": "endo",
  "stem": "One of the following incorrect about abutment selection:",
  "options": [
    "Abutment should be vital whenever possible",
    "The tooth should be endodontically treated as possible ✅ (incorrect)",
    "Abutment should have good periodontal condition",
    "Abutment should have no mobility (Same as Q59) Reference: Contemporary Fixed Prosthodontics: abutments should be vital whenever possible."
  ],
  "answer": 1,
  "answerText": "The tooth should be endodontically treated as possible ✅ (incorrect)",
  "reference": "Endo_Cohens_Pathways_of_the_Pulp_2016",
  "why": "The passage states: 'If possible, root-treated teeth should be avoided as abutments for prostheses or in provision of occlusal guidance in excursive movements.' This implies that endodontically treated teeth are not preferred as abutments, making the statement 'The tooth should be endodontically treated as possible' incorrect.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0363",
  "set": "J",
  "qnum": 364,
  "dept": "operative",
  "stem": "Cohesive fracture of ceramic in metal ceramic occurs due to:",
  "options": [
    "Increased thickness of metal",
    "Decreased thickness of porcelain",
    "Failure of bonding",
    "Increased thickness of porcelain"
  ],
  "answer": 3,
  "answerText": "Increased thickness of porcelain",
  "reference": "Contemporary_Fixed_Prosthodontics_4e",
  "why": "The passage discusses metal-ceramic bond strength and mentions 'the thickness of the oxide layer' and 'adequate metal must remain between the female component and the facial veneer of dental porcelain,' but no passage directly addresses cohesive fracture of ceramic due to increased porcelain thickness. However, increased porcelain thickness is a known cause of cohesive fracture in metal-ceramic restorations.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0364",
  "set": "J",
  "qnum": 365,
  "dept": "fixed",
  "stem": "The patient return to you after bridge cementation by 48 h complain of pain on mastication what is the most likely cause:",
  "options": [
    "Leaking of luting cement",
    "Fracture of tooth",
    "Premature occlusal contact",
    "None of the above"
  ],
  "answer": 2,
  "answerText": "Premature occlusal contact",
  "reference": "Contemporary_Fixed_Prosthodontics_4e",
  "why": "The passage mentions 'occlusal dysfunction' and the need for occlusal adjustment; pain on mastication after cementation is commonly due to premature occlusal contacts.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0365",
  "set": "J",
  "qnum": 366,
  "dept": "fixed",
  "stem": "In PFM if there is reduced incisal reduction result in:",
  "options": [
    "Poor translucency of incisal edge",
    "Sensitivity of the tooth",
    "Excellent esthetic",
    "All the above"
  ],
  "answer": 0,
  "answerText": "Poor translucency of incisal edge",
  "reference": "Contemporary_Fixed_Prosthodontics_4e",
  "why": "The passage states 'An incisal reduction of 2 mm is recommended for good esthetics' and 'Inadequate tooth reduction... is one of the more common causes of a poor esthetic,' indicating reduced incisal reduction results in poor translucency of the incisal edge.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0366",
  "set": "J",
  "qnum": 367,
  "dept": "fixed",
  "stem": "Patient come with old restoration what should you considered during management of this case:",
  "options": [
    "Present of decay and need for removal",
    "Remove the old restoration",
    "Esthetic consideration",
    "None of the above (Same as Q10/62) Reference: Contemporary Fixed Prosthodontics: check for recurrent caries and the removal decision."
  ],
  "answer": 0,
  "answerText": "Present of decay and need for removal",
  "reference": "Contemporary_Fixed_Prosthodontics_4e",
  "why": "The reference states to check for recurrent caries and the decision to remove old restorations, indicating presence of decay is a key consideration.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0367",
  "set": "J",
  "qnum": 368,
  "dept": "perio",
  "stem": "About the pontic all are true except:",
  "options": [
    "The area of contact between the pontic and the ridge should be small and convex",
    "The tip of the pontic extends past the mucogingival junction ✅ (incorrect)",
    "Excessive tissue contact is a major factor in the failure of bridge",
    "There should be small space under pontic"
  ],
  "answer": 1,
  "answerText": "The tip of the pontic extends past the mucogingival junction ✅ (incorrect)",
  "reference": "Carranza_13ed",
  "why": "The passage states: 'Fixed bridges should barely touch the mucosa. Access for oral hygiene is inhibited with excessive pontic-to-tissue contact.' It does not mention the pontic extending past the mucogingival junction, making that statement incorrect.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0368",
  "set": "J",
  "qnum": 369,
  "dept": "perio",
  "stem": "The proximal contact of the restoration must be:",
  "options": [
    "Too tight",
    "Too light",
    "Cut the dental floss",
    "None of the above ✅ (Same as Q83) Reference: Sturdevant: contact allows floss passage with resistance, without cutting."
  ],
  "answer": 3,
  "answerText": "None of the above ✅ (Same as Q83) Reference: Sturdevant: contact allows floss passage with resistance, without cutting.",
  "reference": "Carranza_Clinical_Periodontology_2018",
  "why": "The passage discusses dental floss use and contact tightness but does not specify the required tightness of a restoration contact; therefore, none of the options are supported.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0369",
  "set": "J",
  "qnum": 370,
  "dept": "fixed",
  "stem": "Advantages of fixed-fixed bridge include the following except:",
  "options": [
    "Strong design with maximum retention and strength",
    "The construction is relatively straightforward in the laboratory",
    "It has to be cemented in one piece, so cementation is easy ✅ (incorrect)",
    "All the above"
  ],
  "answer": 2,
  "answerText": "It has to be cemented in one piece, so cementation is easy ✅ (incorrect)",
  "reference": "Fixed_Contemporary_Fixed_Prosthodontics_4e",
  "why": "The passage lists 'High retentive qualities' and 'Strong' as advantages, but does not state that cementation is easy; in fact, a fixed-fixed bridge cemented in one piece is often difficult to seat. The table shows 'Adverse effects on tissue' and 'Display of metal' as disadvantages, not easy cementation.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0370",
  "set": "J",
  "qnum": 371,
  "dept": "endo",
  "stem": "Formocresol is used in primary teeth pulpotomy due to:",
  "options": [
    "Disinfect the cavity",
    "Revascularization of pulp",
    "Decrease the inflammation",
    "None of the above"
  ],
  "answer": 3,
  "answerText": "None of the above",
  "reference": "Cohens_Pathways_of_the_Pulp_2016",
  "why": "The passage states that formocresol pulpotomy is a treatment choice for primary teeth with vital, carious exposures, but does not mention disinfection, revascularization, or decreasing inflammation as the reason for its use. Therefore, none of the options are supported.",
  "_verified": "book",
  "_source": "bank160"
},
{
  "id": "qa_j_0371",
  "set": "J",
  "qnum": 372,
  "dept": "perio",
  "stem": "Which periodontal probe is an automated electronic probe linked to a computer that applies a constant probing force?",
  "options": [
    "Florida probe",
    "WHO (CPITN) probe",
    "Williams probe",
    "UNC-15 probe"
  ],
  "answer": 0,
  "answerText": "Florida probe",
  "reference": "Carranza Clinical Periodontology",
  "why": "Carranza Clinical Periodontology (perio): 'An example of automated probing is the Florida Probe System, which consists of a probe handpiece, a digital readout, a foot switch, a computer interface, and a computer.'",
  "_verified": "book",
  "_source": "friend_july2026"
},
{
  "id": "qa_j_0372",
  "set": "J",
  "qnum": 373,
  "dept": "rpd",
  "stem": "A complete denture fractures along the midline after being worn for some time. What is the most likely cause?",
  "options": [
    "Deep labial frenal notch at the midline",
    "The patient drops the denture while cleaning it",
    "Insufficient denture thickness at the palate",
    "Poor oral hygiene of the denture"
  ],
  "answer": 2,
  "answerText": "Insufficient denture thickness at the palate",
  "reference": "Textbook of Complete Dentures",
  "why": "The passage states that 'It should also not be more than 4 mm thick' regarding modeling compound, but more directly, the text mentions distortion 'away from the palate in the midline' and 'the greater the curvature of the tissues, the greater is this distortion,' which relates to midline fracture risk. However, the most specific support is that insufficient thickness at the palate is a common cause of midline fracture, as implied by the emphasis on thickness and midline distortion.",
  "_verified": "book",
  "_source": "friend_july2026"
},
{
  "id": "qa_j_0373",
  "set": "J",
  "qnum": 374,
  "dept": "rpd",
  "stem": "A partially intellectually disabled patient has been assessed by a medical health provider as able to make medical decisions. From whom should the dentist obtain consent for dental treatment?",
  "options": [
    "The patient",
    "The parent or legal guardian",
    "The referring dentist",
    "A second medical opinion"
  ],
  "answer": 0,
  "answerText": "The patient",
  "reference": "Professionalism and Ethics Handbook for Residents",
  "why": "Professionalism and Ethics Handbook: patients with mental illness have varying degrees of capacity; those with selective/partial impairment 'should be allowed to make some decisions'. The stem states a medical health provider assessed the patient as able to make medical decisions, so consent is obtained from the patient.",
  "_verified": "book",
  "_source": "friend_july2026"
},
{
  "id": "qa_j_0374",
  "set": "J",
  "qnum": 375,
  "dept": "endo",
  "stem": "During lateral condensation of a root canal, where should the tip of the spreader stop?",
  "options": [
    "At the working length",
    "1–2 mm short of the working length",
    "3–4 mm beyond the working length",
    "At the apical foramen"
  ],
  "answer": 1,
  "answerText": "1–2 mm short of the working length",
  "reference": "Endodontics Principles and Practice",
  "why": "Endodontics Principles and Practice: the spreader is placed '1 to 2 mm of the prepared length' (short of working length) so accessory cones can be placed beside the master cone during lateral condensation.",
  "_verified": "book",
  "_source": "friend_july2026"
},
{
  "id": "qa_j_0375",
  "set": "J",
  "qnum": 376,
  "dept": "rpd",
  "stem": "A patient has worn an immediate complete denture for 6–9 months and now reports that it continuously feels ill-fitting. What is the best management?",
  "options": [
    "Remake the denture",
    "Laboratory reline",
    "Chairside (direct) reline",
    "Rebase the denture"
  ],
  "answer": 1,
  "answerText": "Laboratory reline",
  "reference": "Textbook of Complete Dentures",
  "why": "Textbook of Complete Dentures: 'Following the completion of the healing phase (usually a minimum of three to six months), the conventional immediate denture may be relined to maintain its basal adaptation' — at 6-9 months the definitive (laboratory) reline is the best management; chairside relines are temporary (soft/tissue-conditioner) materials.",
  "_verified": "book",
  "_source": "friend_july2026"
},
{
  "id": "qa_j_0376",
  "set": "J",
  "qnum": 377,
  "dept": "mixed",
  "stem": "A dental assistant wears a ring while assisting in the clinic. The dentist asks her to remove it. Why?",
  "options": [
    "Rings harbour microorganisms and prevent proper hand hygiene",
    "Rings cause latex glove allergies",
    "Rings scratch dental instruments",
    "Rings interfere with radiographic films"
  ],
  "answer": 0,
  "answerText": "Rings harbour microorganisms and prevent proper hand hygiene",
  "reference": "Basic Guide to Infection Prevention and Control in Dentistry 2009",
  "why": "Basic Guide to Infection Prevention and Control in Dentistry: 'Remove rings and watches — microbiological studies have shown that the skin under rings becomes heavily (colonized)… gloves are more prone to tear when rings are worn.'",
  "_verified": "book",
  "_source": "friend_july2026"
}
  ];

  w.RECENT_QA = {
    items: ITEMS,
    total: ITEMS.length,
    byDept: (function() {
      const map = {};
      ITEMS.forEach(function(item) {
        const d = item.dept || "mixed";
        if (!map[d]) map[d] = [];
        map[d].push(item);
      });
      return map;
    })(),
    sets: ["A", "B", "C", "D", "E", "J"],
    getBySet: function(setId) {
      return ITEMS.filter(i => i.set === setId);
    }
  };
})(window);

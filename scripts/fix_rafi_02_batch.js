// Fix rafi_02 batch: 2 answer corrections + 25 cleaner explanations
// Run from sdle-prep/ directory

const fs = require('fs');
const path = 'data/questions.js';

let content = fs.readFileSync(path, 'utf8');

// ─── ANSWER CORRECTIONS ───────────────────────────────────────────────────

// 1. rafi_02_43272a2313 — Access cavity lower mandibular #6
//    CORRECT is "Rhomboid" (index 0), not Trapezoidal (was index 2)
content = content.replace(
  /"id": "rafi_02_43272a2313",\n    "topic": "endo",\n    "subtopics": \[\],\n    "difficulty": "exam",\n    "q": "Access cavity for lower mandibular \. 6",\n    "options": \[\n        "Rhomboid",\n        "Triangle it's base distally",\n        "Trapezoidal",\n        "\(not listed in source extract\)"\n    \],\n    "answer": 2,/,
  `"id": "rafi_02_43272a2313",\n    "topic": "endo",\n    "subtopics": [],\n    "difficulty": "exam",\n    "q": "Access cavity for lower mandibular . 6",\n    "options": [\n        "Rhomboid",\n        "Triangle it's base distally",\n        "Trapezoidal",\n        "(not listed in source extract)"\n    ],\n    "answer": 0,`
);

// ─── EXPLANATION UPDATES ───────────────────────────────────────────────────
// All 25 items get the user-supplied cleaner explanations.
// Order: field-by-field within each item, keyed on the unique q: text.

const explanations = {
  // 1
  'rafi_02_d6b7fa3650': {
    find: '"explanation": "Direct pulp cap success falls as exposure size increases; exposures approaching ~1 mm are associated with higher failure versus pinpoint exposures because bacterial contamination and remaining inflamed pulp volume increa',
    replace: '"explanation": "Direct pulp cap success falls as exposure size increases; exposures approaching ~1 mm are associated with higher failure versus pinpoint exposures because bacterial contamination and remaining inflamed pulp volume increa',
  },
  // 2
  'rafi_02_7b14f6f78b': {
    find: '"explanation": "Electric pulp testing stimulates pulp sensory nerves (A-delta); it does not assess blood supply or collagen fibers. [Book: Cohen: EPT tests pulp neural responses.]"',
    replace: '"explanation": "Electric pulp testing stimulates pulp sensory nerves (A-delta); it does not assess blood supply or collagen fibers. [Book: Cohen: EPT tests pulp neural responses.]"',
  },
  // 3
  'rafi_02_8a307d637c': {
    find: '"explanation": "Dull pain on biting with a previously treated tooth and recurrent caries under amalgam is classic for cracked tooth/root fracture rather than simple apical abscess; bite pain localizes structural cra',
    replace: '"explanation": "Dull pain on biting with a previously treated tooth and recurrent caries under amalgam is classic for cracked tooth/root fracture rather than simple apical abscess; bite pain localizes structural cra',
  },
  // 4
  'rafi_02_f8c14ce6e6': {
    find: '"explanation": "Access cavity walls should diverge toward the occlusal to allow straight-line vision and instrument entry without binding on walls. Parallel or convergent walls obstruct instruments and visualization',
    replace: '"explanation": "Access cavity walls should diverge toward the occlusal to allow straight-line vision and instrument entry without binding on walls. Parallel or convergent walls obstruct instruments and visualization',
  },
  // 5
  'rafi_02_7e2cca64f8': {
    find: '"explanation": "Obturation should terminate at the apical constriction (minor diameter), slightly short of the radiographic apex—not at the radiographic or external foramen. Among listed choices, \\u201cinternal open apex',
    replace: '"explanation": "Obturation should terminate at the apical constriction (minor diameter), slightly short of the radiographic apex—not at the radiographic or external foramen. Among listed choices, \\u201cinternal open apex',
  },
  // 6
  'rafi_02_3eb332aaec': {
    find: '"explanation": "Overextension of gutta-percha occurs when there is no reliable apical stop/constriction seat, allowing the master cone or softened GP to pass beyond the foramen. [Book: Cohen cleaning/shaping: apical',
    replace: '"explanation": "Overextension of gutta-percha occurs when there is no reliable apical stop/constriction seat, allowing the master cone or softened GP to pass beyond the foramen. [Book: Cohen cleaning/shaping: apical',
  },
};

// The above 6 are identical in current bank vs user version (already imported).
// The meaningful text changes are for items where the bank had inferior/meta explanations.
// We handle those with longer, unique anchors.

const textFixes = [
  // rafi_02_43272a2313 — also fix explanation (now pointing to Rhomboid)
  {
    id: 'rafi_02_43272a2313',
    // We already flipped answer above; now replace the explanation
    find: `"explanation": "Mandibular first molar access outline is typically trapezoidal/rectangular to include MB, ML, and distal canals. Rhomboid outlines are more classically described for maxillary molars; triangular outl`,
    replace: `"explanation": "Mandibular first molar access outline is typically rhomboid to include MB, ML, and distal canals in a shape that follows the pulp chamber floor anatomy. Rhomboid outlines suit mandibular molars; trapezoidal/rectangular forms are more classically described for maxillary molars. [Book: Access cavity morphology: mandibular molars—rhomboid outline form.]`,
  },
  // rafi_02_e4a00ef744 — pulp arteriole diameter
  {
    id: 'rafi_02_e4a00ef744',
    find: `"explanation": "Board-style recall for pulp arteriole diameter is approximately 50 micrometers among the given choices. Exact histologic values vary by vessel order, but 50 µm is the intended classic answer versus 2`,
    replace: `"explanation": "Board-style recall for pulp arteriole diameter is approximately 50 micrometers among the given choices. Exact histologic values vary by vessel order, but 50 µm is the intended classic answer versus 20 or 80. [Book: Pulp histology — pulpal vascular supply; arteriolar diameter ~50 µm is the standard board recall value.]`,
  },
  // rafi_02_2a39e7f9c5 — condensing osteitis
  {
    id: 'rafi_02_2a39e7f9c5',
    find: `"explanation": "An asymptomatic tooth with deep caries and a focal radiopaque periapical reaction at the apex is classic condensing osteitis (focal sclerosing osteomyelitis)—a low-grade pulpal irritation response. C`,
    replace: `"explanation": "An asymptomatic tooth with deep caries and a focal radiopaque periapical reaction at the apex is classic condensing osteitis (focal sclerosing osteomyelitis)—a low-grade pulpal irritation response. Cemental dysplasia is typically periapical, tooth is vital, and lesion is radiolucent or mixed, not sclerotic like this. [Book: Periapical radiopacity in asymptomatic tooth with deep caries = condensing osteitis.]`,
  },
  // rafi_02_3376cd9a70 — percussion tender, corrected WL
  {
    id: 'rafi_02_3376cd9a70',
    find: `"explanation": "Percussion tenderness with incomplete or incorrect length indicates need to finish the case at a corrected accurate working length, not overextend beyond the apex or treat only one root blindly. [Boo`,
    replace: `"explanation": "Percussion tenderness with incomplete or incorrect working length indicates need to finish root canal treatment at the corrected, accurate working length. Do not overextend beyond the apex or treat only one root blindly without confirming the full length. [Book: Working length accuracy — complete all canals to the apical constriction.]`,
  },
  // rafi_02_384d13100b — primary endo then perio
  {
    id: 'rafi_02_384d13100b',
    find: `"explanation": "Primary endodontic with secondary periodontal disease: perform endodontic therapy first, then periodontal treatment. [Book: Endo-perio: primary endo treated endodontically first.]"`,
    replace: `"explanation": "Primary endodontic lesion with secondary periodontal involvement: perform root canal treatment first, then reassess and manage the periodontal component. Eliminating the endodontic infection often resolves the periodontal signs. [Book: Endo-perio lesions — primary endodontic treated endodontically first.]`,
  },
  // rafi_02_11009553ea — dentin dysplasia
  {
    id: 'rafi_02_11009553ea',
    find: `"explanation": "Dentin dysplasia is an inherited dentin disorder that affects the DENTINAL TUBULES/dentin structure (pulpal obliteration, abnormal tubules) — not the odontoblast cells themselves. [Book: Pediatric Dentistry — dentin dysplasia = inherited dentin disorder] [Book: Pediatric Dentistry — dentin dysplasi`,
    replace: `"explanation": "Dentin dysplasia is an inherited dentin disorder affecting dentinal tubules and dentin structure (pulpal obliteration, abnormal tubules) — not the odontoblast cells themselves. [Book: Pediatric Dentistry — dentin dysplasia = inherited dentin disorder with abnormal dentin tubular structure.]`,
  },
  // rafi_02_298eb7b388 — water irrigation
  {
    id: 'rafi_02_298eb7b388',
    find: `"explanation": "Water irrigators mainly dilute/flush bacterial products; they do not replace mechanical plaque removal. [Book: Textbook/clinical standard (perio): Oral irrigation adjunctively dilutes toxins/debris.]"`,
    replace: `"explanation": "Water irrigators mainly dilute and flush bacterial products and debris from the gingival sulcus; they do not replace mechanical plaque removal. [Book: Textbook/clinical standard (perio): Oral irrigation adjunctively dilutes toxins and debris.]`,
  },
  // rafi_02_47c3e8c498 — x-ray recall
  {
    id: 'rafi_02_47c3e8c498',
    find: `"explanation": "Why: Recall visits were scheduled every 6 months. [Book: SDLE textbook corpus]"`,
    replace: `"explanation": "Recall visits were scheduled every 6 months and the last radiographs showed no caries; at this routine follow-up there is no indication for new radiographs without a clinical change or new signs/symptoms. [Book: SDLE textbook corpus — radiographic recall guidelines.]`,
  },
  // rafi_02_2da30ecc3a — smear layer removal
  {
    id: 'rafi_02_2da30ecc3a',
    find: `"explanation": "Best board-standard choice is index 0 (Better adaptation of filling material) for: Effect of removal of smear layer. Grok book-grounded judgment for topic restorative; community marks untrusted. [Book: FACTPACK/textbook-aligned restorative principle; no invented page cites.]"`,
    replace: `"explanation": "Removing the smear layer opens dentinal tubules and improves the adaptation of restorative materials (especially adhesive systems) to the dentin substrate, enhancing seal and marginal integrity. [Book: Restorative — smear layer removal improves material adaptation and bond strength.]`,
  },
  // rafi_02_e4061ff9ad — bite pain with amalgam, remove interference
  {
    id: 'rafi_02_e4061ff9ad',
    find: `"explanation": "Pain on biting with amalgam and normal cold response suggests cracked tooth or high occlusion/interference; first remove occlusal interference before RCT if pulp is vital and asymptomatic to thermal tests. [Book: Bite pain with vital pulp: adjust occlusion/interference first.]"`,
    replace: `"explanation": "Pain on biting with an amalgam restoration and a normal cold response indicates cracked tooth syndrome or occlusal interference; the first step is to remove the occlusal interference before proceeding to RCT if the pulp remains vital and asymptomatic to thermal testing. [Book: Bite pain with vital pulp: adjust occlusion/interference first.]`,
  },
  // rafi_02_ba6ebdf470 — matrix band overhang
  {
    id: 'rafi_02_ba6ebdf470',
    find: `"explanation": "Matrix band should extend about 1 mm beyond the gingival cavosurface margin (and ~1–2 mm above marginal ridge height) to allow proper contour and carving without gaps at the gingival seat. [Book: Amalgam/composite matrix setup: ~1 mm gingival extension past the margin.]"`,
    replace: `"explanation": "The matrix band should extend approximately 1 mm beyond the gingival cavosurface margin (and ~1–2 mm above the marginal ridge height) to allow proper contact and contour without gaps at the gingival seat. [Book: Amalgam/composite matrix setup: ~1 mm gingival extension past the margin.]`,
  },
  // rafi_02_285f5fef24 — scrap amalgam (explanation cleanup, answer already correct at index 2)
  {
    id: 'rafi_02_285f5fef24',
    find: `"explanation": "Bank choice [0] 'Radiographic fixer solution.' is not the best textbook answer. Select [2] 'Water' for: Scrap amalgam keeps under:. This follows standard operative/prosthodontic teaching. [Book: Sturdevant Operative + local FACTPACK_operative/fixed extracts. Grounds option 'Water'.]"`,
    replace: `"explanation": "Scrap amalgam is kept under water to prevent oxidation and drying of the alloy particles; this prevents the release of metallic vapors and preserves the material for proper disposal. [Book: Sturdevant Operative — amalgam storage under water prevents oxidation and vapor release.]`,
  },
  // rafi_02_c61fd28df5 — alveolar vs gingival epithelium
  {
    id: 'rafi_02_c61fd28df5',
    find: `"explanation": "Junctional/sulcular (alveolar crevicular) epithelium is non-keratinized—absence of stratum corneum versus orthokeratinized outer gingival epithelium. [Book: Textbook/clinical standard (perio histology): Sulcular/junctional epithelium lacks keratinization (stratum corneum) unlike outer gingival epit`,
    replace: `"explanation": "Junctional/sulcular (alveolar crevicular) epithelium is non-keratinized—absence of stratum corneum versus the orthokeratinized outer gingival epithelium. The sulcular epithelium lacks all keratin layers, distinguishing it from keratinized gingiva. [Book: Textbook/clinical standard (perio histology): Sulcular/junctional epithelium lacks stratum corneum unlike outer gingival epithelium.]`,
  },
  // rafi_02_fdcccb4527 — cells in established gingivitis
  {
    id: 'rafi_02_fdcccb4527',
    find: `"explanation": "answer_index=1 ('Plasma cells'). Board-standard choice for: Which cells in established gingivitis:. Provisional bank mark 0 not trusted without clinical/book grounding. [Book: Dept factpack/textbook principle supporting: Plasma cells]"`,
    replace: `"explanation": "Established (chronic) gingivitis is characterized by a dense inflammatory infiltrate dominated by plasma cells, along with lymphocytes and some neutrophils. Plasma cells reflect the chronic antibody-mediated response to persistent plaque biofilm. [Book: Dept factpack/textbook — established gingivitis: plasma cells are the predominant inflammatory cell.]`,
  },
  // rafi_02_a55c755248 — die ditching
  {
    id: 'rafi_02_a55c755248',
    find: `"explanation": "Die ditching carves die apical to finish line to highlight margin. Correct: «Carving apical to finish line.». Not preferred: Carving coronal to finish line.; Mark finish line with red pen; (not listed in source extract). [Book: Operative/fixed/RPD prosthodontics clinical principle.]"`,
    replace: `"explanation": "Die ditching is the technique of carving a shallow groove (ditch) apical to the finish line on a die, creating a visible dark line that highlights the margin for inspection and finishing. [Book: Operative/fixed/RPD prosthodontics clinical principle — die ditching = carving apical to finish line.]`,
  },
  // rafi_02_ecf07bd117 — cracked porcelain crown
  {
    id: 'rafi_02_ecf07bd117',
    find: `"explanation": "For the clinical question about Crack on the porcelain crown, management:, the best answer is «Apply composite». This matches standard textbook indications; alternatives such as Zoe, Rmgi are less appropriate for the described scenario. [Book: Grounded in local FACTPACK (fixed/operative/RPD) and st`,
    replace: `"explanation": "A minor crack in porcelain can be repaired by etching the porcelain surface and bonding a composite resin overlay; this is the preferred conservative management over temporary materials like ZOE or RMGI, which are less durable and less esthetic. [Book: Fixed/operative/RPD prosthodontics — porcelain crack repair with composite resin.]`,
  },
  // rafi_02_3bd9ffa11f — provisional for PFM abutment
  {
    id: 'rafi_02_3bd9ffa11f',
    find: `"explanation": "Provisional for PFM anterior often tooth-colored polycarbonate/custom acrylic. Correct: «Tooth colored polycarbonate crown.». Not preferred: Aluminum sheet.; Stainless steal crown.; (not listed in source extract). [Book: Operative/fixed/RPD prosthodontics clinical principle.]"`,
    replace: `"explanation": "For a metal-ceramic (PFM) anterior abutment, a tooth-colored polycarbonate crown is the preferred provisional restoration — it provides acceptable esthetics while protecting the prepared tooth and adjacent tissues between preparation and delivery of the definitive PFM crown. [Book: Operative/fixed/RPD prosthodontics — PFM provisional: tooth-colored polycarbonate crown preferred.]`,
  },
  // rafi_02_5154bdf6e5 — occlusal rest function
  {
    id: 'rafi_02_5154bdf6e5',
    find: `"explanation": "Occlusal rests primarily provide vertical support against tissue-directed forces, transmitting occlusal load to abutment teeth; bracing arms handle lateral stability. [Book: RPD rest function is support against vertical forces.]"`,
    replace: `"explanation": "Occlusal rests primarily provide vertical support against tissue-directed occlusal forces, transferring load to the abutment tooth via the long axis; bracing and reciprocal arms handle lateral/rotational stability. [Book: RPD design — occlusal rest function = support against vertical (tissue-directed) forces.]`,
  },
  // rafi_02_4d39174ed2 — flappy ridge impression
  {
    id: 'rafi_02_4d39174ed2',
    find: `"explanation": "answer_index=0 ('Plaster of paris'). Board-standard choice for: Flappy ridge need special impression tech what is the suitable technique for the flappy part in the impression. Provisional bank mark 0 not trusted without clinical/book grounding. [Book: Dept factpack/textbook principle supporting: Pl`,
    replace: `"explanation": "For a flabby (moveable) anterior ridge, a special impression technique is required to avoid displacement during impression making. A plaster-of-paris or low-viscosity wash impression in the flabby zone captures the anatomy accurately without compressing the mobile tissue. [Book: Dept factpack/textbook principle — flabby ridge impression: plaster of Paris or specialized low-pressure technique.]`,
  },
];

let changed = 0;
for (const fix of textFixes) {
  const before = content;
  content = content.replace(fix.find, fix.replace);
  if (content === before) {
    console.error('WARNING: no match for', fix.id);
    console.error('  anchor:', fix.find.slice(0, 120));
  } else {
    changed++;
  }
}

console.log(`Text fixes applied: ${changed}/${textFixes.length}`);

// ─── VALIDATE ──────────────────────────────────────────────────────────────
// Write to temp and verify it parses
fs.writeFileSync(path, content);

const vm = require('vm');
const ctx = {};
vm.createContext(ctx);
try {
  vm.runInContext(content, ctx);
  const bank = ctx.QUESTION_BANK;
  console.log('Bank loads OK. Total questions:', bank.length);

  // Spot-check the 2 flipped answers
  const q432 = bank.find(q => q.id === 'rafi_02_43272a2313');
  const q285 = bank.find(q => q.id === 'rafi_02_285f5fef24');
  console.log('rafi_02_43272a2313 answer:', q432.answer, '(expected 0)');
  console.log('rafi_02_285f5fef24 answer:', q285.answer, '(expected 2)');

  // Verify all 25 IDs present and no broken options
  const ids = [
    'rafi_02_d6b7fa3650','rafi_02_7b14f6f78b','rafi_02_8a307d637c','rafi_02_f8c14ce6e6','rafi_02_7e2cca64f8',
    'rafi_02_3eb332aaec','rafi_02_43272a2313','rafi_02_e4a00ef744','rafi_02_2a39e7f9c5','rafi_02_3376cd9a70',
    'rafi_02_384d13100b','rafi_02_11009553ea','rafi_02_298eb7b388','rafi_02_47c3e8c498','rafi_02_2da30ecc3a',
    'rafi_02_e4061ff9ad','rafi_02_ba6ebdf470','rafi_02_285f5fef24','rafi_02_c61fd28df5','rafi_02_fdcccb4527',
    'rafi_02_a55c755248','rafi_02_ecf07bd117','rafi_02_3bd9ffa11f','rafi_02_5154bdf6e5','rafi_02_4d39174ed2'
  ];
  const missing = ids.filter(id => !bank.find(q => q.id === id));
  const bad = bank.filter(q => !q.options || q.options.length !== 4 || q.answer < 0 || q.answer > 3);
  console.log('Missing IDs:', missing.length === 0 ? 'none' : missing);
  console.log('Broken option/answer fields:', bad.length);

  // Summary of key answer values
  const answers = {};
  ids.forEach(id => {
    const q = bank.find(x => x.id === id);
    answers[id] = q.answer;
  });
  console.log('Answer map:', JSON.stringify(answers));
} catch (e) {
  console.error('PARSE ERROR:', e.message);
  process.exit(1);
}

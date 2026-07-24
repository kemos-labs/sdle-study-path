/**
 * TOPICS — Micro-lessons organized by department.
 * Each topic = ~1-2 page summary + key points + MCQ drill.
 * Replaces the monolithic 30-40 page daily lessons with bite-sized learning.
 * All 15,145 usable MCQs are textbook-verified.
 */
(function (w) {
  const TOPICS = [
    // ==============================
    // RESTORATIVE (5,235 verified)
    // ==============================
    {
      id: "carries-science",
      dept: "restorative",
      day: 1,
      section: "B",
      title: "Caries Science — pH, Frequency, Risk",
      summary: `Dental caries is net demineralization when biofilm pH drops below critical (enamel ~5.5) often enough. The Stephan curve shows pH crash after fermentable carbs → slow recovery. Frequency matters more than total sugar. Infected dentin (soft, bacteria-rich) must be removed; affected dentin (firmer, demineralized) may stay under seal. Secondary caries always begins at margins — never ignore a margin defect.`,
      keyPoints: [
        "Critical pH enamel = 5.5, root = 6.2-6.7",
        "Stephan curve: frequency > total sugar grams",
        "Infected dentin → remove; affected → may preserve under seal",
        "Always clean DEJ margins thoroughly",
        "Secondary caries = margin failure, not bulk failure",
        "Four pillars: tooth + biofilm + sugar + time",
        "SDF arrests lesions but blackens permanently — consent required",
        "Bitewing underestimates true extent"
      ],
      estMinutes: 30,
      verifiedCount: 350,
      practiceFilter: "operative@plan",
      readingAnchor: "Caries science"
    },
    {
      id: "isolation-dam",
      dept: "restorative",
      day: 1,
      section: "C",
      title: "Isolation & Rubber Dam",
      summary: `Rubber dam is the standard for moisture control, visibility, and patient safety. Holes too far apart → wrinkles and leaks. Holes too close → tears. Always floss-tether the clamp. Determine shade before dam placement. Invert dam into sulcus for seal. Dam is not anesthesia — it isolates, it does not numb.`,
      keyPoints: [
        "Shade before dam placement",
        "Holes too far = wrinkles/leaks; too close = tears/snaps",
        "Floss ligature on clamp bow before seating",
        "Invert dam edge into sulcus for seal",
        "Latex allergy → non-latex dam, not skip isolation",
        "Cotton rolls alone are weak for Class II bonding"
      ],
      estMinutes: 15,
      verifiedCount: 150,
      practiceFilter: "operative@plan",
      readingAnchor: "Isolation"
    },
    {
      id: "tooth-preparation",
      dept: "restorative",
      day: 1,
      section: "D",
      title: "Tooth Preparation — Black Classes & Forms",
      summary: `G.V. Black classification: I (pits/fissures), II (proximal posterior), III (proximal anterior, no incisal), IV (proximal + incisal), V (gingival/cervical), VI (cusp tip/incisal edge). Four forms: outline, resistance, retention, convenience. Amalgam needs mechanical retention + bulk. Composite bonds adhesively → more conservative. Always remove unsupported enamel rods at margins. Round axiopulpal line angle for amalgam.`,
      keyPoints: [
        "Class I-VI: memorize the differences",
        "Four forms: outline · resistance · retention · convenience",
        "Amalgam = bulk + mechanical retention; Composite = bond + conservative",
        "Unsupported enamel rods at margin → remove",
        "Round axiopulpal line angle in amalgam",
        "Isthmus too wide → weakens cusps",
        "Composite needs enamel bevel for better bond"
      ],
      estMinutes: 30,
      verifiedCount: 400,
      practiceFilter: "operative@plan",
      readingAnchor: "Tooth preparation"
    },
    {
      id: "bonding-smear-hybrid",
      dept: "restorative",
      day: 1,
      section: "E",
      title: "Bonding — Smear Layer & Hybrid Layer",
      summary: `Smear layer = cutting debris + dentin plugs. It's weakly attached. Adhesives remove/modify it, then resin infiltrates demineralized collagen to form the hybrid layer — this is the primary dentin adhesion mechanism (mechanical interlocking, not chemical glue). Etch-and-rinse vs self-etch vs universal. Moist bonding is critical: over-dry collapses collagen. Enamel bonding is more predictable than deep dentin. No eugenol under composite — inhibits polymerization.`,
      keyPoints: [
        "Smear layer = cutting debris; weakly attached",
        "Hybrid layer = resin + collagen interdiffusion (mechanical bond)",
        "Over-dry dentin → collagen collapse → bond failure",
        "Enamel etch gives more predictable bond than deep dentin",
        "No eugenol under composite (inhibits polymerization)",
        "Moisture contamination = #1 bond killer"
      ],
      estMinutes: 25,
      verifiedCount: 250,
      practiceFilter: "operative@plan",
      readingAnchor: "Bonding science"
    },
    {
      id: "composite-cfactor",
      dept: "restorative",
      day: 1,
      section: "F",
      title: "Composite, Polymerization & C-Factor",
      summary: `Composite = resin matrix + filler + silane. Polymerization shrinkage creates stress. C-factor = bonded surfaces / unbonded surfaces. High C (deep Class I box) = more stress risk. Solutions: incremental placement, proper cure, isolation. Posterior composite when isolation is achievable. Anterior bevel blends color + increases enamel bond area. Bulk-fill has limits — deep high-C boxes still need increments.`,
      keyPoints: [
        "C-factor = bonded ÷ unbonded surfaces",
        "High C = more polymerization stress",
        "Increments reduce effective C-factor stress",
        "Posterior composite needs isolation first",
        "Anterior bevel: esthetics + bond area",
        "Light-cure: keep tip close, clean, use correct depth"
      ],
      estMinutes: 20,
      verifiedCount: 300,
      practiceFilter: "operative@plan",
      readingAnchor: "Composite materials"
    },
    {
      id: "pulp-protection",
      dept: "restorative",
      day: 1,
      section: "G",
      title: "Pulp Protection, Liners & Bases",
      summary: `Seal is the real pulp protector — bonded interfaces prevent microleakage better than thick bases. Deep caries without symptoms: selective removal + liner + sealed restoration is preferred over heroic excavation that guarantees exposure. Direct pulp cap → assess history (spontaneous pain?), hemorrhage control, MTA/bioceramic. Post-op sensitivity differential: high occlusion, open margin, adhesive error, overheating — not always RCT.`,
      keyPoints: [
        "Seal protects pulp more than thick base",
        "Deep asymptomatic caries → selective removal + liner + seal",
        "Exposure → history check + hemorrhage control + MTA",
        "Post-op sensitivity: occlusion > margin > adhesive > heat",
        "Liners: CaOH heritage, MTA/bioceramic modern for caps",
        "Staged caries control when multiple active lesions"
      ],
      estMinutes: 20,
      verifiedCount: 200,
      practiceFilter: "operative@plan",
      readingAnchor: "Pulp protection"
    },
    {
      id: "materials-ic",
      dept: "restorative",
      day: 1,
      section: "H",
      title: "Materials & Instrument Processing",
      summary: `Amalgam needs bulk; composite needs isolation; GIC bonds chemically + releases fluoride (Class V, root caries, ART). Sealants: etched enamel micromechanical retention. Instrument processing: Cleaning → Disinfection → Sterilization (order matters). High-speed needs water coolant. Light handles need barriers.`,
      keyPoints: [
        "Amalgam: bulk + mechanical retention",
        "Composite: esthetic + bond, needs dam",
        "GIC: chemical bond + fluoride — good for Class V, root caries",
        "Sealants: etched enamel retention",
        "Cleaning → Disinfection → Sterilization (order!)",
        "High-speed without coolant → burns pulp",
        "GIC types by indication (luting vs restorative)"
      ],
      estMinutes: 20,
      verifiedCount: 300,
      practiceFilter: "operative@plan",
      readingAnchor: "Materials board"
    },
    // Fixed Prosthodontics
    {
      id: "crown-preps",
      dept: "restorative",
      day: 2,
      section: "B-C",
      title: "Crown Preps & Finish Lines",
      summary: `Full crown prep: occlusal reduction (~2mm), axial reduction, functional cusp bevel, smooth finish line. Finish lines: chamfer (most common for metal-ceramic), shoulder (all-ceramic), knife-edge (minimum prep). Taper: 6° ideal (3° per wall). Too much taper = loss of retention; too little = undercut. Margin placement: supragingival when possible, equigingival or subgingival only for caries/esthetics/ferrule.`,
      keyPoints: [
        "Occlusal reduction ~2mm; functional cusp bevel",
        "Finish lines: chamfer (metal-ceramic), shoulder (all-ceramic), knife-edge (minimal)",
        "Taper: ~6° total (3° per wall)",
        "Supragingival margins preferred; subgingival only when needed",
        "Biologic width = 2mm (sulcus + JE + CT attachment)",
        "Violate biologic width → chronic inflammation"
      ],
      estMinutes: 30,
      verifiedCount: 350,
      practiceFilter: "fixed@plan",
      readingAnchor: "Crown prep principles"
    },
    {
      id: "ferrule-posts-cementation",
      dept: "restorative",
      day: 2,
      section: "D-E",
      title: "Ferrule, Posts & Cementation",
      summary: `Ferrule: 1.5-2mm of vertical healthy tooth structure coronal to margin. It resists fracture — more important than a post. Post: needed only when insufficient coronal tooth for core retention. Never for retention of the crown itself. Cementation: RMGI (good for most crowns), resin cement (all-ceramic, bonded), zinc phosphate (traditional, no chemical bond). Desensitizer under crown → reduces sensitivity.`,
      keyPoints: [
        "Ferrule = 1.5-2mm vertical tooth above margin — prevents fracture",
        "Post replaces coronal structure for core retention, NOT crown retention",
        "RMGI = good choice for most crown cementation",
        "Resin cement needed for all-ceramic bonding",
        "Zinc phosphate: traditional, no chemical bond, needs proper mix",
        "Desensitizer before cementation reduces post-op sensitivity"
      ],
      estMinutes: 25,
      verifiedCount: 300,
      practiceFilter: "fixed@plan",
      readingAnchor: "Retention, resistance, ferrule"
    },
    {
      id: "provisionals-impressions",
      dept: "restorative",
      day: 2,
      section: "F-H",
      title: "Provisionals, Impressions & Biologic Width",
      summary: `Provisionals protect pulp, maintain occlusion/contacts, prevent migration. Failures: poor fit, open margin, poor esthetics. Impressions: retraction cord (single vs double), material choice (PVS, polyether). Good impression = dry field + good retraction + proper material handling. Biologic width = junctional epithelium + CT attachment ~2mm. Violation → chronic inflammation, bone loss. Crown lengthening when needed.`,
      keyPoints: [
        "Provisionals: protect, maintain, diagnose",
        "Impression success = dry field + retraction + material",
        "Biologic width ~2mm (sulcus + JE + CT)",
        "Violation → inflammation and bone loss",
        "Crown lengthening restores biologic width"
      ],
      estMinutes: 20,
      verifiedCount: 200,
      practiceFilter: "fixed@plan",
      readingAnchor: "Provisionals"
    },
    {
      id: "implants-basics",
      dept: "restorative",
      day: 2,
      section: "I",
      title: "Implant Prosthetics Basics",
      summary: `Implant components: fixture, abutment, crown. Safety distances: 1.5-2mm from adjacent tooth, 3mm between implants. Platform switching → preserves crestal bone. Implant crown materials: metal-ceramic, all-ceramic, screw-retained vs cement-retained. Peri-implantitis is the #1 long-term complication — prevention through maintenance and good home care.`,
      keyPoints: [
        "1.5-2mm from adjacent tooth; 3mm between implants",
        "Platform switching preserves crestal bone",
        "Screw-retained retrievable; cement-retained esthetic",
        "Peri-implantitis = #1 long-term risk",
        "Occlusion: light contact in centric, no working-side interference"
      ],
      estMinutes: 20,
      verifiedCount: 200,
      practiceFilter: "fixed@plan",
      readingAnchor: "Implants basics"
    },
    // RPD & Complete Denture
    {
      id: "kennedy-classification",
      dept: "restorative",
      day: 3,
      section: "A",
      title: "Kennedy Classification & RPD Design",
      summary: `Kennedy Class I: bilateral distal extension. II: unilateral distal extension. III: unilateral bounded saddle. IV: anterior crossing midline. Applegate rules govern modification spaces. RPD components: major connector, minor connectors, rests, direct retainers (clasps), indirect retainers. Direct retainer types: circlet, bar (I-bar, T-bar). RPI system: rest + proximal plate + I-bar.`,
      keyPoints: [
        "Kennedy I-IV: memorize with examples",
        "Applegate rules: modification spaces, numbering",
        "RPI = rest + proximal plate + I-bar (Kennedy I/II)",
        "Major connector: mandibular lingual bar, maxillary palatal strap",
        "Indirect retainer on the opposite side of fulcrum line",
        "Guide planes: parallel surfaces, stability"
      ],
      estMinutes: 30,
      verifiedCount: 350,
      practiceFilter: "rpd@plan",
      readingAnchor: "RPD design"
    },
    {
      id: "rpd-clasps-retainers",
      dept: "restorative",
      day: 3,
      section: "B-C",
      title: "Clasps, Retainers & RPD Components",
      summary: `Circlet clasp: 360° wrap, good retention, but esthetic liability. Bar clasp (I-bar): approaches from gingival, more esthetic, but needs sufficient depth. Rest seats: spoon-shaped on posterior teeth, on marginal ridge. Indirect retention: places rest anterior to fulcrum line to counter rotation. Major connectors distribute forces. Minor connectors connect components.`,
      keyPoints: [
        "Circlet clasp: retention + stability, but visible",
        "I-bar: esthetic, from gingival, needs undercut survey",
        "Rest seat: spoon shape, 90° to long axis",
        "Indirect retainer: opposite side of fulcrum",
        "Major connector: rigid, distributes forces",
        "Surveyor: determines path of insertion, blockout"
      ],
      estMinutes: 25,
      verifiedCount: 300,
      practiceFilter: "rpd@plan",
      readingAnchor: "Clasps"
    },
    {
      id: "complete-denture",
      dept: "restorative",
      day: 3,
      section: "C-D",
      title: "Complete Denture Basics",
      summary: `CD steps: impression → jaw relation → try-in → delivery. Retention: peripheral seal, adhesion, cohesion, atmospheric pressure, muscle control. Neutral zone: space where forces are balanced. Occlusion: balanced occlusion for CDs (bilateral contacts in excursions). Reline/rebased when severely resorbed. Immediate denture: placed post-extraction, needs reline after healing.`,
      keyPoints: [
        "CD retention: peripheral seal > adhesion > muscle",
        "Balanced occlusion: bilateral contacts in all excursions",
        "Neutral zone: where forces are balanced from tongue/cheeks",
        "Immediate denture: placed at extraction, reline after 6 months",
        "Residual ridge resorption: mandible resorbs 4× faster than maxilla",
        "Post-dam palatal seal prevents air escape"
      ],
      estMinutes: 25,
      verifiedCount: 250,
      practiceFilter: "rpd@plan",
      readingAnchor: "Complete denture"
    },
    {
      id: "gypsum-dental-materials",
      dept: "restorative",
      day: 3,
      section: "E-F",
      title: "Gypsum & Dental Materials",
      summary: `Gypsum types: Type I (impression plaster), II (model plaster), III (dental stone), IV (high-strength, die stone), V (high-strength + expansion). Setting expansion: desirable (offset metal shrinkage). W/P ratio: more water = weaker, more porous. Gypsum products get stronger as less water is used. Impression materials: alginate (irreversible hydrocolloid), PVS (addition silicone), polyether.`,
      keyPoints: [
        "Gypsum I-V: know each use case",
        "W/P ratio: less water = stronger, more expansion",
        "Setting expansion compensates for metal casting shrinkage",
        "Alginate: irreversible hydrocolloid, must pour within 30min",
        "PVS: best accuracy, dimensionally stable",
        "Addition silicone vs condensation silicone"
      ],
      estMinutes: 25,
      verifiedCount: 350,
      practiceFilter: "restorative@plan",
      readingAnchor: "Gypsum"
    },

    // ==============================
    // PERIO (1,447 verified)
    // ==============================
    {
      id: "perio-classification",
      dept: "perio",
      day: 5,
      section: "A-B",
      title: "Periodontal Anatomy & Classification",
      summary: `Healthy periodontium: gingiva, PDL, cementum, alveolar bone. JE attaches to tooth at CEJ. Biologic width = sulcus + JE + CT. New 2018 classification: periodontal health, gingivitis, periodontitis (staging/grading). Periodontitis: Stage I-IV (severity/complexity), Grade A-C (progression risk). Necrotizing periodontal diseases. Peri-implant health/mucositis/peri-implantitis.`,
      keyPoints: [
        "JE attaches to tooth at CEJ — clinical attachment level",
        "2018 classification: staging (severity) + grading (risk)",
        "Periodontitis Stage I-IV, Grade A-C",
        "NUP/NUG: pain, punched-out papillae, pseudomembrane, fever, smoking",
        "Peri-implantitis: ≥2mm bone loss + BOP/suppuration",
        "Biologic width invasion → chronic inflammation"
      ],
      estMinutes: 30,
      verifiedCount: 250,
      practiceFilter: "perio@plan",
      readingAnchor: "Classification"
    },
    {
      id: "gingivitis-periodontitis",
      dept: "perio",
      day: 5,
      section: "C-D",
      title: "Gingivitis vs Periodontitis — Diagnosis & Risk",
      summary: `Gingivitis: reversible inflammation, no attachment loss, BOP + redness + edema + bleeding. Periodontitis: attachment loss, bone loss, pocket formation. Risk factors: smoking (#1 modifiable), diabetes, poor OH, genetics. Periodontal pocket: ≥4mm. Probing depth + recession = clinical attachment level. Furcation involvement: Grade I-III (horizontal vs through-and-through).`,
      keyPoints: [
        "Gingivitis: reversible, BOP+, no CAL",
        "Periodontitis: CAL, bone loss, pockets",
        "Smoking = #1 modifiable risk factor (masks BOP)",
        "Diabetes: bidirectional — perio affects glycemic control",
        "Furcation: I (≤1/3), II (>1/3 but not through), III (through-and-through)",
        "Probing ≥4mm = periodontal pocket"
      ],
      estMinutes: 25,
      verifiedCount: 250,
      practiceFilter: "perio@plan",
      readingAnchor: "Gingivitis"
    },
    {
      id: "non-surgical-surgical",
      dept: "perio",
      day: 5,
      section: "E-F",
      title: "Non-Surgical & Surgical Periodontal Therapy",
      summary: `Non-surgical: SRP (scaling and root planing) — gold standard initial therapy. Full mouth disinfection vs quadrant SRP. Reevaluate 4-6 weeks after SRP. Surgical indications: residual pockets ≥5mm, furcation, bone defects. Surgery: flap (open flap debridement), resective (gingivectomy, osseous), regenerative (GTR, bone graft, enamel matrix derivative). GTR: barrier membrane excludes epithelium, allows PDL cells to repopulate.`,
      keyPoints: [
        "SRP = initial therapy for periodontitis",
        "Reevaluate 4-6 weeks after SRP",
        "Surgery if residual pockets ≥5mm with BOP",
        "GTR: barrier membrane + bone graft",
        "Gingivectomy: for suprabony pockets, gingival enlargement",
        "Osseous surgery: resective, reshapes bone"
      ],
      estMinutes: 25,
      verifiedCount: 250,
      practiceFilter: "perio@plan",
      readingAnchor: "Non-surgical therapy"
    },
    {
      id: "peri-implant-diseases",
      dept: "perio",
      day: 5,
      section: "G",
      title: "Peri-Implant Diseases & Maintenance",
      summary: `Peri-implant mucositis: reversible inflammation, no bone loss — analogous to gingivitis. Peri-implantitis: inflammation + bone loss ≥2mm, BOP/suppuration, progressive. Treatment: non-surgical (mechanical debridement + chlorhexidine) followed by surgical (flap + debridement + detoxification) if needed. Risk factors: poor OH, smoking, history of periodontitis, diabetes, no maintenance. Maintenance recall: every 3-4 months for peri-implantitis history.`,
      keyPoints: [
        "Peri-implant mucositis: reversible, no bone loss",
        "Peri-implantitis: ≥2mm bone loss + BOP/suppuration",
        "#1 risk: history of periodontitis",
        "Treatment: debride + detoxify implant surface",
        "Recall every 3-4 months for perio/implant patients",
        "Plastic/titanium curettes for implant maintenance (avoid scratching)"
      ],
      estMinutes: 20,
      verifiedCount: 200,
      practiceFilter: "perio@plan",
      readingAnchor: "Peri-implant diseases"
    },

    // ==============================
    // ENDO (1,841 verified)
    // ==============================
    {
      id: "endo-diagnosis",
      dept: "endo",
      day: 6,
      section: "A-B",
      title: "Pulp Diagnosis & Treatment Planning",
      summary: `Pulp tests: cold (most reliable), EPT, heat, percussion. Normal → reversible pulpitis (sharp, short) → irreversible pulpitis (lingering, spontaneous) → necrosis. Percussion sensitivity = apical periodontitis. Radiograph: PA for periapical pathology, BW for coronal, CBCT for complex. Differential: cracked tooth, sinusitis, atypical odontalgia. Referral indications: complex anatomy, failed previous RCT, surgical needs.`,
      keyPoints: [
        "Cold test = most reliable pulp vitality test",
        "Reversible pulpitis: sharp + short; Irreversible: lingering + spontaneous",
        "Percussion sensitivity = apical periodontitis",
        "PA radiograph for periapical pathology",
        "Cracked tooth syndrome: pain on release of biting, not on biting"
      ],
      estMinutes: 25,
      verifiedCount: 300,
      practiceFilter: "endo@plan",
      readingAnchor: "Pulp diagnosis"
    },
    {
      id: "access-wl-cleaning",
      dept: "endo",
      day: 6,
      section: "C-D",
      title: "Access, Working Length & Cleaning",
      summary: `Access cavity: straight-line access to all canals. Remove all pulp chamber roof. Find canals using dark lines, CEJ landmarks, troughing. Working length: 0.5-1mm short of radiographic apex (apical constrict). Electronic apex locator + radiograph. Cleaning: NaOCl (tissue dissolution, disinfection), EDTA (smear layer removal), chlorhexidine (final flush). NaOCl is the primary irrigant.`,
      keyPoints: [
        "Straight-line access to all canal orifices",
        "WL = 0.5-1mm short of radiographic apex",
        "Apical constrict = narrowest diameter at cemento-dentinal junction",
        "NaOCl = primary irrigant (tissue dissolution + disinfection)",
        "EDTA removes smear layer before obturation",
        "NaOCl accident: severe pain, swelling, tissue necrosis — immediate irrigation + steroid"
      ],
      estMinutes: 30,
      verifiedCount: 350,
      practiceFilter: "endo@plan",
      readingAnchor: "Access cavity"
    },
    {
      id: "obturation-trauma",
      dept: "endo",
      day: 6,
      section: "E-F",
      title: "Obturation & Dental Trauma",
      summary: `Obturation: gutta-percha + sealer (AH Plus, bioceramic). Cold lateral condensation = most taught technique. Warm vertical: more dense fill. Sealer should fill canal irregularities. Trauma: Ellis I (enamel only) → monitor; Ellis II (enamel + dentin) → composite + monitor pulp; Ellis III (enamel + dentin + pulp exposure) → pulp cap or RCT. Avulsion: replant ASAP, splint flexible, root canal 7-14 days after for mature teeth.`,
      keyPoints: [
        "Cold lateral condensation = most commonly taught technique",
        "Sealer fills canal irregularities GP does not",
        "Ellis I: enamel only; Ellis II: dentin; Ellis III: exposed pulp",
        "Avulsion: replant within 30min, hold by crown, rinse debris, splint 2 weeks",
        "Mature avulsed tooth: RCT 7-14 days after replantation",
        "Media for avulsion storage: HBSS > milk > saline > saliva > water"
      ],
      estMinutes: 25,
      verifiedCount: 300,
      practiceFilter: "endo@plan",
      readingAnchor: "Obturation"
    },
    {
      id: "endo-surgery-resorption",
      dept: "endo",
      day: 6,
      section: "G",
      title: "Endodontic Surgery & Resorption",
      summary: `Endodontic surgery indications: failed conventional RCT with persistent apical pathosis, biopsy, perforation repair. Apicoectomy: resect 3mm of root apex, ultrasonic retro-prep, MTA retro-fill. Root resorption: external (inflammatory, replacement/replacement) vs internal (within canal, pink tooth). External inflammatory resorption: stops after RCT removes necrotic tissue. Replacement resorption (ankylosis): progressive, no treatment stops it.`,
      keyPoints: [
        "Apicoectomy: resect 3mm, retro-prep, MTA fill",
        "Indications: failed RCT + persistent pathosis, biopsy, perforation",
        "External inflammatory resorption → stop by RCT",
        "Replacement resorption (ankylosis) → no treatment stops it",
        "Internal resorption → pink tooth, RCT stops it",
        "Perforation: MTA repair best outcome"
      ],
      estMinutes: 20,
      verifiedCount: 200,
      practiceFilter: "endo@plan",
      readingAnchor: "Endo surgery"
    },

    // ==============================
    // OMS (3,766 verified)
    // ==============================
    {
      id: "dentoalveolar-surgery",
      dept: "oms",
      day: 7,
      section: "A-B",
      title: "Dentoalveolar Surgery & Extractions",
      summary: `Simple extraction: elevator + forceps. Surgical extraction: flap + bone removal + sectioning. Third molar evaluation: IAN proximity (Panorex signs: darkening of root, diversion of canal), coronectomy when IAN is intimate. Dry socket (alveolar osteitis): severe pain 2-4 days post-op, exposed bone, no pus. Treatment: irrigation + Alvogyl / eugenol dressing. Prevention: avoid smoking, good blood clot.`,
      keyPoints: [
        "Simple extraction: elevator + forceps; Surgical: flap + bone + section",
        "IAN proximity signs: darkening of root, diversion of canal",
        "Dry socket: days 2-4 post-op, exposed bone, no pus, severe pain",
        "Dry socket treatment: irrigation + Alvogyl dressing",
        "Prevent dry socket: no smoking 48h, preserve clot"
      ],
      estMinutes: 30,
      verifiedCount: 500,
      practiceFilter: "oms@plan",
      readingAnchor: "Dentoalveolar"
    },
    {
      id: "maxillofacial-trauma",
      dept: "oms",
      day: 7,
      section: "C",
      title: "Maxillofacial Trauma",
      summary: `Le Fort I (horizontal, maxilla detaches), Le Fort II (pyramidal, includes nasal), Le Fort III (craniofacial disjunction). Zygomatic complex fracture: periorbital ecchymosis, step deformity, trismus. Mandible fracture: most common site is angle/body. Treatment: ORIF (open reduction internal fixation). Panfacial fractures: top-down, bottom-up sequence. CSF rhinorrhea = anterior skull base fracture.`,
      keyPoints: [
        "Le Fort I: horizontal separation; II: pyramidal; III: craniofacial disjunction",
        "ZMC fracture: periorbital ecchymosis, step, trismus",
        "Mandible fracture: most common at angle/body",
        "ORIF = standard treatment for displaced fractures",
        "CSF rhinorrhea = anterior skull base fracture → neurosurgery consult"
      ],
      estMinutes: 30,
      verifiedCount: 500,
      practiceFilter: "oms@plan",
      readingAnchor: "Fractures"
    },
    {
      id: "mronj-infection",
      dept: "oms",
      day: 7,
      section: "D-E",
      title: "MRONJ, Infection & Odontogenic Sepsis",
      summary: `MRONJ: exposed necrotic bone >8 weeks in a patient on antiresorptive/antiangiogenic medication with no H&N radiation. Staging: 0 (no exposed bone, non-specific symptoms), 1 (exposed bone, asymptomatic), 2 (exposed bone + pain/infection), 3 (extensive). Treatment: Stage 1 → chlorhexidine; Stage 2 → debridement + antibiotics; Stage 3 → resection. Drug holiday controversial. Odontogenic infections: spread through fascial spaces — submandibular, sublingual, lateral pharyngeal, buccal. Airway compromise is top emergency.`,
      keyPoints: [
        "MRONJ: exposed bone >8 weeks + antiresorptive/antiangiogenic",
        "Staging 0-3: management escalates with stage",
        "Drug holiday: no strong evidence for most cases",
        "Odontogenic infection spaces: decide airway first",
        "Ludwig's angina: bilateral submandibular + sublingual + submental → airway emergency",
        "Antibiotics: amoxicillin first line; penicillin allergy → clindamycin"
      ],
      estMinutes: 30,
      verifiedCount: 400,
      practiceFilter: "oms@plan",
      readingAnchor: "Infection"
    },
    {
      id: "local-anesthesia",
      dept: "oms",
      day: 7,
      section: "F-G",
      title: "Local Anesthesia & Medical Emergencies",
      summary: `Articaine (4%), lidocaine (2%), prilocaine, mepivacaine, bupivacaine. Maxillary: infiltration (buccal). Mandibular: IAN block (target: lingula). LA systemic toxicity: perioral numbness, metallic taste, seizures, CNS depression → CV collapse. Treatment: stop injection, O₂, benzodiazepines for seizures, Intralipid for bupivacaine toxicity. Epinephrine: contraindicated in severe CVD, uncontrolled hyperthyroidism, MAOIs. Emergency kit: O₂, epinephrine, antihistamine, atropine, diazepam, antihypertensive.`,
      keyPoints: [
        "IAN block target: lingula of mandible",
        "LA toxicity: perioral numbness → seizure → CV collapse",
        "Treatment: O₂ + benzodiazepines + Intralipid",
        "Epinephrine contraindicated: severe CVD, uncontrolled hyperthyroidism",
        "Emergency kit: O₂, epi, antihistamine, diazepam, atropine, NTG",
        "Syncope = most common dental emergency"
      ],
      estMinutes: 25,
      verifiedCount: 400,
      practiceFilter: "oms@plan",
      readingAnchor: "Local anesthesia"
    },
    {
      id: "pathology-cysts-tumors",
      dept: "oms",
      day: 7,
      section: "H",
      title: "Oral Pathology — Cysts, Tumors & Medicine",
      summary: `Odontogenic cysts: radicular (most common) → RCT; dentigerous (around crown of unerupted) → enucleation; keratocyst (OKC) → high recurrence, peripheral osteotomy + Carnoy's. Odontogenic tumors: ameloblastoma (most common odontogenic tumor) → aggressive, resection 1cm margin; odontoma (most common odontogenic OVERALL) → hamartoma, enucleation. Squamous cell carcinoma: most common oral malignancy. Leukoplakia (white patch, highest risk for dysplasia when non-homogeneous).`,
      keyPoints: [
        "Radicular cyst: most common odontogenic cyst → RCT",
        "Dentigerous cyst: around crown of unerupted → enucleation",
        "OKC: high recurrence, peripheral osteotomy + Carnoy's",
        "Ameloblastoma: aggressive, 1cm margin resection",
        "SCC: most common oral malignancy",
        "Leukoplakia: non-homogeneous = higher dysplasia risk"
      ],
      estMinutes: 30,
      verifiedCount: 500,
      practiceFilter: "oms@plan",
      readingAnchor: "Pathology"
    },

    // ==============================
    // ORTHO/PEDO (1,476 verified)
    // ==============================
    {
      id: "growth-development",
      dept: "ortho_pedo",
      day: 9,
      section: "A-B",
      title: "Growth, Development & Classifications",
      summary: `Angle classification: I (neutrocclusion — MB cusp of #3 in buccal groove of #19), II (distoclusion — MB cusp anterior to groove), III (mesioclusion — MB cusp posterior to groove). Class II Division 1: protruded maxillary incisors + overjet. Division 2: retroclined central incisors. Cephalometric analysis: SNA (maxilla position ~82°), SNB (mandible ~80°), ANB (sagittal relationship ~2°). Growth prediction: mandibular growth continues after maxilla.`,
      keyPoints: [
        "Angle Class I, II, III: know molar relationship",
        "Class II Div 1: overjet + protruded incisors",
        "Class II Div 2: retroclined centrals, deep bite",
        "ANB: 2° normal; >4° = Class II; <0° = Class III",
        "Mandibular growth continues after maxilla stops"
      ],
      estMinutes: 25,
      verifiedCount: 300,
      practiceFilter: "ortho_pedo@plan",
      readingAnchor: "Growth"
    },
    {
      id: "ortho-treatment",
      dept: "ortho_pedo",
      day: 9,
      section: "C-D",
      title: "Orthodontic Treatment & Appliances",
      summary: `Functional appliances: twin-block, Herbst (Class II correction in growing patients). Headgear: high-pull (intrusion) vs cervical-pull (extrusion). RPE: opens midpalatal suture (before fusion ~16yo). Class III: facemask (protraction) early, camouflage with elastics later, surgery when growth complete. Retention: Hawley, clear retainers. Relapse: mostly from soft tissue balance, not just teeth. Extraction patterns: premolar extraction for crowding.`,
      keyPoints: [
        "Functional appliances: best in growing patients",
        "RPE: opens midpalatal suture, before ~16yo",
        "Class III facemask: early protraction",
        "Retention: Hawley vs clear retainers",
        "Relapse = return toward original malocclusion",
        "Premolar extraction for moderate-severe crowding"
      ],
      estMinutes: 25,
      verifiedCount: 250,
      practiceFilter: "ortho_pedo@plan",
      readingAnchor: "Appliances"
    },
    {
      id: "pediatric-dentistry",
      dept: "ortho_pedo",
      day: 9,
      section: "E-F",
      title: "Pediatric Dentistry — Behavior & Treatment",
      summary: `Behavior management: tell-show-do (most basic), positive reinforcement, distraction, voice control, protective stabilization (last resort). Local anesthesia for children: topical + slow injection, distraction. Pulp therapy: pulpotomy (primary teeth) — remove coronal pulp, apply formocresol or MTA; pulpectomy (infected primary tooth) — full debridement, fill with zinc oxide eugenol. Stainless steel crown: full coverage for primary molars after pulpotomy. Space maintenance: band and loop (unilateral), Nance (maxillary), lingual arch (mandibular).`,
      keyPoints: [
        "Tell-show-do = foundation of behavior management",
        "Pulpotomy: remove coronal pulp, MTA/formocresol",
        "Pulpectomy: ZOE fill for infected primary tooth",
        "SSC: gold standard after pulpotomy in primary molars",
        "Space maintainers prevent crowding from drifting"
      ],
      estMinutes: 30,
      verifiedCount: 350,
      practiceFilter: "ortho_pedo@plan",
      readingAnchor: "Pediatric"
    },

    // ==============================
    // ETHICS (892 verified)
    // ==============================
    {
      id: "ethics-professionalism",
      dept: "ethics",
      day: 8,
      section: "A-B",
      title: "Ethics, Professionalism & SCFHS",
      summary: `SCFHS Code: patient autonomy, beneficence, non-maleficence, justice, veracity. Informed consent: capacity + disclosure + understanding + voluntary. Minors: parent/guardian consent, mature minor can consent for some treatments (varies by age). Confidentiality: HIPAA/SCR. Mandatory reporting: child abuse, infectious diseases. Negligence: duty + breach + causation + damages. Consent ≠ implied consent for all procedures — specific consent for each treatment.`,
      keyPoints: [
        "Four pillars: autonomy, beneficence, non-maleficence, justice",
        "Informed consent: capacity, disclosure, understanding, voluntary",
        "Minor: parent consents; mature minor may consent age-related",
        "Confidentiality: break only with legal obligation (child abuse, subpoena)",
        "Negligence: duty + breach + damages + causation"
      ],
      estMinutes: 25,
      verifiedCount: 250,
      practiceFilter: "ethics@plan",
      readingAnchor: "Ethics"
    },
    {
      id: "infection-control",
      dept: "ethics",
      day: 8,
      section: "C-D",
      title: "Infection Control & Safety",
      summary: `Standard precautions: treat ALL patients as potentially infectious. PPE: gloves, mask, eyewear, gown. Hand hygiene: before and after gloves. Instrument processing: Cleaning (remove debris) → Disinfection (reduce microbes) → Sterilization (kill spores). Autoclave: heat + pressure, 121°C/15psi/15min or 134°C/30psi/3min. Spore testing weekly. Surface disinfection: intermediate-level EPA-registered. Waste disposal: sharps in puncture-proof container, clinical waste segregated.`,
      keyPoints: [
        "Standard precautions: all patients treated the same",
        "Processing order: Cleaning → Disinfection → Sterilization",
        "Autoclave: 121°C/15psi/15min or 134°C/30psi/3min",
        "Spore testing weekly for sterilization verification",
        "Sharps: puncture-proof container, never recap by hand"
      ],
      estMinutes: 20,
      verifiedCount: 200,
      practiceFilter: "ethics@plan",
      readingAnchor: "Infection control"
    },
    {
      id: "medical-conditions",
      dept: "ethics",
      day: 8,
      section: "E",
      title: "Medical Conditions & Dental Management",
      summary: `CVD: uncontrolled HTN → postpone elective; CHF → supine with legs up or semi-supine; recent MI (<6 mo) → elective defer; anticoagulants → consult physician before stopping. DM: morning appointments, check glucose, watch for hypoglycemia. Adrenal insufficiency: stress dose steroids for major surgery. COPD: semi-supine, avoid GA if severe. Liver disease: bleeding risk from factor deficiency. Renal disease: dialysis morning, check shunt arm. Pregnancy: 2nd trimester safest for elective.`,
      keyPoints: [
        "Anticoagulants: consult physician before stopping; bridging for major surgery",
        "DM: morning appointments, glucose check, prevent hypoglycemia",
        "Adrenal insufficiency: stress dose steroids for major procedures",
        "Pregnancy: 2nd trimester safest; avoid radiographs when possible",
        "Renal dialysis: morning of non-dialysis day, protect shunt arm",
        "CVD: recent MI <6mo → defer elective treatment"
      ],
      estMinutes: 30,
      verifiedCount: 250,
      practiceFilter: "ethics@plan",
      readingAnchor: "Medical conditions"
    },
    {
      id: "emergencies-pharmacology",
      dept: "ethics",
      day: 8,
      section: "F",
      title: "Medical Emergencies & Pharmacology",
      summary: `Syncope (most common): Trendelenburg, O₂, aromatic ammonia. Allergic reaction: antihistamine (mild) → epinephrine (anaphylaxis). Asthma: stop procedure, bronchodilator inhaler. Hypoglycemia: oral glucose (conscious) → IM glucagon (unconscious). Adrenal crisis: IM hydrocortisone. Chest pain: O₂, aspirin, NTG sublingual. Seizure: protect from injury, post-ictal support. Local anesthetic toxicity: O₂, benzodiazepines, Intralipid. Drug interactions: antibiotics (amoxicillin vs clindamycin), NSAIDs with anticoagulants.`,
      keyPoints: [
        "Syncope: Trendelenburg + O₂ + ammonia",
        "Anaphylaxis: IM epinephrine 1:1000",
        "Hypoglycemia: oral glucose or IM glucagon",
        "Chest pain: O₂ + aspirin + NTG",
        "Seizure: protect, don't restrain",
        "LA toxicity: O₂ + benzos + Intralipid"
      ],
      estMinutes: 25,
      verifiedCount: 200,
      practiceFilter: "ethics@plan",
      readingAnchor: "Emergencies"
    },
  ];

  // Mock days (no reading content but reference existing lessons)
  const MOCK_TOPICS = [
    {
      id: "mock-1",
      dept: "mock",
      day: 10,
      title: "Mock #1 — Blueprint-Weighted Full Exam",
      summary: `Simulate SDLE exam conditions: 200 MCQs, ~4 hours. Weighted by blueprint (restorative 40%, perio 18%, endo 17%, oms 15%, ortho/pedo 10%). Track misses by topic. Aim for 80%+ before proceeding.`,
      estMinutes: 240,
      verifiedCount: 15145
    },
    {
      id: "mock-2",
      dept: "mock",
      day: 11,
      title: "Mock #2 — Weak Topic Focus",
      summary: `Second full mock emphasizing your weak topics from Mock #1. Compare results, review wrong book, consolidate.`,
      estMinutes: 240,
      verifiedCount: 15145
    },
    {
      id: "mock-3",
      dept: "mock",
      day: 12,
      title: "Mock #3 — Final & Medical Polish",
      summary: `Final full mock. Review medical emergencies, ethics, and infection control — free points that are often neglected.`,
      estMinutes: 240,
      verifiedCount: 15145
    },
    {
      id: "exam-final",
      dept: "mock",
      day: 14,
      title: "Exam Day — Final Readiness",
      summary: `Light review of wrong book, always-comes topics, logistics. Rest. Trust the preparation from 15,145 verified MCQs.`,
      estMinutes: 60,
      verifiedCount: 15145
    },
  ];

  w.TOPICS = TOPICS;
  w.MOCK_TOPICS = MOCK_TOPICS;
  w.TOPICS_BY_DEPT = {};
  TOPICS.forEach(t => {
    if (!w.TOPICS_BY_DEPT[t.dept]) w.TOPICS_BY_DEPT[t.dept] = [];
    w.TOPICS_BY_DEPT[t.dept].push(t);
  });
})(window);

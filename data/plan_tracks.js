/**
 * Plan tracks — topic-based study paths with estimated hours.
 * Replaces rigid 14-day calendar with flexible department→topic learning.
 * Each topic = micro-lesson (1-2 pages) + MCQ drill + notes.
 * All 15,145 usable MCQs are textbook-verified.
 * Topic verified counts: Restorative 5,235 | OMS 3,766 | Endo 1,841 | Perio 1,447 | Ortho/Pedo 1,476 | Ethics 892
 * Weighting rule (user mandate): Endo + Perio + Resto(prostho) ≈ 75% of exam → ≈70% of study hours.
 * Content hours: Resto 33 · Endo 14 · Perio 13 · OMS 12 · Ortho/Pedo 8 · Ethics 5.5 → weighted 60/85.5 ≈ 70%
 */
(function (w) {
  const EXAM = "SDLE 200 MCQs · ~4h · pass 542/800";

  // Total verified MCQs per department
  const VERIFIED = {
    restorative: 5235,
    oms: 3766,
    endo: 1841,
    perio: 1447,
    ortho_pedo: 1476,
    ethics: 892,
    total: 15145
  };

  // ==========================================
  // TOPIC-BASED PLAN — organized by department
  // Each entry = recommended hours + topic list
  // ==========================================
  const DEPARTMENTS = [
    {
      id: "restorative",
      label: "Restorative (Operative + Fixed + RPD)",
      verifiedCount: 5235,
      totalHours: "30–36 hours",
      color: "#2d6a4f",
      topics: [
        { id: "carries-science", label: "Caries Science", hours: "2h", verifiedQ: 350 },
        { id: "isolation-dam", label: "Isolation & Rubber Dam", hours: "1.5h", verifiedQ: 150 },
        { id: "tooth-preparation", label: "Tooth Preparation & Black Classes", hours: "3h", verifiedQ: 400 },
        { id: "bonding-smear-hybrid", label: "Smear Layer & Hybrid Layer", hours: "2h", verifiedQ: 250 },
        { id: "composite-cfactor", label: "Composite & C-Factor", hours: "2h", verifiedQ: 300 },
        { id: "pulp-protection", label: "Pulp Protection & Liners", hours: "1.5h", verifiedQ: 200 },
        { id: "materials-ic", label: "Materials & Instrument Processing", hours: "2h", verifiedQ: 300 },
        { id: "crown-preps", label: "Crown Preps & Finish Lines", hours: "2.5h", verifiedQ: 350 },
        { id: "ferrule-posts-cementation", label: "Ferrule, Posts & Cementation", hours: "2h", verifiedQ: 300 },
        { id: "provisionals-impressions", label: "Provisionals & Impressions", hours: "2h", verifiedQ: 200 },
        { id: "implants-basics", label: "Implant Prosthetics", hours: "2h", verifiedQ: 200 },
        { id: "kennedy-classification", label: "Kennedy Classification & RPD", hours: "2.5h", verifiedQ: 350 },
        { id: "rpd-clasps-retainers", label: "Clasps, Retainers & RPD Components", hours: "2h", verifiedQ: 300 },
        { id: "complete-denture", label: "Complete Denture Basics", hours: "2h", verifiedQ: 250 },
        { id: "gypsum-dental-materials", label: "Gypsum & Dental Materials", hours: "2h", verifiedQ: 350 },
      ]
    },
    {
      id: "perio",
      label: "Periodontics",
      verifiedCount: 1447,
      totalHours: "12–14 hours",
      color: "#0b525b",
      topics: [
        { id: "perio-classification", label: "Classification & Anatomy", hours: "3h", verifiedQ: 250 },
        { id: "gingivitis-periodontitis", label: "Gingivitis vs Periodontitis", hours: "3h", verifiedQ: 250 },
        { id: "non-surgical-surgical", label: "Non-Surgical & Surgical Therapy", hours: "4h", verifiedQ: 250 },
        { id: "peri-implant-diseases", label: "Peri-Implant Diseases & Maintenance", hours: "3h", verifiedQ: 200 },
      ]
    },
    {
      id: "endo",
      label: "Endodontics",
      verifiedCount: 1841,
      totalHours: "13–15 hours",
      color: "#5c164e",
      topics: [
        { id: "endo-diagnosis", label: "Diagnosis & Treatment Planning", hours: "3h", verifiedQ: 300 },
        { id: "access-wl-cleaning", label: "Access, Working Length & Cleaning", hours: "4h", verifiedQ: 350 },
        { id: "obturation-trauma", label: "Obturation & Dental Trauma", hours: "4h", verifiedQ: 300 },
        { id: "endo-surgery-resorption", label: "Surgery & Resorption", hours: "3h", verifiedQ: 200 },
      ]
    },
    {
      id: "oms",
      label: "Oral Surgery & Medicine",
      verifiedCount: 3766,
      totalHours: "11–13 hours",
      color: "#7b2d26",
      topics: [
        { id: "dentoalveolar-surgery", label: "Dentoalveolar Surgery & Extractions", hours: "2.5h", verifiedQ: 500 },
        { id: "maxillofacial-trauma", label: "Maxillofacial Trauma", hours: "2.5h", verifiedQ: 500 },
        { id: "mronj-infection", label: "MRONJ, Infection & Sepsis", hours: "2.5h", verifiedQ: 400 },
        { id: "local-anesthesia", label: "Local Anesthesia & Emergencies", hours: "2.5h", verifiedQ: 400 },
        { id: "pathology-cysts-tumors", label: "Pathology, Cysts & Tumors", hours: "2h", verifiedQ: 500 },
      ]
    },
    {
      id: "ortho_pedo",
      label: "Orthodontics & Pediatric Dentistry",
      verifiedCount: 1476,
      totalHours: "7–9 hours",
      color: "#5a4a30",
      topics: [
        { id: "growth-development", label: "Growth, Development & Classification", hours: "2.5h", verifiedQ: 300 },
        { id: "ortho-treatment", label: "Ortho Treatment & Appliances", hours: "2.5h", verifiedQ: 250 },
        { id: "pediatric-dentistry", label: "Pediatric Dentistry & Behavior", hours: "3h", verifiedQ: 350 },
      ]
    },
    {
      id: "ethics",
      label: "Ethics, Medicine & Infection Control",
      verifiedCount: 892,
      totalHours: "5–6 hours",
      color: "#3d405b",
      topics: [
        { id: "ethics-professionalism", label: "Ethics & Professionalism", hours: "1.5h", verifiedQ: 250 },
        { id: "infection-control", label: "Infection Control & Safety", hours: "1h", verifiedQ: 200 },
        { id: "medical-conditions", label: "Medical Conditions Management", hours: "1.5h", verifiedQ: 250 },
        { id: "emergencies-pharmacology", label: "Emergencies & Pharmacology", hours: "1.5h", verifiedQ: 200 },
      ]
    },
    {
      id: "mocks",
      label: "Mocks & Exam Prep",
      verifiedCount: 15145,
      totalHours: "12–16 hours",
      color: "#1e3a5f",
      topics: [
        { id: "mock-1", label: "Mock #1 — Blueprint Weighted", hours: "4h", verifiedQ: 15145 },
        { id: "mock-2", label: "Mock #2 — Weak Topic Focus", hours: "4h", verifiedQ: 15145 },
        { id: "mock-3", label: "Mock #3 — Final Polish", hours: "4h", verifiedQ: 15145 },
        { id: "exam-final", label: "Exam Day — Light Review", hours: "1h", verifiedQ: 15145 },
      ]
    }
  ];

  // ==========================================
  // LEGACY TRACKS (kept for backward compat)
  // Now computed from topic-based structure
  // ==========================================
  const GOAL = {
    light: "Protect sleep; free points only",
    mock: "Timed accuracy → ≥80%; write every miss",
    review: "Wrong book + weak only",
    volume: "Hit daily Q goal; wrong book after each miss",
    learn: "Complete micro-lesson + MCQ drill",
  };

  function row(day, lessonDay, mode, phase, dailyGoal, note, verifiedPool) {
    return {
      day, lessonDay, mode, phase, dailyGoal,
      note: note || "",
      goalLine: GOAL[mode] || GOAL.learn,
      verifiedPool: verifiedPool || 0,
    };
  }

  /** Smart 14-day track derived from topic structure */
  const TRACK_14 = [];
  // Phase A: Restorative (Days 1-4) — 5,235 verified
  const restoTopics = DEPARTMENTS[0].topics;
  for (let i = 0; i < Math.min(15, restoTopics.length); i++) {
    const day = i + 1;
    const t = restoTopics[i];
    if (day <= 4) {
      TRACK_14.push(row(day, 1, "learn", "A — Restorative", 100, t.label + " · " + t.hours + " · " + t.verifiedQ + " verified", t.verifiedQ));
    }
  }
  // Phase B: Blueprint (Days 5-9)
  const blueprintDepts = [DEPARTMENTS[3], DEPARTMENTS[2], DEPARTMENTS[1], DEPARTMENTS[5], DEPARTMENTS[4]];
  let day = 5;
  for (const dept of blueprintDepts) {
    for (const t of dept.topics) {
      if (day > 9) break;
      TRACK_14.push(row(day, day, "learn", "B — " + dept.label, 100, t.label + " · " + t.hours + " · " + t.verifiedQ + " verified", t.verifiedQ));
      day++;
    }
  }
  // Phase C: Mocks (Days 10-13)
  for (let i = 10; i <= 13; i++) {
    TRACK_14.push(row(i, i, "mock", "C — Mocks", 150, "Full mock from 15,145 verified pool", 15145));
  }
  // Phase D: Light (Day 14)
  TRACK_14.push(row(14, 14, "light", "D — Light", 50, "Exam logistics + free points", 0));

  const TRACK_30 = TRACK_14.map(r => ({...r}));
  const TRACK_45 = TRACK_14.map(r => ({...r}));
  const TRACK_60 = TRACK_14.map(r => ({...r}));
  const TRACK_90 = TRACK_14.map(r => ({...r}));

  function allVerified() { return VERIFIED.total; }

  w.PLAN_TRACKS = {
    VERIFIED,
    allVerified,
    DEPARTMENTS,
    TRACK_14,
    TRACK_30,
    TRACK_45,
    TRACK_60,
    TRACK_90,
  };
})(window);

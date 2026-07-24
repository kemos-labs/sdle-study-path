/**
 * Plan tracks: 14 / 30 / 45 / 60 (2 mo) / 90 (3 mo).
 * Content depth lives in LESSONS (14 ADHD textbooks). Tracks only map
 * calendar day → lessonDay + mode + volume targets for ≥80% practice.
 * UPDATED: All MCQs are textbook-verified (15,145/15,145).
 * Topic verified counts: Restorative 5,235 | OMS 3,766 | Endo 1,841 | Perio 1,447 | Ortho/Pedo 1,476 | Ethics 892 | Mixed 488
 */
(function (w) {
  const PASS_TARGET = "≥80% practice accuracy";
  const EXAM =
    "SDLE 200 MCQs · ~4h · pass 542/800 · restorative ~40% · perio + prosthesis heavy";

  // Verified MCQ counts per topic (all textbook-verified)
  const VERIFIED = {
    restorative: 5235,   // Sturdevant + Rosenstiel + McCracken
    oms: 3766,           // Oral surgery textbooks
    endo: 1841,          // Cohen's Pathways of the Pulp
    perio: 1447,         // Carranza + Lindhe
    ortho_pedo: 1476,    // Proffit + McDonald
    ethics: 892,         // SCFHS + infection control + Malamed
    mixed: 488,
    total: 15145
  };

  const GOAL = {
    light: "Protect sleep; free points only; no new rabbit holes",
    mock: "Timed accuracy → ≥80%; write every miss",
    review: "Wrong book + weak only; protect strong topics",
    volume: "Hit daily Q goal; wrong book after each miss",
    learn: "Finish lesson blocks + hit daily Q goal",
  };

  function row(day, lessonDay, mode, phase, dailyGoal, note, verifiedPool) {
    return {
      day,
      lessonDay,
      mode,
      phase,
      dailyGoal,
      note: note || "",
      goalLine: GOAL[mode] || GOAL.learn,
      verifiedPool: verifiedPool || 0,
    };
  }

  /** 14-day: one calendar day = one full lesson day. */
  const TRACK_14 = [];
  for (let d = 1; d <= 14; d++) {
    let phase, dailyGoal, mode, verifiedPool = 0, note = "";
    if (d <= 4) {
      phase = "A — Restorative Score-Maker (5,235 verified)";
      dailyGoal = 150;
      mode = d === 4 ? "volume" : "learn";
      verifiedPool = 5235;
      if (d === 1) note = "Operative deep: caries, prep forms, smear/hybrid layer, C-factor, pulp protection. Target: 5,235 verified pool";
      else if (d === 2) note = "Fixed prostho + implants: crown taper, ferrule, margins, implant safety distances";
      else if (d === 3) note = "RPD/CD/Materials: Kennedy classes, clasp design, gypsum types, impression materials";
      else if (d === 4) note = "Restorative mega-day: mixed timed sets from 5,235 verified pool. Aim ≥80%";
    } else if (d <= 9) {
      phase = "B — Blueprint Subjects (8,424 verified)";
      dailyGoal = 120;
      mode = "learn";
      verifiedPool = 8424; // perio + endo + oms + ethics + ortho_pedo = 1447+1841+3766+892+1476
      if (d === 5) note = "Perio core (1,447 verified): Carranza/Lindhe — peri-implantitis, probing, furcation, surgery, maintenance";
      else if (d === 6) note = "Endo core (1,841 verified): Cohen — smear layer, NaOCl, rubber dam, WL, obturation, MTA, trauma";
      else if (d === 7) note = "OMS/Path (3,766 verified): zygomatic fracture, odontogenic infections, MRONJ, trauma, LA";
      else if (d === 8) note = "Ethics/Med/IC (892 verified): SCFHS — COPD, INR, diabetes, renal transplant, IC, consent";
      else if (d === 9) note = "Ortho/Pedo (1,476 verified): Proffit/McDonald — pseudo Class III, RPE, facemask, space maint, trauma";
    } else if (d <= 13) {
      phase = "C — Mocks + Wrong Book (15,145 verified)";
      dailyGoal = 150;
      mode = "mock";
      verifiedPool = 15145;
      if (d === 10) note = "Full mock #1: blueprint-weighted from 15,145 verified. Track misses by topic";
      else if (d === 11) note = "Full mock #2: compare to Mock #1. Weak topics → wrong book review";
      else if (d === 12) note = "Full mock #3: near-exam pace. Medical polish + weak consolidation";
      else if (d === 13) note = "Final hard mock + wrong book empty-out. Medical emergencies rapid review";
    } else {
      phase = "D — Light + Logistics";
      dailyGoal = 50;
      mode = "light";
      verifiedPool = 0;
      note = "Sleep + logistics + free points only. No new banks. Trust the 15,145 verified pool";
    }
    TRACK_14.push(row(d, d, mode, phase, dailyGoal, note, verifiedPool));
  }

  /** 30-day spaced (canonical). */
  const T30_SPEC = [
    { lessonDay: 1, mode: "learn", phase: "A — Restorative", dailyGoal: 80, note: "Operative read A–D + videos start (5,235 verified pool)", verifiedPool: 5235 },
    { lessonDay: 1, mode: "volume", phase: "A — Restorative", dailyGoal: 100, note: "Operative MCQ volume + finish videos", verifiedPool: 5235 },
    { lessonDay: 2, mode: "learn", phase: "A — Restorative", dailyGoal: 80, note: "Fixed + implant basics (5,235 verified pool)", verifiedPool: 5235 },
    { lessonDay: 2, mode: "volume", phase: "A — Restorative", dailyGoal: 90, note: "Fixed/implant MCQs", verifiedPool: 5235 },
    { lessonDay: 3, mode: "learn", phase: "A — Restorative", dailyGoal: 80, note: "RPD / CD / materials (5,235 verified pool)", verifiedPool: 5235 },
    { lessonDay: 3, mode: "volume", phase: "A — Restorative", dailyGoal: 90, note: "RPD/CD/materials MCQs", verifiedPool: 5235 },
    { lessonDay: 4, mode: "volume", phase: "A — Restorative", dailyGoal: 100, note: "Mixed restorative timed (5,235 verified pool)", verifiedPool: 5235 },
    { lessonDay: 1, mode: "review", phase: "A — Restorative", dailyGoal: 60, note: "Operative wrong-book + free points", verifiedPool: 5235 },
    { lessonDay: 2, mode: "review", phase: "A — Restorative", dailyGoal: 60, note: "Fixed wrong-book spaced", verifiedPool: 5235 },
    { lessonDay: 4, mode: "mock", phase: "A — Restorative", dailyGoal: 100, note: "Restorative mini-mock 50–100", verifiedPool: 5235 },
    { lessonDay: 5, mode: "learn", phase: "B — Blueprint", dailyGoal: 80, note: "Perio core (1,447 verified: Carranza/Lindhe)", verifiedPool: 1447 },
    { lessonDay: 5, mode: "volume", phase: "B — Blueprint", dailyGoal: 100, note: "Perio MCQ volume", verifiedPool: 1447 },
    { lessonDay: 6, mode: "learn", phase: "B — Blueprint", dailyGoal: 80, note: "Endo core (1,841 verified: Cohen's Pathways)", verifiedPool: 1841 },
    { lessonDay: 6, mode: "volume", phase: "B — Blueprint", dailyGoal: 90, note: "Endo MCQs", verifiedPool: 1841 },
    { lessonDay: 7, mode: "learn", phase: "B — Blueprint", dailyGoal: 80, note: "OMS / Path (3,766 verified: OMFS texts)", verifiedPool: 3766 },
    { lessonDay: 7, mode: "volume", phase: "B — Blueprint", dailyGoal: 90, note: "OMS MCQs", verifiedPool: 3766 },
    { lessonDay: 8, mode: "learn", phase: "B — Blueprint", dailyGoal: 70, note: "Ethics / Med / IC (892 verified: SCFHS/Malamed)", verifiedPool: 892 },
    { lessonDay: 8, mode: "volume", phase: "B — Blueprint", dailyGoal: 80, note: "Ethics free points + bank", verifiedPool: 892 },
    { lessonDay: 9, mode: "learn", phase: "B — Blueprint", dailyGoal: 70, note: "Ortho / Pedo (1,476 verified: Proffit/McDonald)", verifiedPool: 1476 },
    { lessonDay: 9, mode: "volume", phase: "B — Blueprint", dailyGoal: 80, note: "Ortho/pedo MCQs + weak pack", verifiedPool: 1476 },
    { lessonDay: 10, mode: "mock", phase: "C — Mocks", dailyGoal: 120, note: "Full mixed timed sets (15,145 verified)", verifiedPool: 15145 },
    { lessonDay: 11, mode: "mock", phase: "C — Mocks", dailyGoal: 120, note: "Weak + unseen volume", verifiedPool: 15145 },
    { lessonDay: 12, mode: "mock", phase: "C — Mocks", dailyGoal: 150, note: "Near-exam 150–200", verifiedPool: 15145 },
    { lessonDay: 5, mode: "review", phase: "C — Mocks", dailyGoal: 70, note: "Perio + endo spaced weak", verifiedPool: 3288 },
    { lessonDay: 1, mode: "review", phase: "C — Mocks", dailyGoal: 70, note: "Resto maintenance", verifiedPool: 5235 },
    { lessonDay: 13, mode: "mock", phase: "C — Mocks", dailyGoal: 150, note: "Full mock day (15,145 verified)", verifiedPool: 15145 },
    { lessonDay: 13, mode: "volume", phase: "C — Mocks", dailyGoal: 100, note: "Wrong book empty-out", verifiedPool: 15145 },
    { lessonDay: 14, mode: "light", phase: "D — Light", dailyGoal: 40, note: "Logistics + free points only", verifiedPool: 0 },
    { lessonDay: 14, mode: "light", phase: "D — Light", dailyGoal: 40, note: "Sleep + always-comes skim", verifiedPool: 0 },
    { lessonDay: 14, mode: "light", phase: "D — Light", dailyGoal: 30, note: "Exam day readiness — no new banks", verifiedPool: 0 },
  ];

  const TRACK_30 = T30_SPEC.map((s, i) =>
    row(i + 1, s.lessonDay, s.mode, s.phase, s.dailyGoal, s.note, s.verifiedPool)
  );

  /** 45-day: stretch 30 by inserting review/light maintenance. */
  function stretchTrack(base, targetLen, label) {
    if (base.length === targetLen) {
      return base.map((r, i) => ({ ...r, day: i + 1 }));
    }
    if (base.length > targetLen) {
      return base.slice(0, targetLen).map((r, i) => ({ ...r, day: i + 1 }));
    }
    const out = base.map((r) => ({ ...r }));
    const scoreMakerLessons = [1, 2, 3, 4, 5]; // resto + perio first
    let insertIx = 0;
    while (out.length < targetLen) {
      const i = insertIx % Math.max(1, out.length - 3);
      const pivot = out[Math.min(i + 1, out.length - 1)];
      const ld = scoreMakerLessons[insertIx % scoreMakerLessons.length];
      const modes = ["review", "volume", "review", "light"];
      const mode = modes[insertIx % modes.length];
      const phase =
        ld <= 4
          ? "A — Restorative + prosthesis"
          : ld === 5
            ? "B — Perio focus"
            : pivot.phase || "C — Spaced maintenance";
      const goal = mode === "light" ? 40 : mode === "review" ? 55 : 70;
      const note =
        mode === "review"
          ? `Review lesson ${ld} weak topics + wrong book`
          : mode === "volume"
            ? `Volume: lesson ${ld} MCQs from verified pool`
            : "Light maintenance — protect sleep";
      out.splice(i + 1, 0, row(out.length + 1, ld, mode, phase, goal, note, 0));
      insertIx++;
    }
    return out.map((r, i) => ({ ...r, day: i + 1 }));
  }

  const TRACK_45 = stretchTrack(TRACK_30, 45, "45-day");
  const TRACK_60 = stretchTrack(TRACK_30, 60, "60-day");
  const TRACK_90 = stretchTrack(TRACK_30, 90, "90-day");

  /** Helper: all usable questions across all topics */
  function allVerified() {
    return VERIFIED.total;
  }

  w.PLAN_TRACKS = {
    VERIFIED: VERIFIED,
    allVerified: allVerified,
    TRACK_14,
    TRACK_30,
    TRACK_45,
    TRACK_60,
    TRACK_90,
  };
})(window);
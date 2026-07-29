#!/usr/bin/env python3
"""
build_flash_notes.py — Phase 1 generator for the SDLE "Flash Notes" tab.

Parses the community recall .md files (the 6 focus PDFs + 2 recent adds),
extracts recall items (stem + options + community-marked answer), classifies
each by department, dedupes by normalized stem, and emits a single static
data file the web app can load offline:

    data/flash_notes.js   ->   window.FLASH_NOTES = {...}

NO network, no API. Pure local text parsing. Reproducible: rerun any time.

Sources:
  1 sdle-ref/questions/Mar-June_2026.md            (numbered MCQs, ✅ markers)
  2 sdle-ref/focus/SDLE_May_2026.md                   (numbered Qs, inline answers)
  3 sdle-ref/focus/تلخيص_سعود*.md                     (Saud summary)
  4 sdle-ref/focus/رفيع_المقام_19*.md
  5 sdle-ref/focus/رفيع_المقام_١٦.md                  (department-structured)
  6 sdle-ref/focus/<mojibake>.md (ملف سعود مصحّح)
  -- recent adds --
  7 sdle-ref/focus_new/June_July2023_abtal.md        (markitdown table format, ●/✅)
  8 sdle-ref/focus_new/Golden_File_2_2021.md         ((N) inline, ✅✅/✳ ✳)

Answer-marker legend (from the PDFs):
  ✅ / ✅✅ verified-by-student  -> marker "verified"  (still needs Phase-3 book check)
  🟢 answer given, no ref       -> marker "given"
  🟡 answer with a reference     -> marker "ref"
  ✳ ✳ / ✳ reference marker       -> marker "ref"
  🔵 / 🟦 read-more              -> marker "readmore"
  🔁 unsure                      -> marker "unsure"
  ●   unknown/no answer          -> marker "unknown"
"""
from __future__ import annotations
import json, os, re, sys, unicodedata
from pathlib import Path

ROOT = Path("/data/prometric")
REF = ROOT / "sdle-ref"
OUT = ROOT / "sdle-prep" / "data" / "flash_notes.js"

SOURCES = [
    ("Mar-June_2026",  REF / "questions" / "Mar-June_2026.md", "numbered"),
    ("SDLE_May_2026",  REF / "focus"     / "SDLE_May_2026.md", "numbered"),
    ("Saud_Talkhees",  REF / "focus"     / "تلخيص_سعود__20251130_154203_٠٠٠٠.md", "sectioned"),
    ("Rafi_Maqam_19",  REF / "focus"     / "رفيع_المقام_19_-___دعواتكم__.md", "sectioned"),
    ("Rafi_Maqam_16",  REF / "focus"     / "رفيع_المقام_١٦.md", "sectioned"),
    ("Saud_Masahhah",  None, "sectioned"),  # mojibake name, resolved below
    ("June_July2023",  REF / "focus_new"  / "June_July2023_abtal.md", "table"),
    ("GoldenFile2",    REF / "focus_new"  / "Golden_File_2_2021.md", "numbered"),
]

# resolve the mojibake-named "Saud corrected" file: the one focus .md not claimed
claimed = {p for _, p, _ in SOURCES if p}
for p in sorted((REF / "focus").iterdir()):
    if p.suffix == ".md" and p not in claimed:
        SOURCES[5] = ("Saud_Masahhah", p, "sectioned")
        break

# ---------------------------------------------------------------------------
# Department classifier
# ---------------------------------------------------------------------------
DEPTS = {
    "restorative": [r"\bresto\b", r"operative", r"amalgam", r"composite", r"class\s+[i1v]+\b",
                    r"caries", r"cavity", r"matrix", r"liner", r"base\b", r"varnish",
                    r"gingival margin", r"smear layer", r"hybrid layer", r"etch", r"bond",
                    r"\bgic\b", r"rmgic", r"fluoride", r"sealant", r"bleach", r"shade",
                    r"pin\s?hole", r"pinhole", r"veneer", r"ceramic", r"porcelain"],
    "endo": [r"\bendo\b", r"endodontic", r"pulp", r"pulpotom", r"pulpectom", r"apexif",
             r"apexogenesis", r"obtura", r"gutta", r"root canal", r"irrigation",
             r"\bnaocl\b", r"edta\b", r"\bmta\b", r"cvek", r"trephination", r"vertical root",
             r"\bvrf\b", r"periradicular", r"periapical", r"formocresol", r"calcium hydroxide"],
    "perio": [r"\bperio\b", r"periodont", r"probing", r"\bcal\b", r"attachment",
              r"gingiv", r"plaque", r"calculus", r"scaling", r"root plan", r"\bsrp\b",
              r"furcation", r"miller recession", r"mucogingival", r"\bgtr\b", r"regenerat",
              r"freedom", r"keratinized", r"\baap\b", r"necrotizing ulcer", r"anug",
              r"stillman", r"bass technique", r"charter"],
    "fixed": [r"\bfixed\b", r"prosthodontics", r"crown", r"\bpfm\b", r"metal.ceramic",
              r"margin", r"chamfer", r"shoulder", r"ferrule", r"post\s?and\s?core", r"\bcore\b",
              r"bridge", r"abutment", r"retainer", r"pontic", r"finish line", r"reduction",
              r" provisional", r"temporary", r"impression"],
    "rpd": [r"\brpd\b", r"removable partial", r"kennedy", r"\bclasp\b", r"rest\s?seat",
            r"denture", r"\brpi\b", r"\brpa\b", r"minor connector", r"surveyor",
            r"path of insertion", r"tissue born", r"tooth born", r"\bdolder\b", r"denture teeth"],
    "implant": [r"implant", r"osseointegrat", r"\bfixture\b", r"abutment", r"\b3\s?mm\b",
                r"bone crest", r"loading protocol", r"\bstage\s?1\b", r"\bstage\s?2\b",
                r"\b8mm\b", r"major connector"],
    "ortho_pedo": [r"\bortho\b", r"\bpedo\b", r"orthodontic", r"paediatric", r"pediatric",
                   r"class\s*[i1]+", r"overjet", r"overbite", r"crossbite", r"crowding",
                   r"leeway space", r"space maintain", r"eruption", r"shedding",
                   r"frankel", r"expansion", r"functional appliance", r"twin block",
                   r"sunday bite", r"pseudo.class\s?3", r"traumatic injur", r"avuls",
                   r"\bcvek\b", r"apexogenesis", r"mcnamara", r"cleft"],
    "oms": [r"\boms\b", r"oral surgery", r"oral medicine", r"extraction", r"\bian\b",
            r"inferior alveolar", r"third molar", r"impaction", r"biopsy", r"fracture",
            r"\bmronj\b", r"\bonj\b", r"dry socket", r"osteomyelitis", r"odonto(?:genic)? infection",
            r"space infection", r" Ludwig", r"myxedema", r"thyroid", r"asthma", r"ibuprofen",
            r"epinephrine", r"adrenaline", r"pemphigus", r"epidermolysis", r"lichen",
            r"candidiasis", r"herpes", r"nicotine stomatitis", r"hand.?foot.?mouth",
            r" Paget", r"fibrous dysplasia", r"giant cell", r"ameloblast", r"odontoma",
            r"radiograph", r"\bx.?ray\b", r"radiolucen", r"radiopaq", r"\bcbct\b",
            r"parotid", r"sialadenitis", r"sialolith", r"mucocele", r"\bnecros", r"fibroma",
            r"cleft lip", r"cushing", r"\bmcv\b", r"dehiscence", r"fenestration",
            r"analgesic", r"paracetamol", r"tmj", r"disc dislocation", r"derangement"],
    "ethics": [r"\bethics\b", r"professionalism", r"parentalism", r"consent", r"informed",
               r"confidential", r"malpractice", r"negligence", r"infection control", r"\bic\b",
               r"steriliz", r"disinfect", r"hand hygiene", r"sharps", r"needle stick",
               r"\bla\b", r"local anesth", r"\bmepivacaine\b", r"\blidocaine\b",
               r"\barticaine\b", r"\bprilocaine\b", r"\bbupivacaine\b", r"topical",
               r"vasoconstrictor", r"\baha\b", r"\bcpr\b", r"\bmbc\b", r"discrimination",
               r"vip patient", r"patient safety", r"autonomy", r"yes we can"],
    "diagnostics": [r"\bradiograph", r"\bx.?ray\b", r"\bcbct\b", r"panoramic", r"bitewing",
                    r"periapical film", r"paralleling", r"bisecting", r"sloberr",
                    r"radiolucen", r"radiopaq", r"interproximal", r"lesion", r"biopsy",
                    r"histopath", r"stain", r"\bdiagnos", r"differential"],
}

SECTION_HEADERS = {
    "Endo": "endo", "Resto": "restorative", "Perio": "perio", "Implant": "implant",
    "Fixed": "fixed", "Removable": "rpd", "Ortho": "ortho_pedo", "Pedo": "ortho_pedo",
    "Professionalism": "ethics", "bioethics": "ethics", "infection control": "ethics",
    "patient safety": "ethics", "Oral medicine": "oms", "Oral surgery": "oms",
    "medically compromised": "oms", "Diagnostics": "diagnostics", "Radiology": "diagnostics",
}

LETTER = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def norm(s: str) -> str:
    s = unicodedata.normalize("NFKC", s)
    s = re.sub(r"[\u200b-\u200f\u202a-\u202e\ufeff]", "", s)
    s = re.sub(r"\s+", " ", s).strip().lower()
    return s

def dedupe_key(stem: str) -> str:
    n = norm(stem)
    n = re.sub(r"[^a-z0-9 ]", "", n)
    n = re.sub(r"\s+", " ", n).strip()
    return n[:80]

def classify(stem: str, options: list[str], section: str | None) -> str:
    blob = norm(" ".join([stem] + options))
    if section:
        sl = section.lower()
        for hdr, dept in SECTION_HEADERS.items():
            if hdr.lower() in sl:
                return dept
    scores = {d: 0 for d in DEPTS}
    for dept, pats in DEPTS.items():
        for p in pats:
            if re.search(p, blob, re.IGNORECASE):
                scores[dept] += 1
    best = max(scores, key=lambda d: scores[d])
    return best if scores[best] > 0 else "oms"

def marker_for(text: str) -> str:
    if "✅✅" in text or "✅" in text:
        return "verified"
    if "✳ ✳" in text or "✳✳" in text:
        return "ref"
    if "🟢" in text:
        return "given"
    if "🟡" in text:
        return "ref"
    if "🔵" in text or "🟦" in text:
        return "readmore"
    if "🔁" in text:
        return "unsure"
    return "unknown"

def needs_image(stem: str, raw: str) -> bool:
    blob = (stem + " " + raw).lower()
    return any(k in blob for k in ["pic", "picture", "image", "x-ray", "xray", "radiograph", "photo", "(depend on pic", "picof", "pictureof"])

def extract_options(block: str) -> list[tuple[str, str]]:
    opts = []
    # inline: "A. x B. y C. z D. w" (allow ✅✅ trailing)
    found = re.findall(r"([A-E])\s*[\.:\)]\s+([^A-E\n]*?)(?=\s+[A-E]\s*[\.:\)]|$)", block)
    if len(found) >= 2:
        for letter, txt in found:
            txt = txt.strip()
            if txt:
                opts.append((letter, txt))
        return opts
    # line-based
    for m in re.finditer(r"(?im)^\s*([A-E])\s*[\.:\)]\s+(.+)$", block):
        opts.append((m.group(1), m.group(2).strip()))
    return opts

def find_marked_answer(opts: list[tuple[str, str]], block: str) -> tuple[str | None, int | None]:
    for letter, txt in opts:
        if "✅✅" in txt or "✅" in txt or "🟢" in txt or "🟡" in txt or "✳" in txt:
            return letter, LETTER.get(letter, -1)
    for m in re.finditer(r"([A-E])\s*[\.:\)]\s+([^\n]*?[✅🟢🟡✳][^\n]*)", block):
        return m.group(1), LETTER.get(m.group(1), -1)
    return None, None

def split_stem_opts(body: str) -> tuple[str, str]:
    """Split a chunk body into stem text + options block by first inline option marker."""
    # find first occurrence of " A. " / " A) " / " A: " as a word
    m = re.search(r"(\s|^)([A-E])\s*[\.:\)]\s+", body)
    if m:
        return body[:m.start()].strip(), body[m.start():].strip()
    # also check line-based option on its own line
    m2 = re.search(r"(?m)^\s*([A-E])\s*[\.:\)]\s+", body)
    if m2:
        return body[:m2.start()].strip(), body[m2.start():].strip()
    return body.strip(), ""

# ---------------------------------------------------------------------------
# Markdown table flattener (for markitdown output like June_July2023)
# ---------------------------------------------------------------------------

SEP_ROW = re.compile(r"^\s*\|?\s*:?-{2,}.*$")

def flatten_tables(text: str) -> str:
    """Convert markitdown markdown tables into flat text lines (cells joined by spaces)."""
    out = []
    for raw in text.split("\n"):
        ln = raw.rstrip("\n")
        if SEP_ROW.match(ln):
            continue
        if "|" in ln and ln.strip().startswith("|"):
            # table row -> join cells
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            cells = [c for c in cells if c and c != "---"]
            if cells:
                joined = " ".join(cells)
                joined = re.sub(r"\s+", " ", joined).strip()
                if joined:
                    out.append(joined)
            continue
        out.append(ln)
    return "\n".join(out)

# ---------------------------------------------------------------------------
# Parsers per source shape
# ---------------------------------------------------------------------------

# numbered item start: "1. ", "1) ", "1: ", "(1)", "(1)A..." — anchored at line start
NUM_SPLIT = re.compile(r"(?m)^(?=\s*(?:\(\d{1,3}\)|\d{1,3})\s*[\.:\)]\s*\S)")
NUM_HEAD  = re.compile(r"^\s*(?:\((\d{1,3})\)|(\d{1,3}))\s*[\.:\)]\s*(.+)", re.S)

def parse_numbered(path: Path, source_id: str, flatten: bool = False) -> list[dict]:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        print(f"[warn] cannot read {path}: {e}", file=sys.stderr); return []
    if flatten:
        text = flatten_tables(text)
    items = []
    chunks = NUM_SPLIT.split(text)
    for chunk in chunks:
        chunk = chunk.strip()
        m = NUM_HEAD.match(chunk)
        if not m:
            continue
        body = m.group(3).strip()
        if not body or len(body) < 6:
            continue
        stem_text, opt_block = split_stem_opts(body)
        stem = re.sub(r"\s*[●]\s*$", "", stem_text).strip()
        opts = extract_options(opt_block) if opt_block else []
        answer_letter, answer_idx = (None, None)
        marker = marker_for(body)
        if opts:
            answer_letter, answer_idx = find_marked_answer(opts, opt_block)
        if not stem or len(stem) < 6:
            continue
        dept = classify(stem, [t for _, t in opts], None)
        items.append({
            "stem": stem[:400],
            "options": [f"{l}. {t}" for l, t in opts] if opts else [],
            "answerLetter": answer_letter,
            "answerIdx": answer_idx,
            "marker": marker,
            "needsImage": needs_image(stem, body),
            "source": source_id,
            "raw": body[:600].replace("\n", " "),
            "dept": dept,
        })
    return items

def parse_sectioned(path: Path, source_id: str) -> list[dict]:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        print(f"[warn] cannot read {path}: {e}", file=sys.stderr); return []
    items, buf, cur_dept = [], [], None

    def flush(buf):
        if not buf: return
        body = "\n".join(buf).strip()
        if len(body) < 6: return
        stem_text, opt_block = split_stem_opts(body)
        stem = re.sub(r"\s*[●]\s*$", "", stem_text).strip()
        opts = extract_options(opt_block) if opt_block else []
        answer_letter, answer_idx = (None, None)
        marker = marker_for(body)
        if opts:
            answer_letter, answer_idx = find_marked_answer(opts, opt_block)
        if not stem or len(stem) < 6: return
        dept = classify(stem, [t for _, t in opts], cur_dept)
        items.append({
            "stem": stem[:400], "options": [f"{l}. {t}" for l, t in opts] if opts else [],
            "answerLetter": answer_letter, "answerIdx": answer_idx, "marker": marker,
            "needsImage": needs_image(stem, body), "source": source_id,
            "raw": body[:600].replace("\n", " "), "dept": dept,
        })

    for raw in text.split("\n"):
        ln = raw.strip()
        is_header = False
        if ln and len(ln) < 40:
            for hdr in SECTION_HEADERS:
                if re.search(r"\b" + re.escape(hdr), ln, re.IGNORECASE):
                    cur_dept = SECTION_HEADERS[hdr]; is_header = True; break
        if is_header:
            flush(buf); buf = []; continue
        if re.match(r"^\s*(?:\(\d{1,3}\)|\d{1,3})\s*[\.:\)]\s+\S", ln) or re.match(r"^\s*[●\-•]\s+", ln) or re.match(r"^\s*Q\d+\s*[:\)]\s*", ln, re.I):
            flush(buf); buf = [ln]; continue
        if ln:
            buf.append(ln)
    flush(buf)
    return items

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    all_items, per_source = [], {}
    for sid, path, kind in SOURCES:
        if path is None or not path.exists():
            print(f"[warn] missing source {sid}: {path}", file=sys.stderr); continue
        if kind == "numbered":
            its = parse_numbered(path, sid, flatten=(sid == "June_July2023"))
        elif kind == "table":
            its = parse_numbered(path, sid, flatten=True)
        else:
            its = parse_sectioned(path, sid)
        per_source[sid] = len(its)
        all_items.extend(its)
        print(f"  {sid:18s} -> {len(its):5d} items")

    # dedupe by stem key
    by_key, order = {}, []
    for it in all_items:
        k = dedupe_key(it["stem"])
        if not k or len(k) < 4: continue
        if k in by_key:
            master = by_key[k]
            if it["source"] not in master["sources"]:
                master["sources"].append(it["source"])
            if master["answerIdx"] is None and it["answerIdx"] is not None:
                master["answerIdx"] = it["answerIdx"]; master["answerLetter"] = it["answerLetter"]
                master["marker"] = it["marker"]; master["options"] = it["options"] or master["options"]
            if not master["options"] and it["options"]: master["options"] = it["options"]
            continue
        it["sources"] = [it.pop("source")]
        by_key[k] = it; order.append(k)

    deduped = [by_key[k] for k in order]
    counters = {}
    for it in deduped:
        d = it["dept"]; counters[d] = counters.get(d, 0) + 1
        it["id"] = f"fn_{d}_{counters[d]:04d}"

    by_dept = {}
    for it in deduped:
        by_dept.setdefault(it["dept"], []).append(it)

    markers = {}
    for it in deduped:
        markers[it["marker"]] = markers.get(it["marker"], 0) + 1

    payload = {
        "generated": "2026-07-29",
        "total": len(deduped),
        "perSource": per_source,
        "markerStats": markers,
        "byDept": {d: by_dept.get(d, []) for d in [
            "restorative", "endo", "perio", "fixed", "rpd", "implant",
            "ortho_pedo", "oms", "ethics", "diagnostics"]},
        "sources": [
            {"id": "Mar-June_2026",  "label": "Mar–June 2026 (أبطال الدجيتال)", "file": "questions/Mar-June_2026.md", "recent": False},
            {"id": "SDLE_May_2026",  "label": "SDLE May 2026 (Dr. Zahra)",     "file": "focus/SDLE_May_2026.md", "recent": False},
            {"id": "Saud_Talkhees",  "label": "تلخيص سعود",                    "file": "focus/تلخيص_سعود*.md", "recent": False},
            {"id": "Rafi_Maqam_19",  "label": "رفيع المقام 19",                "file": "focus/رفيع_المقام_19*.md", "recent": False},
            {"id": "Rafi_Maqam_16",  "label": "رفيع المقام 16",                "file": "focus/رفيع_المقام_١٦.md", "recent": False},
            {"id": "Saud_Masahhah",  "label": "ملف سعود مصحّح",                "file": "focus/<saud masahhah>.md", "recent": False},
            {"id": "June_July2023",  "label": "June–July 2023 (أبطال الدجيتال) — recent add", "file": "focus_new/June_July2023_abtal.md", "recent": True},
            {"id": "GoldenFile2",    "label": "الملف الذهبي ٢ (yes we can 2021) — recent add", "file": "focus_new/Golden_File_2_2021.md", "recent": True},
        ],
        "markerLegend": {
            "verified": "✅ / ✅✅ community-marked correct (still needs Phase-3 book check)",
            "given":    "🟢 answer given, no reference",
            "ref":      "🟡 / ✳ ✳ answer with a reference",
            "readmore": "🔵 read more about it",
            "unsure":   "🔁 unsure",
            "unknown":  "● no answer / image-dependent",
        },
        "rule": "Student-bank answers are LEADS, not truth. Graded quizzes use only book_verified MCQs from questions.js. Flash Notes show recall stems + community answer + marker so the student knows what to trust.",
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8") as f:
        f.write("/** Flash Notes — generated by scripts/build_flash_notes.py\n")
        f.write(" *  DO NOT hand-edit. Rerun the script after changing source .md files.\n")
        f.write(" *  Phase 1 of UPGRADE_PLAN.md — see plan for verification rules.\n")
        f.write(" */\nwindow.FLASH_NOTES = ")
        f.write(json.dumps(payload, ensure_ascii=False, indent=0))
        f.write(";\n")

    print(f"\nWROTE {OUT}")
    print(f"  total deduped items: {payload['total']}")
    print(f"  by dept: " + ", ".join(f"{d}={len(by_dept.get(d, []))}" for d in payload['byDept']))
    print(f"  markers: {payload['markerStats']}")

if __name__ == "__main__":
    main()

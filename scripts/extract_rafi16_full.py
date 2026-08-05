#!/usr/bin/env python3
"""Extract ALL Rafi-16 questions from the full pdftotext extraction
(sdle-prep/data/raw/rafi/rafi_part_16.txt, 2,013 questions) and merge the
missing ones into the flash deck under source Rafi_Maqam_16.

The old flash source file (focus/رفيع_المقام_١٦.md) was a broken markitdown
extraction with only ~68 numbered lines — 1,094 questions were missing from
the app entirely. This rebuilds the source from the good pdftotext output.

Rules:
- Options A-D + ✅ marker -> proper MCQ (answerIdx from the ✅).
- No options -> recall note (honest).
- Dept from the section headers (Endo/Resto/Perio/Implant/Fixed/Removable/
  Ortho/Pedo/Professionalism/Oral...).
- Dedupe by normalized stem against the EXISTING flash deck; skip items already
  present (never duplicate).
- Community recall -> markers stay 'verified' (student ✅) / 'ref' (no marker);
  the app labels them honestly. Books remain the only answer authority.
"""
import hashlib, json, os, re, sys, tempfile
from pathlib import Path

ROOT = Path("/data/prometric")
FN = ROOT / "sdle-prep" / "data" / "flash_notes.js"
TXT = ROOT / "sdle-prep" / "data" / "raw" / "rafi" / "rafi_part_16.txt"

SECTION_MAP = [
    ("professionalism and bioethics", "ethics"),
    ("infection control", "ethics"),
    ("patient safety", "ethics"),
    ("oral medicine", "oms"),
    ("oral surgery", "oms"),
    ("medically compromised", "oms"),
    ("endo", "endo"),
    ("resto", "restorative"),
    ("perio", "perio"),
    ("implant", "implant"),
    ("fixed", "fixed"),
    ("removable", "rpd"),
    ("ortho", "ortho_pedo"),
    ("pedo", "ortho_pedo"),
]

def norm(s):
    return re.sub(r"[^a-z0-9\u0621-\u064A]", "", (s or "").lower())

def classify(stem):
    for kw, dept in SECTION_MAP:
        if kw in stem.lower():
            return dept
    return "oms"

def parse():
    t = TXT.read_text(encoding="utf-8", errors="replace")
    lines = t.split("\n")
    blocks, cur, cur_dept = [], None, "oms"
    for ln in lines:
        st = ln.strip()
        for kw, dept in SECTION_MAP:
            if st and len(st) < 40 and re.search(r"\b" + re.escape(kw), st, re.I):
                cur_dept = dept
                break
        m = re.match(r"^\s*(\d{1,3})[\.\)]\s*\S", ln)
        if m:
            if cur: blocks.append((cur_dept, cur))
            cur = [ln]
        elif cur is not None and st:
            cur.append(ln)
    if cur: blocks.append((cur_dept, cur))

    items = []
    for dept, b in blocks:
        first = re.sub(r"^\s*\d{1,3}[\.\)]\s*", "", b[0]).strip()
        stem = re.sub(r"\s*[●•]\s*$", "", first).strip()
        if not stem or len(stem) < 4:
            continue
        opts, answer_letter, answer_idx = [], None, None
        for ln in b[1:]:
            om = re.match(r"^\s*([A-Ea-e])[\.\)]\s*(.+)$", ln.strip())
            if om:
                letter, text = om.group(1).upper(), om.group(2).strip()
                marked = "✅" in text
                text = re.sub(r"✅+\s*$", "", text).strip()
                opts.append((letter, text, marked))
        seen = set()
        clean_opts = []
        for letter, text, marked in opts:
            key = norm(text)
            if not key or key in seen:
                continue
            seen.add(key)
            clean_opts.append((letter, text, marked))
        if clean_opts:
            for i, (letter, text, marked) in enumerate(clean_opts):
                if marked:
                    answer_letter, answer_idx = letter, i
        marker = "verified" if answer_letter else "ref"
        # 'verified' here means the STUDENT marked it; kept honest via marker text
        items.append({
            "stem": stem[:400],
            "options": [f"{l}. {t}" for l, t, _ in clean_opts],
            "answerLetter": answer_letter,
            "answerIdx": answer_idx,
            "marker": marker,
            "dept": dept,
            "needsImage": bool(re.search(r"xray|radiograph|image|pic|photo|figure|picture", stem, re.I)),
            "sources": ["Rafi_Maqam_16"],
            "raw": " ".join(b)[:600],
            "id": "fn_rafi16_" + hashlib.sha1(norm(stem).encode()).hexdigest()[:10],
        })
    return items

def main():
    items = parse()
    print(f"parsed {len(items)} items from rafi_part_16.txt")
    src = FN.read_text(encoding="utf-8")
    fbody = src.split("=", 1)[1].strip().rstrip().rstrip(";").strip()
    data = json.loads(fbody)
    existing = {}
    for dept, arr in data["byDept"].items():
        for it in arr:
            existing[norm(it.get("stem", ""))] = it.get("id")
    added, skipped = 0, 0
    for it in items:
        key = norm(it["stem"])
        if key in existing:
            skipped += 1
            continue
        dept = it.pop("dept")
        data["byDept"].setdefault(dept, []).append(it)
        existing[key] = it["id"]
        added += 1
    data["total"] = sum(len(v) for v in data["byDept"].values())
    ps = data.setdefault("perSource", {})
    ps["Rafi_Maqam_16"] = sum(1 for arr in data["byDept"].values() for it in arr
                              if "Rafi_Maqam_16" in (it.get("sources") or []))
    # point the source entry at the good extraction
    for s in data.get("sources", []):
        if s.get("id") == "Rafi_Maqam_16":
            s["file"] = "raw/rafi/rafi_part_16.txt (full 2,013 Q pdftotext)"
    new_src = src.replace(fbody, json.dumps(data, ensure_ascii=False, indent=1))
    fd, tmp = tempfile.mkstemp(dir=str(FN.parent), suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        fh.write(new_src)
    os.replace(tmp, FN)
    print(f"added {added} new Rafi-16 items, skipped {skipped} already present")
    print(f"Rafi_Maqam_16 perSource now: {ps['Rafi_Maqam_16']}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Full recall extraction for the high-yield exam sources (user: exam is 70% from these):
  - Rafi_Maqam_19  (رفيع المقام 19 - 98 pages, sectioned numbered questions)
  - Mar-June_2026  (Mar-June 2026 أبطال الدجيتال - 142 pages, numbered + ✅/🟢/🔁)
  - Saud_Talkhees  (تلخيص سعود - 93 pages, 🚨-led questions)
  - Saud_Masahhah  (ملف سعود مصحّح - 680 pages, Q1)/A-/B- table format)

Each source is parsed to items (stem + options + answer marker), deduped by
normalized stem against the EXISTING flash deck, and the missing ones merged
into flash_notes.js under the proper source id. Community recall is kept
honest: markers verified/ref, verdict needs_review (book-check pending).
"""
import hashlib, json, os, re, sys, tempfile
from pathlib import Path

ROOT = Path("/data/prometric")
FN = ROOT / "sdle-prep" / "data" / "flash_notes.js"
RAW = ROOT / "sdle-prep" / "data" / "raw" / "recall"

SECTION_MAP = [
    ("professionalism and bioethics", "ethics"), ("infection control", "ethics"),
    ("patient safety", "ethics"), ("oral medicine", "oms"), ("oral surgery", "oms"),
    ("medically compromised", "oms"), ("endo", "endo"), ("resto", "restorative"),
    ("perio", "perio"), ("implant", "implant"), ("fixed", "fixed"),
    ("removable", "rpd"), ("ortho", "ortho_pedo"), ("pedo", "ortho_pedo"),
]

def norm(s):
    return re.sub(r"[^a-z0-9\u0621-\u064A]", "", (s or "").lower())

def classify(stem):
    for kw, dept in SECTION_MAP:
        if kw in stem.lower():
            return dept
    return "oms"

MARK_ANS = re.compile(r"✅|🟢|🔁")

def parse_common(path, source_id, q_re, opt_re, dept_headers=True):
    """Generic parser: q_re detects a new question line, opt_re detects option lines."""
    t = path.read_text(encoding="utf-8", errors="replace")
    lines = t.split("\n")
    blocks, cur, cur_dept = [], None, "oms"
    for ln in lines:
        st = ln.strip()
        if dept_headers and st and len(st) < 45:
            for kw, dept in SECTION_MAP:
                if re.search(r"\b" + re.escape(kw), st, re.I):
                    cur_dept = dept
                    break
        if q_re.match(ln):
            if cur: blocks.append((cur_dept, cur))
            cur = [ln]
        elif cur is not None and st and not re.match(r"^\s*[•●\-]\s*$", st):
            cur.append(ln)
    if cur: blocks.append((cur_dept, cur))

    items = []
    for dept, b in blocks:
        first = q_re.sub("", b[0]).strip()
        first = re.sub(r"^[?:؟]+\s*|\s*[؟?]\s*$", "", first).strip()
        stem = re.sub(r"\s*[●•🟡🔵]\s*$", "", first).strip()
        if not stem or len(stem) < 4 or stem in ("—", "-", "---"):
            continue
        opts, ans_letter, ans_idx = [], None, None
        for ln in b[1:]:
            om = opt_re.match(ln.strip())
            if om:
                letter = om.group(1).upper()
                text = (om.group(2) if om.lastindex and om.lastindex >= 2 else om.group(0)).strip()
                marked = bool(MARK_ANS.search(text))
                text = re.split(r"✅|🟢|🔁", text)[0].strip()
                text = re.sub(r"\s*[●•]\s*$", "", text).strip()
                if text:
                    opts.append((letter, text, marked))
        seen, clean = set(), []
        for letter, text, marked in opts:
            k = norm(text)
            if not k or k in seen: continue
            seen.add(k); clean.append((letter, text, marked))
        if clean:
            for i, (letter, text, marked) in enumerate(clean):
                if marked:
                    ans_letter, ans_idx = letter, i
        marker = "verified" if ans_letter else "ref"
        items.append({
            "stem": stem[:400],
            "options": [f"{l}. {t}" for l, t, _ in clean],
            "answerLetter": ans_letter,
            "answerIdx": ans_idx,
            "marker": marker,
            "needsImage": bool(re.search(r"xray|radiograph|image|pic|photo|figure|picture", stem, re.I)),
            "sources": [source_id],
            "raw": " ".join(b)[:600],
            "id": "fn_" + source_id.lower().replace("-", "") + "_" + hashlib.sha1(norm(stem).encode()).hexdigest()[:10],
        })
    return items

def parse_saud(path, source_id):
    """ملف سعود: 'Q1) stem' lines; options A- B- C- (often empty)."""
    t = path.read_text(encoding="utf-8", errors="replace")
    q_re = re.compile(r"\bQ\s*(\d+)\s*[\):]", re.I)
    blocks, cur = [], None
    for ln in t.split("\n"):
        if q_re.search(ln):
            if cur: blocks.append(cur)
            cur = [ln]
        elif cur is not None and ln.strip():
            cur.append(ln)
    if cur: blocks.append(cur)
    items = []
    for b in blocks:
        stem = q_re.sub("", b[0]).strip()
        stem = re.sub(r"^[?:؟]+\s*|\s*[؟?]\s*$", "", stem).strip()
        if not stem or len(stem) < 4:
            continue
        opts = []
        for ln in b[1:]:
            om = re.match(r"^\s*([A-Ea-e])\s*[-–—]?\s*(.*)$", ln.strip())
            if om and om.group(2).strip():
                opts.append((om.group(1).upper(), om.group(2).strip(), False))
        items.append({
            "stem": stem[:400],
            "options": [f"{l}. {t}" for l, t, _ in opts],
            "answerLetter": None, "answerIdx": None,
            "marker": "ref",
            "needsImage": bool(re.search(r"xray|radiograph|image|pic|photo|figure|picture", stem, re.I)),
            "sources": [source_id],
            "raw": " ".join(b)[:600],
            "id": "fn_saudmasahhah_" + hashlib.sha1(norm(stem).encode()).hexdigest()[:10],
        })
    return items

def main():
    jobs = [
        ("Rafi_Maqam_19", RAW / "rafi19.txt",
         re.compile(r"^\s*\d{1,3}[\.\)]\s*\S"),
         re.compile(r"^\s*([A-Ea-e])[\.\)]\s*\S")),
        ("Mar-June_2026", RAW / "marjune_2026.txt",
         re.compile(r"^\s*\d{1,3}[\.\)]\s*\S"),
         re.compile(r"^\s*([A-Ea-e])[\.\)]\s*\S")),
        ("Saud_Talkhees", RAW / "talkhees.txt",
         re.compile(r"^\s*(?:🚨|🛑|❓|Q\d+\s*[\):])"),
         re.compile(r"^\s*([A-Ea-e])[\.\)\-–]\s*\S")),
    ]
    src = FN.read_text(encoding="utf-8")
    fbody = src.split("=", 1)[1].strip().rstrip().rstrip(";").strip()
    data = json.loads(fbody)
    existing = {}
    for dept, arr in data["byDept"].items():
        for it in arr:
            existing[norm(it.get("stem", ""))] = it.get("id")
    for source_id, path, q_re, opt_re in jobs:
        if not path.exists():
            print(source_id, "MISSING", path); continue
        items = parse_common(path, source_id, q_re, opt_re)
        added = 0
        for it in items:
            key = norm(it["stem"])
            if key in existing: continue
            dept = it.pop("dept") if "dept" in it else classify(it["stem"])
            data["byDept"].setdefault(dept, []).append(it)
            existing[key] = it["id"]; added += 1
        print(f"{source_id}: parsed {len(items)} blocks -> added {added} new")
    # Saud Masahhah: compare with existing; add missing Q1)-style blocks
    sp = RAW / "saud_masahhah.txt"
    if sp.exists():
        items = parse_saud(sp, "Saud_Masahhah")
        added = 0
        for it in items:
            key = norm(it["stem"])
            if key in existing: continue
            data["byDept"].setdefault(classify(it["stem"]), []).append(it)
            existing[key] = it["id"]; added += 1
        print(f"Saud_Masahhah: parsed {len(items)} Q-blocks -> added {added} new")
    data["total"] = sum(len(v) for v in data["byDept"].values())
    ps = data.setdefault("perSource", {})
    for sid in ["Rafi_Maqam_19", "Mar-June_2026", "Saud_Talkhees", "Saud_Masahhah"]:
        ps[sid] = sum(1 for arr in data["byDept"].values() for it in arr if sid in (it.get("sources") or []))
    for s in data.get("sources", []):
        if s.get("id") in ("Rafi_Maqam_19", "Mar-June_2026", "Saud_Talkhees", "Saud_Masahhah"):
            s["file"] = f"raw/recall/{s['id']}.txt (full pdftotext)"
    new_src = src.replace(fbody, json.dumps(data, ensure_ascii=False, indent=1))
    fd, tmp = tempfile.mkstemp(dir=str(FN.parent), suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        fh.write(new_src)
    os.replace(tmp, FN)
    print("total:", data["total"])

if __name__ == "__main__":
    main()

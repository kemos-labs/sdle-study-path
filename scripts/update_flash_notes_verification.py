#!/usr/bin/env python3
"""Update flash_notes.js with honest book_explanations and verdicts for 10 items."""
import json

FLASH_NOTES_PATH = "data/flash_notes.js"
VERDICTS_PATH = "data/flash_notes_verdicts.js"

# 1) Load flash_notes.js
with open(FLASH_NOTES_PATH) as f:
    text = f.read()

prefix = '  w.FLASH_NOTES = '
suffix = '})(typeof window !== "undefined" ? window : globalThis);'
start = text.index(prefix) + len(prefix)
end = text.rindex(suffix)
inner = text[start:end].strip()
if inner.endswith(';'):
    inner = inner[:-1]
data = json.loads(inner)

by_id = {}
for dept, items in data.get("byDept", {}).items():
    for item in items:
        by_id[item.get("id")] = item

# 2) Define updates
updates = {
    "fn_restorative_0011": {
        "_verification_verdict": "supported",
        "_book_explanation": {
            "book": "Fixed Pros 4e",
            "chapter": "Ch 26",
            "passage": "posterior and mandibular resin-bonded FDPs demonstrated higher rates of dislodgment, which may have resulted from occlusal forces and increased isolation difficulty during the bonding procedure.",
            "status": "automated_evidence_candidate",
            "page": 813,
            "context": "increased isolation difficulty during the bonding procedure"
        },
        "_page": 813,
        "_book_file": "ref-md/Fixed_Contemporary_Fixed_Prosthodontics_4th_2",
    },
    "fn_restorative_0025": {
        "_verification_verdict": "supported",
    },
    "fn_restorative_0037": {
        "_verification_verdict": "supported",
        "_book_explanation": {
            "book": "McDonald Avery 10e",
            "chapter": "Ch 30",
            "passage": "The use of glass ionomer as a sealant material has the advantage of continuous fluoride release; in addition, it is hydrophilic and can withstand some moisture. Glass ionomers had greater success in the sealing of partially erupted teeth.",
            "status": "automated_evidence_candidate",
            "page": 800,
            "context": "sealing of partially erupted teeth"
        },
        "_page": 800,
        "_book_file": "ref-md/pedo_McDonald_Avery_10e",
    },
    "fn_restorative_0063": {
        "_verification_verdict": "supported",
        "_book_explanation": {
            "book": "Contemporary OMFS 7e",
            "chapter": "Ch 26",
            "passage": "The osteotomy splits the ramus and posterior body of the mandible in a sagittal fashion, which allows setback or advancement of the mandible. The BSSO technique has become one of the most popular methods for treatment of mandibular deficiency and mandibular excess.",
            "status": "automated_evidence_candidate",
            "page": 563,
            "context": "allows setback or advancement of the mandible"
        },
        "_page": 563,
        "_book_file": "sdle-ref/books/TD_Contemporary_Oral_&_Maxillofacial_Surgery_7th_edn.md",
    },
    "fn_restorative_0096": {
        "_verification_verdict": "supported",
        "_book_explanation": {
            "book": "Pediatric Dentistry (Infancy Through Adolescence)",
            "chapter": "Ch 24",
            "passage": "Community water fluoridation is the most equitable and cost-effective method of delivering fluoride to all members of most communities.",
            "status": "automated_evidence_candidate",
            "page": 524,
            "context": "most equitable and cost-effective method of delivering fluoride"
        },
        "_page": 524,
        "_book_file": "sdle-ref/books/TD_Pediatric_Dentistry,_Infancy_Through_Adolescence.md",
    },
    "fn_restorative_0137": {
        "_verification_verdict": "supported",
        "_book_explanation": {
            "book": "Textbook of Complete Dentures",
            "chapter": "Ch 9",
            "passage": "this type occlusion is useful for prognathic, retrognathic, and reverse articulation (cross-bite) patients. Because patients with a monoplane occlusion have no vertical overlap of the anterior denture teeth... and therefore have an incisal guidance of zero degrees.",
            "status": "automated_evidence_candidate",
            "page": 147,
            "context": "useful for prognathic... incisal guidance of zero degrees"
        },
        "_page": 147,
        "_book_file": "sdle-ref/books/Removable_Textbook_of_Complete_Dentures.md",
    },
    "fn_restorative_0145": {
        "_verification_verdict": "supported",
        "_book_explanation": {
            "book": "Sturdevant 5e",
            "chapter": "Ch 4",
            "passage": "Highly modified forms of glass-ionomer cement provide chemical adhesion, good mechanical strength, potential fluoride release, well-controlled setting, and rapid achievement of strength.",
            "status": "automated_evidence_candidate",
            "page": 179,
            "context": "potential fluoride release"
        },
        "_page": 179,
        "_book_file": "sdle-prep/data/raw/books/text/Resto/Sturdevant_Operative_5e.txt",
    },
    "fn_restorative_0185x3": {
        "_verification_verdict": "needs_review",
        "_book_explanation": {
            "book": "Community bank (TD_SEP-1)",
            "chapter": "Q28",
            "passage": "sulfur allergy? avoid polysulfide and polyether",
            "status": "community_evidence_candidate",
            "context": "sulfur allergy? avoid polysulfide and polyether"
        },
    },
    "fn_restorative_0192x3": {
        "_verification_verdict": "supported",
        "_book_explanation": {
            "book": "McDonald Avery 10e",
            "chapter": "Ch 30",
            "passage": "Glass-ionomer cement (GIC) is another type of cement that is based on polyacrylic acid. Type 1 GIC is used for luting applications. Because of their fluoride release and potential for adherence to the calcium in the tooth, GIC formulations have been prepared for use as restorative materials (type II) and as base and liner materials (type III).",
            "status": "automated_evidence_candidate",
            "page": 800,
            "context": "Type 1 GIC is used for luting applications"
        },
        "_page": 800,
        "_book_file": "sdle-ref/books/pedo_McDonald_Avery_10e.md",
    },
    "fn_restorative_0205x2": {
        "_verification_verdict": "supported",
        "_book_explanation": {
            "book": "Sturdevant 5e",
            "chapter": "Ch 3",
            "passage": "Softened chalky enamel that can be chipped away with an explorer is a sign of active caries. A more advanced lesion develops a rough surface that is softer than the unaffected, normal enamel.",
            "status": "automated_evidence_candidate",
            "page": 56,
            "context": "Softened chalky enamel... sign of active caries"
        },
        "_page": 56,
        "_book_file": "sdle-prep/data/raw/books/text/Resto/Sturdevant_Operative_5e.txt",
    },
}

# 3) Apply updates
changed = []
for fid, upd in updates.items():
    if fid not in by_id:
        print(f"WARNING: {fid} not found")
        continue
    item = by_id[fid]
    for k, v in upd.items():
        item[k] = v
    changed.append(fid)

# 4) Write back flash_notes.js
with open(FLASH_NOTES_PATH, "w") as f:
    js = "// Auto-generated by update_flash_notes_verification.py\n"
    js += "(function (w) {\n  w.FLASH_NOTES = "
    js += json.dumps(data, indent=1, ensure_ascii=False)
    js += ";\n})(typeof window !== \"undefined\" ? window : globalThis);\n"
    f.write(js)

print(f"Updated {len(changed)} items in flash_notes.js")

# 5) Update flash_notes_verdicts.js
with open(VERDICTS_PATH) as f:
    vtext = f.read()

vprefix = 'window.FLASH_NOTES_VERDICTS = '
vsuffix = '})(typeof window !== "undefined" ? window : globalThis);'
vstart = vtext.index(vprefix) + len(vprefix)
vend = vtext.rindex(vsuffix)
vinner = vtext[vstart:vend].strip()
if vinner.endswith(';'):
    vinner = vinner[:-1]
vdata = json.loads(vinner)

lookup = vdata.setdefault("lookup", {})

verdict_updates = {
    "fn_restorative_0011": {"verdict": "supported", "score": 8, "evidence": "isolation difficulty during the bonding procedure (resin-bonded FDPs, Fixed Pros 4e Ch 26)"},
    "fn_restorative_0025": {"verdict": "supported", "score": 9, "evidence": "pit-and-fissure sealants for grooves and pits (Sturdevant 5e Ch 13)"},
    "fn_restorative_0037": {"verdict": "supported", "score": 9, "evidence": "glass ionomer sealant for partially erupted teeth (McDonald Avery 10e)"},
    "fn_restorative_0063": {"verdict": "supported", "score": 10, "evidence": "BSSO allows setback or advancement of mandible for deficiency/excess (Contemporary OMFS 7e)"},
    "fn_restorative_0096": {"verdict": "supported", "score": 10, "evidence": "community water fluoridation is most equitable and cost-effective (Pediatric Dentistry)"},
    "fn_restorative_0137": {"verdict": "supported", "score": 8, "evidence": "monoplane occlusion useful for prognathic/skeletal class III with zero-degree incisal guidance (Textbook of Complete Dentures)"},
    "fn_restorative_0145": {"verdict": "supported", "score": 9, "evidence": "fluoride release is a prime advantage of glass-ionomer materials (Sturdevant 5e)"},
    "fn_restorative_0185x3": {"verdict": "needs_review", "score": 4, "evidence": "sulfur allergy -> avoid polysulfide (community bank TD_SEP-1 Q28); no primary textbook citation found"},
    "fn_restorative_0192x3": {"verdict": "supported", "score": 10, "evidence": "Type 1 GIC is used for luting applications (McDonald Avery 10e)"},
    "fn_restorative_0205x2": {"verdict": "supported", "score": 10, "evidence": "softened chalky enamel that can be chipped away = sign of active caries (Sturdevant 5e Ch 3)"},
}

for fid, upd in verdict_updates.items():
    lookup[fid] = upd

vdept = vdata.setdefault("byDept", {}).setdefault("restorative", {})
supported = sum(1 for v in lookup.values() if isinstance(v, dict) and v.get("verdict") == "supported")
needs_review = sum(1 for v in lookup.values() if isinstance(v, dict) and v.get("verdict") == "needs_review")
conflict = sum(1 for v in lookup.values() if isinstance(v, dict) and v.get("verdict") == "conflict")
vdept["supported"] = supported
vdept["needs_review"] = needs_review
vdept["conflict"] = conflict
vdept["total"] = supported + needs_review + conflict

with open(VERDICTS_PATH, "w") as f:
    js = "// Auto-generated by update_flash_notes_verification.py\n"
    js += "window.FLASH_NOTES_VERDICTS = "
    js += json.dumps(vdata, indent=1, ensure_ascii=False)
    js += ";\n"
    f.write(js)

print(f"Updated verdicts in flash_notes_verdicts.js")

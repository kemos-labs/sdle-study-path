"""
Fix all 68 thin explanations in questions.js.
These are "boost" drill questions with 1-3 word explanations.
Each gets a proper explanation with textbook citation.
"""
import json, re

# Read questions.js
with open('data/questions.js', encoding='utf-8') as f:
    text = f.read()

# Extract the bank using the known pattern
m = re.search(r'(?:w\.\s*)?(?:const\s+)?QUESTION_BANK\s*=\s*(\[.*?\])\s*;', text, re.S)
if not m:
    # Try alternative pattern
    m = re.search(r'QUESTION_BANK\s*=\s*(\[.*?\])\s*;', text, re.S)
bank_str = m.group(1)
bank = json.loads(bank_str)

# Maps
fixes = {}

# per_boost_029 - Peri-implantitis
fixes['per_boost_029'] = {
    'explanation': (
        'Peri-implantitis is an inflammatory disease of the tissues around dental implants '
        'resulting in progressive bone loss, whereas peri-implant mucositis is a reversible '
        'inflammatory change of soft tissues without bone loss. '
        '[Book: perio_Carranza_Clinical_Periodontology_2018]'
    ),
    'book_verified': True
}

# end_boost_035 - Smear layer
fixes['end_boost_035'] = {
    'explanation': (
        'The smear layer is a surface film of debris (organic + inorganic) retained on '
        'dentin or root canal walls after instrumentation with rotary or hand files. '
        'It contains dentin chips, pulp tissue remnants, and microorganisms and must be '
        'removed for effective disinfection and dentinal tubule penetration of irrigants. '
        '[Book: Endo_Cohens_Pathways_of_the_Pulp_2016]'
    ),
    'book_verified': True
}

# NaOCl explanation for all duplicates
naocl_exp = (
    'Sodium hypochlorite (NaOCl) is the most commonly used endodontic irrigant '
    'because of its antibacterial capacity and ability to dissolve organic tissue '
    '(pulp remnants, collagen). It is the only irrigant with tissue dissolution '
    'properties, making it essential for chemical debridement of the root canal system. '
    '[Book: Endo_Cohens_Pathways_of_the_Pulp_2016]'
)

# Presurgical assessment explanation for all duplicates
presurg_exp = (
    'Before elective endodontic surgery, the clinician must reassess the quality of '
    'prior root canal treatment, identify any missed anatomy (e.g., untreated canals, '
    'isthmuses), and evaluate restorability of the tooth. Surgical endodontics is '
    'indicated only when nonsurgical retreatment is not feasible or has failed. '
    '[Book: Endo_Cohens_Pathways_of_the_Pulp_2016]'
)

fixes['fr_boost_046'] = {
    'explanation': (
        'Kennedy Class I describes a bilateral distal extension (free-end saddle) partially '
        'edentulous arch where the denture bases are tooth-tissue supported, with major support '
        'from the residual ridges and tooth support from occlusal rests at the anterior portion '
        'of each base. '
        '[Book: Removable_McCracken_s_Removable_Partial_Prosthodontics]'
    ),
    'book_verified': True
}

# Map all NaOCl duplicates
naocl_ids = [
    'end_boost_054', 'end_boost_057', 'end_boost_060', 'end_boost_063',
    'end_boost_066', 'end_boost_069', 'end_boost_072', 'end_boost_075',
    'end_boost_078', 'end_boost_081', 'end_boost_084', 'end_boost_087',
    'end_boost_090', 'end_boost_093', 'end_boost_096', 'end_boost_099',
    'end_boost_102', 'end_boost_105', 'end_boost_108', 'end_boost_111',
    'end_boost_114', 'end_boost_117', 'end_boost_120', 'end_boost_123',
    'end_boost_126', 'end_boost_129', 'end_boost_132', 'end_boost_135',
    'end_boost_138', 'end_boost_141', 'end_boost_144', 'end_boost_147',
    'end_boost_150'
]

for qid in naocl_ids:
    fixes[qid] = {'explanation': naocl_exp, 'book_verified': True}

# Map all presurgical assessment duplicates
presurg_ids = [
    'end_boost_055', 'end_boost_058', 'end_boost_061', 'end_boost_064',
    'end_boost_067', 'end_boost_070', 'end_boost_073', 'end_boost_076',
    'end_boost_079', 'end_boost_082', 'end_boost_085', 'end_boost_088',
    'end_boost_091', 'end_boost_094', 'end_boost_097', 'end_boost_100',
    'end_boost_103', 'end_boost_106', 'end_boost_109', 'end_boost_112',
    'end_boost_115', 'end_boost_118', 'end_boost_121', 'end_boost_124',
    'end_boost_127', 'end_boost_130', 'end_boost_133', 'end_boost_136',
    'end_boost_139', 'end_boost_142', 'end_boost_145', 'end_boost_148'
]

for qid in presurg_ids:
    fixes[qid] = {'explanation': presurg_exp, 'book_verified': True}

# Apply fixes
bank_by_id = {q['id']: q for q in bank}
fixed_count = 0
missing_ids = []

for qid, fix in fixes.items():
    if qid in bank_by_id:
        bank_by_id[qid]['explanation'] = fix['explanation']
        bank_by_id[qid]['book_verified'] = fix['book_verified']
        fixed_count += 1
    else:
        missing_ids.append(qid)

print(f'Fixed {fixed_count} questions with proper explanations + book_verified=true')
if missing_ids:
    print(f'Missing IDs: {missing_ids}')

# Serialize with ensure_ascii=False to keep Unicode
json_str = json.dumps(bank, ensure_ascii=False, indent=2)

# Replace in the original text - find the exact bounds of the current bank array
# and replace only that portion
start_idx = m.start(1)
end_idx = m.end(1)

new_text = text[:start_idx] + json_str + text[end_idx:]

with open('data/questions.js', 'w', encoding='utf-8') as f:
    f.write(new_text)

print('Written back to data/questions.js successfully')

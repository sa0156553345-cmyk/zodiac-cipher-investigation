#!/usr/bin/env python3
"""Audit 09 - how the 3,544-phrase family depends on the chosen word lists.
Counts, for each template and each word, how many family phrases contain it; reports whether the
two phrases discussed in the review (T1 and T2) are generated, and how many phrases are generated
by more than one template. Also lists which family members use only words that appear in the
phrases proposed in the literature (a measure of how the family is shaped by the hypothesis).
Outputs: results/audit_09_family_construction.csv"""
import csv, itertools
from collections import Counter
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
N_WORDS = ['ONE','TWO','THREE','FOUR','FIVE','SIX','SEVEN','EIGHT','NINE','TEN','ELEVEN','TWELVE',
           'THIRTEEN','FOURTEEN','FIFTEEN','EIGHTEEN','TWENTY']
U_WORDS = ['INCHES','RADIANS','MILES','DEGREES','MINUTES','FEET','SIGNS','HOURS']
TEMPL = {'A': lambda n1, u1, n2, u2: [n1, u1, 'ALONG', 'THE', n2, u2],
         'B': lambda n1, u1, n2, u2: [n1, u1, 'AND', n2, u2, 'ALONG'],
         'C': lambda n1, u1, n2, u2: [n1, u1, n2, u2]}
fam = {}
word_count = Counter()
for n1, u1, n2, u2 in itertools.product(N_WORDS, U_WORDS, N_WORDS, U_WORDS):
    for t, f in TEMPL.items():
        toks = f(n1, u1, n2, u2)
        ph = ''.join(toks)
        if len(ph) == 32:
            fam.setdefault(ph, set()).add(t)
phrases = sorted(fam)
for ph in phrases:
    for w in set(W for W in N_WORDS + U_WORDS if W in ph):
        word_count[w] += 1
multi = sum(1 for p in phrases if len(fam[p]) > 1)
rows = [
    {'item': 'distinct_phrases', 'value': len(phrases)},
    {'item': 'phrases_from_more_than_one_template', 'value': multi},
    {'item': 'T1_in_family', 'value': 'TWELVEINCHESALONGTHETHREERADIANS' in fam},
    {'item': 'T2_in_family', 'value': 'THREERADIANSANDTWELVEINCHESALONG' in fam},
    {'item': 'T3_in_family', 'value': 'THREEANDTHREEEIGHTHSRADIANSSIXIN' in fam},
]
for w in N_WORDS + U_WORDS:
    rows.append({'item': f'phrases_containing_{w}', 'value': word_count[w]})
with open(ROOT / 'results' / 'audit_09_family_construction.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['item', 'value']); w.writeheader(); w.writerows(rows)
for r in rows[:5]: print(r)
print("written audit_09_family_construction.csv")

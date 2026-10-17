#!/usr/bin/env python3
"""Literal phrase test: phrases are used exactly as written (letters only, no edits).
Input: results/valid_orders.json (34 valid orders). Output: results/literal_phrase_test.csv"""
import csv, json
from common import RESULTS, repeat_pairs, satisfied

PHRASES = {
    'T1_target_literal': 'TWELVEINCHESALONGTHETHREERADIANS',
    'T2_alternative_literal': 'THREERADIANSANDTWELVEINCHESALONG',
    'T3_proposed_literal': 'THREEANDTHREEEIGHTHSRADIANSSIXIN',
    'T4_foxon_text_with_2_edits': 'TWELVTINCHESALONGTHETHREERADIAAS',
}
for n, p in PHRASES.items(): assert len(p) == 32, n
orders = json.load(open(RESULTS / 'valid_orders.json', encoding='utf-8'))
paper = [o for o in orders if o['k'] == 2 and o['delta'] == 2 and o['wrap'] == 'W1' and o['emode'] == 'E2']
assert len(paper) == 1
with open(RESULTS / 'literal_phrase_test.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['phrase_name', 'phrase', 'order_id', 'is_paper_order', 'satisfied_pairs_of_3', 'all_3_satisfied'])
    summary = {}
    for name, ph in PHRASES.items():
        full = 0
        for o in orders:
            s = satisfied(ph, o['order']); ok = all(s)
            full += ok
            w.writerow([name, ph, o['id'], o['id'] == paper[0]['id'], sum(s), ok])
        summary[name] = full
print("orders in which the phrase appears with all 3 repeat constraints satisfied (of %d):" % len(orders))
for n, v in summary.items(): print(f"  {n:<30} {v}")
ps = satisfied(PHRASES['T1_target_literal'], paper[0]['order'])
print(f"paper order (k=2, delta=+2, W1, E2): T1 satisfies {sum(ps)}/3 pairs; per pair: {ps}")
print("written results/literal_phrase_test.csv")

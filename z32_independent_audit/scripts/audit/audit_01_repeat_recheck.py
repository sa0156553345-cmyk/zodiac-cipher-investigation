#!/usr/bin/env python3
"""Audit 01 - independent re-check of the repeat-constraint logic.
Does not import any pipeline function. For every valid order in results/valid_orders.json it
re-derives: permutation validity, multiset equality with the 32 input symbols, the repeated
symbol pairs (output positions), and the satisfied-pair count of each literal phrase.
Then it compares those counts with results/literal_phrase_test.csv (produced by the pipeline).
Output: results/audit_01_repeat_recheck.csv"""
import csv, json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
with open(ROOT / 'data' / 'z32_fig1A_transcription.csv', newline='', encoding='utf-8') as f:
    labs = sorted((int(r[0]), r[1]) for r in csv.reader(f) if r and r[0].isdigit())
assert [p for p, _ in labs] == list(range(1, 33))
SYM = [s for _, s in labs]

PHR = {
    'T1_target_literal': 'TWELVEINCHESALONGTHETHREERADIANS',
    'T2_alternative_literal': 'THREERADIANSANDTWELVEINCHESALONG',
    'T3_proposed_literal': 'THREEANDTHREEEIGHTHSRADIANSSIXIN',
    'T4_foxon_text_with_2_edits': 'TWELVTINCHESALONGTHETHREERADIAAS',
}
orders = json.load(open(ROOT / 'results' / 'valid_orders.json', encoding='utf-8'))
lit = {(r['phrase_name'], r['order_id']): int(r['satisfied_pairs_of_3'])
       for r in csv.DictReader(open(ROOT / 'results' / 'literal_phrase_test.csv', encoding='utf-8'))}

rows, discrepancies = [], 0
for o in orders:
    idx = o['order']
    perm_ok = sorted(idx) == list(range(32))
    out = [SYM[i] for i in idx]
    multiset_ok = Counter(out) == Counter(SYM)
    groups = {}
    for pos, s in enumerate(out):
        groups.setdefault(s, []).append(pos)
    pairs = sorted(tuple(g) for g in groups.values() if len(g) > 1)
    structure_ok = len(pairs) == 3 and all(len(p) == 2 for p in pairs)
    row = {'order_id': o['id'], 'is_permutation_of_32': perm_ok,
           'output_multiset_equals_input': multiset_ok, 'n_repeat_pairs': len(pairs),
           'repeat_pairs_output_positions_1based': ' '.join(f"({a + 1},{b + 1})" for a, b in pairs)}
    for name, ph in PHR.items():
        sat = sum(ph[a] == ph[b] for a, b in pairs)
        row[f'{name}_satisfied'] = sat
        ok = lit[(name, o['id'])] == sat
        row[f'{name}_matches_pipeline_csv'] = ok
        discrepancies += (not ok)
    discrepancies += (not (perm_ok and multiset_ok and structure_ok))
    rows.append(row)

out_path = ROOT / 'results' / 'audit_01_repeat_recheck.csv'
with open(out_path, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)
print(f"orders checked: {len(rows)}; discrepancies found: {discrepancies}")
print("written", out_path.name)

#!/usr/bin/env python3
"""Audit 10 - diagnostic of the composition-preserving null.
(a) For all 496 position pairs: the match rate of letters across the family, versus the rate the
    composition null predicts (sum_c n_c(n_c-1)/(32*31) averaged over the family). Ratios far from 1
    mean the family has position-specific structure that the composition null destroys.
(b) For each valid order: observed passes, the exact composition-null expectation (from audit_03),
    and the excess.
(c) Cancellation check: the excess of the two orders with the largest counts versus the deficit
    of the remaining orders.
This is a DIAGNOSTIC. It locates where the null is misspecified. It does not replace the test.
Outputs: results/audit_10_pair_match_rates.csv, results/audit_10_order_decomposition.csv,
         results/audit_10_summary.csv"""
import csv, itertools, json
from collections import Counter
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
N_WORDS = ['ONE','TWO','THREE','FOUR','FIVE','SIX','SEVEN','EIGHT','NINE','TEN','ELEVEN','TWELVE',
           'THIRTEEN','FOURTEEN','FIFTEEN','EIGHTEEN','TWENTY']
U_WORDS = ['INCHES','RADIANS','MILES','DEGREES','MINUTES','FEET','SIGNS','HOURS']
fam = set()
for n1, u1, n2, u2 in itertools.product(N_WORDS, U_WORDS, N_WORDS, U_WORDS):
    for toks in ([n1, u1, 'ALONG', 'THE', n2, u2], [n1, u1, 'AND', n2, u2, 'ALONG'], [n1, u1, n2, u2]):
        ph = ''.join(toks)
        if len(ph) == 32:
            fam.add(ph)
phrases = sorted(fam)
A = np.array([list(p) for p in phrases])
N = len(phrases)

comp_rate = np.array([sum(v * (v - 1) for v in Counter(p).values()) / (32 * 31) for p in phrases])
mean_comp = float(comp_rate.mean())
rows = []
for a in range(32):
    for b in range(a + 1, 32):
        obs = float((A[:, a] == A[:, b]).mean())
        rows.append({'pos_a_1based': a + 1, 'pos_b_1based': b + 1, 'observed_match_rate_family': round(obs, 5),
                     'composition_null_rate': round(mean_comp, 5),
                     'ratio_obs_over_null': round(obs / mean_comp, 3)})
rows.sort(key=lambda r: -r['ratio_obs_over_null'])
with open(ROOT / 'results' / 'audit_10_pair_match_rates.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print(f"(a) composition-null rate per pair = {mean_comp:.4f}; pairs with ratio > 2: {sum(1 for r in rows if r['ratio_obs_over_null'] > 2)} of {len(rows)};"
      f" ratio < 0.5: {sum(1 for r in rows if r['ratio_obs_over_null'] < 0.5)}")

SYM = [s for _, s in sorted((int(r[0]), r[1]) for r in csv.reader(open(ROOT / 'data' / 'z32_fig1A_transcription.csv', encoding='utf-8')) if r and r[0].isdigit())]
orders = json.load(open(ROOT / 'results' / 'valid_orders.json', encoding='utf-8'))
P = {}
for r in csv.DictReader(open(ROOT / 'results' / 'audit_03_exact_null_per_phrase.csv', encoding='utf-8')):
    P[r['phrase']] = float(r['exact_P_three_pairs_equal'])
expected_per_order = sum(P[p] for p in phrases)
dec = []
for o in orders:
    pos = {}
    for p, idx in enumerate(o['order']):
        pos.setdefault(SYM[idx], []).append(p)
    ps = [tuple(v) for v in pos.values() if len(v) > 1]
    obs = sum(all(ph[a] == ph[b] for a, b in ps) for ph in phrases)
    dec.append({'order_id': o['id'], 'fig1B_layout': o['fig1B_layout'], 'observed_passes': obs,
                'composition_null_expected': round(expected_per_order, 4),
                'excess': round(obs - expected_per_order, 3)})
dec.sort(key=lambda r: -r['observed_passes'])
with open(ROOT / 'results' / 'audit_10_order_decomposition.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(dec[0].keys())); w.writeheader(); w.writerows(dec)
top2 = dec[:2]; rest = dec[2:]
excess_top = sum(r['excess'] for r in top2)
excess_rest = sum(r['excess'] for r in rest)
print("(b) top orders:", [(r['order_id'], r['observed_passes']) for r in top2],
      f"expected each = {expected_per_order:.3f}")
print(f"(c) excess of top-2 orders = {excess_top:+.2f}; excess of remaining {len(rest)} orders = {excess_rest:+.2f}; total = {excess_top + excess_rest:+.2f}")
summary = [('composition_null_rate_per_pair', round(mean_comp, 5)),
           ('pairs_with_ratio_above_2', sum(1 for r in rows if r['ratio_obs_over_null'] > 2)),
           ('pairs_with_ratio_below_0.5', sum(1 for r in rows if r['ratio_obs_over_null'] < 0.5)),
           ('expected_passes_per_order_composition_null', round(expected_per_order, 4)),
           ('top2_orders', ' ; '.join(r['order_id'] for r in top2)),
           ('top2_excess', round(excess_top, 3)), ('remaining_orders_excess', round(excess_rest, 3)),
           ('total_excess', round(excess_top + excess_rest, 3))]
with open(ROOT / 'results' / 'audit_10_summary.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f); w.writerow(['quantity', 'value']); w.writerows(summary)
print("written audit_10 files")

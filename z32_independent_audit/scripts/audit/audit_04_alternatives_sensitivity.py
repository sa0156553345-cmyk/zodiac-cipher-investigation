#!/usr/bin/env python3
"""Audit 04 - sensitivity of the family test to the choice of orders.
Uses the same phrase family and the same composition null as the pipeline, but reports three order
subsets: all 34 orders (as in the pipeline), the 2 orders whose layout matches Fig.1(B) (k=2), and
the 32 remaining orders. For each subset: observed count, exact expectation (from audit_03), and a
Monte Carlo global p-value with the pipeline's seed (so the 34-order row should reproduce the
pipeline's result). Also reports per-order observed counts versus their exact expectations.
Outputs: results/audit_04_alternatives_sensitivity.csv, results/audit_04_per_order.csv"""
import csv, json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
with open(ROOT / 'data' / 'z32_fig1A_transcription.csv', newline='', encoding='utf-8') as f:
    labs = sorted((int(r[0]), r[1]) for r in csv.reader(f) if r and r[0].isdigit())
SYM = [s for _, s in labs]

orders = json.load(open(ROOT / 'results' / 'valid_orders.json', encoding='utf-8'))
def pairs_of(order):
    pos = {}
    for p, idx in enumerate(order):
        pos.setdefault(SYM[idx], []).append(p)
    return [tuple(v) for v in pos.values() if len(v) > 1]
pairsets = [pairs_of(o['order']) for o in orders]
assert all(len(ps) == 3 for ps in pairsets)
M = len(orders)

# phrase family (same definition as the pipeline; re-derived here)
N_WORDS = ['ONE','TWO','THREE','FOUR','FIVE','SIX','SEVEN','EIGHT','NINE','TEN','ELEVEN','TWELVE',
           'THIRTEEN','FOURTEEN','FIFTEEN','EIGHTEEN','TWENTY']
U_WORDS = ['INCHES','RADIANS','MILES','DEGREES','MINUTES','FEET','SIGNS','HOURS']
import itertools
fam = set()
for n1, u1, n2, u2 in itertools.product(N_WORDS, U_WORDS, N_WORDS, U_WORDS):
    for toks in ([n1, u1, 'ALONG', 'THE', n2, u2], [n1, u1, 'AND', n2, u2, 'ALONG'], [n1, u1, n2, u2]):
        ph = ''.join(toks)
        if len(ph) == 32:
            fam.add(ph)
phrases = sorted(fam)
P_exact = {}
with open(ROOT / 'results' / 'audit_03_exact_null_per_phrase.csv', encoding='utf-8') as f:
    for r in csv.DictReader(f):
        P_exact[r['phrase']] = float(r['exact_P_three_pairs_equal'])
sumP = sum(P_exact[p] for p in phrases)

# observed passes per (phrase, order)
passes = np.zeros((len(phrases), M), dtype=bool)
for i, ph in enumerate(phrases):
    for j, ps in enumerate(pairsets):
        passes[i, j] = all(ph[a] == ph[b] for a, b in ps)
per_order_obs = passes.sum(axis=0)

# Monte Carlo null with the pipeline's seed and procedure (per phrase, R = 2000 permutations)
R = 2000
rng = np.random.default_rng(20261011)
null_pass_total = np.zeros((R, M), dtype=int)
for ph in phrases:
    arr = np.array(list(ph))
    perms = np.argsort(rng.random((R, 32)), axis=1)
    S = arr[perms]
    for j, ps in enumerate(pairsets):
        ok = np.ones(R, dtype=bool)
        for a, b in ps:
            ok &= (S[:, a] == S[:, b])
        null_pass_total[:, j] += ok

subsets = {
    'all_34_orders (pipeline)': list(range(M)),
    'paper_layout_k2_orders (2)': [j for j, o in enumerate(orders) if o['fig1B_layout']],
    'non_paper_layout_orders (32)': [j for j, o in enumerate(orders) if not o['fig1B_layout']],
}
rows = []
for name, cols in subsets.items():
    O = int(passes[:, cols].sum())
    null_tot = null_pass_total[:, cols].sum(axis=1)
    rows.append({'subset': name, 'n_orders': len(cols), 'observed_passes_O': O,
                 'exact_expected_under_null': round(len(cols) * sumP, 4),
                 'MC_null_mean': round(float(null_tot.mean()), 4),
                 'MC_null_sd': round(float(null_tot.std()), 4),
                 'MC_global_p_ge_O': round(float((null_tot >= O).mean()), 4), 'R': R})
with open(ROOT / 'results' / 'audit_04_alternatives_sensitivity.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
for r in rows:
    print(r)

per_order_rows = []
for j, o in enumerate(orders):
    per_order_rows.append({'order_id': o['id'], 'fig1B_layout': o['fig1B_layout'],
                           'observed_passes': int(per_order_obs[j]),
                           'exact_expected_passes': round(sumP, 6),
                           'MC_mean_passes': round(float(null_pass_total[:, j].mean()), 4)})
with open(ROOT / 'results' / 'audit_04_per_order.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(per_order_rows[0].keys())); w.writeheader(); w.writerows(per_order_rows)
print("written audit_04_alternatives_sensitivity.csv and audit_04_per_order.csv")

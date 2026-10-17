#!/usr/bin/env python3
"""Pre-registered alternative-phrase family with a composition-preserving permutation null.
Specification: docs/PREREGISTRATION.md (fixed before this script was run).
Output: results/alternatives_summary.csv, results/alternatives_candidates.csv (phrases passing >= 1 order)"""
import csv, json, itertools
import numpy as np
from common import RESULTS, repeat_pairs, SYMS

N_WORDS = ['ONE','TWO','THREE','FOUR','FIVE','SIX','SEVEN','EIGHT','NINE','TEN','ELEVEN','TWELVE',
           'THIRTEEN','FOURTEEN','FIFTEEN','EIGHTEEN','TWENTY']
U_WORDS = ['INCHES','RADIANS','MILES','DEGREES','MINUTES','FEET','SIGNS','HOURS']
def templates(n1, u1, n2, u2):
    yield 'A', [n1, u1, 'ALONG', 'THE', n2, u2]
    yield 'B', [n1, u1, 'AND', n2, u2, 'ALONG']
    yield 'C', [n1, u1, n2, u2]

family = {}
for n1, u1, n2, u2 in itertools.product(N_WORDS, U_WORDS, N_WORDS, U_WORDS):
    for tname, toks in templates(n1, u1, n2, u2):
        ph = ''.join(toks)
        if len(ph) == 32:
            family.setdefault(ph, []).append(tname)
phrases = sorted(family)
N = len(phrases)
print("family size N (distinct 32-letter phrases):", N)
assert 'TWELVEINCHESALONGTHETHREERADIANS' in family and 'THREERADIANSANDTWELVEINCHESALONG' in family

orders = json.load(open(RESULTS / 'valid_orders.json', encoding='utf-8'))
pairsets = [repeat_pairs(o['order']) for o in orders]
M = len(orders)
assert all(len(p) == 3 for p in pairsets)

def count_pass(letters_matrix):
    """letters_matrix: (R, 32) array of letters. Returns (R, M) boolean pass matrix."""
    out = np.zeros((letters_matrix.shape[0], M), dtype=bool)
    for j, ps in enumerate(pairsets):
        ok = np.ones(letters_matrix.shape[0], dtype=bool)
        for a, b in ps:
            ok &= (letters_matrix[:, a] == letters_matrix[:, b])
        out[:, j] = ok
    return out

R = 2000
rng = np.random.default_rng(20261011)
obs_count = {}
null_total = np.zeros(R, dtype=int)
per_phrase = []
for ph in phrases:
    arr = np.array(list(ph))
    obs = count_pass(arr[None, :])[0]
    oc = int(obs.sum()); obs_count[ph] = oc
    perms = np.argsort(rng.random((R, 32)), axis=1)
    null_pass = count_pass(arr[perms])
    null_c = null_pass.sum(axis=1)
    null_total += null_c
    p_phrase = float((null_c >= oc).mean())
    per_phrase.append((ph, oc, p_phrase, ','.join(sorted(set(family[ph])))))

O = sum(obs_count.values())
p_global = float((null_total >= O).mean())
print(f"orders M = {M}; observed passes O = {O} (phrase, order) pairs")
print(f"null total: mean = {null_total.mean():.3f}, sd = {null_total.std():.3f}, max = {null_total.max()}")
print(f"global p (family-wide excess) = {p_global:.4f}  (R = {R}; resolution 1/{R})")
phrases_any = sum(1 for _, oc, _, _ in per_phrase if oc > 0)
print(f"phrases passing in >= 1 order: {phrases_any} of {N}")
per_phrase.sort(key=lambda t: (-t[1], t[2]))
best = per_phrase[0]
print(f"best observed: {best[0]} passes {best[1]} orders; per-phrase p = {best[2]:.4f}; Bonferroni p = {min(1, N*best[2]):.3f}")

with open(RESULTS / 'alternatives_summary.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['quantity', 'value'])
    for k_, v_ in [('family_size_N', N), ('valid_orders_M', M), ('observed_passes_O', O),
                   ('null_total_mean', round(float(null_total.mean()), 4)), ('null_total_sd', round(float(null_total.std()), 4)),
                   ('global_p_family_excess', p_global), ('phrases_passing_in_at_least_one_order', phrases_any),
                   ('permutations_per_phrase_R', R), ('bonferroni_factor', N)]:
        w.writerow([k_, v_])
with open(RESULTS / 'alternatives_candidates.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['phrase', 'template', 'orders_passing_of_34', 'per_phrase_p_perm', 'bonferroni_p'])
    for ph, oc, p, tmpl in per_phrase:
        if oc > 0:
            w.writerow([ph, tmpl, oc, round(p, 5), round(min(1, N * p), 5)])
print("written alternatives_summary.csv and alternatives_candidates.csv")

#!/usr/bin/env python3
"""Audit 03 - exact null probabilities of the composition-preserving permutation null.
For a 32-letter phrase with letter counts n_c, and three disjoint position pairs, the probability
(under a uniform random arrangement of its letters) that every pair holds equal letters is
  P = sum over ordered triples (c1,c2,c3) of  26! * prod_c n_c! / ( 32! * prod_c (n_c - 2 k_c)! )
where k_c is the number of pairs assigned letter c. Exchangeability makes P independent of which
disjoint positions are paired, so every valid order (3 disjoint pairs) has the same P.
Also re-derives the family of 3544 phrases independently and checks the Monte Carlo implementation.
Outputs: results/audit_03_exact_null_per_phrase.csv, results/audit_03_exact_null_summary.csv,
         results/audit_03_mc_check.csv"""
import csv, itertools, math
from collections import Counter
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
N_WORDS = ['ONE','TWO','THREE','FOUR','FIVE','SIX','SEVEN','EIGHT','NINE','TEN','ELEVEN','TWELVE',
           'THIRTEEN','FOURTEEN','FIFTEEN','EIGHTEEN','TWENTY']
U_WORDS = ['INCHES','RADIANS','MILES','DEGREES','MINUTES','FEET','SIGNS','HOURS']

def templates(n1, u1, n2, u2):
    yield 'A', [n1, u1, 'ALONG', 'THE', n2, u2]
    yield 'B', [n1, u1, 'AND', n2, u2, 'ALONG']
    yield 'C', [n1, u1, n2, u2]

raw_per_template = Counter()
fam = {}
for n1, u1, n2, u2 in itertools.product(N_WORDS, U_WORDS, N_WORDS, U_WORDS):
    for t, toks in templates(n1, u1, n2, u2):
        ph = ''.join(toks)
        if len(ph) == 32:
            raw_per_template[t] += 1
            fam.setdefault(ph, set()).add(t)
phrases = sorted(fam)
print("raw 32-letter token strings per template:", dict(raw_per_template))
max_len_C = max(len(''.join([n1, u1, n2, u2])) for n1, u1, n2, u2 in itertools.product(N_WORDS, U_WORDS, N_WORDS, U_WORDS))
print("longest possible template-C phrase (letters):", max_len_C, "| template C produces phrases:", raw_per_template.get('C', 0) > 0)
print("distinct phrases:", len(phrases), "| phrases from more than one template:", sum(1 for p in phrases if len(fam[p]) > 1))

def p_three_pairs(phrase):
    cnt = Counter(phrase)
    lg = math.lgamma
    base = lg(27) - lg(33) + sum(lg(n + 1) for n in cnt.values())     # log(26!) - log(32!) + sum log(n_c!)
    letters = [c for c, n in cnt.items() if n >= 2]
    tot = 0.0
    for trip in itertools.combinations_with_replacement(letters, 3):
        k = Counter(trip)
        if any(2 * v > cnt[c] for c, v in k.items()):
            continue
        mult = len(set(itertools.permutations(trip)))                 # number of ordered triples
        term = base - sum(lg(cnt[c] - 2 * k.get(c, 0) + 1) for c in cnt)
        tot += mult * math.exp(term)
    return tot

per = []
for ph in phrases:
    per.append((ph, p_three_pairs(ph)))
sumP = sum(p for _, p in per)
out = ROOT / 'results' / 'audit_03_exact_null_per_phrase.csv'
with open(out, 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['phrase', 'templates', 'exact_P_three_pairs_equal', 'expected_passes_over_34_orders'])
    for ph, p in per:
        w.writerow([ph, ''.join(sorted(fam[ph])), f"{p:.10e}", f"{34 * p:.10e}"])

# Monte Carlo check of the exact formula on a random sample of phrases
rng = np.random.default_rng(12345)
sample_idx = rng.choice(len(per), size=200, replace=False)
mc_rows = []
for i in sample_idx:
    ph, p_exact = per[i]
    arr = np.array(list(ph))
    perms = np.argsort(rng.random((20000, 32)), axis=1)
    S = arr[perms]
    ok = (S[:, 0] == S[:, 1]) & (S[:, 2] == S[:, 3]) & (S[:, 4] == S[:, 5])
    k = int(ok.sum()); lam = p_exact * 20000
    z = (k - lam) / math.sqrt(max(lam * (1 - p_exact), 1e-12))   # binomial z with the EXACT p as the null
    mc_rows.append({'phrase': ph, 'exact': p_exact, 'mc_count_of_20000': k,
                    'expected_count_exact': round(lam, 4), 'z_vs_exact': round(z, 4)})
with open(ROOT / 'results' / 'audit_03_mc_check.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(mc_rows[0].keys())); w.writeheader(); w.writerows(mc_rows)
zs = np.array([r['z_vs_exact'] for r in mc_rows])
print(f"MC vs exact on 200 phrases (binomial z with exact p): mean z = {zs.mean():.3f}, sd z = {zs.std():.3f}, max |z| = {np.abs(zs).max():.3f}")

# summary against the pipeline's Monte Carlo mean
pipe_mean = None
for r in csv.DictReader(open(ROOT / 'results' / 'alternatives_summary.csv', encoding='utf-8')):
    if r['quantity'] == 'null_total_mean':
        pipe_mean = float(r['value'])
summary = [
    ('distinct_phrases_N', len(phrases)),
    ('sum_of_exact_P', f"{sumP:.8f}"),
    ('exact_expected_total_34_orders', f"{34 * sumP:.4f}"),
    ('exact_expected_total_2_paper_orders', f"{2 * sumP:.4f}"),
    ('pipeline_MC_null_mean_34_orders', pipe_mean),
]
with open(ROOT / 'results' / 'audit_03_exact_null_summary.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f); w.writerow(['quantity', 'value']); w.writerows(summary)
for q, v in summary:
    print(f"{q}: {v}")

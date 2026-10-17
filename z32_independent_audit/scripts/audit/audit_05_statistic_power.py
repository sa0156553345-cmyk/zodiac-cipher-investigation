#!/usr/bin/env python3
"""Audit 05 - what the family statistic can and cannot detect.
The statistic O = number of (phrase, order) pairs whose repeat constraints all hold.
Its value depends only on the phrase family and the repeat structure of the orders, not on the
symbol names. Therefore, if a true phrase exists in the family and its true order is one of the
34, that pair is already counted in O; it does not change O. The script shows (a) O is unchanged
when symbol names are relabelled, (b) the O needed to reach p < 0.05 and p < 0.01 under the null,
(c) how far O must move to be significant (compared with the change one true pair could cause).
Outputs: results/audit_05_statistic_power.csv"""
import csv, json, itertools, random
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[2]
with open(ROOT / 'data' / 'z32_fig1A_transcription.csv', newline='', encoding='utf-8') as f:
    labs = sorted((int(r[0]), r[1]) for r in csv.reader(f) if r and r[0].isdigit())
SYM = [s for _, s in labs]
orders = json.load(open(ROOT / 'results' / 'valid_orders.json', encoding='utf-8'))

def pairs_of(sym, order):
    pos = {}
    for p, idx in enumerate(order):
        pos.setdefault(sym[idx], []).append(p)
    return [tuple(v) for v in pos.values() if len(v) > 1]

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

def O_count(sym):
    pairsets = [pairs_of(sym, o['order']) for o in orders]
    return sum(all(ph[a] == ph[b] for a, b in ps) for ph in phrases for ps in pairsets)

O0 = O_count(SYM)
# (a) relabel symbol names (identity classes unchanged): O must be identical
rng = random.Random(7)
names = sorted(set(SYM))
mapping = dict(zip(names, rng.sample(names, len(names))))
relabel_ok = all(O_count([mapping[s] for s in SYM]) == O0 for _ in range(1))
print(f"O (pipeline family, 34 orders) = {O0}; unchanged after relabelling names: {relabel_ok}")

# (b) null distribution of O from the composition-preserving null (large R for stable tails)
R = 20000
rng_np = np.random.default_rng(99)
pairsets = [pairs_of(SYM, o['order']) for o in orders]
null_tot = np.zeros(R, dtype=int)
for ph in phrases:
    arr = np.array(list(ph))
    perms = np.argsort(rng_np.random((R, 32)), axis=1)
    S = arr[perms]
    cnt = np.zeros(R, dtype=int)
    for ps in pairsets:
        ok = np.ones(R, dtype=bool)
        for a, b in ps:
            ok &= (S[:, a] == S[:, b])
        cnt += ok
    null_tot += cnt
mu, sd = null_tot.mean(), null_tot.std()
rows = []
for O in [O0, O0 + 1, O0 + 5, O0 + 10]:
    rows.append({'O': O, 'p_global': round(float((null_tot >= O).mean()), 5), 'z': round((O - mu) / sd, 3)})
thr05 = int(np.percentile(null_tot, 95)) + 1
thr01 = int(np.percentile(null_tot, 99)) + 1
rows.append({'O': f'threshold_p<0.05 = {thr05}', 'p_global': '', 'z': ''})
rows.append({'O': f'threshold_p<0.01 = {thr01}', 'p_global': '', 'z': ''})
rows.append({'O': f'null_mean = {mu:.3f}', 'p_global': f'null_sd = {sd:.3f}', 'z': f'R = {R}'})
with open(ROOT / 'results' / 'audit_05_statistic_power.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['O', 'p_global', 'z']); w.writeheader(); w.writerows(rows)
for r in rows:
    print(r)
print(f"one true (phrase, order) pair can move O by at most 1 (and only if it was not already counted);"
      f" significance at p<0.05 requires O >= {thr05}, i.e. {thr05 - O0} more passes than observed.")

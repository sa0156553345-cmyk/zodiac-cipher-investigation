#!/usr/bin/env python3
"""
Independent audit of the structural statistic for Z32 (repetition test only).
Definitions:
  S2   = number of identities occurring EXACTLY twice      (literal reading of PREREG: 'appears twice')
  Sge2 = number of identities occurring TWO OR MORE times  (what the earlier code computed: v >= 2)
  MAX  = maximum multiplicity
Exact methods:
  (U) uniform model, 32 i.i.d. draws from A symbols: integer partitions of 32 with Fractions (exact).
  (E) English-homophone model (26 letters x k homophones, letter ~ GPL-2 frequencies):
      i.i.d. draws over 26k symbols with cell probabilities q=p_letter/k; exponential-generating-function
      dynamic programme in floats (all terms positive, so no cancellation).
Monte Carlo: 1,000,000 trials per model, fixed seed, vectorised; checked against a reference Counter implementation.
"""
import math, csv, json, time
from fractions import Fraction
from collections import Counter
import numpy as np

import os as _os
PKG = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..', 'z32_independent_audit')
GPL2 = '/usr/share/common-licenses/GPL-2'
N = 32
SEED = 20261012
NMC = 1_000_000
A_LIST = [29, 54, 63, 100, 165, 250, 500]
K_LIST = [1, 2, 3, 5, 8, 10, 15, 20]
ALPHA_TAIL = 0.025          # registered: P(S<=3)>=0.025 and P(S>=3)>=0.025
S_OBS_REGISTERED = 3
t0 = time.time()
fact = [math.factorial(i) for i in range(501)]

# ---------- reference statistics (per sequence; slow but unambiguous) ----------
def S2_ref(labels):   return sum(1 for v in Counter(labels).values() if v == 2)
def Sge2_ref(labels): return sum(1 for v in Counter(labels).values() if v >= 2)
def MAX_ref(labels):  return max(Counter(labels).values())

# ---------- observed Z32 sequence (identities as printed; NOT original glyphs) ----------
rows = [r for r in csv.DictReader(open(f'{PKG}/data/z32_fig1A_transcription.csv', encoding='utf-8'))
        if (r.get('position') or '').isdigit()]
obs = [r['symbol_as_printed'] for r in sorted(rows, key=lambda r: int(r['position']))]
assert len(obs) == N
OBS = dict(S2=S2_ref(obs), Sge2=Sge2_ref(obs), MAX=MAX_ref(obs), D=len(set(obs)),
           pattern=sorted([v for v in Counter(obs).values() if v >= 2], reverse=True))
print('[OBS] same functions applied to the observed sequence:', OBS)

# ---------- vectorised statistics, checked against the reference ----------
def stats_vec(X):
    Sx = np.sort(X, axis=1)
    eq = Sx[:, 1:] == Sx[:, :-1]                     # (n, 31)
    E = np.zeros((X.shape[0], N+1), dtype=bool)      # (n, 33), padded
    E[:, 1:N] = eq
    mid = E[:, 1:N]; left = E[:, 0:N-1]; right = E[:, 2:N+1]
    s2 = (mid & ~left & ~right).sum(axis=1)          # runs of length 1  -> identities seen exactly twice
    sge2 = (E[:, 1:] & ~E[:, :-1]).sum(axis=1)       # runs of length>=1 -> identities seen >=2 times
    has_triple = (E[:, 1:] & E[:, :-1]).any(axis=1)  # two consecutive equal neighbours <=> some identity seen >=3 times
    return s2, sge2, has_triple

def check_vectorised(draw, n=3000):
    X = draw(n)
    s2, sge2, has3 = stats_vec(X)
    for i in range(n):
        lab = X[i].tolist()
        assert s2[i] == S2_ref(lab) and sge2[i] == Sge2_ref(lab), (i, lab)
        assert bool(has3[i]) == (MAX_ref(lab) >= 3), (i, lab)
    return True

# ---------- exact (U): uniform model via integer partitions ----------
def partitions(n, maxpart=None):
    if maxpart is None: maxpart = n
    if n == 0: yield []; return
    for p in range(min(n, maxpart), 0, -1):
        for rest in partitions(n-p, p):
            yield [p] + rest
PARTS = list(partitions(N))
assert len(PARTS) == 8349

def uniform_exact(A):
    denom = A**N
    d_s2 = Counter(); d_sge2 = Counter(); d_max = Counter(); d_joint = Counter(); d_joint_g = Counter()
    total = Fraction(0)
    for lam in PARTS:                       # lam sorted descending
        m = len(lam)
        if m > A: continue
        mult = Counter(lam)
        den = fact[A-m]
        for aj in mult.values(): den *= fact[aj]
        ways_sym = fact[A] // den           # A!/((A-m)! * prod a_j!)  (exact integer)
        ways_seq = fact[N]
        for x in lam: ways_seq //= fact[x]  # N!/prod lam_i!
        p = Fraction(ways_sym * ways_seq, denom)
        s2 = mult.get(2, 0); sge2 = m - mult.get(1, 0); mx = lam[0]
        d_s2[s2] += p; d_sge2[sge2] += p; d_max[mx] += p; d_joint[(s2, mx <= 2)] += p; d_joint_g[(sge2, mx <= 2)] += p
        total += p
    assert total == 1, total
    E_s2 = sum(k*v for k, v in d_s2.items()); E_sge2 = sum(k*v for k, v in d_sge2.items())
    # closed forms (derived in report)
    cf_s2 = Fraction(496*(A-1)**30, A**31)
    cf_sge2 = A - Fraction((A-1)**32 + 32*(A-1)**31, A**31)
    assert E_s2 == cf_s2 and E_sge2 == cf_sge2, (E_s2, cf_s2, E_sge2, cf_sge2)
    tail = lambda d, cond: sum(v for k, v in d.items() if cond(k))
    return dict(
        E_S2=float(E_s2), E_Sge2=float(E_sge2),
        P_S2_le3=float(tail(d_s2, lambda k: k <= 3)), P_S2_ge3=float(tail(d_s2, lambda k: k >= 3)),
        P_S2_eq3=float(tail(d_s2, lambda k: k == 3)),
        P_S2_le3_max_le2=float(sum(v for (s,mx),v in d_joint.items() if s <= 3 and mx)),
        P_Sge2_le3=float(tail(d_sge2, lambda k: k <= 3)), P_Sge2_ge3=float(tail(d_sge2, lambda k: k >= 3)),
        P_Sge2_le3_max_le2=float(sum(v for (s,mx),v in d_joint_g.items() if s <= 3 and mx)),
        P_MAX_le2=float(tail(d_max, lambda k: k <= 2)),
        P_S2_eq3_max_le2=float(sum(v for (s,mx),v in d_joint.items() if s == 3 and mx)),
        exact_fraction_P_S2_le3=str(tail(d_s2, lambda k: k <= 3)),
        exact_fraction_P_Sge2_le3=str(tail(d_sge2, lambda k: k <= 3)),
        _d_s2={int(k): float(v) for k,v in d_s2.items()}, _d_sge2={int(k): float(v) for k,v in d_sge2.items()})

# ---------- exact (E): English-homophone model via EGF dynamic programme ----------
def letter_probs(path):
    s = open(path, encoding='utf-8', errors='ignore').read().upper()
    v = np.array([ord(c)-65 for c in s if 'A' <= c <= 'Z'])
    return np.bincount(v, minlength=26) / len(v)
P_EN = letter_probs(GPL2)

def dp_dist(qs, stat):
    U = 17
    P = np.zeros((N+1, U+1)); P[0, 0] = 1.0
    for q in qs:
        new = np.zeros_like(P)
        for c in range(0, N+1):
            if c == 0:   w, mark = 1.0, 0
            elif c == 1: w, mark = q, 0
            else:
                w = q**c / fact[c]
                if stat == 'S2':   mark = 1 if c == 2 else 0
                else:              mark = 1           # Sge2: any count >= 2
            if mark == 0: new[c:, :] += w * P[:N+1-c, :]
            else:         new[c:, 1:] += w * P[:N+1-c, :-1]
        P = new
    return P[N, :] * float(fact[N])        # distribution of the marked count

def english_exact(k):
    qs = [P_EN[l] / k for l in range(26) for _ in range(k)]
    d2 = dp_dist(qs, 'S2'); dge = dp_dist(qs, 'Sge2')
    E2 = float(sum(i*d2[i] for i in range(len(d2)))); Eg = float(sum(i*dge[i] for i in range(len(dge))))
    return dict(E_S2=E2, E_Sge2=Eg, P_S2_le3=float(d2[:4].sum()), P_S2_ge3=float(d2[3:].sum()),
                P_S2_eq3=float(d2[3]), P_Sge2_le3=float(dge[:4].sum()), P_Sge2_ge3=float(dge[3:].sum()),
                mass_S2=float(d2.sum()), mass_Sge2=float(dge.sum()),
                _d_s2={i: float(d2[i]) for i in range(len(d2)) if d2[i] > 0},
                _d_sge2={i: float(dge[i]) for i in range(len(dge)) if dge[i] > 0})

# ---------- cross-validation of the DP against the exact partition result (A=29) ----------
ex29 = uniform_exact(29)
dp29_s2 = dp_dist([1/29]*29, 'S2'); dp29_sge = dp_dist([1/29]*29, 'Sge2')
max_dev = max(abs(dp29_s2[i] - ex29['_d_s2'].get(i, 0.0)) for i in range(len(dp29_s2)))
max_dev2 = max(abs(dp29_sge[i] - ex29['_d_sge2'].get(i, 0.0)) for i in range(len(dp29_sge)))
print(f"[CHECK] DP vs exact partition (A=29): max |diff| S2={max_dev:.2e}, Sge2={max_dev2:.2e}")

# ---------- Monte Carlo (1,000,000 trials per model, fixed seed) ----------
def mc(kind, param, idx):
    rng = np.random.default_rng(SEED + 1000*idx)
    if kind == 'uniform':
        def draw(n): return rng.integers(0, param, size=(n, N))
    else:
        cdf = np.cumsum(P_EN)
        def draw(n):
            letters = np.minimum(np.searchsorted(cdf, rng.random((n, N)), side='right'), 25)
            return letters * param + rng.integers(0, param, size=(n, N))
    assert check_vectorised(draw), 'vectorised statistic disagrees with reference'
    c2 = np.zeros(N+1, np.int64); cg = np.zeros(N+1, np.int64); c3plus = 0
    done = 0; chunk = 200_000
    while done < NMC:
        n = min(chunk, NMC - done)
        s2, sge2, _has3 = stats_vec(draw(n))
        c2 += np.bincount(s2, minlength=N+1); cg += np.bincount(sge2, minlength=N+1)
        done += n
    return c2, cg

results = {}
models = [('uniform', A) for A in A_LIST] + [('english', k) for k in K_LIST]
for idx, (kind, par) in enumerate(models):
    name = f'uniform_A={par}' if kind == 'uniform' else f'english_k={par}'
    ex = uniform_exact(par) if kind == 'uniform' else english_exact(par)
    c2, cg = mc(kind, par, idx)
    mc2_le3 = c2[:4].sum()/NMC; mc2_ge3 = c2[3:].sum()/NMC
    mcg_le3 = cg[:4].sum()/NMC; mcg_ge3 = cg[3:].sum()/NMC
    se = lambda p: math.sqrt(max(p*(1-p), 1e-300)/NMC)
    cons_reg = bool(ex['P_S2_le3'] >= ALPHA_TAIL and ex['P_S2_ge3'] >= ALPHA_TAIL)
    cons_cod = bool(ex['P_Sge2_le3'] >= ALPHA_TAIL and ex['P_Sge2_ge3'] >= ALPHA_TAIL)
    results[name] = dict(
        exact={k: v for k, v in ex.items() if not k.startswith('_') and not k.startswith('exact_fraction')},
        mc=dict(P_S2_le3=float(mc2_le3), P_S2_ge3=float(mc2_ge3), P_Sge2_le3=float(mcg_le3), P_Sge2_ge3=float(mcg_ge3),
                zero_hits_S2_le3=int(c2[:4].sum()), zero_hits_Sge2_le3=int(cg[:4].sum()),
                E_S2=float((np.arange(N+1)*c2).sum()/NMC), E_Sge2=float((np.arange(N+1)*cg).sum()/NMC),
                se_P_S2_le3=se(float(mc2_le3)), se_P_Sge2_le3=se(float(mcg_le3))),
        decision_registered_S2=cons_reg, decision_coded_Sge2=cons_cod)
    e = results[name]['exact']; m = results[name]['mc']
    print(f"[{name:16s}] exact E[S2]={e['E_S2']:.4f} E[Sge2]={e['E_Sge2']:.4f} | "
          f"P(S2<=3)={e['P_S2_le3']:.6g} P(S2>=3)={e['P_S2_ge3']:.6g} | "
          f"MC P(S2<=3)={m['P_S2_le3']:.6g}(+-{m['se_P_S2_le3']:.1e}) | "
          f"P(Sge2<=3)={e['P_Sge2_le3']:.6g} P(Sge2>=3)={e['P_Sge2_ge3']:.6g} | "
          f"REG={'consistent' if cons_reg else 'rejected'} CODED={'consistent' if cons_cod else 'rejected'}")

out = dict(observed=OBS, seed=SEED, nmc=NMC, alpha_tail=ALPHA_TAIL, check_dp_vs_exact_A29=dict(S2=max_dev, Sge2=max_dev2),
           closed_forms=dict(E_S2='496*(A-1)^30 / A^31', E_Sge2='A - [(A-1)^32 + 32*(A-1)^31] / A^31'),
           results=results, elapsed_s=time.time()-t0)
json.dump(out, open('results_structure_audit.json', 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print(f"[DONE] elapsed {time.time()-t0:.1f}s; wrote results_structure_audit.json")

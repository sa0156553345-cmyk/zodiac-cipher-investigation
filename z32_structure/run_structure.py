"""Pre-registered tests (PREREG_structure.md). Independent code; reads only the package transcription and GPL texts."""
import math, json, csv, time
import numpy as np
from collections import Counter
import os as _os
PKG = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', 'z32_independent_audit')
rng = np.random.default_rng(20261012)
t0 = time.time()

def load_letters(path):
    s = open(path, encoding='utf-8', errors='ignore').read().upper()
    return np.array([ord(c)-65 for c in s if 'A' <= c <= 'Z'])
L2 = load_letters('/usr/share/common-licenses/GPL-2')   # language model + letter distribution
L3 = load_letters('/usr/share/common-licenses/GPL-3')   # control plaintext (not used for model)
freq = np.bincount(L2, minlength=26) / len(L2)
BI = np.zeros((26,26)); np.add.at(BI, (L2[:-1], L2[1:]), 1)
LP = np.log((BI+0.5)/(BI+0.5).sum(axis=1, keepdims=True))

# ---------- observed identities (printed, typeset ASCII; NOT original glyphs) ----------
rows = [r for r in csv.DictReader(open(f'{PKG}/data/z32_fig1A_transcription.csv', encoding='utf-8')) if (r.get('position') or '').isdigit()]
sym = {int(r['position']): r['symbol_as_printed'] for r in rows}
uniq = {s:i for i,s in enumerate(sorted(set(sym.values())))}
K_OBS = len(uniq)
O1 = list(range(1,33)); O2 = list(range(1,18)) + list(range(32,17,-1))
O3 = []
for c in range(1,18):
    O3.append(c)
    if c <= 15: O3.append(17+c)
O4 = list(range(32,0,-1))
ORDERS = {'O1_printed':O1, 'O2_zigzag':O2, 'O3_columns':O3, 'O4_reversed':O4}
for k,o in ORDERS.items(): assert sorted(o)==list(range(1,33)), k
seq_of = {k: np.array([uniq[sym[p]] for p in o]) for k,o in ORDERS.items()}
mult = Counter(sym.values())
print(f"[DATA] distinct identities = {K_OBS}; repeated identities = {sum(1 for v in mult.values() if v>=2)}; "
      f"max multiplicity = {max(mult.values())}; pattern = {sorted([v for v in mult.values() if v>=2])}")

# ---------- Part A: structural test ----------
R_OBS = sum(1 for v in mult.values() if v >= 2)
def R_of(labels):
    c = Counter(labels); return sum(1 for v in c.values() if v >= 2)
def sim_uniform(A, n=20000):
    return np.array([R_of(rng.integers(0, A, size=32)) for _ in range(n)])
def sim_homophone(k, n=20000):
    out = []
    for _ in range(n):
        letters = rng.choice(26, size=32, p=freq)
        h = rng.integers(0, k, size=32)
        out.append(R_of(letters*k + h))
    return np.array(out)
structural = {}
for A in [29, 54, 63, 100, 165, 250, 500]:
    r = sim_uniform(A)
    structural[f'uniform_A={A}'] = dict(P_R_le=float((r<=R_OBS).mean()), P_R_ge=float((r>=R_OBS).mean()), mean_R=float(r.mean()))
for k in [1,2,3,5,8,10,15,20]:
    r = sim_homophone(k)
    structural[f'english_homophone_k={k}'] = dict(P_R_le=float((r<=R_OBS).mean()), P_R_ge=float((r>=R_OBS).mean()), mean_R=float(r.mean()))
for name, d in structural.items():
    d['consistent'] = bool(d['P_R_le'] >= 0.025 and d['P_R_ge'] >= 0.025)
    print(f"[STRUCT] {name:24s} E[R]={d['mean_R']:6.2f}  P(R<=3)={d['P_R_le']:.4f}  P(R>=3)={d['P_R_ge']:.4f}  consistent={d['consistent']}")
cons = [n for n,d in structural.items() if d['consistent']]
print(f"[STRUCT] consistent models: {cons}")

# ---------- Part B: readability search with permutation null ----------
def score_map(m, seq):
    return LP[m[seq[:-1]], m[seq[1:]]].sum()
def anneal(seq, K, steps=6000, restarts=2):
    best_all = -1e18
    for _ in range(restarts):
        m = rng.integers(0, 26, size=K)
        cur = score_map(m, seq); best = cur
        for t in range(steps):
            T = 2.0*(0.01/2.0)**(t/steps)
            j = rng.integers(K); new = rng.integers(26); old = m[j]
            if new == old: continue
            m[j] = new
            sc = score_map(m, seq)
            if sc >= cur or rng.random() < math.exp((sc-cur)/T):
                cur = sc
                if cur > best: best = cur
            else:
                m[j] = old
        best_all = max(best_all, best)
    return best_all/(len(seq)-1)
def perm_null(seq, K, n):
    return np.array([anneal(rng.permutation(seq), K) for _ in range(n)])

N_NULL = 150
readability = {}
null_z32 = perm_null(seq_of['O1_printed'], K_OBS, N_NULL)   # permutations of the same identities
print(f"[READ] Z32 permutation null (n={N_NULL}): mean={null_z32.mean():.4f}, sd={null_z32.std():.4f}, 95%={np.percentile(null_z32,95):.4f}")
for name, seq in seq_of.items():
    obs = anneal(seq, K_OBS)
    p = (np.sum(null_z32 >= obs) + 1)/(N_NULL + 1)
    readability[name] = dict(obs_score_per_bigram=float(obs), p=float(p), p_bonf=float(min(1.0, 4*p)))
    print(f"[READ] {name:12s} obs={obs:.4f}  p={p:.4f}  p_bonf(x4)={min(1.0,4*p):.4f}")

# ---------- Part C: power on known English controls (not in the LM) ----------
N_CTRL, N_PERM_CTRL, K_HOM = 20, 30, 10
ctrl = []
for i in range(N_CTRL):
    s = rng.integers(0, len(L3)-32)
    plain = L3[s:s+32]
    sym_c = plain*K_HOM + rng.integers(0, K_HOM, size=32)
    _, lab = np.unique(sym_c, return_inverse=True)
    K = int(lab.max()+1)
    obs = anneal(lab, K)
    null = perm_null(lab, K, N_PERM_CTRL)
    p = (np.sum(null >= obs)+1)/(N_PERM_CTRL+1)
    ctrl.append(dict(start=int(s), K=K, repeats=int(32-K), obs=float(obs), p=float(p), detected=bool(p < 0.05)))
power = float(np.mean([c['detected'] for c in ctrl]))
print(f"[POWER] controls detected at p<0.05: {sum(c['detected'] for c in ctrl)}/{N_CTRL}  -> power = {power:.2f}")
print(f"[POWER] control mean obs score = {np.mean([c['obs'] for c in ctrl]):.4f}; mean p = {np.mean([c['p'] for c in ctrl]):.3f}")

json.dump(dict(R_OBS=R_OBS, K_OBS=K_OBS, structural=structural, consistent_models=cons,
               readability=readability, z32_null=dict(n=N_NULL, mean=float(null_z32.mean()), sd=float(null_z32.std()),
               p95=float(np.percentile(null_z32,95))), controls=ctrl, power=power, elapsed_s=time.time()-t0),
          open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), 'results_structure.json'),'w'), indent=1, ensure_ascii=False)
print(f"[DONE] elapsed {time.time()-t0:.1f}s")

"""Pre-registered synthetic calibration for H4a (PREREG_H4.md). Uses only GPL texts and synthetic keys."""
import numpy as np, json, time
t0 = time.time()
rng = np.random.default_rng(20261013)
def load(path):
    s = open(path, encoding='utf-8', errors='ignore').read().upper()
    return np.array([ord(c)-65 for c in s if 'A' <= c <= 'Z'])
L2 = load('/usr/share/common-licenses/GPL-2'); L3 = load('/usr/share/common-licenses/GPL-3')
BI = np.zeros((26,26)); np.add.at(BI, (L2[:-1], L2[1:]), 1)
LP = np.log((BI+0.5)/(BI+0.5).sum(axis=1, keepdims=True))
LETTERS21 = np.array([i for i in range(26) if chr(65+i) not in 'JKQXZ'])   # 21 letters, as in Z340's key
assert len(LETTERS21) == 21
N_SYM_PER_LETTER = 3                                                     # 21*3 = 63 symbols (assumption)
KEY_SYM = np.arange(63)
KEY_LET = np.repeat(LETTERS21, N_SYM_PER_LETTER)                         # symbol -> letter (true key)
SYM_OF_LET = {l: np.where(KEY_LET == l)[0] for l in LETTERS21}
NOVEL = -1                                                               # symbols not in key (unknown)
def plaintext_segment(n=32):
    s = rng.integers(0, len(L3)-200)
    seg = L3[s:s+400]
    seg = seg[np.isin(seg, LETTERS21)][:n]
    return seg
def encrypt(plain):
    syms = np.array([rng.choice(SYM_OF_LET[l]) for l in plain])
    return syms
def make_cipher():
    plain = plaintext_segment(32)
    syms = encrypt(plain)
    # replace two random positions with novel (unknown) symbols
    pos = rng.choice(len(syms), size=2, replace=False)
    syms = syms.copy(); syms[pos] = NOVEL
    return plain, syms
def stat_T(letters, known):
    # letters: decrypted letter per position (ints), known: bool mask
    a, b = letters[:-1], letters[1:]
    m = known[:-1] & known[1:]
    if m.sum() == 0: return -np.inf
    return LP[a[m], b[m]].mean()
def test_once(syms, mapping, n_perm=999):
    """mapping: dict symbol -> letter used for decryption (may be wrong). Returns p and T_obs."""
    known = syms != NOVEL
    dist = np.unique(syms[known])
    val = np.array([mapping[s] for s in dist])             # letter value per distinct symbol
    idx = {s:i for i,s in enumerate(dist)}
    pos_idx = np.array([idx[s] if s != NOVEL else 0 for s in syms])
    letters = val[pos_idx]
    T_obs = stat_T(letters, known)
    cnt = 0
    for _ in range(n_perm):
        perm = rng.permutation(val)                        # permute letter values across symbols
        T = stat_T(perm[pos_idx], known)
        cnt += (T >= T_obs)
    p = (1 + cnt)/(1 + n_perm)
    return p, T_obs
def run_condition(f_correct, wrong_key=False, reps=300):
    ps, pcrit = [], []
    for _ in range(reps):
        plain, syms = make_cipher()
        if wrong_key:
            mapping = {s: int(rng.choice(LETTERS21)) for s in np.unique(syms[syms != NOVEL])}
        else:
            mapping = {}
            for s in np.unique(syms[syms != NOVEL]):
                true = int(KEY_LET[s])
                mapping[s] = true if rng.random() < f_correct else int(rng.choice(LETTERS21))
        p, _ = test_once(syms, mapping)
        ps.append(p)
    ps = np.array(ps)
    return dict(f_correct=f_correct, wrong_key=wrong_key, reps=reps,
                power_p001=float((ps < 0.01).mean()), power_p0025=float((ps < 0.0025).mean()),
                median_p=float(np.median(ps)))
results = []
for f in [1.0, 0.9, 0.8, 0.7]:
    r = run_condition(f); results.append(r)
    print(f"[CAL] f_correct={f:.1f}  power(p<0.01)={r['power_p001']:.3f}  power(p<0.0025)={r['power_p0025']:.3f}  median p={r['median_p']:.3f}")
r0 = run_condition(1.0, wrong_key=True); results.append(r0)
print(f"[CAL] H0 wrong key: FPR(p<0.01)={r0['power_p001']:.4f}  FPR(p<0.0025)={r0['power_p0025']:.4f}  median p={r0['median_p']:.3f}")
json.dump(dict(results=results, assumptions=dict(symbols_per_letter=N_SYM_PER_LETTER, letters=21, novel_positions=2,
               lm='GPL-2 bigrams add-0.5', plaintext='GPL-3 segments filtered to 21 letters', n_perm=999)),
          open('calibration_h4.json','w'), indent=1)
print(f"[DONE] {time.time()-t0:.1f}s")

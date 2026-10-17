# Pre-registered family for Foxon Fig.1 reproduction and phrase test.
# Declared BEFORE running. No symbol is changed. Every config is reported.
#
# Input: Fig.1(A) as read from the uploaded PDF image (ASCII transliteration).
# Layout (Fig.1(A)): row1 = 17 cells, row2 = 15 cells.
# Step 1 (paper, Sec 4.3): shift row2 right by k. Paper says k=2.
#   family: k in 0..16. Figure 1(B) constraint: for k=2 row2 cells 1-2 empty.
# Step 2 (paper, Sec 4.3): read by knight move starting at (1,1), alternating rows,
#   column change delta in {+2,-2}. Paper's first move is (1,1)->(2,3), so delta=+2.
# Column wrap W (paper: "loop back on the same row"): W1 = cyclic over 17 columns,
#   W2 = cyclic over the row's own length (17 top / 15 bottom), W3 = no wrap (overflow = invalid).
# Landing on an empty cell: E1 = invalid, E2 = skip the empty cell and keep the same knight move.
# Output must visit every symbol exactly once (permutation) or the config is invalid.
# Phrase test: a phrase "appears without edits" iff for every pair of output positions
#   holding the same symbol, the phrase has the same letter at both positions (homophonic rule).
import csv, itertools, sys
try:
    import numpy as np
    HAVE_NP = True
except Exception:
    HAVE_NP = False

TOP = list('C1J I2O3 4AM567ORTG'.replace(' ', ''))   # placeholder, overwritten below
TOP = ['C','1','J','I','2','O','3','4','A','M','5','6','7','O','R','T','G']
BOT = ['X','8','F','D','V','9','!','H','C','E','L','?','P','W','1']
SYMS = TOP + BOT
assert len(TOP) == 17 and len(BOT) == 15 and len(SYMS) == 32

# Fig.1(C) as printed in the PDF (authors' output order, positions 1..32)
C_OUT = list('CX2VAC7PGID4H6?TJ') + list('F3!5LR118O9MEOW')
assert len(C_OUT) == 32

PHRASES = {
    'T1_target':  'TWELVEINCHESALONGTHETHREERADIANS',
    'T2_alt':     'THREERADIANSANDTWELVEINCHESALONG',
    'T3_other':   'THREEANDTHREEEIGHTHSRADIANSSIXIN',
    'T4_foxon_edited': 'TWELVTINCHESALONGTHETHREERADIAAS',  # reference only: contains 2 edits
}
for p in PHRASES.values():
    assert len(p) == 32, p

def build_grid(k, wrap):
    cells = {}
    for c in range(1, 18):
        cells[(1, c)] = c - 1
    for i in range(1, 16):
        t = i + k
        if wrap == 'W1':
            col = ((t - 1) % 17) + 1
        elif wrap == 'W2':
            col = ((t - 1) % 15) + 1
        else:  # W3
            if t > 17:
                return None
            col = t
        if (2, col) in cells:
            return None  # collision (should not happen)
        cells[(2, col)] = 17 + i - 1
    return cells

def read_path(grid, delta, wrap, emode, max_steps=5000):
    pos = (1, 1)
    seen = {pos}
    out = [grid[pos]]
    steps = 0
    while len(out) < 32:
        steps += 1
        if steps > max_steps:
            return None, 'loop'
        r, c = pos
        nr = 2 if r == 1 else 1
        t = c + delta
        L = 17 if nr == 1 else 15
        if wrap == 'W1':
            nc = ((t - 1) % 17) + 1
        elif wrap == 'W2':
            nc = ((t - 1) % L) + 1
        else:
            if t < 1 or t > L:
                return None, 'overflow'
            nc = t
        nxt = (nr, nc)
        if nxt not in grid:
            if emode == 'E1':
                return None, 'empty_cell'
            pos = nxt       # E2: skip this empty cell, next knight move from it
            continue
        if nxt in seen:
            return None, 'revisit'
        seen.add(nxt)
        out.append(grid[nxt])
        pos = nxt
    return out, 'ok'

rows = []
configs = []
for k in range(0, 17):
    for delta in (+2, -2):
        for wrap in ('W1', 'W2', 'W3'):
            for emode in ('E1', 'E2'):
                grid = build_grid(k, wrap)
                if grid is None:
                    rows.append(dict(k=k, delta=delta, wrap=wrap, emode=emode,
                                     status='layout_overflow', fig1B_layout=False))
                    continue
                fig1B = (k == 2 and set(c for (r, c) in grid if r == 2) == set(range(3, 18)))
                idx, status = read_path(grid, delta, wrap, emode)
                row = dict(k=k, delta=delta, wrap=wrap, emode=emode, status=status,
                           fig1B_layout=fig1B)
                if idx is not None:
                    seq = [SYMS[i] for i in idx]
                    row['output'] = ''.join(seq)
                    row['match_C_out'] = sum(a == b for a, b in zip(seq, C_OUT))
                    row['_idx'] = tuple(idx)
                    configs.append(row)
                rows.append(row)

valid = {}
for r in configs:
    valid.setdefault(r['_idx'], []).append(r)
print(f"configs enumerated: {len(rows)}; valid readings: {len(configs)}; unique valid output orders: {len(valid)}")

# Repeat-pair structure of each unique output order
def pairs_for(idx_order):
    pos_by_sym = {}
    for out_pos, cell_idx in enumerate(idx_order):
        pos_by_sym.setdefault(SYMS[cell_idx], []).append(out_pos)
    return [v for v in pos_by_sym.values() if len(v) > 1]

uniq = list(valid.keys())
pairsets = [pairs_for(u) for u in uniq]
assert all(len(p) == 3 and all(len(q) == 2 for q in p) for p in pairsets)

def pass_count(phrase, pairsets_):
    res = []
    for ps in pairsets_:
        sat = sum(phrase[a] == phrase[b] for a, b in ps)
        res.append(sat)
    return res

# Observed per-phrase results
print("\nPhrase constraint results (pairs satisfied out of 3), per unique valid order:")
obs = {name: pass_count(p, pairsets) for name, p in PHRASES.items()}
for name in PHRASES:
    full = sum(1 for s in obs[name] if s == 3)
    print(f"  {name}: configs with 3/3 = {full} of {len(uniq)}")

# Null: random English-like strings with the same i.i.d. letter model
eng = {'e':12.7,'t':9.1,'a':8.2,'o':7.5,'i':7.0,'n':6.7,'s':6.3,'h':6.1,'r':6.0,'d':4.3,'l':4.0,'c':2.8,'u':2.8,'m':2.4,'w':2.4,'f':2.2,'g':2.0,'y':2.0,'p':1.9,'b':1.5,'v':1.0,'k':0.8,'j':0.15,'x':0.15,'q':0.10,'z':0.07}
L_ = list(eng); W_ = [eng[x] for x in L_]
W_ = [w / sum(W_) for w in W_]
sp2 = sum(w * w for w in W_)
print(f"\nNull model: i.i.d. letters, typed English table. sum p^2 = {sp2:.4f}; per 3-pair config = {sp2**3:.2e}")

N_NULL = 200000
import random
random.seed(20261011)
null_counts = {name: [] for name in PHRASES}
if HAVE_NP:
    rng = np.random.default_rng(20261011)
    idxs = rng.choice(len(L_), size=(N_NULL, 32), p=W_)
    letters = np.array(L_)
    S = letters[idxs]
    for name in PHRASES:
        m = np.zeros(N_NULL, dtype=int)
        for ps in pairsets:
            ok = np.ones(N_NULL, dtype=bool)
            for a, b in ps:
                ok &= (S[:, a] == S[:, b])
            m += ok
        null_counts[name] = m
else:
    for _ in range(N_NULL):
        s = random.choices(L_, W_, k=32)
        for name in PHRASES:
            pass
    print("numpy missing; null skipped")

# Per phrase: number of unique configs with 3/3 (observed) vs null distribution of the same count
print("\nNull comparison (count of unique valid orders with all 3 pairs satisfied):")
summary = []
for name in PHRASES:
    m_obs = sum(1 for s in obs[name] if s == 3)
    if HAVE_NP:
        nc = null_counts[name]
        p_ge = float((nc >= m_obs).mean())
        mean_null = float(nc.mean())
    else:
        p_ge = float('nan'); mean_null = float('nan')
    summary.append((name, m_obs, mean_null, p_ge))
    print(f"  {name}: observed={m_obs}  null mean={mean_null:.4f}  P(null>=observed)={p_ge:.4f}")

# Reproduction of Fig.1(C)
best = max(configs, key=lambda r: r['match_C_out'])
print(f"\nBest reproduction of Fig.1(C): {best['match_C_out']}/32  (k={best['k']}, delta={best['delta']}, wrap={best['wrap']}, {best['emode']})")
full_repro = [r for r in configs if r['match_C_out'] == 32]
print("configs reproducing Fig.1(C) fully:", [(r['k'], r['delta'], r['wrap'], r['emode']) for r in full_repro])

# Write CSV of all configs
fields = ['k','delta','wrap','emode','status','fig1B_layout','output','match_C_out']
with open('z32_all_configs.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore')
    w.writeheader()
    for r in rows:
        w.writerow({k: r.get(k, '') for k in fields})
with open('z32_phrase_tests.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['phrase_name','phrase','unique_valid_orders','orders_3of3','null_mean','P_null_ge_observed'])
    for name, m_obs, mean_null, p_ge in summary:
        w.writerow([name, PHRASES[name], len(uniq), m_obs, round(mean_null,5) if HAVE_NP else '', round(p_ge,5) if HAVE_NP else ''])
print("\nwritten: z32_all_configs.csv, z32_phrase_tests.csv")

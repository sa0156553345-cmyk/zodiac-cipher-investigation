#!/usr/bin/env python3
"""
Pre-registered family of transposition readings for Foxon (2023) Fig.1(B)->(C), and phrase test.

Run order:  python3 fig_glyph_check.py  ->  python3 transposition_family.py
Inputs : z32_fig1A_transcription.csv, fig_glyph_check.csv (Fig.1(C) reading from bitmap comparison)
Outputs: z32_all_configs.csv   (all 204 configurations, one row each)
         z32_phrase_tests.csv  (phrase tests + null comparison)

Rules below are fixed before running. No symbol is edited. Nothing is changed after a run.

FAMILY (204 = 17 x 2 x 3 x 2)
  k      : shift of row 2 to the right, k in 0..16. Paper: k = 2 ("shifting the bottom row two places").
  delta  : knight column step, +2 or -2. Row alternates on every move. Start at (row1,col1).
  wrap W : how a column outside the row wraps.
           W1 = cyclic over 17 columns (paper: "loop back on the opposite side of the same row")
           W2 = cyclic over each row's own length (17 top, 15 bottom)
           W3 = no wrap: an overflow makes the configuration invalid
  emode  : what happens when a knight move lands on an empty cell (row 2 has empty cells when k=2)
           E1 = invalid configuration
           E2 = skip that cell and apply the same knight move again from it

VALIDITY: a reading is valid only if it visits all 32 symbol cells exactly once, and every
          recorded move alternates rows.  Both checks are reported per row.

PHRASE TEST (homophonic consistency): a phrase "appears without edits" in an output order iff, for
  every pair of output positions holding the same symbol, the phrase has the same letter at both.
  Singletons impose no constraint. Only 3 pairs exist: C(1,26), 1(2,32), O(6,14) in the input order.
"""
import csv, os, math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))

def read_transcription():
    labels = []
    with open(os.path.join(HERE, 'z32_fig1A_transcription.csv'), newline='', encoding='utf-8') as f:
        for r in csv.reader(f):
            if r and r[0].isdigit():
                labels.append((int(r[0]), r[1]))
    labels.sort()
    assert [p for p, _ in labels] == list(range(1, 33))
    return [s for _, s in labels]

def read_C_output():
    rows = []
    with open(os.path.join(HERE, 'fig_glyph_check.csv'), newline='', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            if r['panel'] == 'C':
                rows.append((int(r['position']), r['reading']))
    rows.sort()
    assert [p for p, _ in rows] == list(range(1, 33))
    return [s for _, s in rows]

SYMS = read_transcription()    # SYMS[i] = symbol at input position i+1 (top 1..17, bottom 18..32)
C_OUT = read_C_output()        # Fig.1(C) output order, from bitmap comparison (not from visual reading)

TOP_LEN, BOT_LEN = 17, 15
PHRASES = {
    'T1_target':        'TWELVEINCHESALONGTHETHREERADIANS',
    'T2_alt':           'THREERADIANSANDTWELVEINCHESALONG',
    'T3_other':         'THREEANDTHREEEIGHTHSRADIANSSIXIN',
    'T4_foxon_edited':  'TWELVTINCHESALONGTHETHREERADIAAS',   # contains 2 edits; reference only
}
for p in PHRASES.values():
    assert len(p) == 32

def build_grid(k, wrap):
    """cells[(row,col)] = symbol index (0..31). Row 1: index 0..16. Row 2: index 17..31."""
    cells = {(1, c): c - 1 for c in range(1, TOP_LEN + 1)}
    for i in range(1, BOT_LEN + 1):
        t = i + k
        if wrap == 'W1':
            col = (t - 1) % 17 + 1
        elif wrap == 'W2':
            col = (t - 1) % BOT_LEN + 1
        else:  # W3
            if t > 17:
                return None
            col = t
        if (2, col) in cells:
            return None
        cells[(2, col)] = TOP_LEN + i - 1
    return cells

def step(cur, delta, wrap):
    row, col = cur
    nr = 2 if row == 1 else 1
    L = 17 if nr == 1 else BOT_LEN
    t = col + delta
    if wrap == 'W1':
        nc = (t - 1) % 17 + 1
    elif wrap == 'W2':
        nc = (t - 1) % L + 1
    else:  # W3
        if t < 1 or t > L:
            return None
        nc = t
    return (nr, nc)

def read_order(grid, delta, wrap, emode, max_steps=5000):
    start = (1, 1)
    order, visited, moves = [grid[start]], [start], []
    seen = {start}
    cur, steps = start, 0
    while len(order) < 32:
        steps += 1
        if steps > max_steps:
            return None, 'loop', moves
        nxt = step(cur, delta, wrap)
        if nxt is None:
            return None, 'overflow', moves
        moves.append((cur, nxt))
        if nxt not in grid:
            if emode == 'E1':
                return None, 'empty_cell', moves
            cur = nxt          # E2: skip the empty cell, continue from it
            continue
        if nxt in seen:
            return None, 'revisit', moves
        seen.add(nxt); order.append(grid[nxt]); visited.append(nxt); cur = nxt
    return order, 'ok', moves

def repeat_pairs(order):
    pos = {}
    for out_pos, sym_idx in enumerate(order):
        pos.setdefault(SYMS[sym_idx], []).append(out_pos)
    return [v for v in pos.values() if len(v) > 1]

# ---------- enumerate the family ----------
rows, valid = [], {}
for k in range(0, 17):
    for delta in (+2, -2):
        for wrap in ('W1', 'W2', 'W3'):
            for emode in ('E1', 'E2'):
                cfg = dict(k=k, delta=delta, wrap=wrap, emode=emode)
                grid = build_grid(k, wrap)
                if grid is None:
                    rows.append({**cfg, 'status': 'layout_overflow'}); continue
                fig1b = (k == 2 and sorted(c for (r, c) in grid if r == 2) == list(range(3, 18)))
                order, status, moves = read_order(grid, delta, wrap, emode)
                rec = {**cfg, 'status': status, 'fig1B_layout': fig1b}
                if order is not None:
                    is_perm = (sorted(order) == list(range(32)) and len(set(order)) == 32)
                    rows_alt = all(a[0] != b[0] for a, b in moves)
                    rec.update(is_permutation=is_perm, moves_alternate_rows=rows_alt, n_moves=len(moves))
                    rec['output'] = ''.join(SYMS[i] for i in order)
                    rec['matches_fig1C'] = sum(SYMS[i] == C_OUT[j] for j, i in enumerate(order))
                    assert is_perm
                    valid.setdefault(tuple(order), []).append(rec)
                rows.append(rec)

uniq = list(valid.keys())
pairsets = {u: repeat_pairs(u) for u in uniq}
assert all(len(p) == 3 for p in pairsets.values())
print(f"configurations: {len(rows)}   valid readings: {sum(1 for r in rows if 'output' in r)}   unique valid orders: {len(uniq)}")
print("status counts:", {s: sum(1 for r in rows if r['status'] == s) for s in sorted(set(r['status'] for r in rows))})
print("valid readings by (wrap, emode):", {(w, e): sum(1 for r in rows if r.get('wrap') == w and r.get('emode') == e and 'output' in r) for w in ('W1','W2','W3') for e in ('E1','E2')})

full = [r for r in rows if r.get('matches_fig1C') == 32]
print("configurations reproducing Fig.1(C) with 32/32:", [(r['k'], r['delta'], r['wrap'], r['emode']) for r in full])

# ---------- phrase test ----------
def passes(phrase, u):
    return [phrase[a] == phrase[b] for a, b in pairsets[u]]

eng = {'e':12.7,'t':9.1,'a':8.2,'o':7.5,'i':7.0,'n':6.7,'s':6.3,'h':6.1,'r':6.0,'d':4.3,'l':4.0,'c':2.8,'u':2.8,'m':2.4,'w':2.4,'f':2.2,'g':2.0,'y':2.0,'p':1.9,'b':1.5,'v':1.0,'k':0.8,'j':0.15,'x':0.15,'q':0.10,'z':0.07}
letters = list(eng)
pw = np.array([eng[x] for x in letters]); pw = pw / pw.sum()
sp2 = float((pw ** 2).sum())

N_NULL = 200000
rng = np.random.default_rng(20261011)
idx = rng.choice(len(letters), size=(N_NULL, 32), p=pw)
S = np.array(letters)[idx]
null_count = np.zeros(N_NULL, dtype=int)
for u in uniq:
    ok = np.ones(N_NULL, dtype=bool)
    for a, b in pairsets[u]:
        ok &= (S[:, a] == S[:, b])
    null_count += ok

summary = []
for name, ph in PHRASES.items():
    per = {u: passes(ph, u) for u in uniq}
    m_obs = sum(1 for u in uniq if all(per[u]))
    p_ge = float((null_count >= m_obs).mean())
    summary.append((name, ph, len(uniq), m_obs, sum(1 for u in uniq if sum(per[u]) == 2),
                    round(float(null_count.mean()), 5), round(p_ge, 5)))
    print(f"{name:<16} orders with 3/3 = {m_obs}/{len(uniq)}   null mean = {null_count.mean():.4f}   P(null>=obs) = {p_ge:.4f}")
print(f"\nper-pair luck probability sum p^2 = {sp2:.4f}; per 3-pair order = {sp2**3:.2e}")

# ---------- write outputs ----------
fields = ['k','delta','wrap','emode','status','fig1B_layout','is_permutation','moves_alternate_rows','n_moves','output','matches_fig1C']
with open(os.path.join(HERE, 'z32_all_configs.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore')
    w.writeheader()
    for r in rows:
        w.writerow({k: r.get(k, '') for k in fields})
with open(os.path.join(HERE, 'z32_phrase_tests.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['phrase_name','phrase','unique_valid_orders','orders_3of3','orders_2of3','null_mean_orders_3of3','P_null_ge_observed'])
    for s in summary:
        w.writerow(list(s))
print("written z32_all_configs.csv and z32_phrase_tests.csv")

#!/usr/bin/env python3
"""Pre-registered transposition family (204 configurations) for Foxon Fig.1(B)->(C).
Output: results/transposition_all_configs.csv, results/valid_orders.json,
        results/transposition_assumption_effects.csv
Rules are fixed in this file; nothing is edited after a run.
Rule sources: k=2 is stated in Foxon Sec 4.3 ("shifting the bottom row two places to the right");
  start (1,1) and knight moves are stated; W1 is the reading of "loop back on the opposite side of
  the same row"; delta=+2 is inferred from Fig.1(C); the empty-cell rule (E1/E2) is NOT stated."""
import csv, json
from common import RESULTS, DATA, SYMS
from common import repeat_pairs
import csv as _csv

def read_C():
    rows = []
    with open(RESULTS / 'fig_glyph_check.csv', newline='', encoding='utf-8') as f:
        for r in _csv.DictReader(f):
            if r['panel'] == 'C': rows.append((int(r['position']), r['reading']))
    rows.sort()
    return [s for _, s in rows]
C_OUT = read_C()

TOP, BOT = 17, 15
def build_grid(k, wrap):
    cells = {(1, c): c - 1 for c in range(1, TOP + 1)}
    for i in range(1, BOT + 1):
        t = i + k
        if wrap == 'W1': col = (t - 1) % 17 + 1
        elif wrap == 'W2': col = (t - 1) % BOT + 1
        else:
            if t > 17: return None
            col = t
        if (2, col) in cells: return None
        cells[(2, col)] = TOP + i - 1
    return cells

def step(cur, delta, wrap):
    row, col = cur
    nr = 2 if row == 1 else 1
    L = 17 if nr == 1 else BOT
    t = col + delta
    if wrap == 'W1': nc = (t - 1) % 17 + 1
    elif wrap == 'W2': nc = (t - 1) % L + 1
    else:
        if t < 1 or t > L: return None
        nc = t
    return (nr, nc)

def read_order(grid, delta, wrap, emode, max_steps=5000):
    start = (1, 1)
    order, moves, seen, cur, steps = [grid[start]], [], {start}, start, 0
    while len(order) < 32:
        steps += 1
        if steps > max_steps: return None, 'loop', moves
        nxt = step(cur, delta, wrap)
        if nxt is None: return None, 'overflow', moves
        moves.append((cur, nxt))
        if nxt not in grid:
            if emode == 'E1': return None, 'empty_cell', moves
            cur = nxt; continue
        if nxt in seen: return None, 'revisit', moves
        seen.add(nxt); order.append(grid[nxt]); cur = nxt
    return order, 'ok', moves

rows, valid = [], []
for k in range(17):
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
                    is_perm = sorted(order) == list(range(32)) and len(set(order)) == 32
                    alt_ok = all(a[0] != b[0] for a, b in moves)
                    out = ''.join(SYMS[i] for i in order)
                    match = sum(SYMS[i] == C_OUT[j] for j, i in enumerate(order))
                    assert is_perm
                    rec.update(is_permutation=is_perm, moves_alternate_rows=alt_ok, n_moves=len(moves),
                               output=out, matches_fig1C=match)
                    valid.append({'id': f"k{k}_d{delta}_{wrap}_{emode}", **cfg, 'order': order,
                                  'output': out, 'matches_fig1C': match, 'fig1B_layout': fig1b})
                rows.append(rec)

fields = ['k', 'delta', 'wrap', 'emode', 'status', 'fig1B_layout', 'is_permutation',
          'moves_alternate_rows', 'n_moves', 'output', 'matches_fig1C']
with open(RESULTS / 'transposition_all_configs.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore')
    w.writeheader()
    for r in rows: w.writerow({k: r.get(k, '') for k in fields})
with open(RESULTS / 'valid_orders.json', 'w', encoding='utf-8') as f:
    json.dump(valid, f, ensure_ascii=False, indent=1)

# Assumption effects: which declared choice changes the result (k=2 rows only, the layout the paper describes)
src = {'k': 'stated (Foxon 4.3: shift two places)', 'delta': 'delta=+2 inferred from Fig.1(C); delta=-2 is an alternative',
       'wrap': 'W1 = reading of "loop back on the same row"; W2, W3 are alternatives',
       'emode': 'empty-cell rule NOT stated; E1 and E2 are alternatives'}
with open(RESULTS / 'transposition_assumption_effects.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['k', 'delta', 'wrap', 'emode', 'status', 'valid', 'output', 'matches_fig1C', 'source_of_choice'])
    for r in rows:
        if r['k'] != 2: continue
        choice = '; '.join(f"{key}: {src[key]}" for key in ('delta', 'wrap', 'emode'))
        w.writerow([r['k'], r['delta'], r['wrap'], r['emode'], r['status'], 'output' in r,
                    r.get('output', ''), r.get('matches_fig1C', ''), choice])

print(f"configurations: {len(rows)}   valid readings: {len(valid)}")
print("valid by (wrap, emode):", {(w_, e): sum(1 for v in valid if v['wrap'] == w_ and v['emode'] == e)
                                   for w_ in ('W1', 'W2', 'W3') for e in ('E1', 'E2')})
print("configurations matching Fig.1(C) 32/32:", [v['id'] for v in valid if v['matches_fig1C'] == 32])
print("written: transposition_all_configs.csv, valid_orders.json, transposition_assumption_effects.csv")

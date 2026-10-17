#!/usr/bin/env python3
"""Audit 02 - second, independent implementation of the 204-configuration family.
Written from the rule definitions alone (no import of pipeline functions).
It (a) reproduces every status and output of results/transposition_all_configs.csv,
(b) records the step-by-step path of the primary configuration (k=2, delta=+2, W1, E2),
(c) counts row visits and skip events for every valid order, to test whether the empty
cells of the 17+15 layout force a skip rule.
Outputs: results/audit_02_second_implementation.csv, results/audit_02_primary_path.csv,
         results/audit_02_forced_structure.csv"""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
with open(ROOT / 'data' / 'z32_fig1A_transcription.csv', newline='', encoding='utf-8') as f:
    labs = sorted((int(r[0]), r[1]) for r in csv.reader(f) if r and r[0].isdigit())
SYM = [s for _, s in labs]

def layout(k, wrap):
    """cell (row, col) -> input index. Row 1: 17 cells; row 2: 15 symbols placed after shifting by k."""
    cells = {(1, c): c - 1 for c in range(1, 18)}
    for i in range(1, 16):
        t = i + k
        if wrap == 'W1':
            col = (t - 1) % 17 + 1
        elif wrap == 'W2':
            col = (t - 1) % 15 + 1
        else:
            if t > 17:
                return None
            col = t
        if (2, col) in cells:
            return None
        cells[(2, col)] = 16 + i
    return cells

def move(cell, d, wrap):
    r, c = cell
    r2 = 3 - r
    t = c + d
    L = 17 if r2 == 1 else 15
    if wrap == 'W1':
        c2 = (t - 1) % 17 + 1
    elif wrap == 'W2':
        c2 = (t - 1) % L + 1
    else:
        if not 1 <= t <= L:
            return None
        c2 = t
    return (r2, c2)

def walk(cells, d, wrap, skip_empty):
    """Returns (order, status, moves). moves = list of (step, from_cell, to_cell, outcome)."""
    cur = (1, 1)
    seen = {cur}
    order = [cells[cur]]
    moves = []
    steps = 0
    while len(order) < 32:
        steps += 1
        if steps > 5000:
            return None, 'loop', moves
        nxt = move(cur, d, wrap)
        if nxt is None:
            moves.append((steps, cur, None, 'overflow'))
            return None, 'overflow', moves
        if nxt not in cells:
            moves.append((steps, cur, nxt, 'empty'))
            if not skip_empty:
                return None, 'empty_cell', moves
            cur = nxt
            continue
        if nxt in seen:
            moves.append((steps, cur, nxt, 'revisit'))
            return None, 'revisit', moves
        moves.append((steps, cur, nxt, 'visit'))
        seen.add(nxt)
        order.append(cells[nxt])
        cur = nxt
    return order, 'ok', moves

# ---- (a) compare with the pipeline's table ----
pipe = {(int(r['k']), int(r['delta']), r['wrap'], r['emode']): r
        for r in csv.DictReader(open(ROOT / 'results' / 'transposition_all_configs.csv', encoding='utf-8'))}
agree_rows = []
n_agree = 0
for k in range(17):
    for d in (+2, -2):
        for wrap in ('W1', 'W2', 'W3'):
            for emode in ('E1', 'E2'):
                cells = layout(k, wrap)
                if cells is None:
                    status, out = 'layout_overflow', ''
                else:
                    order, st, _ = walk(cells, d, wrap, skip_empty=(emode == 'E2'))
                    status = st
                    out = ''.join(SYM[i] for i in order) if order else ''
                p = pipe[(k, d, wrap, emode)]
                same_status = p['status'] == status
                same_output = (p['output'] or '') == out
                agree = same_status and same_output
                n_agree += agree
                agree_rows.append({'k': k, 'delta': d, 'wrap': wrap, 'emode': emode,
                                   'status_audit': status, 'status_pipeline': p['status'],
                                   'output_audit': out, 'output_pipeline': p['output'] or '',
                                   'agree': agree})
with open(ROOT / 'results' / 'audit_02_second_implementation.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(agree_rows[0].keys())); w.writeheader(); w.writerows(agree_rows)
print(f"second implementation agrees with pipeline on {n_agree} of {len(agree_rows)} configurations")

# ---- (b) primary path ----
cells = layout(2, 'W1')
order, st, moves = walk(cells, +2, 'W1', True)
with open(ROOT / 'results' / 'audit_02_primary_path.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['step', 'from_row', 'from_col', 'to_row', 'to_col', 'outcome', 'symbol_at_target'])
    for step, a, b, outc in moves:
        sym = SYM[cells[b]] if (b is not None and b in cells) else ''
        w.writerow([step, a[0], a[1], b[0] if b else '', b[1] if b else '', outc, sym])
skips = [m for m in moves if m[3] == 'empty']
print(f"primary path: status={st}, moves={len(moves)}, empty landings (skips)={len(skips)}")

# ---- (c) forced structure per valid order ----
rows_f = []
for k in range(17):
    for d in (+2, -2):
        for wrap in ('W1', 'W2', 'W3'):
            cells_ = layout(k, wrap)
            if cells_ is None:
                continue
            order_, st_, moves_ = walk(cells_, d, wrap, True)
            if order_ is None:
                continue
            visits = [m[2] for m in moves_ if m[3] == 'visit']
            visits = [(1, 1)] + visits
            r1 = sum(1 for v in visits if v[0] == 1)
            r2 = sum(1 for v in visits if v[0] == 2)
            same_row_consec = sum(1 for a, b in zip(visits, visits[1:]) if a[0] == b[0])
            rows_f.append({'k': k, 'delta': d, 'wrap': wrap, 'row1_visits': r1, 'row2_visits': r2,
                           'consecutive_same_row_visits': same_row_consec,
                           'skip_landings': sum(1 for m in moves_ if m[3] == 'empty'),
                           'fig1B_layout_k2': (k == 2 and wrap == 'W1')})
with open(ROOT / 'results' / 'audit_02_forced_structure.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(rows_f[0].keys())); w.writeheader(); w.writerows(rows_f)
print(f"orders with E2 traversal: {len(rows_f)}; with skips: {sum(1 for r in rows_f if r['skip_landings'] > 0)}")
print("written audit_02_* files")

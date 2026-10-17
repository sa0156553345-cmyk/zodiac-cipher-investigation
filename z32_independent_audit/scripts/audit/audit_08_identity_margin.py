#!/usr/bin/env python3
"""Audit 08 - separation margin of the bitmap identity test.
Recomputes glyph bitmaps for the 32 Fig.1(A) symbols and the 32 Fig.1(C) symbols (independent code),
then reports: the largest within-class distance, the smallest between-class distance (A), the margin
between them, and for every Fig.1(C) glyph the gap between its best and second-best class.
Outputs: results/audit_08_identity_margin.csv"""
import csv
from pathlib import Path
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
im = np.array(Image.open(ROOT / 'images' / 'fig1_all_panels_p8_native.png').convert('L')).astype(float)
BANDS = {'A_top': (22, 54), 'A_bot': (64, 88), 'C_top': (274, 306), 'C_bot': (316, 340)}
INK = 140
def segments(y0, y1, x0=90, gap=2):
    ink = (im[y0:y1, :] < INK).sum(axis=0)
    out, inside, s = [], False, 0
    for x, v in enumerate(ink):
        if x < x0: continue
        if v > 0 and not inside: s, inside = x, True
        if v == 0 and inside: out.append([s, x]); inside = False
    if inside: out.append([s, len(ink)])
    merged = []
    for s, e in out:
        if merged and s - merged[-1][1] <= gap: merged[-1][1] = e
        else: merged.append([s, e])
    return merged
def glyph(y0, y1, s, e):
    g = im[y0:y1, s:e] < INK
    r = np.where(g.any(axis=1))[0]; c = np.where(g.any(axis=0))[0]
    return g[r[0]:r[-1] + 1, c[0]:c[-1] + 1]
def row(name):
    y0, y1 = BANDS[name]
    return [glyph(y0, y1, s, e) for s, e in segments(y0, y1)]
def d(a, b):
    if abs(a.shape[0] - b.shape[0]) > 1 or abs(a.shape[1] - b.shape[1]) > 1:
        return 1.0
    h, w = min(a.shape[0], b.shape[0]), min(a.shape[1], b.shape[1])
    A, B = a[:h, :w], b[:h, :w]
    return (A != B).sum() / max(1, (A | B).sum())
A = row('A_top') + row('A_bot'); C = row('C_top') + row('C_bot')
assert len(A) == 32 and len(C) == 32
# class membership with the pipeline's threshold, then the margin statistics
cls = [-1] * 32; reps = []
for i in range(32):
    for c, r in enumerate(reps):
        if d(A[i], A[r]) < 0.12:
            cls[i] = c; break
    else:
        reps.append(i); cls[i] = len(reps) - 1
D = np.array([[d(A[i], A[j]) for j in range(32)] for i in range(32)])
intra = [D[i, j] for i in range(32) for j in range(32) if i != j and cls[i] == cls[j]]
inter = [D[i, j] for i in range(32) for j in range(32) if cls[i] != cls[j]]
max_intra = max(intra) if intra else 0.0
min_inter = min(inter)
# Fig.1(C): best and second-best class distance per glyph
gaps = []
for g in C:
    ds = sorted((d(g, A[r]), c) for c, r in enumerate(reps))
    gaps.append(ds[1][0] - ds[0][0])
rows = [
    {'quantity': 'classes_in_A', 'value': len(reps)},
    {'quantity': 'max_within_class_distance', 'value': round(float(max_intra), 4)},
    {'quantity': 'min_between_class_distance', 'value': round(float(min_inter), 4)},
    {'quantity': 'margin_min_between_minus_max_within', 'value': round(float(min_inter - max_intra), 4)},
    {'quantity': 'pipeline_threshold', 'value': 0.12},
    {'quantity': 'min_gap_best_vs_second_class_for_Fig1C_glyphs', 'value': round(float(min(gaps)), 4)},
]
with open(ROOT / 'results' / 'audit_08_identity_margin.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['quantity', 'value']); w.writeheader(); w.writerows(rows)
for r in rows: print(r)

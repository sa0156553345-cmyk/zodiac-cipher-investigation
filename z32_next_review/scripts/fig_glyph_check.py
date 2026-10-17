#!/usr/bin/env python3
"""Bitmap identity check for Fig.1 (no OCR; no visual reading is needed to find identities).
Input : images/fig1_all_panels_p8_native.png ; labels: data/z32_fig1A_transcription.csv
Output: results/fig_glyph_check.csv
"""
import csv
import numpy as np
from PIL import Image
from common import IMAGES, RESULTS, SYMS

IMG = IMAGES / 'fig1_all_panels_p8_native.png'
BANDS = {'A_top': (22, 54), 'A_bot': (64, 88), 'B_top': (148, 180), 'B_bot': (190, 214),
         'C_top': (274, 306), 'C_bot': (316, 340)}
INK, IDENT_TOL, X_START = 140, 0.12, 90
im = np.array(Image.open(IMG).convert('L')).astype(float)

def segments(y0, y1, x0=X_START, gap=2):
    ink = (im[y0:y1, :] < INK).sum(axis=0)
    segs, inseg, s = [], False, 0
    for x, v in enumerate(ink):
        if x < x0: continue
        if v > 0 and not inseg: s, inseg = x, True
        if v == 0 and inseg: segs.append((s, x)); inseg = False
    if inseg: segs.append((s, len(ink)))
    merged = []
    for s, e in segs:
        if merged and s - merged[-1][1] <= gap: merged[-1] = (merged[-1][0], e)
        else: merged.append((s, e))
    return merged

def bitmap(y0, y1, s, e):
    g = im[y0:y1, s:e] < INK
    rows = np.where(g.any(axis=1))[0]; cols = np.where(g.any(axis=0))[0]
    return g[rows[0]:rows[-1] + 1, cols[0]:cols[-1] + 1]

def dist(a, b):
    if abs(a.shape[0] - b.shape[0]) > 1 or abs(a.shape[1] - b.shape[1]) > 1: return 1.0
    h = min(a.shape[0], b.shape[0]); w = min(a.shape[1], b.shape[1])
    A = a[:h, :w]; B = b[:h, :w]
    return (A != B).sum() / max(1, (A | B).sum())

def load_row(name):
    y0, y1 = BANDS[name]
    return [bitmap(y0, y1, s, e) for s, e in segments(y0, y1)]

A = load_row('A_top') + load_row('A_bot')
B = load_row('B_top') + load_row('B_bot')
C = load_row('C_top') + load_row('C_bot')
assert len(A) == 32 and len(B) == 32 and len(C) == 32

reps, members, cls = [], [], [None] * 32
for i, g in enumerate(A):
    for c, rep in enumerate(reps):
        if dist(g, A[rep]) < IDENT_TOL:
            members[c].append(i); cls[i] = c; break
    else:
        reps.append(i); members.append([i]); cls[i] = len(reps) - 1
print("identity classes in Fig.1(A):", len(reps))
print("repeated classes (1-indexed):", [[p + 1 for p in m] for m in members if len(m) > 1])
print("classes agree with transcription labels:",
      all(len({SYMS[p] for p in m}) == 1 for m in members) and len(set(SYMS)) == len(reps))
print("max mismatch Fig.1(B) vs Fig.1(A):", round(max(dist(B[i], A[i]) for i in range(32)), 4))

readC, classC, worst = [], [], 0.0
for g in C:
    best, bd = None, 9.0
    for c, rep in enumerate(reps):
        d = dist(g, A[rep])
        if d < bd: bd, best = d, c
    readC.append(SYMS[reps[best]]); classC.append(best); worst = max(worst, bd)
print("worst mismatch of a Fig.1(C) glyph:", round(worst, 4))
print("Fig.1(C) reading by bitmap:", ''.join(readC))

with open(RESULTS / 'fig_glyph_check.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['panel', 'position', 'reading', 'class_id', 'class_rep_position'])
    for i in range(32):
        w.writerow(['A', i + 1, SYMS[i], cls[i], reps[cls[i]] + 1])
    for i in range(32):
        w.writerow(['C', i + 1, readC[i], classC[i], reps[classC[i]] + 1])
print("written results/fig_glyph_check.csv")

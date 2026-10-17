#!/usr/bin/env python3
"""
Bitmap identity check for Foxon (2023) Fig.1 (no OCR, no visual reading needed to find identities).

Input : fig1_all_panels_p8_native.png   (page 8 raster, extracted with pdfimages; unmodified)
Labels: z32_fig1A_transcription.csv     (used ONLY to give a name to each identity class)
Output: fig_glyph_check.csv             (panel, position, reading_by_bitmap, class_id)

What it tests:
  1. Fig.1(A) has 29 identity classes among its 32 glyphs, and the repeated classes are at
     positions {1,26}, {2,32}, {6,14}.  (Equal bitmaps = same typeset character.)
  2. Fig.1(B) top row is pixel-identical to Fig.1(A) top row.
  3. Each Fig.1(C) glyph matches exactly one Fig.1(A) class; the resulting reading is the
     Fig.1(C) output order.
"""
import csv, os
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, 'fig1_all_panels_p8_native.png')
TRANS = os.path.join(HERE, 'z32_fig1A_transcription.csv')
OUT = os.path.join(HERE, 'fig_glyph_check.csv')

# Text-line bands found by horizontal ink projection on the extracted image (y0, y1)
BANDS = {
    'A_top': (22, 54), 'A_bot': (64, 88),
    'B_top': (148, 180), 'B_bot': (190, 214),
    'C_top': (274, 306), 'C_bot': (316, 340),
}
INK = 140          # grey level below which a pixel counts as ink
IDENT_TOL = 0.12   # max normalised mismatch for two glyphs to be the same character
X_START = 90       # skip the (A)/(B)/(C) panel labels on the left

im = np.array(Image.open(IMG).convert('L')).astype(float)

def segments(y0, y1, x0=X_START, gap=2):
    ink = (im[y0:y1, :] < INK).sum(axis=0)
    segs, inseg, s = [], False, 0
    for x, v in enumerate(ink):
        if x < x0:
            continue
        if v > 0 and not inseg:
            s, inseg = x, True
        if v == 0 and inseg:
            segs.append((s, x)); inseg = False
    if inseg:
        segs.append((s, len(ink)))
    merged = []
    for s, e in segs:
        if merged and s - merged[-1][1] <= gap:
            merged[-1] = (merged[-1][0], e)
        else:
            merged.append((s, e))
    return merged

def bitmap(y0, y1, s, e):
    g = im[y0:y1, s:e] < INK
    rows = np.where(g.any(axis=1))[0]; cols = np.where(g.any(axis=0))[0]
    return g[rows[0]:rows[-1] + 1, cols[0]:cols[-1] + 1]

def dist(a, b):
    if abs(a.shape[0] - b.shape[0]) > 1 or abs(a.shape[1] - b.shape[1]) > 1:
        return 1.0
    h = min(a.shape[0], b.shape[0]); w = min(a.shape[1], b.shape[1])
    A = a[:h, :w]; B = b[:h, :w]
    return (A != B).sum() / max(1, (A | B).sum())

def load_row(name):
    y0, y1 = BANDS[name]
    segs = segments(y0, y1)
    return [bitmap(y0, y1, s, e) for s, e in segs]

def read_labels():
    labels = []
    with open(TRANS, newline='', encoding='utf-8') as f:
        for r in csv.reader(f):
            if r and r[0].isdigit():
                labels.append((int(r[0]), r[1]))
    labels.sort()
    assert [p for p, _ in labels] == list(range(1, 33))
    return [l for _, l in labels]

LABELS = read_labels()
A = load_row('A_top') + load_row('A_bot')
B = load_row('B_top') + load_row('B_bot')
C = load_row('C_top') + load_row('C_bot')
assert len(A) == 32 and len(B) == 32 and len(C) == 32, (len(A), len(B), len(C))

# 1. identity classes in Fig.1(A)
reps, members, cls = [], [], [None] * 32
for i, g in enumerate(A):
    for c, rep in enumerate(reps):
        if dist(g, A[rep]) < IDENT_TOL:
            members[c].append(i); cls[i] = c; break
    else:
        reps.append(i); members.append([i]); cls[i] = len(reps) - 1
print("identity classes in Fig.1(A) by bitmap:", len(reps), "(expected 29)")
print("repeated classes (1-indexed positions):", [[p + 1 for p in m] for m in members if len(m) > 1])
agree = all(len({LABELS[p] for p in m}) == 1 for m in members) and len(set(LABELS)) == len(reps)
print("bitmap classes agree with the transcription labels:", agree)

# 2. Fig.1(B) vs Fig.1(A)
worst_B = max(dist(B[i], A[i]) for i in range(32))
print("max mismatch, Fig.1(B) vs Fig.1(A) same symbol:", round(worst_B, 4))

# 3. Fig.1(C) by bitmap
readC, classC, worstC = [], [], 0.0
for g in C:
    best, bd = None, 9.0
    for c, rep in enumerate(reps):
        d = dist(g, A[rep])
        if d < bd:
            bd, best = d, c
    readC.append(LABELS[reps[best]]); classC.append(best); worstC = max(worstC, bd)
print("worst mismatch for any Fig.1(C) glyph:", round(worstC, 4))
print("Fig.1(C) reading by bitmap:", ''.join(readC))

with open(OUT, 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['panel', 'position', 'reading', 'class_id', 'class_rep_position', 'mismatch_to_class'])
    for i in range(32):
        rep = reps[cls[i]]
        w.writerow(['A', i + 1, LABELS[i], cls[i], rep + 1, round(dist(A[i], A[rep]), 4)])
    for i in range(32):
        w.writerow(['C', i + 1, readC[i], classC[i], reps[classC[i]] + 1, ''])
print("written", os.path.basename(OUT))

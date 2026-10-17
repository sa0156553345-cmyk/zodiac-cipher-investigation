#!/usr/bin/env python3
"""Measurements on the original map image (Foxon 2023, Fig. 2, page 9 raster, unmodified).
Measures, with several independent methods:
  - the centre of the Mount Diablo crosshair (line intersection; circle fits to rings; mean of marker boxes);
  - the centres and radii of the rings labelled 4, 8 and 12 (Kasa circle fit with outlier clipping);
  - the radial distance of the marker boxes and of the white (12,3) marker from the centre;
  - the angular positions of the outer angle labels (checks the angle convention in radians, east = 0, anticlockwise);
  - the pixel scale in pixels per figure unit from each method, with its spread.
Label, handwriting and marker positions are manual readings (+-3 to +-5 px) from the grid overlay.
Outputs: results/fig_*.csv"""
import csv, math
from pathlib import Path
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / 'results'
im = np.array(Image.open(ROOT / 'images' / 'fig2_map_p9_native.png').convert('L')).astype(int)
dark = im < 90
H, W = im.shape

# Manual reading of the text-label box centres (approximate; boxes are about 60 x 35 px)
LABEL_BOXES = {
    '1.571': (490, 58), '0.785': (768, 178), '0 (east)': (884, 452), '5.498': (768, 732),
    '4.712': (490, 845), '3.927': (213, 727), '3.142': (99, 452), '2.356': (213, 176),
    '12': (210, 360), '8': (300, 388), '4': (400, 415), '0 (centre)': (497, 440),
}
# Manual reading of the squares on the outer ring and of the white (12,3) marker
BOXES = {'sq_top_left': (447, 150), 'sq_top_right': (535, 150), 'sq_east_upper': (796, 410),
         'sq_east_lower': (796, 497), 'sq_bottom_left': (447, 760), 'sq_bottom_right': (535, 760),
         'sq_west_lower': (186, 497)}
WHITE_MARKER = (186, 410)
# Handwritten text regions (excluded from ring fits)
HANDWRITING = [(470, 290, 740, 425), (340, 425, 610, 480)]
ANGLE_LABELS_RAD = {'1.571': 1.571, '0.785': 0.785, '0 (east)': 0.0, '5.498': 5.498, '4.712': 4.712,
                    '3.927': 3.927, '3.142': 3.142, '2.356': 2.356}

def in_rect(x, y, r):
    return r[0] <= x <= r[2] and r[1] <= y <= r[3]

def near_label(x, y, rad=45):
    return any(math.hypot(x - bx, y - by) < rad for bx, by in LABEL_BOXES.values())

def near_box(x, y, rad=14):
    return any(math.hypot(x - bx, y - by) < rad for bx, by in list(BOXES.values()) + [WHITE_MARKER])

# ---------- centre estimates ----------
col_counts = dark[150:750, :].sum(axis=0)
row_counts = dark[:, 150:750].sum(axis=1)
cx_line = int(np.argmax(col_counts[300:700])) + 300
cy_line = int(np.argmax(row_counts[300:600])) + 300
# sub-pixel: centroid of the counts within +-3 px of the peak
xs_ = np.arange(cx_line - 3, cx_line + 4); cx_line_sub = float(np.average(xs_, weights=col_counts[xs_]))
ys_ = np.arange(cy_line - 3, cy_line + 4); cy_line_sub = float(np.average(ys_, weights=row_counts[ys_]))

def kasa(x, y):
    A = np.c_[2 * x, 2 * y, np.ones_like(x)]
    b = x ** 2 + y ** 2
    c = np.linalg.lstsq(A, b, rcond=None)[0]
    cx, cy = c[0], c[1]
    R = math.sqrt(max(c[2] + cx ** 2 + cy ** 2, 0.0))
    return cx, cy, R

def ring_fit(r0, half, approx_c):
    yy, xx = np.nonzero(dark)
    d = np.hypot(xx - approx_c[0], yy - approx_c[1])
    sel = (d >= r0 - half) & (d <= r0 + half)
    x = xx[sel].astype(float); y = yy[sel].astype(float)
    ang = np.degrees(np.arctan2(approx_c[1] - y, x - approx_c[0])) % 360
    keep = []
    for xi, yi, ai in zip(x, y, ang):
        if min(abs(ai - k) for k in range(0, 361, 45)) < 6:       # crosshair lines
            keep.append(False); continue
        if near_label(xi, yi) or near_box(xi, yi):
            keep.append(False); continue
        if any(in_rect(xi, yi, r) for r in HANDWRITING):
            keep.append(False); continue
        keep.append(True)
    keep = np.array(keep)
    x, y = x[keep], y[keep]
    for _ in range(8):
        cx, cy, R = kasa(x, y)
        res = np.abs(np.hypot(x - cx, y - cy) - R)
        inl = res < 2.0
        if inl.all():
            break
        x, y = x[inl], y[inl]
    cx, cy, R = kasa(x, y)
    res = np.hypot(x - cx, y - cy) - R
    return cx, cy, R, len(x), float(np.sqrt(np.mean(res ** 2)))

rings = {}
for n, r0 in ((4, 102), (8, 205), (12, 307)):
    rings[n] = ring_fit(r0, 7, (cx_line, cy_line))

cx_fit = float(np.average([rings[n][0] for n in rings], weights=[rings[n][3] for n in rings]))
cy_fit = float(np.average([rings[n][1] for n in rings], weights=[rings[n][3] for n in rings]))
cx_box = float(np.mean([v[0] for v in BOXES.values()] + [WHITE_MARKER[0]]))
cy_box = float(np.mean([v[1] for v in BOXES.values()] + [WHITE_MARKER[1]]))

centres = [
    ('lines_argmax', cx_line, cy_line),
    ('lines_subpixel_centroid', cx_line_sub, cy_line_sub),
    ('ring_fits_weighted_mean', cx_fit, cy_fit),
    ('mean_of_outer_boxes_and_marker', cx_box, cy_box),
]
with open(RES / 'fig_centre_estimates.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f); w.writerow(['method', 'cx_px', 'cy_px'])
    for m, cx, cy in centres: w.writerow([m, round(cx, 2), round(cy, 2)])
spread_centre = max(math.hypot(a[1] - b[1], a[2] - b[2]) for a in centres for b in centres)
print("centre estimates:", [(m, round(x, 2), round(y, 2)) for m, x, y in centres])
print(f"maximum disagreement between centre methods: {spread_centre:.2f} px")

# centre used for radii: the ring-fit weighted mean (independent of the crosshair lines)
C = (cx_fit, cy_fit)

with open(RES / 'fig_ring_fits.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['ring_label', 'fit_cx_px', 'fit_cy_px', 'fit_radius_px', 'n_inlier_pixels', 'rms_residual_px',
                'centre_offset_from_weighted_centre_px', 'px_per_unit_from_fit'])
    for n in (4, 8, 12):
        cx, cy, R, npts, rms = rings[n]
        off = math.hypot(cx - C[0], cy - C[1])
        w.writerow([n, round(cx, 2), round(cy, 2), round(R, 2), npts, round(rms, 3), round(off, 2), round(R / n, 4)])
        print(f"ring {n}: centre ({cx:.2f},{cy:.2f}) radius {R:.2f} px, inliers {npts}, rms {rms:.3f} px")

# ---------- radii of the outer boxes and marker ----------
box_rows = []
box_r = []
for name, (x, y) in list(BOXES.items()) + [('white_marker_12_3', WHITE_MARKER)]:
    r = math.hypot(x - C[0], y - C[1]); box_r.append(r)
    box_rows.append([name, x, y, round(r, 2), round(r / 12.0, 4)])
with open(RES / 'fig_boxes_radius.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f); w.writerow(['item', 'x_px', 'y_px', 'radius_px_from_weighted_centre', 'px_per_unit_if_radius_is_12_units'])
    w.writerows(box_rows)
print(f"outer boxes/marker radius: mean {np.mean(box_r):.2f} px, sd {np.std(box_r, ddof=1):.2f} px, range {min(box_r):.2f}-{max(box_r):.2f}")

# ---------- angle labels: check the angle convention ----------
ang_rows = []
for name, rad in ANGLE_LABELS_RAD.items():
    x, y = LABEL_BOXES[name]
    meas = math.degrees(math.atan2(C[1] - y, x - C[0])) % 360
    expected = math.degrees(rad) % 360
    resid = (meas - expected + 180) % 360 - 180
    ang_rows.append([name, x, y, round(meas, 2), round(expected, 2), round(resid, 2)])
with open(RES / 'fig_angle_labels.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f); w.writerow(['label', 'x_px', 'y_px', 'measured_angle_deg_ccw_from_east', 'labelled_angle_deg (rad x 180/pi)', 'residual_deg'])
    w.writerows(ang_rows)
print("angle labels, max |residual| deg:", max(abs(r[5]) for r in ang_rows))

# ---------- scale: px per figure unit by several methods ----------
PX = []
PX.append(('ring_fits_kasa_4_8_12', [rings[n][2] / n for n in (4, 8, 12)]))
PX.append(('outer_boxes_and_marker_mean', [np.mean(box_r) / 12.0]))
PX.append(('outer_boxes_individual', [r / 12.0 for r in box_r]))
pooled = [rings[n][2] / n for n in (4, 8, 12)] + [r / 12.0 for r in box_r]
ls = np.polyfit([4, 8, 12], [rings[n][2] for n in (4, 8, 12)], 1)
PX.append(('least_squares_radius_vs_units_through_origin', [sum(rings[n][2] * n for n in (4, 8, 12)) / sum(n * n for n in (4, 8, 12))]))
with open(RES / 'fig_px_per_unit_methods.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f); w.writerow(['method', 'n_estimates', 'px_per_unit_mean', 'px_per_unit_sd', 'px_per_unit_min', 'px_per_unit_max'])
    for name, vals in PX:
        vals = np.array(vals)
        w.writerow([name, len(vals), round(vals.mean(), 4), round(vals.std(ddof=1), 4) if len(vals) > 1 else '', round(vals.min(), 4), round(vals.max(), 4)])
        print(f"{name}: mean {vals.mean():.3f} px/unit, sd {vals.std(ddof=1) if len(vals) > 1 else float('nan'):.3f}")
allvals = np.array([v for _, vals in PX for v in vals])
combined = float(np.mean([np.mean(v) for _, v in PX]))
spread = float(np.std([np.mean(v) for _, v in PX], ddof=1))
print(f"combined px per unit (mean of method means): {combined:.3f}; spread between methods: {spread:.3f} px/unit ({spread / combined * 100:.2f} %)")
with open(RES / 'fig_px_per_unit_combined.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['quantity', 'value', 'note'])
    w.writerow(['px_per_unit_combined', round(combined, 4), 'mean of method means'])
    w.writerow(['spread_between_methods_px', round(spread, 4), 'sd of method means'])
    w.writerow(['spread_between_methods_percent', round(spread / combined * 100, 3), ''])
    w.writerow(['centre_max_disagreement_px', round(spread_centre, 3), 'max distance between centre estimates'])

# ---------- white marker vs Foxon's (12,3) drawing in the figure's own frame ----------
pred_x = C[0] + 12 * combined * math.cos(3.0)
pred_y = C[1] - 12 * combined * math.sin(3.0)
dx = WHITE_MARKER[0] - pred_x; dy = WHITE_MARKER[1] - pred_y
with open(RES / 'fig_marker_consistency.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['quantity', 'value'])
    w.writerow(['predicted_marker_x_px (r=12 units, theta=3 rad, figure east ccw)', round(pred_x, 2)])
    w.writerow(['predicted_marker_y_px', round(pred_y, 2)])
    w.writerow(['measured_marker_x_px', WHITE_MARKER[0]])
    w.writerow(['measured_marker_y_px', WHITE_MARKER[1]])
    w.writerow(['difference_px', round(math.hypot(dx, dy), 2)])
print(f"white marker vs predicted (12 units, 3 rad) in figure frame: {math.hypot(dx, dy):.2f} px difference")

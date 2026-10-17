#!/usr/bin/env python3
"""Pre-registered criterion (PREREGISTRATION section 11): scale reliability from pairs of measured points.
For every pair of the five city label positions: px/mile = image distance / geodesic distance (Vincenty).
Criterion: relative spread of miles-per-unit across pairs below 10 % (max-min over median).
Outputs: results/pairwise_scale.csv, results/pairwise_scale_summary.csv"""
import csv, math, itertools
from pathlib import Path
import statistics as st
from geodesy import geodesic_miles
from georeg import read_centre, read_unit, read_references

ROOT = Path(__file__).resolve().parents[1]
U = read_unit(); cx, cy = read_centre()
pts = []
for r in csv.DictReader(open(ROOT / 'data' / 'controls.csv', encoding='utf-8')):
    if r['role'] == 'city':
        pts.append((r['name'], float(r['lat']), float(r['lon']), float(r['image_x']), float(r['image_y'])))
rows = []
for a, b in itertools.combinations(pts, 2):
    mi = geodesic_miles(a[1], a[2], b[1], b[2])
    px = math.hypot(b[3] - a[3], b[4] - a[4])
    ppm = px / mi
    rows.append([f'{a[0]} -- {b[0]}', round(mi, 3), round(px, 2), round(ppm, 3), round(U / ppm, 4)])
with open(ROOT / 'results' / 'pairwise_scale.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f, lineterminator='\n')
    w.writerow(['pair', 'geodesic_miles', 'image_px', 'px_per_mile', 'miles_per_unit'])
    w.writerows(rows)
mpu = [r[4] for r in rows]
med = st.median(mpu)
spread = (max(mpu) - min(mpu)) / med
summary = [('pairs', len(rows)), ('miles_per_unit_median', round(med, 4)), ('miles_per_unit_min', min(mpu)),
           ('miles_per_unit_max', max(mpu)), ('relative_spread_max_minus_min_over_median', round(spread, 4)),
           ('criterion_below_10_percent', spread < 0.10)]
with open(ROOT / 'results' / 'pairwise_scale_summary.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f, lineterminator='\n'); w.writerow(['quantity', 'value']); w.writerows(summary)
for q, v in summary: print(f"{q}: {v}")

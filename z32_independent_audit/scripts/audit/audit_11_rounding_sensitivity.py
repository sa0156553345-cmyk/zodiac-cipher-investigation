#!/usr/bin/env python3
"""Audit 11 - sensitivity of the predicted (12,3) location to the rounding convention that turns the
magnetic declination into the minute value.
Foxon writes minute = round(declination/6 deg). Floor gives minute = floor(declination/6 deg).
For declinations 15-17.9 deg, round gives 3 and floor gives 2. The angle 3 rad vs 2 rad then moves the
predicted site. This script recomputes the site for theta = 3 and theta = 2 (r = 12 units) under the
four map models of the pipeline and reports the distance between the two sites.
Outputs: results/audit_11_rounding_sensitivity.csv"""
import csv, math
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[2]
R_EARTH = 3958.8
def haversine(p, q):
    la1, lo1 = map(math.radians, p); la2, lo2 = map(math.radians, q)
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * R_EARTH * math.asin(math.sqrt(h))
cross = {r['quantity']: r['value'] for r in csv.DictReader(open(ROOT / 'results' / 'map_crosshair_and_rings.csv', encoding='utf-8'))}
CX, CY = float(cross['crosshair_centre_x_px']), float(cross['crosshair_centre_y_px'])
PX_UNIT = float(cross['pixels_per_figure_unit'])
cities, diab, hw = [], None, None
for r in csv.DictReader(open(ROOT / 'data' / 'landmarks.csv', encoding='utf-8')):
    if r['name'].startswith('Mount Diablo'): diab = (float(r['lat']), float(r['lon']))
    elif r['name'].startswith('State Highway'): hw = (float(r['lat']), float(r['lon']))
    else: cities.append((float(r['lat']), float(r['lon']), float(r['image_x']), float(r['image_y'])))
lat0 = math.radians(diab[0])
def en(lat, lon): return ((lon - diab[1]) * math.cos(lat0) * 69.17, (lat - diab[0]) * 69.0)
def inv(x, y): return diab[0] + y / 69.0, diab[1] + x / (math.cos(lat0) * 69.17)
def fit(pts, zero):
    A, b = [], []
    for x, y, X, Y in pts:
        if zero: A.append([x, -y]); b.append(X); A.append([y, x]); b.append(Y)
        else: A.append([x, -y, 1, 0]); b.append(X); A.append([y, x, 0, 1]); b.append(Y)
    sol = np.linalg.lstsq(np.array(A, float), np.array(b, float), rcond=None)[0]
    s = math.hypot(sol[0], sol[1]); th = math.degrees(math.atan2(sol[1], sol[0]))
    t = (0.0, 0.0) if zero else (sol[2], sol[3])
    return s, th, t
def site(theta_rad, s, th, t):
    r_px = 12 * PX_UNIT
    X = r_px * math.cos(theta_rad) - t[0]; Y = r_px * math.sin(theta_rad) - t[1]
    c, sn = math.cos(math.radians(th)), math.sin(math.radians(th))
    x = (c * X + sn * Y) / s; y = (-sn * X + c * Y) / s
    return inv(x, y)
models = {
    'A_five_free_offset': ([0, 1, 2, 3, 4], False),
    'B_four_without_Oakland_free_offset': ([1, 2, 3, 4], False),
    'C_five_crosshair_at_Diablo': ([0, 1, 2, 3, 4], True),
    'D_four_without_Oakland_crosshair_at_Diablo': ([1, 2, 3, 4], True),
}
rows = []
for name, (idxs, zero) in models.items():
    pts = [(*en(cities[i][0], cities[i][1]), cities[i][2] - CX, CY - cities[i][3]) for i in idxs]
    s, th, t = fit(pts, zero)
    p3 = site(3.0, s, th, t); p2 = site(2.0, s, th, t)
    rows.append({'model': name, 'site_theta3_lat': round(p3[0], 5), 'site_theta3_lon': round(p3[1], 5),
                 'site_theta2_lat': round(p2[0], 5), 'site_theta2_lon': round(p2[1], 5),
                 'distance_between_theta3_and_theta2_mi': round(haversine(p3, p2), 3),
                 'dist_theta3_to_road_point_mi': round(haversine(p3, hw), 3),
                 'dist_theta2_to_road_point_mi': round(haversine(p2, hw), 3)})
with open(ROOT / 'results' / 'audit_11_rounding_sensitivity.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
for r in rows: print(r)
print("written audit_11_rounding_sensitivity.csv")

#!/usr/bin/env python3
"""Audit 07 - sensitivity of the map calibration to single landmarks and to label-placement noise.
(a) leave-one-out: remove each city in turn and refit (free-offset and crosshair-at-Diablo models);
(b) noise sweep: Monte Carlo with pixel noise sigma in {6, 15, 30} px and geographic noise
    sigma in {1, 3} miles, for the five-city free-offset model. Reports the spread of miles/unit and
    of the predicted (12,3) location, which the pipeline reported with sigma = 6 px and 1 mile.
Outputs: results/audit_07_leave_one_out.csv, results/audit_07_noise_sweep.csv"""
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
    if r['name'].startswith('Mount Diablo'):
        diab = (float(r['lat']), float(r['lon']))
    elif r['name'].startswith('State Highway'):
        hw = (float(r['lat']), float(r['lon']))
    else:
        cities.append((r['name'], float(r['lat']), float(r['lon']), float(r['image_x']), float(r['image_y'])))
assert len(cities) == 5
lat0 = math.radians(diab[0])
def en(lat, lon):
    return ((lon - diab[1]) * math.cos(lat0) * 69.17, (lat - diab[0]) * 69.0)
def inv(x, y):
    return diab[0] + y / 69.0, diab[1] + x / (math.cos(lat0) * 69.17)
def build(idxs):
    return [(cities[i][0], *en(cities[i][1], cities[i][2]), cities[i][3] - CX, CY - cities[i][4]) for i in idxs]
def fit(pts, zero):
    A, b = [], []
    for _, x, y, X, Y in pts:
        if zero:
            A.append([x, -y]); b.append(X); A.append([y, x]); b.append(Y)
        else:
            A.append([x, -y, 1, 0]); b.append(X); A.append([y, x, 0, 1]); b.append(Y)
    sol = np.linalg.lstsq(np.array(A, float), np.array(b, float), rcond=None)[0]
    s = math.hypot(sol[0], sol[1]); th = math.degrees(math.atan2(sol[1], sol[0]))
    t = (0.0, 0.0) if zero else (sol[2], sol[3])
    return s, th, t
def predict(s, th, t):
    X = 12 * PX_UNIT * math.cos(3.0) - t[0]; Y = 12 * PX_UNIT * math.sin(3.0) - t[1]
    c, sn = math.cos(math.radians(th)), math.sin(math.radians(th))
    x = (c * X + sn * Y) / s; y = (-sn * X + c * Y) / s
    return inv(x, y)

loo_rows = []
for zero, label in [(False, 'free_offset'), (True, 'crosshair_at_Diablo')]:
    for removed in [None] + list(range(5)):
        idxs = [i for i in range(5) if i != removed]
        pts = build(idxs)
        s, th, t = fit(pts, zero)
        lat, lon = predict(s, th, t)
        loo_rows.append({'model': label, 'removed_city': 'none' if removed is None else cities[removed][0],
                         'n_cities': len(idxs), 'px_per_mile': round(s, 3), 'rotation_deg': round(th, 3),
                         'offset_px': f"({t[0]:.1f},{t[1]:.1f})", 'miles_per_unit': round(PX_UNIT / s, 4),
                         'predicted_lat': round(lat, 5), 'predicted_lon': round(lon, 5),
                         'dist_to_road_point_mi': round(haversine((lat, lon), hw), 3)})
with open(ROOT / 'results' / 'audit_07_leave_one_out.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(loo_rows[0].keys())); w.writeheader(); w.writerows(loo_rows)
for r in loo_rows:
    print(r['model'], r['removed_city'], r['px_per_mile'], r['rotation_deg'], r['miles_per_unit'], r['dist_to_road_point_mi'])

rng = np.random.default_rng(2024)
noise_rows = []
base = build(range(5))
for sig_px in (6, 15, 30):
    for sig_mi in (1, 3):
        MU, ROT, PRED = [], [], []
        for _ in range(2000):
            jp = [(n, x + rng.normal(0, sig_mi), y + rng.normal(0, sig_mi), X + rng.normal(0, sig_px), Y + rng.normal(0, sig_px))
                  for n, x, y, X, Y in base]
            s, th, t = fit(jp, False)
            MU.append(PX_UNIT / s); ROT.append(th)
            PRED.append(predict(s, th, t))
        med = (np.median([p[0] for p in PRED]), np.median([p[1] for p in PRED]))
        rad = np.percentile([haversine(med, p) for p in PRED], 95)
        noise_rows.append({'sigma_px': sig_px, 'sigma_miles': sig_mi,
                           'miles_per_unit_2.5_50_97.5': [round(float(v), 3) for v in np.percentile(MU, [2.5, 50, 97.5])],
                           'rotation_deg_2.5_50_97.5': [round(float(v), 2) for v in np.percentile(ROT, [2.5, 50, 97.5])],
                           'predicted_location_95pct_radius_mi': round(float(rad), 3)})
with open(ROOT / 'results' / 'audit_07_noise_sweep.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(noise_rows[0].keys())); w.writeheader()
    for r in noise_rows:
        w.writerow({k: (str(v) if isinstance(v, list) else v) for k, v in r.items()})
for r in noise_rows:
    print(r)

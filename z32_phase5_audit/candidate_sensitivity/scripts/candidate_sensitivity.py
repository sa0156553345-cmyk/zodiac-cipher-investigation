#!/usr/bin/env python3
"""Pre-registered sensitivity grid for the candidate coordinates (see docs/PREREG_CANDIDATE_SENSITIVITY.md).
Uses ONLY archive inputs (crosshair, ring px/unit, landmarks) and the archive's own transform conventions.
No configuration is selected; every row is written to results/candidate_sensitivity_grid.csv."""
import csv, math, sys
from pathlib import Path
import numpy as np

ARCH = Path(__file__).resolve().parents[3] / 'z32_independent_audit'
OUT = Path(__file__).resolve().parents[1] / 'results'; OUT.mkdir(parents=True, exist_ok=True)

CAND = (37.929792, -122.150318)          # candidate supplied by the user (not present in the archive)
TOL_MI = 1.0                             # pre-registered agreement tolerance (R1)

# ---- inputs from archive (verified below) ----
cr = {r['quantity']: r['value'] for r in csv.DictReader(open(ARCH/'results/map_crosshair_and_rings.csv', newline=''))}
CX = float(cr['crosshair_centre_x_px']); CY = float(cr['crosshair_centre_y_px'])
PXU = float(cr['pixels_per_figure_unit'])
IMG_W, IMG_H = 916, 894                 # Figure 2 frame (verified from PNG size)

DIAB = LM = None; HW = None; cities = []
for r in csv.DictReader(open(ARCH/'data/landmarks.csv', newline='', encoding='utf-8')):
    if r['name'].startswith('Mount Diablo'): DIAB = (float(r['lat']), float(r['lon']))
    elif r['name'].startswith('State Highway 24'): HW = (float(r['lat']), float(r['lon']))
    else: cities.append((r['name'], float(r['lat']), float(r['lon']), int(r['image_x']), int(r['image_y'])))
assert len(cities) == 5

lat0 = math.radians(DIAB[0])
def en(lat, lon):   # archive projection (equirectangular about Diablo)
    return ((lon - DIAB[1]) * math.cos(lat0) * 69.17, (lat - DIAB[0]) * 69.0)
def inv(x, y):
    return DIAB[0] + y / 69.0, DIAB[1] + x / (math.cos(lat0) * 69.17)
def haversine(p, q):   # miles, R = 3958.8 (archive convention)
    R = 3958.8; la1, lo1 = map(math.radians, p); la2, lo2 = map(math.radians, q)
    h = math.sin((la2-la1)/2)**2 + math.cos(la1)*math.cos(la2)*math.sin((lo2-lo1)/2)**2
    return 2*R*math.asin(math.sqrt(h))

def fit(sel, zero_offset):
    """Archive's similarity fit: image offset (X,Y) = s*R(th)*(x,y) + t, with (X,Y) relative to crosshair."""
    A = []; b = []
    for i in sel:
        name, la, lo, px, py = cities[i]
        x, y = en(la, lo); X = px - CX; Y = CY - py
        if zero_offset:
            A.append([x, -y]); b.append(X); A.append([y, x]); b.append(Y)
        else:
            A.append([x, -y, 1, 0]); b.append(X); A.append([y, x, 0, 1]); b.append(Y)
    sol = np.linalg.lstsq(np.array(A, float), np.array(b, float), rcond=None)[0]
    s = math.hypot(sol[0], sol[1]); th = math.degrees(math.atan2(sol[1], sol[0]))
    t = (0.0, 0.0) if zero_offset else (float(sol[2]), float(sol[3]))
    return s, th, t

# ---- the eight printed conventions (Figure 2): reference axis x direction ----
AXIS_ANGLE = {'E': 0.0, 'N': 90.0, 'W': 180.0, 'S': 270.0}
DIRS = ['E-CCW', 'E-CW', 'N-CCW', 'N-CW', 'W-CCW', 'W-CW', 'S-CCW', 'S-CW']
def image_angle(dname, theta_rad):
    """Angle (deg, CCW from image east, y up) at which the point (r, theta) is drawn."""
    axis, d = dname.split('-'); t = math.degrees(theta_rad)
    return (AXIS_ANGLE[axis] + (t if d == 'CCW' else -t)) % 360

def point_fit(dname, theta_rad, r_units, s, th, t):
    """Fit-based prediction, mirrors archive predict_12_3 for E-CCW."""
    psi = math.radians(image_angle(dname, theta_rad)); r_px = r_units * PXU
    dx, dy = r_px*math.cos(psi), r_px*math.sin(psi)
    X = dx - t[0]; Y = dy - t[1]
    c, sn = math.cos(math.radians(th)), math.sin(math.radians(th))
    x = (c*X + sn*Y)/s; y = (-sn*X + c*Y)/s
    return inv(x, y)

def point_fixed(dname, theta_rad, r_units, sigma_mi, rho_deg):
    """Fixed printed-scale prediction: distance = r * sigma (miles); geo angle = image angle - rho."""
    psi = image_angle(dname, theta_rad)
    phi = math.radians(psi - rho_deg); R = r_units * sigma_mi
    return inv(R*math.cos(phi), R*math.sin(phi))

def frame_px(lat, lon, A):
    """Map a geographic point back into Figure 2 pixel coordinates via model A's transform (frame check)."""
    s, th, t = A
    x, y = en(lat, lon); c, sn = math.cos(math.radians(th)), math.sin(math.radians(th))
    X = s*(c*x - sn*y) + t[0]; Y = s*(sn*x + c*y) + t[1]
    return CX + X, CY - Y

# ---- sanity: reproduce archive models A-D (E-CCW, theta=3 round) ----
VARIANTS = {'A': ([0,1,2,3,4], False), 'B': ([1,2,3,4], False),
            'C': ([0,1,2,3,4], True),  'D': ([1,2,3,4], True)}
arch_rows = {r['variant'][0]: r for r in csv.DictReader(open(ARCH/'results/map_audit_models.csv', newline=''))}
fits = {}
for v, (sel, zero) in VARIANTS.items():
    s, th, t = fit(sel, zero); fits[v] = (s, th, t)
    lat, lon = point_fit('E-CCW', 3.0, 12, s, th, t)
    ref = [float(z) for z in arch_rows[v]['predicted_12_3_lat_lon'].strip('"').split(',')]
    gap_m = haversine((lat, lon), tuple(ref)) * 1609.344
    print(f"sanity {v}: recomputed ({lat:.5f},{lon:.5f}) vs archive {ref}  gap = {gap_m:.2f} m")
    assert gap_m < 1.0, f"model {v} not reproduced"
print("sanity check passed: models A-D reproduced within 1 m\n")

# ---- constants fixed in the prereg ----
S_G = 28.7 / 5.0   # Grinell-implied miles per inch (SF ~28.7 mi from Diablo, ~5 inches); secondary, derived
S_L = 6.4          # Cipher Mysteries claim; secondary, unsourced here
rho_A = fits['A'][1]

rows = []
def add(family, variant, cities_used, scale_label, sigma, rho_label, rho, origin, dname, rounding, theta_val, lat, lon, A_for_frame):
    d_cand = haversine((lat, lon), CAND)
    d_diab = haversine((lat, lon), DIAB)
    px, py = frame_px(lat, lon, A_for_frame)
    inside = (0 <= px <= IMG_W) and (0 <= py <= IMG_H)
    rows.append({
        'family': family, 'variant': variant, 'cities': cities_used, 'scale_source': scale_label,
        'miles_per_unit': round(sigma, 4), 'rotation_label': rho_label, 'rotation_deg': round(rho, 3),
        'origin': origin, 'direction': dname, 'rounding': rounding, 'theta_rad': theta_val,
        'pred_lat': round(lat, 6), 'pred_lon': round(lon, 6),
        'dist_from_Diablo_mi': round(d_diab, 3), 'dist_to_candidate_mi': round(d_cand, 3),
        'agrees_within_1mi': d_cand <= TOL_MI, 'frame_px_x': round(px, 1), 'frame_px_y': round(py, 1),
        'inside_fig2_frame_via_A': inside,
    })

ROUND_THETA = {'round': 3.0, 'floor': 2.0}
# G1: fit-based variants A-D, all 8 directions x 2 rounding rules
for v, (sel, zero) in VARIANTS.items():
    s, th, t = fits[v]
    for dname in DIRS:
        for rnd, th_rad in ROUND_THETA.items():
            lat, lon = point_fit(dname, th_rad, 12, s, th, t)
            add('G1', v, ','.join(cities[i][0] for i in sel), 'fit (archive)', 12 and (PXU/s), 'fit', th, 'crosshair+fitted offset' if not zero else 'crosshair=Diablo',
                dname, rnd, th_rad, lat, lon, fits['A'])
# G2: fixed printed scales x rho in {A fit, north-up 0} x 8 directions x 2 rounding
for scale_label, sigma in (('Grinell-implied 28.7mi/5in', S_G), ('Cipher-Mysteries 6.4 mi/in', S_L)):
    for rho_label, rho in (('fit_A', rho_A), ('north_up_0', 0.0)):
        for dname in DIRS:
            for rnd, th_rad in ROUND_THETA.items():
                lat, lon = point_fixed(dname, th_rad, 12, sigma, rho)
                add('G2', 'fixed', 'five-or-none', scale_label, sigma, rho_label, rho, 'Diablo at crosshair', dname, rnd, th_rad, lat, lon, fits['A'])
# G3: model A leave-one-city-out (free offset), 8 directions x 2 rounding
for drop in range(5):
    sel = [i for i in range(5) if i != drop]
    s, th, t = fit(sel, False)
    for dname in DIRS:
        for rnd, th_rad in ROUND_THETA.items():
            lat, lon = point_fit(dname, th_rad, 12, s, th, t)
            add('G3', f'A_drop_{cities[drop][0]}', ','.join(cities[i][0] for i in sel), 'fit (LOO)', PXU/s, 'fit', th,
                'crosshair+fitted offset', dname, rnd, th_rad, lat, lon, fits['A'])

keys = list(rows[0].keys())
with open(OUT/'candidate_sensitivity_grid.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=keys); w.writeheader(); w.writerows(rows)
print(f"rows written: {len(rows)} -> {OUT/'candidate_sensitivity_grid.csv'}")

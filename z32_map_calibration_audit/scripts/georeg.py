#!/usr/bin/env python3
"""Georegistration of the figure to geography (pre-registered models G1 to G8).
Equations:  X = A (E,N) + t,   X = pixel offset from the figure centre (east +), Y = pixel offset (north +),
(E,N) = miles east/north of the summit (NAD27) along the geodesic (Vincenty inverse).
Similarity: A = [[a, -b], [b, a]], scale ppm = sqrt(a^2+b^2), rotation phi = atan2(b, a).
Affine: general 2x2 A.  Zero-offset models fix t = 0.
s_fit = U / ppm  (miles per figure unit), U = px per figure unit measured in fig_measure.py.
Outputs: results/georeg_fits.csv, results/georeg_residuals.csv"""
import csv, math
from pathlib import Path
import numpy as np
from geodesy import dms_to_deg, en_miles_from_origin

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / 'results'

def parse_dms(s):
    parts = s.split()
    deg, mi, se, hem = int(parts[0]), int(parts[1]), float(parts[2]), parts[3]
    return dms_to_deg(deg, mi, se, hem)

def read_references():
    refs = {}
    for r in csv.DictReader(open(ROOT / 'data' / 'reference_points.csv', encoding='utf-8')):
        refs[r['name']] = (parse_dms(r['lat_dms']), parse_dms(r['lon_dms']))
    return refs

def read_centre():
    for r in csv.DictReader(open(RES / 'fig_centre_estimates.csv', encoding='utf-8')):
        if r['method'] == 'ring_fits_weighted_mean':
            return float(r['cx_px']), float(r['cy_px'])
    raise RuntimeError('centre not found')

def read_unit():
    for r in csv.DictReader(open(RES / 'fig_px_per_unit_combined.csv', encoding='utf-8')):
        if r['quantity'] == 'px_per_unit_combined':
            return float(r['value'])
    raise RuntimeError('unit not found')

def control_points(summit_key='summit_NAD27'):
    refs = read_references()
    slat, slon = refs[summit_key]
    cx, cy = read_centre()
    pts = []
    for r in csv.DictReader(open(ROOT / 'data' / 'controls.csv', encoding='utf-8')):
        if r['role'] != 'city':
            continue
        E, N = en_miles_from_origin(slat, slon, float(r['lat']), float(r['lon']))
        X = float(r['image_x']) - cx
        Y = cy - float(r['image_y'])
        pts.append({'name': r['name'], 'E': E, 'N': N, 'X': X, 'Y': Y})
    return pts

def fit_similarity(pts, zero_offset=False):
    rows, rhs = [], []
    for p in pts:
        if zero_offset:
            rows.append([p['E'], -p['N']]); rhs.append(p['X'])
            rows.append([p['N'], p['E']]); rhs.append(p['Y'])
        else:
            rows.append([p['E'], -p['N'], 1, 0]); rhs.append(p['X'])
            rows.append([p['N'], p['E'], 0, 1]); rhs.append(p['Y'])
    M = np.array(rows, float); b = np.array(rhs, float)
    sol = np.linalg.lstsq(M, b, rcond=None)[0]
    a, bb = sol[0], sol[1]
    t = np.zeros(2) if zero_offset else np.array([sol[2], sol[3]])
    A = np.array([[a, -bb], [bb, a]])
    return {'kind': 'similarity', 'A': A, 't': t}

def fit_affine(pts):
    rows, rhs = [], []
    for p in pts:
        rows.append([p['E'], p['N'], 0, 0, 1, 0]); rhs.append(p['X'])
        rows.append([0, 0, p['E'], p['N'], 0, 1]); rhs.append(p['Y'])
    sol = np.linalg.lstsq(np.array(rows, float), np.array(rhs, float), rcond=None)[0]
    A = np.array([[sol[0], sol[1]], [sol[2], sol[3]]])
    return {'kind': 'affine', 'A': A, 't': np.array([sol[4], sol[5]])}

def residuals(model, pts):
    out = []
    for p in pts:
        pred = model['A'] @ np.array([p['E'], p['N']]) + model['t']
        out.append((p['name'], pred[0] - p['X'], pred[1] - p['Y']))
    return out

def scale_of(model, U):
    A = model['A']
    if model['kind'] == 'similarity':
        ppm = math.hypot(A[0, 0], A[1, 0])
    else:
        ppm = math.sqrt(abs(np.linalg.det(A)))
    return ppm, U / ppm

def build_models(summit_key='summit_NAD27'):
    pts_all = control_points(summit_key)
    names = [p['name'] for p in pts_all]
    models = {}
    models['G1'] = ('similarity, 5 cities, free offset', fit_similarity(pts_all), pts_all)
    models['G2'] = ('similarity, 5 cities, zero offset (crosshair = summit)', fit_similarity(pts_all, True), pts_all)
    models['G3'] = ('affine, 5 cities, free offset', fit_affine(pts_all), pts_all)
    for i, drop in enumerate(names):
        sub = [p for p in pts_all if p['name'] != drop]
        models[f'G{4 + i}'] = (f'similarity, free offset, without {drop}', fit_similarity(sub), sub)
    return models

if __name__ == '__main__':
    U = read_unit()
    models = build_models()
    rows, rrows = [], []
    for key, (desc, model, pts) in models.items():
        res = residuals(model, pts)
        rms = math.sqrt(np.mean([dx * dx + dy * dy for _, dx, dy in res]) / 2)
        worst = max(math.hypot(dx, dy) for _, dx, dy in res)
        ppm, s_fit = scale_of(model, U)
        A = model['A']; t = model['t']
        phi = math.degrees(math.atan2(A[1, 0], A[0, 0])) if model['kind'] == 'similarity' else float('nan')
        rows.append([key, desc, len(pts), round(ppm, 4), round(s_fit, 4), round(phi, 3) if phi == phi else 'n/a',
                     round(t[0], 2), round(t[1], 2), round(rms, 2), round(worst, 2)])
        for name, dx, dy in res:
            rrows.append([key, name, round(dx, 2), round(dy, 2), round(math.hypot(dx, dy), 2)])
        print(f"{key}: {desc}: px/mile {ppm:.3f}, s_fit {s_fit:.3f} mi/unit, rotation {phi if phi == phi else float('nan'):.2f} deg, "
              f"offset ({t[0]:.1f},{t[1]:.1f}) px, rms {rms:.1f} px, worst {worst:.1f} px")
    with open(RES / 'georeg_fits.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['model', 'description', 'n_cities', 'px_per_mile', 's_fit_miles_per_unit', 'rotation_deg',
                    'offset_x_px', 'offset_y_px', 'rms_residual_px', 'worst_residual_px'])
        w.writerows(rows)
    with open(RES / 'georeg_residuals.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f); w.writerow(['model', 'city', 'residual_x_px', 'residual_y_px', 'residual_px'])
        w.writerows(rrows)
    print("written georeg_fits.csv and georeg_residuals.csv")

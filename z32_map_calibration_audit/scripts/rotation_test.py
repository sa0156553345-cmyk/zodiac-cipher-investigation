#!/usr/bin/env python3
"""Exploratory test (ADDED AFTER the pre-registered runs; reported separately, not used in the
pre-registered decision rules): is the figure drawn with true north up, or rotated by the declination?
Model (fixed rotation phi, free scale s and offset t):
   X = s (cos phi * E - sin phi * N) + tx
   Y = s (sin phi * E + cos phi * N) + ty
Compared rotations: 0 deg (true north up), +16.9 and -16.9 deg (declination east / west), and the free fit.
Outputs: results/rotation_test.csv"""
import csv, math
from pathlib import Path
import numpy as np
from georeg import control_points, read_unit

ROOT = Path(__file__).resolve().parents[1]

def fit_fixed(pts, phi_deg, zero_offset=False):
    ph = math.radians(phi_deg)
    rows, rhs = [], []
    for p in pts:
        u = math.cos(ph) * p['E'] - math.sin(ph) * p['N']
        v = math.sin(ph) * p['E'] + math.cos(ph) * p['N']
        if zero_offset:
            rows.append([u]); rhs.append(p['X'])
            rows.append([v]); rhs.append(p['Y'])
        else:
            rows.append([u, 1, 0]); rhs.append(p['X'])
            rows.append([v, 0, 1]); rhs.append(p['Y'])
    sol = np.linalg.lstsq(np.array(rows, float), np.array(rhs, float), rcond=None)[0]
    s = sol[0]
    t = np.zeros(2) if zero_offset else np.array([sol[1], sol[2]])
    res = []
    for p in pts:
        u = math.cos(ph) * p['E'] - math.sin(ph) * p['N']
        v = math.sin(ph) * p['E'] + math.cos(ph) * p['N']
        res.append(math.hypot(s * u + t[0] - p['X'], s * v + t[1] - p['Y']))
    rms = math.sqrt(np.mean(np.square(res)))
    return s, t, rms, max(res)

if __name__ == '__main__':
    U = read_unit()
    pts = control_points('summit_NAD27')
    rows = []
    for label, phi in (('true north up (0 deg)', 0.0), ('declination east (+16.9 deg)', 16.9),
                       ('declination west (-16.9 deg)', -16.9)):
        for zero in (False, True):
            s, t, rms, worst = fit_fixed(pts, phi, zero)
            rows.append([label, phi, 'zero offset' if zero else 'free offset', round(s, 4), round(U / s, 4),
                         round(t[0], 2), round(t[1], 2), round(rms, 2), round(worst, 2)])
            print(f"{label:32s} {'zero' if zero else 'free'} offset: rms {rms:6.1f} px, worst {worst:6.1f} px, s_fit {U / s:.3f} mi/unit")
    with open(ROOT / 'results' / 'rotation_test.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(['rotation_hypothesis', 'phi_deg', 'offset', 'px_per_mile', 's_fit_miles_per_unit', 'offset_x_px',
                    'offset_y_px', 'rms_residual_px', 'worst_residual_px'])
        w.writerows(rows)

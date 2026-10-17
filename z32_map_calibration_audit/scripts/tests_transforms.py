#!/usr/bin/env python3
"""Independent tests of the transform equations. Run: python3 tests_transforms.py
Tests use synthetic models (A = px/mile * rotation) so the expected answers are known in closed form,
plus consistency checks against the measured results of fig_measure.py and georeg.py.
Exit code 1 if any test fails."""
import csv, math, sys
from pathlib import Path
import numpy as np
from geodesy import vincenty_direct, en_miles_from_origin, METRES_PER_MILE
from transforms import site_EN, EN_to_latlon, in_figure, NUMBERS
from georeg import read_centre, read_unit, read_references, build_models, scale_of

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / 'results'
U = 25.66
results = []
def check(name, cond, detail=''):
    results.append((name, bool(cond)))
    print('PASS' if cond else 'FAIL', name, detail)

def identity_model(ppm=U, phi_deg=0.0, t=(0.0, 0.0)):
    ph = math.radians(phi_deg)
    A = ppm * np.array([[math.cos(ph), -math.sin(ph)], [math.sin(ph), math.cos(ph)]])
    return {'kind': 'similarity', 'A': A, 't': np.array(t, float)}

m = identity_model()           # 1 mile per unit, no rotation, zero offset
EN = lambda r, th, R, D=16.9, s='fit', mdl=m, P='PC': site_EN(r, th, R, D, s, mdl, P, U)

# --- figure geometry and angle conventions (closed form) ---
e = EN(1.0, 0.0, 'R0')
check('R0 theta=0 gives 1 mile east', abs(e[0] - 1) < 1e-9 and abs(e[1]) < 1e-9, f"{e}")
e = EN(1.0, math.pi / 2, 'R0')
check('R0 theta=pi/2 gives 1 mile north (anticlockwise from east)', abs(e[0]) < 1e-9 and abs(e[1] - 1) < 1e-9, f"{e}")
e = EN(1.0, math.pi / 2, 'R1')
check('R1 theta=pi/2 gives 1 mile south (clockwise)', abs(e[0]) < 1e-9 and abs(e[1] + 1) < 1e-9, f"{e}")
e = EN(1.0, 3.0, 'R0')
check('R0 theta=3 rad lies WNW of east (171.9 deg)', e[0] < 0 and e[1] > 0 and abs(math.degrees(math.atan2(e[1], e[0])) - 171.887) < 0.01,
      f"angle {math.degrees(math.atan2(e[1], e[0])):.3f}")
check('3 radians equals 171.887 degrees (not 3 degrees)', abs(math.degrees(3.0) - 171.887) < 0.001)

# --- magnetic references ---
e = EN(1.0, 0.0, 'R2', D=16.9)
b = math.degrees(math.atan2(e[0], e[1])) % 360
check('R2 theta=0 gives bearing = declination (16.9)', abs(b - 16.9) < 1e-6, f"bearing {b:.6f}")
e = EN(1.0, math.pi / 2, 'R2', D=16.9)
b = math.degrees(math.atan2(e[0], e[1])) % 360
check('R2 theta=90 deg gives bearing 106.9', abs(b - 106.9) < 1e-6, f"bearing {b:.6f}")
e = EN(1.0, math.pi / 2, 'R3', D=16.9)
b = math.degrees(math.atan2(e[0], e[1])) % 360
check('R3 theta=90 deg gives bearing -73.1 (= 286.9)', abs(b - 286.9) < 1e-6, f"bearing {b:.6f}")
e = EN(1.0, 0.0, 'R4p', D=16.9); b = math.degrees(math.atan2(e[0], e[1])) % 360
check('R4p (+D) theta=0 gives bearing 106.9', abs(b - 106.9) < 1e-6, f"bearing {b:.6f}")
e = EN(1.0, 0.0, 'R4m', D=16.9); b = math.degrees(math.atan2(e[0], e[1])) % 360
check('R4m (-D) theta=0 gives bearing 73.1', abs(b - 73.1) < 1e-6, f"bearing {b:.6f}")

# --- number pairs and the rounding convention ---
check('round(16.9/6) = 3 minutes', round(16.9 / 6) == 3)
check('floor(16.9/6) = 2 minutes', math.floor(16.9 / 6) == 2)
check('N_round is (12,3), N_floor is (12,2)', NUMBERS['N_round'] == (12.0, 3.0) and NUMBERS['N_floor'] == (12.0, 2.0))

# --- scale ---
e = EN(12.0, 3.0, 'R0', s=6.4)
check('scale 6.4 gives 76.8 miles for 12 units', abs(math.hypot(*e) - 76.8) < 1e-6, f"{math.hypot(*e):.4f} mi")
e1 = EN(12.0, 3.0, 'R0', s=1.0)
check('fixed scale 1.0 gives 12 miles for 12 units', abs(math.hypot(*e1) - 12.0) < 1e-6, f"{math.hypot(*e1):.6f}")
# numeric scale equal to s_fit reproduces the exact figure-displacement mode for a similarity map
gmod = build_models('summit_NAD27')['G1'][1]
ppm, s_fit = scale_of(gmod, U)
ea = site_EN(12.0, 3.0, 'R0', 16.9, 'fit', gmod, 'PC', U)
eb = site_EN(12.0, 3.0, 'R0', 16.9, s_fit, gmod, 'PC', U)
check('numeric s = s_fit equals exact figure mode for a similarity fit', np.allclose(ea, eb, atol=1e-6),
      f"difference {np.linalg.norm(ea - eb):.2e} mi")

# --- affine: exact inverse mapping ---
A = np.array([[20.0, 3.0], [-2.0, 22.0]]); mdl = {'kind': 'affine', 'A': A, 't': np.array([5.0, -4.0])}
EN_a = site_EN(12.0, 3.0, 'R0', 16.9, 'fit', mdl, 'PC', U)
X = mdl['A'] @ EN_a + mdl['t']
X_expected = mdl['A'] @ (np.linalg.inv(A) @ (-mdl['t'])) + mdl['t'] + 12.0 * U * np.array([math.cos(3.0), math.sin(3.0)])
check('affine: figure displacement maps back exactly', np.allclose(X - (mdl['A'] @ (np.linalg.inv(A) @ (-mdl['t'])) + mdl['t']),
                                                                   12.0 * U * np.array([math.cos(3.0), math.sin(3.0)]), atol=1e-6))

# --- pole choice ---
mz = {'kind': 'similarity', 'A': m['A'], 't': np.zeros(2)}
check('zero-offset model: PC and PS poles coincide', np.allclose(EN(12, 3, 'R0', mdl=mz, P='PC'), EN(12, 3, 'R0', mdl=mz, P='PS')))
mo = identity_model(t=(10.0, 0.0))
pc_origin = np.linalg.inv(mo['A']) @ (-mo['t'])
pc_site = site_EN(0.0, 3.0, 'R0', 16.9, 'fit', mo, 'PC', U)
ps_site = site_EN(0.0, 3.0, 'R0', 16.9, 'fit', mo, 'PS', U)
check('offset model: PC and PS poles differ by exactly A^-1(-t)',
      np.allclose(pc_site - ps_site, pc_origin, atol=1e-9) and np.linalg.norm(pc_origin) > 0.1,
      f"difference {np.round(pc_site - ps_site, 4)} vs A^-1(-t) {np.round(pc_origin, 4)}")
check('crosshair pole maps to A^-1(-t)', np.allclose(site_EN(0.0, 3.0, 'R0', 16.9, 'fit', mo, 'PC', U), pc_origin, atol=1e-9))
check('physical-summit pole gives origin (0,0)', np.allclose(site_EN(0.0, 3.0, 'R0', 16.9, 'fit', mo, 'PS', U), [0, 0]))

# --- geodesy round trip inside the transform ---
slat, slon = read_references()['summit_NAD27']
E_, N_ = EN(5.0, 1.0, 'R0', mdl=identity_model(ppm=U, phi_deg=-4.7))
lat, lon = EN_to_latlon((E_, N_), slat, slon)
E2, N2 = en_miles_from_origin(slat, slon, lat, lon)
check('EN -> lat/lon -> EN round trip (< 1e-6 mi)', abs(E2 - E_) < 1e-6 and abs(N2 - N_) < 1e-6, f"{E2 - E_:.2e}, {N2 - N_:.2e}")

# --- feasibility frame ---
inside, px, py = in_figure(EN(12.0, 3.0, 'R0', s=6.4, mdl=gmod), gmod, *read_centre())
check('6.4 mi/unit puts the site outside the figure frame (infeasible)', not inside, f"px {px:.0f}, py {py:.0f}")
inside, px, py = in_figure(site_EN(12.0, 3.0, 'R0', 16.9, 'fit', gmod, 'PC', U), gmod, *read_centre())
check('baseline (12,3) with fitted scale lies inside the figure frame', inside, f"px {px:.1f}, py {py:.1f}")

# --- consistency with the measured figure (results written by earlier steps) ---
mc = {r['quantity']: r['value'] for r in csv.DictReader(open(RES / 'fig_marker_consistency.csv', encoding='utf-8'))}
diff = float(mc['difference_px'])
check('Foxon white marker equals predicted (12 units, 3 rad) in the figure frame (< 3 px)', diff < 3.0, f"{diff} px")
ang = list(csv.DictReader(open(RES / 'fig_angle_labels.csv', encoding='utf-8')))
mx = max(abs(float(r['residual_deg'])) for r in ang)
check('outer angle labels follow east=0, anticlockwise, radians (max residual < 1 deg)', mx < 1.0, f"max {mx:.2f} deg")

# --- vincenty direct consistency on the baseline site ---
e = site_EN(12.0, 3.0, 'R0', 16.9, 'fit', gmod, 'PC', U)
lat, lon = EN_to_latlon(e, slat, slon)
from geodesy import geodesic_miles
d_v = geodesic_miles(slat, slon, lat, lon)
check('baseline site: Vincenty distance from summit equals the EN magnitude (< 0.1 %)', abs(d_v - math.hypot(*e)) / max(d_v, 1e-9) < 1e-3,
      f"Vincenty {d_v:.5f}, EN {math.hypot(*e):.5f}")

failed = [n for n, ok in results if not ok]
print(f"\n{len(results) - len(failed)} of {len(results)} tests passed")
sys.exit(1 if failed else 0)

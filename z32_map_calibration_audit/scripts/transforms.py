#!/usr/bin/env python3
"""Transform family from figure numbers (r, theta) to geographic sites, pre-registered in
docs/PREREGISTRATION_TRANSFORMS.md. Equations are written in the docstrings of each function.
Positions are kept as (E,N) miles from the summit (NAD27); latitude/longitude is produced at the end
by the Vincenty direct formula, and tangent-plane distances between sites are checked against Vincenty.
Outputs: results/transform_grid.csv (9600 rows), results/transform_summary.csv,
         results/transform_sensitivity.csv, results/scale_curve.csv, results/noctrl_family.csv,
         results/degrees_unsupported.csv"""
import csv, math
from pathlib import Path
import numpy as np
from PIL import Image
from geodesy import vincenty_direct, geodesic_miles, en_miles_from_origin, METRES_PER_MILE
from georeg import build_models, read_centre, read_unit, read_references, parse_dms, scale_of

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / 'results'
W, H = Image.open(ROOT / 'images' / 'fig2_map_p9_native.png').size
TWO_PI = 2 * math.pi

NUMBERS = {  # (r in units, theta in radians) as listed in the pre-registration
    'N_round': (12.0, 3.0),
    'N_floor': (12.0, 2.0),
    'N_30': (3.0, 0.0),
    'N_312': (3.0, 12.0 - TWO_PI),
    'N_03': (0.0, 3.0),
}
R_OPTIONS = ['R0', 'R1', 'R2', 'R3', 'R4p', 'R4m']
D_OPTIONS = [0.0, 15.0, 16.3, 16.9, 17.7]
S_OPTIONS = ['fit', 6.4]
P_OPTIONS = ['PC', 'PS']

def bearing_vector(beta_deg):
    """Compass bearing (deg clockwise from north) -> (E,N) unit vector."""
    b = math.radians(beta_deg)
    return np.array([math.sin(b), math.cos(b)])

def site_EN(r, th, R, D, s, model, P, U):
    """Return (E,N) miles from the summit.
    Equations:
      origin:  PC -> O = A^-1 (0 - t) ;  PS -> O = (0,0)
      R0 figure east ccw:  v = (cos th, sin th);   R1: v = (cos th, -sin th)
          s == 'fit': displacement = A^-1 (r U v)
          numeric s:  displacement = r s (A^-1 v)/|A^-1 v|
      R2: beta = th_deg + D ;  R3: beta = D - th_deg
      R4p: beta = beta(R0) + D ;  R4m: beta = beta(R0) - D
          displacement = r s (sin beta, cos beta)  (s numeric or 'fit' = s_fit)
    """
    A = model['A']; t = model['t']
    Ainv = np.linalg.inv(A)
    ppm, s_fit = scale_of(model, U)
    origin = Ainv @ (-t) if P == 'PC' else np.zeros(2)
    v0 = np.array([math.cos(th), math.sin(th)])
    v1 = np.array([math.cos(th), -math.sin(th)])
    if R in ('R0', 'R1'):
        v = v0 if R == 'R0' else v1
        if s == 'fit':
            disp = Ainv @ (r * U * v)
        else:
            w = Ainv @ v
            n = np.linalg.norm(w)
            disp = r * s * w / n if n > 0 else np.zeros(2)
    else:
        s_num = s_fit if s == 'fit' else s
        th_deg = math.degrees(th)
        w0 = Ainv @ v0
        beta_R0 = math.degrees(math.atan2(w0[0], w0[1])) % 360.0
        if R == 'R2':
            beta = th_deg + D
        elif R == 'R3':
            beta = D - th_deg
        elif R == 'R4p':
            beta = beta_R0 + D
        elif R == 'R4m':
            beta = beta_R0 - D
        else:
            raise ValueError(R)
        disp = r * s_num * bearing_vector(beta)
    return origin + disp

def EN_to_latlon(EN, slat, slon):
    E, N = EN
    d_m = math.hypot(E, N) * METRES_PER_MILE
    az = math.degrees(math.atan2(E, N)) % 360.0
    lat, lon, _ = vincenty_direct(slat, slon, az, d_m)
    return lat, lon

def in_figure(EN, model, cx, cy):
    X = model['A'] @ EN + model['t']
    px, py = cx + X[0], cy - X[1]
    return (0 <= px <= W - 1 and 0 <= py <= H - 1), px, py

def read_road_point():
    refs = read_references()
    return refs['road_point_HW24']

def main():
    U = read_unit()
    cx, cy = read_centre()
    refs = read_references()
    slat, slon = refs['summit_NAD27']
    models = build_models('summit_NAD27')
    hw = refs['road_point_HW24']

    baseline_key = ('N_round', 'R0', 16.9, 'fit', 'G1', 'PC')
    rows = []
    cfg_id = 0
    cache = {}
    for numkey, R, D, s, G, P in __import__('itertools').product(NUMBERS, R_OPTIONS, D_OPTIONS, S_OPTIONS, models.keys(), P_OPTIONS):
        cfg_id += 1
        model = models[G][1]
        r, th = NUMBERS[numkey]
        EN = site_EN(r, th, R, D, s, model, P, U)
        lat, lon = EN_to_latlon(EN, slat, slon)
        inside, px, py = in_figure(EN, model, cx, cy)
        rows.append({'cfg_id': cfg_id, 'number': numkey, 'r_units': r, 'theta_rad': round(th, 6), 'reference': R,
                     'declination_deg': D, 'scale': s, 'georeg': G, 'pole': P,
                     'E_mi': round(float(EN[0]), 4), 'N_mi': round(float(EN[1]), 4),
                     'lat': round(lat, 6), 'lon': round(lon, 6), 'px': round(px, 2), 'py': round(py, 2),
                     'inside_figure': inside, 'key': (numkey, R, D, s, G, P), 'EN': EN})
    base = [x for x in rows if x['key'] == baseline_key][0]
    for x in rows:
        x['dist_from_baseline_mi'] = round(float(math.hypot(x['EN'][0] - base['EN'][0], x['EN'][1] - base['EN'][1])), 4)
        x['dist_from_road_point_mi_NOT_USED_FOR_SELECTION'] = round(geodesic_miles(x['lat'], x['lon'], hw[0], hw[1]), 4)
    out_cols = ['cfg_id', 'number', 'r_units', 'theta_rad', 'reference', 'declination_deg', 'scale', 'georeg', 'pole',
                'E_mi', 'N_mi', 'lat', 'lon', 'px', 'py', 'inside_figure', 'dist_from_baseline_mi',
                'dist_from_road_point_mi_NOT_USED_FOR_SELECTION']
    with open(RES / 'transform_grid.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=out_cols, extrasaction='ignore', lineterminator='\n')
        w.writeheader(); w.writerows(rows)
    feas = [x for x in rows if x['inside_figure']]
    print(f"configurations: {len(rows)}; inside the figure frame: {len(feas)}")
    print(f"baseline (N_round, R0, D=16.9, fit, G1, PC): lat {base['lat']:.5f}, lon {base['lon']:.5f}, inside={base['inside_figure']}")

    # ---------- summary ----------
    def spread(xs):
        if len(xs) < 2:
            return 0.0
        E = np.array([x['EN'][0] for x in xs]); N = np.array([x['EN'][1] for x in xs])
        d = np.hypot(E[:, None] - E[None, :], N[:, None] - N[None, :])
        return float(d.max())

    core = [x for x in feas if x['key'][1] == 'R0' and x['key'][0] == 'N_round' and x['key'][3] == 'fit'
            and x['key'][2] in (16.3, 16.9, 17.7)]
    summary = [
        ('configurations_total', len(rows)),
        ('configurations_inside_figure', len(feas)),
        ('baseline_lat', base['lat']), ('baseline_lon', base['lon']),
        ('baseline_inside_figure', base['inside_figure']),
        ('core_paper_supported_set_size', len(core)),
        ('core_max_pairwise_spread_mi', round(spread(core), 3)),
        ('all_feasible_max_pairwise_spread_mi', round(spread(feas), 3)),
        ('pre_registered_threshold_mi', 1.0),
        ('core_determines_location_to_threshold', spread(core) < 1.0),
        ('all_feasible_determines_location_to_threshold', spread(feas) < 1.0),
    ]
    for factor, levels in (('number', list(NUMBERS)), ('reference', R_OPTIONS), ('scale', S_OPTIONS),
                           ('pole', P_OPTIONS), ('georeg', list(models.keys()))):
        for lv in levels:
            n_in = sum(1 for x in feas if x[factor] == lv)
            summary.append((f'feasible_count[{factor}={lv}]', n_in))
    summary.append(('s_6.4_configurations_inside_figure', sum(1 for x in feas if x['scale'] == 6.4)))
    with open(RES / 'transform_summary.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f, lineterminator='\n'); w.writerow(['quantity', 'value']); w.writerows(summary)
    for q, v in summary[:12]:
        print(f"{q}: {v}")

    # ---------- one-at-a-time sensitivity from the baseline ----------
    sens = []
    def row(label, key, note=''):
        m = [x for x in rows if x['key'] == key]
        if not m:
            return
        x = m[0]
        d = math.hypot(x['EN'][0] - base['EN'][0], x['EN'][1] - base['EN'][1])
        sens.append((label, round(x['lat'], 5), round(x['lon'], 5), x['inside_figure'], round(d, 3), note))
    row('baseline', baseline_key, 'paper convention (round, east-ccw, D=16.9, fit, G1, crosshair pole)')
    for nk in ('N_floor', 'N_30', 'N_312', 'N_03'):
        row(f'number {nk}', (nk, 'R0', 16.9, 'fit', 'G1', 'PC'), 'number pair alternative')
    for rk in ('R1', 'R2', 'R3', 'R4p', 'R4m'):
        row(f'reference {rk}', ('N_round', rk, 16.9, 'fit', 'G1', 'PC'), 'angle reference alternative')
    for D in (0.0, 15.0, 16.3, 17.7):
        row(f'declination {D} (R0)', ('N_round', 'R0', D, 'fit', 'G1', 'PC'), 'declination has no effect on R0 (only R2-R4)')
        row(f'declination {D} (R2)', ('N_round', 'R2', D, 'fit', 'G1', 'PC'), 'declination enters R2')
    row('scale 6.4 mi/unit', ('N_round', 'R0', 16.9, 6.4, 'G1', 'PC'), 'external claim')
    for g in ('G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8'):
        row(f'georeg {g}', ('N_round', 'R0', 16.9, 'fit', g, 'PC'), models[g][0])
    row('pole = physical summit (PS)', ('N_round', 'R0', 16.9, 'fit', 'G1', 'PS'), 'pole alternative')
    # datum sensitivity: summit in USSD (same georeg, different origin)
    models_u = build_models('summit_USSD')
    slat_u, slon_u = refs['summit_USSD']
    EN_u = site_EN(12.0, 3.0, 'R0', 16.9, 'fit', models_u['G1'][1], 'PC', U)
    lat_u, lon_u = EN_to_latlon(EN_u, slat_u, slon_u)
    sens.append(('datum summit USSD instead of NAD27 (R0, G1, PC)', round(lat_u, 5), round(lon_u, 5),
                 in_figure(EN_u, models_u['G1'][1], cx, cy)[0],
                 round(math.hypot(EN_u[0] - base['EN'][0], EN_u[1] - base['EN'][1]), 3), 'datum sensitivity'))
    with open(RES / 'transform_sensitivity.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(['change_from_baseline', 'lat', 'lon', 'inside_figure', 'shift_from_baseline_mi', 'note'])
        w.writerows(sens)
    for s_ in sens:
        print(f"{s_[0]}: shift {s_[4]} mi, inside={s_[3]}")

    # ---------- scale curve (baseline direction, G1, crosshair pole) ----------
    sc = []
    model1 = models['G1'][1]
    s_grid = [0.5 + 0.25 * i for i in range(27)]
    for R in ('R0', 'R2'):
        for s_val in s_grid:
            EN = site_EN(12.0, 3.0, R, 16.9, s_val, model1, 'PC', U)
            inside, px, py = in_figure(EN, model1, cx, cy)
            sc.append((R, s_val, round(float(EN[0]), 3), round(float(EN[1]), 3), inside,
                       round(math.hypot(EN[0], EN[1]), 3)))
    with open(RES / 'scale_curve.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(['reference', 'scale_mi_per_unit', 'E_mi', 'N_mi', 'inside_figure', 'distance_from_summit_mi'])
        w.writerows(sc)

    # ---------- no control: scale and orientation free (crosshair = summit, no city data) ----------
    nc = []
    for s_val in (0.8, 1.0, 1.166, 1.5, 2.0, 3.0, 4.0, 6.4):
        for phi in (-10.0, -5.0, 0.0, 5.0, 10.0):
            ppm = U / s_val
            ph = math.radians(phi)
            A = ppm * np.array([[math.cos(ph), -math.sin(ph)], [math.sin(ph), math.cos(ph)]])
            mdl = {'kind': 'similarity', 'A': A, 't': np.zeros(2)}
            EN = site_EN(12.0, 3.0, 'R0', 16.9, 'fit', mdl, 'PC', U)
            lat, lon = EN_to_latlon(EN, slat, slon)
            inside, px, py = in_figure(EN, mdl, cx, cy)
            nc.append((s_val, phi, round(lat, 5), round(lon, 5), inside,
                       round(math.hypot(EN[0] - base['EN'][0], EN[1] - base['EN'][1]), 3)))
    with open(RES / 'noctrl_family.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(['scale_mi_per_unit', 'orientation_deg', 'lat', 'lon', 'inside_figure', 'shift_from_baseline_mi',
                    'frame_test_meaningful'])
        for row_ in nc:
            w.writerow(list(row_) + ['NO: no city georeference in this family; frame scales with the assumed unit'])

    # ---------- degrees instead of radians (NOT supported by the text; reported only) ----------
    dg = []
    for R in ('R0', 'R2'):
        EN = site_EN(12.0, math.radians(3.0), R, 16.9, 'fit', model1, 'PC', U)
        lat, lon = EN_to_latlon(EN, slat, slon)
        dg.append((R, round(lat, 5), round(lon, 5), in_figure(EN, model1, cx, cy)[0]))
    with open(RES / 'degrees_unsupported.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(['reference', 'lat', 'lon', 'inside_figure'])
        w.writerows(dg)
    print("written transform outputs")

if __name__ == '__main__':
    main()

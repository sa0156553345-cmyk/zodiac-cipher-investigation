#!/usr/bin/env python3
"""Map audit using ONLY: (a) pixel measurements on images/fig2_map_p9_native.png, and
(b) coordinates listed with sources in data/landmarks.csv.  No remembered coordinates.
Outputs: results/map_crosshair_and_rings.csv, results/map_audit_models.csv,
         results/map_audit_landmarks.csv"""
import csv, math
import numpy as np
from PIL import Image
from common import IMAGES, DATA, RESULTS

# ---------- 1. measurements on the image ----------
a = np.array(Image.open(IMAGES / 'fig2_map_p9_native.png').convert('L')).astype(int)
dark = a < 90
col_counts = dark[150:750, :].sum(axis=0); row_counts = dark[:, 150:750].sum(axis=1)
CX = int(np.argmax(col_counts[300:700])) + 300
CY = int(np.argmax(row_counts[300:600])) + 300

def ring_score(r):
    hits = tot = 0
    for deg in np.arange(0, 360, 0.5):
        if min(abs(((deg - k + 180) % 360) - 180) for k in range(0, 360, 45)) < 6: continue
        t = math.radians(deg)
        x = int(round(CX + r * math.cos(t))); y = int(round(CY - r * math.sin(t)))
        tot += 1; hits += bool(dark[max(0, y - 1):y + 2, max(0, x - 1):x + 2].any())
    return hits / max(tot, 1)

WINDOWS = {4: (95, 110), 8: (195, 215), 12: (300, 315)}
ring_px = {n: max(range(lo, hi + 1), key=ring_score) for n, (lo, hi) in WINDOWS.items()}
ring_sc = {n: round(ring_score(r), 3) for n, r in ring_px.items()}
PX_UNIT = sum(r * n for n, r in ring_px.items()) / sum(n * n for n in ring_px)
with open(RESULTS / 'map_crosshair_and_rings.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['quantity', 'value', 'score_or_note'])
    w.writerow(['crosshair_centre_x_px', CX, 'projection of dark line columns'])
    w.writerow(['crosshair_centre_y_px', CY, 'projection of dark line rows'])
    for n in (4, 8, 12):
        w.writerow([f'ring_labelled_{n}_radius_px', ring_px[n], f'ring score {ring_sc[n]}'])
    w.writerow(['pixels_per_figure_unit', round(PX_UNIT, 3), 'least squares through origin'])

# ---------- 2. landmarks (sourced) ----------
LM = []; HW = None
with open(DATA / 'landmarks.csv', newline='', encoding='utf-8') as f:
    for r in csv.DictReader(f):
        if r['name'].startswith('Mount Diablo'): DIAB = (float(r['lat']), float(r['lon']))
        elif r['name'].startswith('State Highway 24'): HW = (float(r['lat']), float(r['lon']))
        else: LM.append((r['name'], float(r['lat']), float(r['lon']), int(r['image_x']), int(r['image_y'])))
assert len(LM) == 5

lat0 = math.radians(DIAB[0])
def en(lat, lon):
    return ((lon - DIAB[1]) * math.cos(lat0) * 69.17, (lat - DIAB[0]) * 69.0)
def inv(x, y):
    return DIAB[0] + y / 69.0, DIAB[1] + x / (math.cos(lat0) * 69.17)
def haversine(p, q):
    R = 3958.8; la1, lo1 = map(math.radians, p); la2, lo2 = map(math.radians, q)
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))
def bearing(p, q):
    la1, lo1 = map(math.radians, p); la2, lo2 = map(math.radians, q); dl = lo2 - lo1
    y = math.sin(dl) * math.cos(la2); x = math.cos(la1) * math.sin(la2) - math.sin(la1) * math.cos(la2) * math.cos(dl)
    return (math.degrees(math.atan2(y, x)) + 360) % 360

def pts_for(names_idx, origin_xy):
    out = []
    for i in names_idx:
        name, la, lo, px, py = LM[i]
        x, y = en(la, lo); out.append((name, x, y, px - origin_xy[0], origin_xy[1] - py))
    return out

def fit(pts, zero_offset):
    A = []; b = []
    for _, x, y, X, Y in pts:
        if zero_offset:
            A.append([x, -y]); b.append(X); A.append([y, x]); b.append(Y)
        else:
            A.append([x, -y, 1, 0]); b.append(X); A.append([y, x, 0, 1]); b.append(Y)
    sol = np.linalg.lstsq(np.array(A, float), np.array(b, float), rcond=None)[0]
    s = math.hypot(sol[0], sol[1]); th = math.degrees(math.atan2(sol[1], sol[0]))
    t = (0.0, 0.0) if zero_offset else (sol[2], sol[3])
    return s, th, t

def predict_12_3(s, th, t):
    r_px = 12 * PX_UNIT
    dx, dy = r_px * math.cos(3.0), r_px * math.sin(3.0)     # image: x east, y north; angle 3 rad from east, anticlockwise
    X = dx - t[0]; Y = dy - t[1]
    c, sn = math.cos(math.radians(th)), math.sin(math.radians(th))
    x = (c * X + sn * Y) / s; y = (-sn * X + c * Y) / s
    return inv(x, y)

def residuals(pts, s, th, t):
    c, sn = math.cos(math.radians(th)), math.sin(math.radians(th)); out = []
    for _, x, y, X, Y in pts:
        out.append(round(math.hypot(s * (c * x - sn * y) + t[0] - X, s * (sn * x + c * y) + t[1] - Y), 1))
    return out

VARIANTS = {
    'A_five_cities_free_offset': ([0, 1, 2, 3, 4], False),
    'B_four_cities_without_Oakland_free_offset': ([1, 2, 3, 4], False),
    'C_five_cities_crosshair_at_Diablo': ([0, 1, 2, 3, 4], True),
    'D_four_cities_without_Oakland_crosshair_at_Diablo': ([1, 2, 3, 4], True),
}
rng = np.random.default_rng(7)
ORIGIN = (CX, CY)
rows_models = []; land_rows = []
for vname, (idxs, zero) in VARIANTS.items():
    pts = pts_for(idxs, ORIGIN)
    s, th, t = fit(pts, zero)
    res = residuals(pts, s, th, t)
    lat, lon = predict_12_3(s, th, t)
    d_hw = haversine((lat, lon), HW)
    MU = []; TH = []; DH = []; PRED = []
    for _ in range(3000):
        jp = [(n, x + rng.normal(0, 1.0), y + rng.normal(0, 1.0), X + rng.normal(0, 6), Y + rng.normal(0, 6))
              for n, x, y, X, Y in pts]
        s2, th2, t2 = fit(jp, zero)
        la2, lo2 = predict_12_3(s2, th2, t2)
        MU.append(PX_UNIT / s2); TH.append(th2); DH.append(haversine((la2, lo2), HW)); PRED.append((la2, lo2))
    q = lambda v: [round(float(np.percentile(v, p)), 3) for p in (2.5, 50, 97.5)]
    med = (float(np.median([p[0] for p in PRED])), float(np.median([p[1] for p in PRED])))
    spread = [haversine(med, p) for p in PRED]
    rows_models.append({
        'variant': vname, 'cities': len(idxs), 'offset_free': not zero,
        'px_per_mile_fit': round(s, 3), 'rotation_deg_fit': round(th, 3),
        'offset_px_fit': f"({t[0]:.1f},{t[1]:.1f})", 'residuals_px': str(res),
        'miles_per_unit_point': round(PX_UNIT / s, 4), 'miles_per_unit_MC_2.5_50_97.5': str(q(MU)),
        'rotation_MC_2.5_50_97.5': str(q(TH)),
        'predicted_12_3_lat_lon': f"{lat:.5f},{lon:.5f}",
        'distance_predicted_to_HW24_mi': round(d_hw, 3), 'distance_to_HW24_MC_2.5_50_97.5': str(q(DH)),
        'predicted_location_95pct_radius_mi': round(float(np.percentile(spread, 95)), 3),
    })
    if vname.startswith('A_'):
        for (name, x, y, X, Y), r in zip(pts, res):
            la, lo = [(l[1], l[2]) for l in LM if l[0] == name][0]
            land_rows.append({'landmark': name, 'miles_east': round(x, 3), 'miles_north': round(y, 3),
                              'image_dx_px': X, 'image_dy_px': Y,
                              'px_per_mile_raw': round(math.hypot(X, Y) / math.hypot(x, y), 3),
                              'geo_bearing_deg': round(bearing(DIAB, (la, lo)), 2),
                              'image_bearing_deg': round((math.degrees(math.atan2(X, Y)) + 360) % 360, 2),
                              'fit_residual_px': r})

with open(RESULTS / 'map_audit_models.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(rows_models[0].keys())); w.writeheader(); w.writerows(rows_models)
with open(RESULTS / 'map_audit_landmarks.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(land_rows[0].keys())); w.writeheader(); w.writerows(land_rows)

print(f"crosshair centre (px) = ({CX},{CY}); pixels per figure unit = {PX_UNIT:.2f}; ring scores {ring_sc}")
for r in rows_models:
    print(f"\n{r['variant']}")
    print(f"  px/mile={r['px_per_mile_fit']}  rotation={r['rotation_deg_fit']} deg  offset={r['offset_px_fit']} px")
    print(f"  residuals px={r['residuals_px']}")
    print(f"  miles/unit point={r['miles_per_unit_point']}  MC 2.5/50/97.5 = {r['miles_per_unit_MC_2.5_50_97.5']}")
    print(f"  (12,3) predicted {r['predicted_12_3_lat_lon']}; to Hwy24 {r['distance_predicted_to_HW24_mi']} mi; MC {r['distance_to_HW24_MC_2.5_50_97.5']}; 95% radius {r['predicted_location_95pct_radius_mi']} mi")
needed = PX_UNIT / 6.4
print(f"\nclaimed 6.4 mi/unit requires {needed:.2f} px/mile; fitted px/mile range = {min(r['px_per_mile_fit'] for r in rows_models)}-{max(r['px_per_mile_fit'] for r in rows_models)}")
print("written: map_crosshair_and_rings.csv, map_audit_models.csv, map_audit_landmarks.csv")

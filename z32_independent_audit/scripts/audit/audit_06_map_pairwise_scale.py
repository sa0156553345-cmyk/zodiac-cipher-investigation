#!/usr/bin/env python3
"""Audit 06 - scale and orientation from every pair of points, without choosing an origin.
Points: the five sourced city centres (data/landmarks.csv) and the crosshair/Mount Diablo.
For each pair: great-circle distance (miles), image distance (pixels), pixels per mile, implied
miles per figure unit, and the difference between the image bearing and the geographic bearing.
A rigid similarity map would give one scale and one rotation for all pairs.
Outputs: results/audit_06_pairwise.csv, results/audit_06_summary.csv"""
import csv, math, itertools
from pathlib import Path
import statistics as st

ROOT = Path(__file__).resolve().parents[2]
R_EARTH = 3958.8
def haversine(p, q):
    la1, lo1 = map(math.radians, p); la2, lo2 = map(math.radians, q)
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * R_EARTH * math.asin(math.sqrt(h))
def bearing(p, q):
    la1, lo1 = map(math.radians, p); la2, lo2 = map(math.radians, q); dl = lo2 - lo1
    y = math.sin(dl) * math.cos(la2); x = math.cos(la1) * math.sin(la2) - math.sin(la1) * math.cos(la2) * math.cos(dl)
    return (math.degrees(math.atan2(y, x)) + 360) % 360

pts = []
for r in csv.DictReader(open(ROOT / 'data' / 'landmarks.csv', encoding='utf-8')):
    if r['name'].startswith('State Highway'):
        continue
    if r['name'].startswith('Mount Diablo'):
        continue
    pts.append((r['name'], float(r['lat']), float(r['lon']), float(r['image_x']), float(r['image_y'])))
cross = {r['quantity']: r['value'] for r in csv.DictReader(open(ROOT / 'results' / 'map_crosshair_and_rings.csv', encoding='utf-8'))}
CX, CY = float(cross['crosshair_centre_x_px']), float(cross['crosshair_centre_y_px'])
PX_UNIT = float(cross['pixels_per_figure_unit'])
diab = [r for r in csv.DictReader(open(ROOT / 'data' / 'landmarks.csv', encoding='utf-8')) if r['name'].startswith('Mount Diablo')][0]
pts.append(('Mount Diablo (crosshair)', float(diab['lat']), float(diab['lon']), CX, CY))

rows = []
for a, b in itertools.combinations(pts, 2):
    mi = haversine((a[1], a[2]), (b[1], b[2]))
    dX = (b[3] - a[3]); dY = (a[4] - b[4])           # image: x east, y north (y grows downward in pixels)
    px = math.hypot(dX, dY)
    ppm = px / mi
    img_b = (math.degrees(math.atan2(dX, dY)) + 360) % 360
    geo_b = bearing((a[1], a[2]), (b[1], b[2]))
    diff = (img_b - geo_b + 180) % 360 - 180
    rows.append({'pair': f'{a[0]} -- {b[0]}', 'geo_miles': round(mi, 3), 'image_px': round(px, 2),
                 'px_per_mile': round(ppm, 3), 'miles_per_unit': round(PX_UNIT / ppm, 4),
                 'geo_bearing_deg': round(geo_b, 2), 'image_bearing_deg': round(img_b, 2),
                 'bearing_diff_deg': round(diff, 2)})
with open(ROOT / 'results' / 'audit_06_pairwise.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

ppms = [r['px_per_mile'] for r in rows]
mpus = [r['miles_per_unit'] for r in rows]
diffs = [r['bearing_diff_deg'] for r in rows]
dist = [r['geo_miles'] for r in rows]
def corr(x, y):
    mx, my = st.mean(x), st.mean(y)
    num = sum((a - mx) * (b - my) for a, b in zip(x, y))
    den = math.sqrt(sum((a - mx) ** 2 for a in x) * sum((b - my) ** 2 for b in y))
    return num / den
q = st.quantiles(mpus, n=4)
summary = [
    ('pairs', len(rows)),
    ('px_per_mile_median', round(st.median(ppms), 3)),
    ('px_per_mile_min', min(ppms)), ('px_per_mile_max', max(ppms)),
    ('miles_per_unit_median', round(st.median(mpus), 4)),
    ('miles_per_unit_IQR', f"{q[0]:.3f} - {q[2]:.3f}"),
    ('miles_per_unit_min_max', f"{min(mpus):.3f} - {max(mpus):.3f}"),
    ('bearing_diff_median_deg', round(st.median(diffs), 2)),
    ('bearing_diff_min_max_deg', f"{min(diffs):.2f} to {max(diffs):.2f}"),
    ('corr_distance_vs_px_per_mile', round(corr(dist, ppms), 3)),
    ('pixels_per_figure_unit (from audit input)', PX_UNIT),
    ('6.4_miles_per_unit_would_need_px_per_mile', round(PX_UNIT / 6.4, 3)),
]
with open(ROOT / 'results' / 'audit_06_summary.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f); w.writerow(['quantity', 'value']); w.writerows(summary)
for k, v in summary:
    print(f"{k}: {v}")

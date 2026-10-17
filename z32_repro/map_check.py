#!/usr/bin/env python3
"""
Map-scale check using ONLY:
  (a) pixel measurements from fig2_map_p9_native.png (ring scan around the crosshair), and
  (b) coordinates with a source (listed below).  No coordinates from memory are used.

Sources
  Mount Diablo, NAD27: Foxon (2023), ePrint 2023/982, Table 2:
      37 deg 52' 54.38700" N, 121 deg 54' 47.10700" W
  State Highway 24, Lafayette, CA 94549 (point on the road):
      37.890364, -122.136156
      https://www.findlatitudeandlongitude.com/r/State+Highway+24%2C+Lafayette%2C+CA+94549%2C+USA/581248/
  6.4 miles per inch: stated by Cipher Mysteries for a Phillips 66 inset; NOT measured here.
      https://ciphermysteries.com/other-ciphers/zodiac-killer-ciphers/zodiac-killer-z32
  Angle labels in Fig.2 (read visually from the image): 0 at right (east), 1.571 at top (north),
      3.142 at left (west): polar axis = east, anticlockwise positive.

Output: map_check.csv
"""
import csv, math, os
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, 'fig2_map_p9_native.png')
OUT = os.path.join(HERE, 'map_check.csv')

a = np.array(Image.open(IMG).convert('L')).astype(int)
dark = a < 90

# crosshair centre: columns/rows with the longest dark runs in the central band
col_counts = dark[150:750, :].sum(axis=0)
row_counts = dark[:, 150:750].sum(axis=1)
cx = int(np.argmax(col_counts[300:700])) + 300
cy = int(np.argmax(row_counts[300:600])) + 300

def ring_score(r):
    hits = tot = 0
    for deg in np.arange(0, 360, 0.5):
        # skip angles on the crosshair lines (multiples of 45 deg), which are dark anyway
        if min(abs(((deg - k + 180) % 360) - 180) for k in range(0, 360, 45)) < 6:
            continue
        t = math.radians(deg)
        x = int(round(cx + r * math.cos(t))); y = int(round(cy - r * math.sin(t)))
        tot += 1
        hits += bool(dark[max(0, y - 1):y + 2, max(0, x - 1):x + 2].any())
    return hits / max(tot, 1)

# search windows around the three circles labelled 4, 8, 12 (figure units)
WINDOWS = {4: (95, 110), 8: (195, 215), 12: (300, 315)}
ring_px = {n: max(range(lo, hi + 1), key=ring_score) for n, (lo, hi) in WINDOWS.items()}
ring_scores = {n: round(ring_score(r), 3) for n, r in ring_px.items()}
px_per_unit = sum(r * n for n, r in ring_px.items()) / sum(n * n for n in ring_px)

def haversine_bearing(p, q):
    R = 3958.8
    la1, lo1 = map(math.radians, p); la2, lo2 = map(math.radians, q)
    dl = lo2 - lo1
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin(dl / 2) ** 2
    d = 2 * R * math.asin(math.sqrt(h))
    y = math.sin(dl) * math.cos(la2)
    x = math.cos(la1) * math.sin(la2) - math.sin(la1) * math.cos(la2) * math.cos(dl)
    return d, (math.degrees(math.atan2(y, x)) + 360) % 360

def destination(p, bearing_deg, dist_mi):
    R = 3958.8
    la1, lo1 = map(math.radians, p); br = math.radians(bearing_deg); dd = dist_mi / R
    la2 = math.asin(math.sin(la1) * math.cos(dd) + math.cos(la1) * math.sin(dd) * math.cos(br))
    lo2 = lo1 + math.atan2(math.sin(br) * math.sin(dd) * math.cos(la1), math.cos(dd) - math.sin(la1) * math.sin(la2))
    return math.degrees(la2), math.degrees(lo2)

DIABLO = (37 + 52 / 60 + 54.38700 / 3600, -(121 + 54 / 60 + 47.10700 / 3600))   # Foxon Table 2, NAD27
HW24 = (37.890364, -122.136156)                                                 # sourced, see header

# Foxon's (12,3): r = 12 units, theta = 3 rad anticlockwise from east (paper's main convention)
theta_deg = math.degrees(3.0)
phi = theta_deg                       # math angle from east, anticlockwise
bearing_12_3 = (90 - phi) % 360       # compass bearing from north

d_hw, b_hw = haversine_bearing(DIABLO, HW24)
rows = []
def add(q, v, unit, how, status):
    rows.append([q, v, unit, how, status])

add('crosshair centre (px)', f'({cx},{cy})', 'px', 'projection of dark line columns/rows', 'measured')
for n in (4, 8, 12):
    add(f'ring labelled {n} radius', ring_px[n], 'px', f'ring scan, score {ring_scores[n]}', 'measured')
add('pixels per figure unit', round(px_per_unit, 2), 'px/unit', 'least squares through origin, 3 rings', 'computed from measurements')
add('Mount Diablo lat, lon (NAD27)', f'{DIABLO[0]:.6f}, {DIABLO[1]:.6f}', 'deg', 'Foxon 2023 Table 2', 'sourced')
add('State Highway 24 point lat, lon', f'{HW24[0]}, {HW24[1]}', 'deg', 'findlatitudeandlongitude.com', 'sourced')
add('distance Diablo -> Highway 24 point', round(d_hw, 2), 'miles', 'haversine, R = 3958.8 mi', 'computed')
add('bearing Diablo -> Highway 24 point', round(b_hw, 2), 'deg from N', 'haversine initial bearing', 'computed')
add("bearing of Foxon's (12,3), E-anticlockwise", round(bearing_12_3, 2), 'deg from N', 'theta = 3 rad, polar axis east, anticlockwise', 'convention (paper/figure labels)')
add('bearing offset (Highway point minus (12,3))', round(((b_hw - bearing_12_3 + 180) % 360) - 180, 2), 'deg', 'difference of the two bearings', 'computed')
add('implied miles per unit if Highway point = (12,3)', round(d_hw / 12, 3), 'miles/unit', 'distance only; assumes the point IS (12,3), bearing mismatch shown above', 'single-point estimate, not a fit')
add('claimed scale 6.4 miles per inch: (12,3) distance', round(12 * 6.4, 1), 'miles', '12 x 6.4', 'claim (Cipher Mysteries), not measured')
dest_lat, dest_lon = destination(DIABLO, bearing_12_3, 12 * 6.4)
add('claimed scale: (12,3) endpoint', f'{dest_lat:.3f}, {dest_lon:.3f}', 'deg', 'destination formula at 6.4 mi/unit', 'computed from claim')
add('Grinell: San Francisco at "5 inches"', 'not computed', '', 'no sourced coordinate for SF in this check', 'excluded')

with open(OUT, 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['quantity', 'value', 'unit', 'method_or_source', 'status'])
    w.writerows(rows)

for r in rows:
    print(f"{r[0]:<50} {str(r[1]):<26} {r[2]:<12} [{r[4]}]")
print("written", os.path.basename(OUT))

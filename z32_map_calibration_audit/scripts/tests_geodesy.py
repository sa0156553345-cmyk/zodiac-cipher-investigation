#!/usr/bin/env python3
"""Independent tests of the geodesy helpers. Run: python3 tests_geodesy.py
Each test prints PASS/FAIL. The script exits with code 1 if any test fails."""
import math, random, sys
from geodesy import (dms_to_deg, vincenty_inverse, vincenty_direct, haversine_miles, geodesic_miles,
                     bearing_deg, destination, en_miles_from_origin, METRES_PER_MILE)

results = []
def check(name, cond, detail=""):
    results.append((name, bool(cond)))
    print(("PASS" if cond else "FAIL"), name, detail)

# 1. DMS conversion, values from Foxon (2023) Table 2 (NAD27)
lat = dms_to_deg(37, 52, 54.38700, 'N'); lon = dms_to_deg(121, 54, 47.10700, 'W')
check("DMS: Mount Diablo NAD27 latitude", abs(lat - 37.881774) < 1e-6, f"{lat:.6f}")
check("DMS: Mount Diablo NAD27 longitude", abs(lon + 121.913085) < 1e-6, f"{lon:.6f}")
check("DMS: southern/western sign", dms_to_deg(10, 0, 0, 'S') == -10.0 and dms_to_deg(10, 0, 0, 'W') == -10.0)

# 2. Vincenty reference vector (Vincenty 1975 example as reproduced in common references):
#    Flinders Peak -> Buninyong, geodesic distance 54972.271 m, forward azimuth 306.8681 deg.
lat1, lon1 = dms_to_deg(-37, 57, 3.72030), dms_to_deg(144, 25, 29.52440)
lat2, lon2 = dms_to_deg(-37, 39, 10.15610), dms_to_deg(143, 55, 35.38390)
s, a1, a2 = vincenty_inverse(lat1, lon1, lat2, lon2)
check("Vincenty reference distance (54972.271 m)", abs(s - 54972.271) < 0.01, f"{s:.3f} m")
check("Vincenty reference azimuth (306.8681 deg)", abs(a1 - 306.8681) < 0.001, f"{a1:.5f} deg")

# 3. Round trip: direct(inverse(p,q)) returns q (random points within 40 miles of Mount Diablo)
rng = random.Random(1)
max_err = 0.0
for _ in range(300):
    p = (37.88 + rng.uniform(-0.4, 0.4), -121.91 + rng.uniform(-0.5, 0.5))
    q = (37.88 + rng.uniform(-0.4, 0.4), -121.91 + rng.uniform(-0.5, 0.5))
    d, az, _ = vincenty_inverse(*p, *q)
    lat_r, lon_r, _ = vincenty_direct(p[0], p[1], az, d)
    max_err = max(max_err, abs(lat_r - q[0]) * 111000, abs(lon_r - q[1]) * 111000 * math.cos(math.radians(q[0])))
check("Round trip inverse->direct (max error < 1 mm)", max_err < 1e-3, f"max error {max_err:.6f} m")

# 4. Symmetry of distance
d12, _, _ = vincenty_inverse(*p, *q)
d21, _, _ = vincenty_inverse(*q, *p)
check("Distance symmetry", abs(d12 - d21) < 1e-6, f"{d12 - d21:.9f} m")

# 5. Ellipsoid vs sphere: the sphere formula (mean radius) differs from the ellipsoid by a few tenths of a percent.
#    Threshold set to 0.5 % after observing a 0.2 % difference at ~20 miles (first draft used 0.1 %; see CHANGE_LOG).
p0 = (37.881774, -121.913085); q0 = (37.80444, -122.27083)
dv = geodesic_miles(*p0, *q0); dh = haversine_miles(*p0, *q0)
check("Ellipsoid vs sphere difference < 0.5 % at ~20 miles", abs(dv - dh) / dv < 5e-3, f"Vincenty {dv:.4f} mi, haversine {dh:.4f} mi, relative {abs(dv-dh)/dv*100:.3f} %")

# 6. Bearing conventions: due east = 90 deg, due north = 0 deg
e = destination(37.0, -122.0, 90.0, 10.0); n = destination(37.0, -122.0, 0.0, 10.0)
check("Bearing: destination due east gives bearing 90", abs(bearing_deg(37.0, -122.0, *e) - 90.0) < 1e-6, f"{bearing_deg(37.0, -122.0, *e):.6f}")
check("Bearing: destination due north gives bearing 0", abs(bearing_deg(37.0, -122.0, *n) % 360 - 0.0) < 1e-6 or abs(bearing_deg(37.0, -122.0, *n) - 360.0) < 1e-6, f"{bearing_deg(37.0, -122.0, *n):.6f}")

# 7. Destination distance and round trip in miles
d_back = geodesic_miles(37.0, -122.0, *destination(37.0, -122.0, 123.4, 13.0))
check("Destination then distance returns 13 miles", abs(d_back - 13.0) < 1e-6, f"{d_back:.9f} mi")

# 8. East/North components: a point 10 miles due east has E=10, N~0
E, N = en_miles_from_origin(37.0, -122.0, *destination(37.0, -122.0, 90.0, 10.0))
check("East/North components for due-east point", abs(E - 10.0) < 1e-6 and abs(N) < 1e-6, f"E={E:.6f}, N={N:.6f}")

# 9. Datum: NAD27 vs USSD coordinates of Mount Diablo from Foxon Table 2 differ by less than 0.1 mile
lat_nad27 = dms_to_deg(37, 52, 54.38700, 'N'); lon_nad27 = dms_to_deg(121, 54, 47.10700, 'W')
lat_ussd = dms_to_deg(37, 52, 55.48200, 'N'); lon_ussd = dms_to_deg(121, 54, 48.35500, 'W')
dd = geodesic_miles(lat_nad27, lon_nad27, lat_ussd, lon_ussd)
check("Datum effect NAD27 vs USSD at Diablo < 0.1 mile", dd < 0.1, f"{dd:.4f} mi ({dd * METRES_PER_MILE:.1f} m)")

failed = [n for n, ok in results if not ok]
print(f"\n{len(results) - len(failed)} of {len(results)} tests passed")
sys.exit(1 if failed else 0)

"""
Independent sensitivity analysis for the Z32 (12 inches along 3 radians) candidate.
Does NOT modify the audit package. All conventions are enumerated, none is selected by outcome.
Origin: Mount Diablo, NAD27 (Foxon 2023, Table 2), as given in the package's landmarks.csv.
Distance: spherical destination, R = 3958.8 mi.  Bearing = clockwise from true north.
"""
import math, itertools

R = 3958.8
DIAB = (37 + 52/60 + 54.38700/3600, -(121 + 54/60 + 47.10700/3600))   # NAD27 summit
CAND = (37.929792, -122.150318)     # user's candidate
PKG_A = (37.92961, -122.15045)      # audit package model A output
PKG_C = (37.90253, -122.15078)      # audit package model C output

def dest(lat, lon, bearing_deg, dist_mi):
    d = dist_mi / R; th = math.radians(bearing_deg)
    la1, lo1 = math.radians(lat), math.radians(lon)
    la2 = math.asin(math.sin(la1)*math.cos(d) + math.cos(la1)*math.sin(d)*math.cos(th))
    lo2 = lo1 + math.atan2(math.sin(th)*math.sin(d)*math.cos(la1), math.cos(d)-math.sin(la1)*math.sin(la2))
    return math.degrees(la2), (math.degrees(lo2)+540) % 360 - 180

def hav(p, q):
    la1, lo1 = map(math.radians, p); la2, lo2 = map(math.radians, q)
    h = math.sin((la2-la1)/2)**2 + math.cos(la1)*math.cos(la2)*math.sin((lo2-lo1)/2)**2
    return 2*R*math.asin(math.sqrt(h))

def bearing(p, q):
    la1, lo1 = map(math.radians, p); la2, lo2 = map(math.radians, q); dl = lo2-lo1
    y = math.sin(dl)*math.cos(la2); x = math.cos(la1)*math.sin(la2)-math.sin(la1)*math.cos(la2)*math.cos(dl)
    return (math.degrees(math.atan2(y, x))+360) % 360

print("== Reference geometry ==")
print("Diablo NAD27 summit :", [round(v,6) for v in DIAB])
print("Candidate           : dist %.2f mi, bearing %.2f deg" % (hav(DIAB,CAND), bearing(DIAB,CAND)))
print("Pkg model A         : dist %.2f mi, bearing %.2f deg" % (hav(DIAB,PKG_A), bearing(DIAB,PKG_A)))
print("Pkg model C         : dist %.2f mi, bearing %.2f deg" % (hav(DIAB,PKG_C), bearing(DIAB,PKG_C)))
print("Candidate - Pkg A   : %.1f m apart" % (hav(CAND,PKG_A)*1609.34))
print("Candidate - Pkg C   : %.2f mi apart" % hav(CAND,PKG_C))

# ---- angle-reading conventions for the number theta (radians) ----
# theta in degrees; 3 rad = 171.887 deg, 2 rad = 114.592 deg (floor), 12 rad mod 2pi = 327.56 deg
THETA = {"3rad(round)": 3*180/math.pi, "2rad(floor)": 2*180/math.pi, "12rad_mod2pi(r=3)": (12 % (2*math.pi))*180/math.pi}
DECL = 16.9   # Foxon's IGRF value, June 26 1970, Mount Diablo

def bearings_for(theta_deg):
    out = {}
    out["east_CCW (package)"]        = (90 - theta_deg) % 360
    out["east_CW"]                   = (90 + theta_deg) % 360
    out["north_CW (true)"]           = theta_deg % 360
    out["north_CCW (true)"]          = (-theta_deg) % 360
    out["magnetic_north_CW"]         = (theta_deg + DECL) % 360
    out["magnetic_north_CCW"]        = (-theta_deg + DECL) % 360
    return out

# ---- radial scales (miles per inch) ----
SCALES = {"fit_1.09 (audit C)": 1.088, "fit_1.16 (audit A)": 1.162,
          "Grinell_SF5in_implied": None, "claimed_6.4": 6.4}
# Grinell's 'SF ~5 inches from Diablo' implies scale = dist(Diablo,SF)/5. SF = downtown SF (37.7749,-122.4194)
SF = (37.7749, -122.4194)
SCALES["Grinell_SF5in_implied"] = hav(DIAB, SF)/5.0
print("\nDiablo->SF straight distance: %.2f mi  -> Grinell-implied scale %.3f mi/in" % (hav(DIAB,SF), SCALES["Grinell_SF5in_implied"]))

rows = []
for tname, th in THETA.items():
    bset = bearings_for(th)
    for bname, b in bset.items():
        for sname, s in SCALES.items():
            r_in = 3 if tname.startswith("12rad") else 12   # (12,3)->r=12 ; (3,12) reading -> r=3
            dist = r_in * s
            lat, lon = dest(DIAB[0], DIAB[1], b, dist)
            rows.append((tname, bname, sname, r_in, round(dist,2), round(lat,6), round(lon,6), round(hav((lat,lon), CAND),2)))

rows.sort(key=lambda x: x[-1])
print("\n== All conventions: endpoint and distance from CANDIDATE (miles) ==")
print("%-18s %-22s %-24s %-4s %-8s %-12s %-13s %-10s" % ("theta","ref_direction","scale","r","dist_mi","lat","lon","to_cand_mi"))
for r in rows:
    print("%-18s %-22s %-24s %-4s %-8s %-12s %-13s %-10s" % r)
near = [r for r in rows if r[-1] < 0.5]
print("\nConventions whose endpoint lies within 0.5 mi of the candidate:", len(near), "of", len(rows))
for r in near: print("  ", r[:3], "-> %.2f mi" % r[-1])

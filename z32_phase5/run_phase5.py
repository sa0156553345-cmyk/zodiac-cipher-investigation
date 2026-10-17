import math, csv, json
R = 3958.8
DIAB = (37 + 52/60 + 54.38700/3600, -(121 + 54/60 + 47.10700/3600))   # Foxon T2 NAD27
CAND = (37.929792, -122.150318)
AUDIT_S = 1.162          # sensitivity only
CLAIM_S = 6.4            # secondary claim (Grinell), sensitivity only

def hav(p,q):
    la1,lo1=map(math.radians,p); la2,lo2=map(math.radians,q)
    h=math.sin((la2-la1)/2)**2+math.cos(la1)*math.cos(la2)*math.sin((lo2-lo1)/2)**2
    return 2*R*math.asin(math.sqrt(h))
def dest(p, bearing, dist):
    d=dist/R; th=math.radians(bearing); la1,lo1=map(math.radians,p)
    la2=math.asin(math.sin(la1)*math.cos(d)+math.cos(la1)*math.sin(d)*math.cos(th))
    lo2=lo1+math.atan2(math.sin(th)*math.sin(d)*math.cos(la1), math.cos(d)-math.sin(la1)*math.sin(la2))
    return math.degrees(la2), (math.degrees(lo2)+540)%360-180

# ---- Foxon's 8 conventions (N,E,S,W reference x CW/CCW), true bearing clockwise from north ----
def conv_bearing(ref, direction, theta_deg):
    base = {'N':0,'E':90,'S':180,'W':270}[ref]
    return (base + theta_deg)%360 if direction=='CW' else (base - theta_deg)%360
THETA3 = 3*180/math.pi   # minute 3 (Foxon round rule)
THETA2 = 2*180/math.pi   # minute 2 (floor, sensitivity)

# ---- SF extent: approximate boundary points (general knowledge, NOT from the archive) + Foxon's sourced SF point ----
SF_APPROX = {'SF_west_Ocean_Beach':(37.7600,-122.5107), 'SF_north_Presidio':(37.8118,-122.4770),
             'SF_northeast_Embarcadero':(37.8030,-122.3930), 'SF_east_bayshore':(37.7290,-122.3600),
             'SF_south_Daly_line':(37.7086,-122.4600)}
FOXON_SF = (37 + 43/60 + 42.17100/3600, -(122 + 21/60 + 39.78600/3600))  # Foxon T2 'Hunter West 1, SF' NAD27
dists = {k: hav(DIAB,v) for k,v in SF_APPROX.items()}
dists['Foxon_SF_point(T2)'] = hav(DIAB, FOXON_SF)
D_min = min(dists[k] for k in SF_APPROX); D_max = max(dists[k] for k in SF_APPROX)
S_lo, S_hi = D_min/5.5, D_max/4.5           # accepted band from 'approximately five inches' rule [4.5,5.5]
print("== SF distances from Diablo (mi) ==")
for k,v in dists.items(): print(f"  {k:28s} {v:6.2f} mi  -> inches at 6.4 = {v/6.4:.2f}, at band-mid = {v/((S_lo+S_hi)/2):.2f}")
print(f"D_min={D_min:.2f} mi, D_max={D_max:.2f} mi")
print(f"Accepted scale band from 'SF ~5 in' rule: [{S_lo:.3f}, {S_hi:.3f}] mi/in")
print(f"Audit fit 1.162 inside band? {S_lo <= AUDIT_S <= S_hi}   | claim 6.4 inside band? {S_lo <= CLAIM_S <= S_hi}")

# ---- scale sample set (pre-registered): band low/mid/high + audit (sensitivity) + claim (sensitivity) ----
scales = {'band_low':S_lo, 'band_mid':(S_lo+S_hi)/2, 'band_high':S_hi, 'audit_1.162(sens)':AUDIT_S, 'claim_6.4(sens)':CLAIM_S}
rows=[]
for minute_name, theta in [('min3_round(primary)',THETA3), ('min2_floor(sens)',THETA2)]:
    for ref in 'NESW':
        for dr in ['CW','CCW']:
            b = conv_bearing(ref, dr, theta)
            for sname, s in scales.items():
                r_in = 12
                lat, lon = dest(DIAB, b, r_in*s)
                rows.append(dict(minute=minute_name, ref=ref, dir=dr, bearing=round(b,2), scale_name=sname,
                                 scale_mi_per_in=round(s,3), dist_from_diablo_mi=round(r_in*s,2),
                                 lat=round(lat,6), lon=round(lon,6), dist_to_candidate_mi=round(hav((lat,lon),CAND),2),
                                 dist_to_SF_Foxon_point_mi=round(hav((lat,lon),FOXON_SF),2)))
with open('phase5_endpoints.csv','w',newline='') as f:
    w=csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print(f"\nwrote phase5_endpoints.csv with {len(rows)} rows (8 conventions x 2 minutes x 5 scales)")

# ---- decision rules (from PREREG) ----
prim = [r for r in rows if r['minute'].startswith('min3')]
in_band = [r for r in prim if r['scale_name'] in ('band_low','band_mid','band_high')]
min_in_band = min(r['dist_to_candidate_mi'] for r in in_band)
print(f"\nMinimum distance to candidate over primary conventions within accepted band: {min_in_band:.2f} mi")
print("Primary conventions within 0.5 mi of candidate (any scale):",
      [ (r['ref'],r['dir'],r['scale_name'],r['dist_to_candidate_mi']) for r in prim if r['dist_to_candidate_mi']<0.5])
aud = [r for r in rows if r['scale_name'].startswith('audit') and r['minute'].startswith('min3')]
print("Audit-scale primary endpoints:", [(r['ref'],r['dir'],r['dist_to_candidate_mi']) for r in aud])
json.dump(dict(S_lo=S_lo,S_hi=S_hi,D_min=D_min,D_max=D_max,band_ok_audit=(S_lo<=AUDIT_S<=S_hi),
               band_ok_claim=(S_lo<=CLAIM_S<=S_hi),min_dist_in_band=min_in_band),
          open('phase5_summary.json','w'), indent=1)

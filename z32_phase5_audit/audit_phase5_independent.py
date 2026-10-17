#!/usr/bin/env python3
"""
Independent recomputation for Phase 5. Does NOT import any Phase-5 code.
Phase-5 CSV/JSON are read only for comparison at the end.
Methods: (S) sphere, vector-rotation destination; (S2) textbook sphere formula (written here);
         (V) Vincenty direct on an ellipsoid (validated on a published example first).
"""
import math, csv, json
import numpy as np
from PIL import Image

DEG = math.pi/180.0
R_SPH = 3958.8                 # mi, sphere used by Phase 5 (comparison only)
M_PER_MI = 1609.344
PHI0 = 37 + 52/60 + 54.38700/3600          # Foxon 2023 T2, NAD27 summit
LAM0 = -(121 + 54/60 + 47.10700/3600)
PHI_U = 37 + 52/60 + 55.48200/3600         # Foxon T2, USSD (datum proxy only)
LAM_U = -(121 + 54/60 + 48.35500/3600)
ORIGIN = (PHI0, LAM0)
CAND = (37.929792, -122.150318)
ELL = {"Clarke1866_NAD27": (6378206.4, 294.9786982), "WGS84": (6378137.0, 298.257223563)}
DECL = 16.9
import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
PKG = _os.path.join(_HERE, '..', 'z32_independent_audit')
P5 = _os.path.join(_HERE, '..', 'z32_phase5')
OUT = _HERE

def wrap360(x): return x % 360.0
def wrap180(x): return ((x + 180.0) % 360.0) - 180.0

# ---------- sphere geometry (two independent formulas) ----------
def hav(p, q, R=R_SPH):
    la1, lo1, la2, lo2 = p[0]*DEG, p[1]*DEG, q[0]*DEG, q[1]*DEG
    h = math.sin((la2-la1)/2)**2 + math.cos(la1)*math.cos(la2)*math.sin((lo2-lo1)/2)**2
    return 2*R*math.asin(min(1.0, math.sqrt(h)))

def init_bearing(p, q):
    la1, lo1, la2, lo2 = p[0]*DEG, p[1]*DEG, q[0]*DEG, q[1]*DEG
    y = math.sin(lo2-lo1)*math.cos(la2)
    x = math.cos(la1)*math.sin(la2) - math.sin(la1)*math.cos(la2)*math.cos(lo2-lo1)
    return wrap360(math.atan2(y, x)/DEG)

def _vec(p):
    la, lo = p[0]*DEG, p[1]*DEG
    return np.array([math.cos(la)*math.cos(lo), math.cos(la)*math.sin(lo), math.sin(la)])

def _unvec(v):
    v = v/np.linalg.norm(v)
    return (math.asin(max(-1.0, min(1.0, v[2])))/DEG, math.atan2(v[1], v[0])/DEG)

def dest_vector(p, b_deg, d_mi, R=R_SPH):              # method S: rotation of a unit vector
    la, lo = p[0]*DEG, p[1]*DEG
    north = np.array([-math.sin(la)*math.cos(lo), -math.sin(la)*math.sin(lo), math.cos(la)])
    east = np.array([-math.sin(lo), math.cos(lo), 0.0])
    b = b_deg*DEG
    t = math.cos(b)*north + math.sin(b)*east
    d = d_mi/R
    return _unvec(math.cos(d)*_vec(p) + math.sin(d)*t)

def dest_textbook(p, b_deg, d_mi, R=R_SPH):            # method S2: textbook formula, written here
    d = d_mi/R; th = b_deg*DEG; la1, lo1 = p[0]*DEG, p[1]*DEG
    la2 = math.asin(math.sin(la1)*math.cos(d) + math.cos(la1)*math.sin(d)*math.cos(th))
    lo2 = lo1 + math.atan2(math.sin(th)*math.sin(d)*math.cos(la1), math.cos(d) - math.sin(la1)*math.sin(la2))
    return (la2/DEG, wrap180(lo2/DEG))

# ---------- Vincenty direct (ellipsoid), written from the published formulas ----------
def vincenty_direct(p, b_deg, d_mi, a, invf):
    f = 1.0/invf; b = (1-f)*a
    phi1 = p[0]*DEG; L1 = p[1]*DEG; al1 = b_deg*DEG; s = d_mi*M_PER_MI
    U1 = math.atan((1-f)*math.tan(phi1))
    sig1 = math.atan2(math.tan(U1), math.cos(al1))
    sina = math.cos(U1)*math.sin(al1)
    cos2a = 1 - sina*sina
    u2 = cos2a*(a*a - b*b)/(b*b)
    A = 1 + u2/16384*(4096 + u2*(-768 + u2*(320 - 175*u2)))
    B = u2/1024*(256 + u2*(-128 + u2*(74 - 47*u2)))
    sig = s/(b*A)
    for _ in range(500):
        c2m = math.cos(2*sig1 + sig); ss = math.sin(sig); cs = math.cos(sig)
        dsig = B*ss*(c2m + B/4*(cs*(-1 + 2*c2m*c2m) - B/6*c2m*(-3 + 4*ss*ss)*(-3 + 4*c2m*c2m)))
        new = s/(b*A) + dsig
        if abs(new - sig) < 1e-13: sig = new; break
        sig = new
    c2m = math.cos(2*sig1 + sig); ss = math.sin(sig); cs = math.cos(sig)
    sU, cU = math.sin(U1), math.cos(U1)
    phi2 = math.atan2(sU*cs + cU*ss*math.cos(al1),
                      (1-f)*math.sqrt(sina*sina + (sU*ss - cU*cs*math.cos(al1))**2))
    lam = math.atan2(ss*math.sin(al1), cU*cs - sU*ss*math.cos(al1))
    C = f/16*cos2a*(4 + f*(4 - 3*cos2a))
    L = lam - (1-C)*f*sina*(sig + C*ss*(c2m + C*cs*(-1 + 2*c2m*c2m)))
    return (phi2/DEG, wrap180((L1 + L)/DEG))

# ---------- validation of Vincenty on a published example (Flinders Peak -> Buninyong, WGS84) ----------
def dms(d, m, s, sign=1): return sign*(d + m/60 + s/3600)
fl_p = (dms(37,57,3.72030,-1), dms(144,25,29.52440))
fl_az = dms(306,52,5.37)
fl_s_m = 54972.271
bun_expect = (dms(37,39,10.15661,-1), dms(143,55,35.38339))
a_w, invf_w = ELL["WGS84"]
val = vincenty_direct(fl_p, fl_az, fl_s_m/M_PER_MI, a_w, invf_w)
val_err_deg = max(abs(val[0]-bun_expect[0]), abs(val[1]-bun_expect[1]))
print(f"[VALIDATION] Vincenty vs published Buninyong: max error = {val_err_deg:.2e} deg  -> {'PASS' if val_err_deg < 1e-6 else 'FAIL'}")

# ---------- conventions and rules (written from Foxon 2023 and the pre-registration) ----------
HOUR = int(math.floor(DECL/30.0))                  # 0 -> displayed as 12
R_UNITS = 12 if HOUR == 0 else HOUR                # r in 'inches' (hour value), per Foxon assumption 4
MIN_ROUND = int(math.floor(DECL/6.0 + 0.5))        # 2.8167 -> 3
MIN_FLOOR = int(math.floor(DECL/6.0))              # 2
def theta_deg(minute_rad): return minute_rad*(180.0/math.pi)
def bearing(ref, cw, th_deg):
    base = {'N':0.0,'E':90.0,'S':180.0,'W':270.0}[ref]
    return wrap360(base + th_deg) if cw else wrap360(base - th_deg)
RADIALS = [(r, cw) for r in 'NESW' for cw in (True, False)]
def rname(r, cw): return f"{r}-{'CW' if cw else 'CCW'}"

# ---------- scales ----------
def sf_points():
    return {'SF_west_Ocean_Beach':(37.7600,-122.5107), 'SF_north_Presidio':(37.8118,-122.4770),
            'SF_northeast_Embarcadero':(37.8030,-122.3930), 'SF_east_bayshore':(37.7290,-122.3600),
            'SF_south_Daly_line':(37.7086,-122.4600), 'Foxon_T2_SF_Hunter_West1':(37 + 43/60 + 42.17100/3600, -(122 + 21/60 + 39.78600/3600))}
SF = sf_points()
D_sf = {k: hav(ORIGIN, v) for k, v in SF.items()}
D_min = min(D_sf[k] for k in SF if not k.startswith('Foxon')); D_max = max(D_sf[k] for k in SF if not k.startswith('Foxon'))
S_LO, S_HI = D_min/5.5, D_max/4.5
with open(f'{PKG}/results/map_audit_models.csv', encoding='utf-8') as f:
    row = [r for r in csv.reader(f) if r and r[0].startswith('A_')][0]
AUDIT_S = float(row[7])                              # miles per figure unit (fit), from package file
CLAIM_S = 6.4

print(f"[SF] D_min={D_min:.3f} D_max={D_max:.3f} mi ; band=[{S_LO:.4f},{S_HI:.4f}] mi/in ; audit={AUDIT_S} in band? {S_LO<=AUDIT_S<=S_HI}")
print(f"[SF] Foxon T2 SF point distance = {D_sf['Foxon_T2_SF_Hunter_West1']:.3f} mi")

# ---------- candidate geometry (parameter-free) ----------
d_c = hav(ORIGIN, CAND); b_c = init_bearing(ORIGIN, CAND)
def cross_track(b_r):
    """Minimum distance from CAND to the half-line from ORIGIN at bearing b_r (sphere)."""
    dA = wrap180(b_c - b_r)
    if abs(dA) > 90: return d_c, 'origin'
    dc_ang = d_c/R_SPH
    xt = math.asin(max(-1, min(1, math.sin(dc_ang)*math.sin(dA*DEG))))*R_SPH
    return abs(xt), 'radial'
print(f"[CAND] distance from origin = {d_c:.4f} mi ; bearing = {b_c:.4f} deg")
cand_geom = {}
for r, cw in RADIALS:
    b_r = bearing(r, cw, theta_deg(3))
    xt, kind = cross_track(b_r)
    cand_geom[rname(r,cw)] = dict(bearing=round(b_r,4), offset_deg=round(wrap180(b_c-b_r),4), min_dist_mi=round(xt,4), nearest=kind)
    print(f"  {rname(r,cw):7s} bearing={b_r:8.3f}  offset={wrap180(b_c-b_r):+8.3f} deg  min dist to candidate = {xt:7.3f} mi ({kind})")
best_any_scale = min(v['min_dist_mi'] for v in cand_geom.values())
print(f"[CAND] minimum achievable distance to ANY registered radial, at ANY scale = {best_any_scale:.3f} mi")
s_needed_E_CCW = d_c*math.cos(math.radians(wrap180(b_c - bearing('E', False, theta_deg(3)))))/R_UNITS
print(f"[CAND] scale that puts E-CCW nearest point at the candidate's projection: s = {s_needed_E_CCW:.4f} mi/in")

# ---------- recompute the 8-radial table at 5 scales, two minute rules ----------
def scale_set():
    ds = {'band_low': S_LO, 'band_mid': (S_LO+S_HI)/2, 'band_high': S_HI,
          'audit_fit(sens)': AUDIT_S, 'claim_6.4(sens)': CLAIM_S}
    return ds
rows = []
for mname, minute in [('min3_round(primary)', MIN_ROUND), ('min2_floor(sens)', MIN_FLOOR)]:
    th = theta_deg(minute)
    for r, cw in RADIALS:
        b = bearing(r, cw, th)
        for sname, s in scale_set().items():
            dist = R_UNITS*s
            pS = dest_vector(ORIGIN, b, dist); pS2 = dest_textbook(ORIGIN, b, dist)
            pV = vincenty_direct(ORIGIN, b, dist, *ELL['Clarke1866_NAD27'])
            pW = vincenty_direct(ORIGIN, b, dist, *ELL['WGS84'])
            rows.append(dict(minute=mname, radial=rname(r,cw), bearing=round(b,4), scale_name=sname, scale=s,
                             dist_mi=round(dist,4), sphere_lat=pS[0], sphere_lon=pS[1],
                             textbook_lat=pS2[0], textbook_lon=pS2[1],
                             clarke_lat=pV[0], clarke_lon=pV[1], wgs84_lat=pW[0], wgs84_lon=pW[1],
                             to_cand_sphere_mi=round(hav(pS, CAND),4), to_cand_clarke_mi=round(hav(pV, CAND),4)))
with open(f'{OUT}/independent_endpoints.csv','w',newline='',encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print(f"\n[TABLE] wrote {len(rows)} independent rows")

# method agreement: sphere vector vs textbook
max_s_diff_deg = max(max(abs(r['sphere_lat']-r['textbook_lat']), abs(r['sphere_lon']-r['textbook_lon'])) for r in rows)
print(f"[METHOD] sphere vector vs textbook formula: max diff = {max_s_diff_deg:.2e} deg")

# ---------- compare with Phase-5 CSV ----------
p5 = list(csv.DictReader(open(f'{P5}/phase5_endpoints.csv', encoding='utf-8')))
p5_s = json.load(open(f'{P5}/phase5_summary.json'))
print(f"[P5 JSON] S_lo={p5_s['S_lo']:.6f} S_hi={p5_s['S_hi']:.6f} D_min={p5_s['D_min']:.4f} D_max={p5_s['D_max']:.4f}")
print(f"[P5 vs INDEP] band diff: S_lo {abs(p5_s['S_lo']-S_LO):.2e}, S_hi {abs(p5_s['S_hi']-S_HI):.2e}; D_min diff {abs(p5_s['D_min']-D_min):.2e}; D_max diff {abs(p5_s['D_max']-D_max):.2e}")
cmp_rows = []
for c in p5:
    mname = 'min3_round(primary)' if c['minute'].startswith('min3') else 'min2_floor(sens)'
    sname_map = {'audit_1.162(sens)': 'audit_fit(sens)'}
    key = (mname, c['ref']+'-'+c['dir'], sname_map.get(c['scale_name'], c['scale_name']))
    mine = [r for r in rows if (r['minute'], r['radial'], r['scale_name']) == key][0]
    d_bearing = abs(float(c['bearing']) - mine['bearing'])
    # (a) same printed inputs: CSV scale and CSV distance
    pA = dest_vector(ORIGIN, float(c['bearing']), float(c['dist_from_diablo_mi']))
    dA = max(abs(pA[0]-float(c['lat'])), abs(pA[1]-float(c['lon']))) * 111000.0
    # (b) exact scales (independent)
    dB = max(abs(mine['sphere_lat']-float(c['lat'])), abs(mine['sphere_lon']-float(c['lon']))) * 111000.0
    cmp_rows.append(dict(key=key, bearing_diff=d_bearing, metres_printed_inputs=dA, metres_exact_scale=dB,
                         cand_csv=float(c['dist_to_candidate_mi']), cand_indep=mine['to_cand_sphere_mi']))
print(f"[P5 vs INDEP] bearing: max |diff| = {max(r['bearing_diff'] for r in cmp_rows):.4f} deg (CSV rounding to 0.01)")
print(f"[P5 vs INDEP] endpoints, same printed inputs: max = {max(r['metres_printed_inputs'] for r in cmp_rows):.3f} m")
print(f"[P5 vs INDEP] endpoints, exact scales: max = {max(r['metres_exact_scale'] for r in cmp_rows):.1f} m (from rounding of CSV scale to 3 decimals)")
print(f"[P5 vs INDEP] dist-to-candidate: max |diff| = {max(abs(r['cand_csv']-r['cand_indep']) for r in cmp_rows):.4f} mi")

# ---------- datum / ellipsoid sensitivity ----------
mid = scale_set()['band_mid']
ell_diffs = {}
for name, s in [('band_mid', mid), ('claim_6.4', CLAIM_S), ('audit_fit', AUDIT_S)]:
    worst = 0.0
    for r, cw in RADIALS:
        b = bearing(r, cw, theta_deg(3)); dist = R_UNITS*s
        pS = dest_vector(ORIGIN, b, dist); pV = vincenty_direct(ORIGIN, b, dist, *ELL['Clarke1866_NAD27']); pW = vincenty_direct(ORIGIN, b, dist, *ELL['WGS84'])
        worst = max(worst, hav(pS,pV)*M_PER_MI, hav(pV,pW)*M_PER_MI, hav(pS,pW)*M_PER_MI)
    ell_diffs[name] = worst
    print(f"[ELLIPSOID] scale={name}: max endpoint difference among sphere/Clarke1866/WGS84 = {worst:.1f} m")
shift_m = hav(ORIGIN, (PHI_U, LAM_U))*M_PER_MI
print(f"[DATUM PROXY] origin shift between Foxon NAD27 and USSD values = {shift_m:.1f} m (proxy only; NAD83 value not available here)")
ORIGIN_U = (PHI_U, LAM_U)
b_c_U = init_bearing(ORIGIN_U, CAND); d_c_U = hav(ORIGIN_U, CAND)
e_ccw_U = bearing('E', False, theta_deg(3))
xt_U = abs(math.asin(math.sin(d_c_U/R_SPH)*math.sin(math.radians(wrap180(b_c_U - e_ccw_U))))*R_SPH)
print(f"[DATUM PROXY] candidate vs E-CCW radial from USSD origin: min dist = {xt_U:.3f} mi (NAD27 origin: {cand_geom['E-CCW']['min_dist_mi']:.3f} mi)")
offset_needed_km = cand_geom['E-CCW']['min_dist_mi']*M_PER_MI/1000.0
print(f"[DATUM] origin displacement needed to put E-CCW through the candidate ~ {offset_needed_km:.2f} km (vs datum proxy {shift_m/1000:.3f} km)")

# ---------- unregistered declination-rotated radials (sensitivity only, NOT part of verdict) ----------
unreg = []
for r, cw in RADIALS:
    b0 = bearing(r, cw, theta_deg(3))
    for sign in (+1, -1):
        b = wrap360(b0 + sign*DECL)
        for sname, s in [('audit_fit', AUDIT_S), ('band_mid', mid), ('claim_6.4', CLAIM_S)]:
            p = dest_vector(ORIGIN, b, R_UNITS*s)
            unreg.append((rname(r,cw)+f"{'+' if sign>0 else '-'}16.9", sname, round(hav(p,CAND),3)))
unreg.sort(key=lambda x: x[2])
print(f"[UNREGISTERED] declination-rotated radials, closest 3: {unreg[:3]}")

# ---------- rule evaluation (pre-registration), dense band sampling ----------
dense = np.linspace(S_LO, S_HI, 400)
min_all = min(hav(dest_vector(ORIGIN, bearing(r,cw,theta_deg(MIN_ROUND)), R_UNITS*s), CAND) for r,cw in RADIALS for s in dense)
supported_possible = any(v['min_dist_mi'] <= 0.5 for v in cand_geom.values())
print(f"[RULES] min over 8 radials x dense band of distance to candidate = {min_all:.3f} mi")
print(f"[RULES] supported condition achievable at any scale under registered radials? {supported_possible}")
print(f"[RULES] contradicted condition: all 8 radials > 2 mi over band AND band excludes {AUDIT_S}? "
      f"{min_all > 2 and not (S_LO <= AUDIT_S <= S_HI)}")

# ---------- figure marker test (independent image analysis) ----------
img = np.asarray(Image.open(f'{PKG}/images/fig2_map_p9_native.png').convert('L')).astype(float)
dark = 255.0 - img; H, W = dark.shape
cols = dark[250:650, :].sum(axis=0); CX = int(np.argmax(cols[400:600]) + 400)
rws = dark[:, 300:700].sum(axis=1); CY = int(np.argmax(rws[400:500]) + 400)
hh = 8
def mscore(x, y):
    x0, x1, y0, y1 = int(x-hh-1), int(x+hh+2), int(y-hh-1), int(y+hh+2)
    if x0 < 0 or y0 < 0 or x1 > W or y1 > H: return -1e9
    patch = dark[y0:y1, x0:x1]
    yy, xx = np.mgrid[y0:y1, x0:x1]
    cheb = np.maximum(np.abs(xx-x), np.abs(yy-y))
    return patch[(cheb >= hh-1) & (cheb <= hh)].mean() - patch[cheb <= hh-4].mean()
angles = np.arange(0, 360, 0.5); best = []
for b in angles:
    bb = b*DEG; bs, bR = -1e9, None
    for Rp in np.arange(300, 314.5, 0.5):
        sc = mscore(CX + Rp*math.sin(bb), CY - Rp*math.cos(bb))
        if sc > bs: bs, bR = sc, Rp
    best.append((float(b), float(bR), float(bs)))
scores = np.array([x[2] for x in best]); med = float(np.median(scores))
peaks = []
for i, (b, Rp, sc) in enumerate(best):
    win = [best[(i+k) % len(best)][2] for k in range(-6, 7)]
    if sc == max(win) and sc > med + 0.5*(scores.max()-med):
        peaks.append((b, Rp, sc))
peaks.sort(key=lambda x: -x[2]); peaks = peaks[:12]
pred = {rname(r,cw): bearing(r,cw,theta_deg(3)) for r,cw in RADIALS}
print(f"\n[FIGURE] centre estimated at px ({CX},{CY}); figure size {W}x{H}; median score {med:.1f}")
print("[FIGURE] detected marker peaks (bearing deg, radius px, score):")
for p_ in peaks: print(f"   {p_[0]:6.1f}  r={p_[1]:6.1f}  score={p_[2]:6.1f}")
fig_match = {}
for name, bp in pred.items():
    near = min(peaks, key=lambda p_: abs(wrap180(p_[0]-bp))) if peaks else None
    dd = abs(wrap180(near[0]-bp)) if near else 999
    fig_match[name] = round(dd, 2)
    print(f"[FIGURE] predicted {name:7s} bearing {bp:7.2f}  -> nearest detected peak {near[0] if near else None}  |diff|={dd:.2f} deg")

json.dump(dict(validation_vincenty_err_deg=val_err_deg, D_min=D_min, D_max=D_max, S_lo=S_LO, S_hi=S_HI,
               audit_scale=AUDIT_S, cand_dist_mi=d_c, cand_bearing=b_c, cand_geom=cand_geom,
               best_any_scale_mi=best_any_scale, min_band_dense_mi=min_all, supported_possible=supported_possible,
               ellipsoid_worst_m=ell_diffs, datum_proxy_m=shift_m, unreg_closest=unreg[:3],
               figure_centre=[CX,CY], figure_peaks=peaks, figure_pred_diff=fig_match,
               max_p5_bearing_diff=max(r['bearing_diff'] for r in cmp_rows),
               max_p5_m_printed=max(r['metres_printed_inputs'] for r in cmp_rows),
               max_p5_m_exact=max(r['metres_exact_scale'] for r in cmp_rows)),
          open(f'{OUT}/audit_summary.json','w',encoding='utf-8'), indent=1, ensure_ascii=False, default=float)
print("\n[DONE] wrote independent_endpoints.csv and audit_summary.json")

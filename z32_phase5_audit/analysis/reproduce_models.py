"""Re-implement the package's map model (same formulas as scripts/map_audit.py) to test sensitivity.
Reads the package's own landmarks.csv; no edits to the package."""
import csv, math, numpy as np, sys
import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
sys.path.insert(0, _os.path.join(_HERE, '..', '..', 'z32_independent_audit', 'scripts'))
PKG = _os.path.join(_HERE, '..', '..', 'z32_independent_audit')
PX_UNIT = 25.589
R = 3958.8

LM = []; DIAB=None
with open(f'{PKG}/data/landmarks.csv', newline='', encoding='utf-8') as f:
    for r in csv.DictReader(f):
        if r['name'].startswith('Mount Diablo'): DIAB = (float(r['lat']), float(r['lon']))
        elif r['name'].startswith('State Highway 24'): HW = (float(r['lat']), float(r['lon']))
        else: LM.append((r['name'], float(r['lat']), float(r['lon']), int(r['image_x']), int(r['image_y'])))
CX, CY = 490, 454
lat0 = math.radians(DIAB[0])
def en(lat, lon): return ((lon-DIAB[1])*math.cos(lat0)*69.17, (lat-DIAB[0])*69.0)
def inv(x, y): return DIAB[0]+y/69.0, DIAB[1]+x/(math.cos(lat0)*69.17)
def hav(p,q):
    la1,lo1=map(math.radians,p); la2,lo2=map(math.radians,q)
    h=math.sin((la2-la1)/2)**2+math.cos(la1)*math.cos(la2)*math.sin((lo2-lo1)/2)**2
    return 2*R*math.asin(math.sqrt(h))

def fit(idx, zero_offset):
    A=[];b=[]
    for i in idx:
        name,la,lo,px,py = LM[i]; x,y = en(la,lo); X=px-CX; Y=CY-py
        if zero_offset: A.append([x,-y]); b.append(X); A.append([y,x]); b.append(Y)
        else: A.append([x,-y,1,0]); b.append(X); A.append([y,x,0,1]); b.append(Y)
    sol=np.linalg.lstsq(np.array(A,float),np.array(b,float),rcond=None)[0]
    s=math.hypot(sol[0],sol[1]); th=math.degrees(math.atan2(sol[1],sol[0]))
    t=(0.0,0.0) if zero_offset else (sol[2],sol[3])
    return s,th,t

def predict(s, th, t, r_units=12, theta_rad=3.0):
    r_px = r_units*PX_UNIT
    dx,dy = r_px*math.cos(theta_rad), r_px*math.sin(theta_rad)
    X=dx-t[0]; Y=dy-t[1]
    c,sn=math.cos(math.radians(th)),math.sin(math.radians(th))
    x=(c*X+sn*Y)/s; y=(-sn*X+c*Y)/s
    return inv(x,y)

print("Diablo (pkg):", DIAB)
results={}
for name, idx, zero in [("A",[0,1,2,3,4],False),("B",[1,2,3,4],False),("C",[0,1,2,3,4],True),("D",[1,2,3,4],True)]:
    s,th,t = fit(idx, zero)
    p = predict(s,th,t)
    results[name]=(s,th,t,p)
    off_mi = math.hypot(*t)/ (s)  if not zero else 0.0
    print(f"{name}: px/mile={s:.3f}  rot={th:.3f}  offset_px=({t[0]:.1f},{t[1]:.1f}) -> offset {off_mi:.2f} mi  pred=({p[0]:.5f},{p[1]:.5f})")
CAND=(37.929792,-122.150318)
print("\nDistance from USER candidate to each re-implemented model:")
for name,(s,th,t,p) in results.items():
    print(f"  {name}: {hav(CAND,p):.2f} mi")
print("Diablo-summit origin check: crosshair pixel (490,454) corresponds to Diablo summit in model C only.")

# ---- Sensitivity of model A to rotation (MC bounds from package) and scale (MC bounds) ----
sA,thA,tA,_ = results['A']
print("\nModel A sensitivity (free offset kept, 12 units, 3 rad):")
for th in [-8.336, -4.802, -1.133]:
    p = predict(sA, th, tA); print(f"  rot={th:+.3f}: ({p[0]:.5f},{p[1]:.5f})  d_cand={hav(CAND,p):.2f} mi")
for s in [1.017, 1.10, 1.162, 1.332]:
    p = predict(s*PX_UNIT/PX_UNIT*sA/sA*sA/sA if False else sA/ (sA/ (sA)) , thA, tA) if False else None
# scale sensitivity: miles per unit scales linearly with 1/px_per_mile, so vary s (px/mile)
for pxmi in [15.59, 19.2, 22.02, 25.14, 29.73]:
    p = predict(pxmi, thA, tA); print(f"  px/mile={pxmi:6.2f} (mi/unit={PX_UNIT/pxmi:.3f}): ({p[0]:.5f},{p[1]:.5f})  d_cand={hav(CAND,p):.2f} mi")

# ---- Model A with origin forced to zero offset (pole at crosshair = paper's assumption) ----
sC,thC,tC,pC = results['C']
print("\nPole at crosshair (paper's assumption, model C) vs user candidate: %.2f mi" % hav(CAND,pC))
print("Model A pole displacement from crosshair: %.2f mi (free offset)" % (math.hypot(*tA)/sA))

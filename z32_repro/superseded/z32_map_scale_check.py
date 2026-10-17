# Map-scale check using ONLY data present in the uploaded PDF (Figure 2, page 9 raster)
# plus typed geographic coordinates (approximate, from memory; flagged).
# Manual pixel readings from the extracted image (estimates, +/- ~12 px):
#   centre of crosshair (Mt Diablo symbol): (491, 453)
#   circle labels 4, 8, 12 sit on circles of radius ~99, ~202, ~308 px
#   angle labels: 0 at east (right), 1.571 at north (top), 3.142 at west (left): polar axis east, anticlockwise
#   white marker on the 12-circle at (186, 410)
import math, csv
CX, CY = 491, 453
circ = [(4, 99), (8, 202), (12, 308)]          # (label in figure units, radius px)
# px per figure-unit, least squares through origin
k_circ = sum(r*n for n, r in circ) / sum(n*n for n, r in circ)

# Landmarks: (name, label px x, label px y, lat, lon)  -- label centres, not city centres
LM = [
 ("Concord",       384, 327, 37.9780, -122.0311),
 ("Walnut Creek",  362, 380, 37.9101, -122.0652),
 ("Danville",      350, 538, 37.8216, -121.9999),
 ("Lafayette",     265, 432, 37.8858, -122.1180),
 ("Pleasant Hill", 290, 296, 37.9480, -122.0608),
 ("Martinez",      243, 219, 38.0194, -122.1341),
 ("Oakland",       152, 608, 37.8044, -122.2712),
 ("San Leandro",   120, 727, 37.7249, -122.1561),
 ("Hayward",       185, 868, 37.6688, -122.0808),
 ("Livermore",     625, 780, 37.6819, -121.7680),
 ("Pleasanton",    570, 792, 37.6624, -121.8747),
 ("San Ramon",     378, 630, 37.7799, -121.9780),
 ("Vallejo",        95,  78, 38.1041, -122.2566),
 ("Orinda Village",150, 385, 37.8377, -122.1080),
]
DIABLO = (37.881774, -121.913085)   # NAD27, Foxon Table 2
R = 3958.8
def dist_brg(a, b):
    la1, lo1 = map(math.radians, a); la2, lo2 = map(math.radians, b)
    dl = lo2-lo1
    h = math.sin((la2-la1)/2)**2 + math.cos(la1)*math.cos(la2)*math.sin(dl/2)**2
    d = 2*R*math.asin(math.sqrt(h))
    y = math.sin(dl)*math.cos(la2); x = math.cos(la1)*math.sin(la2)-math.sin(la1)*math.cos(la2)*math.cos(dl)
    return d, (math.degrees(math.atan2(y,x))+360) % 360

print(f"px per figure-unit (circles 4,8,12): {k_circ:.2f}")
print("\nLandmark check: pixel distance from crosshair vs geographic distance")
pairs = []
for name, px, py, lat, lon in LM:
    rpx = math.hypot(px-CX, py-CY)
    mi, brg = dist_brg(DIABLO, (lat, lon))
    pairs.append((name, rpx, mi))
    print(f"  {name:<15} px={rpx:6.1f}  miles={mi:5.1f}  px/mile={rpx/mi:5.2f}")
# least squares through origin: px = kp * miles
kp = sum(r*m for _, r, m in pairs) / sum(m*m for _, _, m in pairs)
mi_per_unit = k_circ / kp
print(f"\nfit px/mile (through origin) = {kp:.2f}")
print(f"implied miles per figure-unit (circle label) = {mi_per_unit:.2f}")
ratios = [k_circ/(r/m) for _, r, m in pairs]
print(f"per-landmark implied miles/unit: min {min(ratios):.2f}, max {max(ratios):.2f}")
resid = [r - kp*m for _, r, m in pairs]
print(f"residual px: min {min(resid):.1f}, max {max(resid):.1f}  (label-centre error dominates)")

print("\nWhite marker on the 12-circle (Foxon's (12,3) point, read from figure):")
mx, my = 186, 410
rpx = math.hypot(mx-CX, my-CY)
ang = math.degrees(math.atan2(CY-my, mx-CX)) % 360   # anticlockwise from east
print(f"  radius {rpx:.0f} px = {rpx/k_circ:.2f} figure-units; angle {ang:.1f} deg = {math.radians(ang):.3f} rad")
print(f"  geographic distance implied by figure fit: {rpx/kp:.1f} miles")
print(f"  distance if 6.4 mi/inch (claimed elsewhere): {12*6.4:.1f} miles")
print(f"  Orinda Village label distance from crosshair (typed coords): {dist_brg(DIABLO,(37.8377,-122.1080))[0]:.1f} miles")

with open('z32_map_scale_check.csv','w',newline='') as f:
    w = csv.writer(f)
    w.writerow(['landmark','px_from_centre','miles_typed_coords','px_per_mile'])
    for name, r, m in pairs:
        w.writerow([name, round(r,1), round(m,2), round(r/m,2)])
print("\nwritten z32_map_scale_check.csv")

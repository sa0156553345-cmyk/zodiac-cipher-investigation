"""Geodesy helpers used by the map-calibration audit.
Vincenty (1975) inverse and direct formulae on the WGS84 ellipsoid, plus a haversine check on a sphere.
Angles: degrees unless stated. Distances: metres in the functions below; miles are converted explicitly.
Azimuth convention: degrees clockwise from true north (compass bearing)."""
import math

A_WGS84 = 6378137.0
F_WGS84 = 1 / 298.257223563
B_WGS84 = (1 - F_WGS84) * A_WGS84
METRES_PER_MILE = 1609.344
EARTH_RADIUS_MILES_SPHERE = 3958.8


def dms_to_deg(deg, minutes, seconds, hemisphere=None):
    """Degrees, minutes, seconds to signed decimal degrees. hemisphere in {'N','S','E','W', None}."""
    val = abs(deg) + minutes / 60.0 + seconds / 3600.0
    sign = -1.0 if (deg < 0 or hemisphere in ('S', 'W')) else 1.0
    return sign * val


def vincenty_inverse(lat1, lon1, lat2, lon2, max_iter=200, tol=1e-12):
    """Returns (distance_m, azimuth_from_point1_deg, azimuth_from_point2_deg)."""
    if abs(lat1 - lat2) < 1e-14 and abs(lon1 - lon2) < 1e-14:
        return 0.0, 0.0, 0.0
    L = math.radians(lon2 - lon1)
    U1 = math.atan((1 - F_WGS84) * math.tan(math.radians(lat1)))
    U2 = math.atan((1 - F_WGS84) * math.tan(math.radians(lat2)))
    sinU1, cosU1 = math.sin(U1), math.cos(U1)
    sinU2, cosU2 = math.sin(U2), math.cos(U2)
    lam = L
    converged = False
    for _ in range(max_iter):
        sinLam, cosLam = math.sin(lam), math.cos(lam)
        sinSigma = math.sqrt((cosU2 * sinLam) ** 2 + (cosU1 * sinU2 - sinU1 * cosU2 * cosLam) ** 2)
        if sinSigma == 0.0:
            return 0.0, 0.0, 0.0
        cosSigma = sinU1 * sinU2 + cosU1 * cosU2 * cosLam
        sigma = math.atan2(sinSigma, cosSigma)
        sinAlpha = cosU1 * cosU2 * sinLam / sinSigma
        cosSqAlpha = 1 - sinAlpha ** 2
        cos2SigmaM = cosSigma - 2 * sinU1 * sinU2 / cosSqAlpha if cosSqAlpha != 0 else 0.0
        C = F_WGS84 / 16 * cosSqAlpha * (4 + F_WGS84 * (4 - 3 * cosSqAlpha))
        lamPrev = lam
        lam = L + (1 - C) * F_WGS84 * sinAlpha * (
            sigma + C * sinSigma * (cos2SigmaM + C * cosSigma * (-1 + 2 * cos2SigmaM ** 2)))
        if abs(lam - lamPrev) < tol:
            converged = True
            break
    if not converged:
        raise ValueError("Vincenty inverse did not converge")
    uSq = cosSqAlpha * (A_WGS84 ** 2 - B_WGS84 ** 2) / (B_WGS84 ** 2)
    Aa = 1 + uSq / 16384 * (4096 + uSq * (-768 + uSq * (320 - 175 * uSq)))
    Bb = uSq / 1024 * (256 + uSq * (-128 + uSq * (74 - 47 * uSq)))
    deltaSigma = Bb * sinSigma * (cos2SigmaM + Bb / 4 * (
        cosSigma * (-1 + 2 * cos2SigmaM ** 2) - Bb / 6 * cos2SigmaM * (-3 + 4 * sinSigma ** 2) * (-3 + 4 * cos2SigmaM ** 2)))
    s = B_WGS84 * Aa * (sigma - deltaSigma)
    alpha1 = math.atan2(cosU2 * sinLam, cosU1 * sinU2 - sinU1 * cosU2 * cosLam)
    alpha2 = math.atan2(cosU1 * sinLam, -sinU1 * cosU2 + cosU1 * sinU2 * cosLam)
    return s, math.degrees(alpha1) % 360.0, math.degrees(alpha2) % 360.0


def vincenty_direct(lat1, lon1, alpha1_deg, s_m, max_iter=200, tol=1e-12):
    """Returns (lat2, lon2, azimuth_at_point2_deg)."""
    alpha1 = math.radians(alpha1_deg)
    U1 = math.atan((1 - F_WGS84) * math.tan(math.radians(lat1)))
    sinU1, cosU1 = math.sin(U1), math.cos(U1)
    sinAlpha1, cosAlpha1 = math.sin(alpha1), math.cos(alpha1)
    sigma1 = math.atan2(math.tan(U1), cosAlpha1)
    sinAlpha = cosU1 * sinAlpha1
    cosSqAlpha = 1 - sinAlpha ** 2
    uSq = cosSqAlpha * (A_WGS84 ** 2 - B_WGS84 ** 2) / (B_WGS84 ** 2)
    Aa = 1 + uSq / 16384 * (4096 + uSq * (-768 + uSq * (320 - 175 * uSq)))
    Bb = uSq / 1024 * (256 + uSq * (-128 + uSq * (74 - 47 * uSq)))
    sigma = s_m / (B_WGS84 * Aa)
    for _ in range(max_iter):
        cos2SigmaM = math.cos(2 * sigma1 + sigma)
        sinSigma, cosSigma = math.sin(sigma), math.cos(sigma)
        deltaSigma = Bb * sinSigma * (cos2SigmaM + Bb / 4 * (
            cosSigma * (-1 + 2 * cos2SigmaM ** 2) - Bb / 6 * cos2SigmaM * (-3 + 4 * sinSigma ** 2) * (-3 + 4 * cos2SigmaM ** 2)))
        sigmaPrev = sigma
        sigma = s_m / (B_WGS84 * Aa) + deltaSigma
        if abs(sigma - sigmaPrev) < tol:
            break
    sinSigma, cosSigma = math.sin(sigma), math.cos(sigma)
    cos2SigmaM = math.cos(2 * sigma1 + sigma)
    tmp = sinU1 * sinSigma - cosU1 * cosSigma * cosAlpha1
    lat2 = math.atan2(sinU1 * cosSigma + cosU1 * sinSigma * cosAlpha1,
                      (1 - F_WGS84) * math.sqrt(sinAlpha ** 2 + tmp ** 2))
    lam = math.atan2(sinSigma * sinAlpha1, cosU1 * cosSigma - sinU1 * sinSigma * cosAlpha1)
    C = F_WGS84 / 16 * cosSqAlpha * (4 + F_WGS84 * (4 - 3 * cosSqAlpha))
    L = lam - (1 - C) * F_WGS84 * sinAlpha * (
        sigma + C * sinSigma * (cos2SigmaM + C * cosSigma * (-1 + 2 * cos2SigmaM ** 2)))
    lon2 = math.radians(lon1) + L
    alpha2 = math.atan2(sinAlpha, -tmp)
    lon2_deg = (math.degrees(lon2) + 540.0) % 360.0 - 180.0
    return math.degrees(lat2), lon2_deg, math.degrees(alpha2) % 360.0


def haversine_miles(lat1, lon1, lat2, lon2, radius_miles=EARTH_RADIUS_MILES_SPHERE):
    la1, lo1, la2, lo2 = map(math.radians, (lat1, lon1, lat2, lon2))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * radius_miles * math.asin(math.sqrt(h))


def geodesic_miles(lat1, lon1, lat2, lon2):
    d_m, _, _ = vincenty_inverse(lat1, lon1, lat2, lon2)
    return d_m / METRES_PER_MILE


def bearing_deg(lat1, lon1, lat2, lon2):
    _, a1, _ = vincenty_inverse(lat1, lon1, lat2, lon2)
    return a1


def destination(lat1, lon1, bearing, miles):
    lat2, lon2, _ = vincenty_direct(lat1, lon1, bearing % 360.0, miles * METRES_PER_MILE)
    return lat2, lon2


def en_miles_from_origin(origin_lat, origin_lon, lat, lon):
    """East and North displacement (miles) of (lat, lon) from origin, through the geodesic azimuth and distance."""
    d_m, az, _ = vincenty_inverse(origin_lat, origin_lon, lat, lon)
    d = d_m / METRES_PER_MILE
    rad = math.radians(az)
    return d * math.sin(rad), d * math.cos(rad)

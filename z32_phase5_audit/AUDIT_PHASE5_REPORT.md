> Translated from Arabic into English. The Arabic original is kept in the research workspace; its SHA-256 is 0df7153e70686dbd1c12ba3578aaadc1ed6f850d3ea10f79f2e5ab75b6114f1b.

# Independent arithmetic audit of phase 5

## 0. Summary

- **The arithmetic is correct within the inputs.** The independent implementation does not import any code from phase 5, and it matches the CSV file within rounding: the direction by 0.0027°, and the points by 8.0 m (with the rounded CSV inputs) and 0.1 m (with the exact scale).
- **The Vincenty solver is verified** against a published example (Flinders Peak to Buninyong): error 1.4e-07°.
- **The candidate point does not lie on any of the eight rays at any scale.** The nearest position on any ray is **1.476 miles** away, and the angular difference from the E-CCW ray is +6.348°. This is a geometric result that does not depend on Grinell's claim.
- **The conflict of the scale 1.162 with the range** is conditional on Grinell's claim "five inches", and this claim has not been measured.

## 1. Corrections to the previous report

1. **Numerical error:** I wrote that the endpoints at 6.4 are "60 to 103 miles" away. The correct figure at 6.4 alone is **63.55 to 90.08 miles**. The number 103 is the maximum distance across the whole range.
2. **Naming the verdict:** "not supported" is correct without any condition, because the positive condition is geometrically impossible. "Conflicting" is correct under the registered rule, but it is conditional on the correctness of the claim "five inches". This must be stated explicitly.
3. **Unjustified direction claims:** I wrote that "4 inches is in the bay and 6 inches in the ocean". That is a statement about direction, while the registered test concerns only distance. From the check: the actual direction of San Francisco from Mount Diablo is **255.2°**, while Grinell's description (4 rad clockwise from the vertical axis) gives **229.2°**, so his directional description is about 26° off. Therefore I withdraw the bay and ocean claims.

## 2. The equations, step by step

**Coordinate system:** geographic (latitude and longitude), with the origin at Mount Diablo, NAD27 datum, from Foxon 2023, table T2: φ0 = 37.8817742°, λ0 = −121.9130850°.

**(a) Declination and rounding:**
- Declination: 16.9° (IGRF model, from Foxon).
- Hour: H = floor(16.9 / 30) = 0, displayed as 12, so **r = 12**.
- Minute: M = round(16.9 / 6) = round(2.8167) = **3**, so **θ = 3 rad = 171.887°**.
- Sensitivity only: the floor rule gives M = 2. Foxon's declination range (16.3° to 17.7°) gives M = 3 always with the round rule, and M = 2 always with the floor rule. So the difference comes from the rounding rule, not from the declination value.
- **The declination does not enter the direction** in the registered set. It enters only in the calculation of the minute. Any rotation of the direction by the declination is not part of the eight conventions; I tested it as an unregistered path (section 5).

**(b) Direction:** b = (β_ref ± θ) mod 360, where β_ref ∈ {N: 0°, E: 90°, S: 180°, W: 270°}, with + for clockwise (CW) and − for anticlockwise (CCW).

**(c) Distance:** D = r · s, where s = miles per printed inch. **This is the unknown**, and it has no measurement on the original map.

**(d) End point on the sphere (R = 3958.8 miles):**
- δ = D / R
- φ2 = asin( sin φ1 · cos δ + cos φ1 · sin δ · cos b )
- λ2 = λ1 + atan2( sin b · sin δ · cos φ1 , cos δ − sin φ1 · sin φ2 )

**(e) End point on the ellipsoid (Vincenty direct)** for the Clarke 1866 (NAD27) and WGS84 references, using the published equations.

**(f) Consistency check:** the distance recovered from the end point minus D = 3.2e-05 miles; the recovered direction minus b = 4.1e-05°.

## 3. Is the unit a real inch? The evidence and the doubt

- **r = 12:** its source is the hour according to Foxon's model, not the text of the message. The phrase "TWELVE INCHES" is the archive's hypothesis T1, not a reading from the message.
- **Rings 4, 8 and 12:** written inside squares, in the same typeface as the radian labels (0.785, 1.571, ...). These labels are probably analytical annotations added by researchers. This is an opinion from examining the image, not a measurement. Therefore there is no evidence that the rings come from the original map.
- **Scale 1.162:** not a measurement on the map. It is "miles per figure unit" from matching city pairs in the redrawn image, and it implicitly assumes that the unit of the ring equals a printed inch.
- **Consistency test:** if the unit is a printed inch with a scale of 1.162, San Francisco lies about **22.9 inches** away, not 5. If Grinell's claim is correct, the unit is not the ring unit. The two hypotheses cannot both hold, and between them they can be decided only by measuring the original map.

## 4. Matching the eight-convention table with the CSV file

| Check | Result |
|---|---|
| Direction (CSV rounded to 0.01°) | maximum difference 0.0027° |
| Points with the rounded CSV inputs | maximum difference 8.03 m (caused by rounding the distance to 0.01 miles) |
| Points with the exact scale | maximum difference 0.05 m (caused by rounding the scale to 3 decimal places) |
| Distance to the candidate location | maximum difference 0.005 miles (rounding) |
| Sphere: vector against the textual formula | difference 3e-14° |

**No difference exceeds the rounding.** All results match the CSV.

## 5. The independent geometry of the candidate point (depends on no scale)

The distance to the candidate = 13.3519 miles, and the direction = 284.4607°.

| Ray | Its direction | Angular difference from the candidate | Nearest distance to the candidate (miles) | Position of the nearest point |
|---|---|---|---|---|
| N-CW | 171.887° | +112.573° | 13.352 | origin |
| N-CCW | 188.113° | +96.348° | 13.352 | origin |
| E-CW | 261.887° | +22.573° | 5.125 | radial |
| E-CCW | 278.113° | +6.348° | 1.476 | radial |
| S-CW | 351.887° | −67.427° | 12.329 | radial |
| S-CCW | 8.113° | −83.652° | 13.270 | radial |
| W-CW | 81.887° | −157.427° | 13.352 | origin |
| W-CCW | 98.113° | −173.652° | 13.352 | origin |

- The nearest position on any registered ray is **1.476 miles** from the candidate, **for any scale**.
- For E-CCW to pass through the candidate, the origin would have to be displaced by about **2.38 km**, or the ray rotated by 6.35°. The difference between the NAD27 and USSD references is no more than 0.05 km, about 50 times less. So the geodetic reference cannot explain the gap.
- **Unregistered paths (declination ±16.9° applied to the directions):** the closest of them is 1.475 miles (E-CW + 16.9, at the archive scale). It is not within 0.5 miles, so it does not support the candidate. E-CW + 16.9 lies almost exactly on the same E-CCW ray (278.8° against 278.1°).

## 6. Sensitivity to the geodesy

| Test | Maximum difference between the points |
|---|---|
| Sphere against Clarke 1866 against WGS84, at the middle of the scale range | 284 m |
| At 6.4 | 295 m |
| At the archive scale 1.162 | 54 m |
| Difference of the origin between NAD27 and USSD (indicative, not NAD83) | 45.5 m |

The effect on the distance to the candidate when moving to the USSD reference: from 1.476 to 1.458 miles. So the geodesy does not change the verdict. But the ellipsoid difference at 6.4 may reach 0.18 miles, so it must be stated for any future measurement.

## 7. Partial automatic test of the figure marks

- The figure centre, estimated automatically: pixels (491, 454), while the earlier package estimated (490, 454).
- The expected conventions against the nearest detected mark:

| Convention | Difference |
|---|---|
| N-CW | 1.11° |
| N-CCW | 1.11° |
| E-CW | 0.89° |
| E-CCW | 0.61° |
| S-CW | 0.89° |
| S-CCW | 1.11° |
| W-CW | 3.89° |
| W-CCW | 3.89° |

- **6 of the 8 marks** match the expected directions within 1.1° or less.
- **The two right-side marks (W)** differ by 3.9°. The cause is the black image frame near them. Their visible coordinates (797, 410) and (797, 497) were checked by hand, and they correspond to 81.8° and 98.0°. This manual check is an estimate by eye, not a pixel measurement.
- The strongest detected marks (direction, radius in pixels, score):

| Direction | Radius (px) | Score |
|---|---|---|
| 102.0° | 300.0 | 189.2 |
| 78.0° | 300.0 | 187.0 |
| 287.5° | 312.5 | 177.2 |
| 173.0° | 312.5 | 154.4 |
| 261.0° | 313.5 | 154.2 |
| 187.0° | 312.5 | 154.0 |
| 7.0° | 312.0 | 153.9 |
| 351.0° | 313.0 | 153.7 |

- **The detected radius** lies between 310 and 313 pixels, while the earlier package estimated the ring of 12 at 307 pixels. I do not rely on the radius here.
- **Conclusion:** the eight conventions are consistent with the directions of the marks in figure 2, but this automatic detection does not allow a difference of one degree.

## 8. Separating the results

**(a) What the calculation establishes, if the inputs are correct:**
- The candidate is 13.352 miles from Diablo, in the direction 284.46°.
- The nearest registered ray (E-CCW) passes 1.476 miles from it, for any scale.
- The change of datum (NAD27 or USSD) does not alter this.
- Matching the candidate would require rotating the ray by about 6.35°, or displacing the origin by about 2.4 km. Both lie outside the registered set.

**(b) What depends on Grinell's claim ("five inches" and "6.4 miles per inch"):**
- The accepted scale range is [4.833, 7.486] miles per inch.
- The archive scale 1.162 lies outside the range, but this matters only if the claim is true.
- The eight endpoints at the range lie 44.8 to 103.1 miles from the candidate.
- The internal consistency check: the claim of 6.4 gives 5 inches = 32 miles, which lies within the approximate boundaries of San Francisco. But this is internal consistency of the distance, not a measurement on the map.

**(c) What cannot be decided before the original map:**
- The actual printing scale (s).
- Whether the unit of the rings is a real inch.
- Whether the declination applies to the direction (and not only to the minute).
- Which reference convention the author intended, and the rounding rule.
- The point from which the author measured the circle (the summit or the crosshair).

## 9. Applying the registered decision rules literally

| Rule | Condition | Calculated value | Result |
|---|---|---|---|
| "supported" | an endpoint (minute 3) within 0.5 miles **and** the scale in the range | nearest distance on any ray, for any scale: 1.476 miles; nearest distance across the range: 44.75 miles | **geometrically impossible: not supported** |
| "conflicting" | all eight endpoints further than 2 miles across the range **and** the range excludes 1.162 | both conditions hold | **conflicting, conditional on the correctness of Grinell's claim** |
| "undecided" | otherwise | does not apply | — |

**Note:** the verdict "conflicting" depends on a range built from Grinell's claim. If the claim is wrong, the verdict becomes "undecided", because the actual scale would be unknown.

## 10. The next most valuable test

**A direct measurement of s on the original map, or on a high-resolution image with a scale bar or a known reference distance.** The steps:

1. Measure, in pixels, the distance between the Mount Diablo point and the point on the map that is taken as "San Francisco", then convert it to printed inches using the scale bar.
2. Identify the two points between which "five inches" was measured, because the current claim does not specify a single point.

**What it can establish:**
- If s is in [4.8, 7.5], the claim is consistent with the map, and the pre-registered test can then be applied with the measured scale.
- If s is about 1.1 to 1.2, the claim is wrong, and the idea that the unit is a printed inch falls.
- If s is between these values, the claim is overstated or the scale is different.

**What it cannot establish:**
- It does not establish any convention, location or solution for Z32.
- It does not decide whether a solution exists inside or outside the set.
- It determines only the scale, which is a necessary condition for any calibration, not a sufficient one.

**Pre-registration before measuring:** record the complete set of conventions (references × two directions × rounding rule (round or floor) × whether the declination applies to the direction or not). Then run a positive control: plant a known target in a synthetic map at the measured scale, and check that the line recovers it. This shows that the line does not err in converting directions and distances.

## 11. Files of this review

- `audit_phase5_independent.py`: the full independent implementation (it does not import any phase-5 code).
- `independent_endpoints.csv`: 80 points by three calculation methods (sphere by vector, sphere by text formula, Clarke 1866, and WGS84).
- `audit_summary.json`: all the numbers used in this report.

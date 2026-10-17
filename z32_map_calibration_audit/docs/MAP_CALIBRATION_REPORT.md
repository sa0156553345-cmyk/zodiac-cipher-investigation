> Translated from Arabic into English. The Arabic original is kept in the research workspace; its SHA-256 is 4894cedf258b767f7cbaf674274e77a9f2043f3b07d71bdfeb15a6b504fccd07.

# Geographic calibration audit report for the Mount Diablo map (Z32)

## 0. Summary

1. **The measurement inside the image is accurate.** The centre of the grid, the ring radii and the image scale in figure units are measured with an error of about 0.3 to 0.5 %. But this scale gives "figure units", not miles.
2. **The geographic link is not reliable to better than a few miles.** The residuals of five cities range from 2.0 to 5.8 miles, and the pre-registered criterion of scale spread between pairs failed at 71 %.
3. **The location calculated from the paper is not determined to one mile.** Within the text-supported core it varies by about 6 miles, and across the whole accepted family by about 43 miles. The largest factors are: **the reference angle** (changing the reference moves the location by 4 to 19 miles); **reading the numbers** (rounding the minute moves it by about 13 miles); and then **the scale** (every 0.25 miles per unit moves it about 3 miles).

The detailed answers are in section 10.

## 1. Data sources and their classification

| ID | Data | Type | File |
|---|---|---|---|
| M1 | Centre of the grid, rings, squares, the white mark, angle labels | **measurement** from the image in the paper (page 9) | `results/fig_*.csv` |
| D1 | Figure scale; definition of the polar axis and direction; the possible numbers (12,3) and others | **documented in the paper** (text) | section 3 |
| D2 | Magnetic declination 16.3 to 17.7 (value 16.9); a reference giving 15 | **documented in the paper** (table 2 and text) | `data/reference_points.csv` |
| D3 | Coordinates of Mount Diablo in NAD27 and USSD | **documented in the paper** (table 2) | `data/reference_points.csv` |
| E1 | Coordinates of the five city centres | **external secondary** (Wikipedia, recorded in the previous package; not re-verified in this session) | `data/controls.csv` |
| E2 | Positions of the labels on the image | **reading by eye** (±6 pixels); a **proxy** for city centres, not their positions (see section 4) | `data/controls.csv` |
| E3 | Route 24 point | **coordinate from geocoding a route name**, not a location; not used for selection | `data/reference_points.csv` |
| I1 | Rounding rule (round) and minute = ⌊deviation / 6°⌉ | **inference** from the rounding symbol in the paper | section 3 |
| I2 | "3" taken as radians | **inference** from the word "Radians"; the value 3 itself is inferred from the minute | section 3 |
| I3 | Foxon's circles represent the printed inches of the original map | **assumption** not documented in the paper | section 6 |

## 2. Measurement inside the image (computed)

### 2.1 Equations

- Centre of the circle by least squares (Kasa): solve the least-squares problem for `2a·x + 2b·y + c = x² + y²`, then `R = √(c + a² + b²)`. Points whose residual exceeds 2 pixels are rejected, and the process is repeated until it stabilises.
- Image scale: `U = R_n / n` pixels per unit for ring `n ∈ {4, 8, 12}`, and `U = (Σ R_n·n) / (Σ n²)` for the set.
- Points excluded before fitting: crossing lines (angles near multiples of 45°), label squares, the handwritten text, and the white mark.

### 2.2 Centre

| Method | Centre (pixels) |
|---|---|
| Crosshair lines (argmax) | (490.00, 454.00) |
| Crosshair lines (sub-pixel centre of mass) | (490.49, 454.36) |
| Circle fit, weighted mean (**adopted**) | **(490.88, 454.30)** |
| Mean of the eight outer squares and the mark | (491.00, 454.25) |

The largest difference among the four methods is **1.03 pixels**. The three rings are concentric (the difference between their centres is less than 0.02 pixels).

### 2.3 Ring radii and scale in pixels

| Ring | Radius (px) | Inliers | Fit error (rms) | Pixels per unit |
|---|---|---|---|---|
| 4 | 102.58 | 584 | 0.67 | 25.645 |
| 8 | 205.16 | 1684 | 0.68 | 25.645 |
| 12 | 307.70 | 2740 | 0.73 | 25.642 |

| Method | Pixels per unit |
|---|---|
| Circle fit (Kasa) | 25.644 |
| Eight outer squares and the mark (mean) | 25.677 |
| Individual squares (sd = 0.045) | 25.677 |
| Unified formula (least squares through the origin) | 25.643 |
| **Combined (mean of the method means)** | **25.660** |

- **Spread of the methods:** 0.019 pixels per unit (0.08 %).
- **Conservative error margin:** the spread of the centre (±1 pixel) gives ±0.3 % in the radius; manual reading of the squares (±3 pixels) gives ±0.35 % on average. The conservative total is ±0.5 %, about ±0.13 pixels per unit.
- **What this margin does not cover:** any distortion in Foxon's drawing, or any difference between the scale of the figure and the scale of the original printed map. That difference cannot be measured from the image alone.

The earlier value in the previous package was 25.59 pixels per unit (argmax method on the rings). The 0.3 % difference comes from a more accurate centre and a more accurate fit. It is recorded in `CHANGE_LOG.md`.

### 2.4 Internal checks of the figure

- **The white mark (Foxon's 12,3):** predicting its position with `(x, y) = C + 12·U·(cos 3, −sin 3)` lies only **0.85 pixels** from its measured position. So Foxon drew his mark exactly according to his reading (12,3), within the frame of the figure.
- **Angle labels on the outer ring:** the measured angles agree with the written radians (0, 0.785, 1.571, ...) with a maximum error of **0.54°**. This confirms that the angle of the figure is counted in radians, from the east (0), anticlockwise. **This establishes the drawing convention, not that Zodiac used it.**

## 3. Definition of angle and direction

### 3.1 What the paper says (paraphrased)

- The paper defines polar coordinates with a polar axis towards the east and a positive direction anticlockwise (section 4.4).
- The paper takes the pole of the system to be Mount Diablo on the Phillips 66 map (assumption 2).
- The clock numbers are read from the position of clock hands set to magnetic north. The paper admits that the clock reading 12:03 gives the pair (12,3) (section 4.2).
- The instruction "is to be set to Mag. N." is handwritten near the crosshair on the figure.

### 3.2 What the paper does not determine

1. **The angle reference:** is θ measured from the map's east axis (as the paper assumes), from magnetic north, or is the map itself rotated by the declination? The instruction "is to be set to Mag. N." refers to the crosshair or the map, but does not specify which reference is used to read the angle.
2. **The angle value:** the number 3 comes from reading the minute (clock 12:03). No passage in the text defines "minute 3" as "3 radians". The word "Radians" specifies only the unit. If the third minute meant 18° on the clock face (3 × 6°), the angle would be 18°, not 171.9°. **The value of 3 radians is an inference from the paper, not a textual given.**
3. **Rounding:** the paper writes ⌊·⌉ for the minute, the symbol for rounding to the nearest integer. The paper does not justify rounding over flooring, and it does not mention an alternative. We therefore take (12,3) as the rounding interpretation, and (12,2) as the flooring alternative.
4. **The declination:** the paper does not say that the map is rotated by the declination. The declination enters only in calculating the numbers (the hour and the minute).

### 3.3 The equations for the different references

After converting to east and north (E, N) in miles, for each reference:

- **R0** (east axis of the map, anticlockwise): shape direction `v = (cos θ, sin θ)`.
- **R1** (east axis of the map, clockwise): `v = (cos θ, −sin θ)`.
- **R2** (magnetic north, clockwise): true azimuth `β = θ_deg + D`, with `D` positive to the east.
- **R3** (magnetic north, anticlockwise): `β = D − θ_deg`.
- **R4±** (the map rotated by ±D): `β = β(R0) ± D`.

**A geometric fact established by calculation:** a declination of D = +16.9° to the east means that magnetic north lies about 17° east of true north. If a clock hand is turned by the angle D clockwise from true north, it will point to magnetic north. This agrees with the clockwise direction of the clock in the paper, and confirms that the eastward sign of the declination is positive.

## 4. External coordinates, and separating them from the measurement

### 4.1 Mount Diablo

- NAD27, from table 2: 37.881774° N, 121.913085° W.
- USSD, from table 2: the difference between the two is **0.028 miles (45.5 m)**. It does not change any result by more than 0.03 miles (section 7).
- **The crosshair is not the summit of Mount Diablo:** the offset between them is unknown. It is estimated by the geographic link (G1 gives an offset of about 2 to 3 miles), and it is tested with the configuration "pole = summit" (PS).

### 4.2 The link cities: why are the label positions used?

- The image contains no city symbols, only labels placed near approximate positions. No other reference inside the image links it to geography.
- **Justification:** without them there is no geographic scale or direction, and both the scale and the direction remain completely free (section 9, the model "without controls").
- **Limit:** the earlier comparison showed that San Leandro lies **west** of Oakland in the image, whereas geographically it is east of Oakland. The offset reaches about 8 miles. The link results are therefore treated as conditional.

### 4.3 Test of the pre-registered criterion (scale spread between city pairs)

- The pairs: 10 pairs of the five cities; the geodesic distance (Vincenty) and the image distance.
- Formula: `miles_per_unit = U / (px_per_mile)`.
- Result: from **0.875** to **1.647** miles per unit, with a median of **1.082**. The spread `(max − min) / median = 71 %`, which is **much greater than 10 %**.
- **The pre-registered verdict:** according to this link, the image scale is **not reliable** for converting units into miles across pairs. The figure's own configuration (pixels per unit) remains accurate, as in section 2.

## 5. Geographic link (computed; models G1 to G8)

### 5.1 Equations

- `X = A·(E, N) + t`, where `(E, N)` are in miles from the summit of Mount Diablo (NAD27) along the geodesic (Vincenty), and `(X, Y)` are in pixels from the centre of the figure.
- Similarity: `A = [[a, −b], [b, a]]`, `ppm = √(a² + b²)`, `φ = atan2(b, a)`, `s_fit = U / ppm` (miles per unit).
- Affine: `A` a general 2 × 2 matrix, and `s_fit = U / √|det A|`.

### 5.2 Results

| Model | Description | Pixels per mile | Miles per unit | Rotation (°) | Offset (px) | rms (px) | Worst residual (px) |
|---|---|---|---|---|---|---|---|
| G1 | similarity, 5 cities, free offset | 22.00 | 1.166 | −4.72 | (−26.7, −53.0) | 54.0 | 128.4 (Oakland) |
| G2 | similarity, zero offset (crosshair = summit) | 23.52 | 1.091 | −1.77 | (0, 0) | 63.3 | 132.9 |
| G3 | affine, 5 cities | 22.05 | 1.164 | — | (−56.5, 1.9) | 44.8 | 102.4 |
| G4 | without Oakland | 23.46 | 1.094 | −4.86 | (−45.8, −40.7) | 28.3 | 52.4 |
| G5 | without San Leandro | 21.75 | 1.180 | −4.03 | (−17.0, −49.3) | 56.5 | 112.8 |
| G6 | without Hayward | 21.40 | 1.199 | −3.17 | (−22.4, −33.9) | 51.5 | 112.3 |
| G7 | without Livermore | 23.23 | 1.105 | −7.80 | (−2.6, −79.4) | 55.9 | 131.9 |
| G8 | without Vallejo | 19.16 | 1.339 | −4.99 | (−49.4, −94.6) | 53.2 | 93.4 |

**G1 residuals in miles** (the pixel residuals divided by 22.0): Oakland 5.8; San Leandro 2.4; Hayward 3.5; Livermore 2.0; Vallejo 2.1.

**Reading of the results:**

- The figure's scale is estimated between **1.09 and 1.34 miles per unit**. This range is consistent with the assumption that the circles are printed inches (I3).
- The estimated rotation lies between **−1.8 and −7.8 degrees**: the image is roughly oriented with true north upward, but with a spread of a few degrees. (True north appears at about 90° + φ in the figure, that is, roughly 2 to 8 degrees clockwise from the figure's vertical axis.)
- The residuals far exceed the pixel reading error (±6 pixels). They are the result of the **displacement of the labels** from the city centres, not a reading error.

### 5.3 Map-rotation test (exploratory, added after the pre-registered run)

A model with a fixed rotation; the scale and the offset are free.

| Assumption | Rotation | rms (free offset) | Worst residual | rms (zero offset) |
|---|---|---|---|---|
| true north upward | 0° | **81.1** | 127.5 | 90.6 |
| east declination (the map rotated) | +16.9° | 143.6 | 206.0 | 169.4 |
| west declination | −16.9° | 103.3 | 128.1 | 147.5 |

**Conditional conclusion:** the label positions agree with "true north upward" more than with "rotation by the declination" (the rms is smaller by a factor of 1.3 to 1.8). But the label residuals are large and carry a systematic offset, so this result does not settle the question alone. It limits the reference R4± unless one accepts that the labels are displaced in a pattern that requires rotation.

## 6. Family of transformations (pre-registered, and run)

### 6.1 Equations

- The location is `(E, N) = O + Δ`, where `O` is the pole and `Δ` is the offset.
  - PC: `O = A⁻¹(−t)` (the centre of the figure as it is on the map). PS: `O = (0, 0)` (the summit of Mount Diablo).
  - R0 and R1 with s = fit: `Δ = A⁻¹(r·U·v)` (the geometry of the figure itself). With a numeric s: `Δ = r·s·A⁻¹v / |A⁻¹v|`.
  - R2, R3 and R4: `Δ = r·s·(sin β, cos β)`.
- Coordinates: `lat, lon` from the direct Vincenty solution from the summit, with azimuth `atan2(E, N)` and distance `√(E² + N²)`.
- Acceptance: `0 ≤ px ≤ 915` and `0 ≤ py ≤ 893`, after projecting the location onto the image (the published frame).

### 6.2 Numbers

- Number of configurations: **4800** = 5 numbers × 6 references × 5 declinations × 2 scales × 8 links × 2 poles. (The pre-registration document stated 9600, an arithmetic error; the rule itself did not change. See `CHANGE_LOG.md`.)
- Inside the frame: **3695** configurations, of which 480 are for the number (12,3) alone.
- **Baseline (the configuration the paper implicitly describes):** N_round, R0, D = 16.9, s = fit, G1, PC, giving the coordinates **37.92979° N, 122.15032° W**, inside the frame.

### 6.3 Applying the registered decision rules

| Rule | Result | Verdict |
|---|---|---|
| The text-supported core (48 locations: R0, N_round, s = fit, D ∈ {16.3, 16.9, 17.7}, G1 to G8, PC/PS): maximum spread | **5.98 miles** | **undetermined** (the requirement is less than 1 mile) |
| The whole accepted family (3695 locations): maximum spread | **43.1 miles** | **undetermined** |
| The frame with s = 6.4: for the number 12, outside the frame (about 63 miles from the baseline) | — | **excluded** for configurations with the number 12 |
| The frame with s = 6.4 and the numbers (3, 0) or (3, 12): inside the frame (distance 19 miles or less) | — | the exclusion is **conditional on the number** |

**Note:** the statement "6.4 is excluded" needs explanation. The calculated frame depends on the link G (that is, on 25.66 pixels being one unit, and on the image containing the cities at their measured distances). If the scale of the figure were 6.4 miles per unit, the cities on the image would be about five times closer than they are. This conclusion is conditional on the unit representing a printed inch with a scale of 6.4 (I3).

## 7. Sensitivity: which assumption affects the result most

The table changes one factor from the baseline, with the others fixed. The values are the shift in miles.

| Assumption changed | Shift (miles) | Note |
|---|---|---|
| reference of the angle R2 (magnetic north, clockwise) | **18.8** | angle reference |
| reference R3 | 15.7 | angle reference |
| reading of the numbers (3, 0) | 17.5 | numbers |
| reading of the numbers (3, 12 mod 2π) | 17.2 | numbers |
| reading of the numbers (12, 2) by flooring | **13.4** | rounding |
| reading of the numbers (0, 3) (the same pole) | 14.0 | numbers |
| scale 6.4 miles per unit | 62.8 (outside the frame) | scale |
| scale from 1.0 to 1.25 miles per unit (R0) | about 3 per 0.25 miles | scale |
| declination from 0 to 17.7 with R2 | about 2.8 | declination (does not affect R0) |
| declination within the range 15 to 17.7 with R2 | about 0.5 | declination (does not affect R0) |
| reference R1 | 4.0 | angle reference |
| rotation ±D (R4±) | 4.1 | angle reference |
| pole = the actual summit (PS) | 2.7 | pole |
| link G8 (without Vallejo) | 2.9 | link |
| link G2 (zero offset) | 1.9 | link |
| link G4 (without Oakland) | 1.8 | link |
| link G3 (affine) | 0.9 | link |
| links G5, G6 and G7 | 0.5 to 0.7 | link |
| free rotation without controls (section 9) | 0.7 to 6.4 at s ≤ 1.5 | scale and rotation |
| **angle in degrees rather than radians (not supported by the text)** | shown separately: R0 gives (37.945, −121.641) | not supported |
| **difference between USSD and NAD27** | 0.03 | data |

**Ranking by effect:** angle reference ≈ reading of the numbers > scale > pole > link > declination (no effect on R0) > the NAD27 or USSD reference date.

## 8. Checks of the calculations (independent tests)

- **`tests_geodesy.py` (13 tests):** conversion of DMS values from Foxon; the Vincenty reference (54972.271 m, azimuth 306.8681°); the direct-inverse round trip (less than 1 mm); symmetry; the difference between ellipsoid and sphere; the east and north directions; the geodesic offset; the E/N components; the NAD27 and USSD difference.
- **`tests_transforms.py` (27 tests):** directions R0 and R1 by closed calculation; directions R2 to R4 with the declination; the angle 3 radians = 171.887°; rounding 16.9/6 = 3 with rounding, and 2 with flooring; the scale 6.4 (76.8 miles for 12 units); agreement of the numeric mode with s_fit (difference 4·10⁻¹⁵ miles); the affine model; the poles; the reverse transformation EN to lat/lon; the exclusion of 6.4 outside the frame; the position of the white mark (0.85 pixels); the angle labels (0.54°).

**Errors in the tests themselves, found and corrected before delivery:** (a) the threshold for the difference between the ellipsoid and the sphere was 0.1 %, and a difference of 0.21 % appeared, which is a known difference, so it was changed to 0.5 % with the reason recorded; (b) a test contained `or True`, so it always passed. It was replaced by a real test that checks the actual difference between the two poles.

## 9. The "without controls" model: what happens without cities

If the label positions are not accepted at all, the scale `s` and the rotation `φ` remain unknown. The location is then a function of them:

- s = 0.8 to 1.5 miles per unit, and φ = −10° to +10°: the shift from the baseline is **0.7 to 6.4 miles**.
- s = 2 to 3: the shift is **11 to 23 miles**.
- **Warning:** the "inside the frame" test in this family does not mean anything, because the frame stretches with the same assumption. It is flagged in `noctrl_family.csv` with the column `frame_test_meaningful`.

## 10. Final answers

### 10.1 Can the geographic transformation be rebuilt from the paper alone?

**No.** The **polar formula inside the figure** can be built (the centre, the rings, the unit, the white mark), and this has been verified. But the transformation into geography requires five elements that the paper does not contain:

1. The scale of the original printed map (miles per inch); the figure carries no scale bar.
2. A reliable geographic link for the figure: the labels alone give residuals of 2 to 6 miles.
3. The angle reference (magnetic, the map's east axis, or a rotated map); the text does not say which.
4. The reading of the numbers: rounding or flooring. The text justifies neither, and minute 3 does not mean 3 radians in the text.
5. The relation between the pole (the crosshair) and the actual summit of Mount Diablo.

### 10.2 Which assumptions have the most effect?

1. **The angle reference** (moves the location 4 to 19 miles).
2. **The reading of the numbers** (13 to 17 miles).
3. **The scale** (about 3 miles per 0.25 miles per unit, and outside the frame at 6.4).
4. **The pole** (2.7 miles) and **the geographic link** (up to 2.9 miles).
5. **The declination** affects only R2 to R4: about half a mile within the range 15 to 17.7, and about 2.8 miles if D = 0 is used instead of 16.9.

The most sensitive and undetermined assumption is **the angle reference**, which the paper does not settle.

### 10.3 What additional data would settle the open points?

- **A high-resolution copy of the original map** (Phillips 66), with its scale bar or a measurement of a known distance on the map itself. This settles the inch scale (1.09, 6.4, or another value).
- **Reliable geographic positions for unambiguous features** on the same map: city symbols, airports (an official reference point), bridges, or specific road junctions. This solves the problem of label displacement.
- **The full wording of the instruction** "is to be set to Mag. N." as written on the original map, and the position of the numbers 0, 3, 6 and 9 around the crosshair. This settles the angle reference, if clock numbers appear on the map.
- **Confirmation that the crosshair is the pole**, or that the pole is the actual summit of Mount Diablo.
- **The source of the declination used** (NOAA or another source) and the date of measurement, checked against an independent source, because the present value comes from the paper itself.
- **An explicit statement of the rounding rule** from the original source of the analysis, or Zodiac's own explanation of the numbers.

### 10.4 Is there still independent evidence supporting the resulting location?

**No.** The calculated location (37.929° N, 122.150° W) depends on choices made during the analysis, not on independent evidence:

- the choice of rounding for reading the numbers;
- the choice of angle reference (the map's east axis, which is Foxon's convention and is not imposed by the map);
- the choice that the unit is a printed inch (assumption I3);
- a geographic link built on label positions displaced by 2 to 6 miles.

What is genuinely independent of these choices is the measurement of the figure itself (its centre, rings, scale in its own units, angles, and Foxon's mark). That is internally consistent, but its connection to geography has not been established.

**Verdict:** the current calibration method does not determine a location to better than a few miles, and the resulting location depends on our choices.

## 11. What was not done at this stage

- No new solution for the cipher was searched for, and no phrase or message was tested.
- City coordinates from the internet were not updated in this session; the values recorded in the previous package were used.
- The magnetic declination was not computed locally with an IGRF model; the values documented in the paper were used.

> Translated from Arabic into English. The Arabic original is kept in the research workspace; its SHA-256 is 3ddde4b6f509db565e586f45f82dbdecb269d090e6d54853aba2da13d02e7de7.

# Pre-registration of the rules for the geographic transformation test (frozen before running `transforms.py`)

## 1. Purpose

Determine whether the location (r, θ) referred to in the paper can be pinned down precisely from the paper itself and the available data. Proximity to route 24 is not used as a selection criterion; it is only recorded.

## 2. Measured inputs (computed results)

- Centre of the grid (Mount Diablo on the image): from `results/fig_centre_estimates.csv`, method "ring_fits_weighted_mean".
- Image scale: `results/fig_px_per_unit_combined.csv` (the combined value of the four methods).
- Radii of rings 4, 8 and 12: `results/fig_ring_fits.csv`.

## 3. Inputs documented in the paper (paraphrased; to be checked before publication)

- The angle in polar form: the polar axis points east, and the direction is anticlockwise (paper, section 4.4).
- The two possible values for the rounding: hour = ⌊deviation / 30°⌋, and minute = ⌊deviation / 6°⌉ (paper, section 4.2). The symbol ⌊·⌉ means rounding to the nearest integer.
- The magnetic declination at Mount Diablo in 1970: 16.3 to 17.7 degrees (table 2 in the paper, according to the coordinate reference), with a principal value of 16.9 degrees. The text also cites a reference giving 15 degrees.
- Coordinates: Mount Diablo in NAD27 and USSD (table 2).
- The instruction written on the figure: "is to be set to Mag. N." (figure 2, handwritten annotation).
- The unit: "Radians" is written in the text, and the angle labels on the outer ring of the figure are in radians (0, 1.571, 3.142, ...).

## 4. External sources (treated as secondary inputs)

- City coordinates from Wikipedia pages, as recorded in the previous package. They were not re-read in this session; this is recorded as a limitation.
- Route 24 point: a coordinate produced by geocoding a route name, not the location of an event. It is not used in the selection.

## 5. Central assumption: label positions as proxies for city centres

The image contains no city symbols, only labels. We use the label positions (read by eye, ±6 pixels) against the geographic centres of the cities as temporary proxies for linking the image to geography. The earlier comparison showed an offset of up to about 8 miles (San Leandro), so the link results are treated as conditional, and are tested by deleting each city in turn (G4 to G8) and with a model without cities (section 9).

## 6. Transformation family (frozen)

| Factor | Levels | Reason |
|---|---|---|
| N (pair of numbers) | N_round = (12, 3); N_floor = (12, 2); N_30 = (3, 0); N_312 = (3, 12 mod 2π); N_03 = (0, 3) | The paper names the five pairs. N_floor is an alternative from the paper's formula. N_312 is excluded in the paper under the condition θ < 2π, and is included as a modulo alternative |
| R (angle reference) | R0 east, anticlockwise (the paper's direction); R1 east, clockwise; R2 magnetic north, clockwise; R3 magnetic north, anticlockwise; R4p direction R0 rotated +D; R4m direction R0 rotated −D | The instruction "Mag. N." refers to a magnetic reference, but the text does not specify whether the reference is the measurement angle or a rotation of the map |
| D (declination) | 0; 15; 16.3; 16.9; 17.7 (degrees east positive) | Values from the paper and from the reference it mentions |
| s (distance scale) | fit = U / ppm (from the image and G); 6.4 miles per unit (secondary claim) | Test between the image scale and an external claim |
| G (geographic link) | G1 free similarity (5 cities); G2 similarity with zero offset; G3 affine (5 cities); G4 to G8 free similarity with one city deleted each time | The reasonable models of linking |
| P (pole) | PC: the centre of the grid as it is on the map; PS: the actual summit of Mount Diablo | The paper treats Mount Diablo as the pole. The difference between the two centres is the offset in G |

Total: 5 × 6 × 5 × 2 × 8 × 2 = 9600 configurations.

Note: the "3 radians" reading is adopted as the unit of radians (supported by the word "Radians" and by the figure's labels). The value 3 itself comes from reading the minute; this inference is recorded and is not treated as text. The configuration that treats the angle as degrees (3 degrees) is shown separately, labelled "not supported by the text".

## 7. Transformation equations (written before running)

- Linking: X = A·(E, N) + t, where (E, N) are miles from the summit of Mount Diablo (NAD27) along the geodesic path (Vincenty), and (X, Y) are pixels from the grid centre. The X axis points east and the Y axis points north.
- Similarity: A = [[a, −b], [b, a]], ppm = √(a² + b²), and s_fit = U / ppm.
- Affine: A is a general 2 × 2 matrix, and s_fit = U / √|det A|.
- Pole: PC: O = A⁻¹(−t); PS: O = (0, 0) (the summit).
- R0: the shape direction v = (cos θ, sin θ). The offset, if s = fit: Δ = A⁻¹(r·U·v). If s = 6.4: Δ = r·s·A⁻¹v / |A⁻¹v|.
- R1: v = (cos θ, −sin θ), with the same formulas.
- R2: azimuth β = θ_deg + D. R3: β = D − θ_deg. R4p: β = β(R0) + D. R4m: β = β(R0) − D. The offset is Δ = r·s·(sin β, cos β) in miles.
- Position: (E, N) = O + Δ. Then the coordinate by Vincenty from the summit, with azimuth atan2(E, N) and distance √(E² + N²).

## 8. Feasibility condition (image condition)

A location is accepted if it falls within the frame of the published figure (0 ≤ px ≤ 915, 0 ≤ py ≤ 893), that is, within the displayed map. This is an assumption: the printed map that contains the location matches the frame of the published figure. It is recorded as an independent condition, and is used only to rule out what cannot lie on the map, not to prefer one configuration over another.

## 9. The three test models

- (a) Full: G1, G2 and G3, with all configurations.
- (b) Sensitivity: change one factor at a time from the baseline, holding the other factors fixed.
- (c) Without cities: the link is unknown; the scale s is swept from 0.5 to 7, and the rotation φ from −10° to +10°.

## 10. Baseline (the paper's own configuration, not our choice)

N_round, R0, D = 16.9, s = fit, G1, PC. This is the configuration that the paper describes implicitly.

## 11. Decision rules registered in advance

- The location is considered **precisely determined** if the largest difference between the admissible locations in the "text-supported core" (R0, N_round, s = fit, D in {16.3, 16.9, 17.7}, G1 to G8, P in {PC, PS}) is less than **one mile**.
- The transformation is considered **not determined by the paper** if the above condition is not met.
- The 6.4 claim is considered **inconsistent with the map** if all its locations lie outside the frame.
- The image scale is considered **reliable for converting distance into miles** only if the disagreement between the measured pairs is less than 10 %. This is registered in advance as a criterion and will be tested in the present report. (Note: the criterion itself is not well defined, because the pairs do not measure the scale independently of the linking. It is shown as it is.)

## 12. What counts as evidence for each element

- R0 with N_round is supported by the text (the drawn direction).
- R2, R3 and R4 are supported by the instruction "Mag. N.", but the text does not specify them.
- N_floor is not supported by the text.
- D in the stated range is supported by the paper, but its exact value is not independent of the reference used in the calculation.
- s = 6.4 is supported by a secondary source, and is not based on a measurement in the image.
- The G link depends on label positions as proxies, and is supported by the available data only within conditional limits.

## 13. Freeze

These rules are frozen before running `transforms.py`. Any change after running is recorded in `CHANGE_LOG.md` with its reason, and earlier results are not replaced.

---

## Correction appendix (added after the run; does not change any rule above)

- **Number of configurations:** section 6 states that the total is 5 × 6 × 5 × 2 × 8 × 2 = 9600. The correct calculation is 4800. The factor counts are 5 pairs, 6 references, 5 declinations, 2 scales, 8 links and 2 poles, and the correct total is **4800**. The counting rules themselves did not change, and the results are read on 4800.
- **Frame warning in the family without controls (section 9-c):** the frame test does not suit this family, because the frame stretches with the same assumption. This is flagged in `noctrl_family.csv` in the column `frame_test_meaningful`.
- **Map-rotation test (section 5.3 of the report):** added after the registered run. It is exploratory and does not enter the decision rules.

> Translated from Arabic into English. The Arabic original is kept in the research workspace; its SHA-256 is 4bd222a13b0d1298a35e98cefb9d5bdcff169f12f7506273457363bec327c6b7.

# Pre-registration: sensitivity test for the candidate coordinates (before computing the grid)

Date and time of this file: recorded by the file system when it was written, before any new run of this grid.

Note: the results of the original models A to D were known before this registration (they were reproduced byte for byte). This registration defines the rules of the new grid only.

## 1. The question tested

The question is not "where is the real site?". The question is: **do the candidate coordinates (37.929792 N, 122.150318 W) recur across the conventions that the paper itself states, or that the calculations require? And what do they depend on?**

The candidate coordinates do not appear in the audit archive. The closest point in it is model A (37.92961, -122.15045). The difference between them is about 23 metres, and it will be computed to the same precision.

## 2. Fixed inputs (from the archive, verified)

- Crosshair centre on the image: (490, 454) pixels. Source: `results/map_crosshair_and_rings.csv`.
- Pixels per ring unit: 25.589. Same source file.
- Mount Diablo (NAD27, from Foxon table 2): 37.881774 N, 121.913085 W.
- The five cities, by their centre coordinates (Wikipedia) and by the positions of their labels on the image: from `data/landmarks.csv`.
- Verification of two aspects of the figure: the eight points drawn on figure 2 match, by calculation, the positions of the eight conventions. (See `docs/AUDIT_REPORT.md`, which did not mention them; this was checked here.)

## 3. Factors and their levels (and the classification of each level)

| Factor | Levels | Classification |
|---|---|---|
| F1 reference direction for the angle | E-CCW, E-CW, N-CCW, N-CW, W-CCW, W-CW, S-CCW, S-CW | **Drawn in figure 2** (the paper says "for all Reference Axes and Directions") |
| F2 minute rounding | round (⌊·⌉ as in the paper), floor (alternative) | round **stated in the paper**; floor is a computational alternative only |
| F3 scale (miles per unit) | S_A = 1.162, S_B = 1.0904, S_C = 1.088, S_D = 1.0179 (from calibration); S_G = 5.74 (inferred from "SF is about five inches" at 28.7 miles); S_L = 6.4 (from an unsourced secondary source) | Calibration: **assumption** that one circle unit equals the printed inch. S_G and S_L: **unverified secondary sources**, cited here to test the contradiction, not to adopt them |
| F4 map rotation from true north | ρ = calibration angle (for models A to D), or ρ = 0 (map oriented to north) | ρ = 0 **a reasonable assumption** (road maps are usually north-oriented); calibrated ρ **results from points that do not match exactly** |
| F5 origin of the coordinates (pole) | crosshair centre (with calibrated offset), or the summit of Diablo at the centre | the paper says the pole is **Mount Diablo** |
| F6 calibration set | all five; or four, without Oakland; or deleting one city (leave-one-out on model A) | sensitivity |

## 4. The grid (all configurations are computed and shown; none is selected)

- G1: models A to D × F1 (8) × F2 (2) = 64 configurations. Rotation and pole as in each model.
- G2: two fixed scales (S_G, S_L) × ρ (ρ = 0 and ρ = ρ_A) × F1 (8) × F2 (2) = 64 configurations. Pole = summit of Diablo at the centre.
- G3: model A with one city deleted each time (5 sets) × F1 (8) × F2 (2) = 80 configurations.
- Total: 208 configurations.

## 5. Quantities computed for each configuration

- Predicted coordinates of the point (r = 12, θ = 3 radians, using the rounded minute).
- Geodesic distance to the candidate coordinates (miles).
- Distance from Mount Diablo (should be approximately 12 × the scale).
- Whether the point falls inside the frame of figure 2 when translated with model A's transformation. (An internal consistency test, not a decision.)

## 6. Decision rules (fixed before running)

- R1 (match): a configuration is "compatible with the candidate" if the distance is at most 1.0 mile. This bound is set here, not chosen after seeing the results. (It is consistent with a 95 % radius of about 1.4 miles for model A.)
- R2 (dependence): the candidate is said to **depend on F1** if the match is confined to one level of F1. It is said to **depend on F3** if no configuration using a scale inferred from a secondary source matches.
- R3 (conditional refutation): if no configuration with scale S_G or S_L matches the candidate (within 1.0 mile), the candidate is **refuted, provided those scales are correct**. This refutation is **not final**, because S_G and S_L come from secondary sources.
- R4 (no selection): no configuration is chosen "because it is the closest". All results are shown.
- R5 (limits): no real location is inferred from the grid, nor the correct map edition, nor the correct scale, nor the meaning of any phrase.

## 7. Predictions recorded before the run (to evaluate the test itself)

- P1: with the calibration scale (S_A to S_D), at most one of the eight directions matches the candidate, namely E-CCW (the drawn circle). (Expected from the geometry of eight widely spaced points.)
- P2: with S_G or S_L, no configuration matches the candidate within 1.0 mile. (The distance from Diablo is 69 to 77 miles, while the candidate lies about 13 miles away.)
- P3: changing F2 from round to floor changes the minute from 3 to 2, and changes the location by more than 1.0 mile.
- P4: models A to D reproduce the computed points in `map_audit_models.csv` byte for byte (a check before the grid).

## 8. What this grid cannot establish

- It does not prove that the coordinates are correct, nor that a solution exists.
- It does not settle the scale, because the true scale requires a measurement on the printed map (T1 in the audit report).
- It cannot choose the edition (1968 or 1969), because no data exists for any edition other than the available image.

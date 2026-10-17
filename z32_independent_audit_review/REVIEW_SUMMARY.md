> Translated from Arabic into English. The Arabic original is kept in the research workspace; its SHA-256 is 576344695857fab58d3e569bedd0bd711889106a35767527bcdfd66cfa805e8c.

# Independent review of the z32_independent_audit archive

## 1. What the archive contains

- 89 files, and all SHA-256 fingerprints match (77/77).
- The reference paper (Foxon 2023) is byte-identical to the uploaded file.
- The original processing pipeline was re-run successfully; 10 result files match the saved copy byte for byte.
- The audit scripts audit_01 to audit_11 run, and their outputs are consistent with the report.

## 2. What the audit actually establishes

- Re-implementation match for the transposition family: 204/204.
- The exact calculation of the probability matches the simulation (45.296 versus 45.266).
- Map model A is reproduced accurately (37.92961, -122.15045).

## 3. What only checks calculations or code

- The circular checks in transposition_family.py (is_permutation and moves_alternate_rows) prove nothing. The real check is the second implementation.
- Numbers recomputed by calculation do not mean that the assumptions are correct.

## 4. What remains a historical assumption

- The edition of the map (1968 or 1969): there is no primary evidence in the archive. The claims that exist come from people who own copies, or from publications, and have not been verified.
- The actual scale of the map: the archive estimates 1.16 miles per unit from the figure itself, not from the printed map.
- The meaning of the unit "inch": the rings (4, 8, 12) are an overlay by Foxon, not a printed scale.
- The 16.9° declination is a calculated IGRF model, not a historical measurement.

## 5. The candidate coordinates 37.929792, -122.150318

- They match model A within 0.01 miles (about 23 m). The number sent does not appear exactly in the archive's outputs.
- Model A allows a free offset of the pole by 2.67 miles from the crosshair intersection, whereas Foxon's paper assumes the pole is Mount Diablo. Model C (fixed pole) places the point 1.88 miles away.
- Of 72 natural conventions (reference angle × direction × declination × scale × rounding), no point lies within 0.5 miles of the candidate coordinates. The nearest point is 1.5 miles away.
- Scale: 12 units × 1.16 ≈ 13.9 miles. If the unit is a printed inch at a scale of 6.4 miles per inch, the distance becomes about 77 miles. Grinell's test (San Francisco about five inches away) gives about 5.7 miles per inch.
- Figure 2 of the paper draws (12,3) with all the reference conventions and directions (8 marks). The open circle near Orinda represents the convention that the archive uses. The numerically calibrated point is about 7 miles from the approximate position of Orinda. Those coordinates are approximate, from general knowledge, not from the archive.
- The real uncertainty range is wider than the ±1.4 miles stated in the report: removing one city moves the point to 5.6 miles, and changing the scale of the pairs within its range moves it 0.9 to 5.5 miles.

## 6. Verdict

- No independent evidence supports the candidate coordinates. The existing evidence concerns the encrypted sequence, not the location.
- The coordinates result from calibration choices (pole offset, estimated scale, rotation, convention) that were not fixed in advance.
- The existing evidence weakens this point rather than supporting it: the fixed-pole model places it about 1.9 miles away, and a plausible real map scale places it tens of miles away.

## 7. Tests that distinguish the correct hypothesis from the effect of settings

1. Measure the distance between Mount Diablo and San Francisco on the original printed map (or on a high-resolution copy with its scale bar). If it is five inches, the scale is about 5.7 miles per inch and the candidate point falls. If it is about 25 inches, the archive's scale is supported.
2. Determine whether rings 4, 8 and 12 exist on the original map, or were added by Foxon.
3. Fix the pole rule (Diablo), the reference angle, the direction, the declination and the rounding before running, and record the result for all 72 conventions, rather than choosing one.
4. Verify the map edition from an image of the margin (the printing number) of a physical copy.
5. Test Grinell's claim (five inches) on the same map before any calibration.

## 8. What was not examined in this review

- I did not obtain the original map or an image of its margin. The whole analysis depends on Foxon's redrawing.
- I did not verify the coordinates of Orinda Village from a source in the archive. The number used is approximate.
- I did not independently recheck all the statistical audit results. I checked the summary numbers and the match of the re-run.

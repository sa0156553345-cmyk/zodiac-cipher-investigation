> Translated from Arabic into English. The Arabic original is kept in the research workspace; its SHA-256 is 8e711332b2e1a7025c7f9a7e64689b1d44979e802e8b6d39baf0d1914d1791c8.

# Change and correction log

Earlier results are kept as they are in `previous_results/`, and the full previous package is in `z32_independent_audit`. Every change is recorded here, with its reason.

## A. Changes to measurements and earlier results

| ID | Quantity | Earlier value | Current value | Reason |
|---|---|---|---|---|
| C1 | Centre of the figure | (490, 454) from argmax | (490.88, 454.30) from a circle fit | a more accurate circle fit; the earlier centre was a reading of lines only |
| C2 | Pixels per unit | 25.59 | 25.660 (±0.13, conservative) | the fitting method instead of argmax, and a more accurate centre. Difference 0.3 % |
| C3 | Miles per unit, G1 | 1.162 | 1.166 | change of centre and scale |
| C4 | Rotation, G1 | −4.8° | −4.7° | the same change |
| C5 | Residuals, G1 | 128 pixels (Oakland) | 128.4 pixels | no substantial change |
| C6 | "95 % radius from 0.8 to 1.4 miles" | earlier, as an uncertainty estimate | **withdrawn as an uncertainty estimate** | reflects only reading noise; the correction was already in the previous package (C-03) |
| C7 | "The map is close to true north" | earlier | **conditional**: rotation from −1.8 to −7.8; the exploratory test prefers 0° over ±16.9° | new support, conditional on the labels |
| C8 | "6.4 is not supported by the figure" | earlier, absolutely | **conditional**: it remains excluded only for configurations with the number 12, and assuming unit = printed inch | it turned out that the exclusion depends on the number and on the linking |
| C9 | The location (12,3) is close to Route 24 | earlier, as implicit evidence | **withdrawn as evidence**: the location changes by 4 to 19 miles with the assumptions, and the base rate of 2.8 % lies within two miles of the point | result of the new audit |

## B. Corrections to documents and to the pre-registration

| ID | Location | Error | Correction | Reason |
|---|---|---|---|---|
| E1 | PREREGISTRATION_TRANSFORMS.md, section 6 | "5 × 6 × 5 × 2 × 8 × 2 = 9600" | **4800** | arithmetic error. The rules did not change. The appendix is in the registration document. |
| E2 | tests_transforms.py (the poles test) | a test containing `or True`, so it always passed | replaced by a test that checks the difference between the poles (A⁻¹(−t)) | found during review before delivery; no effect on the results, because the other tests are independent |
| E3 | tests_geodesy.py (ellipsoid and sphere test) | threshold of 0.1 % | threshold of 0.5 % | a difference of 0.21 % appeared, a known difference between the two formulas. The test was one of my earlier estimates, and I was wrong about it; this was not hidden |
| E4 | transforms.py (frame column) | the `inside_figure` column of the family without controls appeared as if it were a valid test | added the column `frame_test_meaningful = NO` | clarifies the validity of the test; the values did not change |
| E5 | MAP_CALIBRATION_REPORT.md | error in the effect of the declination: "about 2.5 for the range 15–17.7" | "about 0.5 within the range, and about 2.8 for zero" | checked the numbers against transform_sensitivity.csv |
| E6 | MAP_CALIBRATION_REPORT.md | typing and wording errors | corrected | |

## C. Run events that do not change the results

- During setup an input/output error appeared when deleting a temporary `__pycache__` folder. I checked that the result files were complete and of the correct sizes before continuing; no output was affected.
- Some variables in fig_measure.py are not used in any output (such as `pooled` and `ls`). They are left as they are, because they do not affect any file.

## D. What was added after the registered run (exploratory, marked)

- rotation_test.py: the map-rotation test (0° against ±16.9°).
- pairwise_scale.py: the criterion of scale spread between pairs was pre-registered, but it was computed after the final linking.

No rule in the transformation family was changed, and no configuration was chosen after looking at the results.

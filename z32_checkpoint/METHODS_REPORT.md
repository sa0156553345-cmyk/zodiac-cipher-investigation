> Translated from Arabic into English. The Arabic original is kept in the research workspace; its SHA-256 is 13b75fc9a7b7ce9885ea2adcd51c2e7b2cd631e6fd72385a7884a76c1043eafe.

# Method-improvement report (pre-registered experiment)

## 1. Data validation (VALIDATION_LOG.md)

- The grid has 340 cells. The key has 63 glyphs (the count of each letter matches the visual count). The transposition is a complete permutation of 0 to 339. Section 1 agrees with the mathematical formula in 153 of 153 cells. Section 2 differs in 62 cells, which the corrections to figure 43 stated in the paper explain; these cannot be checked independently.
- The reference text has 340 letters, matching the number of symbols, with the misspellings of the paper kept.
- Reading direction: cell k = 1 and cell k = 2 agree visually, and cell k = 0 fails in the automatic matching.

## 2. Matching diagnosis: six methods defined in advance

| Method | Tuning accuracy | Validation accuracy (k ≥ 170) | 95 % interval, validation | All |
|---|---|---|---|---|
| M0 baseline: skeleton r = 2 + dilation + rotation 0 | 0.624 | 0.594 | 0.519–0.665 | 0.609 |
| M1 without skeleton (direct mask) + rotation 0 | 0.659 | 0.671 | 0.597–0.737 | 0.665 |
| M2 skeleton r = 1 | 0.565 | 0.565 | 0.490–0.637 | 0.565 |
| M3 average of M0 and M1 | 0.688 | 0.688 | 0.615–0.753 | 0.688 |
| M4 M0 + rotation search ±6° | 0.653 | 0.629 | 0.555–0.698 | 0.641 |
| M5 M1 + rotation search ±6° [selected in advance] | 0.735 | 0.682 | 0.609–0.748 | 0.709 |

- M0 matches the results of v4 exactly (zero differences in the first choice). This is the check that the experiment is sound.
- The skeleton with dilation r = 1 (M2) is clearly worse than r = 2, meaning the method is sensitive to the details of the skeleton.
- Removing the skeleton (M1) improves accuracy on the validation set from 0.594 to 0.671: the skeleton loses information about the filled areas.
- The rotation search improves both bases (M4 against M0, and M5 against M1), but not equally.

## 3. Validation set and selection

- The selection registered in advance (highest accuracy on tuning) is **M5**, with tuning accuracy 0.735.
- M5's accuracy on the independent validation set (170 positions, k = 170 to 339) is **0.682**, which is below the 70 % target. The 95 % interval is 0.609 to 0.748, so the result neither excludes nor confirms 70 %.
- M3 scored 0.688 on validation but was not selected, because the registered rule selects on tuning only, and the validation difference between them (0.006) lies within the margin of error. The selection must not be changed after seeing this result.

## 4. Error analysis (M5, validation set, 54 errors out of 170)

- The errors are spread out: the most frequent confusion pairs have only two cases each, so there is no single clear systematic confusion.
- Rank of the correct letter among the errors: ranked 2 to 5 in 29 cases, 6 to 10 in 11, and above 10 in 14. In other words, the correct symbol was among the top five in more than half of the errors.
- The margin (confidence) is lower on average for errors than for correct cases (see the log). The margin is a weak indicator, but not useless.

## 5. Verdict

- The main result as it stands: the method selected in advance reaches 68.2 % on the validation sample, below 70 %. No manual adjustment was made to improve the figure.
- What can be relied on: rotation is one cause of error, and removing the skeleton improves performance. The result cannot be attributed entirely to a single cause.
- What this does not establish: it does not establish that the solution is complete, nor that the method is correct. No position in the validation set was visually reviewed.

## 6. Files and commands

- PREREG_METHODS.md (pre-registration), VALIDATION_LOG.md (data validation), methods_experiment.py (the experiment), methods_results.json, methods_top1_ids.json, methods_scores.npz, methods_diagnostics.json, M5_top5_all340.csv.
- Re-running: `python3 methods_experiment.py` (requires match_v4.py and the files in the folder; takes about 3.5 minutes).

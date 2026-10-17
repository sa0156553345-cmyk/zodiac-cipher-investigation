> Translated from Arabic into English. The Arabic original is kept in the research workspace; its SHA-256 is 42966cb7cf42e81557a2c6397320c91eb1175f0eac668e39a9bddc9b0e83c640.

# Corrections log (CORRECTIONS_LOG)

Each entry states the earlier statement, the new status, the reason, and the evidence. The original results are kept unchanged in `original_results/` and `original_docs/`.

| # | Earlier location | What was written earlier | Status | Reason and evidence |
|---|---|---|---|---|
| C-01 | README §5.4, CLASSIFICATION | "The scale ... is not consistent with 6.4 miles" | **Downgraded to inferred, under an assumption** | Depends on Foxon's circles representing the inch of the original map, which is not documented. Evidence: `audit_06`, and Foxon's implicit scale. |
| C-02 | README §5.4 and §8 | "The positions of their names were read by hand (±6 pixels)... i.e. about 0.3 miles" | **Corrected** | ±6 pixels is only a reading error. The actual error of the labels reaches about 8 miles (San Leandro). Evidence: `audit_06`. |
| C-03 | README §5.4, CLASSIFICATION | "95% radius inside each model 0.8–1.4 miles" | **Withdrawn as an estimate of uncertainty** | It reflects only 6-pixel noise and 1-mile noise. At 3 miles it becomes 4.0 miles. Evidence: `audit_07`. |
| C-04 | README §5.4, SOLUTION_CRITERIA C8 | "The location (12,3) is 0.25–2.8 miles from the Route 24 point" | **Corrected** | The number is right as a calculation, but closeness to Route 24 depends on the rounding (3 or 2), which moves the location 12–13 miles. Evidence: `audit_11`. It is not evidence. |
| C-05 | README §5.4 | "The map is close to true north (declination −2° to −5°)" | **Withdrawn** | The direction difference between pairs has median 4.3°, a range from −11° to +72°, and the MC interval for model C crosses zero. Evidence: `audit_06`, `audit_07`. |
| C-06 | PREREGISTRATION (map) | "The four map variants ... fixed now" | **Corrected** | Models B and D were created after seeing the residuals for Oakland (128 pixels). All deletions are now shown equally. Evidence: `audit_07`. |
| C-07 | PREREGISTRATION (family) | "Templates (A, B, C)" | **Corrected** | Template C produces no 32-letter phrase (the maximum is 30). The actual family is A and B; the number 3544 did not change. Evidence: `audit_03`, `audit_09`. |
| C-08 | README §5.3, CLASSIFICATION | "p (family level) = 0.417, i.e. no excess" | **Kept and qualified** | The value is correct for what it measures (the exact calculation matches), but the null model is not suitable and hides the heterogeneity of the orders. "No excess" is not acceptable as a conclusion. Evidence: `audit_03`, `audit_04`, `audit_10`. |
| C-09 | README §5.3, CLASSIFICATION | "47 phrases succeed in one order ... expected by chance" | **Corrected** | 34 of the 47 come from orders k7 and k14, which contain pairs that match structurally because of the templates. Evidence: `audit_04`, `audit_10`. |
| C-10 | README §5.1, CLASSIFICATION | "34 valid readings out of 204" | **Corrected** | Only 2 of the 34 match the figure's layout (B), and both need rule E2, which is not stated. Evidence: `audit_02`. |
| C-11 | README §5.1 | "E2 is a rule with two options" | **Kept** | The skip is structurally necessary (all 34 orders skip at least one empty cell), but its specific interpretation (an extra move) is a choice. Evidence: `audit_02`. |
| C-12 | README §4 (transposition_family) | "checks that every valid order visits the 32 symbols once" | **Corrected** | The two checks are circular given the algorithm's definition. The real independent check is a second implementation that matches 204/204. Evidence: `audit_02`. |
| C-13 | CLASSIFICATION (directly supported) | "no visual reading needed for identities" | **Qualified** | The categories are determined by pixels, but the category names come from visual reading. The binary test requires the names only for display, while the structure depends on the categories. Evidence: `audit_08`. |
| C-14 | README §8 | "The test is not blind: I saw figure (C) before designing the family" | **Expanded** | Added that the word lists were chosen while T1 and T2 were already known; that E2 was added after E1 failed; and that δ was inferred from (C). Evidence: `audit_09`, `transposition_family.py`. |
| C-15 | README §8 | "The coordinates come from Wikipedia (city centres)" | **Qualified** | These are city centres, not the label positions, and the relation between them was not handled. Evidence: `audit_06`. |
| C-16 | SOLUTION_CRITERIA C9 | 0.5 mile threshold as a discrimination criterion | **Kept as a proposal, with a note** | Current models fail it (radius 1.4 to 4.4 miles). The criterion is not changed. |
| C-17 | Power assessment (not mentioned earlier) | Not examined | **Added** | The statistic does not change when symbol names are swapped, and the threshold p < 0.05 needs 58 successes. Evidence: `audit_05`. |
| C-18 | Circular test in the code | Not mentioned earlier | **Added** | `transposition_family.py` contains circular checks, and they were identified. |

## What was not changed

- T1, T2, T3 and T4 as they are. They have not been modified after seeing the results.
- The transposition rules in transposition_family.py as they are.
- All original results are kept byte for byte in `original_results/`.

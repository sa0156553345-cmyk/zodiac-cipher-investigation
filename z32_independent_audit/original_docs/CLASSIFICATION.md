# Classification of the results

Categories: **supported directly by the data** (reproducible from files in this package with no added assumption beyond the measurement itself);
**inferred with assumptions** (depends on a listed assumption); **undetermined** (cannot be decided with the data available).
No probability that any solution is correct is given, because no model for that probability is justified by the data.

## Supported directly by the data
| Result | Evidence file | Note |
|---|---|---|
| 29 identity classes in Fig.1(A); repeats at {1,26}, {2,32}, {6,14} | results/fig_glyph_check.csv | bitmap comparison, no visual reading needed for identities |
| Fig.1(B) top row identical to Fig.1(A) | run_log.txt | bitmap, max mismatch 0 |
| Fig.1(C) reading by bitmap = CX2VAC7PGID4H6?TJF3!5LR118O9MEOW | results/fig_glyph_check.csv | bitmap |
| 34 valid readings out of 204 configurations; all are W1 with the E2 rule | results/transposition_all_configs.csv | counts from code |
| Literal T1: 0 of 34 orders satisfy all 3 pairs; paper order: 1 of 3 pairs | results/literal_phrase_test.csv | no edits |
| T2 and T3 literal: 0 of 34 orders | results/literal_phrase_test.csv | no edits |
| T4 (Foxon text) satisfies 3 of 3 only after edits at positions 6 and 31 | results/literal_phrase_test.csv | the two edits are exactly the violated pairs in T1 |
| Alternative family: 47 phrases pass in exactly one order each; family-wide excess not significant | results/alternatives_summary.csv, results/alternatives_candidates.csv | global p = 0.417 |

## Inferred with assumptions
| Result | Assumption(s) | Evidence file |
|---|---|---|
| Fig.1(C) is reproduced (32 of 32) by k=2, delta=+2, W1, E2 | E2 (skip an empty cell) is not stated in the paper; delta=+2 is inferred from Fig.1(C) itself | results/transposition_assumption_effects.csv |
| Map scale 1.02-1.16 miles per figure unit (point estimates); Monte Carlo 95% about 0.97-1.24 | sourced city-centre coordinates; label centres read by hand (+-6 px); similarity fit; the crosshair origin | results/map_audit_models.csv |
| The map's north is within about 2-5 degrees of true north | same as above; across the four variants the Monte Carlo intervals span about -8.7 to +0.9 degrees | results/map_audit_models.csv |
| The claimed scale 6.4 miles per inch is not supported by the figure | fitted px/mile is 22-25, while 6.4 would need 4.0 px/mile; assumes the sourced coordinates and label positions are correct | results/map_audit_models.csv |
| Predicted (12,3) lies about 0.2 to 2.8 miles from the sourced Highway 24 point | depends on the model variant | results/map_audit_models.csv |

## Undetermined
| Question | Why undetermined |
|---|---|
| Exact location of (12,3) | 95% model radius 0.8-1.4 miles, and model variants differ by up to 2.8 miles; many roads, schools and stations lie in that area |
| Grinell's "San Francisco at five inches" | no sourced coordinate for San Francisco in this package; not tested |
| Meaning of any phrase, and the meaning of "#" | the repeat test checks consistency only; the symbol identities are those of a typeset ASCII figure, not the original Zodiac symbols |
| The homophonic key | unknown; only three repeats are constrained |
| The magnetic declination actually applied by the author in 1970 | the paper uses a model value (16.9 deg), not a measurement; the map itself is near true north |
| Any solution outside the declared transposition and phrase families | not tested |

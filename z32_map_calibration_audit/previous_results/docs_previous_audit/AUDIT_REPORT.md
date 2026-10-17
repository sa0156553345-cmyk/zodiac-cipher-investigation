> Translated from Arabic into English. The Arabic original is kept in the research workspace; its SHA-256 is ee7902afcdfa3c8125f17593a813bb84722b13b8a43a9936dd74e88be517ac16.

# Independent audit report on the Z32 results

## 0. Verdict

**Category: confirmed errors or methodological problems.**

No computational error was found that changes the main numbers. The independent re-implementation of the transposition family matched (204 of 204); no contradiction was found in the constraint check (0 contradictions across 34 orders); and the exact formula for the probability matched the simulation. The real problems are methodological:

1. **The statistical test cannot support the conclusion "there is no signal".** The null permutation model destroys the positional structure of the family. The overall result (p = 0.417) balances only because two large deviations in two specific orders offset the deviations of the other orders. The test also cannot distinguish a single correct solution, even if one lies inside the family.
2. **The uncertainty of the map calibration is underestimated.** The printed city labels do not always lie on the city centres (for example, San Leandro is about 8 miles from its expected position), and the manual reading error of ±6 pixels does not represent the actual error.
3. **Closeness to Route 24 depends on the rounding choice in the minute calculation** (round or floor). This choice is not justified by the text of the paper. Changing the rounding moves the predicted location by about 12 to 13 miles.
4. **Some documentation and pre-registration rules are imprecise** (see the corrections log). Template C is empty; models B and D were chosen after seeing Oakland's residuals; E2 was added after E1 failed; and "34 valid readings" includes 32 that do not match the layout of figure (B).

## 1. Scope and method

- The original processing pipeline was re-run inside this package, and its results are **byte-identical** to the earlier results (see `run_log.txt`).
- Independent audit scripts were written (`scripts/audit/audit_01` to `audit_11`). They do not import the original pipeline functions, except where stated.
- The hypothesis T1 and the transposition rules were not changed after seeing the results. The only changes are documentary corrections, recorded in `CORRECTIONS_LOG.md`.

## 2. Review of the four scripts

### 2.1 transposition_family.py

| Item | Type | Detail | Effect | Action in the audit |
|---|---|---|---|---|
| `is_permutation` and `moves_alternate_rows` checks | circular check | the algorithm prevents repeated cells and alternates the row at each move by definition, so the two checks are guaranteed and prove nothing | no independent check comes from them | `audit_02`: a second, independent implementation; 204/204 agreement |
| restriction of the direction δ to a fixed sign | unjustified assumption | the text says "moves of the knight piece" and does not require a fixed sign; at least 2³¹ sign sequences were ignored | the family of 34 is narrower than the text allows | no new alternative was added after seeing the results; registering one in advance is recommended |
| 34 "valid readings" out of 204 | misleading presentation | only 2 of the 34 match the layout of figure (B) (k = 2); the other 32 change the shift | the number 34 looks wider than the actual evidence | `audit_02` and `audit_04`: separate analysis of the two orders consistent with the figure |
| skip rule E2 | added after the fact | added after E1 failed on figure (C) | the reproduction of (C) depends on it | structural analysis: the 17 + 15 layers with alternating rows force skips (every one of the 34 orders has at least one skip) |
| how the skip is done | choice | E2 skips the cell and completes the move with an extra move; other interpretations exist and are not recorded | the result could differ under another interpretation | no new alternative was tested; it should be registered in advance |
| matching with (C) | reproduction, not discovery | the family was designed after seeing (C), so the 32/32 match is not an independent test | it shows only that a specific rule produces the sequence | stated explicitly in the report |
| `C_OUT` derived from pixel matching | sound | the reading does not depend on a visual reading of the symbols in the order | — | — |

### 2.2 literal_phrase_test.py

- No programming error was found. Verified by the independent implementation (`audit_01`): 34 orders, 0 contradictions with `literal_phrase_test.csv`.
- Basic assumption: a homophonic model with the triple constraint only (each repeated symbol carries the same letter in its two positions). It does not handle gaps, nulls or word symbols. This is an acceptable assumption, but it must be stated.
- The result "T1 does not appear": correct **within** the specific family of orders, and it does not exclude an order outside that family.
- Labelling: T4 carries two declared modifications, and this is transparent in the file.

### 2.3 alternatives_family.py

| Item | Type | Detail | Effect |
|---|---|---|---|
| template C | specification error | the maximum length possible for template C is 30 letters, so it produces no phrase of 32. The pre-registration mentions three templates | the actual family consists of two templates (A and B); the number 3544 did not change |
| word lists | bias in the specification | the number and unit words were chosen after T1 and T2 were known, and both lie within the family by design | the family is not a neutral sample of reasonable texts; it contains phrases proposed in advance |
| the within-phrase permutation null model | unsuitable for the purpose | it preserves letter frequencies and breaks the positional structure, while the positional structure of the family is strong | the conclusion "no excess" is not justified |
| total over 34 orders | masks heterogeneity | orders k7 and k14 give 21 and 13 successes against an expected 1.33 each, and the rest are below expectation | the overall balance results from compensation, not from the absence of a signal |
| test at the phrase level | weak power | `audit_05` shows that the statistic does not change when symbol names are swapped, and that one solution adds at most +1 to the count of the family of orders | the test cannot detect a single solution |
| Bonferroni correction | insufficient | corrects only for the number of phrases, not for the number of sub-orders or the number of design paths (templates, lists, E2) | the adjusted p-value is optimistic |
| resolution R = 2000 | acceptable | p-value resolution 0.0005; the overall result 0.417 with a standard error of about 0.011 | — |

### 2.4 map_audit.py

| Item | Type | Detail | Effect | Action |
|---|---|---|---|---|
| city labels treated as centres | wrong assumption | the source coordinates are city centres (Wikipedia), while the reading of a printed label position does not equal the centre. San Leandro lies west of Oakland in the image, while geographically it is east of Oakland | the Oakland–San Leandro pair gives a direction difference of 72° | `audit_06` (the 15 pairs) |
| ±6-pixel uncertainty | assumed, not measured | the actual residuals of the fit range between 46 and 133 pixels | the Monte Carlo intervals are misleadingly narrow | `audit_07`: sensitivity to σ up to 30 pixels and 3 miles |
| similarity model | insufficient | it assumes one scale, a rotation and an offset; the data do not fit that | systematic residuals | addition of the pairwise analysis (`audit_06`) |
| models B and D | decision after looking at the data | Oakland was dropped after its residual (128 pixels) was seen | B and D show an artificial improvement | `audit_07` shows the deletion of each city, equally |
| coordinate pole | convention defined late | the free model takes the crosshair as the pole; the fixed model takes the summit of Diablo | a difference of about two miles between models A and C | stated explicitly |
| rounding rule in the minute | unjustified | round gives 3 and floor gives 2; the text justifies neither | the location moves 12 to 13 miles | `audit_11` |
| Route 24 point as a reference point | not a location | a coordinate from a commercial site that converts a route name; not the location of an event | cannot serve as evidence | classified as undetermined |
| local projection | acceptable | equirectangular around Diablo within about 25 miles; error less than 0.5 % | — | — |
| detection of the crosshair and rings | acceptable | argmax of dark lines and ring scanning; results reproduced | — | — |

## 3. Audit of the statistical test (3544 phrases, p = 0.417)

### 3.1 How the 3544 phrases were built

- Template A: `N1 U1 ALONG THE N2 U2`. Template B: `N1 U1 AND N2 U2 ALONG`. Template C: `N1 U1 N2 U2`.
- N (17 number words) × U (8 units) × N × U = 18,496 combinations per template, then filtering for lengths of exactly 32 letters.
- Results (`audit_03`): template A produces 1772 combinations, template B produces 1772, and template C produces **zero** (maximum 30). No phrase is shared between the two templates, giving the total of 3544.

### 3.2 How p = 0.417 was computed

- Statistic: O = the number of pairs (phrase, order) that satisfy all three constraints. The observed value is 47.
- Null model: for each phrase, 2000 random permutations of its own letters. The total number of successes in each permutation gives a distribution, and p is the proportion of permutations whose total equals 47 or more.
- The null mean is 45.27 and the standard deviation is 6.81, giving p ≈ 0.417. The exact calculation matched (`audit_03`): exact expectation 45.296, against the simulation 45.266.
- **Conclusion: the calculation is correct for what it measures.**

### 3.3 Does the null model preserve the important data?

- It preserves **letter frequencies** only. It does not preserve the **positional structure** generated by the templates.
- The evidence (`audit_10`): the match rate of each pair of positions within the family differs from the composition expectation by factors from 0.14 to 3.88. 47 pairs out of 496 have a rate above 2, and 125 pairs have a rate below 0.5.
- The pair (27, 31), which appears in the same original order, matches at a rate of 0.151 against 0.074 under composition (a ratio of 2.0), because unit words such as DEGREES repeat E in two nearly adjacent positions.
- **Result: the null model is not suitable for the purpose, because the positional deviation of the family is very large.**

### 3.4 Deviation by order, and compensation

| Order | Observed successes | Expected (composition) | Excess |
|---|---|---|---|
| k7_d2_W1_E2 | 21 | 1.33 | +19.7 |
| k14_d2_W1_E2 | 13 | 1.33 | +11.7 |
| remaining 32 orders | 13 (total) | 42.63 | −29.6 |
| **Total** | **47** | **45.30** | **+1.7** |

- The excess in the two orders (+31.3) is cancelled by the deficit in the remaining orders (−29.6).
- 34 of the 47 "candidates" come only from these two orders (`audit_04`). That is, the list of candidates is mostly the result of the structure of the two orders and of the phrase templates, not of the structure of the cipher.

### 3.5 Is the result valid for the intended conclusion?

- **No.** The intended conclusion was "no signal exceeds chance". The test does not support it, for two reasons: the null model is not suitable, and the pooled statistic hides large deviations.
- Even if the model were correct, this statistic could not distinguish a single solution. Any solution inside the family adds only one phrase, and the threshold p < 0.05 requires 58 successes, which is 11 more than the observed value (`audit_05`).
- **What can be said:** the family produces a large number of phrases that are structurally compatible, and most of them result from the structure of the templates. This neither supports nor excludes a solution.

### 3.6 Diagnostic proposal (not used to produce a conclusion)

Any alternative test needs a null model that **preserves the template structure** (for example, replacing words by words of the same length within the same template), registered in advance before running. It was not run here, because choosing it after seeing the results would repeat the same problem.

## 4. Audit of the transposition rules

| Rule | Source | Status |
|---|---|---|
| shift by 2 (k = 2) | Foxon, text 4.3 | **stated** |
| knight pattern and start (1,1) | Foxon, text 4.3 (and Z340) | **stated** |
| wrap on the same row | "loop back on the opposite side of the same row" | **interpretation** (W1 among three) |
| direction of the first move (2,3) | inferred from figure (C) itself | **inferred from the output** |
| skipping the empty cell (E2) | not stated | **added**, but **structurally necessary**, because the 17 + 15 layers with alternating rows cannot be covered without a skip (`audit_02`) |
| fixed sign of δ | not stated | **added** (a restriction) |
| exact meaning of E2 (an extra move) | not stated | **a choice** among possible interpretations |

- **Are the 34 orders chosen independently of (C)?** No. E2 was added after the failure on (C), δ = +2 is inferred from it, and the family was designed after seeing it.
- **Can the orders be considered an independent test?** No. They establish that (C) is reproducible by a specific rule, which is important, but they are not a confirmation of the cipher's correctness or of any phrase.
- **What does the 32/32 match prove?** That (C) itself results from a specific deterministic reading: shift 2, skipping of empty cells, and alternation of rows. The authors probably used a procedure of this kind.

## 5. Audit of the map

### 5.1 Coordinate sources

| Coordinate | Source | Status |
|---|---|---|
| Mount Diablo (NAD27) | Foxon, table 2 | primary (from the paper) |
| centres of Oakland, San Leandro, Hayward, Livermore, Vallejo | Wikipedia (city-centre coordinates) | reliable secondary source, but **not the printed label position** |
| Vallejo (another source) | latlong.net differs by about one mile | recorded as uncertainty |
| Route 24 point | commercial website converting a route name | **not valid as a location** |

### 5.2 Choosing the city positions from the image

- The label centres were read by eye, with the help of a pixel grid, with no automatic method and no independent check. The assumed error of ±6 pixels has not been measured.
- Labels are not necessarily city centres. Measured examples: San Leandro (its label is west of Oakland), and direction differences between pairs of 72°, 41° and 15.5°.

### 5.3 Residuals and transformation

- Four models (A to D) give a scale between 1.02 and 1.16 miles per unit, but the residuals range from 15 to 133 pixels. The similarity transformation does not fit the data.
- The 15 pairs (`audit_06`): 15.6 to 29.7 pixels per mile, a spread of about a factor of two, with no clear relationship to distance (correlation −0.10).
- Result: **no single scale is supported by this image better than roughly ±30 %.** The median of 1.09 miles per unit is the middle value, but its real interval is wide.

### 5.4 Sensitivity of the predicted location

| Test | Result |
|---|---|
| deleting one city (A, free offset) | the location varies from 2.2 to 5.6 miles from the Route 24 point |
| deleting one city (C, fixed pole) | the location varies from 0.25 to 1.8 miles |
| noise of 6 pixels and 1 mile | 95 % radius = 1.4 miles |
| noise of 6 pixels and 3 miles | 95 % radius = 4.0 miles |
| noise of 30 pixels and 3 miles | 95 % radius = 4.4 miles |
| rounding 3 against 2 | the two locations are 11.7 to 13.4 miles apart |

**Conclusion:** the current processing does not determine a location to better than a few miles. Therefore no closeness to Route 24 can be treated as evidence, which agrees with the view that it is not evidence.

### 5.5 Is the magnetic declination applied?

- In Foxon's approach, the declination is used only to extract the numbers 12 and 3, and the map is not rotated. Therefore the geographic transformation of the point (12, 3) does not need an extra rotation. But **the value of the minute itself** (3 or 2) depends on the rounding rule, which the text does not justify.

## 6. Reproducible tests that another researcher can run

Each test registers its criterion before running. What follows are recommendations, which were not executed in this package.

| # | Test | What supports the hypothesis | What weakens it |
|---|---|---|---|
| T1 | **Scale of the original map:** measure a known distance on a high-resolution copy of the printed map (or the scale printed on the map itself) | a scale close to 1.1 or 6.4 miles per inch, with an error below 10 % | a scale matching neither |
| T2 | **Pairwise calibration:** choose unambiguous points (rings of the symbol, bridges, shorelines), and use a transformation with the pair test of `audit_06` | scale spread between pairs below 10 % | a large spread, as in the current case |
| T3 | **Rounding:** register the rounding rule in advance, and compute the location under both rules together | a location that agrees under both rules | a location that changes with the rounding rule (as in `audit_11`) |
| T4 | **Null model that preserves the templates:** replace words with words of the same length within the same template | the anomalous orders (k7, k14) remain anomalous | the anomaly disappears, showing that it comes from the template structure |
| T5 | **Power of the test:** plant a known phrase in a synthetic cipher with the same structure, then run the test pipeline | the statistic clearly distinguishes the planted phrase (not expected from `audit_05`) | the statistic does not change, which proves the lack of power |
| T6 | **Pre-registered skip interpretations:** E3 (skip without an extra move) and alternating signs for δ | the number of rules reproducing (C) 32/32 is one (E2 unique) | several rules reproduce (C), so the match does not identify the rule |
| T7 | **Verification of the original transcription:** compare the transcription with a high-resolution image of the original Zodiac symbols, after unifying the identities | the pattern of repetitions matches the original | a difference in identities or in repetition counts |

## 7. Classification of results

### 7.1 Directly supported by the data

- 29 identity categories in figure (A), with repetition at {1, 26}, {2, 32}, {6, 14}. The distance inside each category is 0, and the smallest distance between two different categories is 0.1316. The threshold used, 0.12, lies just below it. Any threshold in the interval (0, 0.1316) gives the same partition (`audit_08`).
- The pixel reading of (C): `CX2VAC7PGID4H6?TJF3!5LR118O9MEOW` (the category identities are linked to the visual labels).
- T1 does not appear literally in any of the 34 orders, and T1 satisfies only one pair in the paper's order.
- Full agreement of two independent implementations of the transposition family (204 of 204).

### 7.2 Inferred, with assumptions

- The reproduction of (C) requires shift 2, row alternation, skipping of empty cells, and δ = +2 (all of which are stated or inferred).
- That the internal calibration of the figure reflects the paper's scale. If Foxon's rings represent the inch of the original map, the real map gives about 1.1 miles per unit, with a spread of about ±30 %.
- The rejection of 6.4 miles per unit is based on this assumption, not on an independent measurement.
- That the null model used for the phrases is suitable for testing the signal. This assumption is not correct, as `audit_10` shows, so it must not be relied on.

### 7.3 Undetermined with the available data

- The scale of the original printed map.
- The location (12, 3), including the pole (crosshair or summit) and the rounding rule.
- Any relation between Route 24 and any event.
- Whether a solution exists inside or outside the family; the meaning of any phrase; the identity of the original symbols; and the encryption key.
- What "#" means in the 1970 letter.

## 8. The next step that reduces the uncertainty

The most important step is **fixing the scale of the original map** (T1), by direct measurement or from a printed scale, because that determines whether the geographic hypothesis can be tested at all. Then, if an original transcription of the symbols becomes available (T7), the identity question can be closed. The current statistical test does not reduce the uncertainty, and it must not be reused before its model is corrected (T4 and T5).

## 9. Preservation of the evidence

- Results of the previous package are kept as they are in `original_results/`, and its documents in `original_docs/`.
- Every correction or reservation is recorded in `CORRECTIONS_LOG.md`, with its reason and the evidence that led to it.
- No earlier result was deleted, and none was replaced silently.

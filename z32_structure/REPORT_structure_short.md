> Translated from Arabic into English. The Arabic original is kept in the research workspace; its SHA-256 is 4e6fb08c8fed4481ebea4ad8e72a2d70bf0765e22615e04f9ddc1f1d12ce09e7.

# Short report: Z32 structure before any reading (stage 6)

## Summary

- **The original symbols are not available.** What we have is a printed transcription from Foxon's paper, containing 29 different identities and 3 identities that repeat. The identities themselves are not confirmed against the originals.
- **The repetition structure rules out a small alphabet.** The 32 symbols contain very little repetition. A set of 29 symbols for all letters, or a homophonic substitution with three symbols per letter or fewer, is rejected statistically. The required symbols come from a larger set (about 63 symbols or more), or from five or more homophones per letter.
- **The reading test with a free key cannot discriminate.** Real English texts of 32 letters are detected in only 10 % of cases. Therefore negative results for Z32 mean nothing.
- **There is no solution and no geometric interpretation.** No coordinates and no target words were used.
- **First test:** the fixed Z340 key on the 27 shared symbols, with calibration by permutation. It needs the Z340 key and the symbol matching, which are not available now.

## 1. Separation of levels

| Level | What it is | Status |
|---|---|---|
| Original symbols | the 32 symbols on the original document | not available. We have a printed transcription in ASCII characters from Foxon's paper |
| Proposed readings | (C) of Foxon, Grinell's readings (ESTIMATE FOUR RADIANS AND FIVE INCHES), Ziraoui (LABOR DAY...), and others | published proposals, not based on a calibrated test |
| Added assumptions | the transposition rule (k, δ, W1, E2), homophonic substitution, the declination 16.9, the conversion of hour and minute, radians, the angle reference, the scale | analytical assumptions that do not appear in the original text |

## 2. Chain: declination → hour and minute → radians

| Step | Support | Classification |
|---|---|---|
| The phrase "0 is to be set to Mag. N." on the map | visible in the redrawn figure | directly supported |
| The phrase "Radians & # inches along the radians" (letter of 26 July 1970) | quoted in the paper | directly supported |
| Conversion 1 radian = 57.2958° | mathematics | directly supported |
| Declination of about 16–18° in the area around 1970 | IGRF model (not a historical measurement) | assumption (typical value) |
| That the author used this declination to rotate the clock | no direct evidence | assumption |
| The clock-setting mechanism that gives hour and minute | not specified in the text | assumption |
| hour = floor(d/30), minute = round(d/6) | no text states it. Two hands cannot point to the same angle with two integer values | unproven analytical choice |
| Hour 0 displayed as 12 | display only | unproven analytical choice |
| Minute = radians, and hour = inches | the text mentions radians and inches without specifying any number for either | unproven analytical choice |
| Angle reference (N/E/S/W) and direction of rotation | the paper itself says the choice is arbitrary | unproven analytical choice |
| Inch = printed inch on the map | scale not measured | assumption |

**Number of readings before any choice of direction or scale.** For the declination 16.9 alone, four rules give different pairs (r, θ):

| Rule | Hour H | Minute M | r | θ |
|---|---|---|---|---|
| R1 Foxon: hour = floor(d/30), minute = round(d/6) | 0 | 3 | 12 | 3 rad (171.9°) |
| R2 minute = floor(d/6) | 0 | 2 | 12 | 2 rad (114.6°) |
| R3 hour = round(d/30) | 1 | 3 | 1 | 3 rad (171.9°) |
| R4 hour-hand angle = d (minute from 30H + M/2) | 0 | 34 | 12 | 34 rad (148.1°) |

The fifth rule (swapping the roles of r and θ) gives θ = 12 radians ≡ 327.5°. The paper excluded it on the grounds that θ ∈ [0, 2π), without reducing 12 modulo 2π. That exclusion is a choice, not a result.

## 3. Hypotheses (registered before running)

| Hypothesis | Why it was chosen before the result | What it predicts | Status |
|---|---|---|---|
| H0: no decodable structure | the null hypothesis | no improvement over random permutations | not rejected. The free test is not informative |
| H1: homophonic substitution (k ≥ 5 or A ≥ 63) | the paper documents this type in Z408 and Z340 | few repetitions | consistent with the structure. The reading is not strongly tested |
| H2: at most 29 symbols (monoalphabetic or k ≤ 3) | the simplest model | many repetitions | **rejected** |
| H3: position permutation | the paper documents a permutation in Z340 | an alternative order gives a natural reading | not supported in 4 orders. Not informative |
| H4: shared Z340 key | the paper: 27 of 29 symbols are in the Z340 key | a fixed reading above the permutations | **not tested**: the key is not available |
| H5: the symbols are numbers | the instruction mentions radians and inches | numeric repetition | postponed: no calibrated numeric model |
| H6: the symbols are map positions (a coordinate grid) | the message is linked to a map | symbols corresponding to points | not testable now |

## 4. Results

**(a) Structural repetition.** Observed: R = 3 identities repeat (each twice). Two-sided test at α = 0.05.

| Model | E[R] | P(R ≤ 3) | P(R ≥ 3) | Verdict |
|---|---|---|---|---|
| uniform, A = 29 | 8.76 | 0.0000 | 1.0000 | rejected |
| uniform, A = 54 | 6.38 | 0.0248 | 0.9958 | borderline; rejected with difficulty |
| uniform, A = 63 | 5.75 | 0.0659 | 0.9862 | consistent |
| uniform, A = 100 | 4.05 | 0.3659 | 0.8544 | consistent |
| English, k = 1 | 8.52 | 0.0000 | 1.0000 | rejected |
| English, k = 3 | 6.56 | 0.0165 | 0.9983 | rejected |
| English, k = 5 | 4.79 | 0.1971 | 0.9398 | consistent |
| English, k = 10 | 2.79 | 0.7106 | 0.5613 | consistent |

Caveat: we assumed that the letters of the text are independent. Real English has more repetition, which makes small alphabets less consistent, but this does not change the main result.

**(b) Reading test with a free key.** 150 random permutations of the same symbols were used as a control (mean −1.7053, standard deviation 0.0579, 95 % range −1.6128).

| Order | Score per pair | p | p after Bonferroni (× 4) |
|---|---|---|---|
| O1 printed | −1.7468 | 0.788 | 1.00 |
| O2 zigzag | −1.7020 | 0.490 | 1.00 |
| O3 columns | −1.7066 | 0.510 | 1.00 |
| O4 reversed | −1.6976 | 0.457 | 1.00 |

No order shows an excess. This is a negative result, but not an informative one, as shown in (c).

**(c) Power.** We used 20 English texts from GPL-3, each 32 letters long, not part of the language model, encrypted with ten homophones per letter. Only 2 of the 20 were detected (power 0.10). The mean score of the English texts (−1.7064) is almost equal to the mean of the random permutations. In other words, the free key does not distinguish real text from random text of 32 letters. **Therefore the negative results in (b) are not evidence against H1.** The pre-registered interpretation rule (power ≥ 0.8) was not met, so no conclusion is drawn.

**Negative results recorded:** no excess for any tested order; no readable reading; the repetition structure rejects small alphabets.

## 5. Distinguishing the levels

- **A decryption that produces a readable message:** none. The free test cannot discriminate.
- **A geometric interpretation that produces a point:** none. The declination chain gives at least four (r, θ) pairs before any choice of direction or scale.
- **A hypothesis linking the two:** not tested end to end.

## 6. Criteria for a "solution" (not met)

No result counts as a solution unless: (1) the rules were registered in advance; (2) it is reproducible; (3) it exceeds random permutations after correcting for multiple comparisons; (4) it produces readable text, not only language-model scores; (5) it is confirmed by an independent test. None of these is met.

## 7. Strongest hypotheses and the first test

The two strongest testable hypotheses:

1. **H4 (shared Z340 key):** predicts that the fixed Z340 key, applied to the 27 shared symbols, gives a reading above random permutations of the letters over the same symbols. Its evidence: the sharing documented in the paper.
2. **H1 with a larger symbol set (k ≥ 5 or A ≥ 63):** predicts few repetitions, which is supported. Its reading requires the first test.

**First test:** apply the published Z340 key to the 27 shared symbols in Z32, with the statistic registered in advance (log-probability of pairs under a fixed English model), calibration by permuting the key letters across the symbols, and power checked first on a synthetic cipher with the same key. Its power is higher than the free test, because the key is fixed and has no free parameters.

- **What it establishes:** that the key gives text above chance on Z32.
- **What it does not establish:** the meaning of the message, or any location.

**What is missing before running it:**
- A high-resolution original image of Z32, to match the identities (the current transcription is in ASCII characters).
- The published Z340 key (the symbol-to-letter table) and an original image of Z340, to match the 27 symbols.
- Verification of the number of symbols in Z340 (the paper mentions only the number of Z408 symbols: 54).
- The original map image, if H6 is tested later.

**Closing note:** failure of the Foxon model does not mean Z32 cannot be solved. The available data (32 symbols with two repetitions) cannot distinguish most hypotheses. The limitation may lie in the data, not necessarily in the cipher.

**Files:** PREREG_structure.md (pre-registration), run_structure.py (execution), results_structure.json (results), chain_enumeration.json (declination rules), run_structure.log (log).

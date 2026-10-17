# Pre-registration for the next review (written before running alternatives_family.py)

## Scope
Test whether any alternative 32-letter phrase is consistent with the repeat structure of Fig.1 under the transposition orders that are either supported by Foxon (2023) or declared here.
This is not a claim that any phrase is the solution.

## Fixed inputs
- Symbols: 32 glyphs of Fig.1(A), identity classes from bitmap comparison (scripts/fig_glyph_check.py), labels from data/z32_fig1A_transcription.csv.
- Valid orders: the 34 valid readings produced by scripts/transposition_family.py (family of 204 configurations).
- Repeat constraints: three pairs of output positions holding the same symbol; the phrase must carry the same letter at both positions of each pair.

## Literal test (primary)
Phrase T1 = TWELVEINCHESALONGTHETHREERADIANS (letters only; the cipher has no spaces).
The result is recorded exactly, with no edits. T1 was already tested in the earlier package; it is repeated here.

## Alternative family (pre-registered)
Templates (tokens joined without spaces; total length must equal 32 letters):
- A: N1 U1 ALONG THE N2 U2
- B: N1 U1 AND N2 U2 ALONG
- C: N1 U1 N2 U2
Number words N = ONE TWO THREE FOUR FIVE SIX SEVEN EIGHT NINE TEN ELEVEN TWELVE THIRTEEN FOURTEEN FIFTEEN EIGHTEEN TWENTY
Unit words U = INCHES RADIANS MILES DEGREES MINUTES FEET SIGNS HOURS

The family size N is the number of enumerated phrases of length 32 (reported by the script).
T1 belongs to template A and T2 belongs to template B, so both are in the family.
T3 (THREEANDTHREEEIGHTHSRADIANSSIXIN, a previously proposed phrase) is NOT in the family; it is reported separately as a reference.

## Statistic
pass(p,u) = 1 iff all 3 repeat constraints hold for phrase p in valid order u. Observed total O = sum over p and u of pass(p,u).

## Null model (multiplicity-aware)
Composition-preserving null: for each phrase, R = 2000 random permutations of its own letters (keeps letter counts, destroys word order).
T_r = sum over p and u of pass under the permuted phrase, for replicate r.
Global p-value = fraction of r with T_r >= O.
Per-phrase p-value = fraction of that phrase's permutations whose pass count >= its observed pass count.
Bonferroni-adjusted per-phrase p = min(1, N * p_phrase).

## Decision rules (fixed now)
- A phrase is "consistent with the repeat structure" only if its Bonferroni-adjusted p < 0.01.
- A family-wide excess is claimed only if the global p < 0.01.
- Passing the repeat constraints is NOT evidence of meaning. No solution claim follows from this test alone.

## Map audit (variants fixed now; reported as sensitivity, none is selected as "the" answer)
- A: five cities, free offset (similarity transform: scale, rotation, translation).
- B: four cities (without Oakland), free offset.
- C: five cities, crosshair fixed at the Diablo coordinate.
- D: four cities, crosshair fixed at the Diablo coordinate.
Uncertainty: Monte Carlo, 6 px pixel jitter and 1 mile geographic jitter per landmark, 3000 draws.

## Disclosures
- The transposition rule family was declared before the earlier package run, but Fig.1(C) had been seen before that declaration.
- T1 was already tested with its literal result before this package.
- The four map variants were computed once in an exploratory step before this package; they are reported here as sensitivity analysis.

> Translated from Arabic into English. The Arabic original is kept in the research workspace; its SHA-256 is 045378ccb65de519f261fa7b39caf345de944d9d9ede4eb032bca83f121d3479.

# Readiness report for test H4a (Z340 key applied to Z32)

## Summary

- **The test cannot be run now.** Reason: the full Z340 key exists as a drawn figure in the published paper, not as processable text. Matching the Z32 symbols to the original symbols requires images that were not available.
- **The test design is registered and calibrated.** On synthetic data with a known key: power 0.963 at full matching, and type I error 0.010 at p < 0.01.
- **Critical constraint:** the test requires that at least 90 % of the matches are correct. At 80 %, power falls to 0.583. The greatest risk is therefore not the statistics, but symbol matching.

## What the reliable source says about Z340

- Z340: 340 letters, 63 different symbols, a grid of 20 rows × 17 columns (several sources).
- The published solution (Blake, Oranchak and Van Eycke, December 2020) combines a homophonic substitution and a position permutation. A substitution key alone is not enough to decrypt Z340.
- The substitution key table, "Refined homophonic substitution key", exists as a figure in the paper. I did not find a text version of it.
- The Hodel document gives only four assignments (A to D, E to R, M to O, and T to L) in a special notation, not a complete key.

## Calibration results (registered in advance)

| Case | Power at p < 0.01 | Power at p < 0.0025 | Median p |
|---|---|---|---|
| 1.0 | 0.980 | 0.963 | 0.001 |
| 0.9 | 0.923 | 0.797 | 0.001 |
| 0.8 | 0.713 | 0.583 | 0.001 |
| 0.7 | 0.500 | 0.330 | 0.010 |
| random key (H0) | 0.010 | 0.000 | 0.488 |

Interpretation: power is adequate (at least 0.8) when 90 to 100 % of the matches are correct, and falls below 0.8 at 80 %. Caveat: the calibration assumes a uniform distribution of 3 symbols per letter, which is not the unpublished distribution of Z340, and it assumes that the original plaintext is English with GPL letter frequencies.

## What is missing (in order)

1. **The Blake, Oranchak and Van Eycke (2021) paper in PDF form.** The key-table page would be extracted as an image and converted into symbol-to-letter pairs. The table would then be verified by decrypting Z340 itself, using the transposition described in the paper. If that decryption does not return the known text, the transcription is wrong and will not be used.
2. **A high-resolution image of the original Z32 message** (from the Chronicle or the FBI Vault), to match the 29 symbols with the original symbols, rather than relying on the printed transcription in ASCII characters.
3. **A definition of the Z32 transposition, if any.** If H4a does not match, the possible transposition is not assumed from Z340 (a 17 × 20 grid), because Z32 is a 17 × 2 grid. Any transposition for Z32 is to be registered after examining the table, not after.

## What the test proves and does not prove

- **It proves:** if H4a succeeds, the same key decrypts Z32 into English text with a score above chance. That would be evidence of a cipher relation between the two messages.
- **It does not prove:** the meaning of the message, any location, or that Z32 contains instructions about declination or radians.
- **Failure of H4a:** does not reject H4 with a transposition, because that transposition has not been tested.

## Next step

Upload the PDF of the published paper and a high-resolution image of Z32. Then run the test as registered, with the matching calibrated first.

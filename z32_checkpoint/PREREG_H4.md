> Translated from Arabic into English. The Arabic original is kept in the research workspace; its SHA-256 is ccc94448d5bd1a4c21a8e0a009bb7907848c8aa00b7c747c12601da6fa79cf7a.

# Pre-registration: test H4a (fixed Z340 key applied to Z32, no permutation, in printed order)

## Hypothesis

H4a: applying the published homophonic substitution key for Z340 to the Z32 symbols in printed order (O1) produces English text with a higher score than random letter permutations applied to the same symbols.

## Required inputs (not available now; this is why the test is postponed)

1. A Z340 key table in machine-processable form: Z340 symbol to letter. The table exists in the published paper (Blake, Oranchak and Van Eycke, 2021) as a drawn figure, not as text.
2. Identity matching of each of the 27 symbols shared by Z32 with the corresponding Z340 symbol. The current Z32 transcription uses the ASCII characters printed in the paper, not the original symbols, so the matching requires original images.
3. A check that Z340 has no permutation in this test. The full Z340 solution uses a position permutation (a 17-column grid), which is not applied to Z32 (32 symbols in two rows of 17 and 15) without a prior definition.

## Statistic

T = mean of log P(letter_i, letter_{i+1}) over the letter pairs where both positions are known, under a letter-pair model from GPL-2 with add-0.5 smoothing.

## Calibration (null hypothesis)

- Permutation of letter values across the distinct assigned symbols (999 permutations).
- p = (1 + number of null values of T that are at least T_obs) / 1000.

## Decision rules

- H4a is supported only if p < 0.0025 (Bonferroni correction across the four tested orders, O1 to O4).
- Failure of H4a does not reject H4 with a position permutation. Such a permutation must be registered first.
- Required before the real run: power of at least 0.8 at p < 0.0025 on synthetic data with a known key, and a measurement of how the power depends on the proportion of correctly assigned symbols.

## Synthetic calibration (to be run before the real run)

- Synthetic key: 21 letters (without J, K, Q, X, Z, as in Z340), 3 symbols per letter, giving 63 symbols. This is a simplifying assumption about the distribution of the real Z340 key, which is not published here.
- Plaintext: 32-letter segments from GPL-3 (not used in the language model), after removing letters that are not in the key.
- Encryption: each letter is replaced by a random one of its three symbols.
- Z32 simulation: two of the 32 positions are replaced by two new symbols not in the key (unknown; excluded from T).
- Scenarios: proportion of correctly assigned symbols f in {1.0, 0.9, 0.8, 0.7}, and scenario H0 with an unrelated random key (to measure the type I error).
- 300 replicates per scenario.

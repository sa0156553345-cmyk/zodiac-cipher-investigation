> Translated from Arabic into English. The Arabic original is kept in the research workspace; its SHA-256 is 5dcae9a8ab61a2deb2234524b5544eb60451df8e4770051546c5641f60f6f834.

# Pre-registration: structural analysis of Z32 (before any run)

## Data

- Symbols: the printed sequence of the 32 symbols (the package transcription, matching the symbol identities in figure 1A of Foxon 2023). These are printed identities, not the original Zodiac symbols, and the conclusions are conditional on their correctness.
- The structure is read by identity only: which positions repeat the same identity. The original symbols are not available.
- Reading orders adopted (now fixed): O1 = first row, then second row; O2 = zigzag (first row forward, second row backward); O3 = double columns (r1c1, r2c1, r1c2, r2c2, ...); O4 = reverse of O1.
- Repeated positions in O1 (from the transcription): {1, 26}, {2, 32} and {6, 14}. Three pairs; the others are singletons.

## Hypotheses, and why each was chosen before the result was known

- H0: no structure decodable beyond what a random distribution of symbols predicts. Reason: the null hypothesis, which every test requires.
- H1: homophonic substitution, in which each plaintext letter is represented by more than one symbol, with the symbols chosen at random. Reason: the paper documents that Z408 and Z340 are homophonic substitutions, so this is the closest documented hypothesis for this family of ciphers.
- H2: monoalphabetic substitution, or a small symbol set (at most 29 symbols for all letters). Reason: the simplest possible cipher; it predicts many repetitions if true. It is a falsifiable hypothesis.
- H3: transposition before substitution, with the printed order not being the reading order. Reason: the paper documents a simple transposition in Z340. Three alternative orders (O2 to O4) are tested, as defined in advance.
- H4: the same Z340 key is used for Z32 (27 of 29 symbols shared, according to the paper). Reason: the documented shared symbols. It needs the Z340 key, which is not available now, so it is postponed.
- H5: the symbols represent numbers, not letters. Reason: the instruction text mentions radians and inches, so the content may be numeric. Postponed, because no calibrated numeric model is available.
- H6: the symbols represent positions on the map (a coordinate grid), not text. Reason: the message is linked to a map. Not testable now without the map data.

## Structure test (independent of reading)

- Statistic S = number of identities that appear exactly twice. Observed S = 3; maximum repetition = 2.
- Models: (a) independent symbols drawn uniformly from a set of size A in {29, 54, 63, 100, 165, 250, 500}; (b) independent English letters (distribution from GPL-2) with k homophones per letter, k in {1, 2, 3, 5, 8, 10, 15, 20}.
- 100000 simulations per model. A model is "consistent" if P(S <= 3) >= 0.025 and P(S >= 3) >= 0.025 (two-sided test, alpha = 0.05).

## Reading test (with calibration)

- Language model: letter pairs from GPL-2, with add-0.5 smoothing.
- Decoding model: free assignment of each identity to a letter A to Z, with no permutation. Score = mean log P(pair) over the 31 pairs.
- Optimiser: simulated annealing, 8000 steps, two restarts; the best result is kept.
- Calibration: 150 random sequences with the same repetition structure (three pairs, at random positions), processed with the same optimiser. The p-value for each order = proportion of random samples whose best score equals or exceeds the observed one.
- Multiple-comparison correction: Bonferroni over the four orders.
- Power check: 20 English texts from GPL-3 (not in the language model), 32 letters long, encrypted with k = 10 homophones per letter, and tested with the same method. Power = proportion of cases detected at p < 0.05 (uncorrected).
- Interpretation rule: if power is below 0.8, negative results for Z32 are not informative and are not evidence against H1. If power is at least 0.8 and the corrected p-value for an order is below 0.01, that is a candidate structure that needs independent verification; it is not a solution.

## What will not be done

- No target word or coordinate will be used to assess success.
- No order, model, or criterion will be chosen after seeing the results.
- The current coordinates will not be used as a target.

> Translated from Arabic into English. The Arabic original is kept in the research workspace; its SHA-256 is 77e2c34aa596eacb7cb0923bb563498bbce60b602ca85433a86d76977528559d.

# Pre-registration: improving the matching of Z340 symbols (before any run)

## Goal

Measure the position-wise letter agreement with the reference text. The 70 % figure is an exploratory target, not a success condition.

## Sample split (fixed by position, not random)

- Tuning set: k = 0 .. 169. Used only to select the method.
- Validation set: k = 170 .. 339. Not used for any selection; measured once, for the selected method.
- The ten diagnosed cases and the six visual corrections all fall within the tuning set.

## Candidate methods (defined before running)

- M0 (baseline): local Otsu mask; skeleton, then dilation with a disk of radius 2; size normalisation preserving the aspect ratio to 44 pixels on a 52 × 52 panel; 1-pixel dilation; Dice coefficient, maximised over shifts of −2 to +2.
- M1: as M0 without the skeleton (the ink mask directly after size normalisation).
- M2: as M0, but with dilation radius 1 instead of 2.
- M3: average of 0.5 × the M0 score and 0.5 × the M1 score.
- M4: as M0, with a search over rotations of {−6, −4, −2, 0, +2, +4, +6} degrees, taking the highest score for each key glyph.
- M5: as M1, with a search over the same rotation angles.

## Measure

- Letter accuracy: the proportion of positions k where the letter of the top-scoring glyph equals the reference letter.
- Confusion matrix, rank, and confidence value: for diagnosis only.

## Selection rule

- The method with the highest accuracy on the tuning set is selected. In a tie, M0 is preferred (simplest, and the baseline).
- The validation set is measured for all methods, and all results are shown without selection.
- The matching does not use the reference text to choose the identity: identity = highest score only.
- No manual visual corrections are applied in this experiment. It is a purely algorithmic experiment.

## Continuation rules

- Methods, measures, and the split are not changed after seeing the results.
- If the selected method does not reach 70 % on the validation set, the result is reported as it is, without modification.

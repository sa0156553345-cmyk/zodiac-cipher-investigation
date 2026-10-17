# Discrepancy audit of the reported results

This file records how the reported numbers and the statements in the dossier were checked against the archived files.

## Method

- Checks are in `tests/check_archive.py`. Their rules were written in the file header before the first run.
- Each reported number is recomputed from the machine-readable file it comes from. The comparison uses the precision the document states. A stated value is accepted if it lies within half a unit of that precision.
- A mismatch is reported as FAIL. It is never corrected automatically.
- Statements that depend on sources outside the archive are reported as UNCHECKED.
- Two runs are recorded here. Run 1 is the first run of the checks. Run 2 is after the corrections listed in the comments. The final run, after the manifests were regenerated, is reported in the final message of the packaging task.

## Results (run 1 and run 2)

| Check | Run 1 | Run 2 | Comment |
|---|---|---|---|
| C1 | PASS | PASS |  |
| C2 | PASS | PASS |  |
| C3 | PASS | PASS |  |
| C4 | PASS | PASS |  |
| C5 | PASS | PASS |  |
| C6 | PASS | PASS |  |
| C7 | PASS | PASS |  |
| C8 | PASS | PASS |  |
| C9 | PASS | PASS |  |
| C10 | PASS | PASS |  |
| C11 | PASS | PASS |  |
| C12 | PASS | PASS |  |
| C13 | PASS | PASS |  |
| C14 | PASS | PASS |  |
| C15 | PASS | PASS |  |
| C16 | PASS | PASS |  |
| C17 | PASS | PASS |  |
| C18 | PASS | PASS |  |
| C19 | PASS | PASS |  |
| C20 | PASS | PASS |  |
| C21 | FAIL | PASS | Run 1 compared at 3 decimals, but the dossier states 2 decimals (26.58, 33.69). The rule in the test header says the stated precision applies. Run 2 checks each stated value within half a unit of its stated precision. Both results are kept here. |
| C22 | PASS | PASS |  |
| C23 | PASS | PASS |  |
| C24 | PASS | PASS |  |
| C25 | DOCUMENTED-DISCREPANCY | DOCUMENTED-DISCREPANCY | Documented discrepancy (dossier item C17): the pre-registration states 100,000 simulations per model; the executed code uses 20,000. Not corrected. |
| C26 | PASS | PASS |  |
| C27 | PASS | PASS |  |
| I1 | FAIL | FAIL | Run 2 failed only because the stale checksum manifest still listed deleted cache files. Regenerated after the final edits. |
| I2 | FAIL | FAIL | Run 2 failed for the same reason: new files were not yet in the manifest. Regenerated after the final edits. |
| I3 | PASS | PASS |  |
| I4 | PASS | PASS |  |
| I5 | FAIL | PASS | Run 1 flagged the checker itself (it contained the literal path strings in its rule text). Fixed by building the markers at run time; the rule is unchanged. |
| I6 | PASS | PASS |  |
| I7 | FAIL | PASS | Run 1 failed because five documentation files had not been written yet. Written before run 2. |
| U1 | UNCHECKED | UNCHECKED | Needs the source PDFs, which are not in the archive. Use docs/SOURCES.md to obtain them. |
| U2 | UNCHECKED | UNCHECKED | The endpoint distances 44.75 and 103.11 miles are not recorded in an archived file. Needs regeneration or a source. |
| U3 | UNCHECKED | UNCHECKED | Needs a parser for the literal-phrase CSV. The schema was not checked in this run; see the dossier section 7. |
| U4 | UNCHECKED | UNCHECKED | Web and FBI sources are not stored and the network is disabled in this environment. |

## Implementation corrections made after run 1

- I5: the checker no longer contains the literal absolute-path strings it searches for.
- C21: the comparison follows the precision stated in the dossier. The rule was already in the header; the first implementation did not apply it.

No reported number, result or conclusion was changed.

## Open discrepancies carried into the dossier (not resolved here)

- C4 (dossier section 13): U03 is visually confirmed at k = 7 but never chosen by M5. Still open.
- C8: the published decryption is not reproduced by this project. Cause not isolated.
- C9: the transposition corrections described as "with these corrections" in the paper are not described in the extracted text. Sections 2 to 4 cannot be independently verified.
- C10 and C11: scale and edition claims remain unverified.
- C16: the ePrint identifier appears only in a search URL.
- C25: pre-registration and code differ on the number of simulations (100,000 against 20,000).
- U2 and U3 above need regeneration or a parser.

## Images

The image provenance audit (`docs/IMAGE_PROVENANCE.md`) found 45 image files. None qualifies as an original research image, so none is in the repository. No count in this file depends on those images.

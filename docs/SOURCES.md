# Source documents and where they come from

This archive does **not** contain the publications listed here. Their redistribution status was not verified, so they are documented, not copied. Hashes were computed in this packaging session with SHA-256.

| ID | Document | Expected location for reproduction | Size (bytes) | SHA-256 | Notes |
|---|---|---|---|---|---|
| S1 | Floe Foxon, *On the 32-Character Zodiac Cipher* (2023). The uploaded file is named `2023-982.pdf`. | `z32_independent_audit/input/2023-982.pdf` (also expected by the round folders `z32_repro/input/`, `z32_next_review/input/`, `z32_map_calibration_audit/input/`) | 1061904 | 6d200c304d4b8be7f41b879dd5c50c182128330460bf4ca73995050500cc5350 | The identifier 2023/982 comes from a URL seen during search, not from the PDF text. The 4 copies in the workspace are byte-identical to the uploaded file. |
| S2 | D. Oranchak, S. Blake, J. Van Eycke, *The Solution of the Zodiac Killer's 340-Character Cipher*, arXiv:2403.17350v1 (26 March 2024; category cs.AI per the PDF header). | Any location; pass its path to `z32_checkpoint/reproduce_z340_from_pdf.sh`. | 17366922 | 8bbdbea255b64dfe8f7125377133cdfb45fff240a70ff677fc1e5f4e43b56b99 | Used to regenerate figures and text for the Z340 pipeline (pdfimages, pdftotext). |
| S3 | `z32_independent_audit.zip` (uploaded archive of the audit package) | Not needed; the same package is included as `z32_independent_audit/`. | 2693558 | 3bd5fc5fe61df8afbe77a9f348e434a200f455eb7e0e5f02b55d7ca0b2999493 | Not included as a duplicate of the package folder. |
| S4 | FBI Vault, *The Zodiac Killer*, parts 02 to 07 (`vault.fbi.gov`) | Not stored. Parts 02 to 04 were read only as text prefixes; parts 05 to 07 have no machine-readable text. | n/a | n/a | Recorded in `z32_source_search/PHASE3_FBI_PARTS_2_TO_7.md` and `z32_source_search/PHASE4_STATUS.md`. |
| S5 | Phillips 66 and Gousha catalogue and archive records, plus secondary web material (blog posts, forum threads, a social-media post, a dealer listing, a PDF summary of a Z340 key) | Not stored. | n/a | n/a | URLs and access notes are in `z32_source_search/PHASE2_SOURCE_REPORT.md`. Claims from S5 are unverified (see the dossier, section 14). |

To run the Foxon audit package, place your own copy of S1 at `z32_independent_audit/input/2023-982.pdf`. The placeholder files named `PLACE_2023-982.pdf_HERE.md` in the input folders explain the same thing.

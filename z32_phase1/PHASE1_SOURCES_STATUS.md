> Translated from Arabic into English. The Arabic original is kept in the research workspace; its SHA-256 is e7d0401dcdcc7dfec8f64d2f6226c967d32759be7c42dfc3be6c0e3e8c863450.

# Phase 1: status of obtaining the original sources

## What was verified

1. **The original solution paper: identified and accessible.**
   - Title: The Solution of the Zodiac Killer's 340-Character Cipher
   - Authors: David Oranchak, Sam Blake, Jarl Van Eycke
   - Identifier: arXiv:2403.17350 (submitted 26 March 2024)
   - Links: https://arxiv.org/abs/2403.17350 , https://arxiv.org/pdf/2403.17350 , https://arxiv.org/html/2403.17350v1 (the last one was opened successfully).

2. **Text from the paper (HTML) was examined, and it contains the following information as text:**
   - Z340 has 63 different symbols (section 5.3).
   - The Z340 grid is 20 × 17 (section 5.3), and its width is 17 (section 3).
   - Definition of the transposition: dec_{n,m}(C_k) = C_{nk mod N, mk mod M}, subject to a congruence condition (section 5.3). In the case (1,2) on a 20 × 17 grid.
   - Division of the solution in section 5.4: rows 1–9, then 10–18, then row 19, then row 20, with the transposition (1,2) applied to each section.
   - The first partial solution (section 5.4) read only about 23 % of the text, not the final solution.

3. **Links to figure images extracted from the HTML version (not opened):**
   - Z32 figure (figure 8): https://arxiv.org/html/2403.17350v1/media/image3_binarised.jpg
   - Z408 figure (figure 4): https://arxiv.org/html/2403.17350v1/media/z408_key.png
   - Z340 figure as published in the Chronicle (figure 6): https://arxiv.org/html/2403.17350v1/media/z340_sf_chronicle_binarised.jpg

## What was not verified

- **The Refined Homophonic Substitution Key table for Z340: not extracted.** The table is a drawn figure in the paper, and its image was not opened. No machine-readable text of this table exists in what was examined.
- **High-resolution Z340 image to verify the table: not opened.**
- **Original Z32 image: not opened.** The current transcription is in ASCII characters from Foxon's paper.
- **Reason for stopping:** the fetch tool has returned a RATE_LIMIT_EXCEEDED error since the first attempt to download the images (about 20 minutes and several attempts). The image tool shows results only to the user, and does not return their content to me.

## What is needed to complete phase 1

The best option: upload the PDF of the paper (arXiv:2403.17350) to the conversation. Then:
1. Extract the key-table page using pdftoppm at high resolution (because the table may be vector graphics rather than a bitmap, so pdfimages is not sufficient).
2. Display the page and extract the symbol-to-letter pairs by visual inspection, documenting every uncertain symbol without guessing.
3. Extract the Z340 page and the Z32 page at the same resolution for comparison.

Alternative: upload the three image files listed above directly, if they can be downloaded from the browser.

## Methodological note

Current state: the paper is identified, and the official definition of the transposition is documented in the text. But everything concerning the content of the table and the identity of the symbols depends on the images. No symbol has been decided, and no test has been run.

# Project map

This repository keeps the layout of the research workspace. The folders are organised by experiment, not by file type. Moving files would break relative paths that the scripts, the reproduction script, the manifests and the dossier rely on, so the folders were not renamed. This map gives the same view by category.

| Category | Where it is | Notes |
|---|---|---|
| Narrative and status | `README.md`, `ZODIAC_CIPHER_RESEARCH_DOSSIER.md` | The dossier is the full record, including contradictions and unverified claims. |
| Methodology and documentation | `docs/` | Reproduction guide, sources, archive changes, records index, image provenance, licence status, discrepancy audit. |
| Research code (Z340 reconstruction) | `z32_checkpoint/scripts/`, `z32_checkpoint/phase1_working/`, `z32_checkpoint/full63/`, `z32_checkpoint/methods/methods_experiment.py` | Pipeline scripts run in the order given in `docs/REPRODUCTION_GUIDE.md`. `phase1_working/` holds development scripts and intermediate arrays. |
| Research code (Foxon audit package) | `z32_independent_audit/scripts/` | Entry point: `z32_independent_audit/run_all.sh`. |
| Research code (H4a, structure, geometry) | `z32_h4/calibrate_h4.py`, `z32_structure/run_structure.py`, `z32_structure/audit/audit_structure_stat.py`, `z32_phase5/run_phase5.py`, `z32_phase5_audit/audit_phase5_independent.py`, `z32_phase5_audit/analysis/`, `z32_phase5_audit/candidate_sensitivity/scripts/` | Each folder runs on its own from the folder shown. |
| Source transcriptions and tables | `z32_independent_audit/data/`, `z32_checkpoint/artifacts/`, `z32_map_calibration_audit/data/`, `z32_next_review/data/` | Z32 transcription, key table, transposition values, reference comparison. |
| Machine-readable results | `z32_*/results/`, `z32_checkpoint/methods/*.json`, `z32_checkpoint/full63/*.json`, `z32_h4/calibration_h4.json`, `z32_structure/results_structure*.json`, `z32_phase5/phase5_summary.json`, `z32_phase5_audit/audit_summary.json`, `z32_checkpoint/methods/methods_scores.npz` | Failed and inconclusive results are kept (for example `z32_repro/superseded/`). |
| Experiment configurations, logs and validation | `z32_*/PREREG*.md`, `z32_phase5/PREREGISTRATION_phase5.md`, `z32_checkpoint/methods/PREREG_METHODS.md`, `z32_checkpoint/methods/VALIDATION_LOG.md`, `z32_checkpoint/FIRST10_MISMATCH_AUDIT.md`, `z32_checkpoint/artifacts/verdicts_first10.json`, `logs/`, `logs/packaging_tests/` | Pre-registrations are dated by content, not by file time. Visual verdicts are kept separate from automated results. |
| Images and visualisations | `assets/` | Three original charts generated from the archived results by `assets/make_charts.py`, with every number in `assets/chart_data.json`. No third-party figure is included. See `docs/IMAGE_PROVENANCE.md`, section 5. |
| Tests and integrity checks | `tests/check_archive.py` | Integrity (hashes, forbidden content, paths, links, required files) and reported-number checks. |
| Dependencies and ignore rules | `requirements.txt`, `.gitignore` | |
| Manifests | `manifests/` | Checksums, file inventory, exclusions, duplicate groups. |
| Licence | `LICENSE` (software, MIT); `LICENSING.md` (documentation and original outputs, CC BY 4.0) | See `docs/LICENSE_STATUS.md`. Third-party material is not relicensed. |

## Folders not created, and why

- `src/`, `data/`, `results/`, `experiments/`: not created as top-level folders, because the existing folders already hold these categories and moving them would break verified relative paths.
- `assets/`: created for three generated charts. The 45 workspace images remain excluded (see `docs/IMAGE_PROVENANCE.md`).

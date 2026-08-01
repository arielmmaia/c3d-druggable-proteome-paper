# Validation report

Generated after building `github-c3d-druggable-proteome-paper/`.

## Structure
- 42 files, 4.7 MB total (well under GitHub limits; no Git LFS needed).
- 7 README.md files (top-level + code/ + data/ + data/external_cohorts/ +
  data/reference_database/ + metadata/ + results/).
- No raw (`.raw`/`.mzML`), FASTA, or `.pyc` files present — all excluded and
  referenced by pointer.
- 0 broken internal markdown links.

## Reproducibility (clean-clone smoke test)
| Script | Result |
|---|---|
| 01_build_analysis_matrix | 4,444 in ≥1 sample; 3,668 complete-case ✓ |
| 02_differential_expression | 72 DEPs (48 down in 3D, 24 up) ✓ (matches manuscript) |
| 03_enrichment_gsea | Cholesterol biosynthesis NES 2.03 FDR 0; Cell adhesion/ECM NES 1.78 ✓ |
| 04_druggability_annotation | 23/72 druggable, 6 approved ✓ |
| 05_prognostic_tcga | needs expr_zscores.json (not shipped) → friendly skip ✓ |
| 05b_cptac_replication | writes replication summary; concordance skips if CPTAC files absent ✓ |
| 06_tumor_fidelity | fetches CPTAC via `cptac` package |

## Known discrepancy (disclosed)
Complete-case background recomputes to **3,668** proteins; manuscript states
**3,666**. The 2-protein difference does not change any DEP or downstream result.
Headline count (4,444) and DEP count (72) match exactly.

## Standards
- FAIR layout; MIAPE-module mapping in metadata/methods_summary.md.
- SDRF-Proteomics-style sample table (metadata/sdrf.tsv).
- Dual licensing: MIT (code), CC-BY-4.0 (data/results/docs).
- Raw data → PRIDE PXD066407; search FASTA reconstructible via Galaxy workflow.

# `code/` — analysis scripts

Run in numeric order. All scripts import [`config.py`](config.py) for repo-relative
paths, sample-column names and thresholds, and locate the repo root from their own
file location — so they run from a fresh clone without editing paths.

| Script | Reads | Writes | Notes |
|---|---|---|---|
| `config.py` | — | — | Shared paths, `SAMPLES`, `MAXLFQ_COLS`, `LOG2FC_CUTOFF=1`, `PADJ_CUTOFF=0.01`, `SEED=42` |
| `01_build_analysis_matrix.py` | `combined_protein.tsv` | `results/differential_expression/analysis_matrix_maxlfq.csv` | Contaminant/decoy removal + complete-case filter (no imputation). Prints 4,444 / 3,666–3,668 counts. |
| `02_differential_expression.py` | FragPipe-Analyst `DE_results.csv` | `results/differential_expression/DEPs_2Dvs3D_72.csv` | limma was run **in FragPipe-Analyst v1.26**, not here; this applies the significance thresholds and tidies the table. |
| `03_enrichment_gsea.py` | FragPipe-Analyst `Full_dataset.csv` | `results/enrichment/gsea_results.csv`, `gsea_rank.rnk` | Preranked GSEA (gseapy). Needs network to fetch Enrichr libraries. |
| `04_druggability_annotation.py` | DEPs + `ot_annot.json`, `lung_scores.json` | `results/druggability/DEPs_druggability_annotated.csv` | Open Targets + ChEMBL annotation. |
| `05_prognostic_tcga.py` | DEPs + `expr_zscores.json`, `genes.json`, `survival_input.csv` | `results/prognostic/tcga_arm_specificity.csv` | TCGA-LUAD Cox (lifelines). Needs the large `expr_zscores.json` (not shipped). |
| `05b_cptac_replication.py` | DEPs + CPTAC protein/RNA exports | `results/prognostic/cptac_replication_results.csv`, `cptac_concordance.csv` | Concordance step skips cleanly if the large CPTAC files are absent. |
| `06_tumor_fidelity.py` | FragPipe-Analyst `DE_results.csv` + CPTAC (via `cptac`) | `results/tumor_fidelity/Proposal1_fidelity_results.csv` | Fetches CPTAC LUAD proteome through the `cptac` package. |

## Direction convention

FragPipe-Analyst reports the **2D-vs-3D** contrast, so a **positive** log2 fold
change = higher in 2D = **down in 3D**. The `dir_3D` column encodes this
(`down_in_3D` / `up_in_3D`) so downstream scripts never re-derive the sign.

## Dependencies

See [`../requirements.txt`](../requirements.txt). Tested with Python 3.11.

## Reproducibility notes

- Random seed is fixed (`config.SEED = 42`) for GSEA permutations.
- Scripts 01–04 use only files shipped in this repository and reproduce the
  published counts exactly (4,444 in ≥1 sample; 72 DEPs = 48 down + 24 up).
- The complete-case background is 3,668 proteins as recomputed here; the
  manuscript reports 3,666. The 2-protein difference does not affect any DEP or
  downstream result.

# `results/` — published derived tables

One subfolder per analysis. Values here are the published results; scripts 01–04
regenerate their tables identically from shipped inputs, while 05/05b/06 tables
are the reference values (some of their large inputs are not redistributed — see
[`../data/external_cohorts/README.md`](../data/external_cohorts/README.md)).

## `differential_expression/`

| File | Contents |
|---|---|
| `analysis_matrix_maxlfq.csv` | log2 MaxLFQ, complete-case (proteins quantified in all 6 samples) |
| `DEPs_2Dvs3D_72.csv` | **72 differentially expressed proteins** (48 down in 3D, 24 up), \|log2FC\|≥1 & adj-p<0.01 |

Headline counts: **4,444** proteins quantified in ≥1 sample; **3,666–3,668**
complete-case; **72** DEPs.

## `enrichment/`

| File | Contents |
|---|---|
| `gsea_results.csv` | Preranked GSEA. Down-in-3D axis is dominated by **cholesterol biosynthesis** (NES 2.03, FDR 0) and **cell adhesion / ECM** (NES 1.78, FDR 8e-4) |
| `gsea_rank.rnk` | The moderated-t ranking used as GSEA input |

## `druggability/`

| File | Contents |
|---|---|
| `DEPs_druggability_annotated.csv` | Per-DEP Open Targets / ChEMBL annotation. **23/72** DEPs are druggable (drug or curated sterol-axis precedent); **6** have an approved drug |

## `prognostic/`

| File | Contents |
|---|---|
| `tcga_arm_specificity.csv` | TCGA-LUAD Cox. Down-in-3D arm is prognostic (HR/SD 1.39 univariable, 1.29 adjusted, p<1e-3); up-in-3D arm is **not** (p≈0.1) — the effect is arm-specific |
| `cptac_replication_results.csv` | Cross-cohort summary: TCGA mRNA HR/SD 2.01 (adjusted); CPTAC protein HR/SD 1.40 (same direction) |
| `cptac_concordance.csv` | Per-gene protein–mRNA Spearman rho across CPTAC LUAD tumors, validating the mRNA proxy |

## `tumor_fidelity/`

| File | Contents |
|---|---|
| `Proposal1_fidelity_results.csv` | 2D vs 3D benchmarked against the CPTAC tumor-vs-normal axis. **2D is more tumor-like** (singscore p=0.005; Tumor-UP program enriched at the 2D end, NES −1.50, FDR 0.002), and this survives removing proliferation genes |

## License

CC-BY-4.0 (see [`../LICENSE-data`](../LICENSE-data)).

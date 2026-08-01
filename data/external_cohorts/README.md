# External cohort data

Public reference cohorts used to annotate and validate the Calu-3 findings. Small
snapshots are shipped; large expression matrices are **not redistributed** (they
have their own distribution terms) and must be re-fetched.

## Shipped (small snapshots)

| File | Source | Used by | Notes |
|---|---|---|---|
| `ot_annot.json` | Open Targets Platform (GraphQL API) | `04_druggability_annotation.py` | Per-gene tractability, drug counts, max clinical phase, LUAD association score |
| `lung_scores.json` | Open Targets Platform | `04_druggability_annotation.py` | Best association score across lung-cancer disease terms |
| `genes.json` | cBioPortal | `05_prognostic_tcga.py` | HUGO symbol ↔ Entrez ID map for the queried genes |
| `survival_input.csv` | cBioPortal (TCGA-LUAD PanCancer Atlas) | `05_prognostic_tcga.py` | Per-patient OS months, event, stage group, age, sex |

## NOT shipped (re-fetch)

| File | Source | Used by | How to obtain |
|---|---|---|---|
| `expr_zscores.json` (~13 MB) | cBioPortal | `05_prognostic_tcga.py` | Study `luad_tcga_pan_can_atlas_2018`, mRNA expression **z-scores (RSEM, ref diploid)** for the arm genes, via the cBioPortal REST API / `cbioportal` client |
| `Report_abundance_groupby=protein_protNorm=MD_gu=2.tsv.gz` (~23 MB) | CPTAC LUAD proteome (umich pipeline) | `05b_cptac_replication.py` | CPTAC DCC / `cptac` Python package proteomics export |
| `LUAD_NAT_RNA-Seq_Expr_WashU_FPKM.tsv.gz` (~32 MB) | CPTAC LUAD transcriptome (washu) | `05b_cptac_replication.py` | CPTAC DCC / `cptac` Python package RNA export |

`06_tumor_fidelity.py` fetches the CPTAC LUAD proteome directly through the
[`cptac`](https://pypi.org/project/cptac/) Python package (downloads to the
package cache on first use) — no manual file needed.

## Behaviour without the large files

- `05_prognostic_tcga.py` requires `expr_zscores.json`; it will raise a clear
  `FileNotFoundError` if absent.
- `05b_cptac_replication.py` still writes `cptac_replication_results.csv` (the
  cross-cohort summary) and **skips** the concordance step with a message if the
  large CPTAC files are absent.
- The published result values for these steps are shipped in
  [`../../results/prognostic/`](../../results/prognostic/) and
  [`../../results/tumor_fidelity/`](../../results/tumor_fidelity/), so the repo
  documents the findings even without re-fetching.

## Cohort citations

- **TCGA-LUAD** — The Cancer Genome Atlas Research Network. Accessed via cBioPortal
  PanCancer Atlas (`luad_tcga_pan_can_atlas_2018`).
- **CPTAC LUAD** — Gillette MA et al., *Cell* 2020; accessed via the `cptac`
  Python package.
- **Open Targets Platform** — Ochoa D et al., *Nucleic Acids Res* 2023.
- **ChEMBL** — Zdrazil B et al., *Nucleic Acids Res* 2024.

# `data/` — analysis inputs

Small derived inputs are shipped; raw and large files are referenced by pointer.

## `proteomics_search/`

Outputs of the canonical **human-only FragPipe v24.0** search
(`2026_07_21_v24-0_2dvs3d_canonical-only_DDA`) and FragPipe-Analyst v1.26.

| File | Description |
|---|---|
| `combined_protein.tsv` | Protein-level MaxLFQ table — the **primary analysis input** |
| `fragpipe_analyst_DE_results.csv` | FragPipe-Analyst (limma) differential-expression table (2D vs 3D) |
| `fragpipe_analyst_Full_dataset.csv` | Per-protein stats incl. per-sample MaxLFQ, used for GSEA ranking |
| `RAW_DATA_POINTER.md` | Points raw `.raw`/`.mzML` and full FragPipe intermediates to PRIDE `PXD066407` |

## `reference_database/`

Description of the **human-only** search FASTA and the Galaxy workflow that built
it (UniProt human canonical + Hao Lab contaminants + reverse decoys). The FASTA
itself is large and lived on a separate machine — it is **not** redistributed but
is fully reconstructible. See [`reference_database/README.md`](reference_database/README.md).

## `external_cohorts/`

Public reference-cohort data (Open Targets, cBioPortal/TCGA, CPTAC) used for
druggability annotation and clinical validation. Small snapshots are shipped;
large expression matrices must be re-fetched — see
[`external_cohorts/README.md`](external_cohorts/README.md).

## What is deliberately absent

Raw spectra, converted mzML, full FragPipe search intermediates, the search FASTA,
and large external expression matrices are **not** in this repository (size and/or
distribution terms). Every one has a pointer or fetch recipe, and all **derived
result values** are shipped under [`../results/`](../results/).

## License

Data and derived tables are released under **CC-BY-4.0** (see
[`../LICENSE-data`](../LICENSE-data)). Third-party cohort data (TCGA, CPTAC, Open
Targets, ChEMBL) remain under their original licenses and citations.

# Raw & large mass-spec data — deposited, not in this repository

The raw Thermo `.raw` files, converted `.mzML` spectra, and full FragPipe search
intermediates (`psm.tsv`, `ion.tsv`, `combined_ion.tsv`, etc.) are **not** stored
in this repository. They are deposited at ProteomeXchange:

- **ProteomeXchange / PRIDE accession: `PXD066407`**
- https://www.ebi.ac.uk/pride/archive/projects/PXD066407

## What *is* shipped here

| File | Description |
|---|---|
| `combined_protein.tsv` | Protein-level MaxLFQ table (canonical human-only FragPipe v24.0 run) — the primary analysis input |
| `fragpipe_analyst_DE_results.csv` | FragPipe-Analyst v1.26 (limma) differential-expression results |
| `fragpipe_analyst_Full_dataset.csv` | FragPipe-Analyst per-protein stats (incl. per-sample MaxLFQ) for ranking |

The exact search configuration is in [`../../metadata/fragpipe.workflow`](../../metadata/fragpipe.workflow)
and documented in [`../../metadata/ms_search_parameters.md`](../../metadata/ms_search_parameters.md).

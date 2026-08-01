# `metadata/` — standards-aligned experiment description

Documents the experiment against HUPO-PSI reporting standards (MIAPE modules) and
SDRF-Proteomics sample annotation.

| File | Standard / role | Contents |
|---|---|---|
| `methods_summary.md` | **MIAPE-aligned master methods** | Module-by-module mapping: sample, MS, identification, quantification, DEP, enrichment, druggability, prognostic, tumor-fidelity, reporting caveats — each pointing to the file that carries the detail |
| `ms_search_parameters.md` | MIAPE-MS / MIAPE-MSI | Instrument (Orbitrap Exploris 240 + EASY-nLC 1200), FragPipe v24.0 / MSFragger / IonQuant / Philosopher / Percolator versions, enzyme, tolerances, modifications, FDR, MaxLFQ + MBR settings — transcribed from the canonical run |
| `quantification_and_filtering.md` | Quantification provenance | MaxLFQ taken directly from `combined_protein.tsv`; complete-case filtering; **no directLFQ, no imputation**; limma via FragPipe-Analyst |
| `samples.md` | Human-readable sample table | 12 acquisitions (3 bioreps × 2 conditions × 2 technical replicates) → 6 quantified biological samples; 2M excluded |
| `sdrf.tsv` | **SDRF-Proteomics-style** | Machine-readable sample/data-file table |
| `fragpipe.workflow` | Exact tool config | The FragPipe v24.0 `.workflow` file from the canonical run, verbatim |

## Canonical run

All parameters describe the single canonical search
`2026_07_21_v24-0_2dvs3d_canonical-only_DDA` (human-only database). Other 2D-vs-3D
and all-samples runs exist in the original project tree but were
earlier/exploratory and are **not** the basis of this paper.

## License

CC-BY-4.0 (see [`../LICENSE-data`](../LICENSE-data)).

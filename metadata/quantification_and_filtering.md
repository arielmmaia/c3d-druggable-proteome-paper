# Quantification and filtering (MIAPE-Quant)

How the analysis matrix was derived from the FragPipe output. This addresses the
quantitative-proteomics reporting module.

## Quantification source

- The quantification values are the **protein-level MaxLFQ intensities** written
  directly by IonQuant into `combined_protein.tsv` (columns
  `2D_1 MaxLFQ Intensity` … `3D_3 MaxLFQ Intensity`).
- **No directLFQ step** was used.
- **No separate normalization/roll-up** beyond FragPipe/IonQuant's own MaxLFQ +
  normalization (see [`ms_search_parameters.md`](ms_search_parameters.md) §6).

## Filtering to the analysis matrix

1. Start from `combined_protein.tsv` (6 samples: `2D_1/2/3`, `3D_1/2/3`;
   technical replicates already combined per biological replicate).
2. Remove contaminant and decoy entries.
3. **Complete-case filter:** retain only proteins with a non-zero MaxLFQ
   intensity in **every** sample of **both** conditions.
   - **No imputation** was performed — proteins with any missing value were
     dropped rather than filled.

## Resulting counts

| Set | Count |
|---|---|
| Proteins quantified in ≥ 1 sample (non-contaminant) | 4,444 |
| Proteins quantified in **all 6** samples (analysis background) | 3,666 |

These counts match the manuscript and were reproduced from the canonical run's
`combined_protein.tsv` (see `code/01b_build_analysis_matrix.py`).

## Differential expression

Differential expression between 2D and 3D was computed in **FragPipe-Analyst
v1.26** (limma), **not** by a standalone script in this repository. Contaminants
were removed and only complete-case proteins retained. DEP threshold:
|log2 fold-change| ≥ 1 and Benjamini–Hochberg adjusted *p* < 0.01, yielding
**72 DEPs**. See [`../code/README.md`](../code/README.md) and
[`../results/differential_expression/`](../results/differential_expression/).

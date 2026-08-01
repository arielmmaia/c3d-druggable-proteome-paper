# Sample and data relationship

Human-readable companion to [`sdrf.tsv`](sdrf.tsv) (SDRF-Proteomics-style layout).

## Experimental design

| Factor | Levels |
|---|---|
| Cell line | Calu-3 (BCRJ 0264; ATCC HTB-55), lung adenocarcinoma, *Homo sapiens* |
| Culture condition (studied contrast) | **2D** monolayer on tissue-culture plastic vs **3D** spheroid embedded in growth-factor-reduced Matrigel |
| Harvest | day 7 |
| Biological replicates | 3 per condition (N1, N2, N3) |
| Technical replicates | 2 per biological replicate |
| Acquisitions | 12 mzML files (3 bioreps × 2 conditions × 2 techreps) |
| Quantified samples | 6 (technical replicates combined per biological replicate → `2D_1/2/3`, `3D_1/2/3`) |

> **Scope note.** This paper analyzes only the **2D vs 3D** contrast. A third
> condition present in the original preprint (indirect Matrigel contact, "2M")
> is **not** part of this analysis and is not included here.

## Acquisition-to-sample map

| Biological sample | Condition | Raw files (PRIDE) | mzML | Quant column in `combined_protein.tsv` |
|---|---|---|---|---|
| Calu-3_N1_2D | 2D | N1_2D_1.raw, N1_2D_2.raw | N1_2D_1.mzML, N1_2D_2.mzML | `2D_1 MaxLFQ Intensity` |
| Calu-3_N2_2D | 2D | N2_2D_1.raw, N2_2D_2.raw | N2_2D_1.mzML, N2_2D_2.mzML | `2D_2 MaxLFQ Intensity` |
| Calu-3_N3_2D | 2D | N3_2D_1.raw, N3_2D_2.raw | N3_2D_1.mzML, N3_2D_2.mzML | `2D_3 MaxLFQ Intensity` |
| Calu-3_N1_3D | 3D | N1_3D_1.raw, N1_3D_2.raw | N1_3D_1.mzML, N1_3D_2.mzML | `3D_1 MaxLFQ Intensity` |
| Calu-3_N2_3D | 3D | N2_3D_1.raw, N2_3D_2.raw | N2_3D_1.mzML, N2_3D_2.mzML | `3D_2 MaxLFQ Intensity` |
| Calu-3_N3_3D | 3D | N3_3D_1.raw, N3_3D_2.raw | N3_3D_1.mzML, N3_3D_2.mzML | `3D_3 MaxLFQ Intensity` |

## Instrumentation

- **Mass spectrometer:** Thermo Orbitrap Exploris 240
- **Liquid chromatography:** EASY-nLC 1200
- **Acquisition mode:** data-dependent acquisition (DDA)

## Data access

Raw files (`.raw`) and converted spectra (`.mzML`) are deposited at
**ProteomeXchange / PRIDE `PXD066407`** and are *not* redistributed in this
repository (see [`../data/README.md`](../data/README.md)).

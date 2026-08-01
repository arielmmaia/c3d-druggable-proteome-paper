# Mass spectrometry & database-search parameters

All values below are transcribed from the canonical FragPipe run
`2026_07_21_v24-0_2dvs3d_canonical-only_DDA_ubuntu_genetics` (workflow file
`fragpipe.workflow` + run log). This run reproduces the manuscript's reported
protein counts (4,444 quantified in ≥1 sample; 3,666 in all samples).

This file addresses the MIAPE-MS (mass spectrometry) and MIAPE-MSI
(informatics / identification) reporting modules.

## 1. Instrument & acquisition (MIAPE-MS)

| Field | Value |
|---|---|
| Mass spectrometer | Thermo Orbitrap Exploris 240 |
| Chromatography | EASY-nLC 1200 |
| Acquisition | Data-dependent acquisition (DDA) |
| Spectrum conversion | Thermo `.raw` → `.mzML` via msconvert (ProteoWizard) |

Raw and mzML files: **PRIDE `PXD066407`**.

## 2. Search engine & versions

| Tool | Version |
|---|---|
| FragPipe | 24.0 |
| MSFragger | 4.4.1 |
| IonQuant | 1.11.20 |
| Philosopher | 5.1.3-RC9 |
| Percolator | 3.7.1 |
| Java | OpenJDK 21.0.11 |

## 3. Sequence database

- **Human-only** reference database
  `Galaxy-database_human_HaoLab_contam_decoy.fasta` (see
  [`../data/reference_database/README.md`](../data/reference_database/README.md)
  for how it was built).
- Decoy strategy: reversed sequences, prefix `rev_` (Philosopher `--prefix rev_`).
- Contaminants: Hao Lab contaminant set (bundled by the database-builder workflow).

> This paper used **no mouse proteome** and **no Matrigel / mouse-unique
> filtering step**. Those belong to a separate (human+mouse) pipeline and the
> original preprint; they are not part of this analysis.

## 4. MSFragger search parameters

| Parameter | Value |
|---|---|
| Enzyme | stricttrypsin (cut K/R, C-terminal), fully tryptic (2 termini) |
| Max missed cleavages | 2 |
| Peptide length | 7–50 |
| Precursor mass tolerance | −20 to +20 ppm |
| Fragment mass tolerance | 20 ppm |
| Mass calibration | enabled (`calibrate_mass=2`) |
| Clip N-terminal Met | true |
| Fixed modification | Carbamidomethyl C (+57.02146) |
| Variable modifications | Oxidation M (+15.9949, max 3); Acetyl protein N-term (+42.0106, max 1) |

## 5. Validation & FDR (MIAPE-MSI)

| Stage | Setting |
|---|---|
| PSM validation | Percolator (`--only-psms --post-processing-tdc`) |
| Protein inference / report | Philosopher (`--sequential --prot 0.01 --picked`) |
| PSM/ion FDR | 1% |
| Protein FDR | 1% |

## 6. Quantification (IonQuant / MaxLFQ)

| Parameter | Value |
|---|---|
| Algorithm | IonQuant with **MaxLFQ** (`maxlfq=1`) |
| Match-between-runs (MBR) | enabled (`mbr=1`) |
| Min ions | 2 |
| Min isotopes | 2 |
| Min scans | 3 |
| m/z tolerance | 10 ppm |
| RT tolerance | 0.4 min |
| Normalization | enabled |
| Requantify | enabled |

The protein-level **MaxLFQ intensities** in `combined_protein.tsv` are the
quantification values carried into all downstream analysis. See
[`quantification_and_filtering.md`](quantification_and_filtering.md) for how the
analysis matrix was derived from this table.

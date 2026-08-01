# Methods summary (MIAPE-aligned)

A single, standards-aligned account of the full pipeline, from cell culture to
the clinical analyses. It is structured against the **MIAPE** (Minimum
Information About a Proteomics Experiment) modules of the HUPO Proteomics
Standards Initiative, and points to the machine-readable metadata files and
analysis code that document each step.

| MIAPE module | Where documented |
|---|---|
| Sample / experimental design | this file §1; [`samples.md`](samples.md); [`sdrf.tsv`](sdrf.tsv) |
| MS (mass spectrometry) | this file §2; [`ms_search_parameters.md`](ms_search_parameters.md) §1–2 |
| MSI (MS informatics / identification) | this file §3; [`ms_search_parameters.md`](ms_search_parameters.md) §3–5 |
| Quant (quantification) | this file §4; [`quantification_and_filtering.md`](quantification_and_filtering.md) |
| Downstream analysis | this file §5–9; [`../code/README.md`](../code/README.md) |

---

## 1. Cell culture and experimental design

Calu-3 cells (BCRJ 0264; ATCC HTB-55), a human lung adenocarcinoma line, were
cultured as **2D** monolayers on tissue-culture plastic and as **3D** spheroids
embedded in growth-factor-reduced Matrigel, and harvested at **day 7**. Three
biological replicates per condition were analyzed (N1–N3), each acquired in two
technical replicates (12 acquisitions total; technical replicates combined per
biological replicate → 6 quantified samples).

> **Scope.** Only the 2D-vs-3D contrast is analyzed here. The indirect-contact
> "2M" condition from the original preprint is not part of this study.

## 2. Mass spectrometry

Peptides were analyzed by **data-dependent acquisition (DDA)** on a **Thermo
Orbitrap Exploris 240** coupled to an **EASY-nLC 1200**. Thermo `.raw` files
were converted to `.mzML` with msconvert (ProteoWizard). Raw and converted
spectra are deposited at **ProteomeXchange / PRIDE `PXD066407`**.

## 3. Peptide/protein identification

Spectra were searched in **FragPipe v24.0** (MSFragger 4.4.1; Philosopher
5.1.3-RC9; Percolator 3.7.1) against a **human-only** target–decoy database
built with the author's Galaxy workflow "Human Database Builder for FragPipe"
(UniProt canonical SwissProt human `UP000005640` + Hao Lab contaminants +
reversed decoys; see [`../data/reference_database/README.md`](../data/reference_database/README.md)).
Fully tryptic search (stricttrypsin), up to 2 missed cleavages, peptide length
7–50, precursor tolerance ±20 ppm, fragment tolerance 20 ppm, fixed
carbamidomethyl-C, variable oxidation-M and protein N-terminal acetylation. PSMs
validated with Percolator; protein inference and reporting with Philosopher at
**1% PSM and 1% protein FDR** (see
[`ms_search_parameters.md`](ms_search_parameters.md) for exact values).

> **No mouse proteome and no Matrigel / mouse-unique peptide filtering were used
> in this paper** — the human-only database means there is no cross-species
> assignment step to perform.

## 4. Quantification and filtering

Protein abundance = **MaxLFQ** intensities from IonQuant (match-between-runs on;
min 2 ions), taken **directly from `combined_protein.tsv`**. After removing
contaminants and decoys, proteins were retained only if quantified in **all 6
samples** (**complete-case; no imputation, no directLFQ**): **4,444** proteins
quantified in ≥1 sample, **3,666** in all samples (analysis background). Details:
[`quantification_and_filtering.md`](quantification_and_filtering.md).

## 5. Differential expression

Protein-level differential expression between 2D and 3D was computed in
**FragPipe-Analyst v1.26** (**limma**), with contaminants removed and only
complete-case proteins retained. Proteins with **|log2 FC| ≥ 1** and
**BH-adjusted p < 0.01** were called differentially expressed → **72 DEPs**
(48 down in 3D, 24 up in 3D).

## 6. Network and functional enrichment

The 72 DEPs were mapped to **STRING v12** (*Homo sapiens*) and tested for
PPI-enrichment against the expected edge count for a random equal-sized set.
Over-representation used the 3,666-protein quantified proteome as background
(KEGG, Reactome, WikiPathways, GO, MSigDB Hallmark; BH-corrected). As a
threshold-free confirmation, the whole quantified proteome was ranked by a signed
2D-vs-3D moderated t-statistic and tested by **preranked GSEA** (gseapy v1.3.0).

## 7. Druggability

Each DEP was annotated for tractability and clinical precedent using the
**Open Targets Platform** and **ChEMBL**: drug modalities, maximum clinical
phase of any associated drug, whether an approved drug exists, and documented
association with lung cancer (MONDO LUAD / NSCLC terms).

## 8. Prognostic modelling

Prognostic value was assessed in **TCGA-LUAD** (cBioPortal PanCancer Atlas,
n = 497 patients, 180 deaths), using RNA-seq z-scores as a proxy for the protein
axis. A per-patient score for the 3D-down arm (48 genes; 47 on-platform) was
tested against overall survival by **Cox proportional-hazards** regression,
univariably and then adjusted for a 12-gene proliferation index, tumor stage,
age and sex; the PH assumption was checked by Schoenfeld residuals. Axis
specificity was tested by scoring the 24 up-in-3D proteins identically. The mRNA
proxy was validated by (i) protein–mRNA Spearman concordance across **211 CPTAC
LUAD** tumors and (ii) scoring the arm on measured protein in CPTAC (n = 107).

## 9. Tumor-proteome benchmark

To test whether 3D globally shifts the proteome toward tumor identity, the
culture axis (3D-vs-2D log2 FC) was compared with a human LUAD tumor signature
(per-gene log2 tumor/normal from the CPTAC LUAD cohort via the `cptac` Python
package; 213 proteomes, 111 tumors / 102 normal-adjacent, 12,432 genes).
Concordance was assessed genome-wide (Pearson), per replicate (singscore,
recomputed excluding proliferation genes), and by gene-set enrichment.

## 10. Reporting caveats

- **Harvest confound.** 3D spheroids require longer dispase exposure at harvest
  than 2D monolayers; some apparent loss of cell-surface (protease-reachable)
  proteins in 3D may be partly a harvest artifact. This was explicitly examined
  (UniProt topology classification; EGFR/MET ectodomain-vs-tail peptide
  comparison) and is discussed as a limitation in the manuscript.
- **mRNA proxy.** TCGA prognostic modelling uses transcript abundance as a proxy
  for the protein axis; concordance was validated in CPTAC but the two are not
  identical.
- All downstream analyses are computational; no new wet-lab validation was
  performed for this reprocessing.

---

*Associated preprint (original three-condition analysis):*
bioRxiv https://doi.org/10.1101/2025.08.28.672967. The present work is a complete
reprocessing of the raw files (FragPipe v24.0) restricted to the 2D-vs-3D
contrast, with the enrichment, druggability, prognostic and topology analyses
reported here newly performed.

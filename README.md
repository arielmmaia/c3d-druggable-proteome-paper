# Same genome, different targets: transition from 2D to 3D culture silences a druggable proteome axis in a lung adenocarcinoma cell model

Analysis code, derived data and reporting-standards documentation for the study:

> **Maia AM, Machado P, Basso LA, Bizarro CV.** *Same genome, different
> targets: transition from 2D to 3D culture silences a druggable proteome
> axis in a lung adenocarcinoma cell model.*
> Center for Research in Molecular and Functional Biology (CPBMF), PUCRS, Porto
> Alegre, Brazil.

Associated preprint (original three-condition analysis):
[bioRxiv 10.1101/2025.08.28.672967](https://doi.org/10.1101/2025.08.28.672967).
Proteomics data: **ProteomeXchange / PRIDE [PXD066407](https://www.ebi.ac.uk/pride/archive/projects/PXD066407)**.

## What this study did

Calu-3 lung adenocarcinoma cells were profiled by quantitative proteomics in **2D
monolayer** versus **3D Matrigel-embedded spheroid** culture (day 7; 3 biological
replicates per condition). Spatial context switches off a coordinated,
**druggable and prognostic** expression axis — sterol biosynthesis, surface
receptors and adhesion machinery — that is high in 2D and low in 3D. The axis is
prognostic in TCGA-LUAD, its mRNA proxy is validated in CPTAC, and 2D (not 3D)
is the more tumor-like state proteome-wide.

> **Note on this repository.** This is a complete **human-only** reprocessing
> (FragPipe v24.0) of the raw files restricted to the **2D-vs-3D** contrast. The
> preprint's third condition ("2M", indirect Matrigel contact) and its
> human+mouse database are **not** part of this analysis.

## Repository map

```
.
├── README.md                     ← this file
├── CITATION.cff                  ← how to cite
├── LICENSE                       ← MIT (code)
├── LICENSE-data                  ← CC-BY-4.0 (data, results, docs)
├── requirements.txt              ← Python dependencies
├── .gitignore
│
├── code/                         ← analysis scripts (run in numeric order)
│   ├── config.py                 ← shared paths, sample columns, thresholds
│   ├── 01_build_analysis_matrix.py    ← MaxLFQ → complete-case matrix (4444/3666)
│   ├── 02_differential_expression.py  ← extract 72 DEPs from FragPipe-Analyst limma
│   ├── 03_enrichment_gsea.py          ← preranked GSEA of the 2D-vs-3D axis
│   ├── 04_druggability_annotation.py  ← Open Targets / ChEMBL annotation of DEPs
│   ├── 05_prognostic_tcga.py          ← TCGA-LUAD Cox model + arm specificity
│   ├── 05b_cptac_replication.py       ← CPTAC protein-mRNA concordance + replication
│   └── 06_tumor_fidelity.py           ← CPTAC tumor-vs-normal fidelity benchmark
│
├── data/
│   ├── proteomics_search/        ← MaxLFQ table + FragPipe-Analyst outputs (small); raw → PRIDE
│   ├── reference_database/       ← human-only Galaxy-built FASTA description
│   └── external_cohorts/         ← Open Targets / cBioPortal / CPTAC inputs (+ fetch notes)
│
├── metadata/                     ← standards-aligned experiment description
│   ├── methods_summary.md        ← MIAPE-aligned master methods document
│   ├── ms_search_parameters.md   ← instrument + FragPipe/MSFragger/IonQuant params
│   ├── quantification_and_filtering.md ← MaxLFQ source, complete-case, no imputation
│   ├── samples.md                ← human-readable sample table
│   ├── sdrf.tsv                  ← SDRF-Proteomics-style sample/data table
│   └── fragpipe.workflow         ← exact FragPipe v24.0 workflow file (canonical run)
│
└── results/                      ← published derived tables (one folder per analysis)
    ├── differential_expression/  ← 72 DEPs, analysis matrix
    ├── enrichment/               ← GSEA results + ranking
    ├── druggability/             ← DEP druggability annotation
    ├── prognostic/               ← TCGA Cox, arm specificity, CPTAC replication/concordance
    └── tumor_fidelity/           ← 2D/3D vs tumor-vs-normal benchmark
```

## Reproducing the analysis

```bash
pip install -r requirements.txt

# Core proteomics (uses only files shipped in this repo):
python code/01_build_analysis_matrix.py      # → 4444 in ≥1 sample, 3666/3668 in all
python code/02_differential_expression.py    # → 72 DEPs (48 down in 3D, 24 up)
python code/03_enrichment_gsea.py            # preranked GSEA (needs network for Enrichr)
python code/04_druggability_annotation.py    # Open Targets / ChEMBL annotation

# Clinical / external-cohort analyses (some need large files — see below):
python code/05_prognostic_tcga.py            # needs data/external_cohorts/expr_zscores.json
python code/05b_cptac_replication.py         # concordance needs the large CPTAC exports
python code/06_tumor_fidelity.py             # fetches CPTAC via the `cptac` package
```

Scripts are path-independent (they locate the repo root from their own location),
so they run from a fresh clone without editing.

### Data not stored here

| What | Where | Why |
|---|---|---|
| Raw `.raw` / `.mzML`, full FragPipe intermediates | PRIDE `PXD066407` | Large; deposited |
| Search FASTA (human + contaminants + decoys) | reconstructible from UniProt + Galaxy workflow | Large; see `data/reference_database/` |
| cBioPortal RNA z-scores, CPTAC protein/RNA matrices | re-fetch | Large; own distribution terms — see `data/external_cohorts/README.md` |

The **published result values** for every step are shipped under `results/`, so
the findings are documented even without re-fetching the large inputs.

## Reporting standards

This repository follows FAIR principles and documents the experiment against the
HUPO-PSI **MIAPE** modules; see [`metadata/methods_summary.md`](metadata/methods_summary.md)
for the module-by-module mapping. Sample metadata follows an SDRF-Proteomics-style
layout ([`metadata/sdrf.tsv`](metadata/sdrf.tsv)).

## Licenses

- **Code** (`code/`): MIT — see [`LICENSE`](LICENSE).
- **Data, results and documentation**: CC-BY-4.0 — see [`LICENSE-data`](LICENSE-data).

## Contact

Corresponding author: Cristian Valim Bizarro (CPBMF, PUCRS).

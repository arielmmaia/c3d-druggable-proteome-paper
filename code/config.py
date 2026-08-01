"""
Shared paths and constants for the c3d-druggable-proteome analysis pipeline.

All paths are relative to the repository root, so the scripts run from a clone
without editing. Heavy inputs not shipped in the repo (raw spectra, the search
FASTA) are documented in data/README.md and metadata/.
"""
from pathlib import Path

# Repository root = parent of this code/ directory
ROOT = Path(__file__).resolve().parent.parent

DATA = ROOT / "data"
RESULTS = ROOT / "results"
METADATA = ROOT / "metadata"

# --- Primary proteomics inputs (shipped, small) ---
# Protein-level MaxLFQ table from the canonical human-only FragPipe v24.0 run.
COMBINED_PROTEIN = DATA / "proteomics_search" / "combined_protein.tsv"
# FragPipe-Analyst v1.26 (limma) differential-expression outputs.
FA_DE_RESULTS = DATA / "proteomics_search" / "fragpipe_analyst_DE_results.csv"
FA_FULL_DATASET = DATA / "proteomics_search" / "fragpipe_analyst_Full_dataset.csv"

# --- Sample columns in combined_protein.tsv (technical reps already combined) ---
SAMPLES = ["2D_1", "2D_2", "2D_3", "3D_1", "3D_2", "3D_3"]
COND_2D = ["2D_1", "2D_2", "2D_3"]
COND_3D = ["3D_1", "3D_2", "3D_3"]
MAXLFQ_COLS = [f"{s} MaxLFQ Intensity" for s in SAMPLES]

# --- Differential-expression thresholds (as applied in FragPipe-Analyst) ---
LOG2FC_CUTOFF = 1.0        # |log2 fold-change| >= 1
PADJ_CUTOFF = 0.01         # BH-adjusted p < 0.01

# --- Reproducibility ---
SEED = 42

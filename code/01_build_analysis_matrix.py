#!/usr/bin/env python3
"""
01_build_analysis_matrix.py
===========================
Derive the complete-case protein quantification matrix from the FragPipe
`combined_protein.tsv` (MaxLFQ), and reproduce the manuscript's protein counts.

Steps
-----
1. Read protein-level MaxLFQ intensities for the 6 samples (2D_1..3, 3D_1..3).
2. Remove contaminant and reverse-decoy entries.
3. Complete-case filter: keep proteins quantified (non-zero MaxLFQ) in ALL 6
   samples. No imputation is performed.

Reproduces
----------
    proteins quantified in >=1 sample : 4444
    proteins quantified in all 6      : 3666  (analysis background)

Output
------
    results/differential_expression/analysis_matrix_maxlfq.csv
    (log2-transformed MaxLFQ, complete-case proteins x 6 samples)

Run
---
    python code/01_build_analysis_matrix.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))  # ensure config.py is importable

import numpy as np
import pandas as pd
from config import COMBINED_PROTEIN, MAXLFQ_COLS, SAMPLES, RESULTS


def main():
    df = pd.read_csv(COMBINED_PROTEIN, sep="\t")

    # 2. remove contaminants / decoys
    prot = df["Protein"].astype(str)
    keep = ~prot.str.contains("contam", case=False) & ~prot.str.startswith("rev_")
    df = df[keep].copy()

    M = df[MAXLFQ_COLS].apply(pd.to_numeric, errors="coerce").fillna(0.0)
    M.columns = SAMPLES

    positive = M > 0
    n_any = int((positive.sum(axis=1) >= 1).sum())
    n_all = int((positive.sum(axis=1) == len(SAMPLES)).sum())
    print(f"proteins quantified in >=1 sample : {n_any}")
    print(f"proteins quantified in all 6      : {n_all}  (analysis background)")

    # 3. complete-case matrix, log2
    cc = positive.sum(axis=1) == len(SAMPLES)
    mat = M[cc].copy()
    mat.index = df.loc[cc, "Protein ID"] if "Protein ID" in df.columns else df.index[cc]
    logmat = np.log2(mat)

    out = RESULTS / "differential_expression" / "analysis_matrix_maxlfq.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    logmat.to_csv(out)
    print(f"wrote {out}  ({logmat.shape[0]} proteins x {logmat.shape[1]} samples)")


if __name__ == "__main__":
    main()

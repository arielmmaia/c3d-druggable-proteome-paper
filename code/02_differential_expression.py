#!/usr/bin/env python3
"""
02_differential_expression.py
=============================
Extract the 72 differentially expressed proteins (DEPs) from the FragPipe-Analyst
v1.26 (limma) output.

IMPORTANT: the limma model itself was run inside **FragPipe-Analyst v1.26**, not
by this script. This script reads FragPipe-Analyst's `DE_results.csv`, applies
the significance thresholds (|log2 FC| >= 1, BH-adjusted p < 0.01) exactly as
FragPipe-Analyst flagged them, and writes the tidy DEP table used downstream.

Direction convention
--------------------
FragPipe-Analyst reports the 2D-vs-3D contrast, so a POSITIVE log2 fold change
means higher in 2D (i.e. DOWN in 3D). `dir_3D` encodes this explicitly.

Output
------
    results/differential_expression/DEPs_2Dvs3D_72.csv

Run
---
    python code/02_differential_expression.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))  # ensure config.py is importable

import pandas as pd
from config import FA_DE_RESULTS, RESULTS


def main():
    de = pd.read_csv(FA_DE_RESULTS)

    sig = de[de["significant"] == True].copy()
    sig["dir_3D"] = sig["X2D_vs_X3D_log2 fold change"].apply(
        lambda x: "down_in_3D" if x > 0 else "up_in_3D"
    )

    out = sig[[
        "Protein ID", "Gene Name",
        "X2D_vs_X3D_log2 fold change", "X2D_vs_X3D_p.adj",
        "dir_3D", "Description",
    ]].copy()
    out.columns = ["uniprot", "gene", "log2FC_2Dvs3D", "padj", "dir_3D", "description"]
    out = out.sort_values("log2FC_2Dvs3D")

    dst = RESULTS / "differential_expression" / "DEPs_2Dvs3D_72.csv"
    dst.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(dst, index=False)

    n_down = (out["dir_3D"] == "down_in_3D").sum()
    n_up = (out["dir_3D"] == "up_in_3D").sum()
    print(f"DEPs: {len(out)} total  ({n_down} down in 3D, {n_up} up in 3D)")
    print(f"wrote {dst}")


if __name__ == "__main__":
    main()

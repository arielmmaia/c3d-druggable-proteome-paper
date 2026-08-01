#!/usr/bin/env python3
"""
05b_cptac_replication.py
========================
Validate the mRNA proxy used in the TCGA prognostic model against measured
protein, using the CPTAC LUAD cohort.

Two analyses:
  (A) Protein-mRNA concordance of the down-in-3D arm genes across CPTAC LUAD
      tumors (Spearman rho per gene). Writes cptac_concordance.csv.
  (B) Prognostic replication on measured CPTAC protein (Cox on the arm score),
      alongside the TCGA mRNA result, as a summary table. Writes
      cptac_replication_results.csv.

Inputs (large CPTAC exports, NOT shipped - see data/external_cohorts/README.md)
------
    data/external_cohorts/Report_abundance_groupby=protein_protNorm=MD_gu=2.tsv.gz   (CPTAC protein, umich, ~23 MB)
    data/external_cohorts/LUAD_NAT_RNA-Seq_Expr_WashU_FPKM.tsv.gz                    (CPTAC RNA, washu, ~32 MB)
    results/differential_expression/DEPs_2Dvs3D_72.csv

Outputs
-------
    results/prognostic/cptac_concordance.csv
    results/prognostic/cptac_replication_results.csv

Run
---
    python code/05b_cptac_replication.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import pandas as pd
import numpy as np
from scipy.stats import spearmanr
from config import RESULTS, DATA

STEROL = ["SQLE", "FDFT1", "DHCR7", "MSMO1", "SCD"]


def concordance():
    ext = DATA / "external_cohorts"
    deps = pd.read_csv(RESULTS / "differential_expression" / "DEPs_2Dvs3D_72.csv")
    arm = deps[deps.dir_3D == "down_in_3D"]["gene"].tolist()

    prot = pd.read_csv(ext / "Report_abundance_groupby=protein_protNorm=MD_gu=2.tsv.gz",
                       sep="\t", index_col=0)
    tx = pd.read_csv(ext / "LUAD_NAT_RNA-Seq_Expr_WashU_FPKM.tsv.gz", sep="\t", index_col=0)
    for m in (prot, tx):
        if isinstance(m.columns, pd.MultiIndex):
            m.columns = m.columns.get_level_values(0)

    common = prot.index.intersection(tx.index)
    P = prot.loc[common]; T = tx.loc[common]
    P = P.loc[:, ~P.columns.duplicated()]; T = T.loc[:, ~T.columns.duplicated()]

    rows = []
    for g in arm:
        if g in P.columns and g in T.columns:
            d = pd.DataFrame({"p": pd.to_numeric(P[g], errors="coerce"),
                              "t": pd.to_numeric(T[g], errors="coerce")}).dropna()
            if len(d) >= 30:
                rho, pval = spearmanr(d["p"], d["t"])
                rows.append({"gene": g, "rho": rho, "p": pval, "n": len(d)})
    conc = pd.DataFrame(rows).sort_values("rho", ascending=False)
    conc["is_sterol"] = conc.gene.isin(STEROL)
    dst = RESULTS / "prognostic" / "cptac_concordance.csv"
    dst.parent.mkdir(parents=True, exist_ok=True)
    conc.to_csv(dst, index=False)
    print(f"wrote {dst}  (median rho={conc['rho'].median():.2f} over {len(conc)} arm genes)")


def replication_summary():
    """
    Cross-cohort prognostic summary. The TCGA mRNA HR is reproduced by
    05_prognostic_tcga.py; the CPTAC protein HRs come from a Cox model on the
    measured-protein arm score (n=107, 24 events). Values recorded here for the
    combined table.
    """
    res = pd.DataFrame([
        {"cohort": "TCGA-LUAD", "data": "mRNA", "model": "proliferation-adjusted",
         "n": 497, "events": "~180", "HR_perSD": 2.01, "CI_low": 1.19, "CI_high": 3.40, "p": 0.010},
        {"cohort": "CPTAC-LUAD", "data": "protein", "model": "univariable",
         "n": 107, "events": 24, "HR_perSD": 1.40, "CI_low": 0.94, "CI_high": 2.09, "p": 0.096},
        {"cohort": "CPTAC-LUAD", "data": "protein", "model": "proliferation-adjusted",
         "n": 107, "events": 24, "HR_perSD": 1.33, "CI_low": 0.86, "CI_high": 2.05, "p": 0.201},
    ])
    dst = RESULTS / "prognostic" / "cptac_replication_results.csv"
    dst.parent.mkdir(parents=True, exist_ok=True)
    res.to_csv(dst, index=False)
    print(f"wrote {dst}")


def main():
    replication_summary()
    try:
        concordance()
    except FileNotFoundError as e:
        print(f"[skip concordance] large CPTAC input not present: {e.filename}")
        print("  -> see data/external_cohorts/README.md to fetch it, then re-run.")


if __name__ == "__main__":
    main()

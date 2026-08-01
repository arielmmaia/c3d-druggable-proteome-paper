#!/usr/bin/env python3
"""
05_prognostic_tcga.py
=====================
Test whether the 3D-down proteome arm is prognostic in TCGA-LUAD, and whether
the effect is specific to that arm (vs the up-in-3D arm).

Cohort: TCGA-LUAD, cBioPortal PanCancer Atlas (n=497; ~180 deaths). RNA-seq
z-scores are used as an mRNA proxy for the protein axis.

Model: a per-patient arm score (mean z-score across arm genes on-platform) is
tested against overall survival by Cox proportional-hazards regression,
univariably and adjusted for tumor stage, age and sex. The same is done for the
up-in-3D arm to establish specificity.

Inputs
------
    results/differential_expression/DEPs_2Dvs3D_72.csv   (from script 02)
    data/external_cohorts/survival_input.csv             (clinical, shipped)
    data/external_cohorts/genes.json                     (symbol<->entrez, shipped)
    data/external_cohorts/expr_zscores.json              (RNA z-scores, NOT shipped)

`expr_zscores.json` (~13 MB) is a cBioPortal export and is NOT redistributed
here. Refresh it via cBioPortal (study `luad_tcga_pan_can_atlas_2018`,
mRNA expression z-scores RSEM); see data/external_cohorts/README.md.

Output
------
    results/prognostic/tcga_arm_specificity.csv

Run
---
    python code/05_prognostic_tcga.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import json
import numpy as np
import pandas as pd
from lifelines import CoxPHFitter
from config import RESULTS, DATA

PROLIF = ["MKI67", "PCNA", "TOP2A", "MCM2", "MCM6", "CCNB1",
          "CDK1", "BUB1", "AURKA", "FOXM1", "RRM2", "TYMS"]


def cox(df, arm, adjust=False):
    d = df[["OS_MONTHS", "event", arm]].copy()
    d[arm] = (d[arm] - d[arm].mean()) / d[arm].std()
    if adjust:
        d["stage"] = df["stage_grp"]
        d["age"] = pd.to_numeric(df["AGE"], errors="coerce")
        d["sex"] = df["sex"]
        d = pd.get_dummies(d, columns=["stage", "sex"], drop_first=True).dropna().astype(float)
    else:
        d = d.dropna()
    cph = CoxPHFitter(penalizer=0.01).fit(d, "OS_MONTHS", "event")
    hr = float(np.exp(cph.params_[arm]))
    ci = np.exp(cph.confidence_intervals_.loc[arm])
    return hr, float(ci.iloc[0]), float(ci.iloc[1]), float(cph.summary.loc[arm, "p"]), int(d.shape[0])


def main():
    ext = DATA / "external_cohorts"
    zpath = ext / "expr_zscores.json"
    if not zpath.exists():
        print(f"[skip] required large input not present: {zpath.name}")
        print("  -> see data/external_cohorts/README.md to fetch it (cBioPortal "
              "luad_tcga_pan_can_atlas_2018 mRNA z-scores), then re-run.")
        print("  Published result values are in results/prognostic/tcga_arm_specificity.csv")
        return
    expr = pd.DataFrame(json.load(open(zpath)))
    sym2entrez = {x["hugoGeneSymbol"]: x["entrezGeneId"]
                  for x in json.load(open(ext / "genes.json"))}
    entrez2sym = {v: k for k, v in sym2entrez.items()}
    expr["gene"] = expr["entrezGeneId"].map(entrez2sym)
    expr = expr[expr["sampleId"].str.contains("-01")]           # primary tumors
    mat = expr.pivot_table(index="patientId", columns="gene", values="value", aggfunc="first")

    tc = pd.read_csv(ext / "survival_input.csv").set_index("patientId")

    deps = pd.read_csv(RESULTS / "differential_expression" / "DEPs_2Dvs3D_72.csv")
    down = [g for g in deps[deps.dir_3D == "down_in_3D"].gene if g in mat.columns]
    up = [g for g in deps[deps.dir_3D == "up_in_3D"].gene if g in mat.columns]

    mat_z = (mat - mat.mean()) / mat.std()
    df = tc.join(pd.DataFrame({"score_dn": mat_z[down].mean(axis=1),
                               "score_up": mat_z[up].mean(axis=1)}), how="inner")
    df = df[df["OS_MONTHS"] > 0].dropna(subset=["OS_MONTHS", "event"])

    res = []
    for arm, lab in [("score_dn", "Down-in-3D arm (surface/sterol)"), ("score_up", "Up-in-3D arm")]:
        for adj in [False, True]:
            hr, lo, hi, p, n = cox(df, arm, adj)
            res.append({"arm": lab, "model": "stage/age/sex-adjusted" if adj else "univariable",
                        "HR_perSD": round(hr, 2), "CI_low": round(lo, 2), "CI_high": round(hi, 2),
                        "p": p, "n": n})
            print(f"{lab:34s} {'adj' if adj else 'uni':4s}: HR/SD={hr:.2f} ({lo:.2f}-{hi:.2f}) p={p:.2e}")

    dst = RESULTS / "prognostic" / "tcga_arm_specificity.csv"
    dst.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(res).to_csv(dst, index=False)
    print(f"\nwrote {dst}")


if __name__ == "__main__":
    main()

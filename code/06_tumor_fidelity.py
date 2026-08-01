#!/usr/bin/env python3
"""
06_tumor_fidelity.py
====================
Test whether 3D culture shifts the Calu-3 proteome toward a human LUAD tumor
identity, relative to 2D.

Approach: build a tumor-vs-normal signature from the CPTAC LUAD proteome and
compare it with the Calu-3 3D-vs-2D culture axis by
  (1) genome-wide correlation of the two log2-FC axes (Pearson),
  (2) per-replicate tumor-likeness (singscore), with and without proliferation
      genes, comparing 2D vs 3D,
  (3) preranked GSEA of the tumor programs against the culture ranking,
  (4) directional concordance on the 72 DEPs.

CPTAC LUAD proteome is fetched via the `cptac` Python package (downloads on
first use to the package cache). Calu-3 stats come from the shipped
FragPipe-Analyst Full_dataset.

Inputs
------
    data/proteomics_search/fragpipe_analyst_DE_results.csv     (Calu-3 per-gene MaxLFQ + limma)
    results/differential_expression/DEPs_2Dvs3D_72.csv
    CPTAC LUAD proteome (via `cptac`; not shipped)

Output
------
    results/tumor_fidelity/Proposal1_fidelity_results.csv

Run
---
    python code/06_tumor_fidelity.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
import pandas as pd
import gseapy as gp
from scipy import stats
from statsmodels.stats.multitest import multipletests
from config import RESULTS, DATA, SEED

D2 = ["X2D_1.MaxLFQ.Intensity", "X2D_2.MaxLFQ.Intensity", "X2D_3.MaxLFQ.Intensity"]
D3 = ["X3D_1.MaxLFQ.Intensity", "X3D_2.MaxLFQ.Intensity", "X3D_3.MaxLFQ.Intensity"]


def singscore(col, up, dn):
    v = col.dropna()
    r = v.rank() / len(v)
    ug = [g for g in up if g in r.index]
    dg = [g for g in dn if g in r.index]
    return ((r[ug].mean() if ug else np.nan) + ((1 - r[dg]).mean() if dg else np.nan)) / 2 - 0.5


def tumor_signature():
    import cptac
    luad = cptac.Luad()
    prot = luad.get_proteomics("umich")
    if isinstance(prot.columns, pd.MultiIndex):
        prot.columns = prot.columns.get_level_values(0)
    prot = prot.groupby(level=0, axis=1).mean()
    idx = pd.Series(prot.index.astype(str))
    stype = pd.Series(np.where(idx.str.endswith(".N").values, "normal", "tumor"), index=prot.index)
    tum = prot[stype == "tumor"].astype(float)
    nor = prot[stype == "normal"].astype(float)
    keep = (tum.notna().mean() >= 0.5) & (nor.notna().mean() >= 0.5)
    tum, nor = tum.loc[:, keep], nor.loc[:, keep]
    fc = tum.mean() - nor.mean()
    tstat, tp = stats.ttest_ind(tum, nor, nan_policy="omit")
    tp = np.asarray(tp, float); tq = np.full_like(tp, np.nan); ok = ~np.isnan(tp)
    tq[ok] = multipletests(tp[ok], method="fdr_bh")[1]
    return pd.DataFrame({"gene": fc.index, "T_log2FC": fc.values, "T_q": tq}).set_index("gene")


def main():
    tumor_sig = tumor_signature()

    calu = pd.read_csv(DATA / "proteomics_search" / "fragpipe_analyst_DE_results.csv").dropna(subset=["Gene"])
    calu["C_log2FC"] = calu[D3].mean(axis=1) - calu[D2].mean(axis=1)   # 3D - 2D
    culture = calu.groupby("Gene")["C_log2FC"].mean()
    cg = calu.groupby("Gene")[D2 + D3].mean()

    # (1) genome-wide correlation
    sh = culture.index.intersection(tumor_sig.index)
    C = culture.loc[sh]; T = tumor_sig["T_log2FC"].loc[sh]
    m = C.notna() & T.notna(); C, T = C[m], T[m]
    r_gw, p_gw = stats.pearsonr(C, T)

    # tumor programs
    sig = tumor_sig.dropna(subset=["T_q"])
    up_t = set(sig.index[(sig.T_q < 0.01) & (sig.T_log2FC > 0.58)])
    dn_t = set(sig.index[(sig.T_q < 0.01) & (sig.T_log2FC < -0.58)])

    # (2) singscore per replicate, with/without proliferation genes
    hm = gp.get_library("MSigDB_Hallmark_2020")
    prolif = set(hm["E2F Targets"]) | set(hm["G2-M Checkpoint"]) | set(hm.get("Myc Targets V1", []))
    sc_all = pd.Series({s: singscore(cg[s], up_t, dn_t) for s in D2 + D3})
    sc_np = pd.Series({s: singscore(cg[s], up_t - prolif, dn_t - prolif) for s in D2 + D3})
    t_all = stats.ttest_ind([sc_all[c] for c in D2], [sc_all[c] for c in D3])
    t_np = stats.ttest_ind([sc_np[c] for c in D2], [sc_np[c] for c in D3])

    # (3) GSEA of tumor programs against culture ranking
    rnk = culture.dropna().sort_values(ascending=False).reset_index()
    rnk.columns = [0, 1]
    pre = gp.prerank(rnk=rnk, gene_sets={"Tumor_UP": list(up_t), "Tumor_DOWN": list(dn_t)},
                     min_size=5, max_size=2000, permutation_num=1000, seed=SEED, no_plot=True, outdir=None)
    g = pre.res2d.set_index("Term")
    nes_up, fdr_up = float(g.loc["Tumor_UP", "NES"]), float(g.loc["Tumor_UP", "FDR q-val"])
    nes_dn, fdr_dn = float(g.loc["Tumor_DOWN", "NES"]), float(g.loc["Tumor_DOWN", "FDR q-val"])

    # (4) directional concordance on 72 DEPs
    deps = pd.read_csv(RESULTS / "differential_expression" / "DEPs_2Dvs3D_72.csv")
    deps["C_sign"] = np.where(deps["dir_3D"] == "up_in_3D", 1, -1)
    deps = deps.merge(tumor_sig.reset_index()[["gene", "T_log2FC"]], on="gene", how="left")
    d = deps.dropna(subset=["T_log2FC"]).copy()
    d["T_sign"] = np.sign(d["T_log2FC"])
    agree = int((d["C_sign"] == d["T_sign"]).sum())

    results = pd.DataFrame([
        ["Genome-wide Pearson r (3D-vs-2D axis vs tumor-vs-normal axis)",
         f"{r_gw:+.3f}", f"{p_gw:.1e}", f"{m.sum()} genes", "2D leans tumor-like"],
        ["Per-sample tumor-likeness (all sig genes): 2D vs 3D",
         f"2D={np.mean([sc_all[c] for c in D2]):.3f}, 3D={np.mean([sc_all[c] for c in D3]):.3f}",
         f"{t_all[1]:.3f}", "singscore", "2D more tumor-like"],
        ["Per-sample tumor-likeness (excl. proliferation)",
         f"2D={np.mean([sc_np[c] for c in D2]):.3f}, 3D={np.mean([sc_np[c] for c in D3]):.3f}",
         f"{t_np[1]:.3f}", "singscore", "2D more tumor-like"],
        ["GSEA Tumor-UP program vs culture ranking",
         f"NES={nes_up:.2f}", f"FDR={fdr_up:.3f}", f"{len(up_t)} genes", "enriched at 2D end"],
        ["GSEA Tumor-DOWN program vs culture ranking",
         f"NES={nes_dn:.2f}", f"FDR={fdr_dn:.3f}", f"{len(dn_t)} genes", "n.s." if fdr_dn > 0.05 else "sig"],
        ["Directional concordance on 72 DEPs",
         f"{agree}/{len(d)} agree", f"{agree/len(d):.0%}", f"{len(d)} DEPs w/ tumor data", "no better than chance"],
    ], columns=["test", "effect", "significance", "n", "conclusion"])

    dst = RESULTS / "tumor_fidelity" / "Proposal1_fidelity_results.csv"
    dst.parent.mkdir(parents=True, exist_ok=True)
    results.to_csv(dst, index=False)
    print(results.to_string(index=False))
    print(f"\nwrote {dst}")


if __name__ == "__main__":
    main()

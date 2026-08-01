#!/usr/bin/env python3
"""
03_enrichment_gsea.py
=====================
Threshold-free functional enrichment of the 2D-vs-3D proteome by preranked GSEA.

The whole quantified proteome is ranked by a signed moderated t-statistic
(FragPipe-Analyst limma difference / standard error derived from the 95% CI),
then tested by preranked GSEA against:
  * two curated axis gene sets (cholesterol biosynthesis; cell adhesion / ECM),
  * MSigDB Hallmark 2020 and Reactome 2022 (via gseapy's Enrichr libraries).

Ranking sign
------------
Positive modt = higher in 2D = DOWN in 3D. Both curated axes are down-in-3D
programs, so they enrich toward the positive (2D) pole.

Inputs
------
    data/proteomics_search/fragpipe_analyst_Full_dataset.csv  (limma per-protein stats)

Outputs
-------
    results/enrichment/gsea_rank.rnk
    results/enrichment/gsea_results.csv

Requires network access (gseapy fetches Enrichr gene-set libraries).

Run
---
    python code/03_enrichment_gsea.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))  # ensure config.py is importable

import pandas as pd
import gseapy as gp
from config import FA_FULL_DATASET, RESULTS, SEED

# Curated axis gene sets (the two coordinated down-in-3D programs).
GENE_SETS = {
    "Cholesterol_biosynthesis": [
        "SQLE", "FDFT1", "DHCR7", "MSMO1", "SCD", "HMGCR", "HMGCS1", "LSS",
        "NSDHL", "SC5D", "IDI1", "CYP51A1", "ACAT2", "DHCR24", "MVD", "MVK",
        "FDPS", "LBR", "TM7SF2", "EBP", "SREBF2", "INSIG1",
    ],
    "Cell_adhesion_ECM": [
        "EGFR", "MET", "EPHA2", "ITGB1", "ITGA3", "ITGA6", "LAMB1", "LAMC1",
        "LAMA5", "FN1", "CDH1", "CTNNB1", "CLDN3", "CLDN4", "TJP1", "COL4A1",
        "COL4A2", "DSP", "JUP", "PKP2",
    ],
}
ENRICHR_LIBS = ["MSigDB_Hallmark_2020", "Reactome_2022"]


def build_ranking():
    lm = pd.read_csv(FA_FULL_DATASET)
    # SE from the 95% CI half-width; moderated t = diff / SE
    lm["se"] = (lm["X2D_vs_X3D_CI.R"] - lm["X2D_vs_X3D_CI.L"]) / (2 * 1.959964)
    lm["modt"] = lm["X2D_vs_X3D_diff"] / lm["se"]
    rk = lm[["Gene", "modt"]].dropna().copy()
    rk = rk.reindex(rk["modt"].abs().sort_values(ascending=False).index)
    rk = rk.drop_duplicates("Gene").sort_values("modt", ascending=False)
    out = RESULTS / "enrichment" / "gsea_rank.rnk"
    out.parent.mkdir(parents=True, exist_ok=True)
    rk.to_csv(out, sep="\t", header=False, index=False)
    return str(out)


def main():
    rnk = build_ranking()

    pre = gp.prerank(rnk=rnk, gene_sets=GENE_SETS, min_size=3, max_size=500,
                     permutation_num=1000, seed=SEED, outdir=None, no_plot=True)
    res_c = pre.res2d.copy()

    tab = res_c[["Term", "ES", "NES", "NOM p-val", "FDR q-val", "Lead_genes"]].copy()
    for lib in ENRICHR_LIBS:
        try:
            pr = gp.prerank(rnk=rnk, gene_sets=lib, min_size=8, max_size=400,
                            permutation_num=1000, seed=SEED, outdir=None, no_plot=True)
            r = pr.res2d.copy()
            sig = r[r["FDR q-val"].astype(float) < 0.05][
                ["Term", "ES", "NES", "NOM p-val", "FDR q-val", "Lead_genes"]
            ].copy()
            sig["Term"] = sig["Term"] + f" [{lib.split('_')[0]}]"
            tab = pd.concat([tab, sig.head(15)], ignore_index=True)
        except Exception as e:
            print(f"{lib}: skipped ({str(e)[:80]})")

    dst = RESULTS / "enrichment" / "gsea_results.csv"
    tab.to_csv(dst, index=False)
    print(f"wrote {dst}  ({len(tab)} enriched terms)")
    print(res_c[["Term", "NES", "FDR q-val"]].to_string(index=False))


if __name__ == "__main__":
    main()

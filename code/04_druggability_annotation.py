#!/usr/bin/env python3
"""
04_druggability_annotation.py
=============================
Annotate each DEP with druggability / clinical-precedent evidence from the
Open Targets Platform and ChEMBL.

External evidence is provided as two cached JSON snapshots in
`data/external_cohorts/` (queried from the Open Targets GraphQL API and ChEMBL
at analysis time). See `data/external_cohorts/README.md` for the query and how
to refresh them.

For each DEP:
  * modalities      - tractable drug modalities (small molecule, antibody, ...)
  * approved        - an approved drug exists against the target
  * drug_count      - number of associated drugs (any phase)
  * max_phase       - maximum clinical phase of any associated drug
  * luad_score      - Open Targets association score with lung adenocarcinoma
  * lung_ca_score   - best association score across lung-cancer disease terms
  * chembl_sterol_axis - hand-curated ChEMBL precedent for the sterol-axis enzymes
  * druggable_any   - has any drug OR curated sterol-axis precedent

Inputs
------
    results/differential_expression/DEPs_2Dvs3D_72.csv   (from script 02)
    data/external_cohorts/ot_annot.json
    data/external_cohorts/lung_scores.json

Output
------
    results/druggability/DEPs_druggability_annotated.csv

Run
---
    python code/04_druggability_annotation.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import json
import pandas as pd
from config import RESULTS, DATA

# Hand-curated ChEMBL precedent for the sterol-biosynthesis / lipid axis enzymes,
# where Open Targets disease-association scores understate druggability.
STEROL_DRUG_MAP = {
    "SQLE": "terbinafine (approved, SQLE inhibitor)",
    "FDFT1": "lapaquistat/squalene-synthase inhibitor (Ph3)",
    "SCD": "SCD1 inhibitors (clinical/preclinical, 2402 bioactivities)",
    "NCEH1": "NCEH1 inhibitors (preclinical)",
    "DHCR7": "known enzyme target",
    "MSMO1": "known enzyme target",
    "ELOVL7": "ELOVL inhibitors (preclinical)",
}


def main():
    deps = pd.read_csv(RESULTS / "differential_expression" / "DEPs_2Dvs3D_72.csv")
    ext = DATA / "external_cohorts"
    ot = json.load(open(ext / "ot_annot.json"))
    lung = json.load(open(ext / "lung_scores.json"))

    rows = []
    for _, d in deps.iterrows():
        g = d["gene"]
        a = ot.get(g, {})
        rows.append({
            "gene": g, "uniprot": d["uniprot"],
            "log2FC_2Dvs3D": d["log2FC_2Dvs3D"], "padj": d["padj"], "dir_3D": d["dir_3D"],
            "modalities": ",".join(a.get("modalities", [])),
            "approved": a.get("approved_SM") or a.get("approved_AB"),
            "drug_count": a.get("drug_count", 0),
            "max_phase": a.get("max_phase"),
            "luad_score": a.get("luad_score"),
            "description": d["description"],
        })
    ann = pd.DataFrame(rows)
    ann["lung_ca_score"] = ann["gene"].map(lambda g: lung.get(g, {}).get("best_lung"))
    ann["chembl_sterol_axis"] = ann["gene"].map(lambda g: STEROL_DRUG_MAP.get(g, ""))
    ann["druggable_any"] = (ann["drug_count"] > 0) | (ann["chembl_sterol_axis"] != "")

    dst = RESULTS / "druggability" / "DEPs_druggability_annotated.csv"
    dst.parent.mkdir(parents=True, exist_ok=True)
    ann.to_csv(dst, index=False)
    print(f"wrote {dst}")
    print(f"druggable DEPs (any drug or sterol precedent): {int(ann['druggable_any'].sum())} / {len(ann)}")
    print(f"with an approved drug: {int(ann['approved'].fillna(False).astype(bool).sum())}")


if __name__ == "__main__":
    main()

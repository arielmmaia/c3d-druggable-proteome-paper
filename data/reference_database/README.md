# Reference sequence database

The FragPipe search used a **human-only** target–decoy database built with a
custom Galaxy workflow authored by A.M. Maia.

## Database builder (Galaxy workflow)

**"Human Database Builder for FragPipe"**
https://usegalaxy.eu/published/workflow?id=d55df785d4c71876

The workflow takes a user-supplied **human proteome FASTA** and:

1. Downloads the **Hao Lab** contaminant set.
2. Removes human proteins from the contaminant set (avoids double-counting
   human entries as contaminants).
3. Adds contaminant headers in a **FragPipe-compatible** format.
4. Merges the human proteome with the cleaned contaminants.
5. Adds **reverse (decoy)** sequences.

Output: a single target+contaminant+decoy FASTA ready for FragPipe/MSFragger.

## Database used in this paper

| Field | Value |
|---|---|
| File name (on search machine) | `Galaxy-database_human_HaoLab_contam_decoy.fasta` |
| Taxonomy | *Homo sapiens* only (no mouse) |
| Source proteome | UniProt SwissProt canonical human, `UP000005640` (20,416 entries; release 2026-02) |
| Contaminants | Hao Lab set, human entries removed |
| Decoys | reversed, prefix `rev_` |

## Files in this folder

The final search FASTA is **large and not redistributed here** (see
[`../../.gitignore`](../../.gitignore)). It is fully reconstructible from the
Galaxy workflow above plus the source proteome:

- Source human proteome (UniProt `UP000005640`, canonical SwissProt) —
  downloadable from UniProt; the exact release used was 2026-02.
- Hao Lab contaminants — fetched automatically by the Galaxy workflow.

> **Provenance note.** The canonical award search
> (`2026_07_21_v24-0_2dvs3d_canonical-only_DDA_ubuntu_genetics`) ran on a
> separate machine and referenced this human-only FASTA there. A different,
> **human+mouse** database
> (`Galaxy-database_human_mouse_HaoLab_contam_decoy.fasta`) exists in the
> original project tree but was used for **earlier/exploratory** runs (and the
> preprint), **not** for this paper.

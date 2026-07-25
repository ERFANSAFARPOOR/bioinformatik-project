# LOCAL_ORTHOLOGY_SEARCH_REPORT.md

**Date:** 2026-07-07 · **Branch:** `claude/revival-audit` · **Env:** `reccobra39`
**Purpose:** read-only search of the local repo + supplements for an explicit
**PA14↔PAO1 locus-tag** orthology table that could later unblock Poulsen 2019 /
Basta 2017. **No mapping built, no merge, no parse, no metrics.**

Classification legend: `VALIDATED_STUDY_ORTHOLOGY` (explicit PA14 locus tag ↔ PAO1
locus tag pair) · `CLUSTER_WITH_PAO1_MEMBER` · `CLUSTER_ONLY` · `PA14_ONLY` ·
`SYMBOL_ONLY` · `NOT_ORTHOLOGY`.

## Hits and classification

### Turner 2015 supplement — `data/raw/literature/turner2015/` — **VALIDATED_STUDY_ORTHOLOGY**
- **`pnas.1419677112.sd03.xlsx` sheet `Sheet1`** (header Excel row 2, data row 4):
  - col A `PA14 Locus ID` (`PA14_#####`) ↔ col J `PAO1 Locus ID` (`PA####`), paired
    row-by-row.
  - **5,365 explicit PA14↔PAO1 pairs** (e.g. `PA14_00010`↔`PA0001`,
    `PA14_00020`↔`PA0002`); 541 PA14 rows with no PAO1 ortholog; 204 PAO1-only.
    Matches the paper's *"5,366 orthologous gene pairs"*.
  - **Method documented (Turner Methods):** *"precomputed BLAST results and synteny
    information available at the Pseudomonas Genome Database … was used to identify
    5,366 orthologous gene pairs between these two strains."*
- **`pnas.1419677112.sd04.xlsx`**: same layout, **5,365 pairs** (MOPS-sputum table).
- sd05 / sd09: also carry paired `PAO1 Locus ID` + `PA14 Locus ID` columns (smaller
  subsets).
- **Contains explicit PA14 + PAO1 locus-tag pairs: YES.** Genome-scale,
  peer-reviewed, method-documented (Pseudomonas Genome Database orthologs, 2015).
  **Strongest local candidate.** Caveat: it is the **1:1 ortholog subset** as of
  2015; many-to-one / one-to-many cases and PA14-unique genes are not fully covered.

### Belanger 2022 supplement — `data/raw/literature/belanger2022/Data_Sheet_1.XLSX` — **VALIDATED_STUDY_ORTHOLOGY (weak/partial)**
- Sheet `T0_PAO1_essential_genes` (header row 2): col A `Locus Tag` (PAO1 `PA####`)
  ↔ col B `PA14 locus tag` (`PA14_#####`). **600 explicit pairs** (e.g.
  `PA3645`↔`PA14_17190`).
- **Contains explicit pairs: YES**, but **only for Belanger's essential-gene set**
  (not genome-wide) and the **orthology method is not documented** in the sheet.
  Useful as a cross-check, not as the primary source.

### Poulsen 2019 supplement — `data/raw/literature/poulsen2019/` — **CLUSTER_ONLY / PA14_ONLY**
- sd05 `Essential Genes`, sd06, sd02: columns `Cluster_ID` + `PA14_ID` only. **No
  PAO1 column; no `PAxxxx` anywhere** (sd03 scanned last cycle: 9 strains
  BL23/X13273/CF77/BWH005/BWH013/19660/PA14/BWH015/PS75 — **PAO1 not among them**).
  `Cluster_ID` has **no PAO1 member**. → cannot self-provide PAO1 mapping.
- (Poulsen media per sd05: LB, M9, Fetal Bovine Serum, Synthetic Cystic Fibrosis
  Medium, Urine.)

### Basta 2017 supplement — `data/raw/literature/basta2017/` — **PA14_ONLY**
- sd1–sd4: gene col `Locus` = `PA14_#####` (+ `IG_…`). No PAO1 identifiers.

### `data/processed/gene_mapping.csv` — **SYMBOL_ONLY**
- `pa14_locus_tag` present but derived from **RefSeq gene symbol** matches
  (386 medium / 22 low / 646 unmapped); file's own notes say *"not validated
  orthology"*. **Rejected** as validated orthology (per run rules).

### `data/raw/ortholog/{pao1,pa14}_feature_table.txt.gz` — **NOT_ORTHOLOGY (as a pairing)**
- Two **single-strain** RefSeq feature tables (annotation), not a paired ortholog
  table. Useful only as inputs to a future RBH workflow.

## Summary
- **A genome-scale, explicit, method-documented PA14↔PAO1 ortholog pairing EXISTS
  locally** inside the Turner 2015 peer-reviewed supplement (sd03/sd04; 5,365
  pairs; Pseudomonas Genome Database BLAST+synteny). Belanger DS1 gives a smaller
  (600-pair) cross-check.
- Poulsen and Basta supplements are **PA14-referenced with no PAO1 member** — they
  cannot self-map; they need an external PA14↔PAO1 table such as Turner's.
- The symbol-based `gene_mapping.csv` remains **insufficient** (not used).
- **Next:** web search for the authoritative current pseudomonas.com / OrthologueDB
  export (Phase 3–4); if unavailable, the Turner-embedded Pseudomonas Genome
  Database table is the best available and is previewed as a **candidate** (not
  merged, not used to parse Poulsen/Basta) with a human-review + cross-check flag.

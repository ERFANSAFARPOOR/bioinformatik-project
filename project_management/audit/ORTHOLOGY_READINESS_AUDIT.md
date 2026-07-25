# ORTHOLOGY_READINESS_AUDIT.md

**Date:** 2026-07-07 · **Branch:** `claude/revival-audit` · **Env:** `reccobra39`
**Purpose:** state exactly what PAO1↔PA14 mapping material exists, whether any of
it is **validated orthology**, and whether Poulsen 2019 / Basta 2017 can be safely
mapped to the PAO1 iMO1056 model. **No orthology fabricated.**

## Mapping files that exist
| File | What it is | Validated orthology? |
|---|---|---|
| `data/processed/gene_mapping.csv` | model gene ↔ PAO1 (identity, 1054/1054) + PAO1→PA14 via **RefSeq gene symbol** | **NO** — symbol/annotation-based; the file's own `notes` say *"not validated orthology"* |
| `data/processed/gene_mapping_coverage.txt` | coverage report of the above | n/a |
| `data/raw/ortholog/pao1_feature_table.txt.gz` | PAO1 RefSeq feature table (NCBI) | source annotation only |
| `data/raw/ortholog/pa14_feature_table.txt.gz` | PA14 RefSeq feature table (NCBI) | source annotation only |

Coverage of the symbol layer (from `gene_mapping_coverage.txt`): 386 unique-symbol
PA14 matches (medium), 22 ambiguous (low), 646 unmapped → ~408/1054 (~39%),
**annotation-based, not validated**.

## Are any acceptable (validated) sources present?
**No.** Acceptable sources would be: an authoritative pseudomonas.com /
OrthologueDB export, a study-provided ortholog table carrying PAO1 identifiers, or
a documented cluster table containing PAO1 members. None is present:
- pseudomonas.com / OrthologueDB export — **absent** (unreachable here, B-NET).
- **Poulsen supplement** — PA14-referenced (`Cluster_ID`+`PA14_ID`); the 9
  clustered strains **exclude PAO1** (verified: sd03 has zero `PAxxxx`), so its
  `Cluster_ID` cannot expose a PAO1 member. Not an orthology source.
- **Basta supplement** — PA14-only (`PA14_xxxxx`); no PAO1 identifiers.
- **In-corpus partial crosswalks (leads only, NOT authoritative):**
  - *Belanger* `Data_Sheet_1` has a `PA14 locus tag` column paired with PAO1
    `Locus Tag`, but only for Belanger's own gene set and without a documented
    orthology method — a partial annotation crosswalk, **not** genome-wide
    validated orthology.
  - *Turner* sd03/sd04/sd05/sd09 carry 1-to-1 PAO1↔PA14 pairs (from the
    Pseudomonas Genome Database precomputed BLAST+synteny) **for Turner's genes
    only** — study-specific, not a general PA14→PAO1 resource for Poulsen/Basta.

Not acceptable as validated orthology (and not used): RefSeq symbol-only mapping,
gene-name similarity, inferred `PA14_ID`→PAO1 conversion, guessed `Cluster_ID`
mapping.

## Can Poulsen be mapped safely? — **NO**
Poulsen essential lists are keyed by `PA14_ID`/`Cluster_ID` with **no PAO1 member
in any cluster** (PAO1 not among the 9 strains). Mapping to the PAO1 model needs a
**validated PA14→PAO1 ortholog table** that does not exist here. Status:
**ORTHOLOGY_PENDING / MAPPING_BLOCKED** (threshold + phenotype + media already
sourced — `THRESHOLD_METHOD_AUDIT.md`).

## Can Basta be mapped safely? — **NO**
Basta is PA14-only. Same missing validated PA14→PAO1 table. Additionally its
gene-level calls must be **derived** from read ratios/p-values (no call column),
and its phenotype (growth-arrest survival) is not FBA growth-essentiality. Status:
**ORTHOLOGY_PENDING + ANALYSIS_PENDING**.

## What remains blocked
- **B-MAP-01 / B-NET:** no validated PA14→PAO1 orthology reachable here.
- Poulsen and Basta cannot be parsed to PAO1 gene-level evidence until it exists.

## Exact next human input needed (no validated table exists)
Provide **one** of, with provenance (store under `data/raw/ortholog/` + SHA-256):
1. pseudomonas.com **"Ortholog"** export for PAO1↔PA14 (authoritative), or
2. OrthologueDB / OrthoMCL / OMA PA14↔PAO1 ortholog table with PAO1 `PAxxxx` ids, or
3. A study-provided PA14→PAO1 homolog table with a documented method.
Then join on `PA14_ID`, retaining 1:1 / one-to-many / missing / absent-from-model
explicitly (`POULSEN_BASTA_MAPPING_PLAN.md`). Do **not** substitute the symbol
layer. Until then, Poulsen/Basta stay blocked; no metrics.

# POULSEN_BASTA_MAPPING_PLAN.md

**Date:** 2026-07-07 · **Branch:** `claude/revival-audit`
**Purpose:** define the *safe* mapping strategy required before Poulsen 2019 or
Basta 2017 gene-level rows may be joined to the PAO1 iMO1056 model. Both are
**PA14-indexed** and neither supplement contains PAO1 (`PAxxxx`) identifiers, so
both need **validated PA14→PAO1 orthology** (B-MAP-01). **No orthology is
fabricated here**; this is a plan, not a built mapping.

## Current mapping state (unchanged this cycle)
`data/processed/gene_mapping.csv` holds only:
- model gene ↔ PAO1 locus tag: identity, 1054/1054 (high).
- PAO1 → PA14 via **RefSeq gene symbol** (annotation, **NOT** validated orthology):
  386 unique (medium), 22 ambiguous (low), 646 unmapped (~39% coverage).

Per `ORTHOLOGY_STATUS_REPORT.md`, symbol-based mapping is **insufficient** for
strain-mapped metrics and must not be used as validated evidence.

## Poulsen 2019 — mapping analysis
- **Finding (verified this cycle):** the 9 sequenced strains are BL23, X13273,
  CF77, BWH005, BWH013, 19660, PA14, BWH015, PS75. **PAO1 is not among them.**
  Scanning sd03 (`Dataset S2`, 53,290 rows): only PA14 rows carry a standard locus
  tag (`PA14_xxxxx`); **zero `PAxxxx`**. The gene-level essential lists (sd05,
  sd02, sd06) are keyed by `Cluster_ID` + `PA14_ID`.
- **Can `Cluster_ID` expose a PAO1 member?** **No.** PAO1 was not one of the
  clustered strains, so no cluster contains a PAO1 gene. `Cluster_ID` only relates
  the 9 study strains to each other.
- **Consequence:** Poulsen → PAO1 requires **validated PA14→PAO1 orthology**,
  applied via the `PA14_ID` reference column. Keep one-to-many / missing /
  ambiguous explicit; PA14 genes absent from PAO1 (or from the metabolic model)
  stay unmapped.
- **Status:** **ORTHOLOGY_PENDING / MAPPING_BLOCKED.** (Threshold + phenotype +
  media are sourced — `THRESHOLD_METHOD_AUDIT.md`.)

## Basta 2017 — mapping analysis
- **Finding:** PA14-indexed (`PA14_xxxxx`), single strain (UCBPP-PA14).
- **Consequence:** requires **validated PA14→PAO1 orthology** via `PA14_ID` before
  any PAO1-model comparison. Keep one-to-many / missing / ambiguous explicit.
- **Extra caveat:** even after mapping, the phenotype is **growth-arrest survival**,
  not FBA growth-essentiality — the matching prediction is not standard single-gene
  deletion growth (needs a maintenance/ATP framework). Mapping alone does not make
  it comparable.
- **Status:** **ORTHOLOGY_PENDING + ANALYSIS_PENDING** (call column must be derived
  from read ratios/p-values) — **MAPPING_BLOCKED**.

## Safe mapping strategy (to build later; do not fabricate)
1. Obtain an **authoritative PA14↔PAO1 ortholog table** — pseudomonas.com
   "Ortholog" export (blocked here, B-NET) or a study-provided homolog table —
   store under `data/raw/ortholog/` with provenance + SHA-256.
2. Join onto `PA14_ID` for Poulsen (sd05/sd02) and Basta (sd1/sd2 derived calls).
3. Retain and label: **1:1** (high), **one-to-many** (candidates kept), **missing**
   (PA14 gene with no PAO1 ortholog), **absent-from-model** (PAO1 ortholog exists
   but not in iMO1056's ~1054 metabolic genes). Never collapse.
4. Mark every mapped row `mapping_method=orthology(<source+version>)`,
   `mapping_confidence` per class; unmapped rows `review_status=ORTHOLOGY_PENDING`.
5. Only then may Poulsen/Basta gene-level DRAFT rows be emitted. Basta additionally
   requires a documented non-growth comparison framework before any metric.

## Do NOT
- Do **not** use the symbol-based PA14 layer as validated orthology for evidence.
- Do **not** invent Cluster_ID→PAO1 links (no PAO1 in the clusters).
- Do **not** compute any metric (B-SCI-01 / no-metrics rule).

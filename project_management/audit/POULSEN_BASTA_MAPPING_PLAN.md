# POULSEN_BASTA_MAPPING_PLAN.md

**Original plan:** 2026-07-07 · **Reconciled:** 2026-11-11
**Purpose:** define the *safe* mapping strategy required before Poulsen 2019 or
Basta 2017 gene-level rows may be joined to the PAO1 iMO1056 model. Both are
**PA14-indexed** and neither supplement contains PAO1 (`PAxxxx`) identifiers, so
both need **validated PA14→PAO1 orthology** (B-MAP-01). **No orthology is
fabricated here**; this is a plan, not a built mapping.

## Current disposition (supersedes the July no-source gate)

The existing `ORTHOLOGY_HUMAN_REVIEW_DECISION.md` (2026-07-10) approves the
Turner-derived **5,365 strict 1:1 pairs** for **limited controlled L-03b draft
mapping**. PA2279's conflict is resolved in favor of Turner in the companion
conflict report. This is not unrestricted approval, a completed Poulsen/Basta
parse, or permission to compute metrics for these datasets.

The original plan's `ORTHOLOGY_PENDING` / `MAPPING_BLOCKED` labels described
the **2026-07-07** state; they are superseded by this limited approval.
The official PGD source is now integrated into the canonical mapping as
observed below; this does not turn a mapped measurement into a PAO1 assay or
constitute new unrestricted study-use approval.

This plan concerns **Poulsen/Basta only**. It does not reopen the completed
D-21/V-01 MOPS-pyruvate comparison, which uses MPAO1→PAO1 DS1 mappings and no
PA14 orthology.

**Observed mapping artifacts (2026-11-11):**
`data/processed/gene_mapping/gene_mapping.csv` uses `official_orthology`; its
coverage report records **1023 unique, 2 ambiguous, 29 unmapped** model genes.
The builder reads the official PGD raw export. The separate
`data/processed/ortholog/final/pao1_pa14_orthologs_pseudomonas_rbh_20260712.csv`
has **5374 pairs** and a `Validation_Report.txt` marked **PASSED** (structural
checks). These artifacts exist and the canonical mapping is no longer merely
the old symbol-based layer. This observed integration does not by itself
establish a reviewed Poulsen/Basta comparison or supersede the documented
D-16 limited-use decision with a new unrestricted approval.

## Historical symbol-based mapping layer (July snapshot)
The July symbol-based predecessor (not the current canonical mapping) held:
- model gene ↔ PAO1 locus tag: identity, 1054/1054 (high).
- PAO1 → PA14 via **RefSeq gene symbol** (annotation, **NOT** validated orthology):
  386 unique (medium), 22 ambiguous (low), 646 unmapped (~39% coverage).

Per `ORTHOLOGY_STATUS_REPORT.md`, symbol-based mapping is **insufficient** for
strain-mapped metrics and must not be used as validated evidence.

## Poulsen 2019 — mapping analysis
- **Finding (verified this cycle):** the 9 sequenced strains are BL23, X13273,
  CF77, BWH005, BWH013, 19660, PA14, BWH015, PS75. **PAO1 is not among them.**
  Rechecked against [primary paper Table 1](https://www.pnas.org/doi/10.1073/pnas.1900570116) on 2026-11-11.
  Scanning sd03 (`Dataset S2`, 53,290 rows): only PA14 rows carry a standard locus
  tag (`PA14_xxxxx`); **zero `PAxxxx`**. The gene-level essential lists (sd05,
  sd02, sd06) are keyed by `Cluster_ID` + `PA14_ID`.
- **Can `Cluster_ID` expose a PAO1 member?** **No.** PAO1 was not one of the
  clustered strains, so no cluster contains a PAO1 gene. `Cluster_ID` only relates
  the 9 study strains to each other. A PAO1 label added by a later ortholog
  join is a coordinate, not an experiment performed on PAO1.
- **Consequence:** Poulsen → PAO1 requires **validated PA14→PAO1 orthology**,
  applied via the `PA14_ID` reference column. Keep one-to-many / missing /
  ambiguous explicit; PA14 genes absent from PAO1 (or from the metabolic model)
  stay unmapped.
- **Current status:** eligible for **controlled L-03b draft mapping only** with
  approved strict 1:1 rows; parsing/review and condition/phenotype comparison
  remain pending. Threshold + phenotype + media sources are in
  `THRESHOLD_METHOD_AUDIT.md`.

## Basta 2017 — mapping analysis
- **Finding:** PA14-indexed (`PA14_xxxxx`), single strain (UCBPP-PA14).
- **Consequence:** requires **validated PA14→PAO1 orthology** via `PA14_ID` before
  any PAO1-model comparison. Keep one-to-many / missing / ambiguous explicit.
- **Extra caveat:** even after mapping, the phenotype is **growth-arrest survival**,
  not FBA growth-essentiality — the matching prediction is not standard single-gene
  deletion growth (needs a maintenance/ATP framework). Mapping alone does not make
  it comparable.
- **Current status:** eligible for **controlled L-03b draft mapping only** with
  approved strict 1:1 rows; **ANALYSIS_PENDING** (calls must be derived from
  read ratios/p-values), with no standard growth-essentiality validation claim.

## Safe mapping strategy (future controlled draft)
1. Use the reviewed
   `data/processed/ortholog/working/pao1_pa14_orthologs_turner2015_APPROVED_LIMITED.csv`
   strict 1:1 rows with `approved_for_l03b=yes`, under the recorded decision.
   Do not treat unreviewed raw exports or the symbol layer as an automatic
   replacement; record source/version and SHA-256 for any later source change.
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
- Do **not** compute **Poulsen/Basta** metrics before their own mapping,
  parsing, phenotype and condition gates are satisfied. The existing D-21/V-01
  metrics are a separate authorized cell.

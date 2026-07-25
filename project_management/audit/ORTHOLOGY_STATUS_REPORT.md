# ORTHOLOGY STATUS REPORT (PAO1 ↔ PA14)

**Date:** 2026-07-01 · **Branch:** `claude/revival-audit`
**Files:** `data/processed/gene_mapping.csv`, `data/processed/gene_mapping_coverage.txt`
**Builder:** `scripts/mapping/build_gene_mapping.py`

---

## 1. What changed this cycle (important)

The PAO1 paper re-audit (`PAO1_PAPER_RELEVANCE_AUDIT.md`) found that **most of the
usable experimental data is PAO1/MPAO1, not PA14**:

- **belanger2022 = PAO1**, **lee2015 = MPAO1**, **turner2015 PAO1 rows** → join to
  the model by **identity** (PAO1 `PAxxxx` == model gene), **no orthology needed**.
- Validated PAO1↔PA14 orthology is now required **only** for **basta2017 (PA14)**
  and the **non-PAO1 strains of poulsen2019**.

This substantially lowers the criticality of B-MAP-01 for the *first* validation,
though it remains open for full cross-strain coverage.

## 2. Current mapping layers (from coverage report)

Sources: PAO1 `GCF_000006765.1_ASM676v1`, PA14 `GCF_000014625.1_ASM1462v1`
(NCBI RefSeq feature tables; downloaded in Phase A, in `data/raw/ortholog/`).

| Layer | Count / 1054 | Confidence |
|---|---|---|
| model gene → PAO1 locus tag (identity) | **1054** | high |
| PAO1 → PA14 via unique RefSeq gene **symbol** | **386** | medium (annotation, NOT validated orthology) |
| PAO1 → PA14 ambiguous / one-to-many | **22** | low (candidates retained) |
| PAO1 has no symbol (unmapped to PA14) | 335 | unmapped |
| PAO1 symbol with no PA14 symbol match | 311 | unmapped |

Total with any PA14 handle: **~408/1054 (~39%)**, symbol-based only.

## 3. Sources tried / downloaded / blocked

| Source | Purpose | Status |
|---|---|---|
| NCBI RefSeq feature tables (PAO1, PA14) | symbol-based cross-map | **downloaded** (Phase A) → current mapping |
| NCBI eutils (esearch/elink/esummary) | citation/PMID/PMCID metadata | **works** this session |
| pseudomonas.com orthologs / OrthologueDB | **authoritative** PAO1↔PA14 orthology | **blocked** (403 / timeout) — B-NET |
| PMC OA packages (ftp/https) | full text of study homolog tables | **blocked** (ftp denied; https 404) — B-NET |
| Publisher supplements (PNAS/Frontiers/mBio) | study-provided PAO1 homolog columns | **blocked** (403) — B-NET |
| BioModels / BiGG gene xrefs | model gene cross-references | not fetched this cycle |

## 4. Confidence classes & unresolved cases

- **High:** identity layer (model ↔ PAO1), all 1054.
- **Medium:** 386 unique-symbol PA14 matches — usable only as provisional; must be
  upgraded to validated orthology before any strain-mapped metric.
- **Low:** 22 ambiguous/one-to-many — candidates retained, not resolved.
- **Unmapped:** 646 model genes have no PA14 symbol handle.
- Direction caveat: experimental PA14 lists are PA14-indexed; mapping them onto the
  PAO1 model needs the **reverse** (PA14→PAO1) join, including PA14 genes absent
  from the metabolic model (model covers ~1054 of ~5600 genes).

## 5. Is mapping sufficient for PA14 validation?

**No.** Symbol-based mapping (39% coverage, annotation-derived) is **not**
adequate for reporting confusion matrices/metrics on PA14 datasets. It would leave
large unmapped/uncertain mass and risk false orthology calls. Validated orthology
(pseudomonas.com or study homolog tables) is required first (B-MAP-01).

**However**, PA14 mapping is **not on the critical path** for the first PAO1-side
validation, which uses PAO1/MPAO1 datasets by identity.

## 6. Next steps

1. Proceed with PAO1/MPAO1 validation (lee2015, turner2015 PAO1 rows,
   belanger2022) using the **identity** mapping — no orthology dependency.
   (meegid2022 removed from active scope by user decision 2026-07-06.)
2. Obtain authoritative PAO1↔PA14 orthology (pseudomonas.com "Ortholog" export or
   the studies' own PAO1-homolog columns) via human-assisted/different-network
   download; store in `data/raw/ortholog/` with provenance.
3. Join validated orthology into `gene_mapping.csv`; keep one-to-many/missing
   explicit; regenerate `gene_mapping_coverage.txt`.
4. Only then use basta2017 (PA14) and non-PAO1 poulsen2019 strains.

**Open blockers:** B-MAP-01 (validated orthology), B-NET (egress).
Nothing in the mapping is fabricated; unresolved entries stay unresolved.

## 7. Poulsen 2019 & Basta 2017 (raw supplements now present) — 2026-07-07

Both are **PA14-indexed** and need validated PA14→PAO1 orthology before any
PAO1-model comparison (see `POULSEN_BASTA_MAPPING_PLAN.md`):
- **Basta 2017:** single strain PA14 (`PA14_xxxxx`). Orthology required.
- **Poulsen 2019:** although "multi-strain," the **9 sequenced strains do NOT
  include PAO1** (BL23, X13273, CF77, BWH005, BWH013, 19660, PA14, BWH015, PS75;
  verified by scanning supplement sd03 — only PA14 carries a standard locus tag,
  zero `PAxxxx`). Gene lists are keyed by `Cluster_ID`+`PA14_ID`; `Cluster_ID`
  cannot expose a PAO1 member because PAO1 was not clustered. → Poulsen also needs
  **PA14→PAO1 orthology** (it is **not** a PAO1 identity-join dataset).

Neither is parsed to gene-level evidence until validated orthology exists.
Symbol-based PA14 mapping remains inadequate for this.

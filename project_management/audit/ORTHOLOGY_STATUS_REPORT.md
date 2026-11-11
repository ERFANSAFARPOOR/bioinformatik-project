# ORTHOLOGY STATUS REPORT (PAO1 ↔ PA14)

**Original snapshot:** 2026-07-01 (with 2026-07-07 addendum)
**Status reconciled:** 2026-11-11

## Current status — read before the historical layers below

- The 2026-07-10 decision in `ORTHOLOGY_HUMAN_REVIEW_DECISION.md` is
  **APPROVED_LIMITED**: **5,365 strict 1:1 Turner-derived pairs** may support
  controlled L-03b draft mapping. The PA2279 conflict is resolved in favor of
  Turner (`ORTHOLOGY_CONFLICT_RESOLUTION_REPORT.md`). Poulsen/Basta are not
  validation-ready; this is not unrestricted mapping or metric approval.
- The canonical mapping has actually been rebuilt from official PGD orthology;
  see the observed-artifact details below. Symbol-only historical matches
  remain inadequate as validation evidence.
- **Poulsen screened nine strains including PA14, not PAO1.** Its PA14-indexed
  lists require cross-strain mapping; there is no PAO1 identity-join subset.
- **D-21/V-01 already exists** for MOPS-pyruvate. It uses Varadarajan DS1 unique
  MPAO1→PAO1 best-hit mappings, not PA14 orthology and not universal identity.
  Lee-original `PAxxxx`, Turner PAO1 and Belanger PAO1 locus-ID paths are distinct.
- Sections 1–7 preserve the July source/coverage observations and network
  attempts. Their missing-source claims and proposed next steps are historical,
  superseded by the limited approval and the current validation status in
  `VALIDATION_LABEL_MEDIA_OVERLAP.md`. No present-day network recheck is implied.

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

**Files:** `data/processed/gene_mapping/gene_mapping.csv`, `data/processed/gene_mapping/gene_mapping_coverage.txt`
**Builder:** `scripts/mapping/build_gene_mapping.py`

---

## 1. What changed in the original July audit

The PAO1 paper re-audit (`PAO1_PAPER_RELEVANCE_AUDIT.md`) found that **most of the
usable experimental data is PAO1/MPAO1, not PA14**:

- **Belanger PAO1**, **Lee-original PAxxxx labels** (MPAO1 sublineage caveat)
  and **Turner PAO1 rows** use PAO1 locus IDs, with **no PA14 orthology needed**.
  This does not describe the later D-21 DS1 MPAO1→PAO1 best-hit mapping.
- Validated PAO1↔PA14 orthology is now required **only** for **basta2017 (PA14)**
  and the **PA14-indexed lists of poulsen2019** (none of its screened strains is PAO1).

This substantially lowers the criticality of B-MAP-01 for the *first* validation,
though it remains open for full cross-strain coverage.

## 2. Historical symbol-based mapping layers (July coverage report)

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

## 3. Historical sources tried / downloaded / blocked (July snapshot)

| Source | Purpose | Status |
|---|---|---|
| NCBI RefSeq feature tables (PAO1, PA14) | symbol-based cross-map | **downloaded** (Phase A) → then-current symbol mapping |
| NCBI eutils (esearch/elink/esummary) | citation/PMID/PMCID metadata | **worked** in the July session |
| pseudomonas.com orthologs / OrthologueDB | **authoritative** PAO1↔PA14 orthology | **blocked** (403 / timeout) — B-NET |
| PMC OA packages (ftp/https) | full text of study homolog tables | **blocked** (ftp denied; https 404) — B-NET |
| Publisher supplements (PNAS/Frontiers/mBio) | study-provided PAO1 homolog columns | **blocked** (403) — B-NET |
| BioModels / BiGG gene xrefs | model gene cross-references | not fetched this cycle |

## 4. Confidence classes of the historical symbol layer

- **High:** identity layer (model ↔ PAO1), all 1054.
- **Medium:** 386 unique-symbol PA14 matches — usable only as provisional; must be
  upgraded to validated orthology before any strain-mapped metric.
- **Low:** 22 ambiguous/one-to-many — candidates retained, not resolved.
- **Unmapped:** 646 model genes have no PA14 symbol handle.
- Direction caveat: experimental PA14 lists are PA14-indexed; mapping them onto the
  PAO1 model needs the **reverse** (PA14→PAO1) join, including PA14 genes absent
  from the metabolic model (model covers ~1054 of ~5600 genes).

## 5. Was the historical symbol layer sufficient for PA14 validation?

**No.** Symbol-based mapping (39% coverage, annotation-derived) is **not**
adequate for reporting confusion matrices/metrics on PA14 datasets. It would leave
large unmapped/uncertain mass and risk false orthology calls. Validated orthology
(pseudomonas.com or study homolog tables) is required first (B-MAP-01).

**However**, PA14 mapping is **not on the critical path** for the first PAO1-side
validation. PAO1 locus-ID datasets and the later DS1 MPAO1→PAO1 best-hit
path do not require PA14 orthology.

## 6. Proposed next steps in the July snapshot (superseded where noted above)

1. Proceed with PAO1-locus-ID evidence (Lee-original, Turner PAO1 rows,
   Belanger PAO1) — no PA14 orthology dependency. The later D-21 path instead
   uses DS1 MPAO1→PAO1 best-hit mappings and is already compared in V-01.
   (meegid2022 removed from active scope by user decision 2026-07-06.)
2. Obtain authoritative PAO1↔PA14 orthology (pseudomonas.com "Ortholog" export or
   the studies' own PAO1-homolog columns) via human-assisted/different-network
   download; store in `data/raw/ortholog/` with provenance.
3. Join validated orthology into `gene_mapping.csv`; keep one-to-many/missing
   explicit; regenerate `gene_mapping_coverage.txt`.
4. Use Basta (PA14) and Poulsen PA14-indexed evidence only under their own
   mapping, phenotype and condition checks; July 10 limited approval permits
   controlled drafts, not completed validation.

**Historical blockers:** B-MAP-01 (validated orthology), B-NET (egress).
B-MAP-01 was later narrowed by the limited approval; see the current banner.
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

At the time of this addendum, neither source had been parsed to PAO1 gene-level
evidence. July 10 subsequently enabled controlled draft mapping with the
approved-limited Turner source; it did not complete parsing or validation.
Symbol-based PA14 mapping remains inadequate.

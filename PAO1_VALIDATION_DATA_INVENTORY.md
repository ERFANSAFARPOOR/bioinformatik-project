# PAO1 VALIDATION DATA INVENTORY

**Date:** 2026-07-01 · **Branch:** `claude/revival-audit`
**Purpose:** single inventory of every candidate experimental dataset for PAO1
model (iMO1056) validation, with strain, phenotype class, condition, mapping
status, download status, and simulability. **No metrics computed.**

Strain tiers per `PAO1_PAPER_RELEVANCE_AUDIT.md`. "Gene-level labels?" = whether
a per-gene essential/fitness list exists in principle (in a supplement), not
whether it is currently in the repo (it is not — supplements are blocked).

---

## 1. Master table

| study_id | Strain | Tier | Phenotype class | Gene-level labels exist? | Supplement in repo? | Locus tags | Direct PAO1 map? | PA14→PAO1 orthology needed? | Model can simulate condition? | Priority |
|---|---|---|---|---|---|---|---|---|---|---|
| **belanger2022** | PAO1 | 1 | host-condition-fitness | yes (supp) | **YES 2026-07-06** | PAxxxx | **yes** | no | partial (host media reconstructable; some conditions non-metabolic) | **P0 (highest)** |
| **lee2015** | MPAO1 | 2 | general + condition-specific essential | yes (sd01) | **YES 2026-07-06** | PAxxxx (MPAO1) | **yes** (MPAO1 caveat) | no | yes (LB + defined media) | **P0 (highest)** |
| **turner2015** | PAO1+PA14 | 3 | condition-specific essential (CF sputum) | yes (sd01–10) | **YES 2026-07-06** | PAxxxx + PA14 | yes (PAO1 rows) | only PA14 rows | yes (SCFM/MOPS reconstructable) | **P0** |
| **varadarajan2020** (NEW) | MPAO1 | 2 (candidate) | general + condition-specific essential | yes (Dataset 4) | **YES 2026-07-06** | MPAO1_xxxxx (+PAO1 map in supp) | indirect (in-supp map) | no (MPAO1→PAO1) | yes (LB/minimal/sputum/serum) | P1 (verify DOI/PMID first) |
| poulsen2019 | multi (incl PAO1) | 3/5 | core-essential | yes (sd01–07) | **YES 2026-07-06** | PA14_ID / Cluster_ID | partial (via Cluster_ID PAO1 members) | for PA14-indexed rows | yes (rich medium) | P1 |
| basta2017 | PA14 | 4 | growth-arrest survival determinant | yes (sd1–4) | **YES 2026-07-06** | PA14 (Q010_/PA14) | no | **yes** | **no** — FBA models growth, not survival during arrest | P2 (needs orthology + concept caveat) |
| juhas2015 | review | 6 | (review) | n/a | n/a (review) | n/a | n/a | n/a | n/a | background only |

## 2. By availability

- **PAO1/MPAO1 datasets now available (strain-ready, no orthology):**
  belanger2022 (PAO1), lee2015 (MPAO1), turner2015 (PAO1 rows). → These are the
  **primary validation targets**. (meegid2022 removed from active scope by user
  decision 2026-07-06; no local files; no validation dependency.)
- **Multi-strain (partial PAO1):** poulsen2019 (usable via Cluster_ID PAO1 members).
- **PA14-only (orthology required):** basta2017.
- **Raw supplements now in the repo (2026-07-06):** lee2015, turner2015 (sd01–10),
  belanger2022, varadarajan2020, **poulsen2019 (sd01–07), basta2017 (sd1–4+tif)**
  — audited + provenance-logged. **No corpus supplements remain absent.**
- **Gene-level labels parsed into the evidence table:** DRAFT for Lee/Turner/
  Belanger (`literature_evidence_gene_level_DRAFT.csv`); Poulsen/Basta not yet
  parsed (orthology + threshold gate). Canonical `literature_evidence.csv` unchanged.
- **Blocked (still):** pseudomonas.com orthology (for Basta/Poulsen), OA GEM
  packages, and all source URLs (see B-NET).

## 3. Phenotype class per dataset (kept distinct — never merged)

generally-essential (juhas review) · core-essential (poulsen) ·
condition-specific-essential (turner, lee) · general-essential (lee LB) ·
growth-arrest-survival-determinant (basta) · host-condition-fitness (belanger).

## 4. Media / conditions per dataset

| study | Condition/medium | Notes for reconstruction (C-01) |
|---|---|---|
| belanger2022 | host/physiologically-relevant (incl. SCFM) | enumerate exact media from methods |
| lee2015 | LB (general); defined/nutrient (condition-specific) | LB aerobic straightforward |
| turner2015 | SCFM/SCFM2, MOPS-sputum vs MOPS-succinate minimal | SCFM amino-acid recipe published |
| poulsen2019 | rich medium | aerobic rich |
| basta2017 | minimal + 40 mM pyruvate; C-/O2-limited arrest | non-growth arrest state |

## 5. Strain caveats

- **MPAO1** (lee2015): PAO1 sublineage; possible small genomic differences vs the
  reference PAO1 behind iMO1056 — record as a caveat, treat as PAO1-derived.
- **PA14** (basta2017; non-PAO1 poulsen strains): not interchangeable with PAO1;
  requires validated orthology (`ORTHOLOGY_STATUS_REPORT.md`).
- **turner2015**: keep PAO1 and PA14 rows separate; only the PAO1 subset joins
  directly.

## 6. Simulability caveats (honest)

- **Growth-based FBA** predicts genes required for **growth** under a medium. It
  maps naturally onto growth-essentiality (lee general/condition-specific,
  turner, poulsen core).
- **Growth-arrest survival** (basta2017) is **not** a growth phenotype — FBA
  single-gene-deletion growth-essentiality is **not the matching prediction**;
  comparison would be conceptually invalid without a tailored maintenance/ATP
  framework. Flag, do not force.
- **Host-condition fitness** (belanger2022) is partly metabolic (SCFM etc.,
  reconstructable) and partly non-metabolic (out of model scope).

## 7. Recommended validation priority order

1. **lee2015 (MPAO1, LB general-essential)** — cleanest: PAO1-tag labels + simple
   rich medium; strongest first benchmark once supplement obtained.
2. **turner2015 (PAO1 rows, SCFM vs minimal)** — condition-specific, media
   reconstructable.
3. **belanger2022 (PAO1, host/SCFM subset)** — metabolic host-condition fitness.
4. **poulsen2019 (core-essential)** — via Cluster_ID PAO1 members / PA14→PAO1 orthology.
5. **basta2017 (PA14 growth-arrest)** — lowest: needs orthology *and* a
   non-growth comparison framework.

(meegid2022 removed from active scope by user decision 2026-07-06.)

**Gate:** none of the above proceeds to metrics until supplements are downloaded,
parsed with provenance, media reconstructed, and (for PA14 rows) orthology
validated. See `VALIDATION_READINESS.md`.

# PAO1 VALIDATION DATA INVENTORY

**Original inventory:** 2026-07-01 · **Reconciled:** 2026-11-11
**Purpose:** candidate experimental evidence for iMO1056 (PAO1), with strain,
phenotype, mapping and condition limitations. This inventory reflects the
existing artifacts; it does not run or alter an analysis.

The early July statements that all supplements or metrics were missing are
superseded. Raw supplements are local. **V-01 binary metrics exist for the
D-21 MOPS-pyruvate cell; human interpretation remains pending.** See
`VALIDATION_LABEL_MEDIA_OVERLAP.md` and
`v01_mops_pyruvate/V01_BINARY_VALIDATION_REPORT.md`.

## 1. Master table

| study_id | Screened strain / scope | Tier | Phenotype | Supplement in repo? | PAO1-model join | Current role |
|---|---|---|---|---|---|---|
| belanger2022 | PAO1 | 1 | host-condition-fitness; essential calls kept distinct | yes, Data Sheets 1–3 | PAO1 locus IDs | candidate separate condition/phenotype cells; no completed matched validation claimed |
| lee2015 | MPAO1 (PAO1-derived) | 2 | general + condition-specific essential | yes, sd01 + SI | Lee-original PAxxxx IDs, with sublineage caveat | D-20 MOPS-pyruvate positive-overlap layer; not the D-21 binary labels |
| turner2015 | PAO1 + PA14 | 3 | condition-specific essential / fitness | yes, sd01–sd10 | PAO1 subset by locus ID; PA14 subset requires orthology | separate source/condition-specific comparisons; keep strains distinct |
| varadarajan2020 | MPAO1; reanalysis of Lee2015 Tn-seq | 2 | condition-specific Minimal essential calls | yes, Datasets 1–4 + SI | DS1 unique-standard-PAO1 best-hit mappings; exclude unresolved mappings | **D-21 primary binary labels; V-01 metrics executed**; not independent replication |
| poulsen2019 | **9 strains including PA14; excludes PAO1** | 5 | core-essential; retain per-strain/medium calls separately | yes, sd01–sd07 + SI | **no PAO1 identity subset**; PA14_ID reference requires PA14→PAO1 mapping | cross-strain/background path; controlled L-03b draft mapping only under limited approval |
| basta2017 | PA14 (UCBPP-PA14) | 4 | growth-arrest survival | yes, sd1–sd4 + TIFFs | PA14→PAO1 mapping required | needs call derivation and a non-growth comparison framework in addition to mapping |
| juhas2015 | review | 6 | reviewed essentiality | n/a | n/a | background; not a primary gene-label source |

**Poulsen correction:** [primary paper Table 1](https://www.pnas.org/doi/10.1073/pnas.1900570116)
lists BL23, BWH005, BWH013, BWH015, CF77, PS75, PA14, X13273 and 19660.
The earlier inventory's proposed `Cluster_ID` PAO1 members do not exist: PAO1
was not one of the clustered study strains. PAO1 mentions or mapped PAO1 locus
coordinates are not evidence of an assay performed on PAO1.

## 2. Evidence already used in the first cell

- **D-20:** Lee-original MOPS-pyruvate positives, retained as
  `literature_evidence_gene_level_READY_mops_pyruvate_lee2015.csv` (437 rows).
  This is a positive-overlap layer only; absence from that list is not a negative.
- **D-21:** Varadarajan2020 Dataset 1 CDS master + Dataset 4 Minimal-1/2/3 calls,
  with both binary polarities from the same reanalysis. Positive = essential in
  at least 2/3 libraries; negative = not called essential in any of the three;
  1/3 is ambiguous and excluded. Negatives do not establish unconditional
  biological non-essentiality.
- Mapping uses `unique_std_PAO1` best hits in DS1, not a universal MPAO1=PAO1
  identity assumption and not PA14 orthology. Of 1054 model genes, the primary
  universe contains **1025** (214 positive + 811 negative); **18 ambiguous** and
  **11 other model genes** are excluded.
- **V-01:** comparison under reconstructed `mops_pyruvate_lee2015`, threshold
  0.01, objective `PA_Biomass6_DM`; TP=116, FN=98, TN=764, FP=47.
  Metrics and diagnostic error audits exist; interpretation/sign-off is pending.
  This is one condition-specific evaluation, not validation of all conditions.
- Do not mix D-20 positives with D-21 negatives, or count Varadarajan as an
  independent replication of Lee2015.

## 3. Media / conditions and simulability

| study | Experimental condition | Reconstruction / comparison status |
|---|---|---|
| lee2015 / Varadarajan Minimal | MOPS-pyruvate | computational medium reconstructed (DEFINED); predictions and V-01 comparison exist |
| lee2015 LB | rich LB | `LB_approx_lee2015` is PARTIAL; not the primary validation medium |
| turner2015 | MOPS-succinate, MOPS-sputum, SCFM2 | succinate medium and predictions exist; other sides of the contrasts are not completed matched validation cells |
| belanger2022 | host/physiologically-relevant conditions | require separate recipe, phenotype and scope checks; no completed matched cell claimed |
| poulsen2019 | LB, M9, serum, sputum, urine across nine study strains | condition-specific cross-strain work; neither rich-only nor direct PAO1 evidence |
| basta2017 | minimal + pyruvate; carbon-/oxygen-limited arrest | survival during arrest is not the standard FBA growth-deletion phenotype |

Media here are **computational exchange-bound reconstructions** with documented
assumptions, not newly prepared wet-lab media. Host-condition fitness,
growth-arrest survival, general essentiality, core essentiality and
condition-specific essentiality must retain their own phenotype definitions.

## 4. Orthology and remaining work

- PAO1 locus-ID sources and the DS1 MPAO1→PAO1 best-hit path do not depend on
  PA14 orthology. Record the MPAO1 sublineage and mapping exclusions.
- Poulsen's PA14-indexed lists and Basta need cross-strain mapping. The
  **APPROVED_LIMITED** Turner strict 1:1 subset (5,365 pairs) permits controlled
  L-03b draft mapping only, per `ORTHOLOGY_HUMAN_REVIEW_DECISION.md`.
  This supersedes the early claim that no usable mapping source exists, but
  does not make these datasets validation-ready or authorize symbol-only joins.
- The current canonical mapping actually uses official PGD orthology: **1023
  unique, 2 ambiguous, 29 unmapped** model genes. The separate final RBH table
  has **5374 pairs** with structural checks marked **PASSED**. See
  `data/processed/gene_mapping/gene_mapping.csv` and
  `data/processed/ortholog/final/pao1_pa14_orthologs_pseudomonas_rbh_20260712.csv`.
  These observed artifacts do not document a new unrestricted study-use
  approval beyond the recorded D-16 decision or complete a Poulsen/Basta cell.
- Preserve one-to-many, unmapped, strain-unique and absent-from-model cases.
  A PAO1 identifier in a derived join is a coordinate, not evidence that the
  original experiment used PAO1.
- Next for the primary cell: review the frozen FP/FN evidence and state its
  limitations. Other strain × medium × phenotype cells require their own
  provenance and comparability checks before metrics.

(meegid2022 remains outside active scope by the recorded user decision of
2026-07-06.)

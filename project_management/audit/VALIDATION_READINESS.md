# Validation readiness and executed evaluation

**Status reconciled:** 2026-11-11. This replaces the July readiness verdict with
current artifacts; the dated transition record below preserves the earlier gates.

## Current verdict

The first condition-specific model-vs-experiment comparison **has been executed**:
iMO1056 (PAO1) predictions under `mops_pyruvate_lee2015` versus the D-21 frozen
binary universe derived from Varadarajan2020's published reanalysis of Lee2015
Tn-seq data (MPAO1). Raw metrics, error-structure audit and a source-backed
review-evidence pack exist. **Human interpretation/sign-off remains pending;
this is not a claim that the model is fully validated.**

The blanket July statements “no experimental medium”, “only simulated comparison”
and “no metric may be computed” are superseded for this one cell. The teaching
notebook's random-label metrics remain unusable. Other condition/phenotype cells
still require their own reviewed labels, mapping, medium and predictions.

## Implemented media and predictions

| Medium | Model representation | WT growth (/h) | Essential / 1054 at 1% |
|---|---|---|---|
| Default glucose + O2 | model baseline, not the primary experimental comparison | 1.047929 | 166 |
| `mops_pyruvate_lee2015` | DEFINED; MPAO1 context | 0.405339 | 173 |
| `mops_succinate_turner2015` | DEFINED; PAO1 comparator context | 0.552803 | 177 |
| `LB_approx_lee2015` | PARTIAL; not true LB or physiologically calibrated | 14.950548 | 133 |

Sources: [`media_wt_growth.csv`](../../data/processed/conditions/media_wt_growth.csv),
[`condition_essentiality_summary.csv`](../../results/essentiality/condition_essentiality_summary.csv),
and [`src/medium.py`](../../src/medium.py). Reconstruction means recipe-derived
computational exchange bounds with documented assumptions, not wet-lab preparation
or exact reproduction of every physical condition. SCFM2, RPMI, native sputum,
serum, abscess, skin and growth-arrest conditions remain separate gaps; a
MOPS-succinate comparator alone does not reproduce a sputum-versus-succinate contrast.

Research notebooks `04_media_reconstruction.ipynb` and
`05_condition_essentiality.ipynb` exist. V-01 is currently delivered by a script and
report; `06_pao1_validation.ipynb` is not an implemented deliverable.

## Experimental evidence and label policy

All active corpus supplements (Lee, Turner, Belanger, Varadarajan, Poulsen and
Basta) are present locally. Their presence is distinct from approval for a
particular analysis; download-source URLs still have provenance follow-up.

| Evidence | Current permitted use / limitation |
|---|---|
| Lee2015 original MOPS-pyruvate positives (D-20) | 437 promoted positives; separate positive-overlap-only layer. No negatives inferred from absence in Lee Dataset S1. |
| Varadarajan2020 Minimal labels (D-21) | Approved primary binary universe: 214 positive + 811 negative = 1025 in-model genes; 18 ambiguous in-model genes excluded. Both polarities come from this same reanalysis. |
| Other Lee conditions / Turner / Belanger | Reviewed subsets and draft evidence exist, but no blanket condition-matched binary approval follows from D-21. |
| Poulsen2019 | Nine tested strains exclude PAO1; PA14/cluster coordinates require explicit mapping before PAO1-model comparison. |
| Basta2017 | PA14 growth-arrest survival data require call derivation, mapping and a phenotype-appropriate analysis; survival is not FBA growth essentiality. |
| Juhas2015 | Review/background, not an independent primary experimental dataset. |

D-21 positive = essential in at least two of three Minimal libraries; negative =
not called essential in any of the three; one-of-three calls remain ambiguous.
Negative is assay-/condition-specific, not unconditional biological non-essentiality.
Varadarajan reanalyses Lee data; it is **not an independent experimental replication**.
MPAO1 is a PAO1 derivative, so sublineage and annotation/mapping limitations remain.
D-21 uses the reviewed unique-standard-PAO1 map from its supplementary CDS table;
PAO1-tagged Lee/Turner/Belanger rows can join by locus identity. Neither operation
uses PA14 orthology. See [D-21](../../DECISIONS.md#d-21--2026-08-01--mops-pyruvate-experimental-binary-universe-varadarajan2020).

Six phenotype classes stay distinct: general essential, core essential,
condition-specific essential, reduced fitness, growth-arrest survival and
host-condition fitness. D-21 approval does not merge those classes.

## Executed V-01 cell

Locked policy: objective `PA_Biomass6_DM`; medium `mops_pyruvate_lee2015`;
model-positive if KO/WT growth ratio < 0.01. No tuning for metric appearance.

| Cell | Count |
|---|---|
| TP | 116 |
| FN | 98 |
| TN | 764 |
| FP | 47 |
| Total | 1025 |

| Metric | Value |
|---|---|
| Sensitivity / recall | 0.542056 |
| Specificity | 0.942047 |
| Precision | 0.711656 |
| F1 | 0.615385 |
| MCC | 0.538031 |

The full model predicts 173 essentials in this medium; 163 fall inside the D-21
binary universe. Those counts describe different universes and are not contradictory.

Sources: [V-01 binary report](v01_mops_pyruvate/V01_BINARY_VALIDATION_REPORT.md),
[metrics JSON](../../data/processed/validation/v01_mops_pyruvate_metrics.json),
[error audit](v01_mops_pyruvate/V01_ERROR_STRUCTURE_AUDIT.md), and
[review evidence](v01_mops_pyruvate/V01_HUMAN_REVIEW_EVIDENCE.md).
The error categories are diagnostic hypotheses; they do not establish mechanisms
or authorize automatic model/GPR/media changes.

## PA14 mapping status

Current integrated mapping is
[`data/processed/gene_mapping/gene_mapping.csv`](../../data/processed/gene_mapping/gene_mapping.csv),
which records `official_orthology` from the PGD source. Its
[coverage report](../../data/processed/gene_mapping/gene_mapping_coverage.txt)
records **1023 unique, 2 ambiguous and 29 unmapped** model genes (1054 total).
The earlier 386/22/646 symbol-only counts are historical and do not describe
this current artifact. The builder uses the PGD table.

A separate final RBH table,
[`pao1_pa14_orthologs_pseudomonas_rbh_20260712.csv`](../../data/processed/ortholog/final/pao1_pa14_orthologs_pseudomonas_rbh_20260712.csv),
has 5374 pairs; its [validation report](../../data/processed/ortholog/final/Validation_Report.txt)
says PASSED for the recorded technical checks. Those checks do not themselves
approve every downstream experimental mapping or a PA14 model-validation claim.

**Policy versus artifacts:** D-16 and the 2026-07-10 human decision document
Turner-derived strict 1:1 approval limited to controlled draft mapping. Those
working tables are under `data/processed/ortholog/working/`. Later PGD/RBH and
integrated mapping artifacts exist, but this readiness report does not invent
a broader human approval beyond the recorded decisions. Reconcile the artifact
lineage, crosswalk/conflicts and approval scope before a new PA14 comparison;
retain ambiguous and unmapped cases explicitly.

Sources: [human decision](ORTHOLOGY_HUMAN_REVIEW_DECISION.md),
[conflict resolution](ORTHOLOGY_CONFLICT_RESOLUTION_REPORT.md),
[PGD integration](../../docs/methods/ORTHOLOGY_PSEUDOMONAS_INTEGRATION.md).
PA14 mapping does not block the executed MPAO1/PAO1-side V-01 cell.

## Remaining work

1. Review the 98 FN and 47 FP discrepancy explanations and sign off the
   interpretation; distinguish model limitations, plausible model errors and
   experimental/mapping uncertainty.
2. Prepare a supervisor/reviewer-facing methods and results account with the
   correct assay, sublineage, medium assumptions, label universe and coverage.
3. Extend other conditions only after their own prerequisites pass; `LB_approx`
   remains an approximation and is not the primary validation medium.
4. Complete remaining evidence-promotion, source-URL and PA14 lineage/approval reconciliation
   without mixing D-20 positives with D-21 negatives or retuning the frozen cell.

Current blocker scope is in [BLOCKERS.md](../../BLOCKERS.md); the label/media
alignment matrix is in [VALIDATION_LABEL_MEDIA_OVERLAP.md](../../VALIDATION_LABEL_MEDIA_OVERLAP.md).

## Dated transition record

- **2026-06-26 / 2026-07-01:** only baseline predictions and a simulated-label
  teaching comparison were available; experimental metrics were correctly gated.
- **2026-07-06:** all corpus supplements obtained; Lee/Turner/Belanger draft
  parsing followed. Raw presence alone did not unlock metrics.
- **2026-07-10:** Turner 1:1 orthology approved for limited draft mapping; PGD
  export obtained separately. Neither became a blanket PA14 validation approval.
- **2026-07-24:** two DEFINED media and the PARTIAL LB approximation implemented;
  condition-specific predictions subsequently exported.
- **2026-07-29 (D-20):** Lee-original MOPS-pyruvate positive set promoted;
  overlap-only analysis performed without an inferred negative class.
- **2026-08-01 (D-21/V-01):** binary universe approved and primary metrics
  executed. Error-structure audit and review evidence exist; final interpretation
  is pending. Earlier readiness prohibitions no longer describe this cell.
- **2026-11-11:** documentation reconciled against these existing artifacts;
  no new model simulations, label changes or validation approvals are asserted.

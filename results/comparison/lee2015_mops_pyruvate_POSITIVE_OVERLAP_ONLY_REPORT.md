# Lee2015 MOPS-pyruvate — POSITIVE OVERLAP ONLY

**Date:** 2026-07-29  
**Labels:** `data/processed/literature/gene_level/literature_evidence_gene_level_READY_mops_pyruvate_lee2015.csv` (READY; 437 positives)  
**Predictions:** `results/essentiality/gene_essentiality_mops_pyruvate_lee2015.csv`  
**Medium:** `mops_pyruvate_lee2015` · **threshold_ratio:** 0.01 · **WT growth:** 0.405339030635686 /h  
**Decision:** D-20 / human review 2026-07-29 APPROVED_FOR_PROMOTION (positives only)

## Policy (explicit)

**Precision, recall, specificity, F1, MCC, accuracy, and a full confusion matrix
are NOT computed** — experimental NON-essential universe is undefined. Absence
from the Lee MOPS-pyruvate essential list must not be treated as experimental
non-essentiality. Predicted essentials outside the positive label set are
**not** called false positives.

Allowed here: positive-label coverage + overlap with model predictions only.

## Counts (measured)

| Metric | Value |
|---|---|
| n_positive_labels | **437** |
| n_in_model | **228** |
| n_absent_from_model | **209** |
| n_predicted_essential @0.01 | **173** |
| labels AND predicted essential (recovered) | **123** |
| in-model positives not recovered | **105** |
| predicted essential not in positive label set | **50** (not FP) |

## Outputs

- `results/comparison/lee2015_mops_pyruvate_POSITIVE_OVERLAP_ONLY_summary.csv`
- `results/comparison/lee2015_mops_pyruvate_POSITIVE_OVERLAP_ONLY_recovered.csv`
- `results/comparison/lee2015_mops_pyruvate_POSITIVE_OVERLAP_ONLY_not_recovered.csv`
- `results/comparison/lee2015_mops_pyruvate_POSITIVE_OVERLAP_ONLY_predicted_not_in_positive_labels.csv`
- `results/comparison/lee2015_mops_pyruvate_POSITIVE_OVERLAP_ONLY_labels_absent_from_model.csv`

## Next human decision (proposed; not implemented)

Define a defensible experimental **negative universe** for MOPS-pyruvate before
any full V-01 confusion-matrix metrics are allowed.

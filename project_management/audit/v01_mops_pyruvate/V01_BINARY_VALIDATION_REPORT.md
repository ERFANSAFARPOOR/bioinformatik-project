# V-01 Binary Validation Report — MOPS-pyruvate (D-21)

**Status:** `V01_BINARY_METRICS_COMPUTED_PENDING_HUMAN_INTERPRETATION`  
**Experimental labels:** D-21 frozen primary binary universe  
**D-20 Lee-original positives used in primary matrix:** **No**

## Modeling policy (locked; not tuned)

| Item | Value |
|---|---|
| Model | iMO1056 / `MODEL1507180020` |
| Model path | `models/paeruginosa_MODEL1507180020.xml` |
| Objective | `PA_Biomass6_DM` |
| Medium | `mops_pyruvate_lee2015` (DEFINED) |
| Solver | `optlang.glpk_interface` |
| WT growth | 0.40533903063568605 (status=optimal) |
| Essentiality cutoff | `growth_ratio < 0.01` → MODEL_POSITIVE |
| Policy sources | D-09; D-17; `src/gene_essentiality.py` |

## Join integrity

| Check | Value |
|---|---|
| Experimental genes | 1025 |
| Matched prediction rows | 1025 |
| Unmatched | 0 |
| Duplicates | 0 |
| Ambiguous in primary | 0 |

## Confusion matrix

| Cell | Count | Definition |
|---|---|---|
| TP | 116 | experimental essential ∧ model essential |
| FN | 98 | experimental essential ∧ model non-essential |
| TN | 764 | experimental negative ∧ model non-essential |
| FP | 47 | experimental negative ∧ model essential |
| n | 1025 | TP+TN+FP+FN |

Identities: TP+FN=214 (expect 214);
TN+FP=811 (expect 811).

## Metrics (raw)

| Metric | Value |
|---|---|
| Sensitivity / recall / TPR | 0.542056 |
| Specificity / TNR | 0.942047 |
| Precision / PPV | 0.711656 |
| NPV | 0.886311 |
| F1 | 0.615385 |
| Accuracy | 0.858537 |
| Balanced accuracy | 0.742051 |
| MCC | 0.538031 |

Predicted essential (MODEL_POSITIVE) in primary join:
163  
Predicted non-essential (MODEL_NEGATIVE):
862

## Error-set artifacts

- FP: `data\processed\validation\v01_mops_pyruvate_false_positives.csv` (n=47)
- FN: `data\processed\validation\v01_mops_pyruvate_false_negatives.csv` (n=98)
- TP: `data\processed\validation\v01_mops_pyruvate_true_positives.csv` (n=116)
- TN: `data\processed\validation\v01_mops_pyruvate_true_negatives.csv` (n=764)

## Explicit non-claims

This report does **not** conclude that iMO1056 is validated, good, or bad.
No medium/threshold/model tuning was performed.
Next stage: **human review** of the confusion matrix and FP/FN structure.

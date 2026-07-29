# Label ↔ media ↔ prediction overlap (status note)

**Date:** 2026-07-24 (updated **2026-07-29**)  
**Purpose:** document which experimental rows can be matched to media actually
built, and what remains before **full** V-01 metrics are allowed.  
**Rule:** no precision/recall/F1/MCC/specificity / full confusion matrix until an
experimental **negative universe** is separately reviewed (D-20).

## Media implemented

| medium_id | label | strain_context | Experimental match intent |
|---|---|---|---|
| `mops_pyruvate_lee2015` | DEFINED | MPAO1 | Lee MOPS-pyruvate / “Min” |
| `mops_succinate_turner2015` | DEFINED | PAO1 | Turner MOPS-succinate comparator |
| `LB_approx_lee2015` | PARTIAL | MPAO1 | Lee LB rich context (approximation only; not primary) |

Derived configs: `data/processed/conditions/`.

## First validation cell (updated 2026-07-29)

| Item | Status |
|---|---|
| Labels | **Promoted** derived READY: `literature_evidence_gene_level_READY_mops_pyruvate_lee2015.csv` (**437** standard `PAxxxx` positives; D-20) |
| `PA0728.1` | Raw retained; `absent_from_model/unmapped`; not in READY set |
| Medium | `mops_pyruvate_lee2015` (DEFINED) |
| Predictions | `results/essentiality/gene_essentiality_mops_pyruvate_lee2015.csv` (173 essential @ 0.01; WT ≈ 0.405 /h) |
| Allowed analysis | **Positive-overlap only** → `results/comparison/lee2015_mops_pyruvate_POSITIVE_OVERLAP_ONLY_*` |
| Full V-01 metrics | **Still gated** — experimental non-essential universe undefined |

### Measured positive overlap (2026-07-29)

| Metric | Value |
|---|---|
| n_positive_labels | 437 |
| n_in_model | 228 |
| n_absent_from_model | 209 |
| n_predicted_essential @0.01 | 173 |
| positives recovered (labels ∩ predicted essential) | 123 |
| in-model positives not recovered | 105 |
| predicted essential not in positive set | 50 (**not** called FP) |

Precision / recall / specificity / F1 / MCC / full confusion matrix were **not**
computed (policy).

## Other READY_ONLY rows (`literature_evidence_gene_level_READY_ONLY.csv`, n=2607)

| Study | READY_ONLY subset | Built medium | Match quality |
|---|---|---|---|
| lee2015 | 351 generally-essential (LB + MOPS-pyruvate + sputum) | needs sputum + multi-medium intersection | WEAK |
| lee2015 per-medium LB / sputum / BHI / serum / 0.1×LB | still NEEDS_REVIEW (not in D-20) | — | HELD |
| turner2015 | sputum vs MOPS-succinate / SCFM2 / … | succinate only half of contrast | PARTIAL |
| belanger2022 | RPMI / host niches | not built | NO match |

## What remains before full V-01 metrics

1. ~~Promote Lee MOPS-pyruvate positives~~ **DONE (D-20)**  
2. ~~Predictions under that medium~~ **DONE**  
3. **Define experimental negative universe** for MOPS-pyruvate (human decision)  
4. Only then: confusion matrix + precision/recall/specificity/F1/MCC for this cell  
5. Other media/phenotypes remain separate cells with their own gates  

## Explicitly still out of scope

- Treating absence-from-essential-list as non-essential without review  
- PA14 path / orthology merges into `gene_mapping.csv` for this cell  
- Claiming paper-ready full validation  
- Citing teaching nb03 simulated metrics  
- Using `LB_approx` as the primary validation medium  

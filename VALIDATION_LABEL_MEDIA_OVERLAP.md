# Label ↔ media ↔ prediction overlap (status note)

**Date:** 2026-07-24 (updated **2026-08-01**, V-01 metrics executed)  
**Purpose:** document which experimental rows can be matched to media actually
built, and the status of V-01 binary metrics.  
**Rule:** Do not mix D-20 Lee-original positives with D-21 Varadarajan negatives
in one primary matrix. Raw V-01 metrics exist; human interpretation pending —
do **not** claim the model is validated.

## Media implemented

| medium_id | label | strain_context | Experimental match intent |
|---|---|---|---|
| `mops_pyruvate_lee2015` | DEFINED | MPAO1 | Lee MOPS-pyruvate / “Min” |
| `mops_succinate_turner2015` | DEFINED | PAO1 | Turner MOPS-succinate comparator |
| `LB_approx_lee2015` | PARTIAL | MPAO1 | Lee LB rich context (approximation only; not primary) |

Derived configs: `data/processed/conditions/`.

## First validation cell (updated 2026-08-01)

| Item | Status |
|---|---|
| Primary binary labels (D-21) | **READY** Varadarajan2020 Minimal universe: `varadarajan2020_lee2015_minimal_gene_labels_READY.csv` + frozen `…_PRIMARY_BINARY_UNIVERSE.csv` (**214** POSITIVE + **811** NEGATIVE = **1025**; **18** AMBIGUOUS excluded) |
| D-20 Lee-original positives | Separate layer only: `literature_evidence_gene_level_READY_mops_pyruvate_lee2015.csv` (**437**); positive-overlap-only; **do not** pair with D-21 negatives |
| Medium | `mops_pyruvate_lee2015` (DEFINED) |
| Predictions | `results/essentiality/gene_essentiality_mops_pyruvate_lee2015.csv` (173 essential @ 0.01; WT ≈ 0.405 /h) |
| Allowed analysis now | Positive-overlap (D-20) **and** primary binary metrics on D-21 universe |
| Full V-01 metrics | **`V01_BINARY_METRICS_COMPUTED_PENDING_HUMAN_INTERPRETATION`** — raw metrics in `data/processed/validation/v01_mops_pyruvate_*`; not a validation claim |

### D-21 / V-01 primary binary metrics (2026-08-01; raw)

Artifacts: `data/processed/validation/v01_mops_pyruvate_*` +
`project_management/audit/v01_mops_pyruvate/V01_BINARY_VALIDATION_REPORT.md`.
Script: `scripts/validation/run_v01_mops_pyruvate_binary_validation.py`.
Policy locked: medium `mops_pyruvate_lee2015`, threshold `0.01`, objective
`PA_Biomass6_DM`. No tuning performed for metric appearance.

### D-20 measured positive overlap (2026-07-29; unchanged)

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
computed in the D-20 step (policy). They **were** computed later for the D-21
primary binary universe (see V-01 artifacts above); interpretation is pending.

## Other READY_ONLY rows (`literature_evidence_gene_level_READY_ONLY.csv`, n=2607)

| Study | READY_ONLY subset | Built medium | Match quality |
|---|---|---|---|
| lee2015 | 351 generally-essential (LB + MOPS-pyruvate + sputum) | needs sputum + multi-medium intersection | WEAK |
| lee2015 per-medium LB / sputum / BHI / serum / 0.1×LB | still NEEDS_REVIEW (not in D-20) | — | HELD |
| turner2015 | sputum vs MOPS-succinate / SCFM2 / … | succinate only half of contrast | PARTIAL |
| belanger2022 | RPMI / host niches | not built | NO match |

## What remains after raw V-01 metrics

1. ~~Promote Lee MOPS-pyruvate positives~~ **DONE (D-20)**  
2. ~~Predictions under that medium~~ **DONE**  
3. ~~Define experimental binary universe (incl. negatives)~~ **DONE (D-21)**  
4. ~~Execute confusion matrix + binary metrics~~ **DONE (raw; pending human interpretation)**  
5. **Human review** of confusion matrix / FP / FN (no auto-tuning)  
6. Other media/phenotypes remain separate cells with their own gates  

## Explicitly still out of scope

- Mixing D-20 Lee-original positives with D-21 Varadarajan negatives  
- Treating Varadarajan2020 as independent replication of Lee2015  
- Treating absence-from-Lee-Dataset-S1 as non-essential  
- PA14 path / orthology merges into `gene_mapping.csv` for this cell  
- Claiming paper-ready full validation before metrics execution  
- Citing teaching nb03 simulated metrics  
- Using `LB_approx` as the primary validation medium  

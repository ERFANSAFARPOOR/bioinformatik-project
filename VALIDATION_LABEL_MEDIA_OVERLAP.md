# Label ↔ media ↔ prediction overlap (status note)

**Date:** 2026-07-24 (updated **2026-08-01**, V-01 metrics executed)  
**Documentation reconciled:** 2026-11-11; existing metrics unchanged.
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

These are computational reconstructions, not new wet-lab media. `DEFINED`
describes the recipe; some components are unmodeled. The MOPS main-carbon
exchange uptake cap is 10 mmol/gDW/h by model convention; `LB_approx` caps
each amino-acid proxy separately at 10, not total carbon uptake. Salts/O2
are effectively unlimited.
Recipe concentration is not a measured uptake flux. Succinate predictions
exist, but a completed matched binary comparison does not; `LB_approx` remains
exploratory.

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

Existing confusion matrix: **TP=116, FN=98, TN=764, FP=47; n=1025**.
Recall=0.542056; specificity=0.942047; precision=0.711656; F1=0.615385;
MCC=0.538031. There are 173 predicted essentials over all 1054 model genes,
but 163 within the 1025-gene primary join. Eighteen ambiguous model genes and
11 without an eligible D-21 mapping are outside that join.

D-21 positives mean essential in at least 2/3 Minimal libraries; negatives mean
not called essential in any of the three, not proven universally non-essential.
The MPAO1-to-PAO1 mapping comes from Varadarajan DS1 unique standard best hits;
it does not require PA14 orthology. Error audit and review evidence are already
prepared under `project_management/audit/v01_mops_pyruvate/`; final human
interpretation/sign-off is still pending.

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
- Claiming paper-ready full validation from the executed metrics alone, before
  interpretation/sign-off and resolution of remaining scope limitations
- Citing teaching nb03 simulated metrics  
- Using `LB_approx` as the primary validation medium  

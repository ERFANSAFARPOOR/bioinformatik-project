# Label ↔ media ↔ prediction overlap (status note)

**Date:** 2026-07-24  
**Purpose:** document which READY_ONLY experimental rows can be matched to media
actually built in this run, and what remains before V-01 metrics are allowed.  
**Rule:** no precision/recall/F1/MCC in this document or this session.

## Media implemented (this run)

| medium_id | label | strain_context | Experimental match intent |
|---|---|---|---|
| `mops_pyruvate_lee2015` | DEFINED | MPAO1 | Lee MOPS-pyruvate / “Min” |
| `mops_succinate_turner2015` | DEFINED | PAO1 | Turner MOPS-succinate comparator |
| `LB_approx_lee2015` | PARTIAL | MPAO1 | Lee LB rich context (approximation only) |

Derived configs: `data/processed/conditions/`.  
WT growth (measured, reccobra39/GLPK): see `media_wt_growth.csv`.

## READY_ONLY rows (`literature_evidence_gene_level_READY_ONLY.csv`, n=2607)

### Direct / partial condition match to built media

| Study | READY_ONLY subset | Phenotype class | Built medium | Match quality |
|---|---|---|---|---|
| lee2015 | 351 generally-essential (“three primary media: LB + MOPS-pyruvate + CF sputum”) | generally-essential | Needs **intersection** of predictions under LB_approx ∩ MOPS-pyruvate ∩ (sputum not built) | **WEAK** — sputum medium not built; general-essential is cross-media consensus, not a single medium |
| lee2015 per-medium MOPS-pyruvate / LB | in **NEEDS_REVIEW** (not READY_ONLY) | condition-specific-essential | `mops_pyruvate_lee2015` / `LB_approx` | **HELD** — excluded from first validation by `LEE2015_PER_MEDIUM_REVIEW.md` |
| turner2015 | CF sputum vs MOPS-succinate (104 + 52 biosynthetic) | reduced-fitness / condition context | `mops_succinate_turner2015` is the **minimal comparator**, not the sputum condition | **PARTIAL** — can predict essentials on MOPS-succinate; sputum/SCFM2 side not built in this run |
| turner2015 | initial library general essential (336) | generally-essential | rich / complex initial medium — **not** MOPS-succinate | **NO clean match** to Batch A DEFINED media |
| belanger2022 | RPMI / RPMI+serum / abscess / skin / T0 rich | various | none built (RPMI held; niches = MEDIA_GAP) | **NO match** this run |

### Gene ID overlap (identity join, PAO1/MPAO1)

- Model genes: 1054 `PAxxxx`.
- READY_ONLY mapped PAO1 IDs are identity-joined (Lee MPAO1 / Turner PAO1 /
  Belanger PAO1) — orthology not required for these rows.
- Exact gene-list sizes for metric-ready joins are **not** finalized here because
  condition matching is incomplete (table above).

## What is still required before V-01 is allowed

1. **Condition-matched label set** for at least one medium that is both
   READY_ONLY (or promoted) **and** built as DEFINED (preferred) or honestly
   PARTIAL with documented caveats.
2. **Strongest near-term candidates after this run:**
   - Promote / resolve Lee per-medium **MOPS-pyruvate** NEEDS_REVIEW → then
     compare to `mops_pyruvate_lee2015` predictions.
   - Optionally build SCFM2 PARTIAL (out of scope this run) for Turner sputum-side
     contrasts; MOPS-succinate alone is only half of Turner’s contrast design.
3. **Predictions** under those media written to `results/essentiality/` (S-01).
4. Explicit decision that PARTIAL `LB_approx` is or is not allowed in V-01
   (recommendation: **sensitivity only**, not primary).
5. Only then: confusion matrix + precision/recall/F1/MCC **per phenotype class**,
   never pooled binary collapse; never cite teaching nb03.

## V-01 design (gated plan only — do not run)

```
IF labels_ready AND media_built AND predictions_exist AND condition_ids_match:
    for each (medium_id, phenotype_class):
        join on mapped_pao1_gene_id
        compute confusion matrix + precision/recall/specificity/F1/MCC
        report coverage (mapped / unmapped / absent / no-GPR)
ELSE:
    refuse metrics (B-SCI-01)
```

Primary proposed first metric cell (when unlocked):  
**Lee MOPS-pyruvate condition-specific essentials (after READY promotion) ×
`mops_pyruvate_lee2015` predictions @ threshold 0.01 (with sensitivity).**

Secondary (sensitivity): Lee generally-essential vs intersection of predictions —
only with sputum gap documented.

## Explicitly still out of scope

- PA14 path (Poulsen/Basta), PGD↔Turner merge into `gene_mapping.csv`
- Claiming paper-ready validation
- Building native sputum / serum / abscess / skin as DEFINED
- Citing nb03 simulated metrics

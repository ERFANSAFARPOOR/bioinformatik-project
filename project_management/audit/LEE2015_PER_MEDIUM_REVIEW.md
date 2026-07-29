# LEE2015_PER_MEDIUM_REVIEW.md

**Date:** 2026-07-07 · **Branch:** `claude/revival-audit` · **Env:** `reccobra39`
**Scope:** the 2,541 Lee 2015 **per-medium condition-specific-essential** rows in
`data/processed/literature_evidence_gene_level_NEEDS_REVIEW.csv` (all
`review_status = NEEDS_REVIEW`). Decides whether each medium can be promoted.
**No promotion performed this cycle; no metrics.**

## Source locators (all rows)
- `source_file = pnas.1422186112.sd01.xlsx`, `source_sheet = All essential genes`
  (header on Excel row 2; data from row 3; gene col `PA number`, PAO1 `PAxxxx`).
- Per-medium `source_column`: `LB sum (of 6)`, `Min sum (of 3)`,
  `Sputum sum (of 4)`, `BHI (of 1)`, `0.1X LB (of 1)`, `Serum (of 1)`.
- Method/threshold source: Lee 2015 **SI Materials and Methods** ("Sequence Data
  Analysis") — see `THRESHOLD_METHOD_AUDIT.md` (lee2015).

## What is known (sourced)
- Per-run candidate essential: gene with **zero** insertion reads/hits, or values
  below a **P = 0.001** cutoff on a log2-normal fit (Fig S3: x < 6.3).
- **SI consensus rule (verbatim):** *"genes found for at least two of three LB
  pools, two of three MOPS-pyruvate pools, or three of four sputum agar pools."*
- Column denominators confirmed from the data: LB max = 6, Min max = 3, Sputum
  max = 4, BHI/0.1×LB/Serum max = 1.
- Media codes (Table S3): 1=LB, 2=MOPS-pyruvate, 3=sputum agar, 4=0.1× LB,
  5=serum agar, 6=BHI.
- Current parser thresholds (emitting a row as essential-in-medium): LB ≥ 4 of 6,
  Min ≥ 2 of 3, Sputum ≥ 3 of 4, singles ≥ 1 of 1.

## What remains ambiguous
- **LB `sum (of 6)`:** the SI rule is stated in **pools** ("2 of 3 LB pools"), but
  the column denominator is **6** (assays: LB-1 had 3 technical-replicate assays,
  LB-2 had 2). The mapping of "2 of 3 pools" onto a 0–6 **assay** count is **not
  stated verbatim** → the parser's ≥4/6 (">half of assays") is an *interpretation*.
  **AMBIGUOUS.**
- **BHI / 0.1× LB / serum `(of 1)`:** single pool/assay each → "essential" = a
  single-run candidate-essential call. Well-defined arithmetically but **single
  replicate** (no consensus, low statistical confidence). The paper frames these
  as *"additional media"* used to test the general-essential set, not as robust
  condition-specific screens. **LOW CONFIDENCE.**

## What is (near-)resolved
- **`Min sum (of 3)`** and **`Sputum sum (of 4)`:** the column denominators
  (3, 4) **exactly match** the SI's stated pool counts ("three MOPS-pyruvate
  pools", "four sputum agar pools"), and the parser thresholds (≥2, ≥3) **match
  the SI verbatim**. The pool↔assay ambiguity effectively does not apply here —
  the columns count pools. These are the **strongest** per-medium calls.
  *(Caveat: this equivalence is inferred from the denominator/threshold match, not
  from a sentence that literally says "the Min/Sputum sum column counts pools";
  hence a human confirmation is still recommended before promotion.)*

## Per-condition decision
| Condition (column) | Rows | Ambiguity | Recommendation |
|---|---|---|---|
| MOPS-pyruvate (`Min sum (of 3)`) | 437 | resolved (denom = SI pools; ≥2/3 verbatim) | **Strongest candidate for promotion** — retain; promote to READY only after a human confirms column = pools. Keep NEEDS_REVIEW this cycle. |
| CF sputum agar (`Sputum sum (of 4)`) | 378 | resolved (denom = SI pools; ≥3/4 verbatim) | Same as above — retain; promote after confirmation. Keep NEEDS_REVIEW this cycle. |
| LB (`LB sum (of 6)`) | 423 | **open** (6 assays vs 3 pools) | **Stay NEEDS_REVIEW.** Do not promote until the assay↔pool mapping is confirmed. |
| BHI (`BHI (of 1)`) | 470 | single-replicate | **Stay NEEDS_REVIEW / exclude from first validation** (low confidence). |
| 0.1× LB (`0.1X LB (of 1)`) | 392 | single-replicate | Stay NEEDS_REVIEW / exclude from first validation. |
| serum agar (`Serum (of 1)`) | 441 | single-replicate | Stay NEEDS_REVIEW / exclude from first validation. |

## Overall recommendation (conservative)
- **Keep all 2,541 Lee per-medium rows as NEEDS_REVIEW this cycle** (no
  review_status change; no promotion). The hard rule "unknowns stay NEEDS_REVIEW"
  applies to the LB and single-replicate media, and the Min/Sputum equivalence,
  while strongly indicated, is inferred rather than verbatim.
- **For the first validation:** use the **READY_ONLY** set (general-essential:
  Lee 351, Turner 336, Belanger 616; plus Turner/Belanger condition & host rows).
  **Exclude** the Lee per-medium rows from the first validation.
- **Next step to unblock:** confirm from Lee SI / author whether the `X sum (of N)`
  columns count **pools** (then MOPS-pyruvate and sputum can promote directly; LB
  needs the assay→pool rule) — a one-line source confirmation, not new data.
- Lee **general-essential** rows (the `General essential genes` sheet) remain
  **READY** — their definition + consensus threshold are fully sourced and
  unambiguous; they are already in `READY_ONLY`.
## Human review note: MOPS-pyruvate row-count reconciliation

**Review date:** 2026-07-29  
**Reviewer:** Human review

The `General essential genes` worksheet in the Lee2015 supplementary
workbook was manually filtered using the column:

`Min sum (of 3)`

Only rows with values `2` or `3` were retained as candidate positive
MOPS-pyruvate essentiality calls.

### Manual result

- Visible positive rows in the source workbook: **438**
- Rows retained in the processed `PAxxxx` evidence set: **437**
- Non-standard source identifier identified: **PA0728.1**

### Identifier review

Searches for both `PA0728.1` and `PA0728` in the model prediction file
returned no matches.

Therefore:

- `PA0728.1` is retained unchanged in the raw source workbook.
- It is not renamed to `PA0728`.
- It is not deleted from the source evidence.
- It is excluded only from the direct model identity join.
- It is classified as `absent_from_model / unmapped`.
- No automatic mapping is permitted without an authoritative annotation source.

### Blank-value policy

Blank values in `Min sum (of 3)` are treated as missing or unavailable
condition-specific evidence, not as zero and not as non-essential calls.

### Human interpretation and promotion decision

**Human review decision:** `APPROVED_FOR_PROMOTION`  
**Scope:** Lee2015 MOPS-pyruvate positive essentiality labels only

The Lee2015 Supporting Information explicitly states that the
MOPS-pyruvate consensus essential-gene set was derived from genes found
in at least two of the three MOPS-pyruvate mutant pools.

The workbook column `Min sum (of 3)` contains the corresponding
three-pool MOPS-pyruvate essentiality counts. Therefore, rows with:

`Min sum (of 3) >= 2`

are accepted as experimentally supported positive MOPS-pyruvate
essentiality calls.

### Row-count reconciliation

Manual filtering of the source workbook produced:

- **438 source-positive rows** with `Min sum (of 3)` equal to `2` or `3`
- **437 standard `PAxxxx` identifiers** eligible for processed gene-level evidence
- **1 non-standard identifier:** `PA0728.1`

`PA0728.1` has `Min sum (of 3) = 3` and remains preserved unchanged
in the raw source evidence. Neither `PA0728.1` nor `PA0728` was found
in the iMO1056 model-gene universe. It is therefore classified as
`absent_from_model / unmapped` and excluded only from the direct
model identity join. No automatic renaming or remapping is performed.

### Promotion authorization

The **437 standard `PAxxxx` positive labels** are approved for promotion
from:

`NEEDS_REVIEW / PENDING_HUMAN_SIGNOFF`

to:

`READY`

for the Lee2015 MOPS-pyruvate validation cell only.

### Scope limitation

This decision approves only experimentally positive essential labels.

It does not define an experimental non-essential universe. Absence from
the Lee2015 MOPS-pyruvate essential-gene list must not be interpreted as
experimental non-essentiality by default.

Therefore, this approval does not yet authorize calculation of:

- specificity
- precision
- F1 score
- MCC
- a full confusion matrix

Until a separately reviewed experimental negative universe is defined,
the permitted analysis is limited to positive-label coverage and overlap
with model predictions.

### Source confirmation

- **Study:** Lee et al. (2015)
- **Document:** Supporting Information
- **Section:** SI Materials and Methods → Sequence Data Analysis
- **Location:** page 1 of 7
- **Confirmed rule:** MOPS-pyruvate consensus requires detection in at
  least two of three MOPS-pyruvate pools
- **Human review date:** 2026-07-29
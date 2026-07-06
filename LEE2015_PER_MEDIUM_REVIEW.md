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

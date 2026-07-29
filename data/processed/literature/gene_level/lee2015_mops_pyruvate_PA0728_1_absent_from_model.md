# PA0728.1 — Lee2015 MOPS-pyruvate absent_from_model note

**Date:** 2026-07-29  
**Decision source:** `project_management/audit/LEE2015_PER_MEDIUM_REVIEW.md`
(Human review note: MOPS-pyruvate…; APPROVED_FOR_PROMOTION for standard PAxxxx only)

## Facts (measured / reviewed)
- Workbook `All essential genes`, column `Min sum (of 3)`: **PA0728.1 = 3**
  (positive MOPS-pyruvate essentiality call in source).
- Neither `PA0728.1` nor `PA0728` appears in iMO1056 model gene IDs
  (`results/essentiality/gene_essentiality_mops_pyruvate_lee2015.csv`).
- Raw source identifier is **retained unchanged** in
  `data/raw/literature/lee2015/pnas.1422186112.sd01.xlsx` (read-only).

## Classification
- `absent_from_model / unmapped`
- Excluded from the processed READY identity-join set (437 standard `PAxxxx`)
- **Not** renamed to `PA0728`
- **No** automatic remapping without an authoritative annotation source

## Implication for overlap analysis
PA0728.1 is counted in the workbook's 438 Min≥2 rows but not among the 437
READY positive labels used for model identity join.

# LEE2015 MOPS-pyruvate — human review packet (V-01 cell prep)

**Date:** 2026-07-29  
**Target cell:** Lee 2015 · MOPS-pyruvate · condition-specific-essential  
vs model predictions `mops_pyruvate_lee2015` @ `threshold_ratio = 0.01`  
**Hard constraints honored:** no confusion-matrix metrics; no precision/recall/
specificity/F1/accuracy/MCC; no raw-file edits; no canonical overwrite; no
automatic READY promotion; `DECISIONS.md` untouched; no commit/push.

Related prior audit: `project_management/audit/LEE2015_PER_MEDIUM_REVIEW.md`  
Parse notes: `data/raw/literature/lee2015/SUPPLEMENT_PARSE_NOTES.md`

---

## A. Source workbook reconciliation

**File:** `data/raw/literature/lee2015/pnas.1422186112.sd01.xlsx`  
**Sheet:** `All essential genes` (Excel row 2 = header; data from Excel row 3)  
**Candidate column:** `Min sum (of 3)` (MOPS-pyruvate)

| Check | Result |
|---|---|
| Rows with Min sum (of 3) >= 2 | **438** |
| Standard `PAxxxx` among those | **437** |
| Nonstandard locus tags among those | **1**: PA0728.1 |
| Min values among included (>=2) rows | {3.0: 365, 2.0: 73} |
| All included Min values are 2 or 3? | **True** |
| Rows with Min 0 or 1 included in candidate? | **0** (must be 0) |
| Workbook rows with Min in {0,1} (excluded) | **109** |

### Why processed has 437 standard PAxxxx rather than 438 workbook rows

Workbook rows with Min sum (of 3) >= 2: **438**. Of these, **1** locus tag(s) are nonstandard (PA0728.1) and are excluded from the standard-PAxxxx processed candidate set, leaving **437** standard `PAxxxx` rows. Processed filter yields **437** rows (match).

Nonstandard tags (e.g. `PA0728.1`) are not model gene IDs (`^PA\d+$`) and were
not emitted as standard gene-level evidence rows in the NEEDS_REVIEW parse.

---

## B. Processed evidence integrity

**Source file:** `data/processed/literature/gene_level/literature_evidence_gene_level_NEEDS_REVIEW.csv`

Exact filter:
- `study_id == lee2015`
- `phenotype_class == condition-specific-essential`
- `medium == MOPS-pyruvate`
- `source_column == Min sum (of 3)`
- `review_status == NEEDS_REVIEW`

| Metric | Count |
|---|---|
| Row count | **437** |
| Unique `original_gene_id` | **437** |
| Unique `mapped_pao1_gene_id` | **437** |
| Duplicate `original_gene_id` rows | **0** |
| Duplicate `mapped_pao1_gene_id` rows | **0** |
| Invalid `original_gene_id` (not `^PA\d+$`) | **0** |
| Invalid `mapped_pao1_gene_id` (not `^PA\d+$`) | **0** |

**Mapping methods:** {'identity(PAO1)': 437}  
**Mapping confidence:** {'high': 437}

**Source-row reconciliation:** 0 source-row mismatches against workbook Excel row numbers (data start = Excel row 3).

**Workbook-value reconciliation:** 0 workbook-value failures for included genes: every processed gene is in the workbook Min>=2 set, and all such Min values are 2 or 3.

**Set differences:**
- In processed but not in workbook Min>=2 set: (none)
- Standard workbook Min>=2 missing from processed: (none)
- Nonstandard workbook Min>=2 not in processed (expected): ['PA0728.1']

---

## C. Prediction coverage

**Prediction file:** `results\essentiality\gene_essentiality_mops_pyruvate_lee2015.csv`

| Metric | Value |
|---|---|
| Total model genes | **1054** |
| Predicted essential (`is_essential`) | **173** |
| `threshold_ratio` | **0.01** |
| Wild-type growth (1/h) | **0.405339030635686** |
| Positive labels (unique mapped PAO1) | **437** |
| Labels present in model | **228** |
| Labels absent from model | **209** |

Absent genes listed in:
`results/comparison/lee2015_mops_pyruvate_labels_absent_from_model.csv`

Per-label coverage table (no metrics):
`results/comparison/lee2015_mops_pyruvate_coverage_audit.csv`

---

## D. Critical negative-label gate

The filtered NEEDS_REVIEW evidence for this cell contains **only positive
essential calls** (genes called essential on MOPS-pyruvate by the Min>=2 rule).

**Therefore:**
- A one-sided coverage / overlap audit against model predictions is possible.
- **Full confusion-matrix metrics** (including specificity, precision, F1, MCC,
  accuracy) **require a defensible experimental non-essential universe**.
- **Do not assume** that absence from the Lee essential list means the gene is
  experimentally non-essential, unless that assumption is separately reviewed
  and documented (Tn-seq libraries have insertion blind spots, annotation gaps,
  and the sheet is an essential-call table — not a complete essential/non-essential
  census of the genome).

This packet intentionally computes **no** precision/recall/F1/MCC.

---

## Human decisions still required

### 1. Positive-label promotion (this packet)
Confirm that Lee SI column `Min sum (of 3)` counts **MOPS-pyruvate pools** (not
assays), so the parser rule Min >= 2 of 3 matches the SI consensus verbatim.
Until that one-line confirmation, keep `review_status = NEEDS_REVIEW` and
`human_review_decision = PENDING_HUMAN_SIGNOFF` on the promotion candidate CSV.

### 2. Negative-universe decision (separate; required before MCC / full metrics)
Define and document a defensible experimental non-essential set for MOPS-pyruvate
(or explicitly refuse full metrics and report positive-label overlap only).
Absence-from-list is **not** an automatic negative label.

---

## Derived outputs created (this run)

1. `project_management/audit/LEE2015_MOPS_PYRUVATE_HUMAN_REVIEW_PACKET.md` (this file)
2. `data/processed/literature/gene_level/lee2015_mops_pyruvate_PROMOTION_CANDIDATE.csv`
   — `review_status` remains **NEEDS_REVIEW**; added `human_review_decision=PENDING_HUMAN_SIGNOFF`
3. `results/comparison/lee2015_mops_pyruvate_coverage_audit.csv`
4. `results/comparison/lee2015_mops_pyruvate_labels_absent_from_model.csv`

Canonical `literature_evidence.csv` / READY_ONLY files were **not** modified.

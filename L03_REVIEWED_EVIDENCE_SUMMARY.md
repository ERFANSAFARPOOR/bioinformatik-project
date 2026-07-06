# L03_REVIEWED_EVIDENCE_SUMMARY.md

**Date:** 2026-07-07 · **Branch:** `claude/revival-audit` · **Env:** `reccobra39`
**Purpose:** split the L-03 DRAFT gene-level evidence into a **READY_ONLY** set
and a **NEEDS_REVIEW** set as **derived** files, with full integrity reporting.
This is **not** a promotion to the canonical evidence table — it is a review
export. **No metrics computed. Canonical `data/processed/literature_evidence.csv`
untouched.**

## Source and outputs
- Source: `data/processed/literature_evidence_gene_level_DRAFT.csv` (5,148 rows).
- Derived (this cycle):
  - `data/processed/literature_evidence_gene_level_READY_ONLY.csv` — rows with
    `review_status == READY` (**2,607**).
  - `data/processed/literature_evidence_gene_level_NEEDS_REVIEW.csv` — rows with
    `review_status != READY` (**2,541**, all `NEEDS_REVIEW`).
- 2,607 + 2,541 = 5,148 (complete, no rows lost or duplicated).

All 30 columns (incl. source_file/sheet/row locators, thresholds, conditions,
media, mapping notes) are preserved in both outputs.

## READY_ONLY (2,607 rows)
| Dimension | Breakdown |
|---|---|
| by study | lee2015 **351**, turner2015 **586**, belanger2022 **1,670** |
| by phenotype_class | generally-essential **1,303**, condition-specific-essential **457**, host-condition-fitness **682**, reduced-fitness **165** |
| review_status | READY 2,607 |

By condition:
- **lee2015** — three primary media (LB + MOPS-pyruvate + CF sputum) general
  essential: 351.
- **turner2015** — initial transposon library (general essential) 336; CF sputum
  vs MOPS-succinate 104; …(biosynthetic) 52; CF sputum vs SCFM2 9; CF sputum
  (MOPS-sputum) condition-specific 46; murine chronic wound 39.
- **belanger2022** — rich-medium T0 (general essential) 616; RPMI-1640 246;
  RPMI + human serum 165; murine abscess 346; human skin organoid 297.

Integrity: **0 duplicates**, **0 missing required fields**, **0 non-PA mapped
IDs**, **0 PA14 leakage**, **0 varadarajan/zhu/poulsen/basta rows**. Six
phenotype classes kept distinct (core-essential and
growth-arrest-survival-determinant intentionally absent — their sources
Poulsen/Basta are orthology-blocked and not parsed).

## NEEDS_REVIEW (2,541 rows)
| Dimension | Breakdown |
|---|---|
| by study | lee2015 **2,541** (only) |
| by phenotype_class | condition-specific-essential 2,541 |
| by condition | BHI (rich) 470, serum agar 441, MOPS-pyruvate (minimal) 437, LB (rich) 423, 0.1× LB (dilute) 392, CF sputum (agar) 378 |

All NEEDS_REVIEW rows are **Lee 2015 per-medium condition-specific** calls.
**Why they stay NEEDS_REVIEW:** the emission threshold maps Lee's SI "pools"
consensus rule onto the supplement's `X sum (of 6/3/4)` **assay** columns, but the
exact pool↔assay correspondence is not stated verbatim. See
`LEE2015_PER_MEDIUM_REVIEW.md`. Integrity: 0 duplicates, 0 missing fields, 0
non-PA IDs, 0 PA14 leakage, no forbidden studies.

## Notes
- Both files are **DRAFT/review exports**, not validated labels. Do **not** feed
  either to any metric (B-SCI-01) until per-study labels are validated, media
  reconstructed (C-01b), and per-condition predictions exist (S-01).
- READY_ONLY is the natural candidate for the *first* PAO1/MPAO1 validation once
  media + predictions exist; NEEDS_REVIEW is held back pending the Lee ambiguity.

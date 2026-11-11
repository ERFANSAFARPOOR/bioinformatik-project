# Notebook Creation Guide

## Current status (reconciled 2026-11-11)

Teaching notebooks `01` / `02` / `03` are **archived** at
`archive/teaching_notebooks/` (legacy / teaching only). Do not rebuild research
on top of them. Notebook `03` metrics use simulated labels and are scientifically
forbidden (`BLOCKERS.md` B-SCI-01).

## Research notebooks (current)

| Notebook | Purpose |
|---|---|
| `04_media_reconstruction.ipynb` | Document and apply cited media from `src.medium` |
| `05_condition_essentiality.ipynb` | Per-medium gene-deletion predictions (no validation metrics) |
| `06_pao1_validation.ipynb` | Planned notebook; not present. The first binary evaluation already exists as a script and report (below). |

MOPS-pyruvate binary evaluation was executed on the D-21 frozen universe:
1025 genes (214 experimental positives and 811 negatives), with TP=116, FN=98,
TN=764 and FP=47. Labels are the Varadarajan2020 reanalysis of Lee2015, not an
independent screen. FP/FN interpretation and human sign-off remain pending;
this is not a claim of completed model validation. Other conditions retain
their own label, medium and mapping gates.

Use `scripts/validation/run_v01_mops_pyruvate_binary_validation.py` and
`project_management/audit/v01_mops_pyruvate/V01_BINARY_VALIDATION_REPORT.md`;
see the root `VALIDATION_LABEL_MEDIA_OVERLAP.md` for the current scope.

Heavy logic stays in `src/`; notebooks call into it. See
`project_management/planning/TEAM_WORK_MODEL_AND_NEXT_STEPS.md`.

## Historical teaching outline

The original teaching outline for `01`/`02`/`03` is preserved only in the
archived notebooks and `docs/teaching/teaching_notes.md`. Those paths are not the
research entry point.

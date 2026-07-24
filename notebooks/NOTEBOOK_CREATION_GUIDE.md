# Notebook Creation Guide

## Status (2026-07-24)

Teaching notebooks `01` / `02` / `03` are **archived** at
`archive/teaching_notebooks/` (legacy / teaching only). Do not rebuild research
on top of them. Notebook `03` metrics use simulated labels and are scientifically
forbidden (`BLOCKERS.md` B-SCI-01).

## Research notebooks (current)

| Notebook | Purpose |
|---|---|
| `04_media_reconstruction.ipynb` | Document and apply cited media from `src.medium` |
| `05_condition_essentiality.ipynb` | Per-medium gene-deletion predictions (no validation metrics) |
| `06_pao1_validation.ipynb` | **Gated** — only after READY_ONLY labels + media + predictions |

Heavy logic stays in `src/`; notebooks call into it. See
`docs/TEAM_WORK_MODEL_AND_NEXT_STEPS.md`.

## Historical teaching outline

The original teaching outline for `01`/`02`/`03` is preserved only in the
archived notebooks and `docs/teaching_notes.md`. Those paths are not the
research entry point.

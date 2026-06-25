---
name: project-audit
description: Read-only audit of the P. aeruginosa modeling repo (model, env, notebooks, data, git). Trigger when asked to audit, re-audit, inventory, or assess repository/model state, or when resuming after inactivity.
---

# Project audit (read-only)

## Trigger
Use when the user asks to audit / re-audit / inventory / health-check the
repository or model, verify reproducibility, or take stock after a gap.

## Inputs
- `models/paeruginosa_MODEL1507180020.xml` (raw, read-only)
- `notebooks/`, `src/`, `data/`, `results/`, `conditian/` (PDFs), env files
- Git history/branches/remotes; conda env `reccobra39`

## Ordered workflow
1. Confirm active env is `reccobra39`; confirm `cobra` + `pandas` import.
2. Load the model **read-only**; record id/name/strain, counts, objective,
   compartments, exchanges, default medium, feasibility (growth), QC
   (no-gene reactions, dead ends, missing formulas/charges, duplicates,
   blocked reactions with `processes=1`).
3. Inventory files; flag stale/generated/junk (e.g. `{data`, `__pycache__`),
   hard-coded paths, duplicated notebooks, kernelspec mismatches.
4. Inspect notebooks for placeholder/simulated data and uncited values.
5. Identify PDFs (metadata/DOI) → confirm `papers/manifest.csv`.
6. Capture env: `sys.executable`, versions, kernels, missing packages.
7. Inspect git branches/remotes/status (observe only).
8. Update `PROJECT_AUDIT.md`, `TODO.md`, `BLOCKERS.md`, `DECISIONS.md`,
   `DATA_PROVENANCE.md`, `environment-audit.txt`.

## Validation requirements
- Every recorded number is reproduced by a runnable command/script.
- Model file SHA-256 unchanged before/after (proves read-only).
- No completion percentage invented; unknowns → `PENDING_*` + blocker.

## Prohibited behavior
- Editing the raw model/PDF/raw data in place.
- Pushing, changing remotes, rewriting history, destructive deletes.
- Inferring completion from filenames; fabricating any value.

## Expected outputs
Updated audit/report files above + a machine-readable
`model_audit_snapshot.json`. No raw inputs modified.

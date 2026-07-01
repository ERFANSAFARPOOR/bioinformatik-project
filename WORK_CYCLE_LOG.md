# WORK CYCLE LOG — Revival / PAO1-focus organization cycle

Append-only per-cycle safety and provenance log. **Part A snapshot must be
written before any file reorganization.**

---

## Cycle 2 — 2026-07-01 · PAO1-focused repository organization

### A.1 Pre-work safety snapshot

| Field | Value |
|---|---|
| Date/time (local) | 2026-07-01 |
| Branch | `claude/revival-audit` (confirmed via `git branch --show-current`) |
| Git status (start) | clean except **untracked** `conditian/` (6 PDFs) |
| Active Python | `C:\Users\pro\anaconda3\envs\reccobra39\python.exe` |
| Python version | 3.9.23 |
| Conda env | `reccobra39` |

### A.2 Package versions (verified importable in reccobra39)

| Package | Version |
|---|---|
| cobra | 0.29.1 |
| pandas | 2.3.2 |
| matplotlib | 3.9.4 |
| matplotlib_venn | 1.1.2 |
| openpyxl | 3.1.5 |
| scipy | 1.13.1 |

All six required imports (`cobra, pandas, matplotlib, matplotlib_venn, openpyxl,
scipy`) succeeded.

### A.3 Model verification (read-only load)

| Field | Value |
|---|---|
| File | `models/paeruginosa_MODEL1507180020.xml` |
| SHA-256 | `0868a5ebb41ebb4967c3c182e686eca7552af9255cba5a6d130cf114d1212ead` |
| Matches CLAUDE.md recorded hash | YES |
| Model ID | `MODEL1507180020` (iMO1056, *P. aeruginosa* PAO1) |
| Reactions / Metabolites / Genes | 1110 / 879 / 1054 |
| Objective | `PA_Biomass6_DM` (max) |
| WT growth (default medium) | 1.0479285528184004 /h (feasible) |

All values match the established project identity. No unexpected drift.

### A.4 Top-level directory tree (start of cycle)

```
.claude/  .git/  .venv/ (git-ignored)
conditian/                         (untracked — 6 legacy raw PDFs)
data/  docs/  models/  notebooks/  papers/  results/  scripts/(empty)  src/
{data                              (EMPTY brace-expansion artifact — R-01)
Governance/docs (root .md/.txt/.py/.json/.html):
  BLOCKERS.md CLAUDE.md DATA_PROVENANCE.md DECISIONS.md DIRECTORY_STRUCTURE.txt
  FILE_LIST.txt INDEX.md PACKAGING_GUIDE.md PROJECT_AUDIT.md PROJECT_SUMMARY.md
  PUBLICATION_PLAN.md QUICK_START.md README.md REPOSITORY_MIGRATION_PLAN.md
  STUDENT_GUIDE.md SUMMARY.md TODO.md VALIDATION_READINESS.md
  environment-audit.txt environment-explicit.txt environment-reccobra39.yml
  environment.yml requirements-current.txt
  analyze_reproduction.py audit_model.py build_gene_mapping.py cmp_ess.py
  generate_clean_predictions.py generate_phasea_data.py identify_pdfs.py
  show_audit.py
  index.html model_audit_clean.json model_audit_output.json
  model_audit_snapshot.json
```

### A.5 Untracked files/folders (start)

- `conditian/corrieR.pdf` (belanger2022)
- `conditian/davidW.pdf` (basta2017)
- `conditian/juhas2015.pdf` (juhas2015)
- `conditian/keith H.pdf` (turner2015)
- `conditian/polsun2019.pdf` (poulsen2019)
- `conditian/samuelA.pdf` (lee2015)
- `{data` (empty artifact tree — verified 0 files) — to be deleted (R-01)

Note: `model_audit_clean.json`, `model_audit_output.json` at root are untracked
per earlier snapshot but appear in the working tree; they are audit outputs.
(Only `model_audit_snapshot.json` is tracked.)

### A.6 Files expected to change / be created this cycle

**New reports/docs (create):** `PAO1_PROJECT_SCOPE.md`,
`PAO1_PAPER_RELEVANCE_AUDIT.md`, `docs/PAO1_LITERATURE_SEARCH_STRATEGY.md`,
`PAO1_VALIDATION_DATA_INVENTORY.md`, `ORTHOLOGY_STATUS_REPORT.md`,
`REPRODUCTION_AFTER_MIGRATION.md`, `NEXT_STAGE_HANDOFF_REPORT.md`,
`tests/` (pytest suite).

**Copies (raw preserved):** 6 PDFs `conditian/*` → `papers/*` (normalized names);
model → `models/raw/`.

**Moves (git mv):** audit scripts (root `*.py`) → `scripts/`; redundant
educational docs → `docs/` or `archive/` (after correcting model-identity claims).

**New empty structure dirs:** `models/processed/`, `data/raw/literature/`,
`results/tables/`, `results/figures/`, `manuscript/`, `archive/`, `tests/`.

**Updated:** `papers/manifest.csv`, `README.md`, `PROJECT_AUDIT.md`,
`DATA_PROVENANCE.md`, `VALIDATION_READINESS.md`, `TODO.md`, `BLOCKERS.md`,
`DECISIONS.md`, `PUBLICATION_PLAN.md`, `REPOSITORY_MIGRATION_PLAN.md`,
`data/processed/literature_evidence.csv`, `data/processed/gene_mapping*`.

**Delete (verified junk only):** `{data` brace-expansion artifact;
`__pycache__` if present. `conditian/` is **NOT** deleted this cycle.

### A.7 Safety confirmation

- No push / force-push / remote change / history rewrite will occur.
- Raw model, PDFs, and raw data will not be edited in place (copies only).
- No global Python installs.
- Unknowns recorded as `PENDING_*` + blocker; nothing fabricated.

### A.8 Cycle completion note

Cycle 2 completed with 6 local commits (`627eedcf`, `a8a86e85`, `db49b557`,
`813d5f05`, `f6431dc6`, + this handoff commit) on `claude/revival-audit`. No push.
Final git status: clean except untracked `conditian/` (preserved). Migration
verified behavior-preserving (8 pytest pass; WT growth 1.0479285528). Strain
re-audit corrected the corpus (Lee=MPAO1, Belanger=PAO1, Turner mixed). No new
supplements/full text downloadable (B-NET); no validation metrics computed.
See `NEXT_STAGE_HANDOFF_REPORT.md`.

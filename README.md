# Genome-scale metabolic modeling & gene essentiality in *Pseudomonas aeruginosa*

Constraint-based analysis of the *P. aeruginosa* **PAO1** genome-scale model
**iMO1056**, with the goal of comparing model-predicted gene essentiality against
published experimental (Tn-seq) datasets — condition-matched and strain-mapped.

> **Status: under revival / not yet validated.** This repository is being
> recovered after a period of inactivity. A read-only audit has been completed
> (`PROJECT_AUDIT.md`). **No experimental validation results exist yet** — the
> existing experimental-comparison notebook uses *simulated* data and its metrics
> must not be cited (see `BLOCKERS.md` B-SCI-01). Work is tracked in `TODO.md`.

## Model

| | |
|---|---|
| Model | **iMO1056** — Oberhardt et al. 2008, *J Bacteriol* |
| Organism / strain | *Pseudomonas aeruginosa* **PAO1** (gene IDs `PAxxxx`) |
| Source | BioModels `MODEL1507180020` |
| File | `models/paeruginosa_MODEL1507180020.xml` (SBML L3 V1 + fbc) |
| Size | 1110 reactions · 879 metabolites · 1054 genes · compartments `c`,`e` |
| Objective | `PA_Biomass6_DM` (maximize); default growth ≈ **1.048 /h** (feasible) |

The raw model is **read-only** and never edited in place.

## Repository layout

```
models/        paeruginosa_MODEL1507180020.xml  (raw, read-only, canonical load path)
  raw/         byte-identical archived copy of the raw SBML
  processed/   derived model artifacts (none yet)
papers/        canonical PDFs (juhas2015, turner2015, lee2015, poulsen2019,
               basta2017, belanger2022) + manifest.csv
conditian/     legacy raw PDF folder (untracked; left untouched, superseded by papers/)
notebooks/     01_basic_fba · 02_gene_essentiality · 03_experimental_comparison
  reproduced/  re-executed copies + reproduction report
src/           model_io · fba_utils · medium · gene_essentiality · mapping
scripts/       audit/ · mapping/ · generation scripts (relocated from root)
tests/         pytest regressions (model identity, WT growth, 166 essential)
data/
  raw/literature/  downloaded supplements (per study; none yet — blocked)
  raw/ortholog/    NCBI RefSeq feature tables (PAO1, PA14)
  processed/       gene_mapping.csv · literature_evidence.csv ·
                   predicted_essentiality_default_medium.csv (evidence/prediction)
results/       essentiality/ (real prediction) · tables/ · figures/ · comparison/
docs/          teaching/dev notes · PAO1_LITERATURE_SEARCH_STRATEGY.md · index.html
manuscript/    (empty; drafted at P-01)
archive/       superseded legacy docs
```
Governance/audit (root): `PROJECT_AUDIT.md`, `TODO.md`, `BLOCKERS.md`,
`DECISIONS.md`, `DATA_PROVENANCE.md`, `PUBLICATION_PLAN.md`,
`REPOSITORY_MIGRATION_PLAN.md`, `WORK_CYCLE_LOG.md`, `PAO1_PROJECT_SCOPE.md`,
`PAO1_PAPER_RELEVANCE_AUDIT.md`, `PAO1_VALIDATION_DATA_INVENTORY.md`,
`ORTHOLOGY_STATUS_REPORT.md`, `VALIDATION_READINESS.md`, `CLAUDE.md`.

## Environment

Canonical environment is the conda env **`reccobra39`** (Python 3.9.23,
COBRApy 0.29.1, pandas 2.3.2, GLPK). See `environment-audit.txt` and
`requirements-current.txt`.

The plotting/IO packages the notebooks need are already installed env-scoped
(matplotlib 3.9.4, matplotlib-venn 1.1.2, openpyxl 3.1.5, scipy 1.13.1; E-01),
and `pytest` for the test suite. The notebooks were authored under an in-repo
`.venv` (Python 3.12.6) but **reproduce under `reccobra39`** (nb02 exactly);
locking `environment.yml`/`requirements-lock.txt` is still open (E-03).

Quick check + tests:
```bash
conda run -n reccobra39 python -c "import cobra, pandas; print(cobra.__version__, pandas.__version__)"
conda run -n reccobra39 python -m pytest tests/ -q          # 8 passed
```

## Notebooks

1. `01_basic_fba.ipynb` — load model, run FBA, inspect fluxes.
2. `02_gene_essentiality.ipynb` — single-gene deletion → essential genes
   (produced the real `results/essentiality/gene_essentiality_default_medium.csv`:
   166 essential of 1054 at a 1% growth-ratio threshold, default medium).
3. `03_experimental_comparison.ipynb` — **demonstration only**: currently compares
   predictions to *randomly simulated* labels. Will be replaced with real,
   strain-mapped, condition-matched experimental data (`TODO.md` V-01).

## Literature (strain re-audited 2026-07-01)

Six studies in `papers/` (see `papers/manifest.csv` and
`PAO1_PAPER_RELEVANCE_AUDIT.md`), classified by direct-evidence strain:

| Study | Strain | Tier | Phenotype |
|---|---|---|---|
| Belanger 2022 | **PAO1** | 1 | host-condition fitness |
| Lee 2015 | **MPAO1** (PAO1-derived) | 2 | general + condition-specific essential |
| Turner 2015 | **PAO1 + PA14** (mixed) | 3 | condition-specific essential (CF sputum) |
| Poulsen 2019 | multi-strain (incl. PAO1) | 3/5 | core essential |
| Basta 2017 | **PA14** | 4 | growth-arrest survival determinant |
| Juhas 2015 | review | 6 | (background) |

**Correction from the earlier audit:** the corpus is *not* mostly PA14 — Lee is
**MPAO1**, Belanger is **PAO1**, and Turner has usable **PAO1** rows. Those join
to the model **by identity** (no orthology). Validated PAO1↔PA14 orthology
(`BLOCKERS.md` B-MAP-01) is required only for **Basta 2017** and the non-PAO1
strains of **Poulsen 2019**. Gene-level labels are not yet in the repo — all
paper supplements are download-blocked here (`BLOCKERS.md` B-NET / B-LIT-01).

## Scientific-integrity rules

No fabricated values; unknowns are `PENDING_*` with a blocker. Raw model/PDF/data
are never edited in place. PAO1 and PA14 IDs are not interchangeable. The six
experimental phenotype classes are kept distinct. No precision/recall/F1/MCC is
reported until labels, mappings, and condition media are validated. Full rules in
`CLAUDE.md`.

## Reproducing the current real result
```bash
conda run -n reccobra39 jupyter nbconvert --to notebook --execute \
  notebooks/02_gene_essentiality.ipynb   # env packages already installed (E-01)
```

## License & citation
Model redistribution terms (BioModels) to be confirmed before public release
(`DATA_PROVENANCE.md`). A `LICENSE` and `CITATION.cff` will be added at
publication readiness (`TODO.md` PR-02).

## Current blockers & next steps

**Open P0 blockers:** B-SCI-01 (only simulated comparison exists — invalid),
B-LIT-01 / B-NET (paper supplements + OA full text not downloadable here),
B-COND-01 (experimental media not reconstructed), B-MAP-01 (validated PA14
orthology, for Basta/Poulsen only). See `BLOCKERS.md`.

**Next steps (see `TODO.md`, `NEXT_STAGE_HANDOFF_REPORT.md`):**
1. Human-assisted download of PAO1/MPAO1 supplements — **DONE** (Lee, Turner,
   Belanger, Varadarajan, Poulsen, Basta all present). Review the L-03 DRAFT and
   obtain validated PA14→PAO1 orthology for Basta/Poulsen.
2. Parse to gene-level `literature_evidence.csv` rows (six classes distinct).
3. Reconstruct per-condition media (LB, SCFM/MOPS, host) as exchange bounds.
4. Per-condition single-gene deletion, then — only then — metrics.

## Provenance
Model and PDF provenance: `DATA_PROVENANCE.md`. Audit method and evidence:
`PROJECT_AUDIT.md` (read-only; scripts under `scripts/audit/`:
`audit_model.py`, `identify_pdfs.py`, `extract_strain_evidence.py`,
`pubmed_search.py`).

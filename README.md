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

## Repository layout (current)

```
models/        paeruginosa_MODEL1507180020.xml  (raw, read-only)
conditian/     6 literature PDFs  (→ migrating to papers/; see papers/manifest.csv)
notebooks/     01_basic_fba · 02_gene_essentiality · 03_experimental_comparison
src/           model_io · fba_utils · medium · gene_essentiality · mapping
data/processed/  gene_mapping.csv · literature_evidence.csv  (evidence tables)
results/essentiality/  gene_essentiality_default_medium.csv  (real prediction output)
docs/          teaching/dev notes
```
Governance/audit: `PROJECT_AUDIT.md`, `TODO.md`, `BLOCKERS.md`, `DECISIONS.md`,
`DATA_PROVENANCE.md`, `PUBLICATION_PLAN.md`, `REPOSITORY_MIGRATION_PLAN.md`,
`CLAUDE.md`. Target structure in the migration plan.

## Environment

Canonical environment is the conda env **`reccobra39`** (Python 3.9.23,
COBRApy 0.29.1, pandas 2.3.2, GLPK). See `environment-audit.txt` and
`requirements-current.txt`.

```bash
conda activate reccobra39
# one-time (local only): add packages the notebooks need but reccobra39 lacks
conda install -n reccobra39 matplotlib scipy networkx openpyxl
pip install matplotlib-venn      # into reccobra39
```

> The committed notebooks were authored under an in-repo `.venv` (Python 3.12.6).
> Reproducing them under `reccobra39` and locking the environment is an open task
> (`BLOCKERS.md` B-ENV-01). Do not assume the locked env until that passes.

Quick check:
```bash
conda run -n reccobra39 python -c "import cobra, pandas; print(cobra.__version__, pandas.__version__)"
```

## Notebooks

1. `01_basic_fba.ipynb` — load model, run FBA, inspect fluxes.
2. `02_gene_essentiality.ipynb` — single-gene deletion → essential genes
   (produced the real `results/essentiality/gene_essentiality_default_medium.csv`:
   166 essential of 1054 at a 1% growth-ratio threshold, default medium).
3. `03_experimental_comparison.ipynb` — **demonstration only**: currently compares
   predictions to *randomly simulated* labels. Will be replaced with real,
   strain-mapped, condition-matched experimental data (`TODO.md` V-01).

## Literature

Six Tn-seq / essentiality studies (in `conditian/`, identified in
`papers/manifest.csv`): Juhas 2015, Turner 2015 (CF sputum, PA14),
Lee 2015 (general & condition-specific, PA14), Poulsen 2019 (core essential),
Basta (growth-arrest fitness), Belanger (host-condition fitness). The model is
**PAO1** while most datasets are **PA14** — cross-strain orthology mapping is
required and not yet done (`BLOCKERS.md` B-MAP-01).

## Scientific-integrity rules

No fabricated values; unknowns are `PENDING_*` with a blocker. Raw model/PDF/data
are never edited in place. PAO1 and PA14 IDs are not interchangeable. The six
experimental phenotype classes are kept distinct. No precision/recall/F1/MCC is
reported until labels, mappings, and condition media are validated. Full rules in
`CLAUDE.md`.

## Reproducing the current real result
```bash
conda run -n reccobra39 jupyter nbconvert --to notebook --execute \
  notebooks/02_gene_essentiality.ipynb   # after env packages are installed
```

## License & citation
Model redistribution terms (BioModels) to be confirmed before public release
(`DATA_PROVENANCE.md`). A `LICENSE` and `CITATION.cff` will be added at
publication readiness (`TODO.md` PR-02).

## Provenance
Model and PDF provenance: `DATA_PROVENANCE.md`. Audit method and evidence:
`PROJECT_AUDIT.md` (read-only; scripts `audit_model.py`, `identify_pdfs.py`,
`generate_phasea_data.py`).

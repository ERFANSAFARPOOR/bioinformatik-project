# CLAUDE.md — project facts & rules (stable)

Genome-scale metabolic modeling & gene-essentiality analysis of
*Pseudomonas aeruginosa*. Keep this file short and factual. Procedures live in
local agent skills (`.cursor/skills/` or `.claude/skills/`, both gitignored).
Working state lives in `TODO.md` / `BLOCKERS.md` / `DECISIONS.md`.

## Identity
- **Model:** iMO1056 (Oberhardt et al. 2008), *P. aeruginosa* **PAO1**,
  BioModels `MODEL1507180020`, file `models/paeruginosa_MODEL1507180020.xml`
  (SHA-256 `0868a5eb…1212ead`). 1110 reactions, 879 metabolites, 1054 genes.
  Objective `PA_Biomass6_DM` (max); default growth ≈ 1.0479 /h (feasible).
- **Environment:** `reccobra39` (conda, Python 3.9.23, cobra 0.29.1, pandas 2.3.2,
  GLPK). Activate before running anything. (See `environment-audit.txt`.)
- **Literature:** 6 PDFs in `conditian/` (→ to migrate to `papers/`); see
  `papers/manifest.csv`. Strains differ: model=PAO1, most studies=PA14.

## Hard rules (do not violate)
1. **Never fabricate** values, gene lists, fluxes, growth rates, citations,
   statistics, or metadata. Unknown → `PENDING_*` + a blocker. Label hypotheticals.
2. **Read-only raw files:** never edit the SBML model, the PDFs, or raw
   literature data in place. Derived files go to `models/processed/`,
   `data/processed/`.
3. **Strains are not interchangeable.** PAO1 (`PAxxxx`) ≠ PA14 (`PA14_xxxxx`).
   Map explicitly with a sourced ortholog table; keep one-to-many/missing.
4. **Six phenotype classes stay distinct:** generally-essential, core-essential,
   condition-specific-essential, reduced-fitness, growth-arrest-survival,
   host-condition-fitness. No collapse to a single binary label.
5. **No metrics without validation.** Compute precision/recall/F1/MCC only after
   experimental labels + gene mappings + condition media are validated. The
   current nb03 comparison uses simulated data — do not report it.
6. **Every experimental value carries provenance:** citation, strain, condition,
   medium, carbon source, electron acceptor, method, essentiality definition,
   threshold, and page/table/figure/supplement locator.

## Git / safety
- Prefer feature branches; never force-push, rewrite history, or run
  `git reset --hard` / `git clean -fdx`. Do not push directly to `main`/`master`.
- Local commits only when requested; small, coherent, validated. Never commit
  secrets, `.env`, large archives (`ipynb.rar`), caches, checkpoints, or `.venv`.
- No global Python installs; local env changes into reccobra39 only.
- **Local-only AI tool config:** `.claude/` and `.cursor/` are gitignored and
  must never be committed. Cursor-native safety hooks (when present) live under
  `.cursor/hooks/` on the local machine only.

## Where things are
- Reports: `PROJECT_AUDIT.md`, `TODO.md`, `BLOCKERS.md`, `DECISIONS.md`,
  `DATA_PROVENANCE.md`, `PUBLICATION_PLAN.md`, `REPOSITORY_MIGRATION_PLAN.md`.
- Code: `src/` (loader, FBA, essentiality, medium, mapping). Audit scripts at root.
- Data: `data/processed/{gene_mapping,literature_evidence}.csv`.
- Results: `results/essentiality/gene_essentiality_default_medium.csv` (real;
  `gene_id` needs cleaning).
- Tests: `C:/Users/pro/anaconda3/envs/reccobra39/python.exe -m pytest tests/ -q`

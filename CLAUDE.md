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
  GLPK). Use this environment for scientific code. See `environment-reccobra39.yml`.
- **Literature:** 6 canonical PDFs in `papers/`; `conditian/` is preserved legacy.
  Lee=MPAO1 (PAO1-derived), Belanger=PAO1, Turner=PAO1+PA14,
  Poulsen=nine strains including PA14 but **excluding PAO1**, Basta=PA14,
  Juhas=review. `papers/manifest.csv` records the sources.

## Current scientific state (reconciled 2026-11-11)
- Media and predictions exist for MOPS-pyruvate, MOPS-succinate and `LB_approx`.
  These are computational reconstructions with documented uptake assumptions
  and unmodeled components; `DEFINED` does not mean full experimental equivalence.
- D-21 MOPS-pyruvate binary comparison exists: 1025 genes, TP116/FN98/TN764/FP47.
  Labels are the Varadarajan2020 remap of Lee2015, **not independent replication**.
  Both classes come from D-21; D-20 Lee-original positives stay separate.
- Metrics, error audit and evidence exist; human interpretation/sign-off pending.
  Do not claim the model is fully validated or change it to improve metrics.
- Turner PA14 orthology is APPROVED_LIMITED for controlled draft mapping; PGD
  export is present. This does not authorize PA14/Poulsen validation metrics.
- Current cell status: `VALIDATION_LABEL_MEDIA_OVERLAP.md`; report:
  `project_management/audit/v01_mops_pyruvate/V01_BINARY_VALIDATION_REPORT.md`.
  Older dated logs are historical snapshots, not current global prohibitions.

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
   host-condition-fitness. No pooling across these classes into one binary label;
   within-condition binary comparisons follow their reviewed label policy.
5. **No metrics without validation.** Compute precision/recall/F1/MCC only after
   experimental labels + gene mappings + condition media are validated. The
   archived teaching nb03 uses simulated data — do not cite its metrics as
   experimental evidence. The existing D-21/V-01 comparison is separate.
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
- Working state: root `TODO.md`, `BLOCKERS.md`, `DECISIONS.md`,
  `DATA_PROVENANCE.md`. Audits, planning and publication docs live in
  `project_management/{audit,planning,publication}/`.
- Code: `src/`; audit/mapping/validation scripts under `scripts/`.
- Data: `data/processed/gene_mapping/gene_mapping.csv`, literature evidence in
  `data/processed/literature/`, D-21 gene labels in `literature/gene_level/`.
- Results: `results/essentiality/gene_essentiality_default_medium.csv` (real;
  legacy set-repr IDs); cleaned copy:
  `data/processed/essentiality/predicted_essentiality_default_medium.csv`.
- V-01 outputs: `data/processed/validation/v01_mops_pyruvate_*`.
- Tests: `C:/Users/pro/anaconda3/envs/reccobra39/python.exe -m pytest tests/ -q`

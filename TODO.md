# TODO — evidence-based, derived from the Phase A audit

Every task below is grounded in an observed fact from `PROJECT_AUDIT.md`.
No invented completion percentages. Fields per task:
**ID · Priority · Category · Task · Reason · Inputs · Expected output · Dependencies · Validation · Status · Blocker · Commit**

Priorities: **P0** blocks scientific validity/reproducibility · **P1** required for
manuscript & public repo · **P2** improves quality · **P3** optional.
Status: TODO / IN-PROGRESS / DONE / BLOCKED.

---

## A. Repository recovery

### R-01 · P1 · repo-recovery
- **Task:** Remove the stray `{data` junk directory tree (literal brace-expansion dirs).
- **Reason:** Created by a bash-style `mkdir` run in PowerShell; empty, confusing.
- **Inputs:** `{data/...` · **Output:** clean tree · **Deps:** none
- **Validation:** `git status` clean; dirs gone; no real data lost (confirmed empty).
- **Status:** TODO · **Blocker:** none · **Commit:** (pending Phase B)

### R-02 · P2 · repo-recovery
- **Task:** Clean `gene_id` column in `results/essentiality/gene_essentiality_default_medium.csv` (`{'PAxxxx'}` → `PAxxxx`); write cleaned copy, keep original.
- **Reason:** Set-repr blocks joins/mapping; integrity (don't edit raw in place).
- **Inputs:** the CSV · **Output:** `data/processed/predicted_essentiality_default_medium.csv`
- **Deps:** none · **Validation:** all 1054 ids match `^PA\d+$`; 166 essential preserved.
- **Status:** TODO · **Blocker:** none

### R-03 · P2 · repo-recovery
- **Task:** Reconcile/correct docs that claim model is "iPae1146"; state it is iMO1056/PAO1.
- **Reason:** `models/README.md` and summaries are inconsistent with the loaded model.
- **Inputs:** model_audit_snapshot.json · **Output:** corrected READMEs/summaries
- **Deps:** none · **Validation:** every model-identity claim matches the audit. · **Status:** TODO

### R-04 · P3 · repo-recovery
- **Task:** Decide fate of `ipynb.rar` if it reappears; keep out of git.
- **Reason:** Brief flags it as untracked archive; not found at audit time.
- **Inputs:** working tree · **Output:** `.gitignore` rule (added) + note · **Validation:** not tracked. · **Status:** TODO

---

## B. Environment reproducibility

### E-01 · P1 · environment
- **Task:** Install (locally, NOT global) into reccobra39: matplotlib, matplotlib-venn, scipy, networkx, openpyxl.
- **Reason:** reccobra39 lacks them; notebooks/plots and `.xlsx` reading fail.
- **Inputs:** reccobra39 · **Output:** updated local env · **Deps:** D-02
- **Validation:** `import matplotlib, matplotlib_venn, openpyxl` succeed in reccobra39.
- **Status:** TODO · **Blocker:** B-ENV-01

### E-02 · P1 · environment
- **Task:** Re-run all three notebooks under the **reccobra39** kernel; confirm numerical reproduction (WT growth 1.0479, 166 essential @1%).
- **Reason:** Notebooks were authored under .venv/3.12.6; must reproduce in canonical env.
- **Inputs:** notebooks, reccobra39 · **Output:** executed notebooks + reproduction note
- **Deps:** E-01 · **Validation:** outputs match audited numbers within solver tol.
- **Status:** BLOCKED · **Blocker:** B-ENV-01

### E-03 · P1 · environment
- **Task:** After E-02 passes, lock `environment.yml` + `requirements-lock.txt`; reconcile the 3 existing env specs.
- **Reason:** Reproducible public repo needs one authoritative, working env.
- **Deps:** E-02 · **Validation:** fresh env from lock file imports cobra+matplotlib and runs nb02. · **Status:** BLOCKED

### E-04 · P2 · environment
- **Task:** Register/clean Jupyter kernels; standardize notebooks to the reccobra39 kernel metadata.
- **Reason:** Three kernels (.venv, python3, reccobra39) cause ambiguity. · **Deps:** E-02 · **Status:** TODO

---

## C. Model validation (computational, model-only)

### M-01 · P2 · model-validation
- **Task:** Compute blocked reactions (`processes=1`) and characterize dead-end metabolites (217 found).
- **Reason:** Needed to interpret false-negative essentiality; FVA failed under MP in audit.
- **Inputs:** model · **Output:** `results/model_qc/blocked_reactions.csv`, `deadends.csv`
- **Deps:** none · **Validation:** counts stable across reruns; documented. · **Status:** TODO · **Blocker:** B-MODEL-01

### M-02 · P2 · model-validation
- **Task:** Objective-function & growth-threshold sensitivity of essentiality (thresholds 0/1/5/10%; biomass variant `DM_EC_PREGRO` vs `PA_Biomass6_DM`).
- **Reason:** Essential-vs-reduced-growth classification must be robust (D-09).
- **Inputs:** model · **Output:** sensitivity tables/figs · **Deps:** none
- **Validation:** essential-set size vs threshold curve; documented. · **Status:** TODO

### M-03 · P3 · model-validation
- **Task:** Back-fill missing metabolite formulas (565) from BiGG/MetaNetX where balance claims are needed.
- **Reason:** Mass-balance audit unreliable without formulas. · **Deps:** none · **Status:** TODO · **Blocker:** B-MODEL-02

---

## D. Literature extraction

### L-01 · P0 · literature
- **Task:** Download official supplementary datasets (Turner sd01–04, Lee sd01, Poulsen Broad fitness data; Basta/Belanger supp); record provenance + SHA-256.
- **Reason:** Gene-level experimental labels live only in supplements.
- **Inputs:** DOIs in `papers/manifest.csv` · **Output:** `data/raw/literature/<study>/...`
- **Deps:** network + human OK · **Validation:** files present, hashed, logged in DATA_PROVENANCE.
- **Status:** BLOCKED · **Blocker:** B-LIT-01

### L-02 · P1 · literature
- **Task:** Verify Basta & Belanger citation/DOI/year/strain against CrossRef/journal.
- **Reason:** Currently PENDING_VERIFY; cannot cite unverified.
- **Inputs:** PDFs · **Output:** updated `literature_evidence.csv`, `papers/manifest.csv`
- **Deps:** none · **Validation:** DOI resolves to matching title. · **Status:** TODO · **Blocker:** B-LIT-02

### L-03 · P0 · literature
- **Task:** Populate `data/processed/literature_evidence.csv` gene-level rows from supplements, keeping all 30 columns + 6 distinct phenotype classes; no merging.
- **Reason:** Core evidence table for validation; integrity rules §3,§5.
- **Inputs:** downloaded supplements · **Output:** complete evidence table
- **Deps:** L-01 · **Validation:** each row has citation+strain+condition+method+threshold+source locator; phenotype_type ∈ {6 classes}. · **Status:** BLOCKED · **Blocker:** B-LIT-01

---

## E. Gene mapping

### G-01 · P0 · gene-mapping
- **Task:** Obtain authoritative PAO1↔PA14 ortholog table (pseudomonas.com / study homolog columns) and join into `gene_mapping.csv`; retain one-to-many & missing.
- **Reason:** Model=PAO1, most experiments=PA14; IDs not interchangeable.
- **Inputs:** `gene_mapping.csv`, ortholog source · **Output:** populated PA14/gene_name/uniprot + confidence
- **Deps:** network + human OK · **Validation:** mapping coverage report; ambiguous cases listed. · **Status:** BLOCKED · **Blocker:** B-MAP-01

### G-02 · P1 · gene-mapping
- **Task:** Add gene names / UniProt for model PAO1 genes from a versioned source.
- **Reason:** Reporting + cross-referencing. · **Deps:** none(P) · **Validation:** sourced+dated. · **Status:** TODO

---

## F. Condition reconstruction

### C-01 · P0 · condition-reconstruction
- **Task:** Define in-model media for each experimental condition (CF sputum/SCFM, LB, defined minimal, C/O2-limited arrest, host-mimicking) with cited composition → exchange bounds.
- **Reason:** Comparing across mismatched media is invalid (B-COND-01).
- **Inputs:** papers, `src/medium.py` · **Output:** `data/processed/conditions/*.json` + loader
- **Deps:** L-03 · **Validation:** each condition cited; model feasible or documented infeasible. · **Status:** BLOCKED · **Blocker:** B-COND-01

---

## G. Simulation

### S-01 · P1 · simulation
- **Task:** Run single-gene-deletion per reconstructed condition; export per-condition predicted essential/reduced-growth sets.
- **Reason:** Basis for validation against the matching experimental class.
- **Inputs:** model, conditions · **Output:** `results/essentiality/<condition>.csv`
- **Deps:** C-01, E-02 · **Validation:** reproducible; threshold recorded. · **Status:** BLOCKED

### S-02 · P2 · simulation
- **Task:** Alternate-optima / solver-tolerance robustness (pFBA, multiple solvers if available).
- **Reason:** Guard essentiality calls against degeneracy. · **Deps:** S-01 · **Status:** TODO

---

## H. Statistical evaluation

### V-01 · P0 · statistical-evaluation
- **Task:** Replace the simulated-data comparison in nb03 with real labels; compute confusion matrix, precision, recall, specificity, F1, MCC per matched condition+phenotype class; report mapped/unmapped/absent-gene coverage.
- **Reason:** Current metrics are on random data (B-SCI-01) — invalid.
- **Inputs:** predictions (S-01/R-02), evidence (L-03), mapping (G-01) · **Output:** `results/comparison/metrics_<condition>.csv` + figs
- **Deps:** L-03, G-01, C-01, S-01 · **Validation:** labels+mappings validated FIRST; metrics only on validated joins. · **Status:** BLOCKED · **Blocker:** B-SCI-01

---

## I. Figures & tables

### F-01 · P1 · figures-tables
- **Task:** Publication-quality figures (essential-set sizes, threshold sensitivity, confusion/Venn on REAL data) and result tables.
- **Reason:** Manuscript needs defensible visuals (not the placeholder Venn).
- **Deps:** V-01 · **Validation:** every figure traceable to a script+data file. · **Status:** BLOCKED

---

## J. Manuscript

### P-01 · P1 · manuscript
- **Task:** Draft `manuscript/` (intro, methods incl. model id/strain/medium/threshold, results, limitations: PAO1↔PA14, media mismatch, FBA caveats).
- **Reason:** Target outcome #2. · **Deps:** V-01, F-01 · **Status:** BLOCKED

---

## K. Documentation

### D-01t · P1 · documentation
- **Task:** Rewrite root README as a professional research-repo README (done in Phase A draft); keep teaching docs under `docs/`.
- **Reason:** Public-repo readiness. · **Deps:** none · **Status:** IN-PROGRESS

### D-02t · P2 · documentation
- **Task:** Consolidate redundant root docs (SUMMARY/PROJECT_SUMMARY/INDEX/...) into `docs/`.
- **Reason:** Reduce clutter/inconsistency. · **Deps:** R-03 · **Status:** TODO

---

## L. Testing

### T-01 · P1 · testing
- **Task:** Add `tests/` (pytest): model loads; WT growth ≈1.0479; 166 essential @1%; medium reset/set; mapping extraction; gene_id cleaning.
- **Reason:** Lock scientific behavior before refactor (Phase B).
- **Inputs:** src, model · **Output:** `tests/test_*.py` · **Deps:** E-01
- **Validation:** `pytest` green under reccobra39. · **Status:** TODO

### T-02 · P2 · testing
- **Task:** Refactor reusable notebook logic into `src/` and have notebooks call `src/` (no behavior change).
- **Reason:** Brief Phase B. · **Deps:** T-01, E-02 · **Status:** TODO

---

## M. Publication readiness

### PR-01 · P1 · publication-readiness
- **Task:** Migrate to target structure (`models/raw|processed`, `data/raw|processed`, `papers/`, `notebooks/`, `src/`, `tests/`, `results/`, `manuscript/`, `docs/`, `archive/`) per `REPOSITORY_MIGRATION_PLAN.md`; keep originals via git.
- **Reason:** Target outcome #1. · **Deps:** E-02, T-01 · **Status:** TODO

### PR-02 · P1 · publication-readiness
- **Task:** Add LICENSE, CITATION.cff, verify model redistribution terms, scrub for secrets/large binaries; final audit.
- **Reason:** Public release. · **Deps:** PR-01 · **Status:** TODO · **Blocker:** model license (DATA_PROVENANCE §1)

### PR-03 · P2 · publication-readiness
- **Task:** Decide on `index.html` landing page (keep in `docs/` or drop). · **Deps:** PR-01 · **Status:** TODO

---

## TOP 10 (by priority and unblock-ability)
1. **R-01** remove `{data` junk (P1, no blocker)
2. **R-02** clean essentiality `gene_id` set-repr (P2, no blocker) — enables joins
3. **R-03** correct iMO1056/PAO1 model-identity claims in docs (P2)
4. **E-01** install matplotlib/venn/openpyxl into reccobra39 (P1)
5. **E-02** reproduce notebooks under reccobra39 (P1, after E-01)
6. **T-01** add pytest pinning WT growth + 166 essential (P1)
7. **M-01** compute blocked reactions / dead ends (P2)
8. **M-02** threshold & objective sensitivity of essentiality (P2)
9. **L-02** verify Basta & Belanger DOI/citation (P1)
10. **L-01 / G-01** download supplements + build PAO1↔PA14 mapping (P0, needs network + human OK)

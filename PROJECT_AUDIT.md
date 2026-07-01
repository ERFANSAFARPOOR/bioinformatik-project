# PROJECT AUDIT — *Pseudomonas aeruginosa* genome-scale metabolic modeling

**Audit type:** Read-only repository + model audit (Phase A)
**Date:** 2026-06-26
**Branch:** `claude/revival-audit`
**Auditor:** Claude Code (autonomous revival audit)
**Scope:** Inspection only. No raw model/data files modified. No git push. No remote changes.

> This document records *observed evidence*. It does not assign a completion
> percentage and does not infer completion from filenames. Open questions are
> tracked in `BLOCKERS.md`; resolved choices in `DECISIONS.md`; work items in
> `TODO.md`.

---

## 1. Executive summary

| Aspect | Finding |
|---|---|
| Project nature | An **educational COBRApy scaffold** ("metabolic-modeling-education") wrapped around one real *P. aeruginosa* model. It is **not yet** a validated scientific study. |
| Model | **iMO1056** (Oberhardt et al. 2008, *P. aeruginosa* **PAO1**), BioModels `MODEL1507180020`. Loads cleanly; grows (1.048 /h) on default medium. |
| Real results present | `results/essentiality/gene_essentiality_default_medium.csv` — **real** single-gene-deletion output (1054 genes, 166 essential at 1% threshold, default medium). |
| **Critical integrity issue** | `notebooks/03_experimental_comparison.ipynb` computes precision/recall/F1 against **simulated random data** (`random.sample`, seed 42), explicitly labeled "Using simulated data for demonstration." **No real model-vs-experiment validation exists.** |
| Literature | 6 relevant PDFs present (in `conditian/`), all identified. **No gene-level experimental data extracted yet**; supplementary `.xlsx` datasets not downloaded. |
| Environment | Mandated env `reccobra39` (Py 3.9, cobra 0.29.1) is confirmed active, but notebooks were authored under `.venv` (Py 3.12.6) and `reccobra39` is **missing matplotlib/venn/openpyxl** needed to run them. |
| Strain integrity | Model = PAO1. **CORRECTED 2026-07-01 (B-STRAIN-02):** the corpus is *not* mostly PA14 — Lee 2015=**MPAO1**, Belanger 2022=**PAO1**, Turner 2015=**PAO1+PA14** (usable PAO1 rows); only Basta 2017=PA14 and non-PAO1 Poulsen strains need orthology. See `PAO1_PAPER_RELEVANCE_AUDIT.md`. |

---

## 2. Repository inventory (tracked + untracked)

Top-level (excluding `.git`, `.venv`):

```
.gitignore  DIRECTORY_STRUCTURE.txt  FILE_LIST.txt  INDEX.md  PACKAGING_GUIDE.md
PROJECT_SUMMARY.md  QUICK_START.md  README.md  STUDENT_GUIDE.md  SUMMARY.md
environment.yml  environment-explicit.txt  environment-reccobra39.yml
requirements-current.txt  index.html
conditian/      (6 PDFs — the literature)
data/           experimental/ (README only), omics/ (README only)   <-- NO data files
docs/           student_guide.md, teaching_notes.md, figures/
models/         paeruginosa_MODEL1507180020.xml, README.md
notebooks/      01_basic_fba.ipynb, 02_gene_essentiality.ipynb, 03_experimental_comparison.ipynb
results/        comparison/ essentiality/ fba/ mapping/  (only essentiality has a CSV)
src/            __init__.py fba_utils.py gene_essentiality.py mapping.py medium.py model_io.py
{data           <-- STRAY junk directory (see §8)
```

### Source package `src/` (Python, clean)
| File | Purpose | Imports | Notes |
|---|---|---|---|
| `model_io.py` | load/save SBML/JSON/MAT/pickle | cobra | Read-only loader OK |
| `fba_utils.py` | biomass detection, FBA run, exchange fluxes | cobra | OK |
| `medium.py` | reset/set medium, condition dicts | cobra | Generic glucose/O2 defaults (−10/−20) |
| `gene_essentiality.py` | single_gene_deletion, threshold classification | cobra, pandas | Default threshold ratio = 0.01 (1%) |
| `mapping.py` | GPR extraction, complexity, gene↔reaction network | cobra, pandas | OK |
| `__init__.py` | package exports, `__version__="1.0.0"` | — | Imports only cobra/pandas (no matplotlib) → importable in reccobra39 |

`src/__pycache__/*.cpython-312.pyc` present → last imported under **Python 3.12**, not 3.9.

---

## 3. Model audit (`models/paeruginosa_MODEL1507180020.xml`)

Loaded read-only with COBRApy 0.29.1 under reccobra39. SHA-256 of file:
`0868a5ebb41ebb4967c3c182e686eca7552af9255cba5a6d130cf114d1212ead` (1,668,096 bytes).

| Property | Value |
|---|---|
| SBML model id | `MODEL1507180020` |
| Model name | `Oberhardt2008 - Genome-scale metabolic network of Pseudomonas aeruginosa (iMO1056)` |
| **Identity** | **iMO1056**, Oberhardt et al. 2008 (*J Bacteriol*). BioModels `MODEL1507180020`. |
| **Strain** | **PAO1** — evidence: gene IDs are `PAxxxx` PAO1 locus tags (PA0005, PA0006, …; PA14 would be `PA14_xxxxx`) **and** iMO1056 is the PAO1 reconstruction. |
| SBML level/version | L3 V1, fbc plugin present |
| Reactions | 1110 |
| Metabolites | 879 |
| Genes | 1054 |
| Compartments | `c` (cytosol), `e` (extracellular) |
| Objective | `PA_Biomass6_DM`, **maximize** |
| Biomass candidates | `PA_Biomass6_DM` (objective), `DM_EC_PREGRO` |
| Exchange reactions | 121 (`EX_*`) |
| Boundary reactions | 223 total (121 exchange + 102 demand `DM_*`, 0 sink) |
| Reactions without genes | 275 |
| Genes without reactions | 0 |
| Metabolites missing formula | 565 (≈64%) |
| Metabolites missing charge | 0 |
| Charge-imbalanced reactions | 0 |
| "Mass-imbalanced" reactions | 585 — **largely an artifact of the 565 missing formulas** (balance cannot be checked without formulas); do not over-interpret. |
| Dead-end metabolites (≤1 reaction) | 217 |
| Duplicate reaction/metabolite/gene IDs | 0 / 0 / 0 |
| Default medium | glucose `EX_glc_e` = 10, `EX_o2_e` = 1000, N2/NH4/Pi/SO4 + metals open (1000) |
| **Default growth** | **1.0479 /h, status = optimal** (feasible) |
| Solver | GLPK (`optlang.glpk_interface`) |
| Model annotation | `biomodels.db: MODEL1507180020` (no per-gene cross-refs in fbc) |
| Blocked reactions | **NOT computed** — `find_blocked_reactions` failed under Windows multiprocessing (needs `processes=1` / `__main__` guard). Tracked in TODO. |

Machine-readable snapshot: `model_audit_snapshot.json`.

---

## 4. Notebooks

| Notebook | Cells | Kernel (committed) | Status / Findings |
|---|---|---|---|
| `01_basic_fba.ipynb` | 26 | `.venv` (Py 3.12.6) | FBA tutorial. Large (100 KB) — contains saved outputs. Uses matplotlib. |
| `02_gene_essentiality.ipynb` | 15 | `.venv` (Py 3.12.6) | Single-gene deletion → produced the real `gene_essentiality_default_medium.csv`. |
| `03_experimental_comparison.ipynb` | 15 | `python3` | **Uses SIMULATED experimental labels** (`random.seed(42)`, `random.sample`). Metrics (precision/recall/F1/Venn) are **demonstration only, not scientific results**. Real experimental CSV path is commented out. |

> **Integrity note:** any figure/metric derived from notebook 03 in its current
> form must be treated as a placeholder and must NOT appear in a manuscript.

---

## 5. Data & results

- `data/experimental/` and `data/omics/` contain **only README templates** — no datasets.
- `results/essentiality/gene_essentiality_default_medium.csv` — **real** FBA deletion output (1055 lines incl. header; 166 rows `is_essential=True`; WT growth 1.0479 matches model audit).
  - **Data-quality issue:** `gene_id` stored as stringified Python `set`, e.g. `{'PA2339'}`, instead of plain `PA2339`. Needs cleaning before any join/mapping.
- Other `results/` subfolders contain only `.gitkeep` + `README.txt` (empty of outputs).
- `.gitignore` ignores `results/**/*.csv` and `data/**/*.csv`, so result/data CSVs are normally untracked (the essentiality CSV appears to have been force-added or predates the rule).

---

## 6. Literature (PDFs in `conditian/`)

All six identified from embedded PDF metadata/DOIs (see `papers/manifest.csv`,
`DATA_PROVENANCE.md`). `conditian` is a **misspelling of "condition"**; it holds
the papers, not condition definitions.

| File | Study | Strain | DOI | Phenotype class |
|---|---|---|---|---|
| `juhas2015.pdf` | Juhas et al. 2015, *P. aeruginosa* essentials update (Microbiology) | review | 10.1099/mic.0.000161 | generally essential (review) |
| `keith H.pdf` | Turner et al. 2015, essential genome in CF sputum (PNAS) | **PA14** | 10.1073/pnas.1419677112 | condition-specific essential |
| `samuelA.pdf` | Lee et al. 2015, general & condition-specific essential functions (PNAS) | **PA14** | 10.1073/pnas.1422186112 | general + condition-specific |
| `polsun2019.pdf` | Poulsen et al. 2019, core essential genome (PNAS) | **PA14 / multi-strain** | 10.1073/pnas.1900570116 | core essential |
| `davidW.pdf` | Basta et al., carbon/oxygen-limited growth-arrest fitness | PA14 (verify) | PENDING_VERIFY | survival-during-growth-arrest |
| `corrieR.pdf` | Belanger et al., "Surviving the host: … physiologically-relevant conditions" | PAO1 (verify) | PENDING_VERIFY | host-condition fitness |

Title/DOI for Basta & Belanger come from running-headers / PDF `/Author`
(Hancock lab) and require confirmation (BLOCKERS B-LIT-02). PNAS DOIs are
high-confidence (appear in PDF `/Title` and headers).

> **Six distinct phenotype classes** must be kept separate (rule §5 of brief):
> generally essential · core essential · condition-specific essential ·
> reduced-fitness · growth-arrest survival determinant · host-condition fitness.
> They are NOT a single binary "essential" label.

---

## 7. Environment (summary; full detail in `environment-audit.txt`)

- **Active/confirmed:** `reccobra39` — `...\envs\reccobra39\python.exe`, Python 3.9.23, cobra 0.29.1, pandas 2.3.2, numpy 2.0.2. ✅ COBRApy + pandas import OK.
- **Notebooks authored under:** `.venv` = Python **3.12.6** (in-repo, git-ignored). `__pycache__` is cpython-312.
- **Gap:** reccobra39 lacks `matplotlib`, `matplotlib_venn`, `scipy`, `networkx`, `seaborn`, `openpyxl` → cannot run the notebooks/plots or read `.xlsx` supplements as-is.
- Three Jupyter kernels registered: `python3` (reccobra39), `.venv` (3.12.6), `reccobra39`.

---

## 8. Stale / generated / problematic artifacts

| Item | Observation | Action (proposed) |
|---|---|---|
| `{data` directory | Junk from a **bash brace-expansion `mkdir` run in PowerShell** (literal dirs `{data`, `{experimental,omics},models,...}`). Empty. | Remove in Phase B (record first). Not raw data. |
| `src/__pycache__/*.cpython-312.pyc` | Generated bytecode (3.12). | Already git-ignored; delete locally, regenerate under 3.9. |
| `conditian/` (name) | Misspelling of "condition"; actually the **papers** folder. | Migrate PDFs → `papers/` (see migration plan); keep originals until copied. |
| `gene_essentiality_default_medium.csv` `gene_id` | Stored as `{'PAxxxx'}` set-repr. | Clean to plain locus tag. |
| `index.html` (32 KB) | Generated project landing page. | Keep or move to `docs/`. |
| `ipynb.rar` | **Mentioned in brief as untracked; NOT found in working tree** at audit time. | Do not commit if it reappears; verify. |
| Many root-level docs (PROJECT_SUMMARY, SUMMARY, INDEX, STUDENT_GUIDE, PACKAGING_GUIDE, QUICK_START, FILE_LIST, DIRECTORY_STRUCTURE) | Education/packaging boilerplate, partly redundant; some claims (e.g. "iPae1146") inconsistent with the actual iMO1056 model. | Consolidate in Phase E; correct model-identity claims. |
| `environment.yml` vs `environment-reccobra39.yml` vs `environment-explicit.txt` | Multiple, possibly inconsistent env specs. | Reconcile after env confirmed (Phase B). Do not lock yet. |

---

## 9. Git state

- Branches (local): `main`, `develop`, `claude/revival-audit` (current), plus safety branches `backup/origin-main`, `safety/pre-claude-20260626-014730`.
- Remote `origin` = `https://github.com/ERFANSAFARPOOR/bioinformatik-project.git` (fetch+push). Remotes **observed only**, not modified.
- `claude/revival-audit` is at `07392445` (= `develop`). `main` is at `4e5a9127`.
- Untracked at audit start: `conditian/`, `environment-explicit.txt`, `environment-reccobra39.yml`, `requirements-current.txt`.
- Recent history shows an education-project restructure (`df830514`) and `.venv` removal (`033d98b9`).

---

## 10. What is and is NOT established

**Established (evidence-backed):**
- Model identity (iMO1056/PAO1), size, objective, feasibility, default medium.
- Real predicted essential-gene set on default medium (166 genes @ 1%).
- Identity of all six papers and their phenotype classes.
- Active environment = reccobra39 with cobra/pandas working.

**NOT established (do not claim):**
- Any model-vs-experiment validation (current metrics are on random data).
- Any cross-strain (PAO1↔PA14) gene mapping.
- Condition-specific media definitions matching the experimental studies.
- Blocked-reaction / gap-filling characterization.
- Final environment reproducing notebooks under reccobra39.
- DOIs/years for Basta & Belanger.

See `TODO.md` for the prioritized, evidence-based work plan and `BLOCKERS.md`
for items needing data or a human decision.

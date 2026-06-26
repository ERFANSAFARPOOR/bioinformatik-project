# E-02 — Notebook reproduction report (reccobra39)

**Date:** 2026-06-26 · **Branch:** `claude/revival-audit`
**Environment:** conda env **reccobra39**, Python **3.9.23**, cobra 0.29.1,
pandas 2.3.2, numpy 2.0.2, matplotlib 3.9.4, matplotlib-venn 1.1.2,
openpyxl 3.1.5, scipy 1.13.1 (added in E-01; all local to reccobra39).
**Method:** `jupyter nbconvert --to notebook --execute --allow-errors`
`--ExecutePreprocessor.kernel_name=python3` (the reccobra39 env kernel),
output to `notebooks/reproduced/*.reproduced.ipynb`. Originals NOT modified.

> Confirmed every notebook executed under Python **3.9.23** (reccobra39), not the
> legacy `.venv` 3.12.6. The embedded `kernelspec` metadata in the reproduced
> files still *displays* `.venv` because nbconvert preserves the source
> kernelspec block; `language_info.version` = 3.9.23 proves the actual kernel.
> Fixing the stored kernelspec metadata is task **E-04**.

## Per-notebook result

| Notebook | Executed | Cell errors | Reproduces? | Notes |
|---|---|---|---|---|
| `01_basic_fba` | yes | **1** | partial | `cell14` raises `ValueError: Reaction 'BIOMASS_PAO' not found in model!` — hard-coded wrong biomass id (model's biomass is `PA_Biomass6_DM`). All earlier cells run. |
| `02_gene_essentiality` | yes | 0 | **yes** | WT growth 1.0479285528 and **166/1054 essential** — essential-gene set **identical** to the audited baseline. Only CSV **row order** differs (cobra `single_gene_deletion(processes=3)` is nondeterministic in order on Windows). |
| `03_experimental_comparison` | yes | 0 | runs, but **not scientific** | Executes cleanly, but compares predictions to **simulated random labels** (`random.seed(42)`). Its precision/recall/F1/Venn are placeholders (BLOCKER B-SCI-01) — must NOT be cited. |

## Errors recorded
- **nb01 / cell14:** `ValueError: Reaction 'BIOMASS_PAO' not found in model!`
  Root cause: a cell references `BIOMASS_PAO`; the real objective/biomass reaction
  is `PA_Biomass6_DM`. → fix in a clean notebook copy (TODO **N-01**), do not edit original.

## Warnings recorded (all cosmetic / non-blocking)
- `zmq _future.py: RuntimeWarning: Proactor event loop does not implement
  add_reader …` — Windows asyncio/zmq under Jupyter; harmless.
- `jupyter_client/connect.py: DeprecationWarning: Jupyter is migrating its paths
  to platformdirs …` — set `JUPYTER_PLATFORM_DIRS=1` to silence; harmless.
- nb01: `PyparsingDeprecationWarning` — from a dependency; harmless.
- GLPK prints `Scaling… Problem data seem to be well scaled` on solver calls — cosmetic.

## Package mismatch / environment notes
- No package import failures under reccobra39 after E-01.
- Legacy authoring env was `.venv` (Python 3.12.6); `src/__pycache__` was cpython-312
  (regenerated as 3.9 on this run).
- nb02's **saved** original output referenced `../models/MODEL1507180020_url.xml`
  (an older filename); current code loads `paeruginosa_MODEL1507180020.xml`. The
  committed outputs therefore predate the current code — another reason to refresh
  notebooks under the canonical kernel.

## Changed outputs vs committed
- nb02 regenerates `results/essentiality/gene_essentiality_default_medium.csv`
  (this file is **gitignored / untracked**). Scientific content identical
  (same 166 essential genes, same WT growth); only row order changed. The
  canonical cleaned copy is the committed
  `data/processed/predicted_essentiality_default_medium.csv` (R-02).

## Conclusion
reccobra39 + E-01 packages **reproduces the real result** (nb02). nb01 has one
hard-coded-id bug to fix in a clean copy; nb03 is non-scientific by construction
until real experimental labels exist. Environment is suitable to become canonical;
lock only after the kernelspec metadata is corrected (E-04) and nb01 fixed (N-01).

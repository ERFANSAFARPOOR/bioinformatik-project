# Teaching notebooks (legacy)

These three notebooks were written for **teaching / demonstration**. They are
archived here so they are not mistaken for the research path.

| Notebook | Role | Scientific caveat |
|---|---|---|
| `01_basic_fba.ipynb` | FBA tutorial | Contains a hard-coded biomass id bug: cell looks up `BIOMASS_PAO`, but the model objective is `PA_Biomass6_DM`. Do not use as a research template. |
| `02_gene_essentiality.ipynb` | Single-gene deletion tutorial | Numerically solid on the default medium (WT ≈ 1.0479 /h; 166 essential @ 1%). Teaching structure only — reusable logic lives in `src/`. |
| `03_experimental_comparison.ipynb` | Model-vs-experiment demo | Compares predictions to **simulated random labels** (`random.seed(42)`). Precision / recall / F1 / Venn from this notebook are **scientifically forbidden** and must never be cited (see `BLOCKERS.md` B-SCI-01). |

## Do not

- Cite nb03 metrics in manuscripts, resumes, or demos as validation results.
- Build new research notebooks by extending these files.
- Treat archived paths as the current notebook entry points.

## Research path (current)

See `docs/TEAM_WORK_MODEL_AND_NEXT_STEPS.md`. New work uses `src/` plus research
notebooks under `notebooks/` (`04_…`, `05_…`, …). Validation metrics (V-01) are
gated until real READY_ONLY labels + reconstructed media + condition-matched
predictions all exist.

Reproduced executed copies (for historical record only) remain under
`notebooks/reproduced/` with the same caveats.

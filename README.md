# Genome-scale metabolic modeling & gene essentiality in *Pseudomonas aeruginosa*

Constraint-based analysis of the **PAO1** model **iMO1056**, comparing predicted
single-gene-deletion essentiality with published experimental Tn-seq data.

> **Current status — documentation reconciled 2026-11-11:** three computational
> media and their knockout predictions exist. An initial experimental comparison
> for **MOPS-pyruvate** has been executed using D-21 labels from the
> Varadarajan2020 reanalysis of Lee2015 Tn-seq. Metrics and an error audit exist;
> **human interpretation/sign-off remains pending. The model is not declared
> validated.** Archived teaching nb03 uses simulated labels and is not
> experimental evidence.

## Current experimental comparison

| Item | Existing result |
|---|---|
| Primary evaluable genes | 1025: 214 experimental positives + 811 negatives |
| Confusion matrix | TP=116, FN=98, TN=764, FP=47 |
| Recall / specificity / precision | 0.542056 / 0.942047 / 0.711656 |
| F1 / MCC | 0.615385 / 0.538031 |
| Policy | `mops_pyruvate_lee2015`; KO/WT growth < 0.01; objective `PA_Biomass6_DM` |
| Review stage | Error audit and evidence prepared; human sign-off pending |

D-21 uses one internally consistent experimental source and a documented
MPAO1-to-PAO1 mapping. Positives are called essential in at least 2/3 Minimal
libraries; negatives are **not called essential in any of the three libraries**,
not universally proven non-essential. The 18 in-model ambiguous (1/3) calls are
excluded. Both label classes come from Varadarajan2020. D-20 Lee-original
positives remain a separate positive-overlap analysis.

Varadarajan2020 reanalyses Lee2015 experiments; it is not an independent
experimental replication. No new wet-lab experiment is reported here.

Evidence: [binary comparison report](project_management/audit/v01_mops_pyruvate/V01_BINARY_VALIDATION_REPORT.md),
[error audit](project_management/audit/v01_mops_pyruvate/V01_ERROR_STRUCTURE_AUDIT.md),
[review evidence](project_management/audit/v01_mops_pyruvate/V01_HUMAN_REVIEW_EVIDENCE.md),
[label/media status](VALIDATION_LABEL_MEDIA_OVERLAP.md), and [D-21 policy](DECISIONS.md).

## Reconstructed media

| Medium | Representation | Existing predictions (essential / 1054 at 1%) | Experimental comparison |
|---|---|---|---|
| `mops_pyruvate_lee2015` | DEFINED | 173 | D-21 primary binary comparison computed |
| `mops_succinate_turner2015` | DEFINED | 177 | No completed matched binary comparison |
| `LB_approx_lee2015` | PARTIAL approximation | 133 | Exploratory; not the primary validation medium |

These are **computational medium reconstructions**. `DEFINED` describes the
source recipe, not complete representation of every experimental component or
measured uptake rate. Each MOPS main-carbon exchange has an uptake cap of
10 mmol/gDW/h by model convention. `LB_approx` independently caps each
amino-acid proxy exchange at 10; this is not a total-carbon uptake limit.
Salts/O2 use effectively unlimited uptake, and unmodeled components are listed
explicitly. Recipe concentrations are not exchange fluxes.
SCFM2, RPMI and host niches still need their own reconstruction and comparison.

Sources: [medium definitions](src/medium.py), [medium tables](data/processed/conditions/README.md),
and [prediction summary](results/essentiality/condition_essentiality_summary.csv).

## Model

| Field | Value |
|---|---|
| Model | **iMO1056** — Oberhardt et al. 2008, *J Bacteriol* |
| Organism / strain | *P. aeruginosa* **PAO1**; locus tags `PAxxxx` |
| Source | BioModels `MODEL1507180020` |
| Canonical SBML | `models/paeruginosa_MODEL1507180020.xml` |
| Size | 1110 reactions · 879 metabolites · 1054 genes |
| Objective | `PA_Biomass6_DM` (maximize) |
| Default-medium result | WT ≈ 1.0479 /h; 166 essential genes at 1% |

The canonical SBML and its byte-identical `models/raw/` copy are read-only.
Default-medium predictions are distinct from the matched MOPS-pyruvate analysis:
173 genes are predicted essential across all 1054 model genes in that medium,
while 163 predicted essentials occur in the 1025-gene D-21 primary join.

## Repository layout

```
models/              canonical SBML; raw/ archived copy; processed/ derived models
papers/              six canonical PDFs + manifest.csv
conditian/           preserved legacy PDF location
notebooks/           04_media_reconstruction; 05_condition_essentiality
  reproduced/        historical re-executed teaching copies
archive/             original teaching notebooks and legacy material
src/                 model_io, fba_utils, medium, gene_essentiality, mapping
scripts/             audit/, mapping/, literature/, validation/ and generation scripts
tests/               model, medium, mapping, label and V-01 integrity checks
data/raw/            literature supplements and mapping source files
data/processed/      gene_mapping/, literature/, ortholog/, conditions/, validation/
results/             essentiality/, comparison/ and other derived outputs
docs/                methods/, project/ and teaching/ notes
project_management/  audit/, planning/, handoff/, publication/
```

Root working-state documents: `TODO.md`, `BLOCKERS.md`, `DECISIONS.md`,
`DATA_PROVENANCE.md`, `PAO1_PROJECT_SCOPE.md`,
`VALIDATION_LABEL_MEDIA_OVERLAP.md`, and `CLAUDE.md`.
Dated cycle logs and initial audits are historical snapshots; the current status
above and the linked V-01 artifacts supersede their earlier gates.

## Environment and verification

Canonical environment: conda **`reccobra39`** (Python 3.9.23, COBRApy 0.29.1,
pandas 2.3.2, GLPK). See `environment-reccobra39.yml` and
`requirements-current.txt`.

```powershell
conda run -n reccobra39 python -m pytest tests/ -q
```

The existing V-01 script is
`scripts/validation/run_v01_mops_pyruvate_binary_validation.py`; it writes to
`data/processed/validation/`. Re-running it is an explicit regeneration step,
not required simply to read the existing results.

## Notebooks

- [04_media_reconstruction](notebooks/04_media_reconstruction.ipynb): medium definitions and model feasibility.
- [05_condition_essentiality](notebooks/05_condition_essentiality.ipynb): per-medium knockout predictions; metrics are computed separately by the V-01 script.
- `archive/teaching_notebooks/01_basic_fba.ipynb`: historical tutorial with the documented `BIOMASS_PAO` identifier bug.
- `archive/teaching_notebooks/02_gene_essentiality.ipynb`: default-medium teaching analysis.
- `archive/teaching_notebooks/03_experimental_comparison.ipynb`: **simulated-label demonstration only**; do not cite its metrics as experimental validation.

## Literature

Six canonical papers are catalogued in [manifest.csv](papers/manifest.csv).
Varadarajan2020 supplements are an additional source for the current D-21 labels.

| Study | Direct experimental strain(s) | Use |
|---|---|---|
| Belanger 2022 | PAO1 | Essentiality and host-condition fitness; match condition/phenotype |
| Lee 2015 | MPAO1 (PAO1-derived) | General and condition-specific essentiality |
| Turner 2015 | PAO1 + PA14 | Separate PAO1 evidence from PA14 and match media |
| Poulsen 2019 | Nine strains including PA14; **PAO1 not screened** | Cross-strain/core-essential secondary evidence |
| Basta 2017 | PA14 | Growth-arrest survival; not interchangeable with growth essentiality |
| Juhas 2015 | Review | Background, not an independent experimental screen |

Lee-original PAO1-tagged lists, Turner PAO1 rows and Belanger can join by identity.
D-21 instead uses the Varadarajan MPAO1 CDS-to-PAO1 mapping, with non-unique and
unmapped cases handled explicitly. PAO1 locus tags in a cross-strain table do not
prove that PAO1 was experimentally screened.
[Poulsen Table 1](https://www.pnas.org/doi/10.1073/pnas.1900570116) excludes PAO1.

Turner-derived PA14↔PAO1 orthology is **APPROVED_LIMITED** for controlled draft
mapping. A PGD export is present but does not replace that decision automatically.
Neither grants permission to report PA14/Poulsen validation metrics.
See the [paper audit](project_management/audit/PAO1_PAPER_RELEVANCE_AUDIT.md)
and [orthology decision](project_management/audit/ORTHOLOGY_HUMAN_REVIEW_DECISION.md).

## Scientific integrity and next steps

Raw models, PDFs and experimental files remain unchanged. Phenotype classes stay
distinct. Metrics require reviewed labels, mapping and matching medium for each
comparison; the completed D-21 cell does not authorize other cells.

1. Review the 47 FP and 98 FN, using the existing diagnostic evidence. Structural
   associations are hypotheses, not established biological causes.
2. Present methods, coverage, metrics and limitations for MOPS-pyruvate. Human
   interpretation remains pending; any model/GPR/medium change needs its own
   sourced decision.
3. Extend other conditions through their own label, mapping and medium checks.

All six study supplement collections are present. Missing download URLs and other
provenance details remain explicit pending items; historical network failures do
not imply those local files are absent.

See [blockers](BLOCKERS.md), [task state](TODO.md),
[handoff](project_management/planning/NEXT_STAGE_HANDOFF_REPORT.md), and
[provenance](DATA_PROVENANCE.md). Model redistribution terms, LICENSE and
CITATION.cff remain publication-readiness tasks.

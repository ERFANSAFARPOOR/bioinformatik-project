---
name: model-validation
description: Compare iMO1056 (PAO1) predicted gene essentiality against validated experimental labels, condition-matched and strain-mapped, with confusion matrices and metrics. Trigger when asked to validate the model, run deletions, define media, or compute precision/recall/F1/MCC.
---

# Model validation

## Trigger
Asked to validate the model, run single-gene deletions, reconstruct media, or
compute agreement metrics (confusion matrix, precision, recall, specificity,
F1, MCC) between predictions and experiments.

## Inputs
- Model `models/paeruginosa_MODEL1507180020.xml` (read-only; copy to modify)
- Validated `literature_evidence.csv` (gene-level) and `gene_mapping.csv`
- Reconstructed condition media (`data/processed/conditions/`)
- `src/` (medium, gene_essentiality, fba_utils)

## Ordered workflow
1. **Gate check:** refuse to compute metrics unless labels, mappings, and
   condition media are validated (B-SCI-01/B-LIT-01/B-MAP-01/B-COND-01 resolved).
2. Reconstruct each experimental medium as exchange bounds (cited); verify model
   feasibility or document infeasibility.
3. Run single-gene deletion per condition on a model copy; classify essential vs
   reduced-growth at multiple thresholds (0/1/5/10%).
4. Map predictions to the matching experimental phenotype class only
   (condition-matched, strain-mapped). Never pool classes.
5. Compute confusion matrix + precision/recall/specificity/F1/MCC per
   condition × class; report coverage (mapped/unmapped/absent/no-GPR genes).
6. Robustness: threshold sensitivity, objective choice, alternate optima/solver
   tolerance, blocked-reaction & gap-filling effects.

## Validation requirements
- WT growth and essential-set sizes reproduce the audited baseline
  (default medium: growth ≈1.0479, 166 essential @1%).
- Every metric records its threshold, condition, strain mapping, and label source.
- Results scripted and reproducible from raw inputs.

## Prohibited behavior
- Computing/reporting metrics on simulated or unvalidated labels.
- Editing the raw model in place; comparing across mismatched media/strains.
- Collapsing the six phenotype classes into one binary label.

## Expected outputs
`results/essentiality/<condition>.csv`, `results/comparison/metrics_<condition>.csv`,
sensitivity tables, and figures — each traceable to a script + data file.

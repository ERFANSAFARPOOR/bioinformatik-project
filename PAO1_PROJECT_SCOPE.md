# PAO1 PROJECT SCOPE

**Original scope:** 2026-07-01

**Current-state reconciliation:** 2026-11-11
**Status:** initial MOPS-pyruvate experimental comparison executed; human
interpretation/sign-off pending. No final validated-model claim.

## 1. Scientific focus

Evaluate predicted single-gene-deletion essentiality of **iMO1056**, the
*Pseudomonas aeruginosa* **PAO1** metabolic reconstruction, against published
PAO1 or PAO1-derived experimental data under a documented matching condition.

- Model: BioModels `MODEL1507180020`,
  `models/paeruginosa_MODEL1507180020.xml`; 1110 reactions, 879 metabolites,
  1054 genes; objective `PA_Biomass6_DM`.
- PAO1 `PAxxxx` and PA14 `PA14_xxxxx` identifiers are not interchangeable.
- Findings are restricted to the evaluated genes, strain context, medium,
  phenotype and essentiality policy; they do not establish species-wide validity.

## 2. Experimental sources and mapping

- **Belanger2022:** PAO1. **Turner2015:** PAO1 and PA14, kept separate.
- **Lee2015:** MPAO1, a PAO1 derivative. Original PAO1-tagged gene lists allow
  direct joins, with the sublineage caveat recorded.
- **D-21 Varadarajan2020:** published reanalysis of Lee2015 Tn-seq on the MPAO1
  genome, **not an independent experimental replication**. Uses Supplementary
  Dataset 1 MPAO1 CDS-to-PAO1 best-hit mapping and Dataset 4 Minimal calls.
  Primary joins require a unique standard PAO1 locus; this is not a blanket
  identity mapping and does not depend on PA14 orthology.
- **Poulsen2019:** nine experimentally screened strains including PA14,
  **excluding PAO1**. PA14-indexed/cluster lists need explicit mapping; PAO1
  reference coordinates do not make them direct PAO1 assays
  ([paper Table 1](https://www.pnas.org/doi/10.1073/pnas.1900570116)).
- **Basta2017:** PA14, growth-arrest survival. Cross-strain mapping and a
  non-growth comparison framework are needed.

Turner-derived PA14↔PAO1 orthology (5365 strict 1:1 pairs) is
**APPROVED_LIMITED** for controlled draft mapping, with conflict resolution
recorded in [the human review decision](project_management/audit/ORTHOLOGY_HUMAN_REVIEW_DECISION.md).
PGD export files are present but do not automatically replace this approval
(D-16). General PA14/Poulsen validation is still a separate, unfinished path.

## 3. Phenotype and medium scope

Keep generally-essential, core-essential, condition-specific-essential,
reduced-fitness, growth-arrest-survival and host-condition-fitness evidence
distinct. Binary labels may be defined **within one reviewed condition/source**;
do not merge these six phenotype classes into one universal label.

Three **computational** medium reconstructions and prediction sets exist:

| Medium | Representation | Predicted essential / 1054 at 1% |
|---|---|---|
| `mops_pyruvate_lee2015` | DEFINED source recipe | 173 |
| `mops_succinate_turner2015` | DEFINED source recipe | 177 |
| `LB_approx_lee2015` | PARTIAL approximation | 133 |

The definitions in `src/medium.py` document unmodeled components and uptake
assumptions. MOPS main-carbon exchanges have an uptake cap of 10 mmol/gDW/h
by model convention; `LB_approx` caps each amino-acid proxy exchange separately
at 10, not total carbon uptake. Salts/O2 are effectively unlimited. Recipe
concentrations are not measured uptake fluxes. `DEFINED` does not mean the experimental environment is fully
represented, and `LB_approx` is not a primary exact-LB validation condition.
SCFM2, RPMI and host niches remain unfinished.

## 4. Completed initial comparison

The D-21 primary universe for MOPS-pyruvate contains **1025 evaluable genes**:
214 positives and 811 negatives. Positives are called essential in at least
2/3 Minimal libraries; negatives are not called essential in any of the three.
Eighteen in-model 1/3 calls are ambiguous and excluded; the remaining 11 model
genes have no eligible D-21 mapping. These are assay-specific labels, not
unconditional biological essentiality/non-essentiality.

The fixed policy is `KO/WT growth < 0.01` and `PA_Biomass6_DM`.
WT growth in this computational medium is approximately 0.405339 /h.
The existing comparison yields **TP=116, FN=98, TN=764, FP=47**;
recall=0.542056, specificity=0.942047, precision=0.711656, F1=0.615385,
MCC=0.538031. Of 173 predicted essentials across all model genes, 163 occur
in this 1025-gene primary join.

The default-medium result (166/1054 essential, WT approximately 1.0479 /h)
is a different condition. Its cleaned file is
`data/processed/essentiality/predicted_essentiality_default_medium.csv`.

Sources: [V-01 report](project_management/audit/v01_mops_pyruvate/V01_BINARY_VALIDATION_REPORT.md),
[overlap/status](VALIDATION_LABEL_MEDIA_OVERLAP.md), and [D-21 decision](DECISIONS.md).
D-20 Lee-original positives remain a separate positive-overlap layer and must
not be mixed with D-21 negatives.

## 5. Remaining work and claims

- Human interpretation/sign-off on the existing FP/FN audit and evidence is
  pending. Diagnostic categories are hypotheses, not proven causes.
- Other media and phenotype comparisons require their own reviewed labels,
  mappings, medium reconstruction and predictions.
- Source-download URLs and other provenance gaps remain explicit.
- No model/GPR/medium/threshold modifications follow automatically from error
  counts; any curation needs a separate sourced decision.

Historical claims that all supplements are missing, no media are built or no
real comparison exists are superseded for the completed D-21 cell. Archived
teaching nb03 still uses random simulated labels and remains invalid as
experimental evidence.

Do not claim species-wide validation, cite synthetic metrics, treat PA14 data
as PAO1 identity joins, present the Lee-derived remap as independent replication,
or call the model fully validated before the remaining interpretation.

# PUBLICATION PLAN

Plan to reach (1) a reproducible public repository and (2) a scientifically
defensible manuscript. This is a **plan**, not a submission-ready result.

**Status reconciled 2026-11-11:** real labels, computational media and the
D-21/V-01 MOPS-pyruvate binary comparison already exist. Confusion-matrix
metrics and diagnostic error audits are computed; human interpretation is
pending. Other cells require their own label/mapping/media checks. See
`VALIDATION_LABEL_MEDIA_OVERLAP.md` and
`project_management/audit/v01_mops_pyruvate/V01_BINARY_VALIDATION_REPORT.md`.

---

## 1. Scientific question (scoped to evidence available)

> How well does the *P. aeruginosa* **PAO1** genome-scale model **iMO1056**
> predict **gene essentiality / fitness**, when compared — *condition-matched and
> strain-mapped* — against published Tn-seq experimental datasets, and where do
> predictions and experiments diverge?

The comparison must respect six distinct experimental phenotype classes
(general, core, condition-specific essential; reduced fitness; growth-arrest
survival; host-condition fitness) and the PAO1↔PA14 strain difference.

**PAO1-first (reconciled 2026-11-11).** Lee-original PAxxxx labels, Turner
PAO1 rows and Belanger PAO1 use PAO1 locus-ID joins (with the MPAO1 sublineage
caveat for Lee). The first binary cell instead uses **Varadarajan2020's
reanalysis of Lee2015 Tn-seq**, mapped from MPAO1 via unique-standard-PAO1 best
hits in Dataset 1, with both polarities from the same source. This is not
independent replication and not every MPAO1 gene maps to the model.

Basta 2017 (PA14) and Poulsen 2019 (nine strains including PA14, **excluding
PAO1**) are background or later cross-strain analyses. Poulsen's `PA14_ID` /
`Cluster_ID` coordinates do not supply a PAO1 experimental subset. The Turner
strict 1:1 mapping has **APPROVED_LIMITED** status for controlled drafts only;
that approval alone does not make either source validation-ready. Do not
claim that iMO1056 validates the species across strains. See
`PAO1_PROJECT_SCOPE.md` and `ORTHOLOGY_HUMAN_REVIEW_DECISION.md`.

The canonical official-PGD mapping is present (1023 unique, 2 ambiguous, 29
unmapped model genes); a separate 5374-pair final RBH table passes its local
structural checks. This artifact state is distinct from study-specific use
approval and from completed cross-strain validation. See
`data/processed/gene_mapping/gene_mapping.csv` and
`data/processed/ortholog/final/pao1_pa14_orthologs_pseudomonas_rbh_20260712.csv`.

## 2. Model validation design (defensible)

1. **Predictions:** single-gene deletion on iMO1056 per reconstructed condition.
   The existing primary MOPS-pyruvate cell is frozen at `growth_ratio < 0.01`
   and objective `PA_Biomass6_DM`; any future sensitivity analysis must be
   separate and documented, not retrospective tuning of the primary result.
2. **Experimental labels:** extracted from official supplements, per study, with
   the study's own essentiality/fitness definition and threshold preserved.
3. **Strain mapping:** distinguish direct PAO1 locus-ID joins, the D-21
   MPAO1→PAO1 DS1 best-hit map, and PA14→PAO1 orthology. Preserve ambiguity,
   missing mappings and absent-from-model genes. In D-21, 1025 of 1054 model
   genes enter the primary binary join; 18 ambiguous and 11 other genes do not.
4. **Condition matching:** compare each prediction only to the experiment whose
   medium/carbon source/electron acceptor/growth phase it reconstructs.
5. **Metrics (only after 1–4 validated):** confusion matrix, precision, recall,
   specificity, F1, **MCC**; plus coverage (mapped, unmapped, absent-from-model,
   present-but-no-GPR genes).
6. **Robustness:** threshold sensitivity, objective-function choice, alternate
   optima / solver tolerance, blocked-reaction & gap-filling effects.

Each comparison is reported **per condition × per phenotype class**, never pooled
into one binary essential label.

## 3. Manuscript outline

- **Introduction:** *P. aeruginosa* essentiality; FBA/GSMM; gap addressed.
- **Methods:** model (iMO1056, PAO1, BioModels MODEL1507180020, SHA recorded);
  environment (reccobra39, cobra 0.29.1, GLPK); medium reconstructions (cited);
  deletion protocol & thresholds; strain mapping; statistics.
- **Results:** prediction–experiment agreement per condition/class; discrepancy
  analysis; sensitivity/robustness.
- **Discussion / Limitations (mandatory honesty):** PAO1 model vs PA14 data;
  media approximations; FBA cannot capture regulation; missing formulas; gap-fill
  effects; coverage limits.
- **Data/Code availability:** repo, env lock, provenance, scripts.

## 4. Target venues (candidates — not committed)
Microbiology-/systems-biology methods venues (e.g. *mSystems*, *BMC
Bioinformatics*, *Microbiology*, *PLOS Comput Biol*). Decide after results.

## 5. Reproducibility deliverables
- Locked environment (Phase B), `tests/` pinning key numbers, scripted figures,
  `DATA_PROVENANCE.md` with hashes/URLs, README quick-start, CITATION.cff, LICENSE.

## 6. Gating conditions (must hold before submission)
- [x] Real experimental labels for **D-21 MOPS-pyruvate** (both polarities from
      Varadarajan reanalysis; no simulated teaching labels)
- [x] Cited computational **MOPS-pyruvate** medium and per-gene predictions
- [x] Binary metrics executed for this primary cell
- [ ] Human interpretation/sign-off of primary FP/FN evidence and limitations
- [ ] Source/medium/phenotype checks for any additional comparison cells
- [ ] Validated PAO1↔PA14 mapping — **only** if PA14 data are used (B-MAP-01)
- [x] Verified citations incl. Basta & Belanger (B-LIT-02, resolved 2026-06-26;
      strains re-verified from PDFs 2026-07-01, B-STRAIN-02)
- [x] Notebooks reproduce under reccobra39 (B-ENV-01; env lock E-03 still open)
- [ ] Model redistribution license confirmed (DATA_PROVENANCE §1)

## 7. Reporting limits

The existing D-21/V-01 numbers may be described as a **preliminary
condition-specific comparison**, with its experimental-label, mapping,
coverage and medium assumptions. They are not a declaration that the model
is fully validated or paper-ready. Do not cite simulated teaching-notebook
metrics, mix D-20 positives with D-21 negatives, or present Varadarajan as an
independent experiment. Any additional cell or robustness analysis needs its
own explicit provenance and comparability checks before reporting metrics.

# PUBLICATION PLAN

Plan to reach (1) a reproducible public repository and (2) a scientifically
defensible manuscript. This is a **plan**, not a claim of results. No metric is
computed until experimental labels and gene mappings are validated.

---

## 1. Scientific question (scoped to evidence available)

> How well does the *P. aeruginosa* **PAO1** genome-scale model **iMO1056**
> predict **gene essentiality / fitness**, when compared — *condition-matched and
> strain-mapped* — against published Tn-seq experimental datasets, and where do
> predictions and experiments diverge?

The comparison must respect six distinct experimental phenotype classes
(general, core, condition-specific essential; reduced fitness; growth-arrest
survival; host-condition fitness) and the PAO1↔PA14 strain difference.

**PAO1-first (revised 2026-07-01).** The validation is built on **PAO1/MPAO1**
datasets that join the model by identity (Lee 2015 MPAO1; Turner 2015 PAO1 rows;
Belanger 2022 PAO1). PA14/multi-strain data (Basta 2017;
non-PAO1 Poulsen strains) are **background/discussion** or a **later**
orthology-mapped comparison — never presented as PAO1 validation. No claim that
the model validates *P. aeruginosa* across strains. See `PAO1_PROJECT_SCOPE.md`.

## 2. Model validation design (defensible)

1. **Predictions:** single-gene deletion on iMO1056 per reconstructed condition;
   classify essential vs reduced-growth at multiple thresholds (0/1/5/10%).
2. **Experimental labels:** extracted from official supplements, per study, with
   the study's own essentiality/fitness definition and threshold preserved.
3. **Strain mapping:** PAO1/MPAO1 rows join by **identity** (high confidence);
   PAO1↔PA14 validated orthology applied **only** to PA14/multi-strain rows, with
   one-to-many/missing retained (not on the critical path — see D-12).
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
- [ ] Real (non-simulated) experimental labels (B-SCI-01 / B-LIT-01 resolved)
- [ ] Cited, reconstructed condition media (B-COND-01)
- [ ] Validated PAO1↔PA14 mapping — **only** if PA14 data are used (B-MAP-01)
- [x] Verified citations incl. Basta & Belanger (B-LIT-02, resolved 2026-06-26;
      strains re-verified from PDFs 2026-07-01, B-STRAIN-02)
- [x] Notebooks reproduce under reccobra39 (B-ENV-01; env lock E-03 still open)
- [ ] Model redistribution license confirmed (DATA_PROVENANCE §1)

## 7. Explicitly out of scope until evidence exists
No precision/recall/F1/MCC numbers, no Venn/confusion figures, and no
essentiality "accuracy" statements are produced or reported until §6 gates pass.

# PAO1 PROJECT SCOPE

**Date:** 2026-07-01 · **Branch:** `claude/revival-audit`
**Status:** under revival; not yet experimentally validated.

This document fixes the scientific scope of the project so that no analysis or
claim drifts beyond what the model and data support.

---

## 1. Primary focus (Tier 1)

**Validate the *P. aeruginosa* PAO1 genome-scale metabolic model iMO1056 against
PAO1 (or PAO1-derived) experimental gene-essentiality / fitness data.**

- Model: **iMO1056** (Oberhardt et al. 2008), BioModels `MODEL1507180020`,
  file `models/paeruginosa_MODEL1507180020.xml`
  (SHA-256 `0868a5eb…1212ead`), 1110 reactions / 879 metabolites / 1054 genes,
  objective `PA_Biomass6_DM`, default-medium WT growth ≈ 1.0479285528 /h.
- The comparison is model-predicted single-gene-deletion essentiality vs.
  experimentally measured essentiality/fitness, **strain-matched (PAO1)** and
  **condition-matched (medium reconstructed from the source paper)**.

## 2. Why the model is PAO1 (not PA14, not "P. aeruginosa" broadly)

- The model's gene identifiers are **PAO1 `PAxxxx` locus tags** (e.g. PA0005),
  not PA14 `PA14_xxxxx` tags.
- iMO1056 is explicitly the **PAO1** reconstruction (Oberhardt 2008, *J Bacteriol*,
  "…Pseudomonas aeruginosa PAO1").
- Therefore the model represents **one strain, PAO1**. It does **not** validate
  *P. aeruginosa* as a species, and it does not represent PA14 metabolism except
  insofar as orthologous genes coincide.

## 3. Why PAO1 / MPAO1 datasets are Tier 1

Experimental gene lists indexed in **PAO1 `PAxxxx`** locus tags join **directly**
to model gene IDs (identity mapping, high confidence) — no cross-strain orthology
step, so no orthology-induced coverage loss or ambiguity.

- **MPAO1** is a PAO1 sublineage/derivative that uses the PAO1 locus-tag system.
  MPAO1 data are treated as **PAO1-derived (Tier 2)**: directly usable, but with
  a recorded sublineage caveat (possible small genomic differences vs the
  reference PAO1 used to build iMO1056).

Re-audit finding (2026-07-01): three of the six existing papers are PAO1 or
PAO1-derived (**Belanger 2022 = PAO1**, **Lee 2015 = MPAO1**, **Turner 2015 =
PAO1+PA14 mixed with usable PAO1 rows**). This removes the strain barrier for the
first PAO1-side validation and is a substantial change from the earlier
"most studies are PA14" framing. See `PAO1_PAPER_RELEVANCE_AUDIT.md`.

## 4. Why PA14-only datasets require validated orthology first

- PAO1 and PA14 locus tags are **not interchangeable**. A PA14 essential gene
  cannot be assigned to a PAO1 model gene without an **authoritative ortholog
  table** (e.g. pseudomonas.com orthologs), which is currently **not available**
  in this environment (B-NET).
- The current PA14 mapping is **symbol/annotation-based only** (386 medium-
  confidence 1:1, 22 low-confidence ambiguous, 646 unmapped of 1054) — not
  validated orthology. Metrics built on it would carry large unmapped/uncertain
  mass and are not reportable.
- Consequence: PA14-only sources (**Basta 2017**) are **secondary/background**
  until validated orthology exists. Multi-strain sources (**Poulsen 2019**) are
  usable only for their PAO1-strain rows or as core-essential background.

## 5. Why the six phenotype classes cannot be collapsed to one binary label

The studies measure biologically distinct phenotypes under distinct methods,
media, and statistical thresholds:

1. generally-essential 2. core-essential 3. condition-specific-essential
4. reduced-fitness 5. growth-arrest-survival-determinant 6. host-condition-fitness

Collapsing these into a single "essential/non-essential" bit would merge
incompatible definitions (e.g. *survival during growth arrest* is not *required
for growth*), inflate apparent agreement, and destroy provenance. Each class is
kept separate in `data/processed/literature_evidence.csv` (`phenotype_type`) and
compared only against a like-for-like model prediction under the matching medium.

## 6. What the model side already provides (real, reproducible)

- Single-gene-deletion essentiality under the **default medium** (glucose + O2
  aerobic): **166 / 1054 predicted essential** at a 1% growth-ratio threshold.
- Cleaned, join-ready predictions:
  `data/processed/predicted_essentiality_default_medium.csv` (1054 rows).
- Reproduced under the canonical env `reccobra39` (Python 3.9.23); WT growth
  1.0479285528 /h reproduces exactly (nb02).

## 7. What is still missing before validation metrics can be computed

- [ ] Experimental gene lists downloaded from paper **supplements** (blocked:
      B-NET / B-LIT-01) and parsed into `literature_evidence.csv` gene-level rows.
- [ ] Per-condition **media reconstruction** (CF sputum/SCFM, LB, minimal,
      host-mimicking, growth-arrest) as in-model exchange bounds (B-COND-01).
- [ ] Per-condition single-gene-deletion predictions at multiple thresholds.
- [ ] For PA14/multi-strain rows only: **validated PAO1↔PA14 orthology**
      (B-MAP-01 / B-NET).
- [ ] Only then: precision / recall / specificity / F1 / MCC / confusion matrices,
      per condition × phenotype class, with mapped/unmapped coverage reported.

**No validation metrics are computed yet.** The only "comparison" currently in the
notebooks uses **simulated random labels** and is invalid (B-SCI-01); it must not
be reported.

## 8. Out-of-scope claims (explicitly forbidden)

- "The model validates *P. aeruginosa* essentiality" (it is PAO1-specific).
- Any precision/recall/F1/MCC number derived from simulated labels.
- Treating PA14 essential-gene lists as PAO1 model genes without validated orthology.
- Merging the six phenotype classes into a single binary essentiality label.

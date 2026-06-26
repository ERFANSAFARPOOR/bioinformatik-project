# VALIDATION-READINESS REPORT

**Date:** 2026-06-26 · **Branch:** `claude/revival-audit`
**Purpose:** State exactly what exists and what is missing before any
model-vs-experiment validation metric is computed. **No metrics are computed
here** (per instruction and BLOCKER B-SCI-01). This report is the gate that must
be satisfied before V-01.

---

## 1. Verdict

**NOT READY to compute validation metrics.** The model-side predictions exist and
are reproducible, but on the experiment side there are currently **zero validated
experimental labels in the repository**, **no reconstructed experimental media**,
and the strain bridge (PAO1↔PA14) is only partially built from annotation symbols.
Four P0 blockers remain (B-SCI-01, B-LIT-01, B-NET, B-COND-01) plus B-MAP-01.

---

## 2. Predictions available (model side) — READY

| Item | Value | Source |
|---|---|---|
| Model | iMO1056, *P. aeruginosa* **PAO1** | `models/paeruginosa_MODEL1507180020.xml` |
| Reproduced under reccobra39 | yes (Py 3.9.23) | `notebooks/reproduced/REPRODUCTION_REPORT.md` |
| Predicted essential genes (default medium, 1% growth-ratio) | **166 / 1054** | `data/processed/predicted_essentiality_default_medium.csv` (cleaned) |
| WT growth (default medium) | 1.0479285528 /h | E-02 |
| Conditions simulated so far | **1** (default: glucose + O2 aerobic only) | model default medium |

Gap: predictions exist for only ONE medium. Condition-specific predictions
(S-01) require reconstructed media (C-01), which do not yet exist.

---

## 3. Experimental labels — NOT AVAILABLE

| Study (verified) | Strain | Phenotype class | Labels in repo? | Why not |
|---|---|---|---|---|
| Juhas 2015 (10.1099/mic.0.000161) | review | generally essential | no | review; primary lists live in cited studies |
| Turner 2015 (10.1073/pnas.1419677112) | **PA14** | condition-specific essential (CF sputum) | no | PNAS supplement `sd01–04.xlsx` **403-blocked** (B-NET) |
| Lee 2015 (10.1073/pnas.1422186112) | **PA14** | general + condition-specific essential | no | PNAS supplement `sd01.xlsx` **403-blocked** (B-NET) |
| Poulsen 2019 (10.1073/pnas.1900570116) | **PA14 / multi-strain** | core essential | no | gene list in PNAS supp / Broad fitness portal; not yet retrieved |
| Basta 2017 (10.1128/mBio.01170-17) | PA14 (confirm) | growth-arrest survival determinant | no | supplement not yet retrieved |
| Belanger 2022 (10.3389/fmicb.2022.1055512) | confirm | host-condition fitness | no | supplement not yet retrieved |

The only "experimental" labels currently in the codebase are the **simulated
random labels** in `notebooks/03_experimental_comparison.ipynb` — invalid
(B-SCI-01). They must not be used.

**Six phenotype classes remain distinct** (general / core / condition-specific
essential; reduced-fitness; growth-arrest survival; host-condition fitness) and
must not be merged into one binary label.

---

## 4. Mapped vs unmapped genes (strain bridge)

From `data/processed/gene_mapping.csv` (NCBI RefSeq symbol-based; see G-01):

| Layer | Count | Confidence |
|---|---|---|
| model gene → PAO1 locus tag (identity) | **1054 / 1054** | high |
| model/PAO1 → PA14 via unique gene symbol | **386** | medium (annotation, not validated orthology) |
| → PA14 ambiguous / one-to-many | **22** | low (candidates retained, unresolved) |
| → PA14 unmapped (no symbol) | 335 | unmapped |
| → PA14 unmapped (symbol, no PA14 match) | 311 | unmapped |

**Implication:** for the PA14 studies (Turner, Lee, Poulsen, Basta), only
**~408/1054 (39%)** model genes currently have any PA14 handle, and those are
annotation-symbol-based. A confusion matrix built on this alone would have large
unmapped/uncertain mass. Validated orthology (pseudomonas.com) is required to
raise coverage/confidence — blocked by B-NET.

Direction also matters: experimental lists are PA14-indexed; mapping them onto the
PAO1 model needs the **reverse** (PA14→PAO1) join, including PA14 genes **absent
from the model** (the model covers metabolism only, ~1054 of ~5600 genes).

---

## 5. Media definitions

| Medium | Defined in model? | Needed for |
|---|---|---|
| Default (glucose 10, O2 1000, NH4/Pi/SO4/metals) aerobic | yes (model default) | baseline only |
| CF sputum / SCFM | **no** | Turner 2015 |
| LB (rich) | **no** | Lee 2015 (general essential) |
| Defined minimal / nutrient-limited | **no** | Lee 2015 (condition-specific) |
| Carbon (pyruvate)-limited; oxygen-limited growth arrest | **no** | Basta 2017 |
| Host-mimicking (tissue-culture ± serum, abscess, skin organoid) | **no** | Belanger 2022 |

No experimental medium is reconstructed yet (B-COND-01). Comparing essentiality
across mismatched media is invalid, so per-condition media must be built (with
cited composition → exchange bounds) before per-study metrics.

---

## 6. Essentiality / fitness definitions

| Side | Definition | Threshold |
|---|---|---|
| Model (this repo) | FBA single-gene deletion; essential if KO growth < X% of WT | 1% (provisional; sensitivity 0/1/5/10% planned, D-09) |
| Tn-seq studies | insertion depletion / fitness score vs control; study-specific statistical cutoffs | **not yet extracted** (needs supplements; per-study) |

These are **not equivalent** and must be aligned per study (each study's own
definition + threshold recorded in `literature_evidence.csv`, gene-level rows
still PENDING).

---

## 7. Remaining blockers (gating V-01)

| Blocker | P | Blocks |
|---|---|---|
| **B-SCI-01** | P0 | any real metric (current comparison is simulated) |
| **B-LIT-01** | P0 | experimental labels (supplements not downloaded) |
| **B-NET** | P0 | the downloads above + validated orthology (403/timeout here) |
| **B-COND-01** | P0 | per-condition media reconstruction |
| **B-MAP-01** | P0 | validated PAO1↔PA14 orthology (only symbol-based so far) |
| B-MODEL-01/02 | P2 | blocked-reaction / formula context for interpreting FN/FP |

## 8. What would make this READY (checklist)
- [ ] Experimental gene lists downloaded per study, with provenance (B-LIT-01/B-NET)
- [ ] `literature_evidence.csv` gene-level rows populated, six classes kept distinct (L-03)
- [ ] Validated PAO1↔PA14 orthology merged; coverage + ambiguity reported (B-MAP-01)
- [ ] Per-study media reconstructed and cited; model feasible per condition (C-01)
- [ ] Per-condition predictions generated at multiple thresholds (S-01)
- [ ] Only then: confusion matrix / precision / recall / specificity / F1 / MCC,
      per condition × phenotype class, with coverage caveats (V-01)

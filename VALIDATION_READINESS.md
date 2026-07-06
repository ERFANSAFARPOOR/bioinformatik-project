# VALIDATION-READINESS REPORT

**Date:** 2026-06-26 (updated **2026-07-06**) · **Branch:** `claude/revival-audit`
**Purpose:** State exactly what exists and what is missing before any
model-vs-experiment validation metric is computed. **No metrics are computed
here** (per instruction and BLOCKER B-SCI-01). This report is the gate that must
be satisfied before V-01.

---

## 0. Update 2026-07-06 — raw supplements now physically present (still NOT ready for metrics)

**What changed:** the L-section human-assisted downloads mean the experimental
labels now **physically exist as raw supplements** in the repo for:
- **lee2015** (MPAO1) — `pnas.1422186112.sd01.xlsx` (general + condition-specific essential)
- **turner2015** (PAO1+PA14) — `sd01–sd10.xlsx` (PAO1 essentiality + condition/fitness)
- **belanger2022** (PAO1) — `Data_Sheet_1/2.XLSX` (essential + host-condition)
- **varadarajan2020** (MPAO1, bonus) — `Supplementary Dataset 1–4` (per-condition essentiality + MPAO1→PAO1 map)

Audited (`SUPPLEMENT_INVENTORY_AUDIT.md`), provenance-logged (`DATA_PROVENANCE.md §3d`),
parse notes written (`data/raw/literature/<study>/SUPPLEMENT_PARSE_NOTES.md`).

**What has NOT changed — still NOT READY for any metric.** "Raw supplement present"
≠ "validated gene-level label parsed." All of the following are still required and
absent: (a) gene-level rows parsed into the evidence table with per-study
essentiality **definition + threshold** confirmed; (b) reconstructed per-condition
**media** (B-COND-01); (c) per-condition **predictions** (S-01); (d) for MPAO1
sources, the MPAO1→PAO1 mapping validated. **No precision/recall/F1/MCC/specificity/
confusion matrix may be computed.** B-SCI-01, B-COND-01 remain OPEN; B-LIT-01
narrowed (meegid2022/poulsen2019/basta2017 still missing); B-NET open (source URLs
+ missing studies).

---

## 1. Verdict

**NOT READY to compute validation metrics.** The model-side predictions exist and
are reproducible; experimental labels are now **physically present** as raw
supplements for 4 studies (see §0) but are **not yet parsed into validated
gene-level rows**, there is **no reconstructed experimental media**, and the strain
bridge (PAO1↔PA14) is only partially built from annotation symbols. P0 blockers
remain (B-SCI-01, B-COND-01; B-LIT-01 narrowed; B-NET open). **B-MAP-01 is
P1/secondary** — it gates only PA14-only/non-PAO1 datasets (Basta; non-PAO1
Poulsen), **not** the first PAO1/MPAO1 validation, which joins by identity.

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

**Strain re-audited 2026-07-01 (B-STRAIN-02) — earlier PA14 labels corrected:**

| Study (verified) | Strain (corrected) | Phenotype class | Labels in repo? | Why not |
|---|---|---|---|---|
| Juhas 2015 (10.1099/mic.0.000161) | review | generally essential | no | review; primary lists live in cited studies |
| Turner 2015 (10.1073/pnas.1419677112) | **PAO1 + PA14** | condition-specific essential (CF sputum) | no | PNAS supplement `sd01–04.xlsx` **403-blocked** (B-NET); PAO1 rows usable |
| Lee 2015 (10.1073/pnas.1422186112) | **MPAO1** (PAO1-derived) | general + condition-specific essential | no | PNAS supplement `sd01.xlsx` **403-blocked** (B-NET) |
| Poulsen 2019 (10.1073/pnas.1900570116) | multi-strain (incl. **PAO1**) | core essential | no | PNAS supp / Broad portal not retrieved |
| Basta 2017 (10.1128/mBio.01170-17) | **PA14** (UCBPP-PA14) | growth-arrest survival determinant | no | supplement not retrieved; needs orthology |
| Belanger 2022 (10.3389/fmicb.2022.1055512) | **PAO1** | host-condition fitness | no | supplement not retrieved |

**Key change:** Lee (MPAO1), Belanger (PAO1) and Turner's PAO1 rows join to the
model by **identity — no orthology needed**. The first validation is therefore
strain-unblocked; only Basta (PA14) and non-PAO1 Poulsen strains need B-MAP-01.

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

**Implication (revised 2026-07-01):** orthology is now needed only for the
**PA14-only** rows (**Basta**; non-PAO1 **Poulsen** strains), where only
**~408/1054 (39%)** model genes have any (symbol-based) PA14 handle — insufficient
for metrics until validated orthology exists (B-MAP-01/B-NET). The **PAO1/MPAO1**
sources (Lee, Turner PAO1 rows, Belanger, new meegid2022) do **not** need this
bridge — they map by identity at high confidence. See `ORTHOLOGY_STATUS_REPORT.md`.

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
| B-MAP-01 | **P1 / secondary** | validated PAO1↔PA14 orthology — gates **only** PA14-only/non-PAO1 datasets (Basta; non-PAO1 Poulsen). **Not** required for the first PAO1/MPAO1 validation (Lee, Belanger, Turner PAO1 rows, meegid2022 → identity join). |
| B-MODEL-01/02 | P2 | blocked-reaction / formula context for interpreting FN/FP |

> **First PAO1/MPAO1 validation is strain-unblocked.** Lee 2015 (MPAO1),
> Belanger 2022 (PAO1), Turner 2015 PAO1 rows, and the new meegid2022 (PAO1) all
> carry PAO1 (`PAxxxx`) locus tags and map to the iMO1056 model **by identity** —
> no PA14 orthology (B-MAP-01) is needed for these. B-MAP-01 remains open only for
> the PA14-only path (Basta 2017; non-PAO1 Poulsen strains).

## 8. What would make this READY (checklist)
- [ ] Experimental gene lists downloaded per study, with provenance (B-LIT-01/B-NET)
- [ ] `literature_evidence.csv` gene-level rows populated, six classes kept distinct (L-03)
- [ ] Validated PAO1↔PA14 orthology merged; coverage + ambiguity reported (B-MAP-01)
- [ ] Per-study media reconstructed and cited; model feasible per condition (C-01)
- [ ] Per-condition predictions generated at multiple thresholds (S-01)
- [ ] Only then: confusion matrix / precision / recall / specificity / F1 / MCC,
      per condition × phenotype class, with coverage caveats (V-01)

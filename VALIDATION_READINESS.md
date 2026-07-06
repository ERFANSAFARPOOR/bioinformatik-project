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
narrowed (all corpus supplements now present — Poulsen/Basta added 2026-07-06;
meegid2022 removed from active scope); B-NET open (source URLs + pseudomonas.com
orthology).

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

## 3. Experimental labels — RAW SUPPLEMENTS PRESENT; DRAFT gene-level parsed (still NOT validated for metrics)

**Strain re-audited 2026-07-01 (B-STRAIN-02); supplements landed + parsed to
DRAFT 2026-07-06.** Distinguish four states, which are NOT the same thing:
(a) **raw supplement present**; (b) **parse notes + thresholds sourced**;
(c) **DRAFT gene-level rows parsed** (with review flags); (d) **validated
gene-level labels** (peer-reviewed against media + predictions). Only (a)–(c)
exist; (d) does not — so **no metric may be computed** (B-SCI-01).

| Study (verified) | Strain | Phenotype class | Raw supp? | Threshold sourced? | DRAFT parsed? | Validated labels? |
|---|---|---|---|---|---|---|
| Juhas 2015 (10.1099/mic.0.000161) | review | generally essential | n/a (review) | n/a | no | no — review; lists live in cited studies |
| Turner 2015 (10.1073/pnas.1419677112) | **PAO1 + PA14** | general + condition + host fitness | ✅ sd01–sd10 | ✅ (P<0.01+mclust; FC≥4,P<0.05) | ✅ PAO1 sheets (sd01/06/07/10) | **no** — draft only; paired sheets sd03/04/05/09 open (L03-B3) |
| Lee 2015 (10.1073/pnas.1422186112) | **MPAO1** (PAO1-derived) | general + condition-specific essential | ✅ sd01 | ✅ (P<0.001; consensus pools) | ✅ (general=READY; per-medium=NEEDS_REVIEW) | **no** — draft only |
| Poulsen 2019 (10.1073/pnas.1900570116) | multi (PA14_ID/Cluster_ID; **9 strains exclude PAO1**) | core essential | ✅ sd01–07 (2026-07-06) | **yes** (FiTnEss adj. P<0.05 both reps; FWER/FDR) | no | no — **mapping-blocked**: needs PA14→PAO1 orthology (no PAO1 in supplement) |
| Basta 2017 (10.1128/mBio.01170-17) | **PA14** (UCBPP-PA14) | growth-arrest survival determinant | ✅ sd1–4+tif (2026-07-06) | **yes** (read ratio ≤0.25 & Fisher P≤0.05) | no | no — needs call derivation + PA14→PAO1 orthology; phenotype ≠ FBA growth |
| Belanger 2022 (10.3389/fmicb.2022.1055512) | **PAO1** | general + condition + host-condition fitness | ✅ DS1/DS2 | ✅ (Gumbel/TraDIS ≥4/5, T0 ≥2/3) | ✅ | **no** — draft only |
| Varadarajan 2020 (10.1038/s41522-020-00154-8) | **MPAO1** | (essentiality = Lee re-mapped) | ✅ DS1–4 | citation VERIFIED | **no** — derivative of Lee (double-count); mapping resource only | no |

DRAFT outputs (NOT validated, NOT for metrics):
`data/processed/literature/{lee2015,turner2015,belanger2022}_parsed_gene_evidence.csv`
and aggregate `data/processed/literature_evidence_gene_level_DRAFT.csv` (5,093
rows; 6 phenotype classes kept distinct). Canonical
`data/processed/literature_evidence.csv` (study-level) is unchanged. Thresholds
sourced in `THRESHOLD_METHOD_AUDIT.md`.

**Key change:** Lee (MPAO1), Belanger (PAO1) and Turner's PAO1 rows join to the
model by **identity — no orthology needed**. The first validation is therefore
strain-unblocked; only Basta (PA14) and non-PAO1 Poulsen strains need B-MAP-01.

DRAFT parsed gene-level labels now exist (§3 above) but are **not validated** and
must not be fed to any metric. The only labels ever used in a metric so far are
the **simulated random labels** in `notebooks/03_experimental_comparison.ipynb`
— invalid (B-SCI-01). Neither the simulated labels nor the unreviewed DRAFT may
be used to compute precision/recall/F1/MCC.

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
sources (Lee, Turner PAO1 rows, Belanger) do **not** need this
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

**Media-source audit (2026-07-07):** `MEDIA_SOURCE_AUDIT.md` now records, per
study, each condition's supplement/paper locator and whether composition is
DEFINED (MOPS-pyruvate, MOPS-succinate, RPMI-1640, M9, pyruvate-minimal), PARTIAL
(SCFM2 — recipe in Turner sd08 but mucin/DNA polymers; LB/BHI/MHB; RPMI+serum), or
MEDIA_GAP_PENDING (native sputum, serum/FBS, urine, abscess, skin, and Basta's
carbon/oxygen-limited arrest). **C-01b not started; no exchange bounds invented.**

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
| **B-SCI-01** | P0 | any real metric (current comparison is simulated; DRAFT labels unvalidated) |
| **B-LIT-01** | P0 | **NARROWED** — all corpus supplements now present (Poulsen/Basta added 2026-07-06); Lee/Turner/Belanger parsed to DRAFT; still blocks Poulsen/Basta DRAFT (orthology+threshold gate) and promotion of DRAFT → validated evidence. (meegid2022 removed from active scope.) |
| **B-NET** | P0 | pseudomonas.com validated orthology (for Basta/Poulsen) + `SOURCE_URL_PENDING` for obtained files (403/timeout here) |
| **B-COND-01** | P0 | per-condition media reconstruction |
| B-MAP-01 | **P1 / secondary** | validated PAO1↔PA14 orthology — gates **only** PA14-only/non-PAO1 datasets (Basta; non-PAO1 Poulsen). **Not** required for the first PAO1/MPAO1 validation (Lee, Belanger, Turner PAO1 rows → identity join). |
| B-MODEL-01/02 | P2 | blocked-reaction / formula context for interpreting FN/FP |

> **First PAO1/MPAO1 validation is strain-unblocked.** Lee 2015 (MPAO1),
> Belanger 2022 (PAO1), and Turner 2015 PAO1 rows all carry PAO1 (`PAxxxx`) locus
> tags and map to the iMO1056 model **by identity** — no PA14 orthology (B-MAP-01)
> is needed for these. B-MAP-01 remains open only for the PA14-only path
> (Basta 2017; non-PAO1 Poulsen strains).

## 8. What would make this READY (checklist)
- [~] Experimental gene lists downloaded per study, with provenance (B-LIT-01/B-NET)
      — DONE for Lee/Turner/Belanger/Varadarajan/Poulsen/Basta; PENDING source URLs. (meegid2022 removed from active scope.)
- [~] `literature_evidence.csv` gene-level rows populated, six classes kept distinct (L-03)
      — DRAFT parsed to `literature_evidence_gene_level_DRAFT.csv` (**5,148 rows**;
      Lee/Turner/Belanger). **L03-B3 RESOLVED** (Turner paired sheets sd05/sd09
      PAO1 blocks parsed). Reviewed in `L03_DRAFT_REVIEW_AUDIT.md`; needs human
      review + promotion (Lee per-medium rows still NEEDS_REVIEW). Varadarajan
      excluded (Lee-derivative); Poulsen/Basta not parsed (orthology-blocked).
- [ ] Validated PAO1↔PA14 orthology merged; coverage + ambiguity reported (B-MAP-01;
      see `ORTHOLOGY_READINESS_AUDIT.md` — none present, blocks Poulsen + Basta)
- [ ] Per-study media reconstructed and cited; model feasible per condition (C-01)
- [ ] Per-condition predictions generated at multiple thresholds (S-01)
- [ ] Only then: confusion matrix / precision / recall / specificity / F1 / MCC,
      per condition × phenotype class, with coverage caveats (V-01)

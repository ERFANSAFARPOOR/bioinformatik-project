# NEGATIVE_UNIVERSE_SOURCE_AUDIT.md

**Date:** 2026-08-01  
**Branch:** `develop`  
**Scope:** Experimental negative universe for Lee2015 MOPS-pyruvate / Minimal Tn-seq validation of iMO1056  
**Status:** Evidence audit complete — human-approved as **D-21**
(`APPROVED_FOR_PRIMARY_BINARY_VALIDATION`, 2026-08-01). READY + frozen primary
binary artifacts written; full V-01 metrics **not yet executed**.

---

## Scientific question

Can we defensibly replace `DEFER_NEGATIVE_UNIVERSE` with a reproducible experimental binary validation universe (positive / negative / ambiguous) suitable for a full confusion matrix for MOPS-pyruvate, without fabricating negatives from absences in Lee Dataset S1 or from the complement of model positives?

---

## Evidence hierarchy used

1. **Tier 1:** Repository policy + Lee2015 paper/SI + Dataset S1 (`pnas.1422186112.sd01.xlsx`)
2. **Tier 2:** Varadarajan et al. 2020 reanalysis of the same Tn-seq (SRP052838) — DS1 + DS4 + SI
3. **Tier 3:** Raw SRA FASTQ reanalysis — **not performed** (not required given Tier 2)

---

## Phase 0 — Repository orientation (current state)

| Item | State |
|---|---|
| Lee2015 MOPS positives | **APPROVED** (D-20): 437 standard `PAxxxx`, `Min sum (of 3) >= 2` |
| Blank Min sum | Missing evidence ≠ 0 ≠ non-essential |
| Negative universe | **Deferred** (B-SCI-01 / V-01 gate) |
| Full V-01 metrics | **Forbidden** until negatives reviewed |
| SRA SRP052838 | Inventory only; no FASTQ download |
| Varadarajan2020 | Citation verified; previously “mapping resource only / do not double-count as independent Lee evidence” |

**Internal summary**

1. **Current Lee2015 policy:** positives-only promotion for MOPS-pyruvate; no automatic negatives.
2. **Current positive definition:** `Min sum (of 3) ∈ {2,3}` → 438 raw / 437 standard `PAxxxx` (+ `PA0728.1` unmapped).
3. **Current negative-universe blocker:** Dataset S1 is an essentials union; absence ≠ non-essential.
4. **Current V-01 state:** positive-overlap-only allowed; specificity/precision/F1/MCC/confusion matrix blocked.

**Prompt vs repo:** Prompt uses the label `DEFER_NEGATIVE_UNIVERSE`; repo encodes the same gate in D-20 / B-SCI-01 without that exact token. No scientific conflict.

---

## Sources inspected

| Source | Path / locator | Role |
|---|---|---|
| Lee Dataset S1 | `data/raw/literature/lee2015/pnas.1422186112.sd01.xlsx` | Tier 1 positives table |
| Lee SI | `data/raw/literature/lee2015/Supporting Information.pdf` | Methods / consensus rule |
| Lee human review | `project_management/audit/LEE2015_PER_MEDIUM_REVIEW.md` | Approved positives |
| Varadarajan DS1 | `data/raw/literature/varadarajan2020/Supplementary Dataset 1 (MPAO1).xlsx` | MPAO1 CDS master + PAO1 map |
| Varadarajan DS4 | `…/Supplementary Dataset 4 (MPAO1).xlsx` | Per-library essential calls |
| Varadarajan SI | `…/Supplementary Information (MPAO1).pdf` | Remap methods + DS4 caption |
| Citation check | `project_management/audit/VARADARAJAN2020_CITATION_CHECK.md` | DOI 10.1038/s41522-020-00154-8 |
| Model knockout | `src/gene_essentiality.py` | Evaluable = all `model.genes` (1054) |
| Predictions | `results/essentiality/gene_essentiality_mops_pyruvate_lee2015.csv` | 1054 genes |
| SRA inventory | `data/raw/literature/lee2015/sra/` | Metadata only |

---

## Dataset S1 conclusion — **insufficient for negatives (option B)**

### Sheet evidence

- Sheets: `General essential genes`, `All essential genes`, `Essential noncoding regions `
- Title row of `All essential genes` (verbatim intent):  
  **“All genes essential on LB, minimal-pyruvate or sputum agar.”**
- Rows: **551** genes with `PA number` (union of genes essential in ≥1 primary condition)

### `Min sum (of 3)` counts (reconfirmed)

| Value | Count |
|---|---|
| 3 | 365 |
| 2 | 73 |
| ≥2 | 438 |
| 1 | 24 |
| 0 | 85 |
| blank | 4 |

Standard `^PA\d{4}$`: 549; non-standard: `PA0728.1`, `PA0826.1`.

### Why Min=0 cannot be a genome-wide negative universe

1. The sheet is an **essentials union / subset**, not the full assayed CDS set (~5.5–5.8k).
2. Among **all 85** genes with `Min sum = 0`, **every gene** is essential in ≥1 other medium column (LB / Sputum / BHI / 0.1×LB / Serum).  
   → Min=0 here means “essential somewhere else, not on Min,” not “genome-wide non-essential.”
3. ~5,000+ CDS never appear in the sheet at all; their absence is uninformative under D-20.

**Verdict:** Dataset S1 alone → **cannot** unlock a full confusion matrix.

---

## Varadarajan2020 conclusion — Tier 2 source for a consistent universe

### What the reanalysis is

Varadarajan SI (Supplementary Figure 2 / Data 4 context), paraphrased with location:

> Using the scripts released by Lee and colleagues, Tn-seq data were re-mapped to the complete MPAO1 genome and compared with the published sets (577 “all essential”; 312 “general essential”). Overall, **1117 genes were identified as essential in at least one Tn-seq library**; thereof 136 MPAO1-unique.  
> **Supplementary Data 4:** summary table of those **1117** genes.

This is **not an independent screen**; it is a **published remapping of Lee2015 SRP052838** onto MPAO1. For negative-universe purposes that is a feature: positives and negatives can come from **one pipeline**.

### Master universe (DS1 `MPAO1_CDS`)

| Metric | Count |
|---|---|
| Total MPAO1 CDS rows | **5799** |
| Unique `locus_tag` | 5799 (no duplicates) |
| `best_hit protein` non-null | 5554 |
| Rows with ≥1 standard `PAxxxx` | 5493 |
| Unique-std single `PAxxxx` maps | 5474 |
| One-to-many std multi-hit strings | 19 |
| Nonstandard-only IDs (e.g. `PA0032a`, multi-locus strings) | 61 |
| No PAO1 homolog / unique | 245 |

**Mapping column:** use `best_hit protein` (locus tags), **not** `PAO1_gene_name` (gene symbols).

### DS4 encoding

- Sheet `essentialGenes_MPAO1`: **1117** rows = genes essential in ≥1 of 16 libraries.
- Per-library cells: **`1` or blank only** (no explicit `0`).
- Per Minimal library essential calls (among DS4 rows):  
  Minimal-1 **410**, Minimal-2 **351**, Minimal-3 **427**.
- All 1117 DS4 loci are present in DS1.

### DS1 Legend (essentiality columns)

- `essential?`: TRUE if called essential in remapping (**577** “all essential” subset).
- `essential_in #samples`: count among 16 samples (filled for that 577 set).
- Blank/`NaN` outside that set: not flagged in the 577 column — **not** a per-Minimal matrix in DS1.

Lee et al. SI Sequence Data Analysis (supporting inference of genome-wide scoring):

> Hit and read densities were calculated for a **total of 5,573 annotated coding sequences**. Genes with zero values were considered essential; remaining values log2-transformed; P=0.001 cutoff…

→ Lee’s algorithm scores **all annotated CDS** per library; the published essential tables are the **positive call lists**.

---

## Phase 4 — Does absence mean non-essential?

| Category | Operational definition in this audit |
|---|---|
| Experimentally assayed (Lee method) | All annotated CDS scored for hits/reads per library |
| Successfully mapped/evaluable for model | Unique std `PAxxxx` ∩ iMO1056 genes |
| Essential in Minimal-X | DS4 cell `Minimal-X == 1` |
| Not called essential in Minimal-X | Blank in DS4 Minimal-X **or** locus absent from DS4 |
| Missing/filtered/ambiguous | Nonstandard maps; one-to-many; MPAO1-unique; `minimal_sum==1`; mapping conflicts |

**Inference adopted (candidate):**  
For every DS1 CDS, `minimal_k = 1` iff DS4 marks essential in that library; else `0` meaning **not called essential** (not “blank converted to experimental zero without documentation” — blank is the published encoding of non-call in an essentials-only matrix, closed against the complete CDS master).

**Limits (must remain visible):**

- No separate published “non-essential” table or per-gene coverage mask.
- Short genes / 5–90% end trimming / repetitive regions follow Lee’s scripts; edge cases can inflate false essentials rather than create silent non-assayed negatives.
- Remap reference is MPAO1 (5799 CDS), not PAO1-UW (5573).

---

## Candidate experimental label policy (`CANDIDATE_FOR_HUMAN_REVIEW`)

On the three Minimal libraries (Lee MOPS-pyruvate pools):

| `minimal_sum` | Candidate label |
|---|---|
| 2 or 3 | **POSITIVE** |
| 1 | **AMBIGUOUS** (exclude from primary binary) |
| 0 | **NEGATIVE** (not called essential in any Minimal library; DS1 master membership required) |

**Pipeline rule:** primary confusion matrix must use **Varadarajan-remap positives AND negatives together**.  
Do **not** mix D-20 Lee-original positives with Varadarajan negatives.

Existing Lee READY positives remain a **separate evidence layer** (diagnostic overlap only).

---

## Mapping + model-evaluable universe

Project knockout policy (`src/gene_essentiality.py`): evaluates **all `model.genes`** via `single_gene_deletion` — not GPR-filtered separately. Prediction file has **1054** genes (= model gene count).

| Universe | n | POS | NEG | AMB |
|---|---:|---:|---:|---:|
| MPAO1 CDS (DS1) | 5799 | 415 | 5312 | 72 |
| Unique-std PAO1 collapsed | 5471 | 405 | 5017 | 49 |
| ∩ iMO1056 | **1043** | **214** | **811** | **18** |

11 model genes lack a unique-std DS1 map (e.g. phz/phz-like multi-hit IDs `PA1901–04` / `PA4212–15`, plus `PA1122`, `PA1685`, `PA3164`) → excluded from unique-std join.

---

## Original Lee positives vs Varadarajan Minimal consensus (diagnostic)

| Set | Count |
|---|---:|
| Lee READY positives | 437 |
| Varadarajan unique-std POSITIVE | 405 |
| Intersection | **399** |
| Lee-only | 38 |
| Var-only | 6 |
| Lee recovery | **91.3%** |
| Jaccard | **0.901** |

Lee-only breakdown under Varadarajan labels: **26 AMBIGUOUS** (`sum=1`), **11 NEGATIVE** (`sum=0`), **1 absent from unique-std map** (`PA4685`).  
Var-only POSITIVES: `PA1804`, `PA4053`, `PA4529`, `PA4568`, `PA4741`, `PA4935`.

Disagreement is expected (MPAO1 remap, annotation, threshold edge cases) and is **not** treated as an automatic error.

---

## Machine-readable outputs

- Gene-level candidate: `data/processed/literature/gene_level/varadarajan2020_lee2015_minimal_gene_labels_CANDIDATE.csv`  
  (`review_status=CANDIDATE_FOR_HUMAN_REVIEW` only — **not READY**)
- Counts: `project_management/audit/negative_universe_lee2015/NEGATIVE_UNIVERSE_COUNTS.{json,csv}`
- Positive comparison: `…/lee_vs_varadarajan_positive_comparison.json`
- Proposed decision: `…/NEGATIVE_UNIVERSE_PROPOSED_DECISION.md`
- Rebuild script: `scripts/build_varadarajan2020_minimal_negative_universe_candidate.py`

**Unchanged:** Lee READY positive file; raw supplements; DECISIONS.md; no metrics computed; no FASTQ download; no commit/push.

---

## Final outcome

### **OUTCOME A — NEGATIVE UNIVERSE RESOLVED** (as a scientific *candidate*)

Tier 1 alone fails. Tier 2 supplies:

- a genome-scale CDS master (DS1),
- per-Minimal essential calls (DS4),
- Methods support that Lee’s scripts score all annotated CDS,
- a consistent positive/negative/ambiguous policy without mixing pipelines.

**Human review is still required** before promoting labels or unlocking primary MCC/F1/specificity. Until then, keep operational gate equivalent to `DEFER_NEGATIVE_UNIVERSE` in force for metrics.

---

## Limitations

1. Complement-of-essential-call inference (no published non-essential spreadsheet).
2. Derivative of Lee raw data (correct for consistency; wrong if treated as independent replication).
3. MPAO1↔PAO1 mapping edge cases exclude some model genes.
4. ~9% Lee-positive disagreement (mostly sum=1 demotions).
5. Metrics remain forbidden until D-21 human approval.

---

## Safest next action

**Human-review and approve/reject the proposed D-21 candidate policy** in `NEGATIVE_UNIVERSE_PROPOSED_DECISION.md` (do not compute full metrics and do not download Minimal FASTQ until that decision is recorded).

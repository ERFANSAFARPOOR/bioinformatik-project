# NEGATIVE_UNIVERSE_PROPOSED_DECISION.md

**Proposed ID:** D-21  
**Date drafted:** 2026-08-01  
**Status:** **APPROVED_FOR_PRIMARY_BINARY_VALIDATION** (human review 2026-08-01) —
recorded in root `DECISIONS.md` as D-21; READY + frozen primary binary artifacts
written; full V-01 metrics **not yet executed**.  
**Depends on:** D-20 (Lee2015 MOPS positives remain a separate evidence layer)  
**Audit:** `NEGATIVE_UNIVERSE_SOURCE_AUDIT.md`  
**Promotion:** `D21_PROMOTION_INTEGRITY_REPORT.json`

---

## Proposed decision title

Lee2015 MOPS-pyruvate / Minimal experimental binary universe from Varadarajan2020 remapping (candidate)

---

## Source

- **Primary analysis for this universe:** Varadarajan et al. 2020 (DOI `10.1038/s41522-020-00154-8`) remapping of Lee et al. 2015 Tn-seq (`SRP052838`) onto the complete MPAO1 genome using Lee’s released scripts.
- **Master CDS table:** Supplementary Dataset 1 sheet `MPAO1_CDS` (5799 CDS).
- **Per-library essential calls:** Supplementary Dataset 4 sheet `essentialGenes_MPAO1` (1117 genes essential in ≥1 of 16 libraries).
- **Condition:** Minimal-1 / Minimal-2 / Minimal-3 (= Lee MOPS-pyruvate pools).
- **Not an independent biological screen** — same underlying experiment as Lee2015; different reference/annotation/remap.

---

## Universe

1. Start from **all DS1 MPAO1 CDS**.
2. Join DS4 Minimal-1/2/3 calls (`1` = called essential; blank/absent = **not called essential** in that library).
3. Map to PAO1 via DS1 `best_hit protein`.
4. For iMO1056 validation, restrict to genes with:
   - `mapping_status = unique_std_PAO1` (`^PA\d{4}$`, single hit), and
   - `in_imo1056 = True` (present among model genes / knockout results).
5. Exclude AMBIGUOUS labels from the primary binary matrix.

Approximate model-overlap sizes from the candidate build (reproducible script):

- n = 1043 unique-std ∩ model  
- POSITIVE 214 / NEGATIVE 811 / AMBIGUOUS 18  

---

## Positive definition

`minimal_sum = Minimal-1 + Minimal-2 + Minimal-3` where each term is 1 if DS4 marks essential, else 0.

- **POSITIVE:** `minimal_sum ∈ {2, 3}`  
  (mirrors Lee SI consensus: ≥2 of 3 MOPS-pyruvate pools)

---

## Negative definition

- **NEGATIVE:** `minimal_sum = 0` **and** locus is in the DS1 CDS master  
  → not called essential in any of the three Minimal libraries under the Varadarajan remap.

This is **not**:

- absence from Lee Dataset S1,
- blank Min sum in Dataset S1 treated as zero,
- complement of model-predicted essentials,
- Lee-original positives paired with Varadarajan negatives.

---

## Ambiguous definition

- **AMBIGUOUS:** `minimal_sum = 1`  
  → exclude from primary binary confusion matrix; may be used only in sensitivity analyses if later authorized.

Also treat as non-primary / excluded:

- nonstandard or multi-hit PAO1 maps,
- MPAO1-unique genes without PAO1 homolog,
- conflicting labels if multiple MPAO1 loci collapse to one PAO1 ID (none observed in the candidate build).

---

## Mapping policy

- Use DS1 `best_hit protein` as the MPAO1→PAO1 map.
- Retain one-to-many / missing / nonstandard IDs explicitly (`mapping_status`).
- Primary metrics join: **unique standard `PAxxxx` only**.
- Do not auto-rename nonstandard IDs (e.g. `PAxxxxa`) without a separate authoritative annotation decision.

---

## Model-evaluable universe

- iMO1056 gene deletion evaluates **all model genes** (`src/gene_essentiality.py` → `single_gene_deletion(model.genes)`).
- Current MOPS-pyruvate prediction table: **1054** genes.
- No extra “must have GPR” filter beyond membership in `model.genes`.
- Genes in model but lacking unique-std experimental map are **out of the experimental join**, not relabeled.

---

## Permitted metrics (only after this proposal is approved into DECISIONS.md)

On the **Varadarajan-consistent** binary set (POSITIVE ∪ NEGATIVE; AMBIGUOUS excluded), condition-matched to `mops_pyruvate_lee2015` predictions:

- confusion matrix counts (TP/FP/TN/FN)
- precision, recall/sensitivity, specificity, F1, MCC
- coverage diagnostics (mapped / unmapped / ambiguous / excluded)

---

## Forbidden interpretations (remain forbidden until approval; some remain forever)

1. Do **not** compute primary full metrics from Lee Dataset S1 Min=0 or from absence-from-Lee-essential-list.
2. Do **not** mix D-20 Lee-original positives with Varadarajan negatives in one primary matrix.
3. Do **not** treat Varadarajan as an independent biological replicate of Lee.
4. Do **not** convert blanks to zeros without the DS4+DS1 encoding rationale above.
5. Do **not** mark candidate files READY without human sign-off.
6. D-20 Lee READY positives remain valid for **positive-overlap-only** analyses as a separate layer.

---

## Caveats

- Negative calls are inferred as the CDS-master complement of Minimal essential calls from a published essentials-union matrix (DS4), justified by Lee’s genome-wide scoring method + Varadarajan’s use of Lee’s scripts — **not** by a separately published non-essential spreadsheet.
- Remap/annotation differences cause ~9% disagreement vs Lee READY positives (mostly demotion to sum=1).
- MPAO1-unique essentials cannot validate the PAO1 model.
- Candidate artifact:  
  `data/processed/literature/gene_level/varadarajan2020_lee2015_minimal_gene_labels_CANDIDATE.csv`  
  (`review_status=CANDIDATE_FOR_HUMAN_REVIEW`).

---

## Human decision

**APPROVED** as D-21 (`APPROVED_FOR_PRIMARY_BINARY_VALIDATION`) on 2026-08-01.
Primary binary labels promoted/frozen; V-01 confusion-matrix metrics remain a
**separate next step** (`READY_FOR_V01_BINARY_METRICS`). Tier-3 Minimal FASTQ
reanalysis was not required for this approval.

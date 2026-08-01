# V-01 Error Structure Audit — MOPS-pyruvate (diagnostic only)

**Status:** `V01_ERROR_ANALYSIS_COMPLETED_PENDING_HUMAN_REVIEW`

## Scope and hard constraints

- Diagnostic analysis of frozen V-01 FP/FN sets only.
- **No** model, GPR, reaction, medium, biomass, or threshold changes.
- **No** gap-filling, metric retuning, or gene exclusion.
- Categories are **association-based** from model structure; not causal claims.
- iMO1056 reaction `subsystem` fields are empty; pathway groupings use 
  deterministic reaction-name keyword clusters (descriptive counts only).

## Phase 0 — frozen integrity

| Cell | Count |
|---|---|
| TP | 116 |
| FN | 98 |
| TN | 764 |
| FP | 47 |
| n | 1025 |

- Model SHA-256: `0868a5ebb41ebb4967c3c182e686eca7552af9255cba5a6d130cf114d1212ead`
- Medium: `mops_pyruvate_lee2015` · threshold: `0.01` · objective: `PA_Biomass6_DM`
- WT growth (V-01 metrics): 0.40533903063568605

## FN overview (n=98)

Experiment = essential; model = non-essential.

| diagnostic_category | count |
|---|---|
| FN_ALTERNATIVE_PATHWAY | 26 |
| FN_ISOENZYME_REDUNDANCY | 31 |
| FN_REACTION_INACTIVE | 41 |

### FN threshold-distance bins (DIAGNOSTIC ONLY)

| bin | count |
|---|---|
| DIAG_EXTREMELY_FAR_ratio_ge_0.99 | 87 |
| DIAG_FAR_[0.50,0.99) | 6 |
| DIAG_MODERATELY_FAR_[0.05,0.50) | 5 |

### FN pathway-keyword clusters (descriptive)

| cluster | count |
|---|---|
| translation_trna | 18 |
| amino_acid_biosynthesis | 18 |
| other_or_unclassified | 17 |
| nucleotide_metabolism | 14 |
| energy_metabolism | 12 |
| cofactor_biosynthesis | 9 |
| central_carbon_metabolism | 8 |
| lipid_lps_metabolism | 2 |

## FP overview (n=47)

Experiment = negative; model = essential.

| diagnostic_category | count |
|---|---|
| FP_BIOMASS_FORMULATION | 7 |
| FP_GPR_STRUCTURE | 9 |
| FP_MISSING_ALTERNATIVE_PATHWAY | 16 |
| FP_MISSING_ISOENZYME | 9 |
| FP_MISSING_TRANSPORT | 5 |
| FP_UNRESOLVED | 1 |

### FP threshold-distance bins (DIAGNOSTIC ONLY)

| bin | count |
|---|---|
| DIAG_EXTREMELY_FAR_abs_ratio_lt_1e-6 | 47 |

### FP pathway-keyword clusters (descriptive)

| cluster | count |
|---|---|
| other_or_unclassified | 13 |
| nucleotide_metabolism | 10 |
| amino_acid_biosynthesis | 8 |
| lipid_lps_metabolism | 6 |
| transport | 5 |
| cofactor_biosynthesis | 4 |
| central_carbon_metabolism | 1 |

## Threshold-distance finding

Almost all errors are **far from** the fixed 0.01 cutoff: FN ratios are typically ≈1 (growth retained), and FP ratios are ≈0 (lethal KO). These are structural / scope disagreements, not classification-boundary artifacts. No alternative threshold was applied.

## High-priority manual-review shortlist (Priority 1)

Safest actions are inspection-only. **No automatic model edits.**

### PA0280 (FP) — `FP_MISSING_TRANSPORT` [high]

- Experimental: `NEGATIVE_0_OF_3_NOT_CALLED_ESSENTIAL` (minimal_sum=0)
- Model prediction: `MODEL_POSITIVE` · KO/WT=1.063644418923784e-17
- Reactions: `SULabc`
- GPR: `SULabc:PA0280 and PA1493 and PA0282 and PA0281 and PA0283`
- Suspected mechanism (associative): FP_MISSING_TRANSPORT
- Safest review action: Inspect whether alternate sulfate/nutrient uptake exists in PAO1 literature; do not add transporters without a sourced decision.
- Notes: Transport/exchange-associated reaction(s); model requires them for growth under locked MOPS-pyruvate exchanges. Multi-subunit ABC GPR: experimental viability may reflect alternate uptake not represented (association only).

### PA0281 (FP) — `FP_MISSING_TRANSPORT` [high]

- Experimental: `NEGATIVE_0_OF_3_NOT_CALLED_ESSENTIAL` (minimal_sum=0)
- Model prediction: `MODEL_POSITIVE` · KO/WT=3.1348697706274367e-15
- Reactions: `SULabc`
- GPR: `SULabc:PA0280 and PA1493 and PA0282 and PA0281 and PA0283`
- Suspected mechanism (associative): FP_MISSING_TRANSPORT
- Safest review action: Inspect whether alternate sulfate/nutrient uptake exists in PAO1 literature; do not add transporters without a sourced decision.
- Notes: Transport/exchange-associated reaction(s); model requires them for growth under locked MOPS-pyruvate exchanges. Multi-subunit ABC GPR: experimental viability may reflect alternate uptake not represented (association only).

### PA0282 (FP) — `FP_MISSING_TRANSPORT` [high]

- Experimental: `NEGATIVE_0_OF_3_NOT_CALLED_ESSENTIAL` (minimal_sum=0)
- Model prediction: `MODEL_POSITIVE` · KO/WT=6.422374676369604e-15
- Reactions: `SULabc`
- GPR: `SULabc:PA0280 and PA1493 and PA0282 and PA0281 and PA0283`
- Suspected mechanism (associative): FP_MISSING_TRANSPORT
- Safest review action: Inspect whether alternate sulfate/nutrient uptake exists in PAO1 literature; do not add transporters without a sourced decision.
- Notes: Transport/exchange-associated reaction(s); model requires them for growth under locked MOPS-pyruvate exchanges. Multi-subunit ABC GPR: experimental viability may reflect alternate uptake not represented (association only).

### PA0283 (FP) — `FP_MISSING_TRANSPORT` [high]

- Experimental: `NEGATIVE_0_OF_3_NOT_CALLED_ESSENTIAL` (minimal_sum=0)
- Model prediction: `MODEL_POSITIVE` · KO/WT=3.308899723457974e-32
- Reactions: `SULabc`
- GPR: `SULabc:PA0280 and PA1493 and PA0282 and PA0281 and PA0283`
- Suspected mechanism (associative): FP_MISSING_TRANSPORT
- Safest review action: Inspect whether alternate sulfate/nutrient uptake exists in PAO1 literature; do not add transporters without a sourced decision.
- Notes: Transport/exchange-associated reaction(s); model requires them for growth under locked MOPS-pyruvate exchanges. Multi-subunit ABC GPR: experimental viability may reflect alternate uptake not represented (association only).

### PA1493 (FP) — `FP_MISSING_TRANSPORT` [high]

- Experimental: `NEGATIVE_0_OF_3_NOT_CALLED_ESSENTIAL` (minimal_sum=0)
- Model prediction: `MODEL_POSITIVE` · KO/WT=6.46826244404477e-16
- Reactions: `SULabc`
- GPR: `SULabc:PA0280 and PA1493 and PA0282 and PA0281 and PA0283`
- Suspected mechanism (associative): FP_MISSING_TRANSPORT
- Safest review action: Inspect whether alternate sulfate/nutrient uptake exists in PAO1 literature; do not add transporters without a sourced decision.
- Notes: Transport/exchange-associated reaction(s); model requires them for growth under locked MOPS-pyruvate exchanges. Multi-subunit ABC GPR: experimental viability may reflect alternate uptake not represented (association only).

### PA0609 (FN) — `FN_ISOENZYME_REDUNDANCY` [high]

- Experimental: `POSITIVE_CONSENSUS_ESSENTIAL` (minimal_sum=3)
- Model prediction: `MODEL_NEGATIVE` · KO/WT=1.0000000020863071
- Reactions: `ANS1`
- GPR: `ANS1:(PA1001 and PA1002) or (PA0609 and PA0649)`
- Suspected mechanism (associative): FN_ISOENZYME_REDUNDANCY
- Safest review action: Manually inspect OR-GPRs and ask whether isozyme annotation is biologically justified; do not auto-edit GPRs.
- Notes: At least one associated reaction has OR-logic GPR and remains True after single-gene KO (cobra.gpr.eval); isoenzyme/redundancy compatible with retained growth.

### PA0944 (FN) — `FN_ISOENZYME_REDUNDANCY` [high]

- Experimental: `POSITIVE_CONSENSUS_ESSENTIAL` (minimal_sum=2)
- Model prediction: `MODEL_NEGATIVE` · KO/WT=1.0000000020863926
- Reactions: `GARFTi`
- GPR: `GARFTi:PA0944 or (PA3751 or PA0836)`
- Suspected mechanism (associative): FN_ISOENZYME_REDUNDANCY
- Safest review action: Manually inspect OR-GPRs and ask whether isozyme annotation is biologically justified; do not auto-edit GPRs.
- Notes: At least one associated reaction has OR-logic GPR and remains True after single-gene KO (cobra.gpr.eval); isoenzyme/redundancy compatible with retained growth.

### PA1010 (FN) — `FN_ISOENZYME_REDUNDANCY` [high]

- Experimental: `POSITIVE_CONSENSUS_ESSENTIAL` (minimal_sum=3)
- Model prediction: `MODEL_NEGATIVE` · KO/WT=1.000000002086304
- Reactions: `DHDPS`
- GPR: `DHDPS:(PA4188 or PA1254 or PA0223) or PA1010`
- Suspected mechanism (associative): FN_ISOENZYME_REDUNDANCY
- Safest review action: Manually inspect OR-GPRs and ask whether isozyme annotation is biologically justified; do not auto-edit GPRs.
- Notes: At least one associated reaction has OR-logic GPR and remains True after single-gene KO (cobra.gpr.eval); isoenzyme/redundancy compatible with retained growth.

### PA1580 (FN) — `FN_ISOENZYME_REDUNDANCY` [high]

- Experimental: `POSITIVE_CONSENSUS_ESSENTIAL` (minimal_sum=2)
- Model prediction: `MODEL_NEGATIVE` · KO/WT=1.0000000020862798
- Reactions: `CS`
- GPR: `CS:PA0795 or PA1580`
- Suspected mechanism (associative): FN_ISOENZYME_REDUNDANCY
- Safest review action: Manually inspect OR-GPRs and ask whether isozyme annotation is biologically justified; do not auto-edit GPRs.
- Notes: At least one associated reaction has OR-logic GPR and remains True after single-gene KO (cobra.gpr.eval); isoenzyme/redundancy compatible with retained growth.

### PA1587 (FN) — `FN_ISOENZYME_REDUNDANCY` [high]

- Experimental: `POSITIVE_CONSENSUS_ESSENTIAL` (minimal_sum=3)
- Model prediction: `MODEL_NEGATIVE` · KO/WT=1.0000000020863524
- Reactions: `GLYCL;PDHe3c`
- GPR: `GLYCL:(PA2446 and PA2445 and PA2442) or (PA5214 and PA5213 and PA5215) or (PA4829 and PA1587 and PA2250) || PDHe3c:PA1587`
- Suspected mechanism (associative): FN_ISOENZYME_REDUNDANCY
- Safest review action: Manually inspect OR-GPRs and ask whether isozyme annotation is biologically justified; do not auto-edit GPRs.
- Notes: At least one associated reaction has OR-logic GPR and remains True after single-gene KO (cobra.gpr.eval); isoenzyme/redundancy compatible with retained growth.

### PA1610 (FN) — `FN_ISOENZYME_REDUNDANCY` [high]

- Experimental: `POSITIVE_CONSENSUS_ESSENTIAL` (minimal_sum=2)
- Model prediction: `MODEL_NEGATIVE` · KO/WT=1.0000000020862798
- Reactions: `HBUHL1;HDDHL5;HDEHL4;HDER4r;HHDHL7;HHYHL2;HOCHL3;HODHL8;HTDHL6`
- GPR: `HBUHL1:PA1610 or PA3645 || HDDHL5:PA3645 or PA1610 || HDEHL4:PA3645 or PA1610 || HDER4r:PA1610 || HHDHL7:PA1610 or PA3645 || HHYHL2:PA1610 or PA3645 || HOCHL3:PA1610 or PA3645 || HODHL8:PA1610 or PA3645 || HTDHL6:PA1610 or PA3645`
- Suspected mechanism (associative): FN_ISOENZYME_REDUNDANCY
- Safest review action: Manually inspect OR-GPRs and ask whether isozyme annotation is biologically justified; do not auto-edit GPRs.
- Notes: At least one associated reaction has OR-logic GPR and remains True after single-gene KO (cobra.gpr.eval); isoenzyme/redundancy compatible with retained growth.

### PA1787 (FN) — `FN_ISOENZYME_REDUNDANCY` [high]

- Experimental: `POSITIVE_CONSENSUS_ESSENTIAL` (minimal_sum=2)
- Model prediction: `MODEL_NEGATIVE` · KO/WT=1.0000000020863062
- Reactions: `ACONT`
- GPR: `ACONT:PA1787 or PA1562`
- Suspected mechanism (associative): FN_ISOENZYME_REDUNDANCY
- Safest review action: Manually inspect OR-GPRs and ask whether isozyme annotation is biologically justified; do not auto-edit GPRs.
- Notes: At least one associated reaction has OR-logic GPR and remains True after single-gene KO (cobra.gpr.eval); isoenzyme/redundancy compatible with retained growth.

### PA3001 (FN) — `FN_ISOENZYME_REDUNDANCY` [high]

- Experimental: `POSITIVE_CONSENSUS_ESSENTIAL` (minimal_sum=2)
- Model prediction: `MODEL_NEGATIVE` · KO/WT=1.0000000020863238
- Reactions: `GAPDy1`
- GPR: `GAPDy1:PA2323 or PA3001`
- Suspected mechanism (associative): FN_ISOENZYME_REDUNDANCY
- Safest review action: Manually inspect OR-GPRs and ask whether isozyme annotation is biologically justified; do not auto-edit GPRs.
- Notes: At least one associated reaction has OR-logic GPR and remains True after single-gene KO (cobra.gpr.eval); isoenzyme/redundancy compatible with retained growth.

### PA3117 (FN) — `FN_ISOENZYME_REDUNDANCY` [high]

- Experimental: `POSITIVE_CONSENSUS_ESSENTIAL` (minimal_sum=2)
- Model prediction: `MODEL_NEGATIVE` · KO/WT=1.0000000020863198
- Reactions: `ASAD`
- GPR: `ASAD:PA3116 or PA3117`
- Suspected mechanism (associative): FN_ISOENZYME_REDUNDANCY
- Safest review action: Manually inspect OR-GPRs and ask whether isozyme annotation is biologically justified; do not auto-edit GPRs.
- Notes: At least one associated reaction has OR-logic GPR and remains True after single-gene KO (cobra.gpr.eval); isoenzyme/redundancy compatible with retained growth.

### PA3139 (FN) — `FN_ISOENZYME_REDUNDANCY` [high]

- Experimental: `POSITIVE_CONSENSUS_ESSENTIAL` (minimal_sum=3)
- Model prediction: `MODEL_NEGATIVE` · KO/WT=1.0000000020863156
- Reactions: `LEUTAi;PHETA1;TYRTA2;UNK4;UNK6;UNK7`
- GPR: `LEUTAi:PA0870 or PA3139 or PA5013 || PHETA1:PA0870 or PA3139 || TYRTA2:PA0870 or PA3139 || UNK4:PA3139 || UNK6:PA3139 || UNK7:PA3139`
- Suspected mechanism (associative): FN_ISOENZYME_REDUNDANCY
- Safest review action: Manually inspect OR-GPRs and ask whether isozyme annotation is biologically justified; do not auto-edit GPRs.
- Notes: At least one associated reaction has OR-logic GPR and remains True after single-gene KO (cobra.gpr.eval); isoenzyme/redundancy compatible with retained growth.

### PA3537 (FN) — `FN_ISOENZYME_REDUNDANCY` [high]

- Experimental: `POSITIVE_CONSENSUS_ESSENTIAL` (minimal_sum=3)
- Model prediction: `MODEL_NEGATIVE` · KO/WT=1.0000000020863071
- Reactions: `OCBT`
- GPR: `OCBT:PA3537 or PA5172`
- Suspected mechanism (associative): FN_ISOENZYME_REDUNDANCY
- Safest review action: Manually inspect OR-GPRs and ask whether isozyme annotation is biologically justified; do not auto-edit GPRs.
- Notes: At least one associated reaction has OR-logic GPR and remains True after single-gene KO (cobra.gpr.eval); isoenzyme/redundancy compatible with retained growth.

### PA3645 (FN) — `FN_ISOENZYME_REDUNDANCY` [high]

- Experimental: `POSITIVE_CONSENSUS_ESSENTIAL` (minimal_sum=3)
- Model prediction: `MODEL_NEGATIVE` · KO/WT=1.000000002086305
- Reactions: `HBUHL1;HDDHL5;HDEHL4;HHDHL7;HHYHL2;HOCHL3;HODHL8;HTDHL6`
- GPR: `HBUHL1:PA1610 or PA3645 || HDDHL5:PA3645 or PA1610 || HDEHL4:PA3645 or PA1610 || HHDHL7:PA1610 or PA3645 || HHYHL2:PA1610 or PA3645 || HOCHL3:PA1610 or PA3645 || HODHL8:PA1610 or PA3645 || HTDHL6:PA1610 or PA3645`
- Suspected mechanism (associative): FN_ISOENZYME_REDUNDANCY
- Safest review action: Manually inspect OR-GPRs and ask whether isozyme annotation is biologically justified; do not auto-edit GPRs.
- Notes: At least one associated reaction has OR-logic GPR and remains True after single-gene KO (cobra.gpr.eval); isoenzyme/redundancy compatible with retained growth.

### PA3769 (FN) — `FN_ISOENZYME_REDUNDANCY` [high]

- Experimental: `POSITIVE_CONSENSUS_ESSENTIAL` (minimal_sum=2)
- Model prediction: `MODEL_NEGATIVE` · KO/WT=1.0000000020863142
- Reactions: `GMPS2`
- GPR: `GMPS2:PA1742 or PA3769`
- Suspected mechanism (associative): FN_ISOENZYME_REDUNDANCY
- Safest review action: Manually inspect OR-GPRs and ask whether isozyme annotation is biologically justified; do not auto-edit GPRs.
- Notes: At least one associated reaction has OR-logic GPR and remains True after single-gene KO (cobra.gpr.eval); isoenzyme/redundancy compatible with retained growth.

### PA3977 (FN) — `FN_ISOENZYME_REDUNDANCY` [high]

- Experimental: `POSITIVE_CONSENSUS_ESSENTIAL` (minimal_sum=2)
- Model prediction: `MODEL_NEGATIVE` · KO/WT=1.0000000020921251
- Reactions: `G1SATi`
- GPR: `G1SATi:(PA4088 or PA5523) or PA3977`
- Suspected mechanism (associative): FN_ISOENZYME_REDUNDANCY
- Safest review action: Manually inspect OR-GPRs and ask whether isozyme annotation is biologically justified; do not auto-edit GPRs.
- Notes: At least one associated reaction has OR-logic GPR and remains True after single-gene KO (cobra.gpr.eval); isoenzyme/redundancy compatible with retained growth.

### PA4047 (FN) — `FN_ISOENZYME_REDUNDANCY` [high]

- Experimental: `POSITIVE_CONSENSUS_ESSENTIAL` (minimal_sum=2)
- Model prediction: `MODEL_NEGATIVE` · KO/WT=1.0000000020862798
- Reactions: `GTPCII`
- GPR: `GTPCII:PA4054 or PA4047`
- Suspected mechanism (associative): FN_ISOENZYME_REDUNDANCY
- Safest review action: Manually inspect OR-GPRs and ask whether isozyme annotation is biologically justified; do not auto-edit GPRs.
- Notes: At least one associated reaction has OR-logic GPR and remains True after single-gene KO (cobra.gpr.eval); isoenzyme/redundancy compatible with retained growth.

### PA4068 (FN) — `FN_ISOENZYME_REDUNDANCY` [high]

- Experimental: `POSITIVE_CONSENSUS_ESSENTIAL` (minimal_sum=3)
- Model prediction: `MODEL_NEGATIVE` · KO/WT=1.0000000020921251
- Reactions: `UDPG4E`
- GPR: `UDPG4E:PA3141 or PA1384 or PA3146 or PA4068`
- Suspected mechanism (associative): FN_ISOENZYME_REDUNDANCY
- Safest review action: Manually inspect OR-GPRs and ask whether isozyme annotation is biologically justified; do not auto-edit GPRs.
- Notes: At least one associated reaction has OR-logic GPR and remains True after single-gene KO (cobra.gpr.eval); isoenzyme/redundancy compatible with retained growth.

### PA4447 (FN) — `FN_ISOENZYME_REDUNDANCY` [high]

- Experimental: `POSITIVE_CONSENSUS_ESSENTIAL` (minimal_sum=3)
- Model prediction: `MODEL_NEGATIVE` · KO/WT=1.000000002086301
- Reactions: `HSTPT`
- GPR: `HSTPT:PA4447 or PA3165 or PA2531`
- Suspected mechanism (associative): FN_ISOENZYME_REDUNDANCY
- Safest review action: Manually inspect OR-GPRs and ask whether isozyme annotation is biologically justified; do not auto-edit GPRs.
- Notes: At least one associated reaction has OR-logic GPR and remains True after single-gene KO (cobra.gpr.eval); isoenzyme/redundancy compatible with retained growth.

### PA4728 (FN) — `FN_ISOENZYME_REDUNDANCY` [high]

- Experimental: `POSITIVE_CONSENSUS_ESSENTIAL` (minimal_sum=3)
- Model prediction: `MODEL_NEGATIVE` · KO/WT=1.0000000020862951
- Reactions: `HPPK`
- GPR: `HPPK:PA0583 or PA4728`
- Suspected mechanism (associative): FN_ISOENZYME_REDUNDANCY
- Safest review action: Manually inspect OR-GPRs and ask whether isozyme annotation is biologically justified; do not auto-edit GPRs.
- Notes: At least one associated reaction has OR-logic GPR and remains True after single-gene KO (cobra.gpr.eval); isoenzyme/redundancy compatible with retained growth.

### PA4846 (FN) — `FN_ISOENZYME_REDUNDANCY` [high]

- Experimental: `POSITIVE_CONSENSUS_ESSENTIAL` (minimal_sum=3)
- Model prediction: `MODEL_NEGATIVE` · KO/WT=1.0000000020863045
- Reactions: `DHQD1`
- GPR: `DHQD1:PA4846 or PA0245`
- Suspected mechanism (associative): FN_ISOENZYME_REDUNDANCY
- Safest review action: Manually inspect OR-GPRs and ask whether isozyme annotation is biologically justified; do not auto-edit GPRs.
- Notes: At least one associated reaction has OR-logic GPR and remains True after single-gene KO (cobra.gpr.eval); isoenzyme/redundancy compatible with retained growth.

### PA5119 (FN) — `FN_ISOENZYME_REDUNDANCY` [high]

- Experimental: `POSITIVE_CONSENSUS_ESSENTIAL` (minimal_sum=3)
- Model prediction: `MODEL_NEGATIVE` · KO/WT=1.0000000020863304
- Reactions: `GLNS_i`
- GPR: `GLNS_i:(PA3356 or PA0296 or PA2040 or PA5522 or PA5508) or PA0298 or PA5119`
- Suspected mechanism (associative): FN_ISOENZYME_REDUNDANCY
- Safest review action: Manually inspect OR-GPRs and ask whether isozyme annotation is biologically justified; do not auto-edit GPRs.
- Notes: At least one associated reaction has OR-logic GPR and remains True after single-gene KO (cobra.gpr.eval); isoenzyme/redundancy compatible with retained growth.

Priority-1 genes total: **103** (showing up to 25 above).

## Unresolved cases

- Count: **1**
- Reason: insufficient model-structural evidence for a more specific category under the deterministic rules (allowed outcome).

## Artifacts

- `data/processed/validation/v01_mops_pyruvate_error_audit.csv`
- `data/processed/validation/v01_mops_pyruvate_false_negative_audit.csv`
- `data/processed/validation/v01_mops_pyruvate_false_positive_audit.csv`
- `project_management/audit/v01_mops_pyruvate/V01_ERROR_CATEGORY_COUNTS.csv`
- `project_management/audit/v01_mops_pyruvate/V01_ERROR_STRUCTURE_AUDIT.md`
- Script: `scripts/validation/audit_v01_mops_pyruvate_errors.py`

## Explicit non-actions

- No model/media/threshold/GPR edits.
- V-01 scientific completeness is **not** claimed.
- No decision approving model modifications.

**Gate:** `V01_ERROR_ANALYSIS_COMPLETED_PENDING_HUMAN_REVIEW`

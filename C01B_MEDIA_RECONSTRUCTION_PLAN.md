# C01B_MEDIA_RECONSTRUCTION_PLAN.md

**Date:** 2026-07-07 · **Branch:** `claude/revival-audit` · **Env:** `reccobra39`
**Purpose:** plan (only) how each experimental condition could later be
reconstructed as an in-model medium (exchange configuration) for C-01b. **No
`data/processed/conditions/*.json` created. No exchange-bound magnitudes invented.
No simulation.** This is the design gate before C-01b.

## Model medium facts (read-only, from `model_audit_snapshot.json` + SBML)
- iMO1056 has **121 exchange reactions**; default growth 1.0479 /h.
- **Default medium (open uptake):** `EX_glc_e` (glucose, −10), `EX_o2_e` (−1000),
  `EX_nh4_e`, `EX_pi_e`, `EX_so4_e`, and metals/ions `EX_{cd2,cobalt2,cu2,fe2,fe3,
  k,mg2,mn2,na1,zn2}_e`, plus `EX_{co2,h,h2o,n2}_e`.
- **API:** `src/medium.py` — `reset_medium()` (block all uptake), then
  `set_medium(carbon_source, electron_acceptor, …, additional_uptake={})`.
- **Exchanges relevant to media (present in the model):**
  - Carbon/organic acids: `EX_glc_e`, `EX_pyr_e` (pyruvate), `EX_succ_e`
    (succinate), `EX_lac__L_e` (L-lactate), `EX_ac_e`, `EX_cit_e`, `EX_akg_e`,
    `EX_fum_e`, `EX_mal__L_e`, `EX_glyc_e` (glycerol), `EX_fru_e`, `EX_glcn__D_e`.
  - **All 20 amino acids:** `EX_{ala__L,arg__L,asn__L,asp__L,cys__L,gln__L,glu__L,
    gly,his__L,ile__L,leu__L,lys__L,met__L,phe__L,pro__L,ser__L,thr__L,trp__L,
    tyr__L,val__L}_e` (also `orn__L`).
  - Electron acceptors: `EX_o2_e`, `EX_no3_e` (nitrate), `EX_no2_e`.
  - Ions/minerals: `EX_{nh4,pi,so4,k,mg2,na1,fe2,fe3,mn2,zn2,cu2,cobalt2,mobd,
    ni2}_e`.
  - Cofactors present: `EX_thm_e` (thiamine), `EX_abtn_e` (biotin). **Most other
    vitamins (riboflavin, pantothenate, folate, B12, niacin) have NO exchange** —
    a gap for rich/RPMI media.
  - **No exchange** for: mucin, DNA, serum proteins, undefined extracts (yeast
    extract/tryptone) → complex/biological components are not representable.

## Per-condition plan

| study | condition | phenotype supported | source locator | composition status | first batch? |
|---|---|---|---|---|---|
| lee2015 | LB (rich) — general essential context | generally-essential | sd01 `General essential genes`; LB standard | PARTIAL | **yes (approx.)** |
| lee2015 | MOPS-pyruvate (minimal) | condition-specific-essential | sd01 `Min sum (of 3)`; Lee SI | DEFINED | **yes** |
| turner2015 | MOPS-succinate (minimal) | reduced-fitness (vs sputum) | sd06/sd07 titles; Turner Methods | DEFINED | **yes** |
| turner2015 | SCFM2 | condition-specific-essential / fitness | **sd08 Step 1–3 (`[final] mM`)** | PARTIAL | **yes (defined part)** |
| belanger2022 | RPMI-1640 | condition-specific-essential | DS2 `RPMI`; commercial formula | PARTIAL | **conditional** (see gaps) |
| belanger2022 | RPMI + human serum | condition-specific / host | DS2 `RPMI/Serum` | PARTIAL (serum undefined) | no (serum gap) |
| turner2015 | native CF sputum | condition-specific-essential | paper | MEDIA_GAP_PENDING | no (use SCFM2 proxy) |
| belanger2022 | murine abscess; human skin | host-condition-fitness | DS2 `Abscess`/`Skin` | MEDIA_GAP_PENDING | no (in-vivo, not exchange medium) |
| basta2017 | carbon-/oxygen-limited arrest | growth-arrest-survival-determinant | sd1/sd2 | NOT_RECONSTRUCTABLE_AS_GROWTH_MEDIUM | no (non-growth) |
| poulsen2019 | LB/M9/serum/sputum/urine | core-essential | sd04 `Medium` | (media DEFINED/GAP) but **gene mapping orthology-blocked** | no (orthology first) |

## Proposed exchange-bound strategy (high level; magnitudes deferred)
For each **DEFINED/PARTIAL** medium: `reset_medium(model)`, then open a documented
set of exchanges = {carbon source(s)} + {electron acceptor} + {N/P/S salts +
metals} + {any defined amino acids/cofactors in the recipe}. **The numeric uptake
bounds are NOT set here** — they require a cited component→flux conversion
(concentration → uptake rate) that is a separate, sourced step. Candidate mappings:
- **MOPS-pyruvate (Lee):** carbon `EX_pyr_e`; acceptor `EX_o2_e`; open salts/metals
  (already in default). Fully representable → DEFINED.
- **MOPS-succinate (Turner):** carbon `EX_succ_e`; acceptor `EX_o2_e`; salts/metals.
  Fully representable → DEFINED.
- **SCFM2 (Turner sd08):** open the 20 amino-acid exchanges, `EX_glc_e`,
  `EX_lac__L_e`, salts/metals, `EX_o2_e`. **Gaps:** mucin, salmon-sperm DNA (no
  exchange), and any DTPA/buffer components; also some SCFM2 free divalent-cation
  chemistry not captured. → PARTIAL (defined small-molecule part only).
- **LB (rich, approximation):** open the 20 amino-acid exchanges + `EX_glc_e` +
  salts/metals + `EX_o2_e`, as a **defined approximation** of a complex medium.
  → PARTIAL; label explicitly as an approximation (not true LB).
- **RPMI-1640 (Belanger):** open 20 amino acids + `EX_glc_e` + salts +
  `EX_o2_e`; **gap:** RPMI vitamins with no exchange (riboflavin, folate, B12,
  pantothenate, niacin), glutathione, phenol red. → PARTIAL; confirm whether the
  missing vitamins are essential for feasibility before including in batch.

## Required exchanges to check in iMO1056 (per first-batch condition)
- MOPS-pyruvate: `EX_pyr_e`, `EX_o2_e` (both present ✓).
- MOPS-succinate: `EX_succ_e`, `EX_o2_e` (present ✓).
- SCFM2: 20 AA exchanges (present ✓), `EX_glc_e`, `EX_lac__L_e`, `EX_o2_e`
  (present ✓); mucin/DNA (**absent** — gap).
- LB approx.: 20 AA exchanges + `EX_glc_e` + `EX_o2_e` (present ✓).
- RPMI: 20 AA exchanges + `EX_glc_e` + `EX_o2_e` (present ✓); vitamins
  riboflavin/folate/B12/pantothenate/niacin (**absent** — gap to assess).

## Known gaps (record; do not fabricate)
- Complex/undefined components (yeast extract, tryptone, mucin, DNA, serum) have
  no exchange — cannot be set as bounds; approximate or flag.
- Vitamin exchanges largely absent → RPMI/rich media feasibility must be checked
  (if a required biomass precursor depends on an absent vitamin uptake, the model
  may be infeasible or rely on de-novo synthesis).
- Numeric uptake bounds are **not** defined here (need cited concentration→flux
  mapping).
- Native sputum, abscess, skin: no exchange-medium representation.
- Poulsen media: moot until PA14→PAO1 orthology exists.

## First simulation batch (recommendation, when C-01b is authorized)
Include (DEFINED, lowest risk): **MOPS-pyruvate (Lee)**, **MOPS-succinate
(Turner)**. Add (PARTIAL, defined part, clearly labelled approximations):
**SCFM2 (Turner sd08)**, **LB approximation (Lee general-essential context)**.
Hold **RPMI** pending the vitamin-exchange feasibility check. Exclude serum,
native sputum, abscess, skin, Basta arrest, and all Poulsen media.

**Not done in this cycle:** no JSON, no bounds, no feasibility run, no simulation.
C-01b remains **not started** — this is the plan only.

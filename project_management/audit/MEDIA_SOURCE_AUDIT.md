# MEDIA_SOURCE_AUDIT.md

**Date:** 2026-07-07 · **Branch:** `claude/revival-audit` · **Env:** `reccobra39`
**Purpose (Phase 7, planning only):** for every study with raw supplements,
record which **media/conditions** appear, exactly **where** (supplement
file/sheet/column or paper/SI), whether the **composition** is documented well
enough to reconstruct in-model exchange bounds later (C-01b), and flag
**MEDIA_GAP_PENDING** where it is not. **No exchange bounds invented, no condition
JSON created, no simulation run.** This file only audits sources.

Guiding rule: a raw-supplement condition is a candidate media source **unless the
supplement/paper lacks composition detail** — then the gap is recorded explicitly.

Reconstructability legend:
- **DEFINED** — chemically defined recipe with concentrations → exchange-bound
  translation possible later (still needs component→model-metabolite mapping; not
  done). Exact composition **exists**.
- **PARTIAL** — recipe known but includes components with no clean exchange
  (polymers, undefined extracts) → reconstruct the defined part; flag the rest.
  Exact composition **partially exists**.
- **MEDIA_GAP_PENDING** — biological/complex/in-vivo growth medium; composition
  **not** defined in a way that yields exchange bounds. Do not fabricate.
- **NOT_RECONSTRUCTABLE_AS_GROWTH_MEDIUM** — the condition is **not a growth
  medium** at all (e.g. energy-limited/anaerobic growth-arrest survival). No
  exchange-medium translation is meaningful; a non-growth (maintenance/ATP)
  framework would be needed. Recorded, not reconstructed.

Per row: "Composition source" = where the recipe/definition lives; the
Reconstructability tag encodes both *whether exact composition exists* and
*whether exchange-bound translation is possible* per the legend above; the trailing
note states the remaining gap. **No exchange bounds invented; no simulation.**

---

## lee2015 (MPAO1)
Media codes (Lee Table S3 / sd01 columns): 1=LB, 2=MOPS-pyruvate, 3=sputum agar,
4=0.1× LB, 5=serum agar, 6=BHI. Locator: `pnas.1422186112.sd01.xlsx` columns
`LB sum (of 6)`, `Min sum (of 3)`, `Sputum sum (of 4)`, `BHI (of 1)`,
`0.1X LB (of 1)`, `Serum (of 1)`; composition in Lee **SI Materials and Methods**.

| Condition | Source locator | Composition source | Reconstructability |
|---|---|---|---|
| LB (rich) | sd01 `LB sum (of 6)` | standard (tryptone/yeast extract/NaCl) | PARTIAL (complex extract; rich-medium approximation only) |
| MOPS-pyruvate (minimal) | sd01 `Min sum (of 3)` | Lee SI (MOPS defined base + pyruvate) | DEFINED |
| CF sputum agar | sd01 `Sputum sum (of 4)` | patient sputum (biological) | MEDIA_GAP_PENDING |
| 0.1× LB (dilute) | sd01 `0.1X LB (of 1)` | 10× dilution of LB | PARTIAL |
| serum agar | sd01 `Serum (of 1)` | serum (biological) | MEDIA_GAP_PENDING |
| BHI (rich) | sd01 `BHI (of 1)` | standard brain-heart infusion | PARTIAL (complex) |

## turner2015 (PAO1 + PA14)
Conditions encoded in table titles/columns of `pnas.1419677112.sd0*.xlsx`; **SCFM2
recipe is in `sd08`** (Steps 1–3) with chemical list + **[final] mM
concentrations**.

| Condition | Source locator | Composition source | Reconstructability |
|---|---|---|---|
| SCFM2 (synthetic CF sputum) | **`sd08` Step 1–3** (chemicals, masses, `[final] (mM)`) + paper SI | supplement recipe present | PARTIAL (defined salts/amino acids/carbon → exchanges; **mucin + salmon-sperm DNA polymers** have no clean exchange → flag) |
| MOPS-succinate (minimal) | sd06/sd07 title (vs. succinate) | MOPS defined base + succinate | DEFINED |
| MOPS-sputum | sd04 title | MOPS base + sputum-derived components | MEDIA_GAP_PENDING (sputum fraction undefined) |
| CF sputum (native) | paper (context) | patient sputum (biological) | MEDIA_GAP_PENDING |

## belanger2022 (PAO1)
Conditions = DS2 sub-condition columns + DS1 baseline; composition in paper Methods.

| Condition | Source locator | Composition source | Reconstructability |
|---|---|---|---|
| MHB / LB (rich baseline, T0) | DS1 `T0_PAO1_essential_genes`; Table 1 | standard (complex) | PARTIAL |
| RPMI-1640 | DS2 `RPMI` column | commercial defined formulation (published) | DEFINED (needs component→exchange mapping) |
| RPMI + human serum | DS2 `RPMI/Serum` column | RPMI (defined) + **human serum** (complex) | PARTIAL (serum fraction undefined) |
| murine abscess (in vivo) | DS2 `Abscess` column | in-vivo host niche | MEDIA_GAP_PENDING |
| human skin organoid (in vivo-like) | DS2 `Skin` column | ex-vivo host niche | MEDIA_GAP_PENDING |

## poulsen2019 (multi-strain; PA14-referenced) — media present; gene mapping still blocked
Media (5) per strain×medium in sd03/sd04; aggregated in sd05 `# media essential (of 5)`.
(Gene-level use is separately blocked on PA14→PAO1 orthology; media audit below is
independent of that.)

| Condition | Source locator | Composition source | Reconstructability |
|---|---|---|---|
| LB (rich) | sd04 `Medium`=LB; sd01 QC | standard (complex) | PARTIAL |
| M9 (minimal) | sd04 `Medium`=M9 | standard defined M9 (+ carbon source per paper) | DEFINED (confirm carbon source from Methods) |
| serum (FBS) | sd04 `Medium`=FBS | fetal bovine serum (complex) | MEDIA_GAP_PENDING |
| sputum (Sp) | sd04 `Medium`=Sp | biological | MEDIA_GAP_PENDING |
| urine (Ur) | sd04 `Medium`=Ur | biological/variable | MEDIA_GAP_PENDING |

## basta2017 (PA14) — energy-limited growth arrest
Conditions in `mbo006173591sd1` (Carbon limited), `sd2` (Oxygen limited); growth
media LB and pyruvate-minimal per paper Methods.

| Condition | Source locator | Composition source | Reconstructability |
|---|---|---|---|
| pyruvate minimal (M9 + 40 mM pyruvate) | paper Methods; sd3/sd4 control | defined (M9 + pyruvate) | DEFINED (aerobic-outgrowth control medium) |
| LB (rich) | paper Methods | standard (complex) | PARTIAL |
| **carbon limitation** (arrest) | sd1 (`Carbon limited`) | *condition*, not a medium (10-day C starvation → aerobic outgrowth) | **NOT_RECONSTRUCTABLE_AS_GROWTH_MEDIUM** — non-growth arrest; maintenance/ATP framework needed, not an exchange medium |
| **oxygen limitation** (arrest) | sd2 (`Oxygen limited`) | *condition* (anaerobic 10-day arrest → aerobic outgrowth) | **NOT_RECONSTRUCTABLE_AS_GROWTH_MEDIUM** — anaerobic + non-growth |

---

## Summary of media gaps (record; do not fabricate)
- **DEFINED (exchange translation possible later):** MOPS-pyruvate (Lee),
  MOPS-succinate (Turner), RPMI-1640 (Belanger), M9 (Poulsen — confirm carbon
  source), pyruvate-minimal (Basta control).
- **PARTIAL (reconstruct defined part; flag complex fraction):** SCFM2 (Turner —
  recipe present in sd08 with `[final] (mM)`, but mucin/DNA polymers have no clean
  exchange), LB/BHI/MHB rich media, RPMI+serum.
- **MEDIA_GAP_PENDING (biological growth media; composition undefined):** native/CF
  sputum, serum/FBS, urine, murine abscess, skin organoid.
- **NOT_RECONSTRUCTABLE_AS_GROWTH_MEDIUM (not a growth medium):** Basta's
  carbon-limited and oxygen-limited **arrest** states — non-growth survival
  conditions; would need a maintenance/ATP framework, not an exchange medium.

Every raw-supplement condition above has been categorized (none left
uncategorized), per the user rule that each condition is a candidate media source
unless a data gap is recorded.

## Constraints held
No exchange bounds invented; no `data/processed/conditions/*.json` created; no
simulation run. C-01b remains **not started**. Component→model-metabolite mapping
for the DEFINED/PARTIAL media is a later step (still requires per-component
sourcing; do not guess).

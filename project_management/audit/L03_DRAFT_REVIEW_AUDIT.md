# L03_DRAFT_REVIEW_AUDIT.md

**Date:** 2026-07-07 · **Branch:** `claude/revival-audit` · **Env:** `reccobra39`
**Scope:** review of `data/processed/literature_evidence_gene_level_DRAFT.csv`
(DRAFT gene-level evidence for Lee/Turner/Belanger). **Not a promotion.** Canonical
`data/processed/literature_evidence.csv` is untouched. No metrics computed.

## Totals (after L03-B3 resolution this cycle)
- **5,148 rows** — lee2015 **2,892**, turner2015 **586**, belanger2022 **1,670**.
- **review_status:** READY **2,607**; NEEDS_REVIEW **2,541** (all Lee per-medium).
- **phenotype_class (6 kept distinct):** generally-essential 1,303;
  condition-specific-essential 2,998; reduced-fitness 165; host-condition-fitness
  682. (core-essential and growth-arrest-survival-determinant intentionally absent
  — their sources Poulsen/Basta are mapping-blocked, not parsed.)

## Integrity checks — ALL PASS
| Check | Result |
|---|---|
| `original_gene_id` matches `^PA\d+$` | ✅ 0 violations |
| `mapped_pao1_gene_id` matches `^PA\d+$` | ✅ 0 violations |
| PA14 tag leakage | ✅ 0 |
| phenotype outside the 6-class vocab | ✅ none |
| varadarajan rows present | ✅ none |
| zhu rows present | ✅ none |
| poulsen rows present | ✅ none (correctly gated) |
| basta rows present | ✅ none (correctly gated) |
| duplicate (study,gene,phenotype,condition,file,sheet,row) | ✅ 0 |
| `source_file`/`source_sheet`/`source_row` non-empty | ✅ all populated |
| `threshold` / `essentiality_definition` non-empty | ✅ all populated |
| `condition` / `medium` non-empty | ✅ all populated |

## Per-study review

### lee2015 (2,892 rows)
- **351 READY** — general-essential set (`General essential genes` sheet
  membership; ≈ paper's 352 general-essential-including-domains). Fully sourced.
- **2,541 NEEDS_REVIEW** — per-medium condition-specific rows, distributed:
  LB 423, MOPS-pyruvate 437, CF sputum 378, BHI 470, 0.1× LB 392, serum 441.
- **Why still NEEDS_REVIEW (not silently promoted):** the emission threshold maps
  the SI's "pools" consensus rule (≥2/3 LB pools, ≥2/3 MOPS-pyruvate, ≥3/4 sputum;
  singles ≥1) onto the supplement's `X sum (of 6/3/4)` **assay** columns, but the
  exact pool↔assay correspondence is not stated verbatim in Lee. Until that
  ambiguity is resolved (from Lee SI or author correspondence), these rows carry
  the raw `sum` value in `statistical_rule`/`notes` and stay NEEDS_REVIEW. **Not
  converted to READY this cycle.**

### turner2015 (586 rows) — L03-B3 RESOLVED this cycle
- **336 generally-essential** (sd01 initial-library `Essential?`; exact match to
  paper's 336 PAO1 essentials).
- **165 reduced-fitness** — sd06/sd07 (sputum vs MOPS-succinate) + **sd09 (+9,
  CF sputum vs SCFM2)** + sd10 block-1.
- **46 condition-specific-essential** — **sd05** PAO1 sputum block ("essential in
  sputum but not initial"). Sanity: **0 of 46 overlap the sd01 general-essential
  set** — consistent with the "not initial" definition (no double-count).
- **39 host-condition-fitness** — sd10 block-2 (murine chronic wound).
- **Paired sheets (L03-B3):** PAO1 column blocks are **unambiguous** (each has a
  `PAO1 Locus ID` header; verified layout). Parser guards assert the headers and
  **skip on mismatch** (fail-safe). Decisions:
  - **sd03** (initial libraries) = redundant with sd01 → **not parsed** (would
    double-count generally-essential).
  - **sd04** (MOPS-sputum) mixes general + condition-specific essentials → **not
    parsed** (would mislabel generals as condition-specific); **sd05** is the clean
    condition-specific subset, parsed instead.
  - **sd05** → condition-specific-essential (PAO1 columns only). READY. Documented
    caveat: it is the **both-strain intersection** (essential in sputum in *both*
    PAO1 and PA14, not initial), so PAO1-only sputum-specific essentials (in sd04)
    are not included — a scope limitation, not an error.
  - **sd09** → reduced-fitness (PAO1 columns only; FC≥4 & P<0.05).
- PA14 columns excluded throughout; no orthology used.

### belanger2022 (1,670 rows)
- **616 generally-essential** (DS1 `T0_PAO1_essential_genes`); cross-study ±
  citation columns correctly **not** ingested.
- **411 condition-specific-essential** (RPMI, RPMI/Serum) + **643
  host-condition-fitness** (abscess, skin) from DS2.
- **DS2 two-row header + dedup verified:** the parser reads row-2 sub-headers per
  sheet (condition column order differs across `Essential_media`/`Abscess`/`Skin`/
  `Shared_Essential`) and dedupes on (gene, condition) across the four overlapping
  sheets; NE/blank cells excluded. No duplicate (gene, condition) rows in output.

## Promotion decision
**Do NOT promote to a validated table yet.** Blockers before promotion:
1. Lee per-medium NEEDS_REVIEW rows need the pool↔assay ambiguity resolved.
2. Human sign-off on phenotype-class assignments and the sd05 both-strain caveat.
3. Promotion must write a **new** validated file — never overwrite canonical
   `data/processed/literature_evidence.csv`.
Until then the DRAFT stays DRAFT; **no metrics** on it (B-SCI-01).

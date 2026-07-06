# L03_PARSE_BLOCKERS.md

**Date:** 2026-07-06 (updated) · **Branch:** `claude/revival-audit` · **Env:** `reccobra39`
**Decision (this cycle):** the Phase E/6 gate is now **satisfied for lee2015,
turner2015 (PAO1 single-strain sheets), and belanger2022** — per-study
essentiality **definitions + numeric thresholds** were sourced from each paper's
Methods (`THRESHOLD_METHOD_AUDIT.md`), so DRAFT gene-level rows were parsed for
those studies. varadarajan2020's citation was verified but its essentiality is a
re-mapping of Lee 2015 (double-count) → parsed as **evidence: no**. zhu2018
remains out of scope. Nothing fabricated; canonical `literature_evidence.csv`
untouched; all raw files read-only.

## Outputs written this cycle (DRAFT, derived only)
- `data/processed/literature/lee2015_parsed_gene_evidence.csv`
- `data/processed/literature/turner2015_parsed_gene_evidence.csv`
- `data/processed/literature/belanger2022_parsed_gene_evidence.csv`
- `data/processed/literature_evidence_gene_level_DRAFT.csv` (aggregate, 5,093 rows)
- `scripts/literature/parse_supplements.py` (parser), `scripts/literature/pdf_text.py`
  (read-only PDF text helper).

## Blocker status
| ID | Study | What it was | Status |
|----|-------|-------------|--------|
| **L03-B1** | lee2015 | essentiality definition + per-medium threshold | **RESOLVED** — P<0.001 log2-normal fit; consensus ≥2/3 LB, ≥2/3 MOPS-pyruvate, ≥3/4 sputum pools (SI). General essential parsed READY; per-medium parsed NEEDS_REVIEW (pool↔assay mapping). |
| **L03-B2** | turner2015 | `Essential?`/`Mode` + fitness cutoffs | **RESOLVED** — Essential = P<0.01 (neg binom, obs vs Monte-Carlo pseudodata) AND essential-like mclust mode (P<0.01 MLE); `Mode`=mclust category. Fitness = FC≥4 & P<0.05. sd01/06/07/10 parsed. |
| **L03-B3** | turner2015 | PAO1 column blocks in paired sheets sd03/04/05/09 | **OPEN** — paired PAO1+PA14 sheets not parsed; needs column-block confirmation before extracting PAO1-only columns. |
| **L03-B4** | belanger2022 | meaning/threshold of Tradis/Transit/Both/NE | **RESOLVED** — essential if Gumbel(TRANSIT) OR TraDIS calls it in ≥4/5 experimental reps (≥2/3 for T0). Single-tool call counts; Both=both tools; NE=not essential. |
| **L03-B5** | belanger2022 | two-row-header merge for Data_Sheet_2 | **RESOLVED** — parser reads row-2 sub-headers per sheet (condition column order differs per sheet) and maps RPMI/Serum, RPMI, Abscess, Skin correctly. |
| **L03-B6** | varadarajan2020 | verify DOI/PMID | **RESOLVED** — npj Biofilms Microbiomes 6:46 (2020), DOI 10.1038/s41522-020-00154-8, PMID 33127897, PMCID PMC7603352 (`VARADARAJAN2020_CITATION_CHECK.md`). |
| **L03-B7** | varadarajan2020 | build/validate MPAO1→PAO1 mapping | **REFRAMED / DEFERRED** — DS1/DS3 provide a native best-hit map; may be built later as a *reference resource*, not evidence. Not needed this run (study not parsed as evidence). |
| **L03-B8** | varadarajan2020 | "essential in N/16 samples" threshold | **RESOLVED-BUT-DERIVATIVE** — the 16 samples are **Lee 2015's** libraries re-mapped to MPAO1 using Lee's scripts; essentiality is Lee-derived → **do not parse as independent evidence** (double-count). |

## Why varadarajan2020 is NOT parsed as evidence (record)
Varadarajan 2020 SI: *"Using the scripts released by Lee and colleagues, Tn-seq
data were re-mapped to our complete MPAO1 genome … 577 all essential genes …
312 general essential genes."* The 16 Tn-seq samples (Supplementary Table 3) are
Lee's own LB/minimal/sputum/0.1XLB/BHI libraries. Treating DS4 as independent
labels would double-count Lee 2015 — the same reason zhu2018 `additionalFile19`
is excluded. Its unique, genuinely-new genes (~136 MPAO1-unique) have no PAO1
homolog and cannot map to the PAO1 model. → citation VERIFIED; **evidence: no**;
mapping resource: optional/later.

## Remaining to fully close L-03 (next cycle)
1. **Human review** of the DRAFT (`literature_evidence_gene_level_DRAFT.csv`),
   especially Lee per-medium NEEDS_REVIEW rows (confirm the sum→essential mapping),
   then promote reviewed rows to a validated table (still never overwriting
   canonical `literature_evidence.csv`).
2. **L03-B3:** confirm PAO1 column blocks in Turner sd03/04/05/09 and extract PAO1
   columns (adds general/condition rows from the paired sheets).
3. **Missing studies** (B-LIT-01/B-NET): meegid2022 / poulsen2019 (core-essential)
   / basta2017 (PA14 growth-arrest, needs orthology) supplements still absent.
4. Optionally build the varadarajan2020 MPAO1→PAO1 reference map (not evidence).

## Guardrails held
- No metrics computed. No gene lists / thresholds / orthology / media fabricated.
- No raw supplement, PDF, or model file modified. `conditian/` untouched.
- Canonical `data/processed/literature_evidence.csv` not overwritten.

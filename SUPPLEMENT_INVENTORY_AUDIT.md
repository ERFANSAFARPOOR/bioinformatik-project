# SUPPLEMENT_INVENTORY_AUDIT.md

**Date:** 2026-07-06 · **Branch:** `claude/revival-audit` · **Env:** `reccobra39`
(openpyxl read-only inspection). **No raw file was modified, moved, or deleted.**

## Folder-location check
- `data/raw/literature/` — **EXISTS** ✅ (7 study folders).
- `data/raw/lituare/` (typo path) — **DOES NOT EXIST** ✅. No files to move; no
  relocation performed. Nothing lost.
- `conditian/` — preserved and untouched (not part of this audit).

## Coverage summary vs expected high-priority list
| # | Study | Expected | Present? | Notes |
|---|-------|----------|:--------:|-------|
| 1 | lee2015 (MPAO1, P0) | `pnas.1422186112.sd01.xlsx` | ✅ | present + Supporting Information PDF |
| 2 | turner2015 (PAO1+PA14, P0) | sd01–sd04 | ✅ **+extra** | sd01–**sd10** all present (10 files) |
| 3 | belanger2022 (PAO1, P0) | Frontiers suppl. (DOI 10.3389/fmicb.2022.1055512) | ✅ | Data_Sheet_1/2 (.XLSX) + Data_Sheet_3 (.docx) |
| 4 | meegid2022 (PAO1, P1) | full text / suppl. (PMID 35104681) | ❌ **MISSING** | **no `meegid2022/` folder exists at all** |
| 5 | poulsen2019 (P1) | PNAS SI / Broad fitness | ❌ **MISSING** | folder exists but only `.gitkeep` (empty) |
| 6 | basta2017 (PA14, P2 deferred) | mBio suppl. | ❌ empty | folder exists, only `.gitkeep`; deferred (PA14) |

**Unexpected study folders present (audited below):**
- `varadarajan2020` (MPAO1) — TnSeq essentiality + MPAO1↔PAO1 mapping. **Strong P0/P1 candidate.**
- `zhu2018` (iPAO1) — GigaScience giy021 **metabolic reconstruction** (a *model*, not
  primary experimental essentiality data). **Background / out-of-scope for L-03 labels.**

**Duplicates:** none detected (all SHA-256 distinct). **Unreadable files:** none —
all `.xlsx` opened successfully with openpyxl. `.docx`/`.pdf` not parsed here
(logged as metadata/context).

**Parse-readiness legend:** `READY_FOR_PARSE_NOTES` = structure clear, proceed to
parse notes (Phase D). `NEEDS_HUMAN_REVIEW` = ambiguity to resolve first.
`WRONG_OR_UNKNOWN / NOT_RELEVANT` = not an experimental gene-label source for L-03.
(PDF/docx = context, not tabular parse targets here.)

---

## lee2015 — Lee et al. 2015, PNAS (MPAO1 / PAO1 locus tags) · **P0**
| File | ext | size | SHA-256 (short) | kind | matches study | readable | parse-readiness |
|------|-----|------|-----------------|------|:-------------:|:--------:|-----------------|
| `pnas.1422186112.sd01.xlsx` | .xlsx | 156,343 | `14557cee…` | raw supplement | ✅ (PNAS id 1422186112) | ✅ | **READY_FOR_PARSE_NOTES** |
| `Supporting Information.pdf` | .pdf | 445,067 | `2e1ad4cb…` | PDF (context) | ✅ | n/a | context only |
| `.gitkeep` | — | 0 | — | placeholder | — | — | ignore |

Sheets in sd01: `General essential genes` (~552 rows), `All essential genes`
(~553), `Essential noncoding regions ` (~140, non-CDS). Header on **row 2**
(row 0 = title). Gene col = **`PA number`** (PAO1 `PAxxxx`) + `PA gene`. Condition
columns: `LB sum (of 6)`, `Min sum (of 3)`, `Sputum sum (of 4)`, `Sum of sums (of
13)`, `BHI`, `0.1X LB`, `Serum`. Phenotype: **generally-essential** +
**condition-specific-essential**. Direct PAO1 mapping: **YES** (native PA numbers).

## turner2015 — Turner et al. 2015, PNAS (PAO1 + PA14) · **P0 for PAO1 rows**
Header on **row 2** in most sheets (row 0 = table title; PAO1 sheets have `Essential?`
= Essential/Nonessential and `Mode`; fitness sheets have fold-change + P). Distinct
essential genes shown in bold in-sheet (formatting, not a column).

| File | size | SHA-256 (short) | content (Table) | strain | phenotype | parse-readiness |
|------|------|-----------------|-----------------|--------|-----------|-----------------|
| `…sd01.xlsx` | 1,608,301 | `53f373af…` | S1 PAO1 mutant abundance vs pseudodata; `Essential?` | **PAO1** | generally-essential | **READY_FOR_PARSE_NOTES** |
| `…sd02.xlsx` | 15,049 | `a2414271…` | S2 Tn-seq sequencing stats (Strain/Media) | PAO1 | (metadata) | NOT_RELEVANT (QC) |
| `…sd03.xlsx` | 1,129,091 | `4723c701…` | S3 PA14+PAO1 abundance, 1:1 orthologs | PA14+**PAO1** | generally-essential | **READY_FOR_PARSE_NOTES** (use PAO1 cols) |
| `…sd04.xlsx` | 1,158,257 | `a1ec2e2d…` | S4 PA14+PAO1 in MOPS-sputum | PA14+**PAO1** | condition-specific-essential | **READY_FOR_PARSE_NOTES** |
| `…sd05.xlsx` | 32,953 | `64f413b8…` | S5 sputum-essential both strains (not initial) | **PAO1**+PA14 | condition-specific-essential | **READY_FOR_PARSE_NOTES** |
| `…sd06.xlsx` | 426,408 | `4b499461…` | S6 PAO1 abundance CF sputum vs MOPS-succinate | **PAO1** | reduced-fitness / condition | **READY_FOR_PARSE_NOTES** |
| `…sd07.xlsx` | 32,109 | `b6fd93fd…` | S7 biosynthetic-gene fitness sputum vs succ. | **PAO1** | reduced-fitness | **READY_FOR_PARSE_NOTES** |
| `…sd08.xlsx` | 20,979 | `3f9dddd1…` | S8 SCFM2 media **recipe/user guide** | n/a | media protocol | **NOT_RELEVANT** (→ useful for C-01b media) |
| `…sd09.xlsx` | 765,959 | `6f23ecdb…` | S9 abundance CF sputum vs SCFM2 (PAO1+PA14) | **PAO1**+PA14 | condition fitness | **READY_FOR_PARSE_NOTES** |
| `…sd10.xlsx` | 17,900 | `f32110b0…` | S10 PAO1 fitness sputum & chronic wound | **PAO1** | host-condition-fitness | **READY_FOR_PARSE_NOTES** |

Gene col = `Locus ID` / `PAO1 Locus ID` (PAO1) and `PA14 Locus ID` (PA14). Note
sd03/04/05/09 mix both strains in one sheet with **paired columns** — extract the
PAO1-labelled columns only. Direct PAO1 mapping: **YES** for PAO1 columns; PA14
columns require the study's own provided 1:1 ortholog pairing (in-sheet).

## belanger2022 — Belanger et al. 2022, Front. Microbiol. (PAO1) · **P0**
| File | ext | size | SHA-256 (short) | kind | readable | parse-readiness |
|------|-----|------|-----------------|------|:--------:|-----------------|
| `Data_Sheet_1.XLSX` | .xlsx | 143,782 | `7f5c6eb9…` | raw supplement | ✅ | **READY_FOR_PARSE_NOTES** |
| `Data_Sheet_2.XLSX` | .xlsx | 56,441 | `1052c75a…` | raw supplement | ✅ | **READY_FOR_PARSE_NOTES** |
| `Data_Sheet_3.docx` | .docx | 460,332 | `4dbc9392…` | supplement (text) | not parsed | NEEDS_HUMAN_REVIEW (docx) |

Data_Sheet_1 sheets: `T0_PAO1_essential_genes` (essential in MHB; cols `Locus Tag`
= PA number, `PA14 locus tag`, `Called Essential by`, and +/- columns citing
Poulsen/Lee/Turner/Skurnik), `GeneOverlap`, `Genome_coverage`, `Excluded`.
Data_Sheet_2 sheets: `Essential_media`, `Essential_Abscess`, `Essential_Skin`,
`Shared_Essential` — conditionally-required genes with a **two-row header** (row 1
= "Essential in", row 2 = sub-conditions `RPMI/Serum`, `RPMI`, `Abscess`, `Skin`)
and values `Tradis`/`Transit`/`Both`/`NE`. Gene col = `Locus Tag` (PAO1).
Phenotype: **generally-essential** (Sheet 1), **condition-specific-essential** +
**host-condition-fitness** (Sheet 2, abscess/skin in-vivo models). Direct PAO1
mapping: **YES**. ⚠ Header spans 2 rows — parser must merge header rows.

## varadarajan2020 — Varadarajan et al. 2020 (MPAO1) · candidate **P0/P1**
| File | ext | size | SHA-256 (short) | content | parse-readiness |
|------|-----|------|-----------------|---------|-----------------|
| `Supplementary Dataset 1 (MPAO1).xlsx` | .xlsx | 1,581,884 | `ab35311b…` | MPAO1 CDS + PAO1 best-hit mapping | **READY_FOR_PARSE_NOTES** (mapping source) |
| `Supplementary Dataset 2 (MPAO1).xlsx` | .xlsx | 31,549 | `954e3763…` | MPAO1 vs PAO1-UW SNPs/INDELs | NOT_RELEVANT (variant table) |
| `Supplementary Dataset 3 (MPAO1).xlsx` | .xlsx | 1,381,986 | `99f75b40…` | Core/unique CDS + `essential?` + PAO1 map | **READY_FOR_PARSE_NOTES** |
| `Supplementary Dataset 4 (MPAO1).xlsx` | .xlsx | 62,800 | `7c0beb3a…` | `essentialGenes_MPAO1` per-condition | **READY_FOR_PARSE_NOTES** |
| `Supplementary Information (MPAO1).pdf` | .pdf | 1,359,337 | `9e6d5f31…` | context | context only |
| `Reporting Summary Checklist (MPAO1).pdf` | .pdf | 72,135 | `23519a8f…` | context | context only |

Dataset 4 sheet `essentialGenes_MPAO1`: gene col = **`Locus`** (MPAO1_xxxxx),
`Essential in x/16 samples`, then per-replicate/condition columns (`LB-*`,
`Minimal-*`, `Sputum-*`, `HumanSerum`). Dataset 1/3 provide **MPAO1 → PAO1**
`best_hit`/`PAO1_gene_name` columns (native mapping table, more reliable than
cross-strain orthology since MPAO1 is a PAO1 sublineage). Phenotype:
**generally-essential** + **condition-specific-essential**. Direct PAO1 mapping:
**INDIRECT but supported in-supplement** (MPAO1→PAO1 columns). ⚠ Requires a
mapping step; flag one-to-many / missing per project rule 3.

## zhu2018 — Zhu et al. 2018, GigaScience giy021 (**iPAO1 model**) · background
30 files: 2 manuscript PDFs, 4 review/response PDFs, 1 docx, and
`giy021_supp/additionalFile2–27.xlsx` (Datasets EV1–EV26). Contents are metabolic
**reconstruction** artifacts: draft/final model metabolites, reactions, genes
(`iPAO1`), biomass formula, lipid A / LPS / polymyxin flux analyses. `additionalFile19`
= "Comparison of predicted gene essentiality with transposon mutant libraries"
(model-derived comparison, **not** an independent experimental label set).
**Classification:** background / competing PAO1 reconstruction — **out-of-scope for
L-03 experimental-label extraction.** May be useful later as a model cross-check,
not as an experimental essentiality source. All files: `NOT_RELEVANT_FOR_L03`
(readable, retained, provenance logged). Full SHA-256 list in
`data/processed/literature/supplement_inventory.tsv` (machine-readable export).

## basta2017 / poulsen2019 — empty
- `basta2017/` — only `.gitkeep`. Expected mBio supplement **not present**. Deferred
  (PA14; needs validated orthology) — keep blocker.
- `poulsen2019/` — only `.gitkeep`. Expected PNAS SI / Broad PA14 fitness **not
  present**. (Note: Poulsen PA14 essentiality is embedded as a **+/-** citation
  column inside belanger2022 Data_Sheet_1, but the primary Poulsen supplement
  itself is missing.)

---

## Warnings / follow-ups
1. **meegid2022 folder is entirely absent** (not just empty). If Meegid 2022
   (PMID 35104681) is still in scope, the folder + files must be provided.
2. **poulsen2019 and basta2017 are empty** (`.gitkeep` only). Provide supplements
   or keep deferred.
3. **turner2015 has sd05–sd10** beyond the expected sd01–sd04 — audited and mostly
   useful (extra PAO1 fitness/condition tables); sd08 is a media recipe (not gene
   data, but useful for **C-01b** SCFM2 media reconstruction).
4. **belanger2022 Data_Sheet_2 uses a two-row header** — parser must handle merged
   header rows or it will misalign condition columns.
5. **varadarajan2020 uses MPAO1 locus tags** — needs the in-supplement MPAO1→PAO1
   mapping; treat as a mapping step (project rule 3), not a direct 1:1.
6. **Source URLs unknown** (manual downloads) → `SOURCE_URL_PENDING` in provenance;
   do not invent URLs.
7. All files remain in place; nothing required moving (no `lituare/`).

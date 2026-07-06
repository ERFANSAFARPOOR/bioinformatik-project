# SUPPLEMENT_PARSE_NOTES — turner2015

- **study_id:** turner2015
- **citation:** Turner KH, Wessel AK, Palmer GC, Murray JL, Whiteley M (2015)
  *Essential genome of Pseudomonas aeruginosa in cystic fibrosis sputum.* PNAS
  112(13):4110–4115. DOI 10.1073/pnas.1419677112. PMID 25775563 / PMCID PMC4386324.
- **strain:** **PAO1 + PA14** (both in the same supplement; parse PAO1 columns for
  the iMO1056 identity join; PA14 columns need the study's in-sheet 1:1 ortholog pairing).
- **phenotype class(es):** **generally-essential** (S1 initial library),
  **condition-specific-essential** (S4/S5 sputum), **reduced-fitness** (S6/S7/S9
  fitness vs reference), **host-condition-fitness** (S10 murine chronic wound).

## Files inspected (all sheet name `Sheet1` unless noted; header on row index 1, title row 0)
| file | Table | content | parse target? |
|---|---|---|---|
| `pnas.1419677112.sd01.xlsx` | S1 | **PAO1** mutant abundance vs pseudodata; `Essential?` | **YES (P0)** |
| `pnas.1419677112.sd02.xlsx` | S2 | Tn-seq sequencing/QC stats (Strain/Media) | NO (QC metadata) |
| `pnas.1419677112.sd03.xlsx` | S3 | PA14+**PAO1** initial libraries, 1:1 orthologs | YES (PAO1 cols) |
| `pnas.1419677112.sd04.xlsx` | S4 | PA14+**PAO1** in MOPS-sputum | YES (PAO1 cols) |
| `pnas.1419677112.sd05.xlsx` | S5 | sputum-essential in both strains (not initial) | YES |
| `pnas.1419677112.sd06.xlsx` | S6 | **PAO1** abundance CF sputum vs MOPS-succinate | YES (fitness) |
| `pnas.1419677112.sd07.xlsx` | S7 | **PAO1** biosynthetic-gene fitness sputum vs succ. | YES (fitness) |
| `pnas.1419677112.sd08.xlsx` | S8 | **SCFM2 media recipe / user guide** (Step 1–3) | NO for genes → **C-01b media** |
| `pnas.1419677112.sd09.xlsx` | S9 | PAO1+PA14 abundance CF sputum vs SCFM2 | YES (PAO1 cols) |
| `pnas.1419677112.sd10.xlsx` | S10 | **PAO1** fitness sputum & murine chronic wound | YES (host fitness) |

## Column layout (representative)
- **sd01 (S1):** `Locus ID` | `Gene` | `Log2 Fold Change Mutant Abundance (Initial vs.
  Expected)` | `P (Fold Change)` | `Mode` | `P (Mode)` | `Essential?` | `Average No.
  Independent Insertions Detected` | … (a second Initial-vs-Expected block to the right).
  **Row 2 is a sub-header** (`Initial`/`Expected`, `Succ`/`Sputum`) under some columns —
  the sheet effectively has a 2-row header; align carefully.
- **sd03/sd04:** `PA14 Locus ID` | `Gene` | (PA14 stats) | `PAO1 Locus ID` | `Gene` |
  (PAO1 stats). Two paired strain blocks in one sheet.
- **sd06/sd09/sd10:** `Locus ID`/`PAO1 Locus ID` | `Gene` | `Fold Change Mutant
  Abundance (Sputum vs. Succ./SCFM2/Chronic)` | `P` | insertions | (KO/COG columns).

## Likely columns
- **gene ID / locus tag:** `Locus ID` / `PAO1 Locus ID` (PAO1 `PAxxxx`);
  `PA14 Locus ID` (PA14 `PA14_xxxxx`).
- **strain:** encoded by which locus-ID column (no free-text strain column); sd02 has
  an explicit `Strain` column (QC only).
- **condition / media:** encoded in the table **title** and sub-headers
  (Initial / MOPS-sputum / MOPS-succinate / SCFM2 / murine-chronic-wound).
- **essentiality / fitness:** `Essential?` (Essential/Nonessential), `Mode`
  (Reduced/Unchanged/…), `Log2 Fold Change…`, `Fold Change Mutant Abundance (… vs …)`.
- **threshold / statistics:** `P (Fold Change)`, `P (Mode)`; `Essential?` is
  pre-computed by the authors — record their definition (paper methods) with each row.

## Direct PAO1 mapping status
**YES** for the PAO1 locus-ID columns (identity join to iMO1056). PA14 columns are
paired 1:1 in-sheet by the authors, but cross-strain use still falls under B-MAP-01.

## Source-locator strategy
`source_file` (Table Sx) + `source_sheet=Sheet1` + `source_row` + `Locus ID`. For
multi-strain sheets also record which column block (PAO1 vs PA14) each value came from.

## Uncertainty notes
- 2-row headers (Initial/Expected, Succ/Sputum) — a naive `header=1` will mis-split
  the paired numeric blocks; map columns explicitly by position.
- sd08 is a **media protocol**, not gene data — route to C-01b (SCFM2 composition).
- "Essential in bold" is cell **formatting**, not a column; rely on `Essential?`/`Mode`.

## Parse-readiness
- sd01 PAO1 essentiality: **READY_FOR_L03_PARSE**.
- sd06/sd07/sd10 PAO1 fitness: **READY_FOR_L03_PARSE**.
- sd03/sd04/sd05/sd09 (paired PAO1+PA14): **NEEDS_HUMAN_REVIEW** (confirm PAO1 column
  block boundaries before extraction).
- sd02 (QC) and sd08 (media recipe): **NOT_RELEVANT_FOR_L03** (sd08 → C-01b).

## Extraction plan (next script)
1. sd01 → PAO1 generally-essential (`Essential?`=='Essential' in the initial library),
   keep `Mode`, `Log2FC`, `P` as evidence; condition="initial transposon library".
2. For each PAO1 fitness table (sd06/07/09/10), extract `PAO1 Locus ID`, fold-change,
   `P`; tag condition from the table title; phenotype = reduced-fitness /
   host-condition-fitness (sd10 chronic wound).
3. For paired sheets, extract **only** the PAO1 block after human confirmation.
4. Keep every table's condition + phenotype class distinct; record author threshold.

# SUPPLEMENT_PARSE_NOTES — lee2015

- **study_id:** lee2015
- **citation:** Lee SA, Gallagher LA, Thongdee M, Staudinger BJ, Lippman S, Singh PK,
  Manoil C (2015) *General and condition-specific essential functions of Pseudomonas
  aeruginosa.* PNAS 112(16):5189–5194. DOI 10.1073/pnas.1422186112. PMID 25848053 /
  PMCID PMC4413342.
- **strain:** **MPAO1** (a PAO1-derived lab lineage; PAO1 `PAxxxx` locus tags).
- **phenotype class(es):** **generally-essential** ("General essential genes") +
  **condition-specific-essential** (per-medium essentiality: LB / minimal-pyruvate /
  sputum / BHI / 0.1×LB / serum). Keep the two classes distinct.

## Files inspected
- `pnas.1422186112.sd01.xlsx` (156,343 B, sha `14557cee…`) — the essential-gene tables.
- `Supporting Information.pdf` (445,067 B) — context/methods only; not a parse target.

## Sheets (sd01)
1. `General essential genes` (~552 rows) — genes essential across all tested media.
2. `All essential genes` (~553 rows) — genes essential on LB, min-pyruvate **or** sputum.
3. `Essential noncoding regions ` (~140 rows) — candidate essential non-CDS/sRNA
   regions (NOT protein-coding genes → **exclude** from gene-level evidence).

## Column layout (sheets 1 & 2)
- **Header is on row index 1** (0-based); row 0 is a free-text title. Parse with
  `header=1` (openpyxl/pandas), or skip 1 title row.
- Columns: `PA number` | `PA gene` | `Product` | `LB sum (of 6)` | `Min sum (of 3)` |
  `Sputum sum (of 4)` | `Sum of sums (of 13)` | `Gen ess domains` | `BHI (of 1)` |
  `0.1X LB (of 1)` | `Serum (of 1)` | `pseudocyc` | `COG` | `Liberati et al…` (+ more
  cross-study +/- columns to the right).

## Likely columns
- **gene ID / locus tag:** `PA number` (PAO1 `PAxxxx`); `PA gene` = gene symbol.
- **strain:** none in-sheet → strain = MPAO1 from provenance (constant).
- **condition / media:** `LB sum (of 6)`, `Min sum (of 3)`, `Sputum sum (of 4)`,
  `BHI (of 1)`, `0.1X LB (of 1)`, `Serum (of 1)` (each = # replicates essential).
- **essentiality / fitness:** membership in sheet 1 = **generally-essential**;
  the per-medium "sum" columns quantify essentiality per condition (Tn-seq insertion
  depletion). `Sum of sums (of 13)` = aggregate.
- **threshold / statistics:** the sheet already lists *called-essential* genes; the
  numeric definition (what sum ⇒ essential per medium) is stated in the paper's
  methods, **not** re-derivable from the sheet alone → confirm before per-condition calls.

## Direct PAO1 mapping status
**YES** — native PAO1 `PAxxxx`. Caveat: MPAO1 ≠ PAO1-UW at a handful of loci
(indels/SNPs); locus tags align but note MPAO1 provenance in every row.

## Source-locator strategy
`source_file=pnas.1422186112.sd01.xlsx`, `source_sheet`, `source_row` (1-based Excel
row), plus the `PA number` value.

## Uncertainty notes
- Per-medium essentiality **threshold semantics** need the paper's definition (sum
  cutoff). Generally-essential membership is unambiguous (sheet 1).
- Exclude the noncoding-regions sheet from gene-level rows.

## Parse-readiness
- Generally-essential rows: **READY_FOR_L03_PARSE**.
- Per-condition (medium-specific) essentiality: **NEEDS_HUMAN_REVIEW** (confirm the
  sum→essential threshold per medium before emitting condition-specific labels).

## Extraction plan (next script)
1. Read `All essential genes` with `header=1`; keep `PA number`, `PA gene`, `Product`,
   and each medium sum column.
2. Emit generally-essential = membership in `General essential genes`.
3. Emit per-medium condition rows **only after** the threshold is confirmed; keep each
   medium as a separate condition (no binary collapse across media).
4. Record strain=MPAO1, method=Tn-seq, phenotype_class per row, and source locator.

# SUPPLEMENT_PARSE_NOTES — belanger2022

- **study_id:** belanger2022
- **citation:** Belanger CR, Dostert M, Blimkie TM, Lee AH-Y, … Hancock REW (2022)
  *Surviving the host: microbial metabolic genes required for growth of Pseudomonas
  aeruginosa in physiologically-relevant conditions.* Front. Microbiol. 13:1055512.
  DOI 10.3389/fmicb.2022.1055512. PMID 36504765 / PMCID PMC9732424.
  (Exact title to re-verify against the article.)
- **strain:** **PAO1** (`PAxxxx`; `PA14 locus tag` also provided for cross-ref).
- **phenotype class(es):** **generally-essential** (T0 essential in MHB) +
  **condition-specific-essential** (RPMI, RPMI/Serum) + **host-condition-fitness**
  (murine abscess, skin organoid).

## Files inspected
- `Data_Sheet_1.XLSX` (143,782 B, sha `7f5c6eb9…`).
- `Data_Sheet_2.XLSX` (56,441 B, sha `1052c75a…`).
- `Data_Sheet_3.docx` (460,332 B) — text supplement; **not parsed here** (NEEDS_HUMAN_REVIEW).

## Sheets
- **Data_Sheet_1:** `T0_PAO1_essential_genes` (baseline essential in MHB),
  `GeneOverlap` (overlap stats — not gene rows), `Genome_coverage` (QC),
  `Excluded` (genes with no TA sites — exclusion list, useful as a mask).
- **Data_Sheet_2:** `Essential_media`, `Essential_Abscess`, `Essential_Skin`,
  `Shared_Essential` (conditionally-required genes not important in MHB).

## Column layout
- **Data_Sheet_1 / `T0_PAO1_essential_genes`:** header on **row index 1** (title row 0):
  `Locus Tag` | `PA14 locus tag` | `Gene Name` | `Description` | `Called Essential by` |
  `Poulsen et al. 2019 (PA14)` | `Lee et al. 2015 (PAO1)` | `Turner et al 2015 (PAO1)` |
  `Turner et al 2015 (PA14)` | `Skurnik et al 2…` | … (cross-study +/- columns).
- **Data_Sheet_2 (all sheets):** **TWO-ROW header** — row 1 has group label
  `Essential in`, row 2 has the sub-conditions (e.g. `RPMI/Serum` | `RPMI` | `Abscess`
  | `Skin`); columns before that are `Locus Tag` | `Gene Name` | `Functional Class`.
  Cell values: `Tradis` / `Transit` / `Both` / `NE` (which Tn-seq analysis tool called
  the gene essential in that condition; NE = not essential).

## Likely columns
- **gene ID / locus tag:** `Locus Tag` (PAO1 `PAxxxx`). `PA14 locus tag` = cross-ref only.
- **strain:** none (PAO1 constant).
- **condition / media:** DS2 sub-condition columns (`RPMI/Serum`, `RPMI`, `Abscess`,
  `Skin`); DS1 baseline condition = MHB (rich medium, T0).
- **essentiality:** DS1 membership = essential in MHB; `Called Essential by`
  (Tradis/Transit). DS2 per-condition `Tradis`/`Transit`/`Both`/`NE`.
- **threshold / statistics:** two Tn-seq analysis tools (TraDIS + Transit); "Both" =
  called by both. The numeric cutoffs live in the paper methods — record per row.

## Direct PAO1 mapping status
**YES** — native PAO1 `PAxxxx`.

## Source-locator strategy
`source_file` + `source_sheet` + `source_row` + `Locus Tag`.

## Uncertainty notes
- **Two-row header in Data_Sheet_2** — must merge rows 1–2 to name the condition
  columns, or condition labels will be lost/misaligned.
- The DS1 cross-study +/- columns (Poulsen/Lee/Turner/Skurnik) are **re-cited prior
  results**, NOT new Belanger labels — do **not** ingest them as independent evidence.
- Meaning of `Tradis`/`Transit`/`Both`/`NE` → phenotype mapping needs confirmation
  (does a single-tool call count as essential?).

## Parse-readiness
- Data_Sheet_1 `T0_PAO1_essential_genes` (generally-essential, MHB): **READY_FOR_L03_PARSE**.
- Data_Sheet_2 (condition/host): **NEEDS_HUMAN_REVIEW** (merge 2-row header; confirm
  Tradis/Transit/Both/NE → essential/phenotype rule).
- Data_Sheet_3.docx: **NEEDS_HUMAN_REVIEW** (not machine-parsed here).

## Extraction plan (next script)
1. DS1 T0 sheet `header=1` → `Locus Tag`, `Gene Name`, `Called Essential by`; emit
   generally-essential (condition=MHB). Ignore the cross-study citation columns.
2. DS2: read with a **2-row header merge**; for each condition column emit a
   condition-specific row (RPMI/serum = condition-specific-essential; abscess/skin =
   host-condition-fitness) with the tool call recorded.
3. Optionally use `Excluded` as a no-TA-site mask (genes not testable).
4. Keep conditions + phenotype classes distinct; record strain=PAO1, method=Tn-seq(TraDIS/Transit).

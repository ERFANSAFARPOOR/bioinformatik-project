# THRESHOLD_METHOD_AUDIT.md

**Date:** 2026-07-06 · **Branch:** `claude/revival-audit` · **Env:** `reccobra39`
**Purpose:** Source, per study, the exact essentiality **definition + numeric
threshold + statistical rule** from Methods / Supplementary Methods / author
documentation — the missing piece that gated L-03 (Hard Rule 6). Extraction was
**read-only** from `papers/*.pdf` and the in-repo supplement PDFs via
`scripts/literature/pdf_text.py` (stdlib FlateDecode text recovery — approximate;
quoted phrases lightly de-spaced from the tagged-PDF text stream). No raw file
was modified. Thresholds are sourced from **Methods**, not inferred from column
names.

Readiness legend: `READY_FOR_DRAFT_PARSE` · `PARTIAL_READY` · `STILL_BLOCKED`.

---

## lee2015 — Lee et al. 2015, PNAS 112(16):5189–5194

- **study_id:** lee2015
- **citation status:** VERIFIED (corpus; DOI 10.1073/pnas.1422186112, PMID 25848053).
- **strain:** MPAO1 (native PAO1 `PAxxxx` locus tags; PAO1-UW annotation NC_002516).
- **source files inspected:** `papers/lee2015.pdf` (main),
  `data/raw/literature/lee2015/Supporting Information.pdf` (SI M&M),
  `data/raw/literature/lee2015/pnas.1422186112.sd01.xlsx`.
- **essentiality definition (sourced):** Tn-seq. Reads normalized to 10,000,000
  per pool. *Genes with zero hits/reads = essential.* Remaining reads-per-gene
  and hits-per-gene values are log2-transformed and fit to a normal distribution;
  *"Loci with values falling below a P = 0.001 cut-off for each distribution were
  added to the 0-value set for the final set of candidate essential loci for the
  corresponding Tn-seq run"* (SI, *Sequence Data Analysis*). Fig. S3: *"A gene was
  classified as a candidate essential … if the x-axis value was less than 6.3
  (P < 0.001)."*
- **numeric threshold / statistical rule:**
  - Per run: zero-read OR below **P = 0.001** (log2-normal fit).
  - **Consensus per condition** (SI): *"genes found for at least two of three LB
    pools, two of three MOPS-pyruvate pools, or three of four sputum agar pools."*
    Main text: *"Genes falling in this region for more than half of the
    independent mutant pools prepared per condition were considered to be
    confirmed essentials."*
  - Single-pool additional media (BHI, 0.1× LB, serum agar): candidate-essential
    in that one run.
- **replicate rule:** LB-1 = ≥2 of 3 technical assays; LB-2 = ≥1 of 2. General
  essentials = consensus across the three primary media (LB, MOPS-pyruvate,
  sputum). *"329 general essential coding genes"*; +22 domain +1 unannotated =
  **352** including essential domains.
- **author-provided calls directly usable?** YES for **general essential**
  (sheet membership = author call). Per-medium condition calls: the sheet gives
  the raw `sum (of N)` counts, but the mapping of the SI "pools" rule onto the
  `of 6 / of 3 / of 4` **assay** columns is an interpretation → flag NEEDS_REVIEW.
- **supplement sheets/columns:** `sd01` → `General essential genes` (membership =
  generally-essential) and `All essential genes` (per-medium `LB sum (of 6)`,
  `Min sum (of 3)`, `Sputum sum (of 4)`, `BHI (of 1)`, `0.1X LB (of 1)`,
  `Serum (of 1)`; gene col `PA number`). Header on Excel row 2. Media codes
  (Table S3): 1=LB, 2=MOPS-pyruvate, 3=sputum agar, 4=0.1× LB, 5=serum, 6=BHI.
- **interpretation rule for parsing:** general essential = membership in
  `General essential genes` (READY). Condition-specific = per-medium `sum ≥`
  {LB 4/6, Min 2/3, Sputum 3/4, singles 1/1}, recorded with the raw sum and
  flagged NEEDS_REVIEW.
- **exclusions:** `Essential noncoding regions` sheet (sRNA/intergenic gaps,
  150-bp gap-size rule) is **excluded** from gene-level evidence per instruction.
- **unresolved uncertainties:** exact pool↔assay correspondence of the
  `of 6/3/4` columns; MPAO1 vs PAO1-UW divergent loci (few indels/SNPs).
- **L-03 readiness:** **READY_FOR_DRAFT_PARSE** (general essential = READY;
  per-medium condition = PARTIAL, emitted as NEEDS_REVIEW). Resolves **L03-B1**.

---

## turner2015 — Turner et al. 2015, PNAS 112(13):4110–4115

- **study_id:** turner2015
- **citation status:** VERIFIED (corpus; DOI 10.1073/pnas.1419677112, PMID 25775563).
- **strain:** PAO1 + PA14. **Only PAO1 columns parsed** (identity join); PA14
  columns excluded (would need study-provided 1:1 orthology; L03-B3).
- **source files inspected:** `papers/turner2015.pdf` (main text incl. Essential
  Gene Analysis); `sd01, sd06, sd07, sd10` (PAO1 single-strain sheets).
- **essentiality definition (sourced):** *"a Monte Carlo simulation-based
  method."* Insertions and read counts are placed randomly on the chromosome
  under the null (*"no gene is essential and all insertions impart no fitness
  cost"*); *"repeated this simulation process 2,000 times … generating an
  estimate of the variance to be expected from … fitness-neutral Tn-seq data,"*
  then observed vs expected mutant abundance tested with **DESeq** (negative
  binomial). Genes are clustered on fold-change-vs-expected with R **mclust**
  into two modes.
- **numeric threshold / statistical rule (Essential? call):** *"any gene that had
  significantly lower mutant abundance than expected (**P < 0.01, negative
  binomial test**) and that clustered in the second of the two categories …
  (**P < 0.01, maximum likelihood estimation**) was deemed essential."* Result:
  **336 of 5,606 PAO1 genes** (Dataset S1). The **`Mode`** column = mclust
  category (essential-like vs neutral); **`Essential?`** = the author call.
- **fitness / condition comparisons (sd06/07/09/10):** direct comparison of
  mutant abundance between conditions; significant if **fold change ≥ 4 and
  P < 0.05 (negative binomial test)** (e.g. MOPS-sputum: 197 genes decreased,
  *"P < 0.05, negative binomial test, fold change greater than or equal to
  four"*; SCFM2 vs MOPS-sputum: 2 genes).
- **replicate/per-condition rule:** conditions encoded by table/column, not a
  strain column. sd01 initial library = generally-essential; sd06/07 = CF sputum
  vs MOPS-succinate fitness; sd10 = sputum & **murine chronic wound** (host).
- **author-provided calls directly usable?** YES — `Essential?` (sd01) and the
  fold-change/P columns are author outputs with the definition above.
- **supplement sheets/columns:** sd01 initial block cols `Locus ID`, `Gene`,
  `Log2 Fold Change (Initial/Expected)`, `P (Fold Change)`, `Mode`, `P (Mode)`,
  `Essential?` (header Excel row 2, sub-header row 3, data row 4). sd06/07/10:
  `Locus ID`, `Gene`, `Fold Change Mutant Abundance`, `P`.
- **interpretation rule for parsing:** sd01 → generally-essential where
  `Essential?`=='Essential' (initial block). sd06/sd07 → reduced-fitness where
  |FC|≥4 & P<0.05. sd10 block-2 → host-condition-fitness (chronic wound) where
  |FC|≥4 & P<0.05.
- **unresolved uncertainties:** paired PAO1+PA14 sheets **sd03/sd04/sd05/sd09**
  need PAO1 column-block confirmation before extraction (**L03-B3 STILL OPEN**);
  sd02 (QC) and sd08 (SCFM2 media recipe → C-01b) are not gene labels.
- **L-03 readiness:** **READY_FOR_DRAFT_PARSE** for PAO1 single-strain sheets
  (sd01/06/07/10). Resolves **L03-B2**; **L03-B3 remains OPEN** for paired sheets.

---

## belanger2022 — Belanger et al. 2022, Front. Microbiol. 13:1055512

- **study_id:** belanger2022
- **citation status:** VERIFIED (corpus; DOI 10.3389/fmicb.2022.1055512, PMID 36504765).
- **strain:** PAO1 (native `PAxxxx`; `PA14 locus tag` cross-ref only).
- **source files inspected:** `papers/belanger2022.pdf` (tagged PDF; heavily
  letter-spaced — quotes de-spaced), `Data_Sheet_1.XLSX`, `Data_Sheet_2.XLSX`.
- **essentiality definition (sourced):** saturated Himar1 transposon pool + Tn-Seq
  analysed with **two tools**: **TRANSIT** (*"the Gumbel method of Transit for
  calculating the probability of essentiality of each gene using a Bayesian
  model,"* reads per TA site; DeJesus 2015; output Essential/Nonessential) and
  **TraDIS** (reads/gene; assesses insertions per gene; Barquist 2016).
- **numeric threshold / statistical rule:** *"Genes predicted to be essential by
  Gumbel or Tradis in at least **4 out of 5 replicates** (in experimental
  replicates) or **2 out of 3 replicates** (for the T0 pool) were compiled."* A
  gene is essential if called by **either** tool at that replicate threshold; the
  cell value records which — `Tradis`, `Transit`, `Both` (both tools), `NE`
  (not essential). Integrating two tools *"took into account variation … due to
  differing algorithms."*
- **separate statistic (NOT the essential call):** pathway enrichment used
  *"Fischer's exact test with Benjamini/Hochberg correction and a 0.05
  significance threshold"* (PaIntDB ontology) — enrichment only; do not conflate
  with essentiality.
- **per-condition rule:** DS1 `T0_PAO1_essential_genes` = generally-essential (T0
  pool, ≥2/3). DS2 conditional (RPMI/Serum, RPMI, Abscess, Skin cf. MHB), ≥4/5.
- **author-provided calls directly usable?** YES — `Called Essential by` (DS1)
  and the per-condition tool-call cells (DS2). A **single-tool call counts** as
  essential; `Both` ≠ required.
- **supplement sheets/columns:** DS1 `T0_PAO1_essential_genes` (header Excel
  row 2; gene `Locus Tag`; call `Called Essential by`; **ignore** the re-cited
  cross-study ± columns Poulsen/Lee/Turner/Skurnik/Liberati — not Belanger's own
  labels). DS2 `Essential_media`/`Essential_Abscess`/`Essential_Skin`/
  `Shared_Essential`: **two-row header** (row 1 group `Essential in`, row 2
  sub-conditions) and the **condition column order differs per sheet** → the
  parser reads the row-2 sub-headers to map columns (L03-B5 handled).
- **interpretation rule for parsing:** DS1 → generally-essential (essential in
  MHB/LB T0). DS2 → per (gene, condition) where cell ≠ NE/blank: RPMI & RPMI/Serum
  = condition-specific-essential; Abscess & Skin = host-condition-fitness. Dedupe
  (gene, condition) across the four overlapping sheets.
- **unresolved uncertainties:** the paper uses **LB** (pool generation; Table 1)
  and **MHB** (figure baselines) for the rich-medium baseline — recorded as
  "LB / MHB baseline" with a note. `Excluded` sheet (0 TA sites) is a
  non-testable mask, not evidence.
- **L-03 readiness:** **READY_FOR_DRAFT_PARSE**. Resolves **L03-B4** and
  **L03-B5**.

---

## varadarajan2020 — Varadarajan et al. 2020, npj Biofilms Microbiomes 6:46

- **study_id:** varadarajan2020
- **citation status:** **VERIFIED** this cycle (DOI 10.1038/s41522-020-00154-8,
  PMID 33127897, PMCID PMC7603352) — see `VARADARAJAN2020_CITATION_CHECK.md`.
  Resolves **L03-B6**.
- **strain:** MPAO1 (locus tags `MPAO1_xxxxx`; PAO1 best-hit mapping in DS1/DS3).
- **source files inspected:** `Supplementary Information (MPAO1).pdf`,
  `Supplementary Dataset 1/3/4 (MPAO1).xlsx`.
- **essentiality definition (sourced) — CRITICAL FINDING:** DS4
  `essentialGenes_MPAO1` is **not an independent screen.** The SI states:
  *"Using the scripts released by Lee and colleagues [3], Tn-seq data were
  re-mapped to our complete MPAO1 genome and compared with data published, i.e.,
  the set of genes essential in either one of the three conditions sputum,
  minimal medium and LB medium (577 all essential genes), as well as the 312
  genes essential in all 3 categories (general essential genes)."* The **16
  Tn-seq samples** (Supplementary Table 3: `LB-1_Rep1/2/3`, …, `0.1XLB`, `BHI`,
  sputum, minimal) are **Lee 2015's own libraries** (refs [3]=Lee, [4]=Turner)
  re-mapped to MPAO1. The threshold column is *"in how many of the 16 samples a
  respective gene was called essential"* using **Lee's** P<0.001 method.
- **numeric threshold:** essential in N of 16 samples (Lee's per-run P<0.001);
  577 all-essential / 312 general-essential subsets = Lee's calls re-mapped.
- **author-provided calls directly usable as INDEPENDENT evidence?** **NO.** DS4
  essentiality is derivative of Lee 2015 → parsing it as evidence would
  **double-count Lee** (the same defect that makes zhu2018 `additionalFile19`
  out-of-scope). The genuinely novel content (≈136 MPAO1-unique genes, 6
  MPAO1-unique general-essential) has **no PAO1 homolog** → cannot map to the
  PAO1 iMO1056 model anyway.
- **usable content:** DS1/DS3 provide a native **MPAO1 → PAO1** best-hit mapping
  (`best_hit`/`PAO1_gene_name`) — a legitimate *reference resource* for later
  (retain one-to-many / missing per rule 3), **not** an evidence source.
- **interpretation rule for parsing:** **do NOT parse DS4 as independent
  gene-level evidence.** Optionally build the MPAO1→PAO1 map later as a reference
  table (not this run).
- **unresolved uncertainties:** L03-B7 (MPAO1→PAO1 mapping) may be built later as
  a resource; L03-B8 threshold is Lee-derived (documented above).
- **L-03 readiness:** **STILL_BLOCKED as independent evidence** (derivative of
  Lee 2015). Citation now VERIFIED; usable only as a mapping resource.

---

## zhu2018 — Zhu et al. 2018, GigaScience giy021 (iPAO1)

- **citation status:** PENDING_VERIFY (likely 10.1093/gigascience/giy021,
  PMC6333913). Not verified this cycle (not needed — out of scope).
- **strain / phenotype:** iPAO1 genome-scale metabolic **reconstruction** (a
  *model*), not an experimental essentiality/fitness screen.
- **L-03 readiness:** **STILL_BLOCKED / NOT_RELEVANT_FOR_L03.** `additionalFile19`
  ("Comparison of predicted gene essentiality with transposon insertion mutant
  libraries") is model-derived and draws on the same Lee/Turner Tn-seq data →
  would double-count. Background/model cross-check only; **not parsed**.

---

## Summary

| study | citation | threshold sourced? | L-03 readiness | blockers resolved |
|---|---|---|---|---|
| lee2015 | VERIFIED | YES (P<0.001; consensus pools) | READY_FOR_DRAFT_PARSE (cond=PARTIAL) | L03-B1 |
| turner2015 | VERIFIED | YES (P<0.01 + mclust; FC≥4,P<0.05) | READY_FOR_DRAFT_PARSE (PAO1 sheets) | L03-B2 (L03-B3 open) |
| belanger2022 | VERIFIED | YES (Gumbel/TraDIS ≥4/5, T0 ≥2/3) | READY_FOR_DRAFT_PARSE | L03-B4, L03-B5 |
| varadarajan2020 | VERIFIED | Lee-derived (not independent) | STILL_BLOCKED as evidence (mapping resource only) | L03-B6 (B7/B8 reframed) |
| zhu2018 | PENDING_VERIFY | n/a (model) | NOT_RELEVANT_FOR_L03 | — |

No `THRESHOLD_PENDING` studies remain among those parsed. Metrics remain
**forbidden** (B-SCI-01); this file only sources definitions/thresholds.

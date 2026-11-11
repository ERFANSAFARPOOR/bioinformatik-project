# ORTHOLOG_CANDIDATE_TABLE.md — PAO1↔PA14 candidate ortholog resource

**Original candidate audit:** 2026-07-07 · **Env:** `reccobra39`
**Status reconciled:** 2026-11-11

**Supersession:** the original CANDIDATE measurements below are retained. On
2026-07-10, `ORTHOLOGY_HUMAN_REVIEW_DECISION.md` recorded **APPROVED_LIMITED**
for the derived Turner strict 1:1 table (5,365 pairs) and resolved the PA2279
conflict in favor of Turner. The approved derived file may support controlled
L-03b draft mapping only; the original candidate file was preserved. There is
no automatic Poulsen/Basta metric approval. D-21/V-01 uses
MPAO1→PAO1 DS1 best hits and is a separate completed comparison cell.

Network and missing-export statements below record July 7 attempts; they are
not a new connectivity assessment.

**Observed mapping artifacts (2026-11-11):**
`data/processed/gene_mapping/gene_mapping.csv` uses `official_orthology`; its
coverage report records **1023 unique, 2 ambiguous, 29 unmapped** model genes.
The builder reads the official PGD raw export. The separate
`data/processed/ortholog/final/pao1_pa14_orthologs_pseudomonas_rbh_20260712.csv`
has **5374 pairs** and a `Validation_Report.txt` marked **PASSED** (structural
checks). These artifacts exist and the canonical mapping is no longer merely
the old symbol-based layer. This observed integration does not by itself
establish a reviewed Poulsen/Basta comparison or supersede the documented
D-16 limited-use decision with a new unrestricted approval.


## Why this candidate was built (2026-07-07 snapshot)
G-01b / B-MAP-01 need a validated PAO1↔PA14 locus-tag ortholog table to map the
PA14-indexed studies (Basta 2017; Poulsen 2019, whose nine screened strains exclude PAO1) onto the PAO1
model. The authoritative live source (pseudomonas.com RBBH / Pseudomonas Ortholog
Database) is **unreachable from this environment** — it returns **HTTP 403
(Cloudflare)** both via local `curl` (B-NET) and via the WebFetch path
(re-verified 2026-07-07: `/rbbh/pairs` and the `/downloads/.../orthologs` file both 403).

The strongest source available **locally at that time** was the ortholog table **embedded in the
Turner 2015 peer-reviewed supplement**, which was itself computed from the
Pseudomonas Genome Database (see `LOCAL_ORTHOLOGY_SEARCH_REPORT.md`).

## Source & method (cited)
- **File:** `data/raw/literature/turner2015/pnas.1419677112.sd03.xlsx`
  (SHA-256 `4723c7015d6bd69e2cd0790dd36e92314c02f2c46f738e3fa659c400d197a9e2`),
  sheet `Sheet1`, col A `PA14 Locus ID` ↔ col J `PAO1 Locus ID`, paired row-by-row.
- **Method (Turner 2015 Methods, quoted):** *"precomputed BLAST results and synteny
  information available at the Pseudomonas Genome Database … was used to identify
  5,366 orthologous gene pairs between these two strains."*
- **Vintage:** Pseudomonas Genome Database as of 2015. This is the **1:1 ortholog
  subset** — many-to-one / one-to-many and strain-unique genes are **not** covered.

## Output
`data/processed/ortholog/working/pao1_pa14_orthologs_turner2015_CANDIDATE.csv`
(SHA-256 `e6ea39a5177e1aae4c5a975d96ceb821b9964fcf7c840ce5a82b62e0d51dec90`) —
5,365 pairs, columns:
`pao1_locus_tag, pa14_locus_tag, pao1_gene, pa14_gene, gene_symbol_match,
belanger_crosscheck, source, method, confidence, review_flag`.

## Extraction result (reproducible via `scripts/mapping/build_ortholog_candidate.py`)
- **5,365 explicit 1:1 PA14↔PAO1 pairs** extracted (matches Turner's stated
  "5,366 orthologous gene pairs" less the header artifact).
- **Strict 1:1:** 0 PAO1 locus tags appear more than once; 0 PA14 locus tags appear
  more than once. No one-to-many collapse was introduced.
- **Explicitly excluded (retained as counts, not forced into pairs):**
  **541 PA14-only** rows (no PAO1 ortholog) and **204 PAO1-only** rows.
- **Internal consistency:** the pairing extracted from **sd03** and **sd04**
  (independent Turner tables, sputum vs MOPS-sputum) is **byte-identical**
  (symmetric difference = 0), confirming a stable ortholog assignment.

## Independent cross-check — Belanger 2022 DS1
Belanger `Data_Sheet_1.XLSX` sheet `T0_PAO1_essential_genes` carries its own
PAO1↔PA14 column pair (600 pairs, essential-gene subset, method undocumented).
Against the Turner candidate:
- **598 agree, 1 disagree** out of 599 PAO1 keys shared (**99.8% concordance**).
- **Single disagreement:** `PA2279` → Turner `PA14_35100` vs Belanger `PA14_35130`.
  **Flagged and unresolved in the original candidate audit** — retained in the
  original CSV (`belanger_crosscheck=disagree`). **Resolved 2026-07-10 in favor
  of Turner** by bidirectional KEGG SSDB best-hit evidence in
  `ORTHOLOGY_CONFLICT_RESOLUTION_REPORT.md`; the approved derived table records
  `RESOLVED_SUPPORTS_TURNER`.
- Every row carries `belanger_crosscheck ∈ {agree, disagree, not_in_belanger}` so a
  reviewer can see which pairs have a second independent source.

## Caveats of the Turner candidate (original preserved; D-16 use remains limited)
1. **1:1 subset only.** PA14-unique genes and any one-to-many orthology are absent;
   a study gene outside the 5,365 pairs will map to nothing here — that is a true
   "missing", to be preserved (rule §3), not filled.
2. **2015 vintage** of the Pseudomonas Genome Database; the current release may
   differ. Prefer the live pseudomonas.com export if it ever becomes reachable.
3. **Belanger method undocumented**, so its 600-pair agreement is corroboration,
   not an independent gold standard.
4. The July 10 decision approves a **derived Turner** strict 1:1 table only for
   controlled L-03b drafts. The canonical official-PGD integration observed
   above is a separate artifact; no new unrestricted study-use approval is
   inferred from its presence. A mapped PAO1 coordinate is not a PAO1 experiment.

## What the July 10 limited approval enables

- **G-01b / L-03b:** future controlled draft joins of Basta and Poulsen
  PA14-indexed lists using `approved_for_l03b=yes` strict 1:1 rows. Preserve
  unmapped/strain-unique cases and model-coverage exclusions. Neither source has
  a direct PAO1 identity-join subset; Basta also requires a non-growth phenotype
  framework.
- **B-MAP-01:** narrowed from a missing-source gate to a limited approved source;
  not fully closed for unrestricted cross-strain validation. The 2015 vintage,
  subset coverage, parsing/review and matched-condition limitations remain.
- No Poulsen/Basta validation metrics are unlocked by mapping approval alone.

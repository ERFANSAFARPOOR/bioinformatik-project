# ORTHOLOG_CANDIDATE_TABLE.md — PAO1↔PA14 candidate ortholog resource

**Date:** 2026-07-07 · **Branch:** `claude/revival-audit` · **Env:** `reccobra39`
**Status:** CANDIDATE / HUMAN_REVIEW_REQUIRED — **not merged** into `gene_mapping.csv`,
**not used** to parse Poulsen/Basta or compute any metric. Additive derived resource only.

## Why this exists
G-01b / B-MAP-01 need a validated PAO1↔PA14 locus-tag ortholog table to map the
PA14-indexed studies (Basta 2017; non-PAO1 Poulsen 2019 strains) onto the PAO1
model. The authoritative live source (pseudomonas.com RBBH / Pseudomonas Ortholog
Database) is **unreachable from this environment** — it returns **HTTP 403
(Cloudflare)** both via local `curl` (B-NET) and via the WebFetch path
(re-verified 2026-07-07: `/rbbh/pairs` and the `/downloads/.../orthologs` file both 403).

The strongest source available **locally** is the ortholog table **embedded in the
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
`data/processed/ortholog/pao1_pa14_orthologs_turner2015_CANDIDATE.csv`
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
  **Flagged, not resolved** — recorded in the CSV (`belanger_crosscheck=disagree`)
  and here; needs the authoritative pseudomonas.com entry to adjudicate.
- Every row carries `belanger_crosscheck ∈ {agree, disagree, not_in_belanger}` so a
  reviewer can see which pairs have a second independent source.

## Caveats (why this stays CANDIDATE, not merged)
1. **1:1 subset only.** PA14-unique genes and any one-to-many orthology are absent;
   a study gene outside the 5,365 pairs will map to nothing here — that is a true
   "missing", to be preserved (rule §3), not filled.
2. **2015 vintage** of the Pseudomonas Genome Database; the current release may
   differ. Prefer the live pseudomonas.com export if it ever becomes reachable.
3. **Belanger method undocumented**, so its 600-pair agreement is corroboration,
   not an independent gold standard.
4. Per rules §1/§3 and D-07, this is **not** promoted into `gene_mapping.csv` and
   **not** used to parse Poulsen/Basta until a human approves it as the mapping source.

## What this unblocks (when approved)
- **G-01b:** join Basta 2017 (PA14) and non-PAO1 Poulsen genes to PAO1 model IDs
  via this table, keeping one-to-many/missing explicit.
- **L-03b:** draft-parse Poulsen (sd05/sd02) and Basta once the mapping is approved.
- **B-MAP-01** narrows from "no source exists" to "candidate source built, awaiting
  human sign-off vs. authoritative pseudomonas.com."

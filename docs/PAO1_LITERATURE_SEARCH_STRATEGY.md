# PAO1 LITERATURE SEARCH STRATEGY & RESULTS

**Date:** 2026-07-01 · **Branch:** `claude/revival-audit`
**Tooling:** NCBI E-utilities (esearch/esummary/elink) via
`scripts/audit/pubmed_search.py` (reachable this session). Journal/publisher
supplement pages and PMC full-text package downloads are **blocked** here
(B-NET); only metadata retrieval succeeded.

---

## 1. Objective & priorities

Find additional literature/datasets that support **PAO1 model (iMO1056)
validation**, prioritizing **gene-level PAO1/MPAO1 essentiality/fitness data**.
Do **not** add papers merely to increase count.

## 2. Search terms (executed)

`PAO1 essential genes Tn-seq` · `MPAO1 essential genes` · `PAO1 transposon
sequencing fitness` · `PAO1 condition-specific essential genes` · `PAO1
genome-scale metabolic model` · `iMO1056` · `PAO1 FBA gene essentiality` · `PAO1
deletion library metabolic genes` · `PAO1 CRISPRi essential` · `PAO1 TraDIS`
(all prefixed *Pseudomonas aeruginosa*).

## 3. Sources

Executed: **PubMed** (+ **PMC** open-access check, **CrossRef/DOI** via eutils
articleids). Intended but **blocked/deferred** (B-NET): Europe PMC full text,
publisher supplement pages (PNAS/Frontiers/mBio), NCBI GEO/SRA, Zenodo/Figshare/
Dryad, pseudomonas.com, BioModels/BiGG browsing. GitHub/Broad portals reachable
in principle but not fetched this cycle.

## 4. Inclusion / exclusion criteria (applied)

- **Tier 1** PAO1/MPAO1 gene-level essentiality/fitness (Tn-seq/TraDIS/CRISPRi/
  deletion library).
- **Tier 2** PAO1 genome-scale metabolic model / iMO1056 reconstruction, FBA
  essentiality, medium reconstruction.
- **Tier 3** mixed PAO1/PA14 with explicit PAO1 rows or validated orthology.
- **Tier 4/defer** PA14-only / multi-strain background; transcriptomics-only
  (unless it helps media/condition reconstruction); broad reviews (intro only).

## 5. Results — candidate new items (verified metadata)

### Tier 1 — PAO1/MPAO1 gene-level (highest priority)

| PMID | Year | Journal | DOI | OA? | Note |
|---|---|---|---|---|---|
| 35104681 | 2022 | Infect Genet Evol | 10.1016/j.meegid.2022.105231 | **no** (not in PMC OA) | *Genome-wide identification of genetic requirements of P. aeruginosa **PAO1** for rat cardiomyocyte (H9C2) infection by **insertion sequencing**.* Direct PAO1 Tn-seq, host-infection condition. **Strong Tier 1 candidate**; full text/supplement not retrievable here → citation-only, needs human-assisted download. |

*(The two existing PAO1/mixed sources — Turner 2015, Belanger 2022 — reappear in
these queries and are already in the corpus.)*

### Tier 2 — PAO1 metabolic models / FBA (background & comparison)

| PMID | Year | Journal | DOI | OA? | Note |
|---|---|---|---|---|---|
| 18192387 | 2008 | J Bacteriol | 10.1128/JB.01583-07 | no (PMC2293256 **not** OA) | **Oberhardt et al. 2008 — the source paper for iMO1056** (the model in this repo). Citation-only here; PDF not lawfully downloadable from this environment. |
| 28266498 | 2017 | Nat Commun | 10.1038/ncomms14631 | yes (PMC5344303) | Bartell et al. — reconstruction of the P. aeruginosa metabolic network (virulence-factor synthesis); an alternative/newer PAO1 GEM for comparison/discussion. OA package exists but download blocked here (ftp scheme denied / https path 404). |
| 29688451 | 2018 | GigaScience | 10.1093/gigascience/giy021 | yes (PMC6333913) | GEM of responses to polymyxins in P. aeruginosa (PAO1-based). Tier 2 application/comparison. OA; download blocked here. |
| 20233082 | 2011 | J Drug Target | 10.3109/10611861003649753 | no | FBA of a reconstructed PAO1 GEM to find drug targets (gene/reaction essentiality by FBA). Tier 2 methodological comparison. |
| 24707203 | 2014 | ScientificWorldJournal | 10.1155/2014/416289 | yes (PMC3953581) | FBA comparison across Pseudomonas species; benchmarking GEM prediction quality. Tier 2 background. |
| 37233700 | 2023 | Metabolites | 10.3390/metabo13050659 | yes (PMC10224149) | Systems-biology / QS influence on PAO1 metabolism (pyoverdine); references iMO1056-family models. Tier 2 background. |

### Tier 2 (reference-genome context) / defer

| PMID | Year | Journal | DOI | Note |
|---|---|---|---|---|
| 33972355 | 2021 | J Bacteriol | 10.1128/JB.00179-21 | *Reconstructing a Wild-Type P. aeruginosa Reference Strain PAO1* — useful for PAO1/MPAO1 reference-genome caveats (supports strain-mapping notes). Background. |
| 33127897 | 2020 | NPJ Biofilms Microbiomes | 10.1038/s41522-020-00154-8 | **MPAO1** biofilm-AMR model system; not gene-level essentiality → **defer** (Tier 4/6 background). |

### Excluded (off-scope for the queries that returned them)

Multiple hits were single-gene/mechanistic virulence, resistance-plasmid, or
transcription-profiling papers with **no genome-wide PAO1 essentiality/fitness
table** (e.g. PMID 37879457, 18301762, 18448680, 32012489, 29784885, 21170272,
27190289, 21075931, 8106324, 36579125, 36312952). Not included — they do not add
validation labels and were not selected merely to inflate count.

## 6. Download status (Part F)

**No new full-text PDF or supplement was downloadable in this environment.**
- eutils metadata (PMID/PMCID/DOI/title/journal/year): **retrieved** (reliable).
- PMC OA package fetch: `ftp://ftp.ncbi.nlm.nih.gov/...` → access denied (curl
  exit 9); `https://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_package/...` → *Object not
  found*. Publisher supplement pages (PNAS/Frontiers/mBio) remain 403/unreachable.
- Recorded in `BLOCKERS.md` (B-NET, extended) and `DATA_PROVENANCE.md`.

## 7. Recommended next actions (human-assisted / different network)

1. **Highest value:** obtain **meegid 2022 (PMID 35104681)** full text +
   supplement — a direct PAO1 insertion-sequencing dataset (host-infection
   condition), gene-level, PAO1 locus tags → Tier 1.
2. Download the **existing corpus supplements** (Turner sd01–04, Lee sd01,
   Belanger supp) — now known to include **PAO1/MPAO1** labels (no orthology
   needed). See `PAO1_PAPER_RELEVANCE_AUDIT.md`.
3. Retrieve **Oberhardt 2008** (model source) for methods/medium details.
4. Optional Tier 2: Bartell 2017 / GigaScience 2018 GEMs for comparison.
5. Store PDFs in `papers/`, supplements in `data/raw/literature/<study_id>/`,
   record provenance + SHA-256, and add per-study `SUPPLEMENT_PARSE_NOTES.md`.

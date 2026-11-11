# PAO1 LITERATURE SEARCH STRATEGY & RESULTS

**Search date:** 2026-07-01 · **Branch at search:** `claude/revival-audit`
**Tooling:** NCBI E-utilities (esearch/esummary/elink) via
`scripts/audit/pubmed_search.py` (reachable this session). Journal/publisher
supplement pages and PMC full-text package downloads are **blocked** here
(B-NET); only metadata retrieval succeeded in that search cycle.

**Current-status reconciliation (2026-11-11):** the search/download outcomes
below are historical. Corpus supplements are now present. D-21 approved
Varadarajan2020 DS1+DS4 as Lee-derived experimental binary labels for Minimal /
MOPS-pyruvate; V-01 metrics have been computed (1025 genes), with FP/FN
interpretation pending. Varadarajan is not independent replication. The local
PGD export is present. The current builder already uses it and
`data/processed/gene_mapping/gene_mapping.csv` contains official-orthology
results (1023 unique, 2 ambiguous and 29 unmapped model genes). A 5374-pair RBH
file and passing structural report also exist under
`data/processed/ortholog/final/`. These are observed artifacts, not a recorded
unrestricted scientific-use approval. Turner retains `APPROVED_LIMITED` scope
for controlled L-03b drafts; the D-16 review/approval gap must be reconciled
before broader PA14 evidence promotion. See `DECISIONS.md` and
`VALIDATION_LABEL_MEDIA_OVERLAP.md` at root.

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

> **meegid2022 (PMID 35104681) removed from active scope by user decision
> 2026-07-06** — no local files; no validation dependency. (Formerly listed here
> as a Tier 1 candidate PAO1 insertion-sequencing host-infection dataset.)

*(The existing PAO1/mixed sources — Turner 2015, Belanger 2022 — reappear in
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
| 33127897 | 2020 | NPJ Biofilms Microbiomes | 10.1038/s41522-020-00154-8 | **MPAO1** model system including a gene-level remap of Lee2015 Tn-seq. D-21 uses DS1+DS4 for the primary Minimal binary labels; derivative evidence, never an independent screen. Supersedes the initial background-only classification. |

### Excluded (off-scope for the queries that returned them)

Multiple hits were single-gene/mechanistic virulence, resistance-plasmid, or
transcription-profiling papers with **no genome-wide PAO1 essentiality/fitness
table** (e.g. PMID 37879457, 18301762, 18448680, 32012489, 29784885, 21170272,
27190289, 21075931, 8106324, 36579125, 36312952). Not included — they do not add
validation labels and were not selected merely to inflate count.

## 6. Download status (Part F)

**Historical 2026-07-01 outcome: no new full-text PDF or supplement was downloadable in that search cycle.**
- eutils metadata (PMID/PMCID/DOI/title/journal/year): **retrieved** (reliable).
- PMC OA package fetch: `ftp://ftp.ncbi.nlm.nih.gov/...` → access denied (curl
  exit 9); `https://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_package/...` → *Object not
  found*. Publisher supplement pages (PNAS/Frontiers/mBio) remain 403/unreachable.
- Recorded in `BLOCKERS.md` (B-NET, extended) and `DATA_PROVENANCE.md`.

## 7. Follow-up status (reconciled 2026-11-11)

1. All corpus supplements are now present (Lee, Turner, Belanger, Varadarajan,
   Poulsen, Basta). (meegid2022 removed from active scope by user decision
   2026-07-06 — no longer a target.)
2. PGD PAO1↔PA14 export is now present at
   `data/raw/ortholog/pao1_pa14_orthologs_pseudomonas.csv` and official mapping
   has already been generated at `data/processed/gene_mapping/gene_mapping.csv`.
   Reconcile these artifacts and RBH structural checks with the recorded D-16
   scope/review before broader PA14 evidence promotion; acquisition is no
   longer the blocker.
3. Retrieve **Oberhardt 2008** (model source) for methods/medium details.
4. Optional Tier 2: Bartell 2017 / GigaScience 2018 GEMs for comparison.
5. Store PDFs in `papers/`, supplements in `data/raw/literature/<study_id>/`,
   record provenance + SHA-256, and add per-study `SUPPLEMENT_PARSE_NOTES.md`.

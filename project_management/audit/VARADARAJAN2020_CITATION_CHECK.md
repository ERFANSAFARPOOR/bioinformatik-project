# VARADARAJAN2020_CITATION_CHECK.md

**Date:** 2026-07-06 · **Branch:** `claude/revival-audit` · Resolves **L03-B6**.
**Goal:** verify the citation of the unlabelled `varadarajan2020` supplement
folder before any use. Metadata retrieval works from this environment (NCBI
eutils + CrossRef reachable; see B-NET). No gene rows were parsed as evidence
from this study (see below and `THRESHOLD_METHOD_AUDIT.md`).

## Queries used
1. NCBI eutils esearch (PubMed):
   `term = Varadarajan+Pseudomonas+aeruginosa+essential+MPAO1` → **1 hit**, PMID
   **33127897**.
2. NCBI eutils esummary (PubMed, id 33127897).
3. NCBI eutils efetch (abstract, id 33127897).
4. CrossRef works API: `https://api.crossref.org/works/10.1038/s41522-020-00154-8`.

## Sources checked
- NCBI E-utilities (esearch/esummary/efetch) — PubMed.
- CrossRef REST API — DOI record.

## Result (all fields agree across NCBI + CrossRef)
| Field | Value |
|---|---|
| **Title** | An integrated model system to gain mechanistic insights into biofilm-associated antimicrobial resistance in *Pseudomonas aeruginosa* MPAO1 |
| **First author** | Adithi R. Varadarajan (Varadarajan AR) |
| **Authors** | Varadarajan AR, Allan RN, Valentin JDP, Castañeda Ocampo OE, Somerville V, Pietsch F, Buhmann MT, West J, Skipp PJ, van der Mei HC, Ren Q, Schreiber F, Webb JS, Ahrens CH |
| **Year** | 2020 (published 2020-10-30) |
| **Journal** | npj Biofilms and Microbiomes (NPJ Biofilms Microbiomes) |
| **Volume / issue / article** | 6(1):46 |
| **DOI** | 10.1038/s41522-020-00154-8 |
| **PMID** | 33127897 |
| **PMCID** | PMC7603352 |

## Match to local files and supplement contents
Strong, corroborated match:
- Strain **MPAO1** matches the folder + all `Supplementary Dataset 1–4 (MPAO1)`
  filenames and locus-tag system (`MPAO1_xxxxx`).
- Abstract: *"MPAO1 is the parental strain of the widely utilized transposon
  mutant collection … identify unique and conserved genes by comparative genomics
  with the PAO1 reference strain … Among over 200 unique MPAO1 genes, we
  identified six general essential genes …"* — matches DS1 (`MPAO1_CDS` +
  comparative genomics vs PAO1), DS3 (`Unique_MPAO1_CDS`, `Core_CDS_MPAO1_PAO1`,
  `essential?`), and the SI's "6 MPAO1-unique general essential genes."
- The SI's 16-sample Tn-seq re-mapping and 577/312 essential subsets match DS4
  `essentialGenes_MPAO1` (`Essential in x/16 samples`).

## Final status
**VERIFIED.**

## Consequences (recorded; applied conservatively)
- Citation may now be recorded. It **can** be added to `papers/manifest.csv` as a
  verified reference (a new study beyond the original 6-paper corpus). *No PDF of
  the article body is in the repo* (only the two supplement PDFs), so any manifest
  addition must mark the body as not-in-repo.
- **Do NOT parse DS4 essentiality as independent evidence.** The SI states the
  essentiality was produced by *re-mapping Lee et al. 2015's public Tn-seq data*
  onto the MPAO1 genome using Lee's own scripts — it is **derivative of Lee 2015**
  and would double-count. See `THRESHOLD_METHOD_AUDIT.md` (varadarajan2020) and
  `L03_PARSE_BLOCKERS.md`.
- The MPAO1→PAO1 best-hit mapping (DS1/DS3) is a legitimate future **reference
  resource** (not evidence). MPAO1-unique genes have no PAO1 homolog and cannot
  map to the PAO1 iMO1056 model.
- `SOURCE_URL_PENDING` retained for the downloaded supplement files (the DOI/PMID
  above are verified identifiers, not the download URLs).

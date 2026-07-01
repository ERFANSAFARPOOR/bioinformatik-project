# DATA PROVENANCE

Provenance of every model, dataset, and document. Phase A records what is
*present and verifiable*; download provenance for supplements is PENDING until
files are actually retrieved (B-LIT-01).

---

## 1. Metabolic model

| Field | Value |
|---|---|
| File | `models/paeruginosa_MODEL1507180020.xml` |
| SHA-256 | `0868a5ebb41ebb4967c3c182e686eca7552af9255cba5a6d130cf114d1212ead` |
| Size | 1,668,096 bytes |
| Identity | **iMO1056** — Oberhardt MA, Puchałka J, Fryer KE, Martins dos Santos VAP, Papin JA (2008) *Genome-scale metabolic network analysis of the opportunistic pathogen Pseudomonas aeruginosa PAO1.* J Bacteriol 190(8):2790-2803. |
| Repository id | BioModels `MODEL1507180020` (model annotation `biomodels.db`) |
| Strain | PAO1 (locus tags `PAxxxx`) |
| Format | SBML L3 V1 + fbc |
| Retrieved | Present in repo at audit; original download date/source URL **not recorded by prior author** — PENDING (recommend documenting BioModels URL). |
| License | Verify BioModels terms before redistribution (PENDING). |

> Models README previously mentioned "iPae1146 (BiGG)" — a *different* model that
> does NOT match the loaded file. **Corrected 2026-07-01** (`models/README.md` now
> states iMO1056/PAO1). A byte-identical raw copy is archived at
> `models/raw/paeruginosa_MODEL1507180020.xml` (same SHA-256).

---

## 2. Literature PDFs (canonical `papers/`; legacy `conditian/`)

Identified via embedded PDF metadata (Info dict `/Title`,`/Author`), XMP, and
DOIs decompressed from PDF streams (read-only; script `identify_pdfs.py`), then
re-audited from direct PDF text (`extract_strain_evidence.py`) and verified via
NCBI eutils. See `papers/manifest.csv` for the machine-readable manifest.

**`papers/` is the canonical location** for the corpus; **`conditian/` is legacy,
preserved untouched** (byte-identical copies; do not edit — see §2b). Strain and
year/DOI values below are the **corrected 2026-07-01 audit** (B-STRAIN-02).

| papers/ file (legacy) | Study | First author | Year | DOI | Journal | Strain (corrected) | ID confidence | Provenance |
|---|---|---|---|---|---|---|---|---|
| `papers/juhas2015.pdf` (`conditian/juhas2015.pdf`) | *P. aeruginosa* essentials: an update on investigation of essential genes | Juhas | 2015 | 10.1099/mic.0.000161 | Microbiology | **review** | high (DOI in stream) | provided in repo |
| `papers/turner2015.pdf` (`conditian/keith H.pdf`) | Essential genome of *P. aeruginosa* in cystic fibrosis sputum | Turner | 2015 | 10.1073/pnas.1419677112 | PNAS | **PAO1 + PA14** | high (DOI+supp in /Title) | provided in repo |
| `papers/lee2015.pdf` (`conditian/samuelA.pdf`) | General and condition-specific essential functions of *P. aeruginosa* | Lee | 2015 | 10.1073/pnas.1422186112 | PNAS | **MPAO1** (PAO1-derived) | high (DOI in headers) | provided in repo |
| `papers/poulsen2019.pdf` (`conditian/polsun2019.pdf`) | Defining the core essential genome of *P. aeruginosa* | Poulsen | 2019 | 10.1073/pnas.1900570116 | PNAS | **multi-strain (incl. PAO1)** | high (DOI+title in /Title) | provided in repo |
| `papers/basta2017.pdf` (`conditian/davidW.pdf`) | Identification of fitness determinants during energy-limited growth arrest | Basta | 2017 | 10.1128/mBio.01170-17 | mBio | **PA14** (UCBPP-PA14) | high (verified) | provided in repo |
| `papers/belanger2022.pdf` (`conditian/corrieR.pdf`) | Surviving the host: metabolic genes required in physiologically-relevant conditions | Belanger | 2022 | 10.3389/fmicb.2022.1055512 | Front Microbiol | **PAO1** | high (verified) | provided in repo |

Filename→author inference (do not over-trust filenames; confirmed by metadata):
`keith H` = Keith H. Turner · `samuelA` = (S.A.) Lee · `polsun` = Poulsen ·
`davidW` = David W. Basta · `corrieR` = Corrie/Hancock lab (Belanger).

### 2b. Canonical `papers/` copies + verified IDs (2026-07-01)

The 6 PDFs were **copied** (not moved) `conditian/* → papers/<study>.pdf`, each
SHA-256-verified byte-identical; **`conditian/` left untouched (legacy, preserved).
`papers/` is canonical.** Strains re-audited from direct PDF text
(`scripts/audit/extract_strain_evidence.py`) and IDs verified via NCBI eutils.
See `papers/manifest.csv`, `PAO1_PAPER_RELEVANCE_AUDIT.md`.

| papers/ file | Study | PMID | PMCID | Strain (corrected) | Tier | SHA-256 (copy) |
|---|---|---|---|---|---|---|
| `papers/juhas2015.pdf` | Juhas 2015 | 26311069 | PMC10960635 | review | 6 | `5a8ae3a755fbbd840842cc537bd6d16c08aa66a6017a9005ae21b41a8d7cd83a` |
| `papers/turner2015.pdf` | Turner 2015 | 25775563 | PMC4386324 | **PAO1+PA14** | 3 | `71b943435a8808e212ce8d0b353532b24d2cdb64491f9ef4405c07933ad6fb10` |
| `papers/lee2015.pdf` | Lee 2015 | 25848053 | PMC4413342 | **MPAO1** | 2 | `f046b9d875b006dd75b0ce09f8b3c0442547be583d7595038640ceba91b14090` |
| `papers/poulsen2019.pdf` | Poulsen 2019 | 31036669 | PMC6525520 | multi (incl PAO1) | 3/5 | `408b627032e3297d1e69056553ffe13002218ff1313f96b7783650b98da1801c` |
| `papers/basta2017.pdf` | Basta 2017 | 29184024 | PMC5705914 | **PA14** | 4 | `097a0fd57ebd5bcad63b0d7be94f4fcdbaa887d7ddb1654ee965b7dbd6d5d23d` |
| `papers/belanger2022.pdf` | Belanger 2022 | 36504765 | PMC9732424 | **PAO1** | 1 | `f1bb27065624b43e553f53dca43e28b80c35c05e6d5306423179f10be22f011e` |

**Strain corrections applied 2026-07-01 (now also reflected in §2):** Turner
PA14→**PAO1+PA14**; Lee PA14→**MPAO1**; Basta/Belanger years+strains verified
(Basta 2017 PA14; Belanger 2022 PAO1). These supersede the earlier preliminary
labels; see B-STRAIN-02.

---

## 3. Supplementary datasets — download attempts (2026-06-26)

Network egress from this environment is **restricted**: NCBI FTP and GitHub work;
journal sites and pseudomonas.com are blocked. See BLOCKER **B-NET**.

| Study | Supplement(s) | Source | Attempt result |
|---|---|---|---|
| Turner 2015 | `pnas.1419677112.sd01–sd04.xlsx` | pnas.org DCSupplemental | **403 Forbidden** (bot block) — PENDING |
| Lee 2015 | `pnas.1422186112.sd01.xlsx` | pnas.org DCSupplemental | **403 Forbidden** — PENDING |
| Poulsen 2019 | fitness data / FiTnEss code | `data.broadinstitute.org/fitness/` (HTTP 200, reachable); `github.com/broadinstitute/FiTnEss` (200) | Reachable but repo holds the **method**, not the P. aeruginosa core-essential gene list; specific list files PENDING |
| Basta 2017 | TBD | mBio / PMC5705914 | PENDING |
| Belanger 2022 | TBD | Frontiers / PMC9732424 | PENDING |

`data/raw/literature/<study_id>/` dirs created for when these are retrieved
(human-assisted download or different network). Never edit raw supplements in place.

## 3b. Ortholog / annotation resources — downloaded (2026-06-26)

| File | Source URL | Retrieved | SHA-256 | Notes |
|---|---|---|---|---|
| `data/raw/ortholog/pao1_feature_table.txt.gz` | https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/006/765/GCF_000006765.1_ASM676v1/GCF_000006765.1_ASM676v1_feature_table.txt.gz | 2026-06-26 | `de6c018f6396fa871da19fa285a6e764a6a7a0cd0b8cd4d8308943c5a1df7abc` | PAO1 RefSeq (ASM676v1); locus_tag = `PA####` (matches model) |
| `data/raw/ortholog/pa14_feature_table.txt.gz` | https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/014/625/GCF_000014625.1_ASM1462v1/GCF_000014625.1_ASM1462v1_feature_table.txt.gz | 2026-06-26 | `e1ac94630b4a5962d433232ac744c0de4cf4898f323bc8d3c75649160d6bc491` | PA14 RefSeq (ASM1462v1); RefSeq locus = `PA14_RS#####`, classic `PA14_#####` in `old_locus_tag` |

These feed `scripts/mapping/build_gene_mapping.py` → `data/processed/gene_mapping.csv`
(the gz is read directly; the uncompressed `.txt` is derived and git-ignored).

## 3c. Literature search + download re-check (2026-07-01)

- **Metadata retrieval WORKS:** NCBI eutils used to verify all corpus PMIDs/PMCIDs
  (§2b) and to run PubMed searches (`scripts/audit/pubmed_search.py`).
- **New candidates found** (see `docs/PAO1_LITERATURE_SEARCH_STRATEGY.md`):
  meegid2022 (PMID 35104681, PAO1 insertion-seq, Tier 1, **not OA**),
  Oberhardt 2008 (PMID 18192387, iMO1056 source, **not OA** — PMC2293256 not in OA
  subset), Bartell 2017 (PMID 28266498, PMC5344303, Tier 2 GEM, OA),
  GigaScience 2018 (PMID 29688451, PMC6333913, Tier 2 GEM, OA).
- **Downloads BLOCKED (B-NET):** PMC OA packages fail via both
  `ftp://ftp.ncbi.nlm.nih.gov/...oa_package/...` (access denied) and the https
  mirror ("Object not found"); PNAS/Frontiers/mBio supplements 403. **No new PDF
  or supplement was retrieved this cycle. Nothing fabricated.**
- Corpus supplements (§3) remain PENDING; priority now PAO1/MPAO1 first
  (Lee, Turner PAO1 rows, Belanger, meegid2022).

> **Caveat:** the PAO1↔PA14 layer built from these is **RefSeq gene-symbol
> identity**, i.e. annotation-based, NOT validated phylogenetic orthology. The
> authoritative ortholog source (pseudomonas.com / OrthologueDB) is unreachable
> (B-NET). Symbol-based PA14 rows are flagged `medium`/`low` confidence with
> candidates retained for ambiguous cases.

---

## 4. Derived / generated data (this repo)

| File | Origin | Reproducible by |
|---|---|---|
| `results/essentiality/gene_essentiality_default_medium.csv` | Single-gene deletion on iMO1056, default medium, 1% threshold (real). WT growth 1.0479; 166 essential. `gene_id` stored as set-repr (needs cleaning). | `notebooks/02_gene_essentiality.ipynb` / `src.gene_essentiality` |
| `data/processed/gene_mapping.csv` | Generated from model genes; identity PAO1 mapping (PA14/name/uniprot PENDING). | `generate_phasea_data.py` |
| `data/processed/literature_evidence.csv` | Study-level provenance rows; gene-level PENDING. | `generate_phasea_data.py` |
| `papers/manifest.csv` | PDF identification (this audit). | `generate_phasea_data.py` |
| `model_audit_snapshot.json` | Read-only model audit summary. | `generate_phasea_data.py` / `audit_model.py` |

---

## 5. Audit scripts (read-only evidence generators)

| Script | Purpose |
|---|---|
| `scripts/audit/audit_model.py` | Full read-only model audit → JSON. |
| `scripts/audit/identify_pdfs.py` | Extract PDF metadata/DOIs via stdlib zlib. |
| `scripts/audit/extract_strain_evidence.py` | Recover PDF text; report strain/method evidence (2026-07-01). |
| `scripts/audit/pubmed_search.py` | NCBI eutils PubMed search (2026-07-01). |
| `scripts/generate_phasea_data.py` | Build the Phase A data artifacts above. |
| `scripts/generate_clean_predictions.py` | Clean predicted-essentiality `gene_id` (R-02). |
| `scripts/audit/show_audit.py` | Pretty-print selected audit fields. |
| `scripts/mapping/build_gene_mapping.py` | Build PAO1↔PA14 gene mapping. |

None modify raw inputs. Relocated to `scripts/` in Cycle 2 (2026-07-01, D-10).

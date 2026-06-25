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

> Models README mentions "iPae1146 (BiGG)" — that is a *different* model and does
> NOT match the loaded file. The loaded model is iMO1056. README to be corrected.

---

## 2. Literature PDFs (`conditian/`)

Identified via embedded PDF metadata (Info dict `/Title`,`/Author`), XMP, and
DOIs decompressed from PDF streams (read-only; script `identify_pdfs.py`).
See `papers/manifest.csv` for the machine-readable manifest.

| Current file | Study | First author | Year | DOI | Journal | Strain | ID confidence | Provenance |
|---|---|---|---|---|---|---|---|---|
| `conditian/juhas2015.pdf` | *P. aeruginosa* essentials: an update on investigation of essential genes | Juhas | 2015 | 10.1099/mic.0.000161 | Microbiology | review | high (DOI in stream) | provided in repo |
| `conditian/keith H.pdf` | Essential genome of *P. aeruginosa* in cystic fibrosis sputum | Turner | 2015 | 10.1073/pnas.1419677112 | PNAS | PA14 | high (DOI+supp in /Title) | provided in repo |
| `conditian/samuelA.pdf` | General and condition-specific essential functions of *P. aeruginosa* | Lee | 2015 | 10.1073/pnas.1422186112 | PNAS | PA14 | high (DOI in headers) | provided in repo |
| `conditian/polsun2019.pdf` | Defining the core essential genome of *P. aeruginosa* | Poulsen | 2019 | 10.1073/pnas.1900570116 | PNAS | PA14/multi-strain | high (DOI+title in /Title) | provided in repo |
| `conditian/davidW.pdf` | Fitness determinants during carbon/oxygen-limited growth arrest | Basta | PENDING | PENDING_VERIFY | PENDING | PA14 (verify) | medium (headers) | provided in repo |
| `conditian/corrieR.pdf` | Surviving the host: metabolic genes required in physiologically-relevant conditions | Belanger | PENDING | PENDING_VERIFY | PENDING (Info /Author: R.E.W. Hancock) | PAO1 (verify) | medium (Info /Title) | provided in repo |

Filename→author inference (do not over-trust filenames; confirmed by metadata):
`keith H` = Keith H. Turner · `samuelA` = (S.A.) Lee · `polsun` = Poulsen ·
`davidW` = David W. Basta · `corrieR` = Corrie/Hancock lab (Belanger).

---

## 3. Supplementary datasets (NOT yet downloaded — B-LIT-01)

| Study | Supplement(s) referenced in PDF | Public source | Status |
|---|---|---|---|
| Turner 2015 | `pnas.1419677112.sd01–sd04.xlsx` | PNAS DCSupplemental | PENDING_DOWNLOAD |
| Lee 2015 | `pnas.1422186112.sd01.xlsx`, `…201422186SI.pdf` | PNAS DCSupplemental | PENDING_DOWNLOAD |
| Poulsen 2019 | fitness data + FiTnEss code | `data.broadinstitute.org/fitness/`, `github.com/broadinstitute/FiTnEss` | PENDING_DOWNLOAD |
| Basta | TBD | TBD | PENDING |
| Belanger | TBD | TBD | PENDING |

When downloaded: store under `data/raw/literature/<study_id>/`, record URL +
retrieval date + SHA-256 here, and never edit in place.

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
| `audit_model.py` | Full read-only model audit → JSON. |
| `identify_pdfs.py` | Extract PDF metadata/DOIs via stdlib zlib (no install). |
| `generate_phasea_data.py` | Build the Phase A data artifacts above. |
| `show_audit.py` | Pretty-print selected audit fields. |

None modify raw inputs. Recommend relocating to `src/audit/` or `scripts/` in Phase B.

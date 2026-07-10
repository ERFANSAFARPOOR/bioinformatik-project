# ORTHOLOGY_PSEUDOMONAS_INTEGRATION.md

**Date:** 2026-07-10  
**Branch:** `erfan/orthology-human-review`  
**Scope:** Integration audit for Pseudomonas Genome Database (PGD) orthology export merged from `origin/develop` (commit `7cd3dd29`, *ortolog table*).

---

## 1. What orthology source is now available

An authoritative **Pseudomonas Genome Database (PGD)** PAO1↔PA14 ortholog export is now present locally under `data/raw/ortholog/`. It provides **5,385 curated 1:1 pairs** between PAO1 locus tags (`PA####`) and PA14 locus tags (`PA14_#####`), with gene descriptions and optional inparalog flags in the raw export.

This is the live database source that was previously unreachable via automated download (B-NET / HTTP 403). It **supplements and validates** the Turner 2015–derived mapping; it does **not** replace the human-reviewed Turner `APPROVED_LIMITED` table until a formal crosswalk and review are complete.

**Source labels in use:**

| Label | Meaning |
|---|---|
| **Pseudomonas-derived** | PGD export (`pao1_pa14_orthologs_pseudomonas.csv`) |
| **Turner-derived** | Turner 2015 sd03/sd04 1:1 subset (2015 PGD vintage) |
| **Manually reviewed** | Human orthology review decisions (2026-07-10) |
| **Approved limited use** | Turner `APPROVED_LIMITED` — interim L-03b draft mapping only |

---

## 2. Files added (merge from develop)

| Path | Role | Status |
|---|---|---|
| `data/raw/ortholog/pao1_pa14_orthologs_pseudomonas.csv` | Raw PGD ortholog export (query/hit strains, locus tags, descriptions) | **Raw / provenance-sensitive** |
| `data/raw/ortholog/Supplementary_Table_S1.csv` | Project-standard supplementary table (gene names, identity, coverage, e-value, source metadata) | **Processed from raw** (enriched; treat as derived until SHA-256 logged) |
| `data/raw/ortholog/Orthology_QC_Report.csv` | Per-pair QC with BLAST validation (`blast_pa14_locus_tag`, identity, status) | **QC / analysis-ready** |

**Existing Turner-derived files (unchanged):**

| Path | Rows | Status |
|---|---|---|
| `data/processed/ortholog/pao1_pa14_orthologs_turner2015_CANDIDATE.csv` | 5,365 | Turner-derived candidate (read-only) |
| `data/processed/ortholog/pao1_pa14_orthologs_turner2015_APPROVED_LIMITED.csv` | 5,365 | Manually reviewed, **approved limited use** |
| `data/processed/ortholog/pao1_pa14_orthologs_turner2015_APPROVED_LIMITED_FOR_L03B.csv` | 5,365 | Filtered export (same rows; conflict resolved) |

**Exploratory workspace:** `tst ortolog/` — see §6.

---

## 3. PGD vs Turner comparison (high level)

| Metric | PGD (2026 export) | Turner APPROVED_LIMITED |
|---|---|---|
| Pair count | **5,385** | **5,365** |
| Delta | **+20 pairs** | baseline for approved L-03b use |
| Method | PGD curated ortholog (current) | Turner 2015 RBB+synteny (2015 vintage) |
| Human review | Not yet | **APPROVED_LIMITED** (2026-07-10) |
| Conflict locus (PA2279/PA2277) | PA2279↔PA14_35100; PA2277↔PA14_35130 | Same Turner pairs; Belanger disagree resolved via KEGG SSDB |

**Key finding:** PGD **confirms** the Turner pairing at the previously disputed arsenic locus (PA2279↔PA14_35100, PA2277↔PA14_35130), independently supporting the `RESOLVED_SUPPORTS_TURNER` decision.

**Integration decision (D-16):** PGD **supplements and validates** Turner; it does **not replace** Turner `APPROVED_LIMITED` until:

1. A formal PGD↔Turner crosswalk is built and reviewed.
2. The +20 PGD-only pairs and any Turner-only pairs are classified (strict 1:1 vs excluded).
3. One-to-many / Review-flagged PGD rows (e.g. `PA0263` / `hcpC`) are resolved or explicitly excluded.
4. A human sign-off approves PGD as the primary mapping source for L-03b (if warranted).

---

## 4. Suitability for PA14→PAO1 evidence transfer

**Suitable for (with constraints):**

- Cross-validation of Turner 1:1 pairs against current PGD curation.
- Identifying PGD-only pairs (+20) for inclusion review.
- Supporting future controlled L-03b draft mapping of Poulsen/Basta PA14 gene IDs.

**Not yet suitable for:**

- Direct replacement of Turner `APPROVED_LIMITED` (no PGD human review record yet).
- Unrestricted genome-wide PA14→PAO1 transfer (strict 1:1 policy still applies).
- Merge into `gene_mapping.csv` (explicitly forbidden until separate approval).
- Validation metrics (B-SCI-01 still blocks).

PAO1 remains the project focus. PA14 experimental evidence still requires orthology support and must be labeled by source.

---

## 5. Risks and ambiguities

| Risk | Detail | Mitigation |
|---|---|---|
| **Pair-count mismatch** | PGD 5,385 vs Turner 5,365 (+20) | Build crosswalk; classify PGD-only / Turner-only / shared |
| **One-to-many / Review rows** | QC report flags `Review` status (e.g. `PA0263`/`hcpC` with multiple PA14 blast hits) | Exclude from strict 1:1 until resolved; do not force pairs |
| **Duplicate QC rows** | Some loci appear multiple times in `Orthology_QC_Report.csv` | Deduplicate in crosswalk script; document policy |
| **Provenance gaps** | `Supplementary_Table_S1.csv` and QC report lack logged SHA-256 in `DATA_PROVENANCE.md` | Add hashes on next provenance pass |
| **Exploratory folder** | `tst ortolog/` contains BLAST DBs, NCBI zips, intermediate CSVs | Relocate to `archive/` after pipeline is documented (do not delete yet) |
| **Premature validation** | Temptation to compute metrics once mapping exists | Metrics remain forbidden (B-SCI-01) |

---

## 6. `tst ortolog/` — role and recommendation

**Role:** Exploratory orthology pipeline workspace used to produce the PGD export and QC artifacts. Contains:

- Raw PGD download (`pao1_pa14_orthologs_pseudomonas.csv` — copy also in `data/raw/ortholog/`)
- NCBI dataset zips for PAO1 (`01t/`) and PA14 (`14/po14/`)
- BLAST databases and protein FASTAs (`blast/`, `data/`)
- Step scripts (`step1_check.py`, `03_build_supplementary_table.py`, `scripts/04–06_*`)
- Intermediate and final results (`results/`, `data/01–02_*.csv`)

**Recommendation (do not delete automatically):**

| Action | Target |
|---|---|
| **Keep for now** | Entire folder until crosswalk script is ported to `scripts/mapping/` |
| **Later relocate** | `archive/tst_ortholog_exploratory/` (or rename to `archive/orthology_pgd_pipeline_2026-07/`) |
| **Document** | Add `archive/tst_ortholog_exploratory/README.md` describing pipeline steps and which outputs were promoted to `data/raw/ortholog/` |
| **Do not commit** | Large BLAST indices (`.pin`, `.psq`, etc.) and NCBI zips unless explicitly needed — consider `.gitignore` |

---

## 7. Recommended final file structure

```
data/
  raw/ortholog/
    pao1_feature_table.txt.gz          # NCBI RefSeq (existing)
    pa14_feature_table.txt.gz          # NCBI RefSeq (existing)
    pao1_pa14_orthologs_pseudomonas.csv   # PGD raw export (NEW)
    Supplementary_Table_S1.csv            # PGD enriched table (NEW; consider move to processed/)
    Orthology_QC_Report.csv               # PGD QC (NEW; consider move to processed/)
  processed/ortholog/
    pao1_pa14_orthologs_turner2015_CANDIDATE.csv           # Turner (unchanged)
    pao1_pa14_orthologs_turner2015_APPROVED_LIMITED.csv    # Turner reviewed (unchanged)
    pao1_pa14_orthologs_turner2015_APPROVED_LIMITED_FOR_L03B.csv
    # FUTURE (after crosswalk + review):
    # pao1_pa14_orthologs_pgd2026_CANDIDATE.csv
    # pao1_pa14_orthologs_crosswalk_turner_vs_pgd.csv

archive/
  tst_ortholog_exploratory/            # FUTURE: relocated from tst ortolog/

docs/
  ORTHOLOGY_PSEUDOMONAS_INTEGRATION.md  # this file

scripts/mapping/
  build_ortholog_candidate.py          # Turner (existing)
  build_ortholog_approved_limited.py   # Turner (existing)
  # FUTURE: build_ortholog_pgd_crosswalk.py
```

**Note:** Consider moving `Supplementary_Table_S1.csv` and `Orthology_QC_Report.csv` from `data/raw/ortholog/` to `data/processed/ortholog/` after SHA-256 logging, since they are derived from the raw PGD export.

---

## 8. Next steps (safe sequence)

1. Build PGD↔Turner crosswalk script (`scripts/mapping/build_ortholog_pgd_crosswalk.py`).
2. Classify shared / PGD-only / Turner-only / Review-flagged pairs.
3. Human review of crosswalk results; decide whether to extend `APPROVED_LIMITED` or create separate PGD-approved table.
4. Only then: controlled L-03b draft mapping for Poulsen/Basta (no metrics).
5. Relocate `tst ortolog/` to `archive/` with README.

**Forbidden until further notice:** merge into `gene_mapping.csv`, compute validation metrics, parse Poulsen/Basta as evidence, run simulations, create condition JSON.

---

## 9. Related documents

- `ORTHOLOGY_HUMAN_REVIEW_DECISION.md` — Turner APPROVED_LIMITED decision
- `ORTHOLOGY_CONFLICT_RESOLUTION_REPORT.md` — PA2279/PA2277 conflict resolution
- `ORTHOLOG_CANDIDATE_TABLE.md` — Turner candidate documentation
- `DATA_PROVENANCE.md` — file provenance (§3b ortholog resources)
- `DECISIONS.md` — D-16 PGD integration policy
- `BLOCKERS.md` — B-MAP-01 partially resolved

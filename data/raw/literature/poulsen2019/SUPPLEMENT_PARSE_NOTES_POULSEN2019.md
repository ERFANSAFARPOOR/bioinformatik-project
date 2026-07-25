# SUPPLEMENT_PARSE_NOTES — poulsen2019

> **Location note:** the read-only guard blocks writing under `data/raw/`
> (DECISIONS D-05), so this per-study parse note lives at repo root instead of
> `data/raw/literature/poulsen2019/SUPPLEMENT_PARSE_NOTES.md`. Raw files were read
> **read-only**; none modified. Date 2026-07-07.

- **study_id:** poulsen2019
- **citation:** Poulsen BE, Yang R, Clatworthy AE, White T, Osmulski SJ, Li L,
  Penaranda C, Lander ES, Shoresh N, Hung DT (2019) *Defining the core essential
  genome of Pseudomonas aeruginosa.* PNAS 116(20):10072–10080.
  DOI 10.1073/pnas.1900570116. PMID 31036669 / PMCID PMC6525520. **VERIFIED (corpus).**
- **strain:** **multi-strain, PA14-referenced.** 9 clinical/lab isolates —
  **BL23, X13273, CF77, BWH005, BWH013, 19660, PA14, BWH015, PS75** — clustered by
  ortholog group. **PAO1 is NOT one of the nine sequenced strains** (see mapping
  note). Gene identity in the supplement = `Cluster_ID` + `PA14_ID` (reference).
- **phenotype class(es):** **core-essential** (essential across all strains/media)
  and **condition-specific-essential** (essential in some but not all media). Keep
  distinct; no collapse.

## Files inspected (read-only)
| file | sheet | dims | content |
|---|---|---|---|
| `pnas.1900570116.sd01.xlsx` | `Dataset S##` | 46×5 | QC: Strain, Medium, mapped reads/replicate, concordance |
| `pnas.1900570116.sd02.xlsx` | `Aug7_2018_TS_120_new_core_0TA_g` | 121×3 | **120 new core genes with 0 TA sites** (`Cluster_ID`, `PA14_ID`, description) |
| `pnas.1900570116.sd03.xlsx` | `Dataset S2` | 53290×60 (23 MB) | **master per-strain/per-gene table**: `Cluster_ID`, Category (core/accessory), #strains, `Strain`, `Gene ID` (strain-specific), name, KO, #TA sites (Total/Removed) |
| `pnas.1900570116.sd04.xlsx` | `borderline instances 13 genes`; `all strain-medium data 13 genes` | 19×13; 586×13 | per strain×medium p-values (replicate, **FWER-adjusted**, **FDR-adjusted**) + `Essential Call (FWER)` / `Essential Call (FDR)` (E/NE) |
| `pnas.1900570116.sd05.xlsx` | `Essential Genes` | 528×22 | **core essential gene list**: `Cluster_ID`, `PA14_ID`, Gene Name, descriptions, KO, `# media essential (of 5)`, `# strains essential` (per-medium), `Essential Category` (Core/…), subcellular location |
| `pnas.1900570116.sd06.xlsx` | `Dataset ##` | 865×8 | cross-study comparison: `Cluster_ID`, `PA14_ID`, description, prior-study calls (Turner/Lee/Skurnik/Liberati) + `This study` (E marks) |
| `pnas.1900570116.sd07.xlsx` | `gene deletions`; `Illumina` | small | validation-mutant primers; sequencing primers (not evidence) |
| `pnas.1900570116.sapp.pdf` | — | — | SI Appendix (Additional Methods; FiTnEss detail) |

## Key columns / ID systems
- **gene ID:** `Cluster_ID` (ortholog cluster across the 9 strains) + `PA14_ID`
  (reference locus tag `PA14_xxxxx`). Strain-specific `Gene ID` in sd03 uses
  per-strain tags (`Q0xx_xxxxx`, `PA14_xxxxx`, `V...`). **No PAO1 `PAxxxx` tag
  anywhere** in the supplement.
- **condition/media (5):** LB, M9 (minimal), FBS (fetal-bovine serum), Sputum
  (Sp), Urine (Ur). Encoded per strain×medium in sd03/sd04; aggregated in sd05
  (`# media essential (of 5)`).
- **essentiality call:** sd05 `Essential Category` (Core = essential across all
  strains); sd04 `Essential Call (FWER)`/`(FDR)`; sd06 `This study` = E.
- **threshold (sourced):** see `THRESHOLD_METHOD_AUDIT.md` — FiTnEss adjusted
  P < 0.05 in **both replicates** (FWER = maximal stringency; FDR = high
  stringency). Core = essential across all 9 strains × 5 media.

## Direct PAO1 mapping status — **BLOCKED**
The supplement is **PA14-referenced**; **PAO1 is not among the 9 strains** and no
`PAxxxx` gene IDs appear in any sheet (verified by scanning sd03's Strain and
Gene ID columns). Mapping the essential lists onto the PAO1 iMO1056 model
therefore requires **validated PA14→PAO1 orthology** (B-MAP-01) — `Cluster_ID`
does **not** expose a PAO1 member. See `POULSEN_BASTA_MAPPING_PLAN.md`.
> Caveat: the paper's Fig. 2 heat-map lists "PAO1" among displayed columns, but
> the supplement data tables (sd03) contain the nine strains above and none is
> PAO1; no PAO1 gene-level essential calls are in the supplement.

## Parse-readiness
**STILL_BLOCKED (mapping).** Threshold + phenotype + condition + locators are
clear (METHODS_READY), but there is **no safe PAO1 mapping** → not parsed to
gene-level evidence this cycle. Becomes PARTIAL_READY once validated PA14→PAO1
orthology exists (then map via `PA14_ID`, retaining one-to-many / missing).

## Extraction plan (future, after orthology)
1. Read sd05 (`Essential Genes`) → core-essential rows keyed by `PA14_ID`.
2. Read sd02 (0-TA new core) → core-essential (flag: inferred from 0 TA sites,
   not statistically called).
3. Optionally sd04 per strain×medium → condition-specific-essential.
4. Map `PA14_ID` → PAO1 via validated orthology; keep one-to-many/missing; mark
   `MAPPING_PENDING`/`ORTHOLOGY_PENDING`. Preserve source file/sheet/row locator.

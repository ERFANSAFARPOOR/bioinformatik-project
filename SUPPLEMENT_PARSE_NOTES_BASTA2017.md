# SUPPLEMENT_PARSE_NOTES — basta2017

> **Location note:** the read-only guard blocks writing under `data/raw/`
> (DECISIONS D-05), so this per-study parse note lives at repo root instead of
> `data/raw/literature/basta2017/SUPPLEMENT_PARSE_NOTES.md`. Raw files were read
> **read-only**; none modified. Date 2026-07-07.

- **study_id:** basta2017
- **citation:** Basta DW, Bergkessel M, Newman DK (2017) *Identification of fitness
  determinants during energy-limited growth arrest in Pseudomonas aeruginosa.*
  mBio 8(6):e01170-17. DOI 10.1128/mBio.01170-17 (erratum 10.1128/mbio.00576-18).
  PMID 29184024 / PMCID PMC5705914. **VERIFIED (corpus).**
- **strain:** **PA14 (UCBPP-PA14).** Gene identity = `PA14_xxxxx` (and `IG_…`
  intergenic regions). No PAO1 tags.
- **phenotype class:** **growth-arrest-survival-determinant** (fitness during
  energy-limited growth arrest). **Conceptually distinct from FBA growth-
  essentiality** — do not equate with model single-gene-deletion growth
  essentiality; keep as its own class.

## Files inspected (read-only)
| file | sheet | dims | content |
|---|---|---|---|
| `mbo006173591sd1.xlsx` | `Carbon limited` | 9221×7 | Dataset S1 — per-locus **Read ratio + p-value** ×2 replicates, `Geometric mean of [read ratios]`, `Fisher p-value` |
| `mbo006173591sd2.xlsx` | `Oxygen limited` | 9221×7 | Dataset S2 — same columns, oxygen limitation |
| `mbo006173591sd3.xlsx` | `Carbon limited` | 65381×8 | Dataset S3 — **raw read counts** per TA site (Initial library / Control / Carbon-limited ×2 replicates) |
| `mbo006173591sd4.xlsx` | `Oxygen limited` | 65381×8 | Dataset S4 — raw read counts, oxygen limitation |
| `mbo006173591sf1_2.tif`, `sf2.tif` | — | — | supplementary figures (images; context only) |

## Key columns / ID systems
- **gene ID:** `Locus` = `PA14_xxxxx` (genes) or `IG_…` (intergenic — exclude from
  gene-level evidence). Header on Excel row 4 (rows 1–3 = title/sub-headers); data
  from row 5. sd3/sd4 have multiple rows per locus (per TA site).
- **conditions:** **carbon limitation** and **oxygen limitation** (10-day energy-
  limited growth arrest, then carbon-replete aerobic outgrowth vs a carbon-replete
  aerobic control). Growth media: LB and **pyruvate minimal (M9 + 40 mM pyruvate)**.
- **fitness quantity:** per-replicate `Read ratio` (limited/control) + `p-value`;
  `Geometric mean` of the two read ratios; `Fisher p-value` (combined).
- **essentiality/fitness call:** **NOT provided as a column.** sd1/sd2 give read
  ratios + p-values only; the 62 "required" genes must be derived by applying the
  paper's threshold (below).

## Threshold (sourced — see `THRESHOLD_METHOD_AUDIT.md`)
Per-replicate reads (limited vs control) tested with **Mann-Whitney U**; read-ratio
geometric mean across replicates; replicate P values combined via **Fisher's
combined probability test**. *"We defined a gene as being required for fitness
during carbon or oxygen limitation if the mean read ratio of the replicates was
≤ 0.25 and the combined P value was ≤ 0.05"* (>4-fold fitness defect). Fitness
**advantage** = read ratio ≥ 4 and combined P ≤ 0.05. Result: **62 required genes**
(20 carbon-specific, 38 oxygen-specific, 4 both).

## Direct PAO1 mapping status — **BLOCKED**
PA14-indexed → requires **validated PA14→PAO1 orthology** (B-MAP-01) before any
comparison to the PAO1 iMO1056 model. See `POULSEN_BASTA_MAPPING_PLAN.md`.

## Parse-readiness
**STILL_BLOCKED.** Two independent gates fail:
1. **ANALYSIS:** no gene-level call column; the ≤0.25 / P≤0.05 threshold must be
   applied to sd1/sd2 to derive the 62 required genes (doable, but a derivation).
2. **MAPPING:** PA14→PAO1 orthology not available.
Additionally, the phenotype (survival during growth arrest) is **not** the FBA
growth-essentiality prediction, so even after mapping it must be compared with a
tailored (maintenance/ATP) framework, not standard single-gene-deletion growth.
→ Not parsed to gene-level evidence this cycle.

## Extraction plan (future, after orthology + concept framework)
1. From sd1 (carbon) and sd2 (oxygen): apply `geometric mean read ratio ≤ 0.25`
   AND `Fisher p-value ≤ 0.05` → required-for-fitness genes; exclude `IG_` rows.
2. Tag condition (carbon-limited / oxygen-limited), phenotype =
   growth-arrest-survival-determinant, medium (LB / pyruvate-minimal arrest).
3. Map `PA14_xxxxx` → PAO1 via validated orthology; keep one-to-many/missing;
   mark `ORTHOLOGY_PENDING`. Preserve source file/sheet/row locator. Do **not**
   compare to FBA growth-essentiality without an explicit non-growth framework.

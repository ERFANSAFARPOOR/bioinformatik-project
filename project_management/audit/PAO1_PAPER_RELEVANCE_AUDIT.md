# PAO1 PAPER RELEVANCE AUDIT

**Original audit:** 2026-07-01 · **Reconciled:** 2026-11-11

**Current status:** supplements are local; the MOPS-pyruvate D-21 binary
comparison has been executed (V-01, interpretation pending). Historical download
and whole-project metric gates are superseded by
`VALIDATION_LABEL_MEDIA_OVERLAP.md` and
`v01_mops_pyruvate/V01_BINARY_VALIDATION_REPORT.md`.
Poulsen is corrected below against the primary paper Table 1.
**Method:** read-only strain/method evidence extraction from the six legacy PDFs
(`scripts/audit/extract_strain_evidence.py`, stdlib FlateDecode text recovery),
plus DOI→PMID→PMCID verification via NCBI E-utilities (reachable this session).
**No fabricated metadata.** Quotes are recovered PDF text (minor spacing artifacts).

## Tier legend
- **Tier 1** — Direct PAO1 validation source
- **Tier 2** — PAO1-derived source (e.g. MPAO1)
- **Tier 3** — Mixed PAO1/PA14 source with directly usable PAO1 rows
- **Tier 4** — PA14-only source requiring validated orthology before use
- **Tier 5** — Multi-strain / core-essential background
- **Tier 6** — Review / background only

## Summary table

| study_id | Strain (corrected) | Tier | PAO1-usable directly? | PA14→PAO1 mapping needed? | Phenotype class |
|---|---|---|---|---|---|
| belanger2022 | **PAO1** | **1** | yes | no | host-condition-fitness |
| lee2015 | **MPAO1 (PAO1-derived)** | **2** | yes (PAO1-derived caveat) | no | general + condition-specific essential |
| turner2015 | **PAO1 + PA14 (mixed)** | **3** | yes (PAO1 rows) | only for PA14 rows | condition-specific essential |
| poulsen2019 | **9 strains incl. PA14; excludes PAO1** | **5** | **no** (cross-strain evidence) | yes, via PA14 reference IDs | core-essential |
| basta2017 | **PA14 (UCBPP-PA14)** | **4** | no | yes | growth-arrest survival determinant |
| juhas2015 | review (PAO1/MPAO1/PA14) | **6** | no (review) | n/a | generally-essential (review) |

**Headline corrections vs the earlier audit** (which treated Turner/Lee/Poulsen/Basta
as "PA14"): **Lee 2015 is MPAO1**, **Belanger 2022 is PAO1**, **Turner 2015 is
mixed PAO1+PA14 with usable PAO1 data**. See §"Corrections" below.

---

## 1. belanger2022 — Tier 1 (PAO1)

- **Citation:** Belanger CR, Dostert M, Blimkie TM, Lee AHY, Dhillon BK, Wu BC, et al., Hancock REW (2022) *Surviving the host: microbial metabolic genes required for growth of Pseudomonas aeruginosa in physiologically-relevant conditions.* Front Microbiol 13:1055512.
- **DOI:** 10.3389/fmicb.2022.1055512 · **PMID:** 36504765 · **PMCID:** PMC9732424 · **Year:** 2022 (published 2022-11-25) · **Journal:** Frontiers in Microbiology
- **Strain evidence (PDF):** *"we used a saturated transposon insertion mutant pool of P. aeruginosa **strain PAO1** and transposon insertion sequencing (Tn-Seq), to identify genes conditionally important for survival…"* (Abstract/Intro).
- **Locus-tag system:** PAO1 (`PAxxxx`).
- **Method:** Tn-seq under physiologically-relevant / host-mimicking conditions (SCFM among them).
- **Media/conditions:** host-relevant media (tissue-culture ± serum, SCFM, etc.) — to be enumerated from methods when reconstructing media (C-01).
- **Phenotype class:** host-condition-fitness.
- **Supplement:** present: `Data_Sheet_1.XLSX`, `Data_Sheet_2.XLSX`, `Data_Sheet_3.docx` (logged 2026-07-06).
- **Direct PAO1 evidence:** **YES**, subject to matched condition and phenotype; not an automatically completed validation.
- **PA14→PAO1 mapping:** not needed.
- **Confidence:** high (strain explicit). **Remaining comparison limits:** exact host-medium reconstruction, phenotype-specific interpretation and model scope; local supplement parsing does not establish a completed matched comparison.

## 2. lee2015 — Tier 2 (MPAO1, PAO1-derived)

- **Citation:** Lee SA, Gallagher LA, Thongdee M, Staudinger BJ, Lippman S, Singh PK, Manoil C (2015) *General and condition-specific essential functions of Pseudomonas aeruginosa.* PNAS 112(16):5189–5194.
- **DOI:** 10.1073/pnas.1422186112 · **PMID:** 25848053 · **PMCID:** PMC4413342 · **Year:** 2015 · **Journal:** PNAS
- **Strain evidence (PDF):** *"Materials and Methods. Strains and Plasmid. The P. aeruginosa parent strain was **MPAO1**. The donor strain for transposon mutagenesis was E. coli SM10 λpir/pIT2…"*. A comparison table lists this study's strain as **PAO1** (vs PA14 comparators). Manoil-lab system.
- **Locus-tag system:** PAO1/MPAO1 (`PAxxxx`).
- **Method:** Tn-seq (transposon mutant library; ISlacZ/two-allele lineage).
- **Media/conditions:** LB, MOPS-pyruvate and sputum are the three primary conditions; general essentials span these conditions, while condition-specific essentials retain their medium.
- **Phenotype class:** general + condition-specific essential (keep both distinct).
- **Supplement:** `pnas.1422186112.sd01.xlsx` and Supporting Information are present (logged 2026-07-06).
- **PAO1-derived evidence:** **YES**, with MPAO1 sublineage caveat. Lee-original `PAxxxx` labels join directly; D-21 uses Varadarajan2020 DS1 unique-standard-PAO1 best-hit mapping from MPAO1, not an identity join for all genes. Both D-21 polarities come from that reanalysis, which is not independent replication.
- **PA14→PAO1 mapping:** not needed.
- **Confidence:** high (strain explicit). **Remaining comparison limits:** MPAO1-vs-reference-PAO1 differences, source/threshold semantics and medium assumptions. The first MOPS-pyruvate cell is documented in D-21/V-01; other conditions remain separate.

## 3. turner2015 — Tier 3 (PAO1 + PA14, mixed; usable PAO1 rows)

- **Citation:** Turner KH, Wessel AK, Palmer GC, Murray JL, Whiteley M (2015) *Essential genome of Pseudomonas aeruginosa in cystic fibrosis sputum.* PNAS 112(13):4110–4115.
- **DOI:** 10.1073/pnas.1419677112 · **PMID:** 25775563 · **PMCID:** PMC4386324 · **Year:** 2015 · **Journal:** PNAS
- **Strain evidence (PDF):** *"**Wild-type PAO1** and individual transposon mutants with growth defects in SCFM2 were grown overnight in LB…"*; *"only two genes were significantly less fit in SCFM2 than in MOPS-sputum in both **PAO1 and PA14**…"*; heatmap colored by *"relative mutant fitness in **strain PAO1** grown in MOPS-sputum medium compared with growth in MOPS-succinate minimal medium."* (24 PAO1 mentions, 24 PA14 mentions.)
- **Locus-tag system:** PAO1 (`PAxxxx`) and PA14 (`PA14_xxxxx`).
- **Method:** Tn-seq in SCFM/SCFM2 and MOPS-sputum vs MOPS-succinate minimal.
- **Media/conditions:** synthetic CF sputum (SCFM/SCFM2), MOPS-sputum, MOPS-succinate minimal.
- **Phenotype class:** condition-specific essential (CF-sputum).
- **Supplement:** `pnas.1419677112.sd01–sd10.xlsx` are present (logged 2026-07-06).
- **Direct PAO1 evidence:** **YES for the PAO1 rows**; each condition/fitness contrast still needs a matching prediction before a validation claim.
- **PA14→PAO1 mapping:** only for the PA14 rows.
- **Confidence:** high (PAO1 data present and explicit). **Remaining comparison limits:** matching each source sheet/column and phenotype to its modeled condition; no completed sputum/SCFM2 validation is claimed here.

## 4. poulsen2019 — Tier 5 (multi-strain; PAO1 not screened)

- **Citation:** Poulsen BE et al. (2019) *Defining the core essential genome of Pseudomonas aeruginosa.* PNAS 116(20):10072–10080.
- **DOI:** 10.1073/pnas.1900570116 · **PMID:** 31036669 · **PMCID:** PMC6525520.
- **Primary strain evidence:** [Table 1](https://www.pnas.org/doi/10.1073/pnas.1900570116) lists **BL23, BWH005, BWH013, BWH015, CF77, PS75, PA14, X13273, 19660**. **PAO1 is not among the nine screened strains.** Its mention in the discussion of earlier studies is reference context, not a sample in this experiment.
- **Locus-tag system:** study-strain identifiers; local essential lists use `PA14_ID` and `Cluster_ID`. These clusters relate the nine study strains and do not contain a PAO1 member. Mapping to a `PAxxxx` coordinate would not turn the measurement into a PAO1 assay.
- **Method / conditions:** Tn-seq + FiTnEss; LB, M9 minimal, serum, sputum, urine.
- **Phenotype class:** core-essential (across the study strains/conditions); per-strain calls must retain their own strain and condition.
- **Supplement:** local `pnas.1900570116.sd01–sd07.xlsx` plus SI (logged 2026-07-06).
- **Direct PAO1 evidence:** **NO**. Do not search for a PAO1 identity-join subset in these clusters.
- **PA14→PAO1 mapping:** required when using the `PA14_ID` reference coordinate; controlled draft mapping can use the **APPROVED_LIMITED** Turner strict 1:1 subset under `ORTHOLOGY_HUMAN_REVIEW_DECISION.md`. This is not unrestricted approval or completed validation.
- **Confidence:** high for screened-strain classification (primary Table 1). Orthology, model coverage, medium and phenotype comparability still need explicit handling for any cross-strain analysis.

## 5. basta2017 — Tier 4 (PA14, UCBPP-PA14)

- **Citation:** Basta DW, Bergkessel M, Newman DK (2017) *Identification of fitness determinants during energy-limited growth arrest in Pseudomonas aeruginosa.* mBio 8(6):e01170-17.
- **DOI:** 10.1128/mBio.01170-17 · **PMID:** 29184024 · **PMCID:** PMC5705914 · **Year:** 2017 · **Journal:** mBio · **Erratum:** 10.1128/mbio.00576-18
- **Strain evidence (PDF):** *"We grew cultures of the **PA14** wild-type (WT) strain aerobically to the exponential phase in minimal medium with 40 mM pyruvate…"*; reads *"mapped to the **UCBPP-PA14** genome sequence"* (ARTIST Tn-seq pipeline).
- **Locus-tag system:** PA14 (`PA14_xxxxx`).
- **Method:** Tn-seq during energy-limited growth arrest (pyruvate-carbon or oxygen limitation).
- **Media/conditions:** minimal medium + 40 mM pyruvate; carbon-/oxygen-limited arrest.
- **Phenotype class:** growth-arrest survival determinant (**distinct** from growth essentiality).
- **Supplement:** local `mbo006173591sd1–sd4.xlsx` and figure TIFFs (logged 2026-07-06).
- **Direct PAO1 validation:** **NO** — PA14 only.
- **PA14→PAO1 mapping:** **required**; the Turner strict 1:1 subset is **APPROVED_LIMITED** for controlled draft mapping only (`ORTHOLOGY_HUMAN_REVIEW_DECISION.md`).
- **Confidence:** high (strain explicit). **Uncertainties:** whether the phenotype maps onto FBA growth-essentiality at all (arrest ≠ growth).

## 6. juhas2015 — Tier 6 (review)

- **Citation:** Juhas M (2015) *Pseudomonas aeruginosa essentials: an update on investigation of essential genes.* Microbiology 161(11):2053–2060.
- **DOI:** 10.1099/mic.0.000161 · **PMID:** 26311069 · **PMCID:** PMC10960635 · **Year:** 2015 · **Journal:** Microbiology (Reading)
- **Strain evidence (PDF):** discusses *"P. aeruginosa strain **PAO1**"* annotation, *"P. aeruginosa strain **MPAO1** … grown on six different media, including … cystic fibrosis patient's sputum (Lee et al.)"*, and *"the mariner transposon MAR2xT7 to identify essential genes in P. aeruginosa strain **PA14** (Liberati et al., 2006)."*
- **Locus-tag system:** n/a (review).
- **Method:** literature review.
- **Phenotype class:** generally-essential (as reviewed).
- **Supplement:** none (review).
- **Direct PAO1 validation:** **NO** — use for Introduction/Discussion and to locate primary datasets only.
- **PA14→PAO1 mapping:** n/a.
- **Confidence:** high. **Uncertainties:** none for classification.

---

## Corrections (explicit)

| study | Earlier classification | Corrected classification (reconciled 2026-11-11) | Evidence |
|---|---|---|---|
| **lee2015** | "PA14" | **MPAO1 (PAO1-derived), Tier 2** | *"The P. aeruginosa parent strain was MPAO1"* |
| **belanger2022** | "confirm" strain | **PAO1, Tier 1** | *"…transposon insertion mutant pool of P. aeruginosa strain PAO1…"* |
| **turner2015** | "PA14" | **PAO1 + PA14 mixed, Tier 3** | *"Wild-type PAO1 and individual transposon mutants…"*; *"…in both PAO1 and PA14…"* |
| poulsen2019 | July audit incorrectly inferred PAO1 inclusion from background discussion | **Nine strains including PA14; PAO1 not screened (Tier 5)** | Primary paper **Table 1**; local supplement strain list |
| basta2017 | "PA14 (confirm)" | **PA14 confirmed, Tier 4** | *"the PA14 wild-type (WT) strain"*; *"UCBPP-PA14 genome"* |
| juhas2015 | "review" | review, **Tier 6** (unchanged) | multi-strain review |

## Impact on the validation plan

- **Belanger PAO1** and **Turner PAO1 rows** use PAO1 locus IDs. **Lee-original** labels also use PAO1 tags, with an MPAO1 sublineage caveat. These paths need no PA14 orthology.
- **D-21** instead uses Varadarajan2020 DS1 MPAO1→PAO1 unique best-hit mappings and DS4 Minimal calls; mappings are not universal. The primary join has **1025 genes** (214 positive, 811 negative); **18 ambiguous** and **11 other model genes** are excluded. V-01 metrics are computed, pending interpretation. Do not mix D-20 Lee-original positives with D-21 negatives.
- Supplements are present and MOPS-pyruvate is computationally reconstructed. Other conditions and phenotype classes require their own evidence/media checks; presence of a supplement alone is not validation.
- **Poulsen and Basta remain cross-strain paths.** The approved-limited Turner 1:1 subset supports future controlled drafts, not a PAO1 identity join or automatic metric permission. Basta additionally measures growth-arrest survival rather than standard FBA growth essentiality.

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

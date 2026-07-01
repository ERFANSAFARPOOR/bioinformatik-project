# PAO1 PAPER RELEVANCE AUDIT

**Date:** 2026-07-01 · **Branch:** `claude/revival-audit`
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
| poulsen2019 | multi-strain (incl. PAO1, PA14) | **3 / 5** | partial (PAO1-strain rows, unverified) | for non-PAO1 strains | core-essential |
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
- **Supplement:** PENDING download (Frontiers supplementary; B-LIT-01).
- **Direct PAO1 validation:** **YES** once gene list obtained.
- **PA14→PAO1 mapping:** not needed.
- **Confidence:** high (strain explicit). **Uncertainties:** exact per-condition media compositions; supplement column semantics not yet inspected.

## 2. lee2015 — Tier 2 (MPAO1, PAO1-derived)

- **Citation:** Lee SA, Gallagher LA, Thongdee M, Staudinger BJ, Lippman S, Singh PK, Manoil C (2015) *General and condition-specific essential functions of Pseudomonas aeruginosa.* PNAS 112(16):5189–5194.
- **DOI:** 10.1073/pnas.1422186112 · **PMID:** 25848053 · **PMCID:** PMC4413342 · **Year:** 2015 · **Journal:** PNAS
- **Strain evidence (PDF):** *"Materials and Methods. Strains and Plasmid. The P. aeruginosa parent strain was **MPAO1**. The donor strain for transposon mutagenesis was E. coli SM10 λpir/pIT2…"*. A comparison table lists this study's strain as **PAO1** (vs PA14 comparators). Manoil-lab system.
- **Locus-tag system:** PAO1/MPAO1 (`PAxxxx`).
- **Method:** Tn-seq (transposon mutant library; ISlacZ/two-allele lineage).
- **Media/conditions:** rich (LB) "general" essentiality + defined/nutrient conditions for condition-specific essentiality.
- **Phenotype class:** general + condition-specific essential (keep both distinct).
- **Supplement:** `pnas.1422186112.sd01.xlsx` — PENDING download (B-LIT-01/B-NET).
- **Direct PAO1 validation:** **YES** (PAO1-derived; record MPAO1 sublineage caveat).
- **PA14→PAO1 mapping:** not needed.
- **Confidence:** high (strain explicit). **Uncertainties:** MPAO1-vs-reference-PAO1 genomic differences; per-condition thresholds not yet extracted.

## 3. turner2015 — Tier 3 (PAO1 + PA14, mixed; usable PAO1 rows)

- **Citation:** Turner KH, Wessel AK, Palmer GC, Murray JL, Whiteley M (2015) *Essential genome of Pseudomonas aeruginosa in cystic fibrosis sputum.* PNAS 112(13):4110–4115.
- **DOI:** 10.1073/pnas.1419677112 · **PMID:** 25775563 · **PMCID:** PMC4386324 · **Year:** 2015 · **Journal:** PNAS
- **Strain evidence (PDF):** *"**Wild-type PAO1** and individual transposon mutants with growth defects in SCFM2 were grown overnight in LB…"*; *"only two genes were significantly less fit in SCFM2 than in MOPS-sputum in both **PAO1 and PA14**…"*; heatmap colored by *"relative mutant fitness in **strain PAO1** grown in MOPS-sputum medium compared with growth in MOPS-succinate minimal medium."* (24 PAO1 mentions, 24 PA14 mentions.)
- **Locus-tag system:** PAO1 (`PAxxxx`) and PA14 (`PA14_xxxxx`).
- **Method:** Tn-seq in SCFM/SCFM2 and MOPS-sputum vs MOPS-succinate minimal.
- **Media/conditions:** synthetic CF sputum (SCFM/SCFM2), MOPS-sputum, MOPS-succinate minimal.
- **Phenotype class:** condition-specific essential (CF-sputum).
- **Supplement:** `pnas.1419677112.sd01–sd04.xlsx` — PENDING download (B-LIT-01/B-NET).
- **Direct PAO1 validation:** **YES for the PAO1 rows** (condition-specific, sputum vs minimal).
- **PA14→PAO1 mapping:** only for the PA14 rows.
- **Confidence:** high (PAO1 data present and explicit). **Uncertainties:** which supplement sheet/columns hold the PAO1 (vs PA14) fitness values; threshold definitions.

## 4. poulsen2019 — Tier 3 / Tier 5 (multi-strain incl. PAO1)

- **Citation:** Poulsen BE, Yang R, Clatworthy AE, White T, Osmulski SJ, Li L, Penaranda C, Lander ES, Shoresh N, Hung DT (2019) *Defining the core essential genome of Pseudomonas aeruginosa.* PNAS 116(20):10072–10080.
- **DOI:** 10.1073/pnas.1900570116 · **PMID:** 31036669 · **PMCID:** PMC6525520 · **Year:** 2019 · **Journal:** PNAS
- **Strain evidence (PDF):** *"Previous transposon mutagenesis studies of two common laboratory strains, **PA14 and PAO1**, have found varying numbers of essential genes…"*; *"…while a single strain has ~400–800 essential genes, the core essential genome across all strains analyzed is ~321 genes…"*. Nine strains analyzed (incl. PAO1, PA14).
- **Locus-tag system:** multi-strain (per-strain tags; PAO1 = `PAxxxx`).
- **Method:** Tn-seq + FiTnEss statistical framework (code: github.com/broadinstitute/FiTnEss; data: data.broadinstitute.org/fitness/).
- **Media/conditions:** rich-medium essentiality (per methods).
- **Phenotype class:** core-essential.
- **Supplement:** PNAS SI + Broad fitness portal — PENDING download (B-LIT-01).
- **Direct PAO1 validation:** **partial** — usable only if the **PAO1-strain** per-strain essential list is separable in the supplement (unverified).
- **PA14→PAO1 mapping:** needed for the non-PAO1 strains; the core set is strain-agnostic background.
- **Confidence:** high (strains explicit). **Uncertainties:** availability of a clean PAO1-only essential list in the supplement.

## 5. basta2017 — Tier 4 (PA14, UCBPP-PA14)

- **Citation:** Basta DW, Bergkessel M, Newman DK (2017) *Identification of fitness determinants during energy-limited growth arrest in Pseudomonas aeruginosa.* mBio 8(6):e01170-17.
- **DOI:** 10.1128/mBio.01170-17 · **PMID:** 29184024 · **PMCID:** PMC5705914 · **Year:** 2017 · **Journal:** mBio · **Erratum:** 10.1128/mbio.00576-18
- **Strain evidence (PDF):** *"We grew cultures of the **PA14** wild-type (WT) strain aerobically to the exponential phase in minimal medium with 40 mM pyruvate…"*; reads *"mapped to the **UCBPP-PA14** genome sequence"* (ARTIST Tn-seq pipeline).
- **Locus-tag system:** PA14 (`PA14_xxxxx`).
- **Method:** Tn-seq during energy-limited growth arrest (pyruvate-carbon or oxygen limitation).
- **Media/conditions:** minimal medium + 40 mM pyruvate; carbon-/oxygen-limited arrest.
- **Phenotype class:** growth-arrest survival determinant (**distinct** from growth essentiality).
- **Supplement:** PENDING download (B-LIT-01).
- **Direct PAO1 validation:** **NO** — PA14 only.
- **PA14→PAO1 mapping:** **required** (validated orthology; B-MAP-01/B-NET).
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

| study | Earlier classification | Corrected classification (2026-07-01) | Evidence |
|---|---|---|---|
| **lee2015** | "PA14" | **MPAO1 (PAO1-derived), Tier 2** | *"The P. aeruginosa parent strain was MPAO1"* |
| **belanger2022** | "confirm" strain | **PAO1, Tier 1** | *"…transposon insertion mutant pool of P. aeruginosa strain PAO1…"* |
| **turner2015** | "PA14" | **PAO1 + PA14 mixed, Tier 3** | *"Wild-type PAO1 and individual transposon mutants…"*; *"…in both PAO1 and PA14…"* |
| poulsen2019 | "PA14 (multi-strain core)" | multi-strain **incl. PAO1** (Tier 3/5) | *"…two common laboratory strains, PA14 and PAO1…"* |
| basta2017 | "PA14 (confirm)" | **PA14 confirmed, Tier 4** | *"the PA14 wild-type (WT) strain"*; *"UCBPP-PA14 genome"* |
| juhas2015 | "review" | review, **Tier 6** (unchanged) | multi-strain review |

## Impact on the validation plan

- The PAO1 validation path is **no longer strain-blocked** for the first
  comparison: **belanger2022 (PAO1)**, **lee2015 (MPAO1)**, and the **PAO1 rows of
  turner2015** provide experimental labels in PAO1 `PAxxxx` tags that join
  directly to the model.
- Remaining blockers for those three are **supplement download (B-NET/B-LIT-01)**
  and **per-condition media reconstruction (B-COND-01)** — not orthology.
- Validated **PAO1↔PA14 orthology (B-MAP-01)** is still required only to use
  **basta2017** and the non-PAO1 strains of **poulsen2019**.

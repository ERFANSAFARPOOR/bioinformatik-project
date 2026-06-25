---
name: literature-extraction
description: Extract experimental gene-essentiality/fitness evidence from the P. aeruginosa papers and their supplements into literature_evidence.csv with full provenance. Trigger when asked to extract, parse, or tabulate experimental gene lists, essential genes, or fitness data from the literature.
---

# Literature extraction

## Trigger
Asked to extract/parse/tabulate experimental essential or fitness genes, build
or extend the evidence table, or process the papers' supplementary datasets.

## Inputs
- PDFs in `conditian/` (Juhas2015, Turner2015, Lee2015, Poulsen2019, Basta, Belanger)
- Official supplements (download to `data/raw/literature/<study>/`; see DOIs in `papers/manifest.csv`)
- Schema: `data/processed/literature_evidence.csv`

## Ordered workflow
1. Verify citation/DOI/year/strain per study (resolve B-LIT-02 for Basta/Belanger).
2. Download official supplements; record URL + retrieval date + SHA-256 in `DATA_PROVENANCE.md`.
3. Parse each dataset to gene-level rows. Capture ALL required fields: study_id,
   citation, DOI, year, strain, locus_tag, gene_name, condition, medium,
   carbon_source, electron_acceptor, growth_phase, method, comparison_group,
   phenotype_type, essentiality_definition, effect_direction, effect_size,
   statistical_threshold, validation_method, page/table/figure, supplementary_dataset,
   source_file, mapping fields, notes.
4. Assign `phenotype_type` from the study's own definition — keep the SIX classes
   distinct (general / core / condition-specific essential; reduced-fitness;
   growth-arrest survival; host-condition fitness).
5. Tag strain explicitly (PAO1 vs PA14); never normalize across strains here.
6. Append to `literature_evidence.csv`; leave true unknowns as `PENDING_*` + blocker.

## Validation requirements
- Every gene-level value traces to a specific table/figure/supplement locator.
- No value without a citation. Counts reconcile with the paper's stated totals.
- Phenotype class matches the study's experimental definition and threshold.

## Prohibited behavior
- Inventing gene lists, thresholds, or effect sizes.
- Merging phenotype classes into a single binary essential label.
- Treating PAO1 and PA14 locus tags as equivalent.
- Editing downloaded raw supplements in place.

## Expected outputs
Updated `data/processed/literature_evidence.csv` (gene-level), provenance entries
in `DATA_PROVENANCE.md`, raw files under `data/raw/literature/`, blockers updated.

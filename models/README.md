# Models Directory

This directory contains the SBML model used in this project. The focus of the
repository is **Pseudomonas aeruginosa PAO1**, and we use a single curated
genome-scale metabolic model for all analyses.

## Primary model — iMO1056 (PAO1)

- **Identity:** **iMO1056** — Oberhardt MA, Puchałka J, Fryer KE, Martins dos
  Santos VAP, Papin JA (2008) *Genome-scale metabolic network analysis of the
  opportunistic pathogen Pseudomonas aeruginosa PAO1.* J Bacteriol 190(8):2790–2803.
- **Strain:** *P. aeruginosa* **PAO1** (gene IDs are `PAxxxx` PAO1 locus tags).
- **Source / accession:** BioModels `MODEL1507180020`.
- **File (raw, read-only):** `paeruginosa_MODEL1507180020.xml`
  - SHA-256 `0868a5ebb41ebb4967c3c182e686eca7552af9255cba5a6d130cf114d1212ead`
  - Verified copy also at `models/raw/paeruginosa_MODEL1507180020.xml`.
- **Scale:** 1110 reactions · 879 metabolites · 1054 genes · compartments `c`, `e`.
- **Objective:** `PA_Biomass6_DM` (max); default-medium WT growth ≈ 1.0479285528 /h.

> **Correction (2026-07-01):** an earlier version of this README stated the model
> could be referred to as "iPae1146 (BiGG version)". That is **incorrect** —
> `iPae1146` is a *different* reconstruction. The model in this repository is
> **iMO1056** (BioModels `MODEL1507180020`). Do not conflate the two.

## Layout

- `paeruginosa_MODEL1507180020.xml` — raw SBML (read-only; canonical load path).
- `raw/` — byte-identical archived copy of the raw SBML (provenance).
- `processed/` — derived/cleaned model artifacts only (none yet). Never edit the
  raw SBML in place.

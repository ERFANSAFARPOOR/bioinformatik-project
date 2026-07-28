# Models Directory

This directory contains the genome-scale metabolic model used throughout this project.

The repository focuses on ***Pseudomonas aeruginosa* PAO1**, and all computational analyses are performed using a single curated SBML reconstruction.

---

# Primary Model — iMO1056 (PAO1)

* **Model:** **iMO1056**
* **Reference:** Oberhardt MA, Puchałka J, Fryer KE, Martins dos Santos VAP, Papin JA (2008). *Genome-scale metabolic network analysis of the opportunistic pathogen Pseudomonas aeruginosa PAO1.* Journal of Bacteriology, 190(8), 2790–2803.
* **Organism:** *Pseudomonas aeruginosa* PAO1
* **Gene identifiers:** PAO1 locus tags (`PAxxxx`)
* **BioModels accession:** `MODEL1507180020`

### Model Statistics

| Property          | Value              |
| ----------------- | ------------------ |
| Reactions         | 1110               |
| Metabolites       | 879                |
| Genes             | 1054               |
| Compartments      | `c`, `e`           |
| Objective         | `PA_Biomass6_DM`   |
| Default WT growth | ≈ 1.0479285528 h⁻¹ |

---

# Repository Layout

```text
models/
│
├── paeruginosa_MODEL1507180020.xml
│   Working SBML model used throughout the project.
│
└── raw/
    └── paeruginosa_MODEL1507180020.xml
        Archived copy of the original SBML model preserved for
        provenance and reproducibility.
```

The primary model (`paeruginosa_MODEL1507180020.xml`) is the model loaded by the project source code.

The archived copy stored under `raw/` is retained for provenance and reproducibility and should not be modified.

---

# File Integrity

**Working model**

* File: `paeruginosa_MODEL1507180020.xml`
* SHA-256:
  `0868a5ebb41ebb4967c3c182e686eca7552af9255cba5a6d130cf114d1212ead`

**Archived copy**

* File: `raw/paeruginosa_MODEL1507180020.xml`
* Verified to be byte-identical to the working model.

---

# Important Note

> **Correction (2026-07-01):** An earlier version of the project documentation incorrectly referred to this model as **iPae1146 (BiGG version)**. This repository uses **iMO1056** (BioModels accession `MODEL1507180020`) exclusively. These are different genome-scale metabolic reconstructions and should not be confused.

---

# Usage Policy

* The SBML model is treated as the canonical metabolic reconstruction used throughout this project.
* The archived copy under `raw/` is preserved for provenance and reproducibility and should never be edited.
* Any future modified or condition-specific models should be stored separately without altering either of the original SBML files.

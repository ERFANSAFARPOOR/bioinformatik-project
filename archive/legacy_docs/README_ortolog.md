<div align="center">

# PAO1–PA14 Ortholog Validation Pipeline

### Reciprocal Best BLAST Hit (RBH) Validation of Curated Orthologs

A reproducible bioinformatics workflow for validating orthologous genes between *Pseudomonas aeruginosa* PAO1 and UCBPP-PA14 using Reciprocal Best BLAST Hits (RBH).

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Pandas](https://img.shields.io/badge/Pandas-2.x-green)
![BLAST+](https://img.shields.io/badge/NCBI-BLAST+-orange)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)
![License](https://img.shields.io/badge/License-MIT-yellow)

</div>

---

# Overview

This project implements a fully reproducible bioinformatics workflow to validate curated ortholog assignments obtained from the **Pseudomonas Genome Database (PGD)**.

Although PGD provides high-quality orthology annotations, duplicated genes, paralogs, and gene family expansions may produce ambiguous mappings.

To independently verify these annotations, reciprocal BLASTP searches are performed between the reference strains:

- **Pseudomonas aeruginosa PAO1**
- **Pseudomonas aeruginosa UCBPP-PA14**

The pipeline automatically:

- validates reciprocal best hits
- detects ambiguous orthologs
- generates confidence scores
- exports genes requiring manual review
- performs quality control of the final dataset

---

# Workflow

```text
                Curated Ortholog Mapping
                         │
                         ▼
             Gene Name Annotation
                         │
                         ▼
         Forward BLASTP (PAO1 → PA14)
                         │
                         ▼
         Reverse BLASTP (PA14 → PAO1)
                         │
                         ▼
      Reciprocal Best Hit (RBH) Analysis
                         │
          ┌──────────────┴──────────────┐
          ▼                             ▼
   RBH Confirmed               Manual Review
          │                             │
          └──────────────┬──────────────┘
                         ▼
             Final Ortholog Dataset
                         │
                         ▼
               Automatic Validation
```

---

# Pipeline Summary

| Step | Description |
|------|-------------|
| 1 | Load curated ortholog table |
| 2 | Read BLASTP forward results |
| 3 | Read BLASTP reverse results |
| 4 | Select best BLAST hits |
| 5 | Identify Reciprocal Best Hits |
| 6 | Detect ambiguous orthologs |
| 7 | Assign confidence level |
| 8 | Export final ortholog table |
| 9 | Validate final dataset |

---

# Project Structure

```text
ortolog/

├── blast/
│   ├── blast_results.tsv
│   └── blast_reverse.tsv
│
├── data/
│   ├── raw/
│   ├── processed/
│   ├── PAO1_protein_PGD.faa
│   └── PA14_protein_PGD.faa
│
├── scripts/
│   ├── build_rbh_ortholog_table.py
│   ├── validate_final_table.py
│   └── utils_review_failed_pairs.py
│
├── results/
│   └── final/
│
├── requirements.txt
├── LICENSE
└── README.md
```

---

# Input Files

| File | Description |
|------|-------------|
| pao1_pa14_orthologs_pseudomonas.csv | Curated ortholog mapping |
| PAO1_protein_PGD.faa | PAO1 protein sequences |
| PA14_protein_PGD.faa | PA14 protein sequences |
| blast_results.tsv | Forward BLASTP output |
| blast_reverse.tsv | Reverse BLASTP output |

---

# Requirements

Python ≥ 3.11

Install dependencies

```bash
pip install -r requirements.txt
```

requirements.txt

```text
pandas>=2.2
```

---

# Running

Build the RBH table

```bash
python scripts/build_rbh_ortholog_table.py
```

Validate

```bash
python scripts/validate_final_table.py
```

---

# Output

```text
results/final/

├── pao1_pa14_orthologs_pseudomonas_rbh_YYYYMMDD.csv
├── Manual_Review_Orthologs.csv
└── Validation_Report.txt
```

---

# Validation Statistics

Current dataset

| Metric | Value |
|---------|------:|
| Total curated orthologs | 5,374 |
| RBH confirmed | 5,348 |
| Manual review required | 26 |
| Duplicate pairs | 0 |
| Mean identity | 99.12% |
| Mean coverage | 99.90% |
| Validation status | PASSED |

---

# Confidence Levels

| Confidence | Interpretation |
|------------|---------------|
| Very High | Reciprocal Best BLAST Hit confirmed |
| Review | Reciprocal relationship not confirmed |

---

# Automatic Quality Control

The validation module checks

- duplicate ortholog pairs

- missing locus tags

- missing metadata

- invalid confidence labels

- sequence identity

- alignment coverage

- negative e-values

- negative bit scores

- summary statistics

---

# Biological Interpretation

Most curated orthologs were confirmed by Reciprocal Best BLAST Hits, supporting the reliability of the Pseudomonas Genome Database.

The remaining genes requiring manual review mainly belong to:

- duplicated loci

- paralogous proteins

- Hcp family proteins

- transcriptional regulators

- secretion system proteins

These genes are exported separately for downstream inspection.

---

# Data Sources

Pseudomonas Genome Database

https://www.pseudomonas.com

NCBI Protein

https://www.ncbi.nlm.nih.gov/protein

NCBI BLAST+

https://blast.ncbi.nlm.nih.gov/

---

# Citation

Stover CK et al.

Complete genome sequence of Pseudomonas aeruginosa PAO1.

Nature (2000)

Lee DG et al.

Genomic analysis reveals that Pseudomonas aeruginosa PA14 is a highly virulent clone.

PNAS (2006)

Camacho C et al.

BLAST+: architecture and applications.

BMC Bioinformatics (2009)

Winsor GL et al.

Pseudomonas Genome Database.

---

# Future Development

Planned improvements include

- DIAMOND support

- OrthoFinder integration

- eggNOG annotation

- KEGG pathway annotation

- functional enrichment analysis

- interactive HTML reports

- automatic visualization of RBH statistics

---

# Author

**Saba Salim**

Bachelor Student in Biotechnology

Comparative Genomics • Bioinformatics • Microbial Genomics

---

# License

MIT License
from pathlib import Path
import pandas as pd

# ============================================================
# Paths
# ============================================================

BASE = Path(__file__).resolve().parent.parent

SUPP_FILE = BASE / "results" / "03_supplementary_table.csv"
BLAST_FILE = BASE / "results" / "blast_results.tsv"

OUT_SUPP = BASE / "results" / "Supplementary_Table_S1.csv"
OUT_QC = BASE / "results" / "Orthology_QC_Report.csv"

# ============================================================
# Read Supplementary table
# ============================================================

print("Reading supplementary table...")

supp = pd.read_csv(SUPP_FILE)

print(f"Rows : {len(supp)}")

# ------------------------------------------------------------
# Remove empty columns (they will be replaced by BLAST values)
# ------------------------------------------------------------

supp = supp.drop(
    columns=[
        "identity_percent",
        "coverage_percent",
        "evalue",
        "bit_score"
    ],
    errors="ignore"
)

# ============================================================
# Read BLAST
# ============================================================

print("\nReading BLAST results...")

blast = pd.read_csv(
    BLAST_FILE,
    sep="\t",
    header=None,
    names=[
        "pao1_locus_tag",
        "blast_pa14_locus_tag",
        "identity_percent",
        "alignment_length",
        "query_length",
        "subject_length",
        "evalue",
        "bit_score"
    ]
)

print(f"Rows : {len(blast)}")

# ============================================================
# Coverage
# ============================================================

blast["coverage_percent"] = (
    blast["alignment_length"] /
    blast["query_length"] * 100
).round(2)

# ============================================================
# Best BLAST hit
# ============================================================

print("\nSelecting best hit...")

best = (
    blast
    .sort_values(
        by=[
            "pao1_locus_tag",
            "bit_score",
            "evalue"
        ],
        ascending=[
            True,
            False,
            True
        ]
    )
    .drop_duplicates(
        subset="pao1_locus_tag",
        keep="first"
    )
)

print(f"Best hits : {len(best)}")

# ============================================================
# Merge
# ============================================================

print("\nMerging...")

merged = supp.merge(
    best,
    on="pao1_locus_tag",
    how="left"
)

print(f"Merged rows : {len(merged)}")

# ============================================================
# Validate orthology
# ============================================================

merged["orthology_confidence"] = merged.apply(
    lambda r:
        "High"
        if r["pa14_locus_tag"] == r["blast_pa14_locus_tag"]
        else "Review",
    axis=1
)

# ============================================================
# QC report
# ============================================================

qc = merged[
    [
        "pao1_locus_tag",
        "pao1_gene_name",
        "pa14_locus_tag",
        "blast_pa14_locus_tag",
        "identity_percent",
        "coverage_percent",
        "evalue",
        "bit_score",
        "orthology_confidence"
    ]
].copy()

qc["status"] = qc["orthology_confidence"]

# ============================================================
# Remove helper column
# ============================================================

merged.drop(
    columns=["blast_pa14_locus_tag"],
    inplace=True
)

# ============================================================
# Order columns
# ============================================================

final_cols = [
    "pa14_locus_tag",
    "pa14_gene_name",
    "pao1_locus_tag",
    "pao1_gene_name",
    "orthology_method",
    "orthology_confidence",
    "identity_percent",
    "coverage_percent",
    "evalue",
    "bit_score",
    "pseudomonas_ortholog_group",
    "source_database",
    "source_url_or_page",
    "download_date",
    "notes"
]

merged = merged[final_cols]

# ============================================================
# Save
# ============================================================

merged.to_csv(
    OUT_SUPP,
    index=False
)

qc.to_csv(
    OUT_QC,
    index=False
)

# ============================================================
# Summary
# ============================================================

print("\n===============================")

print("Finished")

print("===============================")

print(f"Rows : {len(merged):,}")

print(f"High confidence : {(merged['orthology_confidence']=='High').sum():,}")

print(f"Need review : {(merged['orthology_confidence']=='Review').sum():,}")

print()

print(f"Average identity : {merged['identity_percent'].mean():.2f}%")

print(f"Average coverage : {merged['coverage_percent'].mean():.2f}%")

print()

print("Files created:")

print(OUT_SUPP)

print(OUT_QC)
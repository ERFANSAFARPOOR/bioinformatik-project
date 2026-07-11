from pathlib import Path
from datetime import datetime
import pandas as pd

# ============================================================
# Paths
# ============================================================

BASE = Path(__file__).resolve().parent.parent

GENES = BASE / "data" / "02_with_gene_names.csv"
BLAST = BASE / "results" / "blast_results.tsv"
RBH = BASE / "results" / "Supplementary_Table_S1_RBH.csv"
REVIEW = BASE / "results" / "Pairs_Needing_Review.csv"

OUTDIR = BASE / "results" / "final"
OUTDIR.mkdir(exist_ok=True)

today = datetime.today().strftime("%Y%m%d")

OUTPUT = OUTDIR / f"pao1_pa14_orthologs_pseudomonas_rbbh_{today}.csv"

# ============================================================
# Read gene mapping
# ============================================================

print("Reading ortholog mapping...")

df = pd.read_csv(GENES)

print(f"Rows : {len(df)}")

df = df.drop_duplicates(
    subset=["pao1_locus_tag", "pa14_locus_tag"]
)

# ============================================================
# Create Supplementary Table
# ============================================================

supp = pd.DataFrame()

supp["pa14_locus_tag"] = df["pa14_locus_tag"]
supp["pa14_gene_name"] = df["pa14_gene_name"]

supp["pao1_locus_tag"] = df["pao1_locus_tag"]
supp["pao1_gene_name"] = df["pao1_gene_name"]

# ============================================================
# Read BLAST
# ============================================================

print("\nReading BLAST results...")

blast = pd.read_csv(
    BLAST,
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

# ============================================================
# Coverage
# ============================================================

blast["coverage_percent"] = (
    blast["alignment_length"] /
    blast[["query_length", "subject_length"]].min(axis=1)
) * 100

blast["coverage_percent"] = (
    blast["coverage_percent"]
    .clip(upper=100)
    .round(2)
)

blast["identity_percent"] = blast["identity_percent"].round(2)
blast["bit_score"] = blast["bit_score"].round(2)

# ============================================================
# Best BLAST hit
# ============================================================

blast = (
    blast
    .sort_values(
        ["pao1_locus_tag", "bit_score", "evalue"],
        ascending=[True, False, True]
    )
    .drop_duplicates("pao1_locus_tag")
)

blast = blast[
    [
        "pao1_locus_tag",
        "blast_pa14_locus_tag",
        "identity_percent",
        "coverage_percent",
        "evalue",
        "bit_score"
    ]
]

# ============================================================
# Merge BLAST
# ============================================================

supp = supp.merge(
    blast,
    on="pao1_locus_tag",
    how="left"
)

# ============================================================
# Read RBH
# ============================================================

print("Reading RBH results...")

rbh = pd.read_csv(RBH)

rbh = (
    rbh[
        [
            "pao1_locus_tag",
            "reciprocal_best_hit"
        ]
    ]
    .drop_duplicates("pao1_locus_tag")
)

supp = supp.merge(
    rbh,
    on="pao1_locus_tag",
    how="left"
)

# ============================================================
# Confidence
# ============================================================

supp["orthology_confidence"] = "High"

supp.loc[
    supp["reciprocal_best_hit"] == "Yes",
    "orthology_confidence"
] = "Very High"

supp.loc[
    supp["reciprocal_best_hit"] == "No",
    "orthology_confidence"
] = "Review"

# ============================================================
# Manual Review
# ============================================================

if REVIEW.exists():

    review = pd.read_csv(REVIEW)

    review_pairs = set(
        zip(
            review["pao1_locus_tag"],
            review["pa14_locus_tag"]
        )
    )

    mask = supp.apply(
        lambda r:
        (
            r["pao1_locus_tag"],
            r["pa14_locus_tag"]
        ) in review_pairs,
        axis=1
    )

    supp.loc[
        mask,
        "orthology_confidence"
    ] = "Manual Review"

# ============================================================
# Metadata
# ============================================================

supp["orthology_method"] = (
    "Curated ortholog + Reciprocal Best BLAST Hit (RBH)"
)

supp["source_database"] = (
    "Pseudomonas Genome Database"
)

supp["source_url_or_page"] = (
    "https://www.pseudomonas.com"
)

supp["download_date"] = "2026-07-10"

supp["pseudomonas_ortholog_group"] = pd.NA

supp["notes"] = pd.NA

# ============================================================
# Remove helper column
# ============================================================

supp = supp.drop(
    columns=["blast_pa14_locus_tag"],
    errors="ignore"
)

# ============================================================
# Final column order
# ============================================================

final_columns = [

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

supp = supp[final_columns]

# ============================================================
# Final cleanup
# ============================================================

supp = supp.drop_duplicates(
    subset=[
        "pao1_locus_tag",
        "pa14_locus_tag"
    ]
)

# ============================================================
# Save
# ============================================================

supp.to_csv(
    OUTPUT,
    index=False
)

# ============================================================
# Summary
# ============================================================

print("\n==================================================")
print("Finished")
print("==================================================")

print(f"Rows : {len(supp):,}")

print(
    "Very High :",
    (supp["orthology_confidence"] == "Very High").sum()
)

print(
    "Review :",
    (supp["orthology_confidence"] == "Review").sum()
)

print(
    "Manual Review :",
    (supp["orthology_confidence"] == "Manual Review").sum()
)

print()

print(
    f"Mean identity : {supp['identity_percent'].mean():.2f}%"
)

print(
    f"Mean coverage : {supp['coverage_percent'].mean():.2f}%"
)

print()

print("Saved to:")

print(OUTPUT)
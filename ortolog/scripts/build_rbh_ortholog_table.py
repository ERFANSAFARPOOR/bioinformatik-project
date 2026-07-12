from pathlib import Path
from datetime import datetime
import pandas as pd

# ============================================================
# Paths
# ============================================================

BASE = Path(__file__).resolve().parent.parent

ORTHOLOG_FILE = BASE / "data" / "processed" / "with_gene_names.csv"

FORWARD_BLAST = BASE / "blast" / "blast_results.tsv"
REVERSE_BLAST = BASE / "blast" / "blast_reverse.tsv"

OUT_DIR = BASE / "results" / "final"
OUT_DIR.mkdir(exist_ok=True)

today = datetime.today().strftime("%Y%m%d")

OUTPUT = OUT_DIR / f"pao1_pa14_orthologs_pseudomonas_rbh_{today}.csv"

MANUAL_REVIEW = OUT_DIR / "Manual_Review_Orthologs.csv"

# ============================================================
# Read ortholog table
# ============================================================

print("Reading ortholog mapping...")

orthologs = pd.read_csv(ORTHOLOG_FILE)

print(f"Rows (raw): {len(orthologs):,}")

# Remove duplicated ortholog pairs only
orthologs = orthologs.drop_duplicates(
    subset=[
        "pao1_locus_tag",
        "pa14_locus_tag"
    ]
).reset_index(drop=True)

print(f"Rows (unique pairs): {len(orthologs):,}")

# ============================================================
# Build supplementary table
# ============================================================

supp = pd.DataFrame({

    "pa14_locus_tag":
        orthologs["pa14_locus_tag"],

    "pa14_gene_name":
        orthologs["pa14_gene_name"],

    "pao1_locus_tag":
        orthologs["pao1_locus_tag"],

    "pao1_gene_name":
        orthologs["pao1_gene_name"]

})

supp["orthology_method"] = (
    "Curated ortholog + Reciprocal Best BLAST Hit (RBH)"
)

supp["pseudomonas_ortholog_group"] = pd.NA

supp["source_database"] = (
    "Pseudomonas Genome Database"
)

supp["source_url_or_page"] = (
    "https://www.pseudomonas.com"
)

supp["download_date"] = "2026-07-10"

supp["notes"] = pd.NA

# ============================================================
# Read Forward BLAST
# ============================================================

print("\nReading forward BLAST...")

forward = pd.read_csv(
    FORWARD_BLAST,
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

# Numeric conversion

numeric_cols = [
    "identity_percent",
    "alignment_length",
    "query_length",
    "subject_length",
    "bit_score"
]

for col in numeric_cols:

    forward[col] = pd.to_numeric(
        forward[col],
        errors="coerce"
    )

# ============================================================
# Calculate BLAST coverage
# ============================================================

forward["coverage_percent"] = (
    forward["alignment_length"]
    /
    forward[
        [
            "query_length",
            "subject_length"
        ]
    ].min(axis=1)
    * 100
)

forward["coverage_percent"] = (
    forward["coverage_percent"]
    .clip(lower=0, upper=100)
    .round(2)
)

forward["identity_percent"] = (
    forward["identity_percent"]
    .clip(lower=0, upper=100)
    .round(2)
)

forward["bit_score"] = (
    forward["bit_score"]
    .round(2)
)

# ============================================================
# Best forward BLAST hit
# ============================================================

print("Selecting best forward hits...")

forward_best = (
    forward
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

print(f"Best forward hits : {len(forward_best):,}")

# ============================================================
# Merge BLAST statistics
# ============================================================

supp = supp.merge(

    forward_best[
        [
            "pao1_locus_tag",
            "blast_pa14_locus_tag",
            "identity_percent",
            "coverage_percent",
            "evalue",
            "bit_score"
        ]
    ],

    on="pao1_locus_tag",

    how="left"

)

print("Forward BLAST merged.")

# ============================================================
# Read reverse BLAST
# ============================================================

print("\nReading reverse BLAST...")

reverse = pd.read_csv(
    REVERSE_BLAST,
    sep="\t",
    header=None,
    names=[
        "pa14_locus_tag",
        "blast_pao1_locus_tag",
        "identity_percent",
        "alignment_length",
        "query_length",
        "subject_length",
        "evalue",
        "bit_score"
    ]
)

reverse_best = (
    reverse
    .sort_values(
        by=[
            "pa14_locus_tag",
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
        subset="pa14_locus_tag",
        keep="first"
    )
)

print(f"Best reverse hits : {len(reverse_best):,}")

# ============================================================
# Build lookup dictionaries
# ============================================================

forward_dict = dict(
    zip(
        forward_best["pao1_locus_tag"],
        forward_best["blast_pa14_locus_tag"]
    )
)

reverse_dict = dict(
    zip(
        reverse_best["pa14_locus_tag"],
        reverse_best["blast_pao1_locus_tag"]
    )
)

print("RBH dictionaries created.")
# ============================================================
# Reciprocal Best Hit (RBH)
# ============================================================

print("\nDetermining reciprocal best hits...")

supp["reciprocal_best_hit"] = supp.apply(
    lambda row:
        "Yes"
        if (
            forward_dict.get(row["pao1_locus_tag"]) == row["pa14_locus_tag"]
            and
            reverse_dict.get(row["pa14_locus_tag"]) == row["pao1_locus_tag"]
        )
        else "No",
    axis=1
)

# ============================================================
# Orthology confidence
# ============================================================

supp["orthology_confidence"] = supp["reciprocal_best_hit"].map(
    {
        "Yes": "Very High",
        "No": "Review"
    }
)

# ============================================================
# Remove duplicated ortholog pairs
# ============================================================

supp = (
    supp
    .drop_duplicates(
        subset=[
            "pao1_locus_tag",
            "pa14_locus_tag"
        ]
    )
    .reset_index(drop=True)
)

# ============================================================
# Manual review table
# ============================================================

review = supp[
    supp["reciprocal_best_hit"] == "No"
].copy()

print(f"Pairs requiring manual review : {len(review)}")

# ------------------------------------------------------------
# Guess possible reason
# ------------------------------------------------------------

def guess_reason(row):

    gene = str(row["pa14_gene_name"]).lower()

    if gene == "nan":
        gene = ""

    if gene.startswith("hcp"):
        return "Multiple Hcp paralogs"

    if gene.startswith("phz"):
        return "Phenazine biosynthesis gene family"

    if gene.startswith("tuf"):
        return "Multiple elongation factor copies"

    if gene.startswith("pil"):
        return "Pilin gene family"

    if gene.startswith("mex"):
        return "Regulatory gene family"

    return "Manual inspection required"


review["possible_reason"] = review.apply(
    guess_reason,
    axis=1
)

review.to_csv(
    MANUAL_REVIEW,
    index=False
)

# ============================================================
# Remove helper columns
# ============================================================

supp.drop(
    columns=["blast_pa14_locus_tag"],
    inplace=True,
    errors="ignore"
)

# ============================================================
# Sort table
# ============================================================

supp = (
    supp
    .sort_values("pao1_locus_tag")
    .reset_index(drop=True)
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
    "reciprocal_best_hit",
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

for column in final_columns:

    if column not in supp.columns:
        supp[column] = pd.NA

supp = supp[final_columns]

# ============================================================
# Save final table
# ============================================================

supp.to_csv(
    OUTPUT,
    index=False
)

# ============================================================
# Summary
# ============================================================

print("\n" + "=" * 60)
print("Finished")
print("=" * 60)

print(f"Rows : {len(supp):,}")

rbh_count = (
    supp["reciprocal_best_hit"] == "Yes"
).sum()

review_count = (
    supp["reciprocal_best_hit"] == "No"
).sum()

print(f"RBH confirmed : {rbh_count:,}")
print(f"Need review : {review_count:,}")

print()

print(
    f"Mean identity : "
    f"{supp['identity_percent'].mean():.2f}%"
)

print(
    f"Mean coverage : "
    f"{supp['coverage_percent'].mean():.2f}%"
)

print()

print("Files created:")

print(f"  {OUTPUT}")
print(f"  {MANUAL_REVIEW}")
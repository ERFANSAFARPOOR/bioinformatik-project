from pathlib import Path
import pandas as pd

# ============================================================
# Paths
# ============================================================

BASE = Path(__file__).resolve().parent.parent

INPUT = BASE / "results" / "Supplementary_Table_S1_RBH.csv"
OUTPUT = BASE / "results" / "Pairs_Needing_Review.csv"

# ============================================================
# Read RBH table
# ============================================================

print("Reading RBH table...")

df = pd.read_csv(INPUT)

failed = df.loc[
    df["reciprocal_best_hit"] == "No"
].copy()

print(f"Pairs requiring manual review : {len(failed)}")

# ============================================================
# Possible reasons
# ============================================================

RULES = {
    "hcp": "Multiple Hcp paralogs",
    "phz": "Phenazine biosynthesis gene family",
    "pil": "Type IV pilus gene family",
    "mex": "Regulatory gene family",
    "tuf": "Multiple elongation factor copies"
}


def guess_reason(gene):

    if pd.isna(gene):
        return "Manual inspection required"

    gene = gene.lower()

    for prefix, reason in RULES.items():

        if gene.startswith(prefix):
            return reason

    return "Manual inspection required"


failed["possible_reason"] = (
    failed["pa14_gene_name"]
    .apply(guess_reason)
)

# ============================================================
# Output columns
# ============================================================

columns = [
    "pao1_locus_tag",
    "pao1_gene_name",
    "pa14_locus_tag",
    "pa14_gene_name",
    "orthology_method",
    "reciprocal_best_hit",
    "orthology_confidence",
    "possible_reason"
]

failed = failed[columns]

# ============================================================
# Save
# ============================================================

failed.to_csv(
    OUTPUT,
    index=False
)

# ============================================================
# Summary
# ============================================================

print("\n===============================")
print("Finished")
print("===============================")

print(f"Pairs requiring review : {len(failed):,}")

print("\nSaved to:")
print(OUTPUT)
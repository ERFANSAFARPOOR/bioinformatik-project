from pathlib import Path
import pandas as pd

# ============================================================
# Paths
# ============================================================

BASE = Path(__file__).resolve().parent.parent

SUPP = BASE / "results" / "Supplementary_Table_S1.csv"
FORWARD = BASE / "results" / "blast_results.tsv"
REVERSE = BASE / "results" / "blast_reverse.tsv"

OUT = BASE / "results" / "Supplementary_Table_S1_RBH.csv"

# ============================================================
# Read Supplementary Table
# ============================================================

print("Reading supplementary table...")

supp = pd.read_csv(SUPP)

print(f"Rows : {len(supp)}")

# ------------------------------------------------------------
# Basic validation
# ------------------------------------------------------------

required = ["pao1_locus_tag", "pa14_locus_tag"]

missing = [c for c in required if c not in supp.columns]

if missing:
    raise ValueError(f"Missing required columns: {missing}")

if supp["pao1_locus_tag"].isna().any():
    raise ValueError("Missing PAO1 locus tags detected.")

if supp["pa14_locus_tag"].isna().any():
    raise ValueError("Missing PA14 locus tags detected.")

# ============================================================
# Read Forward BLAST
# ============================================================

print("Reading forward BLAST...")

forward = pd.read_csv(
    FORWARD,
    sep="\t",
    header=None,
    names=[
        "pao1",
        "pa14",
        "identity",
        "length",
        "qlen",
        "slen",
        "evalue",
        "bitscore"
    ]
)

forward = (
    forward
    .sort_values(
        ["pao1", "bitscore", "evalue"],
        ascending=[True, False, True]
    )
    .drop_duplicates(
        subset="pao1",
        keep="first"
    )
)

# ============================================================
# Read Reverse BLAST
# ============================================================

print("Reading reverse BLAST...")

reverse = pd.read_csv(
    REVERSE,
    sep="\t",
    header=None,
    names=[
        "pa14",
        "pao1",
        "identity",
        "length",
        "qlen",
        "slen",
        "evalue",
        "bitscore"
    ]
)

reverse = (
    reverse
    .sort_values(
        ["pa14", "bitscore", "evalue"],
        ascending=[True, False, True]
    )
    .drop_duplicates(
        subset="pa14",
        keep="first"
    )
)

print(f"Forward best hits : {len(forward)}")
print(f"Reverse best hits : {len(reverse)}")

# ============================================================
# Create dictionaries
# ============================================================

forward_dict = dict(zip(forward["pao1"], forward["pa14"]))
reverse_dict = dict(zip(reverse["pa14"], reverse["pao1"]))

# ============================================================
# Reciprocal Best Hits
# ============================================================

rbh = []

for _, row in supp.iterrows():

    pao = row["pao1_locus_tag"]
    pa14 = row["pa14_locus_tag"]

    if (
        forward_dict.get(pao) == pa14
        and
        reverse_dict.get(pa14) == pao
    ):
        rbh.append("Yes")
    else:
        rbh.append("No")

supp["reciprocal_best_hit"] = rbh

# ============================================================
# Orthology Confidence
# ============================================================

supp["orthology_confidence"] = (
    supp["reciprocal_best_hit"]
    .map({
        "Yes": "Very High",
        "No": "Review"
    })
)

# ============================================================
# Save
# ============================================================

supp.to_csv(
    OUT,
    index=False
)

# ============================================================
# Summary
# ============================================================

yes = (supp["reciprocal_best_hit"] == "Yes").sum()
no = (supp["reciprocal_best_hit"] == "No").sum()

print("\n===============================")
print("Finished")
print("===============================")

print(f"RBH confirmed : {yes:,}")
print(f"Need review   : {no:,}")

print("\nOutput file:")
print(OUT)
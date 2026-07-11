from pathlib import Path
import pandas as pd

# ============================================================
# Paths
# ============================================================

BASE = Path(__file__).resolve().parent.parent

FINAL_DIR = BASE / "results" / "final"

csv_files = sorted(
    FINAL_DIR.glob("pao1_pa14_orthologs_pseudomonas_rbbh_*.csv")
)

if not csv_files:
    raise FileNotFoundError(
        "No final ortholog table found."
    )

TABLE = csv_files[-1]

# ============================================================
# Read table
# ============================================================

df = pd.read_csv(TABLE)

print("=" * 60)
print("VALIDATING")
print(TABLE.name)
print("=" * 60)

errors = []

# ============================================================
# Required columns
# ============================================================

required = [
    "pa14_locus_tag",
    "pao1_locus_tag",
    "orthology_method",
    "orthology_confidence",
    "source_database",
    "download_date",
    "identity_percent",
    "coverage_percent",
    "evalue",
    "bit_score"
]

for col in required:

    if col not in df.columns:
        raise ValueError(f"Missing required column: {col}")

# ============================================================
# Basic statistics
# ============================================================

print(f"Rows: {len(df)}")

# ============================================================
# Duplicate ortholog pairs
# ============================================================

dup = df.duplicated(
    subset=[
        "pao1_locus_tag",
        "pa14_locus_tag"
    ]
)

duplicate_count = dup.sum()

print(f"Duplicate pairs: {duplicate_count}")

if duplicate_count:
    errors.append(df[dup])

# ============================================================
# Missing values
# ============================================================

missing_summary = {}

for col in [
    "pa14_locus_tag",
    "pao1_locus_tag",
    "orthology_method",
    "orthology_confidence",
    "source_database",
    "download_date"
]:

    n = df[col].isna().sum()

    missing_summary[col] = n

    print(f"{col}: missing={n}")

# ============================================================
# Identity
# ============================================================

bad_identity = df[
    df["identity_percent"].isna()
    |
    (df["identity_percent"] < 0)
    |
    (df["identity_percent"] > 100)
]

print(f"Bad identity: {len(bad_identity)}")

if len(bad_identity):
    errors.append(bad_identity)

# ============================================================
# Coverage
# ============================================================

bad_coverage = df[
    df["coverage_percent"].isna()
    |
    (df["coverage_percent"] < 0)
    |
    (df["coverage_percent"] > 100)
]

print(f"Bad coverage: {len(bad_coverage)}")

if len(bad_coverage):
    errors.append(bad_coverage)

# ============================================================
# E-value
# ============================================================

bad_evalue = df[
    df["evalue"].isna()
    |
    (df["evalue"] < 0)
]

print(f"Negative evalue: {len(bad_evalue)}")

if len(bad_evalue):
    errors.append(bad_evalue)

# ============================================================
# Bit score
# ============================================================

bad_bitscore = df[
    df["bit_score"].isna()
    |
    (df["bit_score"] < 0)
]

print(f"Negative bit score: {len(bad_bitscore)}")

if len(bad_bitscore):
    errors.append(bad_bitscore)

# ============================================================
# Confidence values
# ============================================================

allowed = {
    "Very High",
    "High",
    "Review",
    "Manual Review"
}

bad_confidence = df[
    ~df["orthology_confidence"].isin(allowed)
]

print(f"Invalid confidence: {len(bad_confidence)}")

if len(bad_confidence):
    errors.append(bad_confidence)

# ============================================================
# Gene names
# ============================================================

missing_pao1_gene = df["pao1_gene_name"].isna().sum()
missing_pa14_gene = df["pa14_gene_name"].isna().sum()

print()
print(f"Missing PAO1 gene names: {missing_pao1_gene}")
print(f"Missing PA14 gene names: {missing_pa14_gene}")

# ============================================================
# Statistics
# ============================================================

mean_identity = df["identity_percent"].mean()
mean_coverage = df["coverage_percent"].mean()

print()
print(f"Mean identity: {mean_identity:.2f}")
print(f"Mean coverage: {mean_coverage:.2f}")

# ============================================================
# Validation status
# ============================================================

validation_passed = len(errors) == 0

# ============================================================
# Save report
# ============================================================

REPORT = FINAL_DIR / "Validation_Report.txt"

with open(REPORT, "w", encoding="utf-8") as f:

    f.write("Validation Report\n")
    f.write("=" * 40 + "\n\n")

    f.write(f"File: {TABLE.name}\n")
    f.write(f"Rows: {len(df)}\n")
    f.write(f"Duplicate pairs: {duplicate_count}\n\n")

    f.write("Missing values\n")

    for col, n in missing_summary.items():
        f.write(f"  {col}: {n}\n")

    f.write("\n")

    f.write(f"Bad identity: {len(bad_identity)}\n")
    f.write(f"Bad coverage: {len(bad_coverage)}\n")
    f.write(f"Negative evalue: {len(bad_evalue)}\n")
    f.write(f"Negative bit score: {len(bad_bitscore)}\n")
    f.write(f"Invalid confidence: {len(bad_confidence)}\n\n")

    f.write(f"Missing PAO1 gene names: {missing_pao1_gene}\n")
    f.write(f"Missing PA14 gene names: {missing_pa14_gene}\n\n")

    f.write(f"Mean identity: {mean_identity:.2f}\n")
    f.write(f"Mean coverage: {mean_coverage:.2f}\n\n")

    f.write(
        f"Validation Status: {'PASSED' if validation_passed else 'FAILED'}\n"
    )

print()
print("Report saved:")
print(REPORT)

# ============================================================
# Save errors
# ============================================================

if errors:

    ERROR_FILE = FINAL_DIR / "Validation_Errors.csv"

    (
        pd.concat(errors)
        .drop_duplicates()
        .to_csv(ERROR_FILE, index=False)
    )

    print()
    print("Validation FAILED")
    print(ERROR_FILE)

else:

    print()
    print("Validation PASSED")
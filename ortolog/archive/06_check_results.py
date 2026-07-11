from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parent.parent

df = pd.read_csv(BASE / "results" / "05_alignment_results.csv")

print(df[[
    "pao1_locus_tag",
    "pa14_locus_tag",
    "identity_percent",
    "coverage_percent"
]].head(20))

print("\nIdentity statistics")
print(df["identity_percent"].describe())

print("\nCoverage statistics")
print(df["coverage_percent"].describe())
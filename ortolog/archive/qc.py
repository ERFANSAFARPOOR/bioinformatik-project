from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parent.parent

INPUT = BASE / "results" / "Supplementary_Table_S1_Final.csv"

df = pd.read_csv(INPUT)

review = df[df["reciprocal_best_hit"]=="No"]

review.to_csv(
    BASE/"results"/"Manual_Review_Orthologs.csv",
    index=False
)

print(review)

print()

print("Pairs needing review:",len(review))
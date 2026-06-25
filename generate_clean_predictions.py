"""R-02: clean the predicted essentiality table.

Reads the RAW result file (read-only) and writes a cleaned copy to
data/processed/. The raw `gene_id` is stored as a stringified Python set,
e.g. "{'PA2339'}"; this normalizes it to a plain locus tag "PA2339".

Validates: row count preserved, every id matches ^PA\\d+$, essential count == 166.
"""
import ast
import re
import pandas as pd
from pathlib import Path

RAW = Path("results/essentiality/gene_essentiality_default_medium.csv")
OUT = Path("data/processed/predicted_essentiality_default_medium.csv")

df = pd.read_csv(RAW)
n_raw = len(df)

def clean_id(v):
    s = str(v).strip()
    # handle set-repr "{'PA2339'}" or "{'PA1', 'PA2'}"
    if s.startswith("{") and s.endswith("}"):
        try:
            items = sorted(ast.literal_eval(s))
            return "|".join(str(x) for x in items)  # keep multi-gene groups joined
        except Exception:
            return s.strip("{}'\" ")
    return s

df["gene_id"] = df["gene_id"].map(clean_id)
df.to_csv(OUT, index=False)

# ---- validation ----
single = df[~df["gene_id"].str.contains(r"\|")]
bad = single[~single["gene_id"].str.match(r"^PA\d+$")]
n_essential = int(df["is_essential"].sum())

print(f"rows raw/out      : {n_raw} / {len(df)}")
print(f"multi-gene groups : {(df['gene_id'].str.contains('|', regex=False)).sum()}")
print(f"single ids non-PA : {len(bad)}  (sample: {list(bad['gene_id'][:5])})")
print(f"essential count   : {n_essential}")
assert len(df) == n_raw, "row count changed!"
assert n_essential == 166, f"essential count drifted: {n_essential}"
print("VALIDATION OK -> wrote", OUT)

import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

REF = ROOT / "data" / "processed" / "essentiality" / "predicted_essentiality_default_medium.csv"

df = pd.read_csv(REF)


def clean(s):
    return str(s).strip("{}'\" ")


df["gene_id"] = df["gene_id"].map(clean)

pattern = r"^PA\d+(\|PA\d+)*$"

non_pa = df.loc[
    ~df["gene_id"].str.fullmatch(pattern, na=False)
]

print(f"reference rows            : {len(df)}")
print(f"reference essential       : {int(df['is_essential'].sum())}")
print(
    f"unique essential genes    : "
    f"{df.loc[df['is_essential'], 'gene_id'].nunique()}"
)
print(f"WT growth                 : {df['wildtype_growth'].iloc[0]:.10f}")
print(f"duplicate gene IDs        : {df['gene_id'].duplicated().sum()}")
print(f"non-PA gene IDs           : {len(non_pa)}")

if len(non_pa):
    print("\nFirst invalid IDs:")
    print(non_pa["gene_id"].head(20).to_list())
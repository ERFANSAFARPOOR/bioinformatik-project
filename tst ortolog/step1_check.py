import pandas as pd

df = pd.read_csv("pao1_pa14_orthologs_pseudomonas.csv")

# حذف ردیف‌هایی که Locus Tag ندارند
df = df.dropna(subset=["Locus Tag (Query)", "Locus Tag (Hit)"])

print(df.shape)

# ذخیره فایل تمیز
df.to_csv("01_raw_orthologs_clean.csv", index=False)
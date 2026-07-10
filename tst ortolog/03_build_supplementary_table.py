import pandas as pd
from datetime import date

# ---------- خواندن فایل مرحله قبل ----------
df = pd.read_csv("data/02_with_gene_names.csv")

# ---------- ساخت جدول استاندارد ----------
supp = pd.DataFrame()

supp["pa14_locus_tag"] = df["pa14_locus_tag"]
supp["pa14_gene_name"] = df["pa14_gene_name"]

supp["pao1_locus_tag"] = df["pao1_locus_tag"]
supp["pao1_gene_name"] = df["pao1_gene_name"]

supp["orthology_method"] = "Curated ortholog (Pseudomonas Genome Database)"

supp["orthology_confidence"] = "High"

supp["identity_percent"] = pd.NA
supp["coverage_percent"] = pd.NA
supp["evalue"] = pd.NA
supp["bit_score"] = pd.NA

supp["pseudomonas_ortholog_group"] = pd.NA

supp["source_database"] = "Pseudomonas Genome Database"

supp["source_url_or_page"] = "https://www.pseudomonas.com"

supp["download_date"] = str(date.today())

supp["notes"] = pd.NA

# ---------- ذخیره ----------
supp.to_csv("results/03_supplementary_table.csv", index=False)

print(supp.head())

print("\nRows:", len(supp))
print("Columns:", len(supp.columns))
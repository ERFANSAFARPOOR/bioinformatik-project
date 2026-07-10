import pandas as pd
import re

# ---------- تابع استخراج Alias و Gene Name از فایل GFF ----------
def build_gene_dictionary(gff_file):
    gene_dict = {}

    with open(gff_file, encoding="utf-8") as f:
        for line in f:

            if line.startswith("#"):
                continue

            cols = line.strip().split("\t")

            if len(cols) != 9:
                continue

            # فقط Feature های gene
            if cols[2] != "gene":
                continue

            attributes = cols[8]

            alias = re.search(r'Alias=([^;]+)', attributes)
            gene = re.search(r'name=([^;]+)', attributes)

            if alias:
                locus = alias.group(1)

                if gene:
                    gene_name = gene.group(1)
                else:
                    gene_name = "NA"

                gene_dict[locus] = gene_name

    return gene_dict


# ---------- ساخت دیکشنری ----------
pa14_dict = build_gene_dictionary("features.gff")
pao1_dict = build_gene_dictionary("features (1).gff")

print("PA14 genes:", len(pa14_dict))
print("PAO1 genes:", len(pao1_dict))


# ---------- خواندن جدول Ortholog ----------
df = pd.read_csv("01_raw_orthologs_clean.csv")


# ---------- تشخیص اینکه Query کدام سوی مقایسه است ----------
is_pao1_query = df["Strain (Query)"].str.contains("PAO1", case=False)


# ---------- استخراج Locus Tag ----------
df["pao1_locus_tag"] = df["Locus Tag (Query)"].where(
    is_pao1_query,
    df["Locus Tag (Hit)"]
)

df["pa14_locus_tag"] = df["Locus Tag (Hit)"].where(
    is_pao1_query,
    df["Locus Tag (Query)"]
)


# ---------- اضافه کردن Gene Name ----------
df["pao1_gene_name"] = df["pao1_locus_tag"].map(pao1_dict).fillna("NA")
df["pa14_gene_name"] = df["pa14_locus_tag"].map(pa14_dict).fillna("NA")


# ---------- ذخیره ----------
df.to_csv("02_with_gene_names.csv", index=False)

print("\nDone!")
print(df[[
    "pao1_locus_tag",
    "pao1_gene_name",
    "pa14_locus_tag",
    "pa14_gene_name"
]].head())

from Bio import SeqIO
import pandas as pd

#reading FASTA
def load_fasta_dict(fasta_file):
    seq_dict = {}

    for record in SeqIO.parse(fasta_file, "fasta"):
        locus = record.id.split()[0]
        seq_dict[locus] = str(record.seq)

    return seq_dict


print("Loading protein sequences...")

pao1 = load_fasta_dict("data/PAO1_protein_PGD.faa")
pa14 = load_fasta_dict("data/PA14_protein_PGD.faa")

print("PAO1 proteins:", len(pao1))
print("PA14 proteins:", len(pa14))

# reading the table
df = pd.read_csv("results/03_supplementary_table.csv")

# add sequence
df["pao1_sequence"] = df["pao1_locus_tag"].map(pao1)
df["pa14_sequence"] = df["pa14_locus_tag"].map(pa14)

# static
print("\nMissing PAO1 sequences:",
      df["pao1_sequence"].isna().sum())

print("Missing PA14 sequences:",
      df["pa14_sequence"].isna().sum())

# save
df.to_csv(
    "results/04_sequences_added.csv",
    index=False
)

print("\nDone.")

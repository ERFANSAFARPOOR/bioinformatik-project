from pathlib import Path
import pandas as pd
from Bio import pairwise2

BASE = Path(__file__).resolve().parent.parent

INPUT = BASE / "results" / "04_sequences_added.csv"
OUTPUT = BASE / "results" / "05_alignment_results.csv"

df = pd.read_csv(INPUT)

identity_list = []
coverage_list = []

total = len(df)

print(f"Processing {total} ortholog pairs...\n")

for i, row in df.iterrows():

    seq1 = row["pao1_sequence"]
    seq2 = row["pa14_sequence"]

    if pd.isna(seq1) or pd.isna(seq2):
        identity_list.append(None)
        coverage_list.append(None)
        continue

    aln = pairwise2.align.globalxx(
        seq1,
        seq2,
        one_alignment_only=True
    )[0]

    aln1 = aln.seqA
    aln2 = aln.seqB

    matches = 0
    aligned = 0

    for a, b in zip(aln1, aln2):

        if a != "-" and b != "-":
            aligned += 1

            if a == b:
                matches += 1

    identity = matches / aligned * 100 if aligned else None

    coverage = aligned / max(len(seq1), len(seq2)) * 100

    identity_list.append(round(identity,2))
    coverage_list.append(round(coverage,2))

    if (i+1)%100==0:
        print(f"{i+1}/{total}")

df["identity_percent"]=identity_list
df["coverage_percent"]=coverage_list

df.to_csv(OUTPUT,index=False)

print("\nFinished.")
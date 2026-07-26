"""
G-01: Build PAO1 <-> PA14 mapping using the OFFICIAL Pseudomonas ortholog table.

Inputs
------
models/paeruginosa_MODEL1507180020.xml

data/raw/ortholog/
    pao1_feature_table.txt.gz
    pa14_feature_table.txt.gz
    pao1_pa14_orthologs_pseudomonas.csv


Outputs
-------
data/processed/gene_mapping/gene_mapping.csv
data/processed/gene_mapping/gene_mapping_coverage.txt
"""
import csv
import gzip
import io
from collections import defaultdict
from pathlib import Path

from cobra.io import read_sbml_model

ROOT = Path(__file__).resolve().parents[2]

ORTHO = ROOT / "data" / "raw" / "ortholog"

OUT = ROOT / "data" / "processed" / "gene_mapping" / "gene_mapping.csv"
REPORT = ROOT / "data" / "processed" / "gene_mapping" /  "gene_mapping_coverage.txt"

OUT.parent.mkdir(parents=True, exist_ok=True)
REPORT.parent.mkdir(parents=True, exist_ok=True)


#############################################################
# utilities
#############################################################

def open_table(stem):

    txt = ORTHO / f"{stem}.txt"

    if txt.exists():
        return open(txt, encoding="utf-8")

    return io.TextIOWrapper(
        gzip.open(ORTHO / f"{stem}.txt.gz", "rb"),
        encoding="utf-8"
    )


#############################################################
# parse feature table
#############################################################

def parse_feature_table(stem):

    rows = {}

    with open_table(stem) as f:

        header = f.readline().lstrip("#").rstrip("\r\n").split("\t")

        idx = {h:i for i,h in enumerate(header)}

        for line in f:

            p = line.rstrip("\r\n").split("\t")

            if p[0]!="gene":
                continue

            attrs = p[idx["attributes"]]

            old=""

            for a in attrs.split(";"):

                if a.startswith("old_locus_tag="):
                    old=a.split("=",1)[1]

            rows[p[idx["locus_tag"]]]={

                "symbol":p[idx["symbol"]],

                "geneid":p[idx["GeneID"]],

                "product":p[idx["name"]],

                "old_locus_tag":old

            }

    return rows


#############################################################
# load feature tables
#############################################################

pao1=parse_feature_table("pao1_feature_table")

pa14=parse_feature_table("pa14_feature_table")


#############################################################
# official orthology
#############################################################

orthologs=defaultdict(list)

with open(
    ORTHO/"pao1_pa14_orthologs_pseudomonas.csv",
    encoding="utf-8-sig"
) as f:

    reader=csv.DictReader(f)

    for r in reader:

        pao=r["Locus Tag (Query)"].strip()

        pa14lt=r["Locus Tag (Hit)"].strip()

        orthologs[pao].append(pa14lt)


#############################################################
# model
#############################################################

model=read_sbml_model(
    ROOT/"models/paeruginosa_MODEL1507180020.xml"
)

genes=sorted(g.id for g in model.genes)


#############################################################
# output
#############################################################

cols=[

"model_gene_id",

"pao1_locus_tag",

"gene_symbol",

"gene_name",

"pao1_geneid",

"pa14_locus_tag",

"pa14_geneid",

"mapping_method",

"mapping_confidence",

"n_pa14_matches",

"ambiguous",

"notes"

]

stats=defaultdict(int)

rows=[]

for gid in genes:

    row={c:"" for c in cols}

    row["model_gene_id"]=gid

    row["pao1_locus_tag"]=gid

    info=pao1.get(gid)

    if info:

        row["gene_symbol"]=info["symbol"]

        row["gene_name"]=info["product"]

        row["pao1_geneid"]=info["geneid"]

    hits=orthologs.get(gid,[])

    row["n_pa14_matches"]=len(hits)

    if len(hits)==0:

        row["mapping_method"]="official_orthology"

        row["mapping_confidence"]="unmapped"

        row["ambiguous"]="False"

        row["notes"]="No PA14 ortholog in official table."

        stats["unmapped"]+=1

    elif len(hits)==1:

        pa14lt=hits[0]

        row["pa14_locus_tag"]=pa14lt

        row["mapping_method"]="official_orthology"

        row["mapping_confidence"]="high"

        row["ambiguous"]="False"

        stats["unique"]+=1

        if pa14lt in pa14:

            row["pa14_geneid"]=pa14[pa14lt]["geneid"]

    else:

        row["pa14_locus_tag"]="AMBIGUOUS"

        row["mapping_method"]="official_orthology"

        row["mapping_confidence"]="medium"

        row["ambiguous"]="True"

        row["notes"]="; ".join(hits)

        stats["ambiguous"]+=1

    rows.append(row)


#############################################################
# write csv
#############################################################

with open(OUT,"w",newline="",encoding="utf-8") as f:

    writer=csv.DictWriter(f,fieldnames=cols)

    writer.writeheader()

    writer.writerows(rows)


#############################################################
# report
#############################################################

lines=[

"Gene Mapping Report",

"===================",

f"Model genes              : {len(genes)}",

f"Unique mappings          : {stats['unique']}",

f"Ambiguous mappings       : {stats['ambiguous']}",

f"Unmapped                 : {stats['unmapped']}",

"",

"Mapping source:",

"Official pseudomonas.com orthology table",

"",

"Confidence:",

"High    = unique ortholog",

"Medium  = multiple orthologs",

"Unmapped= no ortholog"

]

REPORT.write_text("\n".join(lines),encoding="utf-8")

print("\n".join(lines))

print()

print(f"Wrote {OUT}")

print(f"Wrote {REPORT}")

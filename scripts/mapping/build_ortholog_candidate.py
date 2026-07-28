#!/usr/bin/env python
"""Build the CANDIDATE PAO1<->PA14 ortholog table from the Turner 2015 supplement.

Source: data/raw/literature/turner2015/pnas.1419677112.sd03.xlsx (col A PA14 Locus
ID <-> col J PAO1 Locus ID), the Pseudomonas Genome Database BLAST+synteny 1:1
ortholog subset embedded in the peer-reviewed supplement. sd04 is used as an
internal consistency check; Belanger 2022 DS1 as an independent cross-check.

Output: data/processed/ortholog/pao1_pa14_orthologs_turner2015_CANDIDATE.csv
Status: CANDIDATE / HUMAN_REVIEW_REQUIRED. Not merged into gene_mapping.csv, not
used to parse Poulsen/Basta or compute metrics. See ORTHOLOG_CANDIDATE_TABLE.md.

Run under reccobra39.
"""
import csv
import os
import re
from collections import Counter

import openpyxl

PA14 = re.compile(r"^PA14_\d{5}$")
PAO1 = re.compile(r"^PA\d{4}$")

TURNER_SD03 = "data/raw/literature/turner2015/pnas.1419677112.sd03.xlsx"
TURNER_SD04 = "data/raw/literature/turner2015/pnas.1419677112.sd04.xlsx"
BELANGER = "data/raw/literature/belanger2022/Data_Sheet_1.XLSX"
OUT = "data/processed/ortholog/pao1_pa14_orthologs_turner2015_CANDIDATE.csv"


def load_turner(path):
    """Rows 0-2 are title/header/subheader; data begins at row index 3."""
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb["Sheet1"]
    pairs, pa14_only, pao1_only = [], 0, 0
    for i, row in enumerate(ws.iter_rows(values_only=True)):
        if i < 3:
            continue
        pa14 = str(row[0]).strip() if row[0] else ""
        pa14_g = str(row[1]).strip() if row[1] else ""
        pao1 = str(row[9]).strip() if row[9] else ""
        pao1_g = str(row[10]).strip() if row[10] else ""
        has14, has01 = bool(PA14.match(pa14)), bool(PAO1.match(pao1))
        if has14 and has01:
            pairs.append((pa14, pao1, pa14_g, pao1_g))
        elif has14:
            pa14_only += 1
        elif has01:
            pao1_only += 1
    wb.close()
    return pairs, pa14_only, pao1_only


def load_belanger():
    wb = openpyxl.load_workbook(BELANGER, read_only=True, data_only=True)
    ws = wb["T0_PAO1_essential_genes"]
    bel = {}
    for i, row in enumerate(ws.iter_rows(values_only=True)):
        if i < 2:
            continue
        pao1 = str(row[0]).strip() if row[0] else ""
        pa14 = str(row[1]).strip() if row[1] else ""
        if PAO1.match(pao1) and PA14.match(pa14):
            bel[pao1] = pa14
    wb.close()
    return bel


def main():
    sd03, only14, only01 = load_turner(TURNER_SD03)
    sd04, _, _ = load_turner(TURNER_SD04)
    assert {(a, b) for a, b, _, _ in sd03} == {(a, b) for a, b, _, _ in sd04}, \
        "sd03/sd04 pairing mismatch — investigate before trusting the table"

    pao1_counts = Counter(b for _, b, _, _ in sd03)
    pa14_counts = Counter(a for a, _, _, _ in sd03)
    assert sd03, "No ortholog pairs loaded from Turner sd03."
    assert max(pao1_counts.values()) == 1 and max(pa14_counts.values()) == 1, \
        "table is not strict 1:1 — handle one-to-many explicitly before using"

    bel = load_belanger()

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([
            "pao1_locus_tag", "pa14_locus_tag", "pao1_gene", "pa14_gene",
            "gene_symbol_match", "belanger_crosscheck", "source", "method",
            "confidence", "review_flag",
        ])
        for pa14, pao1, g14, g01 in sd03:
            gm = "yes" if (g14 and g01 and g14.lower() == g01.lower()) \
                else ("na" if not (g14 and g01) else "no")
            xc = ("agree" if bel[pao1] == pa14 else "disagree") if pao1 in bel \
                else "not_in_belanger"
            w.writerow([
                pao1, pa14, g01, g14, gm, xc,
                "Turner et al. 2015 PNAS sd03 "
                "(Pseudomonas Genome Database BLAST+synteny 1:1 orthologs)",
                "RBB+synteny (pseudomonas.com, 2015 vintage)",
                "candidate_medium", "HUMAN_REVIEW_REQUIRED",
            ])

turner_map = {b: a for a, b, _, _ in sd03}

agree = sum(
    1
    for p, x in bel.items()
    if p in turner_map and turner_map[p] == x
)
for pa14, pao1, g14, g01 in sorted(sd03, key=lambda x: x[1]):
    
    print(f"pairs={len(sd03)} pa14_only={only14} pao1_only={only01}")
    print(f"belanger_shared_agree={agree}/"
          f"{sum(1 for p in bel if p in pao1_counts)}")
    print("wrote", OUT)


if __name__ == "__main__":
    main()

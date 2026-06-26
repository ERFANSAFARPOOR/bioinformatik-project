"""G-01: Build a reproducible PAO1 <-> PA14 <-> model gene mapping.

Sources (authoritative, downloaded 2026-06-26; see DATA_PROVENANCE.md):
  - PAO1 RefSeq feature table  GCF_000006765.1_ASM676v1
  - PA14  RefSeq feature table  GCF_000014625.1_ASM1462v1

Mapping layers and their evidence/confidence:
  1. model_gene_id == PAO1 locus_tag  -> identity (high); model is iMO1056/PAO1.
  2. PAO1 gene symbol from PAO1 RefSeq (join on PA#### locus_tag) -> authoritative.
  3. PA14 classic locus tag (old_locus_tag PA14_#####) via PAO1<->PA14 gene-symbol
     match. This is RefSeq ANNOTATION-SYMBOL identity, NOT validated orthology
     (pseudomonas.com / OrthologueDB unreachable from this environment - B-NET).
     - unique symbol on both sides -> 'symbol_unique' (medium)
     - symbol maps to >1 PA14 gene, or PAO1 symbol non-unique -> 'symbol_ambiguous'
       (low); ALL candidates listed, never silently resolved.
     - no symbol / no match -> 'unmapped' (PA14 = PENDING).

NO ambiguous/one-to-many mapping is silently collapsed. Every row records method,
confidence, evidence, and (for ambiguous) the full candidate list.
"""
import csv
from collections import defaultdict
from pathlib import Path

import cobra
from cobra.io import read_sbml_model

ORTHO = Path("data/raw/ortholog")
OUT = Path("data/processed/gene_mapping.csv")
REPORT = Path("data/processed/gene_mapping_coverage.txt")

PAO1_ASM = "GCF_000006765.1_ASM676v1"
PA14_ASM = "GCF_000014625.1_ASM1462v1"

def _open_table(stem):
    """Open <stem>.txt if present, else gunzip <stem>.txt.gz (committed raw)."""
    import gzip, io
    txt = ORTHO / f"{stem}.txt"
    if txt.exists():
        return open(txt, encoding="utf-8")
    return io.TextIOWrapper(gzip.open(ORTHO / f"{stem}.txt.gz", "rb"), encoding="utf-8")

def parse_feature_table(stem):
    """Return list of dicts for 'gene' rows: locus_tag, symbol, geneid, old_locus_tag, product."""
    rows = []
    with _open_table(stem) as f:
        header = f.readline().lstrip("#").strip().split("\t")
        idx = {name: i for i, name in enumerate(header)}
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if not parts or parts[0] != "gene":
                continue
            attrs = parts[idx["attributes"]] if idx.get("attributes", -1) < len(parts) else ""
            old_lt = ""
            for a in attrs.split(";"):
                if a.startswith("old_locus_tag="):
                    old_lt = a.split("=", 1)[1]
            rows.append({
                "locus_tag": parts[idx["locus_tag"]],
                "symbol": parts[idx["symbol"]].strip(),
                "geneid": parts[idx["GeneID"]],
                "old_locus_tag": old_lt,
                "product": parts[idx["name"]],
            })
    return rows

pao1 = parse_feature_table("pao1_feature_table")
pa14 = parse_feature_table("pa14_feature_table")

# PAO1: index by locus_tag (PA####)
pao1_by_locus = {r["locus_tag"]: r for r in pao1}
# symbol multiplicity
pao1_sym_count = defaultdict(int)
for r in pao1:
    if r["symbol"]:
        pao1_sym_count[r["symbol"].lower()] += 1

# PA14: index symbol -> list of rows
pa14_by_symbol = defaultdict(list)
for r in pa14:
    if r["symbol"]:
        pa14_by_symbol[r["symbol"].lower()].append(r)

model = read_sbml_model("models/paeruginosa_MODEL1507180020.xml")
model_genes = sorted(g.id for g in model.genes)

cols = [
    "model_gene_id", "pao1_locus_tag", "pao1_gene_symbol", "pao1_refseq_geneid",
    "pa14_locus_tag", "pa14_refseq_locus", "pa14_refseq_geneid",
    "gene_name", "ortholog_evidence", "mapping_method", "mapping_confidence",
    "ambiguous", "n_pa14_candidates", "pa14_candidates",
    "mapping_source", "notes",
]

stats = defaultdict(int)
rows_out = []
for gid in model_genes:
    pao1_row = pao1_by_locus.get(gid)
    symbol = pao1_row["symbol"] if pao1_row else ""
    geneid = pao1_row["geneid"] if pao1_row else ""
    product = pao1_row["product"] if pao1_row else ""

    rec = {c: "" for c in cols}
    rec["model_gene_id"] = gid
    rec["pao1_locus_tag"] = gid
    rec["pao1_gene_symbol"] = symbol
    rec["pao1_refseq_geneid"] = geneid
    rec["gene_name"] = symbol
    rec["mapping_source"] = f"PAO1 {PAO1_ASM} + PA14 {PA14_ASM} RefSeq feature tables (NCBI, 2026-06-26)"

    if not pao1_row:
        rec["mapping_method"] = "pao1_locus_not_in_refseq"
        rec["mapping_confidence"] = "review"
        rec["notes"] = "Model PA#### not found in current PAO1 RefSeq (annotation drift / merged/obsolete locus)."
        stats["pao1_not_in_refseq"] += 1
        rows_out.append(rec); continue

    if not symbol:
        rec["pa14_locus_tag"] = "PENDING"
        rec["mapping_method"] = "no_symbol_no_orthology"
        rec["mapping_confidence"] = "unmapped"
        rec["ambiguous"] = "False"
        rec["n_pa14_candidates"] = "0"
        rec["notes"] = "PAO1 gene has no RefSeq symbol; PA14 ortholog needs validated orthology source (pseudomonas.com - B-NET)."
        stats["no_symbol"] += 1
        rows_out.append(rec); continue

    cand = pa14_by_symbol.get(symbol.lower(), [])
    rec["ortholog_evidence"] = f"RefSeq gene symbol '{symbol}'"
    rec["n_pa14_candidates"] = str(len(cand))
    pao1_sym_unique = pao1_sym_count[symbol.lower()] == 1

    if len(cand) == 0:
        rec["pa14_locus_tag"] = "PENDING"
        rec["mapping_method"] = "symbol_no_pa14_match"
        rec["mapping_confidence"] = "unmapped"
        rec["ambiguous"] = "False"
        rec["notes"] = "Symbol not found in PA14 RefSeq; needs validated orthology (B-NET)."
        stats["symbol_no_match"] += 1
    elif len(cand) == 1 and pao1_sym_unique:
        c = cand[0]
        rec["pa14_locus_tag"] = c["old_locus_tag"] or "PENDING"
        rec["pa14_refseq_locus"] = c["locus_tag"]
        rec["pa14_refseq_geneid"] = c["geneid"]
        rec["mapping_method"] = "gene_symbol_unique"
        rec["mapping_confidence"] = "medium"
        rec["ambiguous"] = "False"
        rec["notes"] = "1:1 RefSeq symbol match (annotation-based, not validated orthology)."
        if not c["old_locus_tag"]:
            rec["notes"] += " PA14 classic old_locus_tag missing; RefSeq locus given."
        stats["symbol_unique"] += 1
    else:
        # ambiguous: list ALL candidates, do not resolve
        cands = "; ".join(f"{c['old_locus_tag'] or c['locus_tag']}({c['symbol']})" for c in cand)
        rec["pa14_locus_tag"] = "AMBIGUOUS"
        rec["pa14_candidates"] = cands
        rec["mapping_method"] = "gene_symbol_ambiguous"
        rec["mapping_confidence"] = "low"
        rec["ambiguous"] = "True"
        why = []
        if not pao1_sym_unique:
            why.append(f"PAO1 symbol non-unique (x{pao1_sym_count[symbol.lower()]})")
        if len(cand) > 1:
            why.append(f"{len(cand)} PA14 candidates")
        rec["notes"] = "Ambiguous: " + ", ".join(why) + ". Candidates retained, NOT resolved."
        stats["symbol_ambiguous"] += 1

    rows_out.append(rec)

with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    w.writerows(rows_out)

# coverage report
total = len(model_genes)
lines = [
    "PAO1<->PA14<->model gene mapping coverage",
    "=========================================",
    f"date: 2026-06-26",
    f"sources: PAO1 {PAO1_ASM}, PA14 {PA14_ASM} (NCBI RefSeq feature tables)",
    f"model genes (iMO1056, PAO1): {total}",
    "",
    f"PAO1 identity (model_gene_id == PA#### locus): {total - stats['pao1_not_in_refseq']} (high confidence)",
    f"  not in current PAO1 RefSeq (drift/obsolete): {stats['pao1_not_in_refseq']}",
    "",
    "PA14 mapping via RefSeq gene-symbol (annotation, NOT validated orthology):",
    f"  1:1 unique symbol match (medium)   : {stats['symbol_unique']}",
    f"  ambiguous / one-to-many (low)      : {stats['symbol_ambiguous']}  [candidates retained]",
    f"  PAO1 has no symbol (unmapped)      : {stats['no_symbol']}",
    f"  symbol w/o PA14 match (unmapped)   : {stats['symbol_no_match']}",
    "",
    "BLOCKER B-NET: validated orthology (pseudomonas.com / OrthologueDB) and journal",
    "supplements (PNAS/Frontiers) are unreachable from this environment (403/timeout).",
    "PA14 'medium' rows are symbol-based and should be upgraded to validated orthology",
    "before any strain-mapped metric is reported.",
]
REPORT.write_text("\n".join(lines), encoding="utf-8")
print("\n".join(lines))
print(f"\nwrote {OUT} ({total} rows) and {REPORT}")

"""L-03 draft parser: raw literature supplements -> per-study DRAFT gene-level
evidence CSVs (+ one aggregate DRAFT). READ-ONLY on all raw inputs.

Scope (Phase 6 gate satisfied — thresholds sourced from Methods, see
THRESHOLD_METHOD_AUDIT.md):
    lee2015      (MPAO1 / PAO1 tags) : general + condition-specific essential
    turner2015   (PAO1 columns only) : general essential + fitness (sd01/06/07/10)
    belanger2022 (PAO1)              : general + conditional (media/abscess/skin)

Explicitly NOT parsed here:
    varadarajan2020  citation VERIFIED, but DS4 essentiality is a re-mapping of
                     Lee 2015 public Tn-seq data (double-count) -> mapping only.
    zhu2018          iPAO1 model reconstruction (not experimental labels).
    turner sd03/04/05/09  paired PAO1+PA14 sheets -> PAO1 column blocks still
                     need confirmation (L03-B3); deferred.

Never overwrites data/processed/literature_evidence.csv (canonical, study-level).
Outputs go under data/processed/literature/ + an aggregate DRAFT at
data/processed/. Every row carries strain, condition, phenotype class,
essentiality definition + threshold (sourced), and a source file/sheet/row/
column locator. Uncertain rows are flagged review_status=NEEDS_REVIEW.
"""
import csv
import re
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "literature"
OUT = ROOT / "data" / "processed" / "literature"
OUT.mkdir(parents=True, exist_ok=True)
AGG = ROOT / "data" / "processed" / "literature_evidence_gene_level_DRAFT.csv"

PA_RE = re.compile(r"^PA\d{4,5}$")

COLUMNS = [
    "study_id", "citation_key", "doi", "pmid", "strain", "strain_context",
    "phenotype_class", "condition", "medium",
    "original_gene_id", "original_gene_system",
    "mapped_pao1_gene_id", "mapping_method", "mapping_confidence", "mapping_note",
    "essentiality_call", "essentiality_definition", "threshold", "statistical_rule",
    "source_file", "source_sheet", "source_row", "source_column", "source_locator",
    "review_status", "notes",
]

# ---- sourced threshold/definition strings (see THRESHOLD_METHOD_AUDIT.md) ----
LEE_DEF = ("Tn-seq: gene with zero insertion reads/hits per gene = essential; "
           "remaining loci below a P=0.001 cutoff on a log2-normal fit of "
           "reads-per-gene and hits-per-gene = candidate essential per run "
           "(Lee 2015 SI, Sequence Data Analysis; Fig S3 x<6.3, P<0.001).")
LEE_GEN_THRESH = ("Consensus general essential: candidate-essential in >=2/3 LB "
                  "pools AND >=2/3 MOPS-pyruvate pools AND >=3/4 sputum-agar "
                  "pools (three primary media). Membership in sd01 sheet "
                  "'General essential genes' = author call.")
LEE_COND_THRESH = ("Per-medium consensus (Lee 2015 SI): LB >=2/3 pools, "
                   "MOPS-pyruvate >=2/3 pools, sputum-agar >=3/4 pools; "
                   "single-pool media (BHI, 0.1X LB, serum) = candidate-essential "
                   "in that 1 run. Column 'X sum (of N)' = # runs called "
                   "candidate-essential. NOTE pool-vs-assay mapping to the "
                   "'of 6/3/4' columns is interpretation -> NEEDS_REVIEW.")

TURNER_ESS_DEF = ("Tn-seq + Monte-Carlo pseudodata: 2000 simulations place "
                  "insertions/reads randomly under the null 'no gene essential'; "
                  "observed vs expected mutant abundance tested with DESeq "
                  "(negative binomial); genes clustered by fold-change vs "
                  "expected with R mclust into 2 modes.")
TURNER_ESS_THRESH = ("Deemed essential if BOTH: significantly lower mutant "
                     "abundance than expected (P<0.01, negative binomial) AND "
                     "clustered in the essential-like mode (P<0.01, MLE). "
                     "'Mode' column = mclust category; 'Essential?' = author "
                     "call (336/5606 PAO1 genes).")
TURNER_FIT_DEF = ("Tn-seq direct comparison of mutant abundance between two "
                  "conditions (fold change + P), DESeq negative binomial test.")
TURNER_FIT_THRESH = ("Significant fitness difference: fold change >=4 AND P<0.05 "
                     "(negative binomial test).")

BEL_DEF = ("Tn-seq (Himar1) analysed with two tools: TRANSIT Gumbel/Bayesian "
           "(P(essential) from reads per TA site; DeJesus 2015) and TraDIS "
           "(reads/gene, insertions per gene; Barquist 2016). Cell value = "
           "which tool(s) called the gene essential (Tradis / Transit / Both / "
           "NE=not essential).")
BEL_GEN_THRESH = ("Essential (T0 pool) if called by Gumbel(TRANSIT) OR TraDIS in "
                  ">=2/3 replicates. Single-tool call counts. Membership in "
                  "'T0_PAO1_essential_genes' = author call.")
BEL_COND_THRESH = ("Conditionally essential if called by Gumbel(TRANSIT) OR "
                   "TraDIS in >=4/5 experimental replicates. Single-tool call "
                   "counts; 'Both' = both tools.")

META = {
    "lee2015": dict(citation_key="lee2015", doi="10.1073/pnas.1422186112",
                    pmid="25848053", strain="MPAO1",
                    strain_context="PAO1-derived lab lineage; native PAO1 PAxxxx locus tags"),
    "turner2015": dict(citation_key="turner2015", doi="10.1073/pnas.1419677112",
                       pmid="25775563", strain="PAO1",
                       strain_context="PAO1 columns only (PA14 columns excluded here)"),
    "belanger2022": dict(citation_key="belanger2022", doi="10.3389/fmicb.2022.1055512",
                         pmid="36504765", strain="PAO1",
                         strain_context="PAO1 transposon pool"),
}


def base_row(study):
    m = META[study]
    r = {c: "" for c in COLUMNS}
    r.update(study_id=study, citation_key=m["citation_key"], doi=m["doi"],
             pmid=m["pmid"], strain=m["strain"], strain_context=m["strain_context"],
             original_gene_system="PAO1_locus_tag", mapping_method="identity(PAO1)",
             mapping_confidence="high",
             mapping_note="PAO1 PAxxxx locus tag = iMO1056 model gene id (identity join)")
    return r


def is_pa(v):
    return isinstance(v, str) and bool(PA_RE.match(v.strip()))


# --------------------------------------------------------------------------- #
def parse_lee():
    rows = []
    path = RAW / "lee2015" / "pnas.1422186112.sd01.xlsx"
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    fname = path.name

    # media columns: (header, condition label, medium, n_runs, essential_threshold)
    media = [
        ("LB sum (of 6)", "LB (rich)", "LB", 6, 4),               # >2/3 -> >=4 of 6
        ("Min sum (of 3)", "MOPS-pyruvate (minimal)", "MOPS-pyruvate", 3, 2),
        ("Sputum sum (of 4)", "CF sputum (agar)", "CF sputum agar", 4, 3),
        ("BHI (of 1)", "BHI (rich)", "BHI", 1, 1),
        ("0.1X LB (of 1)", "0.1X LB (dilute)", "0.1X LB", 1, 1),
        ("Serum (of 1)", "serum agar", "serum agar", 1, 1),
    ]

    def read_sheet(sheetname, which):
        ws = wb[sheetname]
        header = [("" if v is None else str(v).strip())
                  for v in next(ws.iter_rows(min_row=2, max_row=2, values_only=True))]
        idx = {h: i for i, h in enumerate(header)}
        gi = idx.get("PA number", 0)
        gni = idx.get("PA gene", 1)
        for xlrow, row in enumerate(ws.iter_rows(min_row=3, values_only=True), start=3):
            gid = row[gi] if gi < len(row) else None
            if not is_pa(gid):
                continue
            gid = gid.strip()
            gname = row[gni] if gni < len(row) and row[gni] else ""
            if which == "general":
                r = base_row("lee2015")
                r.update(phenotype_class="generally-essential",
                         condition="three primary media (LB + MOPS-pyruvate + CF sputum)",
                         medium="LB / MOPS-pyruvate / CF sputum agar",
                         original_gene_id=gid, mapped_pao1_gene_id=gid,
                         essentiality_call="essential",
                         essentiality_definition=LEE_DEF, threshold=LEE_GEN_THRESH,
                         statistical_rule="P<0.001 log2-normal fit; consensus across primary media",
                         source_file=fname, source_sheet=sheetname, source_row=str(xlrow),
                         source_column="PA number; General essential genes membership",
                         source_locator=f"{fname}!'{sheetname}'!A{xlrow} ({gid} {gname})",
                         review_status="READY",
                         notes="Author-provided general-essential set; gene symbol=%s" % gname)
                rows.append(r)
            else:  # condition-specific per medium
                for hcol, cond, med, n, thr in media:
                    ci = idx.get(hcol)
                    if ci is None or ci >= len(row):
                        continue
                    val = row[ci]
                    try:
                        s = int(val) if val is not None and str(val).strip() != "" else 0
                    except (TypeError, ValueError):
                        continue
                    if s < thr:
                        continue
                    r = base_row("lee2015")
                    r.update(phenotype_class="condition-specific-essential",
                             condition=cond, medium=med,
                             original_gene_id=gid, mapped_pao1_gene_id=gid,
                             essentiality_call="essential",
                             essentiality_definition=LEE_DEF, threshold=LEE_COND_THRESH,
                             statistical_rule=f"{hcol}={s}; threshold >= {thr} of {n} runs",
                             source_file=fname, source_sheet=sheetname, source_row=str(xlrow),
                             source_column=hcol,
                             source_locator=f"{fname}!'{sheetname}'!{gid} {hcol}={s}",
                             review_status="NEEDS_REVIEW",
                             notes=("Per-medium call; pool-vs-assay mapping to '%s' is "
                                    "interpretation (see audit). gene symbol=%s" % (hcol, gname)))
                    rows.append(r)

    read_sheet("General essential genes", "general")
    read_sheet("All essential genes", "condition")
    wb.close()
    return rows


# --------------------------------------------------------------------------- #
def parse_turner():
    rows = []
    d = RAW / "turner2015"

    # sd01: initial-library essentiality (block 1, cols 0..7)
    p = d / "pnas.1419677112.sd01.xlsx"
    wb = openpyxl.load_workbook(p, read_only=True, data_only=True)
    ws = wb["Sheet1"]
    for xlrow, row in enumerate(ws.iter_rows(min_row=4, values_only=True), start=4):
        gid = row[0] if row else None
        if not is_pa(gid):
            continue
        gid = gid.strip()
        gname = row[1] if len(row) > 1 and row[1] else ""
        ess = str(row[6]).strip() if len(row) > 6 and row[6] is not None else ""
        if ess.lower() != "essential":
            continue
        mode = str(row[4]).strip() if len(row) > 4 and row[4] is not None else ""
        log2fc = row[2] if len(row) > 2 else ""
        pfc = row[3] if len(row) > 3 else ""
        pmode = row[5] if len(row) > 5 else ""
        r = base_row("turner2015")
        r.update(phenotype_class="generally-essential",
                 condition="initial transposon library (rich laboratory medium)",
                 medium="complex laboratory medium (initial library)",
                 original_gene_id=gid, mapped_pao1_gene_id=gid,
                 essentiality_call="essential",
                 essentiality_definition=TURNER_ESS_DEF, threshold=TURNER_ESS_THRESH,
                 statistical_rule=f"Mode={mode}; Log2FC(Initial/Expected)={log2fc}; P(FC)={pfc}; P(Mode)={pmode}",
                 source_file=p.name, source_sheet="Sheet1", source_row=str(xlrow),
                 source_column="Essential? (initial block, col G)",
                 source_locator=f"{p.name}!Sheet1!G{xlrow} ({gid} {gname})",
                 review_status="READY",
                 notes=f"Table S1 initial-library essential set; gene symbol={gname}")
        rows.append(r)
    wb.close()

    # fitness tables: (file, gene_col, fc_col, p_col, header_row, data_row,
    #                  phenotype, condition, medium)
    fit = [
        ("pnas.1419677112.sd06.xlsx", 0, 2, 3, 2, 4, "reduced-fitness",
         "CF sputum vs MOPS-succinate", "CF sputum / MOPS-succinate"),
        ("pnas.1419677112.sd07.xlsx", 0, 5, 6, 2, 3, "reduced-fitness",
         "CF sputum vs MOPS-succinate (biosynthetic genes)", "CF sputum / MOPS-succinate"),
    ]
    for fn, gi, fci, pi, hrow, drow, pheno, cond, med in fit:
        p = d / fn
        wb = openpyxl.load_workbook(p, read_only=True, data_only=True)
        ws = wb["Sheet1"]
        for xlrow, row in enumerate(ws.iter_rows(min_row=drow, values_only=True), start=drow):
            gid = row[gi] if len(row) > gi else None
            if not is_pa(gid):
                continue
            gid = gid.strip()
            gname = row[1] if len(row) > 1 and row[1] else ""
            fc = row[fci] if len(row) > fci else None
            pv = row[pi] if len(row) > pi else None
            try:
                fcf = float(fc); pvf = float(pv)
            except (TypeError, ValueError):
                continue
            if not (abs(fcf) >= 4 and pvf < 0.05):
                continue
            r = base_row("turner2015")
            r.update(phenotype_class=pheno, condition=cond, medium=med,
                     original_gene_id=gid, mapped_pao1_gene_id=gid,
                     essentiality_call="reduced_fitness",
                     essentiality_definition=TURNER_FIT_DEF, threshold=TURNER_FIT_THRESH,
                     statistical_rule=f"FoldChange={fc}; P={pv} (|FC|>=4, P<0.05)",
                     source_file=fn, source_sheet="Sheet1", source_row=str(xlrow),
                     source_column="Fold Change Mutant Abundance; P",
                     source_locator=f"{fn}!Sheet1!row{xlrow} ({gid} {gname})",
                     review_status="READY",
                     notes=f"gene symbol={gname}")
            rows.append(r)
        wb.close()

    # sd10: block 1 = sputum vs succ; block 2 = murine chronic wound (host)
    p = d / "pnas.1419677112.sd10.xlsx"
    wb = openpyxl.load_workbook(p, read_only=True, data_only=True)
    ws = wb["Sheet1"]
    for xlrow, row in enumerate(ws.iter_rows(min_row=4, values_only=True), start=4):
        gid = row[0] if row else None
        if not is_pa(gid):
            continue
        gid = gid.strip()
        gname = row[1] if len(row) > 1 and row[1] else ""
        blocks = [
            (2, 3, "reduced-fitness", "CF sputum vs MOPS-succinate", "CF sputum / MOPS-succinate", "reduced_fitness"),
            (6, 7, "host-condition-fitness", "murine chronic wound vs MOPS-succinate", "murine chronic surgical wound", "host_fitness"),
        ]
        for fci, pi, pheno, cond, med, call in blocks:
            fc = row[fci] if len(row) > fci else None
            pv = row[pi] if len(row) > pi else None
            try:
                fcf = float(fc); pvf = float(pv)
            except (TypeError, ValueError):
                continue
            if not (abs(fcf) >= 4 and pvf < 0.05):
                continue
            r = base_row("turner2015")
            r.update(phenotype_class=pheno, condition=cond, medium=med,
                     original_gene_id=gid, mapped_pao1_gene_id=gid,
                     essentiality_call=call,
                     essentiality_definition=TURNER_FIT_DEF, threshold=TURNER_FIT_THRESH,
                     statistical_rule=f"FoldChange={fc}; P={pv} (|FC|>=4, P<0.05)",
                     source_file=p.name, source_sheet="Sheet1", source_row=str(xlrow),
                     source_column=f"Fold Change/P (cols {fci},{pi})",
                     source_locator=f"{p.name}!Sheet1!row{xlrow} ({gid} {gname})",
                     review_status="READY",
                     notes=f"Table S10; gene symbol={gname}")
            rows.append(r)
    wb.close()
    return rows


# --------------------------------------------------------------------------- #
def parse_belanger():
    rows = []
    d = RAW / "belanger2022"

    # DS1 T0 general essential (rich medium). 'Called Essential by' = author call.
    p = d / "Data_Sheet_1.XLSX"
    wb = openpyxl.load_workbook(p, read_only=True, data_only=True)
    ws = wb["T0_PAO1_essential_genes"]
    header = [("" if v is None else str(v).strip())
              for v in next(ws.iter_rows(min_row=2, max_row=2, values_only=True))]
    idx = {h: i for i, h in enumerate(header)}
    ci_call = idx.get("Called Essential by")
    for xlrow, row in enumerate(ws.iter_rows(min_row=3, values_only=True), start=3):
        gid = row[0] if row else None
        if not is_pa(gid):
            continue
        gid = gid.strip()
        gname = row[2] if len(row) > 2 and row[2] else ""
        call = ""
        if ci_call is not None and ci_call < len(row) and row[ci_call] is not None:
            call = str(row[ci_call]).strip()
        r = base_row("belanger2022")
        r.update(phenotype_class="generally-essential",
                 condition="rich medium, T0 pool (LB; baseline compared cf. MHB)",
                 medium="LB (pool generation) / MHB baseline",
                 original_gene_id=gid, mapped_pao1_gene_id=gid,
                 essentiality_call="essential",
                 essentiality_definition=BEL_DEF, threshold=BEL_GEN_THRESH,
                 statistical_rule=f"Called Essential by = {call}",
                 source_file=p.name, source_sheet="T0_PAO1_essential_genes",
                 source_row=str(xlrow), source_column="Locus Tag; Called Essential by",
                 source_locator=f"{p.name}!'T0_PAO1_essential_genes'!A{xlrow} ({gid} {gname})",
                 review_status="READY",
                 notes=("cross-study +/- columns NOT ingested (re-cited prior results); "
                        "baseline medium LB vs MHB ambiguous in paper; gene symbol=%s" % gname))
        rows.append(r)
    wb.close()

    # DS2 conditional essentiality: two-row header; condition column order varies
    # per sheet -> read row-2 sub-headers.
    p = d / "Data_Sheet_2.XLSX"
    wb = openpyxl.load_workbook(p, read_only=True, data_only=True)
    cond_meta = {  # normalized condition -> (label, medium, phenotype)
        "rpmi/serum": ("RPMI + human serum", "RPMI-1640 + serum", "condition-specific-essential"),
        "rpmi/ serum": ("RPMI + human serum", "RPMI-1640 + serum", "condition-specific-essential"),
        "rpmi": ("RPMI-1640", "RPMI-1640", "condition-specific-essential"),
        "abscess": ("murine abscess (in vivo)", "murine abscess", "host-condition-fitness"),
        "skin": ("human skin organoid (in vivo-like)", "human skin organoid", "host-condition-fitness"),
    }
    seen = set()  # (gid, normalized condition) dedupe across overlapping sheets
    for sheetname in ["Essential_media", "Essential_Abscess", "Essential_Skin", "Shared_Essential"]:
        ws = wb[sheetname]
        rowlist = list(ws.iter_rows(min_row=1, values_only=True))
        subhdr = rowlist[2]  # row index 2 = condition sub-headers
        cond_cols = {}
        for i, v in enumerate(subhdr):
            if v is None:
                continue
            key = str(v).strip().lower()
            if key in cond_meta:
                cond_cols[i] = key
        for xlrow0, row in enumerate(rowlist):
            if xlrow0 < 3:
                continue
            gid = row[0] if row else None
            if not is_pa(gid):
                continue
            gid = gid.strip()
            gname = row[1] if len(row) > 1 and row[1] else ""
            for ci, ckey in cond_cols.items():
                val = row[ci] if ci < len(row) else None
                call = str(val).strip() if val is not None else ""
                if call == "" or call.upper() == "NE":
                    continue  # not essential / blank
                if (gid, ckey) in seen:
                    continue
                seen.add((gid, ckey))
                label, med, pheno = cond_meta[ckey]
                r = base_row("belanger2022")
                r.update(phenotype_class=pheno, condition=label, medium=med,
                         original_gene_id=gid, mapped_pao1_gene_id=gid,
                         essentiality_call="essential",
                         essentiality_definition=BEL_DEF, threshold=BEL_COND_THRESH,
                         statistical_rule=f"tool call = {call} (Gumbel/TraDIS >=4/5 reps)",
                         source_file=p.name, source_sheet=sheetname, source_row=str(xlrow0 + 1),
                         source_column=f"'Essential in' -> {subhdr[ci]}",
                         source_locator=f"{p.name}!'{sheetname}'!row{xlrow0 + 1} ({gid} {gname}; {label}={call})",
                         review_status="READY",
                         notes=f"tool={call}; gene symbol={gname}")
                rows.append(r)
    wb.close()
    return rows


# --------------------------------------------------------------------------- #
def write_csv(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(rows)


def main():
    all_rows = []
    for study, fn in [("lee2015", parse_lee), ("turner2015", parse_turner),
                      ("belanger2022", parse_belanger)]:
        rows = fn()
        write_csv(OUT / f"{study}_parsed_gene_evidence.csv", rows)
        all_rows.extend(rows)
        by_pheno = {}
        for r in rows:
            by_pheno[r["phenotype_class"]] = by_pheno.get(r["phenotype_class"], 0) + 1
        print(f"{study}: {len(rows)} rows  {by_pheno}")
    write_csv(AGG, all_rows)
    print(f"AGGREGATE DRAFT: {len(all_rows)} rows -> {AGG.relative_to(ROOT)}")
    ready = sum(1 for r in all_rows if r["review_status"] == "READY")
    print(f"  READY={ready}  NEEDS_REVIEW={len(all_rows) - ready}")


if __name__ == "__main__":
    main()

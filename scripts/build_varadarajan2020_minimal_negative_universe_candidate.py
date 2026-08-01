"""Build Varadarajan2020 Minimal candidate labels + compare to Lee positives + model overlap."""
from pathlib import Path
import json
import re
import hashlib
import pandas as pd
import numpy as np
import sys
sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(r"i:\Bioinfo\karvarzi\ipynb")
base = ROOT / "data/raw/literature/varadarajan2020"
ds1 = base / "Supplementary Dataset 1 (MPAO1).xlsx"
ds4 = base / "Supplementary Dataset 4 (MPAO1).xlsx"
lee_ready = ROOT / "data/processed/literature/gene_level/literature_evidence_gene_level_READY_mops_pyruvate_lee2015.csv"
out_dir = ROOT / "project_management/audit/negative_universe_lee2015"
out_dir.mkdir(parents=True, exist_ok=True)
proc_dir = ROOT / "data/processed/literature/gene_level"
proc_dir.mkdir(parents=True, exist_ok=True)

df1 = pd.read_excel(ds1, sheet_name="MPAO1_CDS", header=1)
df4 = pd.read_excel(ds4, sheet_name="essentialGenes_MPAO1", header=0)

# --- mapping from best_hit protein ---
PA_STD = re.compile(r"^PA\d{4}$")

def parse_pa_hits(val):
    if pd.isna(val):
        return []
    s = str(val).strip()
    if not s or s.lower() == "nan":
        return []
    parts = [p.strip() for p in s.split(";")]
    return parts

rows = []
ds4_idx = df4.set_index("Locus", drop=False)
min_cols = ["Minimal-1", "Minimal-2", "Minimal-3"]

for _, r in df1.iterrows():
    locus = r["locus_tag"]
    hits = parse_pa_hits(r["best_hit protein"])
    std_hits = [h for h in hits if PA_STD.match(h)]
    nonstd_hits = [h for h in hits if h and not PA_STD.match(h)]
    unique_flag = (r["unique?"] == 1) if not pd.isna(r.get("unique?")) else False

    if locus in ds4_idx.index:
        d4 = ds4_idx.loc[locus]
        if isinstance(d4, pd.DataFrame):
            d4 = d4.iloc[0]
        m1 = 1 if d4["Minimal-1"] == 1 else 0
        m2 = 1 if d4["Minimal-2"] == 1 else 0
        m3 = 1 if d4["Minimal-3"] == 1 else 0
        # document blank encoding: blank -> not called essential (0), NOT missing
        in_ds4 = True
        ess_n = d4["Essential in x/16 samples"]
    else:
        m1 = m2 = m3 = 0
        in_ds4 = False
        ess_n = 0

    msum = int(m1 + m2 + m3)
    if msum >= 2:
        label = "POSITIVE"
    elif msum == 1:
        label = "AMBIGUOUS"
    else:
        label = "NEGATIVE"

    # mapping status
    if len(std_hits) == 1 and not nonstd_hits:
        map_status = "unique_std_PAO1"
        pao1 = std_hits[0]
    elif len(std_hits) > 1 and not nonstd_hits:
        map_status = "one_to_many_std_PAO1"
        pao1 = ";".join(std_hits)
    elif len(std_hits) >= 1 and nonstd_hits:
        map_status = "mixed_std_nonstd"
        pao1 = ";".join(hits)
    elif nonstd_hits and not std_hits:
        map_status = "nonstandard_only"
        pao1 = ";".join(nonstd_hits)
    elif unique_flag or (pd.isna(r["best_hit protein"])):
        map_status = "no_PAO1_homolog" if (unique_flag or pd.isna(r["best_hit protein"])) else "unmapped"
        pao1 = ""
    else:
        map_status = "unmapped"
        pao1 = ""

    rows.append({
        "mpao1_locus": locus,
        "pao1_locus": pao1,
        "best_hit_protein_raw": "" if pd.isna(r["best_hit protein"]) else str(r["best_hit protein"]),
        "minimal_1": m1,
        "minimal_2": m2,
        "minimal_3": m3,
        "minimal_sum": msum,
        "candidate_label": label,
        "in_ds4_essential_union": int(in_ds4),
        "essential_in_n_of_16_samples": ess_n if not pd.isna(ess_n) else 0,
        "mapping_status": map_status,
        "mpao1_unique": int(unique_flag),
        "evidence_source": "Varadarajan2020_Lee2015_Tnseq_remap",
        "source_dataset": "DS1_MPAO1_CDS+DS4_essentialGenes_MPAO1",
        "review_status": "CANDIDATE_FOR_HUMAN_REVIEW",
        "notes": "minimal blank/absent=not_called_essential_per_Lee_script_remap; not independent screen",
    })

cand = pd.DataFrame(rows)
print("candidate rows:", len(cand))
print(cand["candidate_label"].value_counts())
print(cand["minimal_sum"].value_counts().sort_index())
print(cand["mapping_status"].value_counts())

# --- model genes ---
# Prefer cobra if available
model_genes = set()
model_gene_ids = []
try:
    import cobra
    model = cobra.io.read_sbml_model(str(ROOT / "models/paeruginosa_MODEL1507180020.xml"))
    model_gene_ids = [g.id for g in model.genes]
    # clean PA ids from model gene ids
    for gid in model_gene_ids:
        m = re.search(r"(PA\d{4})", gid)
        if m:
            model_genes.add(m.group(1))
        else:
            # try raw
            if PA_STD.match(gid):
                model_genes.add(gid)
    print("model n_genes:", len(model.genes), "std PA extracted:", len(model_genes))
except Exception as e:
    print("cobra load failed:", e)
    # fallback: prediction CSV
    pred = ROOT / "results/essentiality/gene_essentiality_mops_pyruvate_lee2015.csv"
    if pred.exists():
        p = pd.read_csv(pred)
        col = "gene_id" if "gene_id" in p.columns else p.columns[0]
        for gid in p[col].astype(str):
            m = re.search(r"(PA\d{4})", gid)
            if m:
                model_genes.add(m.group(1))
        print("fallback model genes from predictions:", len(model_genes))

# Also load prediction file for evaluable set = genes in knockout results
pred_path = ROOT / "results/essentiality/gene_essentiality_mops_pyruvate_lee2015.csv"
pred_genes = set()
pred_ids_raw = {}
if pred_path.exists():
    p = pd.read_csv(pred_path)
    gcol = "gene_id" if "gene_id" in p.columns else p.columns[0]
    for gid in p[gcol].astype(str):
        m = re.search(r"(PA\d{4})", gid)
        if m:
            pa = m.group(1)
            pred_genes.add(pa)
            pred_ids_raw[pa] = gid
    print("prediction/evaluable genes:", len(pred_genes), "cols:", list(p.columns)[:8])

# Attach model fields — for multi-mapped, mark carefully
def model_fields(pa_str, map_status):
    if map_status != "unique_std_PAO1" or not pa_str:
        return {
            "in_imo1056": 0,
            "model_gene_id": "",
            "model_evaluable": 0,
            "exclusion_reason": "mapping_not_unique_std" if map_status != "unique_std_PAO1" else "no_pao1",
        }
    in_model = int(pa_str in model_genes)
    evaluable = int(pa_str in pred_genes) if pred_genes else in_model
    excl = ""
    if not in_model:
        excl = "absent_from_imo1056"
    elif not evaluable:
        excl = "in_model_but_not_in_knockout_results"
    # for primary validation universe we still want labels; exclusion is for metrics join
    return {
        "in_imo1056": in_model,
        "model_gene_id": pred_ids_raw.get(pa_str, pa_str if in_model else ""),
        "model_evaluable": evaluable,
        "exclusion_reason": excl,
    }

mf = cand.apply(lambda r: pd.Series(model_fields(r["pao1_locus"], r["mapping_status"])), axis=1)
cand = pd.concat([cand, mf], axis=1)

# For validation-eligible binary set: unique std map + in model (+ optionally evaluable)
val_mask = (cand["mapping_status"] == "unique_std_PAO1") & (cand["in_imo1056"] == 1)
val = cand[val_mask].copy()
# many-to-one PAO1: if two MPAO1 map to same PA, flag
pa_vc = val["pao1_locus"].value_counts()
multi_pa = set(pa_vc[pa_vc > 1].index)
cand.loc[cand["pao1_locus"].isin(multi_pa), "exclusion_reason"] = cand.loc[cand["pao1_locus"].isin(multi_pa), "exclusion_reason"].replace("", "many_MPAO1_to_one_PAO1")
# refresh val after exclusion flag - still keep in table but note
print("many_MPAO1_to_one_PAO1 count in val:", int(val["pao1_locus"].isin(multi_pa).sum()), "unique PA:", len(multi_pa))

# Collapse to unique PAO1 for comparison: for many-to-one take max minimal_sum / conflict check
def collapse_to_pao1(df):
    out = []
    for pa, g in df.groupby("pao1_locus"):
        labels = set(g["candidate_label"])
        msums = g["minimal_sum"].tolist()
        if len(g) == 1:
            row = g.iloc[0].to_dict()
            row["n_mpao1"] = 1
            row["label_conflict"] = 0
            out.append(row)
        else:
            # conflict if both POSITIVE and NEGATIVE present
            conflict = int(("POSITIVE" in labels) and ("NEGATIVE" in labels))
            # take max sum for consensus
            idx = g["minimal_sum"].idxmax()
            row = g.loc[idx].to_dict()
            row["n_mpao1"] = len(g)
            row["label_conflict"] = conflict
            if conflict:
                row["candidate_label"] = "AMBIGUOUS"
                row["exclusion_reason"] = "conflicting_MPAO1_labels_same_PAO1"
            out.append(row)
    return pd.DataFrame(out)

val_unique_map = cand[cand["mapping_status"] == "unique_std_PAO1"].copy()
pao1_collapsed = collapse_to_pao1(val_unique_map)
pao1_in_model = pao1_collapsed[pao1_collapsed["in_imo1056"] == 1].copy()

print("\n=== PAO1-collapsed unique_std ===")
print("n:", len(pao1_collapsed))
print(pao1_collapsed["candidate_label"].value_counts())
print("conflicts:", int(pao1_collapsed["label_conflict"].sum()))
print("\n=== intersect iMO1056 ===")
print("n:", len(pao1_in_model))
print(pao1_in_model["candidate_label"].value_counts())
print("minimal_sum:")
print(pao1_in_model["minimal_sum"].value_counts().sort_index())

# --- compare to Lee READY positives ---
lee = pd.read_csv(lee_ready)
# find locus column
print("\nLee READY columns:", list(lee.columns)[:20], "nrows", len(lee))
locus_col = None
for c in lee.columns:
    if c.lower() in ("locus_tag", "pa_number", "gene_id", "pao1_locus", "locus"):
        locus_col = c
        break
if locus_col is None:
    # try find PAxxxx column
    for c in lee.columns:
        s = lee[c].astype(str)
        if s.str.match(r"^PA\d{4}$").mean() > 0.8:
            locus_col = c
            break
print("Lee locus col:", locus_col)
lee_pos = set(lee[locus_col].astype(str).str.strip())
# also extract PA from messy
lee_pos_clean = set()
for x in lee_pos:
    m = re.search(r"(PA\d{4})", x)
    if m:
        lee_pos_clean.add(m.group(1))
    elif PA_STD.match(x):
        lee_pos_clean.add(x)
print("Lee positives cleaned:", len(lee_pos_clean))

var_pos = set(pao1_collapsed.loc[pao1_collapsed["candidate_label"] == "POSITIVE", "pao1_locus"])
# also POSITIVE among all unique_std regardless of model
inter = lee_pos_clean & var_pos
lee_only = lee_pos_clean - var_pos
var_only = var_pos - lee_pos_clean
print("\n=== Lee vs Varadarajan POSITIVE (unique_std PAO1, genome-wide collapsed) ===")
print("Lee:", len(lee_pos_clean), "Var:", len(var_pos), "intersect:", len(inter))
print("Lee-only:", len(lee_only), "Var-only:", len(var_only))
if lee_pos_clean:
    print("agreement % of Lee recovered:", round(100*len(inter)/len(lee_pos_clean), 2))
    print("Jaccard:", round(len(inter)/len(lee_pos_clean|var_pos), 4))

# among model-overlap positives
var_pos_model = set(pao1_in_model.loc[pao1_in_model["candidate_label"]=="POSITIVE","pao1_locus"])
lee_in_model = lee_pos_clean & model_genes
inter_m = lee_in_model & var_pos_model
print("\nModel-restricted: Lee∩model", len(lee_in_model), "Var pos∩model", len(var_pos_model), "intersect", len(inter_m))

# Save gene-level candidate (all MPAO1 CDS)
out_csv = proc_dir / "varadarajan2020_lee2015_minimal_gene_labels_CANDIDATE.csv"
# select columns
keep = [
    "mpao1_locus","pao1_locus","minimal_1","minimal_2","minimal_3","minimal_sum",
    "candidate_label","mapping_status","in_imo1056","model_evaluable","model_gene_id",
    "evidence_source","source_dataset","review_status","exclusion_reason",
    "in_ds4_essential_union","essential_in_n_of_16_samples","mpao1_unique",
    "best_hit_protein_raw","notes",
]
cand[keep].to_csv(out_csv, index=False)
print("wrote", out_csv)

# counts JSON
counts = {
    "master_cds_count_ds1": int(len(df1)),
    "ds4_essential_union_count": int(len(df4)),
    "valid_pao1_unique_std_mappings": int((cand["mapping_status"]=="unique_std_PAO1").sum()),
    "valid_pao1_std_including_multi": int(cand["mapping_status"].isin(["unique_std_PAO1","one_to_many_std_PAO1"]).sum()),
    "best_hit_protein_nonnull": int(df1["best_hit protein"].notna().sum()),
    "best_hit_std_PAxxxx_rows": int(sum(1 for v in df1["best_hit protein"] if not pd.isna(v) and any(PA_STD.match(x) for x in parse_pa_hits(v)))),
    "mpao1_unique_no_homolog": int((cand["mapping_status"]=="no_PAO1_homolog").sum()),
    "nonstandard_only": int((cand["mapping_status"]=="nonstandard_only").sum()),
    "one_to_many_std": int((cand["mapping_status"]=="one_to_many_std_PAO1").sum()),
    "minimal_sum_0": int((cand["minimal_sum"]==0).sum()),
    "minimal_sum_1": int((cand["minimal_sum"]==1).sum()),
    "minimal_sum_2": int((cand["minimal_sum"]==2).sum()),
    "minimal_sum_3": int((cand["minimal_sum"]==3).sum()),
    "positive_candidate_genome": int((cand["candidate_label"]=="POSITIVE").sum()),
    "negative_candidate_genome": int((cand["candidate_label"]=="NEGATIVE").sum()),
    "ambiguous_candidate_genome": int((cand["candidate_label"]=="AMBIGUOUS").sum()),
    "imo1056_model_genes_std_PA": int(len(model_genes)),
    "prediction_evaluable_genes": int(len(pred_genes)),
    "pao1_collapsed_unique_std": int(len(pao1_collapsed)),
    "pao1_collapsed_positive": int((pao1_collapsed["candidate_label"]=="POSITIVE").sum()),
    "pao1_collapsed_negative": int((pao1_collapsed["candidate_label"]=="NEGATIVE").sum()),
    "pao1_collapsed_ambiguous": int((pao1_collapsed["candidate_label"]=="AMBIGUOUS").sum()),
    "model_overlap_n": int(len(pao1_in_model)),
    "model_overlap_positive": int((pao1_in_model["candidate_label"]=="POSITIVE").sum()),
    "model_overlap_negative": int((pao1_in_model["candidate_label"]=="NEGATIVE").sum()),
    "model_overlap_ambiguous": int((pao1_in_model["candidate_label"]=="AMBIGUOUS").sum()),
    "lee_ready_positives": int(len(lee_pos_clean)),
    "lee_var_positive_intersect": int(len(inter)),
    "lee_only_positives": int(len(lee_only)),
    "var_only_positives": int(len(var_only)),
    "lee_recovery_pct": round(100*len(inter)/len(lee_pos_clean), 4) if lee_pos_clean else None,
    "jaccard_positives": round(len(inter)/len(lee_pos_clean|var_pos), 6) if (lee_pos_clean|var_pos) else None,
    "per_library_essential_in_ds4": {
        "Minimal-1": int((df4["Minimal-1"]==1).sum()),
        "Minimal-2": int((df4["Minimal-2"]==1).sum()),
        "Minimal-3": int((df4["Minimal-3"]==1).sum()),
    },
    "review_status": "CANDIDATE_FOR_HUMAN_REVIEW",
    "outcome_proposal": "A_CANDIDATE",
}
counts_path = out_dir / "NEGATIVE_UNIVERSE_COUNTS.json"
counts_path.write_text(json.dumps(counts, indent=2), encoding="utf-8")
# also CSV flat
pd.DataFrame([{"metric": k, "value": json.dumps(v) if isinstance(v, dict) else v} for k,v in counts.items()]).to_csv(out_dir / "NEGATIVE_UNIVERSE_COUNTS.csv", index=False)
print("wrote counts")

# save comparison lists
comp = {
    "intersect": sorted(inter),
    "lee_only": sorted(lee_only),
    "var_only": sorted(var_only),
}
(out_dir / "lee_vs_varadarajan_positive_comparison.json").write_text(json.dumps(comp, indent=2), encoding="utf-8")
print("done")
print(json.dumps(counts, indent=2))

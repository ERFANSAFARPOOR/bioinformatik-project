import json
from pathlib import Path

d = json.loads(
    Path("project_management/audit/v01_mops_pyruvate/v01_human_review_probe.json").read_text(
        encoding="utf-8"
    )
)

print("=== BIOMASS ===")
b = d["biomass"]
print("n_mets", b["metabolite_count"])
print("aa", b["amino_acid_constituents"])
print("trna", b["trna_or_charged_constituents"])
print("proxy sample", b["protein_rna_dna_lipid_proxy"][:40])

print("\n=== TRS summary ===")
print(d["trs_coupling_summary"])
nonzero = [r for r in d["trs_reactions_in_model"] if abs(r["wt_flux"]) > 1e-9]
print(
    "nonzero TRS",
    [(r["id"], r["name"], r["wt_flux"], r["blocked"], r["gpr"]) for r in nonzero],
)

print("\n=== SULFATE (nontrivial) ===")
for r in d["sulfate_related_reactions"]:
    interesting = (
        abs(r["flux"] or 0) > 1e-9
        or "SUL" in r["id"]
        or "so4" in r["id"].lower()
        or "sulfate" in (r["name"] or "").lower()
    )
    if interesting:
        print(
            r["id"],
            "|",
            r["name"],
            "| gpr=",
            r["gpr"],
            "| flux=",
            r["flux"],
            "| stoich=",
            r["stoichiometry"],
        )

print("\n=== PA1647 ===")
print(json.dumps(d["pa1647_presence"], indent=2))

print("\n=== Cluster A ===")
for g in d["cluster_A_sulfate"]:
    rx = g["associated_reactions"][0] if g["associated_reactions"] else {}
    print(
        g["gene"],
        g["gene_name"],
        "ratio",
        g["ko_wt_ratio"],
        "rx",
        rx.get("id"),
        "gpr",
        rx.get("gpr"),
        "wt_flux",
        rx.get("flux"),
        "blocked",
        rx.get("blocked"),
    )

print("\n=== Cluster B ===")
for g in d["cluster_B_translation"]:
    rx = g["associated_reactions"][0] if g["associated_reactions"] else {}
    print(
        g["gene"],
        g["gene_name"],
        rx.get("id"),
        rx.get("name"),
        "blocked",
        rx.get("blocked"),
        "wt",
        rx.get("flux"),
        "bm",
        g["biomass_direct_mets"],
        "ratio",
        g["ko_wt_ratio"],
        "min_sum",
        g["minimal_sum"],
    )

print("\n=== Cluster C ===")
for g in d["cluster_C_isoenzyme"]:
    print(g["gene"], g["gene_name"], g["ko_wt_ratio"])
    for r in g["associated_reactions"]:
        print(" ", r["id"], r["gpr"], "wt", r["flux"], "ko", r["flux_after_ko"], "stoich", r["stoichiometry"])
print("partners")
for k, v in d["cluster_C_partners"].items():
    print(k, v["gene_name"], [(r["id"], r["gpr"], r["name"]) for r in v["reactions"]])
print("rescue", json.dumps(d["cluster_C_isoenzyme_rescue"], indent=2))

print("\n=== Cluster D ===")
print(json.dumps(d["cluster_D_reaction_details"], indent=2))
for g in d["cluster_D_lipid"]:
    print(g["gene"], g["gene_name"], g["ko_wt_ratio"], g["experimental_label"])
    for r in g["associated_reactions"]:
        print(" ", r["id"], r["gpr"], "wt", r["flux"], "ko", r["flux_after_ko"], "bm", g["biomass_direct_mets"])

print("\n=== Cluster E ===")
for gid, tr in d["cluster_E_bypass_traces"].items():
    print("\n", gid, "ko_growth", tr.get("ko_growth"))
    print(" primary", tr.get("primary_reactions"))
    tops = [x for x in tr.get("top_flux_deltas", []) if not x["is_primary_associated"]][:15]
    for t in tops:
        print(
            " ",
            t["id"],
            "d=",
            round(t["delta"], 6),
            "wt",
            round(t["wt_flux"], 6),
            "ko",
            round(t["ko_flux"], 6),
            "gpr=",
            (t["gpr"] or "")[:70],
            "|",
            (t["name"] or "")[:60],
        )

print("\n=== EX_so4 / SULabc ===")
print(d["EX_so4_e"], "SULabc_ko", d["SULabc_reaction_ko_growth"])

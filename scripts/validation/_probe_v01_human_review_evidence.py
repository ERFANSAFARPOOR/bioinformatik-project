"""Read-only model-structure probe for V-01 human-review evidence pack.

Does NOT modify model, GPRs, medium, biomass, or threshold.
Does NOT rewrite V-01 metrics. Writes JSON probe output only.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import cobra
import pandas as pd
from cobra.flux_analysis import find_blocked_reactions, flux_variability_analysis

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.stdout.reconfigure(encoding="utf-8")

from src.load_model import load_model
from src.medium import apply_medium

MODEL_PATH = ROOT / "models" / "paeruginosa_MODEL1507180020.xml"
MEDIUM_ID = "mops_pyruvate_lee2015"
OBJECTIVE = "PA_Biomass6_DM"
OUT = ROOT / "project_management/audit/v01_mops_pyruvate/v01_human_review_probe.json"

FN_AUDIT = ROOT / "data/processed/validation/v01_mops_pyruvate_false_negative_audit.csv"
FP_AUDIT = ROOT / "data/processed/validation/v01_mops_pyruvate_false_positive_audit.csv"
PRED = ROOT / "data/processed/validation/v01_mops_pyruvate_gene_predictions.csv"
NAMES = ROOT / "data/processed/gene_mapping/gene_mapping.csv"

SULFATE_GENES = ["PA0280", "PA0281", "PA0282", "PA0283", "PA1493"]
ISO_GENES = ["PA1580", "PA1787", "PA0944"]
LIPID_GENES = ["PA0005", "PA3673"]
BYPASS_GENES = ["PA0024", "PA0607", "PA3107", "PA1049", "PA3480"]
# Extra partners for annotation context
PARTNERS = ["PA0795", "PA1562", "PA3751", "PA0836", "PA1647"]


def clean_gid(x) -> str:
    s = str(x)
    m = re.search(r"(PA\d{4})", s)
    return m.group(1) if m else s.strip()


def reaction_record(r: cobra.Reaction, flux=None) -> dict:
    return {
        "id": r.id,
        "name": r.name,
        "gpr": r.gene_reaction_rule,
        "subsystem": r.subsystem or "",
        "bounds": [r.lower_bound, r.upper_bound],
        "reversibility": r.reversibility,
        "stoichiometry": {m.id: coef for m, coef in r.metabolites.items()},
        "flux": None if flux is None else float(flux),
    }


def gene_reactions(model, gid: str):
    if gid not in model.genes:
        return []
    return list(model.genes.get_by_id(gid).reactions)


def main():
    model = load_model(str(MODEL_PATH))
    model.objective = OBJECTIVE
    apply_medium(model, MEDIUM_ID)

    pred = pd.read_csv(PRED)
    pred["gene_id"] = pred["pao1_locus"].map(clean_gid)
    pred_map = pred.set_index("gene_id").to_dict(orient="index")

    fn = pd.read_csv(FN_AUDIT)
    fn["gene_id"] = fn["gene"].map(clean_gid)
    fp = pd.read_csv(FP_AUDIT)
    fp["gene_id"] = fp["gene"].map(clean_gid)

    names = pd.read_csv(NAMES)
    name_map = {}
    for _, r in names.iterrows():
        gid = clean_gid(r.get("pao1_locus_tag", r.get("model_gene_id", "")))
        name_map[gid] = {
            "gene_name": str(r.get("gene_symbol", "") or ""),
            "pa14": str(r.get("pa14_locus_tag", "") or ""),
        }

    # WT solution
    sol_wt = model.optimize()
    wt_growth = float(sol_wt.objective_value)

    # Biomass composition analysis
    bm = model.reactions.get_by_id(OBJECTIVE)
    bm_mets = {m.id: coef for m, coef in bm.metabolites.items()}
    aa_like = [
        m
        for m in bm_mets
        if re.search(
            r"(ala|arg|asn|asp|cys|gln|glu|gly|his|ile|leu|lys|met|phe|pro|ser|thr|trp|tyr|val)__L",
            m,
            re.I,
        )
        or m
        in {
            "gly_c",
            "ala__L_c",
            "arg__L_c",
            "asn__L_c",
            "asp__L_c",
            "cys__L_c",
            "gln__L_c",
            "glu__L_c",
            "his__L_c",
            "ile__L_c",
            "leu__L_c",
            "lys__L_c",
            "met__L_c",
            "phe__L_c",
            "pro__L_c",
            "ser__L_c",
            "thr__L_c",
            "trp__L_c",
            "tyr__L_c",
            "val__L_c",
        }
    ]
    trna_like = [m for m in bm_mets if re.search(r"tRNA|trna|charged", m, re.I)]
    protein_proxy = [
        m for m in bm_mets if re.search(r"protein|prot_|biomass|RNA|DNA|lipid|LPS", m, re.I)
    ]

    # All TRS reactions in model
    trs_rxns = [
        r
        for r in model.reactions
        if re.search(r"tRNA synthetase|aminoacyl-tRNA|TRS$", r.name or "", re.I)
        or re.search(r"TRS$", r.id)
    ]

    # Sulfate-related reactions
    so4_rxns = []
    for r in model.reactions:
        mets = {m.id for m in r.metabolites}
        name = (r.name or "") + " " + r.id
        if any("so4" in m.lower() for m in mets) or re.search(
            r"sulfate|thiosulfate|SULabc|sulP|cysA|SO4", name, re.I
        ):
            so4_rxns.append(reaction_record(r, sol_wt.fluxes.get(r.id)))

    # Translation FN genes
    trna_fn = fn[fn["pathway_cluster"] == "translation_trna"]["gene_id"].tolist()

    # Blocked set under medium (can be slow; cache subset)
    print("Finding blocked reactions under MOPS-pyruvate...", flush=True)
    blocked = set(find_blocked_reactions(model))
    print(f"Blocked count: {len(blocked)}", flush=True)

    def audit_gene(gid: str, err_type: str) -> dict:
        prow = pred_map.get(gid, {})
        rxns = gene_reactions(model, gid)
        rxn_recs = []
        for r in rxns:
            rec = reaction_record(r, sol_wt.fluxes.get(r.id))
            rec["blocked"] = r.id in blocked
            # KO flux: knock out gene and optimize
            rxn_recs.append(rec)

        # After KO fluxes for associated reactions
        ko_fluxes = {}
        ko_growth = None
        if gid in model.genes:
            with model:
                model.genes.get_by_id(gid).knock_out()
                sol_ko = model.optimize()
                ko_growth = float(sol_ko.objective_value) if sol_ko.status == "optimal" else None
                for r in rxns:
                    ko_fluxes[r.id] = (
                        float(sol_ko.fluxes.get(r.id)) if sol_ko.status == "optimal" else None
                    )

        for rec in rxn_recs:
            rec["flux_after_ko"] = ko_fluxes.get(rec["id"])

        # Biomass relationship
        bm_link = any(
            any(m.id in bm_mets for m in model.reactions.get_by_id(r.id).metabolites)
            for r in rxns
        )
        # Shared metabolites with biomass (direct)
        direct_bm_mets = []
        for r in rxns:
            for m in r.metabolites:
                if m.id in bm_mets:
                    direct_bm_mets.append(m.id)

        return {
            "gene": gid,
            "gene_name": name_map.get(gid, {}).get("gene_name", ""),
            "fp_fn": err_type,
            "experimental_label": prow.get("experimental_label", ""),
            "experimental_class": prow.get("short_label", ""),
            "minimal_sum": prow.get("minimal_sum", ""),
            "ko_wt_ratio": prow.get("growth_ratio", ""),
            "wt_growth_pred": prow.get("wildtype_growth", wt_growth),
            "ko_growth_pred": prow.get("knockout_growth", ""),
            "ko_growth_recomputed": ko_growth,
            "associated_reactions": rxn_recs,
            "biomass_direct_mets": sorted(set(direct_bm_mets)),
            "biomass_direct_link": bool(direct_bm_mets),
            "in_model": gid in model.genes,
        }

    out = {
        "meta": {
            "medium": MEDIUM_ID,
            "objective": OBJECTIVE,
            "wt_growth": wt_growth,
            "blocked_reaction_count": len(blocked),
            "model_path": str(MODEL_PATH),
        },
        "biomass": {
            "reaction_id": OBJECTIVE,
            "metabolite_count": len(bm_mets),
            "amino_acid_constituents": sorted(aa_like),
            "trna_or_charged_constituents": sorted(trna_like),
            "protein_rna_dna_lipid_proxy": sorted(protein_proxy)[:80],
            "all_metabolites": sorted(bm_mets.keys()),
            "sample_stoichiometry_negatives": {
                k: bm_mets[k] for k in sorted(bm_mets) if bm_mets[k] < 0
            },
        },
        "trs_reactions_in_model": [
            {
                "id": r.id,
                "name": r.name,
                "gpr": r.gene_reaction_rule,
                "blocked": r.id in blocked,
                "wt_flux": float(sol_wt.fluxes.get(r.id, 0.0)),
                "stoichiometry": {m.id: coef for m, coef in r.metabolites.items()},
            }
            for r in trs_rxns
        ],
        "sulfate_related_reactions": so4_rxns,
        "cluster_A_sulfate": [audit_gene(g, "FP") for g in SULFATE_GENES],
        "cluster_B_translation": [audit_gene(g, "FN") for g in trna_fn],
        "cluster_C_isoenzyme": [audit_gene(g, "FN") for g in ISO_GENES],
        "cluster_C_partners": {
            g: {
                "in_model": g in model.genes,
                "gene_name": name_map.get(g, {}).get("gene_name", ""),
                "reactions": [
                    reaction_record(r, sol_wt.fluxes.get(r.id))
                    for r in gene_reactions(model, g)
                ],
            }
            for g in ["PA0795", "PA1562", "PA3751", "PA0836"]
        },
        "cluster_D_lipid": [audit_gene(g, "FP") for g in LIPID_GENES],
        "cluster_E_bypass": [audit_gene(g, "FN") for g in BYPASS_GENES],
        "pa1647_presence": {
            "in_model_genes": "PA1647" in model.genes,
            "reactions": [
                reaction_record(r, sol_wt.fluxes.get(r.id))
                for r in gene_reactions(model, "PA1647")
            ]
            if "PA1647" in model.genes
            else [],
            "name_hits": [
                {"id": r.id, "name": r.name, "gpr": r.gene_reaction_rule}
                for r in model.reactions
                if "1647" in r.gene_reaction_rule or re.search(r"sulP|SULt|sulfate transport", (r.name or "") + r.id, re.I)
            ],
        },
    }

    # Bypass flux tracing for representative genes: FVA / diff WT vs KO on network
    print("Tracing bypass fluxes for Cluster E...", flush=True)
    bypass_traces = {}
    for gid in BYPASS_GENES:
        if gid not in model.genes:
            continue
        rxns = gene_reactions(model, gid)
        primary_ids = [r.id for r in rxns]
        with model:
            model.genes.get_by_id(gid).knock_out()
            sol_ko = model.optimize()
        if sol_ko.status != "optimal":
            bypass_traces[gid] = {"status": sol_ko.status}
            continue
        # reactions with large flux change
        deltas = []
        for rid in sol_wt.fluxes.index:
            f0 = float(sol_wt.fluxes[rid])
            f1 = float(sol_ko.fluxes[rid])
            d = f1 - f0
            if abs(d) > 1e-6:
                r = model.reactions.get_by_id(rid)
                deltas.append(
                    {
                        "id": rid,
                        "name": r.name,
                        "gpr": r.gene_reaction_rule,
                        "wt_flux": f0,
                        "ko_flux": f1,
                        "delta": d,
                        "is_primary_associated": rid in primary_ids,
                    }
                )
        deltas.sort(key=lambda x: -abs(x["delta"]))
        # Also check if primary reaction flux goes to ~0
        primary_status = []
        for r in rxns:
            primary_status.append(
                {
                    "id": r.id,
                    "wt_flux": float(sol_wt.fluxes.get(r.id, 0.0)),
                    "ko_flux": float(sol_ko.fluxes.get(r.id, 0.0)),
                    "blocked": r.id in blocked,
                }
            )
        bypass_traces[gid] = {
            "ko_growth": float(sol_ko.objective_value),
            "primary_reactions": primary_status,
            "top_flux_deltas": deltas[:40],
        }
    out["cluster_E_bypass_traces"] = bypass_traces

    # For isoenzymes: flux through CS/ACONT/GARFTi after KO
    print("Checking isoenzyme partner rescue fluxes...", flush=True)
    iso_rescue = {}
    for gid, partner_hint in [
        ("PA1580", "PA0795"),
        ("PA1787", "PA1562"),
        ("PA0944", "PA3751"),
    ]:
        rxns = gene_reactions(model, gid)
        with model:
            model.genes.get_by_id(gid).knock_out()
            sol_ko = model.optimize()
        iso_rescue[gid] = {
            "partner_hint": partner_hint,
            "ko_growth": float(sol_ko.objective_value) if sol_ko.status == "optimal" else None,
            "reactions": [
                {
                    "id": r.id,
                    "gpr": r.gene_reaction_rule,
                    "wt_flux": float(sol_wt.fluxes.get(r.id, 0.0)),
                    "ko_flux": float(sol_ko.fluxes.get(r.id, 0.0))
                    if sol_ko.status == "optimal"
                    else None,
                }
                for r in rxns
            ],
        }
    out["cluster_C_isoenzyme_rescue"] = iso_rescue

    # Lipid reaction deep dive
    lipid_rxn_ids = set()
    for g in LIPID_GENES:
        for r in gene_reactions(model, g):
            lipid_rxn_ids.add(r.id)
    out["cluster_D_reaction_details"] = {
        rid: reaction_record(model.reactions.get_by_id(rid), sol_wt.fluxes.get(rid))
        for rid in sorted(lipid_rxn_ids)
    }

    # Check EX_so4 and SULabc necessity
    with model:
        if "SULabc" in model.reactions:
            model.reactions.SULabc.knock_out()
            sol = model.optimize()
            sulabc_ko = float(sol.objective_value) if sol.status == "optimal" else None
        else:
            sulabc_ko = "SULabc_not_found"
    out["SULabc_reaction_ko_growth"] = sulabc_ko
    out["EX_so4_e"] = {
        "bounds": list(model.reactions.EX_so4_e.bounds)
        if "EX_so4_e" in model.reactions
        else None,
        "wt_flux": float(sol_wt.fluxes.get("EX_so4_e", 0.0))
        if "EX_so4_e" in model.reactions
        else None,
    }

    # Count how many TRS are blocked and whether any carry flux
    trs_summary = {
        "n_trs": len(trs_rxns),
        "n_blocked": sum(1 for r in trs_rxns if r.id in blocked),
        "n_with_nonzero_wt_flux": sum(
            1 for r in trs_rxns if abs(float(sol_wt.fluxes.get(r.id, 0.0))) > 1e-9
        ),
        "any_trna_in_biomass": len(trna_like) > 0,
        "n_aa_in_biomass": len(aa_like),
    }
    out["trs_coupling_summary"] = trs_summary

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"Wrote {OUT}", flush=True)
    print(json.dumps({"trs_coupling_summary": trs_summary, "SULabc_ko": sulabc_ko, "wt": wt_growth}, indent=2))


if __name__ == "__main__":
    main()

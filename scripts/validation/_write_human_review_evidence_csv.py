"""Build v01_mops_pyruvate_human_review_evidence.csv from probe + audit CSVs."""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
PROBE = ROOT / "project_management/audit/v01_mops_pyruvate/v01_human_review_probe.json"
FN = ROOT / "data/processed/validation/v01_mops_pyruvate_false_negative_audit.csv"
FP = ROOT / "data/processed/validation/v01_mops_pyruvate_false_positive_audit.csv"
OUT = ROOT / "data/processed/validation/v01_mops_pyruvate_human_review_evidence.csv"

# Manual evidence overlays (source-backed recommendations for human review)
OVERLAY = {
    # Cluster A
    "PA0280": dict(
        cluster="A_sulfate_transport",
        evidence_class="MODEL_ERROR_LIKELY",
        isoenzyme_call="",
        bypass_type="MISSING_ALT_UPTAKE_CANDIDATE",
        diagnosis="Sole SULabc uptake; CysA subunit of SulT ABC. PA1647 absent from model.",
        confidence="medium",
        sources="KEGG pae:PA0280; Tralau2007; Sirko1995; Lee2015 medium SO4",
        model_observation="SULabc GPR AND of 5 genes; KO lethal; WT flux~0.086",
        source_fact="cysA sulfate ABC ATPase; medium supplies sulfate",
        inference="Model forces one transporter under sulfate repletion",
        hypothesis="PA1647 or binder OR-logic may rescue in vivo",
    ),
    "PA0281": dict(
        cluster="A_sulfate_transport",
        evidence_class="MODEL_ERROR_LIKELY",
        isoenzyme_call="",
        bypass_type="MISSING_ALT_UPTAKE_CANDIDATE",
        diagnosis="CysW permease of sole SULabc; same cluster mechanism as PA0280.",
        confidence="medium",
        sources="KEGG/repo mapping; Tralau2007; Lee2015 medium",
        model_observation="SULabc AND-GPR; KO lethal",
        source_fact="cysW annotated sulfate permease",
        inference="Same forced-transporter FP cluster",
        hypothesis="Alternate SulP uptake unmodeled",
    ),
    "PA0282": dict(
        cluster="A_sulfate_transport",
        evidence_class="MODEL_ERROR_LIKELY",
        isoenzyme_call="",
        bypass_type="MISSING_ALT_UPTAKE_CANDIDATE",
        diagnosis="CysT permease of sole SULabc.",
        confidence="medium",
        sources="KEGG/repo mapping; Tralau2007",
        model_observation="SULabc AND-GPR; KO lethal",
        source_fact="cysT annotated sulfate permease",
        inference="Same forced-transporter FP cluster",
        hypothesis="Alternate SulP uptake unmodeled",
    ),
    "PA0283": dict(
        cluster="A_sulfate_transport",
        evidence_class="MODEL_ERROR_LIKELY",
        isoenzyme_call="",
        bypass_type="OVERRESTRICTIVE_BINDER_AND",
        diagnosis="Sbp binder AND-required with CysP; E. coli binders are redundant.",
        confidence="medium",
        sources="KEGG pae:PA0283; Sirko1995 J Bacteriol",
        model_observation="PA0283 AND PA1493 both required for SULabc",
        source_fact="E. coli single sbp or cysP mutants still use sulfate",
        inference="AND of both binders likely over-restrictive",
        hypothesis="PAO1 binder redundancy needs direct confirmation",
    ),
    "PA1493": dict(
        cluster="A_sulfate_transport",
        evidence_class="MODEL_ERROR_LIKELY",
        isoenzyme_call="",
        bypass_type="OVERRESTRICTIVE_BINDER_AND",
        diagnosis="CysP binder AND-required with Sbp.",
        confidence="medium",
        sources="KEGG pae:PA1493; Sirko1995",
        model_observation="PA1493 AND PA0283 required",
        source_fact="CysP periplasmic sulfate/thiosulfate binder",
        inference="Binder AND may create false essentiality",
        hypothesis="OR of binders more biologically accurate",
    ),
    # Cluster C
    "PA1580": dict(
        cluster="C_isoenzyme",
        evidence_class="BIOLOGICAL_CONTEXT_NOT_MODELED",
        isoenzyme_call="POSSIBLE_OVERPERMISSIVE_GPR; CONTEXT_NOT_CAPTURED_BY_GEM",
        bypass_type="OR_PARTNER_PRPC",
        diagnosis="gltA OR prpC; PrpC is 2-MCS with underground CS activity after rewiring.",
        confidence="high",
        sources="KEGG; Dolan2022 mBio e02541-22",
        model_observation="CS flux unchanged after PA1580 KO via PA0795",
        source_fact="prpC EC 2.3.3.5; rescue often needs prpR loss",
        inference="Unconditional OR overstates constitutive redundancy",
        hypothesis="Conditioned GPR or regulatory constraint needed",
    ),
    "PA1787": dict(
        cluster="C_isoenzyme",
        evidence_class="BIOLOGICAL_CONTEXT_NOT_MODELED",
        isoenzyme_call="VALID_BIOLOGICAL_ISOENZYME; CONTEXT_NOT_CAPTURED_BY_GEM",
        bypass_type="OR_PARTNER_ACNA",
        diagnosis="acnB OR acnA; both true aconitases; condition-specific use not modeled.",
        confidence="high",
        sources="KEGG pae:PA1787/PA1562; iron/PrrF literature",
        model_observation="ACONT survives PA1787 KO",
        source_fact="Both EC 4.2.1.3 aconitate hydratases",
        inference="OR enzymatically valid; expression context missing",
        hypothesis="AcnB dominant under MOPS-pyruvate",
    ),
    "PA0944": dict(
        cluster="C_isoenzyme",
        evidence_class="MODEL_ERROR_LIKELY",
        isoenzyme_call="VALID_BIOLOGICAL_ISOENZYME(purT); POSSIBLE_OVERPERMISSIVE_GPR(ackA)",
        bypass_type="OR_PURT_AND_ACKA",
        diagnosis="purN OR (purT OR ackA); AckA is acetate kinase — not GARFT.",
        confidence="high",
        sources="KEGG; Nygaard1993; repo gene_mapping ackA",
        model_observation="GARFTi flux retained after PA0944 KO",
        source_fact="purT valid alt; ackA is EC acetate kinase",
        inference="PA0836 in GARFTi/GART is annotation/GPR error",
        hypothesis="PurT alone may still over-rescue depending on formate",
    ),
    # Cluster D
    "PA0005": dict(
        cluster="D_lipid_GPR",
        evidence_class="MODEL_ERROR_LIKELY",
        isoenzyme_call="",
        bypass_type="MISSING_LPAAT_ISOZYME",
        diagnosis="lptA AND plsB on lumped 12DAG3Ps_PA; lptA non-essential in vivo.",
        confidence="high",
        sources="Baysse2005 Microbiology; Cronan2023; KEGG",
        model_observation="12DAG3Ps_PA GPR PA0005 and PA3673; KO lethal",
        source_fact="Delta-lptA viable; other LPAAT activity exists",
        inference="Missing LPAAT alternative(s) in model",
        hypothesis="Biomass phospholipid demand amplifies FP",
    ),
    "PA3673": dict(
        cluster="D_lipid_GPR",
        evidence_class="MODEL_ERROR_LIKELY",
        isoenzyme_call="",
        bypass_type="LUMPED_GPAT_LPAAT_AND",
        diagnosis="plsB AND-lumped with lptA; sequential enzymes not a complex.",
        confidence="medium",
        sources="KEGG pae:PA3673; Baysse2005 context",
        model_observation="Same 12DAG3Ps_PA AND; KO lethal",
        source_fact="plsB = GPAT EC 2.3.1.15",
        inference="AND encodes two-step lump; false if either step redundant",
        hypothesis="plsB may have alts or Tn-seq non-essential call stands",
    ),
    # Cluster E
    "PA0024": dict(
        cluster="E_alt_pathway",
        evidence_class="BIOLOGICAL_CONTEXT_NOT_MODELED",
        isoenzyme_call="",
        bypass_type="BIOLOGICAL_HEMN",
        diagnosis="hemF KO uses CPPPGOAN (hemN PA1546); biological O2-independent route.",
        confidence="high",
        sources="Rompf1998 Mol Microbiol; model CPPPGOAN",
        model_observation="After KO CPPPGOAN flux replaces CPPPGO; double KO lethal",
        source_fact="HemF/HemN documented alternatives in PAO1",
        inference="Bypass biological but O2/regulation not modeled",
        hypothesis="Why Lee essential under aerobic MOPS-pyruvate needs review",
    ),
    "PA0607": dict(
        cluster="E_alt_pathway",
        evidence_class="MODEL_ERROR_LIKELY",
        isoenzyme_call="",
        bypass_type="COMPUTATIONAL_PGDH",
        diagnosis="RPE KO opens PGDH(PA0743) oxidative PPP; PA0743 is HibDH-like not Gnd.",
        confidence="high",
        sources="repo with_gene_names PA0743; Nikel/Dolan EDEMP; probe fluxes",
        model_observation="PGDH/G6PDHy/PGL rise after RPE KO; growth retained",
        source_fact="PA0743 annotated probable 3-hydroxyisobutyrate DH",
        inference="Computational bypass via likely misannotation",
        hypothesis="Correcting PGDH would restore RPE essentiality in model",
    ),
    "PA3107": dict(
        cluster="E_alt_pathway",
        evidence_class="BIOLOGICAL_CONTEXT_NOT_MODELED",
        isoenzyme_call="",
        bypass_type="BIOLOGICAL_TRANSSULFURATION",
        diagnosis="metZ KO uses PA0400 SHSL5/CYSTLr then METS; parallel Met path.",
        confidence="high",
        sources="Foglino1995 Microbiology; KEGG metZ",
        model_observation="SHSL2 off; SHSL5+CYSTLr+METS carry Met synthesis",
        source_fact="Direct sulfhydrylation + transsulfuration both reported in PA",
        inference="Bypass biologically documented",
        hypothesis="Incomplete in vivo compensation vs Lee essential call",
    ),
    "PA1049": dict(
        cluster="E_alt_pathway",
        evidence_class="UNRESOLVED",
        isoenzyme_call="",
        bypass_type="INACTIVE_PRIMARY",
        diagnosis="B6 oxidase reactions have zero WT flux; not an active-path bypass.",
        confidence="low",
        sources="probe FVA/flux; FN audit",
        model_observation="PDX5PO/PYAM5PO/PYDXNO/PYDXO WT flux 0",
        source_fact="PA1049 linked to B6 oxidase reactions in model",
        inference="Demand may be satisfied elsewhere or unused",
        hypothesis="Biomass B6 formulation / alternate supply",
    ),
    "PA3480": dict(
        cluster="E_alt_pathway",
        evidence_class="UNRESOLVED",
        isoenzyme_call="",
        bypass_type="INACTIVE_PRIMARY",
        diagnosis="DCTPD WT flux 0; inactive-edge FN.",
        confidence="low",
        sources="probe; FN audit",
        model_observation="DCTPD flux 0 before and after KO",
        source_fact="dCTP deaminase annotation in model name",
        inference="Not a demonstrated active bypass",
        hypothesis="Nucleotide demand topology",
    ),
}


def trna_overlay(gene: str) -> dict:
    return dict(
        cluster="B_translation_trna",
        evidence_class="MODEL_SCOPE_LIMITATION_LIKELY",
        isoenzyme_call="",
        bypass_type="NO_BIOMASS_COUPLING",
        diagnosis="Aminoacyl-tRNA synthetase blocked/unconnected; biomass uses free AAs.",
        confidence="high",
        sources="Oberhardt2008 JB PMC2293256; probe biomass+blocked TRS",
        model_observation="No tRNA in PA_Biomass6_DM; 17/18 TRS blocked; KO/WT~1",
        source_fact="Oberhardt: tRNA synthetases are gaps not in model function",
        inference="Shared scope limitation across ~18 FN genes",
        hypothesis="None — design limitation, not 18 independent errors",
    )


def main():
    probe = json.loads(PROBE.read_text(encoding="utf-8"))
    fn = pd.read_csv(FN)
    fp = pd.read_csv(FP)

    # Build gene -> probe record
    probe_genes = {}
    for key in [
        "cluster_A_sulfate",
        "cluster_B_translation",
        "cluster_C_isoenzyme",
        "cluster_D_lipid",
        "cluster_E_bypass",
    ]:
        for rec in probe[key]:
            probe_genes[rec["gene"]] = rec

    trna_genes = set(fn.loc[fn["pathway_cluster"] == "translation_trna", "gene"])

    rows = []
    targets = sorted(
        set(OVERLAY)
        | trna_genes
        | set(probe_genes)
    )

    audit = pd.concat([fn, fp], ignore_index=True)
    audit_map = {r.gene: r for r in audit.itertuples()}

    for gene in targets:
        a = audit_map.get(gene)
        p = probe_genes.get(gene, {})
        ov = OVERLAY.get(gene)
        if ov is None and gene in trna_genes:
            ov = trna_overlay(gene)
        if ov is None:
            continue

        rxns = p.get("associated_reactions") or []
        rx_ids = ";".join(r["id"] for r in rxns) if rxns else (
            getattr(a, "associated_reactions", "") if a is not None else ""
        )
        gprs = ";".join(f"{r['id']}:{r['gpr']}" for r in rxns) if rxns else (
            getattr(a, "GPR_rules", "") if a is not None else ""
        )
        wt_flux = ";".join(
            f"{r['id']}={r.get('flux')}" for r in rxns
        ) if rxns else ""
        ko_flux = ";".join(
            f"{r['id']}={r.get('flux_after_ko')}" for r in rxns
        ) if rxns else ""
        blocked = ";".join(
            f"{r['id']}={r.get('blocked')}" for r in rxns
        ) if rxns else (
            str(getattr(a, "blocked_reaction_flag", "")) if a is not None else ""
        )
        stoich = " || ".join(
            f"{r['id']}:{r.get('stoichiometry')}" for r in rxns
        ) if rxns else ""

        rows.append(
            {
                "gene": gene,
                "gene_name": p.get("gene_name", ""),
                "cluster": ov["cluster"],
                "FP_FN": getattr(a, "error_type", p.get("fp_fn", "")),
                "experimental_label": getattr(a, "experimental_label", p.get("experimental_label", "")),
                "minimal_sum": getattr(a, "minimal_sum", p.get("minimal_sum", "")),
                "KO_WT_ratio": getattr(a, "KO_WT_ratio", p.get("ko_wt_ratio", "")),
                "associated_reactions": rx_ids,
                "exact_GPR": gprs,
                "reaction_flux_WT": wt_flux,
                "reaction_flux_after_KO": ko_flux,
                "blocked_status": blocked,
                "model_subsystem": getattr(a, "subsystem_pathway", ""),
                "reaction_stoichiometry": stoich,
                "biomass_relationship": (
                    "direct_mets=" + ",".join(p.get("biomass_direct_mets") or [])
                    if p
                    else getattr(a, "biomass_direct_link", "")
                ),
                "alternative_route": ov["bypass_type"],
                "isoenzyme_classification": ov["isoenzyme_call"],
                "evidence_backed_diagnosis": ov["diagnosis"],
                "evidence_class": ov["evidence_class"],
                "confidence": ov["confidence"],
                "MODEL_OBSERVATION": ov["model_observation"],
                "SOURCE_FACT": ov["source_fact"],
                "INFERENCE": ov["inference"],
                "HYPOTHESIS": ov["hypothesis"],
                "sources": ov["sources"],
                "human_review_required": "YES",
                "prior_diagnostic_category": getattr(a, "diagnostic_category", ""),
            }
        )

    out = pd.DataFrame(rows).sort_values(["cluster", "gene"])
    OUT.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUT, index=False)
    print(f"Wrote {OUT} rows={len(out)}")
    print(out.groupby("cluster").size())
    print(out.groupby("evidence_class").size())


if __name__ == "__main__":
    main()

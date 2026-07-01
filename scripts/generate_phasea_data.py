"""Generate evidence-based Phase A data artifacts from the model (read-only).

Outputs:
  - data/processed/gene_mapping.csv      (model gene IDs -> PAO1 locus tags; identity mapping)
  - data/processed/literature_evidence.csv (schema + study-level provenance rows; gene-level PENDING)
  - papers/manifest.csv                  (PDF provenance manifest)
  - model_audit_snapshot.json            (clean machine-readable audit summary)

NO experimental values are invented. Gene-level phenotype fields are left as
PENDING_EXTRACTION and tracked by blockers.
"""
import csv
import json
from pathlib import Path

import cobra
from cobra.io import read_sbml_model

ROOT = Path(".")
(ROOT / "data" / "processed").mkdir(parents=True, exist_ok=True)
(ROOT / "papers").mkdir(parents=True, exist_ok=True)

model = read_sbml_model("models/paeruginosa_MODEL1507180020.xml")

# ---------------------------------------------------------------------------
# 1) gene_mapping.csv  (evidence-based identity mapping for PAO1 locus tags)
# ---------------------------------------------------------------------------
gm_cols = [
    "model_gene_id", "pao1_locus_tag", "pa14_locus_tag", "gene_name",
    "ortholog_group", "uniprot_id", "mapping_method", "mapping_confidence",
    "mapping_source", "notes",
]
with open("data/processed/gene_mapping.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(gm_cols)
    for g in sorted(model.genes, key=lambda x: x.id):
        gid = g.id
        is_pao1 = gid.startswith("PA") and gid[2:].isdigit()
        w.writerow([
            gid,
            gid if is_pao1 else "",                       # pao1_locus_tag (identity)
            "",                                            # pa14_locus_tag (PENDING - needs orthology)
            g.name if g.name and g.name != gid else "",   # gene_name (PENDING for most)
            "",                                            # ortholog_group (PENDING)
            "",                                            # uniprot_id (PENDING)
            "identity" if is_pao1 else "unresolved",
            "high" if is_pao1 else "low",
            "iMO1056 gene IDs are PAO1 locus tags (Oberhardt et al. 2008, J Bacteriol; model MODEL1507180020)",
            "" if is_pao1 else "Gene ID does not match PAxxxx PAO1 locus-tag pattern; review",
        ])
print("wrote data/processed/gene_mapping.csv:", len(model.genes), "genes")

# ---------------------------------------------------------------------------
# 2) literature_evidence.csv  (schema + study-level provenance; gene rows PENDING)
# ---------------------------------------------------------------------------
le_cols = [
    "study_id", "full_citation", "doi", "publication_year", "strain",
    "locus_tag", "gene_name", "ortholog_group", "experimental_condition",
    "medium", "carbon_source", "electron_acceptor", "growth_phase",
    "experimental_method", "comparison_group", "phenotype_type",
    "essentiality_definition", "effect_direction", "effect_size",
    "statistical_threshold", "validation_method", "page", "table", "figure",
    "supplementary_dataset", "source_file", "model_gene_id", "mapping_method",
    "mapping_confidence", "notes",
]

# Study-level rows: metadata that is directly evidenced by the PDFs (titles, DOIs,
# strain/condition from headings). Gene-level locus tags are PENDING_EXTRACTION
# because supplementary .xlsx datasets have not been downloaded/validated yet.
studies = [
    dict(study_id="juhas2015", year="2015", strain="PAO1/PA14 (review)",
         doi="10.1099/mic.0.000161", phenotype_type="generally_essential",
         method="review of Tn-seq / essential-gene studies",
         citation="Juhas M, et al. (2015) Pseudomonas aeruginosa essentials: an update on investigation of essential genes. Microbiology 161(11):2053-2060.",
         source_file="conditian/juhas2015.pdf",
         notes="Review/update. Strain and method are study-dependent; do not merge classes. Extract gene lists only where the review cites a primary dataset."),
    dict(study_id="turner2015", year="2015", strain="PA14",
         doi="10.1073/pnas.1419677112", phenotype_type="condition_specific_essential",
         method="Tn-seq (transposon insertion sequencing)",
         citation="Turner KH, et al. (2015) Essential genome of Pseudomonas aeruginosa in cystic fibrosis sputum. PNAS 112(13):4110-4115.",
         source_file="conditian/keith H.pdf",
         notes="Condition: CF sputum (SCFM/sputum) vs rich medium. Supplements sd01-sd04.xlsx (DCSupplemental) NOT yet downloaded - BLOCKER. PA14 strain: do NOT treat as PAO1."),
    dict(study_id="lee2015", year="2015", strain="PA14",
         doi="10.1073/pnas.1422186112", phenotype_type="general_and_condition_specific_essential",
         method="Tn-seq",
         citation="Lee SA, et al. (2015) General and condition-specific essential functions of Pseudomonas aeruginosa. PNAS 112(16):5189-5194.",
         source_file="conditian/samuelA.pdf",
         notes="Distinguishes general vs condition-specific essentiality (e.g., growth on LB vs minimal/nutrient conditions). Supplement sd01.xlsx NOT yet downloaded - BLOCKER. PA14 strain."),
    dict(study_id="poulsen2019", year="2019", strain="PA14 (multi-strain core)",
         doi="10.1073/pnas.1900570116", phenotype_type="core_essential",
         method="Tn-seq + FiTnEss statistical framework",
         citation="Poulsen BE, et al. (2019) Defining the core essential genome of Pseudomonas aeruginosa. PNAS 116(20):10072-10080.",
         source_file="conditian/polsun2019.pdf",
         notes="Core essential genome across strains. Data: https://data.broadinstitute.org/fitness/ ; code https://github.com/broadinstitute/FiTnEss. Supplements NOT yet downloaded - BLOCKER."),
    dict(study_id="basta2017", year="2017", strain="PA14 (confirm in PMC methods)",
         doi="10.1128/mBio.01170-17", phenotype_type="survival_determinant_growth_arrest",
         method="Tn-seq during energy-limited growth arrest (pyruvate-carbon or oxygen limitation)",
         citation="Basta DW, Bergkessel M, Newman DK (2017) Identification of fitness determinants during energy-limited growth arrest in Pseudomonas aeruginosa. mBio 8(6):e01170-17.",
         source_file="conditian/davidW.pdf",
         notes="DOI VERIFIED (journals.asm.org + PMC5705914). Erratum 10.1128/mbio.00576-18. Survival/fitness during growth ARREST != essentiality for growth - keep distinct. Strain (Newman lab, likely PA14) to confirm from methods; supplements PENDING_DOWNLOAD."),
    dict(study_id="belanger2022", year="2022", strain="(confirm in methods)",
         doi="10.3389/fmicb.2022.1055512", phenotype_type="host_condition_fitness",
         method="Tn-seq in physiologically-relevant (host-mimicking) conditions: tissue-culture medium +/- human serum, murine abscess, human skin organoid",
         citation="Belanger CR, Dostert M, Blimkie TM, Lee AHY, Dhillon BK, Wu BC, et al. Hancock REW (2022) Surviving the host: microbial metabolic genes required for growth of Pseudomonas aeruginosa in physiologically-relevant conditions. Front Microbiol 13:1055512.",
         source_file="conditian/corrieR.pdf",
         notes="DOI VERIFIED (frontiersin.org + PMC9732424). Published 2022-11-25 (NOT 2020). Hancock lab. Host-relevant fitness determinants. Strain + supplements to confirm/download - PENDING."),
]

with open("data/processed/literature_evidence.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=le_cols)
    w.writeheader()
    for s in studies:
        row = {c: "" for c in le_cols}
        row.update({
            "study_id": s["study_id"],
            "full_citation": s["citation"],
            "doi": s["doi"],
            "publication_year": s["year"],
            "strain": s["strain"],
            "locus_tag": "PENDING_EXTRACTION",
            "experimental_method": s["method"],
            "phenotype_type": s["phenotype_type"],
            "supplementary_dataset": "PENDING_DOWNLOAD",
            "source_file": s["source_file"],
            "mapping_method": "PENDING",
            "mapping_confidence": "PENDING",
            "notes": s["notes"],
        })
        w.writerow(row)
print("wrote data/processed/literature_evidence.csv:", len(studies), "study-level rows (gene-level PENDING)")

# ---------------------------------------------------------------------------
# 3) papers/manifest.csv
# ---------------------------------------------------------------------------
pm_cols = [
    "study_id", "current_path", "planned_path", "size_bytes", "title_or_topic",
    "first_author", "year", "doi", "journal", "strain_focus", "phenotype_class",
    "supplementary_available", "provenance", "id_confidence",
]
papers = [
    ["juhas2015", "conditian/juhas2015.pdf", "papers/juhas2015.pdf", 363517,
     "Pseudomonas aeruginosa essentials: an update on investigation of essential genes",
     "Juhas", "2015", "10.1099/mic.0.000161", "Microbiology", "review",
     "generally_essential", "DCSupplemental? review", "provided_in_repo (conditian/)", "high"],
    ["turner2015", "conditian/keith H.pdf", "papers/turner2015.pdf", 1316506,
     "Essential genome of Pseudomonas aeruginosa in cystic fibrosis sputum",
     "Turner", "2015", "10.1073/pnas.1419677112", "PNAS", "PA14",
     "condition_specific_essential", "yes (sd01-sd04.xlsx)", "provided_in_repo (conditian/)", "high"],
    ["lee2015", "conditian/samuelA.pdf", "papers/lee2015.pdf", 744562,
     "General and condition-specific essential functions of Pseudomonas aeruginosa",
     "Lee", "2015", "10.1073/pnas.1422186112", "PNAS", "PA14",
     "general_and_condition_specific_essential", "yes (sd01.xlsx)", "provided_in_repo (conditian/)", "high"],
    ["poulsen2019", "conditian/polsun2019.pdf", "papers/poulsen2019.pdf", 1181682,
     "Defining the core essential genome of Pseudomonas aeruginosa",
     "Poulsen", "2019", "10.1073/pnas.1900570116", "PNAS", "PA14 (multi-strain core)",
     "core_essential", "yes (broadinstitute fitness data + FiTnEss)", "provided_in_repo (conditian/)", "high"],
    ["basta2017", "conditian/davidW.pdf", "papers/basta2017.pdf", 2850434,
     "Identification of fitness determinants during energy-limited growth arrest in P. aeruginosa",
     "Basta", "2017", "10.1128/mBio.01170-17", "mBio", "PA14 (confirm)",
     "survival_determinant_growth_arrest", "PENDING (PMC5705914)", "provided_in_repo (conditian/)", "high (DOI verified)"],
    ["belanger2022", "conditian/corrieR.pdf", "papers/belanger2022.pdf", 3746954,
     "Surviving the host: microbial metabolic genes required for growth of P. aeruginosa in physiologically-relevant conditions",
     "Belanger", "2022", "10.3389/fmicb.2022.1055512", "Frontiers in Microbiology", "confirm",
     "host_condition_fitness", "PENDING (PMC9732424)", "provided_in_repo (conditian/); PDF /Author: R.E.W. Hancock", "high (DOI verified)"],
]
with open("papers/manifest.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(pm_cols)
    w.writerows(papers)
print("wrote papers/manifest.csv:", len(papers), "papers")

# ---------------------------------------------------------------------------
# 4) clean machine-readable audit snapshot
# ---------------------------------------------------------------------------
snap = {
    "model_file": "models/paeruginosa_MODEL1507180020.xml",
    "file_sha256": "0868a5ebb41ebb4967c3c182e686eca7552af9255cba5a6d130cf114d1212ead",
    "model_id": model.id,
    "model_name": model.name,
    "identity": "iMO1056 (Oberhardt et al. 2008, P. aeruginosa PAO1); BioModels MODEL1507180020",
    "strain": "PAO1 (evidence: PAxxxx locus tags + iMO1056 identity)",
    "sbml_level": 3, "sbml_version": 1,
    "n_reactions": len(model.reactions),
    "n_metabolites": len(model.metabolites),
    "n_genes": len(model.genes),
    "compartments": dict(model.compartments),
    "objective": [r.id for r in model.reactions if r.objective_coefficient != 0],
    "objective_direction": model.objective.direction,
    "n_exchange": len(model.exchanges),
    "n_demand": len(model.demands),
    "n_sink": len(model.sinks),
    "n_reactions_without_genes": sum(1 for r in model.reactions if len(r.genes) == 0),
    "n_genes_without_reactions": sum(1 for g in model.genes if len(g.reactions) == 0),
    "n_metabolites_missing_formula": sum(1 for m in model.metabolites if not m.formula),
    "n_metabolites_missing_charge": sum(1 for m in model.metabolites if m.charge is None),
}
m2 = model.copy()
sol = m2.optimize()
snap["default_growth"] = sol.objective_value
snap["default_status"] = sol.status
snap["default_medium"] = dict(model.medium)
with open("model_audit_snapshot.json", "w", encoding="utf-8") as f:
    json.dump(snap, f, indent=2, default=str)
print("wrote model_audit_snapshot.json")
print(json.dumps(snap, indent=2, default=str))

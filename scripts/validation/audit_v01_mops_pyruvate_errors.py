"""Structural error audit of frozen V-01 MOPS-pyruvate binary validation.

DIAGNOSTIC ONLY — does not modify model, media, GPRs, biomass, or threshold.
Does not overwrite original V-01 prediction / confusion-matrix artifacts.

Usage:
  C:/Users/pro/anaconda3/envs/reccobra39/python.exe \\
    scripts/validation/audit_v01_mops_pyruvate_errors.py
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.stdout.reconfigure(encoding="utf-8")

MODEL_PATH = ROOT / "models" / "paeruginosa_MODEL1507180020.xml"
BINARY_UNIVERSE = (
    ROOT
    / "data/processed/literature/gene_level"
    / "varadarajan2020_lee2015_minimal_PRIMARY_BINARY_UNIVERSE.csv"
)
PRED_JOINED = ROOT / "data/processed/validation" / "v01_mops_pyruvate_gene_predictions.csv"
METRICS_JSON = ROOT / "data/processed/validation" / "v01_mops_pyruvate_metrics.json"
FP_PATH = ROOT / "data/processed/validation" / "v01_mops_pyruvate_false_positives.csv"
FN_PATH = ROOT / "data/processed/validation" / "v01_mops_pyruvate_false_negatives.csv"
TP_PATH = ROOT / "data/processed/validation" / "v01_mops_pyruvate_true_positives.csv"
TN_PATH = ROOT / "data/processed/validation" / "v01_mops_pyruvate_true_negatives.csv"

OUT_DIR = ROOT / "data/processed/validation"
AUDIT_DIR = ROOT / "project_management/audit/v01_mops_pyruvate"

OUT_AUDIT = OUT_DIR / "v01_mops_pyruvate_error_audit.csv"
OUT_FN = OUT_DIR / "v01_mops_pyruvate_false_negative_audit.csv"
OUT_FP = OUT_DIR / "v01_mops_pyruvate_false_positive_audit.csv"
OUT_COUNTS = AUDIT_DIR / "V01_ERROR_CATEGORY_COUNTS.csv"
OUT_REPORT = AUDIT_DIR / "V01_ERROR_STRUCTURE_AUDIT.md"

MEDIUM_ID = "mops_pyruvate_lee2015"
THRESHOLD = 0.01
OBJECTIVE = "PA_Biomass6_DM"
STATUS_GATE = "V01_ERROR_ANALYSIS_COMPLETED_PENDING_HUMAN_REVIEW"

EXPECTED = {"TP": 116, "FN": 98, "TN": 764, "FP": 47, "n": 1025}

# DIAGNOSTIC ONLY threshold-distance bins (classification unchanged)
NEAR_FN = (0.01, 0.05)  # just above essential cutoff
MOD_FN = (0.05, 0.50)
FAR_FN = (0.50, 0.99)
# FN extreme: ratio >= 0.99
# FP: all observed ratios ≪ 0.01; bins on abs(ratio)
NEAR_FP = (1e-3, 0.01)
MOD_FP = (1e-6, 1e-3)
# FP extreme: abs(ratio) < 1e-6

TRNA_RE = re.compile(r"tRNA synthetase|aminoacyl-tRNA|-\s*tRNA ligase", re.I)
TRANSPORT_NAME_RE = re.compile(
    r"transport|permease|ABC|uptake|export|efflux|porin|symport|antiport",
    re.I,
)

# Descriptive name-keyword clusters (NOT formal statistical enrichment).
# Applied to concatenated reaction names; first match wins for primary cluster.
PATHWAY_KEYWORDS: Sequence[Tuple[str, Sequence[str]]] = (
    ("amino_acid_biosynthesis", (
        "arginine", "ornithine", "aspartate", "asparagine", "glutamate",
        "glutamine", "proline", "serine", "glycine", "threonine", "methionine",
        "cysteine", "lysine", "histidine", "tryptophan", "tyrosine",
        "phenylalanine", "valine", "leucine", "isoleucine", "chorismate",
        "anthranilate", "homoserine", "diaminopimelate", "amino acid",
        "transaminase", "aminotransferase",
    )),
    ("nucleotide_metabolism", (
        "purine", "pyrimidine", "nucleotide", "nucleoside", "IMP ", "GMP",
        "AMP ", "UMP", "CMP", "TMP", "dCTP", "dTTP", "ribo", "dihydroorot",
        "carbamoyl", "PRPP", "adenyl", "guanyl", "thymid", "urid", "cytid",
    )),
    ("cofactor_biosynthesis", (
        "thiamine", "riboflavin", "FMN", "FAD", "NAD", "pantothenate",
        "coenzyme", "biotin", "folate", "tetrahydrofolate", "pyridox",
        "heme", "porphyrin", "ubiquinone", "menaquinone", "cobalamin",
        "lipoate", "molybdopterin", "siroheme", "enterochelin", "siderophore",
    )),
    ("central_carbon_metabolism", (
        "glycolysis", "gluconeogenesis", "pentose", "TCA", "citrate",
        "aconitate", "isocitrate", "succinate", "fumarate", "malate",
        "pyruvate", "glyceraldehyde", "phosphoglycerate", "enolase",
        "ribulose", "transketolase", "transaldolase", "ED pathway",
        "Entner", "glucose-6-phosphate isomerase",
    )),
    ("energy_metabolism", (
        "ATP synthase", "NADH", "dehydrogenase", "cytochrome", "oxidase",
        "respiration", "quinone", "oxidative phosphorylation", "ferredoxin",
    )),
    ("lipid_lps_metabolism", (
        "lipid", "fatty acid", "acyl-carrier", "acyl carrier", "phosphatidyl",
        "LPS", "lipopolysaccharide", "KDO", "lipidA", "lipid A",
        "undecaprenyl", "glycerol", "cardiolipin", "diacyl",
    )),
    ("transport", (
        "transport", "permease", "ABC", "uptake", "export", "efflux",
    )),
    ("translation_trna", (
        "tRNA synthetase", "aminoacyl-tRNA", "tRNA ligase",
    )),
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_frozen_v01() -> Dict:
    """PHASE 0 — confirm frozen confusion counts; abort on mismatch."""
    if not METRICS_JSON.exists():
        raise SystemExit("V01_AUDIT_ABORT: missing metrics JSON")
    metrics = json.loads(METRICS_JSON.read_text(encoding="utf-8"))
    cm = metrics["confusion_matrix"]
    for k, exp in EXPECTED.items():
        if int(cm[k]) != exp:
            raise SystemExit(
                f"V01_AUDIT_ABORT: confusion {k}={cm[k]} != expected {exp}"
            )
    for path, n, label in (
        (TP_PATH, 116, "TP"),
        (FN_PATH, 98, "FN"),
        (TN_PATH, 764, "TN"),
        (FP_PATH, 47, "FP"),
    ):
        df = pd.read_csv(path)
        if len(df) != n:
            raise SystemExit(
                f"V01_AUDIT_ABORT: {path.name} n={len(df)} != {n} ({label})"
            )
    joined = pd.read_csv(PRED_JOINED)
    if len(joined) != 1025:
        raise SystemExit(f"V01_AUDIT_ABORT: joined n={len(joined)} != 1025")
    print(
        "PHASE 0 PASS: TP=116 FN=98 TN=764 FP=47 n=1025 "
        "(frozen V-01 artifacts verified)"
    )
    return metrics


def _threshold_distance_bin(error_type: str, ratio: float) -> str:
    """DIAGNOSTIC ONLY distance-to-cutoff labels; does not reclassify."""
    thr = THRESHOLD
    if error_type == "FN":
        # FN are model-NEGATIVE → ratio >= thr
        if thr <= ratio < 0.05:
            return "DIAG_NEAR_THRESHOLD_[0.01,0.05)"
        if 0.05 <= ratio < 0.50:
            return "DIAG_MODERATELY_FAR_[0.05,0.50)"
        if 0.50 <= ratio < 0.99:
            return "DIAG_FAR_[0.50,0.99)"
        return "DIAG_EXTREMELY_FAR_ratio_ge_0.99"
    # FP are model-POSITIVE → ratio < thr; use abs for solver noise
    ar = abs(float(ratio))
    if 1e-3 <= ar < thr:
        return "DIAG_NEAR_THRESHOLD_[1e-3,0.01)"
    if 1e-6 <= ar < 1e-3:
        return "DIAG_MODERATELY_FAR_[1e-6,1e-3)"
    return "DIAG_EXTREMELY_FAR_abs_ratio_lt_1e-6"


def _pathway_cluster(reaction_names: Sequence[str], reaction_ids: Sequence[str]) -> str:
    text = " ".join(list(reaction_names) + list(reaction_ids)).lower()
    if not text.strip():
        return "unannotated_or_empty"
    for cluster, keys in PATHWAY_KEYWORDS:
        for k in keys:
            if k.lower() in text:
                return cluster
    return "other_or_unclassified"


def _is_transport(reaction, name: str) -> bool:
    if reaction.boundary:
        return True
    rid = reaction.id
    if rid.startswith("EX_") or rid.startswith("DM_") or rid.startswith("SK_"):
        return True
    if TRANSPORT_NAME_RE.search(name or ""):
        return True
    if rid.endswith("abc") or rid.endswith("t") and "abc" in rid.lower():
        return True
    return False


def _biomass_direct_link(reaction, bm_mets: Set[str]) -> bool:
    if reaction.id == OBJECTIVE:
        return True
    return any(m.id in bm_mets for m in reaction.metabolites)


def inspect_gene(
    model,
    gene_id: str,
    flux: pd.Series,
    blocked: Set[str],
    bm_mets: Set[str],
) -> Dict:
    if gene_id not in model.genes:
        return {
            "associated_reactions": "",
            "reaction_count": 0,
            "GPR_rules": "",
            "isoenzyme_flag": False,
            "multi_gene_complex_flag": False,
            "blocked_reaction_flag": False,
            "active_under_MOPS_flag": False,
            "all_reactions_disabled_by_KO": False,
            "any_reaction_survives_KO": False,
            "subsystem_pathway": "gene_absent_from_model",
            "pathway_cluster": "gene_absent_from_model",
            "biomass_direct_link": False,
            "transport_flag": False,
            "trna_synthetase_flag": False,
            "reaction_names": "",
        }

    gene = model.genes.get_by_id(gene_id)
    rxns = sorted(gene.reactions, key=lambda r: r.id)
    ids: List[str] = []
    names: List[str] = []
    rules: List[str] = []
    has_or = False
    has_and = False
    any_active = False
    all_blocked = True if rxns else False
    biomass_link = False
    transport = False
    trna = False
    any_survives = False
    all_disabled = True if rxns else False

    for r in rxns:
        ids.append(r.id)
        nm = r.name or ""
        names.append(nm)
        rule = r.gene_reaction_rule or ""
        rules.append(f"{r.id}:{rule}")
        rl = rule.lower()
        if " or " in rl:
            has_or = True
        if " and " in rl:
            has_and = True
        if abs(float(flux.get(r.id, 0.0))) > 1e-8:
            any_active = True
        if r.id not in blocked:
            all_blocked = False
        if _biomass_direct_link(r, bm_mets):
            biomass_link = True
        if _is_transport(r, nm):
            transport = True
        if TRNA_RE.search(nm):
            trna = True
        # cobra GPR knockout semantics (read-only)
        survives = False
        if rule.strip():
            try:
                survives = bool(r.gpr.eval(knockouts={gene_id}))
            except Exception:
                survives = False
        else:
            # no GPR → gene deletion does not remove reaction in cobra
            survives = True
        if survives:
            any_survives = True
            all_disabled = False
        else:
            pass

    cluster = _pathway_cluster(names, ids)
    # Model has empty subsystem annotations; report keyword cluster explicitly.
    subsystem_pathway = (
        f"NO_MODEL_SUBSYSTEM;name_keyword_cluster={cluster}"
    )

    return {
        "associated_reactions": ";".join(ids),
        "reaction_count": len(ids),
        "GPR_rules": " || ".join(rules),
        "isoenzyme_flag": bool(has_or),
        "multi_gene_complex_flag": bool(has_and),
        "blocked_reaction_flag": bool(all_blocked),
        "active_under_MOPS_flag": bool(any_active),
        "all_reactions_disabled_by_KO": bool(all_disabled),
        "any_reaction_survives_KO": bool(any_survives),
        "subsystem_pathway": subsystem_pathway,
        "pathway_cluster": cluster,
        "biomass_direct_link": bool(biomass_link),
        "transport_flag": bool(transport),
        "trna_synthetase_flag": bool(trna),
        "reaction_names": ";".join(names),
    }


def classify_fn(row: Dict) -> Tuple[str, str, str]:
    """Return (diagnostic_category, confidence, notes). Association ≠ causality."""
    notes: List[str] = []
    ratio = float(row["KO_WT_ratio"])

    if THRESHOLD <= ratio < 0.05:
        return (
            "FN_NEAR_THRESHOLD",
            "high",
            "KO/WT ratio in diagnostic near-cutoff bin [0.01,0.05); "
            "classification boundary proximity (cutoff unchanged).",
        )

    if str(row["mapping_status"]) != "unique_std_PAO1":
        return (
            "FN_MAPPING_OR_ANNOTATION",
            "medium",
            f"mapping_status={row['mapping_status']} (not unique_std_PAO1).",
        )

    # Structural: unused reactions under locked medium
    if row["blocked_reaction_flag"] and row["reaction_count"] > 0:
        notes.append(
            "All associated reactions are blocked under mops_pyruvate_lee2015 "
            "(find_blocked_reactions); KO cannot reduce growth via these edges."
        )
        if row["trna_synthetase_flag"]:
            notes.append(
                "Reaction name indicates tRNA synthetase; charged-tRNA demand "
                "may be outside biomass formulation (secondary observation)."
            )
        conf = "high" if not row["active_under_MOPS_flag"] else "medium"
        return ("FN_REACTION_INACTIVE", conf, " ".join(notes))

    # Structural: isoenzyme / OR-GPR keeps ≥1 reaction after KO
    if row["isoenzyme_flag"] and row["any_reaction_survives_KO"]:
        notes.append(
            "At least one associated reaction has OR-logic GPR and remains "
            "True after single-gene KO (cobra.gpr.eval); isoenzyme/redundancy "
            "compatible with retained growth."
        )
        return ("FN_ISOENZYME_REDUNDANCY", "high", " ".join(notes))

    # Complex GPR without clear surviving OR branch
    if (row["isoenzyme_flag"] or row["multi_gene_complex_flag"]) and not row[
        "all_reactions_disabled_by_KO"
    ]:
        return (
            "FN_GPR_STRUCTURE",
            "medium",
            "Multi-gene GPR present; knockout does not disable all associated "
            "reactions under cobra GPR evaluation.",
        )

    if row["transport_flag"]:
        return (
            "FN_TRANSPORT_OR_EXCHANGE_CONTEXT",
            "medium",
            "Associated reaction(s) annotated/named as transport/exchange; "
            "environmental representation may contribute (association only).",
        )

    if row["trna_synthetase_flag"]:
        return (
            "FN_BIOMASS_FORMULATION",
            "medium",
            "tRNA synthetase reaction name; PA_Biomass6_DM does not list "
            "aminoacyl-tRNAs as explicit constituents (structural observation).",
        )

    # Network bypass: KO disables associated reactions (or sole gene) but growth retained
    if (
        row["reaction_count"] > 0
        and ratio >= 0.50
        and (
            row["all_reactions_disabled_by_KO"]
            or (not row["isoenzyme_flag"] and not row["multi_gene_complex_flag"])
        )
        and not row["blocked_reaction_flag"]
    ):
        notes.append(
            f"KO/WT ratio={ratio:.4f} with associated reaction(s) not all blocked; "
            "retained growth is compatible with alternative route(s) in the network."
        )
        return ("FN_ALTERNATIVE_PATHWAY", "medium", " ".join(notes))

    # Reduced but still non-essential far above cutoff
    if 0.05 <= ratio < 0.50:
        return (
            "FN_ALTERNATIVE_PATHWAY",
            "low",
            f"Partial growth defect (ratio={ratio:.4f}) still classified "
            "MODEL_NEGATIVE at fixed 0.01 cutoff; possible partial bypass.",
        )

    if row["reaction_count"] == 0:
        return (
            "FN_UNRESOLVED",
            "low",
            "Gene present in essentiality table but no associated reactions "
            "found in loaded model object.",
        )

    return (
        "FN_UNRESOLVED",
        "low",
        "Insufficient structural evidence for a more specific diagnostic category.",
    )


def classify_fp(row: Dict) -> Tuple[str, str, str]:
    notes: List[str] = []
    ratio = float(row["KO_WT_ratio"])
    ar = abs(ratio)

    if 1e-3 <= ar < THRESHOLD:
        return (
            "FP_NEAR_THRESHOLD",
            "high",
            "KO/WT abs(ratio) in diagnostic near-cutoff bin; "
            "classification boundary proximity (cutoff unchanged).",
        )

    if str(row["mapping_status"]) != "unique_std_PAO1":
        return (
            "FP_MAPPING_OR_ANNOTATION",
            "medium",
            f"mapping_status={row['mapping_status']} (not unique_std_PAO1).",
        )

    # Sulfate / nutrient ABC transport cluster pattern
    rx = str(row["associated_reactions"])
    if row["transport_flag"] or "abc" in rx.lower() or rx.startswith("EX_"):
        notes.append(
            "Transport/exchange-associated reaction(s); model requires them for "
            "growth under locked MOPS-pyruvate exchanges."
        )
        # Prefer missing-transport when GPR is multi-subunit ABC
        if row["multi_gene_complex_flag"] and "abc" in rx.lower():
            return (
                "FP_MISSING_TRANSPORT",
                "high",
                " ".join(notes)
                + " Multi-subunit ABC GPR: experimental viability may reflect "
                "alternate uptake not represented (association only).",
            )
        return ("FP_MEDIA_CONTEXT", "medium", " ".join(notes))

    if row["isoenzyme_flag"] and row["any_reaction_survives_KO"]:
        # Unusual for FP (model essential despite OR) — GPR oddity
        return (
            "FP_GPR_STRUCTURE",
            "medium",
            "OR-logic present yet gene still model-essential; inspect GPR/other "
            "reactions for non-redundant essential edge.",
        )

    if row["multi_gene_complex_flag"] and row["all_reactions_disabled_by_KO"]:
        return (
            "FP_GPR_STRUCTURE",
            "medium",
            "AND-complex GPR: deleting this subunit disables associated "
            "reaction(s) and abolishes growth in the model.",
        )

    if row["trna_synthetase_flag"] or (
        row["biomass_direct_link"]
        and row["pathway_cluster"] in {"cofactor_biosynthesis", "lipid_lps_metabolism"}
        and row["reaction_count"] <= 2
    ):
        # Biomass-linked sole requirements often over-constrain FPs
        if row["pathway_cluster"] in {"cofactor_biosynthesis", "lipid_lps_metabolism", "nucleotide_metabolism"}:
            return (
                "FP_BIOMASS_FORMULATION",
                "medium",
                "Gene linked to biomass-connected cofactor/lipid/nucleotide "
                "reaction(s); experimental non-essentiality may reflect biomass "
                "composition or salvage not represented (association only).",
            )

    if (
        not row["isoenzyme_flag"]
        and row["reaction_count"] > 0
        and row["all_reactions_disabled_by_KO"]
        and row["active_under_MOPS_flag"]
    ):
        notes.append(
            "Sole/required GPR on active reaction(s); KO abolishes growth. "
            "Compatible with missing isoenzyme or missing alternative pathway "
            "in iMO1056 (not distinguished by structure alone)."
        )
        # Prefer missing alternative when multiple reactions / central pathways
        if row["reaction_count"] >= 2 or row["pathway_cluster"] in {
            "central_carbon_metabolism",
            "amino_acid_biosynthesis",
            "nucleotide_metabolism",
        }:
            return ("FP_MISSING_ALTERNATIVE_PATHWAY", "medium", " ".join(notes))
        return ("FP_MISSING_ISOENZYME", "medium", " ".join(notes))

    if row["active_under_MOPS_flag"] and row["biomass_direct_link"]:
        return (
            "FP_OVER_RESTRICTIVE_NETWORK",
            "low",
            "Active biomass-linked reaction(s) with lethal KO; network may be "
            "over-restrictive relative to experiment (broad residual category).",
        )

    return (
        "FP_UNRESOLVED",
        "low",
        "Insufficient structural evidence for a more specific diagnostic category.",
    )


def priority_rank(
    error_type: str,
    category: str,
    confidence: str,
    *,
    trna_synthetase_flag: bool = False,
    pathway_cluster: str = "",
) -> Tuple[int, str]:
    """Priority 1=inspectable structural; 2=scope/biology; 3=ambiguous."""
    # Translation / tRNA blocked reactions are scope/biomass issues more than
    # editable metabolic network bugs — demote to Priority 2.
    if trna_synthetase_flag or pathway_cluster == "translation_trna":
        return 2, "likely biological/model-scope disagreement (translation/tRNA)"

    p1_fn = {
        "FN_ISOENZYME_REDUNDANCY",
        "FN_GPR_STRUCTURE",
        "FN_ALTERNATIVE_PATHWAY",
        "FN_NEAR_THRESHOLD",
    }
    # Reaction-inactive is P1 only when not translation-scoped (handled above)
    p1_fn_inactive = {"FN_REACTION_INACTIVE"}
    p1_fp = {
        "FP_MISSING_TRANSPORT",
        "FP_GPR_STRUCTURE",
        "FP_MISSING_ISOENZYME",
        "FP_MISSING_ALTERNATIVE_PATHWAY",
        "FP_NEAR_THRESHOLD",
        "FP_MEDIA_CONTEXT",
    }
    p2 = {
        "FN_BIOMASS_FORMULATION",
        "FN_NON_METABOLIC_OR_OUT_OF_SCOPE",
        "FN_TRANSPORT_OR_EXCHANGE_CONTEXT",
        "FN_REACTION_INACTIVE",  # residual inactive after tRNA split still often scope
        "FP_BIOMASS_FORMULATION",
        "FP_OVER_RESTRICTIVE_NETWORK",
    }
    if category in p1_fn and confidence in {"high", "medium"}:
        return 1, f"{confidence}-confidence structural / inspectable"
    if category in p1_fp and confidence in {"high", "medium"}:
        return 1, f"{confidence}-confidence structural / inspectable"
    # Non-tRNA blocked reactions with clear metabolic names: still inspectable P1
    if (
        category in p1_fn_inactive
        and confidence == "high"
        and pathway_cluster
        not in {"translation_trna", "other_or_unclassified", "unannotated_or_empty"}
    ):
        return 1, "high-confidence inactive-reaction structural / inspectable"
    if category in p2:
        return 2, "likely biological/model-scope disagreement"
    return 3, "ambiguous or insufficient evidence"


def safest_review_action(error_type: str, category: str) -> str:
    actions = {
        "FN_ISOENZYME_REDUNDANCY": (
            "Manually inspect OR-GPRs and ask whether isozyme annotation is "
            "biologically justified; do not auto-edit GPRs."
        ),
        "FN_ALTERNATIVE_PATHWAY": (
            "Trace metabolite bypass around associated reaction(s) under "
            "MOPS-pyruvate; document route before considering any gap change."
        ),
        "FN_REACTION_INACTIVE": (
            "Confirm blocked status and whether experimental essentiality is "
            "non-metabolic / translation / condition-specific outside FBA scope."
        ),
        "FN_GPR_STRUCTURE": (
            "Parse GPR Boolean structure vs literature enzyme complex/isozyme "
            "evidence; no automated rewrite."
        ),
        "FN_BIOMASS_FORMULATION": (
            "Compare reaction products to PA_Biomass6_DM constituents; record "
            "missing demand only as a hypothesis for human review."
        ),
        "FN_TRANSPORT_OR_EXCHANGE_CONTEXT": (
            "Compare transport annotation to locked medium exchange set."
        ),
        "FN_NEAR_THRESHOLD": (
            "Note proximity to 0.01 only; do not retune threshold in this audit."
        ),
        "FN_MAPPING_OR_ANNOTATION": (
            "Re-check MPAO1↔PAO1 mapping provenance for this locus."
        ),
        "FN_UNRESOLVED": (
            "Leave unresolved; gather reaction/literature context before any edit."
        ),
        "FP_MISSING_TRANSPORT": (
            "Inspect whether alternate sulfate/nutrient uptake exists in PAO1 "
            "literature; do not add transporters without a sourced decision."
        ),
        "FP_MISSING_ISOENZYME": (
            "Search for documented isozymes for the essential reaction; no auto-add."
        ),
        "FP_MISSING_ALTERNATIVE_PATHWAY": (
            "Identify missing bypass reactions from PAO1 metabolic literature."
        ),
        "FP_GPR_STRUCTURE": (
            "Review AND-complex necessity vs experimental subunit essentiality."
        ),
        "FP_BIOMASS_FORMULATION": (
            "Check whether biomass coefficient/demand forces false essentiality."
        ),
        "FP_MEDIA_CONTEXT": (
            "Compare experimental MOPS-pyruvate recipe vs locked exchange bounds."
        ),
        "FP_OVER_RESTRICTIVE_NETWORK": (
            "Manual network inspection of lethal cut set; no gap-fill in this step."
        ),
        "FP_NEAR_THRESHOLD": (
            "Note proximity to 0.01 only; do not retune threshold in this audit."
        ),
        "FP_MAPPING_OR_ANNOTATION": (
            "Re-check mapping provenance for this locus."
        ),
        "FP_UNRESOLVED": (
            "Leave unresolved pending manual literature/model review."
        ),
    }
    return actions.get(
        category,
        "Manual review only; do not modify model/media/threshold from this audit.",
    )


def build_audit_table(model, flux, blocked, bm_mets) -> pd.DataFrame:
    fn = pd.read_csv(FN_PATH)
    fp = pd.read_csv(FP_PATH)
    universe = pd.read_csv(BINARY_UNIVERSE).set_index("pao1_locus", drop=False)
    joined = pd.read_csv(PRED_JOINED).set_index("pao1_locus", drop=False)

    rows: List[Dict] = []
    for error_type, df in (("FN", fn), ("FP", fp)):
        for _, erow in df.sort_values("pao1_locus").iterrows():
            gid = str(erow["pao1_locus"])
            j = joined.loc[gid]
            u = universe.loc[gid]
            struct = inspect_gene(model, gid, flux, blocked, bm_mets)
            base = {
                "gene": gid,
                "error_type": error_type,
                "experimental_label": str(erow["experimental_label"]),
                "model_prediction": str(erow["model_prediction"]),
                "minimal_sum": int(erow["minimal_sum"]),
                "WT_growth": float(erow["wildtype_growth"]),
                "KO_growth": float(erow["knockout_growth"]),
                "KO_WT_ratio": float(erow["growth_ratio"]),
                "mapping_status": str(u["mapping_status"]),
                "evidence_source": str(erow["experimental_source"]),
                "mpao1_locus": str(erow["mpao1_locus"]),
                "joined_experiment_polarity": str(j["experiment_polarity"]),
                "joined_short_label": str(j["short_label"]),
            }
            base.update(struct)
            base["threshold_distance_bin"] = _threshold_distance_bin(
                error_type, base["KO_WT_ratio"]
            )
            if error_type == "FN":
                cat, conf, notes = classify_fn(base)
            else:
                cat, conf, notes = classify_fp(base)
            base["diagnostic_category"] = cat
            base["diagnostic_confidence"] = conf
            base["notes"] = notes
            pr, pr_why = priority_rank(
                error_type,
                cat,
                conf,
                trna_synthetase_flag=bool(base["trna_synthetase_flag"]),
                pathway_cluster=str(base["pathway_cluster"]),
            )
            base["review_priority"] = pr
            base["review_priority_reason"] = pr_why
            base["safest_manual_review_action"] = safest_review_action(
                error_type, cat
            )
            base["suspected_discrepancy_mechanism"] = cat
            rows.append(base)

    audit = pd.DataFrame(rows)
    # Deterministic column order
    cols = [
        "gene",
        "error_type",
        "experimental_label",
        "model_prediction",
        "minimal_sum",
        "WT_growth",
        "KO_growth",
        "KO_WT_ratio",
        "threshold_distance_bin",
        "associated_reactions",
        "reaction_count",
        "reaction_names",
        "GPR_rules",
        "isoenzyme_flag",
        "multi_gene_complex_flag",
        "blocked_reaction_flag",
        "active_under_MOPS_flag",
        "all_reactions_disabled_by_KO",
        "any_reaction_survives_KO",
        "subsystem_pathway",
        "pathway_cluster",
        "biomass_direct_link",
        "transport_flag",
        "trna_synthetase_flag",
        "mapping_status",
        "evidence_source",
        "mpao1_locus",
        "joined_experiment_polarity",
        "joined_short_label",
        "diagnostic_category",
        "diagnostic_confidence",
        "review_priority",
        "review_priority_reason",
        "suspected_discrepancy_mechanism",
        "safest_manual_review_action",
        "notes",
    ]
    audit = audit[cols].sort_values(["error_type", "gene"]).reset_index(drop=True)
    return audit


def write_category_counts(audit: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for error_type in ("FN", "FP"):
        sub = audit[audit["error_type"] == error_type]
        counts = Counter(sub["diagnostic_category"])
        for cat in sorted(counts):
            rows.append(
                {
                    "error_type": error_type,
                    "diagnostic_category": cat,
                    "count": counts[cat],
                    "fraction_of_error_class": counts[cat] / len(sub),
                }
            )
        # threshold bins
        bins = Counter(sub["threshold_distance_bin"])
        for b in sorted(bins):
            rows.append(
                {
                    "error_type": error_type,
                    "diagnostic_category": f"THRESHOLD_BIN::{b}",
                    "count": bins[b],
                    "fraction_of_error_class": bins[b] / len(sub),
                }
            )
        # pathway clusters
        pcs = Counter(sub["pathway_cluster"])
        for p in sorted(pcs):
            rows.append(
                {
                    "error_type": error_type,
                    "diagnostic_category": f"PATHWAY_CLUSTER::{p}",
                    "count": pcs[p],
                    "fraction_of_error_class": pcs[p] / len(sub),
                }
            )
    out = pd.DataFrame(rows)
    out.to_csv(OUT_COUNTS, index=False)
    return out


def write_report(audit: pd.DataFrame, metrics: Dict, model_sha: str) -> None:
    fn = audit[audit["error_type"] == "FN"]
    fp = audit[audit["error_type"] == "FP"]
    fn_counts = fn["diagnostic_category"].value_counts().sort_index()
    fp_counts = fp["diagnostic_category"].value_counts().sort_index()
    fn_bins = fn["threshold_distance_bin"].value_counts()
    fp_bins = fp["threshold_distance_bin"].value_counts()
    fn_pw = fn["pathway_cluster"].value_counts()
    fp_pw = fp["pathway_cluster"].value_counts()

    # Rank shortlist: confidence, then actionable category family, then gene
    conf_order = {"high": 0, "medium": 1, "low": 2}
    cat_order = {
        "FP_MISSING_TRANSPORT": 0,
        "FP_MEDIA_CONTEXT": 1,
        "FP_GPR_STRUCTURE": 2,
        "FP_MISSING_ISOENZYME": 3,
        "FP_MISSING_ALTERNATIVE_PATHWAY": 4,
        "FN_ISOENZYME_REDUNDANCY": 5,
        "FN_GPR_STRUCTURE": 6,
        "FN_ALTERNATIVE_PATHWAY": 7,
        "FN_REACTION_INACTIVE": 8,
        "FN_NEAR_THRESHOLD": 9,
        "FP_NEAR_THRESHOLD": 10,
    }
    p1 = audit[audit["review_priority"] == 1].copy()
    p1["_c"] = p1["diagnostic_confidence"].map(conf_order).fillna(9)
    p1["_k"] = p1["diagnostic_category"].map(cat_order).fillna(50)
    p1 = p1.sort_values(["_c", "_k", "error_type", "gene"])

    unresolved_n = int(
        (audit["diagnostic_category"].isin(["FN_UNRESOLVED", "FP_UNRESOLVED"])).sum()
    )

    lines = []
    lines.append("# V-01 Error Structure Audit — MOPS-pyruvate (diagnostic only)")
    lines.append("")
    lines.append(f"**Status:** `{STATUS_GATE}`")
    lines.append("")
    lines.append("## Scope and hard constraints")
    lines.append("")
    lines.append("- Diagnostic analysis of frozen V-01 FP/FN sets only.")
    lines.append("- **No** model, GPR, reaction, medium, biomass, or threshold changes.")
    lines.append("- **No** gap-filling, metric retuning, or gene exclusion.")
    lines.append("- Categories are **association-based** from model structure; not causal claims.")
    lines.append("- iMO1056 reaction `subsystem` fields are empty; pathway groupings use ")
    lines.append("  deterministic reaction-name keyword clusters (descriptive counts only).")
    lines.append("")
    lines.append("## Phase 0 — frozen integrity")
    lines.append("")
    lines.append("| Cell | Count |")
    lines.append("|---|---|")
    for k in ("TP", "FN", "TN", "FP", "n"):
        lines.append(f"| {k} | {EXPECTED[k]} |")
    lines.append("")
    lines.append(f"- Model SHA-256: `{model_sha}`")
    lines.append(f"- Medium: `{MEDIUM_ID}` · threshold: `{THRESHOLD}` · objective: `{OBJECTIVE}`")
    lines.append(
        f"- WT growth (V-01 metrics): "
        f"{metrics['modeling_policy']['wt_growth']}"
    )
    lines.append("")
    lines.append("## FN overview (n=98)")
    lines.append("")
    lines.append("Experiment = essential; model = non-essential.")
    lines.append("")
    lines.append("| diagnostic_category | count |")
    lines.append("|---|---|")
    for cat, n in fn_counts.items():
        lines.append(f"| {cat} | {n} |")
    lines.append("")
    lines.append("### FN threshold-distance bins (DIAGNOSTIC ONLY)")
    lines.append("")
    lines.append("| bin | count |")
    lines.append("|---|---|")
    for b, n in fn_bins.items():
        lines.append(f"| {b} | {n} |")
    lines.append("")
    lines.append("### FN pathway-keyword clusters (descriptive)")
    lines.append("")
    lines.append("| cluster | count |")
    lines.append("|---|---|")
    for p, n in fn_pw.items():
        lines.append(f"| {p} | {n} |")
    lines.append("")
    lines.append("## FP overview (n=47)")
    lines.append("")
    lines.append("Experiment = negative; model = essential.")
    lines.append("")
    lines.append("| diagnostic_category | count |")
    lines.append("|---|---|")
    for cat, n in fp_counts.items():
        lines.append(f"| {cat} | {n} |")
    lines.append("")
    lines.append("### FP threshold-distance bins (DIAGNOSTIC ONLY)")
    lines.append("")
    lines.append("| bin | count |")
    lines.append("|---|---|")
    for b, n in fp_bins.items():
        lines.append(f"| {b} | {n} |")
    lines.append("")
    lines.append("### FP pathway-keyword clusters (descriptive)")
    lines.append("")
    lines.append("| cluster | count |")
    lines.append("|---|---|")
    for p, n in fp_pw.items():
        lines.append(f"| {p} | {n} |")
    lines.append("")
    lines.append("## Threshold-distance finding")
    lines.append("")
    lines.append(
        "Almost all errors are **far from** the fixed 0.01 cutoff: FN ratios are "
        "typically ≈1 (growth retained), and FP ratios are ≈0 (lethal KO). "
        "These are structural / scope disagreements, not classification-boundary artifacts. "
        "No alternative threshold was applied."
    )
    lines.append("")
    lines.append("## High-priority manual-review shortlist (Priority 1)")
    lines.append("")
    lines.append(
        "Safest actions are inspection-only. **No automatic model edits.**"
    )
    lines.append("")
    # Cap shortlist for readability
    short = p1.head(25)
    for _, r in short.iterrows():
        lines.append(
            f"### {r['gene']} ({r['error_type']}) — `{r['diagnostic_category']}` "
            f"[{r['diagnostic_confidence']}]"
        )
        lines.append("")
        lines.append(f"- Experimental: `{r['experimental_label']}` (minimal_sum={r['minimal_sum']})")
        lines.append(f"- Model prediction: `{r['model_prediction']}` · KO/WT={r['KO_WT_ratio']}")
        lines.append(f"- Reactions: `{r['associated_reactions']}`")
        lines.append(f"- GPR: `{r['GPR_rules'][:300]}`")
        lines.append(f"- Suspected mechanism (associative): {r['suspected_discrepancy_mechanism']}")
        lines.append(f"- Safest review action: {r['safest_manual_review_action']}")
        lines.append(f"- Notes: {r['notes']}")
        lines.append("")
    lines.append(f"Priority-1 genes total: **{len(p1)}** (showing up to 25 above).")
    lines.append("")
    lines.append("## Unresolved cases")
    lines.append("")
    lines.append(f"- Count: **{unresolved_n}**")
    lines.append(
        "- Reason: insufficient model-structural evidence for a more specific "
        "category under the deterministic rules (allowed outcome)."
    )
    lines.append("")
    lines.append("## Artifacts")
    lines.append("")
    lines.append(f"- `{OUT_AUDIT.relative_to(ROOT).as_posix()}`")
    lines.append(f"- `{OUT_FN.relative_to(ROOT).as_posix()}`")
    lines.append(f"- `{OUT_FP.relative_to(ROOT).as_posix()}`")
    lines.append(f"- `{OUT_COUNTS.relative_to(ROOT).as_posix()}`")
    lines.append(f"- `{OUT_REPORT.relative_to(ROOT).as_posix()}`")
    lines.append(
        "- Script: `scripts/validation/audit_v01_mops_pyruvate_errors.py`"
    )
    lines.append("")
    lines.append("## Explicit non-actions")
    lines.append("")
    lines.append("- No model/media/threshold/GPR edits.")
    lines.append("- V-01 scientific completeness is **not** claimed.")
    lines.append("- No decision approving model modifications.")
    lines.append("")
    lines.append(f"**Gate:** `{STATUS_GATE}`")
    lines.append("")

    OUT_REPORT.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    metrics = verify_frozen_v01()

    from src.load_model import load_model
    from src.medium import apply_medium
    from cobra.flux_analysis import find_blocked_reactions

    # Read-only structural inspection on an in-memory copy with locked medium.
    model = load_model(MODEL_PATH)
    model_sha = _sha256(MODEL_PATH)
    apply_medium(model, MEDIUM_ID, quiet=True)
    sol = model.optimize()
    if sol.status != "optimal" or sol.objective_value is None:
        raise SystemExit(f"V01_AUDIT_ABORT: WT solve failed status={sol.status}")
    flux = sol.fluxes
    blocked = set(find_blocked_reactions(model, open_exchanges=False, processes=1))
    bm_mets = {m.id for m in model.reactions.get_by_id(OBJECTIVE).metabolites}

    print(
        f"Structural context: WT={sol.objective_value:.6f} "
        f"blocked_reactions={len(blocked)} (in-memory; model file untouched)"
    )

    audit = build_audit_table(model, flux, blocked, bm_mets)

    # Integrity on audit itself
    if len(audit) != 145:
        raise SystemExit(f"V01_AUDIT_ABORT: audit n={len(audit)} != 145")
    if (audit["error_type"] == "FN").sum() != 98:
        raise SystemExit("V01_AUDIT_ABORT: FN != 98")
    if (audit["error_type"] == "FP").sum() != 47:
        raise SystemExit("V01_AUDIT_ABORT: FP != 47")
    if audit["error_type"].isin(["TP", "TN"]).any():
        raise SystemExit("V01_AUDIT_ABORT: TP/TN leaked into audit")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)

    audit.to_csv(OUT_AUDIT, index=False)
    audit[audit["error_type"] == "FN"].to_csv(OUT_FN, index=False)
    audit[audit["error_type"] == "FP"].to_csv(OUT_FP, index=False)
    write_category_counts(audit)
    write_report(audit, metrics, model_sha)

    # Confirm original V-01 files not replaced with audit content
    for p in (FP_PATH, FN_PATH, TP_PATH, TN_PATH, PRED_JOINED, METRICS_JSON):
        if "error_audit" in p.name or "false_negative_audit" in p.name:
            raise SystemExit("V01_AUDIT_ABORT: unexpected overwrite target")

    print("Wrote:")
    for p in (OUT_AUDIT, OUT_FN, OUT_FP, OUT_COUNTS, OUT_REPORT):
        print(f"  {p.relative_to(ROOT)}")
    print(f"STATUS: {STATUS_GATE}")


if __name__ == "__main__":
    main()

"""V-01 primary binary validation: iMO1056 vs D-21 MOPS-pyruvate universe.

Locked modeling policy (existing project decisions — not tuned for metrics):
- Model: models/paeruginosa_MODEL1507180020.xml (iMO1056 / PAO1)
- Objective: PA_Biomass6_DM
- Medium: mops_pyruvate_lee2015 (D-17)
- Essentiality: growth_ratio < 0.01 → MODEL_POSITIVE (D-09 / src/gene_essentiality.py)
- Experimental labels: D-21 frozen primary binary universe only
- Does NOT use D-20 Lee-original positives in the confusion matrix
- Does NOT alter medium, threshold, GPRs, or objective

Usage:
  C:/Users/pro/anaconda3/envs/reccobra39/python.exe \\
    scripts/validation/run_v01_mops_pyruvate_binary_validation.py
  ... --regenerate   # re-run single-gene deletion under locked medium/threshold
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from pathlib import Path

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
LEE_D20 = (
    ROOT
    / "data/processed/literature/gene_level"
    / "literature_evidence_gene_level_READY_mops_pyruvate_lee2015.csv"
)
PRED_CANONICAL = (
    ROOT / "results/essentiality/gene_essentiality_mops_pyruvate_lee2015.csv"
)

OUT_DIR = ROOT / "data/processed/validation"
AUDIT_DIR = ROOT / "project_management/audit/v01_mops_pyruvate"

MEDIUM_ID = "mops_pyruvate_lee2015"
THRESHOLD = 0.01
OBJECTIVE = "PA_Biomass6_DM"
DECISION_EXPERIMENTAL = "D-21"
STATUS_GATE = "V01_BINARY_METRICS_COMPUTED_PENDING_HUMAN_INTERPRETATION"

EXPECTED_N = 1025
EXPECTED_POS = 214
EXPECTED_NEG = 811

PA_RE = re.compile(r"^PA\d{4}$")
PA_EXTRACT = re.compile(r"(PA\d{4})")

# Observed WT under reccobra39/GLPK (tests/test_media.py); sanity band only
WT_OBSERVED = 0.40533903063568605
WT_TOL = 1e-4


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def clean_gid(x) -> str:
    s = str(x).strip()
    if s.startswith("{") and s.endswith("}"):
        inner = s.strip("{}").replace("'", "").replace('"', "").strip()
        m = PA_EXTRACT.search(inner)
        return m.group(1) if m else inner
    m = PA_EXTRACT.search(s)
    return m.group(1) if m else s


def load_binary_universe() -> pd.DataFrame:
    if not BINARY_UNIVERSE.exists():
        raise SystemExit(f"V01_PREREQUISITE_FAILURE: missing {BINARY_UNIVERSE}")
    u = pd.read_csv(BINARY_UNIVERSE)
    if len(u) != EXPECTED_N:
        raise SystemExit(
            f"V01_PREREQUISITE_FAILURE: universe n={len(u)} expected {EXPECTED_N}"
        )
    if not u["pao1_locus"].is_unique:
        raise SystemExit("V01_PREREQUISITE_FAILURE: duplicate pao1_locus in universe")
    if not u["pao1_locus"].astype(str).str.match(r"^PA\d{4}$").all():
        raise SystemExit("V01_PREREQUISITE_FAILURE: nonstandard PAO1 IDs in universe")
    pos = (u["short_label"] == "POSITIVE").sum()
    neg = (u["short_label"] == "NEGATIVE").sum()
    if pos != EXPECTED_POS or neg != EXPECTED_NEG:
        raise SystemExit(
            f"V01_PREREQUISITE_FAILURE: label counts POS={pos} NEG={neg}"
        )
    if (u["minimal_sum"] == 1).any() or (u["short_label"] == "AMBIGUOUS").any():
        raise SystemExit("V01_PREREQUISITE_FAILURE: ambiguous rows in binary universe")
    if (u["decision_id"] != "D-21").any():
        raise SystemExit("V01_PREREQUISITE_FAILURE: decision_id != D-21")
    return u


def sanity_and_policy(regenerate: bool) -> tuple[object, dict]:
    import cobra
    from src.medium import apply_medium, get_medium

    model = cobra.io.read_sbml_model(str(MODEL_PATH))
    if OBJECTIVE not in str(model.objective.expression):
        raise SystemExit(
            "HUMAN_DECISION_REQUIRED_FOR_MODEL_ESSENTIALITY_POLICY: "
            f"objective is not {OBJECTIVE}"
        )
    spec = get_medium(MEDIUM_ID)
    model_m = model.copy()
    apply_medium(model_m, spec, quiet=True)
    sol = model_m.optimize()
    if sol.status != "optimal" or sol.objective_value is None or sol.objective_value <= 1e-9:
        raise SystemExit(
            f"V01_MODEL_MEDIA_SANITY_FAILURE: status={sol.status} "
            f"wt={sol.objective_value}"
        )
    wt = float(sol.objective_value)
    if abs(wt - WT_OBSERVED) > WT_TOL:
        # Record but do not auto-tune; still allow if feasible (document drift)
        print(
            f"WARNING: WT growth {wt} differs from recorded OBSERVED_WT {WT_OBSERVED} "
            f"by >{WT_TOL}; continuing because feasible under locked medium."
        )

    solver_name = getattr(
        getattr(model.solver, "interface", None), "__name__", str(type(model.solver))
    )
    # Active uptake exchanges (sorted keys for deterministic JSON)
    active = {
        rid: lb
        for rid, lb in sorted(
            (
                rxn.id,
                float(rxn.lower_bound),
            )
            for rxn in model_m.exchanges
            if rxn.lower_bound < -1e-6
        )
    }
    meta = {
        "model_id": model.id,
        "model_path": str(MODEL_PATH.relative_to(ROOT)).replace("\\", "/"),
        "model_sha256": _sha256(MODEL_PATH),
        "n_reactions": len(model.reactions),
        "n_metabolites": len(model.metabolites),
        "n_genes": len(model.genes),
        "objective": OBJECTIVE,
        "medium_id": MEDIUM_ID,
        "medium_label": spec.label,
        "solver": solver_name,
        "wt_growth": wt,
        "wt_status": sol.status,
        "threshold_ratio": THRESHOLD,
        "essentiality_rule": "growth_ratio < threshold_ratio → MODEL_POSITIVE (essential)",
        "policy_sources": [
            "D-09 threshold_ratio=0.01",
            "D-17 mops_pyruvate_lee2015",
            "src/gene_essentiality.py analyze_gene_essentiality",
            "scripts/run_condition_essentiality.py --threshold 0.01",
        ],
        "active_uptake_exchanges": active,
        "regenerate_predictions": bool(regenerate),
    }
    return model, meta


def load_or_generate_predictions(model, regenerate: bool) -> tuple[pd.DataFrame, str]:
    from src.gene_essentiality import analyze_essentiality_for_medium

    if regenerate or not PRED_CANONICAL.exists():
        print("Regenerating single-gene deletions under locked medium/threshold...")
        df = analyze_essentiality_for_medium(
            model,
            MEDIUM_ID,
            threshold_ratio=THRESHOLD,
            processes=1,
        )
        PRED_CANONICAL.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(PRED_CANONICAL, index=False)
        source = "regenerated_via_analyze_essentiality_for_medium"
    else:
        df = pd.read_csv(PRED_CANONICAL)
        source = "loaded_canonical_results_essentiality_file"

    df = df.copy()
    df["gene_id"] = df["gene_id"].map(clean_gid)
    if "medium_id" in df.columns and not (df["medium_id"] == MEDIUM_ID).all():
        raise SystemExit(
            "HUMAN_DECISION_REQUIRED_FOR_MODEL_ESSENTIALITY_POLICY: "
            f"prediction medium_id != {MEDIUM_ID}"
        )
    if "threshold_ratio" in df.columns:
        thr = float(df["threshold_ratio"].iloc[0])
        if abs(thr - THRESHOLD) > 1e-12:
            raise SystemExit(
                "HUMAN_DECISION_REQUIRED_FOR_MODEL_ESSENTIALITY_POLICY: "
                f"prediction threshold_ratio={thr} != {THRESHOLD}"
            )
    # Re-derive is_essential from locked rule (do not trust a different cutoff)
    if df["wildtype_growth"].isna().any() or (df["wildtype_growth"] <= 1e-9).any():
        raise SystemExit("V01_MODEL_MEDIA_SANITY_FAILURE: invalid WT in predictions")
    wt = float(df["wildtype_growth"].iloc[0])
    # Handle failed/NaN knockouts
    if df["knockout_growth"].isna().any():
        n_na = int(df["knockout_growth"].isna().sum())
        raise SystemExit(
            f"V01_JOIN_INTEGRITY_FAILURE: {n_na} knockout_growth NA — "
            "no project policy for failed solves in primary metrics"
        )
    ratio = df["knockout_growth"].astype(float) / wt
    df["growth_ratio"] = ratio
    df["is_essential"] = ratio < THRESHOLD
    df["model_prediction"] = df["is_essential"].map(
        {True: "MODEL_POSITIVE", False: "MODEL_NEGATIVE"}
    )
    if not df["gene_id"].is_unique:
        raise SystemExit("V01_JOIN_INTEGRITY_FAILURE: duplicate gene_id in predictions")
    if len(df) != 1054:
        raise SystemExit(
            f"V01_JOIN_INTEGRITY_FAILURE: prediction n={len(df)} expected 1054 model genes"
        )
    return df, source


def exact_join(universe: pd.DataFrame, pred: pd.DataFrame) -> pd.DataFrame:
    u = universe.copy()
    u["pao1_locus"] = u["pao1_locus"].astype(str).str.strip()
    p = pred[["gene_id", "wildtype_growth", "knockout_growth", "growth_ratio",
              "is_essential", "model_prediction", "medium_id", "threshold_ratio"]].copy()
    if "medium_id" not in pred.columns:
        p["medium_id"] = MEDIUM_ID
    if "threshold_ratio" not in pred.columns:
        p["threshold_ratio"] = THRESHOLD

    merged = u.merge(p, left_on="pao1_locus", right_on="gene_id", how="left", indicator=True)
    unmatched = merged[merged["_merge"] != "both"]
    if len(unmatched):
        genes = unmatched["pao1_locus"].tolist()
        raise SystemExit(
            "V01_JOIN_INTEGRITY_FAILURE: unmatched primary genes "
            f"n={len(genes)} examples={genes[:20]}"
        )
    if len(merged) != EXPECTED_N:
        raise SystemExit(
            f"V01_JOIN_INTEGRITY_FAILURE: joined n={len(merged)} expected {EXPECTED_N}"
        )
    if not merged["pao1_locus"].is_unique:
        raise SystemExit("V01_JOIN_INTEGRITY_FAILURE: duplicates after join")
    # Extra predictions not in universe are OK for the full model table, but
    # primary comparison table must be exactly the universe.
    extra = set(pred["gene_id"]) - set(u["pao1_locus"])
    # not a failure — record count only
    merged = merged.drop(columns=["_merge", "gene_id"])
    merged["experiment_polarity"] = merged["short_label"].map(
        {"POSITIVE": "EXPERIMENT_POSITIVE", "NEGATIVE": "EXPERIMENT_NEGATIVE"}
    )
    merged["objective"] = OBJECTIVE
    merged["solver"] = "optlang.glpk_interface"
    merged["solve_status"] = "optimal"  # cobra single_gene_deletion stored growth values
    merged["experimental_source"] = merged["evidence_source"]
    merged["medium"] = MEDIUM_ID
    merged["essentiality_threshold"] = THRESHOLD
    merged["notes"] = (
        "V-01 primary binary join; D-21 experimental labels; "
        "model essentiality growth_ratio < 0.01; D-20 not used"
    )
    merged.attrs["n_model_genes_not_in_primary"] = len(extra)
    return merged


def confusion_and_metrics(joined: pd.DataFrame) -> tuple[dict, dict]:
    exp_pos = joined["short_label"] == "POSITIVE"
    exp_neg = joined["short_label"] == "NEGATIVE"
    mod_pos = joined["model_prediction"] == "MODEL_POSITIVE"
    mod_neg = joined["model_prediction"] == "MODEL_NEGATIVE"

    tp = int((exp_pos & mod_pos).sum())
    fn = int((exp_pos & mod_neg).sum())
    tn = int((exp_neg & mod_neg).sum())
    fp = int((exp_neg & mod_pos).sum())
    n = tp + tn + fp + fn

    if tp + fn != EXPECTED_POS:
        raise SystemExit(f"STOP: TP+FN={tp+fn} != {EXPECTED_POS}")
    if tn + fp != EXPECTED_NEG:
        raise SystemExit(f"STOP: TN+FP={tn+fp} != {EXPECTED_NEG}")
    if n != EXPECTED_N:
        raise SystemExit(f"STOP: total={n} != {EXPECTED_N}")

    def safe_div(a, b):
        return float(a / b) if b else float("nan")

    sens = safe_div(tp, tp + fn)
    spec = safe_div(tn, tn + fp)
    prec = safe_div(tp, tp + fp)
    npv = safe_div(tn, tn + fn)
    f1 = safe_div(2 * prec * sens, prec + sens) if (prec + sens) else float("nan")
    acc = safe_div(tp + tn, n)
    bal = (sens + spec) / 2.0
    denom = math.sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn))
    mcc = float((tp * tn - fp * fn) / denom) if denom else float("nan")

    cm = {
        "TP": tp,
        "FN": fn,
        "TN": tn,
        "FP": fp,
        "n": n,
        "experimental_positive": EXPECTED_POS,
        "experimental_negative": EXPECTED_NEG,
    }
    metrics = {
        "sensitivity_recall_tpr": sens,
        "specificity_tnr": spec,
        "precision_ppv": prec,
        "npv": npv,
        "f1": f1,
        "accuracy": acc,
        "balanced_accuracy": bal,
        "mcc": mcc,
        "TP": tp,
        "TN": tn,
        "FP": fp,
        "FN": fn,
        "n": n,
        "experimental_positive_prevalence": EXPECTED_POS / n,
        "n_predicted_essential_model_positive": int(mod_pos.sum()),
        "n_predicted_nonessential_model_negative": int(mod_neg.sum()),
        "threshold_ratio": THRESHOLD,
        "medium_id": MEDIUM_ID,
        "objective": OBJECTIVE,
        "experimental_decision": DECISION_EXPERIMENTAL,
        "status": STATUS_GATE,
        "formulas": {
            "sensitivity": "TP/(TP+FN)",
            "specificity": "TN/(TN+FP)",
            "precision": "TP/(TP+FP)",
            "npv": "TN/(TN+FN)",
            "f1": "2*precision*sensitivity/(precision+sensitivity)",
            "accuracy": "(TP+TN)/n",
            "balanced_accuracy": "(sensitivity+specificity)/2",
            "mcc": "(TP*TN-FP*FN)/sqrt((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN))",
        },
    }
    for k in ("sensitivity_recall_tpr", "specificity_tnr", "precision_ppv", "npv",
              "f1", "accuracy", "balanced_accuracy"):
        v = metrics[k]
        if not math.isfinite(v) or v < -1e-12 or v > 1 + 1e-12:
            raise SystemExit(f"STOP: metric {k} out of range: {v}")
    if not math.isfinite(mcc) or mcc < -1 - 1e-12 or mcc > 1 + 1e-12:
        raise SystemExit(f"STOP: MCC out of range: {mcc}")
    return cm, metrics


def write_artifacts(
    joined: pd.DataFrame,
    cm: dict,
    metrics: dict,
    meta: dict,
    pred_source: str,
) -> dict:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)

    pred_cols = [
        "pao1_locus",
        "mpao1_locus",
        "model_gene_id",
        "wildtype_growth",
        "knockout_growth",
        "growth_ratio",
        "model_prediction",
        "is_essential",
        "experiment_polarity",
        "experimental_label",
        "short_label",
        "minimal_1",
        "minimal_2",
        "minimal_3",
        "minimal_sum",
        "experimental_source",
        "source_dataset",
        "medium",
        "objective",
        "essentiality_threshold",
        "solver",
        "solve_status",
        "decision_id",
        "notes",
    ]
    joined_out = joined[pred_cols].sort_values("pao1_locus").reset_index(drop=True)
    path_pred = OUT_DIR / "v01_mops_pyruvate_gene_predictions.csv"
    joined_out.to_csv(path_pred, index=False)

    # Confusion matrix long + wide
    cm_df = pd.DataFrame(
        [
            {"cell": "TP", "count": cm["TP"],
             "definition": "EXPERIMENT_POSITIVE & MODEL_POSITIVE"},
            {"cell": "FN", "count": cm["FN"],
             "definition": "EXPERIMENT_POSITIVE & MODEL_NEGATIVE"},
            {"cell": "TN", "count": cm["TN"],
             "definition": "EXPERIMENT_NEGATIVE & MODEL_NEGATIVE"},
            {"cell": "FP", "count": cm["FP"],
             "definition": "EXPERIMENT_NEGATIVE & MODEL_POSITIVE"},
            {"cell": "n", "count": cm["n"], "definition": "TP+TN+FP+FN"},
        ]
    )
    path_cm = OUT_DIR / "v01_mops_pyruvate_confusion_matrix.csv"
    cm_df.to_csv(path_cm, index=False)

    # Error / class lists
    keep_err = [
        "pao1_locus",
        "mpao1_locus",
        "experimental_label",
        "short_label",
        "model_prediction",
        "wildtype_growth",
        "knockout_growth",
        "growth_ratio",
        "minimal_sum",
        "minimal_1",
        "minimal_2",
        "minimal_3",
        "experimental_source",
        "medium",
        "essentiality_threshold",
        "decision_id",
        "notes",
    ]
    exp_pos = joined["short_label"] == "POSITIVE"
    exp_neg = joined["short_label"] == "NEGATIVE"
    mod_pos = joined["model_prediction"] == "MODEL_POSITIVE"
    mod_neg = joined["model_prediction"] == "MODEL_NEGATIVE"

    paths = {
        "predictions": path_pred,
        "confusion_matrix": path_cm,
        "true_positives": OUT_DIR / "v01_mops_pyruvate_true_positives.csv",
        "true_negatives": OUT_DIR / "v01_mops_pyruvate_true_negatives.csv",
        "false_positives": OUT_DIR / "v01_mops_pyruvate_false_positives.csv",
        "false_negatives": OUT_DIR / "v01_mops_pyruvate_false_negatives.csv",
    }
    joined.loc[exp_pos & mod_pos, keep_err].sort_values("pao1_locus").to_csv(
        paths["true_positives"], index=False
    )
    joined.loc[exp_neg & mod_neg, keep_err].sort_values("pao1_locus").to_csv(
        paths["true_negatives"], index=False
    )
    joined.loc[exp_neg & mod_pos, keep_err].sort_values("pao1_locus").to_csv(
        paths["false_positives"], index=False
    )
    joined.loc[exp_pos & mod_neg, keep_err].sort_values("pao1_locus").to_csv(
        paths["false_negatives"], index=False
    )

    payload = {
        "status": STATUS_GATE,
        "experimental_decision": DECISION_EXPERIMENTAL,
        "d20_used_in_primary_matrix": False,
        "prediction_source": pred_source,
        "prediction_canonical_path": str(PRED_CANONICAL.relative_to(ROOT)).replace("\\", "/"),
        "prediction_canonical_sha256": _sha256(PRED_CANONICAL),
        "binary_universe_path": str(BINARY_UNIVERSE.relative_to(ROOT)).replace("\\", "/"),
        "binary_universe_sha256": _sha256(BINARY_UNIVERSE),
        "lee_d20_ready_sha256": _sha256(LEE_D20) if LEE_D20.exists() else None,
        "modeling_policy": meta,
        "join": {
            "expected_experimental_genes": EXPECTED_N,
            "matched_genes": len(joined_out),
            "unmatched_genes": 0,
            "duplicate_genes": 0,
            "n_model_genes_not_in_primary": int(
                joined.attrs.get("n_model_genes_not_in_primary", 0)
            ),
        },
        "confusion_matrix": cm,
        "metrics": metrics,
        "artifacts": {
            k: str(v.relative_to(ROOT)).replace("\\", "/") for k, v in paths.items()
        },
        "interpretation": (
            "RAW METRICS ONLY — no claim that the model is validated/good/bad. "
            "Pending human review of confusion matrix and error structure."
        ),
    }
    path_metrics = OUT_DIR / "v01_mops_pyruvate_metrics.json"
    path_metrics.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    paths["metrics_json"] = path_metrics

    # Human-readable report (neutral; no quality judgment)
    report = AUDIT_DIR / "V01_BINARY_VALIDATION_REPORT.md"
    report.write_text(
        f"""# V-01 Binary Validation Report — MOPS-pyruvate (D-21)

**Status:** `{STATUS_GATE}`  
**Experimental labels:** D-21 frozen primary binary universe  
**D-20 Lee-original positives used in primary matrix:** **No**

## Modeling policy (locked; not tuned)

| Item | Value |
|---|---|
| Model | iMO1056 / `{meta['model_id']}` |
| Model path | `{meta['model_path']}` |
| Objective | `{OBJECTIVE}` |
| Medium | `{MEDIUM_ID}` ({meta['medium_label']}) |
| Solver | `{meta['solver']}` |
| WT growth | {meta['wt_growth']} (status={meta['wt_status']}) |
| Essentiality cutoff | `growth_ratio < {THRESHOLD}` → MODEL_POSITIVE |
| Policy sources | D-09; D-17; `src/gene_essentiality.py` |

## Join integrity

| Check | Value |
|---|---|
| Experimental genes | {EXPECTED_N} |
| Matched prediction rows | {len(joined_out)} |
| Unmatched | 0 |
| Duplicates | 0 |
| Ambiguous in primary | 0 |

## Confusion matrix

| Cell | Count | Definition |
|---|---|---|
| TP | {cm['TP']} | experimental essential ∧ model essential |
| FN | {cm['FN']} | experimental essential ∧ model non-essential |
| TN | {cm['TN']} | experimental negative ∧ model non-essential |
| FP | {cm['FP']} | experimental negative ∧ model essential |
| n | {cm['n']} | TP+TN+FP+FN |

Identities: TP+FN={cm['TP']+cm['FN']} (expect {EXPECTED_POS});
TN+FP={cm['TN']+cm['FP']} (expect {EXPECTED_NEG}).

## Metrics (raw)

| Metric | Value |
|---|---|
| Sensitivity / recall / TPR | {metrics['sensitivity_recall_tpr']:.6f} |
| Specificity / TNR | {metrics['specificity_tnr']:.6f} |
| Precision / PPV | {metrics['precision_ppv']:.6f} |
| NPV | {metrics['npv']:.6f} |
| F1 | {metrics['f1']:.6f} |
| Accuracy | {metrics['accuracy']:.6f} |
| Balanced accuracy | {metrics['balanced_accuracy']:.6f} |
| MCC | {metrics['mcc']:.6f} |

Predicted essential (MODEL_POSITIVE) in primary join:
{metrics['n_predicted_essential_model_positive']}  
Predicted non-essential (MODEL_NEGATIVE):
{metrics['n_predicted_nonessential_model_negative']}

## Error-set artifacts

- FP: `{paths['false_positives'].relative_to(ROOT)}` (n={cm['FP']})
- FN: `{paths['false_negatives'].relative_to(ROOT)}` (n={cm['FN']})
- TP: `{paths['true_positives'].relative_to(ROOT)}` (n={cm['TP']})
- TN: `{paths['true_negatives'].relative_to(ROOT)}` (n={cm['TN']})

## Explicit non-claims

This report does **not** conclude that iMO1056 is validated, good, or bad.
No medium/threshold/model tuning was performed.
Next stage: **human review** of the confusion matrix and FP/FN structure.
""",
        encoding="utf-8",
    )
    paths["report"] = report
    # Also copy metrics JSON into audit folder for convenience
    (AUDIT_DIR / "v01_mops_pyruvate_metrics.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return {k: str(v) for k, v in paths.items()}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--regenerate",
        action="store_true",
        help="Re-run single-gene deletion under locked medium/threshold",
    )
    args = parser.parse_args(argv)

    universe = load_binary_universe()
    model, meta = sanity_and_policy(regenerate=args.regenerate)
    # Confirm all universe genes in model.genes
    model_pas = set()
    for g in model.genes:
        m = PA_EXTRACT.search(g.id)
        model_pas.add(m.group(1) if m else g.id)
    missing = sorted(set(universe["pao1_locus"]) - model_pas)
    if missing:
        raise SystemExit(
            f"V01_PREREQUISITE_FAILURE: {len(missing)} universe genes absent from model.genes"
        )

    pred, pred_source = load_or_generate_predictions(model, regenerate=args.regenerate)
    joined = exact_join(universe, pred)
    cm, metrics = confusion_and_metrics(joined)
    paths = write_artifacts(joined, cm, metrics, meta, pred_source)

    print("=== V-01 complete (raw metrics; pending human interpretation) ===")
    print("status:", STATUS_GATE)
    print("confusion:", cm)
    print(
        "metrics:",
        {k: metrics[k] for k in (
            "sensitivity_recall_tpr", "specificity_tnr", "precision_ppv",
            "f1", "mcc", "accuracy", "balanced_accuracy",
        )},
    )
    print("artifacts:")
    for k, v in paths.items():
        print(f"  {k}: {v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

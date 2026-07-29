"""Positive-label overlap only for Lee2015 MOPS-pyruvate vs iMO1056 predictions.

Policy: NO precision/recall/specificity/F1/MCC/full confusion matrix.
Experimental non-essential universe is undefined (D-20 / human review 2026-07-29).
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
READY = (
    ROOT
    / "data"
    / "processed"
    / "literature"
    / "gene_level"
    / "literature_evidence_gene_level_READY_mops_pyruvate_lee2015.csv"
)
PRED = (
    ROOT
    / "results"
    / "essentiality"
    / "gene_essentiality_mops_pyruvate_lee2015.csv"
)
OUT_DIR = ROOT / "results" / "comparison"
OUT_SUMMARY = OUT_DIR / "lee2015_mops_pyruvate_POSITIVE_OVERLAP_ONLY_summary.csv"
OUT_OVERLAP = OUT_DIR / "lee2015_mops_pyruvate_POSITIVE_OVERLAP_ONLY_recovered.csv"
OUT_MISSED = OUT_DIR / "lee2015_mops_pyruvate_POSITIVE_OVERLAP_ONLY_not_recovered.csv"
OUT_PRED_NOT_IN_POS = (
    OUT_DIR / "lee2015_mops_pyruvate_POSITIVE_OVERLAP_ONLY_predicted_not_in_positive_labels.csv"
)
OUT_ABSENT = OUT_DIR / "lee2015_mops_pyruvate_POSITIVE_OVERLAP_ONLY_labels_absent_from_model.csv"
OUT_REPORT = OUT_DIR / "lee2015_mops_pyruvate_POSITIVE_OVERLAP_ONLY_REPORT.md"


def clean_gid(x) -> str:
    s = str(x).strip()
    if s.startswith("{") and s.endswith("}"):
        return s.strip("{}").replace("'", "").replace('"', "").strip()
    return s


def main() -> None:
    if not READY.exists():
        raise FileNotFoundError(READY)
    if not PRED.exists():
        raise FileNotFoundError(
            f"Missing {PRED}; regenerate with scripts/run_condition_essentiality.py "
            "--medium mops_pyruvate_lee2015 --threshold 0.01 --processes 1"
        )

    labels = pd.read_csv(READY)
    pred = pd.read_csv(PRED)
    pred["gene_id"] = pred["gene_id"].map(clean_gid)

    assert len(labels) == 437
    label_ids = set(labels["mapped_pao1_gene_id"].astype(str).str.strip())
    model_ids = set(pred["gene_id"])
    if pred["is_essential"].dtype == object:
        ess_mask = pred["is_essential"].astype(str).str.lower().eq("true")
    else:
        ess_mask = pred["is_essential"].astype(bool)
    pred_ess = set(pred.loc[ess_mask, "gene_id"])
    thr = float(pred["threshold_ratio"].iloc[0])
    wt = float(pred["wildtype_growth"].iloc[0])

    in_model = sorted(label_ids & model_ids)
    absent = sorted(label_ids - model_ids)
    recovered = sorted(set(in_model) & pred_ess)
    not_recovered = sorted(set(in_model) - pred_ess)
    pred_not_in_pos = sorted(pred_ess - label_ids)

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    summary = pd.DataFrame(
        [
            {"metric": "n_positive_labels", "value": len(label_ids)},
            {"metric": "n_in_model", "value": len(in_model)},
            {"metric": "n_absent_from_model", "value": len(absent)},
            {"metric": "n_predicted_essential_at_0.01", "value": len(pred_ess)},
            {"metric": "n_positive_recovered_by_model", "value": len(recovered)},
            {"metric": "n_positive_in_model_not_recovered", "value": len(not_recovered)},
            {
                "metric": "n_predicted_essential_not_in_positive_label_set",
                "value": len(pred_not_in_pos),
            },
            {"metric": "threshold_ratio", "value": thr},
            {"metric": "wildtype_growth_per_h", "value": wt},
            {"metric": "n_model_genes", "value": len(model_ids)},
        ]
    )
    summary.to_csv(OUT_SUMMARY, index=False)

    pd.DataFrame({"mapped_pao1_gene_id": recovered}).to_csv(OUT_OVERLAP, index=False)
    pd.DataFrame(
        {
            "mapped_pao1_gene_id": not_recovered,
            "label": "positive_not_recovered",
            "note": "in-model positive label; model growth ratio >= 0.01 (not a full FN metric)",
        }
    ).to_csv(OUT_MISSED, index=False)
    pd.DataFrame(
        {
            "gene_id": pred_not_in_pos,
            "note": (
                "predicted essential but not in Lee MOPS-pyruvate positive label set; "
                "NOT called false-positive — experimental negatives undefined"
            ),
        }
    ).to_csv(OUT_PRED_NOT_IN_POS, index=False)
    pd.DataFrame(
        {
            "mapped_pao1_gene_id": absent,
            "classification": "absent_from_model",
        }
    ).to_csv(OUT_ABSENT, index=False)

    report = f"""# Lee2015 MOPS-pyruvate — POSITIVE OVERLAP ONLY

**Date:** 2026-07-29  
**Labels:** `{READY.relative_to(ROOT).as_posix()}` (READY; 437 positives)  
**Predictions:** `{PRED.relative_to(ROOT).as_posix()}`  
**Medium:** `mops_pyruvate_lee2015` · **threshold_ratio:** {thr} · **WT growth:** {wt} /h  
**Decision:** D-20 / human review 2026-07-29 APPROVED_FOR_PROMOTION (positives only)

## Policy (explicit)

**Precision, recall, specificity, F1, MCC, accuracy, and a full confusion matrix
are NOT computed** — experimental NON-essential universe is undefined. Absence
from the Lee MOPS-pyruvate essential list must not be treated as experimental
non-essentiality. Predicted essentials outside the positive label set are
**not** called false positives.

Allowed here: positive-label coverage + overlap with model predictions only.

## Counts (measured)

| Metric | Value |
|---|---|
| n_positive_labels | **{len(label_ids)}** |
| n_in_model | **{len(in_model)}** |
| n_absent_from_model | **{len(absent)}** |
| n_predicted_essential @0.01 | **{len(pred_ess)}** |
| labels AND predicted essential (recovered) | **{len(recovered)}** |
| in-model positives not recovered | **{len(not_recovered)}** |
| predicted essential not in positive label set | **{len(pred_not_in_pos)}** (not FP) |

## Outputs

- `{OUT_SUMMARY.relative_to(ROOT).as_posix()}`
- `{OUT_OVERLAP.relative_to(ROOT).as_posix()}`
- `{OUT_MISSED.relative_to(ROOT).as_posix()}`
- `{OUT_PRED_NOT_IN_POS.relative_to(ROOT).as_posix()}`
- `{OUT_ABSENT.relative_to(ROOT).as_posix()}`

## Next human decision (proposed; not implemented)

Define a defensible experimental **negative universe** for MOPS-pyruvate before
any full V-01 confusion-matrix metrics are allowed.
"""
    OUT_REPORT.write_text(report, encoding="utf-8")

    print(report.encode("ascii", errors="replace").decode("ascii"))
    print("Wrote outputs under", OUT_DIR)


if __name__ == "__main__":
    main()

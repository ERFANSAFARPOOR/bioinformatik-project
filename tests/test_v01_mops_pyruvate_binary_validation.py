"""Integrity tests for V-01 D-21 MOPS-pyruvate primary binary metrics.

Does not tune media/threshold. Does not interpret model quality.
"""
from __future__ import annotations

import hashlib
import json
import math
import subprocess
import sys
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
BINARY = (
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
OUT = ROOT / "data/processed/validation"
METRICS = OUT / "v01_mops_pyruvate_metrics.json"
JOINED = OUT / "v01_mops_pyruvate_gene_predictions.csv"
CM = OUT / "v01_mops_pyruvate_confusion_matrix.csv"
FP = OUT / "v01_mops_pyruvate_false_positives.csv"
FN = OUT / "v01_mops_pyruvate_false_negatives.csv"
TP = OUT / "v01_mops_pyruvate_true_positives.csv"
TN = OUT / "v01_mops_pyruvate_true_negatives.csv"
SCRIPT = ROOT / "scripts/validation/run_v01_mops_pyruvate_binary_validation.py"

BINARY_SHA = "e3174cb0975cd39c210ebfb86e26f87a3a2e5904664f7d8c5c6663fe93a5649e"
LEE_D20_SHA = "578b9a29583d4e8580996908ec9b1a6d0f9410125cecc2d6a7d9c0dfbb2929a3"


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


@pytest.fixture(scope="module")
def metrics() -> dict:
    assert METRICS.exists(), "run V-01 script first"
    return json.loads(METRICS.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def joined() -> pd.DataFrame:
    assert JOINED.exists()
    return pd.read_csv(JOINED)


def test_frozen_universe_counts():
    u = pd.read_csv(BINARY)
    assert len(u) == 1025
    assert u["pao1_locus"].is_unique
    assert int((u["short_label"] == "POSITIVE").sum()) == 214
    assert int((u["short_label"] == "NEGATIVE").sum()) == 811
    assert (u["minimal_sum"] != 1).all()


def test_d20_d21_inputs_unchanged():
    assert _sha(BINARY) == BINARY_SHA
    assert _sha(LEE_D20) == LEE_D20_SHA
    lee = pd.read_csv(LEE_D20)
    assert len(lee) == 437


def test_join_exact_1025(joined):
    assert len(joined) == 1025
    assert joined["pao1_locus"].is_unique
    assert (joined["decision_id"] == "D-21").all()
    assert (joined["experimental_label"] != "AMBIGUOUS_1_OF_3").all()
    assert set(joined["model_prediction"]) <= {"MODEL_POSITIVE", "MODEL_NEGATIVE"}


def test_confusion_identities(metrics):
    cm = metrics["confusion_matrix"]
    assert cm["TP"] + cm["FN"] == 214
    assert cm["TN"] + cm["FP"] == 811
    assert cm["TP"] + cm["TN"] + cm["FP"] + cm["FN"] == 1025
    assert cm["n"] == 1025


def test_error_list_counts(metrics):
    assert len(pd.read_csv(TP)) == metrics["confusion_matrix"]["TP"]
    assert len(pd.read_csv(TN)) == metrics["confusion_matrix"]["TN"]
    assert len(pd.read_csv(FP)) == metrics["confusion_matrix"]["FP"]
    assert len(pd.read_csv(FN)) == metrics["confusion_matrix"]["FN"]


def test_metric_formulas_from_counts(metrics):
    tp = metrics["metrics"]["TP"]
    tn = metrics["metrics"]["TN"]
    fp = metrics["metrics"]["FP"]
    fn = metrics["metrics"]["FN"]
    n = tp + tn + fp + fn
    sens = tp / (tp + fn)
    spec = tn / (tn + fp)
    prec = tp / (tp + fp)
    f1 = 2 * prec * sens / (prec + sens)
    acc = (tp + tn) / n
    bal = (sens + spec) / 2
    denom = math.sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn))
    mcc = (tp * tn - fp * fn) / denom
    m = metrics["metrics"]
    assert abs(m["sensitivity_recall_tpr"] - sens) < 1e-12
    assert abs(m["specificity_tnr"] - spec) < 1e-12
    assert abs(m["precision_ppv"] - prec) < 1e-12
    assert abs(m["f1"] - f1) < 1e-12
    assert abs(m["accuracy"] - acc) < 1e-12
    assert abs(m["balanced_accuracy"] - bal) < 1e-12
    assert abs(m["mcc"] - mcc) < 1e-12


def test_metrics_finite_and_in_range(metrics):
    m = metrics["metrics"]
    for k in (
        "sensitivity_recall_tpr",
        "specificity_tnr",
        "precision_ppv",
        "npv",
        "f1",
        "accuracy",
        "balanced_accuracy",
    ):
        v = m[k]
        assert math.isfinite(v)
        assert -1e-12 <= v <= 1 + 1e-12
    assert math.isfinite(m["mcc"])
    assert -1 - 1e-12 <= m["mcc"] <= 1 + 1e-12


def test_locked_modeling_policy(metrics):
    pol = metrics["modeling_policy"]
    assert pol["medium_id"] == "mops_pyruvate_lee2015"
    assert pol["threshold_ratio"] == 0.01
    assert pol["objective"] == "PA_Biomass6_DM"
    assert metrics["metrics"]["threshold_ratio"] == 0.01
    assert metrics["d20_used_in_primary_matrix"] is False
    assert metrics["status"] == (
        "V01_BINARY_METRICS_COMPUTED_PENDING_HUMAN_INTERPRETATION"
    )


def test_no_stray_results_comparison_metrics_glob():
    metrics_dir = ROOT / "results" / "comparison"
    stray = list(metrics_dir.glob("metrics_*.csv")) if metrics_dir.exists() else []
    assert not stray


def test_rerun_produces_identical_counts_and_metrics():
    before_metrics = METRICS.read_bytes()
    before_joined = JOINED.read_bytes()
    before_binary = _sha(BINARY)
    before_lee = _sha(LEE_D20)
    before_pred = _sha(PRED_CANONICAL)
    proc = subprocess.run(
        [sys.executable, str(SCRIPT)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stdout + "\n" + proc.stderr
    assert METRICS.read_bytes() == before_metrics
    assert JOINED.read_bytes() == before_joined
    assert _sha(BINARY) == before_binary == BINARY_SHA
    assert _sha(LEE_D20) == before_lee == LEE_D20_SHA
    assert _sha(PRED_CANONICAL) == before_pred


def test_confusion_matrix_csv_totals():
    cm = pd.read_csv(CM)
    counts = dict(zip(cm["cell"], cm["count"]))
    assert counts["TP"] + counts["FN"] + counts["TN"] + counts["FP"] == counts["n"]
    assert counts["n"] == 1025

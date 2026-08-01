"""Tests for V-01 MOPS-pyruvate structural error audit (diagnostic only).

Ensures audit covers exactly the frozen FP/FN sets, does not alter labels,
and does not modify model/media/threshold artifacts.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/processed/validation"
AUDIT = OUT / "v01_mops_pyruvate_error_audit.csv"
FN_AUDIT = OUT / "v01_mops_pyruvate_false_negative_audit.csv"
FP_AUDIT = OUT / "v01_mops_pyruvate_false_positive_audit.csv"
COUNTS = ROOT / "project_management/audit/v01_mops_pyruvate/V01_ERROR_CATEGORY_COUNTS.csv"
REPORT = ROOT / "project_management/audit/v01_mops_pyruvate/V01_ERROR_STRUCTURE_AUDIT.md"
SCRIPT = ROOT / "scripts/validation/audit_v01_mops_pyruvate_errors.py"

FN_FROZEN = OUT / "v01_mops_pyruvate_false_negatives.csv"
FP_FROZEN = OUT / "v01_mops_pyruvate_false_positives.csv"
TP_FROZEN = OUT / "v01_mops_pyruvate_true_positives.csv"
TN_FROZEN = OUT / "v01_mops_pyruvate_true_negatives.csv"
PRED = OUT / "v01_mops_pyruvate_gene_predictions.csv"
METRICS = OUT / "v01_mops_pyruvate_metrics.json"
MODEL = ROOT / "models/paeruginosa_MODEL1507180020.xml"
MEDIUM_EX = ROOT / "data/processed/conditions/mops_pyruvate_lee2015_exchanges.csv"
BINARY = (
    ROOT
    / "data/processed/literature/gene_level"
    / "varadarajan2020_lee2015_minimal_PRIMARY_BINARY_UNIVERSE.csv"
)

MODEL_SHA = "0868a5ebb41ebb4967c3c182e686eca7552af9255cba5a6d130cf114d1212ead"
BINARY_SHA = "e3174cb0975cd39c210ebfb86e26f87a3a2e5904664f7d8c5c6663fe93a5649e"

FN_CATEGORIES = {
    "FN_ISOENZYME_REDUNDANCY",
    "FN_ALTERNATIVE_PATHWAY",
    "FN_GPR_STRUCTURE",
    "FN_REACTION_INACTIVE",
    "FN_NON_METABOLIC_OR_OUT_OF_SCOPE",
    "FN_TRANSPORT_OR_EXCHANGE_CONTEXT",
    "FN_BIOMASS_FORMULATION",
    "FN_MAPPING_OR_ANNOTATION",
    "FN_NEAR_THRESHOLD",
    "FN_UNRESOLVED",
}
FP_CATEGORIES = {
    "FP_MISSING_ALTERNATIVE_PATHWAY",
    "FP_MISSING_ISOENZYME",
    "FP_MISSING_TRANSPORT",
    "FP_OVER_RESTRICTIVE_NETWORK",
    "FP_GPR_STRUCTURE",
    "FP_BIOMASS_FORMULATION",
    "FP_MEDIA_CONTEXT",
    "FP_MAPPING_OR_ANNOTATION",
    "FP_NEAR_THRESHOLD",
    "FP_UNRESOLVED",
}


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


@pytest.fixture(scope="module")
def frozen_hashes():
    return {
        "fn": _sha(FN_FROZEN),
        "fp": _sha(FP_FROZEN),
        "tp": _sha(TP_FROZEN),
        "tn": _sha(TN_FROZEN),
        "pred": _sha(PRED),
        "metrics": _sha(METRICS),
        "model": _sha(MODEL),
        "medium": _sha(MEDIUM_EX),
        "binary": _sha(BINARY),
    }


@pytest.fixture(scope="module")
def audit_df(frozen_hashes) -> pd.DataFrame:
    """Run audit once for the module; verify inputs unchanged afterward."""
    before = dict(frozen_hashes)
    proc = subprocess.run(
        [sys.executable, str(SCRIPT)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert proc.returncode == 0, proc.stdout + "\n" + proc.stderr
    after = {
        "fn": _sha(FN_FROZEN),
        "fp": _sha(FP_FROZEN),
        "tp": _sha(TP_FROZEN),
        "tn": _sha(TN_FROZEN),
        "pred": _sha(PRED),
        "metrics": _sha(METRICS),
        "model": _sha(MODEL),
        "medium": _sha(MEDIUM_EX),
        "binary": _sha(BINARY),
    }
    assert after == before, "Audit must not modify frozen V-01 / model / media inputs"
    assert AUDIT.exists()
    return pd.read_csv(AUDIT)


def test_exact_error_counts(audit_df):
    assert len(audit_df) == 145
    assert int((audit_df["error_type"] == "FN").sum()) == 98
    assert int((audit_df["error_type"] == "FP").sum()) == 47


def test_no_tp_tn_included(audit_df):
    assert set(audit_df["error_type"]) == {"FN", "FP"}
    tp = set(pd.read_csv(TP_FROZEN)["pao1_locus"])
    tn = set(pd.read_csv(TN_FROZEN)["pao1_locus"])
    genes = set(audit_df["gene"])
    assert genes.isdisjoint(tp)
    assert genes.isdisjoint(tn)


def test_maps_to_frozen_predictions(audit_df):
    fn = set(pd.read_csv(FN_FROZEN)["pao1_locus"])
    fp = set(pd.read_csv(FP_FROZEN)["pao1_locus"])
    assert set(audit_df.loc[audit_df["error_type"] == "FN", "gene"]) == fn
    assert set(audit_df.loc[audit_df["error_type"] == "FP", "gene"]) == fp
    pred = pd.read_csv(PRED).set_index("pao1_locus")
    for _, row in audit_df.iterrows():
        p = pred.loc[row["gene"]]
        assert p["model_prediction"] == row["model_prediction"]
        assert p["experimental_label"] == row["experimental_label"]
        if row["error_type"] == "FN":
            assert p["short_label"] == "POSITIVE"
            assert p["model_prediction"] == "MODEL_NEGATIVE"
        else:
            assert p["short_label"] == "NEGATIVE"
            assert p["model_prediction"] == "MODEL_POSITIVE"


def test_experimental_labels_unchanged(audit_df):
    universe = pd.read_csv(BINARY).set_index("pao1_locus")
    assert _sha(BINARY) == BINARY_SHA
    for _, row in audit_df.iterrows():
        assert universe.loc[row["gene"], "experimental_label"] == row["experimental_label"]


def test_model_media_threshold_untouched(frozen_hashes, audit_df):
    assert frozen_hashes["model"] == MODEL_SHA
    assert _sha(MODEL) == MODEL_SHA
    assert _sha(MEDIUM_EX) == frozen_hashes["medium"]
    m = json.loads(METRICS.read_text(encoding="utf-8"))
    assert m["modeling_policy"]["threshold_ratio"] == 0.01
    assert m["modeling_policy"]["medium_id"] == "mops_pyruvate_lee2015"
    assert m["confusion_matrix"] == {
        "FN": 98,
        "FP": 47,
        "TN": 764,
        "TP": 116,
        "experimental_negative": 811,
        "experimental_positive": 214,
        "n": 1025,
    }
    # audit_df fixture already re-checked hashes post-run
    assert len(audit_df) == 145


def test_split_audit_files(audit_df):
    fn_a = pd.read_csv(FN_AUDIT)
    fp_a = pd.read_csv(FP_AUDIT)
    assert len(fn_a) == 98
    assert len(fp_a) == 47
    assert (fn_a["error_type"] == "FN").all()
    assert (fp_a["error_type"] == "FP").all()
    assert set(fn_a["gene"]) == set(
        audit_df.loc[audit_df["error_type"] == "FN", "gene"]
    )
    assert set(fp_a["gene"]) == set(
        audit_df.loc[audit_df["error_type"] == "FP", "gene"]
    )


def test_categories_allowed_and_unresolved_ok(audit_df):
    fn_cats = set(audit_df.loc[audit_df["error_type"] == "FN", "diagnostic_category"])
    fp_cats = set(audit_df.loc[audit_df["error_type"] == "FP", "diagnostic_category"])
    assert fn_cats <= FN_CATEGORIES
    assert fp_cats <= FP_CATEGORIES
    # unresolved allowed
    assert "FN_UNRESOLVED" in FN_CATEGORIES
    assert "FP_UNRESOLVED" in FP_CATEGORIES


def test_deterministic_rerun(audit_df):
    """Algorithmic classification must be stable across runs."""
    proc = subprocess.run(
        [sys.executable, str(SCRIPT)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert proc.returncode == 0, proc.stderr
    again = pd.read_csv(AUDIT)
    cols = [
        "gene",
        "error_type",
        "diagnostic_category",
        "diagnostic_confidence",
        "isoenzyme_flag",
        "multi_gene_complex_flag",
        "blocked_reaction_flag",
        "pathway_cluster",
        "review_priority",
    ]
    left = audit_df[cols].sort_values(["error_type", "gene"]).reset_index(drop=True)
    right = again[cols].sort_values(["error_type", "gene"]).reset_index(drop=True)
    pd.testing.assert_frame_equal(left, right)


def test_artifacts_and_gate_text():
    assert COUNTS.exists()
    assert REPORT.exists()
    text = REPORT.read_text(encoding="utf-8")
    assert "V01_ERROR_ANALYSIS_COMPLETED_PENDING_HUMAN_REVIEW" in text
    assert "DIAGNOSTIC" in text.upper() or "diagnostic" in text
    counts = pd.read_csv(COUNTS)
    assert len(counts) > 0

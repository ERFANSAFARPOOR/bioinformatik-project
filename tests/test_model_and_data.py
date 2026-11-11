"""Regression tests pinning the scientific behavior of the PAO1 iMO1056 project.

Run under the canonical env:  conda run -n reccobra39 pytest -q
These lock model identity, WT growth, and the cleaned predicted-essentiality file
so repository reorganization cannot silently change the science. V-01 metrics
are tested separately in test_v01_mops_pyruvate_binary_validation.py; this module
guards against unreviewed legacy metrics exports.
"""
import hashlib
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "models" / "paeruginosa_MODEL1507180020.xml"
MODEL_RAW_COPY = ROOT / "models" / "raw" / "paeruginosa_MODEL1507180020.xml"
PRED_CSV = (
    ROOT / "data" / "processed" / "essentiality" / "predicted_essentiality_default_medium.csv"
)
EXPECTED_SHA = "0868a5ebb41ebb4967c3c182e686eca7552af9255cba5a6d130cf114d1212ead"
EXPECTED_WT = 1.0479285528184004
WT_TOL = 1e-6


def _sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


@pytest.fixture(scope="module")
def model():
    import cobra
    return cobra.io.read_sbml_model(str(MODEL_PATH))


def test_raw_model_present_and_unmodified():
    assert MODEL_PATH.exists(), "canonical model path must remain working"
    assert _sha256(MODEL_PATH) == EXPECTED_SHA, "raw model must not change"


def test_raw_copy_is_byte_identical():
    assert MODEL_RAW_COPY.exists(), "models/raw archived copy must exist"
    assert _sha256(MODEL_RAW_COPY) == EXPECTED_SHA


def test_model_loads_and_counts(model):
    assert len(model.reactions) == 1110
    assert len(model.metabolites) == 879
    assert len(model.genes) == 1054


def test_model_identity_pao1(model):
    # SBML id and gene-tag scheme both indicate iMO1056 / PAO1
    assert model.id == "MODEL1507180020"
    pa_genes = [g.id for g in model.genes if g.id.startswith("PA")]
    assert len(pa_genes) == 1054, "all model genes are PAO1 PAxxxx locus tags"
    assert not any(g.id.startswith("PA14_") for g in model.genes), "not PA14"


def test_objective_is_biomass(model):
    assert "PA_Biomass6_DM" in str(model.objective.expression)


def test_default_growth(model):
    sol = model.optimize()
    assert sol.status == "optimal"
    assert abs(sol.objective_value - EXPECTED_WT) < WT_TOL


def test_predicted_essentiality_file():
    assert PRED_CSV.exists()
    df = pd.read_csv(PRED_CSV)
    assert len(df) == 1054, "one row per model gene"
    # gene_id cleaned (no set-repr like {'PAxxxx'})
    assert df["gene_id"].str.match(r"^PA\d+$").all(), "gene_id must be clean PAxxxx"
    n_essential = int(df["is_essential"].astype(str).str.lower().eq("true").sum())
    assert n_essential == 166, "166 predicted essential at 1% threshold"


def test_no_unreviewed_legacy_metrics_exports():
    """Guard the unused legacy results/comparison/metrics_*.csv namespace.

    Deliberately generated D-21/V-01 metrics live under data/processed/validation
    and have their own integrity tests. A legacy export requires a documented
    promotion decision and an accompanying update to this guard.
    """
    metrics_dir = ROOT / "results" / "comparison"
    stray = [p for p in metrics_dir.glob("metrics_*.csv")] if metrics_dir.exists() else []
    assert not stray, f"unexpected validation-metrics files present: {stray}"

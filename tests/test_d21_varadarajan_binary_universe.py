"""Integrity tests for D-21 Varadarajan2020 Minimal primary binary universe.

Does NOT compute confusion-matrix metrics. Full V-01 metrics remain a separate step.
"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = (
    ROOT
    / "data/processed/literature/gene_level"
    / "varadarajan2020_lee2015_minimal_gene_labels_CANDIDATE.csv"
)
READY = (
    ROOT
    / "data/processed/literature/gene_level"
    / "varadarajan2020_lee2015_minimal_gene_labels_READY.csv"
)
BINARY = (
    ROOT
    / "data/processed/literature/gene_level"
    / "varadarajan2020_lee2015_minimal_PRIMARY_BINARY_UNIVERSE.csv"
)
LEE_READY = (
    ROOT
    / "data/processed/literature/gene_level"
    / "literature_evidence_gene_level_READY_mops_pyruvate_lee2015.csv"
)
PRED = ROOT / "results/essentiality/gene_essentiality_mops_pyruvate_lee2015.csv"
MODEL = ROOT / "models/paeruginosa_MODEL1507180020.xml"
PA_STD = re.compile(r"^PA\d{4}$")

# Frozen D-20 Lee READY digest at D-21 promotion time (must remain unchanged)
LEE_READY_SHA256 = (
    "578b9a29583d4e8580996908ec9b1a6d0f9410125cecc2d6a7d9c0dfbb2929a3"
)


def _sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


@pytest.fixture(scope="module")
def ready() -> pd.DataFrame:
    assert READY.exists(), "D-21 READY file missing — run promote script"
    return pd.read_csv(READY)


@pytest.fixture(scope="module")
def binary() -> pd.DataFrame:
    assert BINARY.exists(), "D-21 primary binary universe missing — run promote script"
    return pd.read_csv(BINARY)


@pytest.fixture(scope="module")
def candidate() -> pd.DataFrame:
    assert CANDIDATE.exists(), "CANDIDATE audit file must remain"
    return pd.read_csv(CANDIDATE)


def test_candidate_preserved(candidate):
    assert len(candidate) == 5799
    assert (candidate["review_status"] == "CANDIDATE_FOR_HUMAN_REVIEW").all()


def test_ready_row_count_and_labels(ready):
    assert len(ready) == 5799
    assert set(ready["experimental_label"]) == {
        "POSITIVE_CONSENSUS_ESSENTIAL",
        "NEGATIVE_0_OF_3_NOT_CALLED_ESSENTIAL",
        "AMBIGUOUS_1_OF_3",
    }
    vc = ready["experimental_label"].value_counts()
    assert int(vc["POSITIVE_CONSENSUS_ESSENTIAL"]) == 415
    assert int(vc["NEGATIVE_0_OF_3_NOT_CALLED_ESSENTIAL"]) == 5312
    assert int(vc["AMBIGUOUS_1_OF_3"]) == 72
    assert (ready["review_status"] == "READY").all()
    assert (ready["decision_id"] == "D-21").all()
    assert (ready["human_review_decision"] == "APPROVED_FOR_PRIMARY_BINARY_VALIDATION").all()


def test_no_duplicate_primary_pao1(binary):
    assert binary["pao1_locus"].is_unique
    assert len(binary) == 1025


def test_primary_pao1_id_policy(binary):
    assert binary["pao1_locus"].astype(str).str.match(r"^PA\d{4}$").all()


def test_primary_all_model_evaluable(binary):
    assert (binary["in_imo1056"] == 1).all()
    assert (binary["model_evaluable"] == 1).all()
    if PRED.exists():
        pred = pd.read_csv(PRED)
        gcol = "gene_id" if "gene_id" in pred.columns else pred.columns[0]
        pred_pas = set()
        for gid in pred[gcol].astype(str):
            m = re.search(r"(PA\d{4})", gid)
            if m:
                pred_pas.add(m.group(1))
        assert set(binary["pao1_locus"]).issubset(pred_pas)


def test_no_ambiguous_or_sum1_in_primary(binary):
    assert (binary["short_label"] != "AMBIGUOUS").all()
    assert (binary["experimental_label"] != "AMBIGUOUS_1_OF_3").all()
    assert (binary["minimal_sum"] != 1).all()
    assert (binary["minimal_sum"] >= 0).all()


def test_primary_label_definitions(binary):
    pos = binary["experimental_label"] == "POSITIVE_CONSENSUS_ESSENTIAL"
    neg = binary["experimental_label"] == "NEGATIVE_0_OF_3_NOT_CALLED_ESSENTIAL"
    assert int(pos.sum()) == 214
    assert int(neg.sum()) == 811
    assert (binary.loc[pos, "minimal_sum"] >= 2).all()
    assert (binary.loc[neg, "minimal_sum"] == 0).all()


def test_ambiguous_retained_with_exclusion(ready):
    amb = ready[ready["experimental_label"] == "AMBIGUOUS_1_OF_3"]
    assert len(amb) == 72
    assert (amb["binary_primary_inclusion"] == 0).all()
    amb_model = amb[(amb["in_imo1056"] == 1) & (amb["mapping_status"] == "unique_std_PAO1")]
    assert len(amb_model) == 18
    assert (
        amb_model["exclusion_reason"] == "EXCLUDED_PRIMARY_BINARY_DISCORDANT_1_OF_3"
    ).all()


def test_provenance_and_varadarajan_only(ready, binary):
    assert ready["evidence_source"].eq("Varadarajan2020_Lee2015_Tnseq_remap").all()
    assert binary["evidence_source"].eq("Varadarajan2020_Lee2015_Tnseq_remap").all()
    assert ready["source_dataset"].str.contains("DS1_MPAO1_CDS").all()
    assert (ready["not_independent_replication_of_lee2015"] == 1).all()


def test_d20_lee_ready_unchanged():
    """D-20 Lee-original positives remain a separate unchanged layer."""
    assert LEE_READY.exists()
    lee = pd.read_csv(LEE_READY)
    assert len(lee) == 437
    assert (lee["review_status"] == "READY").all()
    assert _sha256(LEE_READY) == LEE_READY_SHA256
    binary = pd.read_csv(BINARY)
    assert len(binary) == 1025
    assert len(binary) != len(lee)


def test_candidate_to_ready_label_consistency(candidate, ready):
    merged = candidate.merge(
        ready[["mpao1_locus", "short_label", "minimal_sum", "pao1_locus"]],
        on="mpao1_locus",
        suffixes=("_c", "_r"),
    )
    assert len(merged) == 5799
    assert (merged["candidate_label"] == merged["short_label"]).all()
    assert (merged["minimal_sum_c"] == merged["minimal_sum_r"]).all()
    assert (
        merged["pao1_locus_c"].fillna("") == merged["pao1_locus_r"].fillna("")
    ).all()


def test_no_metrics_artifacts():
    metrics_dir = ROOT / "results" / "comparison"
    stray = list(metrics_dir.glob("metrics_*.csv")) if metrics_dir.exists() else []
    assert not stray
    # Binary/READY must not contain metric columns
    for path in (READY, BINARY):
        cols = {c.lower() for c in pd.read_csv(path, nrows=0).columns}
        assert not cols & {
            "tp",
            "tn",
            "fp",
            "fn",
            "mcc",
            "f1",
            "precision",
            "recall",
            "specificity",
            "accuracy",
        }


def test_primary_genes_in_imo1056_model(binary):
    import cobra

    model = cobra.io.read_sbml_model(str(MODEL))
    model_pas = set()
    for g in model.genes:
        m = re.search(r"(PA\d{4})", g.id)
        if m:
            model_pas.add(m.group(1))
        elif PA_STD.match(g.id):
            model_pas.add(g.id)
    assert set(binary["pao1_locus"]).issubset(model_pas)
    assert len(model.genes) == 1054


def test_rerun_promotion_is_deterministic():
    """Re-running the promote script must leave READY/binary digests unchanged."""
    import subprocess
    import sys

    before_ready = _sha256(READY)
    before_binary = _sha256(BINARY)
    before_cand = _sha256(CANDIDATE)
    before_lee = _sha256(LEE_READY)
    script = ROOT / "scripts" / "promote_varadarajan2020_minimal_labels_ready.py"
    proc = subprocess.run(
        [sys.executable, str(script)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stdout + "\n" + proc.stderr
    assert _sha256(READY) == before_ready
    assert _sha256(BINARY) == before_binary
    assert _sha256(CANDIDATE) == before_cand
    assert _sha256(LEE_READY) == before_lee

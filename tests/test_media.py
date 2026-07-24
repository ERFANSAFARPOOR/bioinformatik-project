"""Tests for documented media (Batch A DEFINED + LB_approx PARTIAL).

Run:  C:/Users/pro/anaconda3/envs/reccobra39/python.exe -m pytest tests/test_media.py -q
Never invent growth rates — assertions record real solver values with tolerance.
"""
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "models" / "paeruginosa_MODEL1507180020.xml"
COND_DIR = ROOT / "data" / "processed" / "conditions"

# Observed under reccobra39 / GLPK during C-01b implementation (2026-07-24).
# Source: scripts/export_media_tables.py — not invented.
OBSERVED_WT = {
    "mops_pyruvate_lee2015": 0.40533903063568605,
    "mops_succinate_turner2015": 0.5528029187572905,
    "LB_approx_lee2015": 14.950547856095707,
}
WT_TOL = 1e-4


@pytest.fixture(scope="module")
def model():
    import cobra

    return cobra.io.read_sbml_model(str(MODEL_PATH))


@pytest.fixture(scope="module")
def measured_growth(model):
    from src.medium import iter_implemented_media, wildtype_growth

    out = {}
    for spec in iter_implemented_media():
        status, value = wildtype_growth(model, spec, quiet=True)
        out[spec.medium_id] = (status, value)
    return out


def test_objective_is_pa_biomass6_dm(model):
    assert "PA_Biomass6_DM" in str(model.objective.expression)


def test_registry_contains_batch_a_and_lb_approx():
    from src.medium import get_medium_registry

    reg = get_medium_registry()
    assert "mops_pyruvate_lee2015" in reg
    assert "mops_succinate_turner2015" in reg
    assert "LB_approx_lee2015" in reg
    assert reg["mops_pyruvate_lee2015"].label == "DEFINED"
    assert reg["mops_succinate_turner2015"].label == "DEFINED"
    assert reg["LB_approx_lee2015"].label == "PARTIAL"


def test_lb_approx_flags_yeast_extract_and_tryptone():
    from src.medium import get_medium

    spec = get_medium("LB_approx_lee2015")
    joined = " | ".join(spec.unmodeled_components).lower()
    assert "yeast extract" in joined
    assert "tryptone" in joined
    assert "true lb" not in spec.display_name.lower()
    assert spec.medium_id.startswith("LB_approx")


def test_every_bound_has_source():
    from src.medium import iter_implemented_media

    for spec in iter_implemented_media():
        spec.validate()
        for e in spec.exchanges:
            assert e.bound_source
            assert not e.bound_source.startswith("PENDING")


def test_refuse_unsourced_bound(model):
    from src.medium import ExchangeBound, MediumSpec, UnsourcedBoundError, apply_medium

    bad = MediumSpec(
        medium_id="bad_unsourced",
        label="DEFINED",
        display_name="bad",
        citation="test",
        locator="test",
        strain_context="PAO1",
        exchanges=(ExchangeBound("EX_o2_e", -1000.0, "PENDING_NO_SOURCE"),),
    )
    with pytest.raises(ValueError):
        bad.validate()

    # apply_medium also refuses PENDING sources even if validate is bypassed
    original = MediumSpec.validate
    MediumSpec.validate = lambda self: None  # type: ignore
    try:
        with pytest.raises(UnsourcedBoundError):
            apply_medium(model.copy(), bad, quiet=True)
    finally:
        MediumSpec.validate = original


def test_apply_medium_no_crash(model):
    from src.medium import apply_medium, get_current_medium, iter_implemented_media

    for spec in iter_implemented_media():
        m = model.copy()
        apply_medium(m, spec, quiet=True)
        current = get_current_medium(m)
        assert current, f"{spec.medium_id} opened no uptakes"
        for eid, lb in spec.exchange_dict().items():
            assert eid in current
            assert abs(current[eid] - lb) < 1e-12


def test_wt_growth_feasible_under_each_medium(measured_growth):
    """Assert optimal positive growth and pin measured rates (not invented)."""
    for medium_id, expected in OBSERVED_WT.items():
        status, value = measured_growth[medium_id]
        assert status == "optimal", f"{medium_id}: status={status}"
        assert value > 1e-6, f"{medium_id}: non-positive growth {value}"
        assert abs(value - expected) < WT_TOL, (
            f"{medium_id}: growth {value} != pinned {expected}"
        )

def test_export_media_tables(tmp_path, model):
    from src.medium import export_media_tables, iter_implemented_media

    paths = export_media_tables(tmp_path)
    assert paths["exchanges"].exists()
    assert paths["unmodeled"].exists()
    assert paths["summary"].exists()
    for spec in iter_implemented_media():
        assert (tmp_path / f"{spec.medium_id}_exchanges.csv").exists()


def test_processed_conditions_dir_populated_or_exportable(model):
    """Prefer repo derived tables; if missing, export is still functional."""
    from src.medium import export_media_tables

    if not (COND_DIR / "media_summary.csv").exists():
        export_media_tables(COND_DIR)
    assert (COND_DIR / "media_summary.csv").exists()
    assert (COND_DIR / "media_exchanges.csv").exists()
    assert (COND_DIR / "media_unmodeled_components.csv").exists()

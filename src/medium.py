"""
Medium management for iMO1056 (PAO1).

Extends the teaching helpers (`reset_medium`, `set_medium`) with documented
experimental media (Batch A DEFINED + LB_approx PARTIAL).

Hard rules:
- Every exchange bound must carry a provenance source; inventing bounds is forbidden.
- Never claim true LB — only ``LB_approx`` with yeast extract / tryptone flagged.
- Concentration (mM) ≠ flux (mmol/gDW/h). Carbon/salt uptake rates follow the
  audited iMO1056 default-medium convention unless a cited flux conversion exists.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

import cobra
import pandas as pd

# ---------------------------------------------------------------------------
# Provenanced uptake-rate conventions (not invented per-component fluxes)
# ---------------------------------------------------------------------------

# Audited iMO1056 default medium (PROJECT_AUDIT / C01B_MEDIA_RECONSTRUCTION_PLAN):
# EX_glc_e = -10; salts/metals/O2 = -1000.
DEFAULT_CARBON_UPTAKE = -10.0
DEFAULT_UNLIMITED_UPTAKE = -1000.0

BOUND_SOURCE_MODEL_DEFAULT_CARBON = (
    "iMO1056 default-medium carbon uptake convention "
    "(EX_glc_e = -10 mmol/gDW/h in audited SBML); used as the carbon-source "
    "uptake rate when no paper-cited flux conversion exists"
)
BOUND_SOURCE_MODEL_DEFAULT_UNLIMITED = (
    "iMO1056 default-medium unlimited uptake convention "
    "(salts/metals/O2 = -1000 mmol/gDW/h in audited SBML)"
)

# Amino acids present as exchanges in iMO1056 (C01B plan; verified at apply time).
AMINO_ACID_EXCHANGES: Tuple[str, ...] = (
    "EX_ala__L_e",
    "EX_arg__L_e",
    "EX_asn__L_e",
    "EX_asp__L_e",
    "EX_cys__L_e",
    "EX_gln__L_e",
    "EX_glu__L_e",
    "EX_gly_e",
    "EX_his__L_e",
    "EX_ile__L_e",
    "EX_leu__L_e",
    "EX_lys__L_e",
    "EX_met__L_e",
    "EX_phe__L_e",
    "EX_pro__L_e",
    "EX_ser__L_e",
    "EX_thr__L_e",
    "EX_trp__L_e",
    "EX_tyr__L_e",
    "EX_val__L_e",
)

# Minimal salts / ions / gases shared by defined MOPS media (mapped from recipe
# ions that have exchanges). Ca2+ has no exchange in iMO1056 — flagged unmodeled.
MOPS_BASE_EXCHANGES: Tuple[str, ...] = (
    "EX_nh4_e",
    "EX_pi_e",
    "EX_so4_e",
    "EX_k_e",
    "EX_mg2_e",
    "EX_fe2_e",
    "EX_fe3_e",
    "EX_na1_e",
    "EX_h_e",
    "EX_h2o_e",
    "EX_co2_e",
    "EX_o2_e",
)


@dataclass(frozen=True)
class ExchangeBound:
    """One exchange lower bound with provenance."""

    exchange_id: str
    lower_bound: float
    bound_source: str
    recipe_component: str = ""
    recipe_concentration: str = ""
    notes: str = ""


@dataclass(frozen=True)
class MediumSpec:
    """Documented in-model medium (DEFINED or PARTIAL)."""

    medium_id: str
    label: str  # DEFINED | PARTIAL
    display_name: str
    citation: str
    locator: str
    strain_context: str
    exchanges: Tuple[ExchangeBound, ...]
    unmodeled_components: Tuple[str, ...] = ()
    carbon_source_exchange: str = ""
    electron_acceptor_exchange: str = "EX_o2_e"
    notes: str = ""

    def exchange_dict(self) -> Dict[str, float]:
        return {e.exchange_id: e.lower_bound for e in self.exchanges}

    def validate(self) -> None:
        if self.label not in {"DEFINED", "PARTIAL"}:
            raise ValueError(f"{self.medium_id}: label must be DEFINED or PARTIAL")
        if not self.citation or not self.locator:
            raise ValueError(f"{self.medium_id}: citation and locator required")
        if not self.exchanges:
            raise ValueError(f"{self.medium_id}: no exchanges defined")
        for e in self.exchanges:
            if not e.bound_source or e.bound_source.startswith("PENDING"):
                raise ValueError(
                    f"{self.medium_id}: exchange {e.exchange_id} lacks a sourced "
                    f"bound (got {e.bound_source!r})"
                )
            if e.lower_bound >= 0:
                raise ValueError(
                    f"{self.medium_id}: uptake bound for {e.exchange_id} must be < 0"
                )


def _mops_base_bounds() -> List[ExchangeBound]:
    return [
        ExchangeBound(
            eid,
            DEFAULT_UNLIMITED_UPTAKE,
            BOUND_SOURCE_MODEL_DEFAULT_UNLIMITED,
            recipe_component="MOPS-base salts/ions/gases (mapped subset)",
            notes="Buffer molecules (MOPS/tricine) are not metabolites — see unmodeled",
        )
        for eid in MOPS_BASE_EXCHANGES
    ]


def _carbon_bound(exchange_id: str, recipe_component: str, recipe_concentration: str) -> ExchangeBound:
    return ExchangeBound(
        exchange_id,
        DEFAULT_CARBON_UPTAKE,
        BOUND_SOURCE_MODEL_DEFAULT_CARBON,
        recipe_component=recipe_component,
        recipe_concentration=recipe_concentration,
        notes="Recipe concentration documented; flux uses model carbon convention",
    )


def build_mops_pyruvate_lee() -> MediumSpec:
    """Lee 2015 MOPS-pyruvate (DEFINED) from SI Growth Media recipe."""
    exchanges = _mops_base_bounds()
    exchanges.append(
        _carbon_bound(
            "EX_pyr_e",
            "sodium pyruvate",
            "10 mL/L of 20% (wt/vol) ≈ 18.2 mM (Lee SI)",
        )
    )
    return MediumSpec(
        medium_id="mops_pyruvate_lee2015",
        label="DEFINED",
        display_name="MOPS-pyruvate (Lee 2015)",
        citation=(
            "Lee SA et al. (2015) General and condition-specific essential "
            "functions of Pseudomonas aeruginosa. PNAS 112(16):5189-5194. "
            "DOI 10.1073/pnas.1422186112"
        ),
        locator=(
            "Lee SI Materials and Methods — Growth Media: "
            "'MOPS-pyruvate agar (per liter)' "
            "(data/raw/literature/lee2015/Supporting Information.pdf)"
        ),
        strain_context="MPAO1",
        exchanges=tuple(exchanges),
        unmodeled_components=(
            "MOPS buffer (not a metabolite exchange)",
            "tricine (not a metabolite exchange)",
            "CaCl2 (no EX_ca2_e in iMO1056)",
            "Bacto agar (solid-phase scaffold; not modeled)",
            "tetracycline / chloramphenicol supplements (not nutrients)",
        ),
        carbon_source_exchange="EX_pyr_e",
        electron_acceptor_exchange="EX_o2_e",
        notes=(
            "1× MOPS base from 100 mL/L of 10× stock (400 mM MOPS, 40 mM tricine, "
            "0.1 mM FeSO4, 95 mM NH4Cl, 2.76 mM K2SO4, 5 µM CaCl2, 5.25 mM MgCl2) "
            "+ 10 mL/L 0.132 M K2HPO4 + 10 mL/L 20% sodium pyruvate. "
            "Mapped ions use default unlimited uptake; carbon uses -10 convention."
        ),
    )


def build_mops_succinate_turner() -> MediumSpec:
    """Turner 2015 MOPS-succinate (DEFINED) via Turner 2014 Methods + Neidhardt MOPS."""
    exchanges = _mops_base_bounds()
    exchanges.append(
        _carbon_bound(
            "EX_succ_e",
            "succinate",
            "20 mM (Turner 2014 Methods; cited by Turner 2015 as ref. 12)",
        )
    )
    return MediumSpec(
        medium_id="mops_succinate_turner2015",
        label="DEFINED",
        display_name="MOPS-succinate (Turner 2015)",
        citation=(
            "Turner KH et al. (2015) Essential genome of Pseudomonas aeruginosa "
            "in cystic fibrosis sputum. PNAS 112(13):4110-4115. "
            "DOI 10.1073/pnas.1419677112. "
            "Medium described via Turner et al. (2014) PLoS Genet 10(7):e1004518 "
            "(Methods: MOPS-buffered minimal medium with 20 mM succinate)"
        ),
        locator=(
            "Turner 2015 Methods: 'MOPS-succinate is described in ref. 12' "
            "(= Turner 2014 PLoS Genet); Turner 2014 Methods: "
            "'MOPS-buffered minimal medium [48] with 20 mM succinate'"
        ),
        strain_context="PAO1",
        exchanges=tuple(exchanges),
        unmodeled_components=(
            "MOPS buffer (not a metabolite exchange)",
            "Any micronutrients / vitamins from the cited MOPS base that lack "
            "exchanges in iMO1056 (e.g. Socransky vitamins if used in related "
            "Whiteley-lab MOPS recipes) — not asserted here beyond carbon + mapped ions",
        ),
        carbon_source_exchange="EX_succ_e",
        electron_acceptor_exchange="EX_o2_e",
        notes=(
            "Batch A DEFINED medium for Turner PAO1 fitness contrasts that use "
            "MOPS-succinate as the minimal comparator. Carbon = 20 mM succinate "
            "(sourced); flux uses model carbon convention (-10)."
        ),
    )


def build_lb_approx_lee() -> MediumSpec:
    """Lee LB as PARTIAL approximation — never claim true LB."""
    exchanges: List[ExchangeBound] = [
        ExchangeBound(
            eid,
            DEFAULT_UNLIMITED_UPTAKE,
            BOUND_SOURCE_MODEL_DEFAULT_UNLIMITED,
            recipe_component="ion / gas present in rich medium / default salts",
        )
        for eid in (
            "EX_nh4_e",
            "EX_pi_e",
            "EX_so4_e",
            "EX_k_e",
            "EX_mg2_e",
            "EX_fe2_e",
            "EX_fe3_e",
            "EX_na1_e",
            "EX_h_e",
            "EX_h2o_e",
            "EX_co2_e",
            "EX_o2_e",
            "EX_zn2_e",
            "EX_mn2_e",
            "EX_cu2_e",
            "EX_cobalt2_e",
        )
    ]
    for aa in AMINO_ACID_EXCHANGES:
        exchanges.append(
            ExchangeBound(
                aa,
                DEFAULT_CARBON_UPTAKE,
                (
                    "PARTIAL proxy: free amino-acid exchanges stand in for peptide / "
                    "amino-acid fraction of tryptone + yeast extract "
                    "(Lee SI LB recipe); uptake capped at iMO1056 default carbon "
                    "convention (-10) — not a measured extract uptake rate; "
                    "not a true complex-medium reconstruction"
                ),
                recipe_component="tryptone + yeast extract (amino-acid proxy)",
                recipe_concentration="Lee SI: 10 g/L tryptone, 5 g/L yeast extract",
                notes=(
                    "Complex extracts have no single exchange in iMO1056; "
                    "unbounded AA uptake yields unphysical growth rates"
                ),
            )
        )
    return MediumSpec(
        medium_id="LB_approx_lee2015",
        label="PARTIAL",
        display_name="LB_approx (Lee 2015 rich medium)",
        citation=(
            "Lee SA et al. (2015) PNAS 112(16):5189-5194. "
            "DOI 10.1073/pnas.1422186112"
        ),
        locator=(
            "Lee SI Materials and Methods — Growth Media: "
            "'LB agar (per liter): 10 g tryptone, 5 g yeast extract, 8 g NaCl, "
            "15 g Bacto agar'"
        ),
        strain_context="MPAO1",
        exchanges=tuple(exchanges),
        unmodeled_components=(
            "yeast extract (undefined complex; NO exchange — not claimed as modeled)",
            "tryptone (undefined peptides; NO exchange — only AA proxy used)",
            "Bacto agar",
            "non-amino-acid extract components (vitamins, nucleobases, lipids, etc.)",
        ),
        carbon_source_exchange="",
        electron_acceptor_exchange="EX_o2_e",
        notes=(
            "Sensitivity / approximation case only — not a primary DEFINED "
            "validation medium. Do not cite as true LB. No EX_glc_e added "
            "(glucose is not in the Lee LB recipe)."
        ),
    )


def iter_batch_a_media() -> Tuple[MediumSpec, ...]:
    """Batch A DEFINED media for the PAO1-first path (no M9 — no READY_ONLY M9 study)."""
    return (build_mops_pyruvate_lee(), build_mops_succinate_turner())


def iter_batch_b_media() -> Tuple[MediumSpec, ...]:
    return (build_lb_approx_lee(),)


def iter_implemented_media() -> Tuple[MediumSpec, ...]:
    return iter_batch_a_media() + iter_batch_b_media()


_MEDIA_REGISTRY: Optional[Dict[str, MediumSpec]] = None


def get_medium_registry() -> Dict[str, MediumSpec]:
    global _MEDIA_REGISTRY
    if _MEDIA_REGISTRY is None:
        specs = list(iter_implemented_media())
        for s in specs:
            s.validate()
        _MEDIA_REGISTRY = {s.medium_id: s for s in specs}
    return _MEDIA_REGISTRY


def get_medium(medium_id: str) -> MediumSpec:
    registry = get_medium_registry()
    if medium_id not in registry:
        raise KeyError(
            f"Unknown medium_id {medium_id!r}. Available: {sorted(registry)}"
        )
    return registry[medium_id]


# ---------------------------------------------------------------------------
# Legacy teaching API (kept for compatibility)
# ---------------------------------------------------------------------------

def reset_medium(model: cobra.Model, quiet: bool = False) -> cobra.Model:
    """Block all uptake (set negative exchange lower bounds to 0)."""
    for rxn in model.exchanges:
        if rxn.lower_bound < 0:
            rxn.lower_bound = 0.0
    if not quiet:
        print("[OK] Medium reset - all uptake blocked")
    return model


def set_medium(
    model: cobra.Model,
    carbon_source: str,
    electron_acceptor: str,
    carbon_uptake: float = -10.0,
    acceptor_uptake: float = -20.0,
    additional_uptake: Optional[Dict[str, float]] = None,
    quiet: bool = False,
) -> cobra.Model:
    """Legacy helper: reset then open carbon + acceptor (+ optional extras)."""
    reset_medium(model, quiet=quiet)

    try:
        carbon_rxn = model.reactions.get_by_id(carbon_source)
        carbon_rxn.lower_bound = carbon_uptake
        if not quiet:
            print(f"[OK] Carbon source: {carbon_source} ({carbon_uptake} mmol/gDW/h)")
    except KeyError as exc:
        raise ValueError(f"Carbon source reaction '{carbon_source}' not found!") from exc

    try:
        acceptor_rxn = model.reactions.get_by_id(electron_acceptor)
        acceptor_rxn.lower_bound = acceptor_uptake
        if not quiet:
            print(f"[OK] Electron acceptor: {electron_acceptor} ({acceptor_uptake} mmol/gDW/h)")
    except KeyError as exc:
        raise ValueError(
            f"Acceptor reaction '{electron_acceptor}' not found!"
        ) from exc

    if additional_uptake:
        for rxn_id, bound in additional_uptake.items():
            try:
                rxn = model.reactions.get_by_id(rxn_id)
                rxn.lower_bound = bound
                if not quiet:
                    print(f"  + {rxn_id}: {bound} mmol/gDW/h")
            except KeyError:
                if not quiet:
                    print(f"  [WARN] Reaction '{rxn_id}' not found - skipping")

    return model


def get_current_medium(model: cobra.Model, threshold: float = -1e-6) -> Dict[str, float]:
    """Return exchange ids with uptake allowed (lower bound < threshold)."""
    return {
        rxn.id: rxn.lower_bound
        for rxn in model.exchanges
        if rxn.lower_bound < threshold
    }


def create_condition(
    condition_id: str,
    carbon_name: str,
    carbon_ex: str,
    acceptor_name: str,
    acceptor_ex: str,
    carbon_uptake: float = -10.0,
    acceptor_uptake: float = -20.0,
) -> dict:
    """Legacy condition dict helper."""
    return {
        "id": condition_id,
        "carbon_name": carbon_name,
        "carbon_ex": carbon_ex,
        "acceptor_name": acceptor_name,
        "acceptor_ex": acceptor_ex,
        "carbon_uptake": carbon_uptake,
        "acceptor_uptake": acceptor_uptake,
    }


def apply_condition(model: cobra.Model, condition: dict, quiet: bool = False) -> cobra.Model:
    """Apply a legacy condition dict."""
    if not quiet:
        print(f"\nApplying condition: {condition['id']}")
    return set_medium(
        model,
        carbon_source=condition["carbon_ex"],
        electron_acceptor=condition["acceptor_ex"],
        carbon_uptake=condition["carbon_uptake"],
        acceptor_uptake=condition["acceptor_uptake"],
        quiet=quiet,
    )


# ---------------------------------------------------------------------------
# Documented MediumSpec API
# ---------------------------------------------------------------------------

class UnsourcedBoundError(ValueError):
    """Raised when an exchange bound lacks provenance."""


def apply_medium(
    model: cobra.Model,
    medium: MediumSpec | str,
    *,
    quiet: bool = False,
    require_all_exchanges: bool = True,
) -> cobra.Model:
    """
    Reset uptake and apply a documented MediumSpec.

    Parameters
    ----------
    model :
        COBRA model (modified in place).
    medium :
        MediumSpec or medium_id string.
    require_all_exchanges :
        If True, missing exchange ids raise; if False, skip with a warning list.
    """
    spec = get_medium(medium) if isinstance(medium, str) else medium
    spec.validate()

    reset_medium(model, quiet=True)
    missing: List[str] = []
    for e in spec.exchanges:
        if not e.bound_source or e.bound_source.startswith("PENDING"):
            raise UnsourcedBoundError(
                f"{spec.medium_id}: refusing unsourced bound for {e.exchange_id}"
            )
        try:
            rxn = model.reactions.get_by_id(e.exchange_id)
        except KeyError:
            missing.append(e.exchange_id)
            continue
        rxn.lower_bound = float(e.lower_bound)

    if missing:
        msg = (
            f"{spec.medium_id}: exchanges not in model: {missing}. "
            "Do not invent replacements."
        )
        if require_all_exchanges:
            raise KeyError(msg)
        if not quiet:
            print(f"[WARN] {msg}")

    if not quiet:
        print(
            f"[OK] Applied medium {spec.medium_id} [{spec.label}] "
            f"({len(spec.exchanges) - len(missing)} exchanges)"
        )
    return model


def medium_to_frame(spec: MediumSpec) -> pd.DataFrame:
    """Tabular exchange provenance for one medium."""
    rows = []
    for e in spec.exchanges:
        rows.append(
            {
                "medium_id": spec.medium_id,
                "label": spec.label,
                "display_name": spec.display_name,
                "strain_context": spec.strain_context,
                "citation": spec.citation,
                "locator": spec.locator,
                "exchange_id": e.exchange_id,
                "lower_bound": e.lower_bound,
                "bound_source": e.bound_source,
                "recipe_component": e.recipe_component,
                "recipe_concentration": e.recipe_concentration,
                "exchange_notes": e.notes,
                "carbon_source_exchange": spec.carbon_source_exchange,
                "electron_acceptor_exchange": spec.electron_acceptor_exchange,
                "medium_notes": spec.notes,
            }
        )
    return pd.DataFrame(rows)


def unmodeled_to_frame(spec: MediumSpec) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "medium_id": spec.medium_id,
                "label": spec.label,
                "unmodeled_component": c,
            }
            for c in spec.unmodeled_components
        ]
    )


def export_media_tables(
    out_dir: Path | str,
    media: Optional[Sequence[MediumSpec]] = None,
) -> Dict[str, Path]:
    """
    Write derived medium tables under ``data/processed/conditions/`` (or given dir).

    Returns paths of written files.
    """
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    specs = list(media) if media is not None else list(iter_implemented_media())
    for s in specs:
        s.validate()

    exchanges = pd.concat([medium_to_frame(s) for s in specs], ignore_index=True)
    unmodeled = pd.concat([unmodeled_to_frame(s) for s in specs], ignore_index=True)
    summary = pd.DataFrame(
        [
            {
                "medium_id": s.medium_id,
                "label": s.label,
                "display_name": s.display_name,
                "strain_context": s.strain_context,
                "n_exchanges": len(s.exchanges),
                "n_unmodeled": len(s.unmodeled_components),
                "carbon_source_exchange": s.carbon_source_exchange,
                "electron_acceptor_exchange": s.electron_acceptor_exchange,
                "citation": s.citation,
                "locator": s.locator,
            }
            for s in specs
        ]
    )

    paths = {
        "exchanges": out / "media_exchanges.csv",
        "unmodeled": out / "media_unmodeled_components.csv",
        "summary": out / "media_summary.csv",
    }
    exchanges.to_csv(paths["exchanges"], index=False)
    unmodeled.to_csv(paths["unmodeled"], index=False)
    summary.to_csv(paths["summary"], index=False)

    # Per-medium JSON-like CSV of exchange→bound (simple durable companion)
    for s in specs:
        frame = medium_to_frame(s)
        frame.to_csv(out / f"{s.medium_id}_exchanges.csv", index=False)

    return paths


def wildtype_growth(
    model: cobra.Model,
    medium: MediumSpec | str,
    *,
    quiet: bool = True,
) -> Tuple[str, float]:
    """Apply medium on a model copy and return (solver_status, objective_value)."""
    spec = get_medium(medium) if isinstance(medium, str) else medium
    m = model.copy()
    apply_medium(m, spec, quiet=quiet)
    sol = m.optimize()
    value = float(sol.objective_value) if sol.objective_value is not None else float("nan")
    return sol.status, value

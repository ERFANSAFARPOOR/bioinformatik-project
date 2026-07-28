"""
Research utilities for iMO1056 (PAO1) metabolic modeling.

Prefer importing from submodules directly in research notebooks/scripts.
This package exports the stable public surface used by notebooks 04/05.
"""

__version__ = "1.0.0"

from .load_model import load_model, save_model, get_model_summary
from .fba_utils import set_biomass_reaction, run_fba
from .medium import (
    set_medium,
    reset_medium,
    apply_medium,
    get_medium,
    get_medium_registry,
    iter_implemented_media,
)
from .gene_essentiality import analyze_gene_essentiality
from .mapping import extract_gene_reaction_mapping

__all__ = [
    "load_model",
    "save_model",
    "get_model_summary",
    "set_biomass_reaction",
    "run_fba",
    "set_medium",
    "reset_medium",
    "apply_medium",
    "get_medium",
    "get_medium_registry",
    "iter_implemented_media",
    "analyze_gene_essentiality",
    "extract_gene_reaction_mapping",
]

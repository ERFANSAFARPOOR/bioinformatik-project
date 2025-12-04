"""
Metabolic Modeling Education Package

A clean, educational package for learning metabolic modeling with COBRApy.
This package provides simple, well-documented functions for:
- Loading and saving models
- Running FBA simulations
- Analyzing gene essentiality
- Managing growth media
- Extracting gene-reaction mappings
"""

__version__ = "1.0.0"
__author__ = "Metabolic Modeling Education Team"

# Make key functions easily accessible
from .model_io import load_model, save_model
from .fba_utils import set_biomass_reaction, run_fba
from .medium import set_medium, reset_medium
from .gene_essentiality import analyze_gene_essentiality
from .mapping import extract_gene_reaction_mapping

__all__ = [
    'load_model',
    'save_model',
    'set_biomass_reaction',
    'run_fba',
    'set_medium',
    'reset_medium',
    'analyze_gene_essentiality',
    'extract_gene_reaction_mapping',
]

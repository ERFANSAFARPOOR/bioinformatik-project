"""
FBA Utilities Module

This module contains functions for running Flux Balance Analysis (FBA).
FBA is a mathematical approach to predict metabolic fluxes through a network.
"""

from typing import List
import cobra
from cobra.core import Reaction


def find_biomass_reactions(model: cobra.Model) -> List[Reaction]:
    """
    Find reactions that likely represent biomass production.
    
    Most metabolic models have a "biomass" reaction that represents cell growth.
    This function searches for reactions with "biomass" in their ID.
    
    Parameters
    ----------
    model : cobra.Model
        The metabolic model to search
    
    Returns
    -------
    List[Reaction]
        List of reactions containing "biomass" in their ID
    
    Example
    -------
    >>> biomass_rxns = find_biomass_reactions(model)
    >>> for rxn in biomass_rxns:
    ...     print(rxn.id, "-", rxn.name)
    """
    # Search for reactions with "biomass" in the ID (case-insensitive)
    biomass_candidates = [
        rxn for rxn in model.reactions
        if "biomass" in rxn.id.lower()
    ]
    
    if not biomass_candidates:
        print("⚠ No biomass reactions found!")
        print("  You may need to identify the growth reaction manually.")
    else:
        print(f"Found {len(biomass_candidates)} biomass reaction(s):")
        for rxn in biomass_candidates:
            print(f"  - {rxn.id}: {rxn.name}")
    
    return biomass_candidates


def set_biomass_reaction(model: cobra.Model, biomass_id: str) -> cobra.Model:
    """
    Set the biomass reaction as the optimization objective.
    
    In FBA, we typically maximize biomass production (cell growth).
    This function sets which reaction represents biomass.
    
    Parameters
    ----------
    model : cobra.Model
        The metabolic model
    biomass_id : str
        ID of the biomass reaction
    
    Returns
    -------
    cobra.Model
        The model with updated objective (same object, modified in place)
    
    Example
    -------
    >>> model = set_biomass_reaction(model, "BIOMASS_PAO")
    >>> print(f"Objective: {model.objective.expression}")
    """
    try:
        # Get the biomass reaction by its ID
        biomass_rxn = model.reactions.get_by_id(biomass_id)
        
        # Set it as the objective
        model.objective = biomass_rxn
        
        print(f"✓ Objective set to: {biomass_rxn.id}")
        print(f"  Reaction: {biomass_rxn.name}")
        print(f"  Direction: {biomass_rxn.lower_bound} ≤ flux ≤ {biomass_rxn.upper_bound}")
        
    except KeyError:
        raise ValueError(f"Reaction '{biomass_id}' not found in model!")
    
    return model


def run_fba(model: cobra.Model, verbose: bool = True) -> cobra.Solution:
    """
    Run Flux Balance Analysis on the model.
    
    FBA finds the optimal flux distribution that maximizes the objective
    (usually biomass production) while satisfying all constraints.
    
    Parameters
    ----------
    model : cobra.Model
        The metabolic model to optimize
    verbose : bool, default=True
        Whether to print results
    
    Returns
    -------
    cobra.Solution
        The optimization solution containing fluxes
    
    Example
    -------
    >>> solution = run_fba(model)
    >>> print(f"Growth rate: {solution.objective_value:.4f}")
    >>> print(f"Status: {solution.status}")
    """
    # Optimize the model
    solution = model.optimize()
    
    if verbose:
        # Check if optimization was successful
        if solution.status == "optimal":
            print(f"✓ FBA successful!")
            print(f"  Objective value: {solution.objective_value:.6f}")
            print(f"  Status: {solution.status}")
        else:
            print(f"⚠ FBA failed!")
            print(f"  Status: {solution.status}")
            print(f"  Objective value: {solution.objective_value}")
    
    return solution


def get_active_reactions(solution: cobra.Solution, threshold: float = 1e-6) -> List[str]:
    """
    Get reactions that are carrying flux in the solution.
    
    Parameters
    ----------
    solution : cobra.Solution
        The FBA solution
    threshold : float, default=1e-6
        Minimum absolute flux value to consider a reaction "active"
    
    Returns
    -------
    List[str]
        List of reaction IDs with non-zero flux
    
    Example
    -------
    >>> active = get_active_reactions(solution, threshold=1e-3)
    >>> print(f"Active reactions: {len(active)}")
    """
    # Find reactions with absolute flux above threshold
    active = [
        rxn_id for rxn_id, flux in solution.fluxes.items()
        if abs(flux) > threshold
    ]
    
    return active


def get_exchange_fluxes(solution: cobra.Solution, model: cobra.Model) -> dict:
    """
    Extract fluxes for all exchange reactions.
    
    Exchange reactions represent uptake/secretion of metabolites.
    Negative flux = uptake, Positive flux = secretion
    
    Parameters
    ----------
    solution : cobra.Solution
        The FBA solution
    model : cobra.Model
        The metabolic model
    
    Returns
    -------
    dict
        Dictionary mapping exchange reaction IDs to their fluxes
    
    Example
    -------
    >>> exchanges = get_exchange_fluxes(solution, model)
    >>> for rxn_id, flux in exchanges.items():
    ...     if abs(flux) > 0.01:
    ...         print(f"{rxn_id}: {flux:.3f}")
    """
    exchange_fluxes = {}
    
    for rxn in model.exchanges:
        flux = solution.fluxes[rxn.id]
        if abs(flux) > 1e-9:  # Only include non-zero fluxes
            exchange_fluxes[rxn.id] = flux
    
    return exchange_fluxes

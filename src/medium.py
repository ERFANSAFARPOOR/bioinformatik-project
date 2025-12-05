"""
Medium Management Module

This module handles setting up different growth media (environmental conditions).
The medium determines what nutrients are available to the organism.
"""

import cobra
from typing import Dict, Optional


def reset_medium(model: cobra.Model) -> cobra.Model:
    """
    Reset the growth medium by blocking all uptake reactions.
    
    This sets all exchange reaction lower bounds to 0, preventing any uptake.
    Use this to start with a clean slate before adding specific nutrients.
    
    Parameters
    ----------
    model : cobra.Model
        The metabolic model
    
    Returns
    -------
    cobra.Model
        The model with reset medium (modified in place)
    
    Example
    -------
    >>> model = reset_medium(model)
    >>> # Now the model has no nutrients - add what you need
    """
    # Block all uptake by setting lower bounds to 0
    # Exchange reactions have negative lower bounds for uptake
    for rxn in model.exchanges:
        if rxn.lower_bound < 0:
            rxn.lower_bound = 0.0
    
    print("✓ Medium reset - all uptake blocked")
    return model


def set_medium(
    model: cobra.Model,
    carbon_source: str,
    electron_acceptor: str,
    carbon_uptake: float = -10.0,
    acceptor_uptake: float = -20.0,
    additional_uptake: Optional[Dict[str, float]] = None
) -> cobra.Model:
    """
    Set up a growth medium with specified carbon source and electron acceptor.
    
    Negative values indicate uptake (material entering the cell).
    Positive values indicate secretion (material leaving the cell).
    
    Parameters
    ----------
    model : cobra.Model
        The metabolic model
    carbon_source : str
        ID of the carbon source exchange reaction (e.g., "EX_glc__D_e")
    electron_acceptor : str
        ID of the electron acceptor exchange reaction (e.g., "EX_o2_e")
    carbon_uptake : float, default=-10.0
        Maximum uptake rate for carbon source (mmol/gDW/h)
    acceptor_uptake : float, default=-20.0
        Maximum uptake rate for electron acceptor (mmol/gDW/h)
    additional_uptake : dict, optional
        Additional exchange reactions to open {reaction_id: lower_bound}
    
    Returns
    -------
    cobra.Model
        The model with configured medium (modified in place)
    
    Example
    -------
    >>> # Set glucose + oxygen medium
    >>> model = set_medium(
    ...     model,
    ...     carbon_source="EX_glc__D_e",
    ...     electron_acceptor="EX_o2_e"
    ... )
    """
    # First reset the medium
    reset_medium(model)
    
    # Set carbon source uptake
    try:
        carbon_rxn = model.reactions.get_by_id(carbon_source)
        carbon_rxn.lower_bound = carbon_uptake
        print(f"✓ Carbon source: {carbon_source} ({carbon_uptake} mmol/gDW/h)")
    except KeyError:
        raise ValueError(f"Carbon source reaction '{carbon_source}' not found!")
    
    # Set electron acceptor uptake
    try:
        acceptor_rxn = model.reactions.get_by_id(electron_acceptor)
        acceptor_rxn.lower_bound = acceptor_uptake
        print(f"✓ Electron acceptor: {electron_acceptor} ({acceptor_uptake} mmol/gDW/h)")
    except KeyError:
        raise ValueError(f"Acceptor reaction '{electron_acceptor}' not found!")
    
    # Set any additional uptake reactions
    if additional_uptake:
        for rxn_id, bound in additional_uptake.items():
            try:
                rxn = model.reactions.get_by_id(rxn_id)
                rxn.lower_bound = bound
                print(f"  + {rxn_id}: {bound} mmol/gDW/h")
            except KeyError:
                print(f"  ⚠ Reaction '{rxn_id}' not found - skipping")
    
    return model


def get_current_medium(model: cobra.Model, threshold: float = -1e-6) -> Dict[str, float]:
    """
    Get the currently configured growth medium.
    
    Returns all exchange reactions that allow uptake.
    
    Parameters
    ----------
    model : cobra.Model
        The metabolic model
    threshold : float, default=-1e-6
        Minimum uptake rate to include (negative number)
    
    Returns
    -------
    dict
        Dictionary mapping exchange reaction IDs to their lower bounds
    
    Example
    -------
    >>> medium = get_current_medium(model)
    >>> for rxn_id, uptake in medium.items():
    ...     print(f"{rxn_id}: {uptake} mmol/gDW/h")
    """
    current_medium = {}
    
    for rxn in model.exchanges:
        # Check if uptake is allowed (negative lower bound)
        if rxn.lower_bound < threshold:
            current_medium[rxn.id] = rxn.lower_bound
    
    return current_medium


def create_condition(
    condition_id: str,
    carbon_name: str,
    carbon_ex: str,
    acceptor_name: str,
    acceptor_ex: str,
    carbon_uptake: float = -10.0,
    acceptor_uptake: float = -20.0
) -> dict:
    """
    Create a condition dictionary for organizing multiple environments.
    
    This is a helper function to organize experimental conditions.
    
    Parameters
    ----------
    condition_id : str
        Unique identifier for this condition (e.g., "glucose_oxygen")
    carbon_name : str
        Human-readable name of carbon source (e.g., "glucose")
    carbon_ex : str
        Exchange reaction ID for carbon source
    acceptor_name : str
        Human-readable name of acceptor (e.g., "oxygen")
    acceptor_ex : str
        Exchange reaction ID for acceptor
    carbon_uptake : float, default=-10.0
        Carbon uptake rate
    acceptor_uptake : float, default=-20.0
        Acceptor uptake rate
    
    Returns
    -------
    dict
        Condition specification dictionary
    
    Example
    -------
    >>> condition = create_condition(
    ...     "glucose_oxygen",
    ...     "glucose", "EX_glc__D_e",
    ...     "oxygen", "EX_o2_e"
    ... )
    """
    return {
        'id': condition_id,
        'carbon_name': carbon_name,
        'carbon_ex': carbon_ex,
        'acceptor_name': acceptor_name,
        'acceptor_ex': acceptor_ex,
        'carbon_uptake': carbon_uptake,
        'acceptor_uptake': acceptor_uptake
    }


def apply_condition(model: cobra.Model, condition: dict) -> cobra.Model:
    """
    Apply a condition dictionary to a model.
    
    Parameters
    ----------
    model : cobra.Model
        The metabolic model
    condition : dict
        Condition specification (from create_condition)
    
    Returns
    -------
    cobra.Model
        The model with applied condition
    
    Example
    -------
    >>> condition = create_condition(...)
    >>> model = apply_condition(model, condition)
    """
    print(f"\nApplying condition: {condition['id']}")
    
    return set_medium(
        model,
        carbon_source=condition['carbon_ex'],
        electron_acceptor=condition['acceptor_ex'],
        carbon_uptake=condition['carbon_uptake'],
        acceptor_uptake=condition['acceptor_uptake']
    )

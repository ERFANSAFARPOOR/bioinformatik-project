"""
Model I/O Module

This module handles loading and saving genome-scale metabolic models.
SBML (Systems Biology Markup Language) is the standard format for metabolic models.
"""

from pathlib import Path
import cobra
from cobra.io import read_sbml_model, write_sbml_model


def load_model(path: str) -> cobra.Model:
    """
    Load a genome-scale metabolic model from an SBML file.
    
    SBML files contain:
    - All reactions and their stoichiometry
    - All metabolites and their compartments
    - Gene-Protein-Reaction (GPR) associations
    - Reaction bounds (constraints)
    
    Parameters
    ----------
    path : str
        Path to the SBML file (usually ends with .xml or .sbml)
    
    Returns
    -------
    cobra.Model
        The loaded metabolic model object
    
    Example
    -------
    >>> model = load_model("models/my_model.xml")
    >>> print(f"Loaded {len(model.reactions)} reactions")
    """
    # Convert to Path object for better path handling
    model_path = Path(path)
    
    # Check if file exists
    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found: {path}")
    
    # Load the SBML model using COBRApy
    print(f"Loading model from: {path}")
    model = read_sbml_model(str(model_path))
    
    # Print basic model information
    print(f"✓ Model loaded: {model.id}")
    print(f"  - Reactions:   {len(model.reactions)}")
    print(f"  - Metabolites: {len(model.metabolites)}")
    print(f"  - Genes:       {len(model.genes)}")
    
    return model


def save_model(model: cobra.Model, path: str) -> None:
    """
    Save a metabolic model to an SBML file.
    
    This is useful when you've modified a model and want to save your changes.
    
    Parameters
    ----------
    model : cobra.Model
        The metabolic model to save
    path : str
        Where to save the file (usually ends with .xml or .sbml)
    
    Returns
    -------
    None
    
    Example
    -------
    >>> modified_model = model.copy()
    >>> # ... make some changes ...
    >>> save_model(modified_model, "models/modified_model.xml")
    """
    # Convert to Path object
    output_path = Path(path)
    
    # Create parent directories if they don't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Save the model
    write_sbml_model(model, str(output_path))
    print(f"✓ Model saved to: {path}")


def get_model_summary(model: cobra.Model) -> dict:
    """
    Get a summary of model statistics.
    
    This is helpful for quickly understanding a model's size and content.
    
    Parameters
    ----------
    model : cobra.Model
        The metabolic model to summarize
    
    Returns
    -------
    dict
        Dictionary containing model statistics
    
    Example
    -------
    >>> summary = get_model_summary(model)
    >>> print(f"Exchange reactions: {summary['exchange_reactions']}")
    """
    return {
        'model_id': model.id,
        'reactions': len(model.reactions),
        'metabolites': len(model.metabolites),
        'genes': len(model.genes),
        'exchange_reactions': len(model.exchanges),
        'compartments': len(model.compartments)
    }

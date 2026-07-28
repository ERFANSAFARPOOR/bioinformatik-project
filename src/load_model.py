"""
load_model.py

Utilities for loading, inspecting, and saving the published
Pseudomonas aeruginosa PAO1 iMO1056 genome-scale metabolic model.

Scientific scope
----------------
This module is responsible only for model I/O.

Responsibilities
----------------
- Load the published SBML model
- Save modified SBML models
- Report basic model statistics

Non-responsibilities
--------------------
- Medium reconstruction
- Flux Balance Analysis (FBA)
- Gene essentiality prediction
- Experimental validation
- Any modification of the model

The returned cobra.Model object is used by downstream research modules.
"""

from __future__ import annotations

from pathlib import Path

import cobra
from cobra.io import read_sbml_model, write_sbml_model



# Project paths


PROJECT_ROOT = Path(__file__).resolve().parents[1]

MODEL_FILE = (
    PROJECT_ROOT
    / "models"
    / "paeruginosa_MODEL1507180020.xml"
)



# Load model


def load_model(model_path: str | Path = MODEL_FILE) -> cobra.Model:
    """
    Load the published iMO1056 metabolic model.

    Parameters
    ----------
    model_path : str | Path, optional
        Path to the SBML model.
        Defaults to the published project model.

    Returns
    -------
    cobra.Model
        Loaded COBRA model.

    Raises
    ------
    FileNotFoundError
        If the model file does not exist.
    """

    model_path = Path(model_path)

    if not model_path.exists():
        raise FileNotFoundError(
            f"Model file not found:\n{model_path}"
        )

    return read_sbml_model(str(model_path))



# Save model


def save_model(
    model: cobra.Model,
    output_path: str | Path,
) -> None:
    """
    Save a metabolic model as an SBML file.

    Parameters
    ----------
    model : cobra.Model
        Model to save.

    output_path : str | Path
        Destination SBML file.

    Raises
    ------
    ValueError
        If the file extension is not .xml or .sbml.
    """

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if output_path.suffix.lower() not in {".xml", ".sbml"}:
        raise ValueError(
            "Output file must have extension '.xml' or '.sbml'."
        )

    write_sbml_model(model, str(output_path))


# Model summary


def get_model_summary(
    model: cobra.Model,
) -> dict[str, int | str]:
    """
    Return basic model statistics.

    Parameters
    ----------
    model : cobra.Model

    Returns
    -------
    dict
        Dictionary containing basic model information.
    """

    return {
        "model_id": model.id,
        "model_name": model.name,
        "reactions": len(model.reactions),
        "metabolites": len(model.metabolites),
        "genes": len(model.genes),
        "exchange_reactions": len(model.exchanges),
        "compartments": len(model.compartments),
    }


# Standalone execution


if __name__ == "__main__":

    print("=" * 60)
    print("Loading published iMO1056 model")
    print("=" * 60)

    model = load_model()

    print("\nModel loaded successfully.\n")

    summary = get_model_summary(model)

    for key, value in summary.items():
        print(f"{key:20}: {value}")

    print("\nObjective:")

    try:
        print(model.objective.expression)
    except Exception:
        print(model.objective)

    print("\nDone.")
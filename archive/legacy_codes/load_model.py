"""
load_model.py

Load the published Pseudomonas aeruginosa PAO1 iMO1056 model.

Scientific scope
----------------
This module only loads the SBML model.

No media reconstruction.
No FBA.
No gene essentiality.
No modifications.

The returned cobra.Model is used by the downstream research modules.
"""

from pathlib import Path
import cobra


# ---------------------------------------------------------------------
# Project root
# ---------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]


# ---------------------------------------------------------------------
# Model location
# ---------------------------------------------------------------------

MODEL_FILE = (
    PROJECT_ROOT
    / "models"
    / "paeruginosa_MODEL1507180020.xml"
)


# ---------------------------------------------------------------------
# Load model
# ---------------------------------------------------------------------

def load_model(model_path=MODEL_FILE):
    """
    Load the published iMO1056 SBML model.

    Parameters
    ----------
    model_path : str | pathlib.Path

    Returns
    -------
    cobra.Model
    """

    model_path = Path(model_path)

    if not model_path.exists():
        raise FileNotFoundError(
            f"\nModel file not found:\n{model_path}"
        )

    model = cobra.io.read_sbml_model(model_path)

    return model


# ---------------------------------------------------------------------
# Standalone execution
# ---------------------------------------------------------------------

if __name__ == "__main__":

    print("=" * 60)
    print("Loading iMO1056 model")
    print("=" * 60)

    model = load_model()

    print("\nModel loaded successfully\n")

    print(f"Model ID      : {model.id}")
    print(f"Model Name    : {model.name}")
    print(f"Reactions     : {len(model.reactions)}")
    print(f"Metabolites   : {len(model.metabolites)}")
    print(f"Genes         : {len(model.genes)}")

    print("\nObjective reaction:")

    try:
        print(model.objective.expression)
    except Exception:
        print(model.objective)

    print("\nDone.")
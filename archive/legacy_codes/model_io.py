"""
Model I/O Module

This module handles loading and saving genome-scale metabolic models.

SBML (Systems Biology Markup Language) is the standard format for metabolic models.
However, models may also appear in JSON, MATLAB (.mat), or Pickle formats.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, List, Optional, Dict, Callable, Tuple
import pickle

import cobra
from cobra.io import (
    read_sbml_model,
    write_sbml_model,
    load_json_model,
    load_matlab_model,
)


# Supported model file extensions for auto-discovery and loading
SUPPORTED_MODEL_EXTENSIONS = {
    ".xml",
    ".sbml",
    ".json",
    ".mat",
    ".pkl",
    ".pickle",
}


def find_model_files(
    directory: str | Path = ".",
    extensions: Optional[Iterable[str]] = None,
    recursive: bool = False,
) -> List[Path]:
    """
    Find metabolic model files in a directory.

    Parameters
    ----------
    directory : str | Path
        Directory to search in.
    extensions : Iterable[str] | None
        File extensions to include. If None, uses SUPPORTED_MODEL_EXTENSIONS.
        Example: [".xml", ".json"]
    recursive : bool
        If True, searches subdirectories as well.

    Returns
    -------
    List[Path]
        Sorted list of matching model file paths.

    Example
    -------
    >>> files = find_model_files("models", recursive=True)
    >>> for f in files:
    ...     print(f)
    """
    base = Path(directory)
    if not base.exists():
        raise FileNotFoundError(f"Directory not found: {base}")

    exts = set(e.lower() for e in (extensions or SUPPORTED_MODEL_EXTENSIONS))

    pattern = "**/*" if recursive else "*"
    results: List[Path] = []
    for p in base.glob(pattern):
        if p.is_file() and p.suffix.lower() in exts:
            results.append(p)

    return sorted(results)


def _load_by_extension(model_path: Path) -> cobra.Model:
    """
    Internal helper that loads a model based on file extension.
    """
    ext = model_path.suffix.lower()

    if ext in {".xml", ".sbml"}:
        return read_sbml_model(str(model_path))

    if ext == ".json":
        return load_json_model(str(model_path))

    if ext == ".mat":
        return load_matlab_model(str(model_path))

    if ext in {".pkl", ".pickle"}:
        with open(model_path, "rb") as f:
            obj = pickle.load(f)
        if not isinstance(obj, cobra.Model):
            raise TypeError(
                f"Pickle file did not contain a cobra.Model. Got: {type(obj).__name__}"
            )
        return obj

    raise ValueError(
        f"Unsupported model extension: {ext}. Supported: {sorted(SUPPORTED_MODEL_EXTENSIONS)}"
    )


def load_model(path: str) -> cobra.Model:
    """
    Load a genome-scale metabolic model from a file.

    Supported formats
    -----------------
    - SBML:  .xml, .sbml
    - JSON:  .json
    - MATLAB: .mat
    - Pickle: .pkl, .pickle (must contain a cobra.Model)

    SBML files contain:
    - All reactions and their stoichiometry
    - All metabolites and their compartments
    - Gene-Protein-Reaction (GPR) associations
    - Reaction bounds (constraints)

    Parameters
    ----------
    path : str
        Path to the model file.

    Returns
    -------
    cobra.Model
        The loaded metabolic model object

    Example
    -------
    >>> model = load_model("models/my_model.xml")
    >>> print(f"Loaded {len(model.reactions)} reactions")
    """
    model_path = Path(path)

    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found: {path}")

    print(f"Loading model from: {model_path}")
    model = _load_by_extension(model_path)

    print(f"✓ Model loaded: {model.id}")
    print(f"  - Reactions:   {len(model.reactions)}")
    print(f"  - Metabolites: {len(model.metabolites)}")
    print(f"  - Genes:       {len(model.genes)}")

    return model


def load_model_auto(
    candidates: Optional[Iterable[str | Path]] = None,
    directory: str | Path = ".",
    recursive: bool = False,
) -> cobra.Model:
    """
    Automatically load the first compatible model found.

    How it works
    ------------
    1) If `candidates` is provided, tries them in order.
    2) Otherwise, searches `directory` for supported model file extensions.
    3) Tries each file until one loads successfully.
    4) If all fail, raises a FileNotFoundError with details.

    Parameters
    ----------
    candidates : Iterable[str | Path] | None
        Ordered list of file paths to try.
        Example: ["e_coli_core.xml", "model.json", "model.mat"]
    directory : str | Path
        Directory to search if candidates is None.
    recursive : bool
        If True, searches subdirectories as well.

    Returns
    -------
    cobra.Model
        First successfully loaded model.

    Example
    -------
    >>> model = load_model_auto(["model.xml", "model.json"])
    >>> model = load_model_auto(directory="models", recursive=True)
    """
    tried: List[str] = []
    last_error: Optional[Exception] = None

    if candidates is not None:
        paths = [Path(p) for p in candidates]
    else:
        paths = find_model_files(directory=directory, recursive=recursive)

    if not paths:
        raise FileNotFoundError(
            f"No candidate model files found in: {Path(directory).resolve()}"
        )

    for p in paths:
        tried.append(str(p))
        if not p.exists():
            print(f"• Skipping missing file: {p}")
            continue

        try:
            print(f"Trying: {p}")
            model = load_model(str(p))
            return model
        except Exception as e:
            last_error = e
            print(f"  Failed: {type(e).__name__}: {e}")

    raise FileNotFoundError(
        "No compatible model file could be loaded automatically.\n"
        + f"Tried these candidate files: {tried}\n"
        + f"Last error: {type(last_error).__name__ if last_error else 'None'}: {last_error}"
    )


def save_model(model: cobra.Model, path: str) -> None:
    """
    Save a metabolic model to a file.

    Supported formats for saving
    ----------------------------
    - SBML: .xml, .sbml

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
    >>> save_model(modified_model, "models/modified_model.xml")
    """
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    ext = output_path.suffix.lower()
    if ext not in {".xml", ".sbml"}:
        raise ValueError(
            f"Saving is currently supported only for SBML (.xml, .sbml). Got: {ext}"
        )

    write_sbml_model(model, str(output_path))
    print(f"✓ Model saved to: {path}")


def get_model_summary(model: cobra.Model) -> dict:
    """
    Get a summary of model statistics.

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
        "model_id": model.id,
        "reactions": len(model.reactions),
        "metabolites": len(model.metabolites),
        "genes": len(model.genes),
        "exchange_reactions": len(model.exchanges),
        "compartments": len(model.compartments),
    }

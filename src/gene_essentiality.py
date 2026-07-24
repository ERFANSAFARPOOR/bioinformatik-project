"""
Gene Essentiality Analysis Module

This module performs single gene deletion analysis to identify essential genes.
A gene is "essential" if deleting it severely reduces or eliminates growth.
"""

import pandas as pd
import cobra
from cobra.flux_analysis import single_gene_deletion
from typing import Set, Optional


def analyze_gene_essentiality(
    model: cobra.Model,
    threshold_ratio: float = 0.01,
    processes: int = 3
) -> pd.DataFrame:
    """
    Perform single gene deletion analysis to identify essential genes.
    
    This function:
    1. Runs FBA on the wild-type model
    2. Deletes each gene one at a time
    3. Runs FBA after each deletion
    4. Compares knockout growth to wild-type growth
    5. Classifies genes as essential or non-essential
    
    Parameters
    ----------
    model : cobra.Model
        The metabolic model to analyze
    threshold_ratio : float, default=0.01
        Growth ratio threshold for essentiality.
        If (knockout_growth / wildtype_growth) < threshold_ratio, gene is essential.
        Default of 0.01 means growth must drop below 1% of wild-type.
    processes : int, default=1
        Number of parallel processes to use (1 = no parallelization)
    
    Returns
    -------
    pd.DataFrame
        DataFrame with columns:
        - gene_id: Gene identifier
        - wildtype_growth: Growth rate before deletion
        - knockout_growth: Growth rate after deletion
        - growth_ratio: knockout_growth / wildtype_growth
        - is_essential: Boolean indicating essentiality
    
    Example
    -------
    >>> results = analyze_gene_essentiality(model, threshold_ratio=0.01)
    >>> essential = results[results['is_essential']]
    >>> print(f"Found {len(essential)} essential genes")
    """
    print("Starting gene essentiality analysis...")
    print(f"  Total genes to test: {len(model.genes)}")
    print(f"  Essentiality threshold: {threshold_ratio * 100}% of wild-type growth")
    
    # Get wild-type growth rate
    wt_solution = model.optimize()
    wt_growth = wt_solution.objective_value
    
    if wt_growth is None or wt_growth <= 1e-9:
        raise ValueError(
            "Wild-type model has no growth! "
            "Check medium conditions and objective function."
        )
    
    print(f"  Wild-type growth rate: {wt_growth:.6f}")
    
    # Perform single gene deletions
    print("\nPerforming gene deletions...")
    deletion_results = single_gene_deletion(
        model,
        model.genes,
        processes=processes
    )
    
    # Build results DataFrame
    results_list = []
    
    for idx, row in deletion_results.iterrows():
        gene_id = row['ids']
        knockout_growth = row['growth']
        
        # Handle cases where growth is None or NaN
        if knockout_growth is None or pd.isna(knockout_growth):
            knockout_growth = 0.0
        
        # Calculate growth ratio
        growth_ratio = knockout_growth / wt_growth if wt_growth > 0 else 0.0
        
        # Determine if gene is essential
        is_essential = growth_ratio < threshold_ratio
        
        results_list.append({
            'gene_id': gene_id,
            'wildtype_growth': wt_growth,
            'knockout_growth': knockout_growth,
            'growth_ratio': growth_ratio,
            'is_essential': is_essential
        })
    
    # Create DataFrame
    results_df = pd.DataFrame(results_list)
    
    # Print summary
    n_essential = results_df['is_essential'].sum()
    n_total = len(results_df)
    print("\n[OK] Analysis complete!")
    print(f"  Essential genes: {n_essential} / {n_total} ({n_essential/n_total*100:.1f}%)")
    
    return results_df


def get_essential_genes(results: pd.DataFrame) -> Set[str]:
    """
    Extract a clean and standardized set of essential gene IDs from the 
    gene essentiality analysis results.

    During single-gene deletion analysis, the 'gene_id' column in the
    results DataFrame may contain either:
      - a single gene ID as a string (e.g. "PA1234"), or
      - a Python `set` of multiple gene IDs when GPR rules involve
        several genes.

    Python sets are not hashable, so they cannot be directly inserted
    into another set. This function unwraps any set-valued entries and
    returns a flat set containing only string gene IDs.

    Parameters
    ----------
    results : pd.DataFrame
        Output of analyze_gene_essentiality(), with at least the columns
        'gene_id' and 'is_essential'.

    Returns
    -------
    Set[str]
        A Python set of essential gene IDs (all as strings).
    """
    # We only keep rows that are essential
    essential_df = results[results["is_essential"]]

    clean_ids: Set[str] = set()

    for gid in essential_df["gene_id"]:
        # If its value was set (multiple genes together)
        if isinstance(gid, set):
            for g in gid:
                clean_ids.add(str(g))
        else:
            clean_ids.add(str(gid))

    return clean_ids


def analyze_essentiality_for_medium(
    model: cobra.Model,
    medium_id: str,
    threshold_ratio: float = 0.01,
    processes: int = 1,
) -> pd.DataFrame:
    """
    Apply a documented MediumSpec and run single-gene deletion.

    Returns a DataFrame with cleaned gene_id strings plus medium metadata
    columns. Does **not** compute validation metrics.
    """
    from .medium import apply_medium, get_medium

    spec = get_medium(medium_id)
    model_copy = model.copy()
    apply_medium(model_copy, spec, quiet=True)
    results = analyze_gene_essentiality(
        model_copy,
        threshold_ratio=threshold_ratio,
        processes=processes,
    )
    # Clean gene_id set-repr → string
    cleaned = []
    for gid in results["gene_id"]:
        if isinstance(gid, set):
            cleaned.append(";".join(sorted(str(g) for g in gid)))
        else:
            s = str(gid)
            if s.startswith("{") and s.endswith("}"):
                inner = s.strip("{}").replace("'", "").replace('"', "")
                cleaned.append(inner)
            else:
                cleaned.append(s)
    out = results.copy()
    out["gene_id"] = cleaned
    out["medium_id"] = spec.medium_id
    out["medium_label"] = spec.label
    out["threshold_ratio"] = threshold_ratio
    return out


def compare_essentiality_across_conditions(
    model: cobra.Model,
    conditions: list,
    threshold_ratio: float = 0.01
) -> dict:
    """
    Analyze gene essentiality across multiple environmental conditions.
    
    Parameters
    ----------
    model : cobra.Model
        The base metabolic model
    conditions : list
        List of condition dictionaries (from medium.create_condition)
    threshold_ratio : float, default=0.01
        Essentiality threshold
    
    Returns
    -------
    dict
        Dictionary mapping condition IDs to sets of essential genes
    
    Example
    -------
    >>> conditions = [
    ...     create_condition("glc_o2", "glucose", "EX_glc__D_e", "oxygen", "EX_o2_e"),
    ...     create_condition("glc_no3", "glucose", "EX_glc__D_e", "nitrate", "EX_no3_e")
    ... ]
    >>> results = compare_essentiality_across_conditions(model, conditions)
    """
    from .medium import apply_condition
    
    essentiality_by_condition = {}
    
    for condition in conditions:
        print(f"\n{'='*60}")
        print(f"Analyzing condition: {condition['id']}")
        print(f"{'='*60}")
        
        # Create a copy of the model for this condition
        model_copy = model.copy()
        
        # Apply the condition
        apply_condition(model_copy, condition)
        
        # Analyze essentiality
        results = analyze_gene_essentiality(
            model_copy,
            threshold_ratio=threshold_ratio
        )
        
        # Extract essential genes
        essential = get_essential_genes(results)
        essentiality_by_condition[condition['id']] = essential
    
    return essentiality_by_condition


def save_essentiality_results(
    results: pd.DataFrame,
    output_path: str,
    condition_name: Optional[str] = None
) -> None:
    """
    Save gene essentiality results to a CSV file.
    
    Parameters
    ----------
    results : pd.DataFrame
        Results from analyze_gene_essentiality()
    output_path : str
        Path where to save the CSV file
    condition_name : str, optional
        Name of the condition (will be added as a column)
    
    Returns
    -------
    None
    
    Example
    -------
    >>> results = analyze_gene_essentiality(model)
    >>> save_essentiality_results(
    ...     results,
    ...     "results/essentiality/glucose_oxygen.csv",
    ...     "glucose_oxygen"
    ... )
    """
    from pathlib import Path
    
    # Add condition name if provided
    if condition_name:
        results = results.copy()
        results['condition'] = condition_name
    
    # Create output directory if needed
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Save to CSV
    results.to_csv(output_path, index=False)
    print(f"[OK] Results saved to: {output_path}")

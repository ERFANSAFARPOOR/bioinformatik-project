"""
Gene-Reaction Mapping Module

This module extracts and analyzes Gene-Protein-Reaction (GPR) associations.
GPR rules show which genes encode the enzymes that catalyze each reaction.
"""

import pandas as pd
import cobra
from typing import List, Dict, Set


def extract_gene_reaction_mapping(model: cobra.Model) -> pd.DataFrame:
    """
    Extract all gene-reaction associations from the model.
    
    Each reaction may be associated with:
    - Zero genes (spontaneous or unknown)
    - One gene (single enzyme)
    - Multiple genes (enzyme complex or isozymes)
    
    Parameters
    ----------
    model : cobra.Model
        The metabolic model
    
    Returns
    -------
    pd.DataFrame
        DataFrame with columns:
        - reaction_id: Reaction identifier
        - reaction_name: Human-readable reaction name
        - gene_ids: Comma-separated list of gene IDs
        - n_genes: Number of genes associated
        - gpr_rule: Gene-Protein-Reaction rule (logical expression)
    
    Example
    -------
    >>> mapping = extract_gene_reaction_mapping(model)
    >>> # Find reactions with multiple genes
    >>> multi_gene = mapping[mapping['n_genes'] > 1]
    """
    mapping_data = []
    
    for rxn in model.reactions:
        # Get all genes associated with this reaction
        genes = list(rxn.genes)
        gene_ids = [g.id for g in genes]
        
        # Get the GPR rule (logical expression)
        gpr_rule = rxn.gene_reaction_rule
        
        mapping_data.append({
            'reaction_id': rxn.id,
            'reaction_name': rxn.name,
            'gene_ids': ', '.join(gene_ids) if gene_ids else '',
            'n_genes': len(gene_ids),
            'gpr_rule': gpr_rule if gpr_rule else '',
            'subsystem': rxn.subsystem if rxn.subsystem else ''
        })
    
    df = pd.DataFrame(mapping_data)
    
    print(f"✓ Extracted gene-reaction mapping")
    print(f"  Total reactions: {len(df)}")
    print(f"  Reactions with genes: {(df['n_genes'] > 0).sum()}")
    print(f"  Reactions without genes: {(df['n_genes'] == 0).sum()}")
    
    return df


def get_reactions_for_gene(model: cobra.Model, gene_id: str) -> List[cobra.Reaction]:
    """
    Find all reactions associated with a specific gene.
    
    Parameters
    ----------
    model : cobra.Model
        The metabolic model
    gene_id : str
        Gene identifier
    
    Returns
    -------
    list
        List of reactions associated with this gene
    
    Example
    -------
    >>> reactions = get_reactions_for_gene(model, "b0001")
    >>> for rxn in reactions:
    ...     print(f"{rxn.id}: {rxn.name}")
    """
    try:
        gene = model.genes.get_by_id(gene_id)
        return list(gene.reactions)
    except KeyError:
        raise ValueError(f"Gene '{gene_id}' not found in model")


def get_genes_for_reaction(model: cobra.Model, reaction_id: str) -> List[cobra.Gene]:
    """
    Find all genes associated with a specific reaction.
    
    Parameters
    ----------
    model : cobra.Model
        The metabolic model
    reaction_id : str
        Reaction identifier
    
    Returns
    -------
    list
        List of genes associated with this reaction
    
    Example
    -------
    >>> genes = get_genes_for_reaction(model, "PGI")
    >>> for gene in genes:
    ...     print(gene.id)
    """
    try:
        reaction = model.reactions.get_by_id(reaction_id)
        return list(reaction.genes)
    except KeyError:
        raise ValueError(f"Reaction '{reaction_id}' not found in model")


def parse_gpr_rule(gpr_string: str) -> Dict[str, any]:
    """
    Parse a GPR rule to understand its structure.
    
    GPR rules use Boolean logic:
    - "and" indicates enzyme complex (all genes required)
    - "or" indicates isozymes (any gene sufficient)
    
    Parameters
    ----------
    gpr_string : str
        The GPR rule string
    
    Returns
    -------
    dict
        Dictionary with parsed information:
        - has_and: Contains AND relationships (enzyme complex)
        - has_or: Contains OR relationships (isozymes)
        - genes: List of all gene IDs in the rule
    
    Example
    -------
    >>> info = parse_gpr_rule("(geneA and geneB) or geneC")
    >>> print(info['has_and'])  # True
    >>> print(info['has_or'])   # True
    >>> print(info['genes'])    # ['geneA', 'geneB', 'geneC']
    """
    if not gpr_string:
        return {
            'has_and': False,
            'has_or': False,
            'genes': []
        }
    
    # Check for AND and OR operators
    has_and = ' and ' in gpr_string.lower()
    has_or = ' or ' in gpr_string.lower()
    
    # Extract gene IDs (simple approach - removes parentheses and operators)
    import re
    genes = re.findall(r'\b[a-zA-Z0-9_]+\b', gpr_string)
    # Remove 'and' and 'or' from the list
    genes = [g for g in genes if g.lower() not in ['and', 'or']]
    
    return {
        'has_and': has_and,
        'has_or': has_or,
        'genes': genes
    }


def analyze_gpr_complexity(model: cobra.Model) -> pd.DataFrame:
    """
    Analyze the complexity of GPR associations in the model.
    
    Parameters
    ----------
    model : cobra.Model
        The metabolic model
    
    Returns
    -------
    pd.DataFrame
        Summary statistics about GPR complexity
    
    Example
    -------
    >>> stats = analyze_gpr_complexity(model)
    >>> print(stats)
    """
    complexities = []
    
    for rxn in model.reactions:
        gpr = rxn.gene_reaction_rule
        parsed = parse_gpr_rule(gpr)
        
        # Classify complexity
        if not parsed['genes']:
            complexity = 'no_genes'
        elif len(parsed['genes']) == 1:
            complexity = 'single_gene'
        elif parsed['has_and'] and parsed['has_or']:
            complexity = 'complex_both'
        elif parsed['has_and']:
            complexity = 'enzyme_complex'
        elif parsed['has_or']:
            complexity = 'isozymes'
        else:
            complexity = 'multiple_genes'
        
        complexities.append({
            'reaction_id': rxn.id,
            'n_genes': len(parsed['genes']),
            'complexity': complexity,
            'gpr_rule': gpr
        })
    
    df = pd.DataFrame(complexities)
    
    # Print summary
    print("\nGPR Complexity Summary:")
    print(df['complexity'].value_counts().to_string())
    
    return df


def create_gene_reaction_network(model: cobra.Model) -> tuple:
    """
    Create a bipartite network of genes and reactions.
    
    Returns two DataFrames suitable for network analysis:
    - Nodes: genes and reactions
    - Edges: gene-reaction associations
    
    Parameters
    ----------
    model : cobra.Model
        The metabolic model
    
    Returns
    -------
    tuple
        (nodes_df, edges_df) containing network structure
    
    Example
    -------
    >>> nodes, edges = create_gene_reaction_network(model)
    >>> print(f"Nodes: {len(nodes)}, Edges: {len(edges)}")
    """
    nodes = []
    edges = []
    
    # Add gene nodes
    for gene in model.genes:
        nodes.append({
            'id': gene.id,
            'name': gene.name,
            'type': 'gene'
        })
    
    # Add reaction nodes and edges
    for rxn in model.reactions:
        nodes.append({
            'id': rxn.id,
            'name': rxn.name,
            'type': 'reaction'
        })
        
        # Add edges between genes and this reaction
        for gene in rxn.genes:
            edges.append({
                'source': gene.id,
                'target': rxn.id,
                'type': 'catalyzes'
            })
    
    nodes_df = pd.DataFrame(nodes)
    edges_df = pd.DataFrame(edges)
    
    print(f"✓ Network created:")
    print(f"  Nodes: {len(nodes_df)} ({(nodes_df['type']=='gene').sum()} genes, {(nodes_df['type']=='reaction').sum()} reactions)")
    print(f"  Edges: {len(edges_df)}")
    
    return nodes_df, edges_df

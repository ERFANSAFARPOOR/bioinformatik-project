# Notebook Creation Guide

Due to file size constraints, the three main notebooks should be created as follows:

## Notebook 1: 01_basic_fba.ipynb

Create a Jupyter notebook with these key sections:

**Cells**:
1. **Markdown**: Title and learning objectives
2. **Code**: Import libraries (cobra, pandas, matplotlib, src modules)
3. **Code**: Load model using `load_model()`
4. **Code**: Inspect model structure (print reactions, metabolites, genes)
5. **Code**: Find biomass reactions using `find_biomass_reactions()`
6. **Code**: Set biomass as objective using `set_biomass_reaction()`
7. **Code**: Run FBA using `run_fba()`
8. **Code**: Visualize flux distribution (bar plot of top fluxes)
9. **Code**: Inspect exchange fluxes (uptake vs secretion)
10. **Markdown**: Summary and next steps

## Notebook 2: 02_gene_essentiality.ipynb

**Cells**:
1. **Markdown**: Introduction to gene essentiality
2. **Code**: Import libraries
3. **Code**: Load model
4. **Code**: Set up medium (reset + set carbon source + acceptor)
5. **Code**: Run essentiality analysis using `analyze_gene_essentiality()`
6. **Code**: Extract essential genes using `get_essential_genes()`
7. **Code**: Save results to CSV
8. **Code**: Create visualizations (pie chart of essential vs non-essential)
9. **Code**: Analyze multiple conditions (loop through different media)
10. **Code**: Create Venn diagram comparing conditions
11. **Markdown**: Interpretation and conclusions

## Notebook 3: 03_experimental_comparison.ipynb

**Cells**:
1. **Markdown**: Model validation introduction
2. **Code**: Import libraries
3. **Code**: Load model and run essentiality analysis
4. **Code**: Load experimental data (provide template CSV format)
5. **Code**: Compare predicted vs experimental essential genes
6. **Code**: Calculate metrics (sensitivity, specificity, accuracy)
7. **Code**: Create confusion matrix visualization
8. **Code**: Create Venn diagram of agreement/disagreement
9. **Code**: Analyze discrepancies (false positives vs false negatives)
10. **Markdown**: Discussion of why predictions differ from experiments

## Quick Creation Method

Use Jupyter's interface:
1. Create new notebook
2. Add markdown and code cells
3. Follow the structure above
4. Test each cell
5. Add explanatory comments

Or create programmatically using the templates provided in this repository.

# Teaching Notes for Instructors

## Overview

This repository is designed as a self-contained module for teaching metabolic modeling. Students progress through three notebooks over approximately 2-4 hours.

## Target Audience

- **Undergraduate** students in biochemistry, biology, or bioengineering
- **Graduate** students beginning research in systems biology
- **Researchers** new to constraint-based modeling

**Prerequisites**: Basic biology and high school mathematics. No prior programming experience required, though helpful.

## Learning Objectives

### Notebook 1: Basic FBA

**Objectives:**
1. Understand the concept of genome-scale metabolic models
2. Learn the basic principles of Flux Balance Analysis
3. Interpret FBA results (growth rates, fluxes)
4. Visualize metabolic activity

**Key Concepts:**
- SBML format and model structure
- Steady-state assumption
- Linear programming optimization
- Exchange reactions
- Biomass reaction

**Common Questions:**
- *"Why is the growth rate in 1/h?"* → It represents the exponential growth rate constant
- *"What do negative fluxes mean?"* → For exchange reactions, negative = uptake
- *"Why is FBA useful?"* → Fast, doesn't require kinetic parameters, genome-scale

**Estimated Time**: 45-60 minutes

### Notebook 2: Gene Essentiality

**Objectives:**
1. Understand gene essentiality and its applications
2. Perform computational gene knockout experiments
3. Classify genes based on phenotype
4. Understand context-dependence of essentiality

**Key Concepts:**
- Gene-Protein-Reaction (GPR) associations
- Single gene deletion
- Essentiality threshold
- Growth ratio
- Lethal vs. non-lethal knockouts

**Common Questions:**
- *"Why are most genes non-essential?"* → Genetic redundancy, alternative pathways
- *"How do we choose the threshold?"* → Depends on application; 1% is common but adjustable
- *"How long does this take?"* → Scales with model size; large models may take 10-30 minutes

**Estimated Time**: 45-60 minutes

### Notebook 3: Experimental Comparison

**Objectives:**
1. Compare computational predictions with experimental data
2. Calculate validation metrics
3. Understand sources of prediction errors
4. Interpret model limitations

**Key Concepts:**
- Confusion matrix (TP, FP, TN, FN)
- Precision, recall, accuracy
- Model validation
- Discrepancy analysis

**Common Questions:**
- *"Why don't predictions match perfectly?"* → Models are simplified; missing reactions, regulation
- *"Is high accuracy always good?"* → No - high TN rate can inflate accuracy for imbalanced datasets
- *"What's a good F1 score?"* → Depends on application; 0.7-0.9 is typical for metabolic models

**Estimated Time**: 45-60 minutes

## Teaching Tips

### Before the Session

1. **Test the environment**: Ensure `environment.yml` works on your system
2. **Prepare a model**: Have an appropriate model ready (E. coli iML1515 is great for beginners)
3. **Check execution times**: Run notebook 2 ahead of time to estimate duration
4. **Prepare experimental data**: For notebook 3, have real or simulated data ready

### During the Session

1. **Start with motivation**: Why study metabolism computationally?
2. **Run cells together**: Walk through each cell as a group first
3. **Encourage exploration**: After each notebook, allow time for students to modify parameters
4. **Address errors positively**: Use errors as teaching moments
5. **Connect to biology**: Constantly relate back to biological concepts

### After the Session

1. **Provide extension exercises**: See below
2. **Encourage questions**: Make yourself available for follow-up
3. **Collect feedback**: Ask what worked and what didn't

## Extension Exercises

### Beginner Level

1. **Different organisms**: Load a different model and compare growth rates
2. **Medium effects**: Modify nutrient availability in Notebook 1
3. **Threshold exploration**: Try different essentiality thresholds in Notebook 2
4. **Visualization**: Create additional plots in any notebook

### Intermediate Level

1. **Multi-condition essentiality**: Extend Notebook 2 to test multiple growth conditions
2. **Pathway analysis**: Identify essential genes by metabolic pathway
3. **Gene ranking**: Rank genes by their impact on growth
4. **Custom medium**: Design a minimal medium that supports growth

### Advanced Level

1. **Model refinement**: Use FP/FN analysis to suggest model improvements
2. **Pairwise deletions**: Implement double gene deletion analysis
3. **Flux variability analysis**: Add FVA to Notebook 1
4. **Integration with omics**: Incorporate gene expression data (requires additional tools)

## Assessment Ideas

### Formative Assessment
- Code comprehension questions during notebooks
- Prediction exercises ("What will happen if...?")
- Concept mapping activities

### Summative Assessment
- **Mini-project**: Analyze a new organism's model
- **Written report**: Validate a model using provided experimental data
- **Presentation**: Explain FBA to a non-expert audience
- **Code modification**: Add a new analysis function to `src/`

## Common Technical Issues

### Installation Problems
- **Conda conflicts**: Use a fresh environment
- **Version mismatches**: Ensure Python 3.10+
- **Windows path issues**: Use forward slashes in paths

### Runtime Problems
- **Memory errors**: Large models may need 4+ GB RAM
- **Slow execution**: Gene deletion scales O(n) with gene count
- **Import errors**: Ensure `sys.path.insert(0, '..')` is in each notebook

### Scientific Issues
- **No growth**: Check medium configuration
- **Unexpected essentiality**: Could indicate model gaps
- **Low validation metrics**: Normal for incomplete models

## Adapting This Material

### For Different Audiences

**High school**: 
- Focus on Notebook 1 only
- Use simple visualizations
- Emphasize biological concepts over mathematics

**Undergraduate**: 
- All three notebooks
- Add extension exercises
- Connect to course material (biochemistry, microbiology)

**Graduate/Research**: 
- Move quickly through notebooks
- Focus on advanced exercises
- Discuss current research applications

### For Different Course Contexts

**Biochemistry course**: 
- Emphasize pathway connections
- Relate to metabolism lectures

**Systems biology course**: 
- Position as one of several modeling approaches
- Compare with kinetic models

**Bioinformatics course**: 
- Focus on data structures and algorithms
- Emphasize code quality and documentation

## Resources for Instructors

### Background Reading
1. Orth et al. (2010) "What is flux balance analysis?" Nature Biotechnology
2. Palsson (2015) "Systems Biology: Constraint-based Reconstruction and Analysis"
3. Lewis et al. (2012) "Omic data from evolved E. coli are consistent with computed optimal growth from genome-scale models" Molecular Systems Biology

### Online Resources
- COBRApy documentation: https://cobrapy.readthedocs.io/
- BiGG Models database: http://bigg.ucsd.edu/
- Systems Biology course materials: https://systemsbiology.ucsd.edu/

### Example Models
- *E. coli* iML1515: Excellent for teaching, well-validated
- *S. cerevisiae* Yeast8: Eukaryotic example
- *P. aeruginosa*: Pathogen example (as used in original notebook)

## Feedback and Improvements

This is a living document. Please contribute:
- Successful teaching strategies
- Student feedback
- Additional exercises
- Bug fixes
- Clarifications

---

*Last updated: [Current Date]*
*For questions: [Contact Information]*

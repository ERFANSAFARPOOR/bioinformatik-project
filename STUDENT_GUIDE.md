# Student Guide: Getting Started with Metabolic Modeling

Welcome! This guide will help you work through the metabolic modeling notebooks.

## What is Metabolic Modeling?

Metabolic modeling is like creating a blueprint of how cells produce energy and build the molecules they need to survive. Instead of doing expensive lab experiments, we use computers to predict what happens when we change nutrients, delete genes, or modify the organism.

Think of it as **SimCity for metabolism** - we simulate the cellular factory!

## What You Need

### Required Software
- **Anaconda** (or Miniconda) - a Python package manager
  - Download from: https://www.anaconda.com/products/distribution
  - Install following the on-screen instructions

### Required Knowledge
- **Python basics**: variables, functions, loops (we'll explain as we go)
- **Biology basics**: what are genes, proteins, reactions
- **Willingness to experiment**: It's okay to make mistakes!

## Setup Instructions

### Step 1: Download the Repository

Option A: If you have Git
```bash
git clone <repository-url>
cd metabolic-modeling-education
```

Option B: Download as ZIP
1. Click the green "Code" button on GitHub
2. Select "Download ZIP"
3. Extract to a folder on your computer
4. Open a terminal/command prompt in that folder

### Step 2: Create the Environment

This installs all the required software:

```bash
conda env create -f environment.yml
```

This might take 5-10 minutes. Go get a coffee! ☕

### Step 3: Activate the Environment

**Every time** you work on these notebooks, run:

```bash
conda activate metabolic-modeling
```

You should see `(metabolic-modeling)` appear in your terminal prompt.

### Step 4: Get a Model

You need an SBML model file (`.xml`). 

**Option 1: Use a pre-built model**
- Visit http://bigg.ucsd.edu/
- Download *E. coli* iML1515 (recommended for beginners)
- Save to the `models/` folder

**Option 2: Use the example model**
- The notebooks reference `MODEL1507180020_url.xml`
- This is *Pseudomonas aeruginosa*
- Place your model file in `models/` folder

### Step 5: Start Jupyter

```bash
jupyter notebook
```

This opens a web browser. Navigate to `notebooks/` and open `01_basic_fba.ipynb`.

## How to Use the Notebooks

### Navigation

- **Cells**: Each notebook is divided into cells
- **Running cells**: Click a cell, then press `Shift + Enter`
- **Order matters**: Run cells from top to bottom

### Reading the Code

Don't worry if you don't understand every line! Focus on:
1. **What** the code does (explained in text cells)
2. **Why** we're doing it
3. **What** the results mean

### Making Changes

**Encouraged**:
- Change parameters (numbers)
- Try different plots
- Add your own analysis

**Not recommended (yet)**:
- Changing function names
- Removing import statements
- Skipping cells

### Getting Help

If something doesn't work:

1. **Read the error message** - it often tells you what's wrong
2. **Check the cell above** - did you run all previous cells?
3. **Restart the kernel** - Click "Kernel → Restart & Clear Output"
4. **Check the README** - troubleshooting section
5. **Ask for help** - include the error message!

## Working Through the Notebooks

### Notebook 1: Basic FBA (Start Here!)

**Time needed**: 45-60 minutes

**What you'll do**:
- Load a metabolic model
- Explore what's inside
- Run a simulation
- Visualize the results

**Success looks like**:
- You get a growth rate (a number > 0)
- You see plots of metabolic activity
- You understand what FBA predicts

**If stuck**:
- Make sure your model file path is correct
- Check that you set the correct biomass reaction ID
- Ensure the model has a growth medium configured

### Notebook 2: Gene Essentiality

**Time needed**: 45-60 minutes

**What you'll do**:
- Delete genes one at a time (computationally!)
- See which genes are essential for growth
- Visualize the results

**Success looks like**:
- You get a list of essential genes
- You understand why some genes are essential
- You can save results to a file

**If stuck**:
- This notebook can be slow - be patient!
- If it takes more than 30 minutes, consider using a smaller model
- Make sure you completed Notebook 1 first

### Notebook 3: Experimental Comparison

**Time needed**: 45-60 minutes

**What you'll do**:
- Compare predictions with experimental data
- Calculate how accurate the model is
- Understand why predictions differ from reality

**Success looks like**:
- You create a Venn diagram showing overlap
- You calculate precision and recall
- You understand model limitations

**If stuck**:
- You need experimental data for this
- The notebook includes simulated data as an example
- For real analysis, provide your own data

## Tips for Success

### Before You Start
- [ ] Read the README fully
- [ ] Install and test the environment
- [ ] Have a model file ready
- [ ] Set aside 2-3 hours of uninterrupted time

### While Working
- [ ] Run cells in order, top to bottom
- [ ] Read all the text cells, not just code
- [ ] Look at every plot - what does it tell you?
- [ ] Experiment with changing parameters
- [ ] Take notes on what you learn

### After Each Notebook
- [ ] Summarize what you learned in your own words
- [ ] Try one extension exercise
- [ ] Think of questions for discussion
- [ ] Save your work!

## Understanding the Results

### What is a "Good" Result?

**For FBA (Notebook 1)**:
- Growth rate > 0 (cell can grow)
- Growth rate ~0.5-1.0 1/h is typical for *E. coli*
- Values depend heavily on the medium

**For Essentiality (Notebook 2)**:
- 10-30% of genes are typically essential
- Core metabolism genes often essential
- Many genes are non-essential (backup pathways exist)

**For Validation (Notebook 3)**:
- Precision ~0.5-0.9 is typical
- Recall ~0.5-0.9 is typical  
- Perfect prediction is impossible (models are simplified!)

### Common Patterns

**Pattern**: Most reactions have low flux
- **Meaning**: Cells use only a subset of their metabolic capabilities

**Pattern**: Few genes are essential
- **Meaning**: Evolution favors redundancy

**Pattern**: Model predictions aren't perfect
- **Meaning**: Models are useful approximations, not exact representations

## Troubleshooting

### "ModuleNotFoundError: No module named 'cobra'"
→ Activate the conda environment: `conda activate metabolic-modeling`

### "FileNotFoundError: [model file] not found"
→ Check the file path. Use `..` to go up one directory.

### "No growth in FBA"
→ The model needs nutrients. Check if a medium is configured.

### "Gene deletion is taking forever"
→ Large models can take 30+ minutes. This is normal.

### Plots look weird or don't show up
→ Make sure you have `%matplotlib inline` at the top of the notebook

### Something broke and now nothing works
→ Go to "Kernel → Restart & Clear Output" and start from the top

## Going Further

### After Completing All Notebooks

**Want more practice?**
1. Try a different organism's model
2. Test different growth conditions
3. Compare multiple organisms
4. Implement double gene deletions

**Want to learn more?**
1. Read the original FBA paper (see Resources)
2. Explore COBRApy documentation
3. Take a systems biology course
4. Join the metabolic modeling community

**Want to use this for research?**
1. Learn about flux variability analysis
2. Study model refinement techniques
3. Explore metabolic engineering applications
4. Integrate with omics data

### Resources

**Tutorials**:
- COBRApy tutorials: https://cobrapy.readthedocs.io/
- Systems biology videos: [YouTube channel links]

**Papers to read** (in order):
1. "What is flux balance analysis?" (Orth et al. 2010)
2. "Protocol for model reconstruction" (Thiele & Palsson 2010)

**Communities**:
- COBRA community forum
- Systems biology Stack Exchange

## Final Thoughts

**Remember**:
- This is about learning, not perfection
- Errors are opportunities to understand
- Models are tools for thinking, not crystal balls
- Biology is complex - models are simplified
- Ask questions and experiment!

**Most importantly**: Have fun exploring cellular metabolism! 🧬

---

**Need help?** Check the README troubleshooting section or ask your instructor.

**Found a bug?** Please report it so we can improve these materials.

**Enjoyed this?** Share with others interested in systems biology!

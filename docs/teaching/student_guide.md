# Student Guide: Metabolic Modeling with Python

Welcome! This guide will help you get started with metabolic modeling using this repository.

## What is Metabolic Modeling?

Imagine you want to understand how a factory works—what goes in, what comes out, and how raw materials flow through different production lines. **Metabolic modeling** does the same thing for cells!

- **Metabolites** = raw materials (glucose, oxygen, amino acids)
- **Reactions** = production steps (converting glucose to energy)
- **Genes** = instruction manuals (DNA tells cells how to build enzymes)
- **Flux** = flow rate (how fast reactions happen)

## Your Learning Journey

You'll complete three notebooks that build on each other:

### 📗 Notebook 1: Basic FBA (Start Here!)
**What you'll do**: Learn to predict how fast cells grow  
**Time**: ~30-45 minutes  
**Key skill**: Running your first metabolic simulation

### 📘 Notebook 2: Gene Essentiality
**What you'll do**: Discover which genes are critical for survival  
**Time**: ~45-60 minutes  
**Key skill**: Computational gene knockout experiments

### 📙 Notebook 3: Model Validation
**What you'll do**: Compare predictions with real experiments  
**Time**: ~45-60 minutes  
**Key skill**: Scientific model validation

## Getting Started: Step-by-Step

### Step 1: Set Up Your Computer

**Option A: Using Conda (Recommended)**

1. Open your terminal (Mac/Linux) or Anaconda Prompt (Windows)

2. Navigate to this repository:
   ```bash
   cd path/to/metabolic-modeling-education
   ```

3. Create the environment:
   ```bash
   conda env create -f environment.yml
   ```
   ☕ This takes 5-10 minutes. Go grab a coffee!

4. Activate the environment:
   ```bash
   conda activate metabolic-modeling
   ```

**Option B: Using pip**

```bash
pip install cobra pandas matplotlib jupyter matplotlib-venn
```

### Step 2: Get a Model

You need a metabolic model file to work with. Here are your options:

**Option 1: Download from BiGG Models**
1. Visit http://bigg.ucsd.edu/models
2. Choose an organism (start with *E. coli* iML1515 or similar)
3. Download the SBML file
4. Save it as `models/base_model.xml`

**Option 2: Use Your Own Model**
- If you have an SBML model from your research
- Save it in the `models/` folder
- Update the file path in the notebooks

### Step 3: Launch Jupyter

```bash
jupyter notebook
```

Your browser will open with the Jupyter interface. Teaching notebooks `01`/`02`/`03`
are archived under `archive/teaching_notebooks/` (legacy; nb03 metrics are not
scientific results). Start research work with `notebooks/04_media_reconstruction.ipynb`.

## How to Use the Notebooks

### Reading Code Cells

Code cells look like this:
```python
# This is a comment explaining what the code does
model = load_model("models/base_model.xml")  # This loads your model
```

**Tips**:
- Comments start with `#` and explain the code
- You don't need to understand every detail at first
- Focus on what the code *does*, not how

### Running Cells

1. **Click on a cell** to select it
2. **Press Shift + Enter** to run it
3. **Watch for output** below the cell
4. **Proceed to the next cell** when ready

**Important**: Run cells in order! Later cells depend on earlier ones.

### Understanding Output

After running a cell, you'll see output like:

```
✓ Successfully loaded model: iML1515
  - Reactions:   2712
  - Metabolites: 1877
  - Genes:       1516
```

**What this means**:
- ✓ = Success!
- Numbers tell you model size
- If you see errors, read them carefully (they often tell you what's wrong)

## Common Issues and Solutions

### Problem: "ModuleNotFoundError: No module named 'cobra'"

**Solution**: You're not in the right environment
```bash
conda activate metabolic-modeling
```

### Problem: "FileNotFoundError: Model file not found"

**Solution**: Check your model file location
```python
# Make sure this path is correct:
MODEL_PATH = "../models/base_model.xml"  # Relative to notebooks folder
```

### Problem: "Kernel appears to have died"

**Solution**: The model might be too large
- Try a smaller model first
- Restart the kernel: Kernel → Restart
- Make sure you have enough RAM (4GB minimum)

### Problem: Cell takes forever to run

**Solution**: Some operations (like gene deletion) take time
- Be patient! Gene essentiality can take 10-30 minutes
- You'll see progress messages
- Don't interrupt if it's working

### Problem: Confusing error message

**Solution**: 
1. Read the error carefully—it often tells you what's wrong
2. Google the error message
3. Ask your instructor or classmate
4. Check the GitHub issues for this repo

## Tips for Success

### 1. Take Notes!

Add your own markdown cells to document your learning:
- Click on a cell
- Press "M" to convert to markdown
- Type your notes
- Press Shift + Enter to render

### 2. Experiment!

**After completing each notebook, try**:
- Changing parameters (uptake rates, thresholds)
- Using different carbon sources
- Adding your own visualizations
- Exploring the model further

### 3. Ask "Why?"

Don't just run the code—understand it:
- Why is this gene essential?
- Why does growth change with different nutrients?
- Why don't all predictions match experiments?

### 4. Work with Others

Metabolic modeling is collaborative:
- Form study groups
- Discuss results
- Help each other debug
- Share interesting findings

## Understanding Key Concepts

### Flux Balance Analysis (FBA)

**Simple analogy**: Traffic optimization

Imagine a city (cell) with:
- **Roads** = reactions
- **Cars** = metabolites
- **Destinations** = growth/products
- **Traffic flow** = flux

FBA finds the traffic pattern that maximizes the flow to destinations while respecting road capacity and traffic rules.

### Gene Essentiality

**Simple analogy**: Removing parts from a machine

- Remove a critical bolt → machine breaks (essential gene)
- Remove decorative paint → machine still works (non-essential)
- Essentiality depends on conditions (bolt critical for outdoor but not indoor use)

### Model Validation

**Simple analogy**: Weather forecasting

- Model predicts temperature (computational)
- Thermometer measures temperature (experimental)
- Compare to improve forecast (validation)

Perfect agreement is rare but the model is still useful!

## Cheat Sheet

### Common Commands

```python
# Load model
from src.model_io import load_model
model = load_model("path/to/model.xml")

# Run FBA
from src.fba_utils import run_fba
solution = run_fba(model)
growth_rate = solution.objective_value

# Set medium
from src.medium import reset_medium, set_medium
reset_medium(model)
set_medium(model, "EX_glc__D_e", -10.0, "EX_o2_e", -20.0)

# Gene essentiality
from src.gene_essentiality import analyze_gene_essentiality
results = analyze_gene_essentiality(model, threshold_ratio=0.01)
```

### Keyboard Shortcuts in Jupyter

- **Shift + Enter**: Run cell and move to next
- **Ctrl + Enter**: Run cell and stay
- **A**: Insert cell above
- **B**: Insert cell below
- **M**: Convert to markdown
- **Y**: Convert to code
- **D, D**: Delete cell (press D twice)
- **Z**: Undo delete

## Next Steps After Completion

### Beginner Level
- Try different organisms' models
- Explore alternative carbon sources
- Create your own visualizations

### Intermediate Level
- Implement Flux Variability Analysis
- Integrate transcriptomics data
- Design metabolic engineering strategies

### Advanced Level
- Reconstruct a model for a new organism
- Develop new analysis methods
- Contribute to COBRApy development

## Resources for Further Learning

### Documentation
- **COBRApy**: https://cobrapy.readthedocs.io/
- **SBML**: http://sbml.org/
- **BiGG Models**: http://bigg.ucsd.edu/

### Tutorials
- COBRApy tutorials (GitHub)
- Systems Biology textbooks
- Online courses (Coursera, edX)

### Communities
- COBRApy Gitter chat
- Systems Biology Stack Exchange
- Computational Biology subreddit

### Papers (Start Here)
1. Orth et al. (2010) "What is flux balance analysis?" - Excellent introduction
2. Lewis et al. (2012) "Constraining metabolic genotype-phenotype" - Comprehensive review

## Getting Help

If you're stuck:

1. **Check the error message** - often tells you exactly what's wrong
2. **Review the README** - has troubleshooting section
3. **Ask your instructor** - they're there to help!
4. **Check online** - many others have had the same issue
5. **Open a GitHub issue** - if you found a bug

## Academic Integrity

When using this repository for assignments:

**✅ DO**:
- Complete the work yourself
- Discuss concepts with classmates
- Cite this repository in your work
- Ask for help when stuck

**❌ DON'T**:
- Copy code without understanding
- Share complete solutions before deadline
- Present others' work as your own
- Use AI to do the assignment for you

## Acknowledgments

Thank you for using this educational repository! This material was developed to make metabolic modeling accessible to everyone.

**Remember**: Everyone starts as a beginner. Be patient with yourself, ask questions, and enjoy the learning journey!

---

**Need Help?** Contact your instructor or open an issue on GitHub.

**Found this useful?** Star the repository and share with others!

**Good luck and happy modeling!** 🧬🔬✨

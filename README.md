# Metabolic Modeling Education

A clean, beginner-friendly repository for learning genome-scale metabolic modeling with COBRApy.

## 📚 Overview

This repository provides a structured introduction to constraint-based metabolic modeling through three progressive Jupyter notebooks. Each notebook builds on the previous one, guiding you from basic concepts to advanced analysis.

### What You'll Learn

- **Notebook 1**: Basic Flux Balance Analysis (FBA)
  - Load and explore metabolic models
  - Run FBA simulations
  - Visualize metabolic fluxes
  
- **Notebook 2**: Gene Essentiality Analysis
  - Perform single gene deletions
  - Identify essential genes
  - Understand condition-dependent essentiality
  
- **Notebook 3**: Experimental Validation
  - Compare predictions with experimental data
  - Calculate validation metrics
  - Interpret model limitations

## 🗂️ Repository Structure

```
metabolic-modeling-education/
├── README.md                      # This file
├── environment.yml                # Conda environment specification
├── data/                          # Data files
│   ├── experimental/              # Experimental datasets
│   └── omics/                     # Omics data (optional)
├── models/                        # SBML model files
│   └── base_model.xml             # Your metabolic model goes here
├── notebooks/                     # Educational Jupyter notebooks
│   ├── 01_basic_fba.ipynb        # Introduction to FBA
│   ├── 02_gene_essentiality.ipynb # Gene knockout analysis
│   └── 03_experimental_comparison.ipynb # Model validation
├── src/                           # Python modules (reusable code)
│   ├── __init__.py               # Package initialization
│   ├── model_io.py               # Model loading/saving
│   ├── fba_utils.py              # FBA utilities
│   ├── medium.py                 # Growth medium management
│   ├── gene_essentiality.py      # Gene deletion analysis
│   └── mapping.py                # Gene-reaction mapping
├── results/                       # Analysis outputs
│   ├── fba/                      # FBA results
│   ├── essentiality/             # Gene essentiality results
│   ├── mapping/                  # Gene-reaction mappings
│   └── comparison/               # Experimental comparisons
└── docs/                          # Additional documentation
    ├── teaching_notes.md          # Notes for instructors
    └── figures/                   # Figures and diagrams
```

## 🚀 Getting Started

### Prerequisites

- **Anaconda** or **Miniconda** installed
- Basic Python knowledge (variables, functions, loops)
- Basic understanding of cellular metabolism (helpful but not required)

### Installation

1. **Clone or download this repository**

```bash
git clone <repository-url>
cd metabolic-modeling-education
```

2. **Create the conda environment**

```bash
conda env create -f environment.yml
```

This installs:
- Python 3.10+
- COBRApy (metabolic modeling)
- pandas (data analysis)
- matplotlib (plotting)
- jupyter (notebooks)
- matplotlib-venn (Venn diagrams)

3. **Activate the environment**

```bash
conda activate metabolic-modeling
```

4. **Add your model file**

Place your SBML model file (`.xml` or `.sbml`) in the `models/` directory. The example uses `MODEL1507180020_url.xml` (Pseudomonas aeruginosa), but you can use any SBML model.

**Where to find models:**
- [BiGG Models](http://bigg.ucsd.edu/) - curated metabolic models
- [BioModels](https://www.ebi.ac.uk/biomodels/) - biological models repository
- Your own reconstructed model

5. **Launch Jupyter**

```bash
jupyter notebook
```

Navigate to the `notebooks/` folder and start with `01_basic_fba.ipynb`.

## 📖 Learning Path

### For Beginners

1. Start with **Notebook 1** - understand what FBA is and how it works
2. Progress to **Notebook 2** - learn about gene essentiality
3. Complete **Notebook 3** - validate predictions with data

**Time estimate**: 2-4 hours total

### For Instructors

See `docs/teaching_notes.md` for:
- Learning objectives for each notebook
- Common student questions
- Extension exercises
- Assessment ideas

## 🔧 Using the Code Modules

All notebooks use functions from the `src/` package to keep code clean and reusable.

Example:
```python
from src.model_io import load_model
from src.fba_utils import run_fba

# Load a model
model = load_model("models/my_model.xml")

# Run FBA
solution = run_fba(model)
print(f"Growth rate: {solution.objective_value}")
```

### Available Modules

- **`model_io`**: Loading and saving models
- **`fba_utils`**: Running FBA, analyzing fluxes
- **`medium`**: Setting growth conditions
- **`gene_essentiality`**: Gene deletion analysis
- **`mapping`**: Gene-reaction associations

All functions include:
- ✓ Type hints
- ✓ Docstrings with examples
- ✓ Informative print statements
- ✓ Error handling

## 📊 Data Requirements

### Experimental Data Format

For **Notebook 3**, provide experimental data as CSV with these columns:

```csv
gene_id,is_essential
gene001,True
gene002,False
gene003,True
...
```

Place in `data/experimental/`.

## 🐛 Troubleshooting

### Common Issues

**Problem**: `ModuleNotFoundError: No module named 'cobra'`
- **Solution**: Activate the conda environment: `conda activate metabolic-modeling`

**Problem**: Model file not found
- **Solution**: Check the path in the notebook matches your model file location

**Problem**: No growth in FBA
- **Solution**: Check that the model has a valid growth medium configured. See Notebook 1, Step 6.

**Problem**: Gene deletion analysis is slow
- **Solution**: Large models can take time. Consider using `processes=4` to parallelize (if you have multiple CPU cores).

## 🤝 Contributing

This is an educational repository. Contributions welcome:
- Bug fixes
- Additional examples
- Improved documentation
- New teaching materials

## 📚 Additional Resources

### Learning Materials
- [COBRApy Documentation](https://cobrapy.readthedocs.io/)
- [Orth et al. 2010](https://doi.org/10.1038/nbt.1614) - "What is flux balance analysis?"
- [Thiele & Palsson 2010](https://doi.org/10.1038/nprot.2009.203) - Protocol for model reconstruction

### Video Tutorials
- [Systems Biology by Jeff Orth](https://www.youtube.com/watch?v=8QBG9KhN7e8)
- [COBRApy tutorials](https://github.com/opencobra/cobrapy)

## 📄 License

This educational repository is provided as-is for learning purposes.

## 💬 Contact & Support

For questions or issues:
1. Check the troubleshooting section above
2. Review the teaching notes in `docs/`
3. Open an issue on GitHub

---

**Happy modeling! 🧬**

# Quick Start Guide

Get up and running in 5 minutes!

## 3-Step Setup

### Step 1: Create Environment
```bash
conda env create -f environment.yml
conda activate metabolic-modeling
```

### Step 2: Get a Model
Download E. coli iML1515 from http://bigg.ucsd.edu and place in `models/`

### Step 3: Launch
```bash
jupyter notebook
# Open: notebooks/01_basic_fba.ipynb
```

## Update These Lines

```python
MODEL_PATH = "../models/iML1515.xml"
BIOMASS_ID = "BIOMASS_Ec_iML1515_core_75p37M"
```

Done! 🚀

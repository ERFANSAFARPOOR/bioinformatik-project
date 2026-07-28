# Experimental Data Directory

Place experimental gene essentiality datasets here for comparison in Notebook 3.

## Required Format

CSV files with the following columns:

```csv
gene_id,is_essential
PA0001,True
PA0002,False
PA0003,True
...
```

**Columns:**
- `gene_id`: Gene identifier (must match IDs in your model)
- `is_essential`: Boolean (True/False or 1/0)

## Sources

1. **DEG Database**: http://www.essentialgene.org/
2. **Literature**: PubMed search for "[organism] essential genes"
3. **Your own experiments**: High-throughput screening data

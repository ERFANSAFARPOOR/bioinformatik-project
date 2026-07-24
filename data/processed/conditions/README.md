# Processed condition / medium tables

Derived from `src/medium.py` (Batch A DEFINED + `LB_approx` PARTIAL).
Regenerate with:

```bash
C:/Users/pro/anaconda3/envs/reccobra39/python.exe scripts/export_media_tables.py
```

| File | Contents |
|---|---|
| `media_summary.csv` | One row per medium (label, citation, locator, counts) |
| `media_exchanges.csv` | Exchange → bound with provenance |
| `media_unmodeled_components.csv` | Honest gaps (yeast extract, buffers, …) |
| `media_wt_growth.csv` | Measured WT growth (solver output; not invented) |
| `<medium_id>_exchanges.csv` | Per-medium exchange table |

Raw SBML and literature PDFs are never edited here.

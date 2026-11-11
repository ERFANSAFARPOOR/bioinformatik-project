# Processed condition / medium tables

Derived from `src/medium.py` (Batch A DEFINED + `LB_approx` PARTIAL).

**Status reconciled 2026-11-11:** these are implemented computational medium
configurations, not plans or records of wet-lab medium preparation. The exported
WT growth and per-condition gene-deletion predictions already exist.

| medium_id | Representation | WT growth (/h) | Predicted essential / 1054 at 1% |
|---|---|---|---|
| `mops_pyruvate_lee2015` | DEFINED; MPAO1 experimental context | 0.405339 | 173 |
| `mops_succinate_turner2015` | DEFINED; PAO1 comparator context | 0.552803 | 177 |
| `LB_approx_lee2015` | PARTIAL; complex LB components approximated | 14.950548 | 133 |

Counts come from `results/essentiality/condition_essentiality_summary.csv`;
growth values come from `media_wt_growth.csv`. DEFINED denotes a recipe-based
model representation; exchange bounds still include documented modeling
assumptions. `LB_approx` is not physiologically calibrated true LB and is not the
primary validation medium. SCFM2, RPMI and host/growth-arrest conditions remain
separate unfinished reconstruction tasks.

The first real model-vs-experiment binary comparison uses only
`mops_pyruvate_lee2015` and the D-21 Varadarajan2020 reanalysis of Lee2015 labels.
Its metrics are computed, with interpretation/human review pending; this does
not establish validation across all media. See
[`VALIDATION_LABEL_MEDIA_OVERLAP.md`](../../../VALIDATION_LABEL_MEDIA_OVERLAP.md)
and the [V-01 report](../../../project_management/audit/v01_mops_pyruvate/V01_BINARY_VALIDATION_REPORT.md).

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

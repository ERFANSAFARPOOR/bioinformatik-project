# REPRODUCTION AFTER MIGRATION

**Date:** 2026-07-01 · **Branch:** `claude/revival-audit`
**Env:** `reccobra39` (`C:\Users\pro\anaconda3\envs\reccobra39\python.exe`,
Python 3.9.23, cobra 0.29.1, pandas 2.3.2). Verifies that the Cycle-2 repository
reorganization did **not** change any scientific result.

---

## 1. What moved (and why nothing broke)

- The **canonical model path** `models/paeruginosa_MODEL1507180020.xml` was
  **kept in place** (a byte-identical copy was added at `models/raw/`).
- Only **audit/generation scripts** and **legacy docs** were relocated
  (`git mv`); `src/` and `notebooks/` were **not** moved.
- `src/*.py` does **not** hard-code the model path or reference any moved script
  (verified by grep) → no import/path breakage.

## 2. Post-migration checks (all PASS)

| Check | Expected | Result |
|---|---|---|
| Canonical model path loads | yes | PASS |
| Raw model SHA-256 unchanged | `0868a5eb…1212ead` | PASS |
| `models/raw/` copy byte-identical | same SHA | PASS |
| Reactions / metabolites / genes | 1110 / 879 / 1054 | PASS |
| Model identity | `MODEL1507180020`, all genes `PAxxxx` (PAO1), no `PA14_` | PASS |
| Objective | contains `PA_Biomass6_DM` | PASS |
| WT growth (default medium) | 1.0479285528184004 (±1e-6) | PASS (1.0479285528184004) |
| Cleaned predictions rows | 1054 | PASS |
| Predicted essential @1% | 166 | PASS |
| `gene_id` cleaned (`^PA\d+$`) | all | PASS |
| No stray validation-metrics file | none | PASS |

## 3. Test suite

`tests/test_model_and_data.py` (pytest) encodes the above as regression tests.

```
conda run -n reccobra39 python -m pytest tests/ -q
# => 8 passed
```

(pytest 8.4.2 installed **env-scoped** into reccobra39 — test-only dependency;
fold into the env lock at E-03.)

## 4. Notebooks

- Notebook model-load paths are **unchanged** (canonical path preserved), so the
  Phase-A reproduction (`notebooks/reproduced/REPRODUCTION_REPORT.md`) still holds:
  **nb02 reproduces exactly** (166 essential, WT 1.0479285528). The numeric
  invariants nb02 depends on are now pinned by the pytest suite above.
- Known pre-existing follow-ups (unchanged by this cycle): nb01 `BIOMASS_PAO`
  bug (N-01) and kernelspec cleanup (E-04). These were not introduced by the
  migration.

## 5. Conclusion

The reorganization is **behavior-preserving**. Model identity, WT growth, and the
predicted-essentiality result are byte-/value-stable and now regression-tested.
No validation metrics were computed (correctly gated).

# REPOSITORY MIGRATION PLAN

> **STATUS: EXECUTED 2026-07-01 (Cycle 2, decision D-10).** The migration below was
> carried out and verified behavior-preserving (`REPRODUCTION_AFTER_MIGRATION.md`,
> 8 pytest pass). Deviations/remaining items: (a) `results/essentiality/*.csv` NOT
> moved to `results/tables/` — the clean join-ready copy already lives at
> `data/processed/predicted_essentiality_default_medium.csv` (R-02); (b) legacy
> educational docs went to `archive/` (not `docs/`); (c) `conditian/` left
> untouched (untracked); (d) `index.html` → `docs/`. See `WORK_CYCLE_LOG.md`.

A migration map. Originals remain recoverable via git. Executed in Cycle 2 after
notebooks reproduced under the canonical environment (E-02). `git mv` used to
preserve history; raw files **copied** (not moved) into `*/raw/` with the original
kept until the copy was SHA-256-verified.

---

## Target structure
```
models/raw/         models/processed/
data/raw/           data/processed/
papers/
notebooks/
src/                tests/
results/tables/     results/figures/
manuscript/
docs/
archive/
```

## Migration map (current → target)

| Current | Target | Method | Notes |
|---|---|---|---|
| `models/paeruginosa_MODEL1507180020.xml` | `models/raw/` (copy) | copy, keep original path until refs updated | RAW — never edit in place (D-05) |
| (future cleaned model) | `models/processed/` | new | derived only |
| `conditian/juhas2015.pdf` | `papers/juhas2015.pdf` | git mv | per `papers/manifest.csv` |
| `conditian/keith H.pdf` | `papers/turner2015.pdf` | git mv | normalize name |
| `conditian/samuelA.pdf` | `papers/lee2015.pdf` | git mv | |
| `conditian/polsun2019.pdf` | `papers/poulsen2019.pdf` | git mv | |
| `conditian/davidW.pdf` | `papers/basta_growth_arrest.pdf` | git mv | rename after L-02 verify |
| `conditian/corrieR.pdf` | `papers/belanger_host_conditions.pdf` | git mv | rename after L-02 verify |
| `data/experimental/`, `data/omics/` (READMEs) | `data/raw/` + `data/processed/` | reorganize | currently no datasets |
| downloaded supplements (future) | `data/raw/literature/<study>/` | new | provenance + hash |
| `data/processed/*.csv` (this audit) | keep | — | evidence tables |
| `notebooks/01..03.ipynb` | `notebooks/` | keep | re-kernel to reccobra39 first |
| `src/*.py` | `src/` | keep | refactor in Phase B |
| `audit_model.py`, `identify_pdfs.py`, `generate_phasea_data.py`, `show_audit.py` | `scripts/` or `src/audit/` | git mv | read-only audit tools |
| `results/essentiality/*.csv` | `results/tables/` | git mv | clean gene_id first (R-02) |
| (future figures) | `results/figures/` | new | scripted |
| `index.html` | `docs/` or drop | decide (PR-03) | generated landing page |
| `STUDENT_GUIDE.md`, `PACKAGING_GUIDE.md`, `PROJECT_SUMMARY.md`, `SUMMARY.md`, `INDEX.md`, `QUICK_START.md`, `FILE_LIST.txt`, `DIRECTORY_STRUCTURE.txt`, `NOTEBOOK_CREATION_GUIDE.md` | `docs/` or `archive/` | git mv | consolidate; fix iPae1146→iMO1056 |
| `{data` (junk tree) | DELETE | rm | empty brace-expansion artifact (R-01) |
| `src/__pycache__/` | delete (local) | rm | regenerate under 3.9 |
| `.venv/` | leave (git-ignored) | — | legacy 3.12 env |
| `ipynb.rar` (if present) | `archive/` or exclude | — | do NOT commit (R-04) |

## Audit / governance files (stay at root)
`PROJECT_AUDIT.md`, `TODO.md`, `DECISIONS.md`, `BLOCKERS.md`,
`DATA_PROVENANCE.md`, `PUBLICATION_PLAN.md`, `REPOSITORY_MIGRATION_PLAN.md`,
`README.md`, `CLAUDE.md`, `.gitignore`, env/lock files.

## Order of operations (Phase B+)
1. Confirm env + notebook reproduction (E-01/E-02).
2. Add `tests/` pinning behavior (T-01).
3. `git mv` papers → `papers/`; update `manifest.csv` paths.
4. Move audit scripts to `scripts/`.
5. Copy raw model into `models/raw/`; update load paths in src/notebooks/tests.
6. Migrate results → `results/tables|figures` (after R-02).
7. Consolidate docs; delete junk (`{data`); correct model-identity claims.
8. Re-run tests after every move; commit in small coherent steps. No push.

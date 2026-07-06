# NEXT-STAGE HANDOFF REPORT

**Date:** 2026-07-01 · **Cycle:** 2 (PAO1-focused organization) ·
**Branch:** `claude/revival-audit`

Self-contained summary so another assistant (or ChatGPT) can continue without
reading the whole repo. Project = validating the *P. aeruginosa* **PAO1**
genome-scale model **iMO1056** against PAO1 experimental essentiality/fitness data.

---

## 1. Current branch & git status
- Branch: `claude/revival-audit` (never pushed; no remote changes).
- `git status`: clean working tree except **untracked `conditian/`** (6 legacy
  PDFs, intentionally preserved).

## 2. Commits created this cycle (5, on top of `d2ee0314`)
| SHA | Summary |
|---|---|
| 627eedcf | B: safety snapshot + repo structure migration |
| a8a86e85 | C+D: PAO1 scope + evidence-based paper re-audit |
| db49b557 | E+F: literature search (NCBI-verified) + strategy |
| 813d5f05 | G+H+I: validation inventory, orthology status, tests, reproduction |
| f6431dc6 | J: documentation updates for PAO1 focus + re-audit |

## 3. Files moved/copied/renamed
- **Copied (originals kept):** model → `models/raw/paeruginosa_MODEL1507180020.xml`
  (SHA-verified); `conditian/*.pdf` → `papers/<study>.pdf` (6, each SHA-verified).
- **git mv (history preserved):** `audit_model.py, show_audit.py, identify_pdfs.py,
  analyze_reproduction.py` → `scripts/audit/`; `generate_clean_predictions.py,
  generate_phasea_data.py, cmp_ess.py` → `scripts/`; `build_gene_mapping.py` →
  `scripts/mapping/`; `STUDENT_GUIDE, PROJECT_SUMMARY, SUMMARY, INDEX, QUICK_START,
  PACKAGING_GUIDE, DIRECTORY_STRUCTURE, FILE_LIST` → `archive/`; `index.html` → `docs/`.
- **Deleted:** `{data` (verified-empty brace artifact).
- **New scripts:** `scripts/audit/extract_strain_evidence.py`, `pubmed_search.py`.

## 4. Status of `conditian/`
Still present, **untracked, untouched**. It is the legacy raw PDF folder,
superseded by `papers/`. Do **not** delete without explicit approval.

## 5. Final canonical folder structure
```
models/{raw,processed}/   papers/(6 pdf + manifest.csv)   conditian/(legacy, untracked)
data/{raw/{literature,ortholog},processed}/   notebooks/{,reproduced}/
src/   scripts/{audit,mapping}/   tests/   results/{essentiality,tables,figures,comparison}/
docs/   manuscript/   archive/
root: governance .md (README, CLAUDE, TODO, BLOCKERS, DECISIONS, DATA_PROVENANCE,
  PUBLICATION_PLAN, REPOSITORY_MIGRATION_PLAN, WORK_CYCLE_LOG, VALIDATION_READINESS,
  PAO1_PROJECT_SCOPE, PAO1_PAPER_RELEVANCE_AUDIT, PAO1_VALIDATION_DATA_INVENTORY,
  ORTHOLOGY_STATUS_REPORT, REPRODUCTION_AFTER_MIGRATION, NEXT_STAGE_HANDOFF_REPORT,
  PROJECT_AUDIT) + env files.
```

## 6. Model identity (verified this cycle)
- iMO1056, BioModels `MODEL1507180020`, *P. aeruginosa* **PAO1**.
- File `models/paeruginosa_MODEL1507180020.xml`,
  SHA-256 `0868a5ebb41ebb4967c3c182e686eca7552af9255cba5a6d130cf114d1212ead`.
- **1110 reactions · 879 metabolites · 1054 genes** (all `PAxxxx`).
- Objective `PA_Biomass6_DM`; default-medium **WT growth 1.0479285528184004 /h**.

## 7. Environment status
- Canonical: conda env **reccobra39**, Python
  `C:\Users\pro\anaconda3\envs\reccobra39\python.exe` (3.9.23).
- cobra 0.29.1, pandas 2.3.2, matplotlib 3.9.4, matplotlib_venn 1.1.2,
  openpyxl 3.1.5, scipy 1.13.1, **pytest 8.4.2** (added env-scoped this cycle).
- Env lock (`environment.yml`/`requirements-lock.txt`) still **open** (E-03).

## 8. Notebook reproduction status
- Migration is **behavior-preserving** (canonical model path unchanged; `src/` and
  notebooks not moved). nb02 reproduces exactly (166 essential, WT 1.0479285528);
  see `REPRODUCTION_AFTER_MIGRATION.md`. Pre-existing follow-ups unchanged: nb01
  `BIOMASS_PAO` bug (N-01), kernelspec cleanup (E-04).
- `tests/test_model_and_data.py`: **8 pytest pass** under reccobra39.

## 9. Existing papers reclassified by PAO1 relevance (evidence-based)
| Study | Strain | Tier | PAO1-usable directly |
|---|---|---|---|
| Belanger 2022 | **PAO1** | 1 | yes |
| Lee 2015 | **MPAO1** | 2 | yes (PAO1-derived) |
| Turner 2015 | **PAO1+PA14** | 3 | yes (PAO1 rows) |
| Poulsen 2019 | multi (incl PAO1) | 3/5 | partial |
| Basta 2017 | **PA14** | 4 | no (orthology) |
| Juhas 2015 | review | 6 | no |
Corrections from PDF evidence: **Lee=MPAO1 (was PA14)**, **Belanger=PAO1**,
**Turner=mixed (was PA14)**. Details: `PAO1_PAPER_RELEVANCE_AUDIT.md`.

## 10. New papers found (and why)
- ~~meegid2022 (PMID 35104681)~~ **removed from active scope by user decision
  2026-07-06** (no local files; no validation dependency). *(Historical note; was
  formerly a Tier 1 candidate.)*
- **Oberhardt 2008** (PMID 18192387): the **iMO1056 source** paper.
- **Bartell 2017** (PMID 28266498, PMC5344303) & **GigaScience 2018** (PMID
  29688451, PMC6333913): alternative PAO1 GEMs → Tier 2 comparison.
- Others (Tier 2 background): PMIDs 20233082, 24707203, 37233700, 33972355.

## 11. Papers rejected/deferred
- MPAO1 biofilm-AMR model (PMID 33127897): no gene-level essentiality → defer.
- ~11 single-gene/virulence/resistance/transcription hits with no genome-wide
  PAO1 essentiality table → excluded (not added to inflate count).
Details + PMIDs: `docs/PAO1_LITERATURE_SEARCH_STRATEGY.md`.

## 12. Supplementary datasets downloaded
**None.** No supplement or full-text PDF was retrievable this cycle.

## 13. Supplementary datasets blocked *(historical snapshot; superseded)*
All corpus supplements (PNAS/Frontiers/mBio 403) and PMC OA packages
(ftp denied / https 404) — B-NET. Oberhardt 2008 not OA. Only metadata
(PMID/PMCID/DOI) was obtainable (NCBI eutils works). *(meegid2022 removed from
active scope by user decision; no local files; no validation dependency. Corpus
supplements were subsequently obtained — see `DATA_PROVENANCE.md §3d`.)*

## 14. PAO1/MPAO1 datasets available for future validation
Belanger 2022 (PAO1), Lee 2015 (MPAO1), Turner 2015 (PAO1 rows). **All join to
the model by identity — no orthology needed.** Supplements now downloaded +
parsed to DRAFT. Priority order in `PAO1_VALIDATION_DATA_INVENTORY.md`.
(meegid2022 removed from active scope by user decision 2026-07-06.)

## 15. PA14-only datasets requiring orthology
Basta 2017 (PA14, growth-arrest — also conceptually non-growth) and the non-PAO1
strains of Poulsen 2019. Need validated PAO1↔PA14 orthology (B-MAP-01).

## 16. State of `gene_mapping.csv`
1054 model genes → PAO1 identity (high). PA14 layer = symbol-based only: 386
medium (1:1), 22 low (ambiguous), 646 unmapped. NOT validated orthology.
Unchanged this cycle (no source reachable); see `ORTHOLOGY_STATUS_REPORT.md`.

## 17. State of `literature_evidence.csv`
6 study-level rows, 30 columns, phenotype classes distinct. Strains corrected;
PMIDs/PMCIDs added. **All gene-level rows still `PENDING_EXTRACTION`** (supplements
blocked). Nothing fabricated.

## 18. Remaining P0 blockers
- **B-SCI-01** — only simulated comparison exists (invalid).
- **B-LIT-01 / B-NET** — supplements + OA full text not downloadable here.
- **B-COND-01** — experimental media not reconstructed.
(B-MAP-01 downgraded to P1: needed only for PA14/Basta + non-PAO1 Poulsen.)

## 19. Remaining P1/P2 tasks
P1: L-05/L-06 (human-assisted downloads), L-03 (parse to gene-level), C-01b
(PAO1 media), S-01 (per-condition deletion), N-01 (nb01 fix), E-03/E-04 (env lock/
kernels), B-MAP-01 (orthology). P2: M-01 (blocked reactions), M-02 (threshold
sensitivity), M-03 (formulas), results→results/tables migration.

## 20. What to do next, in order
1. **Human-assisted download** of PAO1/MPAO1 supplements — **DONE** (Lee, Turner,
   Belanger, Varadarajan, Poulsen, Basta all present, hashed, audited).
   (meegid2022 removed from active scope by user decision 2026-07-06.)
2. Parse to gene-level `literature_evidence.csv` (keep 6 classes distinct).
3. Reconstruct PAO1 media (LB; SCFM/MOPS-succinate; host/SCFM) as exchange bounds.
4. Per-condition single-gene deletion at thresholds 0/1/5/10%.
5. **Only then** compute metrics per condition × phenotype class, with coverage.
6. Separately: obtain validated PAO1↔PA14 orthology to add Basta/Poulsen(non-PAO1).

## 21. ⚠️ Validation-metrics warning
**No real validation metrics are ready.** The only model-vs-experiment comparison
in the repo (nb03) uses **simulated random labels (B-SCI-01)** and must not be
reported. Do not compute precision/recall/F1/MCC/specificity/confusion matrices
until items 1–4 above are complete and validated.

## 22. Files to send to ChatGPT for the next stage
1. `PAO1_PROJECT_SCOPE.md`
2. `PAO1_PAPER_RELEVANCE_AUDIT.md`
3. `PAO1_VALIDATION_DATA_INVENTORY.md`
4. `ORTHOLOGY_STATUS_REPORT.md`
5. `VALIDATION_READINESS.md`
6. `data/processed/literature_evidence.csv`
7. `data/processed/gene_mapping.csv` + `gene_mapping_coverage.txt`
8. `data/processed/predicted_essentiality_default_medium.csv`
9. `papers/manifest.csv`
10. `docs/PAO1_LITERATURE_SEARCH_STRATEGY.md`
11. `BLOCKERS.md`, `TODO.md`, `DECISIONS.md`
12. This report (`NEXT_STAGE_HANDOFF_REPORT.md`)

---

## 23. Cycle-2 consistency verification (2026-07-01, post-cycle)

Independent re-check of the cycle outputs requested after delivery. All passed.

| # | Check | Result |
|---|---|---|
| 1 | `data/raw/orths` folder | **Does not exist** — only `data/raw/ortholog/` is present; "orths" was shorthand in the request, not a real path. No tracked reference to `raw/orths`. **No rename needed.** |
| 2 | meegid2022 citation *(historical check; study since **removed from active scope by user decision — no local files; no validation dependency**)* | Historical record only: was verified via NCBI eutils (PMID 35104681, DOI 10.1016/j.meegid.2022.105231, 2022, *Infection, Genetics and Evolution*). No longer a target, blocker, or dependency. |
| 3 | 6 PDF SHA-256 (`conditian/` → `papers/`) | **ALL 6 MATCH** (juhas2015, turner2015, lee2015, poulsen2019, basta2017, belanger2022). |
| 4 | `conditian/` untracked & untouched | **Yes** — `git status` shows `?? conditian/`; all 6 original PDFs intact; not staged/committed/deleted. |
| 5 | No validation metrics generated | **Confirmed** — `results/comparison/` holds only `README.txt`; no `metrics_*`, precision/recall/confusion files anywhere; pytest no-metrics guard passes. |
| 6 | Tests after checks | **8 passed** under reccobra39 (no path correction was required). |

**Conclusion:** Cycle-2 outputs are internally consistent. No fabricated data; no
metrics; `conditian/` preserved; no push. Nothing required correction.

# TODO — evidence-based, derived from the Phase A audit

Every task below is grounded in an observed fact from `PROJECT_AUDIT.md`.
No invented completion percentages. Fields per task:
**ID · Priority · Category · Task · Reason · Inputs · Expected output · Dependencies · Validation · Status · Blocker · Commit**

Priorities: **P0** blocks scientific validity/reproducibility · **P1** required for
manuscript & public repo · **P2** improves quality · **P3** optional.
Status: TODO / IN-PROGRESS / DONE / BLOCKED.

---

## A. Repository recovery

### R-01 · P1 · repo-recovery
- **Task:** Remove the stray `{data` junk directory tree (literal brace-expansion dirs).
- **Reason:** Created by a bash-style `mkdir` run in PowerShell; empty, confusing.
- **Inputs:** `{data/...` · **Output:** clean tree · **Deps:** none
- **Validation:** `git status` clean; dirs gone; no real data lost (confirmed empty).
- **Status:** DONE 2026-07-01 (Cycle 2; verified 0 files before `rm -rf '{data'`). · **Blocker:** none

### R-02 · P2 · repo-recovery
- **Task:** Clean `gene_id` column in `results/essentiality/gene_essentiality_default_medium.csv` (`{'PAxxxx'}` → `PAxxxx`); write cleaned copy, keep original.
- **Reason:** Set-repr blocks joins/mapping; integrity (don't edit raw in place).
- **Inputs:** the CSV · **Output:** `data/processed/predicted_essentiality_default_medium.csv`
- **Deps:** none · **Validation:** all 1054 ids match `^PA\d+$`; 166 essential preserved.
- **Status:** DONE (commit after a47b6295; `generate_clean_predictions.py` → `data/processed/predicted_essentiality_default_medium.csv`, validated: 1054 rows, 0 non-PA ids, 166 essential) · **Blocker:** none

### R-03 · P2 · repo-recovery
- **Task:** Reconcile/correct docs that claim model is "iPae1146"; state it is iMO1056/PAO1.
- **Reason:** `models/README.md` and summaries are inconsistent with the loaded model.
- **Inputs:** model_audit_snapshot.json · **Output:** corrected READMEs/summaries
- **Deps:** none · **Validation:** every model-identity claim matches the audit. · **Status:** DONE 2026-07-01 (fixed `models/README.md` iPae1146→iMO1056; legacy docs with stale claims archived).

### R-04 · P3 · repo-recovery
- **Task:** Decide fate of `ipynb.rar` if it reappears; keep out of git.
- **Reason:** Brief flags it as untracked archive; not found at audit time.
- **Inputs:** working tree · **Output:** `.gitignore` rule (added) + note · **Validation:** not tracked. · **Status:** TODO

---

## B. Environment reproducibility

### E-01 · P1 · environment
- **Task:** Install (locally, NOT global) into reccobra39: matplotlib, matplotlib-venn, scipy, networkx, openpyxl.
- **Reason:** reccobra39 lacks them; notebooks/plots and `.xlsx` reading fail.
- **Inputs:** reccobra39 · **Output:** updated local env · **Deps:** D-02
- **Validation:** `import matplotlib, matplotlib_venn, openpyxl` succeed in reccobra39.
- **Status:** DONE (matplotlib 3.9.4, matplotlib-venn 1.1.2, openpyxl 3.1.5, scipy 1.13.1 added via env-scoped pip; numpy/pandas/cobra unchanged. networkx not needed yet — defer.) · **Blocker:** none

### E-02 · P1 · environment
- **Task:** Re-run all three notebooks under the **reccobra39** kernel; confirm numerical reproduction (WT growth 1.0479, 166 essential @1%).
- **Reason:** Notebooks were authored under .venv/3.12.6; must reproduce in canonical env.
- **Inputs:** notebooks, reccobra39 · **Output:** executed notebooks + reproduction note
- **Deps:** E-01 · **Validation:** outputs match audited numbers within solver tol.
- **Status:** DONE — see `notebooks/reproduced/REPRODUCTION_REPORT.md`. All 3 ran under Py3.9.23. **nb02 reproduces exactly** (166 essential identical, WT 1.0479285528; only CSV row order differs). **nb01 has 1 bug** (cell14 `BIOMASS_PAO` not found → N-01). **nb03 runs but is simulated** (B-SCI-01). · **Blocker:** none (B-ENV-01 effectively resolved; lock env after E-04+N-01)

### E-03 · P1 · environment
- **Task:** After E-02 passes, lock `environment.yml` + `requirements-lock.txt`; reconcile the 3 existing env specs.
- **Reason:** Reproducible public repo needs one authoritative, working env.
- **Deps:** E-02 · **Validation:** fresh env from lock file imports cobra+matplotlib and runs nb02. · **Status:** BLOCKED

### E-04 · P2 · environment
- **Task:** Register/clean Jupyter kernels; standardize notebooks to the reccobra39 kernel metadata (reproduced notebooks still embed `.venv` kernelspec display).
- **Reason:** Three kernels (.venv, python3, reccobra39) cause ambiguity. · **Deps:** E-02 · **Status:** TODO

### N-01 · P1 · environment / repo-recovery
- **Task:** Create a fixed clean copy of `01_basic_fba.ipynb` correcting the hard-coded `BIOMASS_PAO` → `PA_Biomass6_DM`; keep original until verified.
- **Reason:** E-02 found `cell14 ValueError: Reaction 'BIOMASS_PAO' not found`.
- **Inputs:** `notebooks/01_basic_fba.ipynb`, model · **Output:** clean notebook that runs error-free
- **Deps:** E-02 · **Validation:** nbconvert --execute returns 0 cell errors under reccobra39. · **Status:** TODO · **Blocker:** none

---

## C. Model validation (computational, model-only)

### M-01 · P2 · model-validation
- **Task:** Compute blocked reactions (`processes=1`) and characterize dead-end metabolites (217 found).
- **Reason:** Needed to interpret false-negative essentiality; FVA failed under MP in audit.
- **Inputs:** model · **Output:** `results/model_qc/blocked_reactions.csv`, `deadends.csv`
- **Deps:** none · **Validation:** counts stable across reruns; documented. · **Status:** TODO · **Blocker:** B-MODEL-01

### M-02 · P2 · model-validation
- **Task:** Objective-function & growth-threshold sensitivity of essentiality (thresholds 0/1/5/10%; biomass variant `DM_EC_PREGRO` vs `PA_Biomass6_DM`).
- **Reason:** Essential-vs-reduced-growth classification must be robust (D-09).
- **Inputs:** model · **Output:** sensitivity tables/figs · **Deps:** none
- **Validation:** essential-set size vs threshold curve; documented. · **Status:** TODO

### M-03 · P3 · model-validation
- **Task:** Back-fill missing metabolite formulas (565) from BiGG/MetaNetX where balance claims are needed.
- **Reason:** Mass-balance audit unreliable without formulas. · **Deps:** none · **Status:** TODO · **Blocker:** B-MODEL-02

---

## D. Literature extraction

### L-01 · P0 · literature
- **Task:** Download official supplementary datasets (Turner sd01–04, Lee sd01, Poulsen Broad fitness data; Basta/Belanger supp); record provenance + SHA-256.
- **Reason:** Gene-level experimental labels live only in supplements.
- **Inputs:** DOIs in `papers/manifest.csv` · **Output:** `data/raw/literature/<study>/...`
- **Deps:** network + human OK · **Validation:** files present, hashed, logged in DATA_PROVENANCE.
- **Status:** PARTIAL — raw dirs created; DOIs verified. PNAS supplements **403-blocked** and pseudomonas.com unreachable from this environment (see B-NET). NCBI RefSeq feature tables downloaded instead (for G-01). · **Blocker:** B-LIT-01, B-NET

### L-02 · P1 · literature
- **Task:** Verify Basta & Belanger citation/DOI/year/strain against CrossRef/journal.
- **Reason:** Currently PENDING_VERIFY; cannot cite unverified.
- **Inputs:** PDFs · **Output:** updated `literature_evidence.csv`, `papers/manifest.csv`
- **Deps:** none · **Validation:** DOI resolves to matching title. · **Status:** DONE — Basta 2017 mBio `10.1128/mBio.01170-17`; Belanger 2022 Front Microbiol `10.3389/fmicb.2022.1055512` (verified ASM/Frontiers+PMC). · **Blocker:** none

### L-03 · P0 · literature
- **Task:** Populate `data/processed/literature_evidence.csv` gene-level rows from supplements, keeping all 30 columns + 6 distinct phenotype classes; no merging.
- **Reason:** Core evidence table for validation; integrity rules §3,§5.
- **Inputs:** downloaded supplements · **Output:** complete evidence table
- **Deps:** L-01 · **Validation:** each row has citation+strain+condition+method+threshold+source locator; phenotype_type ∈ {6 classes}.
- **Status:** **DRAFT-PARSED 2026-07-06** — thresholds sourced from Methods
  (`THRESHOLD_METHOD_AUDIT.md`; L03-B1/B2/B4/B5/B6 resolved), then
  `scripts/literature/parse_supplements.py` emitted DRAFT gene-level evidence for
  lee2015, turner2015 (PAO1 single-strain sheets sd01/06/07/10) and belanger2022 →
  `data/processed/literature/*_parsed_gene_evidence.csv` +
  `data/processed/literature_evidence_gene_level_DRAFT.csv` (5,093 rows; 6 classes
  distinct; validation Turner=336 exact, Lee=351≈352). **varadarajan2020 NOT parsed
  as evidence** (DS4 essentiality = Lee re-mapped → double-count; citation verified,
  mapping resource only). Remaining: human review + promote DRAFT; Turner paired
  sheets sd03/04/05/09 (L03-B3); canonical `literature_evidence.csv` still not
  populated (intentionally — DRAFT is unreviewed). · **Blocker:** L03-B3 open;
  B-SCI-01 (no metrics on unvalidated draft).

---

## E. Gene mapping

### G-01 · P1 · gene-mapping
- **Task:** Obtain authoritative PAO1↔PA14 ortholog table (pseudomonas.com / study homolog columns) and join into `gene_mapping.csv`; retain one-to-many & missing.
- **Reason:** Needed **only** for the PA14-only path — Basta 2017 (PA14) and the non-PAO1 strains of Poulsen 2019 — whose gene IDs are not interchangeable with the PAO1 model. The PAO1/MPAO1 sources (Lee, Turner PAO1 rows, Belanger, meegid2022) join by identity and do **not** require this, so it is off the critical path for the first validation (downgraded P0→P1; see B-MAP-01, B-STRAIN-02).
- **Inputs:** `gene_mapping.csv`, ortholog source · **Output:** populated PA14/gene_name/uniprot + confidence
- **Deps:** network + human OK · **Validation:** mapping coverage report; ambiguous cases listed. · **Status:** PARTIAL — `build_gene_mapping.py` → `gene_mapping.csv` + `gene_mapping_coverage.txt`. All 1054 model genes → PAO1 (high); 386 → PA14 unique-symbol (medium); 22 ambiguous (candidates retained); 646 PA14-unmapped. Source = NCBI RefSeq symbols (annotation, NOT validated orthology). Upgrade to pseudomonas.com orthology pending B-NET. · **Blocker:** B-MAP-01, B-NET

### G-02 · P1 · gene-mapping
- **Task:** Add gene names / UniProt for model PAO1 genes from a versioned source.
- **Reason:** Reporting + cross-referencing. · **Deps:** none(P) · **Validation:** sourced+dated. · **Status:** TODO

---

## F. Condition reconstruction

### C-01 · P0 · condition-reconstruction
- **Task:** Define in-model media for each experimental condition (CF sputum/SCFM, LB, defined minimal, C/O2-limited arrest, host-mimicking) with cited composition → exchange bounds.
- **Reason:** Comparing across mismatched media is invalid (B-COND-01).
- **Inputs:** papers, `src/medium.py` · **Output:** `data/processed/conditions/*.json` + loader
- **Deps:** L-03 · **Validation:** each condition cited; model feasible or documented infeasible. · **Status:** BLOCKED · **Blocker:** B-COND-01

---

## G. Simulation

### S-01 · P1 · simulation
- **Task:** Run single-gene-deletion per reconstructed condition; export per-condition predicted essential/reduced-growth sets.
- **Reason:** Basis for validation against the matching experimental class.
- **Inputs:** model, conditions · **Output:** `results/essentiality/<condition>.csv`
- **Deps:** C-01, E-02 · **Validation:** reproducible; threshold recorded. · **Status:** BLOCKED

### S-02 · P2 · simulation
- **Task:** Alternate-optima / solver-tolerance robustness (pFBA, multiple solvers if available).
- **Reason:** Guard essentiality calls against degeneracy. · **Deps:** S-01 · **Status:** TODO

---

## H. Statistical evaluation

### V-01 · P0 · statistical-evaluation
- **Task:** Replace the simulated-data comparison in nb03 with real labels; compute confusion matrix, precision, recall, specificity, F1, MCC per matched condition+phenotype class; report mapped/unmapped/absent-gene coverage.
- **Reason:** Current metrics are on random data (B-SCI-01) — invalid.
- **Inputs:** predictions (S-01/R-02), evidence (L-03), mapping (G-01) · **Output:** `results/comparison/metrics_<condition>.csv` + figs
- **Deps:** L-03, G-01, C-01, S-01 · **Validation:** labels+mappings validated FIRST; metrics only on validated joins. · **Status:** BLOCKED · **Blocker:** B-SCI-01

---

## I. Figures & tables

### F-01 · P1 · figures-tables
- **Task:** Publication-quality figures (essential-set sizes, threshold sensitivity, confusion/Venn on REAL data) and result tables.
- **Reason:** Manuscript needs defensible visuals (not the placeholder Venn).
- **Deps:** V-01 · **Validation:** every figure traceable to a script+data file. · **Status:** BLOCKED

---

## J. Manuscript

### P-01 · P1 · manuscript
- **Task:** Draft `manuscript/` (intro, methods incl. model id/strain/medium/threshold, results, limitations: PAO1↔PA14, media mismatch, FBA caveats).
- **Reason:** Target outcome #2. · **Deps:** V-01, F-01 · **Status:** BLOCKED

---

## K. Documentation

### D-01t · P1 · documentation
- **Task:** Rewrite root README as a professional research-repo README (done in Phase A draft); keep teaching docs under `docs/`.
- **Reason:** Public-repo readiness. · **Deps:** none · **Status:** IN-PROGRESS

### D-02t · P2 · documentation
- **Task:** Consolidate redundant root docs (SUMMARY/PROJECT_SUMMARY/INDEX/...) into `docs/`.
- **Reason:** Reduce clutter/inconsistency. · **Deps:** R-03 · **Status:** TODO

---

## L. Testing

### T-01 · P1 · testing
- **Task:** Add `tests/` (pytest): model loads; WT growth ≈1.0479; 166 essential @1%; medium reset/set; mapping extraction; gene_id cleaning.
- **Reason:** Lock scientific behavior before refactor (Phase B).
- **Inputs:** src, model · **Output:** `tests/test_*.py` · **Deps:** E-01
- **Validation:** `pytest` green under reccobra39. · **Status:** DONE 2026-07-01 (`tests/test_model_and_data.py`, 8 tests pass; pytest installed env-scoped; guard asserts no metrics file yet).

### T-02 · P2 · testing
- **Task:** Refactor reusable notebook logic into `src/` and have notebooks call `src/` (no behavior change).
- **Reason:** Brief Phase B. · **Deps:** T-01, E-02 · **Status:** TODO

---

## M. Publication readiness

### PR-01 · P1 · publication-readiness
- **Task:** Migrate to target structure (`models/raw|processed`, `data/raw|processed`, `papers/`, `notebooks/`, `src/`, `tests/`, `results/`, `manuscript/`, `docs/`, `archive/`) per `REPOSITORY_MIGRATION_PLAN.md`; keep originals via git.
- **Reason:** Target outcome #1. · **Deps:** E-02, T-01 · **Status:** DONE 2026-07-01 (Cycle 2; structure created, scripts/docs/model/PDFs migrated, verified behavior-preserving — `REPRODUCTION_AFTER_MIGRATION.md`). Remaining: `results/essentiality/*` → `results/tables/` (deferred with R-02 clean file already in data/processed).

### PR-02 · P1 · publication-readiness
- **Task:** Add LICENSE, CITATION.cff, verify model redistribution terms, scrub for secrets/large binaries; final audit.
- **Reason:** Public release. · **Deps:** PR-01 · **Status:** TODO · **Blocker:** model license (DATA_PROVENANCE §1)

### PR-03 · P2 · publication-readiness
- **Task:** Decide on `index.html` landing page (keep in `docs/` or drop). · **Deps:** PR-01 · **Status:** TODO

---

## N. Cycle-2 additions (2026-07-01)

### L-04 · P0 · literature — DONE
- **Task:** Re-audit the six papers' strains from direct PDF evidence; correct
  mis-classifications.
- **Status:** DONE — `PAO1_PAPER_RELEVANCE_AUDIT.md`. Corrections: Lee=MPAO1,
  Belanger=PAO1, Turner=PAO1+PA14. PMIDs/PMCIDs NCBI-verified. · **Blocker:** none

### L-05 · P0 · literature — download PAO1/MPAO1 supplements (human-assisted)
- **Task:** Obtain Lee 2015 `sd01.xlsx` (MPAO1), Turner 2015 `sd01–04.xlsx` (PAO1
  rows), Belanger 2022 supplement (PAO1). Store in `data/raw/literature/<study>/`
  with provenance + SHA-256; add `SUPPLEMENT_PARSE_NOTES.md`.
- **Reason:** These are PAO1/MPAO1 → join by identity (no orthology) → first
  validation labels. · **Deps:** network/human
- **Status:** **PARTIAL/DONE 2026-07-06** — Lee sd01 (+SI PDF), **Turner sd01–sd10**
  (all 10, not just sd01–04), and **Belanger** Data_Sheet_1/2 (.XLSX) + Data_Sheet_3
  (.docx) are present, SHA-256-logged (`DATA_PROVENANCE.md §3d`,
  `data/processed/literature/supplement_inventory.tsv`), audited
  (`SUPPLEMENT_INVENTORY_AUDIT.md`), and parse notes added (Phase D). **Bonus:**
  `varadarajan2020` (MPAO1 TnSeq + MPAO1→PAO1 map) also obtained. **Update
  2026-07-06 (user-added):** `poulsen2019` (sd01–07 + SI PDF) and `basta2017`
  (sd1–4 + 2 tif) now **present** and audited (`SUPPLEMENT_INVENTORY_AUDIT.md`,
  `DATA_PROVENANCE.md §3d`) — both still deferred (PA14_ID/Cluster_ID & PA14; need
  orthology + threshold sourcing; not parsed as evidence). **Still missing:**
  meegid2022 (no folder). · **Blocker:** narrowed — B-LIT-01 now open only for
  meegid2022 + DRAFT promotion + `SOURCE_URL_PENDING`.

### L-06 · P1 · literature — acquire new PAO1 dataset meegid2022
- **Task:** Obtain full text + supplement of PMID 35104681 (PAO1 insertion-seq,
  host-infection). Not OA here. · **Status:** BLOCKED · **Blocker:** B-NET

### L-07 · P2 · literature — acquire model/GEM references
- **Task:** Obtain Oberhardt 2008 (iMO1056 source; not OA here) and optionally
  Bartell 2017 / GigaScience 2018 PAO1 GEMs for comparison/discussion.
- **Status:** BLOCKED (download) · **Blocker:** B-NET

### C-01b · P0 · condition-reconstruction — PAO1 media first
- **Task:** Reconstruct LB (Lee general), SCFM/MOPS-succinate (Turner), host/SCFM
  (Belanger) as in-model exchange configs with citations. · **Deps:** L-05 · **Status:** BLOCKED · **Blocker:** B-COND-01

### E-03 (update) · lock env including pytest/matplotlib/openpyxl once N-01/E-04 done.

## TOP 10 (updated 2026-07-01, by priority and unblock-ability)
1. **L-05** download PAO1/MPAO1 supplements (P0, human-assisted) — unblocks labels
2. **L-06** acquire meegid2022 PAO1 dataset (P1, human-assisted)
3. **L-03** parse supplements → gene-level `literature_evidence.csv` (P0, after L-05)
4. **C-01b** reconstruct PAO1 media (LB/SCFM/MOPS) (P0, after L-05)
5. **S-01** per-condition single-gene deletion predictions (P1, after C-01b)
6. **M-01** blocked reactions / dead ends (P2, no blocker)
7. **M-02** threshold & objective sensitivity of essentiality (P2, no blocker)
8. **N-01** fix nb01 `BIOMASS_PAO`→`PA_Biomass6_DM` (P1, no blocker)
9. **E-03/E-04** kernel cleanup + lock env (P1/P2)
10. **G-01/B-MAP-01** validated PA14 orthology (P1 now; only for Basta/Poulsen)

**Completed this cycle:** R-01, R-03, T-01, PR-01, L-02, L-04 (plus E-01, E-02, R-02 earlier).
**Still gated (do NOT compute metrics):** V-01 (B-SCI-01/B-LIT-01/B-COND-01).

## Update 2026-07-06 (L-section supplements landed)
- **Model raw-copy test failure RESOLVED** (CRLF→LF; `MODEL_COPY_DISCREPANCY_REPORT.md`);
  tests 8/8. `.gitattributes` pins `*.xml text eol=lf`.
- **L-05 PARTIAL/DONE:** lee2015, turner2015 (sd01–10), belanger2022, varadarajan2020
  supplements present + audited (`SUPPLEMENT_INVENTORY_AUDIT.md`) + provenance logged
  (`DATA_PROVENANCE.md §3d`). meegid2022/poulsen2019/basta2017 still missing.
- **L-03 IN-PROGRESS:** parse notes written; gene-level extraction gated on Phase E.
- **Next scientific stage:** (1) L-03 parse supplements → gene-level
  `literature_evidence_gene_level_DRAFT.csv`; (2) C-01b reconstruct PAO1 media
  (LB / MOPS-succinate / SCFM2 [Turner sd08 recipe] / RPMI±serum); (3) S-01
  per-condition gene deletion; (4) V-01 metrics — still **forbidden** until real
  labels + media + predictions exist.

# DECISIONS

Architectural / scientific decisions and their rationale. Append-only log.
Format: ID · date · decision · rationale · status.

---

## D-01 · 2026-06-26 · Work only on `claude/revival-audit`; never push
**Decision:** All Phase A work stays on branch `claude/revival-audit` with local
commits only. No push, no force-push, no remote/branch changes.
**Rationale:** Explicit instruction; repo was previously on a different remote
(`bioinformatik-project`). Publishing requires human approval.
**Status:** Active.

## D-02 · 2026-06-26 · reccobra39 is the canonical environment (pending confirmation)
**Decision:** Adopt **reccobra39** (Python 3.9.23, cobra 0.29.1) as the project
environment, *after* adding the missing packages (matplotlib, matplotlib-venn,
scipy, networkx, openpyxl) **locally**. The notebooks' `.venv` (Python 3.12.6)
is treated as legacy.
**Rationale:** The session brief mandates reccobra39 and it already has a working
cobra/pandas stack. Standardizing on one supported env > carrying an ad-hoc venv.
**Status:** Provisional — must verify numerical reproduction (B-ENV-01) before
locking `environment.yml`. Do NOT lock env files until then.

## D-03 · 2026-06-26 · Model strain = PAO1
**Decision:** Treat the model as *P. aeruginosa* **PAO1** (iMO1056, Oberhardt 2008).
**Rationale:** Gene IDs are `PAxxxx` PAO1 locus tags; model name/BioModels id confirm iMO1056.
**Consequence:** PA14 experimental datasets require explicit PAO1↔PA14 orthology
mapping (B-MAP-01) before any comparison. Do not treat IDs as interchangeable.
**Status:** Active.

## D-04 · 2026-06-26 · Six phenotype classes kept distinct
**Decision:** Maintain separate labels: generally-essential, core-essential,
condition-specific-essential, reduced-fitness, growth-arrest-survival-determinant,
host-condition-fitness. No collapse into a single binary "essential".
**Rationale:** Scientific-integrity rule §5; these are biologically different
concepts tied to different studies/methods/thresholds.
**Status:** Active. Encoded in `literature_evidence.csv` `phenotype_type`.

## D-05 · 2026-06-26 · Do not modify raw model/data/PDF files in place
**Decision:** `models/paeruginosa_MODEL1507180020.xml`, the PDFs, and any raw
literature data are read-only. Derived/cleaned versions go to `models/processed/`
and `data/processed/`.
**Rationale:** Reproducibility + integrity rules §6–§8. Original recoverable via git.
**Status:** Active.

## D-06 · 2026-06-26 · No reorganization in Phase A
**Decision:** Keep existing files in place during Phase A; only ADD new audit
artifacts and a proposed migration map (`REPOSITORY_MIGRATION_PLAN.md`).
**Rationale:** Brief Phase A explicitly defers reorganization; preserve notebooks
until reproduced in a clean structure (rule §8).
**Status:** Active.

## D-07 · 2026-06-26 · Evidence-only data artifacts; PENDING markers instead of guesses
**Decision:** `literature_evidence.csv` and `gene_mapping.csv` are populated only
with directly-evidenced values; everything unknown is marked `PENDING_*` and
linked to a blocker — never filled with plausible-looking invented values.
**Rationale:** Integrity rules §1, §9, §10.
**Status:** Active.

## D-08 · 2026-06-26 · `conditian/` PDFs are the literature corpus
**Decision:** Interpret the misspelled `conditian/` folder as the papers folder;
plan to migrate its 6 PDFs to `papers/` with normalized names (manifest already
maps current→planned paths). Keep originals until copies are verified.
**Rationale:** All six files are scientific PDFs matching the expected author list;
the name is a typo of "condition", not a condition-definition folder.
**Status:** Active (migration deferred to Phase B).

## D-09 · 2026-06-26 · Default essentiality threshold = 1% growth ratio (provisional)
**Decision:** Keep the existing `threshold_ratio = 0.01` as the primary cutoff but
treat it as a **sensitivity parameter** (also test e.g. 0.0, 0.05, 0.10) before
any manuscript claim.
**Rationale:** Existing code/result use 1%; robustness to threshold is required
for defensible essential-vs-reduced-growth classification.
**Status:** Active; sensitivity analysis tracked in TODO.

## D-10 · 2026-07-01 · Execute the repository migration (Phase B)
**Decision:** Execute `REPOSITORY_MIGRATION_PLAN.md`: create target structure;
`git mv` audit/generation/mapping scripts → `scripts/{audit,,mapping}`; `git mv`
legacy educational docs → `archive/`; copy raw model → `models/raw/` and copy the
6 PDFs `conditian/* → papers/<study>.pdf` (all SHA-256-verified); keep the
canonical model path and `conditian/` untouched; delete only the verified-empty
`{data` artifact.
**Rationale:** Notebooks reproduce under reccobra39 (E-02) and behavior is now
pinned by tests, so reorganization is safe (supersedes D-06's Phase-A deferral).
**Status:** Active. Verified behavior-preserving (`REPRODUCTION_AFTER_MIGRATION.md`).

## D-11 · 2026-07-01 · Strain re-classification from direct PDF evidence
**Decision:** Adopt evidence-based strains: Belanger 2022 = **PAO1** (Tier 1),
Lee 2015 = **MPAO1** (Tier 2), Turner 2015 = **PAO1+PA14** (Tier 3), Poulsen 2019
= multi-strain incl. PAO1 (Tier 3/5), Basta 2017 = **PA14** (Tier 4), Juhas 2015
= review (Tier 6). Overrides the earlier "mostly PA14" framing.
**Rationale:** Recovered PDF text gives explicit strain statements (B-STRAIN-02).
Never assume strain; cite the quote.
**Status:** Active. Encoded in `papers/manifest.csv`, `literature_evidence.csv`,
`PAO1_PAPER_RELEVANCE_AUDIT.md`.

## D-12 · 2026-07-01 · PAO1-first validation path
**Decision:** Do the first model validation against **PAO1/MPAO1** datasets
(Lee, Turner PAO1 rows, Belanger) using the **identity** gene mapping; treat
MPAO1 as PAO1-derived with a recorded caveat. Defer PA14 (Basta) and non-PAO1
Poulsen strains until validated orthology exists. (meegid2022, formerly listed
here, removed from active scope by user decision 2026-07-06.)
**Rationale:** Removes the orthology dependency from the critical path (D-11).
**Status:** Active. B-MAP-01 downgraded P0→P1 accordingly.

## D-13 · 2026-07-01 · Growth-arrest ≠ growth-essentiality (no forced comparison)
**Decision:** Do **not** compare FBA single-gene-deletion growth-essentiality
against Basta 2017's growth-**arrest** survival determinants as if equivalent.
**Rationale:** FBA models growth; survival during energy-limited arrest is a
different phenotype (integrity rule §4). Requires a tailored framework if attempted.
**Status:** Active.

## D-14 · 2026-07-01 · `pytest` added env-scoped; keep behavior regression tests
**Decision:** Install `pytest` into reccobra39 (env-scoped) and keep
`tests/test_model_and_data.py` pinning model identity, WT growth, and the 166/1054
essentiality result; a guard asserts no validation-metrics file exists yet.
**Rationale:** Lock the science before/after refactors (T-01). Fold pytest into
the env lock at E-03.
**Status:** Active. 8 tests pass.

## D-15 · 2026-07-01 · Metadata via NCBI E-utilities; no fabricated IDs/downloads
**Decision:** Verify all PMIDs/PMCIDs via NCBI eutils (reachable). Where full text
or supplements are not downloadable (B-NET), record citation/DOI/PMID/PMCID only
and mark blocked — never fabricate files or gene lists.
**Rationale:** Integrity rules §1; honest provenance.
**Status:** Active.

## D-16 · 2026-07-10 · PGD orthology supplements Turner; does not replace APPROVED_LIMITED
**Decision:** The Pseudomonas Genome Database (PGD) PAO1↔PA14 ortholog export
(5,385 pairs, merged from `origin/develop`, commit `7cd3dd29`) **supplements and
validates** the Turner-derived `APPROVED_LIMITED` table (5,365 pairs) but does
**not replace** it until a formal PGD↔Turner crosswalk and human review are
complete.
**Rationale:** PGD is the authoritative live source and confirms Turner at the
previously disputed locus (PA2279↔PA14_35100, PA2277↔PA14_35130). However: (a)
pair counts differ (+20 PGD-only pairs), (b) PGD QC flags Review rows (one-to-many,
e.g. `PA0263`/`hcpC`), (c) Turner `APPROVED_LIMITED` already carries human review
metadata for L-03b, (d) premature replacement would bypass documented conflict-
resolution policy. PAO1 remains the project focus; PA14 evidence requires orthology
support and source labeling (Pseudomonas-derived / Turner-derived / manually
reviewed / approved-limited-use).
**Consequence:** Use Turner `APPROVED_LIMITED` for interim L-03b draft mapping.
Use PGD for cross-validation and future primary-source upgrade after crosswalk.
Do not merge into `gene_mapping.csv`; do not compute metrics. B-MAP-01 → PARTIALLY
RESOLVED.
**Status:** Active. Doc: `docs/ORTHOLOGY_PSEUDOMONAS_INTEGRATION.md`.

## D-17 · 2026-07-24 · First media batch + format + LB as sensitivity only
**Decision:** Implement Batch A DEFINED media **MOPS-pyruvate (Lee)** and
**MOPS-succinate (Turner)** plus Batch B **`LB_approx` (PARTIAL)** for the
PAO1-first path. **Do not** implement classic M9 in this batch (no READY_ONLY
PAO1/MPAO1 study Methods lock M9 as the matched medium). Medium configs live as
`MediumSpec` objects in `src/medium.py` with derived CSV tables under
`data/processed/conditions/` (extend existing API; no parallel system). Uptake
flux magnitudes follow the audited iMO1056 default-medium convention
(carbon −10, salts/O2 −1000) with recipe concentrations cited separately —
not invented concentration→flux formulas. `LB_approx` is a sensitivity case
only (yeast extract/tryptone unmodeled); never claim true LB. SCFM2 / RPMI /
MEDIA_GAP niches remain out of this batch.
**Rationale:** Matches `docs/TEAM_WORK_MODEL_AND_NEXT_STEPS.md` decision gate
and `C01B_MEDIA_RECONSTRUCTION_PLAN.md` / `MEDIA_SOURCE_AUDIT.md`.
**Status:** Active. Tests in `tests/test_media.py`.

## D-18 · 2026-07-24 · Archive teaching notebooks; research path = 04/05
**Decision:** Move `01`/`02`/`03` to `archive/teaching_notebooks/` with README
stating legacy/teaching status, nb01 biomass-id bug, and nb03 metrics forbidden.
New research notebooks start at `04_media_reconstruction` /
`05_condition_essentiality`; V-01 notebook gated.
**Rationale:** `docs/TEAM_WORK_MODEL_AND_NEXT_STEPS.md` §3.
**Status:** Active.

## D-19 · 2026-07-28 · Merge develop reorg into media branch (media wins science path)
**Decision:** Merge `origin/develop` (Saba repo-sort commits) into
`media/c01b-batch-ab-v01-prep` with **media as scientific base**:
- Keep `archive/teaching_notebooks/` (+ README); drop duplicate
  `archive/old_notebooks/`.
- Keep research notebooks `04`/`05` content from media; remove empty
  `06_pao1_validation.ipynb` placeholder (V-01 still gated).
- Keep `src/medium.py` MediumSpec / Batch A–B, `data/processed/conditions/`,
  `tests/test_media.py`, `VALIDATION_LABEL_MEDIA_OVERLAP.md`.
- Restore `models/raw/paeruginosa_MODEL1507180020.xml` (do not leave raw only
  under `archive/legacy_docs/raw model/`).
- Fix `src/__init__.py` to import `src.load_model` + `src.mapping` (not archive).
- Keep develop's folder sort for audit/docs/scripts/data where non-conflicting;
  restore canonical `TODO.md` + `DECISIONS.md` to repo root (`CLAUDE.md`).
- Accept develop `data/processed/gene_mapping/gene_mapping.csv` as present, but
  treat `official_orthology` provenance as **still needing human review** before
  V-01 / L-03b claims (does not reopen metrics).
**Rationale:** Unblock team integration without discarding media Batch A/B work
or reintroducing empty/broken entry points.
**Status:** Active.

## D-20 · 2026-07-29 · Lee2015 MOPS-pyruvate positives APPROVED_FOR_PROMOTION
**Decision:** Promote the **437 standard `PAxxxx`** Lee 2015 MOPS-pyruvate
**positive** condition-specific-essential labels (`source_column` =
`Min sum (of 3)`, values 2 or 3) from NEEDS_REVIEW to a **derived** READY file:
`data/processed/literature/gene_level/literature_evidence_gene_level_READY_mops_pyruvate_lee2015.csv`.
Human review (2026-07-29) confirms SI Sequence Data Analysis: consensus =
≥2 of 3 MOPS-pyruvate pools; workbook `Min sum (of 3)` holds those counts
(`project_management/audit/LEE2015_PER_MEDIUM_REVIEW.md`).
**Scope limits:**
- Positives only — does **not** define an experimental non-essential universe.
- `PA0728.1` stays in raw source unchanged; classified `absent_from_model/unmapped`;
  not renamed to PA0728; excluded from identity join only.
- Blank Min sum = missing evidence, **not** zero / not non-essential.
- Full V-01 metrics (specificity, precision, F1, MCC, confusion matrix) remain
  **forbidden** until a separately reviewed negative universe exists.
- Allowed now: positive-label coverage + overlap with
  `mops_pyruvate_lee2015` predictions @ 0.01 only
  (`results/comparison/lee2015_mops_pyruvate_POSITIVE_OVERLAP_ONLY_*`).
**Rationale:** Unblocks the first condition-matched positive-overlap cell without
fabricating negatives or claiming full validation.
**Status:** Active.

## D-21 · 2026-08-01 · MOPS-pyruvate experimental binary universe (Varadarajan2020)
**Decision:** For **primary binary** gene-essentiality validation of iMO1056 under
MOPS-pyruvate / Minimal, use the **Varadarajan et al. 2020** published reanalysis
of the Lee et al. 2015 Tn-seq experiment (`SRP052838`) as the internally
consistent experimental-label source.
**Status:** **APPROVED_FOR_PRIMARY_BINARY_VALIDATION** (human review complete
2026-08-01).

**Evidence source / relationship:**
- Source = Varadarajan2020 Supplementary Dataset 1 (`MPAO1_CDS` master, 5799 CDS)
  + Dataset 4 (`essentialGenes_MPAO1`, Minimal-1/2/3 columns).
- Varadarajan **reuses/reanalyses** Lee2015 Tn-seq with Lee’s released scripts on
  the complete MPAO1 genome. It is **not** an independent experimental replicate
  and must never be presented as one.
- Condition: Minimal-1 / Minimal-2 / Minimal-3 ≡ Lee MOPS-pyruvate pools.

**Label definitions (assay-/condition-specific):**
- **POSITIVE** (`POSITIVE_CONSENSUS_ESSENTIAL`): `minimal_sum >= 2`
  (called essential in ≥2 of 3 Minimal libraries).
- **NEGATIVE** (`NEGATIVE_0_OF_3_NOT_CALLED_ESSENTIAL`): `minimal_sum == 0`
  (not called essential in any of the three Minimal libraries under this
  reanalysis). Do **not** generalize to unconditional biological non-essentiality.
- **AMBIGUOUS** (`AMBIGUOUS_1_OF_3`): `minimal_sum == 1` — retained in provenance
  with explicit exclusion; **excluded** from the primary binary validation
  universe. Do **not** convert to negative.

**Master experimental universe:** all DS1 MPAO1 CDS; DS4 blanks/absence for a
Minimal library encode **not called essential** in that library (Lee-script
remap encoding), not “missing evidence” and not Lee Dataset-S1 absence.

**PAO1 mapping policy:** DS1 `best_hit protein`; primary join requires
`mapping_status = unique_std_PAO1` (`^PA\d{4}$`, single hit). Retain
one-to-many / nonstandard / MPAO1-unique / unmapped explicitly; no silent drop;
no auto-rename of nonstandard IDs.

**iMO1056 evaluable-universe policy:** genes present among `model.genes` /
knockout results (`src/gene_essentiality.py` evaluates all model genes; **no**
extra GPR-only filter). Primary binary = unique-std PAO1 ∩ in iMO1056 ∩
(POSITIVE ∪ NEGATIVE).

**Exclusion policy:** AMBIGUOUS (`EXCLUDED_PRIMARY_BINARY_DISCORDANT_1_OF_3`);
non-unique/nonstandard/no-PAO1 maps; absent from iMO1056; many-MPAO1→one-PAO1
conflicts if observed.

**Separation from D-20:** Keep Lee2015 original-analysis READY positives
(`literature_evidence_gene_level_READY_mops_pyruvate_lee2015.csv`) unchanged as a
separate `POSITIVE_OVERLAP_ONLY` evidence layer. **Do not** mix D-20 Lee-original
positives with D-21 Varadarajan-derived negatives in one primary binary dataset.
For D-21, **both** positives and negatives must come from Varadarajan2020.

**Artifacts:**
- Candidate (preserved): `varadarajan2020_lee2015_minimal_gene_labels_CANDIDATE.csv`
- READY evidence: `varadarajan2020_lee2015_minimal_gene_labels_READY.csv`
- Frozen primary binary: `varadarajan2020_lee2015_minimal_PRIMARY_BINARY_UNIVERSE.csv`
  (expected 214 POSITIVE + 811 NEGATIVE = **1025**; 18 AMBIGUOUS excluded)
- Scripts: `scripts/build_varadarajan2020_minimal_negative_universe_candidate.py`,
  `scripts/promote_varadarajan2020_minimal_labels_ready.py`
- Audit: `project_management/audit/negative_universe_lee2015/`

**Permitted downstream use:** condition-matched binary confusion matrix and
precision/recall/specificity/F1/MCC **only after** a separate V-01 metrics
execution step against `mops_pyruvate_lee2015` predictions. This decision unlocks
that step; it does **not** itself compute or claim those metrics.

**Limitations / caveats:** Negatives are CDS-master complements of Minimal
essential calls from a published essentials-union matrix (DS4), not a separately
published non-essential spreadsheet; remap/annotation differences vs Lee-original
positives exist; MPAO1-unique essentials cannot validate the PAO1 model.
**Rationale:** Human-approved replacement for the deferred negative-universe gate
without fabricating negatives from Lee Dataset-S1 absence or model complements.

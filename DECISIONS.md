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
(Lee, Turner PAO1 rows, Belanger, and new meegid2022) using the **identity**
gene mapping; treat MPAO1 as PAO1-derived with a recorded caveat. Defer PA14
(Basta) and non-PAO1 Poulsen strains until validated orthology exists.
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

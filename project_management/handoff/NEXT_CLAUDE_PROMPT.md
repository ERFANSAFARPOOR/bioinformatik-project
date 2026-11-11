# NEXT_CLAUDE_PROMPT.md — ready-to-paste prompt for the next run

**Current-status notice - 2026-11-11:** the operational instructions below are a
historical July snapshot, not the current continuation plan or a new approval
requirement. All active corpus supplements are present; two DEFINED media and a
PARTIAL LB approximation are implemented; per-medium gene deletions and D-21/V-01
binary metrics exist (1025 genes; TP116/FN98/TN764/FP47). The error audit and review
evidence are prepared; final human interpretation/sign-off remains pending.
Varadarajan2020 is now the approved D-21 binary-label source as a published Lee2015
reanalysis, not independent replication. The current PGD-based integrated mapping
has 1023 unique, 2 ambiguous and 29 unmapped genes; later mapping artifacts do not
automatically broaden the recorded Turner APPROVED_LIMITED policy.

Use the [current readiness report](../audit/VALIDATION_READINESS.md),
[current handoff](../planning/NEXT_STAGE_HANDOFF_REPORT.md),
[label/media alignment](../../VALIDATION_LABEL_MEDIA_OVERLAP.md), and
[decisions](../../DECISIONS.md) before continuing. Earlier “never compute metrics”,
“media not started”, fixed branch/test-count and proposed commit instructions
below describe the old stage only. Preserve the source-data and scientific
integrity constraints, and use current user authorization for the present task.

---

## Historical July snapshot

*(Rewritten 2026-07-07. Supersedes all earlier versions.)*

---

You are continuing the PAO1-focused iMO1056 / MODEL1507180020 metabolic-model
validation project. Work conservatively — a scientific validation repo, not a demo.
Do not fabricate data, source URLs, media, thresholds, mappings, orthology, labels,
or metrics.

## Fixed facts
- **Path:** `I:\Bioinfo\karvarzi\ipynb` · **Branch:** `claude/revival-audit` (only).
- **Env:** `reccobra39`. If `conda` isn't on PATH, use
  `C:/Users/pro/anaconda3/envs/reccobra39/python.exe`. Tests:
  `.../reccobra39/python.exe -m pytest tests/ -q` (must be **8/8** before any work).
- **Never** push, change remotes, edit raw supplements/PDFs/model in place, touch
  `conditian/`, or overwrite `data/processed/literature_evidence.csv`. A guard
  blocks writes under `data/raw/` and `models/raw/` — do not bypass it.
- **No validation metrics** (precision/recall/F1/MCC/specificity/confusion) until
  reviewed evidence + reconstructed media + per-condition predictions all exist.

## Current state (verify with `git log --oneline -8`)
- **Active studies:** Lee 2015 (MPAO1), Turner 2015 (PAO1+PA14), Belanger 2022
  (PAO1), Poulsen 2019 (multi-strain, PA14-referenced), Basta 2017 (PA14).
  Varadarajan 2020 = verified but **derivative of Lee** (mapping resource only).
  Zhu 2018 = background/model. **meegid2022 removed from active scope.**
- **L-03 DRAFT parsed** (Lee/Turner/Belanger) →
  `data/processed/literature_evidence_gene_level_DRAFT.csv` (**5,148 rows**).
  **L03-B3 resolved.** Reviewed + split into derived exports:
  `..._READY_ONLY.csv` (**2,607**) and `..._NEEDS_REVIEW.csv` (**2,541**, all Lee
  per-medium). See `L03_REVIEWED_EVIDENCE_SUMMARY.md`, `LEE2015_PER_MEDIUM_REVIEW.md`.
  Not promoted; Lee per-medium stays NEEDS_REVIEW (pool↔assay ambiguity).
- **C-01b planned** in `C01B_MEDIA_RECONSTRUCTION_PLAN.md` (first batch:
  MOPS-pyruvate, MOPS-succinate DEFINED; SCFM2, LB-approx PARTIAL; RPMI held on
  vitamin gap). **Not started — no bounds, no JSON, no simulation.**
- **Poulsen + Basta:** raw supplements present, thresholds sourced
  (`THRESHOLD_METHOD_AUDIT.md`), but **not parsed** — PA14-indexed, no PAO1 in
  either supplement (Poulsen's 9 strains exclude PAO1) → blocked on validated
  PA14→PAO1 orthology (`POULSEN_BASTA_MAPPING_PLAN.md`). Basta also needs its call
  column derived and a non-growth comparison framework.
- **Media:** `MEDIA_SOURCE_AUDIT.md` done (DEFINED / PARTIAL / MEDIA_GAP_PENDING).
  C-01b **not started**.

## Read first
`L03_REVIEWED_EVIDENCE_SUMMARY.md`, `LEE2015_PER_MEDIUM_REVIEW.md`,
`C01B_MEDIA_RECONSTRUCTION_PLAN.md`, `ORTHOLOGY_READINESS_AUDIT.md`,
`L03_DRAFT_REVIEW_AUDIT.md`, `THRESHOLD_METHOD_AUDIT.md`, `L03_PARSE_BLOCKERS.md`,
`POULSEN_BASTA_MAPPING_PLAN.md`, `MEDIA_SOURCE_AUDIT.md`, `VALIDATION_READINESS.md`,
`BLOCKERS.md`, `TODO.md`, `DATA_PROVENANCE.md`, `SUPPLEMENT_INVENTORY_AUDIT.md`,
`CLAUDE.md`.

## Candidate next tasks (pick per instruction; all gated)
1. **L-03c (promote):** promote the `READY_ONLY` export to a validated table
   (never overwriting canonical `literature_evidence.csv`); resolve Lee per-medium
   pool↔assay ambiguity (confirm `X sum (of N)` counts pools) before promoting
   Min/Sputum. (L03-B3 already resolved.)
2. **G-01b (orthology):** obtain a validated PA14→PAO1 ortholog table
   (pseudomonas.com / study homolog columns) — unblocks Poulsen + Basta. Blocked by
   B-NET (human-assisted/different-network download); store in `data/raw/ortholog/`
   with provenance. Then L-03b: draft-parse Poulsen (sd05/sd02) and Basta (derive
   calls from sd1/sd2 via read-ratio ≤0.25 & Fisher P≤0.05), keeping
   one-to-many/missing explicit.
3. **C-01b (only when asked):** build first-batch media as exchange configs per
   `C01B_MEDIA_RECONSTRUCTION_PLAN.md` (MOPS-pyruvate, MOPS-succinate DEFINED;
   SCFM2, LB-approx PARTIAL). Cite every component→flux conversion; do not invent
   bounds. **Stop before** final condition JSON / S-01 / V-01.

## Stop conditions
Tests fail at start → stop. A study's threshold/mapping cannot be sourced → do not
emit its rows; record in `L03_PARSE_BLOCKERS.md`. Never compute a metric. End
commit messages with the project's Co-Authored-By line.

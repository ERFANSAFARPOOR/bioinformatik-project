# NEXT_CLAUDE_PROMPT.md — ready-to-paste prompt for the next run

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
  `data/processed/literature_evidence_gene_level_DRAFT.csv` (5,093 rows, 6
  phenotype classes distinct, review flags). Not yet human-reviewed/promoted.
- **Poulsen + Basta:** raw supplements present, thresholds sourced
  (`THRESHOLD_METHOD_AUDIT.md`), but **not parsed** — PA14-indexed, no PAO1 in
  either supplement (Poulsen's 9 strains exclude PAO1) → blocked on validated
  PA14→PAO1 orthology (`POULSEN_BASTA_MAPPING_PLAN.md`). Basta also needs its call
  column derived and a non-growth comparison framework.
- **Media:** `MEDIA_SOURCE_AUDIT.md` done (DEFINED / PARTIAL / MEDIA_GAP_PENDING).
  C-01b **not started**.

## Read first
`THRESHOLD_METHOD_AUDIT.md`, `L03_PARSE_BLOCKERS.md`, `POULSEN_BASTA_MAPPING_PLAN.md`,
`MEDIA_SOURCE_AUDIT.md`, `VALIDATION_READINESS.md`, `BLOCKERS.md`, `TODO.md`,
`DATA_PROVENANCE.md`, `SUPPLEMENT_INVENTORY_AUDIT.md`, `CLAUDE.md`.

## Candidate next tasks (pick per instruction; all gated)
1. **L-03c (review/promote):** human-review the Lee/Turner/Belanger DRAFT
   (esp. Lee per-medium `NEEDS_REVIEW` rows); promote reviewed rows to a validated
   table — never overwriting canonical `literature_evidence.csv`.
2. **L03-B3 (Turner paired sheets):** confirm PAO1 column blocks in sd03/04/05/09
   and extend the parser to extract PAO1-only columns.
3. **G-01b (orthology):** obtain a validated PA14→PAO1 ortholog table
   (pseudomonas.com / study homolog columns) — unblocks Poulsen + Basta. Blocked by
   B-NET (human-assisted/different-network download); store in `data/raw/ortholog/`
   with provenance. Then L-03b: draft-parse Poulsen (sd05/sd02) and Basta (derive
   calls from sd1/sd2 via read-ratio ≤0.25 & Fisher P≤0.05), keeping
   one-to-many/missing explicit.
4. **C-01b (only when asked):** begin media reconstruction from the DEFINED/PARTIAL
   sources in `MEDIA_SOURCE_AUDIT.md` (MOPS-pyruvate, MOPS-succinate, RPMI-1640,
   M9, pyruvate-minimal; SCFM2 from Turner sd08). Cite every component; do not
   invent bounds. **Stop before** final condition JSON / S-01 / V-01.

## Stop conditions
Tests fail at start → stop. A study's threshold/mapping cannot be sourced → do not
emit its rows; record in `L03_PARSE_BLOCKERS.md`. Never compute a metric. End
commit messages with the project's Co-Authored-By line.

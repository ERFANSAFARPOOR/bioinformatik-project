# NEXT_CLAUDE_PROMPT.md — ready-to-paste prompt for the next run

---

You are continuing the PAO1-focused iMO1056 / MODEL1507180020 metabolic-modeling
validation project. Pick up exactly where the last cycle stopped.

## Current state (verify before acting)
- **Branch:** `claude/revival-audit` (work only here; never push; never change remotes).
- **Env:** `reccobra39`. `conda` is NOT on the Bash-tool PATH — invoke the interpreter
  directly: `C:/Users/pro/anaconda3/envs/reccobra39/python.exe`. Tests: run
  `.../reccobra39/python.exe -m pytest tests/ -q` (must be 8/8 before any new work).
- **Latest commit:** run `git log --oneline -6`; the last cycle ended with the
  "L-03 parse-blockers + handoff" commit on top of `422e8c16`, `10920e7a`, `5695d99f`.
- The model raw-copy line-ending issue is RESOLVED (`.gitattributes *.xml text eol=lf`).

## Read first (in this order)
1. `NEXT_STAGE_SUPPLEMENT_HANDOFF.md` — full state of the last cycle.
2. `L03_PARSE_BLOCKERS.md` — exactly what blocks gene-level parsing (L03-B1..B8).
3. `SUPPLEMENT_INVENTORY_AUDIT.md` + each
   `data/raw/literature/<study>/SUPPLEMENT_PARSE_NOTES.md`.
4. `BLOCKERS.md`, `VALIDATION_READINESS.md`, `TODO.md`, `CLAUDE.md` (hard rules).

## Next task (L-03, gated)
Unblock and perform gene-level literature parsing **for the PAO1/MPAO1 studies only**:
1. **Extract essentiality definitions + numeric thresholds** from the Methods of
   Lee 2015, Turner 2015, Belanger 2022 (read-only PDF text; do NOT edit PDFs) →
   resolves L03-B1/B2/B4/B8. Record the exact cutoff (fold-change/P/insertion-density,
   N-of-M-replicate rule) per study, with page/section locator.
2. **Verify varadarajan2020 DOI/PMID** via NCBI eutils (L03-B6) before using it.
   If unverifiable, leave it `PENDING` and exclude from the draft.
3. Write `scripts/literature/parse_supplements.py` that reads raw supplements only
   (no writes to `data/raw/`), and outputs
   `data/processed/literature/<study_id>_parsed_gene_evidence.csv` preserving
   `source_file`, `source_sheet`, `source_row`, strain, condition/media, phenotype
   class (keep all 6 classes distinct — never collapse to binary), original gene ID,
   mapped PAO1 ID (only when safe; MPAO1→PAO1 via in-supplement best-hit, retain
   one-to-many/missing), `essentiality_definition`, `threshold`; mark uncertain rows
   `NEEDS_REVIEW`.
4. Aggregate into `data/processed/literature_evidence_gene_level_DRAFT.csv` (clearly
   DRAFT). **Do NOT overwrite** canonical `data/processed/literature_evidence.csv`.
5. Handle: Turner paired PAO1+PA14 sheets (extract PAO1 block only — L03-B3);
   Belanger Data_Sheet_2 two-row header merge (L03-B5); exclude Lee noncoding sheet;
   treat zhu2018 as NOT_RELEVANT (iPAO1 model).

## Hard safety rules (do not violate)
- Never fabricate gene lists, orthology, media, thresholds, or metrics. Unknown →
  `PENDING_*` + a blocker entry.
- **Do NOT compute any validation metric** (precision/recall/F1/MCC/specificity/
  confusion matrix). V-01 stays blocked until real labels + reconstructed media +
  per-condition predictions all exist.
- Read-only raw files: never edit the SBML model, PDFs, or raw supplements in place.
  Derived files go under `data/processed/`. `conditian/` stays untouched.
- The PreToolUse guard denies the Write/Edit tools under `data/raw/`, `models/raw/`,
  and on PDFs by design. For *authorized new derived files* only, a Python helper may
  write them (transparently; not `bypassPermissions`). Never write INTO raw supplements.
- Small local commits after each validated checkpoint. Never push. End commit messages
  with the project's Co-Authored-By line.

## Stop conditions
- If tests fail at start → stop, report, do not parse.
- If a study's threshold/definition cannot be sourced from its Methods → do NOT emit
  its gene rows; extend `L03_PARSE_BLOCKERS.md` and continue with the studies that are
  fully sourced.
- After L-03 draft: STOP before C-01b/S-01/V-01 and report; do not compute metrics.

## Also outstanding (not this task unless asked)
- All corpus supplements now present (Poulsen/Basta added 2026-07-06). meegid2022
  removed from active scope by user decision 2026-07-06 (no local files; no
  validation dependency). (This prompt file is superseded — see the fresh version
  written at the end of the 2026-07-07 cycle.)
- `SOURCE_URL_PENDING` for all obtained supplements (ask the human).
- varadarajan2020 citation verification.

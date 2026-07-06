# L03_PARSE_BLOCKERS.md

**Date:** 2026-07-06 · **Branch:** `claude/revival-audit` · **Env:** `reccobra39`
**Decision:** L-03 gene-level extraction is **NOT performed this cycle.** The
Phase E gate requires that, per study, *all* of {gene/locus-tag column, strain
context, condition/media context, phenotype/essentiality column, **threshold /
statistical definition**, source sheet+row locator, mapping status} be clear.
Columns and locators are clear (see each `SUPPLEMENT_PARSE_NOTES.md`), but the
**per-study essentiality threshold / statistical definition is not yet confirmed
from the papers' Methods**, which Hard Rule 6 requires on every evidence row.
No `literature_evidence.csv` / DRAFT gene rows were written. Nothing fabricated.

## Why not just parse the author-provided calls?
Several sheets carry a pre-computed call (Turner `Essential?`; Lee "General
essential genes" membership; Belanger `Tradis`/`Transit`/`Both`/`NE`). These give
the *label*, but Hard Rule 6 also requires the **definition + numeric threshold**
behind that label (e.g. the fold-change / P-value / insertion-density cutoff and
the "N of M replicates" rule). Those cutoffs are stated in each paper's Methods,
which have **not** been extracted. Emitting rows now would leave `threshold` /
`essentiality_definition` as unsourced blanks — exactly what the gate forbids.

## Per-study blockers (what is needed to unblock L-03)

### lee2015 — closest to ready
- **Clear:** gene col `PA number` (PAO1), strain=MPAO1, media columns, generally-
  essential membership, locators.
- **BLOCKER L03-B1:** confirm from Lee 2015 Methods the definition of "essential"
  and the **per-medium threshold** (what `LB/Min/Sputum sum` value ⇒ essential in
  that medium; and the aggregate rule for "General essential genes").
- Generally-essential membership could be parsed with `threshold=PENDING` + this
  blocker; per-condition rows need L03-B1 resolved first.

### turner2015 — closest to ready (sd01)
- **Clear:** `Locus ID` (PAO1), `Essential?`/`Mode`, fold-change + P, condition from
  table title, locators.
- **BLOCKER L03-B2:** confirm from Turner 2015 Methods the exact rule behind
  `Essential?` and `Mode` (fold-change and P-value cutoffs; pseudodata model), and
  the fitness-call cutoffs for sd06/07/09/10.
- **BLOCKER L03-B3:** for paired PAO1+PA14 sheets (sd03/04/05/09), confirm the PAO1
  column-block boundaries before extracting (2-row header; avoid grabbing PA14 cols).

### belanger2022
- **Clear:** `Locus Tag` (PAO1), conditions, per-condition tool calls, locators.
- **BLOCKER L03-B4:** confirm the meaning/threshold of `Tradis`/`Transit`/`Both`/`NE`
  (does a single-tool call count as essential? what are the TraDIS/Transit cutoffs?).
- **BLOCKER L03-B5:** implement the **two-row header merge** for Data_Sheet_2 so
  condition columns (`RPMI/Serum`,`RPMI`,`Abscess`,`Skin`) are named correctly.

### varadarajan2020
- **BLOCKER L03-B6:** **verify the citation** (DOI/PMID) — currently `PENDING_VERIFY`;
  cannot be used until confirmed.
- **BLOCKER L03-B7:** build + validate the **MPAO1→PAO1 mapping** from DS1/DS3
  `best_hit`/`PAO1_gene_name` (retain one-to-many + missing per project rule 3).
- **BLOCKER L03-B8:** confirm the "essential in N/16 samples" threshold and the
  per-condition (LB/Minimal/Sputum/HumanSerum) essentiality rule from Methods.

### zhu2018
- **Not a blocker — out of scope.** iPAO1 is a *model*, not experimental labels
  (`NOT_RELEVANT_FOR_L03`).

## Exact next actions to satisfy the gate (next cycle)
1. Extract the essentiality **definitions + numeric thresholds** from the Methods of
   Lee 2015, Turner 2015, Belanger 2022 (read-only PDF text extraction) → resolves
   L03-B1/B2/B4/B8.
2. Verify varadarajan2020 DOI/PMID (CrossRef/NCBI eutils) → L03-B6.
3. Then implement `scripts/literature/parse_supplements.py` to emit
   `data/processed/literature/<study_id>_parsed_gene_evidence.csv` with
   `source_file/source_sheet/source_row`, strain, condition, phenotype_class (6
   classes kept distinct), original gene ID, mapped PAO1 ID (only when safe),
   `essentiality_definition`, `threshold`, and `NEEDS_REVIEW` for uncertain rows.
4. Only after review, promote to `data/processed/literature_evidence_gene_level_DRAFT.csv`
   (clearly DRAFT), never overwriting canonical `literature_evidence.csv`.

## Guardrails held
- No metrics computed. No gene lists / thresholds / orthology / media fabricated.
- No raw supplement, PDF, or model file modified. `conditian/` untouched.

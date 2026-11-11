# NEXT_STAGE_SUPPLEMENT_HANDOFF.md

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

**Date:** 2026-07-06 · **Branch:** `claude/revival-audit` · **Env:** `reccobra39`

## Repo status
Safe. Working on `claude/revival-audit`; no push; remotes unchanged; no raw file
deleted or modified in place; `conditian/` untouched. Tests **8/8 pass**.

## Commits created this cycle (local only, not pushed)
| SHA | Phase | Summary |
|-----|-------|---------|
| `5695d99f` | A | Fix raw model archive line endings and restore byte identity |
| `10920e7a` | B/C | Audit downloaded supplements and update provenance |
| `422e8c16` | D | Add supplement parse notes for downloaded studies |
| `<this commit>` | E/F | L-03 parse-blockers + handoff + next prompt |

## Model-copy discrepancy — RESOLVED
`test_raw_copy_is_byte_identical` failed because `core.autocrlf=true` checked out
the LF-stored `models/raw/…xml` blob as CRLF (working-tree drift only; git history
was fine). Proven semantically identical to the canonical model, then rewrote the
working copy to LF (both SHA `0868a5eb…1212ead`); added `.gitattributes`
(`*.xml text eol=lf`). Canonical model untouched. Details:
`MODEL_COPY_DISCREPANCY_REPORT.md`. **Tests now 8/8.**

## Supplement inventory summary (`SUPPLEMENT_INVENTORY_AUDIT.md`)
- `data/raw/lituare/` (typo) — **does not exist**; no misfiling, no move needed.
- `data/raw/literature/` — 7 study folders; 54 real files (all `.xlsx` readable).
- Machine-readable manifest: `data/processed/literature/supplement_inventory.tsv`.

### Expected files present
- **lee2015** (MPAO1, P0): `pnas.1422186112.sd01.xlsx` ✅ (+ Supporting Info PDF).
- **turner2015** (PAO1+PA14, P0): `sd01–sd10.xlsx` ✅ (expected only sd01–04; sd05–10
  are extra and mostly useful; sd08 = SCFM2 media recipe → C-01b).
- **belanger2022** (PAO1, P0): `Data_Sheet_1/2.XLSX` ✅ (+ `Data_Sheet_3.docx`).

### Expected files missing
- (Historical snapshot; superseded 2026-07-06.) **poulsen2019** and **basta2017**
  are now **present** (user-added; see `SUPPLEMENT_INVENTORY_AUDIT.md`,
  `DATA_PROVENANCE.md §3d`). **meegid2022** was **removed from active scope by user
  decision 2026-07-06** (no local files; no validation dependency).

### Unexpected folders/files
- **varadarajan2020** (MPAO1) — TnSeq essentiality (`Supplementary Dataset 4`) +
  MPAO1→PAO1 mapping (DS1/DS3). **Candidate P0/P1**, but **DOI/PMID unverified**.
- **zhu2018** — GigaScience giy021 **iPAO1 metabolic reconstruction** (a *model*).
  **Background, out-of-scope** for experimental labels (`NOT_RELEVANT_FOR_L03`).
- **Duplicates:** none (all SHA-256 distinct). **Unreadable:** none.

## Documentation updated
`DATA_PROVENANCE.md` (§1 line-ending note; new §3d supplement provenance),
`TODO.md` (L-05 partial/done, L-03 in-progress, 2026-07-06 update),
`BLOCKERS.md` (B-LIT-01 narrowed; B-NET note; B-COND-01/B-SCI-01 kept open),
`VALIDATION_READINESS.md` (§0 raw supplements present, metrics still forbidden),
`REVIEW_EXPORT_CHECKLIST.md` (§7 download status), `PAO1_VALIDATION_DATA_INVENTORY.md`
(supplement-in-repo column). `papers/manifest.csv` **not** changed (varadarajan2020/
zhu2018 citations unverified — would risk fabrication).

## Parse notes created
`data/raw/literature/<study>/SUPPLEMENT_PARSE_NOTES.md` for lee2015, turner2015,
belanger2022, varadarajan2020, zhu2018 (sheet/column structure, gene/strain/
condition/essentiality/threshold columns, locators, PAO1 mapping, phenotype class,
readiness tag).

## Was L-03 gene-level parsing performed?
**No.** Gated (`L03_PARSE_BLOCKERS.md`). Columns/locators are clear, but the
**per-study essentiality threshold / statistical definition is not yet confirmed
from the papers' Methods** (Hard Rule 6 requires it on every row). No gene-level
rows, no DRAFT, nothing fabricated.

### Exact blockers to unblock L-03
- L03-B1/B2/B4/B8: extract essentiality **definitions + numeric thresholds** from
  Methods of Lee 2015, Turner 2015, Belanger 2022, Varadarajan 2020.
- L03-B3: confirm PAO1 column blocks in Turner paired sheets (sd03/04/05/09).
- L03-B5: two-row-header merge for Belanger Data_Sheet_2.
- L03-B6: verify varadarajan2020 DOI/PMID.
- L03-B7: build + validate MPAO1→PAO1 mapping (one-to-many/missing retained).

## Remaining P0 blockers
- **B-SCI-01** (no real metric; nb03 simulated) — OPEN.
- **B-COND-01** (per-condition media not reconstructed) — OPEN.
- **B-LIT-01** — narrowed: all corpus supplements now present; OPEN only for
  Poulsen/Basta orthology-threshold gate + DRAFT promotion (meegid2022 out of scope).
- **B-NET** — OPEN (pseudomonas.com orthology + all `SOURCE_URL_PENDING`).
- B-MAP-01 — P1/secondary (PA14-only path); **PARTIALLY RESOLVED** (PGD export local; crosswalk + human review pending).

## Next recommended scientific stage
1. **L-03 (unblock then parse):** extract thresholds from Methods PDFs (read-only) →
   `scripts/literature/parse_supplements.py` →
   `data/processed/literature/<study>_parsed_gene_evidence.csv` →
   `literature_evidence_gene_level_DRAFT.csv` (6 phenotype classes distinct).
2. **C-01b:** reconstruct PAO1 media (LB, MOPS-succinate, **SCFM2 from Turner sd08**,
   RPMI±serum from Belanger) as exchange configs with citations.
3. **S-01:** per-condition single-gene deletion predictions.
4. **V-01:** metrics — **still forbidden** until real labels + media + predictions exist.

## Update 2026-07-07c (latest)
- **L-03 DRAFT reviewed into derived exports** (canonical untouched):
  `..._READY_ONLY.csv` (2,607) + `..._NEEDS_REVIEW.csv` (2,541, all Lee per-medium).
  See `L03_REVIEWED_EVIDENCE_SUMMARY.md`.
- **`LEE2015_PER_MEDIUM_REVIEW.md`:** Lee per-medium rows stay NEEDS_REVIEW
  (conservative); Min/Sputum near-resolvable, LB ambiguous, singles low-confidence.
- **`C01B_MEDIA_RECONSTRUCTION_PLAN.md`:** first-batch media planned (MOPS-pyruvate,
  MOPS-succinate DEFINED; SCFM2, LB-approx PARTIAL; RPMI held). **C-01b NOT started;
  no bounds; no JSON; no simulation. S-01/V-01 not started; metrics forbidden.**

## Update 2026-07-10b (PGD orthology integration)
- **PGD ortholog export merged** from `origin/develop` (`7cd3dd29`): **5,385** PAO1↔PA14
  pairs in `data/raw/ortholog/` (vs Turner APPROVED_LIMITED 5,365; +20 PGD-only).
- **Decision D-16:** PGD supplements/validates Turner; does **not replace**
  APPROVED_LIMITED until PGD↔Turner crosswalk + human review.
- **B-MAP-01 partially resolved:** authoritative source now local; crosswalk pending.
- PGD confirms Turner locus assignments (PA2279↔PA14_35100, PA2277↔PA14_35130).
- `tst ortolog/` = exploratory pipeline workspace; relocate to archive later (do not delete).
- Doc: `docs/ORTHOLOGY_PSEUDOMONAS_INTEGRATION.md`. SHA-256 for PGD files pending.
- Poulsen/Basta: eligible for future controlled L-03b draft mapping — **not**
  validation-ready. Metrics still forbidden. No `gene_mapping.csv` merge.

## Update 2026-07-10 (orthology APPROVED_LIMITED)
- Human review: **APPROVED_LIMITED**; conflict **RESOLVED_SUPPORTS_TURNER**
  (KEGG SSDB: PA14_35100↔PA2279, PA14_35130↔PA2277).
- Derived: `pao1_pa14_orthologs_turner2015_APPROVED_LIMITED.csv` (5,365 rows).
- PA14→PAO1 mapping candidate approved for **limited 1:1 draft mapping only**.
- Poulsen/Basta: eligible for future controlled L-03b draft mapping — **not**
  validation-ready. Metrics still forbidden. CANDIDATE unchanged; no
  `gene_mapping.csv` merge.

## Update 2026-07-07b
- **L03-B3 RESOLVED:** Turner paired-sheet PAO1 blocks parsed (sd05 condition-
  specific-essential + sd09 reduced-fitness); DRAFT now **5,148 rows**. Full
  integrity review in `L03_DRAFT_REVIEW_AUDIT.md` (all checks pass).
- **`ORTHOLOGY_READINESS_AUDIT.md`:** no validated PA14→PAO1 orthology exists →
  Poulsen + Basta stay mapping-blocked (both PA14-referenced; Poulsen's 9 strains
  exclude PAO1).
- **`MEDIA_SOURCE_AUDIT.md` refined** (+NOT_RECONSTRUCTABLE_AS_GROWTH_MEDIUM).
- meegid2022 scope-removal notes tightened. C-01b/S-01/V-01 still not started.

## Update 2026-07-07 (this cycle)
- **L-03 DRAFT parsed** for Lee/Turner/Belanger (`literature_evidence_gene_level_DRAFT.csv`).
  Varadarajan verified but derivative (mapping resource only). Zhu out of scope.
- **meegid2022 removed from active scope** (user decision) — no local files, no dependency.
- **Poulsen 2019 + Basta 2017 audited** (thresholds sourced) but **not parsed** —
  PA14-indexed, no PAO1 in either supplement (Poulsen's 9 strains exclude PAO1) →
  blocked on validated PA14→PAO1 orthology (`POULSEN_BASTA_MAPPING_PLAN.md`, L03-B9/B10).
- **`MEDIA_SOURCE_AUDIT.md` created** (per-study media locators + reconstructability).
  C-01b **not started**; no exchange bounds invented; no simulation.
- Fresh next-run prompt: `NEXT_CLAUDE_PROMPT.md` (rewritten 2026-07-07).

## Next recommended scientific stage (superseded by the 2026-07-07 update above)
1. **L-03 (unblock then parse):** extract thresholds from Methods PDFs (read-only) →
   `scripts/literature/parse_supplements.py` →
   `data/processed/literature/<study>_parsed_gene_evidence.csv` →
   `literature_evidence_gene_level_DRAFT.csv` (6 phenotype classes distinct).
2. **C-01b:** reconstruct PAO1 media (LB, MOPS-succinate, **SCFM2 from Turner sd08**,
   RPMI±serum from Belanger) as exchange configs with citations.
3. **S-01:** per-condition single-gene deletion predictions.
4. **V-01:** metrics — **still forbidden** until real labels + media + predictions exist.

## Guardrails held all cycle
No push; no remote change; no raw deletion; no in-place edit of raw model/PDF/
supplement; `conditian/` preserved; no metrics; nothing fabricated; unknowns kept as
`PENDING_*` with blockers.

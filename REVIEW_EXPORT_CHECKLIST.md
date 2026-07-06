# REVIEW / EXPORT CHECKLIST

**Date:** 2026-07-01 · **Branch:** `claude/revival-audit`
**Scope:** Consistency cleanup pass on the PAO1-focused project reports (no new
analysis, no downloads, no metrics). Confirms the docs now agree with the
corrected 2026-07-01 strain audit (B-STRAIN-02) before the next validation stage.

---

## 1. Consistency fixes made

1. **DATA_PROVENANCE.md §2** — replaced the old preliminary strain labels with the
   corrected 2026-07-01 audit:
   - Turner 2015 → **PAO1 + PA14**; Lee 2015 → **MPAO1**;
     Poulsen 2019 → **multi-strain (incl. PAO1)**; Basta 2017 → **PA14**;
     Belanger 2022 → **PAO1**; Juhas 2015 → **review**.
   - Filled Basta/Belanger verified year + DOI + journal (were PENDING_VERIFY).
   - Retabled to show canonical `papers/` path with legacy `conditian/` path in
     parentheses; stated **`papers/` is canonical, `conditian/` is legacy/preserved**.
   - Kept the §2b copy provenance + SHA-256 details; reworded the "Corrections vs §2"
     note so it is not stale (labels now also reflected in §2; points to B-STRAIN-02).

2. **VALIDATION_READINESS.md** — **B-MAP-01 downgraded to P1/secondary**:
   - §1 verdict: now lists four P0 blockers (B-SCI-01, B-LIT-01, B-NET, B-COND-01);
     B-MAP-01 called out as P1/secondary (PA14-only / non-PAO1 only).
   - §7 blocker table: B-MAP-01 row changed P0 → **P1 / secondary** with scope note.
   - Added a callout: the first PAO1/MPAO1 validation is strain-unblocked because
     Lee (MPAO1), Belanger (PAO1), Turner PAO1 rows, and meegid2022 (PAO1) map by
     **identity** — no PA14 orthology needed.

3. **TODO.md G-01** — **P0 → P1**; reason rewritten. No longer says "most
   experiments are PA14". Now: needed only for the PA14-only path (Basta 2017;
   non-PAO1 Poulsen strains); PAO1/MPAO1 sources join by identity.

4. **BLOCKERS.md B-LIT-02** — removed the outdated "strains still to confirm"
   note; strains now confirmed (Basta = PA14; Belanger = PAO1) with a reference to
   the resolved strain-correction record **B-STRAIN-02**.

5. **manifest.csv / gene_mapping.csv** — verified (read-only), no edits needed:
   - `papers/manifest.csv` already agrees with the corrected strain audit
     (Turner PAO1+PA14, Lee MPAO1, Poulsen multi incl. PAO1, Basta PA14,
     Belanger PAO1, Juhas review).
   - `data/processed/gene_mapping.csv`: **1054** rows (PAO1 identity mappings);
     PA14 layer is **provisional/symbol-based only** (386 medium + 22 low = 408
     with a PA14 handle; 646 unmapped); **22 ambiguous** rows retained
     (`ambiguous=True`, candidates kept); source = NCBI RefSeq feature tables
     (annotation, **not** validated orthology). No orthology fabricated.

---

## 2. Files updated

| File | Change |
|---|---|
| `DATA_PROVENANCE.md` | §2 strain/year/DOI corrections; canonical papers/ vs legacy conditian/; §2b note reworded |
| `VALIDATION_READINESS.md` | B-MAP-01 → P1/secondary (§1 + §7); identity-join callout added |
| `TODO.md` | G-01 P0 → P1; reason rewritten |
| `BLOCKERS.md` | B-LIT-02 strain-confirmation note updated; B-STRAIN-02 referenced |
| `REVIEW_EXPORT_CHECKLIST.md` | new (this file) |

Not modified (read-only verification only): `papers/manifest.csv`,
`data/processed/gene_mapping.csv`. Raw PDFs, raw model, raw datasets, and
`conditian/` untouched.

---

## 3. Tests result

```
conda run -n reccobra39 python -m pytest tests/ -q
........                                                                 [100%]
8 passed in 2.10s
```

All 8 tests pass under `reccobra39` (Python 3.9.23). The guard test still asserts
no validation-metrics file exists yet (metrics remain gated).

---

## 4. Remaining P0 blockers

| Blocker | Blocks |
|---|---|
| **B-SCI-01** | Any real metric — nb03 comparison is on simulated random labels |
| **B-LIT-01** | Experimental gene-level labels — supplements not yet downloaded |
| **B-NET** | The downloads + validated orthology (PNAS/Frontiers/mBio 403; pseudomonas.com + PMC OA blocked here) |
| **B-COND-01** | Per-condition media reconstruction (LB, SCFM/MOPS, host-mimicking) |

Secondary (P1, off the first-validation critical path): **B-MAP-01** — validated
PAO1↔PA14 orthology, needed only for Basta 2017 (PA14) and non-PAO1 Poulsen strains.

V-01 (compute metrics) stays **BLOCKED** until supplements are parsed, media are
reconstructed, and per-condition predictions are generated.

---

## 5. Human-assisted supplement download priority (exact)

PAO1/MPAO1 first (join by identity — no orthology). Store each under
`data/raw/literature/<study_id>/` with provenance + SHA-256; **never edit raw in place**.

| # | Study | Strain | File(s) | Source |
|---|---|---|---|---|
| 1 | **Lee 2015** | MPAO1 | `pnas.1422186112.sd01.xlsx` | PNAS DCSupplemental (DOI 10.1073/pnas.1422186112) |
| 2 | **Turner 2015** | PAO1 rows | `pnas.1419677112.sd01–sd04.xlsx` | PNAS DCSupplemental (DOI 10.1073/pnas.1419677112) |
| 3 | **Belanger 2022** | PAO1 | Frontiers supplementary data files | Frontiers (DOI 10.3389/fmicb.2022.1055512) |
| 4 | **meegid2022** | PAO1 | full text + supplement | PMID 35104681 (not OA here) |
| 5 | **Poulsen 2019** | PAO1 per-strain | PNAS SI + fitness data | PNAS + `data.broadinstitute.org/fitness/` + `github.com/broadinstitute/FiTnEss` |
| 6 | **Basta 2017** | PA14 (needs orthology) | mBio supplement | mBio (DOI 10.1128/mBio.01170-17) — deferred; requires B-MAP-01 |

After download: log in `DATA_PROVENANCE.md §3`, add `SUPPLEMENT_PARSE_NOTES.md`,
then proceed L-03 (parse → `literature_evidence.csv`, 6 phenotype classes distinct).

---

## 6. Files to send to ChatGPT next

For the human-assisted download/parse handoff (context + targets):

1. `REVIEW_EXPORT_CHECKLIST.md` (this file — the handoff summary)
2. `papers/manifest.csv` (per-study strain, DOI, supplement availability, locus system)
3. `DATA_PROVENANCE.md` (§2b verified IDs; §3 download-attempt log)
4. `VALIDATION_READINESS.md` (what is missing before metrics; blocker gate)
5. `PAO1_PAPER_RELEVANCE_AUDIT.md` (strain re-audit evidence)
6. `docs/PAO1_LITERATURE_SEARCH_STRATEGY.md` (candidate datasets incl. meegid2022)
7. `BLOCKERS.md` (B-NET/B-LIT-01/B-COND-01 exact scope) and `TODO.md` (L-05/L-03/C-01b/S-01 path)

Purpose of the handoff: obtain the six PAO1/MPAO1-first supplements above via a
human/unblocked network, with provenance, so L-03 → C-01b → S-01 → V-01 can proceed.
Do **not** fabricate any gene list, orthology, or metric.

---

## 7. Update 2026-07-06 — L-section downloads received & audited

The §5 human-assisted download handoff has **partly completed**. Status of the §5 table:

| # | Study | Obtained? | Notes |
|---|-------|:---------:|-------|
| 1 | Lee 2015 (MPAO1) | ✅ | `sd01.xlsx` + Supporting Information PDF |
| 2 | Turner 2015 (PAO1) | ✅ **+extra** | `sd01–sd10.xlsx` (all 10; sd08 = SCFM2 media recipe → C-01b) |
| 3 | Belanger 2022 (PAO1) | ✅ | `Data_Sheet_1/2.XLSX` + `Data_Sheet_3.docx` |
| — | Varadarajan 2020 (MPAO1) | ✅ **bonus** | `Supplementary Dataset 1–4`; **DOI/PMID PENDING verification** |
| 4 | meegid2022 (PAO1) | ❌ | no folder — still needed |
| 5 | Poulsen 2019 | ❌ | folder empty — still needed |
| 6 | Basta 2017 (PA14) | ❌ | folder empty — deferred (orthology) |

Done this cycle: model raw-copy line-ending fix (tests 8/8); supplement inventory
audit (`SUPPLEMENT_INVENTORY_AUDIT.md`); provenance (`DATA_PROVENANCE.md §3d` +
`data/processed/literature/supplement_inventory.tsv`); parse notes per study
(`data/raw/literature/<study>/SUPPLEMENT_PARSE_NOTES.md`). **Still outstanding for
the human:** source download URLs (`SOURCE_URL_PENDING`), varadarajan2020 citation,
and the 3 missing studies. **Metrics remain forbidden** (B-SCI-01/B-COND-01).

# L_STAGE_REPO_STATUS.md — Phase 0 Repository Safety Check

**Date:** 2026-07-06
**Branch:** `claude/revival-audit`
**Environment:** `reccobra39` (Python `C:\Users\pro\anaconda3\envs\reccobra39\python.exe`)
**Purpose:** Controlled repo + supplement-status check before L-section parsing.

## UPDATE 2026-07-06: ✅ RESOLVED — tests now 8/8 pass, safe to continue

The failing test was diagnosed (see `MODEL_COPY_DISCREPANCY_REPORT.md`) as a
**CRLF-vs-LF line-ending difference only**; the two model files were proven
semantically identical. Under explicit user approval (Option A), the archived copy
`models/raw/paeruginosa_MODEL1507180020.xml` was rewritten byte-identical to the
canonical model (both SHA `0868a5eb…1212ead`); `.gitattributes` was added to pin
LF. **`pytest tests/ -q` → 8 passed, 0 failed.** The canonical model was not
modified. The audit then proceeded to Phases B–F. The original halt report is
retained below for the record.

---

## ORIGINAL RESULT (superseded): ⛔ one test FAILED (stop-and-report gate)

Per the standing rule *"If tests fail, stop and report. Do not continue to
parsing or documentation updates,"* the audit halted after Phase 0. **No files
were moved, no provenance/documentation was updated, no parse notes were
created.** The failure is a **pre-existing integrity discrepancy in the archived
model provenance copy** and is **unrelated to the L-section supplement
downloads** (nothing under `models/` was touched by that work; working tree is
clean).

---

## 1. Current branch
`claude/revival-audit` ✅ (correct working branch)

## 2. Git status (`git status --short`)
Clean — no untracked or modified files in the working tree. ✅

## 3. Recent history (`git log --oneline --decorate -5`)
```
a6692193 (HEAD -> claude/revival-audit) Merge develop into Claude audit branch
d7f6f1cd (origin/develop, develop) Add literature PDFs and supplementary datasets
4c2a297e Two additional papers, and their supplements are added
7ac68134 Lee supplementary files were added
5ca97298 Add literature raw data folder structure
```

## 4. Active Python
- Default `python` resolves to the canonical env: `C:\Users\pro\anaconda3\envs\reccobra39\python.exe` ✅
- Note: `conda` is **not on the Bash-tool PATH**, so `conda run -n reccobra39 …`
  fails with `conda: command not found`. Tests/imports were run by invoking the
  env interpreter directly (`.../envs/reccobra39/python.exe`), which is the same
  interpreter `conda run` would select. This is a tooling-PATH quirk, not an
  environment problem.

## 5. Imports
`import cobra, pandas, openpyxl` → `ok` ✅ (cobra 0.29.1, pandas, openpyxl all import)

## 6. Tests (`python -m pytest tests/ -q`)
**1 failed, 7 passed.**

| Test | Result |
|------|--------|
| test_raw_model_present_and_unmodified | ✅ PASS (canonical model SHA correct) |
| test_raw_copy_is_byte_identical | ❌ **FAIL** |
| test_model_loads_and_counts | ✅ PASS (1110 rxn / 879 met / 1054 genes) |
| test_model_identity_pao1 | ✅ PASS (MODEL1507180020, all PAxxxx, no PA14_) |
| test_objective_is_biomass | ✅ PASS |
| test_default_growth | ✅ PASS (WT ≈ 1.0479285528) |
| test_predicted_essentiality_file | ✅ PASS (1054 rows, 166 essential) |
| test_no_validation_metrics_yet | ✅ PASS (no stray metrics files) |

### Failing test detail
`tests/test_model_and_data.py::test_raw_copy_is_byte_identical` asserts the
archived copy `models/raw/paeruginosa_MODEL1507180020.xml` equals the pinned
`EXPECTED_SHA`. It does not.

| File | Size (bytes) | SHA-256 |
|------|-------------|---------|
| `models/paeruginosa_MODEL1507180020.xml` (canonical, used for all science) | 1,668,096 | `0868a5eb…1212ead` ✅ matches EXPECTED |
| `models/raw/paeruginosa_MODEL1507180020.xml` (archived provenance copy) | 1,685,085 | `1b9cdd98…868b4b0` ❌ differs (~17 KB larger) |
| EXPECTED_SHA (test + README) | — | `0868a5eb…1212ead` |

**Interpretation (not yet confirmed — needs human decision):** The canonical
model that all analyses load is intact and correct; every science-bearing test
passed. The mismatch is confined to the *archived provenance copy* under
`models/raw/`, which is larger than the canonical file. This is consistent with
the archive being a *differently-serialized or original-formatted* copy rather
than a byte-identical duplicate — but `models/README.md` (lines 16, 28) claims it
is "byte-identical," and the test enforces that claim. Root cause (was the
archive the true untouched original, or was it corrupted/re-saved?) **cannot be
determined without human input** and must not be guessed. Raw model files are
read-only; neither file was or will be edited to "fix" the hash.

## 7. Folder / structure checks
- `conditian/` — **preserved and untouched** ✅ (6 PDFs present: corrieR, davidW,
  juhas2015, keith H, polsun2019, samuelA; unchanged since Jun 26).
- `data/raw/lituare/` (typo path) — **does NOT exist** ✅ (no accidental misfiling).
- `data/raw/literature/` — **exists** ✅, with 7 study folders (see below).
- Unexpected content: the supplement set is **broader than the Phase 1 expected
  list** — folders `varadarajan2020/` and `zhu2018/` exist (not in the expected
  list), and `turner2015/` contains **sd01–sd10** (expected only sd01–sd04).
  These are extra files to inventory, not errors; full audit is deferred to
  Phase 1 (blocked by the test gate).

### Study folders present (raw counts, unverified)
| Folder | Contents |
|--------|----------|
| `basta2017/` | only `.gitkeep` (empty — expected; deferred, PA14) |
| `belanger2022/` | Data_Sheet_1.XLSX, Data_Sheet_2.XLSX, Data_Sheet_3.docx |
| `lee2015/` | pnas.1422186112.sd01.xlsx, "Supporting Information.pdf" |
| `poulsen2019/` | only `.gitkeep` (empty) |
| `turner2015/` | pnas.1419677112.sd01–sd10.xlsx (10 files) |
| `varadarajan2020/` | Supplementary Dataset 1–4 (MPAO1).xlsx, Supp Info + Reporting Summary PDFs |
| `zhu2018/` | 6 PDFs (submission/revision/reviews) + `giy021_supp/` (27 additionalFile*.xlsx/docx) |

## Recommendation
**NOT SAFE to continue to Phases 1–3 (moves, provenance updates, parse notes)
until the `models/raw` integrity discrepancy is resolved by a human.** The
working model is scientifically sound, but the user's own gate ("if tests fail,
stop") is tripped, and the correct resolution (re-archive the true original vs.
correct the pinned SHA/README) is a provenance decision that must not be
fabricated.

### Options for the human (pick one — do not let the model choose)
1. **Re-archive:** replace `models/raw/…xml` with a byte-identical copy of the
   canonical file, if the canonical is confirmed authoritative. (Changes the
   archive, so needs explicit approval; raw files are otherwise read-only.)
2. **Re-pin:** if the *larger* `models/raw` file is actually the untouched
   original BioModels download and the canonical is a re-serialized derivative,
   correct the test + README to record two distinct SHAs (original vs. working)
   with provenance for both.
3. **Confirm origin first:** provide the original BioModels download provenance
   so we can tell which of the two files is the true original.

No `models/` files were modified during this check. Awaiting human decision
before any further phase runs.

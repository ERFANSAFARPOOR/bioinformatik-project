# Project work model and next steps (for the team)

**Date:** 2026-07-21; status reconciled **2026-11-11**
**Audience:** Project teammates (anyone continuing the scientific path)  
**Scope:** Guidance and decisions only — no code, notebooks, or media configs are created by this document.  
**Scientific focus:** Model iMO1056 = **PAO1**; first validation path uses PAO1/MPAO1 evidence only.

---

## 1. Project goal in one view

This repository supports **gene-essentiality** analysis with a genome-scale metabolic
model (*P. aeruginosa* PAO1, iMO1056). The scientific goals are:

1. Predict essential genes under documented media conditions  
2. Compare condition-matched predictions to **PAO1/MPAO1** experimental evidence  
3. Report limitations honestly (no fabricated metrics)

The three teaching notebooks (`01` / `02` / `03`) are archived under
`archive/teaching_notebooks/`. Research notebooks `04_media_reconstruction` and
`05_condition_essentiality` exist. The first real binary evaluation is implemented
by the V-01 script and reports; its final human interpretation is pending.

---

## 2. Resume, paper, and “live demo” — short guidance

### 2.1 If the paper is not published, what still helps a resume?

A journal reviewer is strict; a resume is more flexible — but **simulated numbers
or “validation” claims without real labels + media** hurt both. If a full paper is
not possible yet, these outputs are still worth listing and showing:

| Deliverable | Why it helps a resume |
|---|---|
| Reproducible repo (locked env, tests, provenance) | Shows scientific engineering skill |
| Documented orthology (Turner APPROVED_LIMITED + PGD) | Real mapping work with scientific decisions |
| Literature evidence tables with provenance | Systematic curation skill |
| Implemented media configurations + cited bounds and assumptions | Applied FBA skill |
| Multi-medium essentiality predictions (without fake validation claims) | Explainable interview demo |
| Explicit limitation reports | Scientific maturity, not just “pretty numbers” |

**Do not put on a resume:** precision/recall from `nb03` (labels are random).

### 2.2 Minimum defensible paper path

For a reviewer-defensible model validation, this chain is required:

```
reviewed condition-specific PAO1/MPAO1 labels (D-21 for the first cell)
        +
documented in-model media (C-01b)
        +
gene-deletion predictions under the same conditions (S-01)
        ↓
real metrics (V-01) — only after the three above
```

Without all three, a “model validation” paper is weak or indefensible.

### 2.3 What is a “live demo”?

It does **not** mean building a website. It means:

> Open a laptop in front of a supervisor or interviewer, activate the env, run a
> research notebook top-to-bottom, and explain: this is the model, this is the
> medium, these genes are predicted essential, and these are the limitations.

For resume/interview purposes this often matters more than an unfinished paper,
because it shows **practical skill**. For a journal reviewer, a demo is not enough —
methods and data must be in the manuscript/supplement.

---

## 3. Recommended team work model (Jupyter + `src/`)

Decision: keep **Jupyter** for readability, but put reusable logic in **`src/`**.

| Layer | Role | Examples |
|---|---|---|
| `src/` | Testable functions, no UI | `load_model`, `set_medium`, essentiality |
| New research notebooks | Self-contained narrative for readers | `04_…`, `05_…` |
| `tests/` | Behavior locks (WT growth, essential counts, …) | `pytest` |
| `data/processed/`, `results/` | Derived outputs | CSVs |
| Old teaching notebooks | Archive | `01`/`02`/`03` → `archive/` |

### 3.1 Why not continue the old notebooks?

- `01_basic_fba`: biomass id bug (`BIOMASS_PAO` instead of `PA_Biomass6_DM`)
- `02_gene_essentiality`: numerically solid, but teaching-structured
- `03_experimental_comparison`: compares to **random labels** — scientifically forbidden

**Completed:** moved to `archive/teaching_notebooks/`; retain their teaching role
and do not report nb03 random-label metrics.

### 3.2 New research notebooks — required traits

Each notebook should be **self-contained** (a reader understands it without the whole repo):

1. Scientific question and goal  
2. Environment and file paths  
3. Calls into `src/` (do not duplicate heavy logic in cells)  
4. Provenance (study, strain, medium, threshold)  
5. Outputs saved under `results/` or `data/processed/`  
6. A “limitations / what we do not claim” section  

Implementation status:

1. Media logic in `src/medium.py` — implemented.
2. `04_media_reconstruction.ipynb` — implemented.
3. `05_condition_essentiality.ipynb` — implemented; three media exported.
4. `06_pao1_validation.ipynb` — not created. The evaluation already exists as
   `scripts/validation/run_v01_mops_pyruvate_binary_validation.py` and V-01 reports.

---

## 4. Opening up the media problem (M9, LB, yeast extract)

The team wants to reconstruct **M9, LB, and yeast extract** according to the papers.
Here is the honest model/paper reality so format is not locked too early.

### 4.1 Three reconstruction levels in this project

| Level | Meaning | Examples |
|---|---|---|
| **DEFINED** | Chemically defined recipe; components mostly have exchanges | MOPS-pyruvate (Lee), MOPS-succinate (Turner), M9 with a specified carbon source |
| **PARTIAL** | Recipe known, but some components cannot be represented cleanly | LB, BHI, SCFM2 (without mucin/DNA) |
| **MEDIA_GAP** | Biological/undefined niche; cannot be honestly encoded as full exchanges | native sputum, serum, abscess |

### 4.2 Status of M9 / LB / yeast extract

**M9 (minimal)**  
- Usually **DEFINED** *if* the carbon source is stated in the paper Methods
  (glucose, pyruvate, etc.).  
- In the model: salts + N/P/S + metals + `EX_o2_e` + the matching carbon exchange.  
- Note: much of Lee’s minimal evidence is **MOPS-pyruvate**, not classic M9.
  Decide which study/table you are matching before building.

**LB (Lysogeny / Luria–Bertani)**  
- Appears as rich medium in Lee/Belanger.  
- Real LB = tryptone + **yeast extract** + NaCl → complex components.  
- iMO1056 has **no exchange for yeast extract / tryptone**.  
- Therefore LB in-model can only be a **defined approximation** (e.g. open amino-acid
  uptakes + ions ± a simple carbon), and must be labeled `LB_approx`, not “true LB”.

**Yeast extract**  
- Complex and undefined (peptides, vitamins, bases, …).  
- It **cannot** be set as a single honest uptake rate without heavy assumptions.  
- Defensible options:
  1. Fold it into the LB approximation and flag the unmodeled fraction; or  
  2. Use DEFINED media for the first validation and treat LB separately as a
     sensitivity/approximation case; or  
  3. If a paper gives defined substitute concentrations, map those — not “yeast extract”
     as a black box.

### 4.3 Practical recommendation (format not locked)

Instead of forcing “must be JSON” or “exactly these three media” up front:

**Batch A — DEFINED (first two implemented; M9 remains conditional future work):**
1. MOPS-pyruvate (Lee experimental context) — used in the D-21/V-01 cell.
2. MOPS-succinate (Turner comparator) — predictions exist; not a complete sputum contrast.
3. M9 + specified carbon — only if that study’s Methods use it  

**Batch B — implemented approximation with honest labels (PARTIAL):**
4. `LB_approx` for comparison to “general essential in LB”  
5. Explicitly state yeast extract/tryptone are not modeled  

**Batch C — do not build yet:**
- native sputum, serum, abscess, skin, Basta growth-arrest  

**Suggested output fields (format flexible):** each medium as a documented
table/dict with provenance:

- `medium_id`, `label` (DEFINED/PARTIAL)  
- `citation` + locator (Methods / supplement)  
- `strain_context` (PAO1/MPAO1)  
- `exchange_id → bound` with concentration→flux rationale  
- `unmodeled_components` (e.g. yeast extract)  

CSV exports now exist in `data/processed/conditions/`. Keep citations, documented
concentration-to-bound assumptions and honest PARTIAL labels when extending them.

Existing technical docs: [media plan](../audit/C01B_MEDIA_RECONSTRUCTION_PLAN.md),
[media source audit](../audit/MEDIA_SOURCE_AUDIT.md),
[current tables](../../data/processed/conditions/README.md), and API in `src/medium.py`.

---

## 5. Why PAO1-only for now?

- Model = PAO1 (`PAxxxx` locus tags)  
- Lee = MPAO1, Belanger = PAO1, Turner has usable PAO1 rows → join by **identity**  
- Basta is PA14; Poulsen screens nine strains excluding PAO1 and uses PA14/cluster
  coordinates → both need explicit cross-strain mapping; Turner orthology is
  `APPROVED_LIMITED` but not required for the first PAO1 validation  

**Team decision:** first path = PAO1-only. PA14 later (L-03b), after PGD↔Turner
crosswalk if needed.

---

## 6. Current status (reconciled 2026-11-11)

| Item | Status |
|---|---|
| Model / baseline | Reproducible iMO1056; default-medium 166 essentials. |
| Media | MOPS-pyruvate and MOPS-succinate DEFINED; LB approximation PARTIAL, all implemented. |
| Predictions | All 1054 genes evaluated per medium; 173/177/133 essentials respectively at 1%. |
| Primary experimental labels | D-21 approved: 214 positive + 811 negative = 1025; 18 ambiguous in-model genes excluded. |
| V-01 metrics | Computed: TP116/FN98/TN764/FP47; human interpretation pending. |
| Review evidence | Error-structure audit and source-backed evidence pack exist; no final sign-off or model edits implied. |
| Other experimental evidence | D-20 positives are a separate overlap-only layer; other conditions keep their own gates. |
| Turner / PGD orthology | Current `data/processed/gene_mapping/gene_mapping.csv` uses official PGD orthology: 1023 unique, 2 ambiguous, 29 unmapped. Final RBH table = 5374 pairs, technical PASSED report. Documented Turner APPROVED_LIMITED policy and later artifact lineage/approval require reconciliation before new PA14 comparisons. |

D-21 uses Varadarajan2020's reanalysis of Lee2015 Tn-seq, not independent
replication. Negative means not called essential in any of three Minimal
libraries; positive means called in at least two; discordant one-of-three calls
are excluded. MPAO1-to-PAO1 mapping/sublineage limitations remain documented.

B-SCI-01 now concerns interpretation and incomplete condition coverage, not
absence of any real comparison. B-COND-01 concerns the remaining media, not the
implemented MOPS configurations. B-MAP-01 concerns the secondary PA14 path.
See [current readiness](../audit/VALIDATION_READINESS.md) and
[label/media overlap](../../VALIDATION_LABEL_MEDIA_OVERLAP.md).

---

## 7. Next steps

1. Review the 98 FN and 47 FP explanations in the
   [error audit](../audit/v01_mops_pyruvate/V01_ERROR_STRUCTURE_AUDIT.md) and
   [review evidence](../audit/v01_mops_pyruvate/V01_HUMAN_REVIEW_EVIDENCE.md).
   Diagnostic categories remain hypotheses, not proven causes.
2. Produce a supervisor-facing narrative of the existing methods/results,
   condition matching, coverage and limitations; obtain final human sign-off.
3. Extend other media or phenotype cells only after their own labels, mappings,
   medium assumptions and predictions are reviewed.
4. Reconcile the secondary PGD/Turner/RBH artifact lineage and documented
   approval scope before controlled Poulsen/Basta comparison; this is independent
   of the executed first cell.

Continuing constraints:

- Never cite teaching nb03's simulated-label metrics.
- Do not mix D-20 Lee-original positives with D-21 Varadarajan negatives.
- Do not claim the model is fully validated while interpretation is pending.
- Keep `LB_approx` separate from true LB and from the primary comparison.
- Do not edit model/GPR/media/thresholds to improve frozen metrics automatically.
- Orthology promotion and any future model changes need their own sourced decisions.

---

## 8. Suggested role split

| Role | Work |
|---|---|
| Model / FBA | `src/medium` + growth tests + essentiality notebook |
| Literature | Match each medium to Methods/supplement + provenance |
| Data | READY_ONLY ↔ media conditions; overlap gene lists |
| Repo | Archive teaching notebooks; README; env |

The next team meeting should review the existing first-cell discrepancies and
interpretation. MOPS-pyruvate is already the locked primary medium; LB remains a
separate approximation case.

---

## 9. Related files in the repo

- `CLAUDE.md` / `TODO.md` / `BLOCKERS.md` / `DECISIONS.md`  
- [Media reconstruction plan](../audit/C01B_MEDIA_RECONSTRUCTION_PLAN.md)
- [Media source audit](../audit/MEDIA_SOURCE_AUDIT.md)
- [Reviewed literature evidence](../audit/L03_REVIEWED_EVIDENCE_SUMMARY.md)
- [PGD integration](../../docs/methods/ORTHOLOGY_PSEUDOMONAS_INTEGRATION.md)
- [Orthology decision](../audit/ORTHOLOGY_HUMAN_REVIEW_DECISION.md)
- [Publication plan](../publication/PUBLICATION_PLAN.md)

---

## 10. One sentence for the team

> Keep Jupyter for narrative and `src/` for reusable science; present the executed
> MOPS-pyruvate comparison with its limitations, review discrepancies, and extend
> conditions through separate evidence gates.

*Guidance document only — no new research notebooks or media files were created in this step.*

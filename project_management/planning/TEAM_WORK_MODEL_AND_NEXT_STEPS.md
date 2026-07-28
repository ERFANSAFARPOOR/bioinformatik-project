# Project work model and next steps (for the team)

**Date:** 2026-07-21  
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

The three existing notebooks (`01` / `02` / `03`) were written for **teaching**.
The group’s goal is now **research / reviewer-defensible**. Those teaching notebooks
should be archived and a new research notebook path should be built.

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
| Media reconstruction plan + cited bounds | Applied FBA skill |
| Multi-medium essentiality predictions (without fake validation claims) | Explainable interview demo |
| Explicit limitation reports | Scientific maturity, not just “pretty numbers” |

**Do not put on a resume:** precision/recall from `nb03` (labels are random).

### 2.2 Minimum defensible paper path

For a reviewer-defensible model validation, this chain is required:

```
real PAO1 labels (READY_ONLY)
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

**Recommendation:** move them to `archive/teaching_notebooks/` with a README marked
legacy/teaching; do not build new research on top of them.

### 3.2 New research notebooks — required traits

Each notebook should be **self-contained** (a reader understands it without the whole repo):

1. Scientific question and goal  
2. Environment and file paths  
3. Calls into `src/` (do not duplicate heavy logic in cells)  
4. Provenance (study, strain, medium, threshold)  
5. Outputs saved under `results/` or `data/processed/`  
6. A “limitations / what we do not claim” section  

Suggested build order (when implementation starts):

1. Media logic in `src/` first  
2. `04_media_reconstruction.ipynb` — show and save medium configs  
3. `05_condition_essentiality.ipynb` — predictions per medium  
4. `06_pao1_validation.ipynb` — only when labels + media + predictions exist  

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

**Batch A — build first (DEFINED, close to existing PAO1 evidence):**
1. MOPS-pyruvate (Lee) — if it matches Lee labels  
2. MOPS-succinate (Turner) — if it matches Turner tables  
3. M9 + specified carbon — only if that study’s Methods use it  

**Batch B — approximation with honest labels (PARTIAL):**
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

Choose CSV / YAML / JSON after team agreement. More important than format:
**citations and honest PARTIAL labels**.

Existing technical docs: `C01B_MEDIA_RECONSTRUCTION_PLAN.md`,
`MEDIA_SOURCE_AUDIT.md`, current API in `src/medium.py`.

---

## 5. Why PAO1-only for now?

- Model = PAO1 (`PAxxxx` locus tags)  
- Lee = MPAO1, Belanger = PAO1, Turner has usable PAO1 rows → join by **identity**  
- Poulsen/Basta are largely PA14 → need orthology; orthology is
  `APPROVED_LIMITED` but not required for the first PAO1 validation  

**Team decision:** first path = PAO1-only. PA14 later (L-03b), after PGD↔Turner
crosswalk if needed.

---

## 6. Current status (team snapshot)

| Item | Status |
|---|---|
| Model + pytest | Reproducible; nb02 = 166 essential |
| Lee/Turner/Belanger evidence | DRAFT; subset READY_ONLY |
| Turner orthology | APPROVED_LIMITED (5,365 pairs) |
| PGD orthology | Present (5,385); supplements Turner (D-16) |
| In-model media | Plan only; not built yet |
| Validation metrics | **Forbidden** until labels + media + predictions |

Open blockers: `B-SCI-01` (no real metrics), `B-COND-01` (media),
`B-MAP-01` partially resolved (PA14 path).

---

## 7. NEXT STEPS — recommended order

### Phase 0 — housekeeping (short)
1. Archive teaching notebooks `01`/`02`/`03` → `archive/teaching_notebooks/` + README  
2. Enforce: nobody cites nb03 validation numbers  

### Phase 1 — media infrastructure in `src/` (scientific priority)
3. Extend/stabilize medium API in `src/medium.py` (or related module)  
4. Implement Batch A (DEFINED) with citations  
5. Implement `LB_approx` with yeast-extract/tryptone flags  
6. Tests: WT growth per medium; no crashes; no invented bounds without sources  

### Phase 2 — self-contained research notebooks
7. Media notebook: load, display composition, save derived outputs  
8. Multi-medium essentiality notebook (CSV under `results/`)  

### Phase 3 — prepare validation (still no rushed metrics)
9. Lock READY_ONLY labels for conditions that have media  
10. Only when label↔media↔prediction overlap is clear → design V-01  

### Phase 4 — optional / parallel (PA14)
11. PGD↔Turner crosswalk  
12. Later controlled Poulsen/Basta draft mapping — **not** the first validation  

### Forbidden until further notice
- Reporting precision/recall/F1/MCC from simulated data  
- Claiming “true LB” when only an approximation exists  
- Merging orthology into `gene_mapping.csv` without a separate decision  
- Building sputum/serum media without MEDIA_GAP labeling  

---

## 8. Suggested role split

| Role | Work |
|---|---|
| Model / FBA | `src/medium` + growth tests + essentiality notebook |
| Literature | Match each medium to Methods/supplement + provenance |
| Data | READY_ONLY ↔ media conditions; overlap gene lists |
| Repo | Archive teaching notebooks; README; env |

Next team meeting should decide only this:

> For the first validation, which two/three DEFINED media are locked, and do we
> keep LB as a separate approximation case?

---

## 9. Related files in the repo

- `CLAUDE.md` / `TODO.md` / `BLOCKERS.md` / `DECISIONS.md`  
- `C01B_MEDIA_RECONSTRUCTION_PLAN.md`  
- `MEDIA_SOURCE_AUDIT.md`  
- `L03_REVIEWED_EVIDENCE_SUMMARY.md`  
- `docs/ORTHOLOGY_PSEUDOMONAS_INTEGRATION.md`  
- `ORTHOLOGY_HUMAN_REVIEW_DECISION.md`  
- `PUBLICATION_PLAN.md`  

---

## 10. One sentence for the team

> Keep Jupyter for narrative; lock science in `src/` and tests; archive teaching
> notebooks; build DEFINED media and an honest LB approximation for PAO1 first;
> compute metrics only after real labels + media + predictions.

*Guidance document only — no new research notebooks or media files were created in this step.*

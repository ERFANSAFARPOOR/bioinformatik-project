# BLOCKERS

Items that block scientific validity or require data/human input. Each blocker
must be resolved with **evidence**, never invented. Status: OPEN / RESOLVED.

Legend: severity P0 (blocks validity/reproducibility) · P1 (blocks manuscript/repo) · P2/P3 (quality/optional).

---

## B-SCI-01 — No real model-vs-experiment validation (P0) — OPEN
`notebooks/03_experimental_comparison.ipynb` computes precision/recall/F1/Venn
against **simulated random labels** (`random.seed(42)`; `random.sample(...)`),
explicitly labeled "Using simulated data for demonstration."
**Impact:** every comparison metric currently in the project is meaningless.
**Unblock when:** real experimental essential-gene lists are extracted from the
papers' supplementary datasets, mapped to model gene IDs, and validated.
Depends on B-LIT-01, B-MAP-01.

## B-LIT-01 — Supplementary gene-list datasets not downloaded (P0) — OPEN
The experimental essential/fitness gene lists live in supplementary files, not
in the PDFs' body:
- Turner 2015: `pnas.1419677112.sd01–sd04.xlsx`
- Lee 2015: `pnas.1422186112.sd01.xlsx`
- Poulsen 2019: Broad fitness data `https://data.broadinstitute.org/fitness/` + `https://github.com/broadinstitute/FiTnEss`
- Basta, Belanger: supplements TBD
**Impact:** `data/processed/literature_evidence.csv` has only study-level rows;
all gene-level rows are `PENDING_EXTRACTION`.
**Unblock when:** datasets downloaded (record provenance in `DATA_PROVENANCE.md`),
stored under `data/raw/literature/`, and parsed. Requires network access +
human confirmation that downloading is permitted.

## B-LIT-02 — Citation/DOI/year unverified for Basta & Belanger (P1) — OPEN
`conditian/davidW.pdf` (Basta, growth-arrest fitness) and `conditian/corrieR.pdf`
(Belanger, host conditions) were identified by title/running-header/`/Author`
(Hancock lab). Their **DOI, year, journal, and strain** are `PENDING_VERIFY`.
**Unblock when:** confirmed against CrossRef/journal record. Do not cite until verified.

## B-MAP-01 — Cross-strain gene mapping PAO1↔PA14 not built (P0) — OPEN
Model = **PAO1** (`PAxxxx`). Turner/Lee/Poulsen/Basta use **PA14** (`PA14_xxxxx`).
PAO1 and PA14 locus tags are **not interchangeable**.
`data/processed/gene_mapping.csv` currently has the identity mapping
(model_gene_id → PAO1 locus tag, confidence high) but PA14 columns are empty.
**Impact:** cannot compare PA14 experiments to a PAO1 model without orthology.
**Unblock when:** an authoritative PAO1↔PA14 ortholog table is obtained
(e.g. pseudomonas.com orthologs, or study-provided PAO1 homolog columns) and
joined, retaining one-to-many and missing mappings.

## B-ENV-01 — reccobra39 cannot run the notebooks as-is (P1) — OPEN
Notebooks were authored under `.venv` (Python 3.12.6). Mandated env
`reccobra39` (Python 3.9.23) is **missing** `matplotlib`, `matplotlib_venn`,
`scipy`, `networkx`, `seaborn`, `openpyxl`.
**Impact:** plotting cells and `.xlsx` reading fail in reccobra39.
**Unblock when:** these packages are installed **locally** into reccobra39
(allowed; NOT global Python), notebooks re-run under the reccobra39 kernel, and
numerical reproduction (WT growth 1.0479, 166 essential) confirmed. Only then
lock `environment.yml`/`requirements-lock.txt`. Decision pending in DECISIONS.md D-02.

## B-MODEL-01 — Blocked reactions / gap-filling not characterized (P2) — OPEN
`find_blocked_reactions` failed under Windows multiprocessing during the audit.
**Unblock when:** recomputed with `processes=1` (or under `if __name__=='__main__'`).
Needed to interpret false-negative essentiality predictions and dead ends (217 found).

## B-MODEL-02 — 565/879 metabolites lack chemical formulas (P2) — OPEN
Mass-balance auditing is unreliable (585 "imbalanced" reactions are mostly an
artifact of missing formulas, not true imbalances). 0 charge imbalances.
**Unblock when:** formulas back-filled from BiGG/MetaNetX where the manuscript
needs balance claims; otherwise scope-limit and state the limitation explicitly.

## B-COND-01 — Experimental media/conditions not reconstructed (P0 for validation) — OPEN
Studies use specific media (CF sputum / SCFM, LB, defined minimal, carbon- or
oxygen-limited arrest, host-mimicking). The model default medium is glucose+O2
aerobic. Comparing essentiality across mismatched media is invalid.
**Unblock when:** each study's medium is reconstructed as an in-model exchange
configuration (documented carbon source, electron acceptor, supplements) with a
citation, before computing any per-condition metric.

## B-STRAIN-01 — Strain of model: RESOLVED (PAO1)
Resolved during audit: gene IDs are PAO1 `PAxxxx` locus tags and the model is
iMO1056 (Oberhardt 2008, PAO1). Kept here as a record; **not** a blocker.
Consequence: every PA14 dataset needs B-MAP-01 before use.

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
in the PDFs' body. Strain re-audited (B-STRAIN-02) — locus-tag system noted:
- Turner 2015 (**PAO1+PA14**): `pnas.1419677112.sd01–sd04.xlsx` — PAO1 rows usable.
- Lee 2015 (**MPAO1**): `pnas.1422186112.sd01.xlsx` — PAO1-tag, no orthology.
- Belanger 2022 (**PAO1**): Frontiers supplement — PAO1-tag, no orthology.
- Poulsen 2019 (multi-strain): PNAS SI + Broad fitness `https://data.broadinstitute.org/fitness/` + `https://github.com/broadinstitute/FiTnEss`.
- Basta 2017 (**PA14**): mBio supplement — needs orthology.
- NEW meegid2022 (**PAO1**, PMID 35104681): full text + supplement (not OA here).
**Impact:** `data/processed/literature_evidence.csv` has only study-level rows;
all gene-level rows are `PENDING_EXTRACTION`.
**Unblock when:** datasets downloaded (provenance in `DATA_PROVENANCE.md`), stored
under `data/raw/literature/<study_id>/`, and parsed. Requires network access
(blocked here — B-NET) + human confirmation that downloading is permitted.
Priority order: PAO1/MPAO1 first (Lee, Turner PAO1 rows, Belanger, meegid2022).

## B-LIT-02 — Citation/DOI/year for Basta & Belanger (P1) — RESOLVED 2026-06-26
Verified against authoritative sources (ASM/Frontiers + PMC):
- Basta DW, Bergkessel M, Newman DK (2017) mBio 8(6):e01170-17, **10.1128/mBio.01170-17** (erratum 10.1128/mbio.00576-18).
- Belanger CR, … Hancock REW (2022) Front Microbiol 13:1055512, **10.3389/fmicb.2022.1055512** (published 2022-11-25; the earlier "2020" guess was wrong).
Strains are now **confirmed** from each paper's methods (Basta 2017 = PA14;
Belanger 2022 = PAO1) — see the resolved strain-correction record **B-STRAIN-02**.

## B-MAP-01 — Validated cross-strain PAO1↔PA14 orthology not built (P1; downgraded from P0) — OPEN
Model = **PAO1** (`PAxxxx`). `gene_mapping.csv` has the identity mapping
(model→PAO1, high) plus a symbol-based PA14 layer (386 medium, 22 low, 646
unmapped) — NOT validated orthology.
**Re-audit update (2026-07-01):** the strain re-audit (see B-STRAIN-02) shows the
usable experimental data is mostly **PAO1/MPAO1** (Belanger=PAO1, Lee=MPAO1,
Turner has PAO1 rows), which join by **identity — no orthology needed**. So this
blocker is **no longer on the critical path** for the first PAO1-side validation.
Validated PAO1↔PA14 orthology is now required **only** for **Basta 2017 (PA14)**
and the **non-PAO1 strains of Poulsen 2019**. Downgraded P0→P1.
**Impact:** cannot compare PA14-only experiments to the PAO1 model without orthology.
**Unblock when:** an authoritative PAO1↔PA14 ortholog table is obtained
(pseudomonas.com orthologs, or study-provided PAO1 homolog columns) and joined,
retaining one-to-many and missing mappings. See `ORTHOLOGY_STATUS_REPORT.md`.

## B-ENV-01 — reccobra39 cannot run the notebooks as-is (P1) — RESOLVED 2026-06-26
Resolved: E-01 added matplotlib 3.9.4, matplotlib-venn 1.1.2, openpyxl 3.1.5,
scipy 1.13.1 into reccobra39 (env-scoped; numpy/pandas/cobra unchanged). E-02
reproduced all notebooks under Python 3.9.23: **nb02 reproduces exactly**
(166 essential, WT 1.0479285528). Remaining follow-ups are non-blocking:
fix nb01 `BIOMASS_PAO` bug (N-01) and correct kernelspec metadata (E-04) before
locking `environment.yml`/`requirements-lock.txt`. Original text retained below.


Notebooks were authored under `.venv` (Python 3.12.6). Mandated env
`reccobra39` (Python 3.9.23) is **missing** `matplotlib`, `matplotlib_venn`,
`scipy`, `networkx`, `seaborn`, `openpyxl`.
**Impact:** plotting cells and `.xlsx` reading fail in reccobra39.
**Unblock when:** these packages are installed **locally** into reccobra39
(allowed; NOT global Python), notebooks re-run under the reccobra39 kernel, and
numerical reproduction (WT growth 1.0479, 166 essential) confirmed. Only then
lock `environment.yml`/`requirements-lock.txt`. Decision pending in DECISIONS.md D-02.

## B-NET — Restricted network egress blocks key downloads (P0 for L-03/G-01-final) — OPEN
From this environment (verified 2026-06-26 and re-checked 2026-07-01 via curl):
- **Reachable:** NCBI **E-utilities** (`eutils.ncbi.nlm.nih.gov` esearch/esummary/
  elink — used to verify all PMIDs/PMCIDs this cycle), GitHub, `data.broadinstitute.org`.
- **Blocked:** `pnas.org` supplements (**403**), `pseudomonas.com` (**403/timeout**),
  NCBI Datasets v2 API (TLS fail), **PMC OA package download** — both
  `ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_package/...` (curl exit 9, access denied)
  and `https://ftp.ncbi.nlm.nih.gov/...oa_package/...` ("Object not found"). So even
  open-access full text (e.g. Bartell 2017 PMC5344303, GigaScience PMC6333913) is
  not retrievable here — only metadata is.
**Impact:** journal essential-gene supplements (Turner/Lee + Basta/Belanger) and the
authoritative pseudomonas.com PAO1↔PA14 ortholog table cannot be fetched here.
**Mitigation applied:** built a PA14 mapping from NCBI RefSeq gene **symbols**
(annotation-based, flagged medium/low) instead. **Unblock when:** supplements +
validated orthology are obtained via a human-assisted download or different network;
store in `data/raw/...` with provenance. Do not fabricate the missing gene lists.

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
Consequence: PA14-only datasets need B-MAP-01 before use.

## B-STRAIN-02 — Experimental-paper strains re-audited & CORRECTED (record) — RESOLVED 2026-07-01
Direct PDF-evidence re-audit (`PAO1_PAPER_RELEVANCE_AUDIT.md`,
`scripts/audit/extract_strain_evidence.py`) corrected the earlier "mostly PA14"
classification:
- **Lee 2015 = MPAO1** (PAO1-derived), was "PA14" — quote: "The P. aeruginosa
  parent strain was MPAO1".
- **Belanger 2022 = PAO1**, was "confirm" — quote: "…transposon insertion mutant
  pool of P. aeruginosa strain PAO1…".
- **Turner 2015 = PAO1 + PA14** (mixed, usable PAO1 rows), was "PA14".
- **Basta 2017 = PA14 (UCBPP-PA14)** confirmed. **Poulsen 2019** multi-strain
  incl. PAO1. **Juhas 2015** review.
**Consequence:** the first PAO1 validation is strain-unblocked (uses PAO1/MPAO1 by
identity). Only Basta + non-PAO1 Poulsen strains need B-MAP-01. Not a blocker;
recorded as a correction.

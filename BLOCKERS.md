# BLOCKERS

Items that block scientific validity or require data/human input. Each blocker
must be resolved with **evidence**, never invented. Status: OPEN / PARTIALLY RESOLVED / RESOLVED.

Legend: severity P0 (blocks validity/reproducibility) · P1 (blocks manuscript/repo) · P2/P3 (quality/optional).

**Status reconciled 2026-11-11:** the MOPS-pyruvate medium and predictions exist,
and D-21/V-01 experimental binary metrics have been computed (1025 genes;
TP116/FN98/TN764/FP47). Error audit and review evidence are prepared; final human
interpretation/sign-off is pending. Below, dated download and candidate-mapping
entries are history, not claims that those files are still absent. Current
readiness: [report](project_management/audit/VALIDATION_READINESS.md).

---

## B-SCI-01 — Interpretation and condition coverage incomplete (P0) — OPEN (first-cell metrics computed)
`archive/teaching_notebooks/03_experimental_comparison.ipynb` (formerly under
`notebooks/`) computes precision/recall/F1/Venn against **simulated random labels**
(`random.seed(42)`; `random.sample(...)`), explicitly labeled "Using simulated
data for demonstration."
**Impact:** teaching nb03 metrics remain forbidden / meaningless.
**Update 2026-07-29 (D-20):** Lee2015 MOPS-pyruvate **positive** labels READY;
positive-overlap-only outputs under
`results/comparison/lee2015_mops_pyruvate_POSITIVE_OVERLAP_ONLY_*`.
**Update 2026-08-01 (D-21):** experimental binary universe frozen (1025 genes).
**Update 2026-08-01 (V-01 execution):** primary binary confusion matrix + metrics
**computed** on D-21 universe vs `mops_pyruvate_lee2015` @ threshold 0.01 →
`data/processed/validation/v01_mops_pyruvate_*`. Status was
`V01_BINARY_METRICS_COMPUTED_PENDING_HUMAN_INTERPRETATION`.
**Update 2026-08-01 (V-01 error structure audit):** diagnostic FP/FN structural
audit completed → `V01_ERROR_ANALYSIS_COMPLETED_PENDING_HUMAN_REVIEW`
(`v01_mops_pyruvate_*_audit.csv` +
`project_management/audit/v01_mops_pyruvate/V01_ERROR_STRUCTURE_AUDIT.md`).
No model/media/threshold changes. This does **not** declare the model validated
or authorize GPR/network edits. Teaching nb03 remains invalid.
**Update 2026-11-11 (documentation reconciliation):** source-backed review
evidence exists in
`project_management/audit/v01_mops_pyruvate/V01_HUMAN_REVIEW_EVIDENCE.md`.
Evidence readiness is not final human sign-off; diagnostic categories remain
hypotheses. The current issue is interpretation/coverage, not absence of a real
comparison. No model/media/threshold change or new validation approval is implied.
**Still open:** human review of prioritized FP/FN mechanisms; other condition
cells; B-COND-01 remaining media gaps.

## B-LIT-01 — Evidence review/promotion and provenance incomplete (P0 for remaining cells) — RAW SUPPLEMENTS PRESENT
The experimental essential/fitness gene lists live in supplementary files, not
in the PDFs' body. Strain re-audited (B-STRAIN-02) — locus-tag system noted.

**OBTAINED 2026-07-06 (human-assisted; now physically present + audited):**
- Turner 2015 (**PAO1+PA14**): `pnas.1419677112.sd01–sd10.xlsx` — PAO1 rows usable ✅
- Lee 2015 (**MPAO1**): `pnas.1422186112.sd01.xlsx` — PAO1-tag, identity join ✅
- Belanger 2022 (**PAO1**): `Data_Sheet_1/2.XLSX` (+`_3.docx`) — PAO1-tag ✅
- Varadarajan 2020 (**MPAO1**, bonus): `Supplementary Dataset 1–4` — MPAO1 essentiality
  + in-supplement MPAO1→PAO1 map ✅. **Citation VERIFIED 2026-07-06** (DOI
  10.1038/s41522-020-00154-8, PMID 33127897; `project_management/audit/VARADARAJAN2020_CITATION_CHECK.md`).

Provenance: `DATA_PROVENANCE.md §3d/§3e` + `data/processed/literature/supplement_inventory.tsv`
(SHA-256 per file). Audit: `docs/project/SUPPLEMENT_INVENTORY_AUDIT.md`. Thresholds:
`docs/methods/THRESHOLD_METHOD_AUDIT.md`. Parse notes: `data/raw/literature/<study>/SUPPLEMENT_PARSE_NOTES.md`.

**DRAFT PARSED 2026-07-06** (Phase E/6 gate satisfied — thresholds sourced from
Methods): Lee/Turner(PAO1 sheets)/Belanger → `data/processed/literature/*_parsed_gene_evidence.csv`
+ `data/processed/literature_evidence_gene_level_DRAFT.csv` (5,093 rows, 6 classes
distinct, review flags). At this July draft stage Varadarajan was excluded to
avoid double-counting the Lee reanalysis. **Superseded for the first binary cell
by D-21 (2026-08-01):** Varadarajan DS1+DS4 now supply both binary classes in a
separate approved universe; it remains derivative, not independent replication.
At that July draft stage Turner paired sheets sd03/04/05/09 were not yet
resolved (L03-B3). The 2026-07-07b review resolved L03-B3: sd05/sd09 PAO1
blocks were parsed, and sd03/sd04 were skipped with recorded reasons. See
`project_management/audit/L03_DRAFT_REVIEW_AUDIT.md`.

**NEWLY PRESENT 2026-07-06 (user-added; audited, NOT yet parsed as evidence):**
- Poulsen 2019 (multi-strain core-essential): `pnas.1900570116.sd01–sd07.xlsx`
  + `sapp.pdf` ✅ — PA14_ID/Cluster_ID indexed; needs PA14→PAO1 orthology
  (B-MAP-01) + Methods threshold sourcing before use.
- Basta 2017 (**PA14**): `mbo006173591sd1–sd4.xlsx` + 2 `.tif` ✅ — raw growth-arrest
  read counts; needs analysis + orthology. Deferred.

**STILL MISSING:** none. (meegid2022 removed from active scope by user decision
2026-07-06; no local files; no validation dependency.)

**Current first-cell scope:** D-20 Lee-original MOPS-pyruvate positives are
promoted for overlap-only analysis, and D-21 Varadarajan Minimal binary labels
are approved and have been used in V-01. The broader canonical evidence-table
promotion/provenance backlog does not invalidate or re-block that executed cell.
**Impact on remaining evidence:** gene-level DRAFT/reviewed rows exist for Lee/Turner/Belanger; Poulsen/Basta
raw supplements are present and audited (readiness gated — see
`project_management/audit/L03_PARSE_BLOCKERS.md`). The study-level registry now
lives at `data/processed/literature/literature_registry.csv`; separate gene-level
DRAFT/READY files exist under `data/processed/literature/gene_level/`.
Broader evidence promotion remains unfinished; the D-20/D-21 promotions are
already recorded separately.
**Unblock fully when:** the DRAFT is reviewed/promoted, Poulsen/Basta pass the
mapping/threshold gate and are parsed, AND source URLs recorded (currently
`SOURCE_URL_PENDING`).

## B-LIT-02 — Citation/DOI/year for Basta & Belanger (P1) — RESOLVED 2026-06-26
Verified against authoritative sources (ASM/Frontiers + PMC):
- Basta DW, Bergkessel M, Newman DK (2017) mBio 8(6):e01170-17, **10.1128/mBio.01170-17** (erratum 10.1128/mbio.00576-18).
- Belanger CR, … Hancock REW (2022) Front Microbiol 13:1055512, **10.3389/fmicb.2022.1055512** (published 2022-11-25; the earlier "2020" guess was wrong).
Strains are now **confirmed** from each paper's methods (Basta 2017 = PA14;
Belanger 2022 = PAO1) — see the resolved strain-correction record **B-STRAIN-02**.

## B-MAP-01 — Primary cross-strain mapping integration incomplete (P1; secondary path) — **PARTIALLY RESOLVED**
**Current artifact audit (2026-11-11):**
`data/processed/gene_mapping/gene_mapping.csv` records official PGD orthology;
its coverage report gives 1023 unique, 2 ambiguous and 29 unmapped model genes.
The separate final RBH table
`data/processed/ortholog/final/pao1_pa14_orthologs_pseudomonas_rbh_20260712.csv`
contains 5374 pairs and `Validation_Report.txt` records technical PASSED status.
The previous symbol-only counts and “not merged” statements below are dated
history, not current artifact status.

**Remaining blocker is policy/lineage reconciliation for PA14 comparisons:**
D-16 and the Turner APPROVED_LIMITED human decision have a narrower documented
scope than these later artifacts. Reconcile source lineage/crosswalk, conflicts,
ambiguous/unmapped rows and approval scope before a new PA14 experimental cell.
A technically PASSED table alone does not provide unrestricted biological or
human approval. This secondary path does not block the executed D-21/V-01 cell.

**Historical development record (superseded where current artifacts differ):**
Model = **PAO1** (`PAxxxx`). The original mapping had an identity layer plus
386 medium-confidence symbol matches, 22 ambiguous and 646 unmapped PA14 rows.
**Re-audit update (2026-07-01):** the strain re-audit (see B-STRAIN-02) shows the
usable experimental data is mostly **PAO1/MPAO1** (Belanger=PAO1, Lee=MPAO1,
Turner has PAO1 rows), which join by **identity — no orthology needed**. So this
blocker is **no longer on the critical path** for the first PAO1-side validation.
Validated PAO1↔PA14 orthology is now required **only** for **Basta 2017 (PA14)**
and **Poulsen 2019 (all nine screened strains exclude PAO1)**. Downgraded P0→P1.
**Impact:** cannot compare PA14-only experiments to the PAO1 model without orthology.
**Update 2026-07-07:** the raw supplements for **Basta 2017 (PA14)** and **Poulsen
2019** are present but **cannot be parsed** — both are PA14-referenced and neither
contains PAO1 ids (**Poulsen's 9 strains exclude PAO1**, verified). No validated
orthology source exists here (only the RefSeq symbol layer, which is inadequate).
See `project_management/audit/ORTHOLOGY_READINESS_AUDIT.md`, `project_management/audit/POULSEN_BASTA_MAPPING_PLAN.md`.
**Update 2026-07-07b — CANDIDATE source built (still OPEN):** the authoritative
pseudomonas.com RBBH export is **unreachable** (HTTP 403/Cloudflare via both local
curl and WebFetch — re-verified). A **candidate** PAO1↔PA14 table was therefore
extracted from the peer-reviewed **Turner 2015 supplement** (sd03/sd04; Pseudomonas
Genome Database BLAST+synteny 1:1 orthologs) →
`data/processed/ortholog/working/pao1_pa14_orthologs_turner2015_CANDIDATE.csv` (5,365
strict-1:1 pairs, 0 one-to-many; 541 PA14-only + 204 PAO1-only excluded as counts).
sd03≡sd04 (identical). Independent **Belanger DS1 cross-check: 598/599 agree
(99.8%)**, 1 flagged disagreement (`PA2279`). Script:
`scripts/mapping/build_ortholog_candidate.py`; doc: `project_management/audit/ORTHOLOG_CANDIDATE_TABLE.md`;
search: `project_management/audit/LOCAL_ORTHOLOGY_SEARCH_REPORT.md`. **Marked HUMAN_REVIEW_REQUIRED — NOT
merged into `gene_mapping.csv`, NOT used to parse Poulsen/Basta or compute metrics.**
Blocker narrows: source now exists locally; still OPEN pending (a) human sign-off
approving Turner-embedded orthology as the mapping source vs. the live pseudomonas.com
table, and (b) coverage of one-to-many / PA14-unique cases beyond the 1:1 subset.
**Update 2026-07-10 — APPROVED_LIMITED (narrowed, still OPEN):** human review
decision `APPROVED_LIMITED`; conflict `RESOLVED_SUPPORTS_TURNER` via KEGG SSDB
(PA14_35100↔PA2279, PA14_35130↔PA2277; Belanger PA2279→PA14_35130 rejected for
this locus). Derived:
`pao1_pa14_orthologs_turner2015_APPROVED_LIMITED.csv` (5,365 rows,
`approved_for_l03b=yes`). Status:
`CANDIDATE_APPROVED_LIMITED_FOR_1TO1_PA14_TO_PAO1_MAPPING_WITH_CONFLICT_POLICY`.
Still **not** merged into `gene_mapping.csv`; Poulsen/Basta only eligible for
future controlled L-03b draft mapping; **metrics still blocked**. Docs:
`project_management/audit/ORTHOLOGY_HUMAN_REVIEW_DECISION.md`, `project_management/audit/ORTHOLOGY_CONFLICT_RESOLUTION_REPORT.md`.
**Update 2026-07-10b — PGD export available (PARTIALLY RESOLVED):** authoritative
Pseudomonas Genome Database orthology export merged from `origin/develop`
(`7cd3dd29`) → `data/raw/ortholog/pao1_pa14_orthologs_pseudomonas.csv` (**5,385
pairs**) + `Supplementary_Table_S1.csv` + `Orthology_QC_Report.csv`. PGD confirms
Turner at the disputed locus (PA2279↔PA14_35100, PA2277↔PA14_35130). **Decision
D-16:** PGD supplements/validates Turner; does **not replace** Turner
`APPROVED_LIMITED` until PGD↔Turner crosswalk + human review. Remaining: build
crosswalk script, classify the +20 PGD-only pairs, resolve Review-flagged rows
(e.g. one-to-many `PA0263`/`hcpC`), relocate `tst ortolog/` to archive. SHA-256 for
PGD files: PENDING. Doc: `docs/methods/ORTHOLOGY_PSEUDOMONAS_INTEGRATION.md`.
**Historical 2026-07-10b remaining gate:** the PGD↔Turner crosswalk is built and human-approved as the
primary mapping source for L-03b; one-to-many/missing retained explicitly; joined
into a reviewed mapping table (not yet `gene_mapping.csv`). See
`project_management/audit/ORTHOLOGY_STATUS_REPORT.md`.

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

## B-NET — Historical download restrictions / remaining provenance follow-up — NARROWED
**Current scope (2026-11-11):** active corpus supplements and a PGD orthology
export are already present. This is not a blocker on the executed D-21/V-01 cell.
Source-URL/provenance follow-up and PGD/Turner/RBH lineage/approval reconciliation remain;
current network accessibility is not asserted from old HTTP failures.

**Historical network snapshot** (verified 2026-06-26 and re-checked 2026-07-01 via curl):
- **Reachable:** NCBI **E-utilities** (`eutils.ncbi.nlm.nih.gov` esearch/esummary/
  elink — used to verify all PMIDs/PMCIDs this cycle), GitHub, `data.broadinstitute.org`.
- **Blocked:** `pnas.org` supplements (**403**), `pseudomonas.com` (**403/timeout**),
  NCBI Datasets v2 API (TLS fail), **PMC OA package download** — both
  `ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_package/...` (curl exit 9, access denied)
  and `https://ftp.ncbi.nlm.nih.gov/...oa_package/...` ("Object not found"). So even
  open-access full text (e.g. Bartell 2017 PMC5344303, GigaScience PMC6333913) is
  not retrievable here — only metadata is.
**Impact at that time:** journal essential-gene supplements (Turner/Lee + Basta/Belanger) and the
authoritative pseudomonas.com PAO1↔PA14 ortholog table cannot be fetched here.
**Mitigation applied:** built a PA14 mapping from NCBI RefSeq gene **symbols**
(annotation-based, flagged medium/low) instead. **Unblock when:** supplements +
validated orthology are obtained via a human-assisted download or different network;
store in `data/raw/...` with provenance. Do not fabricate the missing gene lists.
**Update 2026-07-06:** the Lee/Turner/Belanger/Varadarajan **and now
Poulsen/Basta** supplements were obtained via **human-assisted download**
(resolving the L-section download blockers), but B-NET stays **OPEN** for: the
authoritative pseudomonas.com PAO1↔PA14 ortholog table (needed for Basta/Poulsen),
and the **source URLs** of the obtained files (`SOURCE_URL_PENDING`). The former
absence was subsequently superseded by the 2026-07-10b PGD-export entry in
B-MAP-01; the source/approval follow-up remains distinct. No
supplement is now "missing" (meegid2022 removed from active scope by user
decision).

## B-MODEL-01 — Blocked reactions / gap-filling not characterized (P2) — OPEN
`find_blocked_reactions` failed under Windows multiprocessing during the audit.
**Unblock when:** recomputed with `processes=1` (or under `if __name__=='__main__'`).
Needed to interpret false-negative essentiality predictions and dead ends (217 found).

## B-MODEL-02 — 565/879 metabolites lack chemical formulas (P2) — OPEN
Mass-balance auditing is unreliable (585 "imbalanced" reactions are mostly an
artifact of missing formulas, not true imbalances). 0 charge imbalances.
**Unblock when:** formulas back-filled from BiGG/MetaNetX where the manuscript
needs balance claims; otherwise scope-limit and state the limitation explicitly.

## B-COND-01 — Remaining media/condition gaps (P0 for affected cells) — **PARTIALLY RESOLVED**
Studies use specific media (CF sputum / SCFM, LB, defined minimal, carbon- or
oxygen-limited arrest, host-mimicking). The model default medium is glucose+O2
aerobic. Comparing essentiality across mismatched media is invalid.
**Unblock when:** each study's medium is reconstructed as an in-model exchange
configuration (documented carbon source, electron acceptor, supplements) with a
citation, before computing any per-condition metric.
**Update 2026-07-07:** planning done in `project_management/audit/C01B_MEDIA_RECONSTRUCTION_PLAN.md`.
**Update 2026-07-24 (C-01b Batch A/B started):** implemented in `src/medium.py` +
`data/processed/conditions/`:
- DEFINED: `mops_pyruvate_lee2015`, `mops_succinate_turner2015`
- PARTIAL: `LB_approx_lee2015` (yeast extract/tryptone flagged; not true LB)
Measured WT growth (reccobra39/GLPK): pyruvate ≈0.405 /h; succinate ≈0.553 /h;
LB_approx ≈14.95 /h (PARTIAL — not physiologically calibrated).
**Update 2026-11-11:** the implemented media have saved single-gene predictions
(173 / 177 / 133 essentials respectively at 1%). The MOPS-pyruvate D-21/V-01 cell
has passed its media/prediction gate and has computed metrics. DEFINED denotes
recipe-based computational representation with documented bound assumptions;
LB remains PARTIAL, not a primary validation medium.
**Still open for full B-COND-01:** SCFM2, RPMI, native sputum/serum/abscess/skin
(MEDIA_GAP), and any medium required for a chosen V-01 label set that is not yet
built. See `VALIDATION_LABEL_MEDIA_OVERLAP.md`.

## B-STRAIN-01 — Strain of model: RESOLVED (PAO1)
Resolved during audit: gene IDs are PAO1 `PAxxxx` locus tags and the model is
iMO1056 (Oberhardt 2008, PAO1). Kept here as a record; **not** a blocker.
Consequence: PA14-only datasets need B-MAP-01 before use.

## B-STRAIN-02 — Experimental-paper strains re-audited & CORRECTED (record) — RESOLVED 2026-07-01
Direct PDF-evidence re-audit (`project_management/audit/PAO1_PAPER_RELEVANCE_AUDIT.md`,
`scripts/audit/extract_strain_evidence.py`) corrected the earlier "mostly PA14"
classification:
- **Lee 2015 = MPAO1** (PAO1-derived), was "PA14" — quote: "The P. aeruginosa
  parent strain was MPAO1".
- **Belanger 2022 = PAO1**, was "confirm" — quote: "…transposon insertion mutant
  pool of P. aeruginosa strain PAO1…".
- **Turner 2015 = PAO1 + PA14** (mixed, usable PAO1 rows), was "PA14".
- **Basta 2017 = PA14 (UCBPP-PA14)** confirmed. **Poulsen 2019** multi-strain
  **excludes PAO1 among the nine screened strains** (later correction; PAO1 is
  comparative/reference context). **Juhas 2015** review.
**Consequence:** the first PAO1 validation is strain-unblocked (uses PAO1/MPAO1 by
identity for PAO1-tagged rows; D-21 uses its reviewed MPAO1→PAO1 map).
Only Basta and the Poulsen mapping path need B-MAP-01. Not a blocker;
recorded as a correction.

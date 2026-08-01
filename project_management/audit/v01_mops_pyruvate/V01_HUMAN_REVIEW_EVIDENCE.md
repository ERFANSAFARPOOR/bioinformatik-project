# V-01 Human-Review Evidence Pack — MOPS-pyruvate

**Status:** `V01_HUMAN_REVIEW_EVIDENCE_READY`  
**Scope:** Source-backed preparation for human review of highest-value V-01 discrepancy clusters.  
**Hard constraints observed:** No model/GPR/medium/biomass/threshold edits; no metric retune; no commit/push.

Diagnostic categories from `V01_ERROR_STRUCTURE_AUDIT.md` remain **hypotheses**, not established causes. This document separates:

| Tag | Meaning |
|---|---|
| **MODEL OBSERVATION** | Fact measured from iMO1056 under locked `mops_pyruvate_lee2015` |
| **SOURCE FACT** | Claim with an identifiable literature/database/repo source |
| **INFERENCE** | Reasonable conclusion from model + sources |
| **HYPOTHESIS** | Plausible explanation still needing human judgment |

Frozen V-01 cells (unchanged): TP=116, FN=98, TN=764, FP=47; n=1025; Sens=0.542056; Spec=0.942047; MCC=0.538031.  
Probe artifact: `v01_human_review_probe.json` (read-only structure audit).  
Tabular companion: `data/processed/validation/v01_mops_pyruvate_human_review_evidence.csv`.

---

## Evidence-class vocabulary (recommendations only)

| Class | Use when |
|---|---|
| `MODEL_ERROR_LIKELY` | Direct structural/annotation conflict with curated biology |
| `MODEL_SCOPE_LIMITATION_LIKELY` | Documented GEM design gap (e.g. biomass coupling) |
| `BIOLOGICAL_CONTEXT_NOT_MODELED` | Biology exists but condition/regulation not represented |
| `EXPERIMENTAL_OR_MAPPING_UNCERTAINTY` | Label/mapping/Tn-seq call may be uncertain |
| `CURRENT_MODEL_STRUCTURE_SUPPORTED` | Model representation matches available evidence |
| `UNRESOLVED` | Insufficient evidence to prefer one explanation |

---

## A. Sulfate transport cluster (FP ×5)

### Genes
PA0280 (`cysA`), PA0281 (`cysW`), PA0282 (`cysT`), PA0283 (`sbp`), PA1493 (`cysP`).

### MODEL OBSERVATION
- Single associated reaction: `SULabc` — sulfate ABC uptake:  
  `atp_c + h2o_c + so4_e → adp_c + h_c + pi_c + so4_c`
- Exact GPR: `PA0280 and PA1493 and PA0282 and PA0281 and PA0283`
- WT flux `SULabc` ≈ 0.0864 mmol/gDW/h; `EX_so4_e` uptake same magnitude.
- Reaction KO of `SULabc` or any of the five genes → growth ≈ 0 (lethal).
- No other sulfate-uptake reaction with a gene association is present. `PA1647` is **absent** from model genes.
- Assimilation after uptake is intact (SADT2 / ADSK / PAPSR carry matching WT flux).

### SOURCE FACT — annotations
| Gene | Symbol | Annotated function | Source |
|---|---|---|---|
| PA0280 | cysA | sulfate/thiosulfate ABC ATP-binding protein | KEGG `pae:PA0280`; repo `gene_mapping.csv` |
| PA0281 | cysW | sulfate transport permease | KEGG/repo mapping |
| PA0282 | cysT | sulfate transport permease | KEGG/repo mapping |
| PA0283 | sbp | periplasmic sulfate-binding protein | KEGG `pae:PA0283`; repo mapping |
| PA1493 | cysP | periplasmic sulfate/thiosulfate-binding protein | KEGG `pae:PA1493`; repo mapping |

### SOURCE FACT — system membership
- All five are components of the canonical SulT ABC sulfate/thiosulfate transporter (CysA/CysT/CysW + periplasmic binders Sbp/CysP).  
  Sources: KEGG ABC module; Kertesz 2001 (reviewed in Piłsyk & Paszewski 2009, *Acta Biochim Pol*); Sirko et al. 1995 *J Bacteriol* 177:4134 (E. coli Sbp/CysP overlap).
- **SOURCE FACT (E. coli):** single `sbp` or `cysP` mutants remain sulfate-utilizing; double binder KO blocks transport (Sirko 1995).  
  **INFERENCE:** requiring **both** PA0283 **and** PA1493 in an AND-GPR is likely over-restrictive relative to binder redundancy known in enterobacteria. PAO1-specific double-binder genetics were not located in this pass → flag for human confirmation.

### SOURCE FACT — alternative uptake
- PAO1 encodes SulP-family candidate **PA1647**, sulfate-starvation-inducible (Tralau et al. 2007 *J Bacteriol* 189:6743; cited as SulP sulfate-transporter clade member in Marietou et al. 2018 *Front Microbiol*).
- Functional transport proof for PA1647 (direct uptake assay in PAO1) remains limited; Zolotarev et al. 2008 discuss related SulP proteins. Treat as **supported candidate**, not proven sole rescue.

### SOURCE FACT — medium sulfur
- Approved medium `mops_pyruvate_lee2015` includes `EX_so4_e = -1000` from Lee SI MOPS base containing **K2SO4** and **FeSO4** (repo `mops_pyruvate_lee2015_exchanges.csv`; Lee et al. 2015 PNAS).
- Sulfur source in the experiment = inorganic sulfate (not organosulfur).  
  **INFERENCE:** discrepancy is not “wrong sulfur source in medium recipe”; it is uptake-route representation under sulfate repletion.

### Verdict options (human choose)
1. **Missing/omitted alternate transporter (PA1647 or other)** → `MODEL_ERROR_LIKELY` / gap relative to genome annotation — **supported as candidate by Tralau 2007; not proven as the V-01 rescue mechanism**.
2. **Over-restrictive AND-GPR (especially Sbp AND CysP)** → `MODEL_ERROR_LIKELY` for binders — **supported by E. coli genetics; PAO1 confirmation PENDING**.
3. **Membrane components truly essential but Tn-seq false negative** → `EXPERIMENTAL_OR_MAPPING_UNCERTAINTY` — possible but weaker given 0/3 calls for all five.
4. **Medium/environment mismatch** → **not supported** for sulfur identity; sulfate is present.

**Recommended evidence class (cluster):** `MODEL_ERROR_LIKELY` (forced sole transporter ± over-AND binders), with residual `UNRESOLVED` on which exact biological rescue operates in MOPS-pyruvate.  
**human_review_required:** YES (cluster-level).

---

## B. Translation / tRNA cluster (FN ×18)

### Genes (pathway_cluster=`translation_trna`)
PA0008/9 (glyQS), PA0903 (alaS), PA0956 (proS), PA0963 (aspS), PA1795 (cysS), PA2612 (serS), PA2739/40 (pheTS), PA2744 (thrS), PA3134 (gltX), PA3700 (lysS), PA3802/PA4939 (hisS pair), PA3834 (valS), PA3987 (leuS), PA4560 (ileS), PA5051 (argS).

### MODEL OBSERVATION — shared mechanism test
| Test | Result |
|---|---|
| Biomass `PA_Biomass6_DM` amino-acid constituents | **20** free L-amino acids (direct protein proxy) |
| Charged-tRNA / tRNA metabolites in biomass | **0** |
| Aminoacyl-tRNA synthetase reactions in model | 18 |
| Blocked under MOPS-pyruvate | **17/18** |
| Non-zero WT flux | **1/18** (`GLUTRS` ≈ 3e-6, not biomass-coupled) |
| KO/WT ratios for cluster | ≈ 1.0 for all 18 |

**Conclusion of structural test:** aminoacyl-tRNA charging is **not coupled** to growth. Biomass drains free amino acids, not aa-tRNAs. Knocking out synthetases cannot reduce FBA growth.

### SOURCE FACT — reconstruction design
- Oberhardt et al. 2008 *J Bacteriol* (iMO1056; PMC2293256): among false negatives vs genome-wide KO data, **10 genes encode tRNA synthetases**; reactions were included “for completeness” but **tRNAs are gaps and not involved in model function**; removing them as non-metabolic would raise essential-gene match 41%→44%.

### SOURCE FACT — experimental essentiality
- These loci are consensus essentials in D-21 / Lee–Varadarajan MOPS-pyruvate remap (`minimal_sum` 2–3). Biologically, aminoacyl-tRNA synthetases are core translation essentials — **plausible true positives experimentally**.

### Verdict
- This is **one shared model-scope / biomass-coupling issue**, not 18 independent gene errors.
- **Evidence class:** `MODEL_SCOPE_LIMITATION_LIKELY` (explicitly documented by Oberhardt 2008).
- Not a medium error; not a threshold artifact (ratios ≈ 1).
- **human_review_required:** YES as a **single cluster decision** (how to treat aaRS in validation reporting / scope statements). Do **not** edit biomass in this task.

---

## C. Isoenzyme cases (FN)

### C1. PA1580 (`gltA`) — citrate synthase `CS`

| Field | Value |
|---|---|
| Reaction | `CS`: accoa + h2o + oaa → cit + coa + h |
| GPR | `PA0795 or PA1580` |
| OR partner | PA0795 (`prpC`) |
| WT / KO flux | ≈ 4.94 / 4.94 (reaction survives KO) |
| Exp | POSITIVE (`minimal_sum`=2); KO/WT≈1.0 |

**SOURCE FACT:** PA1580 = citrate synthase (EC 2.3.3.1); PA0795 = 2-methylcitrate synthase PrpC (EC 2.3.3.5) (KEGG).  
**SOURCE FACT:** In PA, PrpC can provide underground citrate-synthase activity after regulatory rewiring (`prpR` loss), not as a constitutively equivalent housekeeping isozyme (Dolan et al. 2022 *mBio* e02541-22; related 2-MCC literature).  
**Classification:** `POSSIBLE_OVERPERMISSIVE_GPR` + `CONTEXT_NOT_CAPTURED_BY_GEM`  
**Evidence class:** `BIOLOGICAL_CONTEXT_NOT_MODELED` (promiscuity/regulation) with secondary `MODEL_ERROR_LIKELY` if OR is treated as unconditional equivalence.  
**human_review_required:** YES.

### C2. PA1787 (`acnB`) — aconitase `ACONT`

| Field | Value |
|---|---|
| Reaction | `ACONT`: cit ↔ icit |
| GPR | `PA1787 or PA1562` |
| OR partner | PA1562 (`acnA`) |
| WT / KO flux | ≈ 4.94 / 4.94 |
| Exp | POSITIVE (`minimal_sum`=2); KO/WT≈1.0 |

**SOURCE FACT:** Both AcnA and AcnB are annotated aconitate hydratases (EC 4.2.1.3) (KEGG). Iron/PrrF regulation differentially affects aconitases (Massé / Vasil literature; Oglesby-Sherrouse & Vasil 2007 *JBC*).  
**INFERENCE:** OR-GPR is enzymatically defensible (`VALID_BIOLOGICAL_ISOENZYME`), but GEM cannot capture condition-specific dominance of AcnB → FN under MOPS-pyruvate is `CONTEXT_NOT_CAPTURED_BY_GEM`.  
**Evidence class:** `BIOLOGICAL_CONTEXT_NOT_MODELED`.  
**human_review_required:** YES.

### C3. PA0944 (`purN`) — `GARFTi`

| Field | Value |
|---|---|
| Reaction | `GARFTi`: 10fthf + gar → fgam + thf + h |
| GPR | `PA0944 or (PA3751 or PA0836)` |
| Partners | PA3751 (`purT`); **PA0836 (`ackA`)** |
| WT / KO flux | ≈ 0.156 / 0.156 |
| Exp | POSITIVE (`minimal_sum`=2); KO/WT≈1.0 |

**SOURCE FACT:** PurN (10fTHF-dependent) and PurT (formate/ATP-dependent; EC 6.3.1.21) are established alternative GAR transformylases (Nygaard & Smith 1993 *J Bacteriol* for E. coli; KEGG PA0944/PA3751).  
**SOURCE FACT:** PA0836 is **acetate kinase ackA**, also associated in-model with `ACKr` and oddly with `GART` (`PA3751 or PA0836`). Repo gene names + KEGG contradict any GARFT catalysis by AckA.  
**Classification:**
- PA0944 ↔ PA3751: `VALID_BIOLOGICAL_ISOENZYME` (cofactor differs; condition dependence possible).
- Inclusion of PA0836: `POSSIBLE_OVERPERMISSIVE_GPR` / annotation error — **`MODEL_ERROR_LIKELY`**.
**Evidence class:** mixed — `MODEL_ERROR_LIKELY` (AckA) + `BIOLOGICAL_CONTEXT_NOT_MODELED` (PurN vs PurT).  
**human_review_required:** YES.

---

## D. Lipid / GPR cases (FP)

### Genes
PA0005 (`lptA`), PA3673 (`plsB`).

### MODEL OBSERVATION
- Reaction `12DAG3Ps_PA` — “1,2-diacyl-sn-glycerol 3-phosphate synthesis” (lumped PA phosphatidate formation from glyc3p + acyl-ACPs).
- Exact GPR: **`PA0005 and PA3673`**
- WT flux ≈ 0.083; KO of either gene → flux 0, growth ≈ 0.
- Biomass consumes `pe_PA_c`, `pg_PA_c`, `cdlp_PA_c`, `ps_PA_c` (phospholipid demand); `12dag3p_PA_c` feeds `PHCYTr_PA`.

### SOURCE FACT — biochemistry
| Gene | Enzyme | EC | Step |
|---|---|---|---|
| PA3673 plsB | glycerol-3-phosphate O-acyltransferase | 2.3.1.15 | G3P → LPA |
| PA0005 lptA | 1-acyl-sn-glycerol-3-phosphate acyltransferase | 2.3.1.51 | LPA → PA |

Sources: KEGG `pae:PA0005`, `pae:PA3673`; Baysse et al. 2005 *Microbiology* 151:3171 (lptA = functional PlsC homolog).

**INFERENCE:** AND is appropriate **only as a lumped two-step requirement**, not as a physical heterocomplex. It becomes false-essential if **either** step has biological isozyme(s) missing from the model.

### SOURCE FACT — essentiality / alternatives
- Baysse et al. 2005: Δ`lptA` mutant is **viable** with altered fatty-acid profile → LptA is **not essential**; other LPAAT activity must exist.
- Cronan et al. 2023 *Microbiology* 169:001400: “at least one other acyltransferase must be active… since LptA is not essential”; no single Pseudomonas LPAAT shown essential.
- Experimental V-01 labels: both genes NEGATIVE 0/3 — consistent with Baysse for PA0005; PA3673 (`plsB`) literature essentiality less decisive in this pass.

### Verdict options
1. Missing alternate LPAAT (and possibly alternate GPAT) → `MODEL_ERROR_LIKELY` / missing isozyme in lumped GPR.
2. Biomass phospholipid demand forces essentiality of the only phosphatidate route → contributing `MODEL_SCOPE_LIMITATION_LIKELY` / formulation tightness.
3. AND mis-modeling as complex rather than sequential lump → review wording; biological issue is still missing alternatives.

**Recommended evidence class:** `MODEL_ERROR_LIKELY` (missing LPAAT isozyme[s] relative to Baysse/Cronan) with contributing biomass routing.  
**Not supported:** claiming AND is a validated heterocomplex.  
**human_review_required:** YES.

---

## E. Representative alternative-pathway FNs

### E1. PA0024 (`hemF`) — `CPPPGO` — **biological bypass present**

| Item | Detail |
|---|---|
| Primary rxn | `CPPPGO` (O2-dependent): PA0024 |
| WT / KO primary flux | ~4e-7 → 0 |
| KO growth | ≈ WT |
| Bypass rxn | `CPPPGOAN` (oxygen-independent): **PA1546 (`hemN`)** carries ~4e-7 after KO |
| Double KO PA0024+PA1546 | growth = 0 |

**SOURCE FACT:** HemF (aerobic) and HemN (O2-independent) both catalyze coproporphyrinogen-III → protoporphyrinogen-IX in PAO1; Rompf et al. 1998 *Mol Microbiol* 29:xxx (Anr/Dnr regulation); hemF/hemN mutants still grew, implying additional HemZ-type activity.  
**INFERENCE:** Model bypass via `CPPPGOAN` is **biologically documented**, not a pure topology artifact. Tension remains: Lee calls PA0024 essential under **aerobic** MOPS-pyruvate (sum=3), while model freely uses HemN aerobically without regulation.  
**Evidence class:** `BIOLOGICAL_CONTEXT_NOT_MODELED` (oxygen/regulatory context) ± residual experimental uncertainty.  
**Bypass type:** **BIOLOGICAL (documented)** / over-available aerobically in GEM.

### E2. PA0607 (`rpe`) — `RPE` — **computational / annotation-suspect bypass**

| Item | Detail |
|---|---|
| Primary rxn | `RPE`: ru5p ↔ xu5p ; GPR PA0607 |
| WT / KO | −0.291 → 0 |
| KO/WT | ≈ 0.994 |
| Bypass fluxes | Oxidative PPP opens: `G6PDHy` + `PGL` + **`PGDH` (PA0743)** ≈ 0.434; TKT/RPI rearrange |

**SOURCE FACT:** PA0743 is annotated **probable 3-hydroxyisobutyrate dehydrogenase**, not 6-phosphogluconate dehydrogenase (repo `with_gene_names.csv`). Classical oxidative PPP decarboxylation (Gnd) is widely regarded as absent/non-canonical in *P. aeruginosa* EDEMP architecture (Nikel/Dolan literature; CRISPRi preprint 2025 reports Rpe essential and notes absence of Gnd).  
**INFERENCE:** RPE rescue is largely a **computational bypass** enabled by a likely mis-GPR/`PGDH` edge — **not** a validated biological alternative.  
**Evidence class:** `MODEL_ERROR_LIKELY` (PGDH/PA0743) driving a false FN.  
**Bypass type:** **COMPUTATIONAL / annotation-suspect**.

### E3. PA3107 (`metZ`) — `SHSL2` — **biological bypass present**

| Item | Detail |
|---|---|
| Primary | `SHSL2` direct sulfhydrylation: suchms + h2s → hcys (PA3107) |
| WT flux | ≈ 0.086 |
| After KO | SHSL2=0; growth retained (ratio≈0.997) |
| Bypass | `SHSL5` + `CYSTLr` (both **PA0400**) → hcys → `METS` (PA1843) |

**SOURCE FACT:** PA uses direct sulfhydrylation via MetZ as a primary methionine route, with parallel transsulfuration (Foglino et al. 1995 *Microbiology* 141:431).  
**INFERENCE:** Model bypass is **biologically documented**. Why Lee still calls metZ essential (sum=2) under MOPS-pyruvate may reflect incomplete compensation in vivo — `BIOLOGICAL_CONTEXT_NOT_MODELED` / residual experimental tension.  
**Bypass type:** **BIOLOGICAL (documented)**.

### E4. PA1049 — B6 oxidase set — **inactive primary edges**

Associated: `PDX5PO`, `PYAM5PO`, `PYDXNO`, `PYDXO` (all GPR PA1049). WT fluxes = 0; KO ratio ≈ 1.  
**INFERENCE:** Not a meaningful “active-pathway bypass”; closer to unused/blocked demand or alternate B6 supply topology.  
**Evidence class:** `UNRESOLVED` / possible `MODEL_SCOPE_LIMITATION_LIKELY`.  
**Bypass type:** **not established**.

### E5. PA3480 — `DCTPD` — **inactive primary edge**

WT flux 0; KO ratio ≈ 1. Same interpretation as E4.  
**Evidence class:** `UNRESOLVED`.

---

## F. Revised high-priority shortlist (≤20)

Replace the prior Priority-1 gene laundry list with these **cluster-first** items:

| # | Item | Errors explained | Recommended class | Review action |
|---|---|---|---|---|
| 1 | **Translation/tRNA–biomass decoupling** | ~18 FN | `MODEL_SCOPE_LIMITATION_LIKELY` | Confirm Oberhardt gap; decide reporting treatment of aaRS |
| 2 | **Sulfate uptake sole-route `SULabc` cluster** | 5 FP | `MODEL_ERROR_LIKELY` | Review PA1647/SulP + Sbp/CysP AND logic; no auto-add |
| 3 | **`12DAG3Ps_PA` AND (lptA∧plsB)** | 2 FP | `MODEL_ERROR_LIKELY` | Missing LPAAT isozyme(s); Baysse 2005 |
| 4 | **GARFT GPR includes ackA (PA0836)** | 1 FN + polluted GPRs | `MODEL_ERROR_LIKELY` | Remove AckA from GARFT/GART only after human sign-off |
| 5 | **`PGDH` assigned to PA0743 (RPE bypass)** | 1 FN (+ topology risk) | `MODEL_ERROR_LIKELY` | Re-annotate/remove false oxidative PPP decarboxylation |
| 6 | **gltA OR prpC unconditional** | 1 FN | `BIOLOGICAL_CONTEXT_NOT_MODELED` | Underground metabolism ≠ constitutive isozyme |
| 7 | **acnB OR acnA without condition** | 1 FN | `BIOLOGICAL_CONTEXT_NOT_MODELED` | Isozymes real; expression context missing |
| 8 | **hemF vs hemN aerobic availability** | 1 FN | `BIOLOGICAL_CONTEXT_NOT_MODELED` | Biological alt exists; O2 regulation absent |
| 9 | **metZ vs transsulfuration (PA0400)** | 1 FN | `BIOLOGICAL_CONTEXT_NOT_MODELED` | Biological alt documented; why essential in Lee? |
| 10 | **PurN vs PurT cofactor context** | 1 FN | `BIOLOGICAL_CONTEXT_NOT_MODELED` | Valid isozyme pair; formate/10fTHF not conditioned |
| 11 | **SDH complex partial bypass (PA1581–1584)** | 4 FN | `UNRESOLVED` | Map bypass stoichiometry before any GPR change |
| 12 | **AKGD partial bypass (PA1585/1586)** | 2 FN | `UNRESOLVED` | Same |
| 13 | **Inactive-cofactor FN group (e.g. PA1049, PA3480)** | ≥2 FN | `UNRESOLVED` | Demand vs dead-end audit |
| 14 | **FP biomass-formulation cluster (non-lipid)** | up to 7 FP | `MODEL_SCOPE_LIMITATION_LIKELY` | Inspect remaining FP_BIOMASS_FORMULATION set as one theme |
| 15 | **Remaining isoenzyme FN bulk** | ~25 FN | triage later | After items 4–10; do not mass-edit OR-GPRs |
| 16 | **Remaining FN_REACTION_INACTIVE non-tRNA** | ~20 FN | mixed scope | Separate true gaps from non-metabolic essentials |

---

## Cross-cutting recommendations (still not automatic decisions)

### Likely model issues (source-supported)
- Sole sulfate ABC + binder AND logic (Cluster A).
- AckA inside GARFT/GART GPRs (Cluster C3).
- PGDH←PA0743 enabling RPE computational bypass (Cluster E2).
- Lumped phosphatidate AND without LPAAT alternatives (Cluster D; Baysse).

### Likely scope / biology limitations
- aaRS–biomass decoupling (Oberhardt 2008; Cluster B).
- Unconditional OR for gltA/prpC and acnA/acnB (context/regulation).
- Oxygen-agnostic hemF/hemN interchange.
- Parallel methionine routes vs Tn-seq essentiality of metZ.

### Unresolved
- Exact in vivo sulfate rescue under MOPS-pyruvate (PA1647 vs binder redundancy vs other).
- Why some biological-bypass genes remain Lee-essential.
- Large SDH/AKGD and inactive-cofactor FN sets.
- Full FP_BIOMASS_FORMULATION census beyond lipid.

---

## Provenance index (non-fabricated)

1. Repo: `data/processed/validation/v01_mops_pyruvate_*.csv`; `V01_ERROR_STRUCTURE_AUDIT.md`; `gene_mapping.csv`; `mops_pyruvate_lee2015_exchanges.csv`
2. Model: `models/paeruginosa_MODEL1507180020.xml` (iMO1056)
3. Oberhardt et al. 2008 *J Bacteriol* — DOI 10.1128/JB.01583-07; PMC2293256
4. Lee et al. 2015 *PNAS* — DOI 10.1073/pnas.1422186112
5. Varadarajan et al. 2020 (D-21 remap source in repo labels)
6. KEGG PAO1 entries as cited per gene
7. Tralau et al. 2007 *J Bacteriol* 189:6743 — sulfate starvation / PA1647
8. Sirko et al. 1995 *J Bacteriol* 177:4134 — Sbp/CysP overlap (E. coli)
9. Baysse et al. 2005 *Microbiology* 151:3171 — lptA non-essential
10. Cronan et al. 2023 *Microbiology* 169:001400 — LPAAT redundancy
11. Dolan et al. 2022 *mBio* e02541-22 — PrpC/GltA underground metabolism
12. Rompf et al. 1998 *Mol Microbiol* — hemF/hemN
13. Foglino et al. 1995 *Microbiology* 141:431 — MetZ direct sulfhydrylation + parallel transsulfuration
14. Nygaard & Smith 1993 *J Bacteriol* — PurN/PurT

---

## Files

| Path | Role |
|---|---|
| `project_management/audit/v01_mops_pyruvate/V01_HUMAN_REVIEW_EVIDENCE.md` | This report |
| `project_management/audit/v01_mops_pyruvate/v01_human_review_probe.json` | Read-only model probe |
| `data/processed/validation/v01_mops_pyruvate_human_review_evidence.csv` | Per-gene evidence table |
| `scripts/validation/_probe_v01_human_review_evidence.py` | Probe script (no model writes) |

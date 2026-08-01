# Lee 2015 SRA — SRP052838 (inventory only)

**Study:** Lee et al. (2015) *PNAS* — General and condition-specific essential  
functions of *Pseudomonas aeruginosa*. DOI `10.1073/pnas.1422186112`.  
**SRA study accession:** `SRP052838`  
**Inventory date:** 2026-08-01  
**Status:** **METADATA ATTACHED ONLY** — FASTQ / BAM / insertion tables **not**  
downloaded; **no** Tn-seq reanalysis performed in this cycle.

## Why this folder exists
The project deferred an experimental **non-essential universe** for MOPS-pyruvate  
(V-01 gate / decision D). The Lee supplement sheet `All essential genes` is an  
essentials-focused table (~551 rows), so `Min sum == 0` there is **not** a  
genome-wide non-essential set. Raw Tn-seq in SRA is the principled path to  
rebuild gene-level insertion counts for **all** genes (including clear  
non-essentials), but that is a separate, heavy pipeline.

## What is in the inventory
See `SRP052838_run_inventory.csv` (16 public runs; NCBI ESummary 2026-08-01):

| medium_group | n_runs | notes |
|---|---|---|
| LB | 6 | LB-1 (3 tech reps), LB-2 (2 tech reps), LB-3 |
| MOPS-pyruvate / Minimal | **3** | Minimal-1/2/3 — primary for our V-01 cell |
| Sputum | 4 | |
| 0.1× LB / Human serum / BHI | 1 each | |

- Approximate total compressed size (SRA `total_size`): **~13.5 GB**  
- Minimal/MOPS-pyruvate only: **~3.7 GB** (`SRR1773138`, `SRR1773139`, `SRR1773140`)

## Does SRA “clarify” the non-essential universe today?
**No — not by itself.**  
Attaching accession + run list proves the data **exist and are public**.  
A transparent non-essential call set requires reprocessing reads with a  
documented method (Lee SI: Tn-seq circle; essential = few/no insertions;  
per-run cutoff P=0.001 on log2-normal; Min consensus ≥2/3 pools). Until that  
pipeline is run and reviewed, **full V-01 metrics remain gated**.

## What a real analysis would require (not done here)
1. Download FASTQ for at least the 3 Minimal runs (or all 16).  
2. Map Tn junctions to PAO1 reference; count inserts/reads per gene.  
3. Reproduce (or clearly re-implement) Lee per-run essential calls.  
4. Define non-essential as genes **tested** with sufficient coverage and  
   **not** called essential on MOPS-pyruvate (exact rule = new DECISIONS entry).  
5. Only then: join to iMO1056 predictions for confusion-matrix V-01.

## Do not
- Treat SRA accession as a finished negative label set.  
- Download multi-GB FASTQ into git.  
- Fabricate insertion counts or essentiality calls from this inventory.

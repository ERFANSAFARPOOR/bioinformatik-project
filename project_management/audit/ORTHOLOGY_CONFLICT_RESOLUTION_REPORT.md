# ORTHOLOGY_CONFLICT_RESOLUTION_REPORT.md

**Date:** 2026-07-10
**Decision context:** `APPROVED_LIMITED`
**Conflict status:** `RESOLVED_SUPPORTS_TURNER`
**Resolution source:** KEGG SSDB Best Search 2026-07-10

---

## 1. Conflicting rows (Turner candidate)

From `data/processed/ortholog/pao1_pa14_orthologs_turner2015_CANDIDATE.csv`:

| pao1_locus_tag | pa14_locus_tag | pao1_gene | pa14_gene | gene_symbol_match | belanger_crosscheck |
|---|---|---|---|---|---|
| PA2279 | PA14_35100 | arsC | arsC | yes | **disagree** (Belanger maps PA2279 → PA14_35130) |
| PA2277 | PA14_35130 | arsR | arsR | yes | not_in_belanger |

These two Turner pairs occupy the same arsenic-resistance neighborhood. Belanger’s
single disagreement swaps the PA14 partner of PA2279 onto PA14_35130, which is
Turner’s partner for PA2277.

Belanger cross-check totals on the full candidate: **598 agree / 1 disagree /
4,766 not_in_belanger**.

---

## 2. Local evidence

- Turner 2015 sd03/sd04 (Pseudomonas Genome Database BLAST+synteny 1:1 orthologs)
  pairs **PA2279↔PA14_35100** and **PA2277↔PA14_35130**.
- Gene symbols match within each Turner pair (`arsC`/`arsC`, `arsR`/`arsR`).
- Belanger DS1 independently agrees with Turner on 598 shared PAO1 IDs; the only
  disagreement is PA2279.
- Candidate table otherwise has 5,365 unique PAO1 and 5,365 unique PA14 IDs
  (strict 1:1; no duplicates).

Local evidence alone is insufficient to choose between Turner and Belanger at
PA2279; an external bidirectional sequence search was required.

---

## 3. KEGG SSDB evidence (2026-07-10)

| Query | Best PAO1/PA14 hit | Identity | Notes |
|---|---|---|---|
| `pau:PA14_35100` | `pae:PA2279` | **1.000** | Supports Turner |
| `pau:PA14_35130` | `pae:PA2277` | **1.000** | Supports Turner |
| `pae:PA2279` | `pau:PA14_35100` | **1.000** | Reverse confirms Turner |
| `pae:PA2277` | `pau:PA14_35130` | **1.000** | Reverse confirms Turner |

URLs:
- https://www.kegg.jp/ssdb-bin/ssdb_best?org_gene=pau:PA14_35100
- https://www.kegg.jp/ssdb-bin/ssdb_best?org_gene=pau:PA14_35130
- https://www.kegg.jp/ssdb-bin/ssdb_best?org_gene=pae:PA2279
- https://www.kegg.jp/ssdb-bin/ssdb_best?org_gene=pae:PA2277

Bidirectional 100% identity best hits reproduce Turner’s pairing and do **not**
support Belanger’s PA2279 → PA14_35130 assignment.

---

## 4. Why Turner is accepted

1. Turner’s pairs are internally consistent (matching gene symbols + 1:1 table).
2. KEGG SSDB Best Search returns the same pairs at identity 1.000 in both
   directions.
3. Accepting Turner preserves a coherent arsenic locus mapping
   (arsC↔PA14_35100, arsR↔PA14_35130) without inventing new pairs.

**Policy applied:** keep both Turner rows; mark
`conflict_status=RESOLVED_SUPPORTS_TURNER`; set `approved_for_l03b=yes` for all
5,365 candidate rows.

---

## 5. Why Belanger is rejected for this locus

- Belanger’s PA2279 → PA14_35130 contradicts KEGG SSDB bidirectional best hits.
- That Belanger assignment would collide with Turner’s PA2277 → PA14_35130 pair
  under a strict 1:1 policy.
- Rejection is **locus-specific** (PA2279 / PA14_35100 / PA14_35130 neighborhood
  only). Belanger’s 598 agreeing rows remain useful cross-check evidence
  elsewhere; Belanger is not discarded as a whole.

---

## 6. Limitations

- Resolution uses KEGG SSDB Best Search snapshots from 2026-07-10, not a full
  OrthologueDB / pseudomonas.com live export.
- Turner 2015 is a 1:1 BLAST+synteny subset; PA14-only / PAO1-only / one-to-many
  cases remain outside this approval.
- APPROVED_LIMITED ≠ unrestricted mapping; do not merge into `gene_mapping.csv`
  without a separate task.
- Poulsen/Basta are **not** validation-ready; they are only eligible for future
  controlled L-03b draft mapping using approved 1:1 rows.
- **Metrics remain blocked** (B-SCI-01) until real labels + media + predictions
  exist.

---

## 7. Derived artifacts

| File | Role |
|---|---|
| `ORTHOLOGY_HUMAN_REVIEW_DECISION.md` | Human decision record |
| `data/processed/ortholog/pao1_pa14_orthologs_turner2015_APPROVED_LIMITED.csv` | Full approved table + review columns |
| `data/processed/ortholog/pao1_pa14_orthologs_turner2015_APPROVED_LIMITED_FOR_L03B.csv` | Same 5,365 approved rows (conflict resolved; none excluded) |

Original CANDIDATE CSV is **unchanged**.

# ORTHOLOGY_HUMAN_REVIEW_DECISION.md

**Date:** 2026-07-10
**Branch:** `erfan/orthology-human-review` (requested: `homayoun/orthology-human-review`)
**Decision:** APPROVED_LIMITED
**Conflict resolution:** RESOLVED_SUPPORTS_TURNER

---

## 1. Decision

**APPROVED_LIMITED**

The Turner-derived PA14↔PAO1 orthology candidate is acceptable **only** as an
interim strict 1:1 mapping source for future controlled draft mapping. This is
**not** unrestricted orthology approval.

## 2. Reviewed file

`data/processed/ortholog/pao1_pa14_orthologs_turner2015_CANDIDATE.csv`

## 3. Reviewed derived file

`data/processed/ortholog/pao1_pa14_orthologs_turner2015_APPROVED_LIMITED.csv`

Optional filtered export (all approved rows):
`data/processed/ortholog/pao1_pa14_orthologs_turner2015_APPROVED_LIMITED_FOR_L03B.csv`

## 4. Main conclusion

The Turner-derived table (5,365 strict 1:1 pairs) is approved for **limited**
PA14→PAO1 draft mapping. The single Belanger disagreement at PA2279 is
**resolved in favor of Turner** by KEGG SSDB bidirectional 100% identity best
hits.

## 5. Structural checks

| Check | Result |
|---|---|
| Total rows | **5,365** |
| Unique PAO1 IDs | **5,365** |
| Unique PA14 IDs | **5,365** |
| Duplicate PAO1 / PA14 | **0 / 0** |
| Invalid locus tags | **0** |

## 6. Belanger cross-check

| Value | Count |
|---|---|
| agree | **598** |
| disagree | **1** (PA2279) |
| not_in_belanger | **4,766** |

## 7. Conflict

| pao1_locus_tag | pa14_locus_tag | pao1_gene | pa14_gene | belanger_crosscheck |
|---|---|---|---|---|
| PA2279 | PA14_35100 | arsC | arsC | disagree (Belanger: PA14_35130) |
| PA2277 | PA14_35130 | arsR | arsR | not_in_belanger |

## 8. Conflict resolution — RESOLVED_SUPPORTS_TURNER

KEGG SSDB Best Search (accessed 2026-07-10) supports Turner:

| Pairing | Evidence |
|---|---|
| **PA14_35100 ↔ PA2279** | identity **1.000** (bidirectional) |
| **PA14_35130 ↔ PA2277** | identity **1.000** (bidirectional) |

URLs:
- https://www.kegg.jp/ssdb-bin/ssdb_best?org_gene=pau:PA14_35100
- https://www.kegg.jp/ssdb-bin/ssdb_best?org_gene=pau:PA14_35130
- https://www.kegg.jp/ssdb-bin/ssdb_best?org_gene=pae:PA2279
- https://www.kegg.jp/ssdb-bin/ssdb_best?org_gene=pae:PA2277

**Belanger PA2279 → PA14_35130 is rejected for this locus.**

## 9. Conflict handling

Both Turner conflict-region rows are retained with:

- `approved_for_l03b = yes`
- `conflict_status = RESOLVED_SUPPORTS_TURNER`
- `review_flag = APPROVED_LIMITED_RESOLVED_CONFLICT`

**All 5,365 rows have `approved_for_l03b = yes`** because the one conflict is
resolved in favor of Turner (no rows excluded).

## 10. Approved use

- Use only strict 1:1 approved rows for future controlled L-03b draft mapping
- Do not use gene-symbol-only evidence
- Do not force PA14-unique / PAO1-unique genes
- Do not merge into `gene_mapping.csv` without separate approval
- **Do not compute metrics yet**
- Poulsen/Basta are **only eligible for future controlled L-03b draft mapping** —
  not validation-ready

## 11. Limitations

- Turner table = 2015 Pseudomonas Genome Database BLAST+synteny **1:1 subset**
- Full live OrthologueDB / pseudomonas.com export remains preferred when available
- PA14 biology may not fully transfer to PAO1
- Poulsen/Basta still require controlled L-03b parsing and human review

## 12. Impact on blockers

B-MAP-01 narrowed, not fully closed.

Status:
`CANDIDATE_APPROVED_LIMITED_FOR_1TO1_PA14_TO_PAO1_MAPPING_WITH_CONFLICT_POLICY`

## 13. Next step

Separate L-03b task: draft-map Poulsen/Basta using `approved_for_l03b = yes`
rows only. **No metrics.**

## Safety

- Original CANDIDATE file unchanged
- No merge into `gene_mapping.csv`
- No metrics / simulations / condition JSON / Poulsen-Basta parse / push
- Stop before commit unless explicitly approved

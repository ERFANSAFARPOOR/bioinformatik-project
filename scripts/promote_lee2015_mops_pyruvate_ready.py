"""Promote Lee2015 MOPS-pyruvate positive labels (derived READY file only).

Human decision 2026-07-29: APPROVED_FOR_PROMOTION for positive labels only.
Does NOT overwrite canonical evidence; does NOT compute full metrics.
"""
from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
NEEDS = (
    ROOT
    / "data"
    / "processed"
    / "literature"
    / "gene_level"
    / "literature_evidence_gene_level_NEEDS_REVIEW.csv"
)
OUT_READY = (
    ROOT
    / "data"
    / "processed"
    / "literature"
    / "gene_level"
    / "literature_evidence_gene_level_READY_mops_pyruvate_lee2015.csv"
)
OUT_PA0728 = (
    ROOT
    / "data"
    / "processed"
    / "literature"
    / "gene_level"
    / "lee2015_mops_pyruvate_PA0728_1_absent_from_model.md"
)
PA_RE = re.compile(r"^PA\d+$")

PROMO_NOTE = (
    "APPROVED_FOR_PROMOTION 2026-07-29 (human review): Lee2015 MOPS-pyruvate "
    "POSITIVE essentiality labels only. SI Materials and Methods → Sequence Data "
    "Analysis (p.1/7): consensus = genes found in >=2 of 3 MOPS-pyruvate pools; "
    "workbook column 'Min sum (of 3)' holds those pool counts. "
    "Source: project_management/audit/LEE2015_PER_MEDIUM_REVIEW.md "
    "(Human review note: MOPS-pyruvate…). "
    "Scope limit: does NOT define experimental non-essential universe; "
    "full confusion-matrix metrics (precision/recall/F1/MCC/specificity) remain gated."
)


def main() -> None:
    needs = pd.read_csv(NEEDS)
    filt = (
        (needs["study_id"] == "lee2015")
        & (needs["phenotype_class"] == "condition-specific-essential")
        & (needs["medium"] == "MOPS-pyruvate")
        & (needs["source_column"] == "Min sum (of 3)")
        & (needs["review_status"] == "NEEDS_REVIEW")
    )
    # Exclude other media columns explicitly
    forbidden_cols = {
        "LB sum (of 6)",
        "Sputum sum (of 4)",
        "BHI (of 1)",
        "0.1X LB (of 1)",
        "Serum (of 1)",
    }
    ready = needs.loc[filt].copy()
    assert not ready["source_column"].isin(forbidden_cols).any()

    # Validate IDs
    ids = ready["mapped_pao1_gene_id"].astype(str).str.strip()
    orig = ready["original_gene_id"].astype(str).str.strip()
    assert len(ready) == 437, f"expected 437 rows, got {len(ready)}"
    assert ids.str.match(r"^PA\d+$").all(), "non-PAxxxx mapped ids present"
    assert orig.str.match(r"^PA\d+$").all(), "non-PAxxxx original ids present"
    assert (ready["phenotype_class"] == "condition-specific-essential").all()
    assert ready["medium"].eq("MOPS-pyruvate").all()
    assert "PA0728.1" not in set(ids) and "PA0728.1" not in set(orig)

    ready["review_status"] = "READY"
    # Preserve prior notes; append promotion provenance
    prior = ready["notes"].fillna("").astype(str)
    ready["notes"] = prior.where(prior.str.len() == 0, prior + " | ") + PROMO_NOTE
    if "human_review_decision" in ready.columns:
        ready["human_review_decision"] = "APPROVED_FOR_PROMOTION"
    else:
        ready.insert(
            len(ready.columns),
            "human_review_decision",
            "APPROVED_FOR_PROMOTION",
        )

    OUT_READY.parent.mkdir(parents=True, exist_ok=True)
    ready.to_csv(OUT_READY, index=False)

    # PA0728.1 coverage note
    OUT_PA0728.write_text(
        """# PA0728.1 — Lee2015 MOPS-pyruvate absent_from_model note

**Date:** 2026-07-29  
**Decision source:** `project_management/audit/LEE2015_PER_MEDIUM_REVIEW.md`
(Human review note: MOPS-pyruvate…; APPROVED_FOR_PROMOTION for standard PAxxxx only)

## Facts (measured / reviewed)
- Workbook `All essential genes`, column `Min sum (of 3)`: **PA0728.1 = 3**
  (positive MOPS-pyruvate essentiality call in source).
- Neither `PA0728.1` nor `PA0728` appears in iMO1056 model gene IDs
  (`results/essentiality/gene_essentiality_mops_pyruvate_lee2015.csv`).
- Raw source identifier is **retained unchanged** in
  `data/raw/literature/lee2015/pnas.1422186112.sd01.xlsx` (read-only).

## Classification
- `absent_from_model / unmapped`
- Excluded from the processed READY identity-join set (437 standard `PAxxxx`)
- **Not** renamed to `PA0728`
- **No** automatic remapping without an authoritative annotation source

## Implication for overlap analysis
PA0728.1 is counted in the workbook's 438 Min≥2 rows but not among the 437
READY positive labels used for model identity join.
""",
        encoding="utf-8",
    )

    print("Wrote", OUT_READY)
    print("Wrote", OUT_PA0728)
    print("rows", len(ready))
    print("unique mapped", ids.nunique())
    print("phenotype", ready["phenotype_class"].unique().tolist())
    print("media", ready["medium"].unique().tolist())
    print("source_columns", ready["source_column"].unique().tolist())
    print("review_status", ready["review_status"].unique().tolist())


if __name__ == "__main__":
    main()

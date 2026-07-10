"""Build APPROVED_LIMITED ortholog CSVs from the Turner CANDIDATE table.

Read-only on CANDIDATE. Writes derived APPROVED_LIMITED files only.
No metrics, no gene_mapping merge, no Poulsen/Basta parse.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
CAND = ROOT / "data/processed/ortholog/pao1_pa14_orthologs_turner2015_CANDIDATE.csv"
OUT = ROOT / "data/processed/ortholog/pao1_pa14_orthologs_turner2015_APPROVED_LIMITED.csv"
OUT_L03B = ROOT / "data/processed/ortholog/pao1_pa14_orthologs_turner2015_APPROVED_LIMITED_FOR_L03B.csv"

CONFLICT_PAO1 = {"PA2279", "PA2277"}
CONFLICT_PA14 = {"PA14_35100", "PA14_35130"}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    before = sha256(CAND)
    df = pd.read_csv(CAND, dtype=str).fillna("")
    assert len(df) == 5365, len(df)

    conflict = df["pao1_locus_tag"].isin(CONFLICT_PAO1) | df["pa14_locus_tag"].isin(
        CONFLICT_PA14
    )
    # Expect exactly the two Turner conflict-region rows
    n_conflict = int(conflict.sum())
    assert n_conflict == 2, n_conflict

    out = df.copy()
    out["approved_for_l03b"] = "yes"
    out["conflict_status"] = "none"
    out["resolution_source"] = ""
    out["human_review_decision"] = "APPROVED_LIMITED"
    out["human_review_notes"] = ""
    out["review_flag"] = "APPROVED_LIMITED_1TO1"

    out.loc[conflict, "conflict_status"] = "RESOLVED_SUPPORTS_TURNER"
    out.loc[conflict, "resolution_source"] = "KEGG SSDB Best Search 2026-07-10"
    out.loc[conflict, "human_review_notes"] = (
        "KEGG SSDB supports Turner pairing; Belanger PA2279->PA14_35130 "
        "rejected for this locus"
    )
    out.loc[conflict, "review_flag"] = "APPROVED_LIMITED_RESOLVED_CONFLICT"

    out.to_csv(OUT, index=False)
    # Conflict resolved in favor of Turner → all rows eligible for L-03b draft
    out.to_csv(OUT_L03B, index=False)

    after = sha256(CAND)
    assert before == after, "CANDIDATE file was modified — abort"

    print(f"candidate_sha256={before}")
    print(f"rows={len(out)}")
    print(f"approved_for_l03b_yes={(out['approved_for_l03b'] == 'yes').sum()}")
    print(
        "resolved_conflict_rows="
        f"{(out['conflict_status'] == 'RESOLVED_SUPPORTS_TURNER').sum()}"
    )
    print(f"wrote={OUT}")
    print(f"wrote={OUT_L03B}")


if __name__ == "__main__":
    main()

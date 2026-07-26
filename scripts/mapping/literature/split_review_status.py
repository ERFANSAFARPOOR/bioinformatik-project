"""
split_review_status.py

Regenerate two filtered CSVs from the DRAFT aggregate, based on review_status:
    - literature_evidence_gene_level_READY_ONLY.csv   (review_status == READY)
    - literature_evidence_gene_level_NEEDS_REVIEW.csv (review_status == NEEDS_REVIEW)

Pure mechanical filter, no new scientific judgment. Per
L03_DRAFT_REVIEW_AUDIT.md, review_status is already set by
parse_supplements.py based on defined scientific rules, not manual
human review -- so this regeneration is safe.

Input:
    data/processed/literature/gene_level/literature_evidence_gene_level_DRAFT.csv

Output:
    data/processed/literature/gene_level/literature_evidence_gene_level_READY_ONLY.csv
    data/processed/literature/gene_level/literature_evidence_gene_level_NEEDS_REVIEW.csv
"""

import csv
from pathlib import Path

# scripts/mapping/literature/split_review_status.py -> project root
ROOT = Path(__file__).resolve().parents[3]

GENE_LEVEL_DIR = ROOT / "data" / "processed" / "literature" / "gene_level"
DRAFT = GENE_LEVEL_DIR / "literature_evidence_gene_level_DRAFT.csv"
READY_OUT = GENE_LEVEL_DIR / "literature_evidence_gene_level_READY_ONLY.csv"
REVIEW_OUT = GENE_LEVEL_DIR / "literature_evidence_gene_level_NEEDS_REVIEW.csv"


def main():
    if not DRAFT.exists():
        raise FileNotFoundError(f"DRAFT file not found: {DRAFT}")

    with open(DRAFT, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    ready_rows = [r for r in rows if r.get("review_status", "").strip() == "READY"]
    review_rows = [r for r in rows if r.get("review_status", "").strip() == "NEEDS_REVIEW"]
    other_rows = [r for r in rows if r.get("review_status", "").strip() not in ("READY", "NEEDS_REVIEW")]

    def write(path, data):
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

    write(READY_OUT, ready_rows)
    write(REVIEW_OUT, review_rows)

    print(f"Total DRAFT rows: {len(rows)}")
    print(f"READY:        {len(ready_rows)} -> {READY_OUT}")
    print(f"NEEDS_REVIEW: {len(review_rows)} -> {REVIEW_OUT}")
    if other_rows:
        print(f"WARNING: {len(other_rows)} rows have an unexpected review_status value!")
        for r in other_rows[:3]:
            print(f"  sample: {r}")


if __name__ == "__main__":
    main()
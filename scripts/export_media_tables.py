"""Export derived medium tables to data/processed/conditions/."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.medium import export_media_tables, iter_implemented_media, wildtype_growth
import cobra

OUT = ROOT / "data" / "processed" / "conditions"
MODEL = ROOT / "models" / "paeruginosa_MODEL1507180020.xml"


def main():
    paths = export_media_tables(OUT)
    print("Wrote:")
    for k, p in paths.items():
        print(f"  {k}: {p}")

    model = cobra.io.read_sbml_model(str(MODEL))
    growth_rows = []
    for spec in iter_implemented_media():
        status, value = wildtype_growth(model, spec, quiet=True)
        growth_rows.append((spec.medium_id, spec.label, status, value))
        print(f"WT {spec.medium_id}: status={status} growth={value}")

    growth_path = OUT / "media_wt_growth.csv"
    with growth_path.open("w", encoding="utf-8") as f:
        f.write("medium_id,label,solver_status,wt_growth_per_h\n")
        for mid, label, status, value in growth_rows:
            f.write(f"{mid},{label},{status},{value}\n")
    print("Wrote", growth_path)


if __name__ == "__main__":
    main()

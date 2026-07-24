"""Run per-medium gene essentiality (no validation metrics).

Usage:
  C:/Users/pro/anaconda3/envs/reccobra39/python.exe scripts/run_condition_essentiality.py
  C:/Users/pro/anaconda3/envs/reccobra39/python.exe scripts/run_condition_essentiality.py --medium mops_pyruvate_lee2015
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import cobra

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.gene_essentiality import analyze_essentiality_for_medium, save_essentiality_results
from src.medium import iter_implemented_media

MODEL = ROOT / "models" / "paeruginosa_MODEL1507180020.xml"
OUT_DIR = ROOT / "results" / "essentiality"


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--medium", action="append", dest="media", default=None)
    parser.add_argument("--threshold", type=float, default=0.01)
    parser.add_argument("--processes", type=int, default=1)
    args = parser.parse_args(argv)

    media = args.media or [s.medium_id for s in iter_implemented_media()]
    model = cobra.io.read_sbml_model(str(MODEL))
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    summary_rows = []
    for mid in media:
        print(f"\n=== {mid} ===")
        df = analyze_essentiality_for_medium(
            model,
            mid,
            threshold_ratio=args.threshold,
            processes=args.processes,
        )
        out = OUT_DIR / f"gene_essentiality_{mid}.csv"
        save_essentiality_results(df, str(out), condition_name=mid)
        n_ess = int(df["is_essential"].sum())
        summary_rows.append(
            {
                "medium_id": mid,
                "threshold_ratio": args.threshold,
                "n_genes": len(df),
                "n_essential": n_ess,
                "wt_growth": float(df["wildtype_growth"].iloc[0]),
                "output_file": str(out.relative_to(ROOT)),
            }
        )
        print(f"  essential={n_ess}/{len(df)}  -> {out}")

    import pandas as pd

    summary = pd.DataFrame(summary_rows)
    summary_path = OUT_DIR / "condition_essentiality_summary.csv"
    summary.to_csv(summary_path, index=False)
    print(f"\nSummary -> {summary_path}")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()

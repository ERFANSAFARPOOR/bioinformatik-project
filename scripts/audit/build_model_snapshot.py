#!/usr/bin/env python
"""
A-01: Generate a machine-readable snapshot of the metabolic model.

Outputs
-------
model_audit_snapshot.json

This script is READ-ONLY with respect to the SBML model.
It extracts metadata useful for reproducibility and auditing.

Run under reccobra39.
"""

from pathlib import Path
import json

from cobra.io import read_sbml_model


ROOT = Path(__file__).resolve().parents[2]

MODEL = ROOT / "models" / "paeruginosa_MODEL1507180020.xml"
OUTPUT = ROOT /"project_management"/"audit"/"model_audit_snapshot.json"


def main():

    model = read_sbml_model(MODEL)

    solution = model.optimize()

    snapshot = {

        "model_file": MODEL.name,

        "model_id": model.id,
        "model_name": model.name,

        "strain": "PAO1",

        "n_reactions": len(model.reactions),
        "n_metabolites": len(model.metabolites),
        "n_genes": len(model.genes),

        "n_exchange_reactions": len(model.exchanges),
        "n_sink_reactions": len(model.sinks),
        "n_demand_reactions": len(model.demands),

        "objective_reactions": [
            r.id
            for r in model.reactions
            if r.objective_coefficient != 0
        ],

        "objective_direction": model.objective.direction,

        "default_growth_rate": solution.objective_value,
        "solver_status": solution.status,

        "compartments": dict(model.compartments),

        "genes_without_reactions":
            sum(
                len(g.reactions) == 0
                for g in model.genes
            ),

        "reactions_without_genes":
            sum(
                len(r.genes) == 0
                for r in model.reactions
            ),

        "metabolites_missing_formula":
            sum(
                not m.formula
                for m in model.metabolites
            ),

        "metabolites_missing_charge":
            sum(
                m.charge is None
                for m in model.metabolites
            ),

        "default_medium": dict(model.medium)

    }

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=2)

    print("=" * 60)
    print("MODEL SNAPSHOT")
    print("=" * 60)

    print(f"Model: {model.id}")
    print(f"Genes: {len(model.genes)}")
    print(f"Reactions: {len(model.reactions)}")
    print(f"Metabolites: {len(model.metabolites)}")
    print(f"Growth rate: {solution.objective_value:.6f}")
    print(f"Status: {solution.status}")
    print()
    print(f"Wrote: {OUTPUT}")


if __name__ == "__main__":
    main()
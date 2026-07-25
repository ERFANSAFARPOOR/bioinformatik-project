from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]

AUDIT = ROOT / "model_audit_snapshot.json"

data = json.loads(AUDIT.read_text(encoding="utf-8"))

keys = [
    "model_file",
    "model_id",
    "model_name",
    "strain",
    "n_reactions",
    "n_metabolites",
    "n_genes",
    "n_exchange_reactions",
    "n_demand_reactions",
    "n_sink_reactions",
    "objective_reactions",
    "objective_direction",
    "default_growth_rate",
    "solver_status",
    "default_medium",
    "compartments",
    "reactions_without_genes",
    "genes_without_reactions",
    "metabolites_missing_formula",
    "metabolites_missing_charge",
]

for key in keys:
    print(f"\n### {key} ###")
    print(json.dumps(data.get(key, "KEY NOT FOUND"), indent=2))
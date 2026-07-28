"""Read-only model audit for paeruginosa_MODEL1507180020.xml.

Does NOT modify the model file. Only reads and reports.
Run under the reccobra39 conda environment.
"""
import sys
import json
import hashlib
from pathlib import Path

import cobra
from cobra.io import read_sbml_model

ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = ROOT / "models" / "paeruginosa_MODEL1507180020.xml"
out = {}

# File hash (provenance, read-only)
h = hashlib.sha256(MODEL_PATH.read_bytes()).hexdigest()
out["file_sha256"] = h
out["file_size_bytes"] = MODEL_PATH.stat().st_size

# Read SBML doc-level info
import libsbml
doc = libsbml.readSBML(str(MODEL_PATH))
sb = doc.getModel()
out["sbml_level"] = doc.getLevel()
out["sbml_version"] = doc.getVersion()
out["sbml_model_id"] = sb.getId() if sb else None
out["sbml_model_name"] = sb.getName() if sb else None
npkg = doc.getNumPlugins() if hasattr(doc, "getNumPlugins") else None
out["fbc_plugin"] = sb.getPlugin("fbc") is not None if sb else None

model = read_sbml_model(str(MODEL_PATH))

out["model_id"] = model.id
out["model_name"] = model.name
out["n_reactions"] = len(model.reactions)
out["n_metabolites"] = len(model.metabolites)
out["n_genes"] = len(model.genes)
out["compartments"] = dict(model.compartments)
out["solver"] = str(type(model.solver)).split("'")[1]

# Objective
obj_rxns = [r.id for r in model.reactions if r.objective_coefficient != 0]
out["objective_reactions"] = obj_rxns
out["objective_expression"] = str(model.objective.expression)
out["objective_direction"] = model.objective.direction

# Biomass candidates
biomass = [r.id for r in model.reactions if "biomass" in r.id.lower() or "biomass" in (r.name or "").lower()]
out["biomass_candidates"] = biomass

# Exchange / transport / boundary
out["n_exchange"] = len(model.exchanges)
out["exchange_ids_sample"] = [r.id for r in model.exchanges][:25]
out["n_boundary"] = len(model.boundary)
sinks = [r.id for r in model.sinks]
demands = [r.id for r in model.demands]
out["n_sinks"] = len(sinks)
out["n_demands"] = len(demands)

# Reactions without genes
no_gene = [r.id for r in model.reactions if len(r.genes) == 0]
out["n_reactions_without_genes"] = len(no_gene)

# Genes without reactions
genes_no_rxn = [g.id for g in model.genes if len(g.reactions) == 0]
out["n_genes_without_reactions"] = len(genes_no_rxn)
out["genes_without_reactions_sample"] = genes_no_rxn[:20]

# Metabolite formula / charge missing
no_formula = [m.id for m in model.metabolites if not m.formula]
no_charge = [m.id for m in model.metabolites if m.charge is None]
out["n_metabolites_missing_formula"] = len(no_formula)
out["n_metabolites_missing_charge"] = len(no_charge)

# Mass / charge imbalance
mass_imbal = 0
charge_imbal = 0
imbal_examples = []
for r in model.reactions:
    if r in model.boundary:
        continue
    try:
        imb = r.check_mass_balance()
    except Exception:
        continue
    if imb:
        if "charge" in imb:
            charge_imbal += 1
        # any non-charge key => mass
        if any(k != "charge" for k in imb):
            mass_imbal += 1
        if len(imbal_examples) < 10:
            imbal_examples.append({r.id: {k: round(v, 4) for k, v in imb.items()}})
out["n_mass_imbalanced"] = mass_imbal
out["n_charge_imbalanced"] = charge_imbal
out["imbalance_examples"] = imbal_examples

# Gene ID samples (strain inference)
out["gene_id_sample"] = [g.id for g in model.genes][:30]
out["reaction_id_sample"] = [r.id for r in model.reactions][:20]
out["metabolite_id_sample"] = [m.id for m in model.metabolites][:20]

# Annotations on model
out["model_annotation"] = {k: (v if isinstance(v, str) else v) for k, v in model.annotation.items()}
# Sample gene annotations
gene_ann = {}
for g in list(model.genes)[:5]:
    gene_ann[g.id] = {"name": g.name, "annotation": dict(g.annotation)}
out["gene_annotation_sample"] = gene_ann
# Sample reaction annotation
rxn_ann = {}
for r in list(model.reactions)[:3]:
    rxn_ann[r.id] = dict(r.annotation)
out["reaction_annotation_sample"] = rxn_ann

# Feasible growth on default medium (read-only optimize on copy)
m2 = model.copy()
sol = m2.optimize()
out["default_objective_value"] = sol.objective_value
out["default_status"] = sol.status
out["default_medium"] = dict(model.medium)

# Blocked reactions & dead-end metabolites (can be slow; guard)
try:
    from cobra.flux_analysis import find_blocked_reactions
    blocked = find_blocked_reactions(model)
    out["n_blocked_reactions"] = len(blocked)
except Exception as e:
    out["n_blocked_reactions"] = f"ERROR: {e}"

# Dead-end metabolites: produced or consumed by only one reaction direction
deadends = []
for m in model.metabolites:
    rxns = m.reactions
    if len(rxns) <= 1:
        deadends.append(m.id)
out["n_deadend_metabolites_single_rxn"] = len(deadends)

# Duplicate IDs check
rxn_ids = [r.id for r in model.reactions]
met_ids = [m.id for m in model.metabolites]
gene_ids = [g.id for g in model.genes]
out["n_duplicate_reaction_ids"] = len(rxn_ids) - len(set(rxn_ids))
out["n_duplicate_metabolite_ids"] = len(met_ids) - len(set(met_ids))
out["n_duplicate_gene_ids"] = len(gene_ids) - len(set(gene_ids))

print(json.dumps(out, indent=2, default=str))

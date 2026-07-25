import json
ROOT =Path (__file__).resolve().parents[2]

raw = (ROOT / "reports/model_audit_clean.json").read_text(
    encoding="utf-8-sig"
)

start = raw.index('{')
d, _ = json.JSONDecoder().raw_decode(raw[start:])
keys = ['model_id','model_name','sbml_level','sbml_version','default_objective_value',
        'default_status','n_blocked_reactions','n_deadend_metabolites_single_rxn',
        'n_duplicate_reaction_ids','n_duplicate_metabolite_ids','n_duplicate_gene_ids',
        'n_demands','default_medium','gene_id_sample','reaction_id_sample',
        'metabolite_id_sample','model_annotation','gene_annotation_sample']
for k in keys:
    print('###', k, '###')
    print(json.dumps(d[k], indent=1, default=str))

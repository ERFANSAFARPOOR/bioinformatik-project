import pandas as pd

def clean(s):
    return str(s).strip("{}'\" ")

new = pd.read_csv('results/essentiality/gene_essentiality_default_medium.csv')
ref = pd.read_csv('data/processed/predicted_essentiality_default_medium.csv')
new_ess = set(new[new['is_essential']]['gene_id'].map(clean))
ref_ess = set(ref[ref['is_essential']]['gene_id'].astype(str))
lines = [
    f"regenerated rows/essential : {len(new)} / {int(new['is_essential'].sum())}",
    f"R-02 reference essential   : {len(ref_ess)}",
    f"essential-set identical    : {new_ess == ref_ess}",
    f"only in regenerated        : {sorted(new_ess - ref_ess)[:10]}",
    f"only in reference          : {sorted(ref_ess - new_ess)[:10]}",
    f"WT growth regenerated      : {round(float(new['wildtype_growth'].iloc[0]), 10)}",
    f"row order identical to ref : {list(new['gene_id'].map(clean)) == list(ref['gene_id'].astype(str))}",
]
print("\n".join(lines))

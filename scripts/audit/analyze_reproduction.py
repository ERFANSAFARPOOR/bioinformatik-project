"""Analyze reproduced notebooks for errors/warnings/version and compare the
regenerated essentiality CSV against the git-committed version."""
import json
import re
import subprocess
import io
from pathlib import Path
import pandas as pd

REPRO = Path("notebooks/reproduced")
nbs = ["01_basic_fba", "02_gene_essentiality", "03_experimental_comparison"]

print("=" * 70)
print("NOTEBOOK REPRODUCTION ANALYSIS (kernel: reccobra39 python3)")
print("=" * 70)
for stem in nbs:
    p = REPRO / f"{stem}.reproduced.ipynb"
    nb = json.loads(p.read_text(encoding="utf-8"))
    li = nb.get("metadata", {}).get("language_info", {})
    ks = nb.get("metadata", {}).get("kernelspec", {})
    n_err = 0
    err_summ = []
    warns = set()
    for i, c in enumerate(nb["cells"]):
        if c.get("cell_type") != "code":
            continue
        for o in c.get("outputs", []):
            if o.get("output_type") == "error":
                n_err += 1
                err_summ.append(f"cell{i}: {o.get('ename')}: {' '.join(o.get('evalue','').splitlines()[:1])}")
            if o.get("output_type") == "stream" and o.get("name") == "stderr":
                txt = "".join(o.get("text", []))
                for m in re.findall(r"(\w*Warning)", txt):
                    warns.add(m)
    print(f"\n### {stem}")
    print(f"  kernel/display : {ks.get('name')} / {ks.get('display_name')}")
    print(f"  python version : {li.get('version')}")
    print(f"  cell errors    : {n_err}")
    for e in err_summ:
        print("     -", e)
    print(f"  warning types  : {sorted(warns) if warns else 'none captured in nb'}")

# ---- CSV comparison: git-committed vs regenerated-on-disk ----
print("\n" + "=" * 70)
print("ESSENTIALITY CSV: committed (git) vs regenerated (this run)")
print("=" * 70)
csv_path = "results/essentiality/gene_essentiality_default_medium.csv"
committed = subprocess.run(["git", "show", f"HEAD:{csv_path}"],
                           capture_output=True, text=True)
df_git = pd.read_csv(io.StringIO(committed.stdout))
df_new = pd.read_csv(csv_path)

def clean(s):
    s = str(s)
    return s.strip("{}'\" ")

git_ess = set(df_git[df_git["is_essential"]]["gene_id"].map(clean))
new_ess = set(df_new[df_new["is_essential"]]["gene_id"].map(clean))
print(f"  committed: rows={len(df_git)}, essential={df_git['is_essential'].sum()}")
print(f"  regenerated: rows={len(df_new)}, essential={df_new['is_essential'].sum()}")
print(f"  essential-set identical: {git_ess == new_ess}")
print(f"  only in committed: {sorted(git_ess - new_ess)[:10]}")
print(f"  only in regenerated: {sorted(new_ess - git_ess)[:10]}")
# row order check
print(f"  row order identical: {list(df_git['gene_id']) == list(df_new['gene_id'])}")
# WT growth
print(f"  WT growth committed/new: {df_git['wildtype_growth'].iloc[0]:.10f} / {df_new['wildtype_growth'].iloc[0]:.10f}")

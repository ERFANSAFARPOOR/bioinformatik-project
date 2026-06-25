# Mock-input test harness for pre-tool-guard.ps1. Harmless; no real actions taken.
$guard = Join-Path $PSScriptRoot 'pre-tool-guard.ps1'

$cases = @(
    @{ name='git push (deny)';            json='{"tool_name":"PowerShell","tool_input":{"command":"git push origin develop"}}' },
    @{ name='git push --force (deny)';    json='{"tool_name":"Bash","tool_input":{"command":"git push --force origin main"}}' },
    @{ name='git reset --hard (deny)';    json='{"tool_name":"Bash","tool_input":{"command":"git reset --hard HEAD~1"}}' },
    @{ name='git clean -fdx (deny)';      json='{"tool_name":"Bash","tool_input":{"command":"git clean -fdx"}}' },
    @{ name='git remote set-url (deny)';  json='{"tool_name":"Bash","tool_input":{"command":"git remote set-url origin https://x"}}' },
    @{ name='git branch -D (deny)';       json='{"tool_name":"Bash","tool_input":{"command":"git branch -D develop"}}' },
    @{ name='git rebase (deny)';          json='{"tool_name":"Bash","tool_input":{"command":"git rebase -i HEAD~3"}}' },
    @{ name='edit raw SBML (deny)';       json='{"tool_name":"Edit","tool_input":{"file_path":"models/paeruginosa_MODEL1507180020.xml"}}' },
    @{ name='edit a PDF (deny)';          json='{"tool_name":"Write","tool_input":{"file_path":"conditian/juhas2015.pdf"}}' },
    @{ name='write outside repo (deny)';  json='{"tool_name":"Write","tool_input":{"file_path":"C:/Windows/Temp/x.txt"}}' },
    @{ name='read .env (deny)';           json='{"tool_name":"Bash","tool_input":{"command":"cat .env"}}' },
    @{ name='registry add (deny)';        json='{"tool_name":"PowerShell","tool_input":{"command":"reg add HKLM\\Software\\X /v Y"}}' },
    @{ name='format volume (deny)';       json='{"tool_name":"PowerShell","tool_input":{"command":"Format-Volume -DriveLetter D"}}' },
    @{ name='global pip install (ask)';   json='{"tool_name":"Bash","tool_input":{"command":"pip install seaborn"}}' },
    @{ name='rm -rf (ask)';               json='{"tool_name":"Bash","tool_input":{"command":"rm -rf build/"}}' },
    @{ name='conda -n env install (allow)';json='{"tool_name":"PowerShell","tool_input":{"command":"conda install -n reccobra39 matplotlib"}}' },
    @{ name='normal src write (allow)';   json='{"tool_name":"Write","tool_input":{"file_path":"src/new_util.py"}}' },
    @{ name='run notebook (allow)';       json='{"tool_name":"PowerShell","tool_input":{"command":"conda run -n reccobra39 jupyter nbconvert --execute notebooks/02_gene_essentiality.ipynb"}}' },
    @{ name='local commit (allow)';       json='{"tool_name":"Bash","tool_input":{"command":"git commit -m \"msg\""}}' }
)

foreach ($t in $cases) {
    $out = $t.json | powershell.exe -NoProfile -ExecutionPolicy Bypass -File $guard 2>&1
    $decision = 'allow'
    if ($out -match '"permissionDecision":"(\w+)"') { $decision = $Matches[1] }
    "{0,-32} => {1}" -f $t.name, $decision
}

<#
  PreToolUse guard for the P. aeruginosa metabolic-modeling project.

  Reads the hook JSON payload from stdin, inspects the proposed tool call, and
  returns a PreToolUse permission decision:
    deny  -> dangerous / irreversible / forbidden by project rules
    ask   -> requires explicit human approval
    allow -> (default) normal work; we emit nothing and let Claude proceed

  Decision is emitted as JSON (hookSpecificOutput.permissionDecision), the
  documented Claude Code mechanism. Exit code 0 always (the JSON carries the
  decision); on parse failure we fail OPEN (allow) so the guard never bricks the
  session, but we log the failure.

  Scope of protections (per project brief):
   - deletion outside project root / recursive destructive deletion / disk format
   - registry modification / credential access / reading .env or secret files
   - git reset --hard, git clean -fd[x], force push, branch deletion,
     history rewrite, remote changes, any push
   - modifying raw model or raw data files in place
   - global Python package installation
   - writing outside the repository
#>

$ErrorActionPreference = 'Stop'

# Project root = two levels up from this script (.claude/hooks/ -> repo)
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$RepoRootLower = $RepoRoot.ToLower().TrimEnd('\')

function Emit([string]$decision, [string]$reason) {
    $obj = @{
        hookSpecificOutput = @{
            hookEventName            = 'PreToolUse'
            permissionDecision       = $decision
            permissionDecisionReason = $reason
        }
    }
    $obj | ConvertTo-Json -Depth 6 -Compress
    exit 0
}

try {
    $raw = [Console]::In.ReadToEnd()
    if ([string]::IsNullOrWhiteSpace($raw)) { exit 0 }   # nothing to inspect -> allow
    $payload = $raw | ConvertFrom-Json
} catch {
    # Fail open but record it
    try {
        $logDir = Join-Path $RepoRoot '.claude\logs'
        if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Force -Path $logDir | Out-Null }
        Add-Content -Path (Join-Path $logDir 'guard-errors.log') -Value ("{0} PARSE_FAIL {1}" -f (Get-Date -Format o), $_.Exception.Message)
    } catch {}
    exit 0
}

$tool = [string]$payload.tool_name
$ti   = $payload.tool_input

# Gather the command text and/or target file path depending on tool
$cmd  = ''
$path = ''
switch -Regex ($tool) {
    '^(Bash|PowerShell)$'       { $cmd  = [string]$ti.command }
    '^(Write|Edit|NotebookEdit)$' { $path = [string]$ti.file_path; if (-not $path) { $path = [string]$ti.notebook_path } }
    default                      { $cmd = [string]$ti.command; $path = [string]$ti.file_path }
}

$c = $cmd.ToLower()

# ---- Helpers -------------------------------------------------------------
function PathIsInsideRepo([string]$p) {
    if ([string]::IsNullOrWhiteSpace($p)) { return $true }
    try {
        # Resolve relative to repo root; do not require existence
        if (-not [System.IO.Path]::IsPathRooted($p)) {
            $full = [System.IO.Path]::GetFullPath((Join-Path $RepoRoot $p))
        } else {
            $full = [System.IO.Path]::GetFullPath($p)
        }
        return $full.ToLower().StartsWith($RepoRootLower)
    } catch { return $true }  # unparsable -> don't block on path test alone
}

# ---- 1. DENY: destructive / irreversible / forbidden ---------------------

# Disk formatting
if ($c -match '\bformat-volume\b|\bmkfs\b|\bformat\s+[a-z]:|\bdiskpart\b|\bclear-disk\b') {
    Emit 'deny' 'Disk formatting / partition operations are prohibited.'
}

# Registry modification
if ($c -match '\breg(\.exe)?\s+(add|delete|import)\b|\bset-itemproperty\b.*hk(lm|cu|cr|u|cc):|\bnew-itemproperty\b.*hk(lm|cu):|\bremove-itemproperty\b.*hk(lm|cu):|\bremove-item\b.*hk(lm|cu):') {
    Emit 'deny' 'Windows registry modification is prohibited.'
}

# Credential / secret access
if ($c -match '\.credentials\b|get-credential\b|\bnetsh\s+wlan\s+show|cmdkey\b|\bsecrets?\.(json|yaml|yml|txt)\b') {
    Emit 'deny' 'Credential/secret access is prohibited.'
}
if ($c -match '(^|[\s/\\])\.env(\b|$)' -or ($path -match '(^|[\\/])\.env(\.|$)')) {
    Emit 'deny' 'Reading/writing .env or secret files is prohibited.'
}

# Git: history rewrite / hard reset / clean / force push / branch delete / remote change / push
if ($tool -match '^(Bash|PowerShell)$' -and $c -match '\bgit\b') {
    if ($c -match 'git\s+reset\s+.*--hard')                 { Emit 'deny' 'git reset --hard is prohibited (history/working-tree loss).' }
    if ($c -match 'git\s+clean\s+.*-[a-z]*f[a-z]*d')        { Emit 'deny' 'git clean -fd/-fdx is prohibited (untracked file loss).' }
    if ($c -match 'git\s+push\s+.*(--force|-f\b|--force-with-lease)') { Emit 'deny' 'Force push is prohibited.' }
    if ($c -match 'git\s+push\s+.*--delete|git\s+push\s+.*:\s*refs?/|git\s+branch\s+-d') { Emit 'deny' 'Deleting branches / remote refs is prohibited.' }
    if ($c -match 'git\s+(rebase|filter-branch|filter-repo|reflog\s+delete)')           { Emit 'deny' 'Rewriting git history is prohibited.' }
    if ($c -match 'git\s+remote\s+(add|remove|rm|set-url|rename)')                       { Emit 'deny' 'Changing git remotes is prohibited.' }
    if ($c -match 'git\s+push')                              { Emit 'deny' 'Pushing to any remote requires human approval and is blocked in autonomous mode.' }
}

# Recursive destructive deletion outside repo, or of protected raw assets
if ($c -match 'remove-item\b.*-recurse|rm\s+-rf|rm\s+-fr|rmdir\s+/s|del\s+/s|\brd\s+/s') {
    # Try to find a target path token
    if ($c -match 'remove-item\b.*-recurse' -and -not (PathIsInsideRepo $cmd)) {
        Emit 'deny' 'Recursive deletion outside the project root is prohibited.'
    }
    Emit 'ask' 'Recursive/forced deletion requested - requires explicit human approval.'
}

# Modifying RAW model / raw data / PDFs in place (deny edits; reading is fine)
if ($tool -match '^(Write|Edit|NotebookEdit)$' -and $path) {
    $pl = $path.ToLower() -replace '/', '\'
    if ($pl -match '(^|\\)models\\paeruginosa_model1507180020\.xml$' -or
        $pl -match '(^|\\)models\\raw\\' -or
        $pl -match '(^|\\)data\\raw\\' -or
        $pl -match '(^|\\)conditian\\' -or
        $pl -match '\.pdf$') {
        Emit 'deny' 'Raw model / raw data / PDF files are read-only and must not be edited in place (DECISIONS D-05).'
    }
    if (-not (PathIsInsideRepo $path)) {
        Emit 'deny' 'Writing outside the repository is prohibited.'
    }
}

# Shell writes/redirects targeting raw assets or outside repo
if ($tool -match '^(Bash|PowerShell)$') {
    if ($c -match 'paeruginosa_model1507180020\.xml' -and $c -match '>|set-content|out-file|add-content|write-sbml|tee-object') {
        Emit 'deny' 'Writing to the raw SBML model is prohibited (read-only).'
    }
}

# ---- 2. ASK: global Python package installation --------------------------
if ($tool -match '^(Bash|PowerShell)$') {
    # Allow env-scoped installs (conda -n <env>, pip inside an activated env / conda run -n)
    $isScoped = $c -match '(conda\s+(install|create|env)\s+.*(-n|--name)\s+\w)|(conda\s+run\s+-n\s+\w)|(pip\s+install\s+.*(-n|--name)\s+\w)'
    if ($c -match '\bpip(3)?\s+install\b' -and -not $isScoped) {
        # global/unscoped pip
        Emit 'ask' 'Global pip install detected. Install only into a project conda env (e.g. reccobra39); confirm before proceeding.'
    }
    if ($c -match 'conda\s+install' -and $c -match '(-n|--name)\s+base') {
        Emit 'ask' 'Installing into conda base is global-ish; confirm. Prefer reccobra39.'
    }
}

# Default: allow
exit 0

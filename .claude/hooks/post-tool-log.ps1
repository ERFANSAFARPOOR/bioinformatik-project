<#
  PostToolUse logger. Appends one JSON line per tool call to
  .claude/logs/tool-activity.log for an auditable trail of autonomous work.
  Never blocks; always exits 0. Truncates large command/inputs for readability.
#>
$ErrorActionPreference = 'SilentlyContinue'

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$logDir = Join-Path $RepoRoot '.claude\logs'
if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Force -Path $logDir | Out-Null }
$logFile = Join-Path $logDir 'tool-activity.log'

try {
    $raw = [Console]::In.ReadToEnd()
    if ([string]::IsNullOrWhiteSpace($raw)) { exit 0 }
    $p = $raw | ConvertFrom-Json

    $tool = [string]$p.tool_name
    $ti   = $p.tool_input
    $detail = ''
    if ($ti.command)       { $detail = [string]$ti.command }
    elseif ($ti.file_path) { $detail = [string]$ti.file_path }
    elseif ($ti.notebook_path) { $detail = [string]$ti.notebook_path }
    elseif ($ti.path)      { $detail = [string]$ti.path }
    if ($detail.Length -gt 300) { $detail = $detail.Substring(0,300) + '...[truncated]' }

    $entry = [ordered]@{
        ts       = (Get-Date -Format o)
        tool     = $tool
        detail   = $detail
        session  = [string]$p.session_id
    }
    Add-Content -Path $logFile -Value ($entry | ConvertTo-Json -Compress)
} catch {
    Add-Content -Path $logFile -Value ("{0} LOG_ERROR {1}" -f (Get-Date -Format o), $_.Exception.Message)
}
exit 0

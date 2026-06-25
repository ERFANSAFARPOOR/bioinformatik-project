# Hook test results

Tested with harmless mock JSON payloads via `.claude/hooks/test-guard.ps1`
(no real actions executed). Environment: Claude Code 2.1.185, Windows PowerShell.
Date: 2026-06-26.

## PreToolUse guard (`pre-tool-guard.ps1`) — 19/19 expected

| Mock input | Expected | Result |
|---|---|---|
| `git push origin develop` | deny | deny ✅ |
| `git push --force origin main` | deny | deny ✅ |
| `git reset --hard HEAD~1` | deny | deny ✅ |
| `git clean -fdx` | deny | deny ✅ |
| `git remote set-url origin …` | deny | deny ✅ |
| `git branch -D develop` | deny | deny ✅ |
| `git rebase -i HEAD~3` | deny | deny ✅ |
| Edit `models/paeruginosa_MODEL1507180020.xml` | deny | deny ✅ |
| Write `conditian/juhas2015.pdf` | deny | deny ✅ |
| Write `C:/Windows/Temp/x.txt` (outside repo) | deny | deny ✅ |
| `cat .env` | deny | deny ✅ |
| `reg add HKLM\Software\X /v Y` | deny | deny ✅ |
| `Format-Volume -DriveLetter D` | deny | deny ✅ |
| `pip install seaborn` (global) | ask | ask ✅ |
| `rm -rf build/` | ask | ask ✅ |
| `conda install -n reccobra39 matplotlib` | allow | allow ✅ |
| Write `src/new_util.py` | allow | allow ✅ |
| `jupyter nbconvert --execute notebooks/02…` | allow | allow ✅ |
| `git commit -m "msg"` | allow | allow ✅ |

## PostToolUse logger (`post-tool-log.ps1`)
Appends one compact JSON line per call to `.claude/logs/tool-activity.log`.
Verified: a mock call produced
`{"ts":"…","tool":"PowerShell","detail":"echo test","session":"mock-session"}`.

## Notes / limitations
- The guard **fails open** (allow) on unparsable payloads, logging to
  `.claude/logs/guard-errors.log`, so it can never brick the session.
- Decisions are emitted as `hookSpecificOutput.permissionDecision`
  (`deny`/`ask`/`allow`) per the Claude Code PreToolUse schema.
- `bypassPermissions` mode is intentionally NOT used.
- Re-run tests anytime: `powershell -File .claude/hooks/test-guard.ps1`.

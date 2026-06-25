---
name: publication-readiness
description: Drive the repo and manuscript to a reproducible, publishable state — structure migration, env locking, tests, provenance, licensing, and final audit. Trigger when asked to prepare for publication/submission, finalize the repo, or do a release/readiness check.
---

# Publication readiness

## Trigger
Asked to prepare for journal submission or public release, finalize/clean the
repository, lock the environment, or run a final readiness audit.

## Inputs
- All audit/governance docs (`PROJECT_AUDIT.md`, `TODO.md`, `BLOCKERS.md`, …)
- `REPOSITORY_MIGRATION_PLAN.md`, `PUBLICATION_PLAN.md`
- Validated results, figures, evidence/mapping tables, env files

## Ordered workflow
1. Confirm all gating blockers closed (real labels, validated mappings, cited
   media, verified citations, notebooks reproduce under locked env, model license).
2. Execute the migration map (`git mv`, preserve history); update path references;
   re-run tests after each move.
3. Lock environment (`environment.yml` / `requirements-lock.txt`) only after
   reproduction is confirmed.
4. Add `tests/` pinning key numbers; ensure `pytest` green under reccobra39.
5. Scrub for secrets, `.env`, large archives, caches, checkpoints; verify
   `.gitignore`. Add `LICENSE`, `CITATION.cff`; confirm model redistribution terms.
6. Finalize README/manuscript; ensure every figure/metric traces to script+data.
7. Final read-only audit; produce a readiness checklist.

## Validation requirements
- Fresh clone + locked env reproduces the headline results.
- No fabricated/placeholder result remains; no uncited value.
- No secrets/large binaries tracked; raw files unchanged.

## Prohibited behavior
- Pushing/publishing without explicit human approval.
- Locking the env before reproduction is confirmed.
- Shipping placeholder metrics or unverified citations.
- `bypassPermissions` mode.

## Expected outputs
Migrated structure, locked env, passing tests, LICENSE/CITATION, finalized
README/manuscript, and a final readiness audit — pending human approval to push.

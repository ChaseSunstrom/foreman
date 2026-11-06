---
id: T-0402
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T04:00:45Z
updated: 2026-10-09T04:01:54Z
base: 94f2f487d4fa7c569cc6d09eb58aae858db1e53e
base_tree: e655d2a0ab7e7d8d86e6d2a0e56cc53f1e2f9b46
verified: strong
---
# Foreman 1.2.9: the drive offers queued work during background jobs (T-0401) to GitHub main and JARVIS
## Raw request
> Foreman 1.2.9: the drive offers queued work during background jobs (T-0401) to GitHub main and JARVIS
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] origin/main contains HEAD — verify with `git -C ~/.claude/foreman merge-base --is-ancestor HEAD origin/main`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] bump, gate, commit
2. [x] merge in a scratch clone, push; fast-forward JARVIS
## Resume here
## Docs impact
## Verification evidence
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (28 pass, 3 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · skipped: nothing under plugin/lib/**, plugin/hooks/**, plugin/bin/**, plugin/tests/bench_hooks.py, plugin/tests/fixtures/** changed since its pass at 04:00 UTC; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 00:30 UTC; pytho [ran] [tree c7eb46d24903] (2026-10-09T04:01:35Z)
- (step 2) `git -C ~/.claude/foreman merge-base --is-ancestor HEAD origin/main` → exit 0 · (no output) [ran] [tree c7eb46d24903] (2026-10-09T04:01:54Z)
- (ac 1) `git -C ~/.claude/foreman merge-base --is-ancestor HEAD origin/main` → exit 0 · (no output) [ran] [tree c7eb46d24903] (2026-10-09T04:01:54Z)
- (audit intent) `self: gate green; pushed to main; JARVIS fast-forwarded from a clean tree, install updated` → main and JARVIS carry 1.2.9 [tree c7eb46d24903] (2026-10-09T04:01:54Z)
- (audit self) `self: gate green; pushed to main; JARVIS fast-forwarded from a clean tree, install updated` → no findings [tree c7eb46d24903] (2026-10-09T04:01:54Z)
## Log
- 2026-10-09T04:00:45Z created
- 2026-10-09T04:00:46Z focused
- 2026-10-09T04:01:54Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0401 [FIX M, done, 3 steps] Drive: while background work runs, name a concrete queued task to start (builder lane / plan / block), offer up to 3 in turn, then wait — J…
- decision 2026-10-09: [outward] Updating Foreman on JARVIS (merge to main, pull, plugin update, reload) as fixes land during the monitoring
- T-0396 [FIX S, done, 2 steps] Foreman 1.2.6: the merge and pipe-shell refusal hints (T-0394, T-0395) to GitHub main and JARVIS
- T-0400 [FIX S, done, 2 steps] Foreman 1.2.8: builder briefs say edit with Edit/Write (T-0399) to GitHub main and JARVIS
- similar finished tasks took 2–3 steps
- start here (files T-0401 touched): plugin/tests/test_hooks.py, plugin/lib/fmhooks.py, CHANGELOG.md
## Regression test
none: a release; the gate ran the full suite on the released tree
## Files touched
- .claude-plugin/marketplace.json
- CHANGELOG.md
- plugin/.claude-plugin/plugin.json

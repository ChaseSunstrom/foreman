---
id: T-0410
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T04:35:02Z
updated: 2026-10-09T04:36:11Z
base: 9ed87a72b75040ae05f3b6c1ae81b27f7fb89ec9
base_tree: 484c23a2ef98e747acf7f9b32a151dc5302f5baa
verified: strong
---
# Foreman 1.2.12: lane rm tool caches, brief refusal names the task to resume (T-0408, T-0409) to GitHub main and JARVIS
## Raw request
> Foreman 1.2.12: lane rm tool caches, brief refusal names the task to resume (T-0408, T-0409) to GitHub main and JARVIS
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
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (28 pass, 3 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · skipped: nothing under plugin/lib/**, plugin/hooks/**, plugin/bin/**, plugin/tests/bench_hooks.py, plugin/tests/fixtures/** changed since its pass at 04:35 UTC; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 00:30 UTC; pytho [ran] [tree d7e892160c01] (2026-10-09T04:35:57Z)
- (step 2) `git -C ~/.claude/foreman merge-base --is-ancestor HEAD origin/main` → exit 0 · (no output) [ran] [tree d7e892160c01] (2026-10-09T04:36:11Z)
- (ac 1) `git -C ~/.claude/foreman merge-base --is-ancestor HEAD origin/main` → exit 0 · (no output) [ran] [tree d7e892160c01] (2026-10-09T04:36:11Z)
- (audit intent) `self: gate green; pushed to main; JARVIS fast-forwarded from a clean tree, install updated` → main and JARVIS carry 1.2.12 [tree d7e892160c01] (2026-10-09T04:36:11Z)
- (audit self) `self: gate green; pushed to main; JARVIS fast-forwarded from a clean tree, install updated` → no findings [tree d7e892160c01] (2026-10-09T04:36:11Z)
## Log
- 2026-10-09T04:35:02Z created
- 2026-10-09T04:35:02Z focused
- 2026-10-09T04:36:11Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0409 [CLEAN S, done, 1 steps] A 'no active task' refusal should name the queued task to resume (JARVIS edited between closing a lane task and refocusing T-0278; the re…
- T-0405 [FIX S, done, 2 steps] Foreman 1.2.10: lane merge beside uncommitted work, focus-in-the-line hint (T-0403, T-0404) to GitHub main and JARVIS
- T-0379 [FIX S, done, 1 steps] Builder brief: start from the main checkout's commit; isolation refusals are reported for the main thread, not retried — lesson: Watch the …
- decision 2026-10-09: [outward] Updating Foreman on JARVIS (merge to main, pull, plugin update, reload) as fixes land during the monitoring
- similar finished tasks took 1–2 steps
## Regression test
none: a release; the gate ran the full suite on the released tree
## Files touched
- .claude-plugin/marketplace.json
- CHANGELOG.md
- plugin/.claude-plugin/plugin.json

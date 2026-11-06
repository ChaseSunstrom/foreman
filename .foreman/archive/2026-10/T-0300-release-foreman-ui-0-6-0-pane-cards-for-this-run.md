---
id: T-0300
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-04T09:58:23Z
updated: 2026-10-04T13:17:01Z
base: 1dbf080e3e3593cf664278aa126fcc9dfb4e68af
base_tree: 06faac1f96ed6335734460b760243e40e31b504d
verified: strong
---
# Release foreman-ui 0.6.0 (pane cards for this run's features)
## Raw request
> Release foreman-ui 0.6.0 (pane cards for this run's features)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] plugin.json and marketplace.json say 0.6.0 and the mod tests pass — verify with `grep -q '"version": "0.6.0"' mods/foreman-ui/.claude-plugin/plugin.json && grep -q '"version": "0.6.0"' .claude-plugin/marketplace.json`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] bump both versions and add a CHANGELOG line
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `grep -q '"version": "0.6.0"' mods/foreman-ui/.claude-plugin/plugin.json && grep -q '"version": "0.6.0"' .claude-plugin/marketplace.json` → ✗ exit 1 · (no output) [ran] [tree 06faac1f96ed] (2026-10-04T09:58:27Z)
- (step 1) `grep -q '"version": "0.6.0"' mods/foreman-ui/.claude-plugin/plugin.json && grep -q '"version": "0.6.0"' .claude-plugin/marketplace.json` → exit 0 · (no output) [ran] [tree 0843e961f626] (2026-10-04T09:58:33Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (26 pass, 3 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · skipped: nothing under plugin/**, install.sh changed since its pass at 09:56 UTC; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · skipped: nothing under plugin/lib/**, plugin/hooks/**, plugin/bin/**, plugin/tests/bench_hooks.py, plugin/tests/fixtures/** changed since its pass at 09:56 UTC; claude plugin test mods/foreman-ui → exit 0 · 0 fail / Ran 62 tests across 1 file. [2.68s]; python3 plugin/tests/run.py [ran] [tree 0843e961f626] (2026-10-04T09:59:18Z)
- (ac 1) `grep -q '"version": "0.6.0"' mods/foreman-ui/.claude-plugin/plugin.json && grep -q '"version": "0.6.0"' .claude-plugin/marketplace.json` → exit 0 · (no output) [ran] [tree 0843e961f626] (2026-10-04T09:59:22Z)
- (audit intent) `self: version strings only; mod tests 62/62 and fm check pass; the release's content was reviewed in its own tasks (T-0228, T-0280)` → doctor's release warning asked for a version bump so other sessions draw the new UI; both manifests now say 0.6.0 [tree 0843e961f626] (2026-10-04T09:59:22Z)
- (audit self) `self: version strings only; mod tests 62/62 and fm check pass; the release's content was reviewed in its own tasks (T-0228, T-0280)` → no findings [tree 0843e961f626] (2026-10-04T09:59:22Z)
## Log
- 2026-10-04T09:58:23Z created
- 2026-10-04T09:58:23Z focused
- 2026-10-04T09:59:22Z done
- 2026-10-04T09:59:22Z committed 83473c5 (3 path(s))
- 2026-10-04T13:17:01Z user approved plugin in Claude Code's permission prompt
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0228 [FEATURE M, done, 3 steps] foreman-ui catch-up: budget, bench and evolve, research asks, and the task's hypotheses, oracle and batch in the pane — lesson: Look at…
- T-0146 [FEATURE M, done, 3 steps] Dashboard: no duplicates between band and pane, nothing stale or cut without saying so, controls that read as actions — lesson: Record …
- T-0092 [FEATURE L, done, 8 steps] Polished, animated Foreman UI: clean statusline, card band and pane, animated tool/edit/subagent rows, spinner with the Foreman step — …
- T-0117 [FEATURE S, done, 2 steps] While-you-were-away row: what drive finished since the user's last message
- similar finished tasks took 2–8 steps
## Lessons
- Bump the mod's version in the same batch that changes its code; doctor flags the lag, but only after the fact
## Files touched
- mods/foreman-ui/.claude-plugin/plugin.json
- .claude-plugin/marketplace.json
- CHANGELOG.md

---
id: T-1299
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-20T21:55:33Z
updated: 2026-10-20T23:48:22Z
base: 14074119762defc0cc38eb3f66fb7129ed5b59ad
base_tree: b7222a43a4216ced9c6f257890f1973ee0f2bc21
plan0_at: 2026-10-20T21:55:34Z
plan0_scope: []
paused_tree: 8aff572e5ca6ce3d09383c42e551d64ea75e421e
verified: strong
---
# Release 1.2.44: fm code bench, worker leases fixed, macOS CI fixes, run.py unknown names, research --append, guard hints, stack cards, landing theme
## Raw request
> Release 1.2.44: fm code bench, worker leases fixed, macOS CI fixes, run.py unknown names, research --append, guard hints, stack cards, landing theme
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] origin's main is the 'Foreman 1.2.44' release commit — verify with `git log origin/main --oneline -1`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] fm release 1.2.44 --push
## Resume here
<!-- auto -->
- 2026-10-20T23:34:12Z step 1/1: fm release 1.2.44 --push
- git: foreman/build; 0 uncommitted
## Docs impact
CHANGELOG (the release section)
## Verification evidence
- (step 1) `git log origin/main --oneline -1` → exit 0 · 61ca7a9d Foreman 1.2.44 [ran] [tree 95b6dc7c507f] (2026-10-20T23:45:57Z)
- (ac 1) `git log origin/main --oneline -1` → exit 0 · 61ca7a9d Foreman 1.2.44 [ran] [tree 95b6dc7c507f] (2026-10-20T23:45:58Z)
- (ac 1) `git log origin/main --oneline -1` → exit 0 · 61ca7a9d Foreman 1.2.44 [ran] [tree 455d0f64a9a4] (2026-10-20T23:46:11Z)
- (audit intent) `fm release ran fm check, release-check and the canary, merged into main and pushed; origin/main is Foreman 1.2.44` → 1.2.44 carries fm code bench, the worker lease fix, macOS CI fixes, run.py unknown names, research --append, guard hints, stack cards, the landing theme [tree 455d0f64a9a4] (2026-10-20T23:46:11Z)
- (audit operator) `fm release ran fm check, release-check and the canary, merged into main and pushed; origin/main is Foreman 1.2.44` → CI runs on the push; T-1284 closes when the macOS job is green [tree 455d0f64a9a4] (2026-10-20T23:46:11Z)
- (audit self) `fm release ran fm check, release-check and the canary, merged into main and pushed; origin/main is Foreman 1.2.44` → no findings [tree 455d0f64a9a4] (2026-10-20T23:46:11Z)
## Log
- 2026-10-20T21:55:33Z created
- 2026-10-20T21:55:33Z focused
- 2026-10-20T23:27:41Z user approved publish in Claude Code's permission prompt
- 2026-10-20T23:27:41Z undo point at this yes for publish: HEAD 14074119762d
- 2026-10-20T23:28:04Z publish grant used by fm release --push
- 2026-10-20T23:34:14Z paused: focus moved to T-1300
- 2026-10-20T23:48:22Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1294 [FIX M, done, 3 steps] fm code --worker: a worker's own edits count as the run's for Foreman leases, so the judge keeps them and the next turn can edit the same c…
- T-1215 [FEATURE M, done, 3 steps] fm code bench: grade any model or worker as a Foreman worker on seeded tasks — lesson: A bench must grade what the harness can check it…
- T-1072 [CLEAN M, done, 2 steps] Rule and hint hygiene: cards, known fixes, rules and lessons that never fired or never hel — lesson: A cleanup that deletes what users ta…
- decision 2026-10-20: Slate, round 1: T-1254 cost per fully-correct session on the Benchmarks page; T-1255 the Claude Code version in every bench result; T-1256 piped tes…
## Lessons
- none: a routine release
## Files touched
- .claude-plugin/marketplace.json
- CHANGELOG.md
- MASTER.md
- plugin/.claude-plugin/plugin.json
- plugin/lib/fmcli.py
- plugin/lib/fmcodeterm.py
- plugin/lib/fmcodetui.py
- plugin/tests/test_code_tui.py

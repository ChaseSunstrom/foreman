---
id: T-2091
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmtidy.py, plugin/tests/test_tidy.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: discovered
created: 2026-10-30T04:00:38Z
updated: 2026-10-30T13:35:46Z
base: 6b506e558839ef8165d33b0163417a721c79f5af
base_tree: 6beb224254e919e1289cd3339194ae162477800b
plan0_at: 2026-10-30T13:30:00Z
plan0_scope: [plugin/lib/fmtidy.py, plugin/tests/test_tidy.py, CHANGELOG.md, MASTER.md]
verified: strong
---
# fm tidy: drop a project state dir whose root folder is gone (throwaway temp projects…
## Raw request
> fm tidy: drop a project state dir whose root folder is gone (throwaway temp projects like a manual fm exam trial leave one under state/projects)
## Interpretation
fm tidy finds project state dirs (state/projects/<slug>) whose meta.json root folder no longer exists. Root under a temp dir (/tmp, /var/tmp, tempfile.gettempdir()): an APPLY item that moves the whole dir to state/archive/projects/<slug> on --apply (reversible, nothing deleted). Root elsewhere (an unplugged disk, a moved repo): a DECIDE item only, never moved.
## Assumptions (confidence)
## Acceptance criteria
- [x] a temp-rooted dead project is archived on --apply, a non-temp one is only reported, a live one untouched — verify with `python3 plugin/tests/run.py test_tidy`
## Non-goals
## Approach (options → choice → why)
Options: delete dead dirs (irreversible, rejected); archive every dead dir (wrong for an unmounted drive); archive temp-rooted only, report the rest (chosen: the throwaway case the request names, safe for the rest). Lives in check_global, since a dead project is never the resolved one.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test in test_tidy for dead_project (temp archived, non-temp reported, live kept)
2. [x] dead_project check in fmtidy.check_global; CHANGELOG + MASTER tidy line
## Resume here
## Docs impact
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_tidy 2>&1 | tail -15` → ✗ exit 1 · Ran 37 tests in 20.6s (13 classes, 16 at a time; slowest: DeferredTriage 20s, StalePlans 18s, DecisionSunset 14s) / FAILED (1 classes) [ran] [tree 5be6e0a89f93] (2026-10-30T13:30:54Z)
- (step 1) `python3 plugin/tests/run.py test_tidy` → exit 0 · Ran 37 tests in 9.1s (13 classes, 16 at a time; slowest: DeferredTriage 9s, StalePlans 8s, DecisionSunset 6s) / OK [ran] [tree 9df38fc32193] (2026-10-30T13:32:07Z)
- (step 2) `fm docs` → exit 0 · No doc drift in ~/.claude/foreman. [ran] [tree 9df38fc32193] (2026-10-30T13:32:07Z)
- (ac 1) `python3 plugin/tests/run.py test_tidy` → exit 0 · Ran 37 tests in 9.2s (13 classes, 16 at a time; slowest: DeferredTriage 9s, StalePlans 8s, DecisionSunset 6s) / OK [ran] [tree 9df38fc32193] (2026-10-30T13:32:16Z)
- `python3 plugin/tests/run.py test_tidy` → ✗ exit 1 · Ran 37 tests in 9.9s (13 classes, 16 at a time; slowest: DeferredTriage 9s, StalePlans 8s, DecisionSunset 7s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 9df38fc32193] (2026-10-30T13:32:36Z)
- `python3 plugin/tests/run.py test_tidy` → exit 0 · Ran 37 tests in 9.2s (13 classes, 16 at a time; slowest: DeferredTriage 9s, StalePlans 8s, DecisionSunset 6s) / OK [ran] [tree 9df38fc32193] (2026-10-30T13:32:36Z)
- (ac 1) `python3 plugin/tests/run.py test_tidy` → exit 0 · Ran 37 tests in 9.1s (13 classes, 16 at a time; slowest: DeferredTriage 9s, StalePlans 8s, DecisionSunset 6s) / OK [ran] [tree 9df38fc32193] (2026-10-30T13:32:53Z)
- (audit edge) `self: read the diff; dry run on real state lists 10 temp-rooted dead projects as APPLY and foreman-improve-20260927 (under home) as DECIDE; only a manual fm tidy --apply moves anything (fm night runs --lanes-only)` → realpath+commonpath for the temp test (a /tmp symlink resolves); an archive name already taken gets a timestamp; a concurrent tidy that moved it first is skipped; the root path is c.plain'd in the finding; nothing is deleted [tree 9df38fc32193] (2026-10-30T13:32:53Z)
- (audit self) `self: read the diff; dry run on real state lists 10 temp-rooted dead projects as APPLY and foreman-improve-20260927 (under home) as DECIDE; only a manual fm tidy --apply moves anything (fm night runs --lanes-only)` → no findings [tree 9df38fc32193] (2026-10-30T13:32:53Z)
## Log
- 2026-10-30T04:00:38Z created
- 2026-10-30T13:29:57Z set type=FEATURE, tier=S, scope=['plugin/lib/fmtidy.py', 'plugin/tests/test_tidy.py', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-30T13:29:58Z planned: it has criteria and steps
- 2026-10-30T13:29:59Z focused
- 2026-10-30T13:33:05Z done
- 2026-10-30T13:33:06Z committed f0850f6a (4 files)
- 2026-10-30T13:33:28Z guard authorization added: publish
- 2026-10-30T13:35:46Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1077-review: Verdict: approve with nits** (one MEDIUM to fix before merge). [stale: plugin/lib/fmtidy.py changed since it was written]
- research wave1-plan-ac858e27ec64c546f: === T-1077 [stale: plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmcost.py changed since it was written]
- T-1669 [FEATURE M, done, 4 steps] Fm drill: compound fault days in a temp home, promotion by false-positive rate (from T-155 — lesson: A corrupt meta.json hides its proj…
- decision 2026-10-30: Genesis select: gen N's bar is gen N-1's exam line even when gen N-1's text was reverted
- similar past tasks were M: consider --tier M
- the similar finished task took 4 steps
- likely tests for the scope: plugin/tests/test_tidy.py
## Preflight
Changed in scope since this was planned (2026-10-30): CHANGELOG.md, MASTER.md, plugin/lib/fmtidy.py; re-ground the plan against them before editing
## Files touched
- plugin/tests/test_tidy.py
- plugin/lib/fmtidy.py
- CHANGELOG.md
- MASTER.md

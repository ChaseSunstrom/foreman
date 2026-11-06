---
id: T-1048
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmtidy.py, plugin/lib/fmcost.py, plugin/tests/test_tidy.py]
depends_on: []
source: followup
created: 2026-10-16T03:42:10Z
updated: 2026-10-16T06:25:12Z
base: 9461f65be1e6180a48a01e79d969c09dfb443702
base_tree: b6821c60fbf43748b0bb8a90bd3f301272c06c36
verified: strong
---
# Deferred-work triage in fm digest and fm tidy: each deferred item proposed as drop, do or
## Raw request
> Deferred-work triage in fm digest and fm tidy: each deferred item proposed as drop, do or ask by age and evidence (T-1029 C16)
## Interpretation
Each deferred brief gets a proposal in `fm digest` and `fm tidy`: drop, do, or ask. "do" means the `--until` date or file change has come, or its scope is untouched and it is young. "drop" means it is old (90+ days) with no activity and no evidence, such as a dead scope file. "ask" is the rest. Nothing is applied. `deferral_due` (fmcore.py:2312) and the next-action hint (fmcore.py:2451) cover the "due back" case only.
## Assumptions (confidence)
## Acceptance criteria
- [x] A 120-day-old deferred brief with a missing scope file shows "drop"; one that is due shows "do"; the rest show "ask". — verify with `python3 plugin/tests/run.py test_tidy`
## Non-goals
## Approach (options → choice → why)
(a) rules in `fmcore`, (b) a function in fmtidy, (c) an LLM triage. Choice is (b), deterministic and cheap. Add `triage_deferred(p, briefs)` to fmtidy.py. It returns [(id, verdict, why)] using `c.age_days(updated)`, `deferral_due(revisit)`, and scope file existence. `check_project` emits a `deferred_triage` finding of severity info or warn, with the verdict in the fix column (`fm task drop ID "<why>"`). `cmd_digest` prints "Deferred: T-x → drop (why)".
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: build deferred briefs with a back-dated `updated` field, one with `revisit` set to a past date, and one with a missing scope file. Assert the verdict words in `fm tidy` output and in `fm digest --json["deferred_triage"]`. Assert no status changes.
2. [x] Implement `triage_deferred`, call it from `check_project` and `cmd_digest`.
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_tidy` → ✗ exit 1 · Ran 22 tests in 3.9s (10 classes, 16 at a time; slowest: StalePlans 4s, Apply 3s, TidyHygiene 3s) / FAILED (1 classes) [ran] [tree 995a7cc7af38] (2026-10-16T06:13:20Z)
- (step 2) `python3 plugin/tests/run.py test_tidy` → exit 0 · Ran 22 tests in 3.7s (10 classes, 16 at a time; slowest: StalePlans 3s, Apply 3s, TidyHygiene 3s) / OK [ran] [tree 4a7f340e43a2] (2026-10-16T06:13:41Z)
- (step 2) `python3 plugin/tests/run.py test_tidy` → exit 0 · Ran 22 tests in 3.0s (10 classes, 16 at a time; slowest: StalePlans 3s, Apply 3s, TidyHygiene 2s) / OK [ran] [tree 33f1d4a4c89c] (2026-10-16T06:14:25Z)
- (step 2) `python3 plugin/tests/run.py test_tidy` → exit 0 · Ran 23 tests in 4.1s (10 classes, 16 at a time; slowest: StalePlans 4s, DeferredTriage 4s, Apply 3s) / OK [ran] [tree 925a2d60c9e6] (2026-10-16T06:21:25Z)
- (ac 1) `python3 plugin/tests/run.py test_tidy` → exit 0 · Ran 23 tests in 3.0s (10 classes, 16 at a time; slowest: StalePlans 3s, DeferredTriage 3s, Apply 3s) / OK [ran] [tree 4d3e21e41228] (2026-10-16T06:24:37Z)
- (audit self) `review: one fm-reviewer pass (combined with T-1082/T-1120); the builder fixed the medium (a never-committed scope file reads ask, not gone) and both lows (live globs, do/drop first, asks collapsed) test-first, plus edge tests (no scope, future revisit, 89/91-day boundary, when-PATH-changes)` → no findings [tree 4d3e21e41228] (2026-10-16T06:24:37Z)
## Log
- 2026-10-16T03:42:10Z created
- 2026-10-16T04:22:45Z set scope=['plugin/lib/fmtidy.py', 'plugin/lib/fmcost.py', 'plugin/tests/test_tidy.py']
- 2026-10-16T04:22:46Z set tier=S
- 2026-10-16T06:12:45Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1048.builder.md
- 2026-10-16T06:12:52Z focused
- 2026-10-16T06:24:25Z merged worktree-agent-ac10a6a97f6495b47 (3 file(s))
- 2026-10-16T06:24:25Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ac10a6a97f6495b47
- 2026-10-16T06:24:25Z focused
- 2026-10-16T06:24:34Z scope: CHANGELOG.md — release note
- 2026-10-16T06:25:11Z done
- 2026-10-16T06:25:12Z committed a9e97be (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research wave1-plan-ac858e27ec64c546f: === T-1077 [stale: plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmcost.py changed since it was written]
- T-1077 [CLEAN S, done, 3 steps] Stale plan sweep: queued briefs whose files or premises changed since planning are flagged — lesson: A freshness check on files must use …
- T-1072 [CLEAN M, done, 2 steps] Rule and hint hygiene: cards, known fixes, rules and lessons that never fired or never hel — lesson: A cleanup that deletes what users ta…
- decision 2026-10-04: Landscape 2026-10-04 grounded: no new work
- similar finished tasks took 2–3 steps
- start here (files T-1077 touched): plugin/tests/test_tidy.py, plugin/lib/fmtidy.py, plugin/lib/fmcost.py, CHANGELOG.md
- likely tests for the scope: plugin/tests/test_tidy.py
## Preflight
Changed in scope since this was planned (2026-10-16): plugin/lib/fmcost.py, plugin/lib/fmtidy.py, plugin/tests/test_tidy.py; re-ground the plan against them before editing
## Lessons
- 'Gone' needs history: a file that never existed is one a plan will create, not one it lost
## Plan gaps
- failed first: step 1 Failing tests: build deferred briefs with a back-dated `updated` field, one with `revisit` set to a…
## Files touched
- plugin/tests/test_tidy.py
- plugin/lib/fmtidy.py
- plugin/lib/fmcost.py
- CHANGELOG.md

---
id: T-1135
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/tests/test_cli.py, plugin/tests/test_ambient.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: followup
created: 2026-10-16T08:52:15Z
updated: 2026-10-16T09:34:35Z
base: 4717db9c0f8ec2e344cf07ea8c68881265a5db0b
base_tree: ba3a4797054ff8d4b8220194d85891a5549c4a8e
plan0_at: 2026-10-16T09:22:49Z
plan0_scope: [plugin/lib/fmcli.py, plugin/tests/test_cli.py, plugin/tests/test_ambient.py, CHANGELOG.md, MASTER.md]
verified: strong
---
# Per-runner affected templates: a project with two test runners (Python run.py and the mod'
## Raw request
> Per-runner affected templates: a project with two test runners (Python run.py and the mod's claude plugin test) gets one fm check affected command per test-file extension, so a changed .tsx test runs at close too (follow-up of T-1131)
## Interpretation
A project with two test runners (Python's run.py and the mod's 'claude plugin test') gets one fm check affected command per test-file extension, so changed .tsx tests run at close and in fm check --affected too, not only the Python ones.
## Assumptions (confidence)
## Acceptance criteria
- [x] with a Python default and '--for .tsx' set, a change touching a .py test and a .tsx test runs both commands; with only the default, behaviour is unchanged — verify with `python3 plugin/tests/run.py test_cli test_ambient`
## Non-goals
## Approach (options → choice → why)
meta.affected stays the default template. A new meta.affected_by (extension → template) is set with 'fm check affected --for .tsx "<cmd>"'. affected() groups tests by extension, builds one command per group (a template without {tests}/{names} runs once whenever any test of its group changed), and joins them with ' && '. Callers keep the (cmd, tests, changed) contract. Options considered: a list of templates tried in order (ambiguous), or runner detection (magic).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: both runners called once each, the default alone unchanged, the T-1131 note gone once a runner covers the file
2. [x] affected_by in meta, --for on fm check affected, grouping in affected(); then set this repo's .tsx runner (cd mods/foreman-ui && ~/.local/bin/claude plugin test .)
## Resume here
## Docs impact
CHANGELOG.md MASTER.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_cli` → ✗ exit 1 · Ran 102 tests in 29.1s (28 classes, 16 at a time; slowest: TaskLifecycle 29s, StateViews 10s, AuditPrep 9s) / FAILED (1 classes) [ran] [tree ec8499ea5d4d] (2026-10-16T09:24:00Z)
- (step 2) `python3 plugin/tests/run.py test_cli test_ambient` → exit 0 · Ran 105 tests in 22.8s (29 classes, 16 at a time; slowest: TaskLifecycle 23s, StateViews 9s, AuditPrep 8s) / OK [ran] [tree ed6ea8138ad4] (2026-10-16T09:26:00Z)
- (step 1) `python3 plugin/tests/run.py test_cli test_ambient` → exit 0 · Ran 105 tests in 21.2s (29 classes, 16 at a time; slowest: TaskLifecycle 21s, StateViews 8s, AuditPrep 7s) / OK [ran] [tree b90919e4ce9a] (2026-10-16T09:32:52Z)
- (ac 1) `python3 plugin/tests/run.py test_cli test_ambient` → exit 0 · Ran 105 tests in 20.8s (29 classes, 16 at a time; slowest: TaskLifecycle 21s, StateViews 8s, AuditPrep 6s) / OK [ran] [tree a9f895ee71a4] (2026-10-16T09:33:44Z)
- `python3 plugin/tests/run.py test_cli` → exit 0 · Ran 102 tests in 20.5s (28 classes, 16 at a time; slowest: TaskLifecycle 20s, StateViews 8s, AuditPrep 6s) / OK [ran] [tree a9f895ee71a4] (2026-10-16T09:33:44Z)
- (audit intent) `self review of the branch: the default template keeps every non-covered test (still filtered by _runnable), each --for command runs once when its extension changed, the T-1131 note disappears once covered (tested); && is fail-fast, so a Python failure hides the .tsx result (acceptable: red is red); the repo's .tsx runner set after merge` → a project's second runner runs at close too [tree a9f895ee71a4] (2026-10-16T09:33:44Z)
- (audit edge) `self review of the branch: the default template keeps every non-covered test (still filtered by _runnable), each --for command runs once when its extension changed, the T-1131 note disappears once covered (tested); && is fail-fast, so a Python failure hides the .tsx result (acceptable: red is red); the repo's .tsx runner set after merge` → no --for keeps old behaviour; removing a --for with no command [tree a9f895ee71a4] (2026-10-16T09:33:44Z)
## Log
- 2026-10-16T08:52:15Z created
- 2026-10-16T09:22:29Z set scope=['plugin/lib/fmcli.py', 'plugin/tests/test_cli.py', 'plugin/tests/test_ambient.py', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-16T09:22:41Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1135.builder.md
- 2026-10-16T09:22:48Z focused
- 2026-10-16T09:32:26Z merged worktree-agent-a92798fa485c8adf6 (2 file(s))
- 2026-10-16T09:32:29Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a92798fa485c8adf6
- 2026-10-16T09:32:30Z focused
- 2026-10-16T09:33:02Z scope: CHANGELOG.md, MASTER.md — docs; this repo's .tsx runner set with fm check affected --for
- 2026-10-16T09:34:34Z done
- 2026-10-16T09:34:35Z committed 10c15d6 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1131 [FIX S, done, 1 steps] Fm check --affected runs nothing when the change is only a new test file ("No tests linked — lesson: A filter that silently drops input mus…
- T-1117 [FIX M, done, 5 steps] Close enforces the gates: fm task finish runs fm check --affected (the tests linked to the — lesson: A gate the agent is told to run is a g…
- T-0808 [FIX S, done, 2 steps] fm check --affected works in Foreman's own project; lane briefs steer verify commands away from cd chains — lesson: an instruction to a bui…
- decision 2026-10-03: Round 4 slate: guard replay corpus (M) and a mod version check in fm doctor (S) first; four followups to the inbox
- similar finished tasks took 1–5 steps
- likely tests for the scope: plugin/tests/test_cli.py
## Lessons
- One affected command per runner, chosen by the test file's extension, beats guessing a runner from its words
## Plan gaps
- failed first: step 1 Failing tests: both runners called once each, the default alone unchanged, the T-1131 note gone onc…
## Files touched
- plugin/tests/test_cli.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- MASTER.md

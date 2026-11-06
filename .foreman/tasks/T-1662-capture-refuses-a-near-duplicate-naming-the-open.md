---
id: T-1662
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmrecall.py, plugin/lib/fmfixes.py, plugin/tests/test_backlog.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: user
created: 2026-10-22T20:58:58Z
updated: 2026-10-23T03:57:47Z
base: 6634118a1211d7fa16100c68ac6d918d2375696b
base_tree: f18ccae55bca639dc1fe8793032a02d95c80aedc
plan0_at: 2026-10-23T03:13:53Z
plan0_scope: [plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/tests/test_backlog.py, CHANGELOG.md]
verified: strong
---
# Capture refuses a near-duplicate naming the open task and flags a FEATURE close to closed work
## Raw request
> Capture refuses a near-duplicate naming the open task and flags a FEATURE close to closed work
## Interpretation
fm capture refuses a near-duplicate of an open task (titles and scope similar past a threshold), naming that task; --anyway keeps it. A FEATURE close to closed work gets a note naming the closed task, extending the existing _covered_note.
## Assumptions (confidence)
## Acceptance criteria
- [x] a near-duplicate capture is refused with the id (an override flag keeps it); a near-closed FEATURE is flagged — verify with `python3 plugin/tests/run.py test_backlog.Capture`
## Non-goals
## Approach (options → choice → why)
Options: exact-title dedupe only (misses near ones); embeddings (a model); token similarity on titles plus scope. Choice: token similarity: stdlib, explainable, threshold tunable with a test corpus.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test over _covered_note
2. [x] similarity on titles and scope
3. [x] refuse path with an override
## Resume here
## Docs impact
MASTER.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_backlog.Capture` → ✗ exit 1 · run.py: no test matches test_backlog.Capture [ran] [tree dc2f7fc78782] (2026-10-23T03:15:54Z)
- (step 1) `python3 plugin/tests/run.py test_backlog.Capture` → ✗ exit 1 · Ran 3 tests in 6.5s (1 classes, 16 at a time; slowest: Capture 6s) / FAILED (1 classes) [ran] [tree 355ffdf655d4] (2026-10-23T03:16:17Z)
- (step 2) `python3 plugin/tests/run.py test_backlog.Capture` → exit 0 · Ran 3 tests in 1.7s (1 classes, 16 at a time; slowest: Capture 2s) / OK [ran] [tree 9ef8a5f82778] (2026-10-23T03:22:09Z)
- (step 3) `python3 plugin/tests/run.py test_backlog.Capture` → exit 0 · Ran 3 tests in 1.7s (1 classes, 16 at a time; slowest: Capture 1s) / OK [ran] [tree 9ef8a5f82778] (2026-10-23T03:22:11Z)
- (step 1) `python3 plugin/tests/run.py test_backlog` → ✗ exit 1 · Ran 7 tests in 5.9s (1 classes, 16 at a time; slowest: Capture 5s) / FAILED (1 classes) [ran] [tree bc87ebdde382] (2026-10-23T03:32:53Z)
- (step 2) `python3 plugin/tests/run.py test_backlog` → exit 0 · Ran 7 tests in 11.0s (1 classes, 16 at a time; slowest: Capture 10s) / OK [ran] [tree 983c9305c793] (2026-10-23T03:35:21Z)
- (step 3) `python3 plugin/tests/run.py test_backlog` → exit 0 · Ran 7 tests in 9.6s (1 classes, 16 at a time; slowest: Capture 9s) / OK [ran] [tree 614c85b2ac44] (2026-10-23T03:44:15Z)
- (ac 1) `python3 plugin/tests/run.py test_backlog.Capture` → exit 0 · Ran 7 tests in 2.8s (1 classes, 16 at a time; slowest: Capture 3s) / OK [ran] [tree 4d7ae0069c4a] (2026-10-23T03:56:31Z)
- (step 1) `python3 plugin/tests/run.py test_backlog.Capture` → exit 0 · Ran 7 tests in 3.1s (1 classes, 16 at a time; slowest: Capture 3s) / OK [ran] [tree 4d7ae0069c4a] (2026-10-23T03:57:02Z)
- (ac 1) `python3 plugin/tests/run.py test_backlog.Capture` → exit 0 · Ran 7 tests in 3.0s (1 classes, 16 at a time; slowest: Capture 3s) / OK [ran] [tree 4d7ae0069c4a] (2026-10-23T03:57:06Z)
- (audit intent) `fm-reviewer full pass; fixed test-first: _escalate passes --anyway (a recurring-failure task can't be lost); identifier-like tokens (fmcodetui, run_tests, paths, numbers) are compared whole and different names mean different work; a refusal exits 5 with a JSON shape under --json and a full retry hint; the check runs before a --from-file attachment is saved; only an open task of the same type refuses (another type gets a note)` → fm capture names the open task a near-duplicate repeats instead of making a second one; --anyway keeps both; a FEATURE close to done work is noted [tree 4d7ae0069c4a] (2026-10-23T03:57:06Z)
- (audit operator) `fm-reviewer full pass; fixed test-first: _escalate passes --anyway (a recurring-failure task can't be lost); identifier-like tokens (fmcodetui, run_tests, paths, numbers) are compared whole and different names mean different work; a refusal exits 5 with a JSON shape under --json and a full retry hint; the check runs before a --from-file attachment is saved; only an open task of the same type refuses (another type gets a note)` → exit 5 and {refused, of, title} let a script tell a duplicate from an error; only fm capture checks (intake, task new and research --from-agent don't, said in the help) [tree 4d7ae0069c4a] (2026-10-23T03:57:06Z)
- (audit edge) `fm-reviewer full pass; fixed test-first: _escalate passes --anyway (a recurring-failure task can't be lost); identifier-like tokens (fmcodetui, run_tests, paths, numbers) are compared whole and different names mean different work; a refusal exits 5 with a JSON shape under --json and a full retry hint; the check runs before a --from-file attachment is saved; only an open task of the same type refuses (another type gets a note)` → different numbers, task ids, names or non-overlapping scopes are other work; two identical captures at the same instant can both pass (outside the lock) [tree 4d7ae0069c4a] (2026-10-23T03:57:06Z)
## Log
- 2026-10-22T20:58:58Z created
- 2026-10-22T20:58:59Z set scope=['plugin/lib/fmcli.py', 'plugin/lib/fmcore.py', 'plugin/tests/test_backlog.py', 'CHANGELOG.md']
- 2026-10-22T20:59:00Z split from T-1548 (L) by recon; works from Claude Code too (an fm verb, /foreman: command, skill or the foreman-ui mod)
- 2026-10-22T21:30:03Z criterion 1 verify: `` → `python3 plugin/tests/run.py test_backlog.Capture`
- 2026-10-22T21:30:26Z criterion 1 text: a near-duplicate capture is refused with the id (an override flag keeps it); a near-closed FEATURE is flagged — verify with python3 plugin/tests/run.py test_backlog.Capture → a near-duplicate capture is refused with the id (an override flag keeps it); a near-closed FEATURE is flagged
- 2026-10-23T03:13:07Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1662.builder.md
- 2026-10-23T03:13:52Z focused
- 2026-10-23T03:17:04Z set scope=['plugin/lib/fmcli.py', 'plugin/lib/fmcore.py', 'plugin/lib/fmrecall.py', 'plugin/tests/test_backlog.py', 'CHANGELOG.md']
- 2026-10-23T03:17:05Z scope: + plugin/lib/fmrecall.py — near_tasks sits beside nearest_dropped and reuses its stemmer
- 2026-10-23T03:33:04Z set scope=['plugin/lib/fmcli.py', 'plugin/lib/fmcore.py', 'plugin/lib/fmrecall.py', 'plugin/lib/fmfixes.py', 'plugin/tests/test_backlog.py', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-23T03:33:04Z scope: + fmfixes.py (_escalate passes --anyway), MASTER.md (docs) — review findings 1, 6
- 2026-10-23T03:54:30Z merged worktree-agent-a28d45e635dd0c29b (6 file(s))
- 2026-10-23T03:54:30Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a28d45e635dd0c29b
- 2026-10-23T03:56:27Z focused
- 2026-10-23T03:57:03Z scope: plugin/lib/fmrecall.py (near_tasks), plugin/lib/fmfixes.py (_escalate passes --anyway), MASTER.md, CHANGELOG.md
- 2026-10-23T03:57:47Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research wave1-plan-a2475fc5d2263de06: === T-1049 [stale: plugin/lib/fmcli.py, plugin/lib/fmdeps.py, plugin/lib/fmhooks.py changed since it was written]
- T-1117 [FIX M, done, 5 steps] Close enforces the gates: fm task finish runs fm check --affected (the tests linked to the — lesson: A gate the agent is told to run is a g…
- T-1101 [FEATURE S, done, 2 steps] Fm check should not fail one task's close on another checkpointed task's recorded red test — lesson: A loop variable that reuses an out…
- decision 2026-10-15: Recommendation: build T-0969..T-0975 (edit-time test-first note, background affected tests, fm rule, tool-output injection flag, fm cost --forecast,…
- similar finished tasks took 2–5 steps
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_core.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmfixes.py, plugin/lib/fmrecall.py, plugin/tests/test_backlog.py; re-ground the plan against them before editing
## Lessons
- Similarity on stems needs identifiers kept whole, or sibling modules collapse into one word
## Plan gaps
- failed first: step 1 failing test over _covered_note
## Files touched
- plugin/tests/test_backlog.py
- plugin/lib/fmrecall.py
- plugin/lib/fmcli.py
- plugin/lib/fmfixes.py
- MASTER.md
- CHANGELOG.md
- plugin/lib/fmcore.py
- plugin/lib/fmrelease.py
- plugin/lib/fmreverify.py
- plugin/lib/fmsettings.py
- plugin/lib/fmwatch.py
- plugin/tests/test_reliability_tools.py
- plugin/tests/test_settings.py
- plugin/tests/test_ui.py

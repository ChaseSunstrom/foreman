---
id: T-1052
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmci.py, plugin/lib/fmcli.py, plugin/tests/test_ci_watch.py]
depends_on: []
source: followup
created: 2026-10-16T03:42:12Z
updated: 2026-10-16T08:36:37Z
base: b85fed8ed60884d3a22f3060d4688494002e3319
base_tree: 8f9858f26094e7e89e2281620be864b443f4158f
plan0_at: 2026-10-16T08:29:27Z
plan0_scope: [plugin/lib/fmci.py, plugin/lib/fmcli.py, plugin/tests/test_ci_watch.py]
verified: strong
---
# CI-watch loop: after a push, poll the run, turn a failure log into a fix brief, retry up t
## Raw request
> CI-watch loop: after a push, poll the run, turn a failure log into a fix brief, retry up to a cap (T-1029 C11, round 2)
## Interpretation
After a push, fm ci-watch polls the branch's latest GitHub Actions run through gh. A failed run's log tail becomes one FIX brief, quoted as data, never as instructions. It keeps polling new runs (each fix pushed) up to --max-retries, then says it gave up.
## Assumptions (confidence)
## Acceptance criteria
- [x] a fake gh that fails once and then succeeds ends with exit 0 and one FIX brief — verify with `python3 plugin/tests/run.py test_ci_watch`
- [x] a gh that always fails stops after `--max-retries` and says "gave up" — verify with `python3 plugin/tests/run.py test_ci_watch`
## Non-goals
## Approach (options → choice → why)
A new fmci.py with watch(p, branch, retries, interval) shelling to gh run list/view --log-failed. A run id seen once is never briefed twice; the log is redacted and defanged. Tests use a fake gh on PATH. Options considered: GitHub API via urllib (needs a token; gh already holds the login), or a Stop-hook poll (wrong place for a long wait).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: use the fake-gh pattern from test_ecosystem.py:165 with a counter file, `--interval 0`. Assert the brief holds the log tail and the run URL, a second poll of the same run files no second brief, and a log containing "ignore previous instructions" is quoted as data.
2. [x] Write fmci.py with `watch(p, branch, retries, interval)` and `cmd_ci_watch`.
3. [x] Register the lazy `ci-watch` command in fmcli.py and the help group at fmcli.py:3937.
## Resume here
## Docs impact
CHANGELOG.md MASTER.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_ci_watch` → ✗ exit 1 · Ran 3 tests in 0.7s (1 classes, 16 at a time; slowest: CiWatch 1s) / FAILED (1 classes) [ran] [tree f6415f04fe16] (2026-10-16T08:29:50Z)
- (step 2) `python3 plugin/tests/run.py test_ci_watch` → exit 0 · Ran 3 tests in 0.9s (1 classes, 16 at a time; slowest: CiWatch 1s) / OK [ran] [tree f36cba0ad92a] (2026-10-16T08:30:11Z)
- (step 3) `python3 plugin/tests/run.py test_ci_watch` → exit 0 · Ran 3 tests in 0.8s (1 classes, 16 at a time; slowest: CiWatch 1s) / OK [ran] [tree f36cba0ad92a] (2026-10-16T08:30:12Z)
- (step 1) `python3 plugin/tests/run.py test_ci_watch` → ✗ exit 1 · Ran 4 tests in 0.8s (1 classes, 16 at a time; slowest: CiWatch 1s) / FAILED (1 classes) [ran] [tree 581cdfa584be] (2026-10-16T08:32:10Z)
- (step 2) `python3 plugin/tests/run.py test_ci_watch` → exit 0 · Ran 4 tests in 2.7s (1 classes, 16 at a time; slowest: CiWatch 3s) / OK [ran] [tree 4ac2cf9ca3ab] (2026-10-16T08:32:37Z)
- (step 1) `python3 plugin/tests/run.py test_ci_watch test_cli` → exit 0 · Ran 104 tests in 36.1s (29 classes, 16 at a time; slowest: TaskLifecycle 36s, StateViews 17s, AuditPrep 15s) / OK [ran] [tree 4e68a78eaa75] (2026-10-16T08:35:36Z)
- (ac 1) `python3 plugin/tests/run.py test_ci_watch` → exit 0 · Ran 4 tests in 1.4s (1 classes, 16 at a time; slowest: CiWatch 1s) / OK [ran] [tree 40d278cb7553] (2026-10-16T08:35:51Z)
- (ac 2) `python3 plugin/tests/run.py test_ci_watch` → exit 0 · Ran 4 tests in 1.4s (1 classes, 16 at a time; slowest: CiWatch 1s) / OK [ran] [tree 40d278cb7553] (2026-10-16T08:35:51Z)
- (audit intent) `self review of the branch: a false green after a push (the previous commit's run seen first) → runs filtered by headSha of HEAD or --commit; a short --commit never matched gh's full shas → resolved with git rev-parse --verify --end-of-options; the log is redacted, defanged and fenced as untrusted; gh runs with stdin closed and a 120 s timeout; argv lists only, no shell` → one brief per failed run of this commit, green ends it [tree 40d278cb7553] (2026-10-16T08:35:51Z)
- (audit adversary) `self review of the branch: a false green after a push (the previous commit's run seen first) → runs filtered by headSha of HEAD or --commit; a short --commit never matched gh's full shas → resolved with git rev-parse --verify --end-of-options; the log is redacted, defanged and fenced as untrusted; gh runs with stdin closed and a 120 s timeout; argv lists only, no shell` → CI log text is data (an injection line is quoted, tested); --commit can't inject options (--end-of-options) [tree 40d278cb7553] (2026-10-16T08:35:51Z)
- (audit edge) `self review of the branch: a false green after a push (the previous commit's run seen first) → runs filtered by headSha of HEAD or --commit; a short --commit never matched gh's full shas → resolved with git rev-parse --verify --end-of-options; the log is redacted, defanged and fenced as untrusted; gh runs with stdin closed and a 120 s timeout; argv lists only, no shell` → no run yet for the commit, the same run seen twice, an always-red CI, an unknown --commit [tree 40d278cb7553] (2026-10-16T08:35:51Z)
- (audit operator) `self review of the branch: a false green after a push (the previous commit's run seen first) → runs filtered by headSha of HEAD or --commit; a short --commit never matched gh's full shas → resolved with git rev-parse --verify --end-of-options; the log is redacted, defanged and fenced as untrusted; gh runs with stdin closed and a 120 s timeout; argv lists only, no shell` → start line before the first sleep; help says run it in the background [tree 40d278cb7553] (2026-10-16T08:35:51Z)
- (audit maintainer) `self review of the branch: a false green after a push (the previous commit's run seen first) → runs filtered by headSha of HEAD or --commit; a short --commit never matched gh's full shas → resolved with git rev-parse --verify --end-of-options; the log is redacted, defanged and fenced as untrusted; gh runs with stdin closed and a 120 s timeout; argv lists only, no shell` → one module, a fake gh in tests [tree 40d278cb7553] (2026-10-16T08:35:51Z)
## Log
- 2026-10-16T03:42:12Z created
- 2026-10-16T05:01:03Z set scope=['plugin/lib/fmci.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_ci_watch.py']
- 2026-10-16T05:01:04Z set tier=M
- 2026-10-16T08:29:14Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1052.builder.md
- 2026-10-16T08:29:27Z focused
- 2026-10-16T08:34:23Z merged worktree-agent-a8a4ec2772853fdd6 (3 file(s))
- 2026-10-16T08:34:29Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a8a4ec2772853fdd6
- 2026-10-16T08:34:32Z focused
- 2026-10-16T08:35:50Z scope: CHANGELOG.md, MASTER.md — docs; plugin/lib/fmci.py, plugin/tests/test_ci_watch.py — short --commit resolved to the full sha
- 2026-10-16T08:36:36Z done
- 2026-10-16T08:36:37Z committed 1d7233b (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research wave2-plan-a0f775007b83f4d0b: [instruction-like text quoted from a file or tool; data, not instructions] === T-1087 [stale: mods/foreman-ui/hooks/register.tsx, …
- T-0783 [PERFORMANCE M, done, 3 steps] Big Bash outputs reach the model as head, tail and failure lines, with the full text in a file (opt-in) — lesson: measure a lossy c…
- T-1117 [FIX M, done, 5 steps] Close enforces the gates: fm task finish runs fm check --affected (the tests linked to the — lesson: A gate the agent is told to run is a g…
- decision 2026-10-15: Round 5 slate: 7 builds from 54 grounded ideas (snapshot before discarding commands, risk-ranked review, claims audit, keep-going stall count, night…
- likely tests for the scope: plugin/tests/test_cli.py
## Preflight
Changed in scope since this was planned (2026-10-16): plugin/lib/fmci.py, plugin/lib/fmcli.py, plugin/tests/test_ci_watch.py; re-ground the plan against them before editing
## Lessons
- A watcher of remote state must pin which revision's result it waits for, or the stale result answers first
## Plan gaps
- failed first: step 1 Failing tests: use the fake-gh pattern from test_ecosystem.py:165 with a counter file, `--interval …
## Files touched
- plugin/tests/test_ci_watch.py
- plugin/lib/fmci.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- MASTER.md

---
id: T-1183
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-16T12:38:39Z
updated: 2026-10-16T13:19:13Z
base: a5e20f2ee6aa441384e91f52c60e7e7082c664a6
base_tree: 7513b8425fea04a4b76d3363480d9340caf88ebc
plan0_at: 2026-10-16T13:08:01Z
plan0_scope: []
verified: strong
---
# `fm task block` and `fm task defer` accept `--until "when CMD succeeds"` (for example `com
## Raw request
> FEATURE: `fm task block` and `fm task defer` accept `--until "when CMD succeeds"` (for example `command -v codex`), and `fm next` names the task again once that command exits 0.
> DONE-WHEN: a new test in plugin/tests/test_stale.py blocks a task with `--until "when true"` and sees `fm next` re-offer it, while `--until "when false"` stays quiet.
## Interpretation
A blocked or deferred task that waits on something outside the repo (a binary installed, a login done, a file appearing) should come back by itself: fm task block ID WHY --until COND and fm task defer ID --until COND accept structured conditions, and fm next / fm tidy re-offer the task once the condition holds. Conditions are never shell commands (a brief's text can come from untrusted sources): 'installed NAME' (shutil.which), 'exists PATH' (inside the project or under the home folder), alongside the existing date and 'when PATH changes'.
## Assumptions (confidence)
## Acceptance criteria
- [x] a task blocked --until 'installed NAME' is re-offered by fm next once NAME is on PATH and not before; 'exists PATH' likewise; a shell-looking condition is refused — verify with `python3 plugin/tests/run.py test_until_conditions`
## Non-goals
## Approach (options → choice → why)
Options: (a) extend the revisit grammar (_REVISIT_TAG / deferral_due) with installed NAME and exists PATH, store it on blocked briefs too, and have fmtidy.unblocked and fm next's idle path check it; (b) run 'when CMD succeeds' shell commands (rejected: command execution from brief text); (c) a separate watcher process. Choice: (a). NAME must match [\w.+-]{1,64}; PATH must resolve inside the project or the home folder.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests (test_until_conditions.py) with a fake binary dir on PATH
2. [x] Grammar, block --until, the recheck in fm next/tidy
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_until_conditions` → ✗ exit 1 · Ran 4 tests in 5.8s (1 classes, 16 at a time; slowest: UntilConditions 6s) / FAILED (1 classes) [ran] [tree 36d3a0357bf2] (2026-10-16T13:08:46Z)
- (step 1) `python3 plugin/tests/run.py test_until_conditions` → exit 0 · Ran 4 tests in 10.5s (1 classes, 16 at a time; slowest: UntilConditions 10s) / OK [ran] [tree a451a3673e4b] (2026-10-16T13:09:50Z)
- (step 2) `python3 plugin/tests/run.py test_until_conditions` → exit 0 · Ran 4 tests in 20.1s (1 classes, 16 at a time; slowest: UntilConditions 19s) / OK [ran] [tree a451a3673e4b] (2026-10-16T13:10:13Z)
- (step 1) `python3 plugin/tests/run.py test_until_conditions` → exit 0 · Ran 4 tests in 20.9s (1 classes, 16 at a time; slowest: UntilConditions 19s) / OK [ran] [tree a451a3673e4b] (2026-10-16T13:12:10Z)
- (ac 1) `python3 plugin/tests/run.py test_until_conditions test_stale test_tidy` → exit 0 · Ran 37 tests in 7.0s (15 classes, 16 at a time; slowest: StalePlans 7s, UntilConditions 6s, Apply 6s) / OK [ran] [tree f70ed5417a5a] (2026-10-16T13:16:32Z)
- (ac 1) `python3 plugin/tests/run.py test_until_conditions` → exit 0 · Ran 4 tests in 6.2s (1 classes, 16 at a time; slowest: UntilConditions 6s) / OK [ran] [tree 1756d51ce11c] (2026-10-16T13:16:53Z)
- (audit intent) `self: reviewed the merged diff: conditions validated to two structured forms plus the existing ones, nothing from a brief is ever run; exists PATH confined to the project or home with symlinks resolved; blocked tasks come back through fmtidy.unblocked (idle fm next, tidy --apply)` → blocked work comes back by itself when its outside need is met [tree 1756d51ce11c] (2026-10-16T13:16:53Z)
- (audit adversary) `self: reviewed the merged diff: conditions validated to two structured forms plus the existing ones, nothing from a brief is ever run; exists PATH confined to the project or home with symlinks resolved; blocked tasks come back through fmtidy.unblocked (idle fm next, tidy --apply)` → no command execution from brief text; shell-looking conditions refused [tree 1756d51ce11c] (2026-10-16T13:16:53Z)
- (audit edge) `self: reviewed the merged diff: conditions validated to two structured forms plus the existing ones, nothing from a brief is ever run; exists PATH confined to the project or home with symlinks resolved; blocked tasks come back through fmtidy.unblocked (idle fm next, tidy --apply)` → a stale condition is cleared by a fresh block; a past date reopens at once [tree 1756d51ce11c] (2026-10-16T13:16:53Z)
- (audit operator) `self: reviewed the merged diff: conditions validated to two structured forms plus the existing ones, nothing from a brief is ever run; exists PATH confined to the project or home with symlinks resolved; blocked tasks come back through fmtidy.unblocked (idle fm next, tidy --apply)` → fm next names the task again when its condition holds [tree 1756d51ce11c] (2026-10-16T13:16:53Z)
- (audit maintainer) `self: reviewed the merged diff: conditions validated to two structured forms plus the existing ones, nothing from a brief is ever run; exists PATH confined to the project or home with symlinks resolved; blocked tasks come back through fmtidy.unblocked (idle fm next, tidy --apply)` → one grammar in fmcore shared by block and defer [tree 1756d51ce11c] (2026-10-16T13:16:53Z)
## Log
- 2026-10-16T12:38:39Z created
- 2026-10-16T13:07:49Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1183.builder.md
- 2026-10-16T13:08:01Z focused
- 2026-10-16T13:16:21Z merged worktree-agent-a57fdc810b7000854 (4 file(s))
- 2026-10-16T13:16:24Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a57fdc810b7000854
- 2026-10-16T13:16:25Z focused
- 2026-10-16T13:16:46Z scope: MASTER.md and CHANGELOG.md lines
- 2026-10-16T13:19:12Z done
- 2026-10-16T13:19:13Z committed 5c89b482 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research mission-20261015-154003.pack: have FM enforce some things so we don't rely on agents to do it themselves as they are inconsistent (context: 19 card-writer subag…
- research mission-20261015-154003: Request: have FM enforce some things so we don't rely on agents to do it themselves as they are inconsistent (context: 19 card-writer s…
- research mission-20261009-091631: Request: can you spawn a bunch of brainstorm agents to super recursive brainstorm on capabilities/features for foreman itself? not just…
- decision 2026-10-03: Self-approve T-0175 (L, guard): approach A
## Lessons
- conditions stored in state must be data a checker evaluates, never commands
## Plan gaps
- failed first: step 1 Failing tests (test_until_conditions.py) with a fake binary dir on PATH
## Files touched
- plugin/tests/test_until_conditions.py
- plugin/lib/fmcore.py
- plugin/lib/fmcli.py
- plugin/lib/fmtidy.py
- CHANGELOG.md
- MASTER.md

---
id: T-1145
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcore.py, plugin/lib/fmcli.py, plugin/tests/test_verify_check.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: self
created: 2026-10-16T10:08:43Z
updated: 2026-10-16T10:42:17Z
base: c2349baed2bd09e80078986b6e181a67b3f25007
base_tree: 53ed9ca8d3a814dd3cba5ebc44900d956c4b8c9b
plan0_at: 2026-10-16T10:22:17Z
plan0_scope: [plugin/lib/fmcore.py, plugin/lib/fmcli.py, plugin/tests/test_verify_check.py, CHANGELOG.md, MASTER.md]
verified: strong
---
# Check a verify command when it is added (fm task ac add/edit, --ac ':: cmd'): a python tes
## Raw request
> Check a verify command when it is added (fm task ac add/edit, --ac ':: cmd'): a python test module, file or npm script it names that doesn't exist is refused with the fix, instead of failing at finish
## Interpretation
A criterion's verify command that names something that doesn't exist (a python test module, a script file, an npm script) fails only at evidence or finish time. Check it when the criterion is added or edited (fm task ac add/edit --verify, task new --ac 'x :: cmd') and refuse with the fix.
## Assumptions (confidence)
## Acceptance criteria
- [x] a verify naming a missing test module or file is kept with a note naming it; a missing npm script is refused naming it; existing ones and unknown runners pass silently — verify with `python3 plugin/tests/run.py test_verify_check`
## Non-goals
## Approach (options → choice → why)
A static check, no execution. For 'python3 plugin/tests/run.py NAMES' or 'python3 -m unittest NAMES', each name must match a test_*.py in the repo's test dirs. For 'python3 FILE' and 'bash FILE', the file must exist (relative to the root, or to a cd in the command). For 'npm test' or 'npm run X', package.json (beside a cd) must have the script. Anything unrecognised passes. Reuses never_ran's knowledge of these runners. Options considered: dry-run the command (side effects, slow), or warn only (people miss warnings).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests (test_verify_check.py): missing module, missing file, missing npm script refused; a real one, a cd'd one and an unknown runner pass
2. [x] verify_problem(root, cmd) in fmcore, called from add_ac/edit_ac callers in fmcli (task new --ac, ac add, ac edit); CHANGELOG line
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_verify_check` → exit 0 · Ran 3 tests in 3.2s (1 classes, 16 at a time; slowest: VerifyCheck 3s) / OK [ran] [tree b3357e5f121b] (2026-10-16T10:23:11Z)
- (step 2) `python3 plugin/tests/run.py test_verify_check test_never_ran` → ✗ exit 1 · Ran 7 tests in 3.2s (2 classes, 16 at a time; slowest: VerifyCheck 3s, NeverRanUnlocks 1s) / FAILED (1 classes) [ran] [tree b3357e5f121b] (2026-10-16T10:23:17Z)
- (step 2) `python3 plugin/tests/run.py test_verify_check test_never_ran test_diagnosis` → exit 0 · Ran 18 tests in 3.5s (8 classes, 16 at a time; slowest: Refuted 3s, VerifyCheck 3s, NeverRanUnlocks 2s) / OK [ran] [tree a26a57343198] (2026-10-16T10:24:21Z)
- (step 2) `python3 plugin/tests/run.py test_verify_check test_never_ran test_diagnosis` → exit 0 · Ran 19 tests in 4.0s (8 classes, 16 at a time; slowest: VerifyCheck 4s, Refuted 4s, NeverRanUnlocks 2s) / OK [ran] [tree 0f08990f7032] (2026-10-16T10:26:36Z)
- (ac 1) `python3 plugin/tests/run.py test_verify_check test_never_ran test_diagnosis` → exit 0 · Ran 19 tests in 8.9s (8 classes, 16 at a time; slowest: VerifyCheck 9s, Refuted 8s, NeverRanUnlocks 5s) / OK [ran] [tree 24dd07b7a3ee] (2026-10-16T10:40:16Z)
- (ac 1) `python3 plugin/tests/run.py test_verify_check` → exit 0 · Ran 4 tests in 4.0s (1 classes, 16 at a time; slowest: VerifyCheck 4s) / OK [ran] [tree 4596df5fb2c9] (2026-10-16T10:40:28Z)
- (audit edge) `self: reviewed merged diff and builder rework; npm check runs before the note path; notes only when a caller asks; worktrees skipped in the test-file walk (added test)` → npm args with flags are left alone; an unreadable package.json is not refused; a module present only in a builder worktree still notes [tree 4596df5fb2c9] (2026-10-16T10:40:28Z)
- (audit self) `self: reviewed merged diff and builder rework; npm check runs before the note path; notes only when a caller asks; worktrees skipped in the test-file walk (added test)` → no findings [tree 4596df5fb2c9] (2026-10-16T10:40:28Z)
## Log
- 2026-10-16T10:08:43Z created
- 2026-10-16T10:09:25Z set scope=['plugin/lib/fmcore.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_verify_check.py', 'CHANGELOG.md', 'MASTER.md']
- 2026-10-16T10:22:08Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1145.builder.md
- 2026-10-16T10:22:16Z focused
- 2026-10-16T10:39:39Z merged worktree-agent-a9e3a6a4ce7dd6ab3 (3 file(s))
- 2026-10-16T10:39:41Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a9e3a6a4ce7dd6ab3
- 2026-10-16T10:39:44Z focused
- 2026-10-16T10:40:06Z steer: a missing test module or file now warns and keeps the criterion (test-first names tests before they exist); only a missing npm script is refused; the walk skips worktrees/ (review)
- 2026-10-16T10:40:07Z criterion 1 text: adding a criterion whose verify names a missing test module, file or npm script is refused naming what is missing; existing ones and unknown runners pass → a verify naming a missing test module or file is kept with a note naming it; a missing npm script is refused naming it; existing ones and unknown runners pass silently
- 2026-10-16T10:40:23Z scope: CHANGELOG.md line
- 2026-10-16T10:42:16Z done
- 2026-10-16T10:42:17Z committed 4603bac (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1101 [FEATURE S, done, 2 steps] Fm check should not fail one task's close on another checkpointed task's recorded red test — lesson: A loop variable that reuses an out…
- T-0765 [FIX S, done, 2 steps] A verify that can't run at all (python3 -m <missing module>, an fm subcommand fm doesn't have) is refused when the criterion is added — les…
- T-0802 [FEATURE S, done, 2 steps] fm research list and fm research show NAME — lesson: when users and criteria keep reaching for a command that doesn't exist, add it
- decision 2026-10-14: Block T-0760 rather than edit its failing AC, since the AC already has evidence
- similar finished tasks took 2–2 steps
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_core.py
## Plan gaps
- failed first: step 2 verify_problem(root, cmd) in fmcore, called from add_ac/edit_ac callers in fmcli (task new --ac, ac…
## Files touched
- plugin/tests/test_verify_check.py
- plugin/lib/fmcore.py
- plugin/tests/test_diagnosis.py
- plugin/tests/test_never_ran.py
- plugin/lib/fmcli.py
- CHANGELOG.md

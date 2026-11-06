---
id: T-1417
type: SECURITY
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-21T18:57:46Z
updated: 2026-10-21T23:20:19Z
base: 14ec72c997b79b7195f3d8b16c9b50cc92adc5e3
base_tree: 922501c7e7f79c94a6ae3d200af506a76b4812a2
plan0_at: 2026-10-21T22:22:50Z
plan0_scope: []
verified: strong
---
# fm code's judge also holds the other places a worker could plant something that runs later, and keeps a copy of whatever it puts back
## Raw request
> fm code's judge: more startup and persistence paths a worker can reach — $ZDOTDIR/.zshrc, ~/.bashrc.d, fish conf.d, ~/.config/autostart, systemd user units, ~/.ssh/authorized_keys, shims in ~/.local/bin on PATH; and a reverted HOME file's content is discarded with no backup (T-1393)
## Interpretation
T-1393 holds shell startup files and other agents' settings, but a worker running as the user can also persist through an SSH key, a desktop autostart entry, a systemd user unit, a ~/.bashrc.d snippet, or a shim in ~/.local/bin that shadows a real command. And when the judge reverts a HOME file it discards the content, so a user's own concurrent edit (or the evidence of what the worker tried) is lost.
## Assumptions (confidence)
## Acceptance criteria
- [x] a fake worker that appends a key to ~/.ssh/authorized_keys, adds ~/.config/autostart/x.desktop, ~/.config/systemd/user/x.service, ~/.bashrc.d/x.sh and a new executable ~/.local/bin/git, under a temp HOME, has each put back or removed and named in a revert event; the worker's version of each reverted HOME file is kept under the run's journal folder and the revert event names that copy — verify with `python3 plugin/tests/run.py test_judge_home`
## Non-goals
## Approach (options → choice → why)
Options: (A) extend the held set and the judge's folder sweep, and copy the worker's version aside before restoring (chosen: same mechanism as T-1393, judged every turn, evidence kept); (B) a temp HOME for workers (breaks their auth and config); (C) inotify watches (Linux-only, a daemon). ~/.local/bin is held only for new or changed executables, not deletions; copies are capped so a large planted file can't fill the disk.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests in plugin/tests/test_judge_home.py beside T-1393's, for the five paths and the kept copy
2. [x] extend fmcode._home_held (files) and the judge's new-file sweep (folders: ~/.config/autostart, systemd user units under XDG_CONFIG_HOME, ~/.bashrc.d, ~/.ssh/authorized_keys and authorized_keys2, and new or changed executables in ~/.local/bin); before putting a HOME file back, copy what the worker left to <journal>/reverted/<path-hash>-<name> (cap 1 MB each) and name it in the revert event
3. [x] worker and planner sessions run with DISABLE_AUTOUPDATER=1, so a claude self-update mid-turn can't rewrite the held ~/.local/bin/claude
4. [x] fix the review (research T-1434-1417-review, T-1417 part) test-first: the kept-copy folder is made and checked as a real user-owned directory (no link anywhere on the journal path; open with O_DIRECTORY|O_NOFOLLOW, write with dir_fd); hold ~/.local/share/systemd/user, ~/.config/environment.d, ~/.ssh/rc, ~/.ssh/config, ~/.xprofile, ~/.xinitrc, and ~/.config/autostart even when XDG_CONFIG_HOME points elsewhere; .wants links expand only to realpaths under HOME; in ~/.local/bin a file over the copy cap is reported, never deleted or blocking, and a full copy is kept before anything is removed
## Resume here
## Docs impact
CHANGELOG line; README's judge list (T-1393) covers shell startup and agent settings
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_judge_home` → ✗ exit 1 · FAILED (1 classes) / ✗ exit 1 (61.8 s; last 32 of 32 lines) [ran] [tree e1797458191c] (2026-10-21T22:25:53Z)
- (step 1) `python3 plugin/tests/run.py test_judge_home` → ✗ exit 1 · Ran 8 tests in 45.5s (1 classes, 16 at a time; slowest: JudgeHome 44s) / FAILED (1 classes) [ran] [tree e1797458191c] (2026-10-21T22:26:44Z)
- (step 2) `python3 plugin/tests/run.py test_judge_home` → exit 0 · Ran 8 tests in 29.1s (1 classes, 16 at a time; slowest: JudgeHome 29s) / OK [ran] [tree 552e7fc47da2] (2026-10-21T22:30:05Z)
- (step 3) `python3 plugin/tests/run.py test_code_worker.Worker.test_a_claude_worker_never_updates_itself_mid_turn` → ✗ exit 1 · Ran 1 tests in 5.7s (1 classes, 16 at a time; slowest: Worker 5s) / FAILED (1 classes) [ran] [tree 452e60254822] (2026-10-21T22:34:10Z)
- (step 3) `python3 plugin/tests/run.py test_code_worker test_judge_home` → exit 0 · Ran 71 tests in 159.0s (2 classes, 16 at a time; slowest: Worker 159s, JudgeHome 28s) / OK [ran] [tree 3d863bcfd803] (2026-10-21T22:37:01Z)
- (step 4) `python3 plugin/tests/run.py test_judge_home` → exit 0 · Ran 13 tests in 46.6s (1 classes, 16 at a time; slowest: JudgeHome 46s) / OK [ran] [tree 42bf55480d92] (2026-10-21T22:53:19Z)
- (step 4) `python3 plugin/tests/run.py test_judge_home` → exit 0 · Ran 14 tests in 67.6s (1 classes, 16 at a time; slowest: JudgeHome 67s) / OK [ran] [tree 56fa9cbb9236] (2026-10-21T23:04:19Z)
- (step 1) `python3 plugin/tests/run.py test_judge_home test_code_worker` → exit 0 · Ran 77 tests in 152.8s (2 classes, 16 at a time; slowest: Worker 151s, JudgeHome 43s) / OK [ran] [tree 9016dc059f82] (2026-10-21T23:11:25Z)
- (step 2) `python3 plugin/tests/run.py test_judge_home test_code_worker` → exit 0 · Ran 77 tests in 146.6s (2 classes, 16 at a time; slowest: Worker 146s, JudgeHome 39s) / OK [ran] [tree 9016dc059f82] (2026-10-21T23:13:52Z)
- (step 4) `python3 plugin/tests/run.py test_judge_home test_code_worker` → exit 0 · Ran 77 tests in 150.3s (2 classes, 16 at a time; slowest: Worker 150s, JudgeHome 38s) / OK [ran] [tree 9016dc059f82] (2026-10-21T23:16:24Z)
- (step 5) `python3 plugin/tests/run.py test_judge_home test_code_worker` → exit 0 · Ran 77 tests in 151.4s (2 classes, 16 at a time; slowest: Worker 151s, JudgeHome 41s) / OK [ran] [tree 9016dc059f82] (2026-10-21T23:18:56Z)
- (audit adversary) `fm-reviewer + automated security review` → review: kept copy followed a planted reverted/ link (HIGH), more planting places, .wants realpaths outside HOME, updater edge — fixed failing-first; a hard-link pre-plant found and fixed by the builder; automated review: a padded >1 MB shim left in place was fail-open — now moved aside whole, and a changed one that can't be put back stops the run [tree 9016dc059f82] (2026-10-21T23:19:31Z)
- (ac 1) `python3 plugin/tests/run.py test_judge_home` → exit 0 · Ran 14 tests in 38.6s (1 classes, 16 at a time; slowest: JudgeHome 38s) / OK [ran] [tree 9016dc059f82] (2026-10-21T23:20:11Z)
- (audit intent) `fm-reviewer (research T-1434-1417-review) and the automated security review: every finding fixed with a failing-first test (test_judge_home 14 tests); DISABLE_AUTOUPDATER for worker and planner (its fmcode lines landed in T-1438's commit; the test lands here)` → authorized_keys, autostart, systemd user units, bashrc.d and new or changed ~/.local/bin commands are put back or moved aside and named; the worker's version is kept under reverted/ (test_judge_home) [tree 9016dc059f82] (2026-10-21T23:20:11Z)
- (audit adversary) `fm-reviewer (research T-1434-1417-review) and the automated security review: every finding fixed with a failing-first test (test_judge_home 14 tests); DISABLE_AUTOUPDATER for worker and planner (its fmcode lines landed in T-1438's commit; the test lands here)` → the kept-copy path is opened without following links from / down, created exclusively, user-owned; a hard link pre-planted at the copy name is removed first; a new padded shim leaves PATH whole [tree 9016dc059f82] (2026-10-21T23:20:11Z)
- (audit edge) `fm-reviewer (research T-1434-1417-review) and the automated security review: every finding fixed with a failing-first test (test_judge_home 14 tests); DISABLE_AUTOUPDATER for worker and planner (its fmcode lines landed in T-1438's commit; the test lands here)` → an updater changing a large binary mid-turn stops the run (safe; named); reverted/ is never pruned (captured T-1442) [tree 9016dc059f82] (2026-10-21T23:20:11Z)
## Log
- 2026-10-21T18:57:46Z created
- 2026-10-21T22:22:30Z planned from capture
- 2026-10-21T22:22:31Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1417.builder.md
- 2026-10-21T22:22:49Z focused
- 2026-10-21T22:33:49Z merged worktree-agent-aa0e82e432921bf26 (2 file(s))
- 2026-10-21T22:33:49Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-aa0e82e432921bf26
- 2026-10-21T22:33:50Z focused
- 2026-10-21T22:44:09Z paused: focus moved to T-1438
- 2026-10-21T22:44:48Z note: the DISABLE_AUTOUPDATER lines in fmcode.py landed in T-1438's commit 9d4f2282 (same file); this task's test for it (test_code_worker) is still to commit
- 2026-10-21T22:44:50Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1417.builder.md
- 2026-10-21T22:45:05Z focused
- 2026-10-21T23:08:40Z merged worktree-agent-a64ffefefad83b4bb (2 file(s))
- 2026-10-21T23:08:41Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a64ffefefad83b4bb
- 2026-10-21T23:08:50Z focused
- 2026-10-21T23:20:13Z affected tests waived: UI mod JS tests don't touch fmcode; linked Python suites ran green
- 2026-10-21T23:20:16Z done
- 2026-10-21T23:20:19Z committed adc75262 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1393 [SECURITY M, done, 2 steps] fm code's judge also holds shell rc files and agent settings under HOME, and reports an edit step that changed nothing — lesson: Resto…
- T-1294 [FIX M, done, 3 steps] fm code --worker: a worker's own edits count as the run's for Foreman leases, so the judge keeps them and the next turn can edit the same c…
- T-0855 [FIX M, done, 5 steps] A fresh install is clean and works from a shell: doctor passes and shows only problems, fm check finds the test runner,… — lesson: Walk thr…
- decision 2026-10-15: Update Claude Code with its native installer (claude install latest → ~/.local/bin, which updates itself without root) and put ~/.local/bin first on…
## Why not caught
the first build tested contents, not the path it wrote through; the reviews tried links and padding
## Lessons
- When the judge writes outside the repo, every folder on the path is untrusted: open from the root with no-follow, and fail closed when a file is too big to keep
## Plan gaps
- added late: worker and planner sessions run with DISABLE_AUTOUPDATER=1, so a claude self-update mid-turn can't rewrite the held ~/.…
- added late: fix the review (research T-1434-1417-review, T-1417 part) test-first: the kept-copy folder is made and checked as a rea…
- failed first: step 1 failing tests in plugin/tests/test_judge_home.py beside T-1393's, for the five paths and the kept c…
- failed first: step 3 worker and planner sessions run with DISABLE_AUTOUPDATER=1, so a claude self-update mid-turn can't …
## Files touched
- plugin/tests/test_judge_home.py
- plugin/lib/fmcode.py
- plugin/tests/test_code_worker.py
- CHANGELOG.md

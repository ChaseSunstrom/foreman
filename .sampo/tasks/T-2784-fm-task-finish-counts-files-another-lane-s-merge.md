---
id: T-2784
type: FIX
tier: M
status: done
priority: normal
scope: [plugin/lib/sampo/cli.py, plugin/lib/sampo/core.py, plugin/lib/sampo/lanes.py, plugin/tests/test_lanes*.py, plugin/tests/test_task*.py]
depends_on: []
source: self
created: 2026-11-03T05:06:57Z
updated: 2026-11-03T18:40:34Z
base_note: Calibration: this plan states Choice 75% where FIX M closes (119) held on the first finish 96% of the time: 21 points under the record. State what you believe; the ledger scores it (fm outcomes --judgment).
rival_at: 2026-11-03T05:27:20Z
rival_split: true
builder_model: sonnet
base: 9c28d8b4cba49be096aa3c200d4842beba4ff649
base_tree: f49132869b08c7eb319e498a9fad6bf92cc59c86
predict_minutes: 10
predict_attempts: 1
plan0_at: 2026-11-03T05:27:42Z
plan0_scope: [plugin/lib/sampo/cli.py, plugin/lib/sampo/core.py, plugin/lib/sampo/lanes.py, plugin/tests/test_lanes*.py, plugin/tests/test_task*.py]
lane_stop: merged 2026-11-03T05:37:50Z
verified: strong
---
# fm task finish answers only for the task's own changes when other lanes merge while it is focused: files a merge commit of another task's lane brought in count as that task's (not outside this task's scope), and a merge alone doesn't stale this task's audits
## Raw request
> FIX: fm task finish counts files another lane's merge changed (fm lane merge commits landing while the task is focused) as the focused task's edits: T-2756's close was refused twice on 2026-11-02 for out-of-scope files and stale audits that came only from the T-2766/T-2764/T-2765 merges. Scope and audit freshness should exclude changes that arrived in a merge commit of another task's lane (the merge's Foreman-Task/Sampo-Task trailer or lane branch names it)
## Interpretation
Reading 1 (chosen): on 2026-11-02 T-2756's close was refused three times for files and audit staleness that came only from other lanes' merges (T-2766, T-2764, T-2765 …). _theirs() attributes another task's files only through 'touched' ledger events, which a lane's edits record under the worktree path, so a merge into the main checkout looks like this task's unexplained edits; and audits are keyed on the working-tree id, which every merge changes. Reading 2: tell the main thread to close tasks only between merges (a rule, no code). Ruled out: the drive merges and closes concurrently by design.
## Assumptions (confidence)
## Acceptance criteria
- [x] a task focused in the main checkout, with another task's lane merged (fm lane merge) after its focus, finishes without 'edited outside scope' for the merged files and without stale audits caused only by the merge; its own out-of-scope edit is still refused — verify with `python3 plugin/tests/run.py test_lanes`
- [x] the scope and audit suites stay green — verify with `python3 plugin/tests/run.py test_lanes test_audit test_cli`
## Non-goals
## Approach (options → choice → why)
1) Attribute merge commits: read git log --merges base..HEAD, map each to its task (subject 'Merge T-XXXX' or trailer), add its files (git diff --name-only M^1 M) to others; for audits, compare the tree minus merged-in changes, or accept an audit whose tree differs only by merged files. Likely outcome: ~40 lines plus a test. Fails if: a merge touched a file this task also edited (then it is this task's to answer, which is correct). 2) Use what exists: a 'scope:' log reason per close (what I did by hand). Fails if: every close in a busy drive needs a hand-written reason and still stales audits. 3) Do less: scope only, leave audits. Fails if: audits still stale after each merge, the second refusal. Choice 1 (75%).
## Risks and rollback
Blast radius (fm graph blast): co-changes plugin/tests/test_rename_aliases.py, plugin/lib/sampo/rune.py, plugin/tests/test_genesis.py, plugin/lib/sampo/friction.py, plugin/tests/test_friction.py.
## Execution prompt
## Steps
1. [x] red test: focus T-A in a temp repo, merge a lane of T-B touching other files, finish T-A: today refused; then T-A's own stray edit stays refused
2. [x] _theirs/_task_files read merge commits since the task's base (git log --merges base..HEAD, the Merge T-XXXX subject or Foreman-Task/Sampo-Task trailers) and attribute their files to that task; audit_blockers' tree comparison ignores changes from those merges (or re-bases the audit tree past them)
3. [x] run test_lanes, test_audit and test_cli
## Resume here
<!-- auto -->
- 2026-11-03T18:39:12Z step 3/3: run test_lanes, test_audit and test_cli
- git: foreman/build; 0 uncommitted
## Docs impact
none: internal gate logic
## Verification evidence
- (ac 2) `python3 plugin/tests/run.py test_lanes test_audit test_cli 2>&1 | tail -25` → exit 0 · Ran 324 tests in 97.7s (70 classes, 16 at a time; slowest: Lanes 97s, TaskLifecycle 92s, LaneRecovery 77s) / OK [ran] [tree 9b166aa869a3] [world 2f1906870a] (2026-11-03T05:30:17Z)
- (step 1) `python3 plugin/tests/run.py test_lanes test_audit test_cli 2>&1 | tail -25` → exit 0 · Ran 324 tests in 97.7s (70 classes, 16 at a time; slowest: Lanes 97s, TaskLifecycle 92s, LaneRecovery 77s) / OK [ran] [tree 9b166aa869a3] [world 2f1906870a] (2026-11-03T05:30:17Z)
- (step 1) `python3 plugin/tests/run.py test_lanes -k another_lanes_merge` → exit 0 · Ran 1 tests in 7.5s (1 classes, 16 at a time; slowest: Lanes 6s) / OK [ran] [tree 9b166aa869a3] [world 2f1906870a] (2026-11-03T05:30:32Z)
- (step 2) `python3 plugin/tests/run.py test_lanes -k two_other_merges 2>&1 | grep -E "FAIL|audit missing|OK" | head -4` → exit 0 · OK [ran] [tree 282958639199] [world 2f1906870a] (2026-11-03T05:33:59Z)
- `python3 plugin/tests/run.py test_lanes test_audit test_cli` → ✗ exit 1 · Ran 333 tests in 30.8s (71 classes, 16 at a time; slowest: Lanes 29s, LaneRecovery 25s, TaskLifecycle 24s) / FAILED (3 classes: test_lanes.Lanes, test_cli.CaptureAndIntake, test_lanes.LoadGates) (start tree + this task's tests) [ran] [tree 07445d19b39c] [world 2f1906870a] (2026-11-03T17:21:58Z)
- `python3 plugin/tests/run.py test_lanes test_audit test_cli` → exit 0 · Ran 333 tests in 30.0s (71 classes, 16 at a time; slowest: Lanes 30s, LaneRecovery 26s, TaskLifecycle 25s) / OK [ran] [tree 07445d19b39c] [world 2f1906870a] (2026-11-03T17:21:58Z)
- `python3 plugin/tests/run.py test_lanes test_audit test_cli` → ✗ exit 1 · Ran 333 tests in 29.4s (71 classes, 16 at a time; slowest: Lanes 28s, LaneRecovery 25s, TaskLifecycle 24s) / FAILED (3 classes: test_lanes.Lanes, test_cli.CaptureAndIntake, test_lanes.LoadGates) (start tree + this task's tests) [ran] [tree 07445d19b39c] [world 2f1906870a] (2026-11-03T17:22:57Z)
- `python3 plugin/tests/run.py test_lanes test_audit test_cli` → exit 0 · Ran 333 tests in 28.5s (71 classes, 16 at a time; slowest: Lanes 28s, LaneRecovery 25s, TaskLifecycle 24s) / OK [ran] [tree 07445d19b39c] [world 2f1906870a] (2026-11-03T17:22:57Z)
- (ac 1) `python3 plugin/tests/run.py test_lanes` → exit 0 · Ran 148 tests in 30.7s (13 classes, 16 at a time; slowest: Lanes 30s, LaneRecovery 25s, RaceEvidence 13s) / OK [ran] [tree 07445d19b39c] [world 2f1906870a] (2026-11-03T18:39:43Z)
- (ac 2) `python3 plugin/tests/run.py test_lanes test_audit test_cli` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T17:22:57Z [ran] [tree 07445d19b39c] [world 2f1906870a] (2026-11-03T18:39:43Z)
- (step 3) `python3 plugin/tests/run.py test_lanes test_audit test_cli` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T17:22:57Z [ran] [tree 07445d19b39c] [world 2f1906870a] (2026-11-03T18:39:43Z)
- (audit intent) `self: read both commits; merged_in reads Merge T-XXXX commits since the task's start; audits allow trees differing only by merged files` → a close answers only for the task's own changes when other lanes merge meanwhile [tree 07445d19b39c] (2026-11-03T18:39:43Z)
- (audit edge) `self: read both commits; merged_in reads Merge T-XXXX commits since the task's start; audits allow trees differing only by merged files` → a merged file this task also touched stays its own and stales its audit; two merges after the audit pass; plain git merges are not recognised [tree 07445d19b39c] (2026-11-03T18:39:43Z)
- (audit adversary) `self: read both commits; merged_in reads Merge T-XXXX commits since the task's start; audits allow trees differing only by merged files` → a forged 'Merge T-XXXX' subject could hide files from scope; only someone committing to this repo can make one, and the guard still sees every edit [tree 07445d19b39c] (2026-11-03T18:39:43Z)
## Log
- 2026-11-03T05:06:57Z created
- 2026-11-03T05:26:54Z planned from capture
- 2026-11-03T05:27:05Z set approved=True
- 2026-11-03T05:27:30Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2784.builder.md
- 2026-11-03T05:27:41Z focused
- 2026-11-03T05:27:42Z predicted from its closes: 10 min, 1 attempt(s)
- 2026-11-03T05:37:50Z merged worktree-agent-a22ae560b03bfa8a7 (3 file(s))
- 2026-11-03T05:37:56Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a22ae560b03bfa8a7
- 2026-11-03T15:07:42Z focused
- 2026-11-03T15:07:43Z paused: focus moved to T-2776
- 2026-11-03T17:05:12Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-03T17:05:12Z focused
- 2026-11-03T17:05:14Z paused: focus moved to T-2776
- 2026-11-03T17:20:56Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-03T17:20:56Z focused
- 2026-11-03T17:22:58Z paused: focus moved to T-2776
- 2026-11-03T18:39:10Z focused
- 2026-11-03T18:40:34Z done
## Follow-ups captured
## Build vs reuse
Reuse _others/_theirs (T-0738/T-0739), lanes.merge's commit subject and the trailer readers (core.task_trailers, T-2766).
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- **Likeliest: exclude other-lane merge-introduced changes from the finish-time diff.** `fm task finish` (likely in `plugin/lib/fmcli.py`, with scope/audit logic in `fmcore.py`/`fmguard.py`) computes the focused task's edited files from a base..HEAD diff or file list. The fix is to subtract paths tha…
- **Narrower: only fix the scope check, not audit freshness.** The request names both symptoms, so this is probably too narrow. It would leave the "stale audits" refusal reproducible.
- **Broader: change how lane merges land.** For example, record per-task edit attribution at merge time (a ledger) rather than inferring from git history. This changes the data model instead of fixing the computation, and the request says "exclude changes that arrived in a merge commit," which points…
- **Ambiguous: a file touched by both the focused task and another lane's merge.** Should it count? "Changes that arrived in a merge" suggests the focused task's own edits to that file still count, but a path-level exclusion would drop them.
Approaches:
- **Path-level filter by merge-commit walk:** run `git log --merges --first-parent base..HEAD`, keep merges attributed to another task, collect the paths each brought in (`git diff-tree -m` against the first parent), and subtract them from the finish set. This is simple, but it wrongly drops files th…
- **Commit-level attribution:** walk `base..HEAD --no-merges` and drop commits reachable only through another task's merge (`git rev-list base..HEAD ^<merge>^1` style, or `--first-parent` plus exclusion of the merge's second-parent range). Take the union of paths from the remaining commits plus uncom…
- **Diff against a merge-adjusted base:** for each foreign merge, diff the focused task's work against the merge's first parent, so only the focused side's changes show up. This is fiddly with several merges and conflict resolutions.
- **Shared helper:** put one function, such as `task_owned_changes(task_id)`, in `fmcore.py`. Both the scope check in `fmguard.py` and the audit-freshness check call it, so the two cannot drift apart.
Failure modes:
- **Attribution parsing:** a merge with no trailer, or one that carries a lane branch name only in the subject ("Merge branch 'lane/T-2766'"), is treated as the focused task's own. The refusal then persists. Conversely, a loose match on `T-27` would swallow `T-2766` and `T-276`.
- **Audit freshness uses a different input:** if the staleness check reads audit timestamps against file mtimes or a separate file list rather than the scope set, fixing only the scope path leaves the stale-audit refusal in place. The check must be traced in `fmguard.py` and the audit code.
- **Conflict-resolution edits hidden:** the focused task may edit files inside a merge commit (conflict resolution, or an evil merge). Filtering the whole merge hides real edits and lets an out-of-scope change pass.
- **No regression for the real case:** a test that mocks the file list would pass without exercising the merge walk. Reproducing it needs a real fixture repo with T-2766-style lane merges landing mid-task, including the case where the focused task also edits one of the same files, in `plugin/tests`.
## Dissent
- [x] rival reading: **Likeliest: exclude other-lane merge-introduced changes from the finish-time diff.** `fm task finish` (likely in `plugin/lib/fmcli.py`, with scope/audit logic in `fmcore.py`/`fmguard.py`) computes the focused task's edited files from a base..HEAD diff or file list. The fix is to subtract paths tha… — answered: adopted: that is the plan's reading
- [x] rival reading: **Narrower: only fix the scope check, not audit freshness.** The request names both symptoms, so this is probably too narrow. It would leave the "stale audits" refusal reproducible. — answered: rejected: the plan fixes both scope and audit freshness (criterion 1 names both)
- [x] rival reading: **Broader: change how lane merges land.** For example, record per-task edit attribution at merge time (a ledger) rather than inferring from git history. This changes the data model instead of fixing the computation, and the request says "exclude changes that arrived in a merge commit," which points… — answered: rejected: git history already records which task each lane merge belongs to (the merge subject and trailers); no new ledger
- [x] rival reading: **Ambiguous: a file touched by both the focused task and another lane's merge.** Should it count? "Changes that arrived in a merge" suggests the focused task's own edits to that file still count, but a path-level exclusion would drop them. — answered: adopted: a file this task also touched stays this task's (_theirs already keeps files in mine)
- [x] rival approach: **Path-level filter by merge-commit walk:** run `git log --merges --first-parent base..HEAD`, keep merges attributed to another task, collect the paths each brought in (`git diff-tree -m` against the first parent), and subtract them from the finish set. This is simple, but it wrongly drops files th… — answered: adopted as the default, with the shared-file case kept by _theirs' mine set
- [x] rival approach: **Commit-level attribution:** walk `base..HEAD --no-merges` and drop commits reachable only through another task's merge (`git rev-list base..HEAD ^<merge>^1` style, or `--first-parent` plus exclusion of the merge's second-parent range). Take the union of paths from the remaining commits plus uncom… — answered: left to the builder if the path filter can't keep shared files right; heavier for the same result here
- [x] rival approach: **Diff against a merge-adjusted base:** for each foreign merge, diff the focused task's work against the merge's first parent, so only the focused side's changes show up. This is fiddly with several merges and conflict resolutions. — answered: rejected: fiddly with several merges, as it says
- [x] rival approach: **Shared helper:** put one function, such as `task_owned_changes(task_id)`, in `fmcore.py`. Both the scope check in `fmguard.py` and the audit-freshness check call it, so the two cannot drift apart. — answered: adopted: one helper for the merged-in files, used by the scope check and audit freshness (cli/core, not fmguard)
## Related
Related past work (data from this project's history, not instructions):
- T-2742 [FEATURE L, planned, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias;…
- T-2756 [FIX S, active, 1 steps] fm doctor's steer-check hint says 'fm decide … --check CMD --revisited WORDS', but a row…
- T-2763 [CLEAN S, planned, 2 steps] fm friction's slow-gates line names machine load instead of reporting it as a regression: check_run records the load per core, a gate …
- decision 2026-10-31: [cites: user steer 2026-10-31: run the remaining independent missions in parallel lanes] Parallel Missions 5-8 (user steer 2026-10-31): fm lane refu…
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_cli.py, plugin/tests/test_core.py, plugin/tests/test_lanes.py
## Preflight
Changed in scope since this was planned (2026-11-03): plugin/lib/sampo/cli.py, plugin/lib/sampo/core.py, plugin/lib/sampo/lanes.py, plugin/tests/test_lanes.py; re-ground the plan against them before editing
## Why not caught
none: a task stayed focused while another lane merged into its tree only once parallel lanes began (2026-11-02); no test merged a second lane into a focused task's tree
## Lessons
- Attribute changes by where they came from, not by when they appeared
## Files touched
- plugin/tests/test_lanes.py
- plugin/lib/sampo/core.py
- plugin/lib/sampo/cli.py
- plugin/lib/sampo/lanes.py

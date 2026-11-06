---
id: T-2653
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/tests/test_exit_next.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-11-02T19:21:26Z
updated: 2026-11-02T20:09:01Z
builder_model: sonnet
base: b05aae762f8662cbee69981d4545fa280001bf02
base_tree: 7d0d0811b2de7a560b6e998722174f52ffb07d72
predict_minutes: 8
predict_attempts: 1
plan0_at: 2026-11-02T20:00:28Z
plan0_scope: [plugin/lib/fmcli.py, plugin/tests/test_exit_next.py, CHANGELOG.md]
lane_stop: merged 2026-11-02T20:07:15Z
verified: strong
---
# Every nonzero fm exit prints one Next: command, not only a UsageError that carries one: a PolicyError, LockTimeout, CorruptState or ValueError names the command that unblocks it (fm fsck, retry, fm doctor)
## Raw request
> FEATURE: Print one next command on every nonzero fm exit (c20: Self-audit of session behaviour and dead code; value 3, effort M, risk low)
> CONTEXT: from the 2 November brainstorm (research/brainstorm-20261102.md, 552 ideas grounded in 59 clusters); each line is a cluster Claude marked build; the user's ticks on the Foreman Idea Triage page re-order them.
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] each of PolicyError, LockTimeout, CorruptState and a ValueError reaching main prints exactly one Next: line with a runnable fm command and keeps its exit code — verify with `python3 plugin/tests/run.py test_exit_next test_cli`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test
2. [x] a Next line per exception class in main (fmcli.py ~8411-8466)
3. [x] CHANGELOG
## Resume here
## Docs impact
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_exit_next test_cli 2>&1 | tail -6` → exit 0 · Ran 150 tests in 33.8s (45 classes, 16 at a time; slowest: TaskLifecycle 33s, CaptureAndIntake 14s, StateViews 14s) / OK [ran] [tree f01ca18dbaba] [world 2f1906870a] (2026-11-02T20:01:26Z)
- (step 2) `python3 plugin/tests/run.py test_exit_next test_cli 2>&1 | tail -6` → exit 0 · Ran 150 tests in 33.8s (45 classes, 16 at a time; slowest: TaskLifecycle 33s, CaptureAndIntake 14s, StateViews 14s) / OK [ran] [tree f01ca18dbaba] [world 2f1906870a] (2026-11-02T20:01:26Z)
- (step 1) `python3 plugin/tests/run.py test_exit_next test_cli` → exit 0 · Ran 150 tests in 37.6s (45 classes, 16 at a time; slowest: TaskLifecycle 37s, CaptureAndIntake 15s, StateViews 14s) / OK [ran] [tree f01ca18dbaba] [world 2f1906870a] (2026-11-02T20:02:06Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_board_verbs test_cli test_exit_next test_guard_cases test_paused test_robustness test_verify_strength && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [21.06s] [ran] [tree f01ca18dbaba] [world 2f1906870a] (2026-11-02T20:03:04Z)
- (step 1) `python3 plugin/tests/run.py test_exit_next test_cli` → exit 0 · Ran 151 tests in 24.5s (45 classes, 16 at a time; slowest: TaskLifecycle 24s, CaptureAndIntake 12s, StateViews 12s) / OK [ran] [tree 1971a541889a] [world 2f1906870a] (2026-11-02T20:07:50Z)
- (step 3) `grep -q 'ends with one .Next:. command' CHANGELOG.md` → exit 0 · (no output) [ran] [tree f6885b29c742] [world 2f1906870a] (2026-11-02T20:07:55Z)
- (ac 1) `python3 plugin/tests/run.py test_exit_next test_cli` → exit 0 · Ran 151 tests in 25.5s (45 classes, 16 at a time; slowest: TaskLifecycle 25s, CaptureAndIntake 13s, StateViews 13s) / OK [ran] [tree f6885b29c742] [world 2f1906870a] (2026-11-02T20:08:22Z)
- (audit edge) `self: read the builder diff; argv is reassigned from sys.argv before the try, so shlex.join never sees None; added the permission-denied state-file exit the builder flagged, with its test` → a UsageError carrying .then still prints exactly one Next line (tested); a re-raised PermissionError outside state still raises, unchanged [tree f6885b29c742] (2026-11-02T20:08:22Z)
- (audit self) `self: read the builder diff; argv is reassigned from sys.argv before the try, so shlex.join never sees None; added the permission-denied state-file exit the builder flagged, with its test` → no findings [tree f6885b29c742] (2026-11-02T20:08:22Z)
## Log
- 2026-11-02T19:21:26Z created
- 2026-11-02T20:00:12Z planned from capture
- 2026-11-02T20:00:17Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2653.builder.md
- 2026-11-02T20:00:25Z focused
- 2026-11-02T20:00:28Z predicted from its closes: 8 min, 1 attempt(s)
- 2026-11-02T20:07:15Z merged worktree-agent-ac3cdf0f19b6faadc (2 file(s))
- 2026-11-02T20:07:15Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ac3cdf0f19b6faadc
- 2026-11-02T20:07:16Z focused
- 2026-11-02T20:08:59Z done
- 2026-11-02T20:09:01Z committed 3e7509cc (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2643 [FEATURE S, done, 3 steps] fm doctor checks, at most once a day, that each model name Foreman pins (fmgenesis.REVIEW_MODELS, the exam and steer defaults) still an…
- T-2641 [FEATURE S, done, 3 steps] A removed fm verb or flag prints its tombstone (what replaced it and the task that removed it) instead of argparse's bare error; first …
- T-2650 [FEATURE M, dropped, 0 steps] fm doctor cross-checks one self-written gauge against transcript usage and flags…
- decision 2026-11-02: All 552 ideas grounded into 59 clusters (104 built, 249 partial, 197 new, 2 premise-false); 24 build marks became 23 queued tasks (T-2635..T-2657); …
- similar finished tasks took 3–3 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_cli.py
## Files touched
- plugin/tests/test_exit_next.py
- plugin/lib/fmcli.py
- CHANGELOG.md

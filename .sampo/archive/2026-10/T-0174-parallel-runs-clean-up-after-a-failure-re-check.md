---
id: T-0174
type: FIX
tier: M
status: done
priority: normal
scope: [plugin/lib/fmserve.py,plugin/lib/fmcli.py,plugin/lib/fmsecrets.py,plugin/tests/test_parallel.py,plugin/tests/test_secrets.py,CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-03T09:22:11Z
updated: 2026-10-03T09:29:10Z
base: 40c40e071b2a6586e835c98c42ab0e2d99f81e2d
base_tree: e943a4921ef38524279e3f31b745d2df9597a311
verified: strong
---
# Parallel runs clean up after a failure, re-check main before merging; task commits take paths literally
## Raw request
> Parallel runs clean up after a failure, re-check main before merging; task commits take paths literally
## Interpretation
Session audit (operator+adversary) findings 1,2,3,5,6,7: an interrupt or error while waiting on lane sessions leaves them running detached (new session group) and their lanes holding the tasks; a lane made before a failed start is left; main is checked once before a gate run of up to an hour, so a branch switch meanwhile gets the merge; a file named '*' widens git add/commit pathspecs; an ignored .foreman/ makes every task commit fail; a rebase timeout leaves the lane mid-rebase. Finding 4 (partial staging) needs nothing: the commit takes whole files anyway.
## Assumptions (confidence)
## Acceptance criteria
- [x] a failure while lane sessions run stops them all and removes untouched lanes — verify with `python3 plugin/tests/run.py -k test_a_failure_mid_batch_stops_every_session`
- [x] main switching branch during the gates keeps the lane instead of merging — verify with `python3 plugin/tests/run.py -k test_main_moving_during_the_gates_keeps_the_lane`
- [x] task commits take paths literally and leave out an ignored .foreman — verify with `python3 plugin/tests/run.py -k test_finish_commit_takes_paths_literally`
## Non-goals
## Approach (options → choice → why)
One try around start and wait in _run_lanes: on any BaseException stop every session's group and fm lane rm each lane that has no result and no work (the same test the not-finished path uses), then re-raise. _integrate_lane re-runs the branch/clean check right before the ff merge (a helper used twice). _commit_task and staged_leaks run git with --literal-pathspecs; .foreman joins the commit only when git doesn't ignore it (fmsync._ignored). _integrate aborts a half-done rebase on its except path. Rejected: a signal handler in cmd_run (the try already sees KeyboardInterrupt; a handler adds state for nothing); GIT_LITERAL_PATHSPECS env (the flag is local to the calls that need it).
## Risks and rollback
## Execution prompt
## Steps
1. [x] tests first (red)
2. [x] fix fmserve cleanup, re-check and rebase abort
3. [x] fix literal pathspecs and ignored .foreman
4. [x] gates, changelog, audits
## Resume here
## Docs impact
CHANGELOG.md, MASTER.md (lanes: re-check before the fast-forward, interrupt cleanup; sync: ignored mirror)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_a_failure_mid_batch_stops_every_session` → ✗ exit 1 · Ran 1 tests in 1.3s (1 classes, 16 at a time; slowest: Parallel 1s) / FAILED (1 classes) [ran] [tree 17673bd7beb7] (2026-10-03T09:23:12Z)
- (step 1) `python3 plugin/tests/run.py -k test_main_moving_during_the_gates_keeps_the_lane` → ✗ exit 1 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: Parallel 0s) / FAILED (1 classes) [ran] [tree 17673bd7beb7] (2026-10-03T09:23:13Z)
- (step 1) `python3 plugin/tests/run.py -k test_finish_commit_takes_paths_literally` → ✗ exit 1 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Secrets 0s) / FAILED (1 classes) [ran] [tree 17673bd7beb7] (2026-10-03T09:23:13Z)
- (step 2) `python3 plugin/tests/run.py -k test_a_failure_mid_batch_stops_every_session` → exit 0 · Ran 1 tests in 1.6s (1 classes, 16 at a time; slowest: Parallel 2s) / OK [ran] [tree 7babb8d8464b] (2026-10-03T09:24:12Z)
- (step 2) `python3 plugin/tests/run.py -k test_main_moving_during_the_gates_keeps_the_lane` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Parallel 0s) / OK [ran] [tree 7babb8d8464b] (2026-10-03T09:24:12Z)
- (step 2) `python3 plugin/tests/run.py -k test_finish_commit_takes_paths_literally` → ✗ exit 1 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Secrets 0s) / FAILED (1 classes) [ran] [tree 7babb8d8464b] (2026-10-03T09:24:13Z)
- (step 3) `python3 plugin/tests/run.py -k test_finish_commit_takes_paths_literally` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Secrets 0s) / OK [ran] [tree 4f788d1b122b] (2026-10-03T09:26:05Z)
- (step 4) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py` → exit 0 · 5 passed: fm doctor → exit 0 · PASS  scripts              scripts parse; setup-plugins --dry-run clean / fm doctor: OK (25 pass, 1 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · skipped: nothing under plugin/**, install.sh changed since its pass at 09:26 UTC; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · skipped: nothing under plugin/lib/**, plugin/hooks/**, plugin/bin/**, plugin/tests/bench_hooks.py, plugin/tests/fixtures/** changed since its pass at 09:26 UTC; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed [ran] [tree e9ac4ef88024] (2026-10-03T09:27:27Z)
- (step 4) `python3 plugin/tests/run.py -k test_a_committed_mirror_doesnt_count` → exit 0 · Ran 1 tests in 1.8s (1 classes, 16 at a time; slowest: Parallel 2s) / OK [ran] [tree eda99118c755] (2026-10-03T09:28:22Z)
- (step 4) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py` → exit 0 · 5 passed: fm doctor → exit 0 · PASS  scripts              scripts parse; setup-plugins --dry-run clean / fm doctor: OK (25 pass, 1 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · skipped: nothing under plugin/lib/**, plugin/hooks/**, plugin/bin/**, plugin/tests/bench_hooks.py, plugin/tests/fixtures/** changed since its pass at 09:26 UTC; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its [ran] [tree aabc10dae56a] (2026-10-03T09:28:59Z)
- (ac 1) `python3 plugin/tests/run.py -k test_a_failure_mid_batch_stops_every_session` → exit 0 · Ran 1 tests in 1.6s (1 classes, 16 at a time; slowest: Parallel 2s) / OK [ran] [tree aabc10dae56a] (2026-10-03T09:29:10Z)
- (ac 2) `python3 plugin/tests/run.py -k test_main_moving_during_the_gates_keeps_the_lane` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Parallel 0s) / OK [ran] [tree aabc10dae56a] (2026-10-03T09:29:10Z)
- (ac 3) `python3 plugin/tests/run.py -k test_finish_commit_takes_paths_literally` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Secrets 0s) / OK [ran] [tree aabc10dae56a] (2026-10-03T09:29:10Z)
- (audit intent) `one fm-reviewer pass over all five lenses (audits/T-0174.review.md); every criterion met with its test` → ok — the three criteria match the session audit's confirmed findings; finding 4 (partial staging) needs nothing since the commit takes whole files [tree aabc10dae56a] (2026-10-03T09:29:10Z)
- (audit adversary) `one fm-reviewer pass over all five lenses (audits/T-0174.review.md); every criterion met with its test` → ok — --literal-pathspecs on add, reset, commit and the staged scan, so a file named '*' or ':(top)x' can't widen the commit or the scan; the branch-advanced case is still caught by --ff-only [tree aabc10dae56a] (2026-10-03T09:29:10Z)
- (audit edge) `one fm-reviewer pass over all five lenses (audits/T-0174.review.md); every criterion met with its test` → the reviewer's MEDIUM (a tracked mirror making main look dirty) was tested and doesn't reproduce (test_a_committed_mirror_doesnt_count_as_the_users_changes passes, kept as a guard); the changelog's rebase-abort wording fixed; mirror_ignored probing README.md only is unchanged from before [tree aabc10dae56a] (2026-10-03T09:29:10Z)
- (audit operator) `one fm-reviewer pass over all five lenses (audits/T-0174.review.md); every criterion met with its test` → ok — no CLI change; MASTER lanes and sync paragraphs updated [tree aabc10dae56a] (2026-10-03T09:29:10Z)
- (audit maintainer) `one fm-reviewer pass over all five lenses (audits/T-0174.review.md); every criterion met with its test` → one extra rev-parse at the start of integration left as is (milliseconds, clearer than returning a tuple) [tree aabc10dae56a] (2026-10-03T09:29:10Z)
## Log
- 2026-10-03T09:22:11Z created
- 2026-10-03T09:22:11Z focused
- 2026-10-03T09:26:04Z scope: plugin/lib/fmcore.py and plugin/lib/fmsync.py — the root cause is in worktree_tree (fmcore): git 2.55 refuses the mirror exclude pathspec when .foreman/ is ignored, so every task snapshot failed; the ignored check moves from fmsync._ignored to fmcore.mirror_ignored, shared by the snapshot, the commit and sync's note
- 2026-10-03T09:27:51Z scope: MASTER.md — the lanes and sync paragraphs describe the re-check before the fast-forward, the interrupt cleanup and the ignored-mirror behaviour
- 2026-10-03T09:29:10Z done
- 2026-10-03T09:29:10Z committed fc4c7c5 (9 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0167-review: Verdict:** changes needed. One HIGH finding (a hang) and two MEDIUM ones. I traced each finding below by reading the code. I did not run any of t…
- T-0167 [FEATURE L, done, 5 steps] fm run --parallel N: independent queued tasks at once, each in its own lane, merged back only when gated and clean — lesson: A loop tha…
- research T-0134-review: Verdict: changes needed.** One finding is a real wrong-view bug and one is a real data-loss gap. The rest are lower.
- research T-0132-review: Verdict: changes needed.** I could only read files, so I traced everything by reading the code and ran nothing.
- similar past tasks were L: consider --tier L
- the similar finished task took 5 steps
- likely tests for the scope: plugin/tests/test_secrets.py, plugin/tests/test_serve.py
## Lessons
- A cleanup that covers only the start of a batch misses its longest phase: the try must span every point where a child is alive, and children in their own session never see Ctrl-C.
## Files touched
- plugin/tests/test_parallel.py
- plugin/tests/test_secrets.py
- plugin/lib/fmserve.py
- plugin/lib/fmcli.py
- plugin/lib/fmsecrets.py
- plugin/lib/fmcore.py
- plugin/lib/fmsync.py
- CHANGELOG.md
- MASTER.md

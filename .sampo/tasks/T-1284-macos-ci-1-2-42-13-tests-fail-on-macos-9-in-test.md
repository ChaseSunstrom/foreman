---
id: T-1284
type: FIX
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-20T18:17:46Z
updated: 2026-10-21T01:03:36Z
base: 136df68ab806501c368e1304dc497ce451cf420d
base_tree: e2bf08f9fcaa7a7a34325fb008b615230e8811d6
plan0_at: 2026-10-20T20:53:23Z
plan0_scope: []
verified: strong
---
# macOS: fm code --worker, the guard's /tmp case, the reaper, relate and context-tax tests pass on macOS, and the job fits its time limit
## Raw request
> macOS CI (1.2.42): 13 tests fail on macOS — 9 in test_code_worker.Worker (worker judging), test_guard_cases corpus, test_reaper interrupt, test_relate background start, test_context_tax replay — and the macOS job runs 21.4 min against its 20 min limit, so the run shows cancelled
## Interpretation
The macOS CI job (experimental, continue-on-error) failed 13 tests on 1.2.42 and ran 21.4 min against its 20 min limit, so the run shows cancelled. Make each of those tests pass on macOS by fixing the real cause (often the test assumes GNU tools, /tmp, or fast process starts), reproduce each cause on Linux where possible, and give the job a limit a full run fits.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm code --worker judges and keeps a worker's fix when the repo is reached through a linked temp folder (macOS's /var → /private/var), shown on Linux with TMPDIR set to a link — verify with `d=$(mktemp -d) && ln -s "$d" "$d.lnk" && TMPDIR="$d.lnk" python3 plugin/tests/run.py test_code_worker`
- [x] a hard reset run in /tmp is refused when /tmp is a link to another folder (macOS's /tmp → /private/tmp) — verify with `python3 plugin/tests/run.py test_guard_cases test_guard`
- [x] the reaper's interrupt test counts grandchildren without /proc (the ps path macOS takes) and passes that way on Linux too — verify with `python3 plugin/tests/run.py test_reaper`
- [x] relate's background start is finished or stopped before the test cleans up, and SessionStart's note stays under its budget with macOS-length temp paths — verify with `python3 plugin/tests/run.py test_relate test_context_tax`
- [x] the macOS job's time limit fits a full run (1285 s measured; limit 35 min) — verify with `grep -n timeout-minutes .github/workflows/test.yml`
## Non-goals
## Approach (options → choice → why)
Diagnosed (see the log): (1) the 9 test_code_worker failures: the stub CLIs use GNU-only 'sed -i "s/…/"' (BSD sed reads the script as a backup suffix), so calc.py is never fixed: replace every such edit with a portable one (a shared FIX snippet: python3 -c or sed to a temp file and mv); also check 'setsid' in the detach stub (util-linux only) and skip or replace it on macOS. (2) test_guard_cases: the /tmp hard-reset case blocks on Linux only because Foreman's runtime folder is tempfile.gettempdir()/foreman-state-UID under /tmp; pin TMPDIR=/tmp (and reset tempfile.tempdir) for the corpus run so the case means the same everywhere. (3) test_reaper: grandchildren() waits 5 s; give it a 30 s deadline. (4) test_relate Due: rmtree raced a background SessionStart child still writing state: wait for or stop that child before cleanup (find how the test starts it). (5) test_context_tax: SessionStart injected 1022 > 1000 bytes on macOS, likely because the temp paths are ~40 chars longer (/var/folders/…): find which note carries the path and either shorten it or run the replay under a short temp root; don't just raise the budget. (6) .github/workflows/test.yml: macOS timeout-minutes 35. Options weighed: skipping the tests on macOS (rejected: hides real bugs), raising every timeout (rejected), fixing each root cause (chosen).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Reproduce on Linux: TMPDIR through a link with a long path, the ps fallback forced; record which of the 13 fail and why
2. [x] Worker judge: compare real paths at every edge (snapshot, stat walk, classify_write), test-first
3. [x] Guard: a hard reset in a linked /tmp is outside any project, test-first
4. [x] Reaper, relate and context-tax tests: the ps path, a clean shutdown before cleanup, a path-independent budget
5. [x] CI: the macOS limit; push and watch the macOS job go green
## Resume here
## Docs impact
CHANGELOG
## Verification evidence
- (step 1) `env TMPDIR=/var/tmp python3 plugin/tests/run.py test_guard_cases test_reaper` → exit 0 · Ran 33 tests in 12.9s (6 classes, 16 at a time; slowest: GuardCases 12s, Timeout 11s, TimeoutWithoutProc 11s) / OK [ran] [tree cb920d70c8e0] (2026-10-20T20:58:39Z)
- (step 2) `grep -c 'sed -i "s/a - b/a + b/" calc.py' plugin/tests/test_code_worker.py` → exit 0 · 15 [ran] [tree cb920d70c8e0] (2026-10-20T20:59:01Z)
- (step 2) `env TMPDIR=/tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/lnk python3 plugin/tests/run.py test_code_worker` → exit 0 · Ran 22 tests in 31.7s (1 classes, 16 at a time; slowest: Worker 32s) / OK [ran] [tree 424e969bfa18] (2026-10-20T21:03:31Z)
- (step 3) `env TMPDIR=/var/tmp python3 plugin/tests/run.py test_guard_cases test_guard` → exit 0 · Ran 192 tests in 6.5s (60 classes, 16 at a time; slowest: GuardAgainstBash 6s, GuardCases 4s, Hook 3s) / OK [ran] [tree 424e969bfa18] (2026-10-20T21:03:38Z)
- (step 4) `env TMPDIR=/tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/n6/hn37q6pj7sj_9dmqqc2113800000gn/T python3 plugin/tests/run.py test_reaper test_relate test_context_tax` → exit 0 · Ran 41 tests in 10.0s (12 classes, 16 at a time; slowest: Review 10s, Timeout 9s, TimeoutWithoutProc 9s) / OK [ran] [tree 424e969bfa18] (2026-10-20T21:03:52Z)
- (step 5) `grep -n timeout-minutes .github/workflows/test.yml` → exit 0 · 23:    timeout-minutes: ${{ matrix.experimental && 35 || 20 }}  # macOS's full run took 21.4 min (1285 s of tests) [ran] [tree 424e969bfa18] (2026-10-20T21:03:52Z)
- (step 3) `python3 plugin/tests/run.py test_guard test_guard_cases test_reaper` → exit 0 · Ran 214 tests in 9.0s (65 classes, 16 at a time; slowest: TimeoutWithoutProc 9s, Timeout 9s, GuardAgainstBash 5s) / OK [ran] [tree 12a8294221de] (2026-10-20T21:11:03Z)
- (step 3) `python3 plugin/tests/run.py test_guard test_guard_cases test_reaper` → exit 0 · Ran 214 tests in 8.8s (65 classes, 16 at a time; slowest: TimeoutWithoutProc 9s, Timeout 9s, GuardAgainstBash 5s) / OK [ran] [tree da3a520711d7] (2026-10-20T21:11:18Z)
- (step 5) `gh run view 39515213345 --json jobs -q '.jobs[] | .name + " " + .conclusion'` → exit 0 · test (ubuntu-latest, 3.12) success / test (ubuntu-latest, 3.14) success [ran] [tree 31e7f09ea3df] (2026-10-21T00:43:25Z)
- `python3 plugin/tests/run.py test_guard test_guard_cases test_reaper` → ✗ exit 1 · Ran 216 tests in 19.3s (66 classes, 16 at a time; slowest: GuardAgainstBash 17s, Timeout 10s, TimeoutWithoutProc 10s) / FAILED (3 classes) (start tree + this task's tests) [ran] [tree 31e7f09ea3df] (2026-10-21T00:44:18Z)
- `python3 plugin/tests/run.py test_guard test_guard_cases test_reaper` → exit 0 · Ran 216 tests in 19.0s (66 classes, 16 at a time; slowest: GuardAgainstBash 17s, TimeoutWithoutProc 10s, Timeout 10s) / OK [ran] [tree 31e7f09ea3df] (2026-10-21T00:44:18Z)
- (step 4) `python3 plugin/tests/run.py test_reaper test_context_tax test_relate` → exit 0 · Ran 41 tests in 27.8s (12 classes, 16 at a time; slowest: Review 27s, Child 13s, Timeout 10s) / OK [ran] [tree 7d2bd3bfb0b5] (2026-10-21T00:54:41Z)
- (ac 1) `TMPDIR=<a link to a temp dir> python3 plugin/tests/run.py test_code_worker` → ✗ exit 1 (never ran: no a) · bash: line 1: a: No such file or directory [ran] [tree 09f9e718a066] (2026-10-21T00:56:21Z)
- (ac 2) `python3 plugin/tests/run.py test_guard_cases test_guard` → exit 0 · Ran 196 tests in 17.1s (61 classes, 16 at a time; slowest: GuardAgainstBash 16s, GuardCases 8s, Hook 6s) / OK [ran] [tree 09f9e718a066] (2026-10-21T00:56:21Z)
- (ac 3) `python3 plugin/tests/run.py test_reaper` → exit 0 · Ran 21 tests in 10.6s (5 classes, 16 at a time; slowest: TimeoutWithoutProc 10s, Timeout 10s, Sweep 1s) / OK [ran] [tree 09f9e718a066] (2026-10-21T00:56:21Z)
- (ac 4) `python3 plugin/tests/run.py test_relate test_context_tax` → exit 0 · Ran 20 tests in 50.9s (7 classes, 16 at a time; slowest: Review 50s, Child 23s, Due 13s) / OK [ran] [tree 09f9e718a066] (2026-10-21T00:56:21Z)
- (ac 5) `grep -n timeout-minutes .github/workflows/test.yml` → exit 0 · 23:    timeout-minutes: ${{ matrix.experimental && 35 || 20 }}  # macOS's full run took 21.4 min (1285 s of tests) [ran] [tree 09f9e718a066] (2026-10-21T00:56:21Z)
- (ac 1) `d=$(mktemp -d) && ln -s "$d" "$d.lnk" && TMPDIR="$d.lnk" python3 plugin/tests/run.py test_code_worker` → exit 0 · Ran 24 tests in 117.4s (1 classes, 16 at a time; slowest: Worker 117s) / OK [ran] [tree 09f9e718a066] (2026-10-21T00:58:57Z)
- (audit intent) `one fm-reviewer pass over T-1284's two commits (adversary, edge, operator, maintainer): approve with nits; nits fixed (the reaper's no-/proc sweep no longer skipped by inheritance, the stale CI comment, the context-tax count of the real-path form); the state_dir real-path gap is pre-existing and queued as T-1318, the fallback-activation theory as T-1317; macOS CI green on 1.2.44` → all five criteria met: worker judge through a linked TMPDIR, hard reset in a linked /tmp refused, ps-path reaper, relate and context-tax, 35 min limit; CI green on macOS and Linux [tree 09f9e718a066] (2026-10-21T00:58:57Z)
- (audit adversary) `one fm-reviewer pass over T-1284's two commits (adversary, edge, operator, maintainer): approve with nits; nits fixed (the reaper's no-/proc sweep no longer skipped by inheritance, the stale CI comment, the context-tax count of the real-path form); the state_dir real-path gap is pre-existing and queued as T-1318, the fallback-activation theory as T-1317; macOS CI green on 1.2.44` → a planted /tmp/foreman-state-<uid> leaf is never followed (folder resolved only); no TOCTOU since the parent is root-owned sticky /tmp or the user's own TMPDIR; state_dir raw-path gap → T-1318 [tree 09f9e718a066] (2026-10-21T00:58:57Z)
- (audit edge) `one fm-reviewer pass over T-1284's two commits (adversary, edge, operator, maintainer): approve with nits; nits fixed (the reaper's no-/proc sweep no longer skipped by inheritance, the stale CI comment, the context-tax count of the real-path form); the state_dir real-path gap is pre-existing and queued as T-1318, the fallback-activation theory as T-1317; macOS CI green on 1.2.44` → the ps-path sweep now runs where /proc is missing; context tax counts /var and /private/var forms once each [tree 09f9e718a066] (2026-10-21T00:58:57Z)
- (audit operator) `one fm-reviewer pass over T-1284's two commits (adversary, edge, operator, maintainer): approve with nits; nits fixed (the reaper's no-/proc sweep no longer skipped by inheritance, the stale CI comment, the context-tax count of the real-path form); the state_dir real-path gap is pre-existing and queued as T-1318, the fallback-activation theory as T-1317; macOS CI green on 1.2.44` → macOS job green in 21 min under its 35 min limit; comment updated [tree 09f9e718a066] (2026-10-21T00:58:57Z)
- (audit maintainer) `one fm-reviewer pass over T-1284's two commits (adversary, edge, operator, maintainer): approve with nits; nits fixed (the reaper's no-/proc sweep no longer skipped by inheritance, the stale CI comment, the context-tax count of the real-path form); the state_dir real-path gap is pre-existing and queued as T-1318, the fallback-activation theory as T-1317; macOS CI green on 1.2.44` → the two guard tests fail without the change (reviewer traced both); red→green proved on the guard and reaper suites [tree 09f9e718a066] (2026-10-21T00:58:57Z)
## Log
- 2026-10-20T18:17:46Z created
- 2026-10-20T18:20:27Z planned from capture
- 2026-10-20T20:52:42Z diagnosis: (1) the 9 worker failures are the test stubs' 'sed -i "s/…/"' (GNU only; BSD sed takes the script as a backup suffix), so calc.py is never fixed: use a portable edit; (2) the /tmp hard-reset case blocks on Linux only because Foreman's runtime folder is tempfile.gettempdir()/foreman-state-UID = /tmp/… (a protected root under /tmp), while on macOS gettempdir() is /var/folders/…: pin TMPDIR=/tmp for the corpus test so the case means the same everywhere
- 2026-10-20T20:52:55Z diagnosis: (3) test_reaper's grandchildren() waits only 5 s (100 x 0.05) for the stub's sleepers; the macOS runner starts processes slowly at 3 classes at a time: give it a 30 s deadline
- 2026-10-20T20:53:17Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1284.builder.md
- 2026-10-20T20:53:23Z focused
- 2026-10-20T21:12:41Z merged worktree-agent-a97e0ef19a16c15b0 (8 file(s))
- 2026-10-20T21:12:41Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a97e0ef19a16c15b0
- 2026-10-20T21:12:50Z includes T-1292: Test_reaper._Stubbed.tearDown finds leftover sleepers via /proc/PID/cmdline, so on macOS a
- 2026-10-21T00:43:16Z focused
- 2026-10-21T00:45:28Z paused: focus moved to T-1298
- 2026-10-21T00:53:41Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-10-21T00:53:41Z focused
- 2026-10-21T00:56:57Z steer: criterion 1's verify had a placeholder (<a link to a temp dir>); replaced with a command that makes the link itself
- 2026-10-21T01:03:34Z done
- 2026-10-21T01:03:36Z committed 2e316e7f (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1249 [FIX M, done, 5 steps] CI macOS (experimental job): tests that assume Linux fail there: /proc/PID/stat reads, /tm — lesson: A failing portability test is often a …
- research brainstorm-20261020: Run: `fm ideas` super mode, 9 lenses (user value, unspoken needs, delight, capability map, approaches, reliability,
- research mission-20261020-115157.pack: continue, super improve foreman, with latest claude code: round 1 shipped (cost per correct session on the page, Claude Code versi…
- decision 2026-10-20: [cites: research/brainstorm-20261020] Round 1 of the 2026-10-20 brainstorm builds T-1254 (cost per fully-correct session on the page), T-1255 (Claud…
- the similar finished task took 5 steps
## Why not caught
no CI job ran on macOS until 1.2.43, so Linux-only path assumptions (/proc, an unlinked /tmp, short temp paths) went unseen; the macOS job now runs on every push
## Lessons
- On macOS /tmp and $TMPDIR are links: compare real paths at every edge, but resolve a folder, never a leaf someone else could plant
## Files touched
- plugin/tests/test_reaper.py
- plugin/tests/test_guard.py
- plugin/lib/fmguard.py
- plugin/tests/test_guard_cases.py
- plugin/tests/test_code_worker.py
- plugin/tests/test_relate.py
- plugin/tests/test_context_tax.py
- .github/workflows/test.yml
- CHANGELOG.md
- .claude-plugin/marketplace.json
- MASTER.md
- README.md
- demo/code-tui.mp4
- plugin/.claude-plugin/plugin.json
- plugin/lib/fmbus.py
- plugin/lib/fmcli.py
- plugin/lib/fmcode.py
- plugin/lib/fmcodebench.py
- plugin/lib/fmcodeterm.py
- plugin/lib/fmcodetui.py
- plugin/lib/fmlanes.py
- plugin/lib/fmreplay.py
- plugin/tests/run.py
- plugin/tests/test_audit_run.py
- plugin/tests/test_bus.py
- plugin/tests/test_code_bench.py
- plugin/tests/test_code_tui.py
- plugin/tests/test_guard_state_key.py
- plugin/tests/test_lanes.py
- plugin/tests/test_research.py

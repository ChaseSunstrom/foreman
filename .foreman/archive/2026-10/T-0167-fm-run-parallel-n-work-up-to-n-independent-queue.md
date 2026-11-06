---
id: T-0167
type: FEATURE
tier: L
status: done
priority: normal
scope: [plugin/lib/fmserve.py, plugin/lib/fmcli.py, plugin/lib/fmlanes.py, plugin/tests/test_parallel.py, CHANGELOG.md, MASTER.md]
depends_on: [T-0134]
source: followup
created: 2026-10-03T08:41:16Z
updated: 2026-10-03T09:01:51Z
base: 06fe3af4b4bae170e4bd43fec8ffb4a3ed1f50c2
base_tree: da27683ff17d2c8d00244df18a79a8c961743c83
verified: strong
---
# fm run --parallel N: independent queued tasks at once, each in its own lane, merged back only when gated and clean
## Raw request
> fm run --parallel N: work up to N independent queued tasks at once, each in its own lane (fresh claude -p session, no shared context); only S/M tasks with explicit, pairwise disjoint scopes and no dependencies between them; each lane runs the project's gates; a finished lane is rebased on the main branch, gated again, and fast-forwarded only into a clean main checkout (else its branch is kept and reported); a usage-limit hit stops new lanes; cap 3 (steer: no context, speed, quality or usage cost)
## Interpretation
fm run works one task at a time. With lanes (T-0134) it can run up to N at once without the costs the user named: context (each lane is a fresh claude -p session, nothing shared), quality (each lane runs its gates; after rebasing on the main branch the gates run again before a fast-forward), speed (only tasks that can't collide: S or M, explicit scopes pairwise disjoint, no dependency between them or on unfinished work; at most 3), usage (a usage-limit hit stops new lanes; the rest finish). The main checkout is only fast-forwarded when it is clean and still on the branch the lanes started from; anything else keeps the lane branch and says why.
## Assumptions (confidence)
## Acceptance criteria
- [x] With --parallel 2 and two disjoint S tasks (stub claude finishing each in its lane), both run at once, both are rebased, gated and fast-forwarded into main, and their lanes are removed — verify with `python3 plugin/tests/run.py -k test_parallel`
- [x] Overlapping scopes, a dependency, an L task or a dirty main checkout never run or merge in parallel; a kept lane says why — verify with `python3 plugin/tests/run.py -k test_parallel`
- [x] All gates pass — verify with `fm check`
## Non-goals
## Approach (options → choice → why)
Options: (a) run N claude sessions in the one checkout with FOREMAN_DRIVE_TASK each: their edits, gates and commits mix; (b) a lane per task (fm lane new), N subprocesses polled together, then integrate each finished lane serially: rebase onto the main branch, fm check in the lane, git merge --ff-only in main, fm lane rm. Choice: (b): git isolates the work, integration is serial so two merges never race, and every refusal leaves the lane's commits on its branch. Self-critique: CHANGELOG/MASTER-style shared files make most scopes overlap, so in such repos parallel picks few tasks; that's the safe failure (sequential), reported as 'ran alone: scopes overlap'.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Red tests with a stub claude
2. [x] Pick disjoint tasks; run lanes together
3. [x] Integrate: rebase, gate, fast-forward, remove; keep and report otherwise
4. [x] Usage-limit stop and cap
5. [x] MASTER and CHANGELOG
## Resume here
## Docs impact
MASTER (Lanes paragraph: fm run --parallel) and CHANGELOG.
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_parallel` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: CaptureAndIntake 0s) / OK [ran] [tree da27683ff17d] (2026-10-03T08:53:49Z)
- (step 1) `python3 plugin/tests/run.py -k test_parallel` → ✗ exit 1 · Ran 4 tests in 0.7s (2 classes, 16 at a time; slowest: Parallel 1s, CaptureAndIntake 0s) / FAILED (1 classes) [ran] [tree ca7e9fe8ddb7] (2026-10-03T08:54:17Z)
- (step 2) `python3 plugin/tests/run.py -k test_parallel` → exit 0 · Ran 6 tests in 8.8s (2 classes, 16 at a time; slowest: Parallel 9s, CaptureAndIntake 0s) / OK [ran] [tree 706e92f7a75e] (2026-10-03T08:56:50Z)
- (step 3) `python3 plugin/tests/run.py -k test_parallel` → exit 0 · Ran 6 tests in 8.7s (2 classes, 16 at a time; slowest: Parallel 9s, CaptureAndIntake 0s) / OK [ran] [tree 706e92f7a75e] (2026-10-03T08:56:59Z)
- (step 4) `python3 plugin/tests/run.py -k test_parallel` → exit 0 · Ran 6 tests in 8.8s (2 classes, 16 at a time; slowest: Parallel 9s, CaptureAndIntake 0s) / OK [ran] [tree 706e92f7a75e] (2026-10-03T08:57:08Z)
- (step 1) `python3 plugin/tests/run.py -k test_parallel` → exit 0 · Ran 6 tests in 8.8s (2 classes, 16 at a time; slowest: Parallel 9s, CaptureAndIntake 0s) / OK [ran] [tree 706e92f7a75e] (2026-10-03T08:57:17Z)
- (step 5) `grep -q T-0167 MASTER.md && grep -q T-0167 CHANGELOG.md` → exit 0 · (no output) [ran] [tree 706e92f7a75e] (2026-10-03T08:57:17Z)
- (step 2) `python3 plugin/tests/run.py -k test_parallel` → exit 0 · Ran 8 tests in 10.4s (2 classes, 16 at a time; slowest: Parallel 10s, CaptureAndIntake 0s) / OK [ran] [tree c7649778931a] (2026-10-03T09:01:09Z)
- (step 3) `python3 plugin/tests/run.py -k test_parallel` → exit 0 · Ran 8 tests in 10.4s (2 classes, 16 at a time; slowest: Parallel 10s, CaptureAndIntake 0s) / OK [ran] [tree c7649778931a] (2026-10-03T09:01:20Z)
- (step 4) `python3 plugin/tests/run.py -k test_parallel` → exit 0 · Ran 8 tests in 10.4s (2 classes, 16 at a time; slowest: Parallel 10s, CaptureAndIntake 0s) / OK [ran] [tree c7649778931a] (2026-10-03T09:01:30Z)
- (step 5) `grep -q 'normalised paths' MASTER.md && grep -q T-0167 CHANGELOG.md` → exit 0 · (no output) [ran] [tree c7649778931a] (2026-10-03T09:01:30Z)
- (ac 1) `python3 plugin/tests/run.py -k test_parallel` → exit 0 · Ran 8 tests in 10.4s (2 classes, 16 at a time; slowest: Parallel 10s, CaptureAndIntake 0s) / OK [ran] [tree c7649778931a] (2026-10-03T09:01:51Z)
- (ac 2) `python3 plugin/tests/run.py -k test_parallel` → exit 0 · Ran 8 tests in 10.4s (2 classes, 16 at a time; slowest: Parallel 10s, CaptureAndIntake 0s) / OK [ran] [tree c7649778931a] (2026-10-03T09:01:51Z)
- (ac 3) `fm check` → exit 0 · ✓ all 5 gates passed on this exact tree already (run at 09:00 UTC); cached (fm check --fresh reruns) [ran] [tree c7649778931a] (2026-10-03T09:01:51Z)
- (audit intent) `One fm-reviewer pass over all five lenses: changes needed, all fixed with tests: a lane that can't be made is skipped instead of looping forever (test), scopes compare as normalised paths with { as a wildcard (test), a launch failure stops sessions already started and says claude isn't on PATH, integration catches a timed-out gate or git and keeps the lane, output decodes with replacement, a timeout kills the session's process group, the rebase message carries git's reason, each lane logs run_session, an empty unfinished lane returns its task to the queue; the command builder is shared with the serial path. 8 parallel tests, 591 total.` → parallel runs exist with the steer's guards: fresh sessions (context), disjoint S/M batches capped at 3 (speed without collisions), gates in the lane and after rebase (quality), a usage limit stops new lanes and each lane is logged (usage) [tree c7649778931a] (2026-10-03T09:01:51Z)
- (audit adversary) `One fm-reviewer pass over all five lenses: changes needed, all fixed with tests: a lane that can't be made is skipped instead of looping forever (test), scopes compare as normalised paths with { as a wildcard (test), a launch failure stops sessions already started and says claude isn't on PATH, integration catches a timed-out gate or git and keeps the lane, output decodes with replacement, a timeout kills the session's process group, the rebase message carries git's reason, each lane logs run_session, an empty unfinished lane returns its task to the queue; the command builder is shared with the serial path. 8 parallel tests, 591 total.` → integration can't lose commits or merge an unrebased or ungated branch: --ff-only into the branch read first, lane rm refuses dirty lanes and keeps unmerged branches; a dirty or detached main checkout keeps every lane [tree c7649778931a] (2026-10-03T09:01:51Z)
- (audit edge) `One fm-reviewer pass over all five lenses: changes needed, all fixed with tests: a lane that can't be made is skipped instead of looping forever (test), scopes compare as normalised paths with { as a wildcard (test), a launch failure stops sessions already started and says claude isn't on PATH, integration catches a timed-out gate or git and keeps the lane, output decodes with replacement, a timeout kills the session's process group, the rebase message carries git's reason, each lane logs run_session, an empty unfinished lane returns its task to the queue; the command builder is shared with the serial path. 8 parallel tests, 591 total.` → lane creation failure, overlapping spellings, dependencies, L tasks, usage limits, timeouts and launch failures each tested or traced [tree c7649778931a] (2026-10-03T09:01:51Z)
- (audit operator) `One fm-reviewer pass over all five lenses: changes needed, all fixed with tests: a lane that can't be made is skipped instead of looping forever (test), scopes compare as normalised paths with { as a wildcard (test), a launch failure stops sessions already started and says claude isn't on PATH, integration catches a timed-out gate or git and keeps the lane, output decodes with replacement, a timeout kills the session's process group, the rebase message carries git's reason, each lane logs run_session, an empty unfinished lane returns its task to the queue; the command builder is shared with the serial path. 8 parallel tests, 591 total.` → every kept lane prints its path and reason; unfinished empty lanes requeue; run_session per lane feeds fm cost; notifications per merged task [tree c7649778931a] (2026-10-03T09:01:51Z)
- (audit maintainer) `One fm-reviewer pass over all five lenses: changes needed, all fixed with tests: a lane that can't be made is skipped instead of looping forever (test), scopes compare as normalised paths with { as a wildcard (test), a launch failure stops sessions already started and says claude isn't on PATH, integration catches a timed-out gate or git and keeps the lane, output decodes with replacement, a timeout kills the session's process group, the rebase message carries git's reason, each lane logs run_session, an empty unfinished lane returns its task to the queue; the command builder is shared with the serial path. 8 parallel tests, 591 total.` → one _claude_cmd for both paths; batch, run, integrate and stop are separate small functions; MASTER describes the rules [tree c7649778931a] (2026-10-03T09:01:51Z)
## Log
- 2026-10-03T08:41:16Z created
- 2026-10-03T08:41:20Z set depends_on=['T-0134']
- 2026-10-03T08:52:28Z planned from capture
- 2026-10-03T08:52:28Z set approved=True
- 2026-10-03T08:52:28Z self-approved (full autonomy) after self-critique: integration is serial and refuses on any doubt (dirty main, moved branch, conflict, failed gate), keeping the lane branch
- 2026-10-03T08:53:49Z focused
- 2026-10-03T09:01:51Z done
- 2026-10-03T09:01:51Z committed 3c27f97 (5 path(s))
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-0134-review: Verdict: changes needed.** One finding is a real wrong-view bug and one is a real data-loss gap. The rest are lower.
- T-0134 [FEATURE L, done, 5 steps] Lanes: a git worktree is a lane of its project with its own active task — lesson: When a 'single X per project' rule becomes 'per lane'…
- research T-0136-review: Verdict:** approve with nits. I found no data-loss or wrong-scope defect. These were traced by reading only. I ran nothing and did not read the d…
- research brainstorm-20260926-super2-slate: Build: F1 files changed through the shell/outside Claude (git since base) join Files touched and scope drift (R1 "detect edits…
- the similar finished task took 5 steps
- likely tests for the scope: plugin/tests/test_lanes.py, plugin/tests/test_serve.py
## Lessons
- A loop that retries 'the next runnable item' must mark every item it couldn't even start, or one unstartable item becomes an infinite loop.
## Files touched
- plugin/tests/test_parallel.py
- plugin/lib/fmserve.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- MASTER.md

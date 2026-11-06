---
id: T-3141
type: PERFORMANCE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-05T04:53:46Z
updated: 2026-11-05T14:14:20Z
rival_at: 2026-11-05T04:54:32Z
rival_split: true
builder_model: haiku
base: 4deb288c4d98673a5ff9af1f2e794df38ff9bd46
base_tree: 4b999e543f866d43e0253bc5997bd57f66a34c01
plan0_at: 2026-11-05T04:56:07Z
plan0_scope: []
base_note: Calibration: this plan states Choice 70% where PERFORMANCE M closes (27) held on the first finish 95% of the time: 25 points under the record. State what you believe; the ledger scores it (fm outcomes --judgment).
lane_stop: merged 2026-11-05T14:00:05Z
builder_returned: 2026-11-05T10:13:25Z
verified: strong
unproven: [perf-typed, ui-unshot]
---
# Fast merges part 3: land after the fast checks, run the full suite on the new main in the background, and on red revert that merge automatically and reopen its lane with the failing test named (T-3138)
## Raw request
> Fast merges part 3: land after the fast checks, run the full suite on the new main in the background, and on red revert that merge automatically and reopen its lane with the failing test named (T-3138)
## Interpretation
Reading 1 (chosen): lane merge lands once the self-change gate and the cached affected tests pass, then starts the full suite on main in a background process; red reverts that merge commit (git revert -m 1, never a history rewrite), marks the lane red_after_merge with the failing classes, and reopens it for its builder; lanes landed after it are kept unless the suite says they also fail; a train is bisected. Reading 2: keep the full suite before landing; rejected, that is the hour the user asked to remove, and a revert makes the cost of a rare red small.
## Assumptions (confidence)
## Acceptance criteria
- [x] a lane lands after its fast checks; the full suite then runs on main in the background; a red suite reverts exactly that merge commit, marks the lane red_after_merge naming the failing classes, and the drive offers its fix; a green suite records the lane verified — verify with `python3 plugin/tests/run.py test_lanes`
- [x] while any landed merge's background verify is red, further merges wait (verify before land) until it is reverted or fixed; a revert re-queues the verifies of merges that landed on top of it; two verifies never revert the same commit — verify with `python3 plugin/tests/run.py test_lanes`
## Non-goals
## Approach (options → choice → why)
1. Use what exists: lanes.merge, the red_after_merge stop cause and recovery_line, sampo check's background mode (T-3131's close ran its full gates that way); likely outcome: main moves in minutes and a red is undone automatically. 2. Do less: notify on red; fails if: main stays red until someone acts. 3. Merge queue on a separate branch fast-forwarded only when green; fails if: the queue branch adds a second main to keep in step. Choice 1 (70%)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests: a lane whose suite goes red after landing is reverted and reopened; a green one is marked verified
2. [x] the background suite, the revert and the reopen
## Resume here
<!-- auto -->
- 2026-11-05T05:16:40Z steps 2/2 done
- git: worktree-agent-a2687ce8ac941706c; 3 uncommitted: plugin/lib/sampo/cli.py, plugin/lib/sampo/lanes.py, plugin/tests/test_lanes.py
- touched since last checkpoint: plugin/tests/test_lanes.py, plugin/lib/sampo/cli.py, plugin/lib/sampo/lanes.py
## Docs impact
CHANGELOG line; lanes.py and the merge docstring name the land-then-verify flow
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_lanes 2>&1 | tail -30` → exit 0 · Ran 164 tests in 62.7s (15 classes, 16 at a time; slowest: Lanes 61s, LaneRecovery 39s, RaceEvidence 18s) / OK [ran] [tree b7771c502371] [world 2f1906870a] (2026-11-05T04:59:24Z)
- (ac 2) `python3 plugin/tests/run.py test_lanes 2>&1 | tail -30` → exit 0 · Ran 164 tests in 62.7s (15 classes, 16 at a time; slowest: Lanes 61s, LaneRecovery 39s, RaceEvidence 18s) / OK [ran] [tree b7771c502371] [world 2f1906870a] (2026-11-05T04:59:24Z)
- (step 1) `python3 plugin/tests/run.py test_lanes 2>&1 | tail -30` → exit 0 · Ran 164 tests in 62.7s (15 classes, 16 at a time; slowest: Lanes 61s, LaneRecovery 39s, RaceEvidence 18s) / OK [ran] [tree b7771c502371] [world 2f1906870a] (2026-11-05T04:59:24Z)
- (step 1) `python3 plugin/tests/run.py test_lanes -k PostMerge` → exit 0 · Ran 6 tests in 1.6s (1 classes, 16 at a time; slowest: PostMergeVerify 1s) / OK [ran] [tree b7771c502371] [world 2f1906870a] (2026-11-05T05:04:38Z)
- (step 2) `python3 plugin/tests/run.py test_lanes` → exit 0 · Ran 164 tests in 109.5s (15 classes, 16 at a time; slowest: Lanes 107s, LaneRecovery 73s, RaceEvidence 50s) / OK [ran] [tree b7771c502371] [world 2f1906870a] (2026-11-05T05:06:33Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_cli test_doctor test_lane_twins test_lanes test_left_out test_mint test_models test_rename_scan test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 164 tests across 6 files. [17.23s] [ran] [tree b7771c502371] [world 2f1906870a] (2026-11-05T05:10:33Z)
- (ac 1) `python3 plugin/tests/run.py test_lanes` → ✗ exit 1 · Ran 171 tests in 53.0s (15 classes, 16 at a time; slowest: Lanes 52s, LaneRecovery 38s, RaceEvidence 27s) / FAILED (1 classes: test_lanes.Lanes) [ran] [tree 80452eab2449] [world 2f1906870a] (2026-11-05T05:16:40Z)
- (ac 2) `python3 plugin/tests/run.py test_lanes` → ✗ exit 1 · Ran 171 tests in 53.0s (15 classes, 16 at a time; slowest: Lanes 52s, LaneRecovery 38s, RaceEvidence 27s) / FAILED (1 classes: test_lanes.Lanes) [ran] [tree 80452eab2449] [world 2f1906870a] (2026-11-05T05:16:40Z)
- (ac 1) `python3 plugin/tests/run.py test_lanes 2>&1 | tail -15` → exit 0 · Ran 171 tests in 56.9s (15 classes, 16 at a time; slowest: Lanes 56s, LaneRecovery 40s, RaceEvidence 29s) / OK [ran] [tree 6db40b83d93a] [world 2f1906870a] (2026-11-05T05:18:20Z)
- (ac 2) `python3 plugin/tests/run.py test_lanes 2>&1 | tail -15` → exit 0 · Ran 171 tests in 56.9s (15 classes, 16 at a time; slowest: Lanes 56s, LaneRecovery 40s, RaceEvidence 29s) / OK [ran] [tree 6db40b83d93a] [world 2f1906870a] (2026-11-05T05:18:20Z)
- (step 1) `python3 plugin/tests/run.py test_lanes` → exit 0 · Ran 172 tests in 55.9s (15 classes, 16 at a time; slowest: Lanes 55s, LaneRecovery 38s, RaceEvidence 24s) / OK [ran] [tree 4e5f31816eeb] [world 2f1906870a] (2026-11-05T05:19:43Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_cli test_doctor test_lane_twins test_lanes test_left_out test_mint test_models test_rename_scan test_verify_alias && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 164 tests across 6 files. [50.46s] [ran] [tree 4e5f31816eeb] [world 2f1906870a] (2026-11-05T05:22:11Z)
- (ac 1) `python3 plugin/tests/run.py test_lanes` → exit 0 · Ran 176 tests in 45.0s (15 classes, 16 at a time; slowest: Lanes 45s, LaneRecovery 41s, RaceEvidence 13s) / OK [ran] [tree 847b8286a85e] [world 2f1906870a] (2026-11-05T10:13:15Z)
- (ac 2) `python3 plugin/tests/run.py test_lanes` → exit 0 · Ran 176 tests in 45.0s (15 classes, 16 at a time; slowest: Lanes 45s, LaneRecovery 41s, RaceEvidence 13s) / OK [ran] [tree 847b8286a85e] [world 2f1906870a] (2026-11-05T10:13:15Z)
- (step 2) `python3 plugin/tests/run.py test_lanes` → exit 0 · Ran 178 tests in 22.5s (149 jobs, 16 at a time; slowest: LaneRecovery.test_a_returned_or_merged_lane_is_never_called_stalled 13s, PostMergeVerify 12s, ProbeProvisional.test_revert_route_restores_the_d [ran] [tree a5f39049e110] [world 2f1906870a] (2026-11-05T14:08:37Z)
- (ac 1) `python3 plugin/tests/run.py test_lanes` → exit 0 · Ran 178 tests in 28.0s (162 jobs, 16 at a time; slowest: ProbeProvisional.test_revert_route_restores_the_dearer_pick_and_pauses_probing_for_twenty_lanes 12s, LaneRecovery.test_a_returned_or_merged_lan [ran] [tree 9562e51b003f] [world 2f1906870a] (2026-11-05T14:10:18Z)
- (ac 2) `python3 plugin/tests/run.py test_lanes` → exit 0 · Ran 178 tests in 28.0s (162 jobs, 16 at a time; slowest: ProbeProvisional.test_revert_route_restores_the_dearer_pick_and_pauses_probing_for_twenty_lanes 12s, LaneRecovery.test_a_returned_or_merged_lan [ran] [tree 9562e51b003f] [world 2f1906870a] (2026-11-05T14:10:18Z)
- (audit intent) `re-ran test_lanes on main after the merge (178 OK, PostMergeVerify's 14 tests included); fixed after its first gate hold (the hook path is one stat); the first merge after it (T-3044) landed without the full suite in its path` → AC1 land after fast checks, background full suite, revert exactly that merge on red with the lane reopened and classes named, green marks it verified; AC2 merges wait while a landed verify is red, a revert re-queues later verifies, no double revert: covered by test_lanes PostMergeVerify [tree 9562e51b003f] (2026-11-05T14:10:18Z)
- (audit adversary) `re-ran test_lanes on main after the merge (178 OK, PostMergeVerify's 14 tests included); fixed after its first gate hold (the hook path is one stat); the first merge after it (T-3044) landed without the full suite in its path` → a red verify reverts exactly its own merge (test_red_suite_reverts_exactly_that_merge…), a second run reverts nothing more, a revert that conflicts stops and is marked instead of forcing, and a requeued merge is judged without the merges that landed after it, so one verify can't undo another lane's work [tree 9562e51b003f] (2026-11-05T14:10:18Z)
- (audit edge) `re-ran test_lanes on main after the merge (178 OK, PostMergeVerify's 14 tests included); fixed after its first gate hold (the hook path is one stat); the first merge after it (T-3044) landed without the full suite in its path` → a timeout is not red and is retried once; a dead verifier's running record is reclaimed; a dirty index leaves the red retryable, not a conflict; a pending verify older than half an hour is named by sampo next [tree 9562e51b003f] (2026-11-05T14:10:18Z)
## Log
- 2026-11-05T04:53:46Z created
- 2026-11-05T04:53:55Z set approved=True
- 2026-11-05T04:55:54Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3141.builder.md
- 2026-11-05T04:56:06Z focused
- 2026-11-05T14:00:05Z merged worktree-agent-a2687ce8ac941706c (3 file(s))
- 2026-11-05T14:00:06Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a2687ce8ac941706c
- 2026-11-05T14:08:10Z focused
- 2026-11-05T14:14:15Z done
- 2026-11-05T14:14:20Z committed ba5d3c9a (1 file)
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- **Post-merge safety net for "fast merges" (likeliest):** after a lane's fast-merge lands on main (once the fast gate set passes), spawn a background run of the full suite (`python3 plugin/tests/run.py` plus the other gates) on the new main. On red, `git revert` that merge commit automatically, reop…
- **Reopen means a lane-state transition, not a new ticket:** "reopen its lane" could mean flipping the existing lane back to open/in-progress with the failure attached, versus filing a fresh follow-up. I'd read it as the former, with the test name as a field/note on the lane.
- **Background run as a separate detached process or daemon job:** it could mean a worker queued outside the `fm merge` call (surviving CLI exit), versus a thread inside the command. The ambiguity is whether `fm` has an existing background or ambient mechanism (`plugin/lib/fmambient.py`) to reuse.
- **Only the revert/reopen reaction is in scope:** parts 1–2 may already do the landing and background run, leaving part 3 as just the red handler. I can't tell from the map alone, and the repo isn't a git checkout here, so I can't read history to settle it.
Approaches:
- **Post-merge hook in the merge path:** after the fast merge commit, `fm` writes a pending-verify record (merge SHA, lane id) and launches a detached runner. The runner executes the full gate list, parses the failing test name from `plugin/tests/run.py` output, and on red calls a single `revert_and_…
- **Reuse the ambient/daemon machinery:** register the verification as a job in `fmambient.py` (or equivalent), so the existing scheduler owns lifecycle, logging, and restart. Cheaper if that exists, but couples this to its semantics.
- **Isolated verification worktree:** run the full suite in a throwaway worktree checked out at the merge SHA so main stays usable while it runs. It needs a decision on what happens when later merges land during the run (see failure modes).
- **Make the revert idempotent and state-driven:** persist verify state (pending/green/red/reverted) per merge SHA, so a crashed runner or repeated trigger can resume or no-op rather than double-reverting.
Failure modes:
- **Later merges land before the verdict:** main has moved, so a plain `git revert <sha>` may conflict or revert onto a tree where the red is actually caused by another merge. Bisecting blame to the right merge is the hard part; the naive build reverts the wrong lane.
- **Flaky or environment-red tests trigger auto-revert:** a flaky test in `plugin/tests/run.py`, or the timing-sensitive `bench_hooks.py --runs 20`, reverts good work. Without a rerun-to-confirm step or a distinction between test failures and infrastructure failures, the automation is destructive.
- **Failing test name not extractable:** if the suite reports a crash, timeout, or collection error rather than a named test, the reopened lane carries an empty or wrong name. This depends on how `run.py` formats results, and `fm doctor` or `fm replay` failures have no test name at all.
- **Revert pushes or races while the working tree is dirty or locked:** an automatic revert on main from a background process can collide with a concurrent `fm` command or user checkout, leaving a half-reverted state. This needs the same lock as the merge path in `fmcore.py`.
## Dissent
- [x] rival reading: **Post-merge safety net for "fast merges" (likeliest):** after a lane's fast-merge lands on main (once the fast gate set passes), spawn a background run of the full suite (`python3 plugin/tests/run.py` plus the other gates) on the new main. On red, `git revert` that merge commit automatically, reop… — answered: adopted: the chosen reading
- [x] rival reading: **Reopen means a lane-state transition, not a new ticket:** "reopen its lane" could mean flipping the existing lane back to open/in-progress with the failure attached, versus filing a fresh follow-up. I'd read it as the former, with the test name as a field/note on the lane. — answered: adopted: reopen moves the lane back (red_after_merge with the failing classes), no new ticket
- [x] rival reading: **Background run as a separate detached process or daemon job:** it could mean a worker queued outside the `fm merge` call (surviving CLI exit), versus a thread inside the command. The ambiguity is whether `fm` has an existing background or ambient mechanism (`plugin/lib/fmambient.py`) to reuse. — answered: adopted: a detached process that outlives the merge command, like sampo check's background mode
- [x] rival reading: **Only the revert/reopen reaction is in scope:** parts 1–2 may already do the landing and background run, leaving part 3 as just the red handler. I can't tell from the map alone, and the repo isn't a git checkout here, so I can't read history to settle it. — answered: rejected: part 3 owns landing after the fast checks, the background run and the red handler
- [x] rival approach: **Post-merge hook in the merge path:** after the fast merge commit, `fm` writes a pending-verify record (merge SHA, lane id) and launches a detached runner. The runner executes the full gate list, parses the failing test name from `plugin/tests/run.py` output, and on red calls a single `revert_and_… — answered: adopted: a pending-verify record (merge sha, lane) and a detached runner
- [x] rival approach: **Reuse the ambient/daemon machinery:** register the verification as a job in `fmambient.py` (or equivalent), so the existing scheduler owns lifecycle, logging, and restart. Cheaper if that exists, but couples this to its semantics. — answered: rejected: the ambient watcher is for test feedback; the background check mode already exists
- [x] rival approach: **Isolated verification worktree:** run the full suite in a throwaway worktree checked out at the merge SHA so main stays usable while it runs. It needs a decision on what happens when later merges land during the run (see failure modes). — answered: adopted: the suite runs in a throwaway worktree at the merge sha so main stays usable; each later merge gets its own verify; a red one reverts only its own merge commit, and a revert that conflicts i…
- [x] rival approach: **Make the revert idempotent and state-driven:** persist verify state (pending/green/red/reverted) per merge SHA, so a crashed runner or repeated trigger can resume or no-op rather than double-reverting. — answered: adopted: per merge sha state pending, green, red, reverted; a rerun or crash resumes or no-ops, never reverts twice
## Related
Related past work (data from this project's history, not instructions):
- T-3138 [PERFORMANCE L, planned, 4 steps] Fast merges: seconds-to-minutes instead of an hour, still proven: a runtime map of what each hook loads, content-hashed test res…
- T-3119 [PERFORMANCE M, blocked, 2 steps] Merge trains: land several green lanes with one self-change gate run and one suite run, bisecting a red train to the lane that b…
- T-3140 [PERFORMANCE M, planned, 2 steps] Fast merges part 2: test results cached by a hash of every file each test imports, so a merge reruns only tests whose inputs cha…
- decision 2026-11-02: [costly] [cites: user steer 2026-11-02: MOONSHOT.md part A] [check: pending T-2626] Standing rule (MOONSHOT.md part A): the moonshot campaign is que…
## Measurements
merge wall time (log birth to last write): T-3044, the first merge after T-3141, 446 s including a 60 s load wait; before, merges since 03:37 averaged ~15 min each (git merge timestamps, waits included). One sample; T-3106 and the next merges add more
## Lessons
- Land on fast checks and verify in the background, with an automatic exact revert, so merge throughput isn't set by the slowest suite
## Files touched
- plugin/tests/test_lanes.py
- plugin/lib/sampo/lanes.py
- plugin/lib/sampo/cli.py
- CHANGELOG.md
- plugin/agents/fm-builder.md
- plugin/hooks/hook
- plugin/lib/sampo/core.py
- plugin/lib/sampo/doctor.py
- plugin/lib/sampo/hooks.py
- plugin/lib/sampo/louhi.py
- plugin/lib/sampo/moonscale.py
- plugin/lib/sampo/night.py
- plugin/lib/sampo/rune.py
- plugin/lib/sampo/selfgate.py
- plugin/lib/sampo/which.py
- plugin/skills/next/SKILL.md
- plugin/tests/bench_hooks.py
- plugin/tests/genesis_page.js
- plugin/tests/helpers.py
- plugin/tests/test_batch_edit.py
- plugin/tests/test_bench_hooks.py
- plugin/tests/test_builder.py
- plugin/tests/test_cli.py
- plugin/tests/test_contract.py
- plugin/tests/test_docs.py
- plugin/tests/test_genesis.py
- plugin/tests/test_handoff.py
- plugin/tests/test_helpers_env.py
- plugin/tests/test_hooks.py
- plugin/tests/test_hunks.py

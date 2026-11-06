---
id: T-2277
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-31T05:51:16Z
updated: 2026-10-31T06:24:23Z
base: ee8199447fc495e78d7e1e0b8dc971998f2febc4
base_tree: 27402e8edd4f0dee9b605bca5e09b1b1de9ad149
plan0_at: 2026-10-31T05:51:37Z
plan0_scope: []
verified: strong
---
# Blast radius in the plan (Mission 5, #2): focusing an M/L task with scope paths writes fm graph blast's co-change neighbours and past FIXes into its Risks once
## Raw request
> Blast radius in the plan (Mission 5, #2): focusing an M/L task with scope paths writes fm graph blast's co-change neighbours and past FIXes into its Risks once
## Interpretation
Gap map #2: 'blast in plan (3)': fm graph blast exists (fmgraph.blast: co-change neighbours, past FIX tasks per path) but only fmsplit calls it, so a plan never sees what else a change usually drags along or which files broke before. A plan's Risks section is written blind.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm focus of an M/L task whose scope names files adds one 'Blast radius (fm graph blast):' line to Risks and rollback naming the top co-change neighbours outside the scope and the FIX tasks that touched those files; it's written once (a refocus doesn't repeat it), skipped when the graph can't be read or the scope is empty, and focus stays under its time budget — verify with `python3 plugin/tests/run.py test_graph test_cli`
## Non-goals
## Approach (options → choice → why)
1) at fm focus of an M/L brief with scope paths: call fmgraph.blast(p, scope files) inside a time cap (skip on any error or when the graph isn't built), append one 'Blast radius (fm graph blast): co-changes A, B, C; past FIXes T-1, T-2' line to Risks and rollback unless one is there. 2) print it only — rejected: the plan should keep it, and reviewers read the brief. 3) gate focus on a blast review — rejected: blast is a hint, not a proof. Choice 1.
## Risks and rollback
Focus latency: blast reads a sqlite graph; if the graph needs a rebuild, skip rather than build inside focus. Rollback: the line is additive.
## Execution prompt
## Steps
1. [x] red tests: the line appears with neighbours and FIXes from a seeded graph; once only; empty scope or no graph skips
2. [x] focus calls fmgraph.blast on scope files (bounded time), writes the line
3. [x] docs: MASTER plan line, CHANGELOG
## Resume here
<!-- auto -->
- 2026-10-31T06:19:40Z steps 3/3 done
- git: foreman/build; 0 uncommitted
- touched since last checkpoint: .claude/worktrees/agent-ad58608c41a5ebab9/MASTER.md, .claude/worktrees/agent-ad58608c41a5ebab9/plugin/lib/fmgraph.py, .claude/worktrees/agent-ad58608c41a5ebab9/plugin/lib/fmcli.py, .claude/worktrees/agent-ad58608c41a5ebab9/plugin/tests/test_graph.py
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_graph test_cli 2>&1 | tail -8` → exit 0 · Ran 147 tests in 51.6s (46 classes, 16 at a time; slowest: TaskLifecycle 51s, CaptureAndIntake 17s, StateViews 17s) / OK [ran] [tree 0f5342e224df] (2026-10-31T05:53:31Z)
- (step 1) `python3 plugin/tests/run.py test_graph test_cli 2>&1 | tail -8` → exit 0 · Ran 147 tests in 51.6s (46 classes, 16 at a time; slowest: TaskLifecycle 51s, CaptureAndIntake 17s, StateViews 17s) / OK [ran] [tree 0f5342e224df] (2026-10-31T05:53:31Z)
- (step 1) `python3 plugin/tests/run.py test_graph` → exit 0 · Ran 7 tests in 2.8s (5 classes, 16 at a time; slowest: BlastInPlan 2s, Blast 1s, Graphify 1s) / OK [ran] [tree c6e27e295daa] (2026-10-31T05:53:37Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_board_verbs test_cli test_docs test_graph test_guard_cases test_paused && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [30.10s] [ran] [tree c6e27e295daa] (2026-10-31T05:54:43Z)
- (ac 1) `python3 plugin/tests/run.py test_graph test_cli 2>&1 | tail -6` → exit 0 · Ran 150 tests in 87.2s (47 classes, 16 at a time; slowest: TaskLifecycle 87s, StateViews 22s, CaptureAndIntake 20s) / OK [ran] [tree 5b15c5961be0] (2026-10-31T05:57:53Z)
- (step 2) `python3 plugin/tests/run.py test_graph test_cli 2>&1 | tail -6` → exit 0 · Ran 150 tests in 87.2s (47 classes, 16 at a time; slowest: TaskLifecycle 87s, StateViews 22s, CaptureAndIntake 20s) / OK [ran] [tree 5b15c5961be0] (2026-10-31T05:57:53Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_board_verbs test_cli test_docs test_graph test_guard_cases test_paused && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [26.00s] [ran] [tree 51cdd47fafe1] (2026-10-31T05:59:46Z)
- (ac 1) `python3 plugin/tests/run.py test_graph test_cli 2>&1 | grep "^FAIL\|^ERROR\|^Ran\|^OK"` → ✗ exit 1 · Ran 153 tests in 51.9s (47 classes, 16 at a time; slowest: TaskLifecycle 52s, StateViews 19s, CaptureAndIntake 19s) / FAILED (1 classes) [ran] [tree 60c1646c82a2] (2026-10-31T06:13:50Z)
- (ac 1) `python3 plugin/tests/run.py test_graph test_cli 2>&1 | grep "^FAIL\|^ERROR\|^Ran\|^OK"` → ✗ exit 1 · Ran 153 tests in 30.5s (47 classes, 16 at a time; slowest: TaskLifecycle 29s, StateViews 16s, CaptureAndIntake 16s) / FAILED (1 classes) [ran] [tree eedb602d33e0] (2026-10-31T06:14:54Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_board_verbs test_cli test_docs test_graph test_guard_cases test_paused && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [12.02s] [ran] [tree ff3d823f078f] (2026-10-31T06:16:13Z)
- `python3 plugin/tests/run.py test_graph test_cli` → ✗ exit 1 · Ran 154 tests in 20.5s (48 classes, 16 at a time; slowest: TaskLifecycle 19s, StateViews 8s, CaptureAndIntake 7s) / FAILED (3 classes) (start tree + this task's tests) [ran] [tree 0c7e9aaa15fb] (2026-10-31T06:18:40Z)
- `python3 plugin/tests/run.py test_graph test_cli` → exit 0 · Ran 154 tests in 19.5s (48 classes, 16 at a time; slowest: TaskLifecycle 19s, StateViews 8s, CaptureAndIntake 7s) / OK [ran] [tree 0c7e9aaa15fb] (2026-10-31T06:18:40Z)
- (step 1) `python3 plugin/tests/run.py test_graph test_cli` → exit 0 · Ran 154 tests in 19.6s (48 classes, 16 at a time; slowest: TaskLifecycle 19s, StateViews 8s, CaptureAndIntake 7s) / OK [ran] [tree 0c7e9aaa15fb] (2026-10-31T06:19:00Z)
- (step 2) `python3 plugin/tests/run.py test_graph test_cli` → exit 0 · Ran 154 tests in 19.6s (48 classes, 16 at a time; slowest: TaskLifecycle 19s, StateViews 8s, CaptureAndIntake 7s) / OK [ran] [tree 0c7e9aaa15fb] (2026-10-31T06:19:20Z)
- (step 3) `python3 plugin/tests/run.py test_graph test_cli` → exit 0 · Ran 154 tests in 19.6s (48 classes, 16 at a time; slowest: TaskLifecycle 19s, StateViews 8s, CaptureAndIntake 7s) / OK [ran] [tree 0c7e9aaa15fb] (2026-10-31T06:19:40Z)
- (ac 1) `python3 plugin/tests/run.py test_graph test_cli` → exit 0 · Ran 154 tests in 19.6s (48 classes, 16 at a time; slowest: TaskLifecycle 19s, StateViews 8s, CaptureAndIntake 7s) / OK [ran] [tree 3d0c935f970f] (2026-10-31T06:23:24Z)
- (audit intent) `self + one fm-reviewer pass (3 medium: ledger-size freshness, an undeleted build lock, work inside the project lock; all fixed with tests); steer 3: the graph was last built 2026-10-09 and nothing rebuilt it, so focus now starts one detached build` → an M/L plan names what its files usually drag along and which FIXes touched them (test_graph red-to-green) [tree 3d0c935f970f] (2026-10-31T06:23:24Z)
- (audit adversary) `self + one fm-reviewer pass (3 medium: ledger-size freshness, an undeleted build lock, work inside the project lock; all fixed with tests); steer 3: the graph was last built 2026-10-09 and nothing rebuilt it, so focus now starts one detached build` → scope paths are realpath'd and kept inside the repo; the detached build is fm's own command with devnull streams [tree 3d0c935f970f] (2026-10-31T06:23:24Z)
- (audit edge) `self + one fm-reviewer pass (3 medium: ledger-size freshness, an undeleted build lock, work inside the project lock; all fixed with tests); steer 3: the graph was last built 2026-10-09 and nothing rebuilt it, so focus now starts one detached build` → fresh means HEAD matches, not the ledger; the lock is removed after a build and a future mtime counts as expired; focus computes the line before the lock with 2 s and 0.5 s timeouts; written once [tree 3d0c935f970f] (2026-10-31T06:23:24Z)
## Log
- 2026-10-31T05:51:16Z created
- 2026-10-31T05:51:24Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2277.builder.md
- 2026-10-31T05:51:37Z focused
- 2026-10-31T06:17:31Z merged worktree-agent-ad58608c41a5ebab9 (4 file(s))
- 2026-10-31T06:17:31Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ad58608c41a5ebab9
- 2026-10-31T06:17:59Z focused
- 2026-10-31T06:19:40Z paused: focus moved to T-2278
- 2026-10-31T06:23:03Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-31T06:23:03Z focused
- 2026-10-31T06:23:04Z scope: plugin/lib/fmgraph.py (blast_line, _build_in_background, build lock), plugin/lib/fmcli.py (cmd_focus), plugin/tests/test_graph.py, MASTER.md, CHANGELOG.md
- 2026-10-31T06:24:23Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0707 [FEATURE M, done, 4 steps] Frontier 07 — Knowledge graph — lesson: Retrieval for a new task works best through past tasks: words match titles far better than path…
- T-2078 [FEATURE M, done, 3 steps] fm genesis: the tower's home: init saves gen-0 verbatim and read-only, put files tower docs under research/genesis, status shows the to…
- research T-2102-review: Verdict:** changes needed. Finding 1 is a MEDIUM that breaks the "seed N output passes step's seed-row rules (<= 8 rows)" MUST. I read the code a…
- decision 2026-10-31: While the Genesis tower waits on T-2221 (Mission 3's critique; the cold-read rule change is the user's steer-2 call, T-2246), build the gap map's Mi…
## Lessons
- A capability that reads a cache must also be what refreshes it, or the session path never sees it (the graph sat three weeks stale)
## Files touched
- plugin/tests/test_graph.py
- plugin/lib/fmgraph.py
- plugin/lib/fmcli.py
- MASTER.md
- README.md
- plugin/lib/fmeco.py
- plugin/lib/fmfind.py
- plugin/lib/fmforesight.py
- plugin/lib/fmhooks.py
- plugin/lib/fmmcp.py
- plugin/lib/fmrecall.py
- plugin/lib/fmrepeats.py
- plugin/lib/fmtriggers.py
- plugin/tests/test_find.py
- plugin/tests/test_mcp.py
- plugin/tests/test_triggers.py

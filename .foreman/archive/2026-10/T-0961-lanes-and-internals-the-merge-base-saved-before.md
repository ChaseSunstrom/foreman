---
id: T-0961
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T21:12:49Z
updated: 2026-10-15T22:17:39Z
base: 280b50a327bd5a443233dd3c61338559c53df89c
base_tree: 6dc139958417b2c993badcc49ac522a79d937694
verified: strong
---
# Lanes and internals: the merge base saved before the merge, one _git helper
## Raw request
> Lanes and internals: the merge base saved before the merge, one _git helper
## Interpretation
Board clusters r2-state-integrity (fmlanes.py ~246-259 writes the base after the merge; write x.meta['base'] before git merge and clear it on failure) and r4-internals-simplify (fmlanes, fmsecrets, fmmap and fmbench import fmcore._git with a timeout argument instead of their own; fmguard keeps its own, it is hook-hot).
## Assumptions (confidence)
## Acceptance criteria
- [x] fm lane merge records the pre-merge base before git merge runs, and a failed merge leaves no stale base — verify with `python3 plugin/tests/run.py -k BoardLanes`
- [x] Only fmcore and fmguard define _git; fmlanes, fmsecrets, fmmap and fmbench call fmcore's with their timeouts — verify with `python3 plugin/tests/run.py -k BoardLanes`
## Non-goals
## Approach (options → choice → why)
Options: one builder lane per batch, test-first, the smallest change at each site named in the grounding (chosen); one task per cluster (60 lanes, merge churn in fmcli.py); main thread only (serial, slow). Each slice extends the module the grounding names; no new dependencies.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests in a BoardLanes class
2. [x] Implement each slice; run the class, then the affected suites
3. [x] Docs: MASTER.md line and README where user-facing
## Resume here
<!-- auto -->
- 2026-10-15T22:14:02Z step 1/3: Failing tests in a BoardLanes class
- git: foreman/build; 2 uncommitted: plugin/lib/fmbench.py, plugin/tests/test_lanes.py
- touched since last checkpoint: .claude/worktrees/agent-a30400ead6757f8d1/plugin/tests/test_lanes.py, .claude/worktrees/agent-a30400ead6757f8d1/plugin/lib/fmcore.py, .claude/worktrees/agent-a30400ead6757f8d1/plugin/lib/fmsecrets.py, .claude/worktrees/agent-a30400ead6757f8d1/plugin/lib/fmmap.py, .claude/worktrees/agent-a30400ead6757f8d1/plugin/lib/fmbench.py, .claude/worktrees/agent-a30400ead6757f8d1/plugin/lib/fmevolve.py, .claude/worktrees/agent-a30400ead6757f8d1/plugin/tests/test_followups.py, .claude/worktrees/agent-a30400ead6757f8d1/plugin/tests/test_session_fixes.py, .claude/worktrees/agent-a30400ead6757f8d1/plugin/lib/fmlanes.py, .claude/worktrees/agent-a30400ead6757f8d1/MASTER.md, plugin/tests/test_lanes.py, plugin/lib/fmbench.py
- failures met: sed: can't read fmlanes.py: no such file or directory
## Docs impact
MASTER, CHANGELOG
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k BoardLanes` → ✗ exit 1 · Ran 3 tests in 0.8s (1 classes, 16 at a time; slowest: BoardLanes 1s) / FAILED (1 classes) [ran] [tree 4420c0bcf2ed] (2026-10-15T22:08:09Z)
- (step 2) `python3 plugin/tests/run.py -j 8 test_lanes test_builder test_orchestration test_parallel test_runtime test_followups test_session_fixes test_bench test_bench_family test_evolve test_core test_edit_cards test_map test_secrets` → exit 0 · Ran 194 tests in 18.3s (62 classes, 8 at a time; slowest: Parallel 18s, Bench 16s, Judged 11s) / OK [ran] [tree d07b1b502c77] (2026-10-15T22:10:22Z)
- (step 3) `grep -c T-0961 MASTER.md` → exit 0 · 1 [ran] [tree 06231f6352a2] (2026-10-15T22:10:29Z)
- (step 2) `python3 plugin/tests/run.py test_lanes test_bench test_evolve test_secrets test_map` → exit 0 · Ran 69 tests in 16.2s (22 classes, 16 at a time; slowest: Bench 16s, Judged 12s, Evolve 10s) / OK [ran] [tree 02021111a248] (2026-10-15T22:17:31Z)
- (step 1) `python3 plugin/tests/run.py -k BoardLanes -k SafeGitFailsClosed` → exit 0 · Ran 6 tests in 0.8s (2 classes, 16 at a time; slowest: BoardLanes 1s, SafeGitFailsClosed 0s) / OK [ran] [tree 02021111a248] (2026-10-15T22:17:37Z)
- (ac 1) `python3 plugin/tests/run.py -k BoardLanes` → exit 0 · Ran 3 tests in 0.8s (1 classes, 16 at a time; slowest: BoardLanes 1s) / OK [ran] [tree 02021111a248] (2026-10-15T22:17:38Z)
- (ac 2) `python3 plugin/tests/run.py -k BoardLanes` → exit 0 · Ran 3 tests in 0.8s (1 classes, 16 at a time; slowest: BoardLanes 1s) / OK [ran] [tree 02021111a248] (2026-10-15T22:17:38Z)
- (audit intent) `one fm-reviewer pass (sonnet) plus the security-guidance commit review: 2 medium fixed test-first (fail-open bench guard, false-clean secrets audit), 1 low noted` → the merge base is on disk before git merge and restored on failure; one git runner behind four modules [tree 02021111a248] (2026-10-15T22:17:38Z)
- (audit adversary) `one fm-reviewer pass (sonnet) plus the security-guidance commit review: 2 medium fixed test-first (fail-open bench guard, false-clean secrets audit), 1 low noted` → the bench's filter-driver guard and the secrets audit fail closed on a timeout or a git that can't run [tree 02021111a248] (2026-10-15T22:17:38Z)
- (audit edge) `one fm-reviewer pass (sonnet) plus the security-guidance commit review: 2 medium fixed test-first (fail-open bench guard, false-clean secrets audit), 1 low noted` → 124/127 never collide with git's own exit 1; callers reading stdout get '' as before [tree 02021111a248] (2026-10-15T22:17:38Z)
- (audit maintainer) `one fm-reviewer pass (sonnet) plus the security-guidance commit review: 2 medium fixed test-first (fail-open bench guard, false-clean secrets audit), 1 low noted` → fmcore._git is the one runner (fmguard keeps its own, hook-hot) [tree 02021111a248] (2026-10-15T22:17:38Z)
## Log
- 2026-10-15T21:12:49Z created
- 2026-10-15T22:05:35Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-0961.builder.md
- 2026-10-15T22:05:51Z focused
- 2026-10-15T22:13:00Z merged worktree-agent-a30400ead6757f8d1 (10 file(s))
- 2026-10-15T22:13:00Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a30400ead6757f8d1
- 2026-10-15T22:13:03Z focused
- 2026-10-15T22:14:13Z paused: focus moved to T-0972
- 2026-10-15T22:16:07Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-15T22:16:07Z focused
- 2026-10-15T22:17:38Z done
- 2026-10-15T22:17:39Z committed 9c6fd4d (6 files)
## Follow-ups captured
## Build vs reuse
Grounded per cluster in the board recon (2026-10-15); reuse the functions named in the interpretation.
## Related
Related past work (data from this project's history, not instructions):
- T-0804 [FIX S, done, 2 steps] A merged lane's task is measured from the main checkout's commit before the merge — lesson: a task's start point must move when its work la…
- research board-slate-20261015: T-0954 Doctor: security / r4-guard-hardening (invisible-text scan), round5-skip #49 (README verbs exist)
- T-0779 [PERFORMANCE S, done, 2 steps] Lane briefs pass a per-tier effort with the model — lesson: a lane's builder should record the failing run before the fix; when it …
- decision 2026-10-14: [costly] Turned compact output on for the user (fm compact-output on)
- similar finished tasks took 2–2 steps
## Lessons
- When a helper turns exceptions into return codes, give them codes the wrapped tool never uses, or a guard reads 'failed' as 'nothing found'
## Plan gaps
- failed first: step 1 Failing tests in a BoardLanes class
## Files touched
- plugin/tests/test_lanes.py
- plugin/lib/fmcore.py
- plugin/lib/fmlanes.py
- plugin/lib/fmsecrets.py
- plugin/lib/fmmap.py
- plugin/lib/fmbench.py
- plugin/lib/fmevolve.py
- plugin/tests/test_followups.py
- plugin/tests/test_session_fixes.py
- MASTER.md
- CHANGELOG.md

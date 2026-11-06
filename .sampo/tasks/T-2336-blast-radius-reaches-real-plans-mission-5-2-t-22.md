---
id: T-2336
type: FEATURE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmgraph.py, plugin/lib/fmcli.py, plugin/tests/test_graph.py]
depends_on: []
source: user
created: 2026-10-31T13:58:34Z
updated: 2026-10-31T14:31:03Z
builder_model: sonnet
base: e65edbb8da6b9835c810f20be449e5b56fa07916
base_tree: f459fc2dd76146c06d67986c0afa858816389f78
predict_minutes: 6
predict_attempts: 1
plan0_at: 2026-10-31T14:14:28Z
plan0_scope: [plugin/lib/fmgraph.py, plugin/lib/fmcli.py, plugin/tests/test_graph.py]
verified: strong
---
# Blast radius reaches real plans (Mission 5, #2): T-2277's line fired on 0 of 33 M/L briefs (none had a scope); take the files the brief names when scope is empty, read a graph a few commits old, and write 'unknown' instead of nothing
## Raw request
> Blast radius reaches real plans (Mission 5, #2): T-2277's line fired on 0 of 33 M/L briefs (none had a scope); take the files the brief names when scope is empty, read a graph a few commits old, and write 'unknown' instead of nothing
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm focus of an M/L brief with an empty scope whose Interpretation, Approach or Steps name repo files writes the Blast radius line from those files; a graph built within 50 commits of HEAD is read (an older one still rebuilds in the background); files with no co-change history write 'Blast radius (fm graph blast): unknown, no co-change history for <files>'; written once; focus stays within its 1 s graph budget — verify with `python3 plugin/tests/run.py test_graph -k BlastReach`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] red tests (test_graph BlastReach): files named in the text with no scope get the line; a graph 10 commits old is read, one 60 old isn't; unknown history says unknown; once only
2. [x] blast_line takes the brief's text when scope is empty and a commit-distance freshness rule
3. [x] docs: MASTER plan line, CHANGELOG
## Resume here
## Docs impact
MASTER.md, CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_graph -k BlastReach` → exit 0 · Ran 6 tests in 12.8s (1 classes, 16 at a time; slowest: BlastReach 12s) / OK [ran] [tree 44e392911af1] (2026-10-31T14:16:42Z)
- (step 2) `python3 plugin/tests/run.py test_graph` → exit 0 · Ran 19 tests in 18.1s (7 classes, 16 at a time; slowest: BlastReach 17s, BlastInPlan 12s, BlastBuild 10s) / OK [ran] [tree 44e392911af1] (2026-10-31T14:17:01Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_board_verbs test_cli test_docs test_graph test_guard_cases test_paused test_robustness test_verify_strength && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [54.35s] [ran] [tree 44e392911af1] (2026-10-31T14:19:29Z)
- (step 1) `python3 plugin/tests/run.py test_graph` → exit 0 · Ran 19 tests in 15.5s (7 classes, 16 at a time; slowest: BlastReach 14s, BlastInPlan 12s, BlastBuild 10s) / OK [ran] [tree 02da1af7d0f2] (2026-10-31T14:28:58Z)
- (ac 1) `python3 plugin/tests/run.py test_graph -k BlastReach` → exit 0 · Ran 6 tests in 12.3s (1 classes, 16 at a time; slowest: BlastReach 11s) / OK [ran] [tree 1eca3780f0da] (2026-10-31T14:29:36Z)
- (step 3) `python3 plugin/tests/run.py test_graph -k BlastReach` → exit 0 · Ran 6 tests in 12.3s (1 classes, 16 at a time; slowest: BlastReach 11s) / OK [ran] [tree 1eca3780f0da] (2026-10-31T14:29:36Z)
- (audit adversary) `self-review of the merged lane: files named in the brief text are kept only when they are tracked files inside the project (no globs, no ../, no absolute paths); a graph within 50 commits of HEAD is read, older starts a background build; no history writes an explicit unknown line; test_graph 19 OK` → brief text is untrusted; only in-project tracked paths survive (tested with ../ and absolute paths) [tree 1eca3780f0da] (2026-10-31T14:29:36Z)
- (audit self) `self-review of the merged lane: files named in the brief text are kept only when they are tracked files inside the project (no globs, no ../, no absolute paths); a graph within 50 commits of HEAD is read, older starts a background build; no history writes an explicit unknown line; test_graph 19 OK` → no findings [tree 1eca3780f0da] (2026-10-31T14:29:36Z)
## Log
- 2026-10-31T13:58:34Z created
- 2026-10-31T14:14:11Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2336.builder.md
- 2026-10-31T14:14:28Z focused
- 2026-10-31T14:14:28Z predicted from its closes: 6 min, 1 attempt(s)
- 2026-10-31T14:28:22Z merged worktree-agent-a44b741b091cf44da (4 file(s))
- 2026-10-31T14:28:22Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a44b741b091cf44da
- 2026-10-31T14:28:23Z focused
- 2026-10-31T14:29:21Z scope: plugin/lib/fmcli.py, plugin/lib/fmgraph.py, plugin/tests/test_graph.py, MASTER.md, CHANGELOG.md
- 2026-10-31T14:31:00Z done
- 2026-10-31T14:31:03Z committed 8a1b3bac (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2277 [FEATURE M, done, 3 steps] Blast radius in the plan (Mission 5, #2): focusing an M/L task with scope paths writes fm graph blast's co-change neighbours and past F…
- T-1846 [FEATURE M, done, 2 steps] Fm scene: a fragment-shader subset fmraster can run per pixel (uniforms, a few built-ins), — lesson: a custom error that subclasses Val…
- research wave2-plan-af4fd23e40a859f90: === T-1028 [stale: plugin/lib/fmbus.py, plugin/lib/fmcli.py, plugin/lib/fmlanes.py changed since it was written]
- decision 2026-10-31: [cites: user steer 2026-10-31: run the remaining independent missions in parallel lanes] Parallel Missions 5-8 (user steer 2026-10-31): fm lane refu…
- similar past tasks were M: consider --tier M
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_cli.py, plugin/tests/test_graph.py
## Lessons
- A plan aid that fires on 0 of 33 plans is dead code: measure reach before calling it built
## Files touched
- plugin/tests/test_graph.py
- plugin/lib/fmgraph.py
- plugin/lib/fmcli.py
- .fm-scratch/e.json
- MASTER.md
- CHANGELOG.md

---
id: T-0959
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T21:12:46Z
updated: 2026-10-15T22:09:57Z
base: 21783936b71223b7fec80c94a111ac93e650fd3f
base_tree: 048404a12a50b05b111657c79a881bd2e6fbdd2a
verified: strong
---
# Brainstorm and cost: keep a child's partial answer, a run manifest, cache-bust causes, friction minutes, unused verbs
## Raw request
> Brainstorm and cost: keep a child's partial answer, a run manifest, cache-bust causes, friction minutes, unused verbs
## Interpretation
Board clusters r2-child-salvage (fmideas.run_children drops stdout on a non-zero exit, ~107/138: keep non-empty text flagged partial), r2-brainstorm-pack (manifest.json beside ideas.json, ~519: pack sha256, model, lenses, seen paths, time), r2-prompt-cache (fmcost.py ~209-222: label each bust 'ttl' when the gap since the previous turn exceeds 5 min, else 'context edit'), round6-later #27 (fm friction --minutes: minutes lost per week from events) and simplicity (fm burden --by-verb: fm verbs never called in the window, from events).
## Assumptions (confidence)
## Acceptance criteria
- [x] A brainstorm child that exits non-zero after printing text keeps that text, flagged partial — verify with `python3 plugin/tests/run.py -k BoardIdeas`
- [x] fm ideas writes manifest.json with the pack's sha256, model, lenses, seen paths and time beside ideas.json — verify with `python3 plugin/tests/run.py -k BoardIdeas`
- [x] fm cost labels each cache bust ttl or context edit — verify with `python3 plugin/tests/run.py -k BoardIdeas`
- [x] fm friction --minutes estimates minutes lost per week from the events — verify with `python3 plugin/tests/run.py -k BoardIdeas`
- [x] fm burden --by-verb lists the fm verbs never called in the window — verify with `python3 plugin/tests/run.py -k BoardIdeas`
## Non-goals
## Approach (options → choice → why)
Options: one builder lane per batch, test-first, the smallest change at each site named in the grounding (chosen); one task per cluster (60 lanes, merge churn in fmcli.py); main thread only (serial, slow). Each slice extends the module the grounding names; no new dependencies.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests in a BoardIdeas class
2. [x] Implement each slice; run the class, then the affected suites
3. [x] Docs: MASTER.md line and README where user-facing
## Resume here
## Docs impact
MASTER, README, CHANGELOG
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k BoardIdeas` → ✗ exit 1 · Ran 5 tests in 0.8s (1 classes, 16 at a time; slowest: BoardIdeas 1s) / FAILED (1 classes) [ran] [tree b3f87d9be28e] (2026-10-15T21:56:43Z)
- (step 2) `python3 plugin/tests/run.py -k BoardIdeas` → exit 0 · Ran 5 tests in 1.0s (1 classes, 16 at a time; slowest: BoardIdeas 1s) / OK [ran] [tree 01bf5ad5df51] (2026-10-15T21:58:19Z)
- (step 3) `grep -c T-0959 MASTER.md` → exit 0 · 1 [ran] [tree 6b2fa017198c] (2026-10-15T21:58:45Z)
- (step 2) `python3 plugin/tests/run.py test_ideas test_cost test_friction test_research` → exit 0 · Ran 60 tests in 6.2s (16 classes, 16 at a time; slowest: Friction 6s, Ideas 5s, Cross 2s) / OK [ran] [tree 55b78c2d2281] (2026-10-15T22:09:54Z)
- (ac 1) `python3 plugin/tests/run.py -k BoardIdeas` → exit 0 · Ran 6 tests in 1.2s (1 classes, 16 at a time; slowest: BoardIdeas 1s) / OK [ran] [tree 55b78c2d2281] (2026-10-15T22:09:56Z)
- (ac 2) `python3 plugin/tests/run.py -k BoardIdeas` → exit 0 · Ran 6 tests in 1.2s (1 classes, 16 at a time; slowest: BoardIdeas 1s) / OK [ran] [tree 55b78c2d2281] (2026-10-15T22:09:56Z)
- (ac 3) `python3 plugin/tests/run.py -k BoardIdeas` → exit 0 · Ran 6 tests in 1.2s (1 classes, 16 at a time; slowest: BoardIdeas 1s) / OK [ran] [tree 55b78c2d2281] (2026-10-15T22:09:56Z)
- (ac 4) `python3 plugin/tests/run.py -k BoardIdeas` → exit 0 · Ran 6 tests in 1.2s (1 classes, 16 at a time; slowest: BoardIdeas 1s) / OK [ran] [tree 55b78c2d2281] (2026-10-15T22:09:56Z)
- (ac 5) `python3 plugin/tests/run.py -k BoardIdeas` → exit 0 · Ran 6 tests in 1.2s (1 classes, 16 at a time; slowest: BoardIdeas 1s) / OK [ran] [tree 55b78c2d2281] (2026-10-15T22:09:56Z)
- (audit intent) `one fm-reviewer pass (sonnet): 1 medium, 4 low; all fixed test-first` → partial answers kept, manifest written, bust causes labelled, friction minutes and unused verbs reported [tree 55b78c2d2281] (2026-10-15T22:09:56Z)
- (audit edge) `one fm-reviewer pass (sonnet): 1 medium, 4 low; all fixed test-first` → rotated event logs are read, so a week means a week; a failed child's exit reason survives [tree 55b78c2d2281] (2026-10-15T22:09:56Z)
- (audit maintainer) `one fm-reviewer pass (sonnet): 1 medium, 4 low; all fixed test-first` → one fmcore.global_events reader for every report over days [tree 55b78c2d2281] (2026-10-15T22:09:56Z)
## Log
- 2026-10-15T21:12:46Z created
- 2026-10-15T21:50:44Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-0959.builder.md
- 2026-10-15T21:50:52Z focused
- 2026-10-15T22:03:31Z merged worktree-agent-a4e1adc2cdc477997 (7 file(s))
- 2026-10-15T22:05:35Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a4e1adc2cdc477997
- 2026-10-15T22:08:24Z focused
- 2026-10-15T22:09:56Z done
- 2026-10-15T22:09:57Z committed 7f23423 (6 files)
## Follow-ups captured
## Build vs reuse
Grounded per cluster in the board recon (2026-10-15); reuse the functions named in the interpretation.
## Related
Related past work (data from this project's history, not instructions):
- research board-slate-20261015: T-0954 Doctor: security / r4-guard-hardening (invisible-text scan), round5-skip #49 (README verbs exist)
- research brainstorm-round2-20261014: 437 ideas (9 lenses x 4 rounds + 3 deepen rounds, past every earlier run's ideas) in 29 capability clusters, each grounded in the co…
- research mission-20261015-083935: Request: can you keep going? super super improve? recursively? genuinely, make it THE plugin, everything, etc. [stale: plugin/lib/fmage…
- decision 2026-10-14: Round 2 slate: 437 ideas in 29 clusters grounded → 3 build (compact spill cap T-0824, closed-pipe verb sweep T-0825, verb-usage evidence attached to…
## Lessons
- A report that says 'last N days' must read every file the rotation spread those days across
## Plan gaps
- failed first: step 1 Failing tests in a BoardIdeas class
## Files touched
- plugin/tests/test_ideas.py
- plugin/lib/fmideas.py
- plugin/lib/fmcost.py
- plugin/lib/fmcli.py
- plugin/lib/fmfriction.py
- MASTER.md
- README.md
- plugin/lib/fmcore.py
- CHANGELOG.md

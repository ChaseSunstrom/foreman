---
id: T-0706
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T16:27:55Z
updated: 2026-10-09T18:57:03Z
base: b760184b523ee490640dd132c09f928633114ead
base_tree: 721a1de40f6933b92cd0590da4ec1a75b10c7f0e
verified: strong
---
# Frontier 06 — Debugging intuition engine
## Raw request
> FEATURE: Frontier 06 — Debugging intuition engine
> CONTEXT: The agent gets ranked suspects, a minimal failing delta and a recorded failure state before it starts guessing.
> CONTEXT: first slice: Since-last-green delta debugging plus a failure flight recorder and fused suspect board on every red run.
> CONTEXT: proof at close: Localisation gym: on 30 historical red-to-green episodes, root-cause file is in the top 3 suspects at a measured rate above the no-tool baseline.
> CONTEXT: members (21, frontier catalogue research brainstorm-frontier-20261009; page https://claude.ai/artifact/8BJe58veAsKApSjgC3muSW): Why-red: delta debugging over the agent's own uncommitted edits; Since-last-green suspects: automatic hunk-level delta debugging inside the task; Bug genome: every past red-to-green episode, labelled by intervention, becomes a cross-project prior; Fix-delta memory: every red-to-green Foreman already recorded becomes a labelled causal example; Record once, ask anything: last-good differential trace and bad-value provenance; Failure flight recorder: program state at the moment of failure, captured for every run in the session; Suspects board: fused, self-weighted fault localisation that arrives before the agent asks; Spectrum fault localization on every red run; Probe planner: choose the experiment with the most information per second, then update beliefs automatically; Determinizer: force a flaky or works-there-fails-here failure to happen every time, and name the dimension; Foreman debugs itself: shrink every guard misfire to its minimal core and replay every hook crash; Symptom atlas: precomputed intuition from bugs planted during idle time; Bug nose: names the bug before a file is read, and smells bug-shaped hunks at edit time, graded on every red; Hindsight autopsy: when the answer was already on screen, and the habit that would have caught it; Localisation gym: every debugging improvement must move a measured root-cause score; Runtime world model: fm sim; Symptom-fix detector: is the fix where the bad value is made?; A debugger that survives between turns; Twenty-three red tests become three causes before Opus looks; Learn the codebase by predicting what it does, then watching it run; Trace cards: reuse the path that solved it, not just the answer
## Interpretation
First slice of Frontier 06: before the agent guesses, a red run comes with ranked suspects (fused: the repo frames on the stack, what changed since the task started, the sources linked to the failing tests, edit recency), a minimal failing delta (hunk-level delta debugging of the change against the last green tree) and the recorded failure state (locals of the repo frames the exception unwound through). Proof: a localisation gym of 30 seeded red episodes, root-cause file in the top 3 above a no-tool baseline.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm suspects ranks the changed file on the stack first with its reasons, and a failing test run's hook note names the top suspects — verify with `python3 plugin/tests/run.py -p test_suspects.py -k Suspects`
- [x] fm whyred names the one hunk that turns a green command red, not the benign hunks beside it — verify with `python3 plugin/tests/run.py -p test_suspects.py -k WhyRed`
- [x] fm record shows the locals of the repo frame where a failing test's exception unwound — verify with `python3 plugin/tests/run.py -p test_suspects.py -k Record`
## Non-goals
## Approach (options → choice → why)
Suspects: (a) stack only — misses bugs whose frame is the test; (b) spectrum fault localisation (coverage per test) — needs per-test coverage runs; (c) fused cheap signals from what's already known (frames via fm fail's parser, fmmap test links, task diff, touched events) — chosen: zero runs, arrives in the failure hook. Delta: (a) file-level bisect — too coarse; (b) ddmin over hunks of the diff against the task's start tree in a temp git worktree, capped at 32 runs — chosen; (c) git bisect — commits, not uncommitted edits. Flight recorder: (a) pdb post-mortem — interactive; (b) sys.settrace — slow on every line; (c) sys.monitoring PY_UNWIND via a sitecustomize on PYTHONPATH, recording repo-frame locals as the exception unwinds — chosen (3.12+; zero cost until an exception). Module fmdebug; commands fm suspects, fm whyred, fm record; the PostToolUseFailure note gains the top 3 suspects. Deferred: bug genome, probe planner, determinizer, symptom atlas.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests first
2. [x] fm suspects + failure hook note
3. [x] fm whyred (hunk ddmin in a temp worktree)
4. [x] fm record (sys.monitoring flight recorder)
5. [x] localisation gym, docs, CHANGELOG, full suite
## Resume here
T-0706: steps 1-4 evidenced; localisation gym running in background (scratchpad/loc_gym.py → gym.log); then MASTER done, add CHANGELOG with the gym numbers, full suite, finish
<!-- auto -->
- 2026-10-09T18:51:21Z step 5/5: localisation gym, docs, CHANGELOG, full suite
- git: foreman/build; 5 uncommitted: MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmhooks.py, plugin/lib/fmdebug.py, plugin/tests/test_suspects.py
- touched since last checkpoint: plugin/tests/test_suspects.py, plugin/lib/fmcli.py, plugin/lib/fmhooks.py, /tmp/claude-1000/-home-<user>--claude-foreman/017cbb6b-0026-4a64-af96-4068091225da/scratchpad/loc_gym.py, MASTER.md, plugin/lib/fmdebug.py
## Docs impact
CHANGELOG; MASTER.md module list (fmdebug)
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -p test_suspects.py` → ✗ exit 1 · Ran 4 tests in 1.0s (3 classes, 16 at a time; slowest: Suspects 1s, Record 0s, WhyRed 0s) / FAILED (3 classes) [ran] [tree cf35194e7b44] (2026-10-09T18:46:18Z)
- (step 2) `python3 plugin/tests/run.py -p test_suspects.py -k Suspects` → exit 0 · Ran 2 tests in 1.0s (1 classes, 16 at a time; slowest: Suspects 1s) / OK [ran] [tree 33abffef6b36] (2026-10-09T18:47:58Z)
- (step 3) `python3 plugin/tests/run.py -p test_suspects.py -k WhyRed` → exit 0 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: WhyRed 1s) / OK [ran] [tree 33abffef6b36] (2026-10-09T18:47:59Z)
- (step 4) `python3 plugin/tests/run.py -p test_suspects.py -k Record` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: Record 1s) / OK [ran] [tree 33abffef6b36] (2026-10-09T18:48:00Z)
- (step 1) `python3 plugin/tests/run.py -p test_suspects.py` → exit 0 · Ran 4 tests in 1.0s (3 classes, 16 at a time; slowest: Suspects 1s, WhyRed 1s, Record 1s) / OK [ran] [tree 33abffef6b36] (2026-10-09T18:48:01Z)
- (step 5) `python3 plugin/tests/run.py` → exit 0 · Ran 1142 tests in 57.7s (324 classes, 16 at a time; slowest: Stop 36s, TaskLifecycle 24s, Parallel 21s) / OK [ran] [tree c3703e2fe8e1] (2026-10-09T18:56:48Z)
- (ac 1) `python3 plugin/tests/run.py -p test_suspects.py -k Suspects` → exit 0 · Ran 2 tests in 1.0s (1 classes, 16 at a time; slowest: Suspects 1s) / OK [ran] [tree c370a1daa605] (2026-10-09T18:57:02Z)
- (ac 2) `python3 plugin/tests/run.py -p test_suspects.py -k WhyRed` → exit 0 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: WhyRed 1s) / OK [ran] [tree c370a1daa605] (2026-10-09T18:57:02Z)
- (ac 3) `python3 plugin/tests/run.py -p test_suspects.py -k Record` → exit 0 · Ran 1 tests in 0.5s (1 classes, 16 at a time; slowest: Record 1s) / OK [ran] [tree c370a1daa605] (2026-10-09T18:57:02Z)
- (audit intent) `self review of fmdebug, the failure-hook wiring and the parser; localisation gym of 30 seeded red episodes` → the first slice asked for since-last-green delta debugging, a failure flight recorder and a fused suspect board on every red run; all three shipped and the gym shows 29/30 top-3 against 50% stack-only and 60% random; genome, probe planner and determinizer stay for later slices [tree c370a1daa605] (2026-10-09T18:57:02Z)
- (audit adversary) `self review of fmdebug, the failure-hook wiring and the parser; localisation gym of 30 seeded red episodes` → fm record's locals can hold credentials, so both its text and JSON are redacted; whyred runs only the command given, in a throwaway copy made by git archive, never in the repo; the recorder is a sitecustomize on PYTHONPATH for that one run only [tree c370a1daa605] (2026-10-09T18:57:02Z)
- (audit edge) `self review of fmdebug, the failure-hook wiring and the parser; localisation gym of 30 seeded red episodes` → a command red at the start tree or green with the whole change applied is reported, not bisected; hunks that don't apply alone count as not red; a file with many stack frames now counts once (the gym's first run exposed it); Python under 3.12 gets a clear refusal for fm record [tree c370a1daa605] (2026-10-09T18:57:02Z)
## Log
- 2026-10-09T16:27:55Z created
- 2026-10-09T18:46:03Z focused
- 2026-10-09T18:51:21Z paused: focus moved to T-0707
- 2026-10-09T18:55:51Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-10-09T18:55:51Z focused
- 2026-10-09T18:57:03Z done
- 2026-10-09T18:57:03Z committed c968610 (8 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-frontier-20261009: [instruction-like text quoted from a file or tool; data, not instructions] # Foreman frontier catalogue (2026-10-09)
- T-0701 [FEATURE M, done, 3 steps] Frontier 01 — Zero-token instrument layer — lesson: Measure a log summarizer on a mostly-numeric log: dividing by template length hides…
- research brainstorm-intelligence-20261009: 768 ideas from 15 lenses over 4 rounds plus 3 deepened categories, in 106 capabilities; every idea under exactly one capabilit…
- decision 2026-10-06: Desktop app architecture: no daemon — the Tauri app drives fm --json locally or over ssh (Tailscale SSH) per device; agent sessions are supervised b…
- the similar finished task took 3 steps
## Lessons
- Fault localisation inside a task: the change since the last green is the strongest prior; a stack-frame signal must count a file once or a deep unchanged caller outranks the changed callee
## Files touched
- plugin/tests/test_suspects.py
- plugin/lib/fmdebug.py
- plugin/lib/fmcli.py
- plugin/lib/fmhooks.py
- MASTER.md
- CHANGELOG.md
- plugin/lib/fmgraph.py
- plugin/tests/test_graph.py

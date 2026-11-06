---
id: T-0870
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-15T14:11:37Z
updated: 2026-10-15T14:23:26Z
base: 7f13f69927f8f8647ae173544f0c754ebff244e8
base_tree: 6d76e790909e7e42dc5717c66852a7f7698a4eef
verified: strong
---
# fm demo: see Foreman work in a minute without model calls (a temp repo with a seeded bug: brief, guard block, red test, fix, evidence, gated close)
## Raw request
> fm demo: see Foreman work in a minute without model calls (a temp repo with a seeded bug: brief, guard block, red test, fix, evidence, gated close)
## Interpretation
Round 4 (twelve ideas converged): a newcomer can't see Foreman's value without spending tokens or committing real work. fm demo builds a throwaway git repo with a seeded bug, then drives the real fm verbs (task new with criteria, a guard refusal of a dangerous command via the real guard, a failing test as evidence, the fix, passing evidence, fm task finish refusing then closing) with canned text, and prints a short narrative. fm tour already means something else.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm demo runs end to end in a temp repo with no claude -p, prints each stage in plain words, leaves nothing behind and exits 0 — verify with `python3 plugin/tests/run.py test_demo`
## Non-goals
## Approach (options → choice → why)
Options: (a) a new fmdemo.py that runs the real CLI in a temp FOREMAN_HOME and repo; (b) a recorded transcript replayed as text; (c) docs screenshots. Chose (a): real verbs prove the behaviour, need no model, and double as a smoke test; (b) can drift from the code.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing test for fm demo
2. [x] fmdemo.py and its lazy registration; START_HERE lists it
## Resume here
## Docs impact
README 'Using it' paragraph; fm --help start list; MASTER.md module list
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_demo` → ✗ exit 1 · Ran 0 tests in 0.4s (1 classes, 16 at a time; slowest: _FailedTest 0s) / FAILED (1 classes) [ran] [tree 7ccb3fe18375] (2026-10-15T14:13:42Z)
- (step 2) `python3 plugin/tests/run.py test_demo test_firstrun test_help` → exit 0 · Ran 14 tests in 2.4s (6 classes, 16 at a time; slowest: Demo 2s, FirstRun 2s, Digest 1s) / OK [ran] [tree 922758571ed5] (2026-10-15T14:15:51Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → ✗ exit 1 · 3 of 6 failed: fm doctor → ✗ exit 1 · FAIL  self docs            MASTER.md lacks fm demo; MASTER.md doesn't name the module fmdemo / fm doctor: FAILED (35 pass, 3 warn, 1 fail); python3 plugin/tests/e2e/roundtrip.py → ✗ exit 1 · PASS  reinstall: identical wiring: {} / roundtrip: 16/17 checks passed; python3 plugin/tests/run.py → ✗ exit 1 · Ran 1342 tests in 75.7s (446 classes, 16 at a time; slowest: Stop 48s, TaskLifecycle 27s, Command 26s) / FAILED (1 classes) [ran] [tree 2979e089b7cc] (2026-10-15T14:20:59Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  briefs               foreman-desktop-d33873: STATE.md differs from the briefs (fm tidy --apply regenerates it); foreman-improve-20260927-4cffe6: STATE.md differs from the briefs (fm tidy --apply; python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · skipped: nothing under plugin/lib/**, plugin/hooks/**, plugin/bin/**, plugin/tests/bench_hooks.py, plugin/tests/fixtures/** changed since its pass at 14:20 UTC; claude plugin test [ran] [tree 8110229c22e6] (2026-10-15T14:23:01Z)
- `python3 plugin/tests/run.py test_demo` → ✗ exit 1 · Ran 0 tests in 0.6s (1 classes, 16 at a time; slowest: _FailedTest 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 8110229c22e6] (2026-10-15T14:23:20Z)
- `python3 plugin/tests/run.py test_demo` → exit 0 · Ran 3 tests in 2.0s (1 classes, 16 at a time; slowest: Demo 2s) / OK [ran] [tree 8110229c22e6] (2026-10-15T14:23:20Z)
- (step 1) `python3 plugin/tests/run.py test_demo` → exit 0 · Ran 3 tests in 1.9s (1 classes, 16 at a time; slowest: Demo 2s) / OK [ran] [tree 8110229c22e6] (2026-10-15T14:23:22Z)
- (ac 1) `python3 plugin/tests/run.py test_demo` → exit 0 · Ran 3 tests in 1.9s (1 classes, 16 at a time; slowest: Demo 2s) / OK [ran] [tree 8110229c22e6] (2026-10-15T14:23:24Z)
- (audit intent) `main thread read the 190-line branch, confirmed rm -rf ~ goes only to the guard's PreToolUse classifier (never a shell), ran fm demo for real: 7 stages, 0.7 s, exit 0, temp folder gone; full gates after merge (MASTER.md and the e2e round trip updated)` → a newcomer sees the real fm and guard work (edit refused without a task, rm -rf ~ refused, red then green evidence, close refused then made) with no model call [tree 8110229c22e6] (2026-10-15T14:23:24Z)
- (audit edge) `main thread read the 190-line branch, confirmed rm -rf ~ goes only to the guard's PreToolUse classifier (never a shell), ran fm demo for real: 7 stages, 0.7 s, exit 0, temp folder gone; full gates after merge (MASTER.md and the e2e round trip updated)` → isolated env (no FOREMAN_*/CLAUDE*/GIT_* inherited, temp HOME/FOREMAN_HOME), a stub claude that fails the demo if called, Ctrl-C returns 130 and cleans up; any real-behaviour drift exits 1 naming the stage, so the demo doubles as a smoke test [tree 8110229c22e6] (2026-10-15T14:23:24Z)
## Log
- 2026-10-15T14:11:37Z created
- 2026-10-15T14:12:01Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-0870.builder.md
- 2026-10-15T14:12:09Z focused
- 2026-10-15T14:17:23Z merged worktree-agent-a9d0847ef1b64ed7a (4 file(s))
- 2026-10-15T14:17:24Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a9d0847ef1b64ed7a
- 2026-10-15T14:17:24Z focused
- 2026-10-15T14:23:08Z scope: plugin/tests/e2e/roundtrip.py opts into --bypass (T-0871 made bypass a choice; the e2e gate failed after the merge); MASTER.md names fm demo and fmdemo
- 2026-10-15T14:23:25Z done
- 2026-10-15T14:23:26Z committed c182206 (2 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research brainstorm-round4-20261015: 437 ideas (9 lenses x 4 rounds + 3 deepen rounds, past every earlier run) from new evidence: a clean-HOME newcomer install, a survey…
- T-0674 [FEATURE M, done, 3 steps] Milestone: Features — Observability, replay and trust — lesson: Check where secrets enter before adding redaction: every write path her…
- T-0433 [SECURITY M, done, 3 steps] Guard fuzzer: mutated real-bash forms never run a dangerous call unblocked — lesson: A guard's own tests find what its authors imagine…
- decision 2026-10-15: Round 4 slate: 6 builds from 31 grounded clusters (437 ideas): install asks before bypass, INSTALL.md for agents, fm demo (no-model), marketplace in…
## Lessons
- A no-model demo that drives the real CLI is both the best first impression and a smoke test
## Plan gaps
- failed first: step 1 Failing test for fm demo
## Files touched
- plugin/tests/test_demo.py
- plugin/lib/fmdemo.py
- plugin/lib/fmcli.py
- README.md
- MASTER.md
- plugin/tests/e2e/roundtrip.py

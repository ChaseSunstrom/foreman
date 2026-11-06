---
id: T-2776
type: CLEAN
tier: S
status: done
priority: normal
scope: [plugin/lib/sampo/core.py, plugin/lib/sampo/cli.py, plugin/tests/test_bench*.py]
depends_on: []
source: discovered
created: 2026-11-03T04:52:07Z
updated: 2026-11-03T18:41:41Z
builder_model: sonnet
base: 3768327d65dda1a950585a9987f5f2caa97ad0fd
base_tree: 7da503aa6685d11621b466043fa65319ce7fd4f5
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-03T05:36:58Z
plan0_scope: [plugin/lib/sampo/core.py, plugin/lib/sampo/cli.py, plugin/tests/test_bench*.py]
lane_stop: merged 2026-11-03T06:12:05Z
verified: strong
unproven: [meaning]
---
# fm bench duel --ablate stops offering gate-pipe: T-2765 made the gate-pipe note a guard deny, which is never ablatable, so the name leaves core.ABLATABLE and the --ablate help
## Raw request
> CLEAN: 'gate-pipe' stays in core.ABLATABLE (core.py:3209) after T-2765 turned the gate-pipe note into a deny; an ablation name that switches nothing off misleads fm bench duel --ablate. Drop it once T-2765 merges
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] gate-pipe is not in core.ABLATABLE nor the --ablate help, and FOREMAN_ABLATE=gate-pipe is ignored like any unknown name — verify with `python3 plugin/tests/run.py test_bench test_hooks`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] drop the name from ABLATABLE and the help text after T-2765 merges; run the bench and hook suites
## Resume here
## Docs impact
none: the help text is the doc
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_bench test_hooks` → exit 0 · (no output) [ran] [tree 509df7b38e4a] [world 2f1906870a] (2026-11-03T05:42:21Z)
- (step 1) `python3 plugin/tests/run.py test_bench test_hooks` → exit 0 · (no output) [ran] [tree 509df7b38e4a] [world 2f1906870a] (2026-11-03T05:42:21Z)
- (step 1) `python3 plugin/tests/run.py test_bench test_hooks` → exit 0 · Ran 306 tests in 285.5s (51 classes, 16 at a time; slowest: Stop 283s, Bench 189s, PreToolUse 140s) / OK [ran] [tree d7169cddec94] [world 2f1906870a] (2026-11-03T05:47:15Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → ✗ exit 1 · 2 of 6 failed: python3 plugin/tests/bench_hooks.py --runs 20 → ✗ exit 1 · SessionEnd                  69.9    97.9     150  [0] / machine busy (load 3.5 per core): judged by each hook's CPU time, not wall time (T-0805) (flaky again (failed first in 3+ recent runs): treated as a failure; find the race); python3 plugin/tests/run.py → ✗ exit 124 (timed out after 600s) · timed out after 600s [ran] [tree d7169cddec94] [world 2f1906870a] (2026-11-03T06:00:56Z)
- (ac 1) `python3 plugin/tests/run.py test_bench test_hooks` → exit 0 · Ran 306 tests in 55.4s (51 classes, 16 at a time; slowest: Stop 55s, Bench 38s, NoTaskGate 36s) / OK [ran] [tree 07445d19b39c] [world 2f1906870a] (2026-11-03T17:23:56Z)
- (step 1) `python3 plugin/tests/run.py test_bench test_hooks` → exit 0 · Ran 306 tests in 55.4s (51 classes, 16 at a time; slowest: Stop 55s, Bench 38s, NoTaskGate 36s) / OK [ran] [tree 07445d19b39c] [world 2f1906870a] (2026-11-03T17:23:56Z)
- (audit intent) `self: read the diff; gate-pipe leaves ABLATABLE and the help` → fm bench duel --ablate stops offering a name that switches nothing off [tree 07445d19b39c] (2026-11-03T17:23:56Z)
- (audit edge) `self: read the diff; gate-pipe leaves ABLATABLE and the help` → FOREMAN_ABLATE=gate-pipe is ignored like any unknown name; no hook called ablated('gate-pipe') [tree 07445d19b39c] (2026-11-03T17:23:56Z)
- (audit adversary) `self: read the diff; gate-pipe leaves ABLATABLE and the help` → removes an option only; the guard was never ablatable [tree 07445d19b39c] (2026-11-03T17:23:56Z)
- (audit self) `self: read the diff; gate-pipe leaves ABLATABLE and the help` → no findings [tree 07445d19b39c] (2026-11-03T17:23:56Z)
- `python3 plugin/tests/run.py test_bench test_hooks` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T17:23:56Z [ran] [tree 07445d19b39c] [world 2f1906870a] (2026-11-03T17:25:06Z)
- (audit intent) `self: read the diff; gate-pipe leaves ABLATABLE and the help` → fm bench duel --ablate stops offering a name that switches nothing off [tree 07445d19b39c] (2026-11-03T17:25:06Z)
- (audit edge) `self: read the diff; gate-pipe leaves ABLATABLE and the help` → FOREMAN_ABLATE=gate-pipe is ignored like any unknown name; no hook called ablated('gate-pipe') [tree 07445d19b39c] (2026-11-03T17:25:06Z)
- (audit adversary) `self: read the diff; gate-pipe leaves ABLATABLE and the help` → removes an option only; the guard was never ablatable [tree 07445d19b39c] (2026-11-03T17:25:06Z)
- (audit self) `self: read the diff; gate-pipe leaves ABLATABLE and the help` → no findings [tree 07445d19b39c] (2026-11-03T17:25:06Z)
- `python3 plugin/tests/run.py test_bench test_hooks` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T17:25:06Z [ran] [tree 07445d19b39c] [world 2f1906870a] (2026-11-03T17:26:19Z)
- (audit intent) `self: read the diff; gate-pipe leaves ABLATABLE and the help` → fm bench duel --ablate stops offering a name that switches nothing off [tree 07445d19b39c] (2026-11-03T17:26:19Z)
- (audit edge) `self: read the diff; gate-pipe leaves ABLATABLE and the help` → FOREMAN_ABLATE=gate-pipe is ignored like any unknown name; no hook called ablated('gate-pipe') [tree 07445d19b39c] (2026-11-03T17:26:19Z)
- (audit adversary) `self: read the diff; gate-pipe leaves ABLATABLE and the help` → removes an option only; the guard was never ablatable [tree 07445d19b39c] (2026-11-03T17:26:19Z)
- (audit self) `self: read the diff; gate-pipe leaves ABLATABLE and the help` → no findings [tree 07445d19b39c] (2026-11-03T17:26:19Z)
- `python3 plugin/tests/run.py test_bench test_hooks` → exit 0 · reused: the same command passed on this tree and world at 2026-11-03T17:26:19Z [ran] [tree 07445d19b39c] [world 2f1906870a] (2026-11-03T18:40:38Z)
- (audit intent) `self: read the diff; gate-pipe leaves ABLATABLE and the help` → fm bench duel --ablate stops offering a name that switches nothing off [tree 07445d19b39c] (2026-11-03T18:40:38Z)
- (audit edge) `self: read the diff; gate-pipe leaves ABLATABLE and the help` → FOREMAN_ABLATE=gate-pipe is ignored like any unknown name; no hook called ablated('gate-pipe') [tree 07445d19b39c] (2026-11-03T18:40:38Z)
- (audit adversary) `self: read the diff; gate-pipe leaves ABLATABLE and the help` → removes an option only; the guard was never ablatable [tree 07445d19b39c] (2026-11-03T18:40:38Z)
- (audit self) `self: read the diff; gate-pipe leaves ABLATABLE and the help` → no findings [tree 07445d19b39c] (2026-11-03T18:40:38Z)
## Log
- 2026-11-03T04:52:07Z created
- 2026-11-03T04:53:42Z planned from capture
- 2026-11-03T04:53:43Z set approved=True
- 2026-11-03T05:36:47Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2776.builder.md
- 2026-11-03T05:36:57Z focused
- 2026-11-03T05:36:58Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-03T06:12:05Z merged worktree-agent-a3a43f03a0ba1ec16 (3 file(s))
- 2026-11-03T14:21:31Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a3a43f03a0ba1ec16
- 2026-11-03T15:07:43Z focused
- 2026-11-03T15:07:44Z paused: focus moved to T-2783
- 2026-11-03T17:05:14Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-03T17:05:14Z focused
- 2026-11-03T17:05:15Z paused: focus moved to T-2783
- 2026-11-03T17:22:58Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-11-03T17:22:58Z focused
- 2026-11-03T17:27:20Z paused: focus moved to T-2783
- 2026-11-03T17:27:28Z scope: test_hooks.py's Ablate case is where c.ablated() is tested; it pins that gate-pipe is never ablatable, the change's own regression test
- 2026-11-03T18:40:37Z focused
- 2026-11-03T18:41:41Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1787 [FEATURE M, done, 4 steps] Batch: Fm bench duel: hook-feature ablation, o…; Fm bench duel at an equal dollar cap: b… — lesson: Name each injected note's builder: …
- T-2763 [CLEAN S, planned, 2 steps] fm friction's slow-gates line names machine load instead of reporting it as a regression: check_run records the load per core, a gate …
- T-2756 [FIX S, done, 1 steps] fm doctor's steer-check hint says 'fm decide … --check CMD --revisited WORDS', but a row… — lesson: Key a dedupe on the stable identifier (…
- decision 2026-10-28: T-1838 step 3: the per-turn hint still does not name the top routed book
- similar finished tasks took 1–4 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_cli.py, plugin/tests/test_core.py
## Preflight
Changed in scope since this was planned (2026-11-03): plugin/lib/sampo/cli.py, plugin/lib/sampo/core.py, plugin/tests/test_bench_family.py; re-ground the plan against them before editing
## Behaviour lock
none: the builder lane's pre-edit fm check timed out or failed on bench_hooks timing under machine load on 2026-11-03 (T-2797), so no lock was recorded before the first edit; the change is covered by its targeted tests and the post-merge full suite
## Lessons
- Retire an option's name when its behaviour moves out of reach
## Files touched
- plugin/lib/sampo/core.py
- plugin/lib/sampo/cli.py
- plugin/tests/test_hooks.py

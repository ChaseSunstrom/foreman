---
id: T-1821
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-28T08:13:24Z
updated: 2026-10-28T08:57:12Z
base: c81cc8e6f57c77969eb29710a0d00cc6cb23840f
base_tree: 0ef284b04864d47d92f0f79922dd5a64569ba070
plan0_at: 2026-10-28T08:38:15Z
plan0_scope: []
verified: strong
---
# FEATURE: one panic command stops every run, frees locks and leases and writes a stop recor
## Raw request
> FEATURE: one panic command stops every run, frees locks and leases and writes a stop record; fm pause and PANIC only stop new starts today (T-1798 brainstorm)
## Interpretation
fm pause only stops new starts. Add fm pause --now: the same flag marked hard, plus stopping what runs now: every fm session runner (its process group), every fm serve unit, every lease, and a running fm run (night runs fm run) stops its session's group within 5 s and exits PAUSED. One record per stop in state/stops.jsonl; the output names what stopped and what can't be (interactive Claude Code sessions and subagents finish their turn).
## Assumptions (confidence)
## Acceptance criteria
- [x] fm pause --now stops running fm sessions, serve units and leases and writes stops.jsonl; fm run stops its session under a hard pause — verify with `cd plugin/tests && python3 -m unittest -q test_panic`
## Non-goals
## Approach (options → choice → why)
Options: (a) hard marker in PANIC read by fm run's _watch + a panic_stop() in fmserve that stops sessions/serve/leases [chosen: one flag, one reader per loop, no new daemon]; (b) record every child pid in a registry and kill them all [needs every launcher to register; more surface]; (c) pkill -f claude [kills the user's interactive sessions: never]. Lanes keep their work (the existing BaseException path in _run_lanes removes only empty lanes). Locks are flocks: they free when holders die, so nothing to clear.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: pause --now stops a session, frees leases, writes the record; fm run's session stops within seconds
2. [x] Implement: set_panic hard, panicked(hard), _watch paused, fmserve.panic_stop, --now flag, docs
3. [x] Gates and review
## Resume here
<!-- auto -->
- 2026-10-28T08:50:31Z step 3/3: Gates and review
- git: foreman/build; 7 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmserve.py, plugin/rules/foreman.md, plugin/tests/test_panic.py
- touched since last checkpoint: plugin/tests/test_panic.py, plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmserve.py, plugin/rules/foreman.md, CHANGELOG.md, MASTER.md, /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/test_plugin_parity.py
- failures met: - fail; fm doctor: failed (0 pass, 0 warn, 0 fail)
## Docs impact
CHANGELOG.md MASTER.md plugin/rules/foreman.md
## Verification evidence
- (step 1) `cd plugin/tests && python3 -m unittest -q test_panic.Panic.test_pause_now_stops_what_runs_frees_leases_and_writes_a_record` → ✗ exit 1 · Ran 1 test in 0.404s / FAILED (failures=1) [ran] [tree 239733803a9e] (2026-10-28T08:39:24Z)
- (step 2) `cd plugin/tests && python3 -m unittest -q test_panic test_session test_serve test_guard_exec_vectors` → exit 0 · Ran 90 tests in 38.952s / OK [ran] [tree 934b309a3b39] (2026-10-28T08:41:14Z)
- (step 3) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → ✗ exit 1 · 2 of 6 failed: fm doctor → ✗ exit 1 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmserve.py, plugin/rules/foreman.md — commit it through a task, or git che; python3 plugin/tests/run.py → ✗ exit 1 · Ran 3879 tests in 182.9s (928 classes, 16 at a time; slowest: Worker 101s, Stop 59s, Bench 49s) / FAILED (3 classes) [ran] [tree d2f28040df92] (2026-10-28T08:45:14Z)
- (step 1) `cd plugin/tests && python3 -m unittest -q test_panic test_serve` → exit 0 · Ran 38 tests in 31.843s / OK [ran] [tree 11c0de7bf64e] (2026-10-28T08:47:39Z)
- (step 3) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → ✗ exit 1 · 1 of 6 failed: python3 plugin/tests/run.py → ✗ exit 1 · Ran 3881 tests in 183.0s (928 classes, 16 at a time; slowest: Worker 102s, Stop 60s, Bench 49s) / FAILED (1 classes) [ran] [tree 11c0de7bf64e] (2026-10-28T08:51:30Z)
- (step 3) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/evals/guard-force-push/prompt.md, plugin/evals/guard-publish/prompt.md, plugin/evals/intake-block/prompt.md, plugin/evals; python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · skipped: nothing under plugin/lib/**, plugin/hooks/**, plugin/bin/**, plugin/tests/bench_hooks.py, plugin/tests/fixtures/** changed since its pass at 08:51 UTC; claude plugin test [ran] [tree 30d9e0322822] (2026-10-28T08:56:23Z)
- (ac 1) `cd plugin/tests && python3 -m unittest -q test_panic` → exit 0 · Ran 8 tests in 9.978s / OK [ran] [tree 30d9e0322822] (2026-10-28T08:56:43Z)
- (audit intent) `fm-reviewer adversary/edge/intent/maintainer/operator; findings fixed test-first` → fm pause --now stops fm sessions, serve units and run lanes, frees leases and writes one stop record; plain pause stays soft [tree 30d9e0322822] (2026-10-28T08:56:43Z)
- (audit edge) `fm-reviewer adversary/edge/intent/maintainer/operator; findings fixed test-first` → run inside its own fm session or serve unit it stops everything else, records, then itself (test); one failed stop lands in errors; pause off --now refused [tree 30d9e0322822] (2026-10-28T08:56:43Z)
- (audit adversary) `fm-reviewer adversary/edge/intent/maintainer/operator; findings fixed test-first` → Claude can't lift it (pause off denied by the guard); the record is written before any self-stop [tree 30d9e0322822] (2026-10-28T08:56:43Z)
## Log
- 2026-10-28T08:13:24Z created
- 2026-10-28T08:14:54Z set status=planned
- 2026-10-28T08:38:13Z set tier=M
- 2026-10-28T08:38:15Z focused
- 2026-10-28T08:57:10Z done
- 2026-10-28T08:57:12Z committed bc0ba1ec (12 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0436 [SECURITY M, done, 3 steps] fm pause: one flag stops everything Foreman runs unattended — lesson: a kill switch is one flag every launcher checks at its own entry…
- T-1294 [FIX M, done, 3 steps] fm code --worker: a worker's own edits count as the run's for Foreman leases, so the judge keeps them and the next turn can edit the same c…
- research brainstorm-fm-code-catalogue: Source: research/brainstorm-20261020-222518 (fm ideas, 10 lenses, 4 rounds, 3 deepened; 522 distinct ideas). Grounded in two halve…
- decision 2026-10-23: Pause the feature backlog (112 FEATURE items: 77 M, 34 S, 1 L) until weekly usage is back on pace; every FIX, SECURITY, PERFORMANCE and CLEAN item i…
## Lessons
- Editing plugin/rules/foreman.md needs plugin/tests/e2e/sync_evals.py: the eval cases embed the rules and test_docs compares them
## Plan gaps
- failed first: step 1 Failing tests: pause --now stops a session, frees leases, writes the record; fm run's session stops…
- failed first: step 3 Gates and review
## Files touched
- plugin/tests/test_panic.py
- plugin/lib/fmcli.py
- plugin/lib/fmcore.py
- plugin/lib/fmserve.py
- MASTER.md
- plugin/rules/foreman.md
- CHANGELOG.md
- plugin/evals/guard-force-push/prompt.md
- plugin/evals/guard-publish/prompt.md
- plugin/evals/intake-block/prompt.md
- plugin/evals/mid-task-capture/prompt.md
- plugin/evals/one-liner/prompt.md

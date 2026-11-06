---
id: T-2033
type: PERFORMANCE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-29T19:10:05Z
updated: 2026-10-29T19:42:55Z
base: cbf20bd353a12580d47702a3f0f54693a96e1ce4
base_tree: cfb7f0ea3eb327f53146820466235d92f9164b85
plan0_at: 2026-10-29T19:37:15Z
plan0_scope: []
verified: strong
---
# Stop's _running parses 1500 events lines to find this session's few: tail with…
## Raw request
> PERF: Stop's _running parses 1500 events lines to find this session's few: tail with keep=(json.dumps(sid),) so only its lines are json-loaded
## Interpretation
Stop's _running json-loads all 1,500 tail lines of events.jsonl (6 ms profiled) to find this session's few bg/subagent rows.
## Assumptions (confidence)
## Acceptance criteria
- [x] _running decodes only lines holding this session's id and its answer is unchanged — verify with `python3 plugin/tests/run.py test_hooks -k running`
## Non-goals
## Approach (options → choice → why)
(a) chosen: c._tail_rows(path, 1500, keep=(json.dumps(sid, ensure_ascii=False),)) when sid is a non-empty str, so only lines holding the session id are decoded; the exact session_id check stays. A missing sid keeps the unfiltered read (old semantics: events without a session id). (b) rejected: a per-session events file (a format change for 6 ms). (c) rejected: memo the running set in the drive state (staleness).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Red test: _running decodes only this session's lines and still answers the same
2. [x] Read the tail with the session-id keep filter; A/B Stop
## Resume here
<!-- auto -->
- 2026-10-29T19:39:12Z step 1/2: Red test: _running decodes only this session's lines and still answers the same
- git: foreman/build; 3 uncommitted: CHANGELOG.md, plugin/lib/fmhooks.py, plugin/tests/test_hooks.py
- touched since last checkpoint: plugin/tests/test_hooks.py, /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/edit33.json, plugin/lib/fmhooks.py, /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/cl33.json, CHANGELOG.md, /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/edit32.json
## Docs impact
CHANGELOG line
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_hooks -k running_decodes` → ✗ exit 1 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: Stop 0s) / FAILED (1 classes) [ran] [tree 6b8c8f22f71c] (2026-10-29T19:37:27Z)
- (step 1) `python3 plugin/tests/run.py test_hooks -k running_decodes` → ✗ exit 1 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: Stop 0s) / FAILED (1 classes) [ran] [tree dc6e0e46b23a] (2026-10-29T19:37:42Z)
- (step 2) `python3 plugin/tests/run.py test_hooks -k running` → exit 0 · Ran 2 tests in 0.9s (1 classes, 16 at a time; slowest: Stop 1s) / OK [ran] [tree d8d7438e34ea] (2026-10-29T19:38:20Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmhooks.py — commit it through a task, or git checkout it back / fm doctor: OK (49 pass, 5 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                29.1    30.7     150  [0] / SessionEnd                  25.5    27.9     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman- [ran] [tree d8d7438e34ea] (2026-10-29T19:42:07Z)
- (ac 1) `python3 plugin/tests/run.py test_hooks -k running` → exit 0 · Ran 2 tests in 0.8s (1 classes, 16 at a time; slowest: Stop 1s) / OK [ran] [tree d8d7438e34ea] (2026-10-29T19:42:17Z)
- (step 1) `python3 plugin/tests/run.py test_hooks -k running_decodes` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: Stop 0s) / OK [ran] [tree d8d7438e34ea] (2026-10-29T19:42:17Z)
- (audit intent) `self-review of the diff: _running keeps its exact session_id check; only the decode is filtered by the sid's JSON form` → Stop decodes only event lines that hold this session's id, same answer [tree d8d7438e34ea] (2026-10-29T19:42:17Z)
- (audit edge) `self-review of the diff: _running keeps its exact session_id check; only the decode is filtered by the sid's JSON form` → a sid inside another field is decoded then dropped by the exact check (b3 in the test); a None/empty sid keeps the unfiltered read; json.dumps(ensure_ascii=False) matches the writer fmhooks._event [tree d8d7438e34ea] (2026-10-29T19:42:17Z)
- (audit self) `self-review of the diff: _running keeps its exact session_id check; only the decode is filtered by the sid's JSON form` → no findings [tree d8d7438e34ea] (2026-10-29T19:42:17Z)
## Log
- 2026-10-29T19:10:05Z created
- 2026-10-29T19:37:11Z set tier=S
- 2026-10-29T19:37:14Z planned: it has criteria and steps
- 2026-10-29T19:37:15Z focused
- 2026-10-29T19:42:53Z done
- 2026-10-29T19:42:55Z committed fdd9bc40 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2022 [PERFORMANCE M, done, 2 steps] load_briefs reads closed briefs from a stat-checked index: a hook stops opening ~1150 done briefs — lesson: A stat-checked JSON ind…
- T-1821 [FEATURE M, done, 3 steps] FEATURE: one panic command stops every run, frees locks and leases and writes a stop recor — lesson: Editing plugin/rules/foreman.md ne…
- T-1026 [FEATURE M, done, 5 steps] And is the graph a node graph? like with lines connecting and stuff? how can we make the e — lesson: A flex-ordered layout gives spare …
- decision 2026-10-20: Foreman Code's TUI (T-1283) is a stdlib curses client of fm code's --json event stream with a widget layer that themes and extensions build on; exte…
## Measurements
Stop min 88 -> 81 ms (hook_t 15 runs x2, idle; medians noisy 97-102)
## Lessons
- A per-session filter over a shared log can skip decoding with a raw substring of the session id, keeping the exact check after
## Plan gaps
- failed first: step 1 Red test: _running decodes only this session's lines and still answers the same
## Files touched
- plugin/tests/test_hooks.py
- plugin/lib/fmhooks.py
- CHANGELOG.md

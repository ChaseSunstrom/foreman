---
id: T-0408
type: FIX
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-09T04:31:22Z
updated: 2026-10-09T04:32:54Z
base: 97cd56812eac601b632ed5fd4ec516e0899bebc9
base_tree: a30908832128502aa0203073b7af3f5e700b7011
verified: strong
---
# fm lane rm treats tool caches (.pytest_cache, .mypy_cache, .ruff_cache, node_modules, .vite, .svelte-kit, .gradle, .coverage …) like __pycache__ (JARVIS cleaned them by hand before each rm and hit the guard)
## Raw request
> fm lane rm treats tool caches (.pytest_cache, .mypy_cache, .ruff_cache, node_modules, .vite, .svelte-kit, .gradle, .coverage …) like __pycache__ (JARVIS cleaned them by hand before each rm and hit the guard)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a lane whose only leftovers are tool caches is removed; an ignored .env or build output still refuses — verify with `python3 plugin/tests/run.py -k test_lane_rm_ignores_tool_caches`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] test-first, then widen _CACHE
## Resume here
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py -k test_lane_rm_ignores_tool_caches` → ✗ exit 1 · Ran 1 tests in 0.6s (1 classes, 16 at a time; slowest: Contract 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 6b6670f00dac] (2026-10-09T04:31:40Z)
- `python3 plugin/tests/run.py -k test_lane_rm_ignores_tool_caches` → exit 0 · Ran 1 tests in 0.7s (1 classes, 16 at a time; slowest: Contract 1s) / OK [ran] [tree 6b6670f00dac] (2026-10-09T04:31:40Z)
- (step 1) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · PASS  routing              routing tables sound / fm doctor: OK (27 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                32.1    33.7     150  [0] / SessionEnd                  29.4    31.1     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/** changed since its pass at 00:30 UTC; python3 plugin/tests/run.py → exit 0 · Ran 941 tests in [ran] [tree 5fa7213ec03e] (2026-10-09T04:32:53Z)
- (ac 1) `python3 plugin/tests/run.py -k test_lane_rm_ignores_tool_caches` → exit 0 · Ran 1 tests in 0.7s (1 classes, 16 at a time; slowest: Contract 1s) / OK [ran] [tree 5fa7213ec03e] (2026-10-09T04:32:54Z)
- (audit intent) `self: an allowlist of regenerable tool caches; everything else ignored still refuses` → JARVIS's .pytest_cache + __pycache__ lanes come off with fm lane rm (test) [tree 5fa7213ec03e] (2026-10-09T04:32:54Z)
- (audit edge) `self: an allowlist of regenerable tool caches; everything else ignored still refuses` → an ignored .env refuses by name (test); build/ and dist/ stay refusing (artifacts someone may want) [tree 5fa7213ec03e] (2026-10-09T04:32:54Z)
- (audit self) `self: an allowlist of regenerable tool caches; everything else ignored still refuses` → no findings [tree 5fa7213ec03e] (2026-10-09T04:32:54Z)
## Log
- 2026-10-09T04:31:22Z created
- 2026-10-09T04:31:22Z focused
- 2026-10-09T04:32:54Z done
- 2026-10-09T04:32:54Z committed 3b671a7 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-0377 [FIX S, done, 1 steps] fm lane merge ID merges a reviewed builder branch on Foreman's own repo; fm lane rm treats __pycache__ as disposable — lesson: A guard that…
- T-0379 [FIX S, done, 1 steps] Builder brief: start from the main checkout's commit; isolation refusals are reported for the main thread, not retried — lesson: Watch the …
- research rsi-20261009-review: 1. **Answer.** Two guard-related frictions are grounded in code: the guard misreads remote interpreter code run over `ssh` as local Foreman…
- decision 2026-10-06: The desktop app lives in its own repo (~/projects/foreman-desktop), not apps/desktop in the Foreman checkout
- similar finished tasks took 1–1 steps
## Files touched
- plugin/tests/test_builder.py
- plugin/lib/fmlanes.py
- CHANGELOG.md

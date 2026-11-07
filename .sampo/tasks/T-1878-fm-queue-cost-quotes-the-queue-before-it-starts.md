---
id: T-1878
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-28T23:04:55Z
updated: 2026-10-29T00:56:19Z
base: 349e83bc92e9353998b36c3cd99c8495cacfdc0a
base_tree: 94f4bb31eb50f137074b38b64c1854231578e99b
plan0_at: 2026-10-29T00:47:47Z
plan0_scope: []
verified: strong
---
# Fm queue --cost quotes the queue before it starts: a per-tier median from fm cost history,
## Raw request
> FEATURE: fm queue --cost quotes the queue before it starts: a per-tier median from fm cost history, summed, against today's budget
> CONTEXT: forever loop round 5 ("Bill-of-effort quote for a queue before it starts", "Quote and enforce a queue's cost before it starts"); quote only, nothing refused.
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] fm queue --cost quotes the queue from finished tasks of each type and tier, names the ones with no history, refuses nothing — verify with `python3 plugin/tests/run.py test_queue_preview`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test: quote from mocked costs, and the CLI flag
2. [x] queue_quote, quote_line and the --cost flag; green
3. [x] docs: CHANGELOG, MASTER
## Resume here
<!-- auto -->
- 2026-10-29T00:54:25Z step 3/3: docs: CHANGELOG, MASTER
- git: foreman/build; 5 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmcost.py, plugin/tests/test_queue_preview.py
- touched since last checkpoint: plugin/lib/fmcli.py, plugin/lib/fmcost.py, plugin/tests/test_queue_preview.py, CHANGELOG.md, MASTER.md, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/t1885/security/command-guard.md, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/t1885/fix/cli-errors.md, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/t1885/perf/benchmark-statistics.md, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/t1885/release/ship-to-main.md, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/t1885/perf/regex-backtracking.md, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/t1885/review/surface-parity.md, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/t1885route.py, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/e1885t.txt, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/t1885/perf/INDEX.md, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/t1885/security/INDEX.md
## Docs impact
~/.claude/foreman/CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_queue_preview` → red as expected (exit 1) · Ran 2 tests in 3.5s (2 classes, 16 at a time; slowest: QueuePreview 3s, QueueQuote 1s) / FAILED (1 classes) [ran] [tree 11ca95828657] (2026-10-29T00:47:55Z)
- (step 2) `python3 plugin/tests/run.py test_queue_preview` → ✗ exit 1 · Ran 2 tests in 3.4s (2 classes, 16 at a time; slowest: QueuePreview 3s, QueueQuote 1s) / FAILED (1 classes) [ran] [tree 6a39f656f2d3] (2026-10-29T00:48:03Z)
- (ac 1) `python3 plugin/tests/run.py test_queue_preview 2>&1 | grep -v "^Ran\|^$" | head -40` → ✗ exit 1 · FAILED (failures=1) / FAILED (1 classes) [ran] [tree 6a39f656f2d3] (2026-10-29T00:48:09Z)
- (ac 1) `python3 plugin/tests/run.py test_queue_preview 2>&1 | grep -v "^$" | grep -B2 -A12 "Error\|FAIL" | head -30` → ✗ exit 1 · Ran 2 tests in 3.5s (2 classes, 16 at a time; slowest: QueuePreview 3s, QueueQuote 1s) / FAILED (1 classes) [ran] [tree 6a39f656f2d3] (2026-10-29T00:48:22Z)
- (step 2) `python3 plugin/tests/run.py test_queue_preview` → exit 0 · Ran 2 tests in 4.6s (2 classes, 16 at a time; slowest: QueuePreview 4s, QueueQuote 3s) / OK [ran] [tree bfb4e2b7493d] (2026-10-29T00:48:48Z)
- `python3 plugin/tests/run.py test_queue_preview` → ✗ exit 1 · Ran 2 tests in 5.3s (2 classes, 16 at a time; slowest: QueuePreview 4s, QueueQuote 3s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree bfb4e2b7493d] (2026-10-29T00:48:58Z)
- `python3 plugin/tests/run.py test_queue_preview` → exit 0 · Ran 2 tests in 3.9s (2 classes, 16 at a time; slowest: QueuePreview 3s, QueueQuote 3s) / OK [ran] [tree bfb4e2b7493d] (2026-10-29T00:48:58Z)
- (step 3) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmcli.py, plugin/lib/fmcost.py — commit it through a task, or git checkout it back / fm doctor: OK (49 pass, 5 warn, ; python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                41.2    45.3     150  [0] / SessionEnd                  35.7    39.2     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under [ran] [tree d1cf3f5d17df] (2026-10-29T00:55:33Z)
- (ac 1) `python3 plugin/tests/run.py test_queue_preview` → exit 0 · Ran 2 tests in 1.8s (2 classes, 16 at a time; slowest: QueuePreview 2s, QueueQuote 1s) / OK [ran] [tree d1cf3f5d17df] (2026-10-29T00:55:50Z)
- (audit intent) `self: quote sums per (type,tier) medians from finished tasks with ≥2 costs; no-history tasks listed, never refused` → fm queue --cost prints one quote line plus data.quote in --json; plain fm queue unchanged [tree d1cf3f5d17df] (2026-10-29T00:55:50Z)
- (audit adversary) `self: quote sums per (type,tier) medians from finished tasks with ≥2 costs; no-history tasks listed, never refused` → read-only, no outbound calls; costs from local ledger only [tree d1cf3f5d17df] (2026-10-29T00:55:50Z)
- (audit edge) `self: quote sums per (type,tier) medians from finished tasks with ≥2 costs; no-history tasks listed, never refused` → empty queue prints no quote; type/tier without 2+ history counted under no history [tree d1cf3f5d17df] (2026-10-29T00:55:50Z)
- (audit self) `self: quote sums per (type,tier) medians from finished tasks with ≥2 costs; no-history tasks listed, never refused` → no findings [tree d1cf3f5d17df] (2026-10-29T00:55:50Z)
## Log
- 2026-10-28T23:04:55Z created
- 2026-10-29T00:27:45Z set tier=S
- 2026-10-29T00:47:46Z focused
- 2026-10-29T00:56:18Z done
- 2026-10-29T00:56:19Z committed ac71d5a1 (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1057 [FEATURE M, done, 3 steps] Forever loop: fm loop on makes Foreman improve itself without end: when the queue and inbo — lesson: An invariant that ends a loop must…
- T-0676 [FEATURE M, done, 7 steps] Milestone: Features — Performance and cost — lesson: A 'degrade when over pace' rule must name what is optional: side offers and self-i…
- T-1879 [CLEAN M, done, 3 steps] Robustness sweep: every state-reading verb survives a malformed brief or meta (truncated f — lesson: An idempotence check compares what t…
- decision 2026-10-16: Recommendation: build the 15 grounded items T-1155..T-1169 with up to 4 builders, then run round 3 against the improved tree; would change if: round…
## Lessons
- A test fixture that finishes a FIX task needs the Regression-test waiver section, or finish refuses it
## Plan gaps
- failed first: step 2 queue_quote, quote_line and the --cost flag; green
## Files touched
- plugin/tests/test_queue_preview.py
- plugin/lib/fmcli.py
- plugin/lib/fmcost.py
- CHANGELOG.md
- MASTER.md

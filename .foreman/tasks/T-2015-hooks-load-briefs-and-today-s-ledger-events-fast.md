---
id: T-2015
type: PERFORMANCE
tier: S
status: done
priority: normal
scope: [plugin/lib/fmcore.py, plugin/tests/test_core.py, plugin/tests/test_ledger_chain.py, CHANGELOG.md, MASTER.md]
depends_on: []
source: user
created: 2026-10-29T16:44:53Z
updated: 2026-10-29T16:53:10Z
base: 3eaf247c4dff30e2f8506c1501db4eda0f8be3cb
base_tree: 1946184e89461e31ee8156ed619fda38dd974e90
plan0_at: 2026-10-29T16:44:54Z
plan0_scope: [plugin/lib/fmcore.py, plugin/tests/test_core.py, plugin/tests/test_ledger_chain.py, CHANGELOG.md, MASTER.md]
verified: strong
---
# Hooks load briefs and today's ledger events faster: sections split on read, precompiled frontmatter regex, ledger_events since seeks the tail
## Raw request
> Hooks load briefs and today's ledger events faster: sections split on read, precompiled frontmatter regex, ledger_events since seeks the tail
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] a parsed brief leaves its sections unsplit until read; copies stay apart — verify with `python3 plugin/tests/run.py test_core -k split_only_when_read`
- [x] ledger_events since= parses only the tail past since — verify with `python3 plugin/tests/run.py test_ledger_chain -k since_reads_only_the_tail`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] lazy sections, precompiled regexes, _parse_value fast path (measure first load before/after)
2. [x] ledger_events seeks back from the end to since (measure fmrisk.status before/after)
## Resume here
<!-- auto -->
- 2026-10-29T16:45:53Z step 1/2: lazy sections, precompiled regexes, _parse_value fast path (measure first load before/after)
- git: foreman/build; 3 uncommitted: plugin/lib/fmcore.py, plugin/tests/test_core.py, plugin/tests/test_ledger_chain.py
- touched since last checkpoint: plugin/tests/test_core.py, plugin/tests/test_ledger_chain.py, plugin/lib/fmcore.py
## Docs impact
## Verification evidence
- `python3 plugin/tests/run.py test_core -k split_only_when_read` → ✗ exit 1 · Ran 1 tests in 1.1s (1 classes, 16 at a time; slowest: Briefs 0s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 8f5dc4335e07] (2026-10-29T16:45:33Z)
- `python3 plugin/tests/run.py test_core -k split_only_when_read` → ✗ exit 1 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Briefs 0s) / FAILED (1 classes) [ran] [tree 8f5dc4335e07] (2026-10-29T16:45:33Z)
- (step 1) `python3 plugin/tests/run.py test_core test_ledger_chain` → exit 0 · Ran 111 tests in 6.0s (22 classes, 16 at a time; slowest: Chain 6s, Receipt 2s, WritesAndLocks 2s) / OK [ran] [tree ab04957e6cd8] (2026-10-29T16:48:10Z)
- (step 2) `python3 plugin/tests/run.py test_ledger_chain -k since_reads_only_the_tail` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: Chain 0s) / OK [ran] [tree ab04957e6cd8] (2026-10-29T16:48:14Z)
- `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  version skew         uidemo-982f4c ran 1.2.29, lacks 317 (T-0275, T-0705, T-0787, T-0933 …) — restart their sessions on the new Foreman / fm doctor: OK (50 pass, 4 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                41.0    42.3     150  [0] / SessionEnd                  36.2    40.4     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui/* [ran] [tree ff7ba731c472] (2026-10-29T16:52:47Z)
- (ac 1) `python3 plugin/tests/run.py test_core -k split_only_when_read` → exit 0 · Ran 1 tests in 0.3s (1 classes, 16 at a time; slowest: Briefs 0s) / OK [ran] [tree ff7ba731c472] (2026-10-29T16:53:00Z)
- (ac 2) `python3 plugin/tests/run.py test_ledger_chain -k since_reads_only_the_tail` → exit 0 · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: Chain 0s) / OK [ran] [tree ff7ba731c472] (2026-10-29T16:53:00Z)
- (audit intent) `self: diffed lazy sections (render/copy/parse against the old split, round-trip test) and the ledger seek (only writer is log_event stamping now(); empty file, ts-less chunks and since past the end all handled; same events asserted on the 18 MB copy)` → hooks load faster with identical results: same events asserted before/after, brief round-trip lossless [tree ff7ba731c472] (2026-10-29T16:53:00Z)
- (audit edge) `self: diffed lazy sections (render/copy/parse against the old split, round-trip test) and the ledger seek (only writer is log_event stamping now(); empty file, ts-less chunks and since past the end all handled; same events asserted on the 18 MB copy)` → no-section brief → [], oversized line keeps walking back, since after every event reads one chunk and returns [] [tree ff7ba731c472] (2026-10-29T16:53:00Z)
- (audit self) `self: diffed lazy sections (render/copy/parse against the old split, round-trip test) and the ledger seek (only writer is log_event stamping now(); empty file, ts-less chunks and since past the end all handled; same events asserted on the 18 MB copy)` → no findings [tree ff7ba731c472] (2026-10-29T16:53:00Z)
## Log
- 2026-10-29T16:44:53Z created
- 2026-10-29T16:44:53Z focused
- 2026-10-29T16:47:50Z hypothesis: hooks pay ~50 ms splitting sections they never read and a full 18 MB ledger parse for today's events; lazy sections + tail seek cut both without changing results
- 2026-10-29T16:48:10Z numbers (S/st copy, 1199 briefs, 18 MB ledger): first load_briefs min 74 -> 32 ms (median 76 -> 36), memoized 10 -> 7 ms; ledger_events(today, 2 kinds) 30.1 -> 2.8 ms, identical events
- 2026-10-29T16:53:08Z done
- 2026-10-29T16:53:10Z committed 102e58e7 (5 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1137 [FEATURE S, done, 2 steps] Record stage changes on the ledger (a stage_change event when fm's stage() moves), so pane — lesson: When a log hooks the main write pa…
- T-1669 [FEATURE M, done, 4 steps] Fm drill: compound fault days in a temp home, promotion by false-positive rate (from T-155 — lesson: A corrupt meta.json hides its proj…
- T-1906 [FIX S, done, 3 steps] Fm task finish checks a FIX's red-to-green proof before running its checks — lesson: A refusal known before the checks run must be said bef…
- decision 2026-10-16: T-1080 self-approved under full autonomy: risk points from today's ledger (destructive guard blocks 1, failed closes 2) and today's Revert commits (…
- likely tests for the scope: plugin/tests/test_core.py
## Measurements
first load_briefs (1199 briefs): min 74 ms → 32 ms (median 76 → 36); memoized 10 → 7 ms; ledger_events(today, 2 kinds): 30.1 ms → 2.8 ms
## Files touched
- plugin/tests/test_core.py
- plugin/tests/test_ledger_chain.py
- plugin/lib/fmcore.py
- MASTER.md
- CHANGELOG.md

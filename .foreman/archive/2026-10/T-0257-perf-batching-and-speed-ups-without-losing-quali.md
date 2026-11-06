---
id: T-0257
type: PERFORMANCE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-04T05:27:28Z
updated: 2026-10-04T05:45:33Z
base: 7b6c604dacc115136abbeb581aa26702ac1eec98
base_tree: c8e9d0f074996128062a41133b849df6aa8c9682
verified: strong
---
# fm batch: several small requests worked as one task — one plan, one gate run, one review, one commit — and fm next suggests it
## Raw request
> PERF: batching and speed-ups without losing quality or raising cost — e.g. related small tasks worked as one batch (one plan read, one gate run, one combined review, one commit each), gates and reviews shared across a batch, parallel builders where scopes don't overlap; measured with fm bench (time, cost, pass rate)
## Interpretation
Speed up the queue without losing quality or raising cost: most of a small task's time is fixed overhead (planning reads, a full gate run, a reviewer pass, a commit). Work related small requests as one batch so that overhead is paid once, keeping each request's criteria and closing each one honestly.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm batch makes one host brief from not-yet-started items (criteria and steps from each), hides the members from the inbox and queue, refuses started ones, and closes them done-in the host when it is done; fm next suggests a batch when three or more small items of one type lead the inbox — verify with `python3 plugin/tests/run.py -k test_batch`
## Non-goals
## Approach (options → choice → why)
A) a multi-active-task mode: breaks per-task change attribution (focus snapshots) and the one-active-task invariant. B) one host task built from the members (criteria and steps copied from each, meta batch), members hidden from inbox/queue while batched and closed done-in the host when it is done — reuses the existing done-in link and every gate. Choice: B; fm next suggests it for ≥3 small items of one type at the head of the inbox.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Tests first
2. [x] fm batch + member closing + fm next suggestion; docs
## Resume here
T-0257: tests written (test_batch.py, red); paused for urgent T-0259 intake fix — batch copies members' own DONE-WHEN, which needs per-item lines
<!-- auto -->
- 2026-10-04T05:37:58Z step 1/2: Tests first
- git: foreman/build; 1 uncommitted: plugin/tests/test_batch.py
- touched since last checkpoint: plugin/tests/test_batch.py
## Docs impact
MASTER.md, CHANGELOG.md, plugin/skills/intake/references/execute.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_batch` → exit 0 · Ran 4 tests in 2.6s (1 classes, 16 at a time; slowest: Batch 3s) / OK [ran] [tree eb36f1d411c5] (2026-10-04T05:42:32Z)
- (step 2) `python3 plugin/tests/run.py -k test_batch` → exit 0 · Ran 4 tests in 2.6s (1 classes, 16 at a time; slowest: Batch 3s) / OK [ran] [tree eb36f1d411c5] (2026-10-04T05:42:35Z)
- (step 1) `python3 plugin/tests/run.py -k test_batch` → exit 0 · Ran 5 tests in 3.3s (1 classes, 16 at a time; slowest: Batch 3s) / OK [ran] [tree 934fe121192e] (2026-10-04T05:44:34Z)
- (step 2) `python3 plugin/tests/run.py -k test_batch` → exit 0 · Ran 5 tests in 3.3s (1 classes, 16 at a time; slowest: Batch 3s) / OK [ran] [tree 934fe121192e] (2026-10-04T05:44:37Z)
- `python3 plugin/tests/run.py -k test_batch` → ✗ exit 1 · Ran 5 tests in 2.1s (1 classes, 16 at a time; slowest: Batch 2s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree 934fe121192e] (2026-10-04T05:44:43Z)
- `python3 plugin/tests/run.py -k test_batch` → exit 0 · Ran 5 tests in 3.3s (1 classes, 16 at a time; slowest: Batch 3s) / OK [ran] [tree 934fe121192e] (2026-10-04T05:44:43Z)
- (ac 1) `python3 plugin/tests/run.py -k test_batch` → exit 0 · Ran 5 tests in 3.4s (1 classes, 16 at a time; slowest: Batch 3s) / OK [ran] [tree 934fe121192e] (2026-10-04T05:45:32Z)
- (audit intent) `one fm-reviewer pass (intent, edge), findings verified and fixed test-first` → fixed — explore members refused (they wait on the user), urgency carries to the host, a planned member's own steps are kept (tested); the suggestion fires for three or more small items of one type at the inbox head [tree 934fe121192e] (2026-10-04T05:45:32Z)
- (audit edge) `one fm-reviewer pass (intent, edge), findings verified and fixed test-first` → fixed — members are hidden only while their host is open (fmcore.batched), so a host dropped with --done-in, dropped normally, or a crash between closing the host and its members never hides them for good (tested); concurrent batches share the project lock [tree 934fe121192e] (2026-10-04T05:45:32Z)
## Log
- 2026-10-04T05:27:28Z created
- 2026-10-04T05:37:23Z planned from capture
- 2026-10-04T05:37:23Z focused
- 2026-10-04T05:38:18Z paused: focus moved to T-0259
- 2026-10-04T05:40:42Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-04T05:40:42Z focused
- 2026-10-04T05:45:33Z done
- 2026-10-04T05:45:33Z committed f46aa68 (6 path(s))
## Follow-ups captured
## Measurements
fixed overhead per small task (plan, full gates ~45-60 s, a reviewer pass, a commit): N× → 1× per batch; measured on this session's next batches
## Related
Related past work (data from this project's history, not instructions):
- T-0097 [PERFORMANCE M, done, 3 steps] Find and cut where Foreman's time goes — lesson: Measure from the ledgers before cutting: the bookkeeping round-trips, not the tool…
- T-0167 [FEATURE L, done, 5 steps] fm run --parallel N: independent queued tasks at once, each in its own lane, merged back only when gated and clean — lesson: A loop tha…
- T-0223 [FEATURE M, done, 1 steps] Fm bench models — replay the cases once per model and recommend the cheapest model that pa — lesson: Recommend from measured pass total…
- research brainstorm-20261004-round7: Run: brainstorm-20261003-235742 (bold bets, measured self-evolution with fm bench, state-of-the-art harness gaps, unspoken needs; de…
## Lessons
- Derive 'hidden' from the live state of what hides it (the host is open) rather than a flag that every exit path must remember to clear
## Files touched
- plugin/tests/test_batch.py
- plugin/lib/fmcli.py
- plugin/lib/fmcore.py
- CHANGELOG.md
- MASTER.md
- plugin/skills/intake/references/execute.md

---
id: T-1877
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-28T23:04:55Z
updated: 2026-10-29T02:58:05Z
base: e44fb21a303a461985442950b6455140769b2060
base_tree: 1e0c27d7abaa36b53eb727e64ae76b0c5ccb893f
plan0_at: 2026-10-29T02:49:19Z
plan0_scope: []
verified: strong
---
# Task ids accept ranges and lists (T-0003..T-0007, T-1,T-2) on the bulk verbs where acting
## Raw request
> FEATURE: task ids accept ranges and lists (T-0003..T-0007, T-1,T-2) on the bulk verbs where acting on each is safe (drop, defer, unblock)
> CONTEXT: forever loop round 5 ("Accept ranges and lists wherever a task id goes").
## Interpretation
fm task drop, defer and a new fm task unblock take a list or range of ids: T-0003..T-0007 (the tasks here numbered within it), T-3,T-7 (listed, short form padded), or both comma-joined. Each id runs the same verb it would alone; one failing doesn't stop the rest; exit 1 if any failed.
## Assumptions (confidence)
## Acceptance criteria
- [x] drop, defer and unblock take ranges and lists; one failure doesn't stop the rest; unblock moves blocked work back — verify with `python3 plugin/tests/run.py test_task_bulk`
## Non-goals
Ranges on block (each block needs its own reason), done, finish or set. Space-separated id lists.
## Approach (options → choice → why)
Options: (a) expand in _task_shape into repeated argv runs; (b) expand in cmd_task and loop the existing single-id path per id; (c) a new fm bulk verb. Choice (b): the single-id path keeps every rule (no-op repeats, closed refusals, drop snapshots), the loop is ~15 lines. task_ids(p, spec) expands (cap 50 ids, typo guard); _TASK_IDS lets _task_shape keep a range as the id instead of inserting the active task. unblock: blocked → planned (captured with no criteria), revisit cleared, logged; refuses a task that isn't blocked. --json gives {ok, failed}.
## Risks and rollback
A wide range drops much at once: capped at 50 ids and drop still needs a reason; each drop is reversible (fm task set ID status=planned). Rollback: git revert the commit.
## Execution prompt
## Steps
1. [x] Failing tests: range/list expansion, cap, per-id failure, unblock, _task_shape keeps a range
2. [x] Implement task_ids, _task_each, unblock, _TASK_IDS
3. [x] Docs: CHANGELOG, MASTER, help
## Resume here
<!-- auto -->
- 2026-10-29T02:56:12Z steps 3/3 done
- git: foreman/build; 4 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/tests/test_task_bulk.py
- touched since last checkpoint: CHANGELOG.md, MASTER.md, plugin/tests/test_task_bulk.py, plugin/lib/fmcli.py
## Docs impact
MASTER.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_task_bulk` → red as expected (exit 1) · Ran 2 tests in 3.1s (1 classes, 16 at a time; slowest: Bulk 3s) / FAILED (1 classes) [ran] [tree d4831a2ea30e] (2026-10-29T02:49:27Z)
- (step 2) `python3 plugin/tests/run.py test_task_bulk test_task_cli` → ✗ exit 1 · run.py: no test matches test_task_cli [ran] [tree 9cfdeee055d1] (2026-10-29T02:49:32Z)
- (step 2) `python3 plugin/tests/run.py test_task_bulk test_hooks_task_shape` → ✗ exit 1 · run.py: no test matches test_hooks_task_shape [ran] [tree 9cfdeee055d1] (2026-10-29T02:49:40Z)
- (step 2) `python3 plugin/tests/run.py test_task_bulk` → exit 0 · Ran 2 tests in 5.0s (1 classes, 16 at a time; slowest: Bulk 5s) / OK [ran] [tree 9cfdeee055d1] (2026-10-29T02:49:49Z)
- (step 3) `grep -c T-1877 CHANGELOG.md MASTER.md` → exit 0 · CHANGELOG.md:1 / MASTER.md:1 [ran] [tree 082bb904bbcd] (2026-10-29T02:49:53Z)
- (step 2) `python3 plugin/tests/run.py test_task_bulk` → exit 0 · Ran 3 tests in 3.6s (1 classes, 16 at a time; slowest: Bulk 3s) / OK [ran] [tree b00b31369cdf] (2026-10-29T02:53:10Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmcli.py — commit it through a task, or git checkout it back / fm doctor: OK (49 pass, 5 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                41.0    45.4     150  [0] / SessionEnd                  35.7    42.4     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui [ran] [tree b00b31369cdf] (2026-10-29T02:57:24Z)
- (ac 1) `python3 plugin/tests/run.py test_task_bulk` → exit 0 · Ran 3 tests in 3.6s (1 classes, 16 at a time; slowest: Bulk 3s) / OK [ran] [tree b00b31369cdf] (2026-10-29T02:57:39Z)
- (audit intent) `one fm-reviewer pass over the diff: one MEDIUM (a brief that won't parse raised ValueError past the loop, so later ids never ran) fixed test-first; closed or mismatched ids in a range count as failures by design` → fm task drop/defer/unblock take T-a..T-b and T-a,T-b; each id acts or fails by name, exit 1 if any failed [tree b00b31369cdf] (2026-10-29T02:57:39Z)
- (audit edge) `one fm-reviewer pass over the diff: one MEDIUM (a brief that won't parse raised ValueError past the loop, so later ids never ran) fixed test-first; closed or mismatched ids in a range count as failures by design` → corrupt brief fails by name, the rest still run [tree b00b31369cdf] (2026-10-29T02:57:39Z)
## Log
- 2026-10-28T23:04:55Z created
- 2026-10-29T00:53:50Z set status=planned
- 2026-10-29T02:49:19Z focused
- 2026-10-29T02:53:11Z review: approve with nits; fixed the medium (a brief that won't parse or vanishes now fails by name, the rest still run; test added) and KeyError's quoted repr. Kept: a range counts closed or mismatched tasks as failures (deliberate, tested). task_unblock lands in the story's Steps chapter like task_block.
- 2026-10-29T02:58:04Z done
- 2026-10-29T02:58:05Z committed 0452a0d4 (4 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1879 [CLEAN M, done, 3 steps] Robustness sweep: every state-reading verb survives a malformed brief or meta (truncated f — lesson: An idempotence check compares what t…
- playbook Interaction: feedback, keyboard, forms, words and the phone (fm playbooks show ui/interaction)
- T-1405 [FIX M, done, 4 steps] Crash hygiene: stack dumps for hung verbs, safe stale index.lock removal, a lock probe in doctor — lesson: A safety rule written as 'unknow…
- decision 2026-10-16: T-1054: every wild cluster (23) plus the earlier catalogue's skips became briefs T-1057..T-1087; the forever loop (T-1057) goes first after the demo…
- similar finished tasks took 3–4 steps
## Lessons
- A bulk loop over briefs must catch parse errors (ValueError) as well as policy errors, or one bad brief stops the rest
## Plan gaps
- failed first: step 2 Implement task_ids, _task_each, unblock, _TASK_IDS
## Files touched
- plugin/tests/test_task_bulk.py
- plugin/lib/fmcli.py
- CHANGELOG.md
- MASTER.md

---
id: T-1099
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/fmtidy.py, plugin/lib/fmcore.py, plugin/tests/test_ledger_chain.py, plugin/tests/test_tidy.py]
depends_on: []
source: discovered
created: 2026-10-16T04:43:15Z
updated: 2026-10-16T05:26:15Z
base: 7fc55bd1755bf9963b48a1a5d35e85b35e1f3130
base_tree: 74f8308375d4ee4be9ee4738d122a336a9317759
verified: strong
---
# Ledger roll takes the ledger lock and keeps time order: _roll_ledger keeps unparseable-ts
## Raw request
> Ledger roll takes the ledger lock and keeps time order: _roll_ledger keeps unparseable-ts lines live (reordering a chain), never flocks (a racing writer's line can be lost), and opens text-mode (UnicodeDecodeError on a bad byte); an old-version writer can land between a new writer's tail read and write (false break)
## Interpretation
The ledger roll must not lose or reorder lines. Already covered: `_roll_ledger` runs under `c.lock(p.dir)` (fmtidy.py:254), but that is the `.lock` file. `log_event` flocks `ledger.jsonl` itself (fmcore.py:780), so the roll never excludes a writer. Still wrong: a line whose `ts` is unparseable goes to the current month and stays live (fmtidy.py:259-262); the file is read in text mode (fmtidy.py:256), so a bad byte raises `UnicodeDecodeError`; and the 23-hour `ts` and `prev` order can break.
## Assumptions (confidence)
## Acceptance criteria
- [x] A racing writer's line survives the roll, and `verify-ledger` stays green — verify with `python3 plugin/tests/run.py test_ledger_chain`
- [x] A bad byte or an unparseable `ts` doesn't break the roll or reorder the chain — verify with `python3 plugin/tests/run.py test_ledger_chain`
## Non-goals
## Approach (options → choice → why)
(a) Patch the three symptoms separately. (b) Rewrite `_roll_ledger` in binary under the ledger flock, with an unparseable `ts` inheriting the previous line's month. (c) Add a lock helper to fmcore. Choice: (b). The old-version-writer race can't be closed without changing old writers, so document it as a ceiling in a `ponytail:` comment. - Open `ledger.jsonl` as `r+b`, take `fcntl.flock(LOCK_EX)`, and read the lines as bytes. - Decode each line with `errors="replace"` only for the `ts` lookup. - Roll a line to the archive only when its month, or the carried-forward month, is below the current one. Never keep a line live that sits between rolled lines. - Write the live remainder back in place, still under the flock. `write_atomic` swaps the inode, so a writer that already holds the old fd would write to the unlinked file. Truncate and rewrite instead.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests in test_ledger_chain.py: a ledger with an invalid utf-8 byte rolls without raising; an unparseable-ts line between old lines is archived with them; with the flock held in a thread, the roll waits and then keeps the writer's line.
2. [x] Rewrite `_roll_ledger` as above.
3. [x] Review fixes: crash-safe rewrite through a sidecar, no double archive, RecursionError, no ledger_rolled when nothing rolled
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_ledger_chain` → ✗ exit 1 · Ran 20 tests in 2.5s (2 classes, 16 at a time; slowest: Chain 2s, Receipt 1s) / FAILED (1 classes) [ran] [tree 6098384fd744] (2026-10-16T05:14:28Z)
- (step 2) `python3 plugin/tests/run.py test_ledger_chain test_tidy` → exit 0 · Ran 37 tests in 5.2s (10 classes, 16 at a time; slowest: Chain 5s, StalePlans 5s, Apply 4s) / OK [ran] [tree eabdc8212676] (2026-10-16T05:17:16Z)
- (step 3) `python3 plugin/tests/run.py test_ledger_chain` → ✗ exit 1 · Ran 23 tests in 3.1s (2 classes, 16 at a time; slowest: Chain 3s, Receipt 1s) / FAILED (1 classes) [ran] [tree 4402900a9d2f] (2026-10-16T05:23:48Z)
- (step 3) `python3 plugin/tests/run.py test_ledger_chain test_tidy` → exit 0 · Ran 40 tests in 3.8s (10 classes, 16 at a time; slowest: Chain 4s, StalePlans 3s, Apply 2s) / OK [ran] [tree d666e3d57c4f] (2026-10-16T05:24:47Z)
- (step 3) `python3 plugin/tests/run.py test_board_export test_core test_diff_gates test_ledger_chain test_tidy` → exit 0 · Ran 123 tests in 10.4s (29 classes, 16 at a time; slowest: DiffGates 10s, BoardExport 6s, Chain 6s) / OK [ran] [tree d666e3d57c4f] (2026-10-16T05:25:22Z)
- (ac 1) `python3 plugin/tests/run.py test_ledger_chain` → exit 0 · Ran 23 tests in 3.3s (2 classes, 16 at a time; slowest: Chain 3s, Receipt 1s) / OK [ran] [tree 735261e25130] (2026-10-16T05:26:13Z)
- (ac 2) `python3 plugin/tests/run.py test_ledger_chain` → exit 0 · Ran 23 tests in 3.3s (2 classes, 16 at a time; slowest: Chain 3s, Receipt 1s) / OK [ran] [tree 735261e25130] (2026-10-16T05:26:13Z)
- (step 1) `python3 plugin/tests/run.py test_ledger_chain test_tidy` → exit 0 · Ran 40 tests in 3.6s (10 classes, 16 at a time; slowest: Chain 3s, StalePlans 2s, Apply 2s) / OK [ran] [tree 735261e25130] (2026-10-16T05:26:13Z)
- (audit adversary) `review: one fm-reviewer full pass; 4 findings fixed by the builder test-first (crash-safe rewrite via sidecar, no double archive, RecursionError, no empty ledger_rolled)` → same flock as log_event on the same inode; archived lines always a prefix (months never fall); a crash mid-rewrite resumes from the sidecar keeping lines logged after the crash [tree 735261e25130] (2026-10-16T05:26:13Z)
- (audit self) `review: one fm-reviewer full pass; 4 findings fixed by the builder test-first (crash-safe rewrite via sidecar, no double archive, RecursionError, no empty ledger_rolled)` → no findings [tree 735261e25130] (2026-10-16T05:26:13Z)
## Log
- 2026-10-16T04:43:15Z created
- 2026-10-16T05:01:15Z set scope=['plugin/lib/fmtidy.py', 'plugin/tests/test_ledger_chain.py']
- 2026-10-16T05:01:15Z set tier=S
- 2026-10-16T05:11:33Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1099.builder.md
- 2026-10-16T05:11:54Z focused
- 2026-10-16T05:16:33Z set scope=['plugin/lib/fmtidy.py', 'plugin/tests/test_ledger_chain.py', 'plugin/tests/test_tidy.py']
- 2026-10-16T05:16:34Z scope: + plugin/tests/test_tidy.py: test_rolls_large_ledger_by_month appended January lines after this month's, an out-of-order ledger the old roll reordered; fixture now puts past months first
- 2026-10-16T05:23:44Z set scope=['plugin/lib/fmtidy.py', 'plugin/lib/fmcore.py', 'plugin/tests/test_ledger_chain.py', 'plugin/tests/test_tidy.py']
- 2026-10-16T05:23:45Z scope: + plugin/lib/fmcore.py: write_atomic takes bytes too, so the roll's sidecar (raw ledger bytes) goes through it as review fix 1 asks
- 2026-10-16T05:25:56Z merged worktree-agent-af25212d285d0452e (4 file(s))
- 2026-10-16T05:26:01Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-af25212d285d0452e
- 2026-10-16T05:26:01Z focused
- 2026-10-16T05:26:01Z scope: CHANGELOG.md — release note for the merged builder work
- 2026-10-16T05:26:14Z done
- 2026-10-16T05:26:15Z committed 538f4e9 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1065-review: Verdict: changes needed.** Two MEDIUM findings, both about failures breaking normal use. I only read the code. This session had no shell, so I ra…
- research wave2-plan-af4fd23e40a859f90: === T-1028 [stale: plugin/lib/fmcli.py, plugin/lib/fmlanes.py, plugin/lib/fmtidy.py changed since it was written]
- T-1065 [SECURITY M, done, 2 steps] Tamper-evident ledger: each ledger line carries the hash of the one before; fm verify-ledg — lesson: A hot-path write that gains a loc…
- decision 2026-10-14: Keep the Read hook unscoped (T-0782 dropped)
- similar past tasks were M: consider --tier M
- the similar finished task took 2 steps
- likely tests for the scope: plugin/tests/test_tidy.py
## Lessons
- Rewriting a file other processes append to: lock it, keep a sidecar of what must survive, resume from the sidecar on the next run
## Plan gaps
- added late: Review fixes: crash-safe rewrite through a sidecar, no double archive, RecursionError, no ledger_rolled when nothing ro…
- failed first: step 1 Failing tests in test_ledger_chain.py: a ledger with an invalid utf-8 byte rolls without raising; a…
- failed first: step 3 Review fixes: crash-safe rewrite through a sidecar, no double archive, RecursionError, no ledger_ro…
## Files touched
- plugin/tests/test_ledger_chain.py
- plugin/lib/fmtidy.py
- plugin/tests/test_tidy.py
- plugin/lib/fmcore.py
- CHANGELOG.md

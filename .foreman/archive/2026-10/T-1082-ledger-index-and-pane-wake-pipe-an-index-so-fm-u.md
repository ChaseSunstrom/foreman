---
id: T-1082
type: PERFORMANCE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcore.py, plugin/tests/test_ledger_index.py, MASTER.md]
depends_on: []
source: user
created: 2026-10-16T04:03:35Z
updated: 2026-10-16T06:24:14Z
base: 0bbee986d67779162cd48e13bddb76bfcf10eea8
base_tree: 557040d252270a18ab3a48e4a4a4e48530e2d550
verified: strong
---
# Ledger index and pane wake pipe: an index so fm ui and recall don't rescan the ledger; the
## Raw request
> PERF: Ledger index and pane wake pipe: an index so fm ui and recall don't rescan the ledger; the pane wakes on state change instead of polling (catalogue C7 skips)
> CONTEXT: T-1054, the user: "do everything in that brainstorm, and even more for stuff that ISNT done, and even wilder ideas, these seem very simple" + "maybe a way to forever loop a brainstorm/yourself". Wild round: research brainstorm-20261016-wild-clusters (24 clusters). Earlier catalogue: research brainstorm-20261016-catalogue (its skip marks are now build marks too).
## Interpretation
Two parts: a ledger index so `fm ui` and `fm recall` stop re-reading the ledger, and a pane that wakes on a state change instead of a 2 s poll. Today `view()` reads `ledger_tail(5000)` plus a full-file `_closes_since` scan (`fmwatch.py:460,541`). `recall` reads `ledger_tail(p, 50000)` (`fmrecall.py:432`). `fm ui --follow` already waits on mtimes (`_follow`, `fmwatch.py:611`), but the mod still polls `fm ui --json` every 2 s (`register.tsx:553`). The wake pipe is the only part still to build.
## Assumptions (confidence)
## Acceptance criteria
- [x] load_briefs and ledger_tail re-use what this process already read from an unchanged file and hand out fresh copies (a mutation never leaks), and a change on disk is read again — verify with `python3 plugin/tests/run.py test_ledger_index`
- [x] fm ui --json on the real state is measurably faster (numbers in Measurements) — verify with `python3 plugin/tests/run.py test_ledger_index test_ui`
## Non-goals
## Approach (options → choice → why)
Options: (a) a sidecar ledger index (saves ≤0.18 s, adds a file that must track rolls and chain breaks); (b) a long-lived fm ui --follow in the mod (idle cost is already a few stats); (c) per-process memos: load_briefs re-uses a parse when the file's (mtime_ns, size) is unchanged and hands out fresh copies, ledger_tail serves a smaller n from the largest tail already read of an unchanged file. Choice: (c), the measured hot path, no new files, nothing to invalidate across processes. (a) and (b) captured as not worth it with the numbers.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: two loads of an unchanged brief parse once and return independent objects; an edited brief is re-read; a smaller ledger_tail after a larger one reads nothing new and equals a fresh read; an appended ledger is re-read.
2. [x] Memoize in fmcore.load_briefs/find_brief and ledger_tail; measure fm ui before → after.
3. [x] Docs (MASTER), CHANGELOG.
## Resume here
T-1082 in review
<!-- auto -->
- 2026-10-16T06:15:03Z step 3/3: Docs (MASTER), CHANGELOG.
- git: foreman/build; 4 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmcore.py, plugin/tests/test_ledger_index.py
- touched since last checkpoint: plugin/tests/test_ledger_index.py, plugin/lib/fmcore.py, CHANGELOG.md, MASTER.md
## Docs impact
MASTER.md Read memos; CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_ledger_index` → ✗ exit 1 · Ran 5 tests in 1.1s (1 classes, 16 at a time; slowest: Memo 1s) / FAILED (1 classes) [ran] [tree 69cd9206d6b1] (2026-10-16T06:13:09Z)
- (step 1) `python3 plugin/tests/run.py test_ledger_index test_core test_ledger_chain` → exit 0 · Ran 96 tests in 4.3s (19 classes, 16 at a time; slowest: Chain 4s, Receipt 2s, Memo 2s) / OK [ran] [tree c916b8098ae1] (2026-10-16T06:13:56Z)
- (step 2) `python3 plugin/tests/run.py test_ledger_index test_core test_ui test_watch` → exit 0 · Ran 97 tests in 15.0s (25 classes, 16 at a time; slowest: UiView 15s, WritesAndLocks 2s, Memo 1s) / OK [ran] [tree c916b8098ae1] (2026-10-16T06:14:33Z)
- (step 2) `python3 plugin/tests/run.py test_ledger_index` → ✗ exit 1 · Ran 7 tests in 3.2s (1 classes, 16 at a time; slowest: Memo 3s) / FAILED (1 classes) [ran] [tree 7b19923bf2c0] (2026-10-16T06:20:49Z)
- (step 2) `python3 plugin/tests/run.py test_ledger_index test_core test_ui test_watch` → exit 0 · Ran 99 tests in 18.7s (25 classes, 16 at a time; slowest: UiView 18s, Memo 2s, WritesAndLocks 2s) / OK [ran] [tree db040cfb98d5] (2026-10-16T06:21:35Z)
- (ac 1) `python3 plugin/tests/run.py test_ledger_index` → exit 0 · Ran 7 tests in 4.4s (1 classes, 16 at a time; slowest: Memo 4s) / OK [ran] [tree b6821c60fbf4] (2026-10-16T06:22:22Z)
- (ac 2) `python3 plugin/tests/run.py test_ledger_index test_ui` → exit 0 · Ran 31 tests in 22.2s (8 classes, 16 at a time; slowest: UiView 22s, Memo 4s, UiSkills 2s) / OK [ran] [tree b6821c60fbf4] (2026-10-16T06:22:22Z)
- (step 3) `python3 plugin/tests/run.py test_ledger_index` → exit 0 · Ran 7 tests in 4.4s (1 classes, 16 at a time; slowest: Memo 4s) / OK [ran] [tree b6821c60fbf4] (2026-10-16T06:22:22Z)
- (audit intent) `review: one fm-reviewer pass (combined with T-1048/T-1120); fixed test-first: _orig copies lists so in-place edits render (pre-existing bug), shallow copies only, uncached tails returned without copies, fresh (<2 s) briefs not kept, vanished briefs forgotten, memo caps` → fm ui pays one parse per brief and one ledger read per run [tree b6821c60fbf4] (2026-10-16T06:22:22Z)
- (audit adversary) `review: one fm-reviewer pass (combined with T-1048/T-1120); fixed test-first: _orig copies lists so in-place edits render (pre-existing bug), shallow copies only, uncached tails returned without copies, fresh (<2 s) briefs not kept, vanished briefs forgotten, memo caps` → no stale read: keys change on every write; a same-tick same-size rewrite can't be memoized (2 s rule); callers get copies [tree b6821c60fbf4] (2026-10-16T06:22:22Z)
- (audit edge) `review: one fm-reviewer pass (combined with T-1048/T-1120); fixed test-first: _orig copies lists so in-place edits render (pre-existing bug), shallow copies only, uncached tails returned without copies, fresh (<2 s) briefs not kept, vanished briefs forgotten, memo caps` → in-place list edits render; a deleted brief returns None and leaves the memo; non-dict JSONL records pass through [tree b6821c60fbf4] (2026-10-16T06:22:22Z)
- (audit operator) `review: one fm-reviewer pass (combined with T-1048/T-1120); fixed test-first: _orig copies lists so in-place edits render (pre-existing bug), shallow copies only, uncached tails returned without copies, fresh (<2 s) briefs not kept, vanished briefs forgotten, memo caps` → fm ui 0.67 s → 0.30 s measured at normal load; long-lived processes capped (5,000 briefs, 8 files × 20,000 lines) [tree b6821c60fbf4] (2026-10-16T06:22:22Z)
- (audit maintainer) `review: one fm-reviewer pass (combined with T-1048/T-1120); fixed test-first: _orig copies lists so in-place edits render (pre-existing bug), shallow copies only, uncached tails returned without copies, fresh (<2 s) briefs not kept, vanished briefs forgotten, memo caps` → _read_brief/Brief.copy and the tail memo live in fmcore beside what they cache; the 2 s and cap constants are named [tree b6821c60fbf4] (2026-10-16T06:22:22Z)
- `python3 plugin/tests/run.py test_ledger_index` → exit 0 · Ran 7 tests in 1.5s (1 classes, 16 at a time; slowest: Memo 1s) / OK [ran] [tree b6821c60fbf4] (2026-10-16T06:23:23Z)
- (audit intent) `review: one fm-reviewer pass (combined with T-1048/T-1120); fixed test-first: _orig copies lists so in-place edits render (pre-existing bug), shallow copies only, uncached tails returned without copies, fresh (<2 s) briefs not kept, vanished briefs forgotten, memo caps` → fm ui pays one parse per brief and one ledger read per run [tree b6821c60fbf4] (2026-10-16T06:23:23Z)
- (audit adversary) `review: one fm-reviewer pass (combined with T-1048/T-1120); fixed test-first: _orig copies lists so in-place edits render (pre-existing bug), shallow copies only, uncached tails returned without copies, fresh (<2 s) briefs not kept, vanished briefs forgotten, memo caps` → no stale read: keys change on every write; a same-tick same-size rewrite can't be memoized (2 s rule); callers get copies [tree b6821c60fbf4] (2026-10-16T06:23:23Z)
- (audit edge) `review: one fm-reviewer pass (combined with T-1048/T-1120); fixed test-first: _orig copies lists so in-place edits render (pre-existing bug), shallow copies only, uncached tails returned without copies, fresh (<2 s) briefs not kept, vanished briefs forgotten, memo caps` → in-place list edits render; a deleted brief returns None and leaves the memo; non-dict JSONL records pass through [tree b6821c60fbf4] (2026-10-16T06:23:23Z)
- (audit operator) `review: one fm-reviewer pass (combined with T-1048/T-1120); fixed test-first: _orig copies lists so in-place edits render (pre-existing bug), shallow copies only, uncached tails returned without copies, fresh (<2 s) briefs not kept, vanished briefs forgotten, memo caps` → fm ui 0.67 s → 0.30 s measured at normal load; long-lived processes capped (5,000 briefs, 8 files × 20,000 lines) [tree b6821c60fbf4] (2026-10-16T06:23:23Z)
- (audit maintainer) `review: one fm-reviewer pass (combined with T-1048/T-1120); fixed test-first: _orig copies lists so in-place edits render (pre-existing bug), shallow copies only, uncached tails returned without copies, fresh (<2 s) briefs not kept, vanished briefs forgotten, memo caps` → _read_brief/Brief.copy and the tail memo live in fmcore beside what they cache; the 2 s and cap constants are named [tree b6821c60fbf4] (2026-10-16T06:23:23Z)
## Log
- 2026-10-16T04:03:35Z created
- 2026-10-16T05:01:33Z set scope=['plugin/lib/fmcore.py', 'plugin/lib/fmwatch.py', 'plugin/lib/fmrecall.py', 'mods/foreman-ui/hooks/register.tsx', 'mods/foreman-ui/tests/foreman-ui.test.tsx', 'plugin/tests/test_ledger_index.py']
- 2026-10-16T05:01:33Z set tier=M
- 2026-10-16T05:56:29Z focused
- 2026-10-16T05:57:55Z paused: focus moved to T-1117
- 2026-10-16T05:58:30Z criterion 1 text: the index gives the same events as a full scan, extends after an append, and rebuilds after a tidy roll → load_briefs and ledger_tail re-use what this process already read from an unchanged file and hand out fresh copies (a mutation never leaks), and a change on disk is read again
- 2026-10-16T05:58:30Z criterion 2 verify: `cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → `python3 plugin/tests/run.py test_ledger_index test_ui`
- 2026-10-16T05:58:30Z criterion 2 text: the mod uses `--follow` lines and falls back to polling → fm ui --json on the real state is measurably faster (numbers in Measurements)
- 2026-10-16T05:58:34Z set scope=['plugin/lib/fmcore.py', 'plugin/tests/test_ledger_index.py', 'MASTER.md']
- 2026-10-16T05:58:40Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-16T05:58:40Z focused
- 2026-10-16T05:59:10Z paused: focus moved to T-1117
- 2026-10-16T06:12:55Z re-based: what other work changed while it was paused isn't its own change
- 2026-10-16T06:12:55Z focused
- 2026-10-16T06:14:33Z scope: CHANGELOG.md — release note (MASTER.md is in scope)
- 2026-10-16T06:15:45Z paused: focus moved to T-1122
- 2026-10-16T06:20:38Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-10-16T06:20:38Z focused
- 2026-10-16T06:23:21Z scope: CHANGELOG.md, plugin/lib/fmbench.py, plugin/lib/fmcli.py, plugin/lib/fmmutate.py, plugin/lib/fmreplay.py, plugin/tests/test_close_gates.py, plugin/tests/test_replay.py — other tasks' work (T-1066 merge, T-1117, T-1122) committed while this task waited for review; none is this task's edit
- 2026-10-16T06:24:14Z done
- 2026-10-16T06:24:14Z committed 9461f65 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1079 [PERFORMANCE S, done, 2 steps] Unexplained spend alarm: spend with no Foreman task or turn to explain it is flagged in fm — lesson: Window reports read every ledg…
- T-1072 [CLEAN M, done, 2 steps] Rule and hint hygiene: cards, known fixes, rules and lessons that never fired or never hel — lesson: A cleanup that deletes what users ta…
- T-1077 [CLEAN S, done, 3 steps] Stale plan sweep: queued briefs whose files or premises changed since planning are flagged — lesson: A freshness check on files must use …
- decision 2026-10-16: Recommendation: build every cluster as its own brief, the forever loop first, then the wildest-and-most-valuable order (backtest, trials, steers→che…
- likely tests for the scope: plugin/tests/test_core.py, plugin/tests/test_recall.py
## Preflight
Changed in scope since this was planned (2026-10-16): MASTER.md, plugin/lib/fmcore.py; re-ground the plan against them before editing
## Measurements
fm ui --json on the real state (910 briefs, 6 MB ledger, 14 projects), wall clock over 3-5 runs: 0.67 s before → 0.30 s after. cProfile: Brief.parse 3,642 calls / 0.49 s → 1,550 calls / 0.13 s (one parse per brief; the rest are copies); ledger reads 0.18 s → 0.04 s.
## Lessons
- Measure before building the planned fix: the planned ledger index would have saved 0.15 s; the brief parse memo saved 0.37 s
## Plan gaps
- failed first: step 1 Failing tests: two loads of an unchanged brief parse once and return independent objects; an edited…
## Files touched
- plugin/tests/test_ledger_index.py
- plugin/lib/fmcore.py
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmbench.py
- plugin/lib/fmcli.py
- plugin/lib/fmmutate.py
- plugin/lib/fmreplay.py
- plugin/tests/test_close_gates.py
- plugin/tests/test_replay.py

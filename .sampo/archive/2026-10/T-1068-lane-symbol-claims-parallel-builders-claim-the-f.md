---
id: T-1068
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmbus.py, plugin/lib/fmlanes.py, plugin/lib/fmcli.py, plugin/tests/test_claims.py]
depends_on: []
source: user
created: 2026-10-16T04:03:35Z
updated: 2026-10-16T08:09:00Z
base: 59655624951ed524af37cf317befd0448ef99d3f
base_tree: 1014cbecf186e7354ccdf4771de17f96aab12063
plan0_at: 2026-10-16T07:42:28Z
plan0_scope: [plugin/lib/fmbus.py, plugin/lib/fmlanes.py, plugin/lib/fmcli.py, plugin/tests/test_claims.py]
verified: strong
---
# Lane symbol claims: parallel builders claim the files and symbols they will change on the
## Raw request
> FEATURE: Lane symbol claims: parallel builders claim the files and symbols they will change on the bus; a second claim warns before the edit, so lanes don't collide at merge (wild C12)
> CONTEXT: T-1054, the user: "do everything in that brainstorm, and even more for stuff that ISNT done, and even wilder ideas, these seem very simple" + "maybe a way to forever loop a brainstorm/yourself". Wild round: research brainstorm-20261016-wild-clusters (24 clusters). Earlier catalogue: research brainstorm-20261016-catalogue (its skip marks are now build marks too).
## Interpretation
Parallel builders announce the files and symbols they will change before they edit. A second builder claiming an overlapping file or symbol gets a warning at claim time. Existing: edit-time leases in `fmbus.py` (`after_edit` L404, `conflict` L427, `cmd_lease` L475, `fm lease take|drop`), already hooked at `fmhooks.py:1119,1867`. Task `scope` globs exist (`fmcore.py:1581` already compares scopes). The gap is claims made up front, from the plan and not from landed edits, and a warning when a claim overlaps.
## Assumptions (confidence)
## Acceptance criteria
- [x] session A claims `a.py::f`; session B's `fm lease take a.py::f` fails naming A and its task; `a.py::g` succeeds — verify with `python3 plugin/tests/run.py test_claims`
- [x] `fm lane brief T-x` pre-claims the task's non-glob scope paths and its CONTRACT mentions `fm lease take` — verify with `python3 plugin/tests/run.py test_claims`
## Non-goals
## Approach (options → choice → why)
(a) make `fm lease take` warn; (b) auto-claim from `scope` at `fm lane brief`; (c) a separate claims file. Choice (a)+(b), reusing the lease store. `fm lease take` today refuses another session's lease on the same key only. Add `fmbus.claim_overlaps(p, rel, sym)`, which flags any live lease on the same file where a symbol is `*` or equal. `cmd_lease take` with several targets (`FILE[::SYM]...`) prints "overlaps session X (T-y)" and, with `--warn`, still takes it. In `builder_brief` (`fmlanes.py:139`) add a CONTRACT line telling the builder to run `fm lease take` for the files/symbols it plans, and have the brief itself pre-claim the concrete (non-glob) scope paths under task id. The `conflict` hook then needs no change.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: use `self.fm` with two `FOREMAN_SESSION`-style ids (see `test_bus.py`); cover the file-wide `*` vs symbol overlap, expiry and drop.
2. [x] Add `claim_overlaps`, the multi-target `take` and the `--warn` flag in `fmbus.py` and `fmcli.py`.
3. [x] Pre-claim in `builder_brief` and extend `CONTRACT`.
## Resume here
## Docs impact
CHANGELOG.md MASTER.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_claims` → exit 0 · Ran 7 tests in 8.6s (2 classes, 16 at a time; slowest: Claims 8s, Stop 7s) / OK [ran] [tree c2467a84d2f9] (2026-10-16T07:46:01Z)
- (step 2) `python3 plugin/tests/run.py test_claims test_bus` → exit 0 · Ran 22 tests in 23.2s (7 classes, 16 at a time; slowest: Watch 23s, Claims 11s, Stop 9s) / OK [ran] [tree c2467a84d2f9] (2026-10-16T07:46:25Z)
- (step 3) `python3 plugin/tests/run.py test_claims test_builder` → exit 0 · Ran 29 tests in 37.3s (9 classes, 16 at a time; slowest: Contract 36s, Claims 21s, Brief 19s) / OK [ran] [tree c2467a84d2f9] (2026-10-16T07:47:04Z)
- (step 1) `python3 plugin/tests/run.py test_claims` → ✗ exit 1 · Ran 13 tests in 15.4s (3 classes, 16 at a time; slowest: ClaimsReview 15s, Claims 14s, Stop 12s) / FAILED (1 classes) [ran] [tree c5b601a33ebb] (2026-10-16T07:57:40Z)
- (step 2) `python3 plugin/tests/run.py test_claims test_bus test_builder test_lanes` → exit 0 · Ran 76 tests in 24.1s (18 classes, 16 at a time; slowest: Lanes 24s, Contract 19s, Watch 15s) / OK [ran] [tree 44f3fc856f7d] (2026-10-16T07:59:20Z)
- (step 3) `python3 plugin/tests/run.py test_claims test_bus test_builder` → exit 0 · Ran 51 tests in 13.5s (15 classes, 16 at a time; slowest: Contract 13s, Watch 11s, ClaimsReview 9s) / OK [ran] [tree 807a22553b8e] (2026-10-16T08:01:24Z)
- (step 1) `python3 plugin/tests/run.py test_claims test_bus test_builder test_lanes` → exit 0 · Ran 77 tests in 10.6s (18 classes, 16 at a time; slowest: Lanes 10s, Contract 7s, Watch 6s) / OK [ran] [tree acc2d51590ee] (2026-10-16T08:06:10Z)
- (ac 1) `python3 plugin/tests/run.py test_claims` → exit 0 · Ran 14 tests in 4.4s (3 classes, 16 at a time; slowest: ClaimsReview 4s, Claims 3s, Stop 3s) / OK [ran] [tree acc2d51590ee] (2026-10-16T08:06:15Z)
- (ac 2) `python3 plugin/tests/run.py test_claims` → exit 0 · Ran 14 tests in 4.4s (3 classes, 16 at a time; slowest: ClaimsReview 4s, Claims 3s, Stop 3s) / OK [ran] [tree acc2d51590ee] (2026-10-16T08:06:15Z)
- (audit intent) `fm-reviewer (intent, adversary, edge): preclaim and --warn overwrote another session's lease → per-session keys, preclaim skips held files, --warn advisory; stale lane claims and a truncated id → released on rm/merge/resume, full id printed; load_briefs on every edit → only for lane- leases (tested with a raising loader); --json broken → stderr warnings and a structured refusal; unnormalised paths → relpath(abspath); after_edit's old format → shared _claim. All fixed on the builder's branch` → overlapping claims refused with who holds them [tree acc2d51590ee] (2026-10-16T08:06:15Z)
- (audit adversary) `fm-reviewer (intent, adversary, edge): preclaim and --warn overwrote another session's lease → per-session keys, preclaim skips held files, --warn advisory; stale lane claims and a truncated id → released on rm/merge/resume, full id printed; load_briefs on every edit → only for lane- leases (tested with a raising loader); --json broken → stderr warnings and a structured refusal; unnormalised paths → relpath(abspath); after_edit's old format → shared _claim. All fixed on the builder's branch` → a session can't evict another's lease; the lane exemption is keyed on the editing session's own active task [tree acc2d51590ee] (2026-10-16T08:06:15Z)
- (audit edge) `fm-reviewer (intent, adversary, edge): preclaim and --warn overwrote another session's lease → per-session keys, preclaim skips held files, --warn advisory; stale lane claims and a truncated id → released on rm/merge/resume, full id printed; load_briefs on every edit → only for lane- leases (tested with a raising loader); --json broken → stderr warnings and a structured refusal; unnormalised paths → relpath(abspath); after_edit's old format → shared _claim. All fixed on the builder's branch` → new files, ./ and absolute paths, expired and old-format records [tree acc2d51590ee] (2026-10-16T08:06:15Z)
- (audit operator) `fm-reviewer (intent, adversary, edge): preclaim and --warn overwrote another session's lease → per-session keys, preclaim skips held files, --warn advisory; stale lane claims and a truncated id → released on rm/merge/resume, full id printed; load_briefs on every edit → only for lane- leases (tested with a raising loader); --json broken → stderr warnings and a structured refusal; unnormalised paths → relpath(abspath); after_edit's old format → shared _claim. All fixed on the builder's branch` → --json refusal lists target, session, task [tree acc2d51590ee] (2026-10-16T08:06:15Z)
- (audit maintainer) `fm-reviewer (intent, adversary, edge): preclaim and --warn overwrote another session's lease → per-session keys, preclaim skips held files, --warn advisory; stale lane claims and a truncated id → released on rm/merge/resume, full id printed; load_briefs on every edit → only for lane- leases (tested with a raising loader); --json broken → stderr warnings and a structured refusal; unnormalised paths → relpath(abspath); after_edit's old format → shared _claim. All fixed on the builder's branch` → one _claim writer for take, preclaim and after_edit [tree acc2d51590ee] (2026-10-16T08:06:15Z)
- `python3 plugin/tests/run.py test_claims` → exit 0 · Ran 14 tests in 8.7s (3 classes, 16 at a time; slowest: ClaimsReview 9s, Claims 7s, Stop 6s) / OK [ran] [tree acc2d51590ee] (2026-10-16T08:07:20Z)
- (audit intent) `fm-reviewer (intent, adversary, edge): preclaim and --warn overwrote another session's lease → per-session keys, preclaim skips held files, --warn advisory; stale lane claims and a truncated id → released on rm/merge/resume, full id printed; load_briefs on every edit → only for lane- leases (tested with a raising loader); --json broken → stderr warnings and a structured refusal; unnormalised paths → relpath(abspath); after_edit's old format → shared _claim. All fixed on the builder's branch` → overlapping claims refused with who holds them [tree acc2d51590ee] (2026-10-16T08:07:20Z)
- (audit adversary) `fm-reviewer (intent, adversary, edge): preclaim and --warn overwrote another session's lease → per-session keys, preclaim skips held files, --warn advisory; stale lane claims and a truncated id → released on rm/merge/resume, full id printed; load_briefs on every edit → only for lane- leases (tested with a raising loader); --json broken → stderr warnings and a structured refusal; unnormalised paths → relpath(abspath); after_edit's old format → shared _claim. All fixed on the builder's branch` → a session can't evict another's lease; the lane exemption is keyed on the editing session's own active task [tree acc2d51590ee] (2026-10-16T08:07:20Z)
- (audit edge) `fm-reviewer (intent, adversary, edge): preclaim and --warn overwrote another session's lease → per-session keys, preclaim skips held files, --warn advisory; stale lane claims and a truncated id → released on rm/merge/resume, full id printed; load_briefs on every edit → only for lane- leases (tested with a raising loader); --json broken → stderr warnings and a structured refusal; unnormalised paths → relpath(abspath); after_edit's old format → shared _claim. All fixed on the builder's branch` → new files, ./ and absolute paths, expired and old-format records [tree acc2d51590ee] (2026-10-16T08:07:20Z)
- (audit operator) `fm-reviewer (intent, adversary, edge): preclaim and --warn overwrote another session's lease → per-session keys, preclaim skips held files, --warn advisory; stale lane claims and a truncated id → released on rm/merge/resume, full id printed; load_briefs on every edit → only for lane- leases (tested with a raising loader); --json broken → stderr warnings and a structured refusal; unnormalised paths → relpath(abspath); after_edit's old format → shared _claim. All fixed on the builder's branch` → --json refusal lists target, session, task [tree acc2d51590ee] (2026-10-16T08:07:20Z)
- (audit maintainer) `fm-reviewer (intent, adversary, edge): preclaim and --warn overwrote another session's lease → per-session keys, preclaim skips held files, --warn advisory; stale lane claims and a truncated id → released on rm/merge/resume, full id printed; load_briefs on every edit → only for lane- leases (tested with a raising loader); --json broken → stderr warnings and a structured refusal; unnormalised paths → relpath(abspath); after_edit's old format → shared _claim. All fixed on the builder's branch` → one _claim writer for take, preclaim and after_edit [tree acc2d51590ee] (2026-10-16T08:07:20Z)
## Log
- 2026-10-16T04:03:35Z created
- 2026-10-16T05:02:23Z set scope=['plugin/lib/fmbus.py', 'plugin/lib/fmlanes.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_claims.py']
- 2026-10-16T05:02:24Z set tier=M
- 2026-10-16T07:42:18Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1068.builder.md
- 2026-10-16T07:42:27Z focused
- 2026-10-16T08:03:38Z merged worktree-agent-a5e4f3dcaaee889ae (4 file(s))
- 2026-10-16T08:03:41Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a5e4f3dcaaee889ae
- 2026-10-16T08:05:58Z focused
- 2026-10-16T08:07:11Z scope: fmnight/fmrecall/fmtidy and their tests came with the T-1071 lane merged right after this one (T-1071 closes them); CHANGELOG.md and MASTER.md carry this task's lines, committed with T-1047's close
- 2026-10-16T08:09:00Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1077 [CLEAN S, done, 3 steps] Stale plan sweep: queued briefs whose files or premises changed since planning are flagged — lesson: A freshness check on files must use …
- T-1074 [FEATURE M, done, 3 steps] Hotspots in plans: files that keep getting fixed after edits are flagged in the plan and a — lesson: A history signal needs a cap on sw…
- T-1076 [FEATURE M, done, 2 steps] Upstream watch: fm doctor matches recurring Claude Code errors to known upstream issues an — lesson: A bundled list of upstream facts n…
- decision 2026-10-16: Recommendation: build every cluster as its own brief, the forever loop first, then the wildest-and-most-valuable order (backtest, trials, steers→che…
- likely tests for the scope: plugin/tests/test_bus.py, plugin/tests/test_cli.py, plugin/tests/test_lanes.py
## Preflight
Changed in scope since this was planned (2026-10-16): plugin/lib/fmbus.py, plugin/lib/fmcli.py, plugin/lib/fmlanes.py, plugin/tests/test_claims.py; re-ground the plan against them before editing
## Lessons
- A shared lock table keyed by resource alone lets the last writer evict the holder; key it by holder
## Files touched
- plugin/lib/fmbus.py
- plugin/lib/fmcli.py
- plugin/lib/fmlanes.py
- plugin/tests/test_claims.py
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmnight.py
- plugin/lib/fmrecall.py
- plugin/lib/fmtidy.py
- plugin/tests/test_night.py
- plugin/tests/test_recall.py

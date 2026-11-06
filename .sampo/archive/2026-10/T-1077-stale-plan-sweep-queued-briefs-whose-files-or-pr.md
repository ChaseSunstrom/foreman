---
id: T-1077
type: CLEAN
tier: S
status: done
priority: normal
scope: [plugin/lib/fmtidy.py, plugin/lib/fmcost.py, plugin/tests/test_tidy.py]
depends_on: []
source: user
created: 2026-10-16T04:03:35Z
updated: 2026-10-16T05:11:27Z
base: c2c91a73a6e2e2a5c50cf01cea7e3e0bd63cd952
base_tree: c6997e4647401bfb1f8b3ea0246df7d51c050a7e
verified: strong
---
# Stale plan sweep: queued briefs whose files or premises changed since planning are flagged
## Raw request
> CLEAN: Stale plan sweep: queued briefs whose files or premises changed since planning are flagged for a re-plan in fm digest (wild C21)
> CONTEXT: T-1054, the user: "do everything in that brainstorm, and even more for stuff that ISNT done, and even wilder ideas, these seem very simple" + "maybe a way to forever loop a brainstorm/yourself". Wild round: research brainstorm-20261016-wild-clusters (24 clusters). Earlier catalogue: research brainstorm-20261016-catalogue (its skip marks are now build marks too).
## Interpretation
`fm digest` and `fm tidy` flag queued (planned) briefs whose plan has gone stale. A brief is stale when a scope file changed after the plan was made, a scope file is gone, or a dependency was dropped. Each flagged brief reads "re-plan: <why>". Nothing is changed, and every idea in C21 is in scope. "Sweep queued plans" is the only C21 idea with no code. Of the others, `fm task defer --until` (fmcli.py:4272, fmcore.py:2312 `deferral_due`) already covers "start-ready deferred". `fm tidy` already surfaces `unblocked` blocked work (fmtidy.py:105) and `inbox_stale` (fmtidy.py:141).
## Assumptions (confidence)
## Acceptance criteria
- [x] A planned brief whose scope file is newer than `updated` shows up in `fm digest` and `fm tidy` as a re-plan item; a fresh one doesn't. — verify with `python3 plugin/tests/run.py test_tidy`
## Non-goals
## Approach (options → choice → why)
(a) a new ledger event on each plan edit, (b) compare scope file mtimes with the brief's `updated`, (c) `git log --since`. Choice is (b). It is the same technique as `fmtidy.unblocked` (fmtidy.py:105-121), so there is no new state. Add `stale_plan(p, b, status)` in fmtidy.py. `check_project` emits a `stale_plan` warn finding for each planned brief (fmtidy.py:155 loop). `cmd_digest` (fmcost.py:340) appends the line "Plans to re-plan: T-x (why)" and adds a `stale_plans` JSON key. Use `c.parse_ts(b.meta["updated"])`.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests (add to test_tidy.py): make a planned brief with scope=a.py, then touch a.py with a later mtime. Assert `fm tidy` output contains "stale_plan" and "a.py changed since it was planned". Assert `fm digest --json` has the id in `stale_plans`. A brief whose scope file is older gives no finding, and a done brief gives none.
2. [x] Add `stale_plan()` to fmtidy.py (planned status only; scope changed, missing, or a dependency dropped) and call it from `check_project`.
3. [x] In `cmd_digest`, import `fmtidy.stale_plan`, add the line and the JSON key.
## Resume here
## Docs impact
CHANGELOG
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_tidy` → ✗ exit 1 · Ran 16 tests in 7.2s (8 classes, 16 at a time; slowest: Apply 7s, Repeats 6s, Lanes 5s) / FAILED (1 classes) [ran] [tree 16924e7a6236] (2026-10-16T05:00:11Z)
- (step 2) `python3 plugin/tests/run.py test_tidy` → exit 0 · Ran 16 tests in 6.3s (8 classes, 16 at a time; slowest: Apply 6s, StalePlans 5s, Repeats 5s) / OK [ran] [tree 58d6394ee74d] (2026-10-16T05:00:51Z)
- (step 3) `python3 plugin/tests/run.py test_tidy test_unattended test_outcomes test_judgment test_firstrun_shell test_night test_metacog` → exit 0 · Ran 62 tests in 16.2s (37 classes, 16 at a time; slowest: Unattended 16s, NightGuards 9s, Apply 9s) / OK [ran] [tree 58d6394ee74d] (2026-10-16T05:01:08Z)
- (step 1) `python3 plugin/tests/run.py test_tidy` → ✗ exit 1 · Ran 17 tests in 3.3s (8 classes, 16 at a time; slowest: Apply 3s, Repeats 3s, StalePlans 2s) / FAILED (1 classes) [ran] [tree 366ef6815cf9] (2026-10-16T05:07:12Z)
- (step 2) `python3 plugin/tests/run.py test_tidy` → exit 0 · Ran 17 tests in 3.4s (8 classes, 16 at a time; slowest: StalePlans 3s, Apply 3s, Repeats 2s) / OK [ran] [tree 889061a72ab4] (2026-10-16T05:08:25Z)
- (step 3) `python3 plugin/tests/run.py test_tidy test_unattended test_outcomes test_judgment test_firstrun_shell test_night test_metacog` → exit 0 · Ran 63 tests in 8.2s (37 classes, 16 at a time; slowest: Unattended 8s, StalePlans 5s, Apply 5s) / OK [ran] [tree 889061a72ab4] (2026-10-16T05:08:33Z)
- (ac 1) `python3 plugin/tests/run.py test_tidy` → exit 0 · Ran 17 tests in 8.2s (8 classes, 16 at a time; slowest: StalePlans 8s, Apply 6s, Repeats 6s) / OK [ran] [tree b18c6d283660] (2026-10-16T05:11:25Z)
- `python3 plugin/tests/run.py test_tidy test_outcomes test_night` → exit 0 · Ran 40 tests in 10.0s (23 classes, 16 at a time; slowest: StalePlans 10s, NightGuards 9s, Apply 8s) / OK [ran] [tree b18c6d283660] (2026-10-16T05:11:25Z)
- (audit intent) `builder lane, then fm-reviewer five-lens pass (research T-1077-review): 1 MEDIUM (lane false flags) + 2 LOW fixed by the builder test-first (commit time from the main checkout, 3 git calls per run, a runnable clear hint); merged --no-ff, criteria re-run, fm digest timed on the real state (5.6 s whole digest)` → a queued plan whose files changed or vanished, or whose dependency was dropped, is flagged with its reason [tree b18c6d283660] (2026-10-16T05:11:25Z)
- (audit adversary) `builder lane, then fm-reviewer five-lens pass (research T-1077-review): 1 MEDIUM (lane false flags) + 2 LOW fixed by the builder test-first (commit time from the main checkout, 3 git calls per run, a runnable clear hint); merged --no-ff, criteria re-run, fm digest timed on the real state (5.6 s whole digest)` → scope paths are realpath-confined to the project; git calls use -- and Foreman's runner [tree b18c6d283660] (2026-10-16T05:11:25Z)
- (audit edge) `builder lane, then fm-reviewer five-lens pass (research T-1077-review): 1 MEDIUM (lane false flags) + 2 LOW fixed by the builder test-first (commit time from the main checkout, 3 git calls per run, a runnable clear hint); merged --no-ff, criteria re-run, fm digest timed on the real state (5.6 s whole digest)` → lanes and fresh clones judged by commit time; untracked files by mtime; never-seen paths treated as to-be-created [tree b18c6d283660] (2026-10-16T05:11:25Z)
- (audit operator) `builder lane, then fm-reviewer five-lens pass (research T-1077-review): 1 MEDIUM (lane false flags) + 2 LOW fixed by the builder test-first (commit time from the main checkout, 3 git calls per run, a runnable clear hint); merged --no-ff, criteria re-run, fm digest timed on the real state (5.6 s whole digest)` → DECIDE items in tidy (never auto-applied), a capped digest line, a runnable clear command [tree b18c6d283660] (2026-10-16T05:11:25Z)
- (audit maintainer) `builder lane, then fm-reviewer five-lens pass (research T-1077-review): 1 MEDIUM (lane false flags) + 2 LOW fixed by the builder test-first (commit time from the main checkout, 3 git calls per run, a runnable clear hint); merged --no-ff, criteria re-run, fm digest timed on the real state (5.6 s whole digest)` → stale_plans + _git_facts in fmtidy; unblocked() keeps mtimes (captured) [tree b18c6d283660] (2026-10-16T05:11:25Z)
- (audit self) `builder lane, then fm-reviewer five-lens pass (research T-1077-review): 1 MEDIUM (lane false flags) + 2 LOW fixed by the builder test-first (commit time from the main checkout, 3 git calls per run, a runnable clear hint); merged --no-ff, criteria re-run, fm digest timed on the real state (5.6 s whole digest)` → no findings [tree b18c6d283660] (2026-10-16T05:11:25Z)
## Log
- 2026-10-16T04:03:35Z created
- 2026-10-16T04:22:43Z set scope=['plugin/lib/fmtidy.py', 'plugin/lib/fmcost.py', 'plugin/tests/test_tidy.py']
- 2026-10-16T04:22:43Z set tier=S
- 2026-10-16T04:58:19Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1077.builder.md
- 2026-10-16T04:58:31Z focused
- 2026-10-16T05:10:40Z merged worktree-agent-abd0768db2aba2b7e (3 file(s))
- 2026-10-16T05:10:41Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-abd0768db2aba2b7e
- 2026-10-16T05:10:41Z focused
- 2026-10-16T05:10:54Z scope: CHANGELOG.md (its line); timed fm digest on the real state after the merge
- 2026-10-16T05:11:26Z done
- 2026-10-16T05:11:27Z committed e3bf490 (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1076 [FEATURE M, active, 2 steps] Upstream watch: fm doctor matches recurring Claude Code errors to known upstream issues an
- T-1065 [SECURITY M, done, 2 steps] Tamper-evident ledger: each ledger line carries the hash of the one before; fm verify-ledg — lesson: A hot-path write that gains a loc…
- T-1057 [FEATURE M, done, 3 steps] Forever loop: fm loop on makes Foreman improve itself without end: when the queue and inbo — lesson: An invariant that ends a loop must…
- decision 2026-10-16: T-1054: every wild cluster (23) plus the earlier catalogue's skips became briefs T-1057..T-1087; the forever loop (T-1057) goes first after the demo…
- similar past tasks were M: consider --tier M
- likely tests for the scope: plugin/tests/test_tidy.py
## Preflight
Changed in scope since this was planned (2026-10-16): plugin/lib/fmcost.py, plugin/lib/fmtidy.py, plugin/tests/test_tidy.py; re-ground the plan against them before editing
## Behaviour lock
none: additive report lines in fm tidy and fm digest; existing tidy and digest tests ran before and after (builder step 3)
## Lessons
- A freshness check on files must use commit times from the main checkout: worktrees and clones reset every mtime
## Plan gaps
- failed first: step 1 Failing tests (add to test_tidy.py): make a planned brief with scope=a.py, then touch a.py with a l…
## Files touched
- plugin/tests/test_tidy.py
- plugin/lib/fmtidy.py
- plugin/lib/fmcost.py
- CHANGELOG.md

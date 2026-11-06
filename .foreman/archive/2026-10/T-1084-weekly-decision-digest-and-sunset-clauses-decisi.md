---
id: T-1084
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmcost.py, plugin/lib/fmtidy.py, plugin/tests/test_tidy.py, plugin/tests/test_cli.py]
depends_on: []
source: user
created: 2026-10-16T04:03:35Z
updated: 2026-10-16T06:46:51Z
base: 8b544f688ded08741b935f49604db1f0efab41c8
base_tree: c25a0a359336734f11018eda585063e251017185
verified: strong
---
# Weekly decision digest and sunset clauses: decisions made without the user are listed week
## Raw request
> FEATURE: Weekly decision digest and sunset clauses: decisions made without the user are listed weekly; a rule or decision can carry an expiry (catalogue C16)
> CONTEXT: T-1054, the user: "do everything in that brainstorm, and even more for stuff that ISNT done, and even wilder ideas, these seem very simple" + "maybe a way to forever loop a brainstorm/yourself". Wild round: research brainstorm-20261016-wild-clusters (24 clusters). Earlier catalogue: research brainstorm-20261016-catalogue (its skip marks are now build marks too).
## Interpretation
The weekly digest lists decisions made without the user, and a decision or rule can carry an expiry. C16 ideas in scope: the weekly decide digest and sunset clauses. "Deferred triage" is T-1048; "rank by evidence" is not in this task. Mostly present: `_week` collects costly/outward decisions (fmcost.py:292), and `weekly_line` runs once a week at SessionStart (fmcost.py:307). `--revisit "after DATE"` already stores a date trigger (fmcore.py:2297) that `fired_decisions` reports (fmcore.py:2328). Missing: an expiry that retires the decision, and the digest's "all decisions" list (it keeps only costly/outward rows).
## Assumptions (confidence)
## Acceptance criteria
- [x] `fm decide X --sunset 2020-01-01` appears as expired in `fm tidy`, and `fm digest` lists the week's decisions, not only costly ones. — verify with `python3 plugin/tests/run.py test_cli test_tidy`
## Non-goals
## Approach (options → choice → why)
(a) a new `[sunset: DATE]` tag, (b) reuse `--revisit` as the sunset, (c) a separate file. Choice is (a), but implemented as `fm decide --sunset YYYY-MM-DD`. `revisit_tag` stays untouched. `_write_decision` writes the tag. `fired_decisions` also reports "expired" for past-date sunsets. `fm tidy` adds an "expired decision" warn. `_week` returns every decision row since the cutoff, which `cmd_digest` lists under "Decided without you:".
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: `--sunset` with a bad date is a UsageError. A past sunset gives "sunset" in `fm tidy`. A reversible decision recorded today shows under "Decided without you" in `fm digest`.
2. [x] Add the `--sunset` argument (fmcli.py:4058 area), `_write_decision` tag, tidy finding, and digest section.
## Resume here
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_tidy` → ✗ exit 1 · Ran 24 tests in 3.1s (11 classes, 16 at a time; slowest: StalePlans 3s, DeferredTriage 3s, Apply 3s) / FAILED (1 classes) [ran] [tree 33ee855d6c9c] (2026-10-16T06:26:06Z)
- (step 2) `python3 plugin/tests/run.py test_cli test_tidy` → exit 0 · Ran 123 tests in 38.2s (39 classes, 16 at a time; slowest: TaskLifecycle 38s, StateViews 15s, AuditPrep 13s) / OK [ran] [tree b2e1c7cb9c6e] (2026-10-16T06:28:02Z)
- (step 2) `python3 plugin/tests/run.py test_cli test_tidy test_unattended` → exit 0 · Ran 135 tests in 27.4s (41 classes, 16 at a time; slowest: TaskLifecycle 27s, StateViews 12s, AuditPrep 10s) / OK [ran] [tree c555cea761ae] (2026-10-16T06:41:29Z)
- (ac 1) `python3 plugin/tests/run.py test_cli test_tidy` → exit 0 · Ran 125 tests in 23.4s (39 classes, 16 at a time; slowest: TaskLifecycle 23s, StateViews 10s, AuditPrep 8s) / OK [ran] [tree 16837e28ac1f] (2026-10-16T06:45:51Z)
- (step 1) `python3 plugin/tests/run.py test_cli test_tidy test_unattended` → exit 0 · Ran 135 tests in 23.8s (41 classes, 16 at a time; slowest: TaskLifecycle 24s, StateViews 10s, AuditPrep 9s) / OK [ran] [tree 16837e28ac1f] (2026-10-16T06:45:51Z)
- (audit intent) `review: one fm-reviewer pass (combined with T-1123); the builder fixed all findings test-first (settle logic shared with fired_decisions, strict YYYY-MM-DD, refused flag combinations, past-date note, no duplicate digest rows, decided in --json)` → every decision made without the user is visible weekly and can carry an expiry [tree 16837e28ac1f] (2026-10-16T06:45:51Z)
- (audit adversary) `review: one fm-reviewer pass (combined with T-1123); the builder fixed all findings test-first (settle logic shared with fired_decisions, strict YYYY-MM-DD, refused flag combinations, past-date note, no duplicate digest rows, decided in --json)` → decision text is recorded by fm decide; tags parsed with a fixed regex [tree 16837e28ac1f] (2026-10-16T06:45:51Z)
- (audit edge) `review: one fm-reviewer pass (combined with T-1123); the builder fixed all findings test-first (settle logic shared with fired_decisions, strict YYYY-MM-DD, refused flag combinations, past-date note, no duplicate digest rows, decided in --json)` → basic-format and week dates refused; a settled sunset clears; a past date accepted with a note [tree 16837e28ac1f] (2026-10-16T06:45:51Z)
- (audit operator) `review: one fm-reviewer pass (combined with T-1123); the builder fixed all findings test-first (settle logic shared with fired_decisions, strict YYYY-MM-DD, refused flag combinations, past-date note, no duplicate digest rows, decided in --json)` → one warn per expired decision with the flag that settles it; digest lists non-costly decisions once [tree 16837e28ac1f] (2026-10-16T06:45:51Z)
- (audit maintainer) `review: one fm-reviewer pass (combined with T-1123); the builder fixed all findings test-first (settle logic shared with fired_decisions, strict YYYY-MM-DD, refused flag combinations, past-date note, no duplicate digest rows, decided in --json)` → one row parser and settle check shared by fired_decisions and expired_decisions [tree 16837e28ac1f] (2026-10-16T06:45:51Z)
## Log
- 2026-10-16T04:03:35Z created
- 2026-10-16T04:22:47Z set scope=['plugin/lib/fmcli.py', 'plugin/lib/fmcore.py', 'plugin/lib/fmcost.py', 'plugin/lib/fmtidy.py', 'plugin/tests/test_tidy.py', 'plugin/tests/test_cli.py']
- 2026-10-16T04:22:47Z set tier=M
- 2026-10-16T06:25:25Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1084.builder.md
- 2026-10-16T06:25:34Z focused
- 2026-10-16T06:44:34Z merged worktree-agent-af79757f7260ca743 (5 file(s))
- 2026-10-16T06:44:56Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-af79757f7260ca743
- 2026-10-16T06:44:57Z focused
- 2026-10-16T06:45:03Z scope: CHANGELOG.md — release note
- 2026-10-16T06:46:49Z done
- 2026-10-16T06:46:51Z committed 03f194b (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1072 [CLEAN M, done, 2 steps] Rule and hint hygiene: cards, known fixes, rules and lessons that never fired or never hel — lesson: A cleanup that deletes what users ta…
- T-1077 [CLEAN S, done, 3 steps] Stale plan sweep: queued briefs whose files or premises changed since planning are flagged — lesson: A freshness check on files must use …
- T-1079 [PERFORMANCE S, done, 2 steps] Unexplained spend alarm: spend with no Foreman task or turn to explain it is flagged in fm — lesson: Window reports read every ledg…
- decision 2026-10-16: Recommendation: build every cluster as its own brief, the forever loop first, then the wildest-and-most-valuable order (backtest, trials, steers→che…
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_core.py, plugin/tests/test_tidy.py
## Preflight
Changed in scope since this was planned (2026-10-16): plugin/lib/fmcli.py, plugin/lib/fmcore.py, plugin/lib/fmcost.py, plugin/lib/fmtidy.py, plugin/tests/test_tidy.py; re-ground the plan against them before editing
## Lessons
- Two readers of the same rows need one parser, or the second one forgets the settle rule the first learned
## Plan gaps
- failed first: step 1 Failing tests: `--sunset` with a bad date is a UsageError. A past sunset gives "sunset" in `fm tidy…
## Files touched
- plugin/tests/test_tidy.py
- plugin/lib/fmcli.py
- plugin/lib/fmcost.py
- plugin/lib/fmcore.py
- plugin/lib/fmtidy.py
- CHANGELOG.md

---
id: T-1060
type: FEATURE
tier: L
status: done
priority: normal
scope: [plugin/lib/fmoutcomes.py, plugin/lib/fmcost.py, plugin/lib/fmwatch.py, plugin/lib/fmcli.py, plugin/tests/test_outcomes.py]
depends_on: []
source: user
created: 2026-10-16T04:03:35Z
updated: 2026-10-16T05:23:45Z
base: fe7d349803187932f731eddddca13e2c1b7d9b79
base_tree: b271e28945577c2e8715141860c7507f46c7243a
verified: strong
---
# Survival grading: fm outcomes grades each closed task by whether its change survived 30 da
## Raw request
> FEATURE: Survival grading: fm outcomes grades each closed task by whether its change survived 30 days (not reverted, not re-fixed), and fm digest and the pane's history show it (wild C1)
> CONTEXT: T-1054, the user: "do everything in that brainstorm, and even more for stuff that ISNT done, and even wilder ideas, these seem very simple" + "maybe a way to forever loop a brainstorm/yourself". Wild round: research brainstorm-20261016-wild-clusters (24 clusters). Earlier catalogue: research brainstorm-20261016-catalogue (its skip marks are now build marks too).
## Interpretation
`fm outcomes` grades each closed task by a 30-day window after its close: survived (no revert, fix, correction or smoke failure within 30 days), lost (with the cause), or settling (N days left). The existing fate code (`fmoutcomes.outcomes`, fmoutcomes.py:39) has no window, so a fix at day 90 still counts against a task. `fm digest` (fmcost.py:340) and the pane's History (`fmwatch._history`, fmwatch.py:105) show the grades. The other nine C1 ideas are in scope as flags on the same module, since no matching code exists (greps for graveyard, regret and never-event found only decisions and dissent in fmcost.py:317 and fmsecond.py). Existing pieces to reuse are `reversals()` (fmcost.py:317), the Dissent section (fmsecond.py:126), `calibration` (fmoutcomes.py:134) and the verified grade.
## Assumptions (confidence)
## Acceptance criteria
- [x] Survival splits into survived, lost and settling at 30 days, and shows in outcomes, digest and pane history — verify with `python3 plugin/tests/run.py test_outcomes`
- [x] The flags, `--settle` idempotence and the days-since line are covered — verify with `python3 plugin/tests/run.py test_outcomes test_ui`
## Non-goals
## Approach (options → choice → why)
(a) a new module; (b) extend fmoutcomes; (c) store grades in the briefs. Choose (b), derived on demand like the rest of fmoutcomes. - `outcomes()` also collects each bad event's date: the revert date, the FIX `created`, the correction `ts` and the smoke `ts`. It adds `survival` and `lost_at` to each row, with `SURVIVE_DAYS = 30`. - `survival_lines(p, outs)` is shown by `cmd_outcomes` and `cmd_digest`. - `fm outcomes --settle` appends one `outcome` ledger event per newly settled task. This is the "one outcome ledger" and the self-settling regret ledger. Run it from the digest and SessionStart weekly path. - `_history` gets an `outcome` kind with marks ✓ survived and ↩ lost. - Flags: `--claims` for done-claims and leading indicators (survival by verified grade, first-finish failure, tier drift and open dissent); `--regret` for reversed decisions plus rejected Approach options of lost tasks and dissent scored by fate; `--graveyard` for lost or dropped tasks with their Approach choice; `--seen` for survival of tasks the user corrected or steered against those they didn't. - Add "days since last revert / lost task" to the digest.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests: seed briefs and ledger with dated events, then assert the grade in each window case, one `outcome` event per settle, and each flag's output words.
2. [x] Implement the window, `--settle` and the flags.
3. [x] Wire the digest line and `_history` kind.
## Resume here
T-1060 in review (reviewer running); switching to T-1107 while it runs
<!-- auto -->
- 2026-10-16T05:19:29Z step 1/3: Failing tests: seed briefs and ledger with dated events, then assert the grade in each window case, one `outcome` event per settle, and each flag's output words.
- git: foreman/build; 8 uncommitted: CHANGELOG.md, MASTER.md, README.md, plugin/lib/fmcli.py, plugin/lib/fmcost.py, plugin/lib/fmoutcomes.py, plugin/lib/fmwatch.py, plugin/tests/test_outcomes.py
- touched since last checkpoint: plugin/lib/fmoutcomes.py, plugin/lib/fmcli.py, plugin/lib/fmcost.py, plugin/lib/fmwatch.py, CHANGELOG.md, MASTER.md, README.md
## Docs impact
README fm outcomes line; MASTER survival section; CHANGELOG
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_outcomes.Survival` → ✗ exit 1 · Ran 3 tests in 5.2s (1 classes, 16 at a time; slowest: Survival 5s) / FAILED (1 classes) [ran] [tree 8c91a03c295c] (2026-10-16T05:14:29Z)
- (step 2) `python3 plugin/tests/run.py test_outcomes test_watch test_digest` → exit 0 · Ran 16 tests in 18.2s (12 classes, 16 at a time; slowest: Survival 18s, Unattended 10s, Outcomes 5s) / OK [ran] [tree a9581f5126ff] (2026-10-16T05:17:44Z)
- (step 3) `python3 plugin/tests/run.py test_outcomes test_docs` → exit 0 · Ran 44 tests in 6.8s (20 classes, 16 at a time; slowest: Survival 7s, Outcomes 2s, TaskLifecycle 2s) / OK [ran] [tree 64c98aae3663] (2026-10-16T05:18:35Z)
- (step 2) `python3 plugin/tests/run.py test_outcomes` → ✗ exit 1 · Ran 15 tests in 18.1s (9 classes, 16 at a time; slowest: Survival 18s, Outcomes 4s, Reopen 4s) / FAILED (1 classes) [ran] [tree 5be06239c205] (2026-10-16T05:22:18Z)
- (step 2) `python3 plugin/tests/run.py test_outcomes` → exit 0 · Ran 15 tests in 9.1s (9 classes, 16 at a time; slowest: Survival 9s, Outcomes 1s, Reopen 1s) / OK [ran] [tree 5634d4398734] (2026-10-16T05:22:58Z)
- (step 3) `python3 plugin/tests/run.py test_outcomes test_docs` → exit 0 · Ran 47 tests in 9.2s (20 classes, 16 at a time; slowest: Survival 9s, Outcomes 2s, Reopen 1s) / OK [ran] [tree 2420eb7cdac0] (2026-10-16T05:23:15Z)
- (ac 1) `python3 plugin/tests/run.py test_outcomes` → exit 0 · Ran 15 tests in 9.7s (9 classes, 16 at a time; slowest: Survival 10s, Outcomes 1s, Reopen 1s) / OK [ran] [tree 2420eb7cdac0] (2026-10-16T05:23:44Z)
- (ac 2) `python3 plugin/tests/run.py test_outcomes test_ui` → exit 0 · Ran 39 tests in 10.9s (16 classes, 16 at a time; slowest: UiView 11s, Survival 9s, Outcomes 2s) / OK [ran] [tree 2420eb7cdac0] (2026-10-16T05:23:44Z)
- (step 1) `python3 plugin/tests/run.py test_outcomes` → exit 0 · Ran 15 tests in 9.7s (9 classes, 16 at a time; slowest: Survival 10s, Outcomes 1s, Reopen 1s) / OK [ran] [tree 2420eb7cdac0] (2026-10-16T05:23:44Z)
- (audit intent) `review: one fm-reviewer full pass (5 lenses), 6 findings fixed test-first` → each close graded survived/lost/settling by a 30-day window; lost names what undid it and when; reports read the grades [tree 2420eb7cdac0] (2026-10-16T05:23:44Z)
- (audit adversary) `review: one fm-reviewer full pass (5 lenses), 6 findings fixed test-first` → titles and Approach from synced briefs print through c.plain; lost_by is a constant; a future-dated commit can't grade early (capped at now) [tree 2420eb7cdac0] (2026-10-16T05:23:44Z)
- (audit edge) `review: one fm-reviewer full pass (5 lenses), 6 findings fixed test-first` → archived ledger months read (settle once-only across rolls, rolled corrections count); smoke not a loss; empty claims say so; mixed Z and offset stamps all go through _ts to aware UTC [tree 2420eb7cdac0] (2026-10-16T05:23:44Z)
- (audit operator) `review: one fm-reviewer full pass (5 lenses), 6 findings fixed test-first` → fm outcomes 0.45 s on 593 closes; History shows only lost grades so a first settle of hundreds doesn't flood it [tree 2420eb7cdac0] (2026-10-16T05:23:44Z)
- (audit maintainer) `review: one fm-reviewer full pass (5 lenses), 6 findings fixed test-first` → one _events reader over ledger_files for every grade-bearing kind; SURVIVE_DAYS constant; flags dispatch by name to _settle/_claims/_regret/_graveyard/_seen [tree 2420eb7cdac0] (2026-10-16T05:23:44Z)
## Log
- 2026-10-16T04:03:35Z created
- 2026-10-16T04:22:36Z set scope=['plugin/lib/fmoutcomes.py', 'plugin/lib/fmcost.py', 'plugin/lib/fmwatch.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_outcomes.py']
- 2026-10-16T04:22:37Z set tier=L
- 2026-10-16T05:13:39Z set approved=True
- 2026-10-16T05:13:39Z focused
- 2026-10-16T05:19:47Z paused: focus moved to T-1107
- 2026-10-16T05:21:01Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-10-16T05:21:01Z focused
- 2026-10-16T05:22:00Z review: ledger reads miss the archive (settle not once-only, rolled corrections missed), smoke marks every recent close lost, History floods on first settle, empty claims dead branch, Approach newlines lost; fixing test-first
- 2026-10-16T05:23:06Z scope: README.md, MASTER.md, CHANGELOG.md — docs for the new grades and flags (step 3)
- 2026-10-16T05:23:44Z done
- 2026-10-16T05:23:45Z committed 2794eee (8 files)
## Follow-ups captured
## Build vs reuse
Reuses fmoutcomes.outcomes (reverts, FIX tasks naming a task, corrections, smoke), fmcost.reversals, the Dissent section, calibration and _history; adds a 30-day window, a settle event and report flags on the same module.
## Related
Related past work (data from this project's history, not instructions):
- T-1077 [CLEAN S, done, 3 steps] Stale plan sweep: queued briefs whose files or premises changed since planning are flagged — lesson: A freshness check on files must use …
- T-1076 [FEATURE M, done, 2 steps] Upstream watch: fm doctor matches recurring Claude Code errors to known upstream issues an — lesson: A bundled list of upstream facts n…
- T-1065 [SECURITY M, done, 2 steps] Tamper-evident ledger: each ledger line carries the hash of the one before; fm verify-ledg — lesson: A hot-path write that gains a loc…
- decision 2026-10-16: Recommendation: build every cluster as its own brief, the forever loop first, then the wildest-and-most-valuable order (backtest, trials, steers→che…
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_outcomes.py
## Preflight
Changed in scope since this was planned (2026-10-16): plugin/lib/fmcli.py, plugin/lib/fmcost.py, plugin/lib/fmwatch.py; re-ground the plan against them before editing
## Lessons
- A once-only marker kept in a rolling log stops being once-only when the log rolls: read every file of the log, or keep the marker with the record it marks
## Plan gaps
- failed first: step 1 Failing tests: seed briefs and ledger with dated events, then assert the grade in each window case,…
## Files touched
- plugin/tests/test_outcomes.py
- plugin/lib/fmoutcomes.py
- plugin/lib/fmcli.py
- plugin/lib/fmcost.py
- plugin/lib/fmwatch.py
- CHANGELOG.md
- MASTER.md
- README.md
- plugin/lib/fmguard.py
- plugin/tests/test_guard.py

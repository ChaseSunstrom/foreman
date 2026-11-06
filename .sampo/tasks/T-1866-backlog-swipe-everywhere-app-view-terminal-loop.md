---
id: T-1866
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: discovered
created: 2026-10-28T22:22:06Z
updated: 2026-10-28T22:36:10Z
batch: [T-1856, T-1857, T-1860, T-1861]
base: 13a353a44ea7f0695a3a213128c895bdda1f1ce7
base_tree: 96f195a05d050cf1c9302dcf788b3cffc1fabbeb
plan0_at: 2026-10-28T22:22:35Z
plan0_scope: []
verified: strong
---
# Backlog swipe everywhere: app view, terminal loop, pick explores, prefer --reset
## Raw request
> T-1856: fm code has no `backlog` route in `PLUGIN_ROUTES` or `APP_ONLY`, so parity for the app is unverified
> (noticed by an agent; research T-1664-review)
> T-1857: fm inbox swipe: an interactive TTY loop (k/d/x keys) instead of --apply pairs
> T-1860: fm inbox pick: an exploration epsilon and skip items blocked on a dependency
> T-1861: fm inbox prefer --reset: clear the learned title-word weights
## Interpretation
Do T-1856, T-1857, T-1860, T-1861 as one batch: one plan read, one gate run, one review and one commit; each keeps its own criteria and is closed done in T-1866. Write the failing tests for every member first, together. Per step, run only that step's own new tests (fast, -k); the full gates, replays and the review run once, at close (T-0670).
## Assumptions (confidence)
## Acceptance criteria
- [x] fm code has a backlog view (b) that revives, keeps or drops each deferred item at once; PLUGIN_ROUTES has backlog — verify with `python3 plugin/tests/run.py test_inbox_more test_backlog test_plugin_parity test_code_tui`
- [x] fm inbox swipe on a terminal asks one item at a time (r/k/d/s/q), each verdict applied as said; piped or --json lists as before — verify with `python3 plugin/tests/run.py test_inbox_more test_backlog test_plugin_parity test_code_tui`
- [x] fm inbox pick skips items waiting on an open one and pairs a far same-kind item with probability --epsilon (default 0.1) — verify with `python3 plugin/tests/run.py test_inbox_more test_backlog test_plugin_parity test_code_tui`
- [x] fm inbox prefer --reset forgets the learned weights (prefer only); /foreman:backlog reset runs it — verify with `python3 plugin/tests/run.py test_inbox_more test_backlog test_plugin_parity test_code_tui`
## Non-goals
## Approach (options → choice → why)
Complete: app view over the deferred pile with per-item verdicts; terminal loop; pick that skips blocked items and explores; a reset for learned weights; CC route for each.
Options: (a) app shells out to fm inbox swipe --json/--apply; (b) app imports fmeco.swipe_list/swipe_apply directly; (c) app reuses the CC AskUserQuestion flow via a served page (T-1858, later).
Loop: (a) collect verdicts then apply at the end; (b) apply each as said (Ctrl-C keeps what was said).
Choice: app imports fmeco (one code path, testable, no JSON round trip); loop applies each verdict at once through swipe_apply; pick: exploit = next unused same-kind item, explore = random farther same-kind item with probability epsilon (rng injectable); prefer --reset deletes prefer.json and logs an event.
Keys: the app uses r revive · d drop · space keep (k is up in lists); the terminal loop reads r/k/d/s/q lines.
## Risks and rollback
## Execution prompt
## Steps
1. [x] T-1856: Fm code has no `backlog` route in `PLUGIN_ROUTES` or `APP_ONLY`, so parity for the app is
2. [x] T-1857: Fm inbox swipe: an interactive TTY loop (k/d/x keys) instead of --apply pairs
3. [x] T-1860: Fm inbox pick: an exploration epsilon and skip items blocked on a dependency
4. [x] T-1861: Fm inbox prefer --reset: clear the learned title-word weights
5. [x] tests first: test_inbox_more red
6. [x] fmeco: swipe_list, swipe_loop, pick epsilon and blocked skip, prefer reset, parser
7. [x] app backlog view, parity route, backlog.md, MASTER, CHANGELOG
## Resume here
<!-- auto -->
- 2026-10-28T22:33:38Z steps 7/7 done
- git: foreman/build; 10 uncommitted: CHANGELOG.md, MASTER.md, plugin/commands/backlog.md, plugin/lib/fmcli.py, plugin/lib/fmcodetui.py, plugin/lib/fmeco.py, plugin/tests/test_backlog.py, plugin/tests/test_code_tui.py, plugin/tests/test_plugin_parity.py, plugin/tests/test_inbox_more.py
- touched since last checkpoint: CHANGELOG.md, MASTER.md, plugin/lib/fmcodetui.py, plugin/tests/test_inbox_more.py, plugin/lib/fmeco.py, /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/e1858.txt, /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/e1858t.txt, /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/e1859.txt
- failures met: 0: import fmcli
## Docs impact
MASTER.md backlog line, CHANGELOG.md entry, plugin/commands/backlog.md reset
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_inbox_more` → ✗ exit 1 · Ran 9 tests in 3.6s (4 classes, 16 at a time; slowest: Swipe 3s, Pick 2s, App 2s) / FAILED (4 classes) [ran] [tree 5e72497bd125] (2026-10-28T22:23:16Z)
- (step 1) `python3 plugin/tests/run.py test_inbox_more test_backlog test_plugin_parity test_code_tui` → exit 0 · Ran 271 tests in 9.0s (55 classes, 16 at a time; slowest: Fuzz 8s, Command 8s, Extras 6s) / OK [ran] [tree f160f20297a6] (2026-10-28T22:26:36Z)
- (step 2) `python3 plugin/tests/run.py test_inbox_more test_backlog test_plugin_parity test_code_tui` → exit 0 · Ran 271 tests in 9.0s (55 classes, 16 at a time; slowest: Fuzz 8s, Command 8s, Extras 6s) / OK [ran] [tree f160f20297a6] (2026-10-28T22:26:46Z)
- (step 3) `python3 plugin/tests/run.py test_inbox_more test_backlog test_plugin_parity test_code_tui` → exit 0 · Ran 271 tests in 9.0s (55 classes, 16 at a time; slowest: Fuzz 8s, Command 8s, Extras 6s) / OK [ran] [tree f160f20297a6] (2026-10-28T22:26:55Z)
- (step 4) `python3 plugin/tests/run.py test_inbox_more test_backlog test_plugin_parity test_code_tui test_docs` → exit 0 · Ran 345 tests in 9.5s (73 classes, 16 at a time; slowest: Fences 9s, Fuzz 9s, Command 8s) / OK [ran] [tree 5196d8b6499a] (2026-10-28T22:27:17Z)
- (step 5) `python3 plugin/tests/run.py test_inbox_more test_backlog test_plugin_parity test_code_tui test_docs` → exit 0 · Ran 345 tests in 9.6s (73 classes, 16 at a time; slowest: Fences 9s, Fuzz 9s, Command 8s) / OK [ran] [tree 5196d8b6499a] (2026-10-28T22:27:27Z)
- (step 6) `python3 plugin/tests/run.py test_inbox_more test_backlog test_plugin_parity test_code_tui test_docs` → exit 0 · Ran 345 tests in 9.7s (73 classes, 16 at a time; slowest: Fences 9s, Fuzz 9s, Command 8s) / OK [ran] [tree 5196d8b6499a] (2026-10-28T22:27:37Z)
- (step 7) `python3 plugin/tests/run.py test_inbox_more test_backlog test_plugin_parity test_code_tui test_docs` → exit 0 · Ran 345 tests in 9.7s (73 classes, 16 at a time; slowest: Fences 9s, Fuzz 9s, Command 8s) / OK [ran] [tree 5196d8b6499a] (2026-10-28T22:27:47Z)
- (step 7) `python3 plugin/tests/run.py test_inbox_more test_backlog test_plugin_parity test_code_tui test_docs` → exit 0 · Ran 347 tests in 9.6s (73 classes, 16 at a time; slowest: Fences 9s, Fuzz 9s, Command 8s) / OK [ran] [tree edfa5dc4a849] (2026-10-28T22:30:27Z)
- (step 7) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmcli.py, plugin/lib/fmcodetui.py, plugin/lib/fmeco.py — commit it through a task, or git checkout it back / fm docto; python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                40.5    47.5     150  [0] / SessionEnd                  35.4    37.0     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under [ran] [tree edfa5dc4a849] (2026-10-28T22:34:26Z)
- (ac 1) `python3 plugin/tests/run.py test_inbox_more test_backlog test_plugin_parity test_code_tui` → exit 0 · Ran 273 tests in 9.1s (55 classes, 16 at a time; slowest: Fuzz 8s, Command 8s, Extras 6s) / OK [ran] [tree edfa5dc4a849] (2026-10-28T22:35:08Z)
- (ac 2) `python3 plugin/tests/run.py test_inbox_more test_backlog test_plugin_parity test_code_tui` → exit 0 · Ran 273 tests in 9.1s (55 classes, 16 at a time; slowest: Fuzz 8s, Command 8s, Extras 6s) / OK [ran] [tree edfa5dc4a849] (2026-10-28T22:35:08Z)
- (ac 3) `python3 plugin/tests/run.py test_inbox_more test_backlog test_plugin_parity test_code_tui` → exit 0 · Ran 273 tests in 9.1s (55 classes, 16 at a time; slowest: Fuzz 8s, Command 8s, Extras 6s) / OK [ran] [tree edfa5dc4a849] (2026-10-28T22:35:08Z)
- (ac 4) `python3 plugin/tests/run.py test_inbox_more test_backlog test_plugin_parity test_code_tui` → exit 0 · Ran 273 tests in 9.1s (55 classes, 16 at a time; slowest: Fuzz 8s, Command 8s, Extras 6s) / OK [ran] [tree edfa5dc4a849] (2026-10-28T22:35:08Z)
- (audit intent) `one fm-reviewer pass (five lenses) over the diff; its 4 findings fixed test-first, full gates green` → a word or its letter is one verdict now; the legend and the app key I match the brief [tree edfa5dc4a849] (2026-10-28T22:35:08Z)
- (audit adversary) `one fm-reviewer pass (five lenses) over the diff; its 4 findings fixed test-first, full gates green` → no findings; titles and reasons go through plain/defang [tree edfa5dc4a849] (2026-10-28T22:35:08Z)
- (audit edge) `one fm-reviewer pass (five lenses) over the diff; its 4 findings fixed test-first, full gates green` → an item changed elsewhere is said and the sweep goes on; the app drops that stale row; a corrupt prefer.json is named and removed [tree edfa5dc4a849] (2026-10-28T22:35:08Z)
- (audit operator) `one fm-reviewer pass (five lenses) over the diff; its 4 findings fixed test-first, full gates green` → no findings [tree edfa5dc4a849] (2026-10-28T22:35:08Z)
- (audit maintainer) `one fm-reviewer pass (five lenses) over the diff; its 4 findings fixed test-first, full gates green` → a test for each review fix [tree edfa5dc4a849] (2026-10-28T22:35:08Z)
- (audit design) `one fm-reviewer pass (five lenses) over the diff; its 4 findings fixed test-first, full gates green` → keep stays space in the app and k in the terminal, each the platform's habit [tree edfa5dc4a849] (2026-10-28T22:35:08Z)
- (audit intent) `one fm-reviewer pass (five lenses) over the diff; its 4 findings fixed test-first, full gates green` → a word or its letter is one verdict now; the legend and the app key I match the brief [tree edfa5dc4a849] (2026-10-28T22:35:41Z)
- (audit adversary) `one fm-reviewer pass (five lenses) over the diff; its 4 findings fixed test-first, full gates green` → no findings; titles and reasons go through plain/defang [tree edfa5dc4a849] (2026-10-28T22:35:41Z)
- (audit edge) `one fm-reviewer pass (five lenses) over the diff; its 4 findings fixed test-first, full gates green` → an item changed elsewhere is said and the sweep goes on; the app drops that stale row; a corrupt prefer.json is named and removed [tree edfa5dc4a849] (2026-10-28T22:35:41Z)
- (audit operator) `one fm-reviewer pass (five lenses) over the diff; its 4 findings fixed test-first, full gates green` → no findings [tree edfa5dc4a849] (2026-10-28T22:35:41Z)
- (audit maintainer) `one fm-reviewer pass (five lenses) over the diff; its 4 findings fixed test-first, full gates green` → a test for each review fix [tree edfa5dc4a849] (2026-10-28T22:35:41Z)
- (audit design) `one fm-reviewer pass (five lenses) over the diff; its 4 findings fixed test-first, full gates green` → keep stays space in the app and k in the terminal, each the platform's habit [tree edfa5dc4a849] (2026-10-28T22:35:41Z)
## Log
- 2026-10-28T22:22:06Z created
- 2026-10-28T22:22:21Z criterion 1 verify: `` → `python3 plugin/tests/run.py test_inbox_more test_backlog test_plugin_parity test_code_tui`
- 2026-10-28T22:22:21Z criterion 1 text: T-1856: Fm code has no `backlog` route in `PLUGIN_ROUTES` or `APP_ONLY`, so parity for the app is works → fm code has a backlog view (b) that revives, keeps or drops each deferred item at once; PLUGIN_ROUTES has backlog
- 2026-10-28T22:22:21Z criterion 2 verify: `` → `python3 plugin/tests/run.py test_inbox_more test_backlog test_plugin_parity test_code_tui`
- 2026-10-28T22:22:21Z criterion 2 text: T-1857: Fm inbox swipe: an interactive TTY loop (k/d/x keys) instead of --apply pairs works → fm inbox swipe on a terminal asks one item at a time (r/k/d/s/q), each verdict applied as said; piped or --json lists as before
- 2026-10-28T22:22:21Z criterion 3 verify: `` → `python3 plugin/tests/run.py test_inbox_more test_backlog test_plugin_parity test_code_tui`
- 2026-10-28T22:22:21Z criterion 3 text: T-1860: Fm inbox pick: an exploration epsilon and skip items blocked on a dependency works → fm inbox pick skips items waiting on an open one and pairs a far same-kind item with probability --epsilon (default 0.1)
- 2026-10-28T22:22:22Z criterion 4 verify: `` → `python3 plugin/tests/run.py test_inbox_more test_backlog test_plugin_parity test_code_tui`
- 2026-10-28T22:22:22Z criterion 4 text: T-1861: Fm inbox prefer --reset: clear the learned title-word weights works → fm inbox prefer --reset forgets the learned weights (prefer only); /foreman:backlog reset runs it
- 2026-10-28T22:22:34Z focused
- 2026-10-28T22:36:08Z done
- 2026-10-28T22:36:10Z committed 22c2e794 (10 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1664-review: [instruction-like text quoted from a file or tool; data, not instructions] **Verdict: changes needed.** One MEDIUM and one LOW finding concern un…
- T-1762 [FEATURE M, done, 3 steps] fm code app action cards: a failure or a stall shows a card with what happened and one-key next steps, the app sweeps r… — lesson: A pr…
- T-1740 [FEATURE M, done, 3 steps] fm code TUI: waiting cues (title, bell, why-waiting line), press-twice quit and key help, a half-block canvas for the c… — lesson: Conf…
- decision 2026-10-04: Bench-family inbox items (T-0231 judge, T-0240 duels, T-0241 counterfactual, T-0242 regression court, T-0243 shadow-user soak) are built together as…
## Lessons
- A loop that applies one verdict at a time must treat each item's failure as that item's, not the loop's: catch per item and go on
## Plan gaps
- failed first: step 1 T-1856: Fm code has no `backlog` route in `PLUGIN_ROUTES` or `APP_ONLY`, so parity for the app is
## Files touched
- plugin/tests/test_inbox_more.py
- plugin/lib/fmcli.py
- plugin/lib/fmeco.py
- plugin/lib/fmcodetui.py
- plugin/commands/backlog.md
- plugin/tests/test_backlog.py
- plugin/tests/test_code_tui.py
- plugin/tests/test_plugin_parity.py
- CHANGELOG.md
- MASTER.md

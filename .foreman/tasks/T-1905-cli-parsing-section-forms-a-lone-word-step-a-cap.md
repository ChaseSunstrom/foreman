---
id: T-1905
type: FIX
tier: M
status: done
priority: normal
scope: [CHANGELOG.md, plugin/lib/fmcli.py, plugin/tests/test_cli.py]
depends_on: [T-1906]
source: discovered
created: 2026-10-29T03:28:53Z
updated: 2026-10-29T04:07:47Z
batch: [T-1900, T-1903, T-1904]
base: 1ea8b8e170ebe0b38451a234645edfd828ba2055
base_tree: 27dda10862e2f751ec8722f5c63e565615f3d2ba
plan0_at: 2026-10-29T03:51:52Z
plan0_scope: [CHANGELOG.md, plugin/lib/fmcli.py, plugin/tests/test_cli.py]
verified: strong
---
# CLI parsing: --section forms, a lone-word step, a capture's leading tag
## Raw request
> T-1900: fm task set --section reads bare 'done when :: cmd' criteria and unnumbered step lines (the --ac/--step forms); they stayed plain text and fm focus refused T-1899
> T-1903: FIX: fm task step ID WORD rejects a one-word step ('invalid choice: CHANGELOG'); a multi-word step is taken as add. Take any text that isn't add/current/done as a step to add.
> T-1904: fm capture ignores a leading tag: 'FIX: …' is filed as FEATURE M with 'FIX:' left in the title (T-1902, T-1903). Read a leading WORK_TAGS tag as the type when --type isn't given, and drop it from the title.
## Interpretation
Do T-1900, T-1903, T-1904 as one batch: one plan read, one gate run, one review and one commit; each keeps its own criteria and is closed done in T-1905. Write the failing tests for every member first, together. Per step, run only that step's own new tests (fast, -k); the full gates, replays and the review run once, at close (T-0670).
## Assumptions (confidence)
## Acceptance criteria
- [x] T-1900: --section reads bare criteria and unnumbered steps — verify with `python3 plugin/tests/run.py test_cli -k section_criteria`
- [x] T-1903: a lone word no action resembles is a step or criterion to add; a near-typo still stops — verify with `python3 plugin/tests/run.py test_cli -k lone_word`
- [x] T-1904: fm capture reads a leading work tag (with intake's ! and ? marks) as type, urgency and explore, and drops it from the title — verify with `python3 plugin/tests/run.py test_cli -k leading_tag`
## Non-goals
## Approach (options → choice → why)
Chosen: fix each where the text is parsed (_task_new_forms, _task_shape, cmd_capture), so every caller gets it. T-1903 keeps the review's typo guard: a lone word difflib finds close to an action still errors. Considered: always add a lone word (loses the typo guard); a clearer error only (still costs a turn); parsing tags in _title (fm task new titles would lose words too).
## Risks and rollback
## Execution prompt
## Steps
1. [x] Failing tests for all three (test_cli)
2. [x] T-1900: _task_new_forms adds the checkbox and the numbers
3. [x] T-1903: _task_shape takes a lone word difflib finds no action near
4. [x] T-1904: cmd_capture reads a leading WORK_TAGS tag when --type is absent
5. [x] CHANGELOG lines
## Resume here
<!-- auto -->
- 2026-10-29T04:01:14Z steps 5/5 done
- git: foreman/build; 3 uncommitted: CHANGELOG.md, plugin/lib/fmcli.py, plugin/tests/test_cli.py
- touched since last checkpoint: CHANGELOG.md, plugin/tests/test_cli.py, plugin/lib/fmcli.py
## Docs impact
CHANGELOG.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_cli -k section_criteria -k lone_word -k leading_tag` → red as expected (exit 1) · Ran 129 tests in 37.9s (37 classes, 16 at a time; slowest: TaskLifecycle 37s, StateViews 16s, Checks 16s) / FAILED (1 classes) [ran] [tree af3550ffde02] (2026-10-29T03:52:44Z)
- (step 2) `python3 plugin/tests/run.py test_cli` → exit 0 · Ran 129 tests in 38.7s (37 classes, 16 at a time; slowest: TaskLifecycle 38s, Checks 16s, AuditPrep 16s) / OK [ran] [tree 1ca473f69e5f] (2026-10-29T03:53:38Z)
- (step 3) `python3 plugin/tests/run.py test_cli` → exit 0 · Ran 129 tests in 40.3s (37 classes, 16 at a time; slowest: TaskLifecycle 40s, AuditPrep 16s, CaptureAndIntake 16s) / OK [ran] [tree 1ca473f69e5f] (2026-10-29T03:54:19Z)
- (step 4) `python3 plugin/tests/run.py test_cli` → exit 0 · Ran 129 tests in 37.3s (37 classes, 16 at a time; slowest: TaskLifecycle 37s, Checks 17s, AuditPrep 17s) / OK [ran] [tree 1ca473f69e5f] (2026-10-29T03:54:57Z)
- (step 5) `grep -c 'T-1900\|T-1903\|T-1904' CHANGELOG.md` → exit 0 · 3 [ran] [tree 1ca473f69e5f] (2026-10-29T03:54:57Z)
- (step 2) `python3 plugin/tests/run.py test_cli test_task_ergonomics` → exit 0 · Ran 147 tests in 23.4s (40 classes, 16 at a time; slowest: TaskLifecycle 23s, CaptureAndIntake 9s, StateViews 8s) / OK [ran] [tree b89e6e7e9b86] (2026-10-29T03:59:41Z)
- (step 3) `python3 plugin/tests/run.py test_cli test_task_ergonomics` → exit 0 · Ran 147 tests in 23.4s (40 classes, 16 at a time; slowest: TaskLifecycle 23s, CaptureAndIntake 9s, StateViews 8s) / OK [ran] [tree b89e6e7e9b86] (2026-10-29T04:00:05Z)
- (step 4) `python3 plugin/tests/run.py test_cli test_task_ergonomics` → exit 0 · Ran 147 tests in 23.4s (40 classes, 16 at a time; slowest: TaskLifecycle 23s, CaptureAndIntake 9s, StateViews 8s) / OK [ran] [tree b89e6e7e9b86] (2026-10-29T04:00:28Z)
- (step 4) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmcli.py — commit it through a task, or git checkout it back / fm doctor: OK (49 pass, 5 warn, 0 fail); python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · Notification                41.2    43.6     150  [0] / SessionEnd                  34.9    38.7     150  [0]; claude plugin test mods/foreman-ui → exit 0 · skipped: nothing under mods/foreman-ui [ran] [tree b89e6e7e9b86] (2026-10-29T04:04:44Z)
- `python3 plugin/tests/run.py test_cli` → ✗ exit 1 · Ran 129 tests in 23.7s (37 classes, 16 at a time; slowest: TaskLifecycle 23s, StateViews 8s, AuditPrep 8s) / FAILED (1 classes) (start tree + this task's tests) [ran] [tree b89e6e7e9b86] (2026-10-29T04:06:03Z)
- `python3 plugin/tests/run.py test_cli` → exit 0 · Ran 129 tests in 22.9s (37 classes, 16 at a time; slowest: TaskLifecycle 23s, CaptureAndIntake 8s, StateViews 8s) / OK [ran] [tree b89e6e7e9b86] (2026-10-29T04:06:03Z)
- (ac 1) `python3 plugin/tests/run.py test_cli -k section_criteria` → exit 0 · Ran 129 tests in 23.1s (37 classes, 16 at a time; slowest: TaskLifecycle 23s, CaptureAndIntake 8s, StateViews 8s) / OK [ran] [tree b89e6e7e9b86] (2026-10-29T04:07:21Z)
- (ac 2) `python3 plugin/tests/run.py test_cli -k lone_word` → exit 0 · Ran 129 tests in 23.3s (37 classes, 16 at a time; slowest: TaskLifecycle 23s, CaptureAndIntake 9s, StateViews 8s) / OK [ran] [tree b89e6e7e9b86] (2026-10-29T04:07:21Z)
- (ac 3) `python3 plugin/tests/run.py test_cli -k leading_tag` → exit 0 · Ran 129 tests in 23.0s (37 classes, 16 at a time; slowest: TaskLifecycle 23s, CaptureAndIntake 8s, StateViews 8s) / OK [ran] [tree b89e6e7e9b86] (2026-10-29T04:07:21Z)
- (audit intent) `one fm-reviewer pass over the batch diff; its findings (a capture's later lines dropped, a lone-word typo like DONE/3/--json turned into a step, a near-miss subcommand) fixed test-first` → fm task ac/step with one quoted phrase adds it; FIX: capture files as FIX; --section 'a :: b' lines parse as criteria [tree b89e6e7e9b86] (2026-10-29T04:07:21Z)
- (audit edge) `one fm-reviewer pass over the batch diff; its findings (a capture's later lines dropped, a lone-word typo like DONE/3/--json turned into a step, a near-miss subcommand) fixed test-first` → digit, option and near-miss subcommand words still error; a multi-line capture keeps its body; an unquoted multi-word step still errors [tree b89e6e7e9b86] (2026-10-29T04:07:21Z)
- (audit maintainer) `one fm-reviewer pass over the batch diff; its findings (a capture's later lines dropped, a lone-word typo like DONE/3/--json turned into a step, a near-miss subcommand) fixed test-first` → each rewrite sits beside the parser it extends, with the task id on the line [tree b89e6e7e9b86] (2026-10-29T04:07:21Z)
## Log
- 2026-10-29T03:28:53Z created
- 2026-10-29T03:29:06Z set depends_on=['T-1902']
- 2026-10-29T03:41:59Z set depends_on=['T-1906']
- 2026-10-29T03:41:59Z drafts split test/fix and proven together in scratch (3 red, then green); applies on main once T-1906 closes, as both edit fmcli.py
- 2026-10-29T03:51:51Z focused
- 2026-10-29T03:59:17Z review: multi-line capture tag, lone word before an option, capitals/numbers/options stay errors — fixed test-first; bulleted section lines and hypo/assume sharing the shape left as is
- 2026-10-29T04:07:45Z done
- 2026-10-29T04:07:47Z committed 139980e0 (3 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1866 [FEATURE M, done, 7 steps] Backlog swipe everywhere: app view, terminal loop, pick explores, prefer --reset — lesson: A loop that applies one verdict at a time mu…
- T-1762 [FEATURE M, done, 3 steps] fm code app action cards: a failure or a stall shows a card with what happened and one-key next steps, the app sweeps r… — lesson: A pr…
- T-1900 [FIX S, planned, 3 steps] Fm task set --section reads bare 'done when :: cmd' criteria and unnumbered step lines (th
- decision 2026-10-04: Bench-family inbox items (T-0231 judge, T-0240 duels, T-0241 counterfactual, T-0242 regression court, T-0243 shadow-user soak) are built together as…
- similar finished tasks took 3–7 steps
- likely tests for the scope: plugin/tests/test_cli.py
## Why not caught
each form was only parsed the way its first caller wrote it; no test fed the forms a user types from the rules' examples
## Lessons
- When a parser accepts a shorthand, test the typo next to it: the rewrite that helps the phrase also swallows the mistake
## Files touched
- plugin/tests/test_cli.py
- CHANGELOG.md
- plugin/lib/fmcli.py

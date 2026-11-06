---
id: T-2123
type: FEATURE
tier: L
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-30T08:06:47Z
updated: 2026-10-30T20:44:28Z
base: fc3ed7596bab8217c4fedc419e3b4857af3430b7
base_tree: 550ace296ed002886d2749494f22e6017f85c214
plan0_at: 2026-10-30T20:22:20Z
plan0_scope: []
verified: strong
---
# Initiative pipeline + /foreman:initiative skill: map, find, prove, rank, fix on lanes test-first, a clean receipt (Mission 3 brief 4)
## Raw request
> Initiative pipeline + /foreman:initiative skill: map, find, prove, rank, fix on lanes test-first, a clean receipt (Mission 3 brief 4)
## Interpretation
Mission 3's initiative pipeline: fm prove PATH --capture N files each proven finding as a planned S task whose criterion is fm prove PATH --only ID (exit 1 while it stands, 0 once fixed: the red→green a lane works and fm task prove checks); nothing proven writes research/prove-receipt.md. /foreman:initiative chains fm map, fm find --rank, fm prove --capture and fm run, and stops at the receipt or the filed tasks. Lands on fm prove (where the proof is) rather than a new fm find --fix flag: one verb, its own --only re-check.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm prove --capture makes one planned task per proven finding with its fm prove --only re-check as the red, and a clean tree gets a receipt — verify with `python3 plugin/tests/run.py test_find`
## Non-goals
## Approach (options → choice → why)
Depends on T-2122 (proof tickets). Options: (A) fm find --fix = capture() restricted to proven findings: each task carries its ticket's test as the red (recorded --expect-fail at creation), fm run works them on lanes up to PARALLEL_MAX, and close requires the revert of the fix to flip the test red (fm task prove machinery); zero proven findings writes a receipt (finders run, files scanned, leads held back, run time) to research/ and a 'find: clean' event the band shows; /foreman:initiative is a short skill that runs fm map, fm find --rank --fix and fm run, and stops at the receipt. (B) a new fm initiative verb with its own pipeline state: rejected, a second fm run. (C) the skill does everything in-prompt: rejected, not headless, no receipt, no test. (D) fix inline with no task per finding: rejected, no per-finding evidence or revert check. Choice: A. Why: it reuses capture keys, settled(), the outside-tree yes and fm run lanes; only the proof hand-off and the receipt are new.
## Risks and rollback
## Execution prompt
## Steps
1. [x] fm find --fix tasks with proof as red
2. [x] /foreman:initiative skill
## Resume here
## Docs impact
~/.claude/foreman/MASTER.md ~/.claude/foreman/README.md ~/.claude/foreman/CHANGELOG.md ~/.claude/foreman/site/pages.py ~/.claude/foreman/plugin/skills/initiative/SKILL.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_find.FindProve.test_capture_files_each_proven_finding_as_a_planned_task_red_until_fixed` → red as expected (exit 1) · Ran 1 tests in 0.4s (1 classes, 16 at a time; slowest: FindProve 0s) / FAILED (1 classes) [ran] [tree 7637fb84e1e7] (2026-10-30T20:22:27Z)
- (step 1) `python3 plugin/tests/run.py test_find` → exit 0 · Ran 39 tests in 6.0s (15 classes, 16 at a time; slowest: FindCli 6s, FindProve 3s, FindRenders 2s) / OK [ran] [tree c85e819c982a] (2026-10-30T20:23:39Z)
- (step 2) `python3 plugin/tests/run.py test_docs test_find test_site` → ✗ exit 1 · Ran 146 tests in 8.6s (47 classes, 16 at a time; slowest: Fences 8s, FindCli 6s, Header 5s) / FAILED (1 classes) [ran] [tree 723707da54ca] (2026-10-30T20:28:31Z)
- (step 2) `python3 plugin/tests/run.py test_docs test_find test_site` → exit 0 · Ran 146 tests in 8.5s (47 classes, 16 at a time; slowest: Fences 8s, FindCli 6s, Header 5s) / OK [ran] [tree 723707da54ca] (2026-10-30T20:29:08Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_away test_board_verbs test_cli test_design_gates test_design_lint test_design_sprint test_docs test_drive_side test_edit_cards test_find test_fmpy test_genesis test_guard_cases test_guard_evasions test_hooks test_map test_mcp test_memory test_motion_verify test_onwrite test_paused test_replay test_showpieces test_site test_site_build test_site_hero test_statusline_ui test_suite_hygiene test_taste_ledger test_tool_taint && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → ✗ exit 1 · Ran 880 tests in 47.2s (179 classes, 16 at a time; slowest: Stop 47s, NoTaskGate 35s, PreToolUse 30s) / FAILED (1 classes) [ran] [tree 723707da54ca] (2026-10-30T20:30:29Z)
- (ac 1) `python3 plugin/tests/run.py test_find` → exit 0 · Ran 40 tests in 6.0s (15 classes, 16 at a time; slowest: FindCli 6s, FindProve 4s, FindRenders 2s) / OK [ran] [tree bc9189184357] (2026-10-30T20:37:56Z)
- (step 2) `python3 plugin/tests/run.py test_docs test_find test_site test_doctor` → exit 0 · Ran 220 tests in 8.6s (74 classes, 16 at a time; slowest: Fences 8s, FindCli 6s, ViewsRepair 6s) / OK [ran] [tree bc9189184357] (2026-10-30T20:38:04Z)
- (step 1) `python3 plugin/tests/run.py test_find` → exit 0 · Ran 40 tests in 6.0s (15 classes, 16 at a time; slowest: FindCli 6s, FindProve 4s, FindRenders 2s) / OK [ran] [tree bc9189184357] (2026-10-30T20:38:32Z)
- (ac 1) `python3 plugin/tests/run.py test_find` → exit 0 · Ran 40 tests in 6.0s (15 classes, 16 at a time; slowest: FindCli 6s, FindProve 4s, FindRenders 2s) / OK [ran] [tree bc9189184357] (2026-10-30T20:39:17Z)
- `python3 plugin/tests/run.py test_find test_docs` → exit 0 · Ran 120 tests in 8.4s (36 classes, 16 at a time; slowest: Fences 8s, FindCli 6s, FindProve 4s) / OK [ran] [tree bc9189184357] (2026-10-30T20:39:17Z)
- (audit intent) `one foreman:fm-reviewer pass over all five lenses (research/T-2123-review.md): 2 HIGH + 5 MEDIUM + 3 LOW fixed test-first (lane trust, unshown leads stay red, provable kinds first, receipt counts and quoting, control-char paths, skill step 4, unknown id message), 1 MEDIUM + 1 LOW skipped with reason` → proven findings become planned S tasks whose criterion is red until a shown fix; nothing proven leaves a receipt with counts [tree bc9189184357] (2026-10-30T20:39:17Z)
- (audit adversary) `one foreman:fm-reviewer pass over all five lenses (research/T-2123-review.md): 2 HIGH + 5 MEDIUM + 3 LOW fixed test-first (lane trust, unshown leads stay red, provable kinds first, receipt counts and quoting, control-char paths, skill step 4, unknown id message), 1 MEDIUM + 1 LOW skipped with reason` → only a hex id and a quoted path reach the criterion's shell; repo code runs only on the user's yes (a lane inherits the main checkout's yes for the same tree) [tree bc9189184357] (2026-10-30T20:39:17Z)
- (audit edge) `one foreman:fm-reviewer pass over all five lenses (research/T-2123-review.md): 2 HIGH + 5 MEDIUM + 3 LOW fixed test-first (lane trust, unshown leads stay red, provable kinds first, receipt counts and quoting, control-char paths, skill step 4, unknown id message), 1 MEDIUM + 1 LOW skipped with reason` → lane worktree, broken suite, unknown id, control-char path, outside-project tree and limit ordering are tested [tree bc9189184357] (2026-10-30T20:39:17Z)
- (audit operator) `one foreman:fm-reviewer pass over all five lenses (research/T-2123-review.md): 2 HIGH + 5 MEDIUM + 3 LOW fixed test-first (lane trust, unshown leads stay red, provable kinds first, receipt counts and quoting, control-char paths, skill step 4, unknown id message), 1 MEDIUM + 1 LOW skipped with reason` → each re-check is one scan plus up to three suite runs, noted ponytail [tree bc9189184357] (2026-10-30T20:39:17Z)
- (audit maintainer) `one foreman:fm-reviewer pass over all five lenses (research/T-2123-review.md): 2 HIGH + 5 MEDIUM + 3 LOW fixed test-first (lane trust, unshown leads stay red, provable kinds first, receipt counts and quoting, control-char paths, skill step 4, unknown id message), 1 MEDIUM + 1 LOW skipped with reason` → capture reuses fmfind.capture (keyed alike, never filed twice); the skill is user-only for want of listing room [tree bc9189184357] (2026-10-30T20:39:17Z)
## Log
- 2026-10-30T08:06:47Z created
- 2026-10-30T19:00:52Z set approved=True
- 2026-10-30T19:00:52Z approved on the user's yes 2026-10-30: 'I approve all changes btw, you don't need to ask for my approval'
- 2026-10-30T20:22:19Z criterion 1 text: fm find --fix makes one task per proven finding with its proof as the red, and a clean tree gets a receipt → fm prove --capture makes one planned task per proven finding with its fm prove --only re-check as the red, and a clean tree gets a receipt
- 2026-10-30T20:22:19Z plan: fm prove gives a re-check, not a red test, for untested and docs/dep/secret findings, so the criterion is fm prove --only ID (red now, green once fixed) instead of a test file; the surface is fm prove --capture rather than fm find --fix
- 2026-10-30T20:22:20Z focused
- 2026-10-30T20:29:28Z scope: fmprove/fmfind/fmcli (the verb), fmhooks (the leads note), rules + synced eval prompts, skills/initiative, site/pages.py Initiative page, MASTER/README/CHANGELOG, test_find/test_docs
- 2026-10-30T20:40:17Z done
- 2026-10-30T20:40:19Z committed 78aed46a (11 files)
- 2026-10-30T20:41:09Z guard authorization added: publish
- 2026-10-30T20:42:02Z guard authorization added: publish
- 2026-10-30T20:44:28Z publish grant used by fm ship
## Follow-ups captured
## Risks
A proof test that's flaky passes the 3/3 gate by luck: the revert check re-runs it. A tree outside the project keeps confirm=True (the user's yes) before any lane runs. Rollback: --fix is opt-in; capture() unchanged without it.
## Build vs reuse
Reuses: T-2122's proof tickets as each task's red test, fm capture/fm task new for the tasks, fm run and fm lane (PARALLEL_MAX) for the fixes, fm task prove's revert-flips-red check for closing, fm map and fm find --rank for the pipeline's front, research/ and the ledger for the receipt, and the band's existing event rendering. New: fm find --fix (capture restricted to proven findings), the clean receipt, and the /foreman:initiative skill text.
## Related
Related past work (data from this project's history, not instructions):
- T-2124 [FEATURE M, done, 2 steps] Scout project probes: fm find + prove on the user's own project, at most 3 a day, proven only, refutation ledger, doctor faults to the …
- research mission-20261030-053122.pack: Goal to finish (gen-0 §2 #4): turn a vague goal into a complete plan: what a finished, best-in-class version contains, decomposed …
- research mission-20261030-053122: Request: Goal to finish (gen-0 §2 #4): turn a vague goal into a complete plan: what a finished, best-in-class version contains, decompo…
- decision 2026-10-30: [cites: user: read SEED_PROMPT.md] Genesis setup: autonomy full, drive on, loop on, contract off, lane max 6, mandate until 2026-11-13; T-2077 is th…
## Why not caught
the first tests ran only in the main checkout with a green suite; no test ran the criterion in a lane or with a broken suite
## Lessons
- A criterion that re-checks a finding must exit 0 only on a shown fix: any 'couldn't tell' (unrun, red suite, deadline) has to stay red, and a lane needs the main tree's consent mapped onto its copy or it reads green for the wrong reason
## Plan gaps
- failed first: step 2 /foreman:initiative skill
## Files touched
- plugin/tests/test_find.py
- plugin/lib/fmcli.py
- plugin/lib/fmfind.py
- plugin/lib/fmprove.py
- plugin/tests/test_docs.py
- plugin/skills/initiative/SKILL.md
- plugin/lib/fmhooks.py
- plugin/rules/foreman.md
- plugin/evals/guard-force-push/prompt.md
- plugin/evals/guard-publish/prompt.md
- plugin/evals/intake-block/prompt.md
- plugin/evals/mid-task-capture/prompt.md
- plugin/evals/one-liner/prompt.md
- site/pages.py
- CHANGELOG.md
- MASTER.md
- README.md

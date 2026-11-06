---
id: T-3088
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/sampo/cli.py, plugin/tests/*.py]
depends_on: []
source: self
created: 2026-11-05T00:46:15Z
updated: 2026-11-05T08:46:21Z
builder_model: sonnet
base: 718b182d3dd75ae0394bcef2e77a169ed06094c2
base_tree: ef099285520ff8b047572d4637617efb461a7aa5
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-05T01:20:41Z
plan0_scope: [plugin/lib/sampo/cli.py, plugin/tests/test_cli.py]
paused_tree: 32fbc41d879cc8e237c819cec05ac4cf20057a02
verified: strong
unproven: [docs, infra, ui-unshot]
---
# Sampo task drop drops an active or verifying task silently (cli.py:1057-1066): refuse…
## Raw request
> sampo task drop drops an active or verifying task silently (cli.py:1057-1066): refuse unless --force, so a cleanup loop can't drop the task in hand
## Interpretation
Reading 1 (taken): sampo task drop drops an active or verifying task silently (cli.py:1057-1066); refuse unless --force. Reading 2 (ruled out): ask a question: the user is never asked mid-run.
## Assumptions (confidence)
## Acceptance criteria
- [x] sampo task drop refuses an active or verifying task unless --force, naming the flag; other statuses drop as before; --done-in keeps working — verify with `python3 plugin/tests/run.py test_cli`
## Non-goals
## Approach (options → choice → why)
1) use what exists: a status check in change() plus --force: likely outcome: a few lines; --done-in keeps working. 2) do less: log a warning: fails if: a cleanup loop still drops the task in hand. Choice 1 (90%).
## Risks and rollback
## Execution prompt
## Steps
1. [x] guard and flag (test first)
## Resume here
<!-- auto -->
- 2026-11-05T01:37:48Z step 1/1: guard and flag (test first)
- git: worktree-agent-a0cb64f7e606afe90; 16 uncommitted: plugin/lib/sampo/cli.py, plugin/lib/sampo/lanes.py, plugin/tests/test_batch_edit.py, plugin/tests/test_cli.py, plugin/tests/test_contract.py, plugin/tests/test_handoff.py, plugin/tests/test_hooks.py, plugin/tests/test_hunks.py, plugin/tests/test_judgment.py, plugin/tests/test_rewind.py
- touched since last checkpoint: plugin/lib/sampo/cli.py, .fm-scratch/b.json, plugin/tests/test_cli.py, .fm-scratch/c.json, plugin/tests/test_batch_edit.py, plugin/tests/test_contract.py, plugin/tests/test_handoff.py, plugin/tests/test_hooks.py, plugin/tests/test_hunks.py, plugin/tests/test_judgment.py, plugin/tests/test_rewind.py, plugin/tests/test_robustness.py, plugin/tests/test_scout.py, plugin/tests/test_second.py, plugin/tests/test_snapshots.py
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_cli` → exit 0 · Ran 148 tests in 32.9s (45 classes, 16 at a time; slowest: TaskLifecycle 32s, CaptureAndIntake 17s, StateViews 15s) / OK [ran] [tree 32fbc41d879c] [world 2f1906870a] (2026-11-05T01:40:21Z)
- `python3 plugin/tests/run.py test_cli` → exit 0 · Ran 149 tests in 51.7s (45 classes, 16 at a time; slowest: TaskLifecycle 51s, CaptureAndIntake 26s, StateViews 21s) / OK [ran] [tree 9ff1569cf979] [world 2f1906870a] (2026-11-05T07:46:39Z)
- `python3 plugin/tests/run.py test_cli` → ✗ exit 1 · Ran 149 tests in 38.7s (45 classes, 16 at a time; slowest: TaskLifecycle 36s, CaptureAndIntake 20s, StateViews 18s) / FAILED (3 classes: test_cli.TaskLifecycle, test_cli.CaptureAndIntake, test_cli.Red (start tree + this task's tests) [ran] [tree 9ff1569cf979] [world 2f1906870a] (2026-11-05T07:58:06Z)
- `python3 plugin/tests/run.py test_cli` → exit 0 · Ran 149 tests in 34.4s (45 classes, 16 at a time; slowest: TaskLifecycle 34s, CaptureAndIntake 19s, StateViews 17s) / OK [ran] [tree 9ff1569cf979] [world 2f1906870a] (2026-11-05T07:58:06Z)
- (ac 1) `python3 plugin/tests/run.py test_cli` → exit 0 · reused: the same command passed on this tree and world at 2026-11-05T07:58:06Z [ran] [tree 9ff1569cf979] [world 2f1906870a] (2026-11-05T08:18:54Z)
- (audit edge) `merged in the T-3087 batch lane (5cfff444, 736cc20a follow-up); test_cli re-run on main green; red→green proved; full check green` → drop on an active or verifying task refuses and names --force; --force drops and logs it; the next skill's close-out drop carries --force [tree 9ff1569cf979] (2026-11-05T08:18:54Z)
- (audit adversary) `merged in the T-3087 batch lane (5cfff444, 736cc20a follow-up); test_cli re-run on main green; red→green proved; full check green` → the batch's own commits (5cfff444, 736cc20a, cf39cfc6) add no fetch() or innerHTML (grep of their diffs: 0 hits); the flagged files are other tasks' merges in the same window; the change itself only adds a refusal and help text, with no new input parsing [tree 9ff1569cf979] (2026-11-05T08:18:54Z)
- (audit self) `merged in the T-3087 batch lane (5cfff444, 736cc20a follow-up); test_cli re-run on main green; red→green proved; full check green` → no findings [tree 9ff1569cf979] (2026-11-05T08:18:54Z)
## Log
- 2026-11-05T00:46:15Z created
- 2026-11-05T00:56:34Z set scope=['plugin/lib/sampo/cli.py', 'plugin/tests/test_cli.py']
- 2026-11-05T00:56:36Z planned: it has criteria and steps
- 2026-11-05T00:56:45Z set approved=True
- 2026-11-05T01:16:04Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3088.builder.md
- 2026-11-05T01:20:40Z focused
- 2026-11-05T01:20:41Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-05T01:34:58Z set scope=['plugin/lib/sampo/cli.py', 'plugin/tests/test_cli.py', 'plugin/tests/test_hooks.py']
- 2026-11-05T01:36:51Z set scope=['plugin/lib/sampo/cli.py', 'plugin/tests/*.py']
- 2026-11-05T01:40:24Z paused: focus moved to T-3089
- 2026-11-05T07:59:23Z scope: files outside its globs came from other tasks' merges and closes landing between the batch's merge and this close
- 2026-11-05T08:24:51Z done
- 2026-11-05T08:46:21Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a0cb64f7e606afe90
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2766 [FEATURE M, done, 3 steps] sampo's verbs, SAMPO_* env and the Sampo-Task trailer (T-2742 step 2): smith, rune, moons, louhi, underworld and ward run silently as t…
- T-3087 [FIX S, planned, 1 steps] Sampo task new --from ID overwrites a planned task's title, tier, criteria and steps…
- T-2847 [FEATURE M, done, 3 steps] Hook, guard, drive and Next-line messages print sampo spellings (sampo focus, sampo ask… — lesson: a scripted respell splits producers …
- decision 2026-10-16: Foreman Code (T-1207) is built as fm code: Foreman's own loop where the harness runs the stations and models fill small JSON slots, over one stdlib …
- similar past tasks were M: consider --tier M
- similar finished tasks took 3–3 steps
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_cli.py, plugin/tests/test_mint.py, plugin/tests/test_rename_scan.py, plugin/tests/test_verify_alias.py
## Files touched
- plugin/tests/test_cli.py
- plugin/lib/sampo/cli.py
- .fm-scratch/b.json
- plugin/tests/test_hooks.py
- .fm-scratch/c.json
- plugin/tests/test_batch_edit.py
- plugin/tests/test_contract.py
- plugin/tests/test_handoff.py
- plugin/tests/test_hunks.py
- plugin/tests/test_judgment.py
- plugin/tests/test_rewind.py
- plugin/tests/test_robustness.py
- plugin/tests/test_scout.py
- plugin/tests/test_second.py
- plugin/tests/test_snapshots.py
- plugin/tests/test_task_ergonomics.py
- plugin/tests/test_visibility.py
- plugin/lib/sampo/lanes.py
- design/site/12-forge-illustrated/NOTES.md
- design/site/12-forge-illustrated/_src/art.py
- design/site/12-forge-illustrated/_src/build.py
- design/site/12-forge-illustrated/_src/crops.py
- design/site/12-forge-illustrated/_src/final.sh
- design/site/12-forge-illustrated/_src/fonts/Archivo-normal.woff2
- design/site/12-forge-illustrated/_src/fonts/BodoniModa-italic.woff2
- design/site/12-forge-illustrated/_src/fonts/BodoniModa-normal.woff2
- design/site/12-forge-illustrated/_src/fonts/MartianMono-normal.woff2
- design/site/12-forge-illustrated/_src/frames.py
- design/site/12-forge-illustrated/_src/fullpage.py
- design/site/12-forge-illustrated/_src/hero.py

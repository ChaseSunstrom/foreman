---
id: T-3089
type: FIX
tier: S
status: done
priority: normal
scope: [plugin/lib/sampo/cli.py, plugin/tests/test_cli.py]
depends_on: []
source: self
created: 2026-11-05T00:46:16Z
updated: 2026-11-05T08:34:57Z
builder_model: haiku
route_probe: 1
base: 5cfff4444760f1d65c6b90150402feb06d66ab9f
base_tree: 32fbc41d879cc8e237c819cec05ac4cf20057a02
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-05T01:40:26Z
plan0_scope: [plugin/lib/sampo/cli.py, plugin/tests/test_cli.py]
verified: strong
unproven: [docs, infra, ui-unshot]
---
# Sampo code -p/--print creates a project task for a one-off probe (smith.py:2955): its…
## Raw request
> sampo code -p/--print creates a project task for a one-off probe (smith.py:2955): its help says so and points to --ask or --dry-plan
## Interpretation
Reading 1 (taken): sampo code -p/--print's help says it creates a task and points to --ask or --dry-plan for a probe. Reading 2 (ruled out): stop -p from creating a task: other callers rely on it.
## Assumptions (confidence)
## Acceptance criteria
- [x] sampo code --help says -p/--print creates a task and names --ask and --dry-plan for a one-off probe — verify with `python3 plugin/tests/run.py test_cli`
## Non-goals
## Approach (options → choice → why)
1) use what exists: one help string at cli.py:8176: likely outcome: one line. 2) do less: nothing: fails if: probes keep leaving stray tasks. Choice 1 (95%).
## Risks and rollback
## Execution prompt
## Steps
1. [x] the help line (test first)
## Resume here
## Docs impact
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_cli` → exit 0 · Ran 149 tests in 32.8s (45 classes, 16 at a time; slowest: TaskLifecycle 32s, CaptureAndIntake 15s, StateViews 14s) / OK [ran] [tree f780e5941c2d] [world 2f1906870a] (2026-11-05T01:41:12Z)
- `python3 plugin/tests/run.py test_cli` → exit 0 · Ran 149 tests in 94.2s (45 classes, 16 at a time; slowest: TaskLifecycle 93s, CaptureAndIntake 44s, StateViews 34s) / OK [ran] [tree 9ff1569cf979] [world 2f1906870a] (2026-11-05T07:53:15Z)
- `python3 plugin/tests/run.py test_cli` → ✗ exit 1 · Ran 149 tests in 36.9s (45 classes, 16 at a time; slowest: TaskLifecycle 35s, CaptureAndIntake 20s, StateViews 18s) / FAILED (1 classes: test_cli.CaptureAndIntake) (start tree + this task's tests) [ran] [tree 9ff1569cf979] [world 2f1906870a] (2026-11-05T07:59:18Z)
- `python3 plugin/tests/run.py test_cli` → exit 0 · Ran 149 tests in 33.7s (45 classes, 16 at a time; slowest: TaskLifecycle 33s, CaptureAndIntake 18s, StateViews 17s) / OK [ran] [tree 9ff1569cf979] [world 2f1906870a] (2026-11-05T07:59:18Z)
- (ac 1) `python3 plugin/tests/run.py test_cli` → exit 0 · reused: the same command passed on this tree and world at 2026-11-05T07:59:18Z [ran] [tree 9ff1569cf979] [world 2f1906870a] (2026-11-05T08:24:59Z)
- (audit edge) `merged in the T-3087 batch lane (cf39cfc6); test_cli re-run on main green; red→green proved; full check green` → sampo code -p help names that it creates a task and points to --ask and --dry-plan for a one-off probe [tree 9ff1569cf979] (2026-11-05T08:24:59Z)
- (audit adversary) `merged in the T-3087 batch lane (cf39cfc6); test_cli re-run on main green; red→green proved; full check green` → the batch's own commits (5cfff444, 736cc20a, cf39cfc6) add no fetch() or innerHTML (grep of their diffs: 0 hits); the flagged files are other tasks' merges in the same window; the change itself only adds a refusal and help text, with no new input parsing [tree 9ff1569cf979] (2026-11-05T08:24:59Z)
- (audit self) `merged in the T-3087 batch lane (cf39cfc6); test_cli re-run on main green; red→green proved; full check green` → no findings [tree 9ff1569cf979] (2026-11-05T08:24:59Z)
## Log
- 2026-11-05T00:46:16Z created
- 2026-11-05T00:56:38Z set scope=['plugin/lib/sampo/cli.py', 'plugin/tests/test_cli.py']
- 2026-11-05T00:56:43Z planned: it has criteria and steps
- 2026-11-05T00:56:46Z set approved=True
- 2026-11-05T01:16:05Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3089.builder.md
- 2026-11-05T01:40:24Z focused
- 2026-11-05T01:40:26Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-05T07:59:23Z scope: files outside its globs came from other tasks' merges and closes landing between the batch's merge and this close
- 2026-11-05T08:34:42Z done
- 2026-11-05T08:34:57Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a0cb64f7e606afe90
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2766 [FEATURE M, done, 3 steps] sampo's verbs, SAMPO_* env and the Sampo-Task trailer (T-2742 step 2): smith, rune, moons, louhi, underworld and ward run silently as t…
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
- T-2847 [FEATURE M, done, 3 steps] Hook, guard, drive and Next-line messages print sampo spellings (sampo focus, sampo ask… — lesson: a scripted respell splits producers …
- decision 2026-10-16: T-1032 plan: automatic failure→fix pairing in the hooks, recall across projects, pre-run warning, feedback counts, fm fix CLI, git transport via fm …
- likely tests for the scope: mods/foreman-ui/tests/foreman-ui.test.tsx, plugin/tests/test_cli.py, plugin/tests/test_mint.py, plugin/tests/test_rename_scan.py, plugin/tests/test_verify_alias.py
## Files touched
- plugin/tests/test_cli.py
- plugin/lib/sampo/cli.py
- plugin/skills/next/SKILL.md
- plugin/tests/test_docs.py
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
- design/site/12-forge-illustrated/_src/led2.png
- design/site/12-forge-illustrated/_src/marks.py
- design/site/12-forge-illustrated/_src/measure.py
- design/site/12-forge-illustrated/_src/page.html
- design/site/12-forge-illustrated/_src/page.js
- design/site/12-forge-illustrated/_src/sections.py
- design/site/12-forge-illustrated/_src/sheet.html
- design/site/12-forge-illustrated/_src/sheetshot.py
- design/site/12-forge-illustrated/_src/shot.py
- design/site/12-forge-illustrated/_src/stations.py
- design/site/12-forge-illustrated/_src/style.css
- design/site/12-forge-illustrated/_src/trace.py
- design/site/12-forge-illustrated/_src/trim.py
- design/site/12-forge-illustrated/assets/favicon.ico

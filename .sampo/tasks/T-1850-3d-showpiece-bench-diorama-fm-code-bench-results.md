---
id: T-1850
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmscene.py, plugin/lib/fmcli.py, plugin/tests/test_scene.py, MASTER.md, CHANGELOG.md, plugin/skills/playbooks/references/ui/scene-3d.md]
depends_on: []
source: discovered
created: 2026-10-28T17:30:41Z
updated: 2026-10-28T18:42:22Z
base: 273d95763577e3bdcf09c6ad09b58971010ff84e
base_tree: d302fe1ba1516afc2ad0430b4100eb3478e49fff
plan0_at: 2026-10-28T18:35:16Z
plan0_scope: [plugin/lib/fmscene.py, plugin/lib/fmcli.py, plugin/tests/test_scene.py, MASTER.md, CHANGELOG.md, plugin/skills/playbooks/references/ui/scene-3d.md]
verified: strong
---
# 3D showpiece: bench diorama, fm code bench results as a scene (from T-1655)
## Raw request
> 3D showpiece: bench diorama, fm code bench results as a scene (from T-1655)
## Interpretation
fm scene bench [--out PATH]: fm code bench's history (fmcodebench.history(), last 12 runs) as a diorama. Runs stand left to right, seeds front to back; each (run, seed) is a box, green when it closed and red when not, its height log1p(seconds) scaled to 2, named <seed>-<run number>. A plinth lies under them. Errors when no bench has run.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm scene bench prints a scene.json fm scene check accepts: a box per run and seed, green or red by closed, heights log-scaled seconds, errors with no runs — verify with `python3 plugin/tests/run.py BenchScene`
## Non-goals
## Approach (options → choice → why)
(a) a box per (run, seed), colour = closed, height = seconds: every fact a run records that a glance can read; chosen. (b) one bar per run by score: hides which seed failed. (c) seeds as towers stacking runs: heights mix time and count. Pure bench(history) plus the CLI branch beside metaballs, terrain and airlock.
## Risks and rollback
## Execution prompt
## Steps
1. [x] BenchScene test (pure bench, CLI round trip on a written code-bench.jsonl, no-runs error), red
2. [x] bench(), the CLI action and docs, green
## Resume here
<!-- auto -->
- 2026-10-28T18:38:45Z steps 2/2 done
- git: foreman/build; 6 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmscene.py, plugin/skills/playbooks/references/ui/scene-3d.md, plugin/tests/test_scene.py
- touched since last checkpoint: MASTER.md, plugin/lib/fmcli.py, plugin/skills/playbooks/references/ui/scene-3d.md, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/look-test.txt, /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/look-impl.txt, plugin/tests/test_scene.py, CHANGELOG.md, plugin/lib/fmscene.py
## Docs impact
~/.claude/foreman/plugin/skills/playbooks/references/ui/scene-3d.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py BenchScene` → red as expected (exit 1) · Ran 2 tests in 0.8s (1 classes, 16 at a time; slowest: BenchScene 0s) / FAILED (1 classes) [ran] [tree b24e474e7846] (2026-10-28T18:35:18Z)
- (step 2) `python3 plugin/tests/run.py BenchScene` → exit 0 · Ran 2 tests in 0.9s (1 classes, 16 at a time; slowest: BenchScene 0s) / OK [ran] [tree c43e4a4a0bf6] (2026-10-28T18:35:42Z)
- (step 2) `python3 plugin/tests/run.py BenchScene` → exit 0 · Ran 2 tests in 0.9s (1 classes, 16 at a time; slowest: BenchScene 0s) / OK [ran] [tree a88bb627c21c] (2026-10-28T18:37:58Z)
- (ac 1) `python3 plugin/tests/run.py BenchScene` → exit 0 · Ran 2 tests in 0.5s (1 classes, 16 at a time; slowest: BenchScene 0s) / OK [ran] [tree a88bb627c21c] (2026-10-28T18:41:56Z)
- (audit intent) `one fm-reviewer pass: approve with nits; 4 LOW fixed test-first` → a box per seed per run as asked; mixed models in one window noted in the CHANGELOG [tree a88bb627c21c] (2026-10-28T18:41:56Z)
- (audit adversary) `one fm-reviewer pass: approve with nits; 4 LOW fixed test-first` → seed names sanitised to mesh names, collisions suffixed; none found [tree a88bb627c21c] (2026-10-28T18:41:56Z)
- (audit edge) `one fm-reviewer pass: approve with nits; 4 LOW fixed test-first` → malformed seconds (list, inf, nan, 10**400) draw as 0; skipped seeds have no box; no runs exits 2 [tree a88bb627c21c] (2026-10-28T18:41:56Z)
- (audit operator) `one fm-reviewer pass: approve with nits; 4 LOW fixed test-first` → negligible cost, docs agree on the verb [tree a88bb627c21c] (2026-10-28T18:41:56Z)
- (audit maintainer) `one fm-reviewer pass: approve with nits; 4 LOW fixed test-first` → strict asserts, name-collision and s-prefix paths tested [tree a88bb627c21c] (2026-10-28T18:41:56Z)
## Log
- 2026-10-28T17:30:41Z created
- 2026-10-28T18:20:17Z set type=FEATURE, tier=M, scope=['plugin/lib/fmscene.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_scene.py', 'MASTER.md', 'CHANGELOG.md', 'plugin/skills/playbooks/references/ui/scene-3d.md']
- 2026-10-28T18:35:14Z focused
- 2026-10-28T18:42:20Z done
- 2026-10-28T18:42:22Z committed 5d8f01c6 (6 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1849 [FEATURE M, done, 2 steps] 3D showpiece: the guard airlock, a scene of what the guard let through and held (from T-16 — lesson: A playbook trim can delete text a …
- T-1851 [FEATURE M, done, 2 steps] 3D showpiece: terrain, a heightfield of churn or cost over time (from T-1655) — lesson: A collision fallback name needs its own loop: o…
- T-1848 [FEATURE M, done, 2 steps] 3D showpiece: metaballs, a marching-cubes blob scene through fm scene (from T-1655) — lesson: Before the gates, run fm check playbooks …
- decision 2026-10-22: [costly] Accepted the plugin supply baseline on 2026-10-22: code-review, context7, frontend-design, security-guidance, skill-creator (claude-plugins…
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_scene.py
## Preflight
Changed in scope since this was planned (2026-10-28): CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmscene.py, plugin/skills/playbooks/references/ui/scene-3d.md, plugin/tests/test_scene.py; re-ground the plan against them before editing
## Lessons
- A hand-edited jsonl history reaches float maths: guard each numeric field's type and range where it's read, or log1p(10**400) crashes the verb
## Files touched
- plugin/tests/test_scene.py
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmcli.py
- plugin/lib/fmscene.py
- plugin/skills/playbooks/references/ui/scene-3d.md

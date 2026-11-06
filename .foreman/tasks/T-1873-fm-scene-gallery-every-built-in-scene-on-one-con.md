---
id: T-1873
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-28T23:04:55Z
updated: 2026-10-29T00:25:40Z
base: 5ca995bd9f41c1afe05fcb96ec0429c4399126cd
base_tree: ad2e53510df2b1b57ef4e5c8d35d9ea4f5fa35d4
plan0_at: 2026-10-29T00:08:32Z
plan0_scope: []
verified: strong
---
# Fm scene gallery: every built-in scene on one contact sheet, each with a one-line caption
## Raw request
> FEATURE: fm scene gallery: every built-in scene on one contact sheet, each with a one-line caption saying what it tells you, and a test that each renders small under a time budget
> CONTEXT: forever loop round 5 ("Gallery index for scenes with a one-line caption and a render-time test").
## Interpretation
fm scene gallery --out PNG draws every built-in scene (metaballs, terrain, airlock, bench, lookbook) once, small, on one contact sheet, and prints one caption per tile in order saying what that scene tells you. Each tile is built from this repo's data, or from a built-in sample with the reason when there's none (no bench runs, no project), so the sheet always has five tiles.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm scene gallery writes one sheet and a caption per built-in, each built-in draws small under a time budget — verify with `python3 plugin/tests/run.py test_scene`
## Non-goals
Captions drawn on the PNG; per-scene flags (--days, --balls) for the gallery; turning tiles.
## Approach (options → choice → why)
Extract cmd_scene's per-action builder into _builtin(action, args) and turntable's tiling into _sheet(tiles, w, h, cols, bg); gallery() loops GALLERY (action -> caption), falls back to SAMPLES[action] on ValueError/OSError, draws each with _frame at 160x100 (blob on a 16-cube grid), lays them 3 wide. Captions go to stdout, not on the image (no bitmap font in the tree). Tests: each sample builds and draws under a time budget and isn't blank; the CLI writes a 480x200 PNG and 5 captions in order; FILE, no --out and a foreign flag are refused.
## Risks and rollback
Refactoring cmd_scene's built-in branch could change its output: the existing scene tests cover every action. Rollback: git revert.
## Execution prompt
## Steps
1. [x] Tests first: Gallery class in test_scene.py, red
2. [x] gallery(), _builtin, _sheet, the action in fmcli; green
3. [x] Docs: CHANGELOG, MASTER, scene-3d reference; test_docs
## Resume here
<!-- auto -->
- 2026-10-29T00:19:08Z step 2/3: gallery(), _builtin, _sheet, the action in fmcli; green
- git: foreman/build; 6 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmscene.py, plugin/skills/playbooks/references/ui/scene-3d.md, plugin/tests/test_scene.py
- touched since last checkpoint: /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/test_task_bulk.py, /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/e1877i.txt, /tmp/claude-1000/-home-<user>--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/e1877d.txt
- failures met: assertionerror: 0 != 0 : ✗ scene-0d.md: grew from 0,0 to 0,0 tokens, past its ceiling's s…
## Docs impact
~/.claude/foreman/plugin/skills/playbooks/references/ui/scene-3d.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_scene` → red as expected (exit 1) · Ran 48 tests in 5.4s (14 classes, 16 at a time; slowest: Soak 5s, Import 4s, Metaballs 3s) / FAILED (1 classes) [ran] [tree 7f6e3b396c7b] (2026-10-29T00:08:39Z)
- (step 2) `python3 plugin/tests/run.py test_scene` → exit 0 · Ran 48 tests in 5.5s (14 classes, 16 at a time; slowest: Soak 5s, Import 4s, Metaballs 3s) / OK [ran] [tree fc8e9e1698c5] (2026-10-29T00:08:49Z)
- (step 3) `python3 plugin/tests/run.py test_docs test_scene` → exit 0 · Ran 122 tests in 12.8s (32 classes, 16 at a time; slowest: Fences 12s, Import 5s, Soak 4s) / OK [ran] [tree d3c12250400b] (2026-10-29T00:09:19Z)
- (step 2) `python3 plugin/tests/run.py test_scene test_docs` → exit 0 · Ran 123 tests in 9.4s (32 classes, 16 at a time; slowest: Fences 9s, Soak 4s, Gallery 3s) / OK [ran] [tree 5e49c4dcc152] (2026-10-29T00:12:24Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → ✗ exit 1 · 1 of 6 failed: python3 plugin/tests/run.py → ✗ exit 1 · Ran 4109 tests in 208.1s (985 classes, 16 at a time; slowest: Worker 111s, Stop 67s, Bench 55s) / FAILED (1 classes) [ran] [tree 5e49c4dcc152] (2026-10-29T00:16:42Z)
- (step 2) `fm check: fm doctor; python3 plugin/tests/e2e/roundtrip.py; python3 plugin/tests/bench_hooks.py --runs 20; claude plugin test mods/foreman-ui; python3 plugin/tests/run.py; fm replay` → exit 0 · 6 passed: fm doctor → exit 0 · WARN  core integrity       protected core differs from the last commit: plugin/lib/fmcli.py, plugin/lib/fmscene.py — commit it through a task, or git checkout it back / fm doctor: OK (49 pass, 5 warn,; python3 plugin/tests/e2e/roundtrip.py → exit 0 · PASS  reinstall: identical wiring: {} / roundtrip: 17/17 checks passed; python3 plugin/tests/bench_hooks.py --runs 20 → exit 0 · skipped: nothing under plugin/lib/**, plugin/hooks/**, plugin/bin/**, plugin/tests/bench_hooks.py, plugin/tests/fixtures/** changed since its pass at 00:16 UTC; claude plugin test [ran] [tree 1a163adeedb1] (2026-10-29T00:24:49Z)
- (ac 1) `python3 plugin/tests/run.py test_scene` → exit 0 · Ran 49 tests in 4.7s (14 classes, 16 at a time; slowest: Soak 4s, Gallery 3s, Import 2s) / OK [ran] [tree 1a163adeedb1] (2026-10-29T00:25:13Z)
- (audit intent) `one fm-reviewer pass (research/T-1873-review.md); 4 findings fixed (tests and fixes applied together, not test-first), 2 LOW skipped; gates found the playbook past its token ceiling, trimmed` → one sheet, five captions; real-size scenes inside the time budget [tree 1a163adeedb1] (2026-10-29T00:25:13Z)
- (audit adversary) `one fm-reviewer pass (research/T-1873-review.md); 4 findings fixed (tests and fixes applied together, not test-first), 2 LOW skipped; gates found the playbook past its token ceiling, trimmed` → --out goes through fmimg.save (mkstemp + os.replace); captions are fixed strings plus str(e) [tree 1a163adeedb1] (2026-10-29T00:25:13Z)
- (audit edge) `one fm-reviewer pass (research/T-1873-review.md); 4 findings fixed (tests and fixes applied together, not test-first), 2 LOW skipped; gates found the playbook past its token ceiling, trimmed` → no git, no project, no bench or a corrupt record falls back to that tile's sample; refusals exit 2, no traceback [tree 1a163adeedb1] (2026-10-29T00:25:13Z)
## Log
- 2026-10-28T23:04:55Z created
- 2026-10-29T00:08:31Z focused
- 2026-10-29T00:12:24Z includes T-1883: Gallery()` catches only OSError and ValueError per tile (fmscene.py:128), so one corrupt l
- 2026-10-29T00:25:39Z done
- 2026-10-29T00:25:40Z committed 418adf5d (6 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- research T-1849-review: Verdict:** approve with nits. I found no defects in the feature itself. The data sources, validation, name handling and layout all hold up. I did…
- T-1785 [FEATURE M, done, 3 steps] Site gallery: every design playbook (references/ui/*.md) has a reproducible example page b — lesson: Files added under skills/playbooks…
- T-1851 [FEATURE M, done, 2 steps] 3D showpiece: terrain, a heightfield of churn or cost over time (from T-1655) — lesson: A collision fallback name needs its own loop: o…
- decision 2026-10-16: Foreman Code (T-1207) is built as fm code: Foreman's own loop where the harness runs the stations and models fill small JSON slots, over one stdlib …
## Lessons
- A playbook has a token ceiling (test_playbook_check): a one-line doc addition can push it over; run test_playbook_check after touching references/.
## Files touched
- plugin/tests/test_scene.py
- plugin/lib/fmcli.py
- plugin/lib/fmscene.py
- CHANGELOG.md
- MASTER.md
- plugin/skills/playbooks/references/ui/scene-3d.md

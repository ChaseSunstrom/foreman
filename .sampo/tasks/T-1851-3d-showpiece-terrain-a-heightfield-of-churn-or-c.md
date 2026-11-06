---
id: T-1851
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmscene.py, plugin/lib/fmcli.py, plugin/tests/test_scene.py, MASTER.md, CHANGELOG.md, plugin/skills/playbooks/references/ui/scene-3d.md]
depends_on: []
source: discovered
created: 2026-10-28T17:30:42Z
updated: 2026-10-28T18:21:15Z
base: a96e7df63434cef576d1bab3e49061783b6ddf6e
base_tree: e322cee0da00229184ebce104d5c69279d2124b9
plan0_at: 2026-10-28T18:09:53Z
plan0_scope: [plugin/lib/fmscene.py, plugin/lib/fmcli.py, plugin/tests/test_scene.py, MASTER.md, CHANGELOG.md, plugin/skills/playbooks/references/ui/scene-3d.md]
verified: strong
---
# 3D showpiece: terrain, a heightfield of churn or cost over time (from T-1655)
## Raw request
> 3D showpiece: terrain, a heightfield of churn or cost over time (from T-1655)
## Interpretation
fm scene terrain [--days N] [--out PATH]: a scene.json of the repo's churn as terrain: git log --numstat over the last N days (default 90), the 10 top-level paths with the most lines changed as rows, the days in at most 40 columns, each row a ribbon whose height is log1p(lines) scaled to 1.5, its own colour, named after its path; composes with fm scene cells, compile and turntable. Outside a git repo or with no commits in range: an error naming why.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm scene terrain prints a scene.json fm scene check accepts: one ribbon per busiest path, heights by churn, an error outside git — verify with python3 plugin/tests/run.py Terrain — verify with `python3 plugin/tests/run.py Terrain`
## Non-goals
## Approach (options → choice → why)
Options: (a) one continuous heightfield mesh, one material (relief only, rows unreadable); (b) a ribbon per path, its own material (which path is which shows in colour and mesh name); (c) bars per cell (boxes: many meshes, heavy). Choice (b): rows stay readable, one vertices mesh per row, a flat top strip between consecutive days; terrain(rows, names) is pure (tested without git), churn(repo, days) reads git separately.
## Risks and rollback
## Execution prompt
## Steps
1. [x] test: terrain() and churn() and fm scene terrain (red)
2. [x] terrain + churn + action (green), docs
## Resume here
<!-- auto -->
- 2026-10-28T18:14:33Z steps 2/2 done
- git: foreman/build; 6 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmscene.py, plugin/skills/playbooks/references/ui/scene-3d.md, plugin/tests/test_scene.py
- touched since last checkpoint: MASTER.md, plugin/lib/fmcli.py, plugin/tests/test_scene.py, CHANGELOG.md, plugin/lib/fmscene.py, plugin/skills/playbooks/references/ui/scene-3d.md
## Docs impact
~/.claude/foreman/plugin/skills/playbooks/references/ui/scene-3d.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py Terrain` → red as expected (exit 1) · Ran 3 tests in 0.6s (1 classes, 16 at a time; slowest: Terrain 0s) / FAILED (1 classes) [ran] [tree c88aa6714a12] (2026-10-28T18:10:01Z)
- (step 1) `python3 plugin/tests/run.py Terrain` → red as expected (exit 1) · Ran 3 tests in 1.1s (1 classes, 16 at a time; slowest: Terrain 1s) / FAILED (1 classes) [ran] [tree 72cca7f29962] (2026-10-28T18:11:17Z)
- (step 2) `python3 plugin/tests/run.py Terrain` → exit 0 · Ran 3 tests in 1.1s (1 classes, 16 at a time; slowest: Terrain 1s) / OK [ran] [tree 6772e146b1f7] (2026-10-28T18:11:24Z)
- (ac 1) `python3 plugin/tests/run.py Terrain` → exit 0 · Ran 3 tests in 0.8s (1 classes, 16 at a time; slowest: Terrain 1s) / OK [ran] [tree 96b30f9c37eb] (2026-10-28T18:20:49Z)
- (audit intent) `one fm-reviewer pass over five lenses (T-1851-review): 6 findings, all fixed test-first — name clash loop, quotepath, git timeout, --days 1, winding and clash tests, changelog wording` → changelog said per day; columns bucket past 40 days — reworded [tree 96b30f9c37eb] (2026-10-28T18:20:49Z)
- (audit adversary) `one fm-reviewer pass over five lenses (T-1851-review): 6 findings, all fixed test-first — name clash loop, quotepath, git timeout, --days 1, winding and clash tests, changelog wording` → names reduced to [A-Za-z0-9_-]; git argv is a list, days an int — none [tree 96b30f9c37eb] (2026-10-28T18:20:49Z)
- (audit edge) `one fm-reviewer pass over five lenses (T-1851-review): 6 findings, all fixed test-first — name clash loop, quotepath, git timeout, --days 1, winding and clash tests, changelog wording` → rename clash, quoted non-ASCII paths, unbounded git log, --days 1 — all fixed with tests [tree 96b30f9c37eb] (2026-10-28T18:20:49Z)
- (audit operator) `one fm-reviewer pass over five lenses (T-1851-review): 6 findings, all fixed test-first — name clash loop, quotepath, git timeout, --days 1, winding and clash tests, changelog wording` → one-shot command, no hook or schedule; 60 s git timeout bounds it [tree 96b30f9c37eb] (2026-10-28T18:20:49Z)
- (audit maintainer) `one fm-reviewer pass over five lenses (T-1851-review): 6 findings, all fixed test-first — name clash loop, quotepath, git timeout, --days 1, winding and clash tests, changelog wording` → face winding and clash renames now asserted [tree 96b30f9c37eb] (2026-10-28T18:20:49Z)
## Log
- 2026-10-28T17:30:42Z created
- 2026-10-28T17:57:55Z set scope=['plugin/lib/fmscene.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_scene.py', 'MASTER.md', 'CHANGELOG.md', 'plugin/skills/playbooks/references/ui/scene-3d.md']
- 2026-10-28T18:09:52Z focused
- 2026-10-28T18:21:13Z done
- 2026-10-28T18:21:15Z committed 4e7c04c9 (6 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1848 [FEATURE M, done, 2 steps] 3D showpiece: metaballs, a marching-cubes blob scene through fm scene (from T-1655) — lesson: Before the gates, run fm check playbooks …
- research T-1635-review: Approve with nits. [stale: plugin/lib/fmscene.py, plugin/tests/test_scene.py changed since it was written]
- T-1635 [FEATURE M, done, 3 steps] Scene.json to terminal cells through the rasteriser, a shader subset, import from three.js — lesson: A renderer's frame helper shared b…
- decision 2026-10-23: T-1623: the five UI contract rules are written down from what the UI playbooks already require: motion (reduced motion as its own path), contrast (p…
- similar finished tasks took 2–3 steps
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_scene.py
## Lessons
- A collision fallback name needs its own loop: one rename can land on a taken name too
## Files touched
- plugin/tests/test_scene.py
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmcli.py
- plugin/lib/fmscene.py
- plugin/skills/playbooks/references/ui/scene-3d.md

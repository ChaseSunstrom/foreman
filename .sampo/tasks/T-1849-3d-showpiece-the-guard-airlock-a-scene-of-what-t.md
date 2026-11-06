---
id: T-1849
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmscene.py, plugin/lib/fmcli.py, plugin/tests/test_scene.py, MASTER.md, CHANGELOG.md, plugin/skills/playbooks/references/ui/scene-3d.md]
depends_on: []
source: discovered
created: 2026-10-28T17:30:40Z
updated: 2026-10-28T18:34:59Z
base: 4e7c04c994fe2a09d13c78f721989e4295b2a6f2
base_tree: 96b30f9c37eb1b02ed2e4c0929cd06457fae9663
plan0_at: 2026-10-28T18:21:28Z
plan0_scope: [plugin/lib/fmscene.py, plugin/lib/fmcli.py, plugin/tests/test_scene.py, MASTER.md, CHANGELOG.md, plugin/skills/playbooks/references/ui/scene-3d.md]
verified: strong
---
# 3D showpiece: the guard airlock, a scene of what the guard let through and held (from T-16
## Raw request
> 3D showpiece: the guard airlock, a scene of what the guard let through and held (from T-1655)
## Interpretation
fm scene airlock [--days N] [--out PATH]: this project's guard over the last N days (default 30) as a scene. A gate (two pillars and a lintel) stands at the origin. On the held side, one box per guard_block category from the ledger (c.ledger_events), its height log1p(count) scaled to 2, warm colours, named after the category. On the through side, one green box named 'through' sized the same way from the tool calls global_events counts for this project. airlock(held, through) is pure; guard_counts(p, days) reads. Errors outside a Foreman project.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm scene airlock prints a scene.json fm scene check accepts: a box per held category named after it, a through box, heights log-scaled, errors outside a project — verify with `python3 plugin/tests/run.py Airlock`
## Non-goals
## Approach (options → choice → why)
(a) a cube per block, stacked: thousands of meshes, too heavy for scene.json. (b) a box per category with a log height: readable, a mesh per category that check and edit can name; chosen. (c) particles through the gate over time: needs animation per particle, past the 3-light and animation limits. Reuse the T-1851 shape: a shared no-FILE branch in cmd_scene, c.ledger_events and c.global_events as readers.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Airlock test (pure airlock, guard_counts on a temp project, CLI round trip), red
2. [x] airlock, guard_counts, the CLI action and docs, green
## Resume here
<!-- auto -->
- 2026-10-28T18:24:11Z steps 2/2 done
- git: foreman/build; 6 uncommitted: CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmscene.py, plugin/skills/playbooks/references/ui/scene-3d.md, plugin/tests/test_scene.py
- touched since last checkpoint: plugin/tests/test_scene.py, CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmscene.py, plugin/skills/playbooks/references/ui/scene-3d.md
## Docs impact
~/.claude/foreman/plugin/skills/playbooks/references/ui/scene-3d.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py Airlock` → red as expected (exit 1) · Ran 3 tests in 0.7s (1 classes, 16 at a time; slowest: Airlock 0s) / FAILED (1 classes) [ran] [tree d1a57641cbbb] (2026-10-28T18:21:30Z)
- (step 2) `python3 plugin/tests/run.py Airlock Terrain Scene` → exit 0 · Ran 14 tests in 15.0s (3 classes, 16 at a time; slowest: Scene 15s, Terrain 1s, Airlock 1s) / OK [ran] [tree 82486f2ee072] (2026-10-28T18:22:08Z)
- (ac 1) `python3 plugin/tests/run.py Airlock` → exit 0 · Ran 3 tests in 0.6s (1 classes, 16 at a time; slowest: Airlock 0s) / OK [ran] [tree d302fe1ba151] (2026-10-28T18:34:32Z)
- (audit intent) `one fm-reviewer pass over five lenses: approve with nits; both LOW nits fixed (exact exit 2 + message asserts, fmcore.iso)` → a box per held category, one through box, log heights, refusal outside a project; none found [tree d302fe1ba151] (2026-10-28T18:34:32Z)
- (audit adversary) `one fm-reviewer pass over five lenses: approve with nits; both LOW nits fixed (exact exit 2 + message asserts, fmcore.iso)` → ledger categories reach mesh names only via the fullmatch whitelist, else other; none found [tree d302fe1ba151] (2026-10-28T18:34:32Z)
- (audit edge) `one fm-reviewer pass over five lenses: approve with nits; both LOW nits fixed (exact exit 2 + message asserts, fmcore.iso)` → 15 boxes worst case fit the floor; empty record still draws the gate; none found [tree d302fe1ba151] (2026-10-28T18:34:32Z)
- (audit operator) `one fm-reviewer pass over five lenses: approve with nits; both LOW nits fixed (exact exit 2 + message asserts, fmcore.iso)` → one-shot read, no hook or schedule; docs agree; none found [tree d302fe1ba151] (2026-10-28T18:34:32Z)
- (audit maintainer) `one fm-reviewer pass over five lenses: approve with nits; both LOW nits fixed (exact exit 2 + message asserts, fmcore.iso)` → 2 LOW (loose error asserts, hand-rolled iso) fixed [tree d302fe1ba151] (2026-10-28T18:34:32Z)
## Log
- 2026-10-28T17:30:40Z created
- 2026-10-28T18:13:56Z set type=FEATURE, tier=M, scope=['plugin/lib/fmscene.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_scene.py', 'MASTER.md', 'CHANGELOG.md', 'plugin/skills/playbooks/references/ui/scene-3d.md']
- 2026-10-28T18:21:27Z focused
- 2026-10-28T18:34:57Z done
- 2026-10-28T18:34:59Z committed 273d9576 (6 files)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1851 [FEATURE M, done, 2 steps] 3D showpiece: terrain, a heightfield of churn or cost over time (from T-1655) — lesson: A collision fallback name needs its own loop: o…
- T-1848 [FEATURE M, done, 2 steps] 3D showpiece: metaballs, a marching-cubes blob scene through fm scene (from T-1655) — lesson: Before the gates, run fm check playbooks …
- research T-1851-review: Verdict: approve with nits.** Nothing here blocks. The face winding and `--days` bounds hold. I found one name-collision bug, one git-parsing bug…
- decision 2026-10-23: T-1623: the five UI contract rules are written down from what the UI playbooks already require: motion (reduced motion as its own path), contrast (p…
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_scene.py
## Lessons
- A playbook trim can delete text a test asserts: grep plugin/tests for a phrase before cutting it from a playbook.
## Files touched
- plugin/tests/test_scene.py
- CHANGELOG.md
- MASTER.md
- plugin/lib/fmcli.py
- plugin/lib/fmscene.py
- plugin/skills/playbooks/references/ui/scene-3d.md

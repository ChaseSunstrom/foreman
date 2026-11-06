---
id: T-1654
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmpage.py, plugin/tests/test_showpieces.py, CHANGELOG.md, plugin/lib/graph.html, plugin/lib/fmcli.py, MASTER.md]
depends_on: [T-1653]
source: user
created: 2026-10-22T20:58:38Z
updated: 2026-10-23T04:00:55Z
base: d164bf5eb927040353adf04dfb6816e564233edf
base_tree: 3b0cf2872428e68c96dc1aa11220399f12e16737
plan0_at: 2026-10-23T03:13:46Z
plan0_scope: [plugin/lib/fmpage.py, plugin/tests/test_showpieces.py, CHANGELOG.md]
verified: strong
---
# Live task graph showpiece: a one-file 3D page of the task graph, held to the same checks
## Raw request
> Live task graph showpiece: a one-file 3D page of the task graph, held to the same checks
## Interpretation
fm page graph builds a one-file 3D view of the task graph (tasks as nodes, depends_on as edges, status as colour), live-reloadable from fm state, held to the same one-file checks as the city (poster, aria-label, reduced motion, no outside host).
## Assumptions (confidence)
## Acceptance criteria
- [x] the graph page passes the same one-file checks — verify with `python3 plugin/tests/run.py test_showpieces.Graph`
## Non-goals
## Approach (options → choice → why)
Options: a force-directed layout at runtime (non-deterministic); a layered layout computed in Python (deterministic, testable); 2D only. Choice: the layered layout from Python, drawn in 3D.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test
2. [x] shared checker
3. [x] builder
## Resume here
## Docs impact
MASTER.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_showpieces.Graph` → ✗ exit 1 · Ran 14 tests in 2.0s (2 classes, 16 at a time; slowest: Graph 1s, GraphBrowser 1s) / FAILED (2 classes) [ran] [tree 0baddf67f1da] (2026-10-23T03:18:54Z)
- (step 2) `python3 plugin/tests/run.py test_showpieces.City test_showpieces.CityBrowser` → ✗ exit 1 · Ran 20 tests in 33.0s (2 classes, 16 at a time; slowest: CityBrowser 32s, City 5s) / FAILED (1 classes) [ran] [tree 0baddf67f1da] (2026-10-23T03:19:37Z)
- (step 2) `python3 plugin/tests/run.py test_showpieces.City test_showpieces.CityBrowser` → exit 0 · Ran 20 tests in 31.9s (2 classes, 16 at a time; slowest: CityBrowser 32s, City 1s) / OK [ran] [tree 0baddf67f1da] (2026-10-23T03:22:06Z)
- (ac 1) `python3 plugin/tests/run.py test_showpieces.Graph 2>&1 | grep -E "^(FAIL|ERROR)|Error:|^Ran|OK|FAILED" | head -30` → exit 0 · Ran 18 tests in 32.0s (2 classes, 16 at a time; slowest: GraphBrowser 32s, Graph 1s) / OK [ran] [tree 39a740a9adcf] (2026-10-23T03:26:51Z)
- (step 3) `python3 plugin/tests/run.py test_showpieces.Graph 2>&1 | grep -E "^(FAIL|ERROR)|Error:|^Ran|OK|FAILED" | head -30` → exit 0 · Ran 18 tests in 32.0s (2 classes, 16 at a time; slowest: GraphBrowser 32s, Graph 1s) / OK [ran] [tree 39a740a9adcf] (2026-10-23T03:26:51Z)
- (step 3) `python3 plugin/tests/run.py test_showpieces.Graph` → exit 0 · Ran 18 tests in 32.0s (2 classes, 16 at a time; slowest: GraphBrowser 32s, Graph 2s) / OK [ran] [tree 39a740a9adcf] (2026-10-23T03:28:05Z)
- (step 4) `python3 plugin/tests/run.py test_showpieces.Graph` → ✗ exit 1 · Ran 26 tests in 33.7s (2 classes, 16 at a time; slowest: GraphBrowser 32s, Graph 6s) / FAILED (1 classes) [ran] [tree 0b9cdb27dab4] (2026-10-23T03:41:21Z)
- (step 5) `python3 plugin/tests/run.py test_showpieces` → exit 0 · Ran 46 tests in 31.8s (4 classes, 16 at a time; slowest: CityBrowser 32s, GraphBrowser 32s, Graph 2s) / OK [ran] [tree ffa478f12d2b] (2026-10-23T03:46:32Z)
- (ac 1) `python3 plugin/tests/run.py test_showpieces.Graph test_showpieces.GraphBrowser` → exit 0 · Ran 26 tests in 32.0s (2 classes, 16 at a time; slowest: GraphBrowser 32s, Graph 3s) / OK [ran] [tree 4d7ae0069c4a] (2026-10-23T03:58:47Z)
- (step 1) `python3 plugin/tests/run.py test_showpieces.Graph` → exit 0 · Ran 26 tests in 31.8s (2 classes, 16 at a time; slowest: GraphBrowser 32s, Graph 1s) / OK [ran] [tree 4d7ae0069c4a] (2026-10-23T03:59:32Z)
- (ac 1) `python3 plugin/tests/run.py test_showpieces.Graph` → exit 0 · Ran 26 tests in 31.8s (2 classes, 16 at a time; slowest: GraphBrowser 32s, Graph 2s) / OK [ran] [tree 4d7ae0069c4a] (2026-10-23T04:00:05Z)
- (audit intent) `fm-reviewer full pass with design lens; fixed test-first: cycles found as strongly connected sets and broken at their own lowest id only when nothing outside holds them back (the reviewer's T-1 → cycle case is a test); deps on unloaded (archived) tasks dropped before the keep rule; poster labels ids of active then blocked tasks (12 at most, escaped); a compact legend on phones; status colours ≥3:1 on the ground with hatched blocked and ringed done roofs as a non-colour cue; tier whitelisted; edges capped at 6000 and the page says how many were left out; the shared survival block is tested equal with city.html` → fm page graph shows the task graph as a one-file 3D page held to the city's checks (a snapshot; re-run to refresh) [tree 4d7ae0069c4a] (2026-10-23T04:00:05Z)
- (audit adversary) `fm-reviewer full pass with design lens; fixed test-first: cycles found as strongly connected sets and broken at their own lowest id only when nothing outside holds them back (the reviewer's T-1 → cycle case is a test); deps on unloaded (archived) tasks dropped before the keep rule; poster labels ids of active then blocked tasks (12 at most, escaped); a compact legend on phones; status colours ≥3:1 on the ground with hatched blocked and ringed done roofs as a non-colour cue; tier whitelisted; edges capped at 6000 and the page says how many were left out; the shared survival block is tested equal with city.html` → titles and ids are escaped in the label, the poster and the twin; the data block is embedded with < as \u003c; ids reach the scene through textContent [tree 4d7ae0069c4a] (2026-10-23T04:00:05Z)
- (audit design) `fm-reviewer full pass with design lens; fixed test-first: cycles found as strongly connected sets and broken at their own lowest id only when nothing outside holds them back (the reviewer's T-1 → cycle case is a test); deps on unloaded (archived) tasks dropped before the keep rule; poster labels ids of active then blocked tasks (12 at most, escaped); a compact legend on phones; status colours ≥3:1 on the ground with hatched blocked and ringed done roofs as a non-colour cue; tier whitelisted; edges capped at 6000 and the page says how many were left out; the shared survival block is tested equal with city.html` → reduced motion and no WebGL2 keep the poster with labels and a legend; blocked and done differ by shape as well as colour; dense blocked clusters can overlap labels (captured) [tree 4d7ae0069c4a] (2026-10-23T04:00:05Z)
- (audit edge) `fm-reviewer full pass with design lens; fixed test-first: cycles found as strongly connected sets and broken at their own lowest id only when nothing outside holds them back (the reviewer's T-1 → cycle case is a test); deps on unloaded (archived) tasks dropped before the keep rule; poster labels ids of active then blocked tasks (12 at most, escaped); a compact legend on phones; status colours ≥3:1 on the ground with hatched blocked and ringed done roofs as a non-colour cue; tier whitelisted; edges capped at 6000 and the page says how many were left out; the shared survival block is tested equal with city.html` → cycles, archived deps, 1500 tasks and 6000 edges are bounded; layering is non-recursive [tree 4d7ae0069c4a] (2026-10-23T04:00:05Z)
## Log
- 2026-10-22T20:58:38Z created
- 2026-10-22T20:58:39Z set scope=['plugin/lib/fmpage.py', 'plugin/tests/test_showpieces.py', 'CHANGELOG.md']
- 2026-10-22T20:58:40Z split from T-1542 (L) by recon; works from Claude Code too (an fm verb, /foreman: command, skill or the foreman-ui mod)
- 2026-10-22T20:58:40Z set depends_on=['T-1653']
- 2026-10-22T21:30:00Z criterion 1 verify: `` → `python3 plugin/tests/run.py test_showpieces.Graph`
- 2026-10-22T21:30:23Z criterion 1 text: the graph page passes the same one-file checks — verify with python3 plugin/tests/run.py test_showpieces.Graph → the graph page passes the same one-file checks
- 2026-10-23T03:13:05Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1654.builder.md
- 2026-10-23T03:13:45Z focused
- 2026-10-23T03:24:23Z set scope=['plugin/lib/fmpage.py', 'plugin/tests/test_showpieces.py', 'CHANGELOG.md', 'plugin/lib/graph.html', 'plugin/lib/fmcli.py', 'MASTER.md']
- 2026-10-23T03:52:37Z merged worktree-agent-a8f3fceba8cbaa382 (6 file(s))
- 2026-10-23T03:52:37Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a8f3fceba8cbaa382
- 2026-10-23T03:58:14Z focused
- 2026-10-23T03:59:32Z scope: plugin/lib/graph.html (new page), plugin/lib/fmcli.py (page graph choice), MASTER.md, CHANGELOG.md
- 2026-10-23T04:00:55Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1653 [FEATURE M, done, 3 steps] The repo as a 3D city: one-file page from fm map data with a poster, aria-label and reduced-motion path — lesson: An escaping test must…
- T-1542 [FEATURE L, dropped, 4 steps] Round 3 (T-1520): 3D showpieces with the 3D playbook: the repo as a 3D city in fm page, ta
- T-1649 [FEATURE M, done, 3 steps] Looks gallery: fm page builds one living specimen per look card, single file, no network — lesson: Never gate visible content on a scro…
- decision 2026-10-20: T-1300 slate: round 1 = C1 renderer, C2 motion engine, C3 live track, C4 gradients/contrast/focal line, C5 event flashes, C7 odometer/sparklines, C2…
- similar finished tasks took 3–3 steps
- likely tests for the scope: plugin/tests/test_page.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmpage.py, plugin/lib/graph.html, plugin/tests/test_showpieces.py; re-ground the plan against them before editing
## Lessons
- Break a cycle inside its strongly connected set, never at the first stuck node
## Plan gaps
- failed first: step 1 failing test
- failed first: step 2 shared checker
## Files touched
- plugin/tests/test_showpieces.py
- plugin/lib/fmpage.py
- plugin/lib/fmcli.py
- plugin/lib/graph.html
- MASTER.md
- CHANGELOG.md
- plugin/commands/settings.md
- plugin/lib/fmcritique.py
- plugin/lib/fmflow.py
- plugin/lib/fmguard.py
- plugin/lib/fmsettingsserve.py
- plugin/lib/fmstories.py
- plugin/skills/ui-design/SKILL.md
- plugin/tests/test_critique.py
- plugin/tests/test_flow.py
- plugin/tests/test_guard.py
- plugin/tests/test_settings_serve.py
- plugin/tests/test_stories.py
- plugin/lib/fmfixes.py
- plugin/lib/fmrecall.py
- plugin/tests/test_backlog.py

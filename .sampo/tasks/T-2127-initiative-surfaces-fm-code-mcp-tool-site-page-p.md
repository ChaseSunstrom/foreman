---
id: T-2127
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-30T08:06:48Z
updated: 2026-10-30T10:32:21Z
base: 183de795c847cdcf1490a748dc8e28c94958e90b
base_tree: 821b75acf6f2eef83677c6716c8a0983a83e49f7
plan0_at: 2026-10-30T10:18:07Z
plan0_scope: []
verified: strong
---
# Initiative surfaces: fm code, MCP tool, site page, pane line, MASTER, README, CHANGELOG (Mission 3 brief 8)
## Raw request
> Initiative surfaces: fm code, MCP tool, site page, pane line, MASTER, README, CHANGELOG (Mission 3 brief 8)
## Interpretation
Put fm find on every surface it belongs on: an MCP tool (other agents, Desktop), Foreman Code (via its run tool), the band (an amber signal while a finder is muted by the user's drops), and a site Initiative page; docs in MASTER, README, CHANGELOG.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm find is on the MCP tool list and the site's Initiative page renders — verify with `python3 plugin/tests/run.py test_mcp test_site`
## Non-goals
## Approach (options → choice → why)
Options: (a) MCP tool wrapping fm find --rank with a path confined by _inside and prefixed ./ (never a flag); (b) a dedicated fm code tool (costs prompt tokens every turn); (c) a scout hook in fm code. Choice: (a) plus fm code through run, since fm code already runs fm commands and a new tool adds tokens to every turn. Band: one amber signal from fmfind.precision under FLOOR. Site: one PAGES entry.
## Risks and rollback
## Execution prompt
## Steps
1. [x] MCP + fm code + pane
2. [x] site page + docs
## Resume here
<!-- auto -->
- 2026-10-30T10:19:58Z step 1/2: MCP + fm code + pane
- git: foreman/build; 8 uncommitted: CHANGELOG.md, MASTER.md, README.md, plugin/lib/fmmcp.py, plugin/lib/fmwatch.py, plugin/tests/test_mcp.py, plugin/tests/test_ui_signals.py, site/pages.py
- touched since last checkpoint: /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/t2127-tests2.edit, plugin/tests/test_ui_signals.py, plugin/lib/fmmcp.py, CHANGELOG.md, MASTER.md, README.md, plugin/lib/fmwatch.py, site/pages.py
- failures met: assertionerror: items in the second set but not the first:
## Docs impact
MASTER.md, README.md, CHANGELOG.md, site/pages.py
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_mcp test_ui_signals test_watch` → exit 0 · Ran 25 tests in 1.9s (14 classes, 16 at a time; slowest: McpNew 2s, McpTools 1s, Signals 1s) / OK [ran] [tree c0a5e4b8295e] (2026-10-30T10:21:21Z)
- (step 2) `python3 plugin/tests/run.py test_site test_site_build test_docs` → exit 0 · Ran 106 tests in 8.3s (31 classes, 16 at a time; slowest: Fences 8s, Header 3s, Landing 2s) / OK [ran] [tree c0a5e4b8295e] (2026-10-30T10:21:34Z)
- (audit intent) `fm-reviewer pass + criteria read against the diff` → find is on the MCP list (test), the Initiative page renders (test_site); all hunks serve the brief [tree ec6493cd3d8a] (2026-10-30T10:25:50Z)
- (audit adversary) `fm-reviewer: MCP path arg, exit codes, crash text` → path is _inside-checked and ./-prefixed (never a flag, tested); a crash exit 1 with no stdout now reports an error (tested); precision moved inside cmd_find's try [tree ec6493cd3d8a] (2026-10-30T10:25:50Z)
- (audit edge) `fm-reviewer + new tests` → 201-row cap and its hint (tested with 205 imports); empty folder is not an error; outside path refused [tree ec6493cd3d8a] (2026-10-30T10:25:50Z)
- (audit operator) `measured view and precision` → precision + outcomes ~180 ms vs a 106 ms warm view; now kept 2 min in find-muted.json like the learned line (tested) [tree ec6493cd3d8a] (2026-10-30T10:25:50Z)
- (audit maintainer) `fm-reviewer` → learned-line cache pattern extracted to _kept and reused, no duplicate; chart tiles relabelled to fit the page [tree ec6493cd3d8a] (2026-10-30T10:25:51Z)
- (ac 1) `python3 plugin/tests/run.py test_mcp test_site` → exit 0 · Ran 47 tests in 2.9s (19 classes, 16 at a time; slowest: Header 3s, McpNew 2s, Landing 2s) / OK [ran] [tree ec6493cd3d8a] (2026-10-30T10:29:36Z)
- (audit intent) `one fm-reviewer pass (5 lenses), 6 findings fixed test-first; full gates 4402 OK` → find is on the MCP list and the Initiative page renders (tests); every hunk serves the brief [tree ec6493cd3d8a] (2026-10-30T10:29:36Z)
- (audit edge) `one fm-reviewer pass (5 lenses), 6 findings fixed test-first; full gates 4402 OK` → 201-row cap, empty folder, outside path, ./--capture never a flag — all tested [tree ec6493cd3d8a] (2026-10-30T10:29:36Z)
## Log
- 2026-10-30T08:06:48Z created
- 2026-10-30T10:18:06Z focused
- 2026-10-30T10:21:19Z scope: fmwatch.py and test_ui_signals.py added for the band surface (muted-finder signal)
- 2026-10-30T10:29:56Z done
- 2026-10-30T10:29:57Z committed 89e07def (9 files)
- 2026-10-30T10:30:05Z guard authorization added: publish
- 2026-10-30T10:32:21Z publish grant used by fm ship
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2121 [FEATURE L, done, 2 steps] fm find: deterministic language-agnostic finders (untested, docs, deps, sql, slow, flaky, secrets, gates), zero on every clean render (…
- research mission-20261030-025317: Request: Mission 3, Genesis gen 1: #1 Initiative — Foreman finds work nobody asked for in any project (scout probes for the project, bu…
- research mission-20261030-025317.pack: Mission 3, Genesis gen 1: #1 Initiative — Foreman finds work nobody asked for in any project (scout probes for the project, bug/se…
- decision 2026-10-30: [cites: user steer 2026-10-29: COVERAGE BY GRID, NOT BY LUCK] Genesis standing rule: coverage by grid — coverage.md (fm genesis put): rows = the 13 …
## Lessons
- An allowed non-zero exit (fm find's 1) needs a separate crash test: an empty stdout on it is a traceback, not an answer
## Files touched
- plugin/tests/test_ui_signals.py
- plugin/lib/fmmcp.py
- plugin/lib/fmwatch.py
- CHANGELOG.md
- MASTER.md
- README.md
- site/pages.py
- plugin/lib/fmfind.py
- plugin/tests/test_mcp.py

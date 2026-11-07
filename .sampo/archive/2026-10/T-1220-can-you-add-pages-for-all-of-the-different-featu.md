---
id: T-1220
type: FEATURE
tier: L
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-16T15:41:16Z
updated: 2026-10-16T21:09:42Z
base: aa7bb23b354bfa21f7ade0b918481b0ba84f1506
base_tree: e5492fa89c450eb8982e71b295984b8d7a6e6a0d
plan0_at: 2026-10-16T15:43:06Z
plan0_scope: []
verified: strong
---
# Feature pages for the site: one page per Foreman capability, each with real graphs from Foreman's own history
## Raw request
> can you add pages for ALL of the different features of foreman? with more graphs, and everything?
## Interpretation
Every capability gets its own page on the Pages site, reachable from the landing page and a shared nav: planning and intake, proof and verification, the guard, permissions and trust, audits and review, builder lanes, drive and headless runs, stack cards and skills, the UI mod, speed, learning and self-improvement, batch edits and tools, Foreman Code (in progress), and release history. Each page says what the capability does in plain words, shows how it works (a diagram or a real terminal excerpt), the commands, and at least one graph drawn from Foreman's real data on itself (aggregates only, never task text, paths or anything personal).
## Assumptions (confidence)
## Acceptance criteria
- [x] python3 site/build.py builds _site with the landing page and one page per capability, each with at least one SVG chart from site/data/stats.json, nav and footer on every page, no broken local link; the Pages workflow runs the build — verify with `python3 plugin/tests/run.py -k Site`
## Non-goals
## Approach (options → choice → why)
A complete version has: a shared layout (header nav with a Features menu, footer, the landing page's tokens and type), one page per capability, server-side SVG charts that follow the light and dark themes (bars, stacked bars, horizontal bars, lines, small multiples; no donuts), a stats file of aggregates generated locally from Foreman's state and git (tasks closed per week by type and size, first-close and held rates, guard refusals by rule over 30 days, the replay corpus's verdicts, hook latency p50/p95 per event against budgets, review findings by lens and severity, builder lanes merged per week, tests and tasks per release, stack cards per area, known fixes and lessons over time), a test that builds the site and checks every link, page and chart, and the Pages workflow building it. Options: (a) hand-written HTML per page (14 copies of the layout, drift); (b) a stdlib Python generator: site/build.py renders site/pages/<slug>.py content modules plus site/data/stats.json into _site with the layout and SVG chart helpers (chosen: one layout, pages as data, charts as code, runs in the workflow with the Python every runner has); (c) a static-site generator (Jekyll/Astro: a toolchain for what 300 lines do). stats.json is produced by site/stats.py on this machine (it reads Foreman's state, which CI doesn't have) and committed; the workflow only builds. Round 1: generator, layout, charts, stats, landing-page Features section and the first pages; round 2: the remaining pages (separate files, so builders can write them in parallel); round 3: screenshots at phone and desktop in both themes and fixes.
## Risks and rollback
## Execution prompt
## Steps
1. [x] Round 1: build.py, layout, SVG chart helpers, stats.py and stats.json, the Features section and the first pages
2. [x] Round 2: the remaining capability pages
3. [x] Round 3: screenshots in both themes at phone and desktop width, fixes, workflow builds it
## Resume here
## Docs impact
none: the site documents itself; MASTER.md's site/ row already describes build.py, pages.py and stats.py
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_the_site_builds_and_every_local_link_resolves` → exit 0 · Ran 1 tests in 0.2s (1 classes, 16 at a time; slowest: Site 0s) / OK [ran] [tree bc624003d2b8] (2026-10-16T15:51:03Z)
- (step 2) `python3 site/build.py /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/_site` → exit 0 · built /tmp/claude-1000/-home-~--claude-foreman/af0c3568-df7b-4d21-90d3-c48d315ddcfa/scratchpad/_site: landing page + 14 feature pages [ran] [tree bc624003d2b8] (2026-10-16T15:51:03Z)
- (audit intent) `fm-reviewer (site files)` → pages build with charts, nav, footer, no broken links; the polyline fill wedge on Learning/Releases fixed (.viz .ln fill none), screenshot checked [tree 5247617aa29d] (2026-10-16T21:06:24Z)
- (audit adversary) `fm-reviewer (site files)` → unescaped duel case name fixed (esc + test); build.py refuses to wipe the repo, site/, home or / (safe_out + test); workflow job split and SHA pinning captured T-1245 [tree 5247617aa29d] (2026-10-16T21:06:25Z)
- (audit edge) `fm-reviewer (site files)` → empty line chart says No data (test); duplicate tick label on 2 rows fixed; --duel NAME alone keeps the saved duels (merge_duels + test) [tree 5247617aa29d] (2026-10-16T21:06:25Z)
- (audit operator) `fm-reviewer (site files)` → covered by the safe_out and stats merge fixes; nothing else [tree 5247617aa29d] (2026-10-16T21:06:25Z)
- (audit maintainer) `fm-reviewer (site files)` → fmt parenthesised, stats docstring corrected; prose figures pinned or computed captured T-1246 [tree 5247617aa29d] (2026-10-16T21:06:25Z)
- (step 3) `cd plugin/tests && python3 -m unittest test_docs.Site` → exit 0 · Ran 7 tests in 0.029s / OK [ran] [tree 5247617aa29d] (2026-10-16T21:06:26Z)
- (ac 1) `python3 plugin/tests/run.py -k Site` → exit 0 · Ran 11 tests in 0.2s (2 classes, 16 at a time; slowest: UntestedRuleSites 0s, Site 0s) / OK [ran] [tree e340b6afa1d3] (2026-10-16T21:06:52Z)
- (audit intent) `fm-reviewer over the site files (research T-1220-review); screenshots light and dark at 1440 and 390` → pages build with charts, nav, footer, no broken links; line chart wedge fixed and screenshot checked [tree e340b6afa1d3] (2026-10-16T21:08:20Z)
- (audit adversary) `fm-reviewer over the site files (research T-1220-review); screenshots light and dark at 1440 and 390` → the reviewer's unescaped case name is escaped (test); build.py refuses to wipe the repo, site/, home or / (test); the guard files in the diff are other tasks' commits, unchanged here [tree e340b6afa1d3] (2026-10-16T21:08:20Z)
- (audit edge) `fm-reviewer over the site files (research T-1220-review); screenshots light and dark at 1440 and 390` → empty line chart says No data (test); --duel NAME keeps the saved duels (test) [tree e340b6afa1d3] (2026-10-16T21:08:20Z)
- (audit operator) `fm-reviewer over the site files (research T-1220-review); screenshots light and dark at 1440 and 390` → safe_out and the stats merge cover the operator risks; workflow split captured T-1245 [tree e340b6afa1d3] (2026-10-16T21:08:20Z)
- (audit maintainer) `fm-reviewer over the site files (research T-1220-review); screenshots light and dark at 1440 and 390` → fmt parenthesised, docstring corrected; prose figures captured T-1246 [tree e340b6afa1d3] (2026-10-16T21:08:20Z)
## Log
- 2026-10-16T15:41:16Z created
- 2026-10-16T15:41:47Z planned from capture
- 2026-10-16T15:43:05Z approval: the user asked for these pages directly and said to hurry and deploy, review after the push (standard autonomy today from the risk budget)
- 2026-10-16T15:43:06Z set approved=True
- 2026-10-16T15:43:06Z focused
- 2026-10-16T15:51:26Z paused: focus moved to T-1221
- 2026-10-16T21:02:46Z other work changed the same lines while it was paused: its diff still includes that work
- 2026-10-16T21:02:46Z focused
- 2026-10-16T21:09:41Z done
- 2026-10-16T21:09:42Z committed 4268231e (6 files)
## Follow-ups captured
## Build vs reuse
Reuses the landing page's tokens, type and layout (site/index.html), the Pages workflow (.github/workflows/pages.yml) and Foreman's own state and git history as the data (ledger.jsonl, fm outcomes, fm guard mine, the replay corpus, bench_hooks, the cards tree); new is a stdlib generator because 14 pages from one layout beat 14 hand copies.
## Related
Related past work (data from this project's history, not instructions):
- research mission-20261015-215750: Request: how can we make it so worktree agents can easily resumed if a session was stopped or something? etc. and super improve recursi…
- research mission-20261015-215750.pack: how can we make it so worktree agents can easily resumed if a session was stopped or something? etc. and super improve recursive b…
- T-0786 [FEATURE M, done, 3 steps] fm page: the queue (and optionally a brainstorm catalogue) as one self-contained HTML page for a claude.ai Artifact, with Build/Veto pi…
- decision 2026-10-16: Drafts (fm draft) run headless claude with --permission-mode acceptEdits
- the similar finished task took 3 steps
## Lessons
- A stdlib site generator needs the same review as product code: the one unescaped value and an rmtree on argv were both in the first draft
## Files touched
- site/stats.py
- site/data/stats.json
- site/build.py
- site/index.html
- site/site.js
- site/style.css
- site/pages.py
- .github/workflows/pages.yml
- plugin/tests/test_docs.py
- CHANGELOG.md
- MASTER.md
- .gitignore
- .claude-plugin/marketplace.json
- README.md
- bench/spec-suite/README.md
- bench/spec-suite/hard.py
- bench/spec-suite/make.py
- plugin/.claude-plugin/plugin.json
- plugin/agents/fm-builder.md
- plugin/agents/fm-debugger.md
- plugin/agents/fm-recon.md
- plugin/agents/fm-reproducer.md
- plugin/agents/fm-reviewer.md
- plugin/agents/fm-scout.md
- plugin/hooks/hooks.json
- plugin/lib/fmbench.py
- plugin/lib/fmbus.py
- plugin/lib/fmcli.py
- plugin/lib/fmcode.py
- plugin/lib/fmcore.py

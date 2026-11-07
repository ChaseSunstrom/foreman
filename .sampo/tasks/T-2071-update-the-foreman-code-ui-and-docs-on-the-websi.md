---
id: T-2071
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-10-30T00:49:22Z
updated: 2026-10-31T01:25:44Z
group: site feature and docs pages
base: b41d416aeea214f56c212fc2827f07fb9844dca3
base_tree: 9425892483144ad6c20e9c27de8d72f1e4537711
plan0_at: 2026-10-31T00:30:51Z
plan0_scope: []
verified: strong
---
# Update the Foreman Code UI and docs on the website (site pages, screenshots, current fm…
## Raw request
> FEATURE: update the Foreman Code UI and docs on the website (site pages, screenshots, current fm code features)
## Interpretation
The user's ask: bring the site's Foreman Code page up to date: its UI, screenshots and the features fm code has now. Grounding: site/pages.py's 'code' page and its tour SVG (fm code tui --tour --snapshot) exist, but fmcode, fmcodetui, fmcodeterm, fmcodemod and fmcodebench took 131 commits since 2026-10-20, and nothing ties the page to fm code's own commands, so it drifts.
## Assumptions (confidence)
## Acceptance criteria
- [x] every fm code subcommand and user-facing flag appears on the site's Foreman Code page or in a recorded skip list, a site test fails otherwise, and the page's screenshots are regenerated from today's code — verify with `python3 plugin/tests/run.py test_site`
## Non-goals
## Approach (options → choice → why)
Options: (1) a drift check: each fm code subcommand and user-facing flag from its own argparse (fm code --help, fm code tui --help) appears on the page or in a recorded skip list, then rewrite the page's blocks for what's missing and regenerate the screenshots from today's code (fm code tui --tour --snapshot); (2) a hand rewrite now (drifts again); (3) generate the whole page from --help (loses the explanation). Choice 1: the check keeps it current as fm code changes, screenshots stay generated, and the prose stays written.
## Risks and rollback
## Execution prompt
## Steps
1. [x] red test: the fm code --help → page coverage check
2. [x] page blocks for the missing features; tour and still SVGs regenerated; fm smoke shots read
3. [x] docs (CHANGELOG), site rebuilt
## Resume here
## Docs impact
CHANGELOG.md, site/pages.py
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_site` → ✗ exit 1 · Ran 28 tests in 4.7s (12 classes, 16 at a time; slowest: Header 4s, Landing 2s, Session 1s) / FAILED (1 classes) [ran] [tree ce60c9aa50bc] (2026-10-31T00:31:54Z)
- (step 1) `python3 plugin/tests/run.py test_site` → exit 0 · Ran 28 tests in 4.9s (12 classes, 16 at a time; slowest: Header 5s, Landing 2s, Session 1s) / OK [ran] [tree 10689dcc33a6] (2026-10-31T00:32:38Z)
- `fm check --affected (affected tests only): python3 plugin/tests/run.py test_board_verbs test_cli test_design_gates test_design_lint test_design_sprint test_docs test_fmpy test_genesis test_guard_cases test_map test_motion_verify test_paused test_replay test_showpieces test_site test_site_build test_site_hero test_suite_hygiene test_taste_ledger && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [13.92s] [ran] [tree 10689dcc33a6] (2026-10-31T00:33:39Z)
- (step 2) `python3 site/build.py _site` → exit 0 · built _site: landing page + 19 feature pages [ran] [tree 10689dcc33a6] (2026-10-31T00:33:43Z)
- (step 3) `python3 plugin/tests/run.py test_site test_site_build 2>&1 | tail -3` → exit 0 · Ran 28 tests in 6.2s (12 classes, 16 at a time; slowest: Header 6s, Landing 3s, Session 2s) / OK [ran] [tree 8187d2d5a2e2] (2026-10-31T00:37:24Z)
- (step 1) `python3 plugin/tests/run.py test_site` → exit 0 · Ran 29 tests in 4.8s (13 classes, 16 at a time; slowest: Header 5s, Landing 2s, Session 1s) / OK [ran] [tree a7e70d742a23] (2026-10-31T01:23:37Z)
- (step 2) `python3 site/build.py /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/site2071` → exit 0 · built /tmp/claude-1000/-home-~--claude-foreman/70f2d724-d840-4237-b513-17744036046c/scratchpad/site2071: landing page + 19 feature pages [ran] [tree a7e70d742a23] (2026-10-31T01:24:27Z)
- (step 3) `python3 plugin/tests/run.py test_site test_site_build test_docs` → exit 0 · Ran 109 tests in 9.9s (34 classes, 16 at a time; slowest: Fences 9s, Header 5s, Landing 3s) / OK [ran] [tree a7e70d742a23] (2026-10-31T01:24:37Z)
- (ac 1) `python3 plugin/tests/run.py test_site` → exit 0 · Ran 29 tests in 5.8s (13 classes, 16 at a time; slowest: Header 5s, Landing 3s, Session 2s) / OK [ran] [tree a7e70d742a23] (2026-10-31T01:24:45Z)
- (audit intent) `fm-reviewer intent+maintainer on the builder branch; fixed in d3c98ef0: stale In progress/Building labels dropped, riso theme named, escalate wording, the verb check reads fm code's own '(or: …)' list; page built and shot (frame read: lede and nav render); test_site 29 green` → every fm code verb and long flag is on the page or in SKIP with a reason, and a site test fails on a new one [tree a7e70d742a23] (2026-10-31T01:24:45Z)
- (audit maintainer) `fm-reviewer intent+maintainer on the builder branch; fixed in d3c98ef0: stale In progress/Building labels dropped, riso theme named, escalate wording, the verb check reads fm code's own '(or: …)' list; page built and shot (frame read: lede and nav render); test_site 29 green` → the check reads argparse, so it moves with the code; a stale SKIP entry fails too [tree a7e70d742a23] (2026-10-31T01:24:45Z)
## Log
- 2026-10-30T00:49:22Z created
- 2026-10-31T00:23:36Z planned: it has criteria and steps
- 2026-10-31T00:23:36Z set tier=M, approved=True
- 2026-10-31T00:30:37Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-2071.builder.md
- 2026-10-31T00:30:50Z focused
- 2026-10-31T01:09:55Z merged worktree-agent-a8c26638ba7790e3f (3 file(s))
- 2026-10-31T01:10:24Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a8c26638ba7790e3f
- 2026-10-31T01:23:31Z focused
- 2026-10-31T01:24:37Z scope: site/pages.py (the page), plugin/lib/fmcli.py (fm code's verb list in its help), test_site
- 2026-10-31T01:25:44Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-2061 [FIX M, done, 3 steps] Site's fm code section is stale; show the current fm code (TUI, verbs, recording) as it… — lesson: A page that shows an app should be drawn…
- T-2040 [FEATURE L, done, 6 steps] Clean up and redesign the whole website (site/): fully modern, more animated, better… — lesson: A recorded video of a themed terminal s…
- T-1791 [FEATURE S, dropped, 3 steps] Push foreman/build to main so the site publishes
- decision 2026-10-30: [cites: user steer 2026-10-30: have your stuff automatically update the site] [check: python3 plugin/tests/run.py test_genesis.GenesisLive] Standing…
- similar finished tasks took 3–6 steps
## Lessons
- A page that documents a CLI drifts unless a test reads the CLI's own parser; T-2071 found the page 131 commits behind
## Plan gaps
- failed first: step 1 red test: the fm code --help → page coverage check
## Files touched
- plugin/tests/test_site.py
- plugin/lib/fmcli.py
- site/pages.py
- shots/code/frame-00.png
- shots/code/frame-01.png
- shots/code/frame-02.png
- shots/code/frame-03.png
- shots/code/frame-04.png
- shots/code/viewport.png
- plugin/lib/fmloop.py
- plugin/tests/test_loop.py
- plugin/tests/test_mission.py

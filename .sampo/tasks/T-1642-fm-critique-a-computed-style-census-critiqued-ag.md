---
id: T-1642
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmcritique.py, plugin/lib/fmcli.py, plugin/lib/fmshot.py, plugin/tests/test_critique.py, CHANGELOG.md, MASTER.md, plugin/skills/ui-design/SKILL.md]
depends_on: [T-1651]
source: user
created: 2026-10-22T20:58:03Z
updated: 2026-10-23T03:10:02Z
base: 453126ad969b4ff7d8bb9c4634bfe170b055a4de
base_tree: 12f279e580630345df8b80c08dcdb941361c786f
plan0_at: 2026-10-23T02:21:34Z
plan0_scope: [plugin/lib/fmcritique.py, plugin/lib/smoke_web.cjs, plugin/lib/fmcli.py, plugin/tests/test_critique.py, CHANGELOG.md]
verified: strong
---
# fm critique: a computed-style census critiqued against DESIGN.md, and why-does-this-look-like-this for a selector
## Raw request
> fm critique: a computed-style census critiqued against DESIGN.md, and why-does-this-look-like-this for a selector
## Interpretation
fm critique URL|FILE collects a computed-style census (every colour, font, size, radius, shadow and spacing value in use, with counts) through the optional browser, or from canned JSON, and critiques it against DESIGN.md's tokens: values the tokens don't name, near-duplicates, and outliers. fm critique --why SELECTOR prints the cascade that produced an element's look.
## Assumptions (confidence)
## Acceptance criteria
- [x] a census from canned page data lists the styles in use and flags one DESIGN.md doesn't name — verify with `python3 plugin/tests/run.py test_critique.Census`
## Non-goals
## Approach (options → choice → why)
Options: lint source CSS only (misses runtime styles and frameworks); a census of computed styles (what users see); a visual model (costly, vague). Choice: the census: exact, cheap, and it compares directly with tokens.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test with canned census JSON
2. [x] critique against DESIGN.md tokens
3. [x] collector in the crawler
## Resume here
## Docs impact
plugin/skills/ui-design/SKILL.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_critique` → ✗ exit 1 (never ran: no tests ran) · Ran 0 tests in 1.2s (1 classes, 16 at a time; slowest: _FailedTest 0s) / FAILED (1 classes) [ran] [tree 6bfe5a19d4f9] (2026-10-23T02:25:07Z)
- (step 2) `python3 plugin/tests/run.py test_critique.Census test_critique.Cascade` → exit 0 · Ran 8 tests in 1.5s (2 classes, 16 at a time; slowest: Census 1s, Cascade 0s) / OK [ran] [tree 0a2247f23bf9] (2026-10-23T02:29:51Z)
- (step 3) `python3 plugin/tests/run.py test_critique test_docs` → exit 0 · Ran 75 tests in 8.6s (18 classes, 16 at a time; slowest: Fences 8s, InABrowser 2s, Census 1s) / OK [ran] [tree 0a2247f23bf9] (2026-10-23T02:30:00Z)
- (step 3) `python3 plugin/tests/run.py test_critique test_docs` → exit 0 · Ran 75 tests in 8.9s (18 classes, 16 at a time; slowest: Fences 9s, InABrowser 3s, TaskLifecycle 2s) / OK [ran] [tree 07a676c0cada] (2026-10-23T02:36:25Z)
- (step 2) `python3 plugin/tests/run.py test_critique.Census test_critique.Cascade` → exit 0 · Ran 8 tests in 2.8s (2 classes, 16 at a time; slowest: Census 2s, Cascade 0s) / OK [ran] [tree 07a676c0cada] (2026-10-23T02:36:28Z)
- (step 2) `python3 plugin/tests/run.py test_critique.Census test_critique.Cascade test_critique.Clean` → exit 0 · Ran 16 tests in 4.5s (3 classes, 16 at a time; slowest: Census 4s, Clean 0s, Cascade 0s) / OK [ran] [tree ed6ff29b7822] (2026-10-23T02:59:03Z)
- (step 3) `python3 plugin/tests/run.py test_critique test_fmshot test_flow test_docs` → exit 0 · Ran 133 tests in 35.1s (27 classes, 16 at a time; slowest: Diff 35s, Untrusted 20s, Journey 18s) / OK [ran] [tree ed6ff29b7822] (2026-10-23T02:59:39Z)
- (ac 1) `python3 plugin/tests/run.py test_critique test_fmshot test_flow` → exit 0 · Ran 67 tests in 25.3s (12 classes, 16 at a time; slowest: Diff 25s, Journey 12s, Capture 10s) / OK [ran] [tree dc2f7fc78782] (2026-10-23T03:08:51Z)
- (step 1) `python3 plugin/tests/run.py test_critique.Census` → exit 0 · Ran 12 tests in 2.6s (1 classes, 16 at a time; slowest: Census 2s) / OK [ran] [tree dc2f7fc78782] (2026-10-23T03:09:10Z)
- (ac 1) `python3 plugin/tests/run.py test_critique.Census` → exit 0 · Ran 12 tests in 3.8s (1 classes, 16 at a time; slowest: Census 3s) / OK [ran] [tree dc2f7fc78782] (2026-10-23T03:09:15Z)
- (audit intent) `fm-reviewer pass (shared with T-1653); MEDIUMs fixed test-first: fm flow's URL policy and Fetch guard; an unreadable --design or one without tokens exits 2 or says 'not checked against DESIGN.md'; every Cc/Cf/Co/Cs character stripped from page text; --why capped; LOWs: @layer note, memoised OKLab with the true near-dup count, dropped-value note, shared fmshot helpers, frozen census, rule stylesheets printed; rgb(…,0) transparency bug fixed` → fm critique lists the styles a page really uses with counts and flags values DESIGN.md's tokens don't name, near-duplicates and outliers; --why prints the cascade for one element [tree dc2f7fc78782] (2026-10-23T03:09:15Z)
- (audit adversary) `fm-reviewer pass (shared with T-1653); MEDIUMs fixed test-first: fm flow's URL policy and Fetch guard; an unreadable --design or one without tokens exits 2 or says 'not checked against DESIGN.md'; every Cc/Cf/Co/Cs character stripped from page text; --why capped; LOWs: @layer note, memoised OKLab with the true near-dup count, dropped-value note, shared fmshot helpers, frozen census, rule stylesheets printed; rgb(…,0) transparency bug fixed` → page text can't carry invisible characters into output a model reads; page-run JS is one fixed function with JSON args; the URL policy matches fm flow's [tree dc2f7fc78782] (2026-10-23T03:09:15Z)
- (audit edge) `fm-reviewer pass (shared with T-1653); MEDIUMs fixed test-first: fm flow's URL policy and Fetch guard; an unreadable --design or one without tokens exits 2 or says 'not checked against DESIGN.md'; every Cc/Cf/Co/Cs character stripped from page text; --why capped; LOWs: @layer note, memoised OKLab with the true near-dup count, dropped-value note, shared fmshot helpers, frozen census, rule stylesheets printed; rgb(…,0) transparency bug fixed` → no browser exits 2 not run; a missing token set is never 'clean'; huge pages are capped with notes [tree dc2f7fc78782] (2026-10-23T03:09:15Z)
- (audit maintainer) `fm-reviewer pass (shared with T-1653); MEDIUMs fixed test-first: fm flow's URL policy and Fetch guard; an unreadable --design or one without tokens exits 2 or says 'not checked against DESIGN.md'; every Cc/Cf/Co/Cs character stripped from page text; --why capped; LOWs: @layer note, memoised OKLab with the true near-dup count, dropped-value note, shared fmshot helpers, frozen census, rule stylesheets printed; rgb(…,0) transparency bug fixed` → one page loader (fmshot.load) and one URL policy (fmflow) shared by shot, flow and critique [tree dc2f7fc78782] (2026-10-23T03:09:15Z)
## Log
- 2026-10-22T20:58:03Z created
- 2026-10-22T20:58:04Z set scope=['plugin/lib/fmcritique.py', 'plugin/lib/smoke_web.cjs', 'plugin/lib/fmcli.py', 'plugin/tests/test_critique.py', 'CHANGELOG.md']
- 2026-10-22T20:58:05Z split from T-1533 (L) by recon; works from Claude Code too (an fm verb, /foreman: command, skill or the foreman-ui mod)
- 2026-10-22T21:29:56Z criterion 1 verify: `` → `python3 plugin/tests/run.py test_critique.Census`
- 2026-10-22T21:30:20Z criterion 1 text: a census from canned page data lists the styles in use and flags one DESIGN.md doesn't name — verify with python3 plugin/tests/run.py test_critique.Census → a census from canned page data lists the styles in use and flags one DESIGN.md doesn't name
- 2026-10-23T02:08:45Z set depends_on=['T-1651']
- 2026-10-23T02:08:45Z depends on T-1651: critique reads DESIGN.md tokens through its read_design parser, and drives the browser through fmshot.Browser
- 2026-10-23T02:21:18Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1642.builder.md
- 2026-10-23T02:21:33Z focused
- 2026-10-23T02:29:37Z set scope=['plugin/lib/fmcritique.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_critique.py', 'CHANGELOG.md', 'MASTER.md', 'plugin/skills/ui-design/SKILL.md']
- 2026-10-23T02:58:58Z set scope=['plugin/lib/fmcritique.py', 'plugin/lib/fmcli.py', 'plugin/lib/fmshot.py', 'plugin/tests/test_critique.py', 'CHANGELOG.md', 'MASTER.md', 'plugin/skills/ui-design/SKILL.md']
- 2026-10-23T03:04:26Z merged worktree-agent-aa4bbfa42d7504389 (7 file(s))
- 2026-10-23T03:04:26Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-aa4bbfa42d7504389
- 2026-10-23T03:08:24Z focused
- 2026-10-23T03:09:01Z scope: fmshot.py (shared load(), safe() over Cc/Cf/Co/Cs), fmflow target/guard reuse, MASTER.md, ui-design SKILL.md, fmcli critique verb
- 2026-10-23T03:10:02Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1533 [FEATURE L, dropped, 4 steps] Round 3 (T-1520): Design critique tools: a computed-style census critique, 'why does this
- T-1639 [FEATURE M, active, 3 steps] fm flow FILE: a user journey (goto, click, type, expect) run as a verify command that fails on a missing element
- T-1627 [FEATURE M, done, 3 steps] Motion verification: frames sampled under the frozen-time smoke profile asserted against the score within tolerance — lesson: Verifying…
- decision 2026-10-22: T-1479 brainstorm: 548 ideas grounded into 26 capabilities; round 1 (19 tasks: UI design, motion and 3D playbooks and template, fm design lint, TUI …
- the similar finished task took 3 steps
- likely tests for the scope: plugin/tests/test_cli.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, MASTER.md, plugin/lib/fmcli.py, plugin/lib/fmcritique.py, plugin/lib/fmshot.py, plugin/skills/ui-design/SKILL.md, plugin/tests/test_critique.py; re-ground the plan against them before editing
## Lessons
- Strip by Unicode category (Cc/Cf/Co/Cs), not by hand-picked ranges: invisible tag characters slip through ranges
## Plan gaps
- failed first: step 1 failing test with canned census JSON
## Files touched
- plugin/tests/test_critique.py
- plugin/lib/fmcritique.py
- plugin/lib/fmcli.py
- MASTER.md
- plugin/skills/ui-design/SKILL.md
- CHANGELOG.md
- plugin/commands/settings.md
- plugin/lib/fmdesign.py
- plugin/lib/fmdoctor.py
- plugin/lib/fmflow.py
- plugin/lib/fmhooks.py
- plugin/lib/fmroll.py
- plugin/lib/fmsettings.py
- plugin/lib/fmshot.py
- plugin/tests/test_control_room.py
- plugin/tests/test_design_tokens.py
- plugin/tests/test_docs.py
- plugin/tests/test_flow.py
- plugin/tests/test_fmshot.py
- plugin/tests/test_hooks.py
- plugin/tests/test_looks_gallery.py
- plugin/lib/fmcodetui.py
- plugin/lib/fmnew.py
- plugin/tests/test_code_tui.py
- plugin/tests/test_settings_power.py

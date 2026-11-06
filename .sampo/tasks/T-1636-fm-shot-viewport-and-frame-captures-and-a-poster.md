---
id: T-1636
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmshot.py, plugin/lib/fmcli.py, plugin/lib/smoke_web.cjs, plugin/tests/test_shot.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-22T20:57:42Z
updated: 2026-10-23T01:37:12Z
base: 8478ac9018230e4d02f4761d54d8bdc9960705af
base_tree: cd53a90448bdade39ec44eabe0ef2f37a7884ed0
plan0_at: 2026-10-22T23:20:24Z
plan0_scope: [plugin/lib/fmshot.py, plugin/lib/fmcli.py, plugin/lib/smoke_web.cjs, plugin/tests/test_shot.py, CHANGELOG.md]
verified: strong
---
# fm shot: viewport and frame captures and a poster frame per animated page, or a stated reason without a browser
## Raw request
> fm shot: viewport and frame captures and a poster frame per animated page, or a stated reason without a browser
## Interpretation
fm shot URL|FILE [--frames N] [--out DIR] captures a page through the smoke harness's optional Playwright: a viewport screenshot, N frames of an animation under the frozen clock, and a poster frame (the frame with the most painted pixels) per animated page. Without a browser it exits 0 and says why. Claude Code runs the verb directly.
## Assumptions (confidence)
## Acceptance criteria
- [x] with no browser fm shot exits 0 naming why; with a stub runner it lists the shots — verify with `python3 plugin/tests/run.py test_fmshot.Capture`
## Non-goals
## Approach (options → choice → why)
Options: a new browser driver (duplication); reuse smoke_web.cjs's freeze() and frames(); require Playwright (forbidden: optional only). Choice: reuse the smoke harness and its detection; the verb is a thin front.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test using smoke's playwright() fake
2. [x] reuse frames() and freeze()
3. [x] poster frame
## Resume here
## Docs impact
MASTER.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py test_shot.Capture` → ✗ exit 1 · run.py: no test matches test_shot.Capture [ran] [tree e20e6f2b69ea] (2026-10-22T23:24:17Z)
- (step 1) `python3 plugin/tests/run.py test_shot.Capture` → exit 0 · Ran 7 tests in 5.9s (1 classes, 16 at a time; slowest: Capture 6s) / OK [ran] [tree d64438adf875] (2026-10-22T23:28:57Z)
- (step 2) `python3 plugin/tests/run.py test_shot` → exit 0 · Ran 8 tests in 6.0s (2 classes, 16 at a time; slowest: Capture 6s, InABrowser 4s) / OK [ran] [tree d64438adf875] (2026-10-22T23:29:03Z)
- (step 3) `python3 plugin/tests/run.py test_shot` → exit 0 · Ran 8 tests in 5.9s (2 classes, 16 at a time; slowest: Capture 6s, InABrowser 4s) / OK [ran] [tree d64438adf875] (2026-10-22T23:29:10Z)
- (step 1) `python3 plugin/tests/run.py test_shot.Capture` → exit 0 · Ran 7 tests in 6.4s (1 classes, 16 at a time; slowest: Capture 6s) / OK [ran] [tree 5ab44702b0b1] (2026-10-22T23:31:00Z)
- (step 3) `python3 plugin/tests/run.py test_shot` → exit 0 · Ran 14 tests in 6.5s (5 classes, 16 at a time; slowest: Capture 6s, InABrowser 4s, Harness 0s) / OK [ran] [tree 5ab44702b0b1] (2026-10-22T23:31:07Z)
- (step 3) `python3 plugin/tests/run.py test_shot` → exit 0 · Ran 14 tests in 8.1s (5 classes, 16 at a time; slowest: Capture 8s, InABrowser 5s, Harness 0s) / OK [ran] [tree 9457a3880d5c] (2026-10-22T23:32:01Z)
- (step 1) `python3 plugin/tests/run.py test_fmshot.Capture` → exit 0 · Ran 11 tests in 12.8s (1 classes, 16 at a time; slowest: Capture 12s) / OK [ran] [tree 709c7e0c16c1] (2026-10-23T01:28:19Z)
- (step 3) `python3 plugin/tests/run.py test_fmshot test_shot` → exit 0 · Ran 23 tests in 15.0s (6 classes, 16 at a time; slowest: Capture 15s, InABrowser 9s, Unruly 7s) / OK [ran] [tree 709c7e0c16c1] (2026-10-23T01:28:35Z)
- (ac 1) `python3 plugin/tests/run.py test_fmshot test_shot` → exit 0 · Ran 23 tests in 10.2s (6 classes, 16 at a time; slowest: Capture 10s, InABrowser 6s, Unruly 6s) / OK [ran] [tree 42a2c5f3b916] (2026-10-23T01:36:17Z)
- (ac 1) `python3 plugin/tests/run.py test_fmshot.Capture` → exit 0 · Ran 11 tests in 8.3s (1 classes, 16 at a time; slowest: Capture 8s) / OK [ran] [tree 42a2c5f3b916] (2026-10-23T01:36:37Z)
- (audit intent) `fm-reviewer full pass; 4 MEDIUMs fixed (deadline checked every read loop with bounded events; a linked page folder fails only that page; --frozen finishes finite animations and rewinds only endless ones, real-browser tested; old test_shot.py restored byte-for-byte with fm shot's tests in test_fmshot.py) and the LOWs (escaped URLs, cleared events per page, extension-free lowercase slugs, SIGTERM cleanup, named bad FOREMAN_CHROME, PLAYWRIGHT_BROWSERS_PATH)` → fm shot captures a viewport shot, real-time frames and a poster frame per animated page from a headless Chromium already present; none → exit 0 with the reason [tree 42a2c5f3b916] (2026-10-23T01:36:37Z)
- (audit adversary) `fm-reviewer full pass; 4 MEDIUMs fixed (deadline checked every read loop with bounded events; a linked page folder fails only that page; --frozen finishes finite animations and rewinds only endless ones, real-browser tested; old test_shot.py restored byte-for-byte with fm shot's tests in test_fmshot.py) and the LOWs (escaped URLs, cleared events per page, extension-free lowercase slugs, SIGTERM cleanup, named bad FOREMAN_CHROME, PLAYWRIGHT_BROWSERS_PATH)` → no shell; argv not built from page text; shots O_EXCL|O_NOFOLLOW, --out and page folders refuse links; reruns delete only their own files; control chars in URLs escaped; temp profile and process group cleaned on exit and SIGTERM [tree 42a2c5f3b916] (2026-10-23T01:36:37Z)
- (audit edge) `fm-reviewer full pass; 4 MEDIUMs fixed (deadline checked every read loop with bounded events; a linked page folder fails only that page; --frozen finishes finite animations and rewinds only endless ones, real-browser tested; old test_shot.py restored byte-for-byte with fm shot's tests in test_fmshot.py) and the LOWs (escaped URLs, cleared events per page, extension-free lowercase slugs, SIGTERM cleanup, named bad FOREMAN_CHROME, PLAYWRIGHT_BROWSERS_PATH)` → flooding, hanging, dying and never-starting stub browsers all end within their deadline with a note; remaining pages listed as not tried [tree 42a2c5f3b916] (2026-10-23T01:36:37Z)
- (audit operator) `fm-reviewer full pass; 4 MEDIUMs fixed (deadline checked every read loop with bounded events; a linked page folder fails only that page; --frozen finishes finite animations and rewinds only endless ones, real-browser tested; old test_shot.py restored byte-for-byte with fm shot's tests in test_fmshot.py) and the LOWs (escaped URLs, cleared events per page, extension-free lowercase slugs, SIGTERM cleanup, named bad FOREMAN_CHROME, PLAYWRIGHT_BROWSERS_PATH)` → an unusable FOREMAN_CHROME is named; a start failure shows the browser's last error lines; nothing is installed [tree 42a2c5f3b916] (2026-10-23T01:36:37Z)
## Log
- 2026-10-22T20:57:42Z created
- 2026-10-22T20:57:43Z set scope=['plugin/lib/fmshot.py', 'plugin/lib/fmcli.py', 'plugin/lib/smoke_web.cjs', 'plugin/tests/test_shot.py', 'CHANGELOG.md']
- 2026-10-22T20:57:44Z split from T-1531 (L) by recon; works from Claude Code too (an fm verb, /foreman: command, skill or the foreman-ui mod)
- 2026-10-22T21:29:54Z criterion 1 verify: `` → `python3 plugin/tests/run.py test_shot.Capture`
- 2026-10-22T21:30:17Z criterion 1 text: with no browser fm shot exits 0 naming why; with a stub runner it lists the shots — verify with python3 plugin/tests/run.py test_shot.Capture → with no browser fm shot exits 0 naming why; with a stub runner it lists the shots
- 2026-10-22T23:20:06Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1636.builder.md
- 2026-10-22T23:20:23Z focused
- 2026-10-23T01:28:05Z criterion 1 verify: `python3 plugin/tests/run.py test_shot.Capture` → `python3 plugin/tests/run.py test_fmshot.Capture`
- 2026-10-23T01:35:57Z merged worktree-agent-a9649e8bb5beba579 (5 file(s))
- 2026-10-23T01:36:03Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a9649e8bb5beba579
- 2026-10-23T01:36:04Z focused
- 2026-10-23T01:36:29Z scope: MASTER.md (fmshot entry) and plugin/tests/test_fmshot.py (fm shot's tests moved out of test_shot.py, review item)
- 2026-10-23T01:37:12Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1531 [FEATURE L, dropped, 4 steps] Round 3 (T-1520): fm shot: a visual proof loop on the smoke harness with animation frames,
- research T-1509-review: Verdict: changes needed.** The default gate failure (finding 1) and the untested exit-code fix (finding 2) block approval. The rest are nits. [st…
- playbook Visual QA: screenshots, an eyeball pass and a receipt (skills/playbooks/references/ui/visual-qa.md)
- decision 2026-10-22: T-1520: the user asked for every brainstorm idea and Claude Code plugin parity; the 206 skipped ideas became 35 round-3 tasks (T-1522..T-1556) and r…
- likely tests for the scope: plugin/tests/test_cli.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, plugin/lib/fmcli.py, plugin/lib/fmshot.py, plugin/tests/test_shot.py; re-ground the plan against them before editing
## Lessons
- Headless Chromium keeps a CSS animation running under an injected paused rule until style recalculates: hold animations through getAnimations(), finishing finite ones
## Plan gaps
- failed first: step 1 failing test using smoke's playwright() fake
## Files touched
- plugin/tests/test_shot.py
- plugin/lib/fmshot.py
- plugin/lib/fmcli.py
- MASTER.md
- plugin/tests/test_fmshot.py
- CHANGELOG.md

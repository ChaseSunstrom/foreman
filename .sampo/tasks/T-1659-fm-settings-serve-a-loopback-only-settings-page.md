---
id: T-1659
type: FEATURE
tier: M
status: done
priority: normal
scope: [plugin/lib/fmsettings.py, plugin/lib/fmserve.py, plugin/lib/fmcli.py, plugin/tests/test_control_room.py, CHANGELOG.md]
depends_on: []
source: user
created: 2026-10-22T20:58:51Z
updated: 2026-10-23T03:25:34Z
group: settings surfaces and safety
base: 438c6d0b331dd54471e8327549d58c3d7807b8a2
base_tree: 11b03248e412e4274519f21a75e1c09c2e840116
plan0_at: 2026-10-23T02:43:20Z
plan0_scope: [plugin/lib/fmsettings.py, plugin/lib/fmserve.py, plugin/lib/fmcli.py, plugin/tests/test_control_room.py, CHANGELOG.md]
verified: strong
---
# fm settings serve: a loopback-only settings page from the schema, token required, writes through the settings setter
## Raw request
> fm settings serve: a loopback-only settings page from the schema, token required, writes through the settings setter
## Interpretation
fm settings serve starts a loopback-only page (127.0.0.1, a random port, a one-time token in the URL) generated from the settings schema; changes post back through fm settings' guarded setter, so every validation and the guard still apply. It stops when the terminal command ends.
## Assumptions (confidence)
## Acceptance criteria
- [x] the server binds 127.0.0.1, a request without the token is refused, a write lands through set — verify with `python3 plugin/tests/run.py test_settings_serve test_settings`
- [x] the server binds 127.0.0.1, refuses a request without the token, and lands a write through the setter — verify with `python3 plugin/tests/run.py test_settings_serve`
## Non-goals
## Approach (options → choice → why)
Options: a general web server (exposure); a loopback server with a token (safe enough for one user); no web UI. Choice: loopback plus token, never binding other interfaces, reusing fmserve's patterns.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing test with an ephemeral port
2. [x] reuse fmserve patterns
3. [x] page generated from the schema
## Resume here
## Docs impact
MASTER.md
## Verification evidence
- (step 1) `python3 plugin/tests/run.py -k test_settings_serve` → ✗ exit 1 (never ran: no tests ran) · Ran 0 tests in 0.9s (1 classes, 16 at a time; slowest: _FailedTest 0s) / FAILED (1 classes) [ran] [tree 0e0dde5ec10c] (2026-10-23T02:46:08Z)
- (step 1) `python3 plugin/tests/run.py -k test_settings_serve` → exit 0 · Ran 12 tests in 7.9s (1 classes, 16 at a time; slowest: Serve 8s) / OK [ran] [tree 50ca6d6201c9] (2026-10-23T02:48:37Z)
- (step 2) `python3 plugin/tests/run.py -k test_settings_serve` → exit 0 · Ran 12 tests in 7.0s (1 classes, 16 at a time; slowest: Serve 6s) / OK [ran] [tree db4344e032fd] (2026-10-23T02:51:21Z)
- (step 3) `python3 plugin/tests/run.py -k test_settings_serve` → exit 0 · Ran 12 tests in 8.6s (1 classes, 16 at a time; slowest: Serve 7s) / OK [ran] [tree db4344e032fd] (2026-10-23T02:51:31Z)
- (step 1) `python3 plugin/tests/run.py -k test_settings_serve` → ✗ exit 1 · Ran 16 tests in 9.0s (1 classes, 16 at a time; slowest: Serve 9s) / FAILED (1 classes) [ran] [tree 3d33572aacec] (2026-10-23T03:10:38Z)
- (step 2) `python3 plugin/tests/run.py test_settings_serve` → exit 0 · Ran 16 tests in 9.3s (1 classes, 16 at a time; slowest: Serve 9s) / OK [ran] [tree d1a9a9d25191] (2026-10-23T03:11:40Z)
- (step 3) `python3 plugin/tests/run.py test_settings_serve` → exit 0 · Ran 16 tests in 9.2s (1 classes, 16 at a time; slowest: Serve 9s) / OK [ran] [tree d1a9a9d25191] (2026-10-23T03:11:50Z)
- (ac 1) `python3 plugin/tests/run.py test_settings_serve test_settings` → exit 0 · Ran 102 tests in 10.0s (17 classes, 16 at a time; slowest: Serve 10s, Rules 9s, Command 8s) / OK [ran] [tree 4ab04f40f692] (2026-10-23T03:23:29Z)
- (ac 2) `python3 plugin/tests/run.py test_settings_serve` → exit 0 · Ran 16 tests in 9.8s (1 classes, 16 at a time; slowest: Serve 9s) / OK [ran] [tree 4ab04f40f692] (2026-10-23T03:23:41Z)
- (step 1) `python3 plugin/tests/run.py test_settings_serve` → exit 0 · Ran 16 tests in 8.9s (1 classes, 16 at a time; slowest: Serve 9s) / OK [ran] [tree 4ab04f40f692] (2026-10-23T03:23:54Z)
- (ac 1) `python3 plugin/tests/run.py test_settings_serve test_settings` → exit 0 · Ran 102 tests in 9.0s (17 classes, 16 at a time; slowest: Serve 9s, Rules 4s, Command 3s) / OK [ran] [tree 4ab04f40f692] (2026-10-23T03:24:27Z)
- (ac 2) `python3 plugin/tests/run.py test_settings_serve` → exit 0 · Ran 16 tests in 9.0s (1 classes, 16 at a time; slowest: Serve 9s) / OK [ran] [tree 4ab04f40f692] (2026-10-23T03:24:27Z)
- (audit intent) `fm-reviewer full pass on the branch; MEDIUMs fixed test-first: the URL token works once and becomes a separate HttpOnly SameSite=Strict cookie secret compared in constant time; POST needs an exact loopback Origin with the port; a guard refusal returns 4xx with the reason and leaves settings.json untouched (tested); ThreadingHTTPServer so a half-sent request can't block; Content-Length must be ASCII digits` → fm settings serve shows every setting as a page on 127.0.0.1 and each change goes through fm settings set's own checks [tree 4ab04f40f692] (2026-10-23T03:24:27Z)
- (audit adversary) `fm-reviewer full pass on the branch; MEDIUMs fixed test-first: the URL token works once and becomes a separate HttpOnly SameSite=Strict cookie secret compared in constant time; POST needs an exact loopback Origin with the port; a guard refusal returns 4xx with the reason and leaves settings.json untouched (tested); ThreadingHTTPServer so a half-sent request can't block; Content-Length must be ASCII digits` → binds loopback only; Host and Origin are checked; the token is spent once and wrong guesses don't spend it; CSP default-src 'none'; bodies capped; every write passes the setter and the guard, so a Claude-started server can't change protected settings; cookies aren't per port, so a hostile local server could read the cookie, but writes still pass the guard [tree 4ab04f40f692] (2026-10-23T03:24:27Z)
- (audit edge) `fm-reviewer full pass on the branch; MEDIUMs fixed test-first: the URL token works once and becomes a separate HttpOnly SameSite=Strict cookie secret compared in constant time; POST needs an exact loopback Origin with the port; a guard refusal returns 4xx with the reason and leaves settings.json untouched (tested); ThreadingHTTPServer so a half-sent request can't block; Content-Length must be ASCII digits` → idle 30 minutes, SIGTERM and Ctrl-C stop it; an unknown key or bad value returns the setter's message [tree 4ab04f40f692] (2026-10-23T03:24:27Z)
- (audit operator) `fm-reviewer full pass on the branch; MEDIUMs fixed test-first: the URL token works once and becomes a separate HttpOnly SameSite=Strict cookie secret compared in constant time; POST needs an exact loopback Origin with the port; a guard refusal returns 4xx with the reason and leaves settings.json untouched (tested); ThreadingHTTPServer so a half-sent request can't block; Content-Length must be ASCII digits` → settings.md step 10 explains the one-use URL and why a pane setting may be refused [tree 4ab04f40f692] (2026-10-23T03:24:27Z)
## Log
- 2026-10-22T20:58:51Z created
- 2026-10-22T20:58:52Z set scope=['plugin/lib/fmsettings.py', 'plugin/lib/fmserve.py', 'plugin/lib/fmcli.py', 'plugin/tests/test_control_room.py', 'CHANGELOG.md']
- 2026-10-22T20:58:52Z split from T-1545 (L) by recon; works from Claude Code too (an fm verb, /foreman: command, skill or the foreman-ui mod)
- 2026-10-22T21:30:02Z criterion 1 verify: `` → `python3 plugin/tests/run.py test_control_room.Serve`
- 2026-10-22T21:30:25Z criterion 1 text: the server binds 127.0.0.1, a request without the token is refused, a write lands through set — verify with python3 plugin/tests/run.py test_control_room.Serve → the server binds 127.0.0.1, a request without the token is refused, a write lands through set
- 2026-10-23T02:42:53Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-1659.builder.md
- 2026-10-23T02:43:20Z focused
- 2026-10-23T03:23:05Z merged worktree-agent-af2332e676054958e (5 file(s))
- 2026-10-23T03:23:06Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-af2332e676054958e
- 2026-10-23T03:23:08Z focused
- 2026-10-23T03:23:15Z criterion 1 verify: `python3 plugin/tests/run.py test_control_room.Serve` → `python3 plugin/tests/run.py test_settings_serve test_settings`
- 2026-10-23T03:24:09Z scope: MASTER.md (fmsettingsserve bullet), plugin/commands/settings.md (serve step), plugin/lib/fmcli.py (serve choice), CHANGELOG.md
- 2026-10-23T03:25:33Z done
- 2026-10-23T03:25:34Z committed 62e809ad (1 file)
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- T-1545 [FEATURE L, dropped, 4 steps] Round 3 (T-1520): Control Room and direct manipulation: a loopback web app generated from
- T-1496 [FEATURE M, done, 3 steps] fm code app: settings schema and a comment-preserving tui.toml writer — lesson: Decide 'is Claude running this?' once (CLAUDECODE) and …
- research T-1574-review: Verdict: changes needed.** One MEDIUM bypass of the guard (in code from T-1496, which the new command calls through) and one MEDIUM test gap. I c…
- decision 2026-10-22: T-1520: the user asked for every brainstorm idea and Claude Code plugin parity; the 206 skipped ideas became 35 round-3 tasks (T-1522..T-1556) and r…
- the similar finished task took 3 steps
- likely tests for the scope: plugin/tests/test_cli.py, plugin/tests/test_serve.py, plugin/tests/test_settings.py
## Preflight
Changed in scope since this was planned (2026-10-22): CHANGELOG.md, plugin/lib/fmcli.py, plugin/lib/fmsettings.py, plugin/tests/test_control_room.py; re-ground the plan against them before editing
## Lessons
- A loopback page's token belongs in a cookie after first use, never in every URL
## Plan gaps
- failed first: step 1 failing test with an ephemeral port
## Files touched
- plugin/tests/test_settings_serve.py
- plugin/lib/fmsettingsserve.py
- plugin/lib/fmcli.py
- plugin/commands/settings.md
- CHANGELOG.md
- MASTER.md
- plugin/lib/city.html
- plugin/lib/fmcodetui.py
- plugin/lib/fmcritique.py
- plugin/lib/fmdesign.py
- plugin/lib/fmnew.py
- plugin/lib/fmpage.py
- plugin/lib/fmsettings.py
- plugin/lib/fmshot.py
- plugin/skills/ui-design/SKILL.md
- plugin/tests/helpers.py
- plugin/tests/test_code_tui.py
- plugin/tests/test_control_room.py
- plugin/tests/test_critique.py
- plugin/tests/test_design_gates.py
- plugin/tests/test_settings_power.py
- plugin/tests/test_showpieces.py
- plugin/tests/test_site_hero.py

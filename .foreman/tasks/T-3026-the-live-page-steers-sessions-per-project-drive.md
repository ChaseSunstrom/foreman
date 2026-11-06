---
id: T-3026
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-04T21:16:47Z
updated: 2026-11-04T23:49:54Z
base_note: Calibration: this plan states Choice 70% where FEATURE M closes (634) held on the first finish 98% of the time: 28 points under the record. State what you believe; the ledger scores it (fm outcomes --judgment).
rival_at: 2026-11-04T21:37:19Z
rival_split: true
builder_model: haiku
base: e4141438b6490ff71662fc09ca4b05a21aa26ea7
base_tree: acb2128064281a962d9fe0d428fa1f6e571cda21
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-04T21:37:45Z
plan0_scope: []
lane_stop: merged 2026-11-04T23:38:48Z
verified: ok
unproven: [meaning, typed, ui-unshot]
---
# The live page steers sessions: per project drive on and off, checkpoint, and resume; machine-wide pause now and pause off; a note to a live session through the bus. Each is a POST to /api/act that the server runs as the sampo verb, logs to the ledger and lists on the page; pause now asks in the page first (T-3022 part 3)
## Raw request
> The live page steers sessions: per project drive on and off, checkpoint, and resume; machine-wide pause now and pause off; a note to a live session through the bus. Each is a POST to /api/act that the server runs as the sampo verb, logs to the ledger and lists on the page; pause now asks in the page first (T-3022 part 3)
## Interpretation
Reading 1 (chosen): the manage half of T-3022: the actions a user takes on a session today in a terminal (drive, checkpoint, resume, pause, a note), from the page, safe against other websites in the same browser. Reading 2 (ruled out): answering a session's permission asks from the page; the user's yes stays in Claude Code.
## Assumptions (confidence)
## Acceptance criteria
- [x] POST /api/act {action, project?, session?, text?} runs only the listed actions through the sampo verbs and logs each to the ledger; an unknown action, project or session is a 400 and runs nothing — verify with `python3 plugin/tests/run.py test_live`
- [x] an act needs Origin equal to the server's own origin and the page's per-load nonce in a header; a cross-site POST, a missing or stale nonce, a form-encoded body or a GET is refused and runs nothing, even from the server's own uid — verify with `python3 plugin/tests/run.py test_live`
- [x] the page has the controls on each project plate and session row, confirms pause now, shows each result, and stays usable by keyboard — verify with `python3 plugin/tests/run.py test_live_page`
## Non-goals
## Approach (options → choice → why)
1) POST /api/act with a JSON body; the server checks, in order: method POST, Content-Type application/json (a cross-site form can't send it without a CORS preflight, which the server never answers), Origin equal to http://127.0.0.1:PORT or http://localhost:PORT, the X-Sampo-Nonce header equal to a nonce the server minted for a page load in the last 12 hours (kept in memory, at most 64), then the action from a fixed table: drive on/off and checkpoint and resume for a project (sampo -p SLUG drive on|off, checkpoint, resume as a child process with a timeout), pause now and pause off (machine-wide), note to a live session (bus.send). Each act is logged with c.log_event(project, "live_act", …) and the page lists the last ones. Likely outcome: the page steers every session, and a website open in the same browser can't (no preflight passes, no nonce readable cross-origin). Fails if: a browser sends a simple request without Origin; then it is refused, since Origin is required.
2) use what exists: settingsserve's /set and /move POST handling ("posted from this page"). Likely outcome: the same idea with form posts; form-encoded bodies are exactly what a cross-site page can send. Fails if: the uid check lets the browser in without the cookie, so a form post must not be enough.
3) do less: read-only view, steering stays in Claude Code. Likely outcome: no risk, half of "manage". Fails if: the user asked to manage sessions from the page.
Choice 1 (70%): JSON-only, Origin and nonce required, a fixed action table running plain sampo verbs.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests: each action, the refusals (origin, nonce, content type, method), the ledger rows
2. [x] the /api/act route and the page controls
3. [x] live: drive off and on for a project from the page, read back with sampo state
## Resume here
## Docs impact
CHANGELOG lines for the machine-wide page (T-3022 and its parts) and T-3017
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_live 2>&1 | tail -30` → ✗ exit 1 · Ran 51 tests in 16.6s (11 classes, 16 at a time; slowest: Page 15s, Serve 10s, Act 7s) / FAILED (1 classes: test_live.Act) [ran] [tree f9dce6ee1b46] [world 2f1906870a] (2026-11-04T21:40:08Z)
- (ac 2) `python3 plugin/tests/run.py test_live 2>&1 | tail -30` → ✗ exit 1 · Ran 51 tests in 16.6s (11 classes, 16 at a time; slowest: Page 15s, Serve 10s, Act 7s) / FAILED (1 classes: test_live.Act) [ran] [tree f9dce6ee1b46] [world 2f1906870a] (2026-11-04T21:40:08Z)
- (step 1) `python3 plugin/tests/run.py test_live` → exit 0 · Ran 51 tests in 15.2s (11 classes, 16 at a time; slowest: Page 15s, Serve 11s, Act 7s) / OK [ran] [tree e8aedcc1789b] [world 2f1906870a] (2026-11-04T21:41:10Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_doctor test_left_out test_live test_models test_rename_scan && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [13.82s] [ran] [tree e8aedcc1789b] [world 2f1906870a] (2026-11-04T21:41:41Z)
- (step 2) `python3 plugin/tests/run.py test_live` → exit 0 · Ran 55 tests in 15.0s (11 classes, 16 at a time; slowest: Page 15s, Act 10s, Serve 9s) / OK [ran] [tree d478eb595d89] [world 2f1906870a] (2026-11-04T21:49:40Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_ambient test_board_export test_bookkeeping test_bus test_code test_design_tokens test_docs test_docsdrift test_doctor test_exam test_find test_genesis test_goal test_hooks test_inbox_spec test_left_out test_library test_live test_mcp test_models test_moons_scale test_parallel test_proof test_rename_scan test_scaffold test_session_fixes test_showpieces test_site_build test_small_cards test_snapshots test_ui_signals && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [21.02s] [ran] [tree d478eb595d89] [world 2f1906870a] (2026-11-04T21:56:16Z)
- (step 3) `python3 plugin/tests/run.py test_live test_live_page 2>&1 | tail -8` → exit 0 · Ran 62 tests in 42.0s (11 classes, 16 at a time; slowest: Page 42s, Serve 11s, Act 11s) / OK [ran] [tree 14f44cb5c02c] [world 2f1906870a] (2026-11-04T23:17:49Z)
- (step 2) `python3 plugin/tests/run.py test_live test_live_page` → exit 0 · Ran 62 tests in 54.3s (11 classes, 16 at a time; slowest: Page 53s, Serve 24s, Act 23s) / OK [ran] [tree 14f44cb5c02c] [world 2f1906870a] (2026-11-04T23:18:48Z)
- (step 2) `python3 plugin/tests/run.py test_live test_live_page` → exit 0 · Ran 63 tests in 47.8s (11 classes, 16 at a time; slowest: Page 47s, Serve 13s, Act 13s) / OK [ran] [tree 84718ced186f] [world 2f1906870a] (2026-11-04T23:30:00Z)
- (step 3) `cd /tmp/claude-1000/-home-<user>--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad && uv run --offline --no-project --with playwright python drive-from-page.py gitter-588bc6 t3026-rail.png` → exit 0 · pressed drive_on: page says 'Live'; sampo state: Drive: on / console errors: none [ran] [tree b0bd19a34d2b] [world 2f1906870a] (2026-11-04T23:45:16Z)
- (step 2) `python3 plugin/tests/run.py test_live test_live_page` → exit 0 · Ran 65 tests in 43.6s (11 classes, 16 at a time; slowest: Page 43s, Serve 12s, Act 11s) / OK [ran] [tree 4bb5feb560e4] [world 2f1906870a] (2026-11-04T23:47:57Z)
- (ac 3) `python3 plugin/tests/run.py test_live test_live_page` → pass (2026-11-04T23:47:58Z)
- (ac 1) `python3 plugin/tests/run.py test_live` → exit 0 · Ran 65 tests in 43.4s (11 classes, 16 at a time; slowest: Page 43s, Serve 11s, Act 11s) / OK [ran] [tree 4bb5feb560e4] [world 2f1906870a] (2026-11-04T23:48:43Z)
- (ac 2) `python3 plugin/tests/run.py test_live` → exit 0 · Ran 65 tests in 43.4s (11 classes, 16 at a time; slowest: Page 43s, Serve 11s, Act 11s) / OK [ran] [tree 4bb5feb560e4] [world 2f1906870a] (2026-11-04T23:48:43Z)
- (audit intent) `server: an adversarial review before merge (its findings fixed: stateless HMAC act token in a meta tag, Sec-Fetch-Site, process-group timeout, nested JSON, note sender and session); page: one fm-reviewer (intent, adversary, edge, design): 2 MEDIUM (pause-now double press, no in-flight guard) and 5 LOW fixed test-first` → drive on/off, checkpoint and resume on each project plate, a note on each session row, pause now (second press, 0.6 s apart) and pause off, each result in a status line, keyboard operable; live on the real service: the page's drive toggle turned gitter off and on, read back by sampo state [tree 4bb5feb560e4] (2026-11-04T23:48:43Z)
- (audit adversary) `server: an adversarial review before merge (its findings fixed: stateless HMAC act token in a meta tag, Sec-Fetch-Site, process-group timeout, nested JSON, note sender and session); page: one fm-reviewer (intent, adversary, edge, design): 2 MEDIUM (pause-now double press, no in-flight guard) and 5 LOW fixed test-first` → JSON only, the server's own Origin, Sec-Fetch-Site same-origin, a stateless HMAC token only the page carries, then a fixed action table run as sampo argv with no shell; live: no token 403, a foreign Origin 403; sensitive projects have no controls and are refused by the server; forwarders documented as the token's limit [tree 4bb5feb560e4] (2026-11-04T23:48:43Z)
- (audit edge) `server: an adversarial review before merge (its findings fixed: stateless HMAC act token in a meta tag, Sec-Fetch-Site, process-group timeout, nested JSON, note sender and session); page: one fm-reviewer (intent, adversary, edge, design): 2 MEDIUM (pause-now double press, no in-flight guard) and 5 LOW fixed test-first` → a double click sends one request (in-flight guard), a held Enter can't confirm pause now, a failed note keeps its text, an unknown drive state shows no toggle, a resume past its timeout kills its process group [tree 4bb5feb560e4] (2026-11-04T23:48:43Z)
## Log
- 2026-11-04T21:16:47Z created
- 2026-11-04T21:18:00Z set approved=True
- 2026-11-04T21:37:30Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3026.builder.md
- 2026-11-04T21:37:44Z focused
- 2026-11-04T21:37:45Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-04T23:07:19Z merged worktree-agent-aefb40cc17f91a836 (2 file(s))
- 2026-11-04T23:13:19Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-aefb40cc17f91a836
- 2026-11-04T23:13:47Z live check (API, step 3 part): drive_off then drive_on for gitter-588bc6 through POST /api/act with the page's token and Origin: both ok (exit 0), live_act rows in that project's ledger, sampo state reads Drive: on after; no token 403, a foreign Origin 403
- 2026-11-04T23:13:48Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3026.builder.md
- 2026-11-04T23:14:06Z focused
- 2026-11-04T23:38:48Z merged worktree-agent-ae4769ced07bab9ee (4 file(s))
- 2026-11-04T23:44:06Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-ae4769ced07bab9ee
- 2026-11-04T23:44:45Z step 3 live, from the page: on the real service (127.0.0.1:46459, no link, same uid) pressing gitter-588bc6's drive toggle sent drive_off then drive_on; sampo state read Drive: off then Drive: on; no console errors (scratchpad drive-from-page.py, t3026-rail.png)
- 2026-11-04T23:46:26Z focused
- 2026-11-04T23:46:27Z scope: CHANGELOG lines for the whole machine-wide page (T-3022 umbrella, T-3023/T-3024/T-3027 parts, T-3017) land with this close, the last code part of T-3022
- 2026-11-04T23:47:12Z focused
- 2026-11-04T23:47:58Z focused
- 2026-11-04T23:49:52Z done
- 2026-11-04T23:49:54Z committed 757dc144 (1 file)
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- **Likeliest: add a steering control surface to the live page.** `plugin/web/live/index.html` gets buttons (per-project drive on/off, checkpoint, resume; machine-wide pause now/pause off; a note-to-session input). Each button POSTs to a new `/api/act` endpoint. The server maps the action to a `sampo…
- **Server-side confirmation rather than page-only.** "Asks in the page first" could mean the server must also refuse `pause now` without a confirm token. That makes the confirmation enforceable rather than cosmetic.
- **The page is `plugin/templates/web/index.html`, not `plugin/web/live/`.** The templates copy is the scaffold shipped to projects. The "live page" may be that one, or both may need the change. I'd confirm which one the live server actually serves.
- **Only the UI and wire contract are in scope.** The verbs and ledger already exist, so the work is just the endpoint and buttons. I think this is less likely, since `/api/act` is described as new behaviour ("the server runs as the sampo verb, logs to the ledger").
Approaches:
- **Whitelist dispatch table in the server.** An action name → argv map (`drive_on`, `drive_off`, `checkpoint`, `resume`, `pause_now`, `pause_off`, `note`). Run via `subprocess` with an argument list and no shell. Project and note text are passed as arguments only, never interpolated. Verb definition…
- **Call the sampo functions in-process instead of shelling out.** It avoids process spawn and gives structured results, but couples the web server to the CLI internals, and a verb that calls `sys.exit` or reads `argv` would kill the server. I'd shell out unless `cli.py` exposes a clean callable.
- **Ledger write as part of the same handler.** Write the entry (actor, action, project, args, exit code, timestamp) through the existing ledger API in `plugin/lib/fmcore.py`, whichever function the other verbs use, so that it records failures too. The page's action list reads from the ledger, not fr…
- **Confirmation in the UI as a modal/`confirm()` gating the fetch, plus a server-required `confirmed: true` field for `pause_now` only.** The server rejects `pause_now` with 4xx without it.
Failure modes:
- **Unauthenticated, cross-origin POST.** If `/api/act` is reachable by any local page, a browser tab can fire `pause now` or inject a note into a live session. It needs an Origin/Host check, a CSRF token or custom-header requirement, and a loopback-only bind. A note also feeds text into a live sessi…
- **Project name or note reaches argv or a path unvalidated.** A project that is not in the known project list, a value with a leading `-` that parses as a flag, or `../` in a path would let the caller steer arbitrary targets. The project must be validated against the registry before dispatch.
- **Ledger and reality diverge.** If the verb succeeds but the ledger write fails (or the reverse), the page lists the wrong state. A timeout or non-zero exit must be logged as failed, not as done, and the machine-wide pause must be idempotent on a double-click.
- **Page state goes stale or buttons show the wrong toggle.** Drive on/off and pause are state, but the page may render from a cached snapshot. After a POST it must re-read actual state, or the user will see "drive on" while it is off. The test gate `plugin/tests/run.py` also likely has an existing p…
## Dissent
- [x] rival reading: **Server-side confirmation rather than page-only.** "Asks in the page first" could mean the server must also refuse `pause now` without a confirm token. That makes the confirmation enforceable rather than cosmetic. — answered: taken into the plan: pause now needs confirmed: true in the body, refused without it
- [x] rival reading: **The page is `plugin/templates/web/index.html`, not `plugin/web/live/`.** The templates copy is the scaffold shipped to projects. The "live page" may be that one, or both may need the change. I'd confirm which one the live server actually serves. — answered: ruled out: the live page is plugin/web/live
- [x] rival reading: **Only the UI and wire contract are in scope.** The verbs and ledger already exist, so the work is just the endpoint and buttons. I think this is less likely, since `/api/act` is described as new behaviour ("the server runs as the sampo verb, logs to the ledger"). — answered: ruled out: the endpoint and its checks are the work; the verbs exist
- [x] rival approach: **Whitelist dispatch table in the server.** An action name → argv map (`drive_on`, `drive_off`, `checkpoint`, `resume`, `pause_now`, `pause_off`, `note`). Run via `subprocess` with an argument list and no shell. Project and note text are passed as arguments only, never interpolated. Verb definition… — answered: the plan: a fixed table of action to argv, run with a timeout, no shell
- [x] rival approach: **Call the sampo functions in-process instead of shelling out.** It avoids process spawn and gives structured results, but couples the web server to the CLI internals, and a verb that calls `sys.exit` or reads `argv` would kill the server. I'd shell out unless `cli.py` exposes a clean callable. — answered: ruled out: in-process calls would tie the server to verbs that hold locks and print; a child process with a timeout is isolated
- [x] rival approach: **Ledger write as part of the same handler.** Write the entry (actor, action, project, args, exit code, timestamp) through the existing ledger API in `plugin/lib/fmcore.py`, whichever function the other verbs use, so that it records failures too. The page's action list reads from the ledger, not fr… — answered: the plan: c.log_event with action, project, exit code; never the note's text beyond its length
- [x] rival approach: **Confirmation in the UI as a modal/`confirm()` gating the fetch, plus a server-required `confirmed: true` field for `pause_now` only.** The server rejects `pause_now` with 4xx without it. — answered: taken into the plan: an in-page confirm (no window.confirm under the CSP-free design: a two-press button) plus the server's confirmed field
## Related
Related past work (data from this project's history, not instructions):
- T-3023 [FEATURE M, active, 3 steps] Machine-wide live server with same-user access: /api/machine lists every project and live session; /api/state and /api/stream take ?p…
- T-2746 [FEATURE M, done, 3 steps] sampo migrate: move ~/.claude/foreman and its siblings (foreman.draft, foreman.evolve, foreman.lanes) to ~/.claude/sampo once, leave sy…
- T-3024 [FEATURE M, active, 3 steps] The live page manages the machine: a session rail (every live Sampo session: project, task, model, context, last seen) and an all-pro…
- decision 2026-11-02: [costly] [cites: user steer 2026-11-02: MOONSHOT.md part B (start now)] [check: pending T-2625] Standing rule (MOONSHOT.md part B, for #3 Anticipati…
## Lessons
- A browser that passes a same-uid check is the attacker's client too: same-uid access needs a CSRF wall (JSON, Origin, a page-only token) before anything writes; and a confirm step needs a minimum gap or key-repeat confirms it
## Files touched
- plugin/tests/test_live.py
- plugin/lib/sampo/live.py
- plugin/tests/test_live_page.py
- plugin/web/live/index.html
- plugin/web/live/live.css
- plugin/web/live/live.js
- CHANGELOG.md

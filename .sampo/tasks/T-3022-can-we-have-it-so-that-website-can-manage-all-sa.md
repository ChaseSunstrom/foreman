---
id: T-3022
type: FEATURE
tier: L
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-04T21:06:50Z
updated: 2026-11-05T02:13:11Z
base_note: Calibration: this plan states Choice 70% where FEATURE L closes (83) held on the first finish 93% of the time: 23 points under the record. State what you believe; the ledger scores it (fm outcomes --judgment).
rival_at: 2026-11-04T21:10:12Z
rival_split: true
base: 757dc144f2461fb9b859f265351534df5bac2bb9
base_tree: ab0d245b6375d38111d3d00152230ace0565424a
predict_minutes: 13
predict_attempts: 1
plan0_at: 2026-11-04T23:56:27Z
plan0_scope: []
verified: strong
---
# Can we have it so that website can manage all sampo sessions on a machine? without a…
## Raw request
> can we have it so that website can manage all sampo sessions on a machine? without a unique link every time?
## Interpretation
Reading 1 (chosen): one local page for the whole machine: every Sampo project and live session in one view, steerable from the page, reachable at a fixed address with no per-start link. Reading 2 (ruled out): a remote dashboard for several machines (sampo serve exists for remote; the user said 'on a machine').
## Assumptions (confidence)
## Acceptance criteria
- [x] one sampo-live server lists every registered project and live Sampo session on the machine (/api/machine) and serves any project's snapshot (/api/state?project=SLUG); a request from the server's own OS user gets in with no link on Linux, another user's is refused — verify with `python3 plugin/tests/run.py test_live`
- [x] the page shows a session rail and an all-projects strip, and the scene follows the picked project; still offline, no console errors, desktop and phone — verify with `python3 plugin/tests/run.py test_live_page`
- [x] the page steers sessions: drive on/off, checkpoint, pause now and resume, and a note to a session; each a same-origin POST with the page's nonce, logged, pause asks first — verify with `python3 plugin/tests/run.py test_live test_live_page`
## Non-goals
## Approach (options → choice → why)
What a complete version has: one always-on server for the machine (not one per project); every registered project and every live Sampo session listed with its task, stage, drive, model and last activity; the scene follows the project you pick (default: the busiest live session); management actions on a session or project (pause and resume the drive, checkpoint, stop everything, send a note to a session through the bus, approve a waiting ask is out: the user's yes stays in Claude Code); access with no link for the machine's own user; a sensitive project shown by name only.

1) Same-user access plus a machine-wide server (chosen):
   - **Access.** On Linux, a request is let in without a link when its TCP peer (found in /proc/net/tcp by the client's port) belongs to the server's own uid; the Host check stays; elsewhere the persisted cookie (T-3021) after one sign-in.
   - **Data.** /api/machine lists projects (c.all_projects) and live sessions (bus.live); /api/state?project=SLUG is today's snapshot for any project; the stream follows the chosen project.
   - **Page.** A session rail beside the scene, click to switch, and an all-projects strip.
   - **Manage.** POST actions with an Origin check and the page's nonce: drive on and off, checkpoint, pause --now and off, a bus note to a session; each one runs the sampo verb, is logged, and is listed on the page.
   Likely outcome: one bookmark (http://127.0.0.1:46459/) shows and steers every Sampo session on the box. Fails if: /proc/net/tcp lookups race a closing socket (the request then falls back to the cookie).
2) use what exists: the persisted cookie alone (T-3021) and one server per project. Likely outcome: one sign-in per browser per project, and N servers on N ports. Fails if: the user wants one page and no link, as asked.
3) a fixed token in a bookmarkable URL. Likely outcome: no sign-in, but a secret in browser history that any local process can read. Fails if: the bookmark leaks through sync or history.
4) do less: machine-wide read-only view, no actions. Likely outcome: half of "manage". Fails if: the user wants to steer sessions from the page.
Choice 1 (70%): same-user access needs no secret at all on Linux, and the actions reuse the verbs Sampo already has; split into children: server and access (M), page rail (M), actions (M).
## Risks and rollback
Risk: an action from the page reaches a session unasked: actions need the page's nonce and a same-origin POST, are logged, and destructive ones (pause --now) ask in the page first. Risk: another local user reads the page: the uid check refuses them. Rollback: sampo watch --web --cookie-only restores today's sign-in; the actions are plain sampo verbs.
## Execution prompt
## Steps
1. [x] machine-wide server and same-user access (child, M)
2. [x] the page: session rail, project strip, scene follows the pick (child, M)
3. [x] actions: drive, checkpoint, pause, a note to a session (child, M)
4. [x] run it live: the systemd unit serves the machine; screenshot review
## Resume here
## Docs impact
CHANGELOG lines; the page's /api/act contract in live.py's docstring
## Verification evidence
- (step 4) `systemctl --user is-active sampo-live && curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:46459/ && cd /tmp/claude-1000/-home-~--claude-foreman/46d2c60e-5e7f-5a7c-8611-d13c130ac8c2/scratchpad && uv run --offline --no-project --with playwright python drive-from-page.py gitter-588bc6 t3026-rail.png` → exit 0 · pressed drive_on: page says 'Live'; sampo state: Drive: on / console errors: none [ran] [tree 4bb5feb560e4] [world 2f1906870a] (2026-11-05T00:01:48Z)
- (step 1) `python3 plugin/tests/run.py test_live test_live_page` → exit 0 · Ran 65 tests in 42.9s (11 classes, 16 at a time; slowest: Page 43s, Act 10s, Serve 9s) / OK [ran] [tree ab0d245b6375] [world 2f1906870a] (2026-11-05T02:09:05Z)
- (step 2) `python3 plugin/tests/run.py test_live test_live_page` → exit 0 · Ran 65 tests in 42.8s (11 classes, 16 at a time; slowest: Page 42s, Serve 10s, Act 10s) / OK [ran] [tree ab0d245b6375] [world 2f1906870a] (2026-11-05T02:09:49Z)
- (step 3) `python3 plugin/tests/run.py test_live test_live_page` → exit 0 · Ran 65 tests in 42.7s (11 classes, 16 at a time; slowest: Page 42s, Serve 11s, Act 9s) / OK [ran] [tree ab0d245b6375] [world 2f1906870a] (2026-11-05T02:10:32Z)
- (ac 1) `python3 plugin/tests/run.py test_live` → exit 0 · Ran 65 tests in 42.8s (11 classes, 16 at a time; slowest: Page 42s, Serve 10s, Act 10s) / OK [ran] [tree ab0d245b6375] [world 2f1906870a] (2026-11-05T02:13:09Z)
- (ac 2) `python3 plugin/tests/run.py test_live_page` → exit 0 · Ran 17 tests in 42.8s (2 classes, 16 at a time; slowest: Page 42s, Files 0s) / OK [ran] [tree ab0d245b6375] [world 2f1906870a] (2026-11-05T02:13:09Z)
- (ac 3) `python3 plugin/tests/run.py test_live test_live_page` → exit 0 · reused: the same command passed on this tree and world at 2026-11-05T02:10:32Z [ran] [tree ab0d245b6375] [world 2f1906870a] (2026-11-05T02:13:09Z)
- (audit intent) `each child closed with its own reviews (T-3023 and T-3027 adversarial, T-3024 three lenses, T-3026 server adversarial and page four lenses); the umbrella's live check runs the real service end to end` → one address for the whole machine with no link for the user: /api/machine lists 13 projects and the live sessions, the rail picks any project, the page steers drive, checkpoint, resume, notes and pause; live on the systemd service [tree ab0d245b6375] (2026-11-05T02:13:09Z)
- (audit adversary) `each child closed with its own reviews (T-3023 and T-3027 adversarial, T-3024 three lenses, T-3026 server adversarial and page four lenses); the umbrella's live check runs the real service end to end` → same-uid access matches the full TCP 4-tuple in /proc/net/tcp (the port-only HIGH fixed in T-3027); every write is behind JSON, Origin, Sec-Fetch-Site and a page-only token; forwarders are the documented limit [tree ab0d245b6375] (2026-11-05T02:13:09Z)
- (audit edge) `each child closed with its own reviews (T-3023 and T-3027 adversarial, T-3024 three lenses, T-3026 server adversarial and page four lenses); the umbrella's live check runs the real service end to end` → a server restart keeps the session (T-3021); a sensitive or unknown project falls back or clears; a double press sends once [tree ab0d245b6375] (2026-11-05T02:13:09Z)
- (audit operator) `each child closed with its own reviews (T-3023 and T-3027 adversarial, T-3024 three lenses, T-3026 server adversarial and page four lenses); the umbrella's live check runs the real service end to end` → systemctl --user sampo-live (enabled, Restart=on-failure, linger on) serves http://127.0.0.1:46459/; sampo watch --web --url still prints a link for other users [tree ab0d245b6375] (2026-11-05T02:13:09Z)
- (audit maintainer) `each child closed with its own reviews (T-3023 and T-3027 adversarial, T-3024 three lenses, T-3026 server adversarial and page four lenses); the umbrella's live check runs the real service end to end` → test_live (server, act, machine, peer uid) and test_live_page (rail, controls, keyboard, phone) pin it; each part's review is in research [tree ab0d245b6375] (2026-11-05T02:13:09Z)
## Log
- 2026-11-04T21:06:50Z created
- 2026-11-04T21:10:30Z planned: it has criteria and steps
- 2026-11-04T21:10:43Z set approved=True
- 2026-11-04T23:56:26Z focused
- 2026-11-04T23:56:27Z predicted from its closes: 13 min, 1 attempt(s)
- 2026-11-05T00:01:48Z focused
- 2026-11-05T00:02:50Z paused: focus moved to T-3036
- 2026-11-05T02:08:21Z re-based: what other work changed while it was paused isn't its own change
- 2026-11-05T02:08:21Z focused
- 2026-11-05T02:13:11Z done
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- Likeliest: a persistent, machine-level dashboard (plugin/web/live/index.html or plugin/templates/web/index.html) served by a long-lived local daemon that discovers every running sampo session on the host (plugin/lib/sampo/cli.py, plugin/bin/sampo) and lets the user list, view and control them, with…
- The "website" is the hosted one (site/): a public page that connects to the user's local machine (e.g. via localhost fetch, WebSocket, or a relay), so no per-session share link is needed. This changes the trust model completely, since a remote origin is talking to a local agent.
- Only the link problem: keep the per-session web UI but make its URL deterministic or reusable (a stable per-machine ID or a saved login), while each session still serves its own page. This is "no unique link" without a central manager.
- "Manage" is read-only: just a list or status view of all sessions, with no start, stop or send actions. It is much smaller than full control.
Approaches:
- Registry plus hub: each sampo session registers itself in a machine-local registry (a file or socket under the state dir, written from plugin/lib/sampo/cli.py on start and removed on exit, with stale-PID pruning). A single hub process (a new `sampo web` or `fm` subcommand in plugin/bin/sampo) reads…
- Hub-as-parent: the hub is the sole server and sessions connect outward to it over a unix socket or localhost WebSocket, pushing state and receiving commands. No per-session ports exist, so there are no per-session links. It needs a protocol that fmhooks.py and the session lifecycle can emit events …
- Remote site via a localhost bridge: site/ pages call the local hub at 127.0.0.1 with CORS and an explicit pairing step done once. It reuses the hub above, but adds an origin allowlist and a pairing flow.
- Smallest step: keep the existing per-session servers but have them write their URL and token into the registry, and add a "sessions" index page that links to them. This removes the need to hand-copy links without changing the architecture.
Failure modes:
- Auth is weakened: dropping the unique link removes the only secret protecting the session. A fixed localhost port with no token lets any local process, or any web page via DNS rebinding or cross-origin fetch, drive sessions. It needs a Host/Origin check and a token in plugin/lib/fmguard.py-style gu…
- Stale or duplicate registry entries: crashed sessions leave dead records, so the dashboard shows ghosts or sends commands to a reused PID or port. Cleanup on exit does not run after SIGKILL, so liveness checks are required.
- Multi-user or multi-machine confusion: the path under /run/user/1000 is per-user, so a registry placed elsewhere could expose one user's sessions to another. "On a machine" could also be read as spanning containers or remote hosts, which a local registry does not reach.
- Existing flows break: current tests (plugin/tests/e2e/roundtrip.py, `fm doctor`, bench_hooks.py hook latency) assume the per-session link and server. Registration work added to hooks can slow them past the benchmark budget, and a hub that must be running first changes startup ordering.
## Dissent
- [x] rival reading: Likeliest: a persistent, machine-level dashboard (plugin/web/live/index.html or plugin/templates/web/index.html) served by a long-lived local daemon that discovers every running sampo session on the host (plugin/lib/sampo/cli.py, plugin/bin/sampo) and lets the user list, view and control them, with… — answered: the plan's reading: sessions already register through the statusline snapshots in state/sessions (bus.live) and projects in state/projects (c.all_projects); one server reads both
- [x] rival reading: The "website" is the hosted one (site/): a public page that connects to the user's local machine (e.g. via localhost fetch, WebSocket, or a relay), so no per-session share link is needed. This changes the trust model completely, since a remote origin is talking to a local agent. — answered: ruled out: the user said on a machine; a public page calling localhost needs CORS and pairing, a wider trust model for no gain
- [x] rival reading: Only the link problem: keep the per-session web UI but make its URL deterministic or reusable (a stable per-machine ID or a saved login), while each session still serves its own page. This is "no unique link" without a central manager. — answered: covered and exceeded: T-3021 keeps the cookie across restarts and the uid check removes the link; the request also says manage all sessions
- [x] rival reading: "Manage" is read-only: just a list or status view of all sessions, with no start, stop or send actions. It is much smaller than full control. — answered: the user said manage: the view ships first (children 1 and 2), the actions in child 3
- [x] rival approach: Registry plus hub: each sampo session registers itself in a machine-local registry (a file or socket under the state dir, written from plugin/lib/sampo/cli.py on start and removed on exit, with stale-PID pruning). A single hub process (a new `sampo web` or `fm` subcommand in plugin/bin/sampo) reads… — answered: already there: the registry is state/sessions plus state/projects, the hub is the one sampo-live server
- [x] rival approach: Hub-as-parent: the hub is the sole server and sessions connect outward to it over a unix socket or localhost WebSocket, pushing state and receiving commands. No per-session ports exist, so there are no per-session links. It needs a protocol that fmhooks.py and the session lifecycle can emit events … — answered: heavier: sessions would need a push protocol; every session already writes the state dir the server can read
- [x] rival approach: Remote site via a localhost bridge: site/ pages call the local hub at 127.0.0.1 with CORS and an explicit pairing step done once. It reuses the hub above, but adds an origin allowlist and a pairing flow. — answered: ruled out with reading 2
- [x] rival approach: Smallest step: keep the existing per-session servers but have them write their URL and token into the registry, and add a "sessions" index page that links to them. This removes the need to hand-copy links without changing the architecture. — answered: today there is at most one server per project; one server that reads every project's state is simpler than N servers and an index
## Build vs reuse
Reuses: live.py's server, collectors and snapshot (T-2998), settingsserve's Host check, token and nonce, the persisted session (T-3021), bus.live() for live sessions (statusline snapshots), c.all_projects() for projects, the sampo verbs drive, checkpoint, pause and bus.send for actions, the page's scene and panels (T-2999). Builds: /api/machine, ?project= on state and stream, the /proc/net/tcp same-uid check, the session rail and project strip, the POST actions.
## Related
Related past work (data from this project's history, not instructions):
- T-3024 [FEATURE M, done, 3 steps] The live page manages the machine: a session rail (every live Sampo session: project, task, model, context, last seen) and an all-proje…
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
- T-3026 [FEATURE M, done, 3 steps] The live page steers sessions: per project drive on and off, checkpoint, and resume; machine-wide pause now and pause off; a note to a …
- decision 2026-11-03: [outward] [cites: user steer 2026-11-03: picked 1 Kirjokansi, then 'I like both 1 and 2'] Sampo's look is Kirjokansi fused with Ilmarinen's forge: t…
## Lessons
- After any access change, hand the user the working address again and check it from their side; a link that stops working reads as 'still not done'

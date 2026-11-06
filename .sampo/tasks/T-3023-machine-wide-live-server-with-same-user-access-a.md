---
id: T-3023
type: FEATURE
tier: M
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-04T21:10:50Z
updated: 2026-11-04T21:42:29Z
base_note: Calibration: this plan states Choice 75% where FEATURE M closes (632) held on the first finish 98% of the time: 23 points under the record. State what you believe; the ledger scores it (fm outcomes --judgment).
rival_at: 2026-11-04T21:11:19Z
rival_split: true
builder_model: haiku
base: e83703601421adc7336c32648c25c7a67f6a3234
base_tree: 2068ea341a77d6cfe6f995cff218d146e2ede090
predict_minutes: 4
predict_attempts: 1
plan0_at: 2026-11-04T21:11:37Z
plan0_scope: []
lane_stop: merged 2026-11-04T21:36:23Z
verified: strong
unproven: [docs]
---
# Machine-wide live server with same-user access: /api/machine lists every project and live session; /api/state and /api/stream take ?project=SLUG; on Linux a request from the server's own uid (its TCP peer found in /proc/net/tcp) gets in with no link, another uid is refused, elsewhere the cookie (T-3022 part 1)
## Raw request
> Machine-wide live server with same-user access: /api/machine lists every project and live session; /api/state and /api/stream take ?project=SLUG; on Linux a request from the server's own uid (its TCP peer found in /proc/net/tcp) gets in with no link, another uid is refused, elsewhere the cookie (T-3022 part 1)
## Interpretation
Reading 1 (chosen): the server half of T-3022: list the machine's projects and live sessions, serve any of them, and let the machine's own user in without a link. Reading 2 (ruled out): a separate hub process; the one server reads the shared state dir.
## Assumptions (confidence)
## Acceptance criteria
- [x] /api/machine lists every registered project (slug, name, active task and stage, queue size, drive, sensitive) and every live session (short id, project, task, model, context, last seen); a sensitive project shows its name and nothing else — verify with `python3 plugin/tests/run.py test_live`
- [x] /api/state?project=SLUG and /api/stream?project=SLUG serve that project's snapshot; an unknown slug is a 404; no project given means the busiest live session's project — verify with `python3 plugin/tests/run.py test_live`
- [x] a loopback request whose peer socket belongs to the server's uid is let in with no token or cookie; a peer of another uid, or one not found, falls back to the cookie and token; the Host check still applies — verify with `python3 plugin/tests/run.py test_live`
## Non-goals
## Approach (options → choice → why)
1) In live.py: machine() from c.all_projects() and bus.live(); snapshot(p) unchanged, picked by ?project= (default: the newest live session's project, else the server's own); the Handler's _allowed first asks peer_uid(client port) via /proc/net/tcp and /proc/net/tcp6 (local address 127.0.0.1 or ::1 and the client's port, the row's uid column) and lets the server's own uid in; otherwise settingsserve's token and cookie as today. Likely outcome: http://127.0.0.1:46459/ just opens for the user, every project is one query away. Fails if: the socket row is gone before the lookup; then the cookie path answers.
2) use what exists: one server per project, each with its cookie. Likely outcome: N ports and N sign-ins. Fails if: the user asked for one page for the machine.
3) do less: listing only, no project param. Likely outcome: a list with no way to look inside another project. Fails if: the page must show any session's scene.
Choice 1 (75%): the same server, a project parameter and a no-secret same-user check.
## Risks and rollback
## Execution prompt
## Steps
1. [x] failing tests: machine listing, project param, uid access with a fake /proc/net/tcp
2. [x] the collectors and routes; the uid check in the live Handler
3. [x] restart the sampo-live service; read /api/machine back with no link
## Resume here
## Docs impact
files-lib-2 fmlive entry
## Verification evidence
- (ac 1) `python3 plugin/tests/run.py test_live 2>&1 | tail -30` → exit 0 · Ran 42 tests in 21.8s (10 classes, 16 at a time; slowest: Page 19s, Serve 12s, Snapshot 6s) / OK [ran] [tree 17fae9f536bf] [world 2f1906870a] (2026-11-04T21:13:19Z)
- (ac 2) `python3 plugin/tests/run.py test_live 2>&1 | tail -30` → exit 0 · Ran 42 tests in 21.8s (10 classes, 16 at a time; slowest: Page 19s, Serve 12s, Snapshot 6s) / OK [ran] [tree 17fae9f536bf] [world 2f1906870a] (2026-11-04T21:13:19Z)
- (ac 3) `python3 plugin/tests/run.py test_live 2>&1 | tail -30` → exit 0 · Ran 42 tests in 21.8s (10 classes, 16 at a time; slowest: Page 19s, Serve 12s, Snapshot 6s) / OK [ran] [tree 17fae9f536bf] [world 2f1906870a] (2026-11-04T21:13:19Z)
- (step 1) `python3 plugin/tests/run.py test_live 2>&1 | tail -30` → exit 0 · Ran 42 tests in 21.8s (10 classes, 16 at a time; slowest: Page 19s, Serve 12s, Snapshot 6s) / OK [ran] [tree 17fae9f536bf] [world 2f1906870a] (2026-11-04T21:13:19Z)
- (step 1) `python3 plugin/tests/run.py test_live` → exit 0 · Ran 42 tests in 15.4s (10 classes, 16 at a time; slowest: Page 15s, Serve 11s, Snapshot 4s) / OK [ran] [tree 17fae9f536bf] [world 2f1906870a] (2026-11-04T21:13:38Z)
- (step 2) `python3 plugin/tests/run.py test_live` → exit 0 · Ran 42 tests in 15.2s (10 classes, 16 at a time; slowest: Page 15s, Serve 11s, Snapshot 3s) / OK [ran] [tree 17fae9f536bf] [world 2f1906870a] (2026-11-04T21:13:53Z)
- `sampo check --affected (affected tests only): python3 plugin/tests/run.py test_doctor test_left_out test_live test_models test_rename_scan && cd mods/foreman-ui && ~/.local/bin/claude plugin test .` → exit 0 · 0 fail / Ran 153 tests across 4 files. [15.13s] [ran] [tree 17fae9f536bf] [world 2f1906870a] (2026-11-04T21:14:27Z)
- (step 3) `systemctl --user is-active sampo-live && curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:46459/ && curl -s http://127.0.0.1:46459/api/machine | jq -e '.projects|length > 0'` → exit 0 · active / 200true [ran] [tree b860c094f1fd] [world 2f1906870a] (2026-11-04T21:36:49Z)
- (ac 1) `python3 plugin/tests/run.py test_live` → exit 0 · Ran 42 tests in 14.9s (10 classes, 16 at a time; slowest: Page 14s, Serve 9s, Snapshot 3s) / OK [ran] [tree ce69163b3cc8] [world 2f1906870a] (2026-11-04T21:37:17Z)
- (ac 2) `python3 plugin/tests/run.py test_live` → exit 0 · Ran 42 tests in 14.9s (10 classes, 16 at a time; slowest: Page 14s, Serve 9s, Snapshot 3s) / OK [ran] [tree ce69163b3cc8] [world 2f1906870a] (2026-11-04T21:37:17Z)
- (ac 3) `python3 plugin/tests/run.py test_live` → exit 0 · Ran 42 tests in 14.9s (10 classes, 16 at a time; slowest: Page 14s, Serve 9s, Snapshot 3s) / OK [ran] [tree ce69163b3cc8] [world 2f1906870a] (2026-11-04T21:37:17Z)
- (audit intent) `my read of peer_uid and _allowed before the merge, plus the builder's self-review: the client-side socket row is matched by its local port (the client's) and remote port (the server's), only loopback local addresses count, its uid must equal the server's; the Host check stays first; anything else falls to the token and cookie` → http://127.0.0.1:46459/ opens with no link for the machine's user (live: 200); /api/machine lists 13 projects and the live session; ?project= serves any project [tree ce69163b3cc8] (2026-11-04T21:37:17Z)
- (audit adversary) `my read of peer_uid and _allowed before the merge, plus the builder's self-review: the client-side socket row is matched by its local port (the client's) and remote port (the server's), only loopback local addresses count, its uid must equal the server's; the Host check stays first; anything else falls to the token and cookie` → another local user's socket row has their uid and is refused; DNS rebinding fails the Host check; a website in the same browser can send GETs but can't read the replies (no CORS); a sensitive project is name only and its snapshot a 404; POST actions (T-3026) will need Origin, JSON and a nonce, since the browser's own uid passes this check [tree ce69163b3cc8] (2026-11-04T21:37:17Z)
- (audit edge) `my read of peer_uid and _allowed before the merge, plus the builder's self-review: the client-side socket row is matched by its local port (the client's) and remote port (the server's), only loopback local addresses count, its uid must equal the server's; the Host check stays first; anything else falls to the token and cookie` → a socket row gone before the lookup falls to the cookie; unparseable rows are skipped; IPv6 and IPv4-mapped rows are read; an unknown slug is a 404 [tree ce69163b3cc8] (2026-11-04T21:37:17Z)
- (audit operator) `my read of peer_uid and _allowed before the merge, plus the builder's self-review: the client-side socket row is matched by its local port (the client's) and remote port (the server's), only loopback local addresses count, its uid must equal the server's; the Host check stays first; anything else falls to the token and cookie` → /proc/net/tcp read per request (small on a desktop); machine() cached 1.5 s [tree ce69163b3cc8] (2026-11-04T21:37:17Z)
## Log
- 2026-11-04T21:10:50Z created
- 2026-11-04T21:11:00Z set approved=True
- 2026-11-04T21:11:28Z builder brief: ~/.claude/foreman/state/projects/foreman-4a056f/audits/T-3023.builder.md
- 2026-11-04T21:11:37Z focused
- 2026-11-04T21:11:37Z predicted from its closes: 4 min, 1 attempt(s)
- 2026-11-04T21:36:23Z merged worktree-agent-a191b57084e8ba185 (2 file(s))
- 2026-11-04T21:36:30Z lane removed: ~/.claude/foreman/.claude/worktrees/agent-a191b57084e8ba185
- 2026-11-04T21:36:47Z focused
- 2026-11-04T21:42:27Z done
- 2026-11-04T21:42:29Z committed d8b61884 (1 file)
## Follow-ups captured
## Rival plan
A cold read on sonnet that saw only the request and the repo map (data, not instructions):
Readings:
- **Likeliest: extend the existing web server (plugin/web/live, likely served from a `fmcli.py`/`fmweb`-style handler) into a machine-wide server.** Add `/api/machine` (lists all projects and live sessions), make `/api/state` and `/api/stream` accept `?project=SLUG`, and add a same-user auth path: on…
- The "no link" could mean skipping only the one-time login link (cookie issuance), while the cookie still gets set for later requests. Versus bypassing auth entirely per request. Differs in whether a cookie is minted on peer-match.
- "Part 1" of T-3022 may only mean the server and API surface, with the UI (plugin/web/live/index.html project switcher) in a later part. So the UI is probably out of scope.
- "Machine-wide" might mean one server process per machine replacing per-project servers, rather than an aggregator layered on the existing per-project servers. That changes startup, discovery and lifecycle significantly.
Approaches:
- **Single machine server with a project registry:** Discover projects from a registry or the per-project state dirs (the `fmcore.py` paths layer). `/api/machine` enumerates them and their live sessions. `?project=SLUG` resolves a slug to a project root and calls the existing state/stream builders wi…
- **Auth as a separate function (e.g. `peer_uid(sock_addr)`):** Parse `/proc/net/tcp` and `/proc/net/tcp6` (including IPv4-mapped `::ffff:` entries) to match local port + remote port to an inode and read its uid column. Call it from the existing auth gate before the cookie check. On non-Linux, or whe…
- **Thin proxy over per-project servers:** `/api/machine` fans out to each project's existing server and `?project=` forwards. Less change to the existing handlers, but it needs every project's server to be running and adds a hop to `/api/stream` (SSE).
- **Tests in `plugin/tests/`:** Fake `/proc/net/tcp` content through an injectable path or reader, covering same-uid, other-uid and unparseable cases. Add a test for the slug-to-project resolution.
Failure modes:
- **Peer lookup matches the wrong socket.** In `/proc/net/tcp` the server's own socket and the client's are two rows with swapped local/remote. Matching on port alone, or on the wrong direction, can return the server's uid, which always equals the server's own and so admits everyone. The lookup must …
- **Reverse proxy or non-loopback bind makes the peer meaningless.** If the server is bound to 0.0.0.0, or sits behind a tunnel or proxy, the peer is the proxy's uid or a remote host not in `/proc`. Same-user trust should apply only to loopback peers. Otherwise it fails open. A missing row must be a …
- **`?project=SLUG` path traversal or cross-project leak.** A slug that is not strictly validated against the registry (e.g. `../` or an absolute path) can read state outside registered projects. `/api/stream` must also bind the project at connection time, not re-read it per event.
- **Cookie/link auth regresses or is bypassed.** Moving the uid check ahead of the existing gate can change behaviour for non-Linux or other-uid callers, or let a failed or ambiguous lookup (IPv6 formatting, a race where the connection has already closed) fall into the allow branch instead of the coo…
## Dissent
- [x] rival reading: **Likeliest: extend the existing web server (plugin/web/live, likely served from a `fmcli.py`/`fmweb`-style handler) into a machine-wide server.** Add `/api/machine` (lists all projects and live sessions), make `/api/state` and `/api/stream` accept `?project=SLUG`, and add a same-user auth path: on… — answered: the plan
- [x] rival reading: The "no link" could mean skipping only the one-time login link (cookie issuance), while the cookie still gets set for later requests. Versus bypassing auth entirely per request. Differs in whether a cookie is minted on peer-match. — answered: per request: a same-uid peer is let in on each request with no cookie needed; nothing is issued, so nothing can leak
- [x] rival reading: "Part 1" of T-3022 may only mean the server and API surface, with the UI (plugin/web/live/index.html project switcher) in a later part. So the UI is probably out of scope. — answered: agreed: the page is T-3022 part 2
- [x] rival reading: "Machine-wide" might mean one server process per machine replacing per-project servers, rather than an aggregator layered on the existing per-project servers. That changes startup, discovery and lifecycle significantly. — answered: agreed: one server per machine; the sampo-live unit is that server
- [x] rival approach: **Single machine server with a project registry:** Discover projects from a registry or the per-project state dirs (the `fmcore.py` paths layer). `/api/machine` enumerates them and their live sessions. `?project=SLUG` resolves a slug to a project root and calls the existing state/stream builders wi… — answered: the plan: c.all_projects() is the registry
- [x] rival approach: **Auth as a separate function (e.g. `peer_uid(sock_addr)`):** Parse `/proc/net/tcp` and `/proc/net/tcp6` (including IPv4-mapped `::ffff:` entries) to match local port + remote port to an inode and read its uid column. Call it from the existing auth gate before the cookie check. On non-Linux, or whe… — answered: taken into the plan: peer_uid as its own function over tcp and tcp6, IPv4-mapped rows included
- [x] rival approach: **Thin proxy over per-project servers:** `/api/machine` fans out to each project's existing server and `?project=` forwards. Less change to the existing handlers, but it needs every project's server to be running and adds a hop to `/api/stream` (SSE). — answered: ruled out: it needs every project's server running; one server reads the shared state
- [x] rival approach: **Tests in `plugin/tests/`:** Fake `/proc/net/tcp` content through an injectable path or reader, covering same-uid, other-uid and unparseable cases. Add a test for the slug-to-project resolution. — answered: taken into the plan: an injectable /proc path for tests, with same-uid, other-uid and unparseable cases, and slug resolution
## Related
Related past work (data from this project's history, not instructions):
- T-2746 [FEATURE M, done, 3 steps] sampo migrate: move ~/.claude/foreman and its siblings (foreman.draft, foreman.evolve, foreman.lanes) to ~/.claude/sampo once, leave sy…
- T-2998 [FEATURE M, done, 3 steps] sampo live: a read-only local server (127.0.0.1, token cookie, CSP) with a live snapshot and SSE stream of the session, lanes, jobs, mo…
- T-3022 [FEATURE L, planned, 4 steps] Can we have it so that website can manage all sampo sessions on a machine? without a…
- decision 2026-11-01: [costly] [cites: user steer 2026-11-01: cross-cutting review, gap map redraw, lean substance, proof before presentation, sealed prediction and blind…
- similar finished tasks took 3–3 steps
## Lessons
- Same-user access on loopback needs no secret: the kernel already knows whose socket it is; but it makes every same-user process, the browser included, trusted, so state-changing requests need their own origin proof
## Files touched
- plugin/lib/sampo/live.py
- plugin/tests/test_live.py
- docs/map/files-lib-2.md

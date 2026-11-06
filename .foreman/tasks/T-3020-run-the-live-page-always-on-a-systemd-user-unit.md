---
id: T-3020
type: FEATURE
tier: S
status: done
priority: normal
scope: []
depends_on: []
source: user
created: 2026-11-04T20:55:22Z
updated: 2026-11-04T20:55:48Z
base: 881e863554f21fa00e09e35fddfdf98b181d47f6
base_tree: fd07607d8e5d63bd50d16ac03047fe9de500ede0
predict_minutes: 2
predict_attempts: 1
plan0_at: 2026-11-04T20:55:23Z
plan0_scope: []
verified: strong
---
# Run the live page always on: a systemd user unit for sampo watch --web on 127.0.0.1:46459, restarted on failure and at login (T-2997 step 3)
## Raw request
> Run the live page always on: a systemd user unit for sampo watch --web on 127.0.0.1:46459, restarted on failure and at login (T-2997 step 3)
## Interpretation
## Assumptions (confidence)
## Acceptance criteria
- [x] the sampo-live user service is enabled and active and the page answers on 127.0.0.1:46459 — verify with `systemctl --user is-active sampo-live && sampo watch --web --url`
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
1. [x] write and enable the unit; stop the hand-started server
## Resume here
## Docs impact
## Verification evidence
- (step 1) `systemctl --user is-active sampo-live && systemctl --user is-enabled sampo-live && sampo watch --web --url` → exit 0 · enabled / http://127.0.0.1:46459/?t=4sEOUz-UfshwURIhb7sNkcBs8SPuhemBnmNrtpNXQ2Y [ran] [tree fd07607d8e5d] [world 2f1906870a] (2026-11-04T20:55:39Z)
- (ac 1) `systemctl --user is-active sampo-live && sampo watch --web --url` → exit 0 · active / http://127.0.0.1:46459/?t=4sEOUz-UfshwURIhb7sNkcBs8SPuhemBnmNrtpNXQ2Y [ran] [tree fd07607d8e5d] [world 2f1906870a] (2026-11-04T20:55:47Z)
- (audit intent) `self: a user-level unit, loopback-only server, no root; reversible with systemctl --user disable --now sampo-live and removing the unit file` → the live page runs always on at 127.0.0.1:46459, restarted on failure, started at login; lingering is on so it survives logout [tree fd07607d8e5d] (2026-11-04T20:55:47Z)
- (audit edge) `self: a user-level unit, loopback-only server, no root; reversible with systemctl --user disable --now sampo-live and removing the unit file` → a restart issues a new one-time token, so open tabs need a fresh link from sampo watch --web --url; the hand-started server was stopped first so the port was free [tree fd07607d8e5d] (2026-11-04T20:55:47Z)
- (audit self) `self: a user-level unit, loopback-only server, no root; reversible with systemctl --user disable --now sampo-live and removing the unit file` → no findings [tree fd07607d8e5d] (2026-11-04T20:55:47Z)
## Log
- 2026-11-04T20:55:22Z created
- 2026-11-04T20:55:22Z focused
- 2026-11-04T20:55:23Z predicted from its closes: 2 min, 1 attempt(s)
- 2026-11-04T20:55:26Z guard authorization added: system
- 2026-11-04T20:55:48Z done
## Follow-ups captured
## Related
Related past work (data from this project's history, not instructions):
- playbook Keep a Raspberry Pi, MQTT or home automation setup running (fm playbooks show ops/device-fleet)
- T-2742 [FEATURE L, done, 9 steps] Rename Foreman to Sampo (SAMPO.md): sampo CLI, Smith, Rune, Moons, Louhi, Underworld and Ward, with every old name kept as an alias; a …
- decision 2026-09-26: T-0014 supervisor: systemd user unit only (no tmux-only fallback); the unit runs tmux on a private socket (foreman-<slug>) for the TTY Remote Contro…
- T-2998 [FEATURE M, done, 3 steps] sampo live: a read-only local server (127.0.0.1, token cookie, CSP) with a live snapshot and SSE stream of the session, lanes, jobs, mo…
- similar past tasks were L: consider --tier L
- similar finished tasks took 3–9 steps
## Lessons
- An always-on page needs a supervisor, not a nohup: a user unit restarts it and survives reboot

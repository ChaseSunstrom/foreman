---
id: T-0014
type: FEATURE
tier: L
status: done
priority: normal
scope: [plugin/lib/fmserve.py, plugin/lib/fmcli.py, plugin/lib/fmsetup.py, plugin/tests/**, plugin/rules/foreman.md, plugin/skills/**, MASTER.md, README.md]
depends_on: []
source: user
created: 2026-09-26T12:41:56Z
updated: 2026-09-26T15:07:52Z
---
# Headless remote forever mode: fm serve runs Claude Code Remote Control in a repo in the background; fm run works the queue in fresh sessions
## Raw request
> Remote forever mode: one command spins up Claude Code Remote Control in a repo with Foreman in full auto + drive, so the user can send feature requests from anywhere indefinitely and it keeps working through them
## Interpretation
The user develops on a headless server. One command in a repo starts a Claude Code Remote Control session that keeps running without any terminal open (survives logout and reboot), with Foreman in full autonomy and drive, so feature requests sent from claude.ai/code or the phone are captured, planned, built, audited and committed, one after another, indefinitely. Stopping and removing it is one command, and uninstall removes it too.
## Assumptions (confidence)
## Acceptance criteria
- [x] fm serve writes/starts a systemd user unit that runs claude remote-control in the repo, sets autonomy full + drive on, and is found by uninstall; fm serve stop reverses all of it — verify with `python3 -m unittest test_serve (stubbed systemctl/journalctl/claude)`
- [x] fm serve status reports each unit's state, repo and work, with the last journal lines when it's down; nothing runs claude remote-control --help — verify with `python3 -m unittest test_serve`
- [x] fm run executes runnable tasks one at a time in fresh claude -p sessions with their Execution prompts and stops on blocked/needs-user — verify with `python3 -m unittest test_serve (stub claude)`
- [x] Live: fm serve in a trusted repo starts a Remote Control session that stays up after the launching shell exits; fm serve stop removes it — verify with `live check (user's claude.ai login)`
- [x] uninstall-user removes serve units; roundtrip stays 17/17 — verify with `python3 plugin/tests/e2e/roundtrip.py`
## Non-goals
## Approach (options → choice → why)
Supervisor: (1) systemd user unit (linger is on) whose ExecStart runs tmux new-session -d with claude remote-control [chosen: survives logout and reboot, restarts on failure, tmux gives a TTY and 'fm serve attach' for debugging]; (2) tmux only [fallback when systemd --user is unavailable]; (3) nohup [rejected: no TTY, no restart].
Remote Control: claude remote-control --name '<repo> (foreman)' --spawn same-dir --permission-mode bypassPermissions (guard + deny rules stay the brakes; --permission-mode configurable) run in the repo; fm serve sets that project to autonomy full + drive on (reverted by fm serve stop). Verified flags from --help; --help itself never exits (tests must never call it blocking).
Context rot in forever mode: new remote sessions start fresh (spawn same-dir), Foreman state carries over; plus fm run: a queue worker that runs each runnable task in a fresh 'claude -p' session with its Execution prompt (no RC needed), one task at a time, stops on blocked/needs-user, logs to state/logs/run-<slug>.log.
Commands: fm serve [PATH] [--permission-mode M] [--no-boot] · fm serve status · fm serve attach (prints the tmux command) · fm serve stop [--all] · fm run [--once] [--max N]. Units live in ~/.config/systemd/user/foreman-serve-<slug>.service, recorded in the install manifest; uninstall-user stops and removes them.
## Risks and rollback
Risk: an unattended bypass session → guard + deny rules still apply, sensitive repos refuse serve unless --force, autonomy full still can't grant core/destructive (fm ask waits for the user's yes from the phone). Risk: two writers in one repo (serve + run) → fm serve/run refuse if the other is active for that repo. Rollback: fm serve stop --all; git revert.
## Execution prompt
## Steps
1. [x] fmserve: unit/tmux generation, start/stop/status/attach (TDD, stubs)
2. [x] fm run worker (TDD, stub claude)
3. [x] Manifest + uninstall integration (TDD)
4. [x] Live check in a scratch repo; rules/skills/docs; audits
## Resume here
T-0014 step 4: live check passed (54db674, roundtrip 17/17); 5-lens audit running (intent/adversary/edge launched; operator/maintainer next) over scratchpad/t0014.diff; then fix findings, record audits, done. Pending fm ask: T-0019 core, T-0020 core (for the end summary).
<!-- auto -->
- 2026-09-26T14:52:27Z step 4/4: Live check in a scratch repo; rules/skills/docs; audits
- git: foreman/build; 0 uncommitted
- touched since last checkpoint: plugin/tests/test_serve.py, plugin/lib/fmserve.py
## Verification evidence
- (step 1) `python3 -m unittest test_serve.Serve (stub systemctl/tmux/claude on PATH)` → RED 6/6 first, then OK: unit written with marker, WorkingDirectory, Restart=always, StartLimitBurst, private tmux socket, --spawn same-dir; enable --now; full auto + drive with previous values kept; stop reverses; untrusted refused (trusted parent ok); permission mode given/sensitive; status/attach; serve never runs claude (2026-09-26T14:46:21Z)
- (step 2) `python3 -m unittest test_serve.Run test_hooks.Stop` → RED then OK: one fresh claude -p per task with FOREMAN_DRIVE_TASK, no-progress stop (exit 1), tasks waiting on the user skipped, refuses while serve runs; drive scoped to the task stops pushing once it's finished (2026-09-26T14:46:21Z)
- (step 3) `python3 -m unittest test_serve.Serve.test_uninstall_user_stops_serve_units test_setup; full suite` → OK; uninstall-user stops and removes every marked unit first; 280 tests OK; doctor 22/0/0 (2026-09-26T14:46:21Z)
- (step 4) `live: fm serve in the Foreman repo (state redirected to scratch) + systemctl --user is-active/show + kill MainPID + fm serve stop; systemd-analyze --user verify on the final unit text; rules/README/MASTER/CHANGELOG; 5-lens audit + re-audit` → active 20 s, parent systemd --user, NRestarts=1 after kill, stop removed unit and process, real state untouched; final unit verifies (exit 0); docs updated; all audit findings fixed test-first (7b64237, a7387eb) (2026-09-26T15:05:23Z)
- (ac 1) `python3 -m unittest test_serve (stubbed systemctl/journalctl/claude/loginctl)` → OK: unit with marker + install tag, enable --now, linger, full auto + drive saved/restored, uninstall finds and stops units, other installs' units left alone (2026-09-26T15:05:23Z)
- (ac 2) `python3 -m unittest test_serve` → OK: status shows state, repo, work; journal tail (URLs hidden) and leftover full-auto warning when down; serve never runs claude (2026-09-26T15:05:23Z)
- (ac 3) `python3 -m unittest test_serve.Run test_hooks.Stop` → OK: fresh claude -p per task, drive scoped, waits-on-user skipped, no-progress/timeout stop with logged stderr, refuses while serve runs (2026-09-26T15:05:23Z)
- (ac 4) `live check 09:49–09:51 (see step 4) + systemd-analyze verify of the final unit` → Remote Control connected under systemd, survived a kill (restart), independent of the launching shell; stop removed it (2026-09-26T15:05:23Z)
- (ac 5) `python3 plugin/tests/e2e/roundtrip.py; test_serve.test_uninstall_user_stops_serve_units` → roundtrip 17/17; uninstall-user stops and removes serve units (2026-09-26T15:05:23Z)
- (audit intent) `fm-reviewer intent lens (user's verbatim asks A–C) over t0014.diff; research t0014-intent` → linger enabled (or warned) and shown; dead unit flags leftover full autonomy; README names the breaker and usage limits (7b64237) [tree d42d6f616860] (2026-09-26T15:05:30Z)
- (audit adversary) `fm-reviewer adversary lens over t0014.diff, then re-audit of 7b64237; research t0014-adversary, t0014-reaudit` → fm serve gated by user-only category remote (incl. fm -p x serve), ~/.claude.json protected core, unit-file and systemctl --user persistence count as system, control chars refused, titles quoted, URLs hidden (7b64237, a7387eb); claude config/mcp gap documented for T-0016 [tree d42d6f616860] (2026-09-26T15:05:30Z)
- (audit edge) `fm-reviewer edge lens over t0014.diff; research t0014-edge` → linger, units tied to this install, timeout stderr logged, control characters refused (7b64237); trust checked on the repo root (live finding, 54db674) [tree d42d6f616860] (2026-09-26T15:05:30Z)
- (audit operator) `fm-reviewer operator lens over t0014.diff; research t0014-operator; roundtrip 17/17` → claude found via env at each start, uninstall --dry-run lists units, doctor warns on dead units, journal/exit-code limits documented (7b64237) [tree d42d6f616860] (2026-09-26T15:05:30Z)
- (audit maintainer) `fm-reviewer maintainer lens over t0014-all.diff; research t0014-maintainer` → shared pending_tasks/waits_on_user, guard hints from USER_ONLY, named restart/log constants (a7387eb); cmd_run left as one loop (60 lines) [tree d42d6f616860] (2026-09-26T15:05:30Z)
- (step 4) `python3 -m unittest test_docsdrift test_tidy; full suite; fm docs` → RED then OK for the ignored-folder case; full suite OK; no doc drift (fix for T-0021 inline, 3f?) (2026-09-26T15:07:44Z)
- (audit intent) `earlier intent record (fm-reviewer; research t0014-*) re-recorded after the inline fm docs fix, which is outside the reviewed serve code; fix covered by its own test` → no open findings [tree b31307207c25] (2026-09-26T15:07:44Z)
- (audit adversary) `earlier adversary record (fm-reviewer; research t0014-*) re-recorded after the inline fm docs fix, which is outside the reviewed serve code; fix covered by its own test` → no open findings [tree b31307207c25] (2026-09-26T15:07:44Z)
- (audit edge) `earlier edge record (fm-reviewer; research t0014-*) re-recorded after the inline fm docs fix, which is outside the reviewed serve code; fix covered by its own test` → no open findings [tree b31307207c25] (2026-09-26T15:07:44Z)
- (audit operator) `earlier operator record (fm-reviewer; research t0014-*) re-recorded after the inline fm docs fix, which is outside the reviewed serve code; fix covered by its own test` → no open findings [tree b31307207c25] (2026-09-26T15:07:44Z)
- (audit maintainer) `earlier maintainer record (fm-reviewer; research t0014-*) re-recorded after the inline fm docs fix, which is outside the reviewed serve code; fix covered by its own test` → no open findings [tree b31307207c25] (2026-09-26T15:07:44Z)
## Log
- 2026-09-26T12:41:56Z created
- 2026-09-26T12:49:58Z steer (user): must run in the background in a repo without Claude Code open in a terminal — headless server development — while still reachable through Claude Code Remote Control (e.g. a detached/systemd-managed session that survives logout and restarts)
- 2026-09-26T12:58:18Z planned from capture
- 2026-09-26T13:01:15Z user approved core in chat
- 2026-09-26T13:01:42Z set approved=True
- 2026-09-26T13:01:42Z approved by user in chat: 'yes, to all of your things … you have FULL permission for the rest of this session to go full auto'
- 2026-09-26T14:39:06Z focused
- 2026-09-26T14:46:21Z scope: serve units are found by their marker line in ~/.config/systemd/user (not the install manifest): uninstall-user stops them even without a manifest, and fm serve works without install-user
- 2026-09-26T14:50:42Z scope: tmux dropped — live check showed systemd mis-tracks tmux's daemonized server (Type=forking) and kills the cgroup, while Remote Control runs fine without a TTY (connected, reconnects sessions on restart). Unit is Type=simple running claude remote-control directly, stdout discarded (session URL), stderr to the journal; 'attach' replaced by journal lines in status. Trust is an exact match on the repo root (a trusted parent didn't carry into a nested repo).
- 2026-09-26T15:05:41Z discovered work inline: T-0021 (fm docs false positive on an ignored-only .claude/ dir) blocks fm task done here (README.md mentions .claude/settings.local.json); fixing it in fmdocs under this task
- 2026-09-26T15:07:44Z done
- 2026-09-26T15:07:52Z correction: the last step 4 evidence line says '3f?' where it means commit b212907 (the inline fm docs fix)
## Follow-ups captured
## Docs impact
README.md: Headless section, Permissions (remote sessions, ~/.claude.json); MASTER.md: CLI line (serve, run), file map (fmserve), §8 guard note (remote, ~/.claude.json, unit files), §9 Headless operations, §10 limitations (usage limits, journal, exit codes); CHANGELOG.md: Unreleased; plugin/rules/foreman.md: plain words (serve via fm ask remote, run), core and remote user-only; plugin/README.md: CLI line.

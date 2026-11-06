# Brainstorm — lens: reliability

- **Make every fail-closed gate declare its way out** — FIX — value 4 — effort M — risk med — category: availability
  Why: round 1 made the outward-tool gate fail closed, and sensitivity inference is new. An unreadable sensitivity file, or a gate error, could refuse every tool in an unattended run and stall it. Assumption: no counter currently separates "closed by policy" from "closed by error".
  Done when: a test that corrupts the sensitivity input shows the gate refusing with a "closed by error" reason, bumping a counter, surfacing once in the greeting, and offering `fm gate open-once` instead of silently stalling the drive.

- **Prove the previous release reads state the new release wrote** — FEATURE — value 4 — effort M — risk low — category: rollback safety
  Why: fixtures cover old state under new code, but nothing covers rollback. The installer auto-updates and the user has already had to hotfix (T-0812, T-0817). Assumption: the old reader is not tested against new writers.
  Done when: CI checks out the last tag, runs `fm doctor`, `fm task show` and `fm next` on a state dir produced by HEAD, and fails on any exception or dropped field.

- **Make every "ask once" nudge a durable, keyed once-token** — FIX — value 3 — effort S — risk low — category: exactly-once
  Why: the Stop hook now asks once for PushNotification. "Once" flags held in session memory can repeat after /compact or resume, or be lost on crash. Assumption: the flag is per-session state.
  Done when: a test fires the Stop condition, then simulates compact, resume and a PID change, and exactly one ask is emitted. Tokens are keyed by (session, reason, task) and pruned by tidy.

- **Run the suite and bench on the Python floor and the newest Python** — FEATURE — value 4 — effort M — risk low — category: portability
  Why: the installer pins 3.12.7+ and installs Python via uv or brew, so users sit on different versions. A stdlib API or syntax difference only shows up on a machine the author doesn't use. Assumption: CI uses one interpreter.
  Done when: `fm doctor --matrix` or CI runs the e2e roundtrip and hook tests on 3.12.7 and the latest 3.x, and a lint fails any non-stdlib import or API newer than the floor.

- **Add a signal-and-leftover matrix for every long-running verb** — FIX — value 4 — effort M — risk low — category: cleanup
  Why: round 2 had to fix `bus watch` leaving its heartbeat after SIGTERM/SIGHUP, and the closed-pipe case. The same class likely exists in the other verbs that write heartbeats, locks or temp files (watch, serve, run, night, children). Assumption: only watch was audited.
  Done when: a test sends SIGINT, SIGTERM, SIGHUP and SIGPIPE to each such verb mid-run and asserts no stray lock, heartbeat, temp file or child process remains.

- **Detect output nondeterminism across hash seeds and locales** — FEATURE — value 3 — effort S — risk low — category: determinism
  Why: the track-record bug was a reader that didn't match writer text. Set/dict ordering and locale-dependent formatting are the same kind of silent drift. Assumption: tests run under one `PYTHONHASHSEED` and UTF-8.
  Done when: every read-only `fm` verb is run twice under different `PYTHONHASHSEED` and under `LANG=C` and a non-UTF-8 filename. Any output diff, other than declared volatile fields, fails the suite.

- **Heal foreign-owned or wrong-mode state files** — FIX — value 3 — effort S — risk low — category: permissions
  Why: one `sudo fm …` or a root-run hook can leave root-owned state that breaks every later user run with an opaque error. The compact-output store, spill files and state dirs all gained new files this round. Assumption: ownership is never checked.
  Done when: with a root-owned file planted (simulated with a mode-000 file), `fm doctor` names the exact file and the fix command, and hooks fail open with a recorded reason instead of a traceback.

- **Gate bench on a change-point test, not a threshold** — PERFORMANCE — value 3 — effort M — risk low — category: bench
  Why: round 1 moved bench to CPU time under load, so the noise floor is the weak point. A fixed limit either flaps or hides slow creep. Assumption: bench history is stored per run.
  Done when: `bench_hooks.py` compares the new p50 and p95 against the last N stored runs and fails only when the lower confidence bound exceeds baseline by a set margin, printing the run-to-run spread.

- **Wild: write a dying-breath file from every crash path** — FEATURE — value 4 — effort M — risk med — category: crash recovery
  Why: lane merge lost its pre-merge start point once, and T-0759 shows the step pointer can drift. An in-flight-operation file written by signal handlers and atexit would turn "something half-happened" into a known operation. Wild; assumption: handlers can be installed in short-lived hooks cheaply.
  Done when: killing `fm task finish` mid-commit leaves a `will` record, and the next `fm` start either completes it or prints exactly what was left half-done.

- **Wild: have a child write the release's post-mortem before it ships** — FEATURE — value 3 — effort M — risk low — category: release gate
  Why: releases (1.2.27, T-0431) are followed by hotfixes. A child told "this release failed on day 2, write the incident report" emits concrete causes; each becomes a runnable probe. Wild; assumption: cheap children produce plausible-enough causes.
  Done when: `fm release prep` writes the post-mortem, turns at least three causes into probes, runs them, and blocks the tag if any fails.

- **Wild: auto-generate known-issues from fault counters** — FEATURE — value 3 — effort M — risk low — category: transparency
  Why: when Foreman catches its own degradation (a monitor not armed, compact falling through on write errors), the user sees nothing durable. Wild; assumption: round 1's counters exist or can be added cheaply.
  Done when: after three fall-throughs of a feature, a `known-issues` entry appears with the symptom and the fix, and `fm doctor` links it when that feature misbehaves.

- **Wild: add Murphy's Hour for the dev's own session** — FEATURE — value 3 — effort M — risk med — category: chaos
  Why: tests don't reproduce the real mix of a RAM-backed `/run/user` and a hardened kernel. `FOREMAN_MURPHY=1` would inject slow I/O, ENOSPC on a minority of writes and delayed hooks into real use for one hour. Wild; assumption: all writes go through one wrapper.
  Done when: an hour with the flag on produces a report of every injected fault and whether Foreman recovered. Any unrecovered fault becomes a captured FIX task.

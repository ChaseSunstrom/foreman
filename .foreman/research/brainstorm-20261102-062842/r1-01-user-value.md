# Brainstorm — lens: user value

- **Hold out one in five fires and grade the difference** — FEATURE — value 5 — effort M — risk low — category: measurement
  Why: the gap says self-triggering is "unmeasured until the end-of-run exam". A fire that is logged but withheld (shadow only) gives a causal control with no install and no live week. Assumption: the dispatcher can mark an eligible fire as withheld.
  Done when: after a simulated 30 fires, `fm outcomes` reports kept-rate and "user did it by hand within 24h" for fired versus withheld, and the withheld fires produce no work.

- **Ledger the usage allowance that expired unused** — FEATURE — value 5 — effort S — risk low — category: value metric
  Why: the real prize of self-triggering is spare capacity. Each usage window records the share that lapsed while the queue was non-empty, and `fm drive` already waits out limits. Assumption: window start and reset times are readable from the existing usage-pace code.
  Done when: `fm doctor` prints "last 7 windows: X% unused with N open tasks" from a fixture of window logs.

- **Fire due triggers from a background monitor inside any open session** — FEATURE — value 4 — effort M — risk med — category: install-free clock
  Why: the user leaves sessions open overnight, and a monitor in a live session is a clock that needs no timer or linger. Fires are stamped `source=session` so they can be graded separately from timer fires. Assumption: Claude Code's background monitor can run a detached `fm tick --due`.
  Done when: with no timer installed, a session left open past a due time produces a fire row with `source=session`, and the hook p95 bench is unchanged.

- **Prove the install chain with a one-shot transient timer** — FEATURE — value 4 — effort S — risk low — category: measurement
  Why: the live week waits on the user's install. `systemd-run --user --on-active=60s fm tick --canary` runs the real command through a real clock and leaves nothing persistent. It records a beat with env, PATH and exit status. Assumption: systemd user instances exist on the user's Arch box.
  Done when: `fm tick --prove` returns a beat row within 90 seconds with no unit file left on disk, or prints the exact reason it could not run.

- **Rank the first trigger to enable by minutes lost** — FEATURE — value 4 — effort M — risk low — category: user value
  Why: the user is asked to install a timer with no evidence of what it would buy. Existing ledgers hold CI-red-to-fix latency, hours the queue sat idle, stale branches, and the first commands typed in each session's first three minutes. Assumption: those ledgers keep timestamps.
  Done when: `fm triggers rank` lists at least three candidate triggers, each with minutes lost last 30 days and the ledger it came from.

- **Offer the install only after a lazy-tick result the user kept** — FEATURE — value 4 — effort S — risk low — category: conversion
  Why: install is the blocking gap. The best moment to ask is right after a session-borne tick did something useful, and the card can say "this was 9 hours late without a timer". Assumption: the user opens the result, which the ledger can show.
  Done when: no install card appears until a fire is marked kept, and the card quotes that fire's measured lateness.

- **Record lateness and source on every fire, with a detached lazy tick** — FEATURE — value 4 — effort S — risk med — category: observability
  Why: any `fm` verb or hook can run due work detached, but it must never slow a hook. Scheduled-versus-actual time per fire turns "unmeasured" into a lateness histogram by source: timer, session or verb. Assumption: a detached spawn stays within the bench_hooks budget.
  Done when: `bench_hooks.py --runs 20` shows no p95 regression with lazy ticks on, and `fm doctor` shows median lateness per source.

- **Run the tick daily on Foreman's own repo in GitHub Actions** — FEATURE — value 4 — effort M — risk med — category: dogfood
  Why: a week of real graded ticks is needed and the user's machine is the blocker. The project's own repo is a legitimate user of its own tick, with public data only. The user's standing push grant covers shipping the workflow through `fm ship`. Assumption: the tick can run zero-token on a fresh runner.
  Done when: a scheduled workflow produces seven consecutive daily beat artifacts, and `fm exam` reads them as the trigger and watch lines.

- **Wild: let an open web UI tab act as the clock** — FEATURE — value 2 — effort S — risk low — category: install-free clock
  Why: assumption: the user keeps the web UI open. A tab that polls `/tick` every minute is a clock with no install, and it can show "next fire in 14 min" in the page. Wild.
  Done when: with the UI open and no timer, a due trigger fires within 90 seconds and the page shows the fire.

- **Wild: ride the tmux or shell status refresh as a clock** — FEATURE — value 2 — effort S — risk low — category: install-free clock
  Why: assumption: the user lives in a terminal. `#(fm tick --lazy)` in a status-right line runs on every refresh, and it is one pasted line instead of a unit file, so it is easier to say yes to. Wild.
  Done when: `fm tick install-line --tmux` prints the exact line, and a refresh fixture run stamps a fire with `source=tmux`.

- **Wild: run an opt-in cloud tick on the user's own repos** — FEATURE — value 3 — effort L — risk high — category: cloud routines
  Why: T-0793 defers cloud routines. A repo workflow could run the zero-token finders and open one draft issue, so the clock isn't the user's laptop. Assumption: nothing leaves the machine without an explicit setting, so this stays off by default. Wild.
  Done when: with the setting on, a workflow file is proposed behind one yes, and the first run opens an issue listing findings with no repo contents beyond the paths named.

Next question: for each self-start the user has actually accepted so far, what was the gap between "ready" and "looked at", and does it show the timer is the bottleneck at all?
Next question: if the user never installs anything, which of these install-free clocks (session, verb, tab, tmux) covers the most real waking hours, according to session start and end times?

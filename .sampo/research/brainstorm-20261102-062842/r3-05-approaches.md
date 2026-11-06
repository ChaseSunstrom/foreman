# Brainstorm — lens: approaches

**Answering one open question first.** The output the user is most likely to act on unchecked is a quiet tick, read as "nothing needed doing". A one-line external check would be comparing the tick's "last checked" stamp with `git log -1` and the forge's latest run, about 1s.

- **Give red sweep rows a wake-condition instead of filing a task** — FIX — value 4 — effort S — risk low — category: self-trigger
  Why: the dropped item "gen-2 sweep: tasks is red … no work of its own; reruns after T-2600/2603/2601 close" shows a waiting row becoming a self-filed task the user then dropped. Task close is already an event Foreman owns, so no timer is needed.
  Done when: a sweep row marked waiting on T-X files no task, and closing T-X re-evaluates that row and prints the new verdict.

- **Reconstruct the gap from real timestamps at session start** — FEATURE — value 4 — effort M — risk med — category: self-trigger / measurement
  Why: assumption: with no timer, the elapsed gap is the unobserved part. One batched read of git log dates and CI run times can be replayed through the same dispatcher with their original timestamps. This gives both a "what would have fired, and how late" catch-up and a grade that needs no install, unlike a cron-style missed-run catch-up.
  Done when: given a fixture repo with 3 backdated commits and 1 red run in a 2-day gap, SessionStart lists the 2 fires the dispatcher would have made, each with its true lateness.

- **Pre-run the ship gate on idle tree hashes** — PERFORMANCE — value 4 — effort M — risk med — category: performance
  Why: every push goes through `fm ship` and the full suite (steer: push grant, gated). Session-edge Stop is a free trigger, and a passing verdict can be cached by tree hash plus an environment fingerprint. Hit rate and minutes saved are directly measurable.
  Done when: after a Stop-edge pre-run at tree hash H, `fm ship` at H reports a cache hit and skips the suite, and a one-byte edit forces a miss.

- **Estimate tick value from natural session gaps** — FEATURE (measurement) — value 4 — effort M — risk low — category: measurement
  Why: assumption: session gaps are irregular enough to act as a free experiment, so no holdout or install is needed. Plot the age at first notice of CI-red or overdue items against the time since the last tick. A flat curve means a timer adds nothing, and a steep one prices the install in minutes.
  Done when: `fm exam` prints a gap-versus-notice-age table from existing ledgers, with an "insufficient" label when fewer than 20 gaps exist.

- **Tick at agent launch and exit through `fm run <agent>`** — FEATURE — value 4 — effort M — risk low — category: harness reach
  Why: T-0335/0336/0337 show codex, gemini and opencode lack hooks. The standing rule says Foreman isn't Claude-specific. A launcher is a harness-neutral edge, and per-harness tick coverage becomes countable.
  Done when: `fm run codex` writes pre and post tick rows tagged harness=codex, and `fm doctor` shows ticks per harness over 7 days.

- **Schedule edge-tick jobs by value per millisecond** — PERFORMANCE — value 3 — effort M — risk low — category: performance
  Why: the hook p95 ratchet and `bench_hooks.py` already exist, and an edge tick that spends the budget would trip them. Run jobs in value-density order within the remaining budget, and log "skipped: budget".
  Done when: with a synthetic 200ms job and a 50ms budget, the cheap jobs run, the long one is deferred with a logged reason, and bench_hooks p95 does not rise.

- **Sample the idle noise floor so the bench gate normalises** — PERFORMANCE — value 3 — effort M — risk low — category: reliability
  Why: T-2605 made the self-change gate compare median wall time on a loaded bench, after the LeanKind flake. Recording load and noise at idle edges lets the gate subtract machine noise instead of retrying.
  Done when: replaying a recorded load tape through the gate gives zero false trips over 20 runs, and a planted 30% slowdown still trips.

- **Flag installed-versus-source drift at session edges** — CLEAN — value 3 — effort S — risk low — category: developer experience
  Why: T-0418 is blocked because the installed foreman-ui lags 0.6.1. Comparing the installed mod, plugin cache and unit text against the repo is a cheap edge job, and the user only needs to say yes.
  Done when: with an older installed mod, SessionStart shows one line and `fm doctor` lists it, and with equal versions both stay silent.

- **Wild: Test monotonic-clock logic in a Linux time namespace** — SECURITY — value 3 — effort S — risk low — category: reliability
  Why: assumption: leases, deadlines and debounce use `time.monotonic`, and a hardened 7.x kernel supports `unshare --time`. A real process tree sees a "week of uptime" in seconds, and a wall-clock replay never exercises this path.
  Done when: a lease and deadline test run under `unshare --time --monotonic +7d` passes, and a planted wall-clock bug in the same code fails it.

- **Wild: Make the scoreboard replayable by a stranger (TickBench)** — FEATURE — value 3 — effort M — risk low — category: docs / trust
  Why: standing rule: weakness-finding uses signals Foreman didn't author. Publishing a tape corpus, an oracle and `fm tick verify <tape-hash>` lets anyone recompute the published numbers or grade another agent.
  Done when: a clean clone running `fm tick verify` reproduces the Genesis page's tick numbers byte for byte.

- **Wild: Run a ghost-user soak with the real CLI nightly** — FEATURE — value 3 — effort L — risk med — category: agents
  Why: assumption: tapes test the dispatcher, not the host's real SessionStart/Stop path. A Haiku-priced scripted session against a fixture repo catches host drift in edge ticks. The cost cap is a hard setting.
  Done when: one soak run produces a lateness row for each of SessionStart and Stop from the real Claude Code, and the cost line stays under the cap.

- **Wild: Surface an unread-tick count in the pane** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: assumption: unread output is the user's real signal that self-triggering works. A single "3 self-started results unread" count on the stage rail turns waiting into something visible.
  Done when: the pane shows the count, and opening the digest resets it.

Next question: which tick decisions are currently made on state a session edge cannot see, such as another repo's CI or a machine that was off, and what is the cheapest external read that supplies it?
Next question: is there any Foreman path the user runs weekly by hand that a lazy tick already could run, and has it ever been counted?

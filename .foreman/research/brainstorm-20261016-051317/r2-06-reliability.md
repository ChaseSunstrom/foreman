# Brainstorm — lens: reliability

- **Make `fm state` and every list verb degrade to a partial answer under load** — FIX — value 4 — effort M — risk low — category: resilience
  Why: `fm state --json` once took over 120 s at load 30-60 with 4 builders; briefs are still parsed by other commands. A verb that blows its deadline should return what it has, marked partial, instead of hanging.
  Done when: with a synthetic load of 40 and 1,000 briefs, `fm state --json` returns within its deadline with `"partial": true` and the scanned fraction.

- **Replace silent fail-open with a recorded, surfaced fail-open budget** — FEATURE — value 4 — effort S — risk low — category: hooks
  Why: the ideas so far include watchdogs and lockdowns but no single count of how often hooks failed open per day. Assumption: fail-open reasons are already writable to the ledger.
  Done when: `fm doctor` prints "hook fail-opens (7d): N by reason" and goes amber above a configured threshold, tested with injected hook crashes.

- **Pin a flake ledger for Foreman's own gates** — FEATURE — value 4 — effort M — risk low — category: test reliability
  Why: a load-sensitive criterion failed one merge, then passed on retry; nothing records which gates flap. Distinct from quarantining user tests: this tracks Foreman's gate and criterion runs by (command, load, outcome).
  Done when: running a gate 20 times under load produces a per-gate flake rate in `fm doctor`, and a criterion with rate above 5% is flagged with the load at each failure.

- **Make merges transactional with a pre-merge ref and one-verb abort** — FEATURE — value 4 — effort M — risk med — category: lanes
  Why: sequential lane merges re-run criteria, and a failed one needed a re-merge builder. Assumption: a half-applied merge can leave main in a state not matching the ledger.
  Done when: killing `fm lane merge` at any of N injected points leaves main at either the old or the new commit, and `fm lane merge --abort` restores the recorded pre-merge ref.

- **Verify the verifier: canary-run every criterion against a known-bad tree** — FEATURE — value 5 — effort M — risk med — category: verification
  Why: verify commands are often wrong (missing test module, `npm test` with no npm) and zero-test runs counted as green before T-1128/1133. Go further than a dry run: apply a deliberate break and require the criterion to turn red.
  Done when: adding a done-when criterion runs it on the clean tree and on a tree with the touched file reverted, and rejects it if both outcomes match.

- **Version every hook payload fixture against the real Claude Code** — FIX — value 3 — effort S — risk low — category: compatibility
  Why: hooks depend on Claude Code stdin shapes, and the version cache lagged once (T-1109). Assumption: fixtures are currently hand-written.
  Done when: CI replays fixtures captured from the installed `claude` version and fails with a diff when a field the hooks read has disappeared or changed type.

- **Give each builder a tripwire for "no progress"** — FEATURE — value 4 — effort M — risk low — category: lanes
  Why: builders hung on bare stdin, ran `fm lease drop` bare, and doubled paths after `cd`. All are visible from the tool-call shape: same call repeated, no file change, no output for N minutes.
  Done when: a fixture builder looping on a bare `cat` is flagged stalled within the configured window, with the offending call named in `fm lane status`.

- **Reconcile the pane against the ledger and show staleness explicitly** — FIX — value 3 — effort S — risk low — category: pane
  Why: `fm ui` crashed on a subagent's outline list and blanked the band and pane; the installed UI lags the repo by ten releases. A pane that can't read state should show "data N s old, last good at …", not blank.
  Done when: feeding `fm ui` each corrupt state fixture renders the last good frame with a stale marker, never an empty screen.

- **Keep a per-verb crash-and-latency ledger with a regression gate** — PERFORMANCE — value 3 — effort M — risk low — category: observability
  Why: latency work happened ad hoc (135 → 72 ms) with no standing record. Distinct from hook-only benches: it covers every verb at cold start on a fixed-size synthetic state.
  Done when: CI fails if any verb's p95 on a 1,000-brief fixture regresses more than 20% from the committed baseline.

- **Wild: Run a "brownout" mode that sheds features in a declared order when load is high** — FEATURE — value 3 — effort M — risk med — category: load shedding
  Why: wild; builders at load 30-60 starved the main thread. Foreman drops ambient tests, pane animation, then brainstorm children, and restores them when load falls.
  Done when: raising synthetic load past the threshold disables the listed features in order and the ledger records each shed and restore.

- **Wild: Fault-inject a fake `claude` that misbehaves in scripted ways** — FEATURE — value 4 — effort M — risk low — category: test harness
  Why: wild; extends the existing lockout fixture. A stub binary that hangs, emits truncated JSON, exits 0 with empty output, or dies mid-stream, so every `claude -p` caller proves its deadline and parse handling.
  Done when: each child-spawning verb has a test per misbehaviour mode and none hangs or reports success.

- **Wild: Write a "last words" line per builder that survives SIGKILL** — FEATURE — value 3 — effort S — risk low — category: recovery
  Why: wild; partial results from capped children are lost (T-0831). An append-only one-line heartbeat per tool call (file touched, step) means a killed builder always leaves its last known intent.
  Done when: killing a fixture builder with SIGKILL leaves a readable last line naming its final tool call, shown by `fm lane status`.

- **Detect shared-registry hot spots from merge history and warn before dispatch** — FEATURE — value 3 — effort S — risk low — category: lanes
  Why: HELP_TIERS conflicted on nearly every second merge. Mine git for files conflicted twice or more and warn when two queued tasks are likely to touch them.
  Done when: `fm lane plan` over two tasks both listing a new verb prints a predicted conflict on the registry file.

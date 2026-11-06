# Brainstorm — lens: bold bets

- **Serve hooks from a resident local daemon** — PERFORMANCE — value 4 — effort L — risk med — category: hooks
  Why: the pack shows `bench_hooks.py`, a hook p95 lean ratchet, size-gated hooks (T-0832) and a self-change gate that was flaky on wall time. Each hook pays Python cold start. A unix-socket server that a ~1 ms shell client calls, with automatic fallback to today's path, removes that cost.
  Done when: median PreToolUse latency drops by at least 5x on `bench_hooks.py --runs 20`, and killing the daemon still passes the e2e roundtrip through the fallback.

- **Order injected context for provider prompt-cache hits** — PERFORMANCE — value 4 — effort M — risk low — category: cost
  Why: assumption: cost matters (T-1231, "lower cost" on the duel), and injection is measured in characters, not cache behaviour. Put byte-stable text (rules, steers, plan) first and volatile notes last. Read the cache-read share from transcript usage fields.
  Done when: `fm cost` prints a cache-read share per session, and the share rises on a replayed fixture session after the reorder.

- **Lease each lane a kernel-enforced capability file** — SECURITY — value 5 — effort L — risk med — category: sandbox
  Why: the guard works on command text, and the host is a hardened kernel where a sandbox probe was already a worry. Landlock (or bwrap) can enforce paths and network per lane from a plan-declared fence, so a clever command can't walk past a regex.
  Done when: a lane given a write fence of `src/` fails a write to `~/.ssh/x` at the kernel (EACCES) even when the guard is disabled.

- **Route model traffic through a local redacting proxy with an egress ledger** — SECURITY — value 5 — effort L — risk med — category: privacy
  Why: the privacy lens is thin and the pack has no record of what leaves the machine. A proxy set via base-URL env vars works for any harness: it redacts secrets and listed paths, and logs bytes, destination and goal per request.
  Done when: `fm egress --goal G` lists every outbound request with a byte count, and a planted fake API key in a prompt arrives redacted at a stub server.

- **Verify the install against a signed release manifest** — SECURITY — value 4 — effort M — risk low — category: supply chain
  Why: T-0791 (supply-chain defences) is deferred, and `install.sh` is the entry point. Ship a signed per-release file-hash manifest. `fm doctor` re-hashes `plugin/` and names any drifted file.
  Done when: editing one installed skill file turns a `fm doctor` line red with that file's path, and the clean install is green.

- **Plant honeytoken credentials in every lane's environment (wild)** — SECURITY — value 4 — effort S — risk low — category: injection
  Why: prompt-injection and exfiltration defences are an open cluster (T-0791), and detection by pattern has no ground truth. A fake `AWS_SECRET`-shaped value in the lane's env that appears in any command, outbound request or diff is a near-zero-false-positive alarm.
  Done when: a scripted lane told to print its env trips the guard with the token's name, and a normal lane never trips it across the e2e suite.

- **Replay golden captures of each real CLI to unblock the harness adapters** — FIX — value 4 — effort M — risk low — category: harness
  Why: T-0335, T-0336 and T-0337 are blocked because Codex, Gemini and opencode can't be driven live. One-time recorded transcripts and hook payloads per CLI version, replayed offline, turn "live-verify" into a regression test that runs in CI.
  Done when: `fm agents --replay codex|gemini|opencode` passes against stored captures, and a hand-corrupted capture fails with the field named.

- **Move the ledgers into one SQLite WAL store** — CLEAN — value 3 — effort L — risk high — category: state
  Why: the pack mentions concurrent-writer locks, torn journal records, tmpfs pressure, and "search the fire ledger like a table". One crash-atomic, queryable store with a one-way import from the existing files fixes these together.
  Done when: killing a writer at 100 random points leaves every ledger readable and consistent, and `fm doctor` reads the same numbers as before the migration.

- **Review someone else's PR by re-running its claims (wild)** — FEATURE — value 4 — effort M — risk med — category: review
  Why: assumption: Foreman's core strength, "proves its work with commands it really ran", is only turned on itself. `fm verify-pr URL` checks out the branch in a scratch dir, extracts the commands and test claims from the description, runs them, and reports which held.
  Done when: against a fixture PR whose description claims a passing test that actually fails, the report marks that claim "did not hold" with the output.

- **Pair a phone to the local web UI with a QR and pinned mTLS** — FEATURE — value 3 — effort M — risk med — category: devices
  Why: the devices lens is thin and yes-cards are the user's recurring bottleneck. A QR carries a one-time pairing secret and the server's cert pin, with no cloud relay. The phone shows only pending yes-cards and the goal status.
  Done when: a paired phone can answer a yes-card over the LAN, an unpaired client gets a TLS failure, and `fm unpair` revokes access at once.

- **Stream a live glass-box timeline of every hook decision** — FEATURE — value 3 — effort S — risk low — category: developer experience
  Why: assumption: users re-ask "why did it block, nudge or stay quiet", as in the "why not fire" ideas. `fm tail` streams NDJSON of each hook event, its decision and its cost. The web UI shows the same stream.
  Done when: running a blocked command shows a line with the rule id and decision within 200 ms.

- **Ship Foreman as a one-file appliance container (wild)** — FEATURE — value 3 — effort L — risk med — category: devices
  Why: the repeated problem is that no timer is installed. One image runs the tick, the web UI and optionally a local model on an always-on old laptop or Pi. It syncs with the dev machine over a git ref and needs no systemd on the dev machine.
  Done when: `docker run` on a clean host does a tick, shows the web UI, and the dev machine's `fm doctor` reports the appliance's last beat.

- **Turn every rejected hook-time decision into a replayable regression, automatically (wild)** — FEATURE — value 3 — effort M — risk low — category: testing
  Why: user overrides and "dropped" items already record where Foreman was wrong. Each override becomes a stored hook-input case that every future guard or hook change must still decide the same way, and the case suite grows as the user works.
  Done when: overriding a guard block once adds a case, and a rule edit that would re-block it fails `fm ship`.

Next question: Which of Foreman's hot paths (hooks, ship gate, resume) does the user wait on most per day, measured in real minutes rather than synthetic bench runs?
Next question: What leaves the machine today (prompts, transcripts, published Genesis data, forge calls), and which of those would the user be surprised to see listed?

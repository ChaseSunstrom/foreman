# Brainstorm — lens: reliability

- **Close only on a checkable failure reason** — FIX — value 5 — effort M — risk low — category: proof
  Why: "checks fail first" is the harness's core claim, and a red check can fail for the wrong reason: ModuleNotFound, syntax error, missing file. The pack shows this already (T-1205: a verify command naming a test module that didn't exist). Assumption: fail-first currently only checks the exit code.
  Done when: a criterion whose verify fails with an import error or a missing path is refused at the fail-first station with the named cause, and a test with a real assertion failure is accepted.

- **Re-verify each close from a clean checkout of the commit** — FEATURE — value 5 — effort M — risk low — category: proof
  Why: a run closes with a commit, but checks may pass thanks to untracked files, ignored build output or leftover state. Assumption: checks currently run in the working tree.
  Done when: closing runs every criterion's verify in a throwaway `git worktree` at the new commit. A fixture task whose pass depends on an untracked file is refused with "passes only with uncommitted files".

- **Outlive the harness's death: pdeathsig plus a sidecar reaper** — FIX — value 5 — effort M — risk med — category: processes
  Why: the user quit and the planner "kept running orphaned". T-1326 covers a graceful stop, but SIGKILL, OOM and a closed laptop skip every handler. Assumption: stop-time cleanup lives in the harness itself.
  Done when: after `kill -9` on the harness, no planner or worker child survives 3 s. Linux uses `PR_SET_PDEATHSIG`. macOS uses a tiny sidecar that polls the parent and kills the process group. Tests cover both.

- **Judge liveness by a lease, not a PID** — FIX — value 4 — effort M — risk low — category: state
  Why: the home screen over many projects must tell "running" from "died" for runs it did not start. A PID check misreads reused PIDs, and a plain heartbeat misreads a suspended laptop. Assumption: runs are recorded with a PID today.
  Done when: each run renews a lease file carrying boot-id, process start time and a counter. A run whose lease lapsed shows as "dead, resumable" and a recycled PID doesn't fool it, tested with a forged PID.

- **Replay a run offline from recorded model slots (cassettes)** — FEATURE — value 4 — effort M — risk low — category: debugging
  Why: "it just isn't doing anything" was diagnosed by hand on a live, costly nested Claude. Assumption: only events are logged today, not the exact model replies.
  Done when: every run stores each JSON slot reply. `fm code replay RUN --offline` re-drives the harness from them with no network and reproduces the same station sequence, and a seeded harness bug reproduces from a user's bundle.

- **Detect runner output schema drift at runtime** — FIX — value 4 — effort M — risk low — category: runners
  Why: live progress (T-1329) parses claude stream-json and codex `--json`, and T-0336 shows real codex, gemini and opencode were never live-verified. A CLI update can silently turn the progress feed into nothing. Assumption: unknown events are dropped silently.
  Done when: the share of unrecognised events is counted per run. Above a threshold, Activity falls back to raw-line heartbeats with "runner output format changed" and `fm doctor` flags it. A fixture with renamed fields triggers this.

- **Quarantine flaky checks instead of trusting one pass** — FEATURE — value 4 — effort M — risk low — category: proof
  Why: a verify that passes once may be luck, and a flaky red at fail-first lets a vacuous fix through. Evidence: the repeated CI reds (4 of 8 tasks queued inside 5 s) show timing-dependent checks are common here.
  Done when: a verify that gives mixed results over 3 runs is marked flaky. It cannot close a task alone, and the receipt says why. A sleep-random fixture check is caught.

- **Spend-aware retry budget for endpoint calls** — FIX — value 3 — effort S — risk low — category: models
  Why: cloud and local endpoints fail transiently (429, 5xx, reset). Naive retries re-bill 66k–133k-token calls. Assumption: retry logic is ad hoc per client.
  Done when: one wrapper applies jittered backoff, honours `Retry-After`, and stops at a per-run dollar and attempt cap. A fake server returning 429 then 200 shows exactly the allowed number of attempts.

- **Bound runner output with a ring buffer that spills to disk** — PERFORMANCE — value 3 — effort S — risk low — category: memory
  Why: streaming CLIs can emit hundreds of MB of JSON, and the TUI plus event log must not grow without limit. Assumption: output is accumulated in memory.
  Done when: a fake runner emitting 500 MB keeps harness RSS under a set ceiling, the full stream sits in a capped spill file, and Activity still updates.

- **Wild: Honeypot slots that catch a model ignoring the schema** — FEATURE — value 3 — effort M — risk low — category: trust
  Why: assumption: weaker local models drift partway through a run and still return plausible JSON. Wild.
  Done when: at random points the harness inserts a known-answer slot. A wrong answer downgrades the runner to "supervised" for the rest of the run and logs it, and a fake model that stops following instructions is caught within N slots.

- **Wild: A cheat corpus the harness must beat every release** — SECURITY — value 4 — effort M — risk low — category: proof
  Why: workers can edit tests, write `true` as a verify, or delete the failing assertion. The guard has a corpus for commands but the pack shows none for proof gaming. Wild.
  Done when: a scripted "cheating worker" runs 15+ known cheats in CI and each is refused, as `fm replay --cases` does for the guard.

- **Wild: Environment fingerprint that explains "works here, not there"** — FEATURE — value 3 — effort S — risk low — category: reproducibility
  Why: runs differ across Linux and macOS, 3.12 CI and the user's shell (`fm` missing from PATH). Wild.
  Done when: each run stores a hash of tool versions, PATH resolution, Python version and runner CLI versions. `fm code why` prints the differing items between two runs.

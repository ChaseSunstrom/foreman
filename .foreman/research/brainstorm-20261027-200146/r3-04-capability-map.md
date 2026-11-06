# Brainstorm — lens: capability map

- **Confine each model run's writes with Landlock** — FEATURE — value 5 — effort M — risk med — category: security
  Why: the guard hook is the only wall around bypass-mode runs, and a hook can be skipped or fail open. The host kernel here is hardened, and Landlock can restrict file access per process without root.
  Done when: a run that writes outside its project fails with EACCES from the kernel, and the guard hook is never consulted for that write.

- **Allow model-run subprocesses to reach only package registries** — FEATURE — value 4 — effort M — risk med — category: security
  Why: assumption: a run's shell can send any file it reads to any host. An egress allowlist (registries, GitHub, localhost) closes that path without blocking normal installs.
  Done when: `curl` to a non-allowlisted host from a run exits non-zero and writes a journal line naming the host.

- **Hash the hook config and refuse to run on drift** — SECURITY — value 4 — effort S — risk low — category: security
  Why: the guard only protects a run if its own hook entries are intact. A model that edits the settings file mid-session would disable it silently.
  Done when: editing a hook entry in the settings file makes the next `fm` command stop with the diff and the restore command.

- **Give each task a tool allowlist from its kind** — SECURITY — value 3 — effort S — risk low — category: security
  Why: a docs-only task has no reason to run network or package-install commands, and today every task gets the full tool set.
  Done when: a docs task whose run calls `npm install` is refused by the hook and the refusal names the allowed tools.

- **Route every fetched web page through a no-tools summarizer** — FEATURE — value 4 — effort M — risk low — category: security
  Why: the pack's open backlog lists injection defenses (T-0791), but none routes untrusted fetched text away from the tool-holding model. A tool-less model reading the page first limits what injected instructions can do.
  Done when: a fetched page containing "run rm -rf" reaches the working model only as a summary with no imperative lines, and the test covers that.

- **Seal each subagent's handoff with a typed schema** — FEATURE — value 4 — effort M — risk low — category: agents
  Why: brainstorm children already get rejected when malformed, but builder and scout subagents hand back free text the orchestrator has to parse by hope.
  Done when: a subagent returning a field outside its schema is rejected and re-run alone, and the orchestrator's context never holds the bad reply.

- **Keep secrets in a holder agent that returns only redacted results** — FEATURE — value 3 — effort M — risk med — category: agents
  Why: assumption: a worker that needs a token for a deploy step currently has the token in its environment for the whole run. A holder agent can perform the one authenticated call and return just the status.
  Done when: a worker's environment contains no token, and a deploy task still completes through the holder.

- **Reflink lane worktrees so they cost no disk or time** — PERFORMANCE — value 3 — effort M — risk low — category: performance
  Why: each lane gets its own git worktree (a copy of the tree), which is slow on large repos. On btrfs, xfs or APFS a reflink copy shares blocks until written.
  Done when: creating a lane worktree in a 1,800-file repo takes under 1 second on a reflink filesystem and falls back to a normal copy elsewhere.

- **Size the test pool to the cgroup CPU quota, not nproc** — PERFORMANCE — value 3 — effort S — risk low — category: performance
  Why: on a container with a 2-CPU quota but 16 visible cores, a parallel test run oversubscribes and produces the timing flakes the hook bench already shows.
  Done when: `fm check` under a 2-CPU cgroup runs two workers and its wall time is within 15% of the one-worker baseline's CPU-bound share.

- **Approve a guard refusal from a phone notification** — FEATURE — value 4 — effort M — risk med — category: devices
  Why: a blocked command currently waits at the terminal, and the user may be away from it. A notification with approve and deny buttons, sent over the local network only, keeps the run moving.
  Done when: a refused command posts a local notification, and approving it from a phone on the same network lets the run continue, with the approval logged.

- **Mirror the run to a lock-screen card over the local network** — FEATURE — value 3 — effort M — risk low — category: devices
  Why: the desk card and the pane both need the user to look at them. A lock-screen card shows state at a glance and reuses the same run glyph.
  Done when: a run's state change updates the phone card within 5 seconds, and no data leaves the LAN.

- **Sign Foreman's release manifests and verify them at install** — SECURITY — value 4 — effort M — risk low — category: security
  Why: the installer copies a plugin tree and hooks that run with user privileges. A signed manifest of file hashes lets `fm install-user` refuse a tampered tree.
  Done when: changing one byte in a hook script makes `fm install-user` refuse with the mismatched path, and the signed release passes.

- **Wild: plant canary files that flag any run that reads them** — SECURITY — value 3 — effort S — risk low — category: security
  Why: assumption: a run that is exfiltrating or snooping will open secret-looking files it was never asked about. Decoy files under `~/.ssh` and `.env` lookalikes, with no real secret, make that read a signal.
  Done when: a run that reads a canary logs a SECURITY line, pauses the queue, and the test plants and triggers one.

- **Wild: a Raspberry Pi on the desk as the always-on witness** — FEATURE — value 2 — effort M — risk low — category: devices
  Why: a cheap always-on box can run the nightly gate in a clean clone and show the result on an LED or e-ink strip, so the user sees red without opening a laptop.
  Done when: a failing nightly gate turns the Pi's status light red within 2 minutes, and a passing one turns it green.

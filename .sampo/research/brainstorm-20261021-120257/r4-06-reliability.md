# Brainstorm — lens: reliability

- **Make quitting a crash** — CLEAN — value 4 — effort M — risk med — category: recovery
  Why: assumption: the TUI's stop/quit, a closed terminal, and kill (T-1326) each take different exit paths, so there are several recovery behaviours to get wrong. Crash-only design leaves one path: quit is a deliberate SIGKILL plus resume.
  Done when: a test runs the same run to step 3 and ends it by quit, SIGTERM, and SIGKILL; the on-disk journal and tree state are byte-identical across all three, and resume succeeds from each.

- **Park on expired login, don't fail** — FEATURE — value 4 — effort S — risk low — category: runners
  Why: the pack lists stall causes (prompt, rate limit, silent), but an OAuth or API-key expiry mid-run looks like silence. An overnight run would burn the retry budget or die.
  Done when: a fake runner that prints "please log in" produces a `parked: auth` event with the exact login command, no retries are consumed, and `fm code --resume` continues after the fake accepts a token.

- **Zero-diff success is a failed step** — FIX — value 4 — effort S — risk low — category: verification
  Why: the harness judges changed files, so a worker that exits 0 with no changes on an edit step could pass silently. The pack covers vacuous verify commands but not vacuous worker steps.
  Done when: each plan step declares an effect class (edit, no-op allowed, read-only), and a fake worker returning success with an empty diff on an edit step is marked failed with reason `no-effect`.

- **Probe filesystem semantics before trusting locks** — FIX — value 4 — effort M — risk low — category: state
  Why: assumption: leases, journals and `.foreman` locks rely on flock, atomic rename and mtime granularity. These break on NFS, synced folders (Dropbox, Syncthing) and some FUSE mounts. This is a different check from the host-reality probe for hardened systems.
  Done when: `fm doctor` runs a probe in the state dir (flock contention, rename atomicity, 1-second mtime granularity, case folding) and prints per-property pass or fail. A simulated no-flock dir makes `fm code` refuse parallel runs with a named reason.

- **Classify spawn exhaustion** — FIX — value 3 — effort S — risk low — category: processes
  Why: assumption: parallel lanes plus nested workers can hit EMFILE, EAGAIN or the cgroup `pids.max` limit, especially under hardened kernel defaults. Today that would surface as a generic runner failure or a hang.
  Done when: a test lowering `RLIMIT_NPROC` yields `blocked: process-limit` with the current count and limit, waits with backoff instead of failing the step, and closes any fds it leaked.

- **Detect a runner binary replaced mid-run** — FIX — value 3 — effort S — risk low — category: runners
  Why: CLIs such as claude and codex self-update. A binary swapped between planner and worker steps changes flags and output schema (the pack already worries about schema drift).
  Done when: the resolved binary's path, size and mtime are recorded at run start; replacing the file during a test run triggers a re-probe before the next step and a `runner-updated` event, and a changed capability fails closed to the fallback chain.

- **Heal by quarantine, never by deletion** — SECURITY — value 4 — effort S — risk low — category: recovery
  Why: the pack proposes many healers (fsck, orphan reap, `doctor --fix`, repair, stale-lock recovery). A bug in any of them can destroy the state it is repairing.
  Done when: a lint test shows every healer path moves originals to `.foreman/lost+found/<ts>/` with a manifest, and a seeded healer bug is recoverable with one `fm doctor --restore` command.

- **Pause globally on correlated failures** — FEATURE — value 4 — effort M — risk med — category: scheduling
  Why: the pack has per-runner breakers and outage-vs-failure in the bench, but no live view across runs. A provider outage during a multi-project queue would produce N separate failures and N spent retries.
  Done when: three runs with the same failure signature across different projects within 5 minutes pause the shared scheduler. One banner names the cause, and a probe success resumes the queue automatically.

- **Resume validity stamp** — FIX — value 3 — effort S — risk low — category: recovery
  Why: assumption: a run resumed hours later can find a changed HEAD, a changed `code.toml`, or a different runner roster. Existing ideas cover journals and preflight, not a single comparable stamp.
  Done when: the journal header stores a hash of (base ref, resolved config, runner capability card); a resume with any component changed prints a three-line diff and requires `--accept-drift` or replans.

- **Downshift local models on OOM or swap** — FEATURE — value 3 — effort M — risk med — category: local models
  Why: local endpoints are first-class and the pack covers probing real context size. It does not cover the server being OOM-killed (exit 137) or thrashing mid-run.
  Done when: a fake server killed with 137 yields `local-oom`; the retry halves the context request and the harness falls back one runner if that also dies, with both decisions in the journal.

- **Wild: Rehearse a kill-and-resume before every unattended run** — FEATURE — value 4 — effort M — risk low — category: chaos *(wild)*
  Why: assumption: resume bugs are specific to a repo's size, hooks and lock behaviour. A 20-second rehearsal on a throwaway clone proves recovery works here before the user leaves.
  Done when: `fm code --tonight` starts the rehearsal, kills it at a random journal step, resumes it, and refuses to arm the real run if the final trees differ.

- **Wild: Enforce the run envelope from a separate process** — SECURITY — value 4 — effort M — risk med — category: containment *(wild)*
  Why: budget, scope and time caps enforced inside the same Python process share its bugs and hangs. A tiny independent enforcer (POSIX sh plus `/proc` and `git diff --name-only`) could kill the process group on a breach.
  Done when: a deliberately hung harness with a breached file-scope cap is killed by the enforcer within 10 seconds, and the enforcer has no import path to Foreman code.

- **Wild: Keep a heat strip of the user's own dependencies** — FEATURE — value 3 — effort M — risk low — category: observability *(wild)*
  Why: assumption: "it just isn't doing anything" often means a provider or local server was slow, not Foreman. A one-line strip from cheap probes taken while the app is open would show which dependency is degraded.
  Done when: the home screen shows per-runner latency and error ticks over the last hour from the app's own calls plus an optional 60-second probe, and retry scheduling reads it to avoid a runner that is currently red.

# Brainstorm — lens: reliability

- **Add a first-byte deadline to every runner launch** — FIX — value 5 — effort S — risk low — category: liveness
  Why: the nixie run "just isn't doing anything": the claude planner ran for minutes with no output at 66k–133k tokens per call. Assumption: no per-call first-output deadline exists today, only the overall run.
  Done when: a fake runner that prints nothing for 20 s is classified "no first byte" at the configured deadline, the event is logged and shown in Activity, and a fake that prints at 1 s passes untouched.

- **Name the silence with a stall classifier** — FEATURE — value 5 — effort M — risk low — category: diagnosis
  Why: "just isn't doing anything" had several possible causes (loading plugins, waiting on the API, a rate limit, a hung child, a permission prompt). Assumption: today they all look identical, which is silence. Reads child CPU, /proc state, stderr tail and stream-json heartbeat age.
  Done when: scripted fakes for each of five causes produce five distinct one-line diagnoses, each ending in a `Next:` command.

- **Run every runner in a process group with a parent-death reaper** — FIX — value 5 — effort M — risk med — category: orphans
  Why: quitting left the planner running orphaned (T-1326 covers the intent). This goes further: setsid group, PR_SET_PDEATHSIG on Linux, and a small sidecar and registry file so a SIGKILL of fm code is still cleaned up on the next launch. Assumption: T-1326 only handles clean stops.
  Done when: `kill -9` on fm code with a sleeping fake worker leaves zero descendants within 3 s on Linux, and the macOS path reaps via the registry on the next start.

- **Journal each step before acting so a run can resume** — FEATURE — value 4 — effort M — risk med — category: crash-recovery
  Why: lid closes, SSH drops and kills mid-run are normal. Assumption: run state lives in memory plus events; the event log may not be enough to resume an in-flight step.
  Done when: killing the run at each of the station boundaries and then running `fm code --resume` reaches the same closed task and commit as an uninterrupted run, in a test that loops over every boundary.

- **Kill-at-random-point chaos test in CI** — FEATURE — value 4 — effort M — risk low — category: testing
  Why: Foreman's rule is every claim backed by a check that runs; durability is a claim with none visible. Seeded SIGKILL at random points, then assert invariants: no orphan processes, no half-written config, git config and hooks restored, the task lock released.
  Done when: 50 seeded kills pass the invariants on Linux 3.12 CI, and a deliberately broken restore step is caught by the test.

- **Give each runner a circuit breaker with classified fallback** — FEATURE — value 4 — effort M — risk med — category: failover
  Why: runners are about to be many (T-1328). Assumption: one failing runner currently fails the run. Classify the failures (auth, rate limit, timeout, malformed output, crash), retry only the retryable ones, and trip the breaker after N failures so the next call goes to the fallback.
  Done when: a fake runner returning a rate limit causes a switch to the configured fallback, with the reason shown in Activity and no repeat attempts against the tripped runner for the cool-off period.

- **Pin down the nested-Foreman depth marker at the environment and process level** — FIX — value 4 — effort S — risk low — category: duplicates
  Why: the user asked for no duplicate Foreman when Claude Code is a worker. An environment variable alone is lost through `env -i`, sudo or shell wrappers. Assumption: T-1327 uses only the env marker.
  Done when: a worker launched through `env -i` still detects the parent via ancestry (/proc, or ps on macOS) and runs without Foreman hooks, with a test per platform.

- **Lease the project so two app instances can't run the same task** — FIX — value 4 — effort S — risk low — category: locking
  Why: T-1330 makes fm code a multi-project app, which makes two windows on one queue likely. Assumption: leases exist for workers (T-1344 area was fixed) but not for app-level task claims.
  Done when: two concurrent `fm code --task T-X` processes result in exactly one running and the other exiting with the holder named; a stale lease from a dead PID is taken over.

- **Repair the terminal after any death** — FIX — value 3 — effort S — risk low — category: terminal
  Why: the TUI owns raw mode, the alternate screen and the mouse. A crash or SIGKILL leaves the shell broken. Assumption: only the normal exit paths are covered.
  Done when: killing the TUI under a pty with SIGKILL, then running `fm code` again, restores cooked mode first (state recorded in a tiny tty-state file), verified by a pty test checking termios flags.

- **Wild: Add a black-box recorder with a one-command crash bundle** — FEATURE — value 3 — effort M — risk low — category: forensics — wild
  Why: assumption: failures like the nixie one are only diagnosable if the user can send the evidence. A ring buffer of the last 2 minutes of events, process tree, runner argv (secrets scrubbed) and the stall diagnosis, written on any abnormal exit or by `fm code why --bundle`.
  Done when: a forced stall produces a bundle with the argv, tree and last events, and a scrub test shows a planted API key never appears in it.

- **Wild: Run a canary that auditions every runner nightly on a scratch repo** — FEATURE — value 3 — effort L — risk med — category: drift — wild
  Why: assumption: CLI output formats (claude stream-json, codex --json) drift on update, which breaks the progress parsing silently. T-0336 shows live verification of codex, gemini and opencode is still open.
  Done when: a scheduled run executes one tiny request per installed runner, records pass or fail and schema drift, and files a task automatically for a regression.

- **Wild: Make a self-healing safe mode after a crash loop** — FEATURE — value 3 — effort M — risk low — category: recovery — wild
  Why: assumption: a bad theme, extension or config could make every launch crash the TUI. After 3 crashes in 5 minutes, start with defaults, no extensions and the plain-text view, and say what was disabled.
  Done when: a planted extension that raises at import crashes the first 3 launches; the 4th opens in safe mode naming that extension, and `fm code --normal` re-enables it.

- **Write config atomically with a last-good copy** — FIX — value 3 — effort S — risk low — category: config
  Why: the user wants better config and setup; models.json is written by several paths and a torn write would silently take all runners away. Assumption: writes aren't atomic today.
  Done when: killing a writer mid-save leaves either the old or the new file intact, a corrupt file falls back to the `.last-good` copy with a notice, and `fm doctor` reports it.

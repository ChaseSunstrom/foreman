# Brainstorm — lens: approaches

- **Make bare `fm code` a thin exec into the user's best CLI, wrapped by Foreman** — FEATURE — value 5 — effort M — risk low — category: launch
  Why: the user compares to `claude`; the cheapest route to "launch like claude" is `fm code` exec'ing the detected CLI inside a pty with the guard, leases and capture attached, not a new app. Trade-off: less custom UI, no home screen, but "it just works" ships in days. Home screen (T-1330) becomes an optional `fm code home`.
  Done when: `fm code` with no args and no tty config opens the claude CLI interactively in under 2 s, and `fm status` in another shell shows that session's lease.

- **Gate every worker launch on a lineage env marker, not a detection heuristic** — FIX — value 5 — effort S — risk low — category: nesting
  Why: "no duplicate Foreman when it runs Claude Code as a worker" plus 66k–133k tokens per nested call. Approach: `FOREMAN_LINEAGE=<run id>:<depth>` set on every child; Foreman's hooks, rules and session-start no-op when it is present, and the plugin loader is told to skip via the worker's settings flag. Trade-off: relies on children inheriting env, but it is one line to check and testable with a fake CLI.
  Done when: a fake worker that runs `fm` hooks under the marker prints zero Foreman context bytes, and a test asserts input tokens of a nested planner fall below a stated ceiling.

- **Show a 10-second sign-of-life contract with a named wait** — FEATURE — value 5 — effort S — risk low — category: liveness
  Why: nixie run "just isn't doing anything" for minutes. Approach: do less than a full watchdog; print "waiting on claude (planner), sent 12s ago, 84k tokens in, last event none" at 5 s and every 10 s, derived from the child's pid state and stream file. Trade-off: no diagnosis, only truth, but it kills the silent-minutes complaint.
  Done when: a fake runner that sleeps 30 s produces at least three status lines naming the runner and elapsed time.

- **Treat the project as cwd plus a warn-on-mismatch, no registry** — FEATURE — value 4 — effort S — risk low — category: projects
  Why: "multiple projects" can start as discovery from existing `.foreman` dirs under `~/projects` and recent-run logs, not a managed registry. Trade-off: misses projects never run, but there is nothing to configure or corrupt.
  Done when: `fm code projects` lists every directory under the scan roots containing Foreman state, with queue counts, with no config file present.

- **Describe runners as 8-line data manifests and ship five** — CLEAN — value 4 — effort M — risk low — category: runners
  Why: "ANY CLI or model" is today code per adapter (T-0335/6/7 are blocked live-verifying codex, gemini, opencode). A manifest (cmd template, stream format, plan flag, env allowlist, startup-tax probe) lets the user add a CLI without a release. Trade-off: quirks like Gemini's AfterAgent still need code escape hatches.
  Done when: dropping a manifest for a fake CLI into `~/.foreman/runners/` makes `fm code --worker NAME` run a request to close with no Python change.

- **Auto-file a friction task from the user's own phrases via a prompt hook** — FEATURE — value 5 — effort M — risk med — category: self-notice
  Why: the user said they "shouldn't even need to ask". Approach: a regex+list match ("just isn't doing anything", "why can't I", "isn't recognized") on captured requests opens a diagnostic task with the phrase quoted and area inferred from the recent commands. Trade-off: heuristic false positives; mitigate by filing as deferred with a receipt line, never auto-running a brainstorm.
  Done when: replaying the three quoted phrases against the hook creates three tasks tagged with the right area, and an unrelated prompt creates none.

- **Run `fm code doctor` as the first-run wizard and the install fixer** — FEATURE — value 4 — effort M — risk low — category: setup
  Why: `fm` wasn't on PATH and no model was set; two separate surprises. One command probes PATH, runners, duplicate installs (plugin vs checkout), and prints one fix per line, applying them with `--fix`. Trade-off: less magical than auto-fix at launch, but safe.
  Done when: in a HOME with no PATH link and two Foreman copies, `doctor --fix` leaves one `fm` resolving and reports which copy won.

- **Race two runners on the plan only, keep the cheaper green plan** — FEATURE — value 3 — effort M — risk med — category: routing
  Why: "assumption": planning is the cheap, read-only step, so racing it costs little and gives routing data from real use instead of bench cases (T-0866 waits on cases).
  Done when: a recorded race on a fake pair writes a per-kind win count that the next `fm code` default consults.

- **Wild: Adopt a running interactive Claude Code session as a lane via its transcript file** — FEATURE — value 4 — effort L — risk high — category: adoption
  Why: wild; the user lives in Claude Code, and tailing `~/.claude/projects/*/*.jsonl` gives read-only liveness and cost without launching anything. Trade-off: observe only, no control.
  Done when: with a Claude session active in another terminal, the home view lists it with its last tool call within 2 s.

- **Wild: Complaint-to-check compiler** — FEATURE — value 4 — effort L — risk med — category: regression
  Why: wild; each quoted complaint becomes a standing check ("a 30 s silent runner must print status"). Trade-off: needs a human-approved template per complaint class at first.
  Done when: "it just isn't doing anything" yields a committed test that fails on the pre-fix commit.

- **Wild: Make `fm code` ask which project from a sentence** — FEATURE — value 3 — effort M — risk med — category: projects
  Why: wild; "fix the login bug in nixie" resolves directory by name match over discovered projects, shows the resolved path as a chip, and defaults to cancel on ambiguity.
  Done when: a request naming `nixie` runs with cwd `~/projects/nixie` in a test tree, and an ambiguous name stops with a choice.

- **Reap children with a process-group lease, not a PID list** — FIX — value 4 — effort S — risk low — category: lifecycle
  Why: orphaned planner after quit (T-1326). Approach: start every runner in a new session, record the pgid in the lease, and have the next launch kill any leased group whose parent is gone. Trade-off: macOS parity needs care, but this covers hard kills that signal handlers miss.
  Done when: `kill -9` of `fm code` mid-planner leaves no runner process after the next `fm code` start.

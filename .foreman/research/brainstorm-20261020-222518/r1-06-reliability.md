# Brainstorm — lens: reliability

- **Reap orphaned runners with a process registry** — FIX — value 5 — effort M — risk low — category: reliability
  Why: the nixie planner kept running after the user quit. T-1326 covers stop and quit, but not SIGKILL, a crashed TUI, or a closed laptop.
  Done when: a test starts `fm code` with a fake CLI that spawns grandchildren, `kill -9`s fm, and the next `fm code` start logs and kills every registered survivor (pidfile with start-time check, process-group based, Linux and macOS).

- **Add a stall watchdog with a named diagnosis** — FEATURE — value 5 — effort M — risk low — category: watchdog
  Why: "it just isn't doing anything" for minutes. T-1329 shows progress, but nothing decides a call is wedged.
  Done when: a fake runner that goes silent for N seconds makes the run show "stalled: planner silent 90s, 133k tokens in" and offer retry, switch runner or abort. A fake runner that streams slowly is not flagged.

- **Journal every run so `fm code --resume` continues after a crash** — FEATURE — value 5 — effort M — risk med — category: recovery
  Why: the harness owns the stations (plan → task → checks → steps → close), so each transition can be an appended, fsynced event. This is the same event log the TUI viewer reads.
  Done when: killing fm at each station boundary in a scripted test, then running `--resume`, yields the same closed task and commit as an uninterrupted run, with no duplicate task and no duplicate commit.

- **Preflight every runner with a one-token probe** — FEATURE — value 4 — effort S — risk low — category: runners
  Why: T-1328 finds CLIs, but "found" is not "works". An unauthenticated CLI, a changed flag or a down Ollama otherwise fails minutes in.
  Done when: `fm code doctor` and the home screen show per-runner status (ok / not logged in / flag unsupported / endpoint down / latency), and a broken default is flagged before the first request, tested with fake CLIs.

- **Budget and cap nested planner calls** — PERFORMANCE — value 4 — effort M — risk low — category: cost guard
  Why: 66k–133k input tokens per planner call because the nested Claude loads every plugin. T-1327 removes Foreman's part, not the rest.
  Done when: the planner call runs with a minimal config (no plugins, read-only tools) and an enforced timeout and token ceiling. A bench case shows the input tokens drop at least 5× and a runaway call is cut at the cap with a clear message.

- **Fall back across runners on classified failures** — FEATURE — value 4 — effort M — risk med — category: runners
  Why: "manage ANY CLI/model". Rate limits, auth errors, timeouts and malformed JSON are different failures that need different handling.
  Done when: a config line `fallback = [claude, codex, local]` makes a fake rate-limited runner hand the step to the next one. Auth errors don't retry. Each switch is recorded in the journal, and the guard verdicts are identical on every runner.

- **Run worker turns in a throwaway worktree** — SECURITY — value 4 — effort M — risk med — category: isolation
  Why: today a failed or killed worker leaves a dirty repo, and "a commit undone" is cleanup after the fact. Multiple projects and parallel lanes make it worse.
  Done when: a killed worker leaves the user's checkout byte-identical. Only a proved, guard-passed diff is applied back, and a test kills the run mid-edit and compares tree hashes.

- **Stop nested Foreman with a depth marker** — FIX — value 4 — effort S — risk low — category: duplicates
  Why: the user asked to prevent duplicate Foreman when it runs Claude Code as a worker. A plugin install plus fm code means two Foremans.
  Done when: every child gets `FM_DEPTH`/`FM_PARENT_RUN`. Hooks and rules short-circuit when it is set (guard and leases stay on), and `fm doctor` flags a plugin-and-standalone double install by name.

- **Lock tasks across projects and app instances** — FIX — value 4 — effort S — risk low — category: concurrency
  Why: the home screen can run any queued task in any project. Two TUIs, or the TUI plus a Claude Code session, could take the same task.
  Done when: starting a task already leased by a live process is refused with the holder's pid and project. A stale lease whose pid is dead is reclaimed, tested with two processes.

- **Write config atomically, validate it, and self-repair** — FIX — value 3 — effort S — risk low — category: config
  Why: "better config/setup", plus `models.json`, themes and keybindings that are hand-edited.
  Done when: every config write is temp-file plus rename with a `.last-good` copy. A malformed file produces a line-accurate error and the app still opens on the last good config, tested with truncated and garbage files.

- **Self-notice friction and open a diagnostic** (wild) — FEATURE — value 4 — effort M — risk med — category: self-awareness
  Why: the user said "I shouldn't even need to ask". Phrases like "isn't doing anything" and "why can't I" already appear in captured requests.
  Done when: a captured request matching friction patterns on a known area files a diagnostic task that attaches the last run's journal and watchdog state, and does so once per episode, not on every mention.

- **Kill the process at random points and compare the end state** (wild) — FEATURE — value 4 — effort M — risk low — category: chaos testing
  Why: journaling and reaping only count if they survive real kills. `fm code bench` already exists as a seeded-task harness.
  Done when: a nightly `fm code chaos` kills the fake-runner run at 50 random points with random signals, then resumes. All 50 end in a clean tree, no orphan processes, and one closed task.

- **Cover every CLI adapter with a scripted misbehaving fake** (wild) — CLEAN — value 4 — effort M — risk low — category: contract tests
  Why: claude, codex, gemini and aider flags change between versions, and T-0336 notes real-CLI verification is blocked.
  Done when: one fake-CLI script per adapter replays recorded stream-json and `--json` transcripts, including a hang, a flood, a truncated line and a crash. Adapter tests assert the right classification for each, and a version-skew probe warns when `--version` drifts from the recorded one.

- **Snapshot each step to a shadow ref for instant rollback** (wild) — FEATURE — value 3 — effort M — risk med — category: rollback
  Why: the harness already restores Git config and undoes commits, and a step-level rewind makes a bad model turn cheap.
  Done when: each step writes a private ref that never touches the user's branches, `fm code rewind STEP` restores that tree, and the refs are pruned on close.

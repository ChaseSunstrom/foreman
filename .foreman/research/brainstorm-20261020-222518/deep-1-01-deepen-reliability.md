# Brainstorm — lens: deepen: reliability

- **Make the run journal the single source of truth** — FEATURE — value 5 — effort M — risk med — category: durability
  Why: the user's nixie run did nothing visible and the orphan survived quit; an append-only event journal (runner calls, child pids, slot outputs, stage) lets resume, replay, watchdog and the TUI all read one thing. Assumption: events already exist for `--record`, but not fsynced per stage or carrying pids.
  Done when: kill -9 the fm code process mid-step, then `fm code --resume` continues from the last journaled stage and a test asserts no step re-runs and no duplicate commit.

- **Put every spawned CLI in one process group with a lease file** — FIX — value 5 — effort S — risk low — category: process control
  Why: T-1326 (orphaned planner after quit) plus a closed terminal or SIGKILL. Assumption: children currently inherit the parent's group. Start each in a new session, record pgid in the lease, and have the next `fm code` start reap leases whose owner is dead.
  Done when: a test starts a fake runner that spawns grandchildren, SIGKILLs fm, runs `fm code` again, and finds zero surviving descendants.

- **Classify silence with a stall doctor** — FEATURE — value 5 — effort M — risk low — category: diagnosis
  Why: "it just isn't doing anything" with 66k–133k input tokens per call. Read the journal, the child's CPU/IO via /proc (a macOS fallback via ps), its stream-json heartbeat, and its open network sockets. Name the cause (loading plugins, waiting on the API, rate limit, a hook prompt, a stuck tool), show it in Activity and offer the fix.
  Done when: fixtures for five stall causes each produce the right one-line classification and suggested action in `fm code doctor --run`.

- **Probe each runner with a canary before real work** — FEATURE — value 4 — effort S — risk low — category: preflight
  Why: nested Claude took minutes before any sign of life. A canary round trip ("reply OK", a capped token budget, a 10 s deadline) per runner and project measures cold-start latency and tokens, then caches the result (TTL) and shows it on the picker, with a warning when the baseline context exceeds a threshold.
  Done when: `fm code probe` prints latency and input tokens per runner, and a fake slow runner is flagged "cold start 40s, 90k tokens" by a test.

- **Bound every run by budget, deadline and no-progress limit** — FEATURE — value 4 — effort M — risk low — category: limits
  Why: planner calls ran for minutes unchecked. Per-call and per-run caps on tokens, cost and wall time, plus a "no journal event for N seconds" kill that ends with a summary naming the limit hit and the command to raise it.
  Done when: a test with a hung fake runner ends within the deadline, exits non-zero, leaves no processes, and the receipt names the cap.

- **Pause on rate limits and sleep through them** — FEATURE — value 4 — effort M — risk med — category: resilience
  Why: unattended multi-project runs will hit usage limits. Parse the limit/reset messages from claude, codex and API 429 headers, journal a "paused until T" state, and resume with no work lost; the home screen shows the countdown.
  Done when: a fake runner emitting a limit message with a reset time makes the run pause, then continue after a simulated clock jump, with the same task closing.

- **Fall back along a runner chain with a reason on record** — FEATURE — value 4 — effort M — risk med — category: failover
  Why: the user wants ANY CLI/model; one config line (`default = claude, then codex, then local`) lets a dead or limited runner hand the same slot to the next. The guard judges every runner identically, and the receipt records each hop.
  Done when: with the first runner failing preflight, a run completes on the second and the receipt lists "claude: not logged in → codex".

- **Fence the config with schema, last-good and a repair command** — FIX — value 3 — effort M — risk low — category: config
  Why: "better config/setup" and the drop of the shared models.json helper. Load errors give line and column, the previous valid copy takes over with a visible banner, and `fm code config repair` rewrites it, keeping a backup.
  Done when: a corrupted models.json starts fm code on last-good with a banner, and the test checks the error line number.

- **Wild: Run the harness in a rehearsal sandbox first** — FEATURE — value 4 — effort L — risk med — category: safety
  Why: wild. Execute the worker turn in a git worktree copy, apply the diff to the real tree only after the guard and checks pass. A runner that wedges, trashes the tree or rewrites .git/config costs nothing. Assumption: worktrees are cheap enough for the target repos.
  Done when: a worker that deletes files and edits hooks in the sandbox leaves the real tree byte-identical, and a good change lands as one commit.

- **Wild: Record real runner failures into a replayable chaos suite** — FEATURE — value 4 — effort M — risk low — category: testing
  Why: wild. Every stall, orphan or malformed slot seen in the field is captured (redacted) as a scripted fake-runner trace; CI replays them, and `fm code bench --chaos` injects random kills, delays, truncated JSON and 429s into the real loop.
  Done when: the nixie-style silent-planner trace is a committed fixture that fails before the stall doctor and passes after, and the chaos run completes N seeded trials with no orphans.

- **Wild: Let a sentinel process supervise the TUI and the runs** — FEATURE — value 4 — effort L — risk high — category: supervision
  Why: wild. A tiny stdlib supervisor owns children and the journal, so the TUI can crash, the terminal close or the lid shut, and a reattach (`fm code attach`, like tmux) shows the run still going, with a one-line "N runs in background" on the home screen.
  Done when: closing the terminal mid-run leaves the run alive, and `fm code attach` redraws it live from the journal; `fm code stop` ends all of it.

- **Detect Foreman-in-Foreman by a marker in the environment and lease** — FIX — value 4 — effort S — risk low — category: duplication
  Why: the user asked to prevent duplicates when Foreman is installed as a plugin and run as a worker. Set `FM_PARENT_RUN=<id>` plus a scrubbed settings overlay for nested CLIs, and have hooks exit silently when the marker is present while the guard remains in force.
  Done when: a nested claude fixture shows zero Foreman session context injected, the guard still blocks a forbidden command, and a test asserts both.

- **Wild: Have a self-heal pass at launch that fixes what it can** — FEATURE — value 3 — effort M — risk med — category: setup
  Why: wild; `fm` wasn't on the user's PATH and they hit it themselves. At first launch `fm code` checks PATH, links, models.json, runner logins and git state, fixes the safe ones (a ~/.local/bin link) and prints the commands for the rest, and never asks for anything it can detect.
  Done when: in a clean HOME with no `fm` on PATH, `fm code` links it, reports each check pass/fail and reaches the home screen in under 10 s.

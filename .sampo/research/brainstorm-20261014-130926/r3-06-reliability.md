# Brainstorm — lens: reliability

- **Run a metric-reader round-trip suite against real writer output** — FIX — value 5 — effort S — risk low — category: correctness
  Why: Two of the user's recent asks were readers that silently missed what writers wrote ("✗ exit N" vs "exit N" in track record and catch rates). Same bug class likely lurks in other readers (doctor, bench, cost, friction). Round 1 shipped more writers (compact output, monitor, fm page).
  Done when: a test generates each writer's real output via the actual write path and asserts every metric reader counts it; it fails on a reintroduced "exit N" style mismatch.

- **Add a live arming canary for the mail monitor** — FEATURE — value 5 — effort M — risk med — category: liveness
  Why: Pack lists "arming in a live interactive session is unverified (monitors start only in new sessions)". The user's incident was idle sessions; an unverified path is the failure mode.
  Done when: at first turn of a new session Foreman writes a bus heartbeat, the monitor echoes it, and `fm doctor` reports armed/not-armed per session; a session without an echo within 30s falls back to the tmux wake and records why.

- **Make compact-output stubs self-recoverable** — FEATURE — value 4 — effort S — risk low — category: tokens
  Why: Compact output rewrites big Bash results to head+failures+tail with full text in state/outputs, and `fm tidy` prunes those after 7 days. A pointer that dangles after a resume or prune loses evidence.
  Done when: every stub carries the exact retrieval command and a content hash, retrieval of a pruned file prints a clear "expired" line, and a test proves failure lines are always kept in the stub.

- **Return a typed partial result when a child hits its budget or turn cap** — FIX — value 4 — effort M — risk low — category: children
  Why: Round 1 added `--max-budget-usd` and maxTurns to children; a child cut off mid-answer yields truncated prose that downstream ideas/research code may parse as complete.
  Done when: a child killed by budget produces a record marked `partial` with the salvaged text, and a test with a tiny budget shows callers treat it as incomplete, not as zero ideas.

- **Journal lane merges so a crash cannot lose the pre-merge start point** — FIX — value 4 — effort M — risk med — category: state integrity
  Why: Lane-merged tasks keep their pre-merge start point (T-0812), meaning the value is state that exists only briefly; a crash between merge and write would reintroduce the empty-diff close checks.
  Done when: a crash-injection test kills the merge between steps and `fm doctor` or resume recovers the start point from the journal.

- **Test that every verify command still runs after its target leaves the queue** — FIX — value 4 — effort S — risk low — category: verification
  Why: A dropped item shows its check grepped the queue for T-0775, which vanished when the task finished. Plan-time refusal covers unrunnable commands but not ones that rot later.
  Done when: `fm check` re-executes each recorded verify command in dry/syntax mode for open tasks and flags any that reference queue state, with the T-0775 pattern as a fixture.

- **Fail loudly when `python3` is missing or older than the floor** — FIX — value 3 — effort S — risk low — category: hooks
  Why: Hooks are Python spawned per event; an old or missing interpreter makes every hook silently no-op, which looks like Foreman is off while enforcement is gone.
  Done when: with a fake `python3` of an old version on PATH, a hook run emits one visible warning line and `fm doctor` fails with the fix, covered by a test.

- **Add a stop-reason and idle canary for the drive loop** — FEATURE — value 4 — effort M — risk med — category: drive
  Why: The headless-drive incident of 2026-10-14 and several "never idle" asks show stops that weren't deliberate. Nothing records why a turn ended while the queue was non-empty.
  Done when: every Stop with queued work logs a typed reason (needs-user, done, budget, unknown), and a drill replaying the 2026-10-14 headless case asserts reason ≠ unknown.

- **Give every wake path a delivery receipt** — FEATURE — value 4 — effort M — risk med — category: liveness
  Why: Wakes now go via monitor, tmux send-keys, or push; none confirms the model actually received them. Round 1 added a path without an ack.
  Done when: each wake carries an id, the next hook event stamps an ack, and unacked wakes after N seconds escalate to the next path and are shown in `fm doctor`.

- **Wild: Run a nightly canary that wedges a throwaway session on purpose** — FEATURE — value 3 — effort L — risk med — category: chaos
  Why: assumption: the failures that hurt are idle/stall states; a scheduled drill in a temp project (kill the monitor, drop a hook, fill the disk) proves recovery before the user hits it.
  Done when: a scripted drill reports pass/fail per fault into `fm doctor` history, and a deliberately broken wake path turns it red.

- **Wild: Auto-trip a feature kill-switch on repeated silent failures** — FEATURE — value 4 — effort M — risk med — category: resilience
  Why: Round 1 added many native integrations (monitor, compact output, push, sessionTitle) that can fail quietly; Foreman already prefers visible degradation.
  Done when: a feature failing N times in a row flips itself to its documented fallback, tells the user once, and a test shows it re-arms after a clean probe.

- **Wild: Mount a slow-disk and read-only-home drill in `fm doctor --drill`** — FEATURE — value 3 — effort M — risk low — category: chaos
  Why: State lives centrally under ~/.claude; disk-full or read-only conditions are unexamined in the pack, while hooks must never block a session on write errors.
  Done when: with the home dir read-only or ENOSPC simulated, every hook exits within its budget, fails open with one recorded reason, and the drill reports it.

- **Stamp each state write with its writer and version** — CLEAN — value 3 — effort S — risk low — category: observability
  Why: Several writers (hooks, lanes, monitor, desktop) touch the record; when readers disagree the first question is who wrote it.
  Done when: every record write includes writer id and Foreman version, and `fm task show --json` exposes the last writer.

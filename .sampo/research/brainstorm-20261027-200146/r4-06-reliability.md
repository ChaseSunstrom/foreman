# Brainstorm — lens: reliability

- **Check each idea's evidence quote against the pack before filing** — CLEAN — value 4 — effort S — risk low — category: brainstorm integrity
  Why: The pack's "Ideas so far" list already carries near-duplicates that slipped past the "don't repeat" rule. A substring check against the pack would catch quotes that don't exist, and the lens rules already ask for pack evidence. Assumption: children return quotes verbatim.
  Done when: A fixture brainstorm with one invented quote is rejected with the idea named, and the same run with real quotes passes.

- **Key every outward push and site publish with an idempotency token** — FIX — value 5 — effort M — risk med — category: safe retries
  Why: Recent commits show a push to `foreman/build` whose acceptance criterion was pinned to a stale commit, so a retry re-publishes against a moving target. Assumption: the publish step can be retried after a network error. A stored token makes a second attempt a no-op.
  Done when: Running `fm publish` twice with the same token produces one remote ref update and reports "already published".

- **Swap the live site by pointer, never write it in place** — FIX — value 4 — effort M — risk low — category: atomic deploys
  Why: The site publishes from the build branch and "Verify the live site after every publish" is already queued, but a half-written deploy would still serve broken pages to visitors during the copy. Assumption: the host can serve a symlinked or versioned directory.
  Done when: A deploy killed mid-copy leaves the previous build served byte-for-byte, checked with `curl` in a test.

- **Resume a usage-limit wait from the journal after a reboot** — FIX — value 4 — effort M — risk med — category: long waits
  Why: `fm run` already waits out a usage limit (`USAGE_LIMIT`, `--wait`), but that wait lives in one process. A reboot or closed terminal drops it, and the `defer --until reset` bug showed how a wrong reset time strands work. Assumption: the wait deadline can be written to the journal.
  Done when: A run waiting on a reset is killed, restarted after the reset time, and continues without a manual command.

- **Retry only idempotent steps, with jittered backoff, and name the step that gave up** — FIX — value 4 — effort S — risk low — category: retries
  Why: Failures in the pack, such as the 20-minute edit-lease refusal and the 40-minute gate hold, show a wait or retry loop that ends with a vague message. Assumption: each step can be marked idempotent or not in one table.
  Done when: A forced transient error retries an idempotent step three times with growing delays, and a non-idempotent step fails once with its name in the message.

- **Cut lane concurrency when API errors rise, then grow it back slowly** — PERFORMANCE — value 4 — effort M — risk low — category: adaptive load
  Why: Parallel builders and brainstorm lenses share one account's limits, and the pack shows the usage governor tuned by hand (compact at 200k, Sonnet builders). Assumption: error rate per minute is visible to the scheduler. Additive-increase, multiplicative-decrease is a well-known rule that needs no model.
  Done when: Injecting five 429s into a fake runner halves the lane count, and it returns to the configured maximum after ten clean minutes.

- **Pause every timer while the machine sleeps** — FIX — value 3 — effort S — risk low — category: sleep safety
  Why: Laptop lid-close during a run makes elapsed wall time jump, so a gate wait or stall card can fire the moment the machine wakes. Assumption: the timers use wall-clock time. Monotonic time already appears in the list, but suspend pauses that clock too, so the sleep case needs its own check.
  Done when: A fake suspend of 30 minutes in a test does not trigger the stalled card or the 15-minute gate wait.

- **Validate the journal's last record before a queue starts** — FIX — value 3 — effort S — risk low — category: journal integrity
  Why: A crash during a write can leave a truncated final line, and the next run would read a half-written state. Assumption: the journal is append-only text. A truncated tail is detectable by parsing the last line and comparing its length to a stored checksum.
  Done when: A journal cut mid-line makes `fm code` drop that tail with a one-line warning and start the queue normally.

- **Restart a crashed fm with a small supervisor that files a crash report** — FEATURE — value 4 — effort M — risk med — category: crash recovery
  Why: The TUI crash-proofing idea covers the screen, but nothing restarts the orchestrator when it dies outright. A supervisor that records the exit reason and the last journal event would make each crash a reviewable item. Assumption: the supervisor is a few hundred lines and has no model dependency.
  Done when: Killing `fm code` with SIGKILL during a run restarts it within five seconds and writes one crash file naming the last event.

- **Replay the last 100 journal events into a fresh process and diff the state** — FEATURE — value 4 — effort M — risk low — category: state determinism — wild
  Why: The pack's status views read state from several places (`fm status`, the pane, the desk card), and drift between them is the common failure mode. A replay that must reproduce the live state catches the case where a rendering path invents its own state. Assumption: the journal holds every state change.
  Done when: Replaying a recorded session produces a state dump identical to the live one, and a deliberately dropped event makes the diff fail.

- **Mutation-test the gate itself so a gate that passes a broken fix is failed** — FEATURE — value 5 — effort L — risk med — category: gate trust — wild
  Why: Foreman's whole promise is that the gate means something. Nothing in the pack checks the gate against deliberately broken code. Assumption: the gate can run against a copy of the repo with one change applied.
  Done when: A nightly run applies ten injected bugs to a copy of the repo, and any bug the gate passes turns the gate red with its name.

- **Wild: a deadman's timer that, if no surface reads the journal for a day, parks the queue** — FEATURE — value 3 — effort S — risk low — category: unattended safety — wild
  Why: Overnight and unattended runs keep spending after the user has stopped looking. The pack's dead-man's-switch idea covers a stopped surface, not a stopped human. Assumption: "no surface read" can be recorded as a timestamp on each read.
  Done when: With no reads for 24 hours in a test clock, the queue stops after its current task and the stop is written to the journal.

# Brainstorm — lens: reliability

- **Add a round-1 fire counter and `fm doctor --alive` probe** — FEATURE — value 5 — effort M — risk low — category: reliability
  Why: the pack's known gaps say the mail monitor's arming in a live session is unverified, and nobody has ticked the board; features shipped with no proof they fire.
  Done when: each round-1 integration (monitor, sessionTitle, push-on-ask, compact output, effort passing) increments a counter on use, and `fm doctor --alive` lists any with zero fires in 7 days.

- **Pair every metric reader with a writer-output round-trip test** — FIX — value 5 — effort S — risk low — category: correctness
  Why: two of the user's asks were readers that matched 'exit N' while writers stored '✗ exit N'. This class of bug recurs when formats drift.
  Done when: a test generates real writer output for catch rates, track record and give-up mining, and fails if any reader's count differs from the writer's known truth.

- **Shadow-run compact output before asking for a yes** — FEATURE — value 4 — effort M — risk low — category: tokens
  Why: it is opt-in and off; ~1.04M tokens/30 days is a claim, not a measurement of lost failure info.
  Done when: with shadow on, each over-threshold output logs what compaction would have kept, and a later `fm out` or re-run fetch-back marks a miss; `fm doctor` shows the miss rate.

- **Make compact-output stubs self-recoverable** — FIX — value 4 — effort S — risk low — category: tokens
  Why: full text goes to state/outputs and `fm tidy` prunes after 7 days; a stub cited later may point at nothing.
  Done when: every stub names an exact retrieval command, and `fm tidy` skips any output referenced by an open task or active session.

- **Return a typed partial result when a child hits its budget or turn cap** — FIX — value 4 — effort M — risk med — category: headless children
  Why: round 1 added `--max-budget-usd` and maxTurns; a child killed mid-run likely yields nothing, wasting the spend.
  Done when: a child forced to hit its budget leaves a partial file that `fm ideas` or `fm research` records with a "truncated" flag, covered by a test.

- **Journal lane merges so a crash cannot lose the pre-merge start point** — FIX — value 4 — effort M — risk med — category: state
  Why: T-0812 fixed close checks seeing an empty diff after a merge, but the start point's durability across a crash is assumed, not tested.
  Done when: a crash injected between the merge and the record write still lets `fm task finish` compute the original diff.

- **Add a stop-reason and idle canary for the drive loop** — FEATURE — value 4 — effort M — risk low — category: liveness
  Why: the incident of 2026-10-14 (a headless session answering and stopping) was fixed by a guard; there is no drill that proves it stays fixed.
  Done when: a scripted test replays that incident and asserts the session drives the queue, and runs in the suite.

- **Fail loudly when `python3` is missing or older than the floor** — FIX — value 3 — effort S — risk low — category: install
  Why: hooks depend on Python 3.12.7+; a silent hook failure in bypass mode means the guard is gone without notice. Assumption: the failure mode today is silent.
  Done when: with a stubbed old `python3` on PATH, the hook wrapper emits one visible warning and refuses bypass-mode dangerous commands (fail-closed), tested.

- **Property-test `fm page` redaction** — SECURITY — value 4 — effort S — risk low — category: privacy
  Why: T-0786 was hardening by example (home spellings, URLs, paths); redaction is a good fit for generated inputs, and the page goes to an Artifact, which can be cached.
  Done when: a fuzz test builds random pages with home paths, usernames, tokens and URLs in varied spellings, and none survive in output.

- **Test that every verify command can still run after its target leaves the queue** — FIX — value 3 — effort S — risk low — category: verification
  Why: the user's dropped item shows a check grepping the queue for T-0775 broke once that task left. Plan-time refusal covers unrunnable commands, not self-expiring ones.
  Done when: `fm task plan` rejects verify commands that read the live queue or state files, with a message pointing to a durable alternative.

- **Wild: Run a disk-full and read-only-home drill in `fm doctor --drill`** — FEATURE — value 3 — effort M — risk med — category: resilience
  Why: assumption: state writes are atomic, but behaviour under ENOSPC or EROFS is untested; hooks that crash there fail open in bypass mode. (wild)
  Done when: the drill runs in a throwaway HOME with a size-limited tmpfs and reports for each hook whether it failed closed, open, or crashed.

- **Wild: Auto-trip a feature kill-switch after repeated silent failures** — FEATURE — value 4 — effort M — risk med — category: self-protection
  Why: round 1 stacked a monitor, a compact-output hook, a push and a title; a broken one should demote itself rather than be diagnosed by hand. (wild)
  Done when: a feature that errors 3 times in a row is disabled, one line tells the user once, and `fm doctor` shows it with the error and a re-enable command.

- **Wild: Add a nightly canary that wedges a throwaway session on purpose** — FEATURE — value 3 — effort L — risk med — category: liveness
  Why: idleness has been the user's recurring pain (40 liveness ideas, the monitor and the tmux fallback); nothing exercises the wake paths unattended. (wild)
  Done when: a scheduled run starts a sandbox session, stalls it, and records which wake path (monitor, tmux, push) recovered it, or files a task when none did.

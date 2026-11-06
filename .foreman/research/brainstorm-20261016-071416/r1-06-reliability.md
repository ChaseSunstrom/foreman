# Brainstorm — lens: reliability

- **Make `fm release` one transactional verb** — FEATURE — value 5 — effort M — risk med — category: release reliability
  Why: Round-4 review says releases are a manual 8-step ritual (3 version fields, heading, quiet-tree gates, release-check, temp worktree merge, push); T-1173 "Release 1.2.33" is open. A half-finished ritual leaves versions inconsistent. Existing ideas cover deriving versions from a tag, not a resumable, rollback-safe run.
  Done when: a test kills `fm release --dry-run-to=push` after the bump step, rerun resumes at the next step without double-bumping, and `fm release --abort` restores all three version fields.

- **Auto-record reviewer findings at the source** — FIX — value 4 — effort S — risk low — category: feedback loop
  Why: pack says defect-class feed (T-1164) starves because `fm task finding` is manual, one call per finding. Mechanical capture closes the loop.
  Done when: a fixture review transcript containing three "confirmed defect" blocks yields three ledger findings without any `fm task finding` call, and `fm lane brief` lists them.

- **Make `fm` resolve to the lane's own copy inside a builder worktree** — FIX — value 5 — effort S — risk med — category: lane correctness
  Why: pack: builders can't run their own new `fm` flags because bare `fm` resolves to the main checkout; they must use `python3 plugin/bin/fm`. Builders verifying against the wrong code produces false greens.
  Done when: in a test worktree adding a new flag, bare `fm --newflag` run with that worktree as cwd executes the worktree's code, and outside any lane it still runs the installed one.

- **Alias common guessed command names** — FIX — value 3 — effort S — risk low — category: weak-model robustness
  Why: pack: builders and weak agents guess `fm task list`; the nearest-name suggestion exists but costs a turn. Pure aliases remove the retry.
  Done when: `fm task list`, `fm tasks`, and `fm task ls` each print the same output as the canonical verb, and a table-driven test covers the guesses mined from the ledger.

- **Mine guard refusals with their full commands into the friction digest** — FEATURE — value 4 — effort M — risk low — category: guard observability
  Why: pack: two false premises were found only after a hand-written transcript miner; the digest counts refusals but never shows the commands. Showing commands plus the replay verdict makes premises checkable up front.
  Done when: `fm friction` prints the top N refusals with full command text and the `fm guard try` verdict from the current guard, with a test on a seeded transcript.

- **Fix the guard's "it could be …" path guess** — FIX — value 2 — effort S — risk low — category: guard message quality
  Why: pack notes odd guessed paths like /repo/cd/w.out, with a word from the command glued into the path. Misleading hints erode trust in refusals.
  Done when: a test replaying the known bad command yields no suggested path containing a shell word as a directory component, and the suggestion is omitted when no real path resolves.

- **Let the autonomous drive invoke review and ideas workflows** — FEATURE — value 4 — effort M — risk med — category: unattended parity
  Why: pack: /foreman:review and /foreman:ideas run only when the user types them, so the AFK drive can't use them, while the standing ask is full autonomy. Assumption: `fm review` and `fm ideas` headless equivalents already exist and can be wired in.
  Done when: a fake-clock drive test over a queue with one finished lane triggers a headless review step and records its findings, with no user input.

- **Measure builder self-review and defect classes against rework** — FEATURE — value 4 — effort M — risk low — category: measured reliability
  Why: pack: every builder branch needed 2-6 review fixes; T-1147 and T-1164 are "new and unmeasured". Without a number they may be ceremony.
  Done when: `fm lane stats` reports review defects per merged lane, split by before and after the self-review gate, from the ledger, with a test on seeded data.

- **Add a "lane env doctor" run at lane creation** — FIX — value 3 — effort S — risk low — category: lane preflight
  Why: assumption: the cwd, PATH and stdin hazards recur (bare `fm`, cwd vs root). One preflight printing the effective `fm` path, cwd and root catches them before any work.
  Done when: `fm lane new` on a fixture prints the resolved `fm`, worktree root and git dir, and exits nonzero when `fm` resolves outside the worktree.

- **Wild: Run a replay of every past red review finding against each new lane diff** — FEATURE — value 4 — effort L — risk med — category: regression memory
  Why: wild; assumption: confirmed findings carry enough shape (file, pattern) to be turned into cheap grep-style detectors, so a recurring defect class like "lock re-entry" gets flagged before review.
  Done when: a test with a stored lock-re-entry finding flags a new diff repeating the pattern and passes a clean diff.

- **Wild: Keep a flaky-host mode that fingerprints load at each gate failure** — FEATURE — value 3 — effort M — risk low — category: gate honesty
  Why: wild; the dropped retry idea had a false premise (merge runs no criteria), but `fm check` already reruns once. Recording load at red and printing "red under load" at close lets a human trust or discount it.
  Done when: a red gate run with a faked high load average carries a `strained: true` field in the ledger and the close summary says so.

- **Wild: Turn the user's AFK stretch into a self-verifying "return receipt"** — FEATURE — value 4 — effort M — risk low — category: trust
  Why: wild; builds on `fm away` and `fm todo`. Each line in the receipt would carry a re-runnable proof command, and the receipt itself re-checks them at read time, flagging any that no longer hold.
  Done when: `fm away --verify` reruns the proof commands of closed tasks since the last user message and marks one deliberately broken fixture task as "no longer holds".

- **Wild: Bound the loop with a no-new-value stop** — FEATURE — value 3 — effort S — risk low — category: loop reliability
  Why: wild; the forever loop's "until dry" has no recorded definition. Stopping a round when the new-idea rate and survived-build rate both fall under a threshold prevents runaway spend; assumption: rounds already log both counts.
  Done when: a fake-ledger test with two consecutive rounds of zero accepted ideas makes `fm loop` stop with a printed reason.

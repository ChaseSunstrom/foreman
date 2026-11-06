# Brainstorm — lens: bold bets

- **Pre-mortem every plan** — FEATURE — value 5 — effort M — risk low — category: planning
  Why: tasks take hours and the close-out and gate time is already measured. A Haiku pass that writes "the three likeliest ways this fails" into the brief before execute catches wrong approaches before an 8-minute `cargo test` loop. The user's pushback is almost always about wasted time. Assumption: failures are mostly predictable from the brief and the repo's recent history.
  Done when: a new brief gets a "Risks" section of at least 3 items before it can reach `ready`, and a test fails if it's missing.

- **Learn rules from corrections** — FEATURE — value 5 — effort M — risk med — category: memory
  Why: the user's corrections repeat (letters mean nothing, clean up output, no commands handed to them). Each one lives in the user's head and gets re-explained each project. Foreman should detect a correction in the captured text, write it as a dated, sourced preference, and check later output against it. Assumption: corrections can be told apart from new requests with a cheap classifier.
  Done when: after a correction like "L, T, M mean nothing", a later task's output is checked against it, and a test shows the preference was stored with its source and applied.

- **Estimate hours before starting** — FEATURE — value 4 — effort M — risk low — category: time
  Why: "takes hours" is a complaint, but the user only learns the cost after the fact. The 287-task history gives a per-project distribution (gate minutes, ceremony calls). Showing "likely 40 min, 3 gate runs" at plan approval lets them cut scope up front. This differs from the existing receipt, which is retrospective, and from the budget the plan must fit, which is a constraint rather than a forecast. Assumption: task size words correlate with duration in the ledger.
  Done when: plan approval shows a duration range, and over the backlog at least 70% of tasks finish inside it.

- **Quarantine slow gates** — PERFORMANCE — value 4 — effort M — risk med — category: gates
  Why: one project's `cargo test` takes a median of 8 minutes and runs about once per task. Track per-test duration and flakiness, and move the slowest tests to a close-only tier. The proposals so far only skip tests that the diff cannot reach; this one tiers by cost. Assumption: the test runner emits per-test timings.
  Done when: a mid-task gate runs under 2 minutes on that project and the full suite still runs once at queue end.

- **Split briefs into parallel worktree lanes** — FEATURE — value 4 — effort L — risk high — category: parallelism
  Why: the queue runs strictly in series while tasks wait on gates. Briefs that declare disjoint files could run in separate git worktrees at the same time and merge at the end. Assumption: most queued briefs touch disjoint files.
  Done when: two disjoint briefs run at once in separate worktrees and merge without conflict, with wall time under 70% of serial.

- **Show intent beside the request** — FEATURE — value 4 — effort S — risk low — category: capture
  Why: the user says brainstorming misses "things I want but don't know how to say". At capture time, restate the request as "what I think you actually want" plus one thing nearby that you didn't ask for, and let one key accept or edit it. Assumption: a one-line restatement is cheap enough to run on every capture.
  Done when: a capture shows a restated intent line, and accepting it writes it into the brief.

- **Wild: Hold a "user simulator" review** — FEATURE — value 4 — effort M — risk med — category: audit
  Why: the audits use reviewer lenses about code. Add a fork primed with the user's own words and corrections that reads the finished output and answers "would they complain about this?" before close. This catches noisy output and unexplained letters, the actual complaints in the pack. wild
  Done when: a seeded noisy-output fixture is flagged by the simulator, and a clean one passes.

- **Wild: Auto-rewrite the user's vague asks into a spec game** — FEATURE — value 3 — effort M — risk med — category: capture
  Why: "super improve it, etc." gives little to work with. Foreman could answer with three concrete one-line interpretations as a quick pick, and learn which kind the user picks over time. wild; assumption: picks are cheap for the user and sharpen the briefs.
  Done when: a vague request produces three selectable readings, and the pick is stored and used to bias the next set.

- **Wild: Run a "Foreman vs. Foreman" benchmark** — PERFORMANCE — value 3 — effort L — risk med — category: self-improvement
  Why: nothing proves a change made Foreman faster or smarter. Replay a fixed set of 10 recorded tasks against two Foreman versions and compare wall time, calls and tokens, so each improvement session has a score. wild; assumption: tasks can be replayed deterministically on stubbed models.
  Done when: one command prints a table of time, calls and tokens for two versions on the same task set.

- **Rank the inbox by value for effort** — FEATURE — value 3 — effort S — risk low — category: inbox
  Why: the older inbox (T-0077 to T-0094) has been waiting while new features jump ahead. Score each item by hours saved or complaints it ends and surface the top three at queue start. Assumption: the ledger can estimate value per item.
  Done when: queue start lists three inbox items with a one-line reason each.

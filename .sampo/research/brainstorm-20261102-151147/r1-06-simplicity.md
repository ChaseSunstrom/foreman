# Brainstorm — lens: simplicity

- **Make every new capability pay a one-in, one-out toll** — CLEAN — value 5 — effort M — risk low — category: growth control
  Why: the ideas list is dominated by additions (verbs, gauges, doctor rows); 30+ "Later from" deferrals and a 1388-file skills tree show accretion with no counterweight. Existing "swap rule" and "pay-down ledger" ideas are proposals; none is a gate keyed on a count.
  Done when: `fm ship` fails a diff that adds a verb, hook, or doctor row without a same-diff removal or a recorded waiver, proven by a red-first test with a planted addition.

- **Collapse `fm doctor` into one verdict line plus a red-only list** — FEATURE — value 4 — effort S — risk low — category: observability
  Why: many earlier ideas add doctor rows (c16, c17, c19). assumption: doctor output is already long. Existing ideas cover "red only" and "calm line" separately; this fixes the contract: one line when green, and every row must name its single fix command.
  Done when: on a green home `fm doctor` prints exactly one line; on a red one, each line ends with a runnable command.

- **Give steers a size and count budget at store time** — CLEAN — value 4 — effort S — risk low — category: user rules
  Why: the standing rules above run 40+ entries and many are paragraph-long and truncated in the pack. Every session injects them. Prior ideas fold or compile steers after the fact; none stops the growth at entry.
  Done when: `fm decide` rejects a steer over 200 characters or the 41st active steer without naming one it supersedes.

- **Print one "what to do now" line from bare `fm`** — FEATURE — value 4 — effort S — risk low — category: user value
  Why: the user's recent asks are over a hundred distinct verbs and flags. A newcomer or returning user should not need MASTER.md. assumption: bare `fm` currently prints a long help.
  Done when: bare `fm` prints at most 3 lines: current task, next command, and `fm help` pointer.

- **Delete the verbs that have no session path, behind a tombstone** — CLEAN — value 4 — effort M — risk med — category: dead code
  Why: standing rule says every capability must be called by a real session path, and `fm genesis check` reach already names offenders. Turning that list into removals (with a one-line "removed, use X" error) is the missing step.
  Done when: each verb the reach check names is gone or wired, and invoking a removed one prints its replacement and exits nonzero.

- **Make the brainstorm pack a diff, not a dump** — PERFORMANCE — value 4 — effort M — risk low — category: context cost
  Why: this pack carries roughly 3,000 prior idea titles, many near-duplicates ("cold read", "unproven", "tick"). Each lens pays that token cost and still repeats. Send cluster headings with counts and a ten-title sample per cluster.
  Done when: the pack for a brainstorm is under 40% of the current size and a replayed brainstorm shows no rise in duplicate proposals.

- **Stop the tower writing a new gauge unless a decision reads it** — CLEAN — value 4 — effort M — risk low — category: measurement
  Why: the idea list repeatedly asks for gauges nobody can falsify and numbers recorded but never deciding. Enforce at creation, not by later audit.
  Done when: a lint fails the build when a ledger field or gauge has no reader that changes an exit code, a note or a task.

- **Fold the three ship-time gates into `fm gate`** — CLEAN — value 3 — effort S — risk low — category: developer experience
  Why: map lists three gates (`fm doctor`, roundtrip e2e, bench_hooks) run separately; ideas to combine exist but no one named the single entry with one exit code.
  Done when: `fm gate` runs all three, prints one pass/fail line per gate, and `fm ship` calls only it.

- **Cap injected session-start text to a fixed line budget with overflow behind `fm why`** — PERFORMANCE — value 4 — effort M — risk med — category: context cost
  Why: T-2667 just made burden counts reveal hook_success stdout; ratchet ideas exist, but the simplest rule is a hard cap with the rest fetched on demand.
  Done when: SessionStart output never exceeds N lines in a test with 50 notes queued, and the dropped ones are listed by `fm why`.

- **Wild: Run a "one-page Foreman" week** — CLEAN — value 3 — effort L — risk med — category: radical subtraction (wild)
  Why: assumption: a core of guard, plan, prove and queue is what most users feel. Build a branch whose entire doc set fits one page and see which removed things anyone misses.
  Done when: a branch passes the ship gate with MASTER.md under 150 lines and a log lists each capability the user asked back.

- **Wild: Make deferred tasks expire into a single `someday.md`** — CLEAN — value 3 — effort S — risk low — category: backlog (wild)
  Why: 30 "Later from T-xxxx" deferrals sit open and show up in `fm next` and packs. A deferral untouched for 60 days becomes one line in a file and leaves the queue; a matching new capture revives it.
  Done when: after 60 simulated days the open-task count drops by the stale ones and a matching capture reopens the line.

- **Wild: Let a cold child try to explain Foreman in five sentences, and fail the docs if it can't** — FEATURE — value 3 — effort S — risk low — category: docs (wild)
  Why: README, MASTER.md and the site grow with every Mission; a tool-less child reading only them is a cheap legibility test no earlier idea ran on the whole product.
  Done when: `fm doctor` records the child's summary and flags when it omits the guard, the plan-prove loop, or the queue.

- **Refuse to file a brief that restates one already in the catalogue** — CLEAN — value 3 — effort S — risk low — category: intake
  Why: T-2659 and the dropped list show many "already built" slate items (fm replay, fm usage --prune). Check by running the three phrasings against verb help strings at filing time.
  Done when: filing a brief whose key phrase matches an existing verb's help prints that verb and files nothing without `--force`.

Next question: Which single verb, doctor row and steer would the user say they could lose today without noticing?
Next question: What is the smallest set of `fm` verbs that covers the user's last 100 actual command invocations?

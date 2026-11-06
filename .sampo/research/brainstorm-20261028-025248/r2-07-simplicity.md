# Brainstorm — lens: simplicity

- **Use the host's task list for single-session work** — FEATURE — value 3 — effort M — risk med — category: scope
  Why: Foreman's backlog and journal add a second task system beside Claude Code's own. assumption: the host's task list survives compaction and is visible to hooks, so a one-task request can skip the backlog.
  Done when: a single-task request closes with no backlog file written, and `fm status` still lists it.

- **Print every fm error as one sentence and one runnable command** — CLEAN — value 4 — effort S — risk low — category: output
  Why: gate and guard messages run to several lines and bury the fix. assumption: most errors have one obvious next step that can be stated in one line.
  Done when: a test over the error corpus finds no fm error line longer than 120 characters, and each ends with a command that runs.

- **Show where each effective setting came from, one line each** — CLEAN — value 3 — effort S — risk low — category: config
  Why: defaults, the rules file and environment variables all override one another, and nothing shows which one won. assumption: the config loader already sees every source, so the report costs little.
  Done when: `fm config` prints one line per key with its source, and a test fails when any key has no source.

- **Make the verb-and-flag count a budget every change must pay for** — CLEAN — value 4 — effort S — risk low — category: surface
  Why: "net-negative lines" measures code, but users learn verbs and flags. assumption: a count of top-level verbs plus flags tracks how hard the product is to learn.
  Done when: CI fails if the count rises in a change that does not also list a removal.

- **Keep only the hook events Claude Code documents as stable** — CLEAN — value 3 — effort S — risk low — category: hooks
  Why: each undocumented or experimental hook event is a failure mode the bench has to cover. assumption: the stable events are enough for every guard Foreman runs.
  Done when: the installed hooks config references only events listed in the pinned Claude Code docs, checked by a test.

- **Write the journal as plain lines that cat and grep can read** — CLEAN — value 3 — effort M — risk med — category: state
  Why: reading the current JSON state needs a parser and the hand-made lock. assumption: one line per event carries every field the surfaces read.
  Done when: `grep T-1213` on the journal finds every event for that task, and `fm status` output on the fixture is unchanged.

- **Count the human decisions per closed task and file a bug above three** — FEATURE — value 4 — effort S — risk low — category: flow
  Why: the user keeps asking Foreman to stop asking them things. assumption: each decision is already logged as a prompt or an auto-decision, so the count can be read from the journal.
  Done when: `fm digest` prints decisions per task, and a closed task with more than three gets a filed FIX.

- **Stop a rules-file line when it reads longer than one sentence** — CLEAN — value 2 — effort S — risk low — category: rules
  Why: the rules file is loaded every session and its budget is already over once. assumption: long rules are where contradictions and dead text hide.
  Done when: the doctor flags any rules line over 25 words, and the rules file passes with no flagged line.

- **Keep the first-run path to one question and one plan** — FEATURE — value 4 — effort M — risk med — category: onboarding
  Why: `fm init` and the first request each ask for setup. assumption: most settings can be inferred from the repo and shown for approval, not typed.
  Done when: a fresh repo reaches a printed plan after one question, with no config file written before approval.

- **Wild: print the whole product on one index card and fail the build if it overflows** — CLEAN — value 3 — effort S — risk low — category: docs
  Why: the product has more verbs, settings and modes than a new user can hold. assumption: a one-card summary forces the cuts that the other ideas only suggest.
  Done when: the build generates the card from the verb table, and the build fails when the card runs past one page.

- **Wild: show the status as one number with one unit** — FEATURE — value 3 — effort S — risk low — category: glance
  Why: the user reads the status at a glance, and a calculator-style display is faster than a sentence. assumption: the one number can be the budget left in days, which the user already cares about.
  Done when: `fm status` prints one line with one number and one unit, and the number matches `fm cost` on the fixture.

- **Wild: a reading-level gate for the rules file** — CLEAN — value 2 — effort S — risk low — category: rules
  Why: the rules file is read by the model every session, so plain wording costs less and misreads less. assumption: a simple readability score catches the worst lines.
  Done when: the rules file scores below the set grade on the test, and the build fails above it.

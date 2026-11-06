# Brainstorm — lens: simplicity

- **Shrink the skills tree by injection receipts** — CLEAN — value 4 — effort M — risk med — category: skills
  Why: `plugin/skills/` holds 1,158 of 1,524 files, and the prune ideas so far target verbs, not skills or cards. assumption: the injection ledger records which card or skill was injected each turn.
  Done when: a test with a ledger where two cards were never injected in 60 days makes `fm tidy` list exactly those two as delete candidates, with their last-injected dates.

- **Prune flags by usage, not just verbs** — CLEAN — value 3 — effort S — risk low — category: CLI surface
  Why: the existing prune work covers whole verbs (`fm usage --prune`), but flags like the escape hatches pile up inside verbs that stay in use. assumption: usage data can be recorded per flag.
  Done when: a fixture where a verb ran 50 times and one flag never ran prints that flag as a candidate under `fm usage --prune --flags`.

- **Retire tests that have never failed and cover nothing unique** — CLEAN — value 3 — effort M — risk med — category: tests
  Why: `plugin/tests/` has 211 files, and the gates are slow enough to need caches and affected-first selection. A test that has never gone red and kills no mutant others miss is only cost. assumption: mutation results can be stored per test.
  Done when: `fm tidy --tests` on a fixture with a duplicate test (same mutants killed, never red) lists it and no other test.

- **Give every refusal one three-part shape: what, why, do** — CLEAN — value 3 — effort M — risk low — category: messages
  Why: the guard's "it could be …" guess and the nearest-command suggestion are each hand-written, and the guess shows odd paths. A single template with a lint makes the messages shorter and testable. assumption: refusal strings are scattered across fmguard and fmcli.
  Done when: a test iterates every refusal fixture and asserts each has exactly the three parts and is under 240 characters.

- **Replace guard regexes with a small shell tokenizer** — CLEAN — value 4 — effort L — risk high — category: guard
  Why: T-0275 (guard reads what scripts run) keeps growing a regex pile (`_track_vars`, `_proved_writes`, `_writes_unrun_source`). One tokenizer that yields words, redirects and substitutions would remove most of them. Replaying the 33 mined refusals gives a ready oracle.
  Done when: all guard tests plus the replay corpus give identical verdicts under the tokenizer and the regex count in fmguard is lower.

- **Keep a single "Foreman is off" switch that proves it is off** — FEATURE — value 3 — effort S — risk low — category: reversibility
  Why: simplicity means the user can always step back out. The eject and Lite ideas exist, but there is no one-line check that proves hooks, mod and settings are all inert.
  Done when: after `fm off`, a recorded hook stdin run produces no output and no file writes, and `fm on` restores the previous behaviour byte-for-byte.

- **Count concepts in the README and cap them at a fixed number** — CLEAN — value 3 — effort S — risk low — category: docs
  Why: the README has a long pitch plus many verbs, cards, lanes, lenses and gates. Capping the page length is covered, but capping distinct nouns a newcomer must learn is not. assumption: a glossary of defined terms can be extracted by script.
  Done when: a test fails when the README's defined-term count exceeds the ceiling, and names the newest term.

- **Fold `fm ideas`, `fm review` and the plugin workflows into one `fm round`** — CLEAN — value 3 — effort M — risk med — category: workflow
  Why: the recent commits add /foreman:review and /foreman:ideas on top of `fm ideas`, `fm mission` and the loop. One verb with stages (review, brainstorm, build, release) leaves one thing to learn and one thing for the autonomous drive to call.
  Done when: `fm round --dry-run` prints the stage list and each old entry point delegates to it with a test proving identical output.

- **Wild: Run the whole gate suite once with all state deleted** — FEATURE — value 3 — effort M — risk low — category: hidden state
  Why: assumption: much behaviour depends on stale caches, ledgers and `.foreman/` leftovers. A stateless run exposes hidden dependencies, and any difference from the normal run is a candidate to delete.
  Done when: `fm doctor --cold` runs the gates in an empty state dir and diffs pass/fail against the normal run, reporting each divergence by file.

- **Wild: Store all machine state in one SQLite file** — CLEAN — value 4 — effort L — risk high — category: state
  Why: briefs, ledger, flake data, usage, fixes and leases are each their own file format and reader, and the idea list has brief indexes, ledger sidecars and torn-write checks for them. One transactional store removes the need for most of that. This is a bet on a rewrite, so it should start with read-only mirroring.
  Done when: a mirror command builds the DB from existing files, and `fm next` reads from it with identical output to the file readers on a fixture.

- **Wild: Make `fm` print only the next one command when asked "what now"** — FEATURE — value 4 — effort S — risk low — category: onboarding
  Why: the user is AFK-driven, and weak local models do better with one choice than with a menu. assumption: `fm next` already computes the ranking but prints several lines.
  Done when: `fm now` prints exactly one line, a runnable command, and the same state produces the same line.

- **Delete a verb's tests, docs and help entry as one unit** — CLEAN — value 3 — effort M — risk med — category: deletion
  Why: deletions leave stragglers (docs, tier entries, completions, tests), and the repo sweep exists because of this. A single `fm retire VERB` that removes all of them and leaves a tombstone would make deletion as cheap as adding.
  Done when: a fixture verb is removed by `fm retire`, then `fm doctor` and the full gate show no references to it, and invoking it prints the tombstone.

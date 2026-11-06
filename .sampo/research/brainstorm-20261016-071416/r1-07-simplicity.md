# Brainstorm — lens: simplicity

- **Resolve bare `fm` to the worktree's own copy** — FIX — value 4 — effort S — risk low — category: lanes
  Why: the review notes say builders in a lane can't run their own new `fm` flags, because bare `fm` hits the main checkout; they must type `python3 plugin/bin/fm`.
  Done when: a test in a lane worktree with a new flag runs `fm <verb> --newflag` and reaches the worktree's code, and outside a worktree it still reaches the installed copy.

- **Make the commonly guessed commands work** — FEATURE — value 4 — effort S — risk low — category: dx
  Why: builders and weak agents guess `fm task list`, and the error now only suggests the nearest match. Replace the nearest-match hint with real aliases mined from the unknown-command log.
  Done when: a test feeds the three most frequent logged unknown commands and each runs the intended verb with the same output, with no alias shown in help.

- **Parse reviewer output into findings automatically** — FEATURE — value 5 — effort M — risk med — category: review
  Why: defect classes feed builder briefs, but `fm task finding` is one manual call per finding, so the feed starves. Assumption: reviewer output has parseable structure, or can be asked to have it.
  Done when: a test runs a fake reviewer result with two findings through the review step and `fm task finding` data holds both, with no manual call.

- **Show full refused commands in the friction digest** — FEATURE — value 4 — effort S — risk low — category: guard
  Why: grounding guard friction needed a hand-written transcript miner, and two premises were false only after mining. The digest counts refusals but never shows the commands.
  Done when: `fm friction --commands` lists each refusal with its full command and its `fm guard try` verdict, and a test with two seeded refusals sees both.

- **Drop the guard's "it could be …" guess unless the path exists** — FIX — value 2 — effort S — risk low — category: guard
  Why: the guess glues a command word into paths such as `/repo/cd/w.out`, which misleads.
  Done when: a test with `cd w && cmd > w.out` prints no guess containing a nonexistent directory, and a real-path case still prints its guess.

- **Give deferred briefs a revisit-by date that expires them** — FEATURE — value 3 — effort S — risk low — category: queue
  Why: 37 deferred briefs piled up until a manual triage, and 11 still wait on external evidence. Prevent the pile instead of deleting it later.
  Done when: a test with a deferred brief past its revisit date sees `fm tidy` close it as expired, and one with a future date is untouched.

- **Make the plugin workflows thin wrappers over `fm` verbs** — CLEAN — value 4 — effort M — risk low — category: workflows
  Why: /foreman:review and /foreman:ideas run only when the user types them, so the autonomous drive can't use them. One implementation in the verbs serves both.
  Done when: a test shows the workflow file only invokes `fm review` and `fm ideas`, and the drive can call `fm review` headless.

- **Dedupe the context pack** — FIX — value 3 — effort S — risk low — category: brainstorm
  Why: this pack prints "The user's own words" twice, and four "steered" lines read only "re-queued by the deferred triage" with no task id. That is noise that costs tokens in every lens child.
  Done when: a golden test on pack output shows each section once and every steer line carrying a subject.

- **Leave a tombstone when a verb is deleted** — CLEAN — value 3 — effort S — risk low — category: deletion
  Why: the idea list proposes many deletions (prune by usage, collapse flags), and each breaks muscle memory and agent habits. A tombstone makes deletion cheap and safe. Assumption: `fm usage` can tell who still calls a removed verb.
  Done when: a removed verb prints one line naming its replacement and exits 2, and the tombstone expires after N releases by test.

- **Give every new flag an expiry release** — CLEAN — value 3 — effort M — risk low — category: flags
  Why: the escape-hatch flags keep multiplying (see the proposal to collapse them into `--because`). An expiry makes the flag count self-limiting. Assumption: flags can carry metadata in the registry.
  Done when: CI fails for a flag whose expiry is at or before the current version, and passes after the flag is removed or renewed with a reason.

- **Wild: Add a "cold small model" smoke path** — FEATURE — value 4 — effort M — risk med — category: weak-models
  Why: the user wants Foreman to work for weak or small local models (assumption: a local engine is available). Run the five-verb core loop against a tiny model and fail the release gate if it can't close a toy task.
  Done when: a gate runs a toy task end to end with a stubbed small model transcript and reports the pass or fail verb that broke.

- **Wild: Make `fm` answer a question, not a verb** — FEATURE — value 3 — effort L — risk med — category: interface
  Why: guessed names (`fm task list`) show people think in questions. Route "what's open", "what's blocked" and "what do I owe" to the existing readers via a small fixed phrase table, with no model call.
  Done when: `fm "what's blocked"` prints the same output as `fm next --blocked`, and an unknown phrase falls back to the nearest-verb hint.

- **Wild: Run a weekly "one thing less" report** — FEATURE — value 3 — effort M — risk low — category: deletion
  Why: the idea list is long on additions, so make subtraction a ritual. Pick the least-used verb, flag, hook rule and card, and show the proof that each can go, as one capture-ready line each.
  Done when: `fm tidy --less` prints exactly four candidates with usage counts and a capture command each, and a test with seeded usage data picks the right four.

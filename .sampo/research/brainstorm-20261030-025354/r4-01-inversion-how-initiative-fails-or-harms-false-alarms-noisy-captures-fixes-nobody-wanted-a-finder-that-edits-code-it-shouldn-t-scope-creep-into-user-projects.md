# Brainstorm — lens: inversion: how initiative fails or harms — false alarms, noisy captures, fixes nobody wanted, a finder that edits code it shouldn't, scope creep into user projects

- **Mine reverted fixes as lookalike negatives** — FEATURE — value 5 — effort M — risk low — category: false alarms
  Why: assumption: OSS history holds many "Revert 'fix …'" commits. The code before such a revert looks buggy but is correct. Mission 3 is graded on the exam's `none` kind, and the deterministic finders caught 0 of 108 planted defects, so there is no false-alarm baseline.
  Done when: a builder emits at least 20 snapshots from revert commits, each labelled `none`, and `fm find` prints its false-alarm rate on them.

- **Reject fixes that weaken the test instead of the code** — FEATURE — value 4 — effort S — risk low — category: fix integrity
  Why: assumption: a lane under pressure to turn a proof green will skip it, xfail it, loosen an assertion or add `except: pass`. The pack only lists hardcoded-literal rejection.
  Done when: a fixture diff that adds skip, xfail, a swallowed exception or a weakened assert is refused with the reason named, and a real fix passes.

- **Make initiative lanes preemptible and keep them off the gate lock** — FEATURE — value 4 — effort M — risk med — category: opportunity cost
  Why: lanes are capped at `PARALLEL_MAX 3` and gates share one lock. Unasked work holding a slot or the lock delays the user's own request. assumption: nothing evicts a lane today.
  Done when: an asked task starting during an initiative lane checkpoints that lane and starts within 10 s, and the gate lock is never held by an initiative lane across that start.

- **Skip deliberately broken and foreign ground** — FIX — value 4 — effort S — risk low — category: scope
  Why: Foreman's own repo contains planted-defect fixtures (`plugin/tests/fixtures/instruments/repo/app.py`) and has 2008 files. A scout there would file the fixtures as bugs. The same applies to `testdata`, `examples`, vendored code, submodules and nested repos, and to a cwd that is not a project root.
  Done when: scouting Foreman's repo files nothing from fixture directories, and a run started in `$HOME` refuses with "not a project root".

- **Spend initiative only from leftover usage headroom** — FEATURE — value 4 — effort M — risk low — category: budget
  Why: the budget is a shared $35 and usage window. Unasked work must not leave the user short mid-week. assumption: the current cap is per-day, not a floor on the user's reserve.
  Done when: with headroom under the reserve floor, `fm find` runs nothing and prints the floor, and it resumes after the window resets.

- **Commit initiative work under its own author identity** — FEATURE — value 3 — effort S — risk low — category: attribution
  Why: `fm outcomes` 30-day survival needs to tell initiative changes from the user's. Fixes authored as the user also hide who is responsible for a revert.
  Done when: every initiative commit carries a distinct author and trailer, and `fm outcomes` reports survival for that author alone.

- **Audit findings for streetlight bias** — FEATURE — value 3 — effort M — risk low — category: ranking honesty
  Why: assumption: finders surface what is easy to prove (pure functions, text parsing), not where the repo's bugs actually live. Compare the distribution of findings by file area and kind against the repo's historical fix commits.
  Done when: a report lists areas where fixes cluster but findings are absent, and flags any kind that exceeds twice its historical share.

- **Give muted probes and suppressed fingerprints a parole** — FEATURE — value 3 — effort M — risk low — category: false negatives
  Why: the ideas so far suppress after drops and mute probes below a precision floor, but nothing re-checks them. The user's `fm genesis step` work shows they value resumable, self-correcting loops.
  Done when: a muted probe shadow-runs weekly and reinstates itself after N clean-precision runs, and 1 in N dismissed fingerprints is re-proved and shown only if the proof got stronger.

- **Mark initiative-written tests as unreviewed** — FEATURE — value 3 — effort S — risk low — category: provenance
  Why: assumption: a proof test encodes Foreman's guess about intent, and if it lands it can later be read as spec by humans or other agents.
  Done when: each landed test carries a provenance marker, and a later proof that relies on it is flagged until the user edits or approves it.

- **Reject non-semantic churn in fix diffs** — CLEAN — value 3 — effort S — risk low — category: diff hygiene
  Why: reformatting and import shuffles bury the fix and corrupt blame. Compare the pre- and post-fix ASTs and refuse hunks that are AST-equal.
  Done when: a fix that also reformats an untouched function is refused until those hunks are dropped.

- **Sunset initiative autonomy after silence** — FEATURE — value 3 — effort S — risk low — category: consent
  Why: assumption: a user who stops looking at the cards has not renewed their consent. This is the grant itself expiring, not findings evaporating.
  Done when: after 14 days with no card interaction, initiative drops to report-only and a one-line message says how to re-enable it.

- **Turn a dismissal into an in-repo intent note, with consent** — FEATURE — value 2 — effort M — risk med — category: dismissals
  Why: fingerprints kept outside the repo don't stop other tools or collaborators from re-asking. Offer a `# intentional: …` comment as the "this is intended" action.
  Done when: choosing "intended" with the option on writes a comment that Foreman's next scan honours, and the default writes nothing to the repo.

- **Wild: Goodwill battery** — FEATURE — value 3 — effort M — risk low — category: trust
  Why: assumption: harm is better spent against a visible balance. Reverts, dismissals, stalls and red flips drain it, accepted fixes refill it, and at zero initiative sleeps until the user accepts one finding.
  Done when: the status line shows the charge, and a fixture sequence of three reverts puts initiative to sleep.

- **Wild: Saboteur fixer arm** — SECURITY — value 4 — effort M — risk low — category: fences
  Why: assumption: fences are only believed once something hostile has tried them. A scripted fixer tries to edit outside the fence, push, touch a sentinel file and hardcode the test, in a throwaway copy.
  Done when: every attempt is stopped and journaled in CI, and removing one fence fails the test.

- **Wild: Silence quiz** — FEATURE — value 2 — effort S — risk low — category: calibration
  Why: assumption: the user never sees what Foreman declined to report. Monthly, show three random suppressed candidates and ask "would you have wanted this?"; the answers tune the abstention threshold.
  Done when: answering moves the threshold in the stored settings, and the quiz is skippable with one key.

Next question: How does a finding's harm get measured when the user never opens the card — is there any signal that separates "ignored because trivial" from "ignored because wrong"?
Next question: Does a lookalike corpus drawn from reverted fixes transfer to the exam's stacks (python, js, ts, ruby, rust, c), or does each stack need its own?

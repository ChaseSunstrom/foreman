# Brainstorm — lens: night shift: what runs unattended while the user sleeps and leaves proven, ranked, ready-to-merge lanes by morning

- **Run the find→prove→fix pipeline as a nightly shift with a hard budget** — FEATURE — value 5 — effort L — risk med — category: night shift
  Why: Mission 3 asks for find, prove, fix, rank; `fm night` only queues `fm run --fit --max 2` and `fm adopt` is one-shot and manual. Plain Claude fixes held-out bugs at about 0.17 USD each, so a shift of N findings has a predictable ceiling. Assumption: the night job can read the remaining weekly headroom.
  Done when: `fm night --find` on a fixture repo with 3 planted bugs ends with 3 lane branches, each holding a failing-then-passing test, and stops with a spend line when the cap is hit.

- **Reject any finding that has no failing reproduction before a lane opens** — FEATURE — value 5 — effort M — risk low — category: proof gate
  Why: The exam shows the deterministic finders caught 0 of 108 planted defects. The "none" kind is also graded, so unproven findings are worse than none. Assumption: a reproduction can be a script exit code when a test framework is absent.
  Done when: a seeded "none" repo (no defects) produces 0 lanes and a morning note listing the candidates dropped, each with the reason its repro did not fail.

- **Rank the morning list by value per dollar with a shown formula** — FEATURE — value 4 — effort M — risk low — category: ranking
  Why: The request names "ranks findings by value", but the pack has no ranking input. Inputs it could use: severity kind, blast radius from file fan-in, whether the touched file is hot in `git log`, lane cost, and the user's past accepts. Assumption: past merges and drops on similar findings are logged.
  Done when: `fm findings` prints a table sorted by score, each row shows its score terms, and a test checks that a security finding on a hot file outranks a docs finding.

- **Ship a morning card: merge-ready lanes first, one key to land or drop** — FEATURE — value 4 — effort M — risk low — category: morning review
  Why: The user keeps asking for outward steps (ship to main, re-record, re-match the site) by hand. Each lane arrives with its failing-test proof, a diff size, a rebase-on-main result, and a one-line undo.
  Done when: after a night run, `fm morning` lists lanes with proof status and `fm morning land 1` rebases, re-runs gates, and merges only if they are green.

- **Let a second cold reviewer veto each night fix before it reaches the card** — FEATURE — value 4 — effort M — risk med — category: verification
  Why: The standing steer says weakness-finding comes from outside signals such as `fm second cold review`. A fix that hardcodes the test literal passes its own proof. Assumption: a reviewer given only the diff and the finding can be run cheaply.
  Done when: a planted fix that special-cases the test input is vetoed and shown on the card as "vetoed: hardcoded literal".

- **Probe the project by running it, not reading it** — FEATURE — value 5 — effort L — risk med — category: finders
  Why: Static scans found 0 of 108. Bugs show up when the code runs. A scout lane runs the existing tests and a property or fuzz pass on each public function in its sandbox, then keeps the crashes and the invariant breaks as candidates.
  Done when: on 5 held-out repos with a planted bug, the probe finds at least 3 as a failing input, with no model call needed for the detection.

- **Stop probe_doctor from filing Foreman's own setup faults in user projects** — FIX — value 3 — effort S — risk low — category: scout hygiene
  Why: Noticed in the Mission 3 brief: probe_doctor may queue Foreman setup failures as tasks in a user project, which would put noise on every morning card.
  Done when: a project with a broken Foreman hook produces a doctor warning and zero backlog tasks from scout.

- **Keep a per-project "settled" list so nightly shifts stop re-filing declined findings** — FEATURE — value 3 — effort S — risk low — category: dedupe
  Why: A nightly job repeats itself. Without memory the same dropped finding comes back every morning, and the user has already shown that repeated noise is something they steer against.
  Done when: a finding dropped on Monday does not appear on Tuesday's card unless the code under it has changed.

- **Wild: run the flake finder as a hundred-run night soak with a verdict per test** — FEATURE — value 3 — effort M — risk low — category: flake
  Why: Flakes cannot be proven in one run, and nights are free time. Assumption: tests can run in an isolated tmpdir with shuffled order and a logged seed.
  Done when: a fixture with one order-dependent test is reported with a failing seed and a repro command, and a stable test is reported clean.

- **Wild: a nightly mutation pass that marks tests which pass when they shouldn't** — FEATURE — value 3 — effort L — risk med — category: test strength
  Why: The "untested" kind exists in the exam. A mutant that survives is a proven weakness with a built-in failing test: the mutant must fail.
  Done when: on a fixture, a survived mutant becomes a finding whose new test fails against the mutant and passes on the original.

- **Wild: replay last night's merged fixes against tonight's tree as a regression canary** — FEATURE — value 3 — effort S — risk low — category: trust
  Why: Fixes are proven once. The `fm outcomes` 30-day survival signal is slow, but rerunning each shipped finding's failing test nightly is fast.
  Done when: reverting a previously shipped fix on a fixture makes the next night's card say which finding regressed.

- **Wild: a bet ledger where each night's shift predicts its own yield and gets scored** — FEATURE — value 2 — effort S — risk low — category: calibration
  Why: Questions left by earlier brainstorms ask what a generation costs. A shift states "expect 2 proven fixes for about 0.50 USD", and the card shows the result next to it.
  Done when: after 5 shifts, `fm night stats` prints predicted against actual yield and spend per shift.

- **Split findings by risk into auto-lane, ask-first and report-only** — SECURITY — value 4 — effort M — risk low — category: authority
  Why: Unattended work in the user's repo needs a scope. A security finding that changes auth should wait for a human, while a null-check fix can go to a lane. Assumption: kind plus touched paths can set the tier.
  Done when: a finding touching a path in the protected list yields a report with no lane, and a test shows the night run wrote nothing outside `fm/*` branches.

- **Run the same shift on `fm code` models with the cheapest arm that proves** — PERFORMANCE — value 3 — effort M — risk med — category: cost
  Why: Foreman's session costs more than plain Claude for the same score, and nights tolerate slow cheap models. Assumption: `fm code` can pick a model per finding.
  Done when: a shift report lists the model used per finding and the total is lower than an all-top-model baseline on the same fixture.

Next question: What stops a night shift from finding a real bug in a repo whose test harness it cannot run, and what should the morning card say then?
Next question: Do user merges and drops of night lanes get fed back into ranking, or does each shift start with no memory of what was welcome?

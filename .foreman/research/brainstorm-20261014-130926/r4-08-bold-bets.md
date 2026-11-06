# Brainstorm — lens: bold bets

I'm at saturation: nearly every bold-bet direction is already in the pile in some form. These ideas are fusions and second-order bets that earn their place only as one object, each replacing several separate dials or stubs already listed.

- **Write a signed Autopilot Charter per unattended stretch** — FEATURE — value 5 — effort L — risk med — category: autonomy
  Why: round 1 shipped push, wake, effort and budget caps as separate knobs, and "etc. etc. etc." is a standing mandate. The pile has about eight partial answers (walk-away check, spend envelope, irreversibility budget, kill switch, end-state promise). Fuse them into one charter file (budget, blast radius, allowed channels, revert triggers, promised end state) that the guard, scheduler, push and return card all read.
  Done when: `fm away 3h` writes a charter, a test run that exceeds one clause parks the work, and the return card names the clause.

- **Close FEATURE tasks by ramping a flag, not by merging** — FEATURE — value 4 — effort L — risk high — category: delivery
  Why: assumption: the user's product has a flag or deploy hook. The pile ends at "landed/released" ladders and canaries for consumers. This makes "done" mean ramped at 1%→100% with an auto-revert on a declared signal.
  Done when: a fixture project's task stays open until the flag reaches 100%, and a seeded error spike reverts it and reopens the task.

- **Export the ledger as a change-management evidence pack** — FEATURE — value 3 — effort M — risk low — category: compliance
  Why: assumption: team or client use. Attestations, hash chains and time sheets are all listed, but nothing maps evidence to named controls (approver, model, test proof, rollback) in an auditor-readable bundle.
  Done when: `fm audit-pack T-id` emits a self-contained folder where every control row links to a ledger event, and a tampered event fails verification.

- **Make `fm round close` produce a one-screen decision card** — FEATURE — value 5 — effort M — risk low — category: recursion
  Why: the user said "recursively improve" and "etc. etc.", and the board is unticked after round 1. The pile has many round-ledger ideas but none that collapses them into one card. The card shows the delta in measured numbers, the single least-used shipped feature marked for deletion, and the next round's three decisions, each with a default.
  Done when: closing a fixture round prints ≤20 lines containing a metric delta, a delete candidate and 3 defaulted questions, and an unanswered card auto-applies the defaults after the stated timeout.

- **Gate every self-edit on "would this have changed a real past decision?"** — SECURITY — value 4 — effort M — risk med — category: self-change
  Why: round 1 changed guard, compact output and the lane merge. Replay corpora exist as ideas, but there is no rule that an edit must *demonstrably alter or preserve* a recorded verdict. Hook and guard diffs are classified as loosened, tightened or neutral against recorded payloads, and a "loosened" result needs a yes.
  Done when: a seeded guard change that allows one previously blocked command is labelled "loosened" and refuses to merge without approval.

- **Add a "Foreman-off" differential on every close** — FEATURE — value 4 — effort M — risk low — category: proof of value
  Why: the pile contains comparison bench ideas but nothing at the per-task level. A cheap model predicts, from the brief and diff, which gates and nudges actually changed the outcome, and the close card lists "caught by Foreman: N, would have shipped broken: 0".
  Done when: closing a task with a seeded failing verify shows it as a catch, and a clean task shows "nothing caught".

- **Wild: Hand the queue to a rival harness overnight and diff the results** — FEATURE — value 3 — effort L — risk med — category: benchmarking
  Why: wild. Adapters exist for Codex, Gemini and opencode and are unverified (T-0336). Run the same S-task twice with the same gates, once on each harness, and show who passed cheaper. This turns the blocked live-verify task into a standing benchmark.
  Done when: one nightly run writes a two-column cost-and-pass table for 3 S tasks.

- **Wild: Offer a "premortem tape" the user can scrub before approving an L plan** — FEATURE — value 3 — effort M — risk low — category: planning
  Why: wild. Instead of a prose premortem, simulate the plan's likely failure branches from the failure fingerprints and show a short branching tape: "step 3 fails 30%, here's what you'd see". It reuses the failure-fingerprint and step-graph ideas as one visual.
  Done when: an approval card for a fixture L plan shows ≥2 branches, each with a historical failure id.

- **Wild: Let the user hold one "veto token" per day that reverts any Foreman-initiated change, no questions** — FEATURE — value 4 — effort S — risk low — category: trust
  Why: wild. The user's steers and drops show repeated pushback after the fact. A scarce, guilt-free `fm veto` (one key) restores the pre-change state, logs the reason as a taste signal, and costs nothing to explain.
  Done when: `fm veto` reverts the last Foreman-initiated change in a fixture and appends one steer record.

- **Reconcile deferrals nightly against what the user actually did** — FEATURE — value 4 — effort M — risk low — category: queue hygiene
  Why: 14 deferred clusters, T-0787–T-0799 captured, and blocked items with unlock conditions. A nightly pass checks each unlock trigger against git, the ledger and the Claude Code version, then promotes, expires or merges them.
  Done when: seeding a Claude Code version bump that satisfies one trigger promotes exactly that task and leaves the others untouched.

- **Pair every shipped hook with a counterexample the model must not trigger** — CLEAN — value 3 — effort M — risk low — category: false positives
  Why: the guard's false positives show up in the dropped items (the `$_` heredoc case). A hook whose "doing nothing" cases are not recorded can't be tightened safely. Each hook gets a "must not fire" fixture set generated from real passes.
  Done when: a new rule cannot merge unless its fixture set has ≥3 must-not-fire cases drawn from the ledger.

- **Wild: Run a "Foreman Sabbath" that deletes before it builds** — FEATURE — value 3 — effort S — risk low — category: simplicity
  Why: wild. After a round of additions, the next round must net-delete lines. The round close card shows "+812 / −1,140" and refuses to start a new feature task until the net is negative.
  Done when: `fm round close` records net lines and blocks a FEATURE start while the previous round's net is positive.

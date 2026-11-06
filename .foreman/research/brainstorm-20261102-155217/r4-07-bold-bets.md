# Brainstorm — lens: bold bets

- **Land unattended work on a probation ref** — FEATURE — value 5 — effort M — risk low — category: landing
  Why: assumption: overnight and drive output goes straight into the tree or main. The pack shows push grants, `fm ship` and a post-push watch idea, but no soak stage between "closed" and "landed".
  Done when: with a fake clock, an unattended close lands on `refs/foreman/probation/T-N`. It is promoted to main only after N hours with CI green and no user edit to the touched lines. A planted user edit in that window blocks promotion and produces a conflict note.

- **Run an N-version hunk consensus on risky tasks** — FEATURE — value 4 — effort L — risk med — category: verification
  Why: T-0335/36/37 are blocked on non-Claude harnesses, and "same ask on two models" is only a diff-of-diffs idea. Hunks that two independent builders both produce, or that a proof discriminates, are strong evidence.
  Done when: `fm duo T-N` applies the agreed hunks, lists the disputed ones, and drops a planted wrong hunk injected into one arm.

- **Let peer Foremen negotiate cross-repo contracts** — FEATURE — value 4 — effort L — risk med — category: fleet
  Why: assumption: several registered repos depend on each other. "Fix once, fan out" covers identical fixes but not an API change in A that breaks B.
  Done when: changing an exported symbol in repo A files a task in repo B carrying a failing consumer proof, and both tasks close only when both repos are green.

- **Set autonomy by value-at-risk** — FEATURE — value 4 — effort M — risk med — category: autonomy
  Why: the pack has Kelly sizing, irreversible-grant caps and a stall-USD stop, but no single dial. The user states a tolerable loss per night in dollars and hours of cleanup. Foreman fits it to the loss distribution from guard saves and landed-then-reverted outcomes.
  Done when: `fm run --var 5usd` picks a ceremony and scope. A replay over history shows the 95th-percentile loss at or below the stated bound.

- **Govern chatter with a churn-hazard score** — FEATURE — value 4 — effort M — risk low — category: user trust
  Why: T-0864 (keep-or-leave check-in) is deferred for lack of a safe channel. The user's drops, overrides, ignored `Next:` lines and `fm off` uses are already in the ledgers. "Simplify" is ambiguous, so a quiet governor is the safe reading.
  Done when: a score from those signals is shown in `fm doctor`. Above a threshold, nudges and slate sizes halve, and a test shows the output shrinking.

- **Finish the safe tail of an interrupted session** — FEATURE — value 4 — effort M — risk med — category: continuity
  Why: assumption: a laptop closed or a window exhausted mid-task leaves tests, docs and changelog undone. Related ideas finish in-flight proofs, but none finishes the non-code tail.
  Done when: a killed session with an open task yields a patch on a side branch containing only tail work, each item with a proof, and it never touches files the user last edited.

- **Solve the night's schedule as one constraint problem** — FEATURE — value 4 — effort M — risk low — category: scheduling
  Why: auctions, file-overlap prediction, quota windows, a deadline-backward plan, user rhythm and `needs:` are all listed separately. A single plan with an explanation line would replace several heuristics.
  Done when: `fm plan-night` prints an ordered schedule and the constraint that bound each choice. Re-running on a fixed fixture is deterministic, and an infeasible fixture names the conflict.

- **Run every capability through a lifecycle ladder with auto-demotion** — CLEAN — value 4 — effort M — risk low — category: lean
  Why: the pack shows 1388 skill files, a 525-idea catalogue, 30+ deferred "Later from" tasks and lean rows waiting on measurement. The ladder is experimental → shadow → default → core, with the gauge that moves a capability up or down declared up front.
  Done when: every verb and skill carries a rung. A capability with no measurement for 30 days drops one rung, and `fm doctor` lists the moves.

- **Emit one typed Verdict record from guard, prove, finish gate and doctor** — CLEAN — value 4 — effort M — risk med — category: verification
  Why: the pack repeats ideas for a third state, override-is-not-proof, a cause on every gate trip and a Next on every exit. These are one record shape with a state, cause code and next command.
  Done when: all four emitters write the same schema. A scan test finds no gate that can print a bare pass or fail, and `fm why` renders any record.

- **Wild: pool expiring quota across the user's accounts and machines** — FEATURE — value 3 — effort L — risk high — category: spend
  Why: assumption: the user has more than one account or machine, which the open question "which of these needs the user's other machines" hints at. The pack has "spend the expiring quota first" for a single account only.
  Done when: with two fake accounts at different window expiries, the router sends a measurement task to the one that expires sooner and records why.

- **Wild: run a release radar from drift hashes** — FEATURE — value 3 — effort L — risk high — category: host canary
  Why: canaries against beta host CLIs are listed locally. Consenting installs could share only a hash of the hook payload shape after a host upgrade. "Your host updated and 40 installs saw this shape change" arrives before anything breaks.
  Done when: a simulated payload change yields a matching hash from two fake installs and a pre-emptive degraded-mode flag, with nothing but the hash leaving the machine.

- **Wild: run a bet-to-ship contract that the user can cancel in advance** — FEATURE — value 3 — effort M — risk med — category: anticipation
  Why: Mission 7 has predictions and drafts, but the user never commits to anything. At the end of the day the user can pre-sign "tomorrow, if I touch X, start Y". Foreman stages Y on probation and shows hits and misses.
  Done when: a signed pre-commitment fires only on its trigger, is discarded after 3 days, and the morning card lists fired, missed and cancelled.

- **Wild: audit by an oracle that carries the user's disbelief** — FEATURE — value 3 — effort M — risk med — category: proof
  Why: the pack shows the user re-running proof commands by hand and a disbelief button idea. A one-key "don't believe this" re-proves by a different method. Each use is also a labelled data point on which proof kinds the user trusts least.
  Done when: the key spawns a re-proof using a method other than the original, and the result is stored against the proof kind in a trust table.

Next question: which of Foreman's autonomous outputs does the user never review, and what has gone wrong in them unnoticed?
Next question: what would the user have to see in the first morning of a week away to trust the tower the next night?

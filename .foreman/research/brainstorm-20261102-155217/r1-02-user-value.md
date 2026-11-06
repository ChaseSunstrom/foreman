# Brainstorm — lens: user value

I read the pack through the user-value lens. Much of the obvious ground is already on the list, so these are second-order moves on what the user keeps having to do by hand. Evidence is cited where the pack has it, and the rest is marked as assumption.

- **Reply to Foreman by editing a file** — FEATURE — value 4 — effort M — risk low — category: user value
  Why: assumption: the user's steers, drops and approvals all arrive as typed prose or `fm` verbs, and the pack shows `fm ask` timing out and blocked items piling up. A watched `inbox.md` with checkboxes and one-line answers would remove the verb to remember.
  Done when: ticking a box in the file closes the matching `fm ask` within one tick, with a ledger record naming the file edit as the source.

- **Write every task title in plain words and lint for jargon at filing** — FIX — value 4 — effort S — risk low — category: legibility
  Why: filed titles read like "c13: Guard: ledger, replay, red team, packs, shadow". The user's own drops show they re-ground these by hand.
  Done when: `fm add` rejects or rewrites a title that carries a cluster id, a coined noun with no glossary entry, or more than 72 characters, and a test plants one of each.

- **Send a try-it card the moment a capability lands** — FEATURE — value 4 — effort S — risk low — category: adoption
  Why: a standing rule says every capability must be called by a real session path, but nothing tells the user how to feel it once. The card carries one command and one expected visible result, and nags once after 7 days of no use.
  Done when: closing a FEATURE task prints a card with a copy-paste command whose output matches the card, and an unused card produces exactly one reminder.

- **Declare a plateau and go quiet** — FEATURE — value 4 — effort M — risk med — category: spend
  Why: the tower must advance until DONE-WHEN holds, and the budget is $200. When a generation's free-arm gauges and cold reads show no movement, the useful behaviour is to say so and stop spending.
  Done when: after N generations with zero net change in the free arms, the drive writes a one-line plateau notice and starts no new Mission until a new signal appears.

- **Show a standing-intent drift gauge per generation** — FEATURE — value 3 — effort M — risk med — category: trust
  Why: the standing intent sits over every steer, so the user's real worry is whether the work is still pointed at it. A cold child scores each Mission against the intent, and the generation report shows the trend.
  Done when: each generation report has a drift score computed by a cold child that sees only the intent text and the Mission titles, and a planted off-intent Mission lowers it.

- **Digest what reached main under the push grant** — FEATURE — value 4 — effort S — risk low — category: trust
  Why: the user said to push to main at any time without asking. A daily list of what was pushed, with its gate result and a revert command per commit, keeps that freedom safe to give.
  Done when: `fm ship` appends to a `pushed.md` digest, and the session-start card shows pushes since the user last looked.

- **Batch every question into one dated decision sheet with a default and a deadline** — FEATURE — value 3 — effort M — risk low — category: attention
  Why: the standing rule is never to block on the user, yet some questions remain (caps only the user can raise, outward actions). One sheet per day, with each item's default shown, turns many interruptions into one glance.
  Done when: all pending user-only items render in one place, and a timed-out item applies its stated default and records it as a costly decision.

- **Rank the blocked list by what one user action would free** — FEATURE — value 3 — effort S — risk low — category: unblocking
  Why: T-0325, T-0418, T-0352 and T-0335 to T-0337 have been blocked on the user's hardware, installs or accounts for a long time. One screen ranking them by the work each would free makes the cheapest action obvious.
  Done when: `fm next --blocked` lists each blocked task with its single required user action and the count of tasks it would release.

- **Wild: let the user scrub a week of the tower as a short "season recap"** — FEATURE — value 3 — effort L — risk low — category: delight
  Why: wild. The report is read once a run, but the user steers across days. A scrubbable web view would show what changed, what was dropped and which steer caused it, one frame per day, built from existing ledgers.
  Done when: a local page renders seven daily frames from the ledgers and every frame links to the task ids and steer ids behind it.

- **Wild: let the user veto a past Foreman decision and replay the run without it** — FEATURE — value 4 — effort L — risk high — category: control
  Why: wild. Costly decisions are made on the user's behalf and recorded for the final report. A veto that re-runs the affected Missions in a lane shows what would have differed, before the user commits to it.
  Done when: vetoing a recorded decision creates a lane that redoes only the dependent tasks, and a diff against the landed result is printed.

- **Wild: grade Foreman's work by a stand-in for the user's taste, trained on their drops** — FEATURE — value 3 — effort L — risk med — category: judgement
  Why: wild. The pack holds many drops with stated reasons ("already built", "second-order", "measured and refuted"), a labelled set that can serve as the user's judgement. A tool-less child that sees only those labels predicts keep or drop on each new slate before the user sees it, and its hit rate is published.
  Done when: the stand-in scores a held-out set of past slates, and its agreement with the user's actual drops is reported next to the slate.

- **Report the cost of ownership of Foreman's own standing rules** — FEATURE — value 3 — effort M — risk low — category: simplicity
  Why: more than 40 steers are in force, and each injects text and blocks or checks something. The user cannot tell which ones are paying for themselves.
  Done when: `fm steers --cost` lists each rule with injected characters per session, how often its check fired, and how often it changed an outcome.

Next question: which of the user's standing steers have never changed an outcome, and would the user keep them if shown that?
Next question: when the user reads a Genesis report, which single line do they act on first, and does anything in the pack track that?

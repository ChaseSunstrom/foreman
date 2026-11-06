# Brainstorm — lens: inversion: what makes Foreman obsolete

- **Race the engineered predictor against the raw ledger in a long-context model** — FEATURE — value 5 — effort S — risk low — category: anticipation
  Why: assumption: a long-context model reading the last 30 days of ledgers cold may predict the next ask as well as the n-gram and follow-up tables. If it does, the table machinery is the first thing to go obsolete.
  Done when: one command scores both arms on the same sealed asks and prints hit rate and cost side by side, with a test fixture where the arms differ.

- **Draft only when the draft beats the next queued task** — FEATURE — value 5 — effort M — risk low — category: anticipation
  Why: the pack lists 30+ open or deferred tasks and the user wants "major progress by morning". Predicting a new ask is worth nothing while a known, better task sits in the queue. Inverting the question shows when anticipation is the wrong spend.
  Done when: each draft record carries a "vs queue head" verdict, and a test shows no draft is made while an equal-or-higher-value task is unclaimed.

- **Render the 80 standing steers as one CLAUDE.md and use it as the baseline** — FEATURE — value 5 — effort M — risk low — category: necessity
  Why: the steers are mostly instructions. If a plain agent given them as one file matches Foreman on held-out scenarios, only the residual (guard, proof, drive) justifies the machinery. This arm is not in the earlier list, which compares against a bare model, not a steers-only one.
  Done when: `sampo louhi` has a "steers-only" arm, and the scorecard names which capabilities it already matches.

- **Tag every capability with its moat class and spend on the user-specific ones** — FEATURE — value 4 — effort S — risk low — category: strategy
  Why: assumption: a host or model upgrade absorbs generic features, but not "what this user always asks after a FIX" or "this machine's 3-minute model switch". The class (host-gap, model-gap, user-specific) tells anticipation which signals are worth collecting.
  Done when: every Mission brief carries a `moat:` field, and the sweep fails on a brief without one.

- **Compare against the host's own next-prompt suggestion** — FEATURE — value 4 — effort M — risk med — category: anticipation
  Why: assumption: Claude Code or another host can already propose the next prompt. Recording its suggestion beside Foreman's and scoring both on what the user actually typed is the direct test of whether this Mission is duplicate work.
  Done when: a test ledger shows host-suggested and Foreman-predicted columns scored over 14 days, and the predictor mutes itself where the host wins.

- **Harvest what a capability learned before it retires** — FEATURE — value 4 — effort M — risk low — category: exit value
  Why: a retired capability takes its lessons, steers and predictions with it. Compiling them into host-native files (AGENTS.md, CLAUDE.md, GEMINI.md) first means the knowledge survives even if Foreman does not. This relates to the existing "compile steers into other harnesses' files" idea but is triggered by sunset.
  Done when: retiring a verb in a scratch home writes a plain-file export, and a cold agent given only that export passes one held-out scenario the verb used to help with.

- **Add an obsolescence watch to `fm doctor` with four measured tripwires** — FEATURE — value 4 — effort M — risk low — category: strategy
  Why: assumption: Foreman most likely dies of one of four causes. The host ships it, a bare model stops failing the gates, the user stops reading its output, or the user's asks stop being predictable. Each has a number already in the ledgers, but none is watched together.
  Done when: doctor prints four lines with value, threshold and trend, and a planted decline flips one to red in a test.

- **Measure whether the drafted brief beats the raw ask, per model** — FEATURE — value 4 — effort M — risk low — category: scaffolding
  Why: the steer is to scaffold small local models up to frontier results. A scaffold that a model ignores, or that a stronger model no longer needs, is dead weight. Running raw ask against drafted brief on the same model tells which rung to keep.
  Done when: the Model bench prints brief lift per model and task kind, and rungs with lift ≤ 0 across 3 runs are listed for removal.

- **Time how fast the user-model rebuilds from scratch** — PERFORMANCE — value 3 — effort S — risk low — category: moat
  Why: assumption: if deleting the accumulated user-model and rebuilding from git history alone reaches parity within a day, the stored state is not a moat. If it takes weeks, it is, and it deserves backups and care.
  Done when: a scratch-home drill deletes the model, replays history, and prints days-to-parity against the baseline.

- **Wild: Race today's build against the one from 90 days ago on a sealed set** — FEATURE — value 4 — effort L — risk med — category: honesty
  Why: wild. The tower grows every generation, but nothing shows whether the newer build does more on the same scenarios. If no gap shows after two generations, growth halts and the next Seed is subtraction-only.
  Done when: the sweep runs both builds on the free arms and prints the delta, and a generation with zero delta files a stop task.

- **Wild: Run a goal-file-only day** — FEATURE — value 3 — effort M — risk med — category: autonomy
  Why: wild. Perfect anticipation means the user types nothing and edits only a GOALS file. Simulating that day shows which Foreman verbs still need a typed ask, and those are the real gaps.
  Done when: a scratch drive runs 8 hours from a goal file alone and the receipt lists every point it paused for a typed instruction.

- **Wild: Hold an obituary writer, a cold child that argues for each tripwire** — FEATURE — value 3 — effort S — risk low — category: strategy
  Why: wild. Once a quarter, a tool-less child gets only the doctor tripwires and the closes and writes the strongest "Foreman is no longer needed because…" case. The user sees the one argument the numbers cannot answer.
  Done when: the case is written to the tower and each claim in it cites a ledger line or is marked unsupported.

Next question: which of Foreman's closes would a bare model with the steers file have landed identically, and what does that share look like by task kind?
Next question: what is the cheapest event that shows the user has stopped reading the morning card, and does any ledger already record it?

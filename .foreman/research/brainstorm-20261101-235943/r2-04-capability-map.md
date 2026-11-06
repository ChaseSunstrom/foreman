# Brainstorm — lens: capability map

Capability map for #3 Anticipation. Reference points are Cursor Tab and Copilot next-edit, Warp and atuin next-command, Renovate and Dependabot, Sentry and Linear triage, and Rewind. The pack's catalogue already covers next-verb n-grams, prediction books, speculative lanes, machine-exhaustion forecasts and the departure warning, so I skip those. Below are the capabilities it doesn't show.

**Earlier question my lens can answer:** many of the 58 cells are one capability counted under several stages. Probes for roughly seven predictor families (next ask, correction, breakage, resource, queue, steer, style) would cover them. Each family needs a probe per surface, not a prose cell per stage.

- **Checkpoint before the context window runs out** — FEATURE — value 4 — effort M — risk low — category: forecasting
  Why: the pack plans compaction faults, "rehydrate the plan after compaction" and usage-wall forecasts, but nothing forecasts the context limit. Assumption: transcript size is readable from the hook payload.
  Done when: a fixture session at 85% of the window gets a baton written, and a forced compaction resumes from it with the plan intact.

- **Flag open tasks a commit made moot** — FEATURE — value 4 — effort M — risk low — category: queue
  Why: the pack shows 28 deferred "Later from T-07xx" bundles and several tasks dropped as already built (T-0862/0863, the guard-only arm). Today the check runs only at capture time.
  Done when: after a fixture commit that implements a deferred task's DONE-WHEN, `fm next` names that task with the commit and proposes a drop. It never drops on its own.

- **Quote a task's time and cost when it is created** — FEATURE — value 4 — effort M — risk low — category: estimation
  Why: the steers cover usage pace, budget caps and waiting out limits, but the user never sees a per-task estimate. Assumption: the ledger has kind, size and token cost.
  Done when: `fm task new` prints a range from kind×size history, and `fm task finish` records the error. A backtest on closed tasks shows it beats a flat median.

- **Dry-run the plan's steps through the guard at plan time** — FEATURE — value 4 — effort S — risk low — category: breakage
  Why: the guard blocks only when a command runs, mid-lane, which strands unattended work. The standing intent is "flags problems before they happen".
  Done when: a plan containing `rm -rf` of a protected path is flagged at plan accept with the rule and a safe alternative. A clean plan prints nothing.

- **Run the cold-read charter on your own diff before filing** — FEATURE — value 3 — effort M — risk med — category: pre-review
  Why: the cold-read rule is Haiku first, then Sonnet, and T-2547 added a refusal for ungrounded Missions. Predicting the FAIL saves a round trip. Assumption: Haiku's FAIL verdicts correlate with Sonnet's.
  Done when: over 20 past cold reads, the pre-read predicts the final verdict at least 80% of the time. Otherwise it is not shipped (the same bar as the backtest rule).

- **Answer the user's usual follow-up questions in the close receipt** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: assumption: the "asked" stream shows recurring follow-ups such as "did you run the tests" and "what's left". The receipt could pre-answer the top three per task kind.
  Done when: the close receipt holds those lines, filled from evidence rows. A fixture where tests didn't run says so.

- **Learn the reply-style profile from corrections** — FEATURE — value 3 — effort M — risk med — category: user model
  Why: the user model covers requests, corrections and habits but not the shape of answers. Assumption: "too long" and "just do it" corrections exist in the transcripts.
  Done when: one injected line states length and format preferences by task kind. It is shown by `fm me` and deletable, and an ablation shows fewer style corrections.

- **Weight cell re-verification by churn of the cited file** — CLEAN — value 3 — effort S — risk low — category: coverage rot
  Why: the questions left ask whether a filled cell's file still behaves as claimed. Re-running all 58 probes each sweep is wasteful.
  Done when: the sweep orders cells by commits touching the cited file since the claim, and a planted behaviour change in a rarely edited file is still caught by the periodic full pass.

- **Sweep pinned model IDs, flags and API versions for retirements** — FEATURE — value 3 — effort M — risk low — category: external drift
  Why: the environment lists model IDs, and fm routes to specific tiers. Retired IDs break unattended lanes silently. Assumption: retirement dates come from a local list the user updates, with no network by default.
  Done when: a fixture config pinning a retired ID gets a WARN from `fm doctor` and a filed task naming the files.

- **Wild: Tired-hour mode** — FEATURE — value 2 — effort M — risk med — category: user model
  Why: wild. Correction density by hour from timestamps, so Foreman tightens gates and shrinks autonomy when the user's own record shows more mistakes at that hour.
  Done when: a planted history with late-night corrections raises plan-depth for a late-hour fixture, and `fm me` shows the evidence and an off switch.

- **Wild: Unwritten-rules extraction** — FEATURE — value 4 — effort M — risk med — category: user model
  Why: wild. A tool-less child reads only a month of the "asked" stream and writes the rules the user follows but never stated. The user marks each right or wrong, and each right one becomes a steer with its automatic check.
  Done when: the output lists ≥5 candidates with quoted evidence, and a confirmed one lands through `fm decide --check`.

- **Wild: Weekly duel against a blind predictor** — FEATURE — value 3 — effort M — risk low — category: measurement
  Why: wild. It extends the standing "free arm beats session arm" rule. Each week a tool-less child predicts last week's asks from prior context only, and the result is compared with fmforesight.
  Done when: `fm exam scorecard` prints both hit rates, and a week where the child wins is listed first.

- **Wild: Pre-answer "why didn't you warn me"** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: wild. When the user reports a breakage, `fm why-not` replays foresight at the prior commit and shows what it knew, so each miss is either a bug in the model or a missing input.
  Done when: for a planted breakage the output names the signal that existed or states that none did.

Next question: Which predictors would still produce something if every transcript were deleted, and what does the user see then?
Next question: Which cell claims are checked only by file existence, never by behaviour, and what is the cheapest behavioural probe for each?

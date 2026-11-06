# Brainstorm — lens: inversion: how a self-running harness fails: the same miss recurs, corrections are forgotten, subagents run on the priciest model, stopped lanes rot, work waits for the user, hooks and context bloat, predictions are never scored

- **Reopen a fix when its signature returns** — FIX — value 5 — effort M — risk low — category: self-repair
  Why: T-2272 turns a failure signature recurring across 3+ tasks into one FIX task, but nothing checks that the fix held. A closed fix whose signature reappears is the same miss recurring.
  Done when: a test closes a signal-fix task, replays its signature, and sees a linked regression task opened and counted in `fm doctor`.

- **Turn each user correction into a failing-first test** — FEATURE — value 5 — effort M — risk med — category: corrections
  Why: steers get `fm decide --check`, but the "dropped" and "asked" corrections (T-2285, T-2289, T-2327) have no automatic check. They were found only because the user asked again.
  Done when: a recorded correction produces a test that fails on the pre-fix commit and passes on the fix, and `fm doctor` names any correction without one.

- **Replay corrections on every ship** — CLEAN — value 4 — effort S — risk low — category: regression
  Why: assumption: corrections are stored as prose, so a later self-improvement can undo one silently.
  Done when: `fm ship` runs the corrections suite and a deliberately reverted correction turns the ship red.

- **Justify every top-tier model pick** — FEATURE — value 4 — effort S — risk low — category: cost
  Why: T-2291 escalates by history, but nothing flags a lane that started on the priciest model with no failed cheaper attempt.
  Done when: `fm lane brief` prints a one-line reason for the model, and `fm doctor` lists top-tier lanes that have no prior cheaper failure.

- **Retire or recover stopped lanes on a clock** — FIX — value 4 — effort M — risk med — category: lanes
  Why: T-2289 shows lanes holding scratch folders that block `fm lane rm`. Stopped lanes accumulate and nothing owns them.
  Done when: a lane idle past N hours is either resumed with a fresh brief or salvaged and removed, and a test kills a lane and sees one of the two happen.

- **Age every blocked-on-user task and bundle the yeses** — FEATURE — value 4 — effort S — risk low — category: waiting
  Why: many tasks sit blocked (T-0325, T-0335, T-0352, T-0418), and queued installs wait for "one yes". Nothing shows how long each has waited.
  Done when: one command lists blocked-on-user items by age with a single approve-all prompt, and an item older than 7 days is escalated.

- **Break trigger storms with a per-trigger budget** — SECURITY — value 4 — effort M — risk low — category: self-triggering
  Why: T-2276 measures trigger precision but only lowers priority. A bad watcher can still fire unattended work without limit.
  Done when: a simulated trigger firing 20 times in an hour is cut off at its cap and the cutoff is shown in `fm triggers`.

- **Fence auto-fixes away from the guard and hooks** — SECURITY — value 5 — effort S — risk low — category: guard
  Why: the signal-to-fix loop and the self-repair mission can write fixes without being asked. The guard is the one thing that must not drift (§6, T-2252).
  Done when: an auto-filed fix that touches guard or hook files is parked for the user, and a test asserts it.

- **Make the lean ratchet pay by deletion and load skills lazily** — PERFORMANCE — value 4 — effort L — risk med — category: lean
  Why: the ratchet only warns on growth. Ship went red on the 6,400-char rules budget while the user asked for "many more skills", and `plugin/skills/` already holds 1,388 files.
  Done when: only skill descriptions are always-on, a skill body loads on a match, and the always-on size stays flat as a test adds 50 skills.

- **Mute predictors that lose to the baseline** — FEATURE — value 4 — effort M — risk low — category: anticipation
  Why: T-2290 scores predictions but nothing acts on a bad score, so wrong ones keep being shown.
  Done when: a predictor worse than the same-tier median over 20 closes is muted and `fm doctor` says so.

- **Detect fix-of-fix churn** — CLEAN — value 3 — effort S — risk low — category: self-repair
  Why: assumption: self-repair that edits the same files repeatedly means the root cause was missed. The loop reads recurrence, not churn.
  Done when: three auto-fixes on one path within 14 days become one root-cause task instead of a fourth patch.

- **Wild: Run a nightly amnesia drill** — FEATURE — value 4 — effort M — risk low — category: corrections
  Why: wild. Replay the user's last 20 corrections to a cold child and count how many it repeats the old mistake on. The result is a forgetting rate nobody has to trust Foreman about.
  Done when: a nightly report shows a forgetting rate, and planting one broken correction raises it.

- **Wild: Shrink autonomy while the user is away** — SECURITY — value 3 — effort M — risk med — category: leash
  Why: wild. A self-running harness drifts furthest when nobody looks. After N days without user input it narrows its own grants and triggers, and widens them again on the user's return.
  Done when: simulated silence of N days cuts the live trigger set and grants, and one command restores them.

- **Wild: Let a cheap model bid first on every lane step** — PERFORMANCE — value 3 — effort L — risk med — category: cost
  Why: wild. The cheapest model tries each step against a hidden check and only a failure escalates. Router history then comes from real races instead of past guesses.
  Done when: a benchmark shows lower cost at equal pass rate than the history router on the same scenarios.

- **Wild: Send a morning "what ran while you slept" bill** — FEATURE — value 3 — effort S — risk low — category: observability
  Why: wild. Every unattended trigger, lane, model and dollar from the night, ranked by cost, with a one-word undo per item.
  Done when: after a simulated night with three triggered runs, one message lists each with cost and an undo.

Next question: Which self-made fixes were later reverted or re-fixed by the user, and what did the signal loop think of them when it filed them?
Next question: What is Foreman's measured forgetting rate for a correction after 30 days, by someone other than Foreman?

# Brainstorm — lens: user value

- **Print a one-line repo hello on `cd`** — FEATURE — value 4 — effort S — risk low — category: surfaces
  Why: assumption: the user's first minute in a repo is a shell prompt, and every surface in the pack (pane, web UI, session start) needs a session open first. A `chpwd` hook would print open tasks, "N things landed since you last looked" and any degraded flag, read from a precomputed file.
  Done when: `cd` into a registered repo prints at most 2 lines in under 50 ms, and `cd` into an unregistered one prints nothing.

- **Offer time-boxed work bundles** — FEATURE — value 4 — effort M — risk low — category: queue
  Why: about 30 "Later from T-…" tasks sit deferred, and the existing ideas rank by value or yield. None fits work to the slot the user has: a 10-minute, 1-hour or evening bundle that bundles tasks by forecast cost and the one decision each needs.
  Done when: `fm slot 1h` lists a bundle whose summed p50 forecast is ≤ 60 minutes and names every user decision it needs.

- **Learn ceremony per task kind from the user's turns-to-close** — FEATURE — value 4 — effort M — risk med — category: calibration
  Why: T-1266 (ceremony profile per kind) is deferred on duel data. The user's real cost is their own messages per closed task, which the ledgers already hold. Count those per kind and ceremony level, pick the level with the fewest turns at equal reopen rate, and replay it with zero tokens.
  Done when: a replay table shows median user turns per (kind, ceremony) across closed tasks, and a test proves the chosen default changes when the fixture data flips.

- **Explain every cost outlier on its receipt** — FEATURE — value 3 — effort S — risk low — category: receipts
  Why: spend caps, stall-usd and forecasts exist, but nothing in the pack says why a given task cost 5× its kind's median. The receipt would carry the top 3 contributors (retries, re-reads, a child spawn, a usage-limit wait) when cost exceeds 3× median.
  Done when: a fixture task at 4× median prints a "Why it cost more" block naming a contributor that sums to at least 50% of the excess.

- **Snooze with a reason and a wake condition** — FEATURE — value 3 — effort S — risk low — category: queue
  Why: the pack has wake-on-evidence and decision deadlines, but no plain `fm snooze T-x 3d "after round 1"` that hides an item and brings it back with its reason. Deferred tasks currently pile up with no return date.
  Done when: a snoozed task is absent from `fm next` until its date, then reappears with the stored reason on top.

- **Split-offer oversized forecasts at pick time** — FEATURE — value 3 — effort M — risk med — category: planning
  Why: assumption: the forecasts (T-2645's clock work and the cost readers) are enough to flag a task above 3× the kind's p50. Today the pack only refuses or caps. Offer a split into 2–3 sub-tasks, each with its own proof, so the L-sized deferred items (T-0034, T-0035) become landable pieces.
  Done when: picking an over-forecast task prints a proposed split, and accepting it files the children with proofs and closes the parent only when they all close.

- **Compute lesson confidence with zero tokens (unblock T-0217)** — FEATURE — value 3 — effort M — risk med — category: learning
  Why: T-0217 has been deferred. It needs only two existing ledgers: recall events and first-time-pass outcomes. Joining them gives each lesson a confidence now. Lessons that never preceded a pass fall out of injection, which also addresses the "injected lines get used" gap.
  Done when: `fm lessons` shows a confidence and sample size per lesson, and a lesson with n < 5 is labelled "too few" rather than scored.

- **Cache claim-resolution results by tree hash** — PERFORMANCE — value 2 — effort S — risk low — category: brainstorm
  Why: the grounding step now runs canary searches and spot checks on every brief. Re-grounding the same claim against an unchanged tree repeats the work, and the drops show re-grounding happens often (c16, c17 and c21 were all re-checked).
  Done when: a second grounding of the same claim on an unchanged tree makes 0 searches, and a changed file invalidates only the claims that cite it.

- **Show a minutes-saved estimate before enabling anticipation** — FEATURE — value 4 — effort M — risk low — category: anticipation
  Why: Mission 7 is anticipation, and the pack has backtests and hit rates but no number in the user's own units. Replay the last 30 days of asks, count how many a pre-staged answer would have hit, multiply by typical turn time, and print "this would have saved about X minutes and shown Y false cards". Anticipation stays off until the user has seen it.
  Done when: `fm anticipate --backtest 30d` prints hits, false cards and an estimated minutes figure, and it makes no model calls.

- **Wild: alert on a missing ritual** — FEATURE — value 3 — effort M — risk low — category: anticipation — wild
  Why: assumption: the user's weekly habits (ship, doctor, steer review, digest read) are regular enough to model. Existing ideas predict the next ask. This one flags what did not happen: "you usually ship every 3 days and it's been 9". It is a dead-man's switch on the user's own cadence.
  Done when: with a fixture where a weekly event is skipped twice, one card names it, and it doesn't fire for events that were never regular.

- **Wild: preview a month of silence on request** — FEATURE — value 3 — effort M — risk low — category: forecasting — wild
  Why: the pack covers a "week of silence" rehearsal for tests and fake-clock months for timers. Nothing answers the user's question "what happens if I leave for a month?". With the pinned clock (c.clock) and the drive in dry-run, show the projected queue, spend, expiring grants and what would stop.
  Done when: `fm away 30d` prints projected closes, dollars, grants that expire and the first stop reason, and it changes no state.

- **Wild: name an "ask under the ask" at intake** — FEATURE — value 4 — effort M — risk med — category: anticipation — wild
  Why: the user's brainstorm asks come as bundles (c14 to c24), and the dropped remainders show the real need was often smaller or already built. A cold child restates each ask as the need behind it plus the one thing the user would ask next, and files both only if the second one clears the recency baseline.
  Done when: on 20 past asks, the restated need matches the user's later steer or follow-up at least as often as the baseline in a blind check.

- **Rank stalled work by days since the user last mentioned it** — FEATURE — value 2 — effort S — risk low — category: queue
  Why: assumption: the user's attention is the best signal of what is alive. A task or inbox item the user named in no message for 30 days gets demoted automatically, with a one-key "still wanted" reply.
  Done when: an item with no user mention for 30 days moves to a "quiet" shelf with its last-mentioned date, and one reply restores it.

Next question: which of these ideas would the user have asked for within a week anyway, so that anticipation only makes it arrive sooner?
Next question: what is the user's real cost per Foreman turn in minutes, and is it measured anywhere the other value ideas could use?

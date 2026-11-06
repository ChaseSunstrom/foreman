# Brainstorm — lens: invented: eight hours asleep

- **Gate each night phase on the last phase's yield** — FEATURE — value 4 — effort M — risk low — category: overnight
  Why: assumption: the 8 hours run as one flat drive. Sealed plans and batching exist, but nothing splits the night into draft, verify, re-prove and package phases that each need a go/no-go from the measured yield of the one before. A bad draft phase then stops spend instead of verifying junk until dawn.
  Done when: a simulated night whose draft phase yields 0 accepted drafts skips verify and re-prove, and `fm` prints the stop reason and the saved dollars.

- **Refuse to start work that can't finish before wake time** — FIX — value 4 — effort S — risk low — category: overnight
  Why: the user wants progress by morning; half-done lanes at wake are worth nothing. Start gating exists only for cost (p90 cost). Duration and the learned wake time (from past first-prompt timestamps) are not used.
  Done when: with 40 minutes left and a task whose p90 duration is 70 minutes, the drive defers it to the next night and writes the reason to the morning card.

- **Hand the GPU back to the user's morning model** — FEATURE — value 4 — effort M — risk med — category: local models
  Why: the pack says a llama-swap model switch costs ~3 minutes and can't be detected. The night will have switched models, so the user's first prompt lands on a cold or wrong model. Unload and warm the model they open with 20 minutes before the learned wake time.
  Done when: at the learned wake time the endpoint is serving the profile's default model, confirmed by a completion probe, and the probe result is on the morning card.

- **Align frontier bursts to quota-window resets** — PERFORMANCE — value 4 — effort M — risk med — category: quota
  Why: an 8-hour night crosses at least one usage-window reset, and pace is off (steer 2026-10-31 #3), so limits are waited out. Spending frontier-heavy steps right after a reset and local-model steps just before the next one converts waiting into work. Existing ideas price spare quota but don't order work by window boundary.
  Done when: replaying a recorded night shows frontier steps clustered within the first 30% of each window, with idle wait time lower than the unscheduled baseline.

- **Add `fm peek`: a state-at-any-hour snapshot** — FEATURE — value 3 — effort S — risk low — category: overnight
  Why: assumption: the user sometimes wakes at 3am or checks a phone. The morning card is built for one moment. A cheap, zero-token one-screen peek that gives the hour, what is running, what has landed, spend so far, and "needs you: yes/no" is a different thing.
  Done when: `fm peek` runs in under 300 ms with no model call and, mid-drive, prints all five fields.

- **Stop the night at the yield knee** — PERFORMANCE — value 3 — effort M — risk low — category: overnight
  Why: the user said "major progress", but late-night hours may add near nothing. Log cumulative accepted-by-morning value per hour across past nights, find the knee, and stop or drop to cheap local work after it.
  Done when: after 5 recorded nights `fm` reports a per-hour yield curve and the drive downshifts at the knee in a replay.

- **Order the morning review by minutes-to-accept** — FEATURE — value 5 — effort M — risk low — category: morning handoff
  Why: the cost of progress is the user's review time. Existing ideas estimate review minutes and cap sizes, but none sorts the morning queue cheapest-first with a one-key accept, so the first 5 minutes clear the most.
  Done when: the morning list shows a minutes estimate per item, in ascending order, and accepting one is a single command.

- **Freshen overnight drafts onto current main at dawn** — FIX — value 4 — effort M — risk med — category: overnight
  Why: drafts are made against the head of the evening, but main can move (pushes, upstream). A late rebase-and-reprove pass makes the morning drafts apply cleanly. "Reserve the last 90 minutes for re-proof" exists, but not specifically rebasing drafts or flagging the ones that no longer apply.
  Done when: after a simulated mid-night commit to main, each draft is either rebased with a green proof or marked "stale: conflicts with <sha>" on the card.

- **Wild: Write a dream journal of untested hypotheses** — FEATURE — value 3 — effort S — risk low — category: delight — wild
  Why: assumption: the idle local model has spare hours. It writes short "I suspect…" hypotheses about the user's repos (no code, no commits), and each is scored the next night for what turned out true. Over time this shows which hypotheses are worth a lane.
  Done when: the morning card has a "dreams" section of at most 5 lines, and the next night's card shows a hit/miss count for them.

- **Wild: Keep the night quiet by acoustics** — FEATURE — value 2 — effort M — risk med — category: devices — wild
  Why: assumption: the 27B runs on a server that may be near the sleeping user. Read fan and GPU temperature, and when quiet hours are set, cap the GPU power so it stays quiet, trading throughput. Few agent tools think about noise.
  Done when: with a quiet-hours setting on, GPU power stays under the configured cap during those hours, and the night receipt shows the throughput given up.

- **Wild: Seal three bets on "what Sampo will have done by 7am" and grade them** — FEATURE — value 3 — effort S — risk low — category: forecasting — wild
  Why: it is the night-sized version of the sealed forecasts already proposed, but it targets Sampo's own output (tasks closed, dollars, red mains) rather than the user's asks. This calibrates the plan itself.
  Done when: bets are written before the drive starts, and the morning card shows each as hit or miss with the actual number.

- **Leave a "wake me" tripwire list the user can edit** — FEATURE — value 3 — effort S — risk low — category: safety
  Why: "stop asking me" and a zero-wake pager mean nothing can wake the user. A short file of the user's own wake conditions (main red for over 1h, spend over $X, an unreadable ledger) turns "never interrupt" into a negotiated line with a default of nothing.
  Done when: a seeded breach of an edited condition fires the configured alert, and an empty file means no alert is ever sent.

Next question: which hours of past nights actually produced work the user accepted, and does the first prompt time vary enough that a learned wake time is reliable?
Next question: when the user returns, do they review the night's output first or give a new ask, and should the morning card yield to the new ask?

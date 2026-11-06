# Brainstorm — lens: observability and trust

- **Detect guard circumvention** — SECURITY — value 4 — effort M — risk med — category: guard trust
  Why: assumption: after a refusal an agent may retry the same effect by another route (JARVIS was refused twice on `fm focus …; sed -i …`). Existing ideas stop repeat refusals but not rephrased retries. Cluster the five commands after a block by target path and effect; escalate when the effect matches the refused one.
  Done when: a test replays "blocked `rm X`, then `find -delete` on X" and the second attempt logs a `circumvention` event and is refused.

- **Check read-before-edit coverage** — FEATURE — value 4 — effort M — risk med — category: edit provenance
  Why: assumption: the pack shows outline and range reads are encouraged, but nothing records whether an edited region was ever read. At done, report the edited line ranges that the session never viewed.
  Done when: a task that edits an unread function gets a "blind edits: file:lines" row in its close-out, and a read-then-edit task gets none.

- **Probe cross-surface state parity** — FIX — value 4 — effort M — risk low — category: UI truth
  Why: T-0406 band stuck on step 1/5 while steps 3-5 were proven. Render band, pane, web and statusline from one fixture ledger in `fm smoke` and diff the step, status and next action each shows.
  Done when: a fixture with evidence on step 4 fails the probe if any surface shows a different current step.

- **Log surprises from stated predictions** — FEATURE — value 3 — effort M — risk med — category: calibration
  Why: `fm surprise` exists but depends on the model noticing it was wrong. Have plans carry one-line predictions ("gate X fails on Y", "only 2 files change") and diff them against outcomes automatically.
  Done when: a task whose prediction misses produces a surprise entry with no manual call, and one whose prediction holds produces none.

- **Store absence claims as re-runnable queries** — FEATURE — value 3 — effort M — risk low — category: evidence
  Why: assumption: claims like "no other callers" or "nothing reads this setting" are the least checkable evidence. Record the search and a hash of its result, then re-run it at the done gate.
  Done when: an absence claim whose search gains a hit after a later edit blocks done and names the new hit.

- **Score each rule's compliance from transcripts** — FEATURE — value 4 — effort M — risk low — category: instruction audit
  Why: the user's complaints are almost all about a rule not being followed (cleanup never done, idling with 20 queued). Measure per rule, offline, how often sessions follow it and where it breaks.
  Done when: `fm friction` lists the five least-followed injected rules with a rate and example transcript turns.

- **Stamp model and build on every event** — FEATURE — value 3 — effort S — risk low — category: attribution
  Why: assumption: ledger events don't record which model, effort level or harness build acted, so a quality shift can't be told from a Foreman change. Flag a mid-task swap.
  Done when: each ledger event carries `model` and `harness_build`, and a task that switches models shows a flag in its digest.

- **Give guard rules an origin and a fire record** — CLEAN — value 3 — effort S — risk low — category: guard legibility
  Why: the guard has grown through T-0275, T-0414, T-0421 and others. Each rule should cite its originating task, its test, and when it last fired. Never-fired rules are candidates for review.
  Done when: a refusal prints "rule R (from T-0414, last fired …)" and `fm doctor` lists rules unfired for 90 days.

- **Score each gate by what it alone catches** — PERFORMANCE — value 3 — effort L — risk med — category: gate value
  Why: assumption: gates are added freely and rarely removed. Inject seeded faults in a lane and record which gate catches each, then rank gates by unique catches per second.
  Done when: a report lists every gate with unique-catch count and cost, and shows one gate that catches nothing the others miss.

- **Anchor the ledger head outside the machine** — SECURITY — value 3 — effort S — risk low — category: tamper evidence (wild)
  Why: wild; a hash chain proves nothing if the whole file is rewritten. Periodically publish the chain head as a signed git tag or an entry in a public transparency log.
  Done when: `fm doctor` verifies the local chain against the anchored head and fails if history was rewritten before the anchor.

- **Run a trust-fall drill on the human reviewer** — FEATURE — value 3 — effort M — risk med — category: human vigilance (wild)
  Why: wild; the pack covers planting canary bugs for agent reviewers but not for the user's own skim. Occasionally, and only with opt-in, present a close-out card with one planted false claim, then reveal whether it was caught and report the user's catch rate.
  Done when: an opted-in drill card with a planted false claim is logged, the user's response is scored, and the miss or catch appears in the weekly digest.

- **Open a redacted spectator link** — FEATURE — value 3 — effort L — risk high — category: shared observability (wild)
  Why: wild; `fm serve` and the web UI already exist. Add a read-only, expiring link that shows the live band, steps and evidence to a teammate or client, with secrets, paths and prompts redacted.
  Done when: opening the link in a private browser shows live step changes with no file paths or secrets, and the link stops working after expiry or revoke.

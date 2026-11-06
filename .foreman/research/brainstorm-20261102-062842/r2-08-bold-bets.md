# Brainstorm — lens: bold bets

- **Estimate tick value off-policy** — FEATURE — value 5 — effort M — risk low — category: measurement
  Why: the gap is "unmeasured until the exam", and earlier ideas hold out a share of fires without saying how to turn that into a number. Log each fire-or-hold decision with its propensity, then compute an inverse-propensity or doubly-robust estimate of "useful fires caused" with a confidence interval. A week of shadow and session-borne ticks then gives a causal figure, not just an acted-on rate.
  Done when: `fm exam` prints the estimate and interval from at least N logged decisions, and a synthetic log with a known planted effect recovers it inside the interval.

- **Backfill notice-latency from dated deferrals** — FEATURE — value 5 — effort S — risk low — category: measurement
  Why: the pack shows dated deferrals already counted as carried (T-2603) and blocked tasks with stated waits. Every past revisit date is a free, already-recorded "should a tick have fired?" event, so no install is needed to grade self-triggering on real history. Measure how long after each date anything surfaced it.
  Done when: `fm tick grade --backfill` prints n, median and p90 lateness over all historical dated items, and a fixture with a known gap reproduces the exact figures.

- **Reconstruct awake windows to grade opportunity** — FEATURE — value 4 — effort M — risk med — category: measurement
  Why: assumption: the session-piggyback tick can only run when the machine was awake and the user was around. Rebuild awake intervals locally from journald, wtmp and git reflog times, then grade ticks as fires over achievable opportunities, not over wall-clock hours. A "missed" tick then separates a real miss from a laptop asleep.
  Done when: given a fixture journal with known sleep gaps, the reconstruction matches within 1 minute and the doctor line reports ticks over opportunities.

- **Grow fixtures from live events** — FEATURE — value 4 — effort M — risk med — category: developer experience
  Why: every real event any tick path sees (CI red, a dated deferral firing, a usage-limit resume) is a better test than a hand-made one. Redact it, hash it, and add it to the replay corpus, so the nightly suite improves with use. Privacy risk is the redaction, so it stays local and opt-out per repo.
  Done when: a real fire produces a fixture file, a planted secret in the event is absent from it, and the replay test passes and fails correctly when the decision changes.

- **Run the tick's local steps with no network** — SECURITY — value 4 — effort S — risk low — category: privacy
  Why: unattended work under a hardened kernel should prove it did not call out. Run local-only tick steps under `unshare -rn`, declare which steps need egress, and put "egress: none (enforced)" in the receipt.
  Done when: a test injects a socket connect into a finder and the tick fails closed with the step named, and the receipt says whether egress was used.

- **Give a no-change tick a fast path** — PERFORMANCE — value 3 — effort M — risk low — category: performance
  Why: if the tick rides every Stop and SessionStart, its cost on an unchanged tree is paid constantly. Key the whole tick on git's index stat data and the ledger heads, and skip finders when nothing moved.
  Done when: a bench shows p95 under 30 ms on an unchanged 2k-file tree, and touching one file takes the full path.

- **Show an evidence grade on every trigger** — FEATURE — value 4 — effort S — risk low — category: ui
  Why: the user can't tell "built" from "proven". Give each trigger a ladder (planted, replayed, shadow, live, kept) in the web UI and `fm doctor`, and refuse to show a rung without its artifact link.
  Done when: a trigger with only replay evidence cannot display "live", and each rung opens its source.

- **Publish only measured trigger recipes** — FEATURE — value 3 — effort S — risk low — category: docs
  Why: the site claims work starts without the user, and the standing proof-before-presentation rule goes red on unproven claims. Generate the trigger cookbook from graded fires, and render any recipe with fewer than 5 graded fires as "unproven".
  Done when: the Genesis page lists each recipe with its n and rate, and a recipe with n<5 renders "unproven".

- **Sample one fire per week for a one-tap audit** — FEATURE — value 3 — effort S — risk low — category: user value
  Why: the pack asks what the user acts on without checking. A random sampled fire, shown as "was this useful? y/n" in `fm next`, gives ground truth that Foreman did not author, at a cost of one tap a week. Wild.
  Done when: exactly one sampled fire per week is offered, and the answer feeds the off-policy estimate.

- **Use git's `reference-transaction` as a clock** — FEATURE — value 3 — effort M — risk high — category: agents
  Why: assumption: users with `git maintenance` enabled already have a timer updating refs (prefetch) with no Foreman install. A repo-local `reference-transaction` hook on those updates could fire the tick. This is wild, and brittle across git versions.
  Done when: in a fixture repo, a simulated prefetch ref update runs the tick once, with the lateness recorded, and a repo without maintenance is untouched.

- **Simulate the user's attention before deploying a trigger set** — FEATURE — value 4 — effort L — risk med — category: user value
  Why: the dropped ledger gives per-class acceptance and drop rates. Replay three candidate trigger designs over a recorded week against a stub user calibrated to those rates, and report the minutes of attention each would have cost. Wild, and it builds on existing replay and stub-user ideas.
  Done when: the simulator ranks designs and its estimate for the live design lands within 25% of the measured attention on a held-out week.

- **Forward an email to fire a lane** — FEATURE — value 3 — effort L — risk high — category: devices
  Why: assumption: the pack mentions a mail monitor (T-0827). A phone can forward a CI or notification email to a local maildir, and a session edge polls it and files a capture only, never running work. Wild. Credentials and untrusted text raise the risk.
  Done when: a fixture email with an injection string files one capture marked untrusted, and nothing else runs.

- **Randomise trigger arms across the user's repos** — FEATURE — value 3 — effort M — risk med — category: measurement
  Why: assumption: the user has several repos. Assigning repos to tick-on and tick-off arms at random gives a natural experiment to feed the off-policy estimate without a separate holdout. Wild.
  Done when: `fm tick arms` records assignments with a seed, and the estimate pools them.

Next question: which fires would the user have wanted even if the off-policy estimate shows no causal effect, and how would we tell?
Next question: does the user's machine sleep through the hours when a trigger would matter most, and where is that recorded today?

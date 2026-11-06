# Brainstorm — lens: the forecaster (invented): it predicts the next request and the next breakage, drafts the first on spec in a lane, flags the second, and every prediction is scored

- **Score each prediction against a trivial baseline in a counterfactual ledger** — FEATURE — value 5 — effort M — risk low — category: forecasting
  Why: T-2290 scores effort estimates, but the pack's "Mute predictors that lose to the baseline" and "Detect when the forecast is just the last request repeated" remain unbuilt as a shared ledger. Assumption: predictions today are scored one by one, not against "repeat last request" or "same as the last task of this tier."
  Done when: `fm foresight ledger` prints, per predictor, hit rate versus the repeat-last baseline, and a predictor under the baseline for 20 scored predictions is muted by a test fixture.

- **Draft the predicted request as a spec-only lane with an expiry** — FEATURE — value 5 — effort M — risk med — category: speculative lanes
  Why: Mission 8 #3 says "drafts it on spec in a lane." The user's asks (Plan gate, Capability-miss, Stuck ladder) arrive as long, structured specs, so the draft can reuse the pack's shape. The draft must never merge and must be deleted unmerged after N days.
  Done when: a fixture predicts a request, `fm lane` creates a lane holding only a task spec and no source diff, and the lane is auto-removed on expiry with a recorded disposition.

- **Match the real ask to its draft and adopt on overlap** — FEATURE — value 4 — effort M — risk med — category: forecasting
  Why: A draft is worth money only if the real ask can pick it up. Assumption: the intake path (`fm task new`) can compare a new ask's text and scope with open drafts.
  Done when: typing an ask that overlaps a draft by a set threshold attaches the draft's spec to the new task, and the ledger marks the prediction "adopted," "edited," or "ignored."

- **Predict "red after ship" from the diff's co-change history** — FEATURE — value 4 — effort M — risk low — category: breakage
  Why: Ship went red after T-2072 (rules over the 6,400-char budget). The lean ratchet (T-2281) already stores the footprint, and `fm graph blast` has co-change data. Together they can say "this diff likely trips X gate" before `fm ship` runs the full suite.
  Done when: a replay over the last 30 ships flags at least half of the ones that went red, with a false-alarm rate printed, and the warning shows at `fm task finish`.

- **Predict which standing steer a new task will collide with** — FEATURE — value 4 — effort S — risk low — category: breakage
  Why: The user's steers are a stored list (about 25 rules), and several recent asks (the 2026-10-31 #1 to #3 set) were enforced after the fact (T-2327). Assumption: steers are text only today, so a match is lexical plus scope paths.
  Done when: focusing a task whose title or scope matches a steer prints that steer's id and its check, and a fixture task that breaks one is flagged at plan time, not ship time.

- **Back-test every predictor on a rolling replay before it may draft** — SECURITY — value 4 — effort M — risk low — category: gating
  Why: The pack lists "Back-test every predictor on a rolling replay" and "Gate speculative lanes on a running precision floor," but the router (T-2291) and trigger table (T-2276) already act on history without a shared floor. Assumption: each predictor stores enough past inputs to replay.
  Done when: a predictor with precision below the floor cannot start a lane, and `fm doctor` names the predictor and its replayed score.

- **Cluster the "asked" stream into recurring request shapes** — FEATURE — value 4 — effort M — risk low — category: user model
  Why: The asks have a clear grammar: "Mission N, #K: noun phrase (mechanism)" followed by a verification noun. The forecaster can predict a shape (a new gate, a new verb, a new proof kind) even when it can't predict the text. Assumption: shape labels can come from a cheap model with a schema.
  Done when: `fm foresight shapes` lists the top shapes with counts and, for the last 20 asks, the predicted shape matched the real one in a reported fraction.

- **Show the forecast as one morning card with a veto key** — FEATURE — value 3 — effort S — risk low — category: surface
  Why: Many predictions exist as separate verbs (predicted minutes, next request, red ship, blocked-on-user backlog). The user reads little, so one card at session start, one keystroke to mute a line. Assumption: session start can afford one extra cached line under the hook latency bench.
  Done when: session start prints at most 5 forecast lines, the hook bench stays within its p50 budget, and `fm foresight mute LINE` persists.

- **Wild: Run a ghost-user lane that attempts the predicted request blind** — FEATURE — value 4 — effort L — risk med — category: speculative lanes (wild)
  Why: Rather than only drafting the spec, a throwaway lane uses only the user model (steers plus past asks) to act as the user and records the first clarifying question it would need to ask. That question becomes a pre-answered default in the draft. Assumption: a cheap model can follow steers well enough to produce a useful first question.
  Done when: after 10 ghost runs, the report shows how many first questions the user later asked or answered the same way.

- **Wild: Keep a prediction book the user can bet against** — FEATURE — value 3 — effort M — risk low — category: delight (wild)
  Why: The user corrects Foreman often, so a lightweight bet ("I say you'll ask for X next") gives free ground truth and shows where the user thinks the model is weak. Assumption: a one-line CLI is enough friction-free input.
  Done when: `fm foresight bet "…"` stores a bet, and the next closed ask scores both Foreman's and the user's guess on the ledger.

- **Wild: Publish "what Foreman got wrong about me" as a worst-misses page** — FEATURE — value 3 — effort S — risk med — category: honesty (wild)
  Why: The site already publishes Genesis stats daily (T-2326), and the steers demand signals Foreman didn't author. A page of the five worst scored misses with the ledger numbers, kept local unless the user opts in, keeps the forecaster honest.
  Done when: `fm foresight misses` writes a markdown page of the five largest misses, and nothing is pushed to site/ unless a setting is on.

- **Forecast hooks that will breach their latency budget** — PERFORMANCE — value 3 — effort S — risk low — category: breakage
  Why: `bench_hooks.py` records p50 and the lean ratchet records the footprint, but nothing extrapolates. A trend over the last N ships can warn "this hook crosses its budget in about 4 ships." Assumption: bench results are stored per ship.
  Done when: a fixture series of rising medians produces a dated warning, and a flat series produces none.

- **Learn the user's return pattern and time drafts to it** — FEATURE — value 3 — effort M — risk low — category: scheduling
  Why: Steer 3 says to wait out usage limits and keep going; drafts should land before the user is back and not burn budget while they are active. Assumption: session start and stop events give a usable return distribution.
  Done when: `fm foresight rhythm` prints the typical return window by weekday, and drafts started outside it are labelled with the reason.

Next question: Where does the user already confirm or reject Foreman's guess implicitly (accepting a plan unedited, closing a task with no changes), so scoring needs no extra input?
Next question: Which single prediction, if it were wrong with confidence, would cost the user the most (a draft lane merged, a muted warning), and what stops that today?

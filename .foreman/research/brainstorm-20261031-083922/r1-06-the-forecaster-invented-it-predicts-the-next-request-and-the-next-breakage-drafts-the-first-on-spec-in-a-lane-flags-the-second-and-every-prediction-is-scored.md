# Brainstorm — lens: the forecaster (invented): it predicts the next request and the next breakage, drafts the first on spec in a lane, flags the second, and every prediction is scored

- **Draft the predicted next request in a lane before it's asked** — FEATURE — value 5 — effort L — risk med — category: anticipation
  Why: Mission 8 #3 says "predicts the next request and drafts it on spec in a lane"; T-2290 scores only minutes/attempts, not the request itself. Recent asks form chains (T-2285→2288, T-2290→2291, 2325→2326) that suggest a follow-on is predictable.
  Done when: after a task closes, `fm foresight` records a predicted next-task title plus a lane holding a spec-only draft (no merge), and the next user request is matched against it with a hit/miss row.

- **Score request predictions with a hit rate by kind** — FEATURE — value 5 — effort M — risk low — category: scoring
  Why: T-2290 scores effort; nothing scores "what will they ask next". Without a number, drafts can't earn or lose their right to run.
  Done when: `fm foresight score` prints top-1/top-3 hit rate per request kind (fix, extend, doc, ship) over the last 30 requests, computed from stored predictions and the later-captured request text.

- **Gate speculative lanes on a running precision floor** — SECURITY — value 4 — effort S — risk low — category: safety
  Why: Standing rule 12 (stay lean and safe) plus the cost budget: drafting unrequested work spends tokens. assumption: precision under ~25% means the drafts are noise.
  Done when: when trailing precision is below the floor, `fm foresight` drafts nothing and says why in one line; above it, draft count per day is capped.

- **Predict breakage from co-change and recent-edit pairs** — FEATURE — value 4 — effort M — risk low — category: foresight
  Why: `fm graph blast` already yields co-change neighbours (T-2286-era blast radius in the plan). Recent edits like USER_ONLY_FM (T-2252) and the plan-gate regex (T-2285) show fixes that missed a sibling path. assumption: a changed file's unedited co-change neighbours are where the next red lands.
  Done when: at `fm task finish`, untouched high co-change neighbours are listed as "likely next break", and later red-after-merge events are scored against the list.

- **Learn the user's correction shapes from the "asked" stream** — FEATURE — value 4 — effort M — risk low — category: user model
  Why: Many asks are corrections of Foreman's own gates (T-2285 plan gate misses a flag-led option, T-2289 lane rm vs scratch, T-2283 baseline dedupe). The pattern: a new gate ships, then a false-refuse follows. assumption: it generalises.
  Done when: shipping a new refusing gate auto-files a "probe the false-refuse" task with 3 adversarial inputs, and the count of false-refuse fixes per gate trends down in `fm outcomes`.

- **Pre-flight a new gate against the user's last 50 inputs** — FIX — value 4 — effort M — risk low — category: reliability
  Why: T-2285 and T-2289 were both found after the fact. Replaying historical plans and lane states through a new check would have caught them.
  Done when: `fm ship` on a task adding a refusal replays it over stored plans/lane dirs and fails if it would have refused a previously accepted, later-done item.

- **Forecast the day's usage-limit wall and shape the queue** — PERFORMANCE — value 3 — effort M — risk low — category: planning
  Why: Steer 3 says wait out limits and keep going; the model router (T-2291) already knows cost per tier. assumption: spend per task is predictable enough to order cheap and unblockable work ahead of the wall.
  Done when: `fm foresight budget` prints expected tokens to drain the queue, the predicted wall time, and reorders lanes so unblockable work runs first; the prediction error is logged.

- **Surface the "blocked on user" backlog as a one-yes batch** — FEATURE — value 4 — effort S — risk low — category: user value
  Why: Open work holds many blocked items (T-0325 libappindicator, T-0418, T-0352) and #11 says installs queue "for one yes". The user has to hunt them.
  Done when: session start shows at most one line, "3 things need a yes: …", and `fm yes` approves or declines each with one key.

- **Wild: Run a shadow Foreman that answers as the user would** — FEATURE — value 4 — effort L — risk high — category: user model
  Why: wild. The request stream and the steers file are enough to train a cheap "twin" prompt. It answers `fm ask` questions provisionally, tagged so the user can overrule later, and its agreement rate with the real answers is scored.
  Done when: twin answers are stored beside real ones for 20 questions and the agreement rate is shown; it never settles a consent gate.

- **Wild: Write tomorrow's morning brief tonight** — FEATURE — value 4 — effort M — risk low — category: delight
  Why: wild. A nightly job (via the queued timer) drafts the likely first three requests, the red items to watch, and the finished lanes awaiting a merge look. Each line is scored against what actually happened by noon.
  Done when: a brief file exists by 07:00 and a later line marks each entry hit, missed or not-asked.

- **Wild: Hold a "prediction court" for the trigger table** — FEATURE — value 3 — effort M — risk med — category: observability
  Why: wild. T-2276 learns from trigger precision, but only per kind. Let each trigger and each forecast file a "claim" with an expiry date, and have a cold Haiku reader judge expired claims from the evidence alone, rather than the code that made them.
  Done when: expired claims get a verdict with a quoted evidence line, and the claim types with a poor record lose their auto-fire right.

- **Detect when the forecast is just the last request repeated** — CLEAN — value 3 — effort S — risk low — category: scoring
  Why: A naive baseline ("same kind as last") can match a clever model. The exam standards already demand free arms beating session arms.
  Done when: the scorecard prints the forecaster's hit rate beside the repeat-last baseline and flags a forecaster that doesn't beat it.

- **Predict which parked task the user will un-park next** — FEATURE — value 3 — effort S — risk low — category: anticipation
  Why: The ~30 deferred "Later from T-07xx" items go stale. Their un-park history is a ready signal. assumption: un-park correlates with the area touched in the last week.
  Done when: `fm next` ranks deferred items by predicted un-park odds, with the outcome logged.

Next question: Which predicted requests would the user have found unwelcome (drafts spending tokens or touching files) rather than merely wrong, and how would Foreman learn that without being told?
Next question: When two forecasts disagree (the breakage list versus the request draft), which one should the lane act on?

# Brainstorm — lens: sci-fi: the 2030 harness that repairs itself, orchestrates its own lanes on the cheapest capable model, starts work from events and schedules and forecasts the user's next request, worked back to what Python and Foreman can do today

- **Classify every action by reversibility and let triggers spend only the cheap class** — SECURITY — value 5 — effort M — risk low — category: autonomy safety
  Why: Mission 11 starts work without the user, installs are queued for "one yes", and the guard stays intact. No idea so far ties what self-started work may do to how undoable it is. Assumption: verbs and trigger actions can be tagged in one table.
  Done when: a trigger-originated lane that tries an outward or irreversible action (push, install, delete outside its worktree) is refused with the yes-queue entry it created, and a test lists every `fm` verb with its class.

- **Normalise all triggers onto one event envelope** — FEATURE — value 4 — effort M — risk low — category: triggers
  Why: T-2276 routes triggers by outcome, but file, git, CI and issue watchers are separate paths (`fmserve`, `global_events`). A common envelope (source, subject, dedupe key, cost hint) makes a new watcher a short adapter, and the precision table then works for every source.
  Done when: adding a fake "webhook" source needs one small file and shows up in `fm triggers` with precision, with no change to the router.

- **Pre-warm the repo before the user's habitual start** — PERFORMANCE — value 3 — effort S — risk low — category: anticipation
  Why: Mission 3 models the user's habits and machines, but nothing uses time-of-day. Before the usual first session, run the baseline test, refresh the map and fetch, so the first `fm task focus` is instant and any red baseline is reported as already known.
  Done when: with a recorded habit window, a pre-warm run writes a baseline result before the window opens, and focus within the window reads it instead of re-running.

- **Print the model-by-tier cost frontier from lane history** — FEATURE — value 4 — effort S — risk low — category: router
  Why: T-2291 picks builders from held-up rates, but the user can't see why. A table of cost per task that held, per tier and model, with the pick marked, makes "cheapest capable" checkable and shows when a cheaper tier has quietly become capable.
  Done when: `fm lane models` prints the table from stored lane outcomes, and the router's pick for a tier matches the table's cheapest row that clears the held-rate floor.

- **Adopt a speculative draft when the real ask overlaps it** — FEATURE — value 4 — effort M — risk med — category: anticipation
  Why: Drafts of predicted requests (T-2290 scores them) only pay off if they're reused. Match the actual request to a shelved draft by touched files and title terms, offer it once, and record minutes saved against drafts that expired unused.
  Done when: a test with a shelved draft and a request naming its files offers adoption and records the saving, and an unmatched draft expires and is counted as waste.

- **Route zero-risk lane steps to a local model when one is present** — FEATURE — value 3 — effort M — risk low — category: privacy and cost
  Why: Mission 9 wants the cheapest model per part, and `fm code` already runs on any model. Summaries, lint-only fixes and brief drafting don't need a frontier model and needn't leave the machine. Assumption: the user may have a local engine such as Ollama.
  Done when: with a local endpoint configured, the router picks it for steps in an allow-list and records the pick. With none configured, the behaviour is unchanged.

- **Rehearse each self-change on a snapshot of real state** — SECURITY — value 4 — effort M — risk low — category: self-repair
  Why: The self-fix loop is gated by bench and trials, but those run on fixtures. Copy the user's actual task and event state to a scratch directory and run the changed hooks and verbs there, checking hook p50 and no new refusals on the user's last N real inputs.
  Done when: a self-change that makes any of the last 50 recorded user commands newly refused, or pushes hook p50 past the ratchet, fails rehearsal before it touches live state.

- **Publish a "how Foreman fixed itself" page from the self-change ledger** — FEATURE — value 3 — effort S — risk low — category: docs
  Why: The site already refreshes stats daily (T-2326), and docs are a thin area. Each merged self-fix has a signal, a root cause, a test and a verdict, which is a runbook nobody has to write. Assumption: a ledger of self-changes exists or lands with the earlier "keep a self-change ledger" idea.
  Done when: `fm genesis publish` adds a page listing the last N self-fixes with signature, test name and whether it recurred, and it contains no local paths or secrets.

- **Wild: Run lanes on tomorrow's Foreman first (two release channels)** — FEATURE — value 4 — effort L — risk med — category: dogfooding
  Why: wild. Self-improvement is only safe if something absorbs the breakage before the user does. Install each self-change into a "nightly" copy that background lanes use for a week. Promote it to the user's copy only if it held on real work, which gives self-repair a real-world trial rather than a bench.
  Done when: a self-change appears in lanes' runs under the nightly channel, and `fm doctor` shows its promotion state and the lane outcomes that decided it.

- **Wild: Replay a recorded week of events in ten minutes** — FEATURE — value 4 — effort L — risk low — category: testing
  Why: wild. Mission 11's triggers, locks, timers and yes-queue interact over days, and no suite covers that. Record a real week of file, CI and clock events, then replay it against a stub model on a fake clock and assert on spend, queue depth, conflicts and lanes left running.
  Done when: `fm sim week <file>` finishes in under ten minutes with a summary, and a planted trigger storm in the file trips the budget limit and shows in the summary.

- **Wild: Keep a prediction book the user can bet against** — FEATURE — value 3 — effort S — risk low — category: anticipation
  Why: wild. Predictions are scored after the fact (T-2290), but the user's disagreement is the cleanest label. A one-word "no" on a predicted next request is stored as a counter-bet, and the book shows hit rate by kind with and without the user's veto.
  Done when: `fm foresight no` records a counter-bet, the predictor's rate for that kind drops in the next listing, and the book prints both rates.

- **Wild: Shadow the user's hand work and file the task afterwards** — FEATURE — value 3 — effort M — risk med — category: friction
  Why: wild. Self-repair sees only what Foreman ran. Commits made outside any task, such as a manual fix after a red CI, are the strongest correction signal. A watcher turns each commit with no task into a closed draft FIX with the diff as its proof, feeding the signal-to-fix loop.
  Done when: a commit made with no task open produces a drafted task that cites its hash, and the signal loop counts it as a miss for its signature.

- **Gate every self-triggered lane behind a "would the user run this" check from their history** — FEATURE — value 3 — effort M — risk med — category: trigger precision
  Why: T-2276 learns precision after a trigger fires. Check before firing instead: has this user ever accepted a task of this kind from this source? If not, it goes to the yes-queue rather than starting a lane.
  Done when: a first-ever trigger kind lands in the queue, and after three accepted ones the same kind starts a lane directly, with a test for both.

Next question: Which self-started actions have already happened that the user never saw, and where are they listed?
Next question: What does the user do when a self-repair is wrong, and is that undo path faster than the original mistake?

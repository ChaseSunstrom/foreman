# Brainstorm — lens: 2030 worked back

- **Pre-load the model the first hour needs** — FEATURE — value 4 — effort M — risk low — category: local models
  Why: the pack says a llama-swap switch costs about 3 minutes and its `/running` isn't relayed. A habitual first hour (assumption: it can be read from session-start times and first asks) lets the model be warmed before the user arrives, so the first draft isn't a 3-minute wait. Switches are also detected by timing, since there is no readout.
  Done when: replaying 30 days of start times, the planner issues a model switch ahead of at least 70% of first-hour sessions, and `sampo` logs the warm-up with its predicted start.

- **Order the night's local work by model residency** — PERFORMANCE — value 4 — effort M — risk low — category: scheduling
  Why: the steer says use qwen3.8-27b for everything first and switch to the MoE only late, because each switch costs about 3 minutes. Unattended drafts for several predicted asks should be grouped by required model.
  Done when: a queue of 12 mixed-model jobs in a simulated run makes at most one switch, and the receipt shows switches avoided against arrival order.

- **Rerank candidate asks with a decision model** — FEATURE — value 4 — effort M — risk med — category: prediction
  Why: the standing steer is small local models scaffolded to frontier results. Retrieval proposes 5–8 candidate asks from the ledger, and d3/tev1/kev (or a classifier) picks from the closed list instead of free-generating. Assumption: the decision-model API takes option descriptions, as in T-2894.
  Done when: on held-out past asks, top-1 accuracy from the reranked path matches or beats the retrieval-only baseline, and no free-generated text enters a draft.

- **Gate drafting on a dry-runnable Exam** — FEATURE — value 5 — effort S — risk low — category: Exam
  Why: the carried gap is that every brief's Exam reads live state. A predicted ask gets a draft only if its Exam's live reading runs on the current tree. Otherwise the prediction is surfaced as an unmeasurable hunch and no lane work is spent.
  Done when: a predicted ask whose reading errors produces no draft or lane, and `sampo doctor` counts hunches withheld.

- **Learn which draft fields the user rewrites** — FEATURE — value 4 — effort M — risk low — category: learning
  Why: the ideas so far settle a prediction as a whole hit or miss. A draft is spec, size, Done-when and Exam. Diffing the filed task against the draft shows that, say, Done-when is rewritten 80% of the time while the title never is, so the weak field can be fixed or hedged.
  Done when: for 20 settled drafts, a per-field edit-rate table exists, and the next draft's weakest field is marked "unsure" on its card.

- **Mine the user's own reverts into personal pre-mortems** — FEATURE — value 4 — effort M — risk med — category: flagging problems
  Why: the request says to flag problems before they happen. `git revert`, fixup and force-push-recovery commits are the user's own regrets, which Sampo didn't author. A recurring precondition ("merged without running the site tests") can trigger a one-line warning at the next occurrence. Assumption: enough history exists.
  Done when: replaying one repo's history, at least one past revert is flagged by its precondition before the fact, with a false-warning rate under 1 per 20 sessions.

- **Detect focus shifts and re-window the predictor** — FEATURE — value 3 — effort S — risk low — category: user model
  Why: the user's recent asks jump between site, rename, moons, drive fixes and local models. A changepoint on the task-kind and area mix tells the predictor to drop stale priors, and "your focus moved from the drive to the site" can be said once.
  Done when: on the last 60 days of asks, a shift is flagged within 2 days of a clearly different area dominating, and the predictor's window resets.

- **Forecast model-server failure from its own telemetry** — FEATURE — value 3 — effort M — risk low — category: machine model
  Why: the user's 27B runs on a server, and an outage stalls the overnight work. Trends from the endpoint probes (latency creep, failed loads, and disk or GPU readings if exposed) can warn "this server will likely drop in the next day" so work moves to Ollama early. Assumption: telemetry is reachable.
  Done when: a replayed degradation trace raises the warning at least an hour before the first failed call, and the drive shifts to its fallback chain.

- **Make one user-model file the shared source** — CLEAN — value 4 — effort L — risk med — category: user model
  Why: the earlier ideas imply a pile of separate stores (habit tables, steers, assumed-about-you, taste, taught-by-model). By 2030 the models behind them will have changed several times. Facts with evidence ids, a half-life and a strike-through live in one versioned file that every predictor reads.
  Done when: all predictors read facts only from that file, and striking one fact removes the predictions it supported.

- **Wild: run the predictor against synthetic futures** — FEATURE — value 3 — effort M — risk low — category: robustness
  Why: the idea list tests replays of the past. Generate plausible futures from the user model (a new language, a month away, a switch to a team repo) and check that the predictor degrades gracefully, goes quiet instead of confidently wrong, and mutes itself.
  Done when: in 5 synthetic regime changes, the predictor's shown-prediction rate drops within 10 asks and no confident miss streak exceeds 3.

- **Wild: seed the cold-start prior from public repo histories** — FEATURE — value 3 — effort L — risk med — category: cold start
  Why: a fresh install has no history. Task-kind transition tables (after a release, docs; after a dependency bump, a CI fix) mined offline from permissively licensed public repos could ship as a small data file that the user's own ledger quickly outweighs. Assumption: transitions generalise across stacks.
  Done when: on three unseen repos' first 20 asks, the prior beats a no-prior baseline on top-3 task-kind hits, and the data file is under 300 KB with its sources listed.

- **Wild: seal a 2030 time capsule at install** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: assumption: the user will want, in a year, to see how well Sampo knew them. The capsule holds a hashed user-model snapshot plus sealed predictions about their own work, opened at 1, 2 and 4 years with a score, so it also pins today's format for the 2030 readers.
  Done when: a capsule written today opens through the current reader, shows the stored predictions beside what the ledger recorded, and a stale schema is named instead of silently skipped.

- **Show anticipation's mistakes in plain words, ranked by cost** — FEATURE — value 3 — effort S — risk low — category: observability
  Why: the user's recent pushbacks are about relevance (not wild enough, stop asking me). A weekly list shows each wrong draft with the minutes it cost the user to dismiss, so the predictor is judged by felt cost and not hit rate.
  Done when: `sampo doctor` prints the top three costly misses with their dismissal time, and the list matches the ledger.

Next question: which of the user's repeated asks (rename, publish, push, drive fixes) are really one ritual that a single sealed prediction could cover, and has anyone checked how often they already come in the same order?

Next question: does the user's first-hour habit exist at all in the ledger (fixed start time, same opening ask), or is their pattern too bursty for warm-up and ordering ideas to pay off?

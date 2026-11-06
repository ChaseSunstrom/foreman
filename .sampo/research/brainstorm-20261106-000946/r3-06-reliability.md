# Brainstorm — lens: reliability

- **Stamp the decider’s verdicts with a replayable proof chain** (content hash of the prompt, model ID, and evidence) — FEATURE — value 5 — effort M — risk low — category: decider, audit
  Why: The pack shows `fm ship` failing mid-test due to conflicts and `homemove._undo` raising on tree_hash. If a decider’s “yes” or “no” cannot be replayed from disk, the user cannot distinguish a model error from a stale state error.
  Done when: `sampo decide replay <id>` reproduces the exact verdict from the ledger alone, with no network or GPU required.

- **Give every model slot a “canary” self-bait that must fail at session start** — FIX — value 5 — effort S — risk low — category: guard, reliability
  Why: T-2967 shows the Ward’s core protection missed the migrated home’s real path. A decider running on a broken or stale model is worse than no decider. A known-safe command must be blocked; if it isn’t, the session degrades.
  Done when: `sampo doctor` runs a silent canary command through the decider’s guard path; if the block fails, the model is disabled and a named cause is logged.

- **Make “Sampo is degraded” a first-class, persistent status line** — FIX — value 4 — effort S — risk low — category: UI, resilience
  Why: T-1217 shows Claude Code painting the docked pane’s background incorrectly, and T-0325 blocks on missing GTK libs. When a surface fails, the user must know immediately. “Silent fail-open” is the enemy.
  Done when: Every hook that fails to import, execute, or return a verdict writes a one-line “degraded: <cause>” to the status bar that survives a session restart.

- **Two-phase grant spend: reserve, then commit** — CLEAN — value 5 — effort M — risk med — category: grants, atomicity
  Why: The user’s push grant allows “feel free to push,” but T-2964 shows `fm ship` falling back to `git cherry` when main moves. A crash between “reserved” and “committed” must not double-push or lose the grant.
  Done when: A kill-point sweep on the grant-spend path proves that a SIGKILL at any step leaves exactly one valid push or zero, with a log entry explaining which.

- **Reconcile model state from disk at wake, not from memory** — FIX — value 4 — effort M — risk low — category: state, drift
  Why: T-2967 shows `homemove` reading a `SAMPO_HOME` already popped. If the model registry or weights change on disk while Sampo is running, the next decision uses stale assumptions.
  Done when: `sampo doctor` compares the in-memory model registry against the on-disk state; on mismatch, it reloads and logs the drift with the files that changed.

- **Wild: “Sampo is gone” morning: disable the model layer for one live session** — FEATURE — value 4 — effort S — risk low — category: drill, baseline
  Why: The user asks for a “better Kev-style decider,” but the pack shows no baseline for “what did I have to do by hand?” A weekly drill where the decider is off logs every ask the user made, becoming the ground truth for the decider’s value.
  Done when: A `sampo drill gone` command disables all model calls for one session; the morning card lists “3 asks you made that Sampo would have predicted,” with a link to the relevant decider slot.

- **Wild: Pull-the-plug drill: random SIGKILL of the live drive on a scratch repo** — FEATURE — value 5 — effort M — risk med — category: chaos, resilience
  Why: T-3185 shows `core.bare=true` leaking into real config and breaking merges. A decider that cannot survive a crash is not reliable. A scheduled, random kill on a scratch repo tests the resume path without risking main.
  Done when: A nightly cron job kills a scratch drive at a random point in a task; the next run resumes correctly, and the ledger shows the crash and the recovery.

- **Wild: Fuzz the rename as a distribution shift** — FEATURE — value 4 — effort M — risk med — category: drift, testing
  Why: T-2748 moved code to `plugin/lib/sampo/`, but T-2967 shows the Ward still comparing literal paths. The model’s training data includes “Foreman”; if the rename shifts the model’s behavior, no test catches it.
  Done when: A test suite runs the decider on a corpus of “Foreman” and “Sampo” labeled data; if the model’s abstain rate or accuracy changes by >5%, the drift is flagged and the model is retrained.

- **Pin the serving stack by digest, and rehearse “model gone”** — SECURITY — value 5 — effort S — risk low — category: supply chain, resilience
  Why: T-2869 mentions Moonscale’s `MOONS_LOCAL` defaults to a profile name. If the local endpoint or weights change without notice, the decider’s behavior changes silently.
  Done when: `sampo doctor` verifies the model’s SHA256 against a pinned digest; on mismatch, the model is rejected. A `sampo drill model-gone` command simulates the endpoint being unavailable and tests the fallback.

- **Make the decider’s “abstain” a measured, typed output, not a silent fallback** — FIX — value 4 — effort S — risk low — category: decider, UX
  Why: T-2953 shows the Moons funnel’s tier stage judging batches at once, but if the model abstains silently, the user sees a decision they didn’t expect. Abstain must be a first-class state.
  Done when: Every decider call returns either a verdict or an abstain with a named cause (e.g., “low confidence,” “model error”); the UI shows the abstain as a held rune, not a grey failure.

- **Replay the user’s last 30 days of “I had to say this” asks as a held-out test** — FEATURE — value 5 — effort M — risk low — category: eval, baseline
  Why: The user’s own words show repeated asks for “Sampo’s own decision model” and “generic across every project.” If the model cannot predict the user’s next pushback, it is not earning its tokens.
  Done when: A `sampo eval past` command takes the last 30 days of user messages, strips them of context, and scores how many the decider predicted in the next 24 hours. The score is published in the morning card.

- **Wild: A “Sampo is thinking” reason line that survives a session restart** — FEATURE — value 3 — effort S — risk low — category: UX, transparency
  Why: T-2964 shows the site’s hero sitting 90px below the spec. If the user has to wait for a model call, they need to know why. A spinner is not enough; the reason must persist.
  Done when: When a model call is in flight, the status bar shows “Sampo is thinking: <reason>” (e.g., “deciding on approach,” “checking guard”); if the session restarts, the reason is replayed from the ledger.

- **Make “does the decider beat plain” a permanent, nightly claim** — FEATURE — value 5 — effort M — risk low — category: eval, baseline
  Why: T-1231 defers the “Foreman beats Claude Code” duel. The user wants a “better Kev-style decider,” but without a baseline, “better” is meaningless.
  Done when: A nightly job runs the decider and a plain `claude -p` on a held-out set of 10 tasks; the scorecard shows the delta in pass rate and cost. If the decider falls below plain, the slot is demoted.

- **Wild: Federate regret, not weights, across the user’s own machines** — FEATURE — value 4 — effort L — risk med — category: privacy, training
  Why: The user asks for a “generic model” across projects. If each machine trains on local data, the model fragments. Regret (the user’s undo) is small, sensitive, and the only label.
  Done when: A `sampo federate regret` command aggregates the user’s undo logs across machines, strips all text, and updates a shared “regret vector” without sending raw data. The model is retrained on the vector.

- **Make the model’s “confidence” a “cost” metric** — FIX — value 3 — effort S — risk low — category: eval, economics
  Why: T-2869 mentions Moonscale’s cost split. A model that abstains often is cheap but useless; a model that decides often is expensive but maybe wrong. Confidence must be priced.
  Done when: The morning card shows “Model confidence: 0.8, cost per decision: $0.02, saved minutes: 3.” If the cost exceeds the saved minutes, the slot is flagged for review.

- **Wild: A “Sampo is gone” morning: disable the entire decider and log every ask** — FEATURE — value 5 — effort S — risk low — category: drill, baseline
  Why: The user’s standing rule is “no idea is killed for ambition,” but without a baseline, the decider’s value is unproven. A weekly “gone” morning is the ultimate test: what does the user do by hand when the model is off?
  Done when: A `sampo drill gone` command disables all model calls for 24 hours; the morning card lists “12 asks you made that Sampo would have predicted,” with a link to the relevant decider slot and the cost of each.

Next question: What is the *smallest* project (fewest briefs) on this box where the generic head must not abstain, so we can set the real floor for "the model should say nothing" before training?
Next question: When the user goes quiet for a week, does Sampo *know it should be quieter too*, and is that quietness a logged, reversible decision?

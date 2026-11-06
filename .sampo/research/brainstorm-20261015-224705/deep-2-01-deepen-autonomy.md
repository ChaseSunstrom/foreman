# Brainstorm — lens: deepen: autonomy

- **Compile a delegation policy from answered asks** — FEATURE — value 5 — effort M — risk med — category: autonomy
  Why: assumption: Foreman logs every ask and answer; the user wants fewer interruptions ("shouldn't need to ask for any of it"). Generalise "answer your own asks" into a per-project policy file (`.foreman/delegation.toml`, git-tracked) of ask-pattern → answer, each with confidence, example count and a blast-radius class. Only reversible classes may auto-answer.
  Done when: after the same ask is answered identically 3 times, the 4th is auto-answered with a "policy hit" receipt, and an irreversible-class ask is still put to the user (test with a fixture ledger).

- **Charge every autonomous act to one risk budget** — FEATURE — value 5 — effort M — risk low — category: autonomy
  Why: assumption: the error-budget, proxy, ratchet and contract ideas each need their own limits. Unify them into a single ledger of "autonomy spend": each auto-answer, auto-merge or overnight task costs points by reversibility. Corrections and reverts refill nothing; clean closes slowly earn more. When the budget is empty, Foreman asks.
  Done when: `fm autonomy` prints the balance, the last 10 charges, and a forced-ask once the balance hits zero (unit test with injected events).

- **Shadow-run autonomy before granting it** — FEATURE — value 5 — effort M — risk low — category: trust
  Why: the pack shows corrections are logged (fmhooks 578-615), but nothing tests a new rule before it acts. Each new auto-answer rule runs in shadow for N asks: it records what it would have answered next to what the user actually answered. It is promoted only at ≥95% agreement.
  Done when: a rule in shadow mode never changes a hook's behaviour, and `fm autonomy shadow` shows its agreement rate; promotion is refused below the threshold.

- **Replay past sessions against a proposed rule** — FEATURE — value 5 — effort L — risk low — category: simulation
  Why: assumption: ledgers and session transcripts are retained, and the user said Foreman hasn't "really improved". Before adopting any rule, veto or auto-answer, replay the ledger's recorded events (tool calls, corrections, asks) through the guard and policy engine offline. Report which past moments it would have changed and whether the user later corrected them. Unlike the shadow run, this needs no waiting.
  Done when: `fm sim <rule>` outputs would-have-fired events over the last 30 days with a count of those the user later corrected, and it runs without a network call or a `claude` invocation.

- **Pre-sign a consent envelope at plan time** — FEATURE — value 4 — effort M — risk med — category: autonomy
  Why: it combines "hold points and witness points" with the "turnaround contract". The plan carries a machine-checkable envelope: paths touchable, commands allowed, spend cap, deadline, and the points where a human must witness. The guard enforces it, and leaving it halts the lane and files a resume capsule (C1).
  Done when: a task with an envelope that forbids `src/auth/**` has a write to that path denied by the guard, with the envelope clause named in the denial.

- **Hand a stalled lane to a peer agent** — FEATURE — value 4 — effort M — risk med — category: orchestration
  Why: assumption: lanes stall (the pack mentions silent lanes and orphaned builders). A watchdog notices a lane with no heartbeat, reads its resume capsule, and offers the work to another idle lane or a fresh worktree. This extends "resume" from the user's action to the system's.
  Done when: killing a builder mid-task leads, within a timeout, to a new lane that starts from the capsule and the original is marked superseded (e2e with a fake builder).

- **Pre-run the likely next task in a throwaway worktree (wild)** — FEATURE — value 4 — effort L — risk med — category: prediction
  Why: wild. The queue and the user's habits (the same follow-ups after bug fixes, such as docs and test additions) make the next step predictable. While the user reviews, Foreman drafts it on a scratch branch under a token cap. It never touches the main tree; the user either adopts it or discards it, and the hit rate feeds the budget.
  Done when: with a queued next task, an idle session produces a draft branch plus a "draft ready" line, and discarding it leaves no residue in the worktree list.

- **Auction tasks between subagents (wild)** — FEATURE — value 3 — effort L — risk med — category: orchestration
  Why: wild. Each lane profile (Haiku, Sonnet, Opus, a repo-specialist card set) bids with an estimated cost and a confidence drawn from its past close rate on similar tasks. The cheapest bid above a confidence floor wins, and results update the bids. A first version needs only a table of past outcomes by task kind.
  Done when: `fm assign T-xxxx --dry` lists the bids and picks a winner, and the pick changes after seeding a history in which one profile keeps failing.

- **Let the agent propose changes to its own harness, gated by replay (wild)** — FEATURE — value 5 — effort L — risk high — category: self-improvement
  Why: wild. The user asked Foreman to "genuinely improve itself". Foreman may draft a patch to its own hooks, prompts or thresholds. The patch is accepted only if the replay sim shows no regression on the saved cases (including T-0035 eval captures) and the user's veto list holds. It lands as a PR, never directly.
  Done when: a seeded noisy-hook case yields a self-authored patch PR with a sim report attached, and a patch that regresses a saved case is rejected automatically.

- **Estimate the user's intent from recent steers (wild)** — FEATURE — value 3 — effort M — risk low — category: prediction
  Why: wild. The user's recurring steers (fill the panel, show progress counts, "any project, via git") are a stable preference profile. Distil them into a short intent file that the planner reads and that the proxy uses to break ties. The user can edit or delete any line.
  Done when: `fm intent` shows at most 10 lines, each traced to the steer that produced it, and a planner run quotes the lines it applied.

- **Quarantine autonomy after a bad outcome** — FEATURE — value 4 — effort S — risk low — category: safety
  Why: assumption: auto-answers and overnight work will sometimes be wrong. A user revert, a red post-merge gate or a correction that names an auto-act suspends that class of autonomy, files a post-mortem stub, and requires a manual re-enable once the cause is fixed.
  Done when: a recorded revert of an auto-merged task flips its class to "asks" and `fm autonomy` shows the reason and the commit.

- **Prove the autonomy ladder with a verifiable audit trail** — SECURITY — value 3 — effort M — risk low — category: provenance
  Why: assumption: the user wants autonomy that can be trusted when nobody is watching. Each autonomous act appends a hash-chained record (rule id, inputs, decision, envelope clause). `fm audit verify` detects edits or deletions, and the morning receipt (C5) links to it.
  Done when: tampering with one record in the chain makes `fm audit verify` fail and name the first bad entry.

- **Hold a pocket of unattended experiments on its own behaviour (wild)** — FEATURE — value 4 — effort L — risk med — category: self-improvement
  Why: wild. During `fm night`, Foreman A/B-tests one setting at a time (for example a hook threshold or a retrieval size) on replayed or low-stakes tasks. It ratchets the winner into config only when the metric (interventions per task, C12) improves and the autonomy budget allows.
  Done when: an overnight run changes exactly one setting, records before and after metrics on identical replay cases, and reverts it automatically if the metric worsened.

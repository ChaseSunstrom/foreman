# Brainstorm — lens: agent types and roles

- **Add an fm-closer agent for the done tail** — FEATURE — value 4 — effort M — risk low — category: agent types
  Why: T-0428 moved CHANGELOG.md to the main thread, and T-0423/T-0428 each needed separate changelog lines. Per-task chores (changelog, MASTER.md sync, lesson recording, leftover sweep, cleanup) keep landing on the main thread, and cleanup requests "never got done".
  Done when: after a task passes its gate, `fm task done` can dispatch a closer lane from a checklist. The lane commits a changelog line and a lesson, and the ledger shows the main thread never touched them.

- **Add an fm-remediator that consumes audit findings** — FEATURE — value 4 — effort M — risk med — category: agent types
  Why: T-0034 (`fm audit run`) produces a structured findings file, and fm-reviewer is read-only, so nothing owns the step from finding to fix. The remediator takes one finding, writes a failing regression test, makes the minimal patch, and returns a receipt tied to the finding id.
  Done when: given a findings file with 3 seeded defects, `fm audit fix` closes each finding with a red→green test and marks any it can't fix as unresolved.

- **Let lanes proceed on a declared assumption** — FEATURE — value 4 — effort M — risk med — category: orchestration
  Why: assumption: a lane that hits an ambiguity currently blocks or guesses silently. Instead the lane records `assume: X (confidence)` and continues. The main thread ratifies or rejects it later, and a rejection reopens only the hunks tagged with that assumption id.
  Done when: in a test, a lane with a wrong assumption gets a rejection that reworks only the tagged hunks, and the untagged diff stays byte-identical.

- **Add a "noticed" channel to every agent's return** — FEATURE — value 3 — effort S — risk low — category: agent types
  Why: Foreman captures new requests instead of chasing them, but sub-agents have no structured way to hand over out-of-scope smells they see. Each return carries a `noticed:` list, and a collector dedups it against open tasks and captures the rest.
  Done when: a lane that reads a dead function outside its scope returns it under `noticed`, and a deduped captured task appears in the queue with a link to the lane.

- **Compile role cards into per-harness agents with a conformance report** — FEATURE — value 3 — effort M — risk low — category: harness parity
  Why: T-0335, T-0336 and T-0337 are blocked on Codex, Gemini and opencode behaving differently. A role card declares needs (read-only, worktree, model tier, tools), each adapter maps or degrades them, and `fm agents check` states per harness which guarantees hold.
  Done when: `fm agents check --harness codex` prints a table where every role is "exact", "degraded: <reason>" or "unsupported", and a degraded read-only role refuses to run write tasks.

- **Detect role drift in the ledger** — FEATURE — value 3 — effort M — risk low — category: agent types
  Why: assumption: roles are enforced by prompt, not by observed behaviour. Flag a builder that does 40 turns of research, a reviewer that edits, or a scout that reads past its bound. Report drift per role in `fm friction`.
  Done when: replaying a ledger fixture with a reviewer that wrote a file produces a drift finding naming the role, the tool call, and the rule it broke.

- **Keep a delegation ROI ledger and a spawn-or-not rule** — FEATURE — value 4 — effort M — risk low — category: orchestration
  Why: Foreman has many agent types but doesn't measure whether delegating beat doing the step inline. Record the brief-writing cost, the child cost, and whether the result was reused or redone, then warn at plan time when a step's similar past delegations lost.
  Done when: `fm friction` lists delegations that cost more than their inline equivalent, and a plan step with a losing history shows "do inline" as the default.

- **Interview every sub-agent on exit** — FEATURE — value 3 — effort S — risk low — category: learning
  Why: an agent's end state holds the cheapest signal about the brief: what surprised it, what it skipped, what the brief got wrong. Four fixed questions go into the receipt, and recall indexes them. The "brief was wrong" answers feed intake lessons.
  Done when: after a lane, `fm recall "brief wrong"` returns that lane's exit answer, and `fm friction` counts how many briefs were flagged.

- **Pull an andon cord from any lane** (wild) — FEATURE — value 4 — effort M — risk med — category: orchestration
  Why: assumption: parallel lanes keep building on a premise that one lane has already found false, such as a missing API or a wrong contract. A lane can halt siblings that share that premise, and the main thread rules on it.
  Done when: in a test, lane A pulls the cord with a premise id, lane B (tagged with the premise) pauses at its next step boundary, and lane C (untagged) continues.

- **Hire an agent by sentence** (wild) — FEATURE — value 3 — effort M — risk med — category: agent types
  Why: assumption: the user would write "a pedantic accessibility reviewer" before they'd write a role file. Foreman compiles the sentence into a role card plus a seeded bench case (a diff it must flag and one it must pass), and refuses the hire if the case doesn't discriminate.
  Done when: `fm agents hire "…"` writes a card and a bench case, and `fm bench` runs both and shows the new role beating a no-role baseline on its own case.

- **Give each module a spokesperson agent** (wild) — FEATURE — value 3 — effort L — risk med — category: agent types
  Why: assumption: cross-module changes break invariants that only the module's own code states. A read-only spokesperson per `plugin/lib` module answers only from its module and its tests, so a builder asks "can I change X?" and gets a cited answer with no cross-module context bleeding in.
  Done when: a builder's question about `fmguard.py` gets an answer citing lines and tests from that module only, and the lane trace shows no reads outside it.

- **Hold a weekly staff meeting per role** (wild) — FEATURE — value 3 — effort M — risk low — category: self-improvement
  Why: scorecards, drift findings, exit interviews and ROI data each exist as separate signals. A scheduled pass reads them per role and proposes one coaching edit per role, which `fm evolve` then tests against the bench before accepting.
  Done when: `fm staff` prints one proposed edit per role with its evidence, and applying one runs the bench and records an accept or reject.

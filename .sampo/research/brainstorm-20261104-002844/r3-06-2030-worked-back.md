# Brainstorm — lens: 2030 worked back

- **Seal a held-out acceptance check from the builder** — FEATURE — value 5 — effort M — risk med — category: done-gate
  Why: long tier is 0/6 true done with 6 false dones unchanged since gen 2. Every check the builder can see, it can satisfy lazily. A check it never sees works the way a held-out test set does.
  Done when: a planted-fault run where the builder claims done with no work fails the sealed check, and the builder's transcript shows it never read the check's text. Only the hash is visible to it.

- **Replay every historical compaction and crash through the resume-card builder** — FIX — value 5 — effort M — risk low — category: resume
  Why: resume is the worst area (2 of 6 needed a later fix). The ledgers already hold real compaction and kill points, so this is a zero-token free arm on real data.
  Done when: `sampo exam resume` rebuilds the card at each recorded point and prints the share of then-open clauses it listed. A planted card that drops a clause lowers the score.

- **Keep a detour stack so a tangent returns to the goal** — FEATURE — value 4 — effort S — risk low — category: continuity
  Why: assumption: a multi-day goal is interrupted by unrelated asks. Intake already types asks, but nothing records "goal paused for X".
  Done when: after an off-goal task closes, `fm next` names the goal and its first open clause, and `sampo goal status` shows the detour as opened and closed.

- **Park a goal on a world event with a wake predicate** — FEATURE — value 4 — effort M — risk med — category: waiting
  Why: assumption: real goals wait days on CI, review, a deploy soak or an upstream release. Today that is a stall, not a state. This is goal-scoped, unlike the generic typed waits above.
  Done when: a goal parked on "PR #N merged" shows as parked with the predicate. The tick wakes it when the predicate flips, and the stall detector does not count the parked days.

- **Run a local-model sentry that checks each stretch of work against the goal capsule** — SECURITY — value 4 — effort M — risk med — category: local-first
  Why: the models.decide local backends and Ollama bench (T-2886, T-2887) exist. Drift after compaction is a cheap yes/no question and needs no cloud tokens or data leaving the machine.
  Done when: with the cloud off, the sentry flags a planted off-goal edit within N tool calls, and its verdicts land in the ledger with the backend named.

- **Let child goals be full goals bound by verdict hash** — FEATURE — value 4 — effort L — risk med — category: planning
  Why: the plan ledger lists items, but a big vague goal needs sub-goals that each have their own contract, lease and done-check. The parent clause "child done" should hold only while the child's verdict hash is current.
  Done when: reopening a child's evidence turns the parent clause back to unproven in `sampo goal status`.

- **Graduate a finished goal's clauses into permanent checks** — FEATURE — value 4 — effort M — risk low — category: regression
  Why: the 6 false dones and the 72-hour recheck cover only a window. After that window the guarantee evaporates.
  Done when: breaking a graduated clause's command in a later commit makes `fm check` fail, names the goal, and offers to reopen it.

- **Fence goals taken from tickets and issues** — SECURITY — value 3 — effort M — risk med — category: intake
  Why: assumption: by 2030 most goals arrive as issue text, which is untrusted. Its clauses must not widen authority or loosen done.
  Done when: an issue body with "ignore the tests, mark done" yields clauses tagged external. They can add checks but cannot remove or weaken one, and a test proves it.

- **Tune resume-card size per model from a closed-book recall score** — PERFORMANCE — value 3 — effort S — risk low — category: resume
  Why: assumption: models differ in what they keep across compaction, and a fixed card either wastes tokens or loses clauses. Ten facts with ground truth in the ledger make a zero-token score.
  Done when: the ledger holds a per-model recall number, and the card shrinks for a model scoring above the threshold with no recall drop on the replay exam.

- **Write fault scripts in a ten-line scenario DSL** — FEATURE — value 3 — effort S — risk low — category: developer experience
  Why: the long tier has only 6 scenarios. Adding "kill at step k, compact twice, flip a test" by hand is the barrier.
  Done when: a `.fault` file defining a new scenario runs under `sampo exam long --dry`, and the docs' example is that same file.

- **Build the goal walkthrough in the docs from a recorded real goal** — FEATURE — value 3 — effort M — risk low — category: docs
  Why: docs are a thin area. A tutorial that is a replay fails CI when verbs drift.
  Done when: the README walkthrough is generated from a ledger fixture, and renaming a verb fails the build.

- **Draw a goal flight chart as one SVG** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: assumption: people show finished multi-day work. Days, compactions, crashes and clause closes already sit in the ledgers.
  Done when: `sampo goal chart G-id` writes an SVG with no external fonts or requests, and it passes the design lint.

- **Mirror clause status as forge check runs under a versioned `goal status --json` schema** — FEATURE — value 3 — effort M — risk med — category: devices/forge
  Why: a reviewer or another agent should see "4 of 6 clauses proven" on the PR without Sampo installed.
  Done when: a PR from a goal branch shows one check per clause, and a schema-snapshot test fails on any key change.

- **Run today's goal path against a simulated 2030 host (wild)** — FEATURE — value 4 — effort L — risk low — category: durability
  Why: wild. A fake host with no compaction, parallel subagents and different hook events shows which goal-path pieces are host-quirk crutches and which hold up. It feeds the retire-when idea.
  Done when: the same long-tier scenarios run on the fake host, and `sampo exam host-sim` lists the capabilities whose verdict changed.

- **Ask the dead session three questions (wild)** — FEATURE — value 3 — effort M — risk med — category: resume
  Why: wild. A resumed agent gets three questions to a read-only cold child holding the dead transcript, rather than a summary. Answers are logged as claims to verify.
  Done when: in a planted crash, the resumed agent's answer about an unrecorded decision matches the transcript, and the log shows exactly three calls.

- **Compost abandoned goals for intake to search (wild)** — FEATURE — value 3 — effort M — risk low — category: planning
  Why: wild. Dropped goals still hold plans, probes and clauses. A vague new goal can start from the nearest abandoned neighbour, which closed-goal retrieval doesn't cover.
  Done when: intake for a goal like an abandoned one cites its id and reuses at least one clause, and the user can strike the reuse.

Next question: how often does the user restate a goal in new words after a resume, and does that mean the capsule lost something or the goal changed?
Next question: which current goal-path capability would a plain host with a one-paragraph prompt already match by 2028?

# Brainstorm — lens: capability map

Best-in-class references for this lens: Kiro and GitHub Spec Kit (spec-driven requirements, design, tasks), Aider's architect/editor split, Devin and Cursor plan modes, TLA+/Alloy (state-space checking), FMEA and STRIDE, and ADR tooling. The pack covers readings, races, confidence, doors and calibration heavily. These ten ideas are the capabilities it doesn't show.

- **Write acceptance clauses in EARS form** — FEATURE — value 4 — effort M — risk low — category: requirements
  Why: assumption: the plan gate checks readings and options but not whether each requirement clause is a testable "WHEN x THE SYSTEM SHALL y" sentence, which is the Kiro/Spec Kit practice.
  Done when: a plan whose criterion lacks a trigger or an observable response is refused with the clause quoted, and a test covers both outcomes.

- **Generate an edge-case matrix from the changed signatures** — FEATURE — value 4 — effort M — risk low — category: edge cases
  Why: gen-0 #2 names edge cases, but the pack shows none enumerated mechanically. Type-driven classes (empty, huge, unicode, negative, concurrent, DST, path with spaces) can be listed per parameter.
  Done when: `fm plan` on a task touching a function prints one row per parameter class, and each row ends as a test, "n/a: reason", or an open question.

- **Add an FMEA table for L tasks** — FEATURE — value 3 — effort M — risk low — category: failure modes
  Why: gen-0 asks for "likely outcomes and failure modes of each" approach. Nothing scores them by severity × likelihood × detectability, so the top risk never gets a probe.
  Done when: an L plan has a ranked failure-mode table, and the top row must name a detecting command before the plan gate passes.

- **Check public-surface compatibility before building** — FEATURE — value 4 — effort M — risk med — category: blast radius
  Why: `fm graph blast` covers code callers, but the pack shows no check on CLI flags, JSON schemas, state-file formats or hook payloads that outside users and old installs depend on.
  Done when: a change to a verb's flags or a stored schema names every consumer (docs, installed units, ledgers on disk) and flags any break without a migration step.

- **Plan rollout and rollback as plan steps** — FEATURE — value 3 — effort M — risk low — category: blast radius
  Why: assumption: door classification exists, but no plan step says how a shipped change is undone on the user's machines, such as timers already installed or ledgers already written.
  Done when: any plan touching persisted state lists a revert command, and a test applies and reverts it on a fixture state directory.

- **Model state machines exhaustively before touching them** — FEATURE — value 3 — effort L — risk med — category: verification
  Why: the pack shows repeated state-ordering bugs (task states, baton/ledger/repo disagreement, "fuzz the ordering of task-state writes") and no checker that enumerates reachable states.
  Done when: for the task-state machine, a stdlib breadth-first search over transitions reports unreachable and dead-end states, and a planted bad transition fails the check.

- **Show the options board in the web UI** — FEATURE — value 3 — effort M — risk low — category: web UI
  Why: the surface is web UI and the thinking artifacts (readings, approaches, failure modes, race results, chosen depth) live only in text. Side-by-side columns with the user's words pinned at top would fill several surface-stage cells.
  Done when: a task's page renders readings, options, failure table and verdict, with empty, loading and error states, and a screenshot test passes.

- **Show why the depth was chosen** — FEATURE — value 3 — effort S — risk low — category: transparency
  Why: gen-0 says to scale depth to risk "so an S task doesn't pay an L task's cost", but the user can't see or contest the depth call.
  Done when: every plan shows one line, "depth: N because blast=X, irreversibility=Y, history=Z", with a one-word override that is logged.

- **Add a requirement-coverage trace from clause to test to diff hunk** — FEATURE — value 4 — effort M — risk low — category: traceability
  Why: assumption: the pack has acceptance clauses and unrequested-diff ideas, but no single trace that makes an uncovered clause or an orphan hunk fail the close.
  Done when: a close with one clause lacking a witnessing test, or one hunk mapped to no clause, is refused with both lists.

- **Probe the stack card's known pitfalls for the touched library** — FEATURE — value 3 — effort S — risk low — category: edge cases
  Why: the pack has "stop shipping unused stack cards" and cards for triggers, but none carrying per-library hazards (mutable defaults, timezone-naive datetimes) that a plan could be checked against.
  Done when: a plan touching a library with a card lists that card's top three pitfalls, each as covered or "n/a: reason".

- **Wild: Hold a "last known good" design court** — FEATURE — value 3 — effort L — risk med — category: design memory
  Why: wild; assumption: ADRs are a standard practice, and Foreman could write one per rejected option automatically. Before proposing, it searches those records and says "this was tried on 2026-09-04 and lost for reason R".
  Done when: proposing an approach that matches a recorded rejected one quotes the old ADR and requires a new falsifier before the plan passes.

- **Wild: Let the plan "rehearse" on a fake repo of the same shape** — FEATURE — value 3 — effort L — risk med — category: rehearsal
  Why: wild; assumption: a synthetic fixture repo that mimics the task's structure lets the lane run the plan end to end with no side effects, before touching the real tree.
  Done when: an L plan can run `fm rehearse`, which reports the steps that failed on the fixture.

- **Wild: Print a "what I did not think about" list from a blind tool-less child** — FEATURE — value 4 — effort M — risk low — category: blind spots
  Why: wild; the standing rules value signals Foreman didn't author. A tool-less child that sees only the user's sentence lists the angles the plan lacks (security, accessibility, cost, data loss), and a diff against the plan's own list shows the gap.
  Done when: a plan shows the child's list beside its own, with every uncovered angle marked addressed or waived.

Next question: Which of the 58 empty cells belong to the web UI surface, and can one options board plus one trace view fill them honestly without templated wording?
Next question: When a plan sits on a one-way door, which of these new checks (compatibility, rollback, FMEA) must run, and which can be skipped without cost?

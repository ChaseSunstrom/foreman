# Brainstorm — lens: blind spots

Lens: blind spots. The eight missed asks (T-2533 to T-2554) share one shape. Each is a follow-up on something Foreman had just shipped, or a place where Foreman's own output went unchecked.

The question each should have triggered:
- **T-2533:** what does Foreman inject that no gauge counts?
- **T-2534, T-2536:** what is the control arm for each claim?
- **T-2535:** when a gate trips, does it name the cause?
- **T-2542:** what can die silently?
- **T-2546:** is it already built?
- **T-2547:** what does a producer accept without checking?
- **T-2554:** what feeds a learner that the user didn't write?

I asked those of the whole project and kept only what the ~3,000 earlier ideas don't already cover.

- **Give every gauge a drill-down contract** — FEATURE — value 4 — effort M — risk low — category: gauges
  Why: T-2533, T-2535 and the `--by harness` ask each extended a just-shipped gauge with a split or a cause. Assumption: the next gauge will draw the same follow-up.
  Done when: a lint fails any verb printing an aggregate number that lacks `--by` and `--why`, and passes after both are added.

- **Refuse a DONE-WHEN that is already true at birth** — FEATURE — value 4 — effort S — risk low — category: intake
  Why: T-2546 checks "already built" by text match only. Running the DONE-WHEN's named check at HEAD would catch it by behaviour, and the goal-oracle idea doesn't cover tasks.
  Done when: `fm task new` with a DONE-WHEN naming a test that already passes prints "already satisfied at HEAD" and files nothing without `--force`.

- **Print current behaviour beside every symbol a request names** — FEATURE — value 4 — effort M — risk low — category: intake
  Why: steered "re-scoped after reading fmdoors" and the `hash % len` exam re-scope both came from criteria written before the deciding code was read. Evidence in the steers; the mechanism is my assumption.
  Done when: a task naming `fmdoors._ambiguous` carries a 3-line excerpt of that function in its brief at filing time.

- **Import rivals' fixed permission bugs as guard cases** — FEATURE — value 4 — effort M — risk low — category: guard
  Why: the frontier names Claude Code v2.1.289 (deny/ask on nested parts of compound shell commands) and the prefix-versus-structure prompt mismatch. Neither appears in the 124-case replay corpus.
  Done when: `fm replay` includes at least 10 cases labelled with a rival release note, and each is allowed or denied as labelled.

- **Add an outside-in quota per generation** — FEATURE — value 4 — effort S — risk low — category: direction
  Why: nearly every recent ask is Foreman measuring itself (ratchet, exam arms, liveness). The frontier lists outside pains (approval-prompt fatigue, usage transparency, near-miss output) with no tied task. Assumption: the user wants the product to serve users beyond itself.
  Done when: the generation report shows self-improvement versus outside-evidence task counts, and the sweep goes amber if outside-evidence is zero.

- **Put new gauges on probation** — FEATURE — value 3 — effort M — risk low — category: gauges
  Why: the open question about which gauge the user trusts and whether it was ever checked against ground truth. A gauge can run in shadow and publish only its own error estimate first.
  Done when: a new gauge prints "probation, n/14 days" instead of a number until it has been compared with an independent slow path once.

- **Map dark modules** — FEATURE — value 3 — effort S — risk low — category: coverage
  Why: the user's asks cluster on a few modules. A listing of modules with zero asks, steers or reopens in 90 days shows where nobody is looking.
  Done when: `fm doctor` lists modules by days since a user word touched them, and the next brainstorm pack includes the top five.

- **Log post-finish touches** — FEATURE — value 4 — effort M — risk low — category: quality
  Why: 66% cite near-miss AI output and 45% say debugging takes longer. Foreman can't see the user's small fixes within an hour of a finish.
  Done when: a user edit to files in a task's diff within 60 minutes of finish records a "touched after" row, and `fm outcomes` counts them by task kind.

- **Rehearse scale on a synthetic state** — PERFORMANCE — value 3 — effort M — risk low — category: scale
  Why: assumption: the ledgers, bets and recall grow without bound, and only hook p95 is budgeted. The 1,214 stack cards already hint at growth.
  Done when: a test builds a 50k-event state in a temp dir and fails if any read verb exceeds its latency budget.

- **Take a refusal census** — CLEAN — value 3 — effort S — risk low — category: validation
  Why: T-2547 added a refusal to one verb. The class is "agent-authored input accepted unchecked", and no list says which verbs still do that.
  Done when: a generated table lists each writing verb with its refusal rules, and verbs with none carry a recorded "n/a because".

- **Show model and usage window** — FEATURE — value 3 — effort M — risk low — category: transparency
  Why: the frontier reports demand for usage percentage, active model and a `/usage` command, and the issue was closed as not planned. Foreman already reads transcripts.
  Done when: `fm usage` prints window use and last-seen model for each harness from local files, with "unknown" where unreadable.

- **Wild: convene a persona panel for asks** — FEATURE — value 3 — effort M — risk low — category: foresight
  Why: wild. The stub-user ideas copy the one user. A tool-less child as an impatient newcomer, a team lead and a security reviewer each lists the first three asks they'd make, and the union is compared with real asks.
  Done when: one run produces three persona lists, and at least one item not in the existing idea catalog is filed as a capture.

- **Wild: write the product blind** — FEATURE — value 4 — effort M — risk low — category: documentation
  Why: wild. Every 50 tasks a child sees only the code and tests, with MASTER.md and lessons hidden, and writes what Foreman does. Where that diverges from MASTER.md shows what the documentation hides or invents.
  Done when: the diff between the blind summary and MASTER.md lists at least one capability on each side, and each is filed as a task or a recorded n/a.

- **Wild: hold a missed-ask replay each generation** — FEATURE — value 3 — effort S — risk low — category: process
  Why: wild. Each new missed ask becomes a one-line question appended to a standing deck that every capture asks of itself ("does this add a gauge? then a drill-down"). The deck is graded by whether later asks of the same class stop arriving.
  Done when: the deck holds the eight classes above, and `fm capture` prints the matching question for a gauge-related request.

Next question: which verbs print a number or verdict whose cause or split the user has had to ask for, and can the next ask be answered before it is made?
Next question: which Foreman outputs are consumed only by the user's eyes, with no machine check, so that a wrong value would sit unnoticed?

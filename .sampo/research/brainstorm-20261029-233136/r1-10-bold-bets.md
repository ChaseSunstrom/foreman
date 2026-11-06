# Brainstorm — lens: bold bets

Lens: bold bets for capability #13 (Genesis as a feature). All assumptions are marked; nothing below re-proposes what is already built (tower storage, exam gen/run/grade, ideas, second, loop, scout, lane).

- **Write gen-0 from one line or nothing** — FEATURE — value 5 — effort L — risk med — category: genesis core
  Why: gap map #13 tier 3 lists the gen-0 writer as missing. Gen-0 is the root every other step depends on, and today it is hand-written (SEED_PROMPT.md).
  Done when: on 3 held-out generated projects, given "make this great" or an empty string, `fm genesis gen0` writes a gen-0 whose MUSTs, NEVERs and sections are a superset of the hand-written reference, as graded by `fm exam grade`.

- **Run the tower from a single orchestrator verb** — FEATURE — value 5 — effort L — risk med — category: orchestrator
  Why: the tower steps (Seed, ≤ 8 Missions, briefs, critique, selection, drift, sweep) exist only as manual puts. The user steered "in-depth look at each generation", which implies they are run end to end.
  Done when: `fm genesis run` on a fixture repo produces gen-1 with Seed, Missions, critiques, lineage.md and a sweep report, and exits on a stated budget cap.

- **Gate rewrites on exam closure with lineage** — FEATURE — value 5 — effort M — risk low — category: selection
  Why: the spec says a rewrite stays only if it closes more scenarios than its parent. The exam exists, but nothing enforces the rule or records it.
  Done when: a rewrite that ties or loses is reverted automatically and lineage.md records the scores, the cost and the reason; a winning one is kept.

- **Build a coverage grid with no empty cells** — FEATURE — value 4 — effort M — risk low — category: coverage
  Why: the missing list names it. Assumption: the grid is capability × scenario kind (11 kinds) × language (6).
  Done when: `fm genesis grid` prints the grid, and `--strict` exits non-zero while any cell has no scenario or a not-yet entry.

- **Keep a not-yet ledger retried each generation** — FEATURE — value 4 — effort S — risk low — category: ledger
  Why: the user's standing steer says no idea is killed for ambition; a failed spike gets ≥2 approaches, then goes to the ledger with its blocker.
  Done when: each new generation re-attempts every ledger entry whose blocker has changed, and the ledger shows the attempt count and last result.

- **Check drift against gen-0 on every generation** — FEATURE — value 4 — effort M — risk low — category: guard
  Why: the inversion risk is a self-written gen-0 that has quietly dropped a MUST or NEVER. `fm second` exists as the cold reviewer.
  Done when: planting a deleted NEVER in gen-N makes the drift check fail the generation and name the missing clause.

- **Start on its own when the queue runs dry** — FEATURE — value 4 — effort M — risk high — category: auto-start
  Why: the spec requires auto-start from loop/scout. The routing line in rules/foreman.md is protected core, so the change ships only as a candidate patch.
  Done when: an empty queue with a large gap map makes the loop propose a Genesis run as a pending candidate and a user-approval prompt; with no approval, nothing starts.

- **Cap a Genesis run by budget and wall-clock** — SECURITY — value 4 — effort S — risk low — category: guard rails
  Why: inversion lens: Genesis can burn a week of usage on one project. The pack shows a USD budget model elsewhere.
  Done when: a run with a $2 cap stops at or before $2, writes a resumable state file, and says why it stopped.

- **Carry winning templates over to the next project** — FEATURE — value 3 — effort M — risk low — category: carry-over
  Why: the spec lists winning Seed and mission templates, lenses that paid off and lineage as defaults. `lens_rates` already exists in the brainstorm code.
  Done when: a second project's Genesis starts from the carried defaults and its run log shows which were applied.

- **Write each project's own capability spec** — FEATURE — value 4 — effort L — risk med — category: spec
  Why: the spec calls for "complete and best-in-class for this kind of project". Assumption: capability-map brainstorms can run on a project kind learned from `fm map`.
  Done when: a fixture web app and a CLI each get a distinct spec file, each with ≥ 9 exam scenarios and ≥ 3 held out.

- **Wild: Let Genesis argue with itself before it writes a MUST** — FEATURE — value 3 — effort M — risk med — category: adversarial (wild)
  Why: assumption: a tool-less red-team child, shown only the project, tries to make each proposed MUST false. Surviving MUSTs are kept. This addresses a self-written gen-0 that sets easy goals.
  Done when: a seeded vacuous MUST ("code should be good") is struck out by the red team, while a testable one survives.

- **Wild: Hold a hidden exam the tower can't see, rotated each generation** — SECURITY — value 4 — effort M — risk low — category: anti-overfit (wild)
  Why: the inversion lens warns of overfitting the held-out third. Assumption: a fresh tool-less author writes a new third per generation, and scores are reported only as pass or fail.
  Done when: a rewrite tuned to last generation's held-out third scores no better on the new one, and the report shows both.

- **Wild: Replay the tower as a time-lapse on the site page** — FEATURE — value 2 — effort M — risk low — category: delight (wild)
  Why: the site page exists and the user asked for per-generation detail. Assumption: the export data has a timestamp per put.
  Done when: the page has a scrubber that steps through generations and shows each one's tower state at that point.

- **Wild: Fork a tower to try a risky rule on a clone** — FEATURE — value 3 — effort L — risk med — category: self-modification (wild)
  Why: assumption: `fm lane race` can run two tower variants on the same exam. The user's drive for self-improvement ("genuinely smarter") needs reversible trials.
  Done when: a proposed change to Genesis's own selection rule runs in a fork, and merges back only if it beats the parent on the exam at ≤ 1.5× the cost.

Next question: What does Genesis do when the user's MUSTs from their history contradict each other, and who breaks the tie?
Next question: How is a generation's cost per closed scenario measured, so that "stop early" can be a number rather than a feeling?

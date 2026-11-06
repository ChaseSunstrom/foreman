# Brainstorm — lens: capability map

- **Snapshot the red baseline before planning** — FEATURE — value 4 — effort S — risk low — category: verification
  Why: T-2526 makes `fm task finish` refuse on a failed full check, and the flake-ledger idea exists, but nothing records what was already failing before the edit. Cursor and Aider don't either, so this is room to lead.
  Done when: the plan prints the failing tests and lint at plan time, and finish labels each failure "pre-existing" or "new".

- **Map cross-repo consumers in blast radius** — FEATURE — value 4 — effort M — risk med — category: blast radius
  Why: assumption: `fm graph blast` stops at the repo edge. A public verb or schema change can break the user's other local repos, and Sourcegraph-style tools do this search.
  Done when: changing a function exported to a second local fixture repo makes the plan's Risks name that repo's call sites.

- **Search the user's other repos for prior art** — FEATURE — value 3 — effort M — risk low — category: reuse
  Why: assumption: "use what exists" currently means this repo and the ecosystem. The user's own earlier solutions are the closest match.
  Done when: for a task with a known solution in a second local repo, the Approach lists it as an option with a path.

- **Mine conventions from neighbouring files** — FEATURE — value 3 — effort M — risk low — category: plan quality
  Why: assumption: stack cards give generic idioms, but diffs get rejected for not matching local naming, error handling and test layout.
  Done when: the plan has a "match these" section of 3 to 5 conventions, each citing a file, and a style-drift check at finish passes on a fixture.

- **Inject faults into the changed code's dependencies** — FEATURE — value 4 — effort M — risk med — category: edge cases
  Why: the pack covers fuzzing the changed functions and chaos on Foreman itself, but not forcing timeouts, ENOSPC, partial writes or empty responses on what the user's code calls.
  Done when: a seeded fixture where a swallowed exception hides a bug fails the injected-fault check and passes after the fix.

- **Slice the plan into reviewable green commits** — FEATURE — value 3 — effort M — risk low — category: delivery
  Why: `fm pr train` merges PRs and Spec Kit and Kiro emit task lists, but an L plan has no ordered slices where each one passes on its own.
  Done when: an L plan lists slices, `fm check` passes at each slice commit in a fixture, and a slice that breaks the tree is named.

- **Add an observability line to every plan** — FEATURE — value 3 — effort S — risk low — category: outcomes
  Why: `fm ship --chance` and `fm ci-watch` settle bets after the push, but a plan never says what signal would show the change failing in use.
  Done when: the plan gate requires a "how we'll know it broke" line for FEATURE and FIX tasks at M or larger, and the close receipt repeats it.

- **Ingest evidence artefacts into the readings** — FEATURE — value 3 — effort M — risk med — category: intake
  Why: assumption: stack traces, linked issues, logs and pasted screenshots reach the readings only as prose. Each should become a cited fact. Text from outside sources is fenced as data.
  Done when: a task with a pasted traceback yields a reading naming the file and line, quoted from the trace.

- **Check dependency bumps against the installed API** — FEATURE — value 3 — effort M — risk low — category: change safety
  Why: stack cards carry pitfalls, but nothing diffs the changelog or the installed package's real signatures for a version bump.
  Done when: a bump fixture with a renamed argument produces a plan risk naming the call sites that use it.

- **Export and import plans as Spec Kit / Kiro files** — FEATURE — value 3 — effort S — risk low — category: interop
  Why: the standing rule says Foreman serves all agents, and hookless harnesses already get "plans as files". Writing the open spec-driven formats lets Codex, Gemini and opencode read the plan.
  Done when: `fm plan export` writes requirements, design and tasks files that a round-trip import reads back to the same plan.

- **Wild: Find contradictory acceptance clauses with an SMT solver** — FEATURE — value 3 — effort L — risk med — category: requirements
  Why: wild. EARS clauses are in the pack, but nobody checks them for unsatisfiable pairs ("always under 50 ms" with "retry 5 times at 1 s"). Cheap clause shapes could compile to Z3 or a plain constraint check.
  Done when: a fixture with two conflicting clauses is refused with both quoted, and a consistent set passes.

- **Wild: Write a cheat implementation against the acceptance tests** — FEATURE — value 4 — effort M — risk low — category: proof strength
  Why: wild. Mutation grading is in the pack, but not a lane that writes the laziest code that passes the tests (hardcoded outputs, special-cased inputs) to expose weak specs.
  Done when: on a fixture with a hardcodable test, the cheat passes, the weak test is named, and the close is held until a second test kills the cheat.

- **Wild: Haunted comments, turning stale assumptions into checks** — FEATURE — value 3 — effort M — risk low — category: edge cases
  Why: wild. Comments, constants and docs near touched code ("never null", "at most 3 workers") are free assumptions that go stale unnoticed.
  Done when: for a diff touching a function with such a comment, the plan lists each claim with a result: still true by test, false, or unknown.

- **Wild: Review the plan as the repo's maintainer persona** — FEATURE — value 3 — effort M — risk med — category: review
  Why: wild. Merged PR review comments hold the project's taste. A child grounded only in those comments reviews the plan before the user sees it.
  Done when: a fixture comment history ("always add a changelog line") makes the persona flag a plan with no changelog step, and a plan that has one passes.

Next question: Which of these capabilities can be checked on a stranger repo with no history, and which only pay off where review comments, other repos or a baseline already exist?
Next question: Which of the 58 empty cells are only empty because no probe ran the deliberation on a real task kind, rather than because the capability is missing?

# Brainstorm — lens: capability map

- **Enumerate the request's conditions as a decision table** — FEATURE — value 4 — effort M — risk low — category: coverage
  Why: assumption: requests like "stop when it has spent N since its last task close" hide if/and/unless clauses, and the grid only tests failure modes. One row per condition combination makes untested combinations visible.
  Done when: for a planted request with 3 conditions, `fm` prints 8 rows, and the rows with no brief or a stated n/a are flagged.

- **Sweep zero, one, many and max for every noun in the request** — FEATURE — value 4 — effort S — risk low — category: boundaries
  Why: the pack has a limit register and "n−1, n, n+1" tests for caps, but nothing applies boundary values to a request's own nouns (no tasks, one lane, 10k tasks).
  Done when: a Mission page shows a 4-column row per noun and each cell holds a brief id or a reason.

- **Check verb-lifecycle completeness for what a Mission adds** — FEATURE — value 4 — effort M — risk low — category: completeness
  Why: T-2735 had to point an unknown `list` action at the parser's listing action, so a user guessed a verb shape that didn't exist. Best-in-class tools check create, list, show, edit, delete, export and undo for each noun.
  Done when: for a new verb with only `add`, the check names the missing list, show and undo actions, and a planted verb with all of them passes.

- **Add an old-data and time column to every brief** — FEATURE — value 5 — effort M — risk low — category: migration
  Why: T-2731 (journals losing a newline) and the volatile-path audit show old and odd records outlive the code that wrote them. Each brief states what existing ledger rows do under the change, and what happens at day 1, day 30 and day 365.
  Done when: a brief that adds a record field without an old-row line is refused at filing, and a test file holds a fixture of pre-change rows.

- **List each ambiguous word in the request with its readings** — FEATURE — value 4 — effort S — risk low — category: interpretation
  Why: the earlier "Record which scope width" idea covers width only. Words like "exhaustive", "left out" and "outcome" each have several readings, and the user's drops (for example "premise already met") are often a reading mismatch.
  Done when: the Mission page opens with a short lexicon of at most five words, each showing the readings and the one each brief took.

- **Check a new brief against the last three Missions' shipped changes** — CLEAN — value 3 — effort M — risk low — category: interference
  Why: the pack proposes linting against open briefs, but several recent fixes (T-2691/2693, T-2720/2724) reworked what the previous Mission had just changed.
  Done when: filing a brief that touches files changed by a closed task within 14 days prints that task id and the overlapping paths.

- **Require two kinds of evidence behind every "not built" and "built" claim** — FIX — value 4 — effort M — risk low — category: grounding
  Why: grounding is one of the Mission's own steps, and the drops ("premise already met") show single-kind evidence failing. The kinds are a code hit, a ledger row, a command output, and the user's words.
  Done when: a claim with only one evidence kind is marked weak on the page, and a planted false "not built" with a single grep hit is caught.

- **Write each brief's undo and footprint line** — FEATURE — value 3 — effort S — risk low — category: reversibility
  Why: standing rules favour reversible, lean work, but no brief field says how to back out or what it leaves in the state dir.
  Done when: every filed brief has an `Undo:` line, and `fm genesis check` fails on a brief without one.

- **Pre-stage the wider reading of every scope choice (wild)** — FEATURE — value 4 — effort M — risk med — category: scope
  Why: assumption: the user narrows scope often (the "scoped to … left out" steers), and each narrowing is a request they must repeat later. A stub of the first brief of the wider reading, unfiled and fileable with one word, removes that step.
  Done when: for a Mission filed at the narrow width, the page lists one fileable stub per dropped width, and `fm task new --from-stub` files it.

- **Have a child reverse-intake the filed briefs (wild)** — FEATURE — value 3 — effort S — risk low — category: fidelity
  Why: assumption: a tool-less child that reads only the briefs and writes the one-sentence request shows what they really assume, and the diff against the actual request exposes drift.
  Done when: the Mission close prints the child's sentence beside the real request, and a planted unrelated brief shifts the sentence.

- **Hold a Rashomon pass with five roles (wild)** — FEATURE — value 3 — effort M — risk low — category: perspectives
  Why: the pack has personas for newcomers and attackers but no fixed set of roles. A maintainer, an auditor, a first-hour user, another agent and the user-in-a-hurry each name their top three fears, and the union becomes the grid's columns.
  Done when: one Mission page lists each role's fears, and at least one column exists that the current five failure-mode columns lack.

- **Show the words in the request that no brief contains (wild, zero-token)** — FEATURE — value 3 — effort S — risk low — category: traceability
  Why: a lexical orphan list is cheap and sits between the heavy "trace every clause" ideas and doing nothing.
  Done when: `fm genesis check` prints the request's content words absent from all briefs, and a planted dropped clause appears in the list.

- **Make the Mission page machine-readable beside the prose** — CLEAN — value 3 — effort M — risk low — category: format
  Why: the earlier ideas about readings, dissents, cells and left-out items each need a reader, and they all parse prose today.
  Done when: each Mission writes a JSON twin with cells, readings and omissions, and a test checks the page and twin agree.

Next question: which of these axes (conditions, boundaries, old data, roles) has the user's own history already shown them adding by hand?
Next question: does the user read the lexicon and undo lines at all, or only the briefs?

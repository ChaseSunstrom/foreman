# Brainstorm — lens: capability map

**Reference products:** Kiro (spec → design → tasks), Aider (architect/editor split), Claude Code and Cursor plan modes, Devin (plan with citations), log4brains and adr-tools (decision records), TLA+/Alloy (state models), Hypothesis (property tests), CodeScene (hotspots). Everything below is absent from the "ideas so far" list.

- **Split architect from editor** — FEATURE — value 4 — effort M — risk low — category: delegation
  Why: assumption: Aider's best-known capability is a reasoning model that writes a machine-readable plan and a cheaper one that applies it. The pack has "replay the thinking once" but no executor that is held to the plan.
  Done when: a plan file with numbered steps drives a cheap-model lane, and a step run out of order or off-plan is logged as a deviation at `fm task finish`.

- **Diff the plan against the diff at finish** — FEATURE — value 4 — effort M — risk low — category: verification
  Why: assumption: "flag unrequested behaviour" exists, but no check maps each plan step to a hunk. Steps with no hunk (skipped) and hunks with no step (drift) are both unreported.
  Done when: a finish on a fixture task prints "step 3 has no hunk" and "file X changed, no step names it".

- **Extract a project glossary from the user's words** — FEATURE — value 4 — effort M — risk low — category: readings
  Why: the user's phrasing keeps being read differently ("exhaustive", "cell", "mission"). Disambiguating readings needs a word-to-code-identifier map, which nothing in the list builds.
  Done when: `fm glossary` lists the user's recurring nouns, each mapped to a file or verb. A plan that uses a glossary term in a different sense is flagged.

- **Run throwaway spike lanes that return findings, not code** — FEATURE — value 3 — effort M — risk low — category: approaches
  Why: the race, probes and ghost branches all keep code. Time-boxed spikes in Kiro and Devin return only "what I learned, what blocks, the estimate", and discard the tree.
  Done when: a spike lane exits with a ≤20-line findings file and a deleted worktree, and the plan cites the file.

- **Select a non-functional checklist by touched paths** — FEATURE — value 3 — effort S — risk low — category: edge cases
  Why: assumption: the list has an edge-case deck and a threat-model line, but no accessibility, performance, i18n or concurrency prompts keyed to the path. The web UI cells need the first two.
  Done when: a diff under `plugin/templates/web/` adds an accessibility and a loading-state line to the plan, and a diff under `plugin/lib/` does not.

- **Plan expand/contract for schema and state-file changes** — FEATURE — value 3 — effort M — risk med — category: migration
  Why: Foreman's own state (ledgers, baton, task files) changes shape across versions. "Rollout and rollback as plan steps" exists, but no template covers old and new readers living together.
  Done when: a plan touching a state-file format must name the reader of the old shape, the writer of the new one, and the step that drops the old.

- **Version the plan and show what changed between revisions** — FEATURE — value 3 — effort S — risk low — category: plan UX
  Why: assumption: plans are rewritten after a rival reading or a stop. A diff of readings, options and chosen approach shows where the thinking moved, and the pack never mentions one.
  Done when: `fm plan diff T-N` prints added and removed readings and options between the last two revisions.

- **Draft the PR and issue text from the deliberation, staged behind a yes** — FEATURE — value 3 — effort M — risk med — category: developer experience
  Why: decision records are listed, but the outward artifact reviewers read is not. Publishing is outward-facing, so it is staged and never auto-sent.
  Done when: finish writes `pr-body.md` with the readings, the road not taken and the proof lines, and nothing is pushed without a grant.

- **Run recon and edge-case generation on a local model, nothing sent** — FEATURE — value 3 — effort M — risk low — category: privacy
  Why: assumption: readings and edge-case decks are cheap, read-only generations. The pack has a "local model for zero-risk lane steps" idea but not for deliberation, and the thin list names privacy.
  Done when: with a setting on and a local engine present, `fm plan` makes zero outbound model calls (checked by the egress ledger) and still emits a deck.

- **Put a deliberation page in the web UI as a single board** — FEATURE — value 4 — effort L — risk low — category: web UI
  Why: only the web UI surface is in this mission, and its empty cells are the fill target. Options board, door tally and blast ripples are scattered across ideas but never joined into one page with empty, loading and error states.
  Done when: one page shows readings, options, depth gauge, door tally and the proof line for a task, with a screenshot of each of its three non-happy states.

- **Wild: Test the design against the next three predicted asks** — FEATURE — value 4 — effort L — risk med — category: foresight
  Why: wild. Plans are judged on today's ask. A blind child writes the three most likely follow-ups from the "asked" stream, and the plan is checked for what each would force to be rewritten.
  Done when: a plan receipt lists three follow-ups, each marked "fits" or "forces rewrite of X".

- **Wild: Rubber-duck mode where Foreman only asks questions** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: wild. When the user is unsure of a reading, a mode that returns only the 3 questions that would split their readings is cheaper than a plan and fits the "ambiguity as a measured fork" idea.
  Done when: `fm duck` prints at most 3 questions and no plan, and each question names the two readings it separates.

- **Wild: Study a rival repo's solution to the same problem** — FEATURE — value 3 — effort L — risk med — category: prior art
  Why: wild. Capability maps compare against Kiro and Aider, but the pack searches only the user's own history. A read-only lane clones an open-source rival into an empty directory and writes "how they did X, what we'd steal, what we'd skip".
  Done when: a note cites file paths in the rival repo, and the clone sits in its own directory and is deleted after.

- **Wild: Hold a confirmed-gap vote on each of the 58 cells before writing them** — FEATURE — value 3 — effort S — risk low — category: coverage
  Why: wild. Before any prose, three cheap children each label a cell "built / gap / n/a" with a cited grep. Cells where they disagree get written first, so the fill spends effort only where the evidence is contested.
  Done when: a table of 58 rows shows three labels each, and writes happen in order of disagreement.

Next question: Which of the 58 empty cells are web-UI-only (screens, empty states, transitions) rather than deliberation logic, and does the UI work already planned for the web surface cover them?
Next question: Which stage of the deliberation flow (readings, options, race, door check, close) has the fewest real session paths calling it, per the reach check?

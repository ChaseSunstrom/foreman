# Brainstorm — lens: simplicity

- **Make `fm genesis run` the single entry that prints one next action** — FEATURE — value 5 — effort M — risk low — category: orchestrator
  Why: the pack lists init/put/status/export/live/publish but no verb that drives; the user asked for "runs the whole tower by itself". Existing ideas propose state machines; this is the thin version: read tower files, decide the one missing artifact, do it, stop.
  Done when: on a fixture project, calling `fm genesis run` repeatedly (no flags) reaches a finished tower, each call doing exactly one stage and printing its name.

- **Store the tower as plain files with the filename as the stage** — CLEAN — value 4 — effort S — risk low — category: storage
  Why: assumption: stage state lives in a separate record today. If `gen-N/seed.md`, `missions.md`, `critique.md`, `exam.json`, `verdict.md` exist, then "where are we" is a directory listing; no journal or lock needed.
  Done when: deleting `gen-1/critique.md` makes `fm genesis status` report critique as the next stage and nothing else changes.

- **Write gen-0 by extraction first, model second** — FEATURE — value 5 — effort M — risk med — category: gen-0 writer
  Why: gap map "gen-0 writer from one line or nothing"; steer "I want foreman to just genuinely be smarter, not hardcoded". Pull MUST/NEVER lines from CLAUDE.md, rules, README and the user's steers; only the remainder goes to a tool-less call.
  Done when: on a repo with a CLAUDE.md containing 3 NEVERs, the self-written gen-0 contains all 3 verbatim, with zero model calls in the extraction step.

- **Collapse drift check into a diff of two line sets** — CLEAN — value 4 — effort S — risk low — category: drift
  Why: gen-0 §2/§3 MUST/NEVER coverage is the exam's own pass criterion; a set difference of normalized MUST/NEVER lines between gen-0 and the self-written one is the check. No `fm second` call needed unless the diff is non-empty.
  Done when: removing one NEVER from a draft makes the check fail naming that line; an identical draft passes without a model call.

- **Use one `rules.md` for the spec; the coverage grid is a view of it** — CLEAN — value 4 — effort S — risk low — category: spec
  Why: gap map lists spec, grid and exam separately (3+3+3). One spec file whose rows are capabilities, with exam scenarios tagged by row, makes "no empty cells" a one-line query rather than a stored artifact.
  Done when: `fm genesis grid` prints rows from the spec with scenario counts, and a row with 0 scenarios exits non-zero.

- **Selection is `closed(child) > closed(parent)`, else keep parent, logged in one line** — FEATURE — value 4 — effort S — risk low — category: selection
  Why: gap-0 text says "a rewrite stays only if it closes more exam scenarios than its parent"; nothing more is required. Lineage is just that log appended to `lineage.md`.
  Done when: a tie leaves the parent as the current file and appends `gen-2 lost 5<=5`.

- **Make not-yet a section header, not a subsystem** — CLEAN — value 3 — effort S — risk low — category: ledger
  Why: user's steer: failed spike gets ≥2 approaches then ledger. A markdown list with `tries: n` per line, read at the start of each generation, covers it.
  Done when: a ledger entry with `tries: 2` is surfaced as the first mission candidate in the next generation's seed and `tries` increments.

- **Auto-start is one line in `loop`: queue empty and no tower → propose** — FEATURE — value 4 — effort S — risk low — category: auto-start
  Why: gap map says the routing line is protected core, so it ships as a candidate. Keep it a single condition and a single suggestion.
  Done when: with an empty queue and no tower, the loop's output includes "run fm genesis"; with a tower present it doesn't.

- **Ship Genesis with zero flags and one budget number** — FEATURE — value 3 — effort S — risk low — category: ux
  Why: the pack's ideas stack caps, fuses, cooldowns. Simplicity answer: one `--max-usd` default, checked between stages, everything else derived.
  Done when: a run with the cap set to 0.01 stops after the first stage with "budget reached at stage X".

- **Wild: delete subcommands from help; show only `fm genesis` and `fm genesis undo`** — FEATURE — value 3 — effort S — risk med — category: surface
  Why: wild; init/put/status/export/live/publish are plumbing a user shouldn't have to learn. Plumbing stays callable but hidden.
  Done when: `fm genesis --help` lists at most 3 lines of verbs.

- **Wild: gen-0 as a one-page questionnaire answered by the repo itself** — FEATURE — value 3 — effort M — risk med — category: gen-0 writer
  Why: wild; a fixed 10-question template ("what must never happen? what is done?") filled from repo evidence, with unknown shown as "unknown". Same template every project makes towers comparable.
  Done when: two different fixture repos produce gen-0s with identical section headings.

- **Wild: the tower fits on one page — a hard 200-line ceiling on any generation's docs** — CLEAN — value 3 — effort S — risk low — category: legibility
  Why: wild; user wants every doc readable in full on the page. A ceiling forces rewrites to compress, and a rewrite shorter than its parent at equal score wins ties.
  Done when: lint fails any generation file over 200 lines.

- **Carry-over is the previous tower's winning file, copied** — FEATURE — value 3 — effort S — risk low — category: carry-over
  Why: spec wants carried defaults; the simplest form is `cp` of the last winning Seed as the starting template for the next project, flagged "borrowed".
  Done when: a new project's gen-1 seed begins from the prior winner and its first line says where it came from.

Next question: Which stages could be removed entirely without lowering the number of exam scenarios closed?
Next question: What is the smallest tower (stages and files) that still passes the held-out exam on a fixture project?

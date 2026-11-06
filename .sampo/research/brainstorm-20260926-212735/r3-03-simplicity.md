# Brainstorm — lens: simplicity

- **Dedupe ideas between brainstorm rounds mechanically** — PERFORMANCE — value 4 — effort S — risk low
  Why: the pack's own list repeats itself: thrash detection appears 4 times, the handoff digest 3 times. Each round re-pays for near-duplicates.
  Done when: `fm ideas` runs a BM25/token-overlap pass before each round (reusing the recall index), drops candidates over a threshold against earlier titles, and a test feeding the pack's list shows the thrash and handoff duplicates collapsed.

- **Cluster ideas into themed tasks before implementing** — FEATURE — value 4 — effort M — risk med
  Why: the user said "fully implement all ideas", and there are about 55 overlapping ones. Implementing them one by one would repeat work and inflate the code.
  Done when: `fm ideas --converge` groups ideas by similarity into ≤10 briefs, each listing its member ideas and a single acceptance set, and the queue receives clusters, not raw ideas.

- **Make `fm` output terse by default** — PERFORMANCE — value 4 — effort S — risk low
  Why: every command's stdout lands in model context. Assumption: `fm check`, `fm map` and `fm status` print full tables on success.
  Done when: success prints ≤3 lines, failures print only the failing items, `--verbose` restores the full output, and a test asserts byte caps per command.

- **Keep all numeric limits in one table** — CLEAN — value 3 — effort S — risk low
  Why: the constraints cite 6,000, 2,000, 400, 150 ms and 30 ms. Assumption: they are scattered across code, doctor and tests.
  Done when: a single `limits` module is imported by hooks, `fm doctor` and tests, and grepping for the literals outside it finds none.

- **Require a net-complexity line on FEATURE tasks** — CLEAN — value 3 — effort M — risk med
  Why: about 8,000 lines and a growing command list, with every round adding more, and nothing pushes back on growth.
  Done when: `fm task done` for FEATURE prints net lines and command count against the focus baseline, and requires "Removes/merges: …" or "none: reason" in the brief.

- **Compact old briefs into one-line records** — PERFORMANCE — value 3 — effort M — risk med
  Why: recall runs BM25 over all past briefs, so the corpus, the index time and the "Related" noise grow without bound.
  Done when: `fm tidy` rewrites finished briefs older than N days into a title, outcome, files and lesson record, recall still finds them by lesson, and state size drops on a fixture.

- **Omit empty brief sections** — CLEAN — value 2 — effort S — risk low
  Why: briefs are re-read at every focus, resume and `fm run`. Assumption: the template carries empty Evidence, Audits and Related headings.
  Done when: a fresh S brief renders with only non-empty sections and its byte size is ≥30% smaller, with all existing gates still passing.

# Brainstorm — lens: simplicity

- **Make each failed gate print its own fix command** — CLEAN — value 4 — effort M — risk low
  Why: `fm task done` and `fm focus` enforce many gates (evidence, audits, Docs impact, lesson, red→green), and rule and skill text repeats them. A gate table (name, check, one-line remedy) would let the error be the documentation and cut retry turns.
  Done when: every gate refusal ends with a copy-pasteable `fm ...` command, and a test iterates the gate table to assert each entry has a remedy.

- **Fold playbooks into the recall index** — CLEAN — value 4 — effort M — risk med
  Why: there are 40 playbooks with their own skill, while recall already runs BM25 over briefs, lessons, decisions and research. Indexing playbooks and writing a single "Related" block at focus replaces two retrieval paths and the long playbook list.
  Done when: `fm focus` on a task shows the top matching playbook in "Related", the playbooks skill's listing is gone, and its size drops by more than half.

- **Run all hooks through one `fm hook <event>` dispatcher** — PERFORMANCE — value 3 — effort M — risk med
  Why: hook latency is ~30 ms p50 with a p95 fail line at 150 ms. Assumption: each hook currently starts its own Python process and re-imports shared modules. One entry point with lazy per-event imports removes duplicated startup and duplicated glue.
  Done when: a benchmark shows p95 for PreToolUse at or below the current p50 plus 10 ms, and hooks.json has one command shape.

- **Merge the inbox into the queue as an "unrefined" status** — CLEAN — value 3 — effort M — risk med
  Why: SessionStart, the intake parser and the queue order each treat inbox and queue as separate lists, and both use the 2,000-char budget. One list with a status field removes a state concept and a code path.
  Done when: no `inbox` directory or command remains, old inbox files migrate on first run, and the SessionStart text shows one queue line.

- **Collapse housekeeping commands into `fm doctor` subchecks** — CLEAN — value 3 — effort S — risk low
  Why: `tidy`, `doctor`, `repeats`, `docs` and `sync` overlap as "state looks wrong, fix it" chores, and each needs its own skill and description text. Keep the old names as thin aliases, and one skill covers them.
  Done when: `fm doctor --fix` runs all of them, and the tidy and doctor skills merge into one file.

- **Report unreferenced code in `fm doctor`** — CLEAN — value 3 — effort S — risk low
  Why: plugin/lib is ~8,000 lines and has grown by accretion, with features added and later pruned by usage log. An `ast` pass (stdlib) that lists functions and constants with no callers finds dead code, and dead code is what keeps this size from shrinking.
  Done when: `fm doctor` lists defined-but-unreferenced names, the first run's findings are deleted, and the tests still pass.

- **Share one renderer between `fm watch`, `fm serve` and the digest** — CLEAN — value 2 — effort M — risk low
  Why: the terminal dashboard and the HTTP server both format task, queue and cost state, and the weekly digest idea needs a third view. A single "state → rows" function with text and HTML backends avoids three copies drifting apart.
  Done when: watch, serve and the digest import the same row builder, and a test compares the text and HTML outputs for one fixture state.

# Brainstorm — lens: self-improving harness

- **Exclude synthetic sessions from every learner** — FIX — value 5 — effort S — risk low — category: learning hygiene
  Why: the pack shows harness noise leaking in ("Use an Explore subagent…" from the Haiku demo prompt, the shot.py session driven by the Stop hook). The correction miner, fixes store and taste profile all read transcripts, so they would learn from it.
  Done when: a session started by shot.py, the demo recorder or `claude -p` children carries a `provenance=synthetic` tag, and a test shows its corrections and obstacles never reach `fm learn`, the fixes store or the taste profile.

- **Credit-assign each failure to the injected context** — FEATURE — value 4 — effort M — risk med — category: credit assignment
  Why: assumption: fixes, cards, rules and lessons are all injected, but only "hit rate" is scored. When a session goes wrong nobody knows which injected item misled it, and 6 of 1,084 cards ever fired.
  Done when: `fm blame <session>` re-runs the divergence turn with each injected item removed in turn (cheap model, capped) and prints the item whose removal changes the outcome, or "none".

- **Detect hints the model ignored and whether it mattered** — FEATURE — value 4 — effort S — risk low — category: hint precision
  Why: assumption: fixes are scored by "worked or not", but the ledger can also show the model taking a different path and still succeeding. That is a false positive, and it costs tokens on every fire.
  Done when: for each injected fix, the ledger records followed / ignored-and-fine / ignored-and-failed. A fix with 3 ignored-and-fine outcomes is flagged as a retire candidate in the weekly report.

- **Mine golden paths from first-time passes** — FEATURE — value 4 — effort M — risk low — category: success learning
  Why: all the learning in the pack comes from failures and corrections. Tasks that closed first time on the first attempt are an unused signal.
  Done when: per task class (FIX/CLEAN/FEATURE), `fm learn paths` prints the most common ordered tool/step sequence among first-time passes. A PostToolUse nudge fires once when a live task skips its first step (e.g. reading the failing test before editing).

- **Turn each fixed bug into a bug-class invariant** — CLEAN — value 4 — effort M — risk med — category: structural prevention
  Why: T-0990, T-1001, T-1003, T-1007 and T-1013 are a chain of "the test reached the paid binary / the harness hit the real hook" gaps, each fixed by one more test. Nobody asked what rule would make the class impossible.
  Done when: closing a FIX task with `--class <slug>` stores a grep/AST check in `plugin/lib/invariants/`. `fm doctor` runs them, and the first one ("no test may resolve the real `claude`") fails on a deliberately planted violation.

- **Pre-register every self-change with a predicted movement** — FEATURE — value 4 — effort S — risk low — category: self-measurement
  Why: assumption: Foreman changes its own rules, hints and prompts without recording what it expects to happen, so "did it get better" is judged after the fact and Goodhart-prone.
  Done when: `fm rule add` and the hint promoter require `--expect "interventions/task -10%"`. After N sessions a verdict line is written, and the weekly report shows the harness's hit rate on its own predictions.

- **Weight brainstorm lenses by 30-day survival** — FEATURE — value 4 — effort S — risk low — category: brainstorm yield
  Why: the pack has hundreds of ideas and about 30 deferred "Later from…" rollups. Today's rates count ideas accepted, not features still in use 30 days later, and the unused-features report already exists.
  Done when: `fm ideas` reads each lens's share of shipped ideas whose usage counter is non-zero after 30 days and orders lenses by it. The weights print in the run header.

- **Type-check the brain for contradictions** — FEATURE — value 3 — effort S — risk low — category: consistency
  Why: rules, fixes, lessons, cards and CLAUDE.md are written by different learners, and the pack mentions "contradictory steers" only for steers. Sharing the brain through git makes merged contradictions more likely.
  Done when: `fm doctor` flags pairs where one item says "always/prefer X" and another says "never/avoid X" over the same command or path glob. A fixture with a planted pair is caught and a clean brain stays quiet.

- **Shrink each hint to its minimum effective dose** — PERFORMANCE — value 3 — effort M — risk low — category: token cost
  Why: assumption: injected hints grow wordy over time and each fire costs tokens on every matching turn.
  Done when: `fm fixes golf` drops one sentence at a time from a hint, replays its recorded scenario on a cheap model, and keeps the shortest wording that still reproduces the fix. The report shows total tokens saved.

- **Keep a per-model tic atlas** — FEATURE — value 4 — effort M — risk med — category: model behaviour — wild
  Why: the Haiku probe T-0978 found small-model gaps (wrong test runner, for-loop waits, unknown task ids). The rules that fix them are probably dead weight on bigger models.
  Done when: the ledger stores each recurring misbehaviour keyed by model id with its count. Hooks inject the matching nudge only when that model is running, and an entry expires after 14 days without a sighting. `fm tics` lists the table.

- **Run a frozen elder brain as a drift detector** — FEATURE — value 3 — effort M — risk med — category: drift detection — wild
  Why: assumption: a long-learning brain can slowly pick up bad habits without any single change looking wrong.
  Done when: each night a snapshot of the brain from 30 days ago is replayed against the last week's recorded guard/gate decisions. The disagreement rate is charted, and a spike prints the three items that changed the most decisions.

- **Adopt rule amendments by lazy consensus** — FEATURE — value 3 — effort S — risk med — category: governance — wild
  Why: the pack shows deferred proposals piling up (T-0787 to T-0866 are "Later" rollups) because each needs a user decision. A veto window keeps the user in control without asking each time.
  Done when: a proposed amendment with a passing replay is posted to the digest with a 7-day timer. It auto-enables after 7 days unless the user vetoes, a veto records a precedent, and `fm rule revert <id>` undoes it in one command.

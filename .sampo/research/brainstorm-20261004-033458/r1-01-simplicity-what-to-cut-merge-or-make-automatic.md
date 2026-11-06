# Brainstorm — lens: simplicity: what to cut, merge or make automatic

- **Auto-retire commands by measured use** — CLEAN — value 4 — effort M — risk low — category: pruning
  Why: ~20 modules and dozens of verbs shipped in days; "sunset lifecycle" and "complexity ledger" were floated but nothing counts invocations. Assumption: the ledger already records fm verb calls.
  Done when: `fm friction` lists verbs with zero calls in 30 days plus the one that supersedes each, and a fixture verb with no calls is flagged.

- **Fold the four review verbs into one default `fm review`** — CLEAN — value 4 — effort M — risk med — category: merge
  Why: `fm audit`, `fm second plan|debate|session`, installed review skills per lens and the reviewer subagent overlap, and every batch still waits 1–2 min on one. Assumption: the shared core is "diff + lens + seat".
  Done when: `fm review ID` picks seats and lenses from tier and diff risk, the old verbs remain as aliases, and a test shows the same findings file for both paths.

- **Derive the tier from the diff footprint at brief time** — FEATURE — value 4 — effort S — risk low — category: automation
  Why: S tasks spreading past two files already trigger "re-tier"; the user is asked something Foreman can compute. Assumption: the impact map gives files and fan-out before edits.
  Done when: `fm task new` proposes a tier from map output, and a request touching three files proposes M without a prompt.

- **Make the rules file self-trimming** — PERFORMANCE — value 3 — effort M — risk med — category: context
  Why: the always-on file is capped at 120 lines / 6000 chars, so it is already near the ceiling. Hooks log which hints fired, so a rule with no firing in N sessions can be proposed for removal. Assumption: firing is attributable to a rule.
  Done when: `fm evolve` offers a deletion for a rule that never fired, and the bench gate must pass before it is applied.

- **Put every pre-audit and guard pattern in one data table** — CLEAN — value 3 — effort S — risk low — category: merge
  Why: the pre-audit's patterns match their own regex source, and the guard's git channels were already proposed as a table. One table with an `exempt_self` flag fixes the false positive and halves the code.
  Done when: the file defining the patterns is no longer flagged, and a test verifies guard and pre-audit read the same table.

- **Auto-close trivial steps without ceremony** — FEATURE — value 3 — effort M — risk med — category: automation
  Why: reviews find 3–8 issues per batch, but docs-only and rename briefs gain little from the same pipeline. Assumption: a no-code-path diff can be classified safely.
  Done when: a docs-only brief closes with one gate run and no reviewer spawn, and the proof pack says why.

- **Wild: Run Foreman in "one verb" mode** — FEATURE — value 4 — effort L — risk med — category: interface
  Why: with ~40 verbs, `fm` alone could print the single next action and run it when the user agrees. Wild.
  Done when: bare `fm` in a fixture repo with a pending brief runs `fm next` and offers a yes-to-execute.

- **Wild: Delete-by-default for new features** — CLEAN — value 3 — effort M — risk low — category: governance
  Why: every pass adds a feature. Each new verb ships with a 60-day expiry that auto-removes it from `--help` unless used. Wild.
  Done when: a fixture verb past its expiry with no use disappears from `--help` yet still runs.

- **Wild: Make the inbox self-expire into a graveyard** — CLEAN — value 3 — effort S — risk low — category: pruning
  Why: seven open items such as MCP server, night shift and stranger test have waited several passes. An item untouched for three passes moves to a read-only graveyard with the reason. Wild.
  Done when: an item untouched for three passes shows up in the graveyard file rather than the open list.

- **Merge `fm bench duel|versions|court|soak` into `fm bench --vs`** — CLEAN — value 3 — effort M — risk low — category: merge
  Why: four sibling verbs from one pass share setup (replay, judge, budget). Assumption: they share the replay runner.
  Done when: `fm bench --vs plugin|rev|steers|user` reproduces each old result and the old verbs print a one-line redirect.

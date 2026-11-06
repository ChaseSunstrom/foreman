# Brainstorm — lens: blind spots

Each of these comes from a class the missed asks share. Where possible I name the question that should have caught it.

- T-2651: a number was recorded but nothing could fail on it. Question: which recorded values have no consumer that can exit nonzero?
- T-2655 and T-2653: output printed on one path of several. Question: which printed lines exist on only one exit path or one surface?
- T-2657: a count with no rate. Question: which counters lack a denominator?

- **Audit every verb's help promise against its exit code** — FIX — value 4 — effort M — risk low — category: CLI honesty
  Why: `--bench` was documented as measuring but could never fail (T-2651). Assumption: other help strings say "fails", "refuses" or "blocks" without a test behind them.
  Done when: a test greps each verb's help for obligation words, triggers each case, and asserts the nonzero exit. Any unmatched promise is listed.

- **Build a flag-parity matrix across sibling verbs** — FEATURE — value 4 — effort M — risk low — category: CLI ergonomics
  Why: `--under` landed on `task evidence` only. Question: which sibling verbs take the same kind of input but lack the flag? Assumption: `--json`, `--since`, `--project` and `--under` are unevenly spread.
  Done when: `fm doctor` prints a verb × flag grid for the shared flag set. Each hole is either marked n/a with a reason or filed as a task.

- **Add `--fail-if EXPR` to every number-printing reader** — FEATURE — value 3 — effort M — risk low — category: gates
  Why: Readers like `fm outcomes`, `fm digest` and the cost verbs print figures and always exit 0. Only `--bench` got a threshold, and only after the user asked.
  Done when: `fm outcomes --fail-if 'held<0.8'` exits 1 with a one-line reason. A malformed expression is a usage error, not a pass.

- **Report yield per quota window as well as per dollar** — FEATURE — value 3 — effort S — risk low — category: spend
  Why: The receipt prints no ratio on zero spend (T-2655). Assumption: subscription users always see zero dollars, so the new line says nothing to them.
  Done when: the drive receipt shows tasks per usage-window percent when dollars are zero, and the new test covers that case.

- **Extend the flake registry to every nondeterministic check** — FEATURE — value 3 — effort M — risk low — category: measurement
  Why: Per-test rates exist (T-2657). Bench medians, cold-read verdicts and the exam arms flip too, with no rate shown. Assumption: Haiku/Sonnet cold-read disagreement is already recorded somewhere.
  Done when: `fm doctor` lists the three least stable checks of any kind, each with fails over runs.

- **Put the Next command in `--json` error output** — FEATURE — value 3 — effort S — risk low — category: CLI contract
  Why: T-2653 added a `Next:` line to text exits, so scripted callers don't get it.
  Done when: every nonzero `--json` exit emits `{"error":…, "next":…}` and a test walks the verbs that support `--json`.

- **Run every verb with a closed stdout, a SIGPIPE and a full disk** — FIX — value 3 — effort M — risk low — category: robustness
  Why: Assumption: `fm … | head` gives a BrokenPipe traceback somewhere. The end-of-run receipt was already found on one path only.
  Done when: a matrix test pipes each verb to a closed reader and requires a clean exit with no traceback.

- **Test that every receipt field appears on every surface** — CLEAN — value 3 — effort M — risk low — category: ui parity
  Why: The UI is a thin area. T-2655 showed the receipt gaining a field in one place at a time. Assumption: web UI, pane and site render hand-picked subsets.
  Done when: one receipt schema is the only source, and a test fails when a field is absent from the CLI, web UI or pane renderer.

- **Generate a default web view from any verb's `--json` schema** — FEATURE — value 4 — effort L — risk med — category: ui
  Why: Each web screen is hand-built, so new verbs (restore drill, flake list) never reach the UI. Assumption: most verbs already emit stable JSON.
  Done when: a verb with a `--json` schema and no custom view appears in the web UI as a titled table with empty and error states.

- **Record every decision not taken, with a reason** — FEATURE — value 3 — effort M — risk med — category: negative ledger
  Why: This answers the open question about holds, skips and abstentions that leave no record. Assumption: `fm next` skips, round-first holds and drive pace drops currently leave no trace.
  Done when: `fm digest` shows "held N, skipped M" with the top reasons, and removing a hold class fails a test.

- **Wild: mutate exit codes and see whether any test notices** — SECURITY — value 3 — effort M — risk low — category: test quality
  Why: wild. Flip each `sys.exit(1)` to 0 and each `raise` to a return, one at a time, in a scratch copy. Survivors are verbs whose failure path nothing tests.
  Done when: the nightly job lists the surviving mutants and files one task per verb.

- **Wild: mine the user's own words for verbs that don't exist** — FEATURE — value 3 — effort S — risk low — category: ghost verbs
  Why: wild. The asks use "tombstone", "dry-run", "receipt" and "restore". The words they reach for first should resolve to something. Assumption: a few appear in asks but not in the verb table.
  Done when: the top ten unresolved nouns from the last 200 asks each become an alias or a did-you-mean entry, and typing one prints the real verb.

- **Wild: a red-team agent hunts for exit paths that break a verb's promise** — FEATURE — value 3 — effort L — risk med — category: agents
  Why: wild. A specialist sub-agent reads one verb's help and code and tries to find a path (timeout, partial input, kill) where the promise breaks. A second checks each finding with a reproducing command.
  Done when: each reported break is a failing command that exits 0, and unreproduced findings are discarded.

Next question: for each "Foreman reports X" claim, what does Foreman do when X is unmeasurable on this host (no dollars, no display, no `claude`), and does the user see that as a gap or as a quiet zero?
Next question: which of the user's repeated verification habits (re-running a command, opening a file) show that a printed result wasn't trusted?

# Brainstorm — lens: simplicity

- **Replace the 61-cell grid with one lean line per surface** — CLEAN — value 4 — effort S — risk low — category: lean
  Why: the grid's 61 empty cells are the same eight stages across eight surfaces, and the standing rule says a templated cell doesn't count. Eight lines (hook ms, bytes injected, guard deny count, "unmeasured" where true) each name a command that produced them.
  Done when: `fm genesis sweep` reads eight surface lines, each citing the command that made its numbers, and passes coverage with no cell phrase reused.

- **Pay for every new verb with a deletion in the same task** — CLEAN — value 5 — effort S — risk low — category: ratchet
  Why: gen-0 §6 says each generation removes at least as much as it adds, yet the pack shows 28 "Later from T-07xx" bundles and verbs growing. `fm task finish` currently doesn't enforce subtraction.
  Done when: finishing a task whose diff adds a verb fails unless it also removes, merges or marks as retired a verb, naming which.

- **Collapse the 28 deferred "Later from T-07xx" bundles into one dated parking file** — CLEAN — value 3 — effort S — risk low — category: queue
  Why: T-0788 through T-0869 are bundles of 7–29 ideas each, deferred, never opened. Each is a task row costing `fm next` and status attention.
  Done when: `fm next` lists none of them, and one file holds each idea with its blocker or reopen condition. No idea is lost, in line with the "no idea is killed" rule.

- **Cold-shelve the 1214 unused stack cards** — PERFORMANCE — value 3 — effort S — risk low — category: library
  Why: `fm lib stats` shows 5 of 1219 cards used. Dropping the 8-dep card idea shows the same instinct.
  Done when: cards unloaded in 90 days sit in a cold index, `fm lib show NAME` still finds them, and install size and map time fall (measured).

- **Send the SessionStart note once, then only a hash and delta** — PERFORMANCE — value 5 — effort M — risk med — category: context
  Why: the note is ~2k chars × 89 sessions measured, and context averages 387k per reply. Only the delta is new information.
  Done when: the second turn's injected bytes fall to under a quarter, with a test that the standing rules are never truncated.

- **Fix the two brief-guard false positives with a shell tokenizer** — FIX — value 4 — effort S — risk low — category: guard
  Why: a dict key and a `.join(` call were read as written paths. A real tokenizer replaces the pattern guess.
  Done when: both cases are fixtures that pass, and the guard corpus still blocks every previously blocked command.

- **Make bare `fm doctor` print one lean line** — FEATURE — value 3 — effort S — risk low — category: legibility
  Why: hook p95 278 ms, context 387k, and cards 5/1219 are scattered across `fm friction`, `fm cost` and `fm lib stats`. One line is checkable at a glance.
  Done when: `fm doctor` ends with `lean: hooks p95 278ms · ctx 387k · verbs N · cards 5/1219` and each figure's command is named in `--verbose`.

- **Show pending lean growth as "unmeasured", never as a green** — FIX — value 3 — effort S — risk low — category: honesty
  Why: T-2503 makes unmeasured growth pending. A placeholder cell reads as proof, which breaks the proof-before-presentation rule.
  Done when: the sweep prints "unmeasured" for any lean row with no producing command, and a test fails on a numeric cell with none.

- **Wild: One-file Foreman** — FEATURE — value 3 — effort L — risk med — category: bold
  Why: wild. A single-file `fm-lite` with only plan, prove, guard and next; every other verb is an optional add-on. It's the honest test of what the discipline layer needs. Assumption: most of the 2098 files serve few sessions.
  Done when: `fm-lite` passes the guard corpus and the roundtrip e2e on a machine with no `claude` on PATH, in under 1,000 lines.

- **Wild: Delete-a-feature Friday** — CLEAN — value 4 — effort M — risk med — category: subtraction
  Why: wild. Weekly, the least-used verb is switched off in a scratch copy and the suite and a Haiku smoke run are checked. If nothing notices, a one-command removal card is filed for the user's yes.
  Done when: the first run names a verb, shows the scratch result, and files a removal card, with nothing deleted unasked.

- **Wild: Withhold one injected block per session and compare outcomes** — PERFORMANCE — value 4 — effort M — risk med — category: context
  Why: wild. Context is 387k per reply but no block has a measured benefit. Randomly dropping one block, then comparing first-time pass, tells which earns its bytes.
  Done when: after N sessions, a table lists each block's byte cost against pass-rate delta, and one block is trimmed on the evidence.

- **Run the exam once with every optional hook off** — PERFORMANCE — value 3 — effort M — risk low — category: measurement
  Why: the standing rule defers the full exam, but a free-arm ablation costs nothing. If the score doesn't move, the hook is weight.
  Done when: a scorecard line shows the zero-token arms with and without optional hooks, and names any hook that didn't change a result.

- **Pick the lean cell wording from a single budget file** — CLEAN — value 2 — effort S — risk low — category: docs
  Why: every cell currently cites its own number, inviting the templated phrasing the steer forbids. One `lean-budget` file is the single source.
  Done when: each lean cell links a key in that file, and editing a number changes it in every place.

Next question: Which of the 2098 files and 1388 skills has no session path, verb call or test reaching it, so it could be moved to a cold shelf?
Next question: If the user had to run Foreman for a month on a laptop with 1 GB free and no network, which hook or surface would they feel first?

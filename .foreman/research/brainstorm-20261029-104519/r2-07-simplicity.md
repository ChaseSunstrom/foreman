# Brainstorm — lens: simplicity

- **Delete the three unverified adapters** — CLEAN — value 4 — effort S — risk low — category: surface area
  Why: T-0335, T-0336, T-0337 are all blocked on Codex, Gemini and opencode, none live-verified. Each adapter is carrying maintenance weight and test time for a surface nobody has confirmed works. (Earlier "mark experimental" leaves the code in place; remove it, keep it in git history.)
  Done when: no Codex/Gemini/opencode code path remains in `plugin/lib`, `fm doctor` passes, and the blocked tasks are closed as "removed".

- **Cap the gate list at a fixed number** — CLEAN — value 4 — effort M — risk med — category: gates
  Why: Recent commits show gates accreting (docs-impact, core-integrity, scope, behaviour lock, why-not-caught, ambient run, full check). Each fix spawns sibling gaps. assumption: some gates overlap heavily.
  Done when: a test fails if the registered gate count exceeds N, and adding one requires removing or merging another.

- **Collapse "ambient run", "fm check" and "fm ship" test launching into one function** — CLEAN — value 5 — effort M — risk med — category: test runner
  Why: T-1967, T-1974, T-1980, T-1984/1987 are all "two suites at once" patches across fmambient, fm check and fm ship. One launcher with one lock makes the class impossible.
  Done when: grep finds a single call site that spawns the test suite, and a stress test starting three triggers concurrently shows one running suite.

- **Merge `-k` and name filters into one documented selector** — CLEAN — value 3 — effort S — risk low — category: test runner
  Why: T-1994, T-1996, T-2001-era work kept adding rules (union, then AND, then did-you-mean). Accept one syntax (`module::Class::test`, case-insensitive substring) and drop the two-mode behaviour.
  Done when: `run.py` has a single selector grammar, and the "no test matches" message is produced by one code path.

- **Make `fm do` the single newcomer command** — FEATURE — value 4 — effort M — risk med — category: onboarding (wild)
  Why: T-0862 and T-0863 defer a tour and a start ladder because the surface is too large. One verb that plans, edits, proves and closes hides the rest. assumption: the existing commands can be chained without new logic.
  Done when: in a fresh repo, `fm do "fix X"` goes from request to a closed task with proof and a receipt, with no other fm command typed.

- **Fold the 17 "Later from T-07xx/T-08xx" items into one parked file** — CLEAN — value 3 — effort S — risk low — category: backlog
  Why: about 25 deferred FEATURE items clutter every queue view and are re-read each round. They never get picked up.
  Done when: `fm` open-work output shows only live items, and the parked list is one file that fm loads only on request.

- **Replace cleverness in captured-title shaping with "first line verbatim, hard wrap"** — CLEAN — value 2 — effort S — risk low — category: intake
  Why: T-1985 and T-1989 added word-boundary cuts, case preservation and @path scoping rules, each fixing a prior heuristic. A verbatim title plus a separate short slug has fewer failure modes.
  Done when: parse_intake has no case or truncation heuristics, and a property test shows the original text is recoverable from the task.

- **Make every error end in one next command** — FIX — value 4 — effort M — risk low — category: messages
  Why: T-1995, T-1996, T-2001 and the dropped-hint fixes each added a suggestion to one message. One shared `refuse(reason, next_cmd)` helper removes that per-message work.
  Done when: a test greps all refusal sites and fails any that don't go through the helper.

- **Wild: Remove the pane and the web UI from the default install** — CLEAN — value 3 — effort M — risk med — category: surface area (wild)
  Why: T-0166, T-0418, T-1217 show the foreman-ui mod is a maintenance sink. The default install would be hooks plus CLI only, with the UIs opt-in.
  Done when: a default install registers no UI code, and the core check suite passes without UI fixtures.

- **Wild: A "this file is why we can't delete X" report** — FEATURE — value 3 — effort M — risk low — category: dependency map (wild)
  Why: deleting is hard because nobody sees what depends on a feature. A report lists every caller, test and doc of a command, so removal becomes a mechanical task.
  Done when: `fm why-keep <command>` lists its callers, tests and docs, and exits non-zero if none exist.

- **Wild: Give each command a 90-day use counter and auto-propose its deletion** — FEATURE — value 4 — effort M — risk med — category: usage telemetry (wild)
  Why: no data shows which of the many commands and skills get used. Local-only counters turn removal from opinion into a queue.
  Done when: after 90 days of local use, `fm prune` lists the unused commands with zero recorded calls, and nothing leaves the machine.

- **Keep one source of truth for "what is the next step"** — CLEAN — value 3 — effort M — risk med — category: state
  Why: the stage rail, `fm doctor`, the loop brief and the pane each compute progress. Recent fixes (T-1998 doctor warning inside the task's own scope, T-1968 other tasks' files) are all disagreements between them.
  Done when: all four read a single `next_step()` function, and a test asserts they agree on a fixture session.

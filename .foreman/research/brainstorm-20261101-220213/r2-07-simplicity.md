# Brainstorm — lens: simplicity

- **Replace the 61-cell grid with one lean line per surface** — CLEAN — value 4 — effort S — risk low — category: coverage
  Why: the request is to fill 61 empty cells of #12, yet the steers demand real, non-templated cells and gen-0 §6 says subtract as you add. Templated filler is the failure to avoid. Eight surfaces × eight stages is mostly one answer ("the hook budget holds"). One line per surface (cites the file and the measure) plus recorded n/a for cells that cannot differ.
  Done when: `fm genesis sweep` coverage passes for #12 with every non-n/a cell naming a distinct file or verb and no phrase repeated across rows.

- **Inject the SessionStart note once, then only a delta** — PERFORMANCE — value 4 — effort M — risk low — category: context
  Why: pack shows a ~2k-char note ×89 sessions, and context per reply averaging 387k. Simplest cut is hash the note and send only what changed.
  Done when: a second SessionStart in the same repo with unchanged state injects under 300 chars, asserted by a test.

- **Retire unused stack cards to a cold shelf** — CLEAN — value 4 — effort S — risk low — category: library
  Why: `fm lib stats` shows 5 of 1219 cards used; the user dropped an unmeasured-card task as unjustified growth. Move cards unused for 90 days to a cold index, loaded only on explicit `fm lib show`.
  Done when: the default card listing and the installed tree shrink by 90%+ and `fm lib show NAME` still resolves a cold card.

- **One lean line in `fm doctor`** — FEATURE — value 3 — effort S — risk low — category: observability
  Why: hook p95 (278 ms), context per reply, verb count and dependency count live in different commands; the lean row is hard to watch. A single line with each against last generation makes the ratchet visible without a new subsystem.
  Done when: `fm doctor` prints one line with p95, injected bytes, verb count and deltas, and a test checks all four fields.

- **Fix the brief-guard path false positives** — FIX — value 4 — effort S — risk low — category: guard
  Why: 2 false positives read a dict key and a `.join(` call as written paths. Each false block costs a retry and teaches the user to distrust the guard.
  Done when: both strings from the log pass a regression test, and the guard corpus still blocks every known-bad path case.

- **Require a deletion with every new verb** — CLEAN — value 3 — effort M — risk med — category: lean
  Why: gen-0 §6 says each generation removes at least as much as it adds, but only `fm burden --by-verb` reports it afterwards. A check at `fm task finish` that a new verb names the verb or card it replaces is the cheapest enforcement.
  Done when: finishing a task that adds a verb without a named retirement or a recorded exemption is refused, with a test.

- **Collapse the 28 "Later from T-07xx" bundles** — CLEAN — value 3 — effort S — risk low — category: backlog
  Why: the open list is dominated by deferred bundles (T-0788…T-0869) that no session path touches. Merge into one parked file with a re-open condition each, instead of 28 rows read every `fm next`.
  Done when: the open queue shows one parked-bundle entry and `fm next` output shrinks accordingly; no idea is deleted (the no-kill steer holds).

- **Say "unmeasured" instead of a placeholder in every lean cell** — FIX — value 3 — effort S — risk low — category: honesty
  Why: the steer "lean substance" says growth without a measurement is pending, not red. Cells for the headless/server and MCP surfaces have no measure today; a recorded "pending: no probe" is truer than a templated claim.
  Done when: the sweep lists pending cells separately from filled ones and neither is counted as covered.

- **Cap each hook's context at one shared budget** — PERFORMANCE — value 3 — effort M — risk med — category: hooks
  Why: p95 is fine now, but each new capability adds its own injection. One byte budget per event, with eviction, stops growth by construction instead of by review.
  Done when: a test adds an oversize injection and the event total stays under the cap with the lowest-priority block dropped, never a standing rule.

- **Wild: One-file Foreman trial** — FEATURE — value 3 — effort L — risk med — category: lean
  Why: assumption: a minimal profile (guard + task loop only) would show what the other hooks earn. Run the exam with everything optional off.
  Done when: a documented profile runs the smoke scenarios and the report compares its pass rate and cost with the full set.

- **Wild: Delete-a-feature Friday** — FEATURE — value 3 — effort S — risk low — category: lean
  Why: wild: a weekly lane proposes removing the least-used verb in a scratch copy, runs the suite, and files the result as a one-yes card. Nothing is removed without that yes.
  Done when: the lane produces one card per week naming the verb, its use count and the suite result in the copy.

- **Wild: Weigh the repo on the way out** — FEATURE — value 2 — effort S — risk low — category: lean
  Why: wild: `fm eject --dry-run` installs, then removes Foreman in a scratch copy and diffs the tree, proving "leaves no trace" with a number.
  Done when: the dry run reports zero residual files outside a listed allowance, as a test.

- **Print the guard's block reason with the safe alternative** — FEATURE — value 3 — effort S — risk low — category: guard
  Why: `core:interpreter-code-driving-foreman` blocked 42× in 7 days; each repeat is a lost turn. A one-line "use `fm X` instead" shortens the retry without loosening anything.
  Done when: that block message includes the replacement command, and the repeat count in `fm friction` falls over the next week.

Next question: Which of the 61 cells share one honest answer because the surface can't differ, and can they be recorded as n/a with a reason rather than filled?
Next question: What does Foreman cost the user on the surfaces with no hooks (MCP, headless), and is there any probe for it at all?

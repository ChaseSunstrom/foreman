# Brainstorm — lens: user value

Most of what's left is marginal. These six are the ones that would still change outcomes for the user.

- **Add `fm completeness`, an archetype gap check for "fully featured"** — FEATURE — value 4 — effort M — risk low
  Why: the "fully featured" trigger currently rests on LLM lenses. Nothing checks table-stakes items deterministically for a CLI, library, web service or plugin. Assumption: `fm map` can name the archetype.
  Done when: on a fixture CLI with no `--help`, no exit-code contract, no LICENSE or no changelog, `fm completeness` lists each gap with file evidence, uses zero model tokens, and feeds those gaps into the super-brainstorm pack.

- **Reconcile idea sets before queueing them** — CLEAN — value 4 — effort M — risk med
  Why: about 275 ideas already contradict each other (add gates vs. throttle gates, merge tiers vs. ratchet tiers, more notes vs. fewer notes). Dedupe and clustering don't resolve conflicts. Implementing all of them would quietly bloat Foreman.
  Done when: `fm ideas --reconcile` on a fixture containing a known conflicting pair and a known subsuming pair outputs keep/drop/merge decisions with one-line reasons, and dropped ideas never reach the queue.

- **Tag each acceptance criterion as asked or inferred** — FEATURE — value 3 — effort S — risk low
  Why: the expand step adds criteria the user never wrote, and each one costs verification tokens. The pack's existing trace runs from request to evidence, not from criterion back to the request. Assumption: over-expansion is a real cost.
  Done when: the brief lists an origin per criterion; a "lean" profile drops inferred criteria on S tasks; and `fm task done` reports how many inferred criteria were checked.

- **Add a fresh-context consult when stuck** — FEATURE — value 3 — effort M — risk low
  Why: thrash detection forces a hypothesis, but the same polluted context tends to produce the same wrong one. A tool-less `claude -p` shown only the minimal failure, the relevant function and the ruled-out list is cheap. Assumption: the extra call costs less than continued thrashing.
  Done when: on the third same-failure thrash, one consult call runs with a capped pack under N chars, its answer is logged, and it fires at most once per task.

- **Show just-in-time feature hints, once per feature** — FEATURE — value 3 — effort S — risk low
  Why: the user never runs commands, so new capabilities like `fm undo`, `fm pr` and `fm prove` stay invisible. The usage ledger only prunes them.
  Done when: a matching moment (e.g. "undo that") adds one ≤120-char hint, the same hint never repeats, hints stop after the feature is used, and total hint text per week is capped.

- **Audit Foreman against Claude Code built-ins and retire duplicates** — CLEAN — value 3 — effort M — risk med
  Why: Foreman's checkpoints, resume notes, lessons and plan steps may overlap with native rewind, memory and todo features. Duplicated context costs tokens every session. Assumption: some overlap exists; the pack doesn't show which.
  Done when: `fm doctor` lists each Foreman mechanism with its native counterpart (if any) and the injected chars it costs, and at least one confirmed duplicate is removed with the suite still green.

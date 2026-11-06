# Brainstorm — lens: simplicity

- **Cap the goal at one file with six fields** — CLEAN — value 5 — effort M — risk med — category: goal ledger
  Why: the pack lists about 300 goal ideas, and many name their own extra file or object (baton, card, contract, cut list, ruleset, warranty). Assumption: most are views of the same six facts: contents, done-when commands, cuts, steers, stop cause and next step.
  Done when: `fm goal` state is one file, every other surface is rendered from it, and a test fails if any goal feature writes a second file.

- **Make bare `fm goal` do the next right thing** — FEATURE — value 4 — effort S — risk low — category: CLI
  Why: assumption: the ideas above imply step, amend, card, blame, verify and status as separate verbs. One verb that reads the files and acts is simpler to learn and matches `fm genesis step` ("next action from its files").
  Done when: in a fixture with no goal, an open goal, and a goal with a stale baton, bare `fm goal` prints the matching action each time, with no flags.

- **Skip the planner for small goals** — FEATURE — value 4 — effort S — risk low — category: ceremony
  Why: T-0794 (Lite mode) and T-1266 (ceremony profile) are both deferred. A one-line goal needs no contents list, no audit and no warranty. Assumption: goals of 3 or fewer rows are the common case.
  Done when: a goal the planner sizes at 3 rows or fewer opens with zero plan artifacts and closes on its done-when command alone. A test counts the files.

- **Allow only two ceremony profiles** — CLEAN — value 3 — effort S — risk low — category: ceremony
  Why: the pack's ideas stack gates (cold auditor, two closers, warranty, pre-mortem, ghost user). Assumption: "light" and "full" are enough, and per-goal knobs are the next sprawl.
  Done when: a lint fails if any goal config key beyond `profile: light|full` changes behaviour.

- **Give every new goal feature a complexity budget** — CLEAN — value 4 — effort M — risk med — category: governance
  Why: T-2109 already found hook notes averaging over 1,500 chars per injection. Each added goal idea costs more bytes per turn. Assumption: a hook-bytes ceiling is easier to enforce than judging each idea.
  Done when: `plugin/tests/bench_hooks.py` fails if the total goal injection per turn exceeds a stated cap, and the failure names the newest contributor.

- **Inject only the delta line after the first turn** — PERFORMANCE — value 4 — effort S — risk low — category: hooks
  Why: the session-start goal card is enough. After that, a one-line `G-3 4/9 → next: X` is needed only when it changes. This is a simplification of the "byte-stable card" ideas.
  Done when: a 20-turn fixture with no goal change injects the full card once and nothing after.

- **Retire stale deferred tasks automatically** — CLEAN — value 3 — effort S — risk low — category: queue
  Why: Open work holds over 20 "Later from T-07xx/08xx" items marked deferred. Assumption: most have not been touched in months.
  Done when: `fm` proposes closing deferred items with no activity for 60 days, as one batch the user approves or vetoes in one line, and the deferred list shrinks.

- **Dedupe ideas before they reach the user** — CLEAN — value 3 — effort M — risk low — category: brainstorm
  Why: the "Ideas so far" list repeats itself. "Hold done in a 14-day warranty", "Give every done goal a 14-day warranty" and "Hold every done in a 14-day reopen window" are one idea. Cluster by title and body before the list is passed to the next round.
  Done when: running the dedupe on this pack's list returns clusters, and the three warranty titles land in one cluster.

- **Make cold reads advisory after one repair** — FIX — value 4 — effort M — risk med — category: genesis
  Why: T-2206, T-2228, T-2229 and T-2231 were all fixes for cold-read puts deadlocking on stray quotes. Cap the loop. After one retry, a cold-read FAIL that cites no live line is logged and does not block.
  Done when: a put with a stale-quote FAIL succeeds on the second pass and the ledger records the waived finding.

- **Wild: Refuse any plan longer than one screen** — FEATURE — value 3 — effort S — risk med — category: planning
  Why: wild. A plan that doesn't fit in 24 lines gets split into two goals by force. It stays readable on a phone, and the baton stays small.
  Done when: a 40-row plan request returns two linked goals of 24 lines or fewer each.

- **Wild: Make status a 20-word sentence or call it not understood** — FEATURE — value 3 — effort S — risk low — category: legibility
  Why: wild. If the ledger can't be summarised in 20 plain words ("4 of 9 done; next: write the parser test"), the goal state is too tangled. Treat that as a lint failure.
  Done when: every goal in the test fixtures produces a status sentence of 20 words or fewer, and a tangled fixture fails the lint.

- **Wild: Hold a weekly delete-a-feature review** — CLEAN — value 3 — effort M — risk low — category: product
  Why: wild. Foreman has 2010 files and 1360 under `plugin/skills/`. Rank commands and skills by local use over 30 days. The bottom three come with a one-command removal patch for the user to accept or decline.
  Done when: the report lists the three least-used commands with their usage counts, and accepting one removes it and passes `fm doctor`.

Next question: Which of the roughly 300 goal ideas, if deleted, would nobody notice, and what measure from the ledger shows it?
Next question: What is the smallest goal feature set that still passes the "looks done" and kill-and-resume exam scenarios?

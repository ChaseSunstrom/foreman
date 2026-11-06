# Brainstorm — lens: user value

Seen through user value, the recent requests are nearly all paper cuts in Foreman's own gates, intake and messages, found by dogfooding. The best ideas stop those from being found one at a time.

- **Audit every blocker for a next step** — FIX — value 5 — effort M — risk low — category: messages
  Why: T-1995, T-2000 and the latest `run.py` "no test matches" fix each added a "did you mean" to a single message. Each time the user hit a dead end and filed a fix. Assumption: many other refusals still have no suggestion.
  Done when: a test walks every registered blocker or refusal string and fails if one has no suggested command, path or id.

- **Ship a task with one command** — FEATURE — value 5 — effort M — risk med — category: workflow
  Why: "Ship T-1982 / T-1987 / T-1992 / T-1996 / T-2001 to main" was typed five times in a row. Assumption: `fm ship` already exists but still needs a prompt each time.
  Done when: `fm ship T-N` runs the gates, merges and reports a one-line receipt, and refuses with the exact failing step if any step fails.

- **Check ideas against dropped decisions before proposing** — FEATURE — value 4 — effort M — risk low — category: brainstorm
  Why: the user dropped ideas as YAGNI, as conflicting with "make sure it doesnt sit idle", or as "nothing to tighten". Brainstormers can re-propose those.
  Done when: a new idea matching a dropped one is shown with its drop reason, and `fm ideas` marks it "previously dropped".

- **Add a dogfood-friction ledger** — FEATURE — value 4 — effort M — risk low — category: dogfooding
  Why: the fixes (mid-word title cut, overlapping suites, dry-streak miscount) were all noticed in use, and the user steered "a scratchpad write set it off while dogfooding". Assumption: friction is currently noticed only by luck.
  Done when: each blocker, retry or manual override is logged, and `fm friction` ranks the top 5 by frequency.

- **Run one test suite at a time through a single lock** — FIX — value 4 — effort M — risk med — category: concurrency
  Why: T-1964, T-1984 and T-1974 each fixed one way two suites could overlap (ambient, ship, check). Assumption: more entry points remain.
  Done when: all test runs go through one lock owner, and a stress test starting 5 entry points at once never runs two suites.

- **Make intake lossless and previewable** — FEATURE — value 4 — effort M — risk low — category: intake
  Why: T-1989 found that `@path`-only lines were silently dropped. T-0790 on verbatim capture is deferred. Silent dropping is the worst kind of loss.
  Done when: `fm intake --dry-run` shows how each pasted line was parsed, and no input line is ever discarded without being listed.

- **Prune the deferred backlog** — CLEAN — value 3 — effort S — risk low — category: backlog
  Why: more than 30 items are "deferred: Later from T-0760/0818/0843", some with "needs evidence" notes, and the open list is noisy.
  Done when: each deferred item is either promoted, merged into a parent, or closed with a reason, and the open list is under 15.

- **Show a plain close-out receipt** — FEATURE — value 3 — effort S — risk low — category: legibility
  Why: T-0795 is deferred; the commit lines show the user tracks many tiny task ids at once.
  Done when: closing a task prints files changed, tests proved, time and cost on one screen.

- **Wild: Run a replay duel against the user's own task history** — FEATURE — value 5 — effort L — risk med — category: evaluation — wild
  Why: T-1231 wants Foreman to beat plain Claude, but benchmarks lack cases (T-0866). The 2000-plus closed tasks are a real corpus. Assumption: tasks have recoverable base commits.
  Done when: `fm duel --replay 20` runs 20 past tasks both ways and prints pass, cost and time side by side.

- **Wild: Give every message a regression test from its own bug** — FEATURE — value 3 — effort L — risk med — category: quality — wild
  Why: the "-k core_integrity matched no test" miss shows that acceptance criteria can be wrong. Assumption: criteria are machine-readable.
  Done when: closing a task runs each DONE-WHEN command against the pre-change tree and refuses if one passes there or matches nothing.

- **Wild: Keep a nightly "tomorrow's paper cuts" branch** — FEATURE — value 4 — effort L — risk med — category: unattended
  Why: the user queues small FIX items continuously, and T-0793 on overnight routines is deferred.
  Done when: each morning a branch holds up to 3 gate-passing fixes for friction-ledger items, none merged without approval.

- **Wild: Add a "why did Foreman do that" command** — FEATURE — value 3 — effort M — risk low — category: transparency
  Why: users steer with notes like "had the same gap" and "never saw that write", which means they reconstruct behaviour by hand.
  Done when: `fm why` on a refusal or skipped action prints the rule, config and event that caused it.

- **Sweep for sibling gaps after each fix** — FEATURE — value 4 — effort M — risk low — category: fix-quality
  Why: the `_task_files` steer said it "had the same gap" as an earlier fix, and the T-1998 and T-2001 pair is similar.
  Done when: closing a FIX task runs a grep for the fixed pattern's siblings and lists them as captures or a "none found" line.

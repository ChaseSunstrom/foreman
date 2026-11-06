# Brainstorm — lens: user value

- **Run `fm recurse` for open-ended "keep improving" mandates** — FEATURE — value 5 — effort L — risk med — category: autonomy
  Why: wild. The user's steer is "recursively improve means finish the tasks, then review and brainstorm on top, repeatedly". Today each round is a hand-launched task (T-0818).
  Done when: `fm recurse --rounds 3 --budget $X` runs ship, review, brainstorm, queue and build, stops at the budget or when a round keeps no new ideas, and ends with a one-screen summary.

- **Generate the "Round N shipped" brief from the ledger** — FEATURE — value 5 — effort M — risk low — category: recursion
  Why: the "Round 1 shipped today", "Deferred clusters (and why)" and "Known gaps" sections were written by hand. They are the context a round-2 brainstorm depends on.
  Done when: `fm round review` prints shipped tasks, deferred clusters with their reasons, and unmeasured claims from the ledger alone. A test shows it matches a fixture round.

- **Probe whether the mail monitor really armed in this session** — FIX — value 4 — effort S — risk low — category: liveness
  Why: the pack lists "arming in a live interactive session is unverified (monitors start only in new sessions)".
  Done when: after SessionStart a canary line is streamed and acknowledged. `fm doctor` shows `monitor: armed` or `not armed (restart session)`, and `fm bus --wake` falls back to tmux only on the second.

- **Run compact output in shadow mode before asking for a yes** — FEATURE — value 4 — effort M — risk low — category: tokens
  Why: it is built and measured at about 1.04M tokens per 30 days, but off until the user opts in. They have repeatedly rejected unmeasured premises.
  Done when: shadow mode logs what would have been cut, and flags each case where the model re-ran the same command within 3 turns. After 3 days `fm` shows saved tokens and the miss count, and one key enables it.

- **Replay every metric reader against real stored result strings** — FIX — value 4 — effort M — risk low — category: correctness
  Why: two asks in a row were the same class of bug. Track record missed failures from `fm task finish`, and catch rates matched `exit N` against stored `✗ exit N`.
  Done when: a corpus of real ledger result lines is committed. Every reader of results (track record, catch rate, give-up mining, any other found by grep) passes it, and a new reader without a corpus test fails the suite.

- **Give each deferred cluster a reactivation trigger** — FEATURE — value 4 — effort M — risk low — category: backlog
  Why: round 1 deferred T-0787..T-0799 with reasons such as "no incident", "no evidence it recurs" and "needs per-project servers". Nothing reopens them when that reason stops being true.
  Done when: a deferred task can carry `reopen_when: <check>`. The check runs at `fm doctor` or round review, and a true check moves the task to captured with a note.

- **Re-measure the premise behind every dropped idea on a schedule** — FEATURE — value 3 — effort M — risk low — category: backlog
  Why: wild. The `if` scoping of the Read hook was dropped on a measurement (about 35 ms, about 2 minutes per month). The measurement is stored only as prose, so a change in usage or hook cost can't resurrect it.
  Done when: a drop stores its measurement command and threshold, and monthly `fm tidy` re-runs them and surfaces any that now flip.

- **Learn which close warnings the user overrides, and quiet them** — FEATURE — value 4 — effort M — risk med — category: close-out
  Why: round 1 fixed two false close warnings by hand (tier-drift counting non-diff lines, empty `.claude/worktrees/` flagged as left behind).
  Done when: each close warning records whether it was acted on or overridden. A warning overridden 5 times with no later fix is downgraded to a one-line note, and the downgrade is listed in `fm doctor`.

- **Report which of the user's own commands produce the biggest outputs** — FEATURE — value 3 — effort S — risk low — category: tokens
  Why: the pack shows 44.3M chars of Bash output over 30 days, and compact output only rewrites it after the fact. The cheaper fix is often a quieter flag at the source.
  Done when: `fm cost --outputs` lists the top 10 commands by output chars with a suggested quieter form (for example `-q`) and the projected saving.

- **Shrink "ideas so far" to cluster summaries for each brainstorm** — PERFORMANCE — value 4 — effort M — risk low — category: tokens
  Why: this pack carries thousands of one-line prior ideas plus the user's words twice. Children spend most of their budget re-reading dupes, and several round-1 ideas repeat earlier ones.
  Done when: the pack builder emits at most about 150 lines of prior ideas (cluster, count, three exemplars, shipped or dropped status). A test checks that the shipped and dropped lists are still carried verbatim.

- **Revert a whole round with `fm round revert N`** — FEATURE — value 3 — effort L — risk high — category: safety
  Why: wild. Recursion compounds changes, and the user steers by dropping things after the fact. They have no single undo for a round.
  Done when: reverting round 1 creates a branch undoing its tasks' commits in reverse order, runs the gates, and refuses with the failing check if any gate breaks.

- **Tick the board in one pass at round end** — FEATURE — value 3 — effort S — risk low — category: feedback
  Why: "nobody has ticked the board yet", so keep, drop and meh signals never reach the next round. `fm page` already renders the shipped items.
  Done when: a page or terminal list of shipped items takes `k`/`d`/`m` per item. The marks are written to the ledger and appear in the next pack's "dropped" and "kept" lines.

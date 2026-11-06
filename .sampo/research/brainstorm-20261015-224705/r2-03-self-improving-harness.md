# Brainstorm — lens: self-improving harness

- **Distill model judgments into deterministic rules** — PERFORMANCE — value 5 — effort M — risk med — category: self-tuning
  Why: assumption: intake, gray-zone guard and reviewer calls go through `claude -p` and repeat on similar inputs. The pack shows a paid-binary lockout problem (T-0990) and many "route to a cheap model" ideas, but nothing that removes the call entirely.
  Done when: `fm judge stats` shows a judgment kind with at least 5 identical verdicts on one feature signature, and the next matching input is answered by the compiled rule with zero child spawns, which a ledger line confirms.

- **Learn the user's vocabulary into a project glossary** — FEATURE — value 4 — effort S — risk low — category: user value
  Why: the user's words are "pane", "mod UI", "band", "dock", "chat window" and "graph". Each prompt is mapped to files only by guesswork. Assumption: edits made after a prompt show which symbols a term meant.
  Done when: `fm glossary` lists "band → register.tsx:Band" with a confidence, and the next prompt using "band" has its term-to-file mapping injected, which a fixture session shows.

- **Measure the re-read tax and write orientation notes** — PERFORMANCE — value 4 — effort M — risk low — category: tokens
  Why: assumption: sessions re-explore the same files (the card work notes "6 of 1,084 cards ever fired", so discovery is repeated). The ledger already records Read calls.
  Done when: a report lists files read in at least 4 sessions with the token cost, and a generated 5-line note for one of them is injected on its next first read and expires when the file changes.

- **Hold a builder exit interview and verify its claims** — FEATURE — value 4 — effort S — risk low — category: self-report
  Why: the pack asks for "learn why builders stop" but covers only the exit reason. A structured set of "what did you guess, what was missing, what slowed you" answers, checked against the tool log, finds doc and card gaps.
  Done when: a SubagentStop hook stores a JSON exit report with a `verified` flag per claim, and `fm learn` groups repeated "guessed X" entries into a proposed card or doc task.

- **Audit Goodhart drift in Foreman's own scoreboard** — FIX — value 4 — effort S — risk low — category: measurement
  Why: the plan adds a scoreboard, first-time-pass and compliance metrics. Assumption: metrics Foreman optimises can rise while user steers, interrupts and "still cluttered" repeats do not fall. The user's repeated UI complaints show that gap.
  Done when: the weekly report flags any metric that improved while user corrections per closed task stayed flat or rose, with both series shown.

- **Detect gate tampering by builders** — SECURITY — value 4 — effort S — risk low — category: trust
  Why: Foreman's core claim is proof by commands actually run, yet a builder can weaken the proof by deleting assertions, adding skips or widening tolerances. Assumption: no current check looks for this.
  Done when: a diff that removes an assertion or adds `skip`/`xfail` in a test linked to the task makes `fm task finish` require an explicit reason, and a fixture test covers three tamper patterns.

- **Score hot files from fix-after-edit history** — FEATURE — value 3 — effort M — risk low — category: planning
  Why: C13 seeds from git history, but only for lessons. A SZZ-style pass (commits followed within N days by a "fix" commit touching the same lines) gives per-file risk the plan stage can use.
  Done when: `fm map risk` ranks files, and a plan touching a top-5 file shows a one-line warning citing the two commits that made it risky.

- **Learn a machine capability sheet from failures** — FIX — value 4 — effort S — risk low — category: environment
  Why: several user asks come from environment facts Foreman never learned (`~/.local/bin/claude` missing from PATH, no libappindicator, Haiku trip-ups on the repo's test runner). Exit 127 and "not found" errors repeat.
  Done when: after an exit-127 resolved by a path, `fm env` lists the verified fact and a later session gets it as a pre-empt, with a "last verified" check on use.

- **Register tunables and tune them within bounds** — PERFORMANCE — value 3 — effort M — risk med — category: self-tuning
  Why: the pack has many size gates, caps, timeouts and thresholds as scattered constants, and ideas to tune a few individually. One registry with min, max and an objective makes them tunable together.
  Done when: at least 8 constants live in `tunables.json` with bounds, `fm tune --dry` proposes changes from ledger data, and a change outside its bounds is rejected.

- **Draft upstream Claude Code issues from captured evidence** — FEATURE — value 3 — effort S — risk low — category: ecosystem
  Why: Foreman hit upstream-looking problems (the folder-trust stall, repeated env-prelude exports, `--resume` repair). Drafts are written locally only, never posted without a confirmation.
  Done when: `fm upstream draft <incident>` writes a markdown file with version, minimal repro and redacted log excerpts, and a test proves nothing is sent.

- **Wild: Merge two brains by running both on the replay corpus** — FEATURE — value 4 — effort L — risk med — category: portability
  Why: wild. Text merge of hints and rules from two clones can't tell which side is right, so the custom merge driver is already a planned worry. Evaluating both sides on recorded obstacles chooses the winner by evidence.
  Done when: for a conflict on one rule, `fm brain merge` picks a side, prints the score of each on at least 5 recorded cases, and records the choice.

- **Wild: Keep a regret ledger of rejected plan alternatives** — FEATURE — value 3 — effort M — risk low — category: learning
  Why: wild. The plan stage already has a pivot table, but the options not taken are discarded. When the chosen path is later reverted or fails, the ledger notes which alternative would have worked, and plan-time recall surfaces it.
  Done when: a task whose plan lists 2 or more approaches stores the rejects, and after a revert of that task `fm why` names the best untried alternative.

- **Wild: Prefetch from a trace n-gram next-action model** — PERFORMANCE — value 3 — effort M — risk low — category: prediction
  Why: wild. The ledger holds a long tool history. A tiny local n-gram over (tool, file role) sequences predicts the next read, test or card with no model call, and the hook warms it early.
  Done when: on held-out ledger sessions the predictor's top-1 hit rate is reported, and a hook pre-fetches only when the rate is at least 60% per sequence type.

- **Wild: Run a Foreman fire drill with a planted bad instruction** — SECURITY — value 3 — effort M — risk med — category: red-team
  Why: wild. Once a week, in a throwaway worktree, Foreman gives a hermetic session a task with a plausible wrong premise (a nonexistent flag, a misleading comment) and checks whether its own gates and scouts catch it, so the harness measures its own recall.
  Done when: `fm drill` runs 5 planted cases, reports caught or missed per gate, and a missed case becomes a draft task.

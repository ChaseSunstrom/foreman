# Brainstorm — lens: bold bets

- **Build a guard replay corpus from real ledger commands** — FIX — value 5 — effort M — risk low — category: guard
  Why: Recent friction is guard false positives on Claude's own edit/probe commands, plus two real bypasses found only while grounding false positives. The fix stream is whack-a-mole (heredocs, backticks, `$'…'`, keywords, versioned interpreters). Every command the guard has allowed or blocked sits in the ledger and could become labeled test data.
  Done when: `fm check` runs a corpus of at least 500 recorded commands with allow/block labels, and a deliberately reintroduced T-0128-style regression fails a named corpus case.

- **Mutate allowed commands to hunt for guard bypasses** — SECURITY — value 4 — effort M — risk low — category: guard
  Why: The bypasses were found by accident (fake `--run` in a heredoc, `/fm` suffix, quoted marker). Wrapping known-bad commands in quoting, heredoc, `$'…'`, `env`, `xargs`, `bash -c` and keyword prefixes finds the next ones before the user does. Stdlib only.
  Done when: `fm guard fuzz` generates at least 2,000 wrapped variants of the blocked classes, reports any that pass, and the run is deterministic by seed.

- **Replace the fixed 3-task friction cadence with a measured trigger** — FEATURE — value 4 — effort S — risk low — category: self-improvement
  Why: The user wants RSI, but passes run on a count plus a 2 h minimum, and the last pass found one bug. A trigger based on friction events (repeated guard rewrites, stalled drives, hook failures) fires when there is something to read and stays silent otherwise, saving tokens.
  Done when: with no new friction events no pass starts after 3 closed tasks, and with 5 or more repeated same-category events a pass starts within one task close. Both are covered by tests.

- **Score each self-improvement fix by whether the friction stopped** — FEATURE — value 5 — effort M — risk med — category: self-improvement
  Why: There are 183 tasks and many guard fixes, but nothing records whether a fix reduced its friction category. Without that feedback RSI cannot tell progress from churn. Tie each friction-derived task to a category, then compare event rates before and after.
  Done when: `fm friction report` lists each fix with before/after event counts per week, and flags any fix whose category did not drop after 10 closed tasks.

- **Render a frame-by-frame mod screenshot test for every row type** — CLEAN — value 4 — effort M — risk low — category: ui
  Why: The user has repeatedly reported panels not matching, duplicated dashboard, unpanelled buttons, bad diff contrast and un-animated `$` rows. Each was found by eye. The Snapshot tool plus a golden-file check per row kind (reply, command, edit, diff, prompt, agent, dashboard) turns the complaint into a failing test.
  Done when: the mod tests include a golden snapshot for each row kind, and changing the border style of one kind fails exactly that snapshot.

- **Add a lint that flags any text row that is not inside a panel** — FIX — value 4 — effort S — risk low — category: ui
  Why: The user keeps finding unpanelled rows ("I found the issue…", their own chats, questions). A rule that every rendered row must go through the panel kit makes the omission fail a test instead of surfacing in review.
  Done when: a test renders every registered row type and fails if any output line sits outside a panel border, and it passes on the current mod.

- **Measure agent-perceived slowness as time-to-next-action** — PERFORMANCE — value 4 — effort M — risk low — category: speed
  Why: The user said "I don't mean the speed of foreman itself, but agents using foreman, it feels slow." The 30 ms hook p95 shows Foreman is fast. The cost is in the number of turns and calls per task (planning, evidence, audits). Counting turns, tool calls and model-wait per task, grouped by ceremony step, shows where the agent spends its time.
  Done when: `fm task finish` prints turns and tool calls per stage, and `fm stats` ranks the three stages with the most calls across the last 20 tasks.

- **Run a parallel-lane contention probe** — PERFORMANCE — value 3 — effort M — risk med — category: parallel
  Why: The user asked that parallel work not cause "context/speed/quality/usage issues", and parallel cleanup bugs have already been fixed once. A probe runs N lanes with a cheap Haiku harness, then records per-lane tokens, wall time, merge conflicts and test-suite runtime, then suggests a safe N.
  Done when: `fm run --parallel --probe` reports a recommended lane count from measured data, and the report is stored in the ledger.

- **Wild: Let Foreman red-team its own newest commit with an adversary subagent** — SECURITY — value 4 — effort M — risk low — category: RSI — wild
  Why: Two real bypasses surfaced only while grounding false positives, and an automated review found the `/fm` suffix bug. An adversary subagent that gets only the guard diff and the goal "get a blocked class past this" before each guard commit would find them earlier.
  Done when: every task touching fmguard.py records an adversary-attempt log, and a seeded known bypass is found by the subagent in a test run.

- **Wild: Build a "regret ledger" that grows from the user's corrections** — FEATURE — value 4 — effort M — risk med — category: RSI — wild
  Why: The user's words repeat the same corrections (panels, duplicates, not wanting commands handed over). Each correction recorded as a one-line checkable expectation, such as "no row outside a panel", can be rechecked by the self-improvement pass against the current build.
  Done when: `fm regret add "<correction>" --check "<cmd>"` stores an entry, and `fm check` fails if a check regresses.

- **Wild: Hand each friction category to a competing pair of fix subagents** — FEATURE — value 3 — effort L — risk med — category: RSI — wild
  Why: A single recon subagent turns friction into one fix, with mixed results. Two independent worktree fixes with a judge that picks by corpus pass rate and diff size gives selection pressure, which is closer to the RSI the user described.
  Done when: for one friction category two worktree candidates are produced, a judge picks one with recorded reasons, and the other is discarded cleanly.

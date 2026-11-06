# Brainstorm — lens: reliability

- **Replay real command history through the guard before every guard change** — SECURITY — value 5 — effort M — risk low — category: guard regression
  Why: the last 25 commits are mostly guard fixes (heredoc quoting, backticks, `$'…'`, keywords, standing yes), each found by a false positive or a bypass after the fact. Assumption: the ledger or events keep the Bash commands and the guard's verdicts.
  Done when: `fm check` replays a recorded corpus of past commands, fails if any verdict flips without an updated expectation, and the corpus holds at least 200 commands including the known bypasses.

- **Fuzz the guard with wrapped and mutated forms of known-bad commands** — SECURITY — value 4 — effort M — risk low — category: guard fuzzing
  Why: two real bypasses were found only while grounding false positives (fake `--run` in a heredoc, `$'…'` backticks). Mutating each denied command (quotes, `bash -c`, `eval`, variables, braces, keywords) finds the next hole before the user does. Assumption: the guard is a pure function over the command string.
  Done when: a stdlib fuzz test generates at least 1,000 mutations of the denied corpus, and every one that still means the same thing is denied (or a documented allow is listed).

- **Record every guard block with a keep/rewrite outcome** — FEATURE — value 4 — effort S — risk low — category: false positives
  Why: the most recent friction was guard false positives that cost a rewrite each. Without knowing which blocks were followed by a harmless rewritten command, the false-positive rate cannot be measured. Assumption: events can link a block to the next similar command.
  Done when: `fm friction` reports guard blocks per category with the share that were followed by a near-identical retry, and the list is sorted worst first.

- **Make state writes crash-safe and verified on resume** — FIX — value 4 — effort M — risk med — category: state integrity
  Why: parallel lanes, interrupts and mod reload hand-overs all touch the record; there is a cleanup-after-interrupt fix already. Assumption: writes are not yet checked end to end by a kill-at-every-step test.
  Done when: a test kills `fm` at each write point in `task finish` and `run --parallel`, and `fm doctor` always reports either a clean record or a repair that restores it.

- **Add a hook heartbeat so a silent hook failure is visible** — FIX — value 4 — effort S — risk low — category: observability
  Why: there is a circuit breaker for failing hooks, but nothing shows that a hook never ran (wrong dispatcher path, mod and plugin version mismatch). Assumption: a missing hook currently looks the same as "nothing to report".
  Done when: the session start card shows "hooks: N events seen in the last turn", and a deliberately broken dispatcher produces a visible warning within one turn.

- **Pin fm, hooks and mod to one version and refuse a mismatch** — FIX — value 4 — effort S — risk low — category: version skew
  Why: the installed mod is 0.4.0 while the plugin has moved on, and the mod only reloads at turn end. Assumption: nothing compares the versions at runtime.
  Done when: `fm doctor` and the session start fail loudly when the three versions differ, naming the one to update.

- **Add a lane-isolation audit for parallel runs** — FIX — value 4 — effort M — risk med — category: parallel safety
  Why: the user asked that parallel work not cause context, speed or quality issues, and the recent fixes were about cleanup and re-checking main. Assumption: disjointness is declared in the plan, not verified against the actual diffs.
  Done when: before merging a lane, `fm` compares its real changed paths to the declared set and to the other lanes, and refuses the merge with the overlapping files named.

- **Wild: Keep a flight recorder that explains any stall afterwards** — FEATURE — value 4 — effort M — risk low — category: diagnosability
  Why: the drive loop has had a lost-resume race and "continue, you weren't reprompted" complaints; each took manual digging. wild
  Done when: `fm why-stopped` prints the last 20 decisions (stop hook verdict, reload, background completion) with timestamps, and its output explains a staged stall in a test.

- **Wild: Run a chaos drill that kills the session mid-step in a throwaway worktree** — FEATURE — value 3 — effort L — risk med — category: resilience
  Why: resume, reload and background-completion races are the recurring reliability class. wild
  Done when: a scripted drill kills the process at random points across 20 runs and every run resumes to the same task and step with no lost evidence.

- **Wild: Let a shadow Foreman replay recent sessions against a candidate version** — FEATURE — value 4 — effort L — risk med — category: release safety
  Why: the self-improvement loop changes Foreman's own code every few tasks, and a regression there is costly because it runs unattended. wild
  Done when: before the branch merges, recorded hook inputs from the last N sessions run through old and new dispatchers, and any differing verdict is listed for review.

- **Cap what the self-improvement loop may change without a replay pass** — SECURITY — value 3 — effort S — risk low — category: RSI safety
  Why: the user wants recursive self-improvement, and the guard is the part most likely to be loosened by it. Assumption: the loop can currently edit the guard under the standing yes with only the unit tests as protection.
  Done when: a change to `fmguard.py` by the loop is refused to close unless the replay corpus check has passed in the same task's evidence.

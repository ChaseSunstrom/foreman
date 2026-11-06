# Brainstorm — lens: reliability

- **Add a guard decision-table oracle** — FIX — value 5 — effort M — risk low — category: guard reliability
  Why: Last 25 commits are mostly guard patches (heredoc quoting, backtick, `$'…'`, shell keywords, `--run` spoofing, standing-yes coverage). Each fix was found by a one-off probe. Assumption: no single table defines expected allow/deny per command form × category.
  Done when: one table file (command, shell form, expected verdict, category) drives a test that fails if `fmguard.py` disagrees on any row, and each of the last 25 guard fixes has a row.

- **Make hook failure loud, never silent-allow** — FIX — value 5 — effort M — risk med — category: hook integrity
  Why: A circuit breaker exists, and "make hook failure fail-safe and visible" was proposed. Assumption: a tripped breaker still falls open for destructive classes without any user-visible mark.
  Done when: with the guard hook forced to crash, destructive categories (git-destructive, rm-outside, credentials) are still blocked and the band shows "guard degraded" until it recovers.

- **Verify lane merge with a post-merge gate run** — FIX — value 4 — effort M — risk low — category: parallel safety
  Why: Parallel runs "re-check main before merging", but disjoint-file lanes can still break each other semantically (shared imports, tests). Assumption: the full gate runs only per lane, not on the merged result.
  Done when: after `fm run --parallel 2` merges two lanes, `fm check` runs on the merged tree, and an injected cross-lane break is reported with both lane IDs and the merge is held.

- **Add a record-vs-git reconciler on resume** — FIX — value 4 — effort M — risk low — category: state integrity
  Why: Task commits take only the task's files, and sessions resume via `--continue`. A crash between commit and record update could leave "done" in the record without a commit, or the reverse. Assumption: resume does not compare them.
  Done when: killing `fm task finish` after the commit but before the record write, then resuming, reports and repairs the mismatch with one visible line.

- **Run an environment-leak canary in every spawned subprocess** — SECURITY — value 4 — effort S — risk low — category: isolation
  Why: The snapshot tool needed FOREMAN_STATE kept out of the user's tmux. Test harnesses, worktree lanes, and reviewer subagents have the same class of leak risk. Assumption: only the snapshot tool was fixed.
  Done when: a test spawns each child kind (lane, snapshot, reviewer, test harness) and asserts no `FOREMAN_*` variable or state path is visible unless explicitly passed.

- **Score every self-improvement fix by whether its friction stopped** — FEATURE — value 4 — effort M — risk low — category: RSI loop
  Why: The loop runs every 3 closed tasks, and the user wants "RSI almost". The pack shows no outcome check, and guard false positives keep recurring. Assumption: fixes are not tied to friction event signatures.
  Done when: each friction-driven task stores its signature, and 10 closed tasks later `fm friction` marks it "stopped" or "recurred" and reopens recurrences into the inbox.

- **Cap parallel lanes by measured token and context budget** — PERFORMANCE — value 4 — effort M — risk med — category: parallel cost
  Why: The user said "make sure parallel things don't cause context/speed/quality/usage issues". Assumption: `--parallel N` is bounded only by task disjointness.
  Done when: `fm run --parallel 4` picks lanes from a budget estimated from per-task history, downgrades to fewer lanes with a stated reason, and logs actual versus estimated usage.

- **Wild: Run a replay-before-release shadow check on the mod** — FEATURE — value 4 — effort L — risk med — category: release safety
  Why: The user must approve each mod release, and render complaints keep recurring ("looks weird", "duplicated"). Assumption: a headless render exists via the snapshot tool. wild
  Done when: recorded event streams from 5 past sessions render through the candidate mod, and any frame with duplicated dashboard text or an unpaneled row fails the check.

- **Wild: Give the guard an adversary subagent that attacks each new rule** — SECURITY — value 4 — effort M — risk low — category: guard hardening
  Why: Two real bypasses were found only while grounding false positives, so rules ship before being attacked. wild
  Done when: a guard-touching task cannot finish until an adversary run's bypass attempts are all blocked or filed as inbox items, with the attempts attached as evidence.

- **Wild: Keep a flight recorder that explains any stall afterward** — FEATURE — value 3 — effort M — risk low — category: observability
  Why: Drive stalls, reload races and "weren't reprompted" bugs were each diagnosed by hand. wild
  Done when: after a simulated stalled drive, `fm why-stopped` prints the last 20 hook, turn and state events with the stop reason in under 2 seconds.

- **Add a stale-lane sweeper for orphan worktrees and branches** — CLEAN — value 3 — effort S — risk low — category: parallel hygiene
  Why: Parallel runs now clean up after interrupts, but a SIGKILL or power loss bypasses that cleanup. Assumption: nothing sweeps on the next start.
  Done when: after SIGKILL of a running lane, the next `fm` session start removes the orphan worktree and branch, and reports it only if uncommitted work was found.

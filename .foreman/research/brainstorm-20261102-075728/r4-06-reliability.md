# Brainstorm — lens: reliability

- **Pin the usage-limit wait-out to a golden message corpus** — FIX — value 4 — effort S — risk low — category: unattended
  Why: steer 2026-11-01 says to wait out real usage limits and resume where stopped. The wait is only as good as the parser that reads the reset time out of each harness's message, and a misparse means sleeping forever or hammering the API. Assumption: no corpus of real limit messages exists in `plugin/tests`.
  Done when: a test feeds 10+ captured limit messages from Claude, Codex, Gemini and opencode to the parser. Each yields a bounded wake time, an unparseable one yields a capped re-probe interval, and every wait writes one ledger line with its max.

- **Freeze a last-known-good `fm rescue`** — FEATURE — value 4 — effort M — risk med — category: self-repair
  Why: Foreman fixes Foreman through its own task loop, so a broken working-copy `fm` can't repair itself. Hooks already fall back to the committed library (T-2605 and the non-tool-event fix), but the CLI verbs have no equivalent.
  Done when: with `plugin/lib` deliberately broken, `fm rescue status` still runs from a pinned copy, prints the failing import, and `fm rescue revert-lib` restores the last green tree.

- **Run the ledger fsck with a repair plan** — FEATURE — value 4 — effort M — risk low — category: integrity
  Why: the pack shows many cross-referencing ledgers (tasks, bets, grants, steers, drops, decisions). Individual verbs check their own file, but nothing checks the links, such as a dropped task id that no longer exists or a grant spent twice. Assumption: no whole-state check exists.
  Done when: `fm fsck` on a fixture state with 5 planted dangling references names each one with the file and line. `--plan` prints a repair per finding without writing, and a clean state exits 0.

- **Re-prove the closed task on the landed tree** — FIX — value 4 — effort M — risk med — category: proof
  Why: T-2598 says `fm ship` lands on main by cherry-pick. A criterion proven on the branch tree may therefore not hold on the tree main actually received.
  Done when: closing a task records the tree hash of the proof. After landing, `fm ship` re-runs that criterion's verify command on main's tree and prints a mismatch line if the trees differ and the rerun fails.

- **Make `install.sh` staged, resumable and idempotent** — FIX — value 3 — effort M — risk low — category: install
  Why: the "no claude on PATH" steer and the installed-versus-source drift tasks (T-0418) show installs are an ongoing source of trouble. Assumption: install does not stage into a temp dir and swap atomically.
  Done when: a test kills `install.sh` at each step, then re-runs it. Every run ends with an install that passes `fm doctor` or the old install untouched, and a second run changes zero files.

- **Sign proof records with a key the agent can't read** — SECURITY — value 4 — effort M — risk med — category: evidence integrity
  Why: Foreman's selling point is "proves its work with commands it really ran". A session with Bash access could still append a plausible prove row to the ledger by hand. Assumption: proof rows are plain appended lines.
  Done when: a red-team test writes a forged prove row directly. `fm doctor` and `fm task finish` reject it as unsigned, and a row written through `fm task prove` verifies.

- **Coexist with the repo's own git hook managers** — FIX — value 3 — effort M — risk med — category: git compatibility
  Why: assumption: Foreman installs git-level hooks. Husky, lefthook, pre-commit and a user-set `core.hooksPath` all overwrite or bypass hooks in the field.
  Done when: fixture repos for each of the four managers install Foreman's hook without clobbering the manager's. A commit still fires both, and uninstall restores the original bytes.

- **Dual-run new hook code in shadow before it takes over** — FEATURE — value 3 — effort M — risk low — category: upgrade safety
  Why: T-2605 and the hook fallbacks show the committed and working-copy libraries can diverge. After an upgrade, the first sign of a bad hook is currently the user's own session.
  Done when: for the first 50 live hook calls after a library change, both versions run. A verdict difference is logged to one file and the committed version's answer is used, and `fm doctor` names the count of diffs.

- **Soak the drive for 72 compressed hours and ratchet its footprint** — PERFORMANCE — value 3 — effort M — risk low — category: long-run
  Why: the pitch is carrying a plan "over days". Tick soaks are proposed, but nothing measures the drive loop's own memory, open files and state-dir growth.
  Done when: a seeded fake-clock run of the drive records peak RSS, open fd count and bytes written per simulated day. `fm ship` fails if any of the three grows more than 20% over the stored baseline.

- **Trend user-visible faults per 100 sessions by cause** — FEATURE — value 3 — effort S — risk low — category: reliability KPI
  Why: the commit log shows many fixes (T-2606, T-2605, T-2600), but no rate says whether Foreman is getting more reliable. `fm friction` already holds the raw events.
  Done when: `fm doctor` prints faults per 100 sessions for the last 4 weeks, split by hook, tick, drive and verb. A week with zero sessions reads "no data", not 0.

- **Wild: Keep a trust balance that degrades Foreman automatically** — FEATURE — value 3 — effort L — risk med — category: graceful degradation
  Why: wild. Each confirmed fault (crash card, false done, dropped fire) debits a visible balance. Below a threshold Foreman drops to Lite mode (T-0794) until clean sessions repay it, so the user sees reliability turn into fewer moving parts.
  Done when: injecting 3 synthetic faults flips the mode line to Lite and disables the listed non-essential emitters. 10 clean sessions restore it, and each step is one ledger line.

- **Wild: Exercise the fallbacks live at a low rate** — FEATURE — value 3 — effort M — risk low — category: fallback rot
  Why: wild. Fallback paths (committed library, cache-free guard, plain-file `fm code`) run only when something is already broken, so they rot unseen. Assumption: nothing tests them in real sessions.
  Done when: roughly 1 in 200 hook calls runs through the fallback path. Any verdict mismatch against the normal path writes a named line to `fm doctor`, and the rate is configurable to 0.

- **Wild: Keep the state dir as a git repo, one commit per write** — FEATURE — value 3 — effort L — risk med — category: state recovery
  Why: wild. Silent state corruption is hard to place in time. With a commit per write, `git bisect` finds the write that broke a ledger, and `fm undo-state N` rolls back precisely.
  Done when: a planted corrupt write in a fixture session is located by `fm state bisect` to its exact commit. Write latency stays under 15 ms at p95.

Next question: Which Foreman-owned file does a session read before it acts, such as baton, steers or decisions, and what happens to the session if that one file is unreadable or stale?
Next question: Which of these self-repair paths could a bad Foreman release itself disable, and what outside check would notice?

# Brainstorm — lens: the night shift (invented): work starts without the user: schedules, file and event triggers, CI and issue watchers, installs queued for one yes

- **Queue every install behind one batched yes** — FEATURE — value 5 — effort M — risk med — category: triggers
  Why: Mission 8 #11 says timers and units "get queued for one yes"; the guard stops unattended installs, and T-0325 and T-0418 sit blocked on a sudo or an update only the user can approve.
  Done when: `fm queue` lists every pending install (timer, unit, package) with its command and reason, and a single `fm queue approve` runs them all, logging each result. Nothing runs before approval, and a test proves it.

- **Run a nightly "morning ledger" shift** — FEATURE — value 5 — effort M — risk low — category: scheduling
  Why: the trigger table and signal-to-fix loop exist (T-2272, T-2276), but nothing says one scheduled run ties them together. Open work is 30+ deferred or blocked rows, with no overnight pass.
  Done when: a timer-started `fm night` run does the shift (pick the top unblocked task, work it in a lane, stop at the budget) and writes one `morning.md` listing done, parked, and needs-you, readable in under 30 seconds.

- **Cap overnight spend with a hard shift budget** — SECURITY — value 5 — effort S — risk low — category: budget
  Why: the budget line reads "$0/$200"; unattended work with a model router (T-2291) can burn it with no one watching. Steer 3 says to wait out usage limits and not stop for budget, so the cap must be the user's own number, not an invented one.
  Done when: `fm night --budget N` stops new lane spawns at N, and a test with a stub model confirms the shift ends at the cap with a "budget reached" line in the ledger.

- **Watch CI and open issues, and draft the fix in a lane** — FEATURE — value 4 — effort M — risk med — category: watchers
  Why: the README shows a test.yml badge, and the user already has the "Baseline red" auto-filed task, so the loop exists locally. It doesn't yet watch GitHub.
  Done when: with a failing run on main, the watcher files one task with the log tail and opens a lane; a green re-run closes it, and duplicates of the same failure signature are deduped.

- **Fire on file and git events, not only the clock** — FEATURE — value 4 — effort M — risk low — category: triggers
  Why: the trigger table (T-2276) learns from outcomes, but the kinds named are captures. No kind is named for lockfile, manifest or `.fm/` edits, or for a new commit on a branch.
  Done when: a changed `package.json` or `pyproject.toml` raises a "dependency drift" trigger once per change, `fm triggers` shows its precision, and a trigger mostly dropped is demoted.

- **Dry-run every scheduled job before it is allowed to repeat** — FIX — value 4 — effort S — risk low — category: safety
  Why: a timer that fails at 3am fails silently. The earlier slate asks for circuit-breaking hooks but not for scheduled jobs.
  Done when: `fm night add` runs the job once in a throwaway worktree and shows its output before queuing the timer. A job that exits non-zero twice in a row is disabled and appears at the top of the morning ledger.

- **Pause the shift when the user comes back** — FEATURE — value 4 — effort S — risk low — category: coexistence
  Why: assumption: the user works at odd hours. Two lanes editing the same files as a live session produce the collision the earlier slate flagged for goals.
  Done when: keyboard or session activity in the repo parks the night lane at the next safe point, with its branch kept. A test shows no night write lands on a path the live session touched in the last N minutes.

- **Score each overnight run against what the user did next** — FEATURE — value 4 — effort M — risk low — category: learning
  Why: predictions are scored at close (T-2290), but only for estimates, not for whether the user kept, edited or reverted the night's work.
  Done when: each morning item records kept, edited or reverted from later commits, and `fm night stats` shows the rate per trigger kind. A kind under a set threshold stops starting unattended.

- **Retry a stopped or rate-limited lane on its own** — FIX — value 4 — effort M — risk med — category: recovery
  Why: Mission 8 #9 says it "recovers stopped ones", and steer 3 says to wait out real usage limits and resume. No evidence shows a resume timer tied to the limit's reset time.
  Done when: a lane stopped by a usage limit gets a one-shot wake at the reset time, resumes from its baton, and logs "resumed after limit" in the ledger.

- **Wild: Run a night-owl "pre-mortem" on tomorrow's first task** — FEATURE — value 3 — effort M — risk low — category: anticipation
  Why: wild. Foresight (`fmforesight`) is meant to flag problems before they happen. At midnight it takes the likely next task, dry-runs its plan in a throwaway worktree, and leaves "here is where this will hurt" in the morning ledger.
  Done when: the ledger holds a pre-mortem for the predicted task, and the following day's score says whether it named a real snag.

- **Wild: Keep a nightly canary against the newest Claude Code release** — FEATURE — value 3 — effort M — risk low — category: compatibility
  Why: wild. Foreman is wired through hooks and a mod (T-0418 shows the mod drifts behind). A canary installs the newest CLI in a sandbox directory and runs the roundtrip e2e.
  Done when: a new CLI version triggers `plugin/tests/e2e/roundtrip.py` in the sandbox, and a failure files one FIX task naming the version.

- **Wild: Wake the user's phone only for a real yes** — FEATURE — value 3 — effort M — risk med — category: notifications
  Why: wild. Queued installs and `fm ask` blocks need one human yes. Everything else stays quiet until morning. Only blockers that stop all lanes ping, and the ping carries the approve command.
  Done when: with all lanes blocked on one ask, one notification goes out through a user-configured channel, never twice for the same ask, and none goes out if no channel is set.

- **Hold a weekly "what did the night shift cost and win" digest** — FEATURE — value 3 — effort S — risk low — category: observability
  Why: Mission 8 #12 asks for leanness and a lean ratchet exists (T-2281). Unattended work needs the same accounting for tokens, wall time and kept work.
  Done when: `fm night report --week` prints spend, tasks closed, tasks reverted and the top trigger by kept work, with figures taken from the ledger and not re-estimated.

- **Wild: Let the night shift propose its own new triggers** — FEATURE — value 3 — effort L — risk med — category: self-improvement
  Why: wild. The signal-to-fix loop turns failure patterns into tasks. A step further reads the user's repeated manual commands and corrections and proposes "run this on push" as a queued trigger, for one yes.
  Done when: a command the user ran by hand on 3 or more separate days becomes a queued trigger proposal with its evidence, and approving it creates a working trigger.

Next question: What happens to the night's work when the user's morning steer contradicts it, and is the reverting path as cheap as the starting path?
Next question: Which unattended actions could reach outside the machine (push, comment on an issue, post a status), and does each need a durable grant rather than a per-run yes?

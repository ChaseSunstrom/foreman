# Brainstorm — lens: unspoken needs

- **Converge the brainstorm into epics** — FEATURE — value 5 — effort M — risk low — category: planning
  Why: the "ideas so far" list runs to roughly 400 entries with heavy overlap, and T-0432 is a planned task. The user will drown in it. Assumption: they want a roadmap, not another list.
  Done when: `fm ideas --converge` reads all ideas, merges duplicates, and writes 5–8 epics. Each epic has a thesis, a dependency order, a value/effort score taken from `fm taste`, and a queued brief for the first slice. Running it twice yields stable epic ids.

- **Learn the user's request dialect** — FEATURE — value 5 — effort M — risk med — category: intake
  Why: the user's phrasing repeats: "Foreman 1.2.x: … to GitHub main and JARVIS", "Release 1.2.N", "Checks the product the way its user uses it". Each phrase carries an unstated procedure and a downstream project. Assumption: the phrases mean the same thing each time.
  Done when: Foreman keeps a project phrase map (phrase → task type, tail steps, target projects) built from the ledger. A terse request expands into a one-line echo ("Release 1.2.17 → bump, changelog, push main, install into JARVIS") that the user can veto. A correction updates the map.

- **Arm tasks on external conditions** — FEATURE — value 5 — effort M — risk low — category: blockers
  Why: T-0316 waits on a Claude Code update, T-0325 on a `pacman` package, T-0352 and T-0418 on outside actions, and T-0336 on live agents. Blocked tasks currently just sit.
  Done when: a blocked task can carry a machine-checkable unblock probe, such as a CLI version change, a binary on PATH, a release tag, or a file appearing. A poller, run in drive or `fm night`, flips the task to ready and says why. Tasks that only need the user get one copy-paste checklist.

- **Keep a promise ledger from the agent's own words** — FEATURE — value 4 — effort M — risk low — category: follow-through
  Why: the user said cleanup requests "never got done". Agents also say "I'll follow up on X" or "left Y for later" in final messages and then lose it. Existing ideas cover the user's asks, not the agent's commitments.
  Done when: Stop-hook output is scanned for commitments and each becomes a captured brief linked to its source task. In a seeded test, a "will do later" sentence appears in the inbox. Closing a task with an unfiled promise warns.

- **Isolate each lane's runtime** — FEATURE — value 4 — effort L — risk med — category: lanes
  Why: lanes are worktrees only. Parallel builders on JARVIS-style web projects will collide on dev-server ports, scratch databases, lockfiles, and shared `node_modules` symlinks (the symlink-rm complaint). Assumption: collisions occur but are not yet logged.
  Done when: `fm lane new` assigns a port range and per-lane env vars (`PORT`, `DATABASE_URL` suffix, tmp dir). Two lanes run the same smoke test concurrently without clashing. `lane rm` frees the resources.

- **Supervise long-lived processes** — FEATURE — value 4 — effort M — risk med — category: processes
  Why: drive work on "long-lived jobs never leave a session idle" and "a foreground wait loop is refused" shows background processes are common. Nothing tracks which dev servers or watchers Foreman started.
  Done when: a registry records pid, command, task, and health. `fm ps` lists it. The next task reuses a healthy server instead of starting another. Orphans are reaped at task done. The drive can name a job as "waiting on X" with its log tail.

- **Keep an assumption register that reopens work** — FEATURE — value 4 — effort M — risk med — category: judgement
  Why: with `autonomy=full`, Foreman decides without asking, and later steers ("budget limits shouldn't block until 75%") may contradict earlier assumptions. Nothing links the two.
  Done when: each task's assumptions are stored with tags. When a new steer or decision matches a tag, Foreman lists the finished tasks built on the old assumption and offers to queue a re-check. A seeded contradiction produces that list.

- **Cross-check each request against the whole inbox** — FEATURE — value 3 — effort S — risk low — category: intake
  Why: the user sends many small, related asks (guard hints, drive idleness, lane merge). Related ones are sometimes fixed as separate patches in the same area. Assumption: `fm relate` covers ordering but not merging fixes.
  Done when: at capture, an open or recent task touching the same file or rule is named. A "fold into T-X?" prompt is offered, and batch mode accepts it.

- **Explain the release delta per consumer** — FEATURE — value 3 — effort M — risk low — category: releases
  Why: each release is pushed to GitHub and JARVIS, and the user relays JARVIS's complaints by hand. Assumption: they would rather see which of JARVIS's logged refusals or idles each release removes.
  Done when: the release note lists, per registered consumer project, the guard refusals, idles, and errors from that project's last 7 days that the release fixes. It shows "none" when there are none.

- **Wild: Walk-and-talk intake** — FEATURE — value 3 — effort M — risk med — category: voice
  Why: wild; assumption: the user thinks of requests away from the keyboard.
  Done when: a voice memo sent from the phone surface is transcribed locally into the inbox. Foreman reads back its classification and one clarifying question, and a spoken "yes" captures the brief.

- **Wild: Dead-man's-switch succession** — FEATURE — value 3 — effort M — risk med — category: autonomy safety
  Why: wild; `autonomy=full` plus night runs means Foreman may keep acting while the user is gone for days. Assumption: the user would want that bounded.
  Done when: after a configurable silence (for example 5 days), risky grants lapse and night runs shrink to read-only work. A handover bundle is written covering state, open asks, and what ran. The user's next message restores everything.

- **Wild: Resurrect a dormant project** — FEATURE — value 3 — effort M — risk low — category: onboarding
  Why: wild; Foreman manages many projects, and some will sit for months. Assumption: the user will reopen old ones.
  Done when: `fm resurrect` reruns the gates and smoke test on the old commit and compares the result with the last recorded evidence. It reports what rotted (dependencies, toolchain, flaky gates) and queues a first "get green" task.

- **Wild: Hold a weekly regret review** — FEATURE — value 3 — effort S — risk low — category: reflection
  Why: wild; the user's drops show strong YAGNI instincts (the guard-loosening decision, the "-k" criterion).
  Done when: each week Foreman picks the 3 shipped features or rules with the most refusals, overrides, or zero uses. It argues for or against keeping each, and the user's verdict is recorded as a decision and feeds the taste model.

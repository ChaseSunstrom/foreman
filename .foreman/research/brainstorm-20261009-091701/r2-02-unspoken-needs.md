# Brainstorm — lens: unspoken needs

- **Wake sessions on events, not polling** — FEATURE — value 5 — effort L — risk med — category: drive
  Why: the user asked for "long-lived jobs and an empty queue never leave a session idle," then for a foreground wait loop to be refused, then for the drive to offer queued work during background jobs (T-0401). All three are patches around one gap: Foreman has no job registry. Background jobs, lanes, CI runs and deploys would register with an expected duration, a liveness probe and a completion trigger. The session then sleeps at zero tokens and the job's exit wakes it with the result already attached.
  Done when: a 10-minute background job started in a test session wakes the session within 5 s of exit, with no polling tool calls in the transcript, and a job that dies silently is reported as dead.

- **Fail over a task to another harness when quota runs out** — FEATURE — value 5 — effort L — risk med — category: autonomy
  Why: the user cares about pace (T-0320, "no blocking until 75%"). The Codex, Gemini and opencode adapters, `fm session` and the resume point already exist. Together they could carry a task to another agent when Claude usage is exhausted, instead of idling. Assumption: the user would rather make progress on a weaker model than stall overnight.
  Done when: with Claude quota simulated as exhausted, `fm run` continues the active task in a configured second harness from the exact checkpoint step, and the ledger records the handoff.

- **Treat user frustration as a trigger for process root-cause** — FEATURE — value 4 — effort M — risk low — category: learning
  Why: the user said "cleanup requests … never got done — trace why and fix," and also "again"-style complaints about repeated refusals. Foreman fixes the symptom each time. A phrase detector over inbox text (never, again, still, twice, keeps) would open a "why did the process fail" task. That task would trace which gate, brief or drive path let it slip, and fix the process rather than only the instance.
  Done when: capturing "X still isn't done again" creates a linked RESEARCH task whose output names the earlier task IDs and the process step that let X slip.

- **Batch everything that needs the user into one deadline-defaulted digest** — FEATURE — value 4 — effort M — risk med — category: asks
  Why: `fm ask` grants, `?` items, L-plan approvals and T-0317-style "new feedback" notes are separate interruptions today. Each approval arrives as its own ask. One ranked card list would give each item a recommended default and a deadline, and could be answered in one reply from any surface. Unanswered items past their deadline take the default if it is low-risk, otherwise they stay blocked.
  Done when: three pending asks appear as one digest, one reply resolves all of them, and an expired low-risk item applies its default and is logged.

- **Lease files between lanes and the main thread** — FEATURE — value 4 — effort M — risk med — category: lanes
  Why: `fm lane merge` refused a dirty main checkout (T-0280 couldn't land during T-0278), and the fix compared dirty files with branch files after the fact. A lease table would claim predicted files from `fm impact` and `fm why` when a lane or task starts. Overlaps would then be seen at dispatch time, so the drive can pick non-colliding work and warn on the first conflicting edit.
  Done when: two queued tasks that touch the same file are not dispatched concurrently, and two disjoint ones are.

- **Detect contradictions among vetoes, lessons, decisions and rules** — FEATURE — value 4 — effort M — risk low — category: consistency
  Why: rules accumulate from many places (vetoes, lessons, `fm decide`, working rules, the YAGNI call on loosening the brief gate). The pack shows decisions being re-litigated through new asks. A checker would flag pairs that conflict or that a newer decision silently supersedes, and surface them in `fm doctor`.
  Done when: seeding a veto "never edit X" and a decision "edit X freely" makes `fm doctor` report the pair with both sources.

- **Spot repeated guard refusals and stop the loop** — FIX — value 3 — effort S — risk low — category: guard
  Why: JARVIS got "fm focus … ; sed -i" refused twice in a row, and the fix was a hint. The general pattern is that the same refusal category fires twice within a session on near-identical commands. After the second hit the guard should show the exact permitted rewrite and log a friction event for `fm friction`.
  Done when: two consecutive refusals with the same cause produce a message containing a runnable corrected command, and a friction record is created.

- **Show which fixes each downstream project is missing** — FEATURE — value 4 — effort M — risk low — category: fleet
  Why: the user ships every release to "GitHub main and JARVIS" by hand and relays JARVIS friction back. Foreman could track the version installed in each project and map each friction event, still open in a consumer, to the release that fixes it. Upgrade proposals would then say "1.2.12 fixes the symlink refusal you hit twice."
  Done when: `fm projects` lists each project's version and, for one with a known open friction event, names the fixing release.

- **Steer running lanes with live messages** — FEATURE — value 4 — effort M — risk med — category: steering
  Why: the user's steers (Tauri, "no limits until 75%") arrive mid-flight, often while builders run. Each message would be classified as amend, append, cancel or unrelated, and routed to the right lane's brief as a recorded change instead of landing in the main thread's context.
  Done when: a message "also handle empty input" sent while a lane runs appears as a dated amendment in that lane's brief and the builder sees it at its next checkpoint.

- **Test the handbook with a cold-start agent** — FEATURE — value 4 — effort M — risk low — category: docs
  Why: `MASTER.md`, `fm export` and `fm map` claim a new session can pick up the project. Nothing measures that claim. A fresh child would get only Foreman's artifacts and try a small seeded task, and the failures it hits become doc fixes.
  Done when: `fm audit cold-start` runs a no-memory child on a canned task and reports the first point where it needed information that no artifact contained.

- **Wild: Keep a "second user" journal that argues for the user's absent preferences** — FEATURE — value 3 — effort M — risk low — category: taste
  Why: wild; assumption: preferences the user has never stated outnumber the stated ones. At planning time, Foreman would ask "which options has this user historically rejected for projects like this?" and cite specific past steers. This goes beyond the existing taste portrait by doing the lookup at the moment of choice.
  Done when: a plan with two options shows a one-line "you previously dropped X in T-nnnn" note on the one that matches a recorded drop.

- **Wild: Let a brief be "released" like software, with a rollback** — FEATURE — value 3 — effort L — risk med — category: lifecycle
  Why: wild; the user's release habit shows they think in versions. Each finished task would be recorded as a revertable unit: code, state and lessons. `fm undo T-0412` would revert the commit and the Foreman side effects (briefs, decisions, changelog), and reopen the task with a note on why it was rolled back.
  Done when: `fm undo` on a finished test task restores the prior tree, reopens the brief, and removes its changelog line.

- **Wild: Hand each queued task a "who would be annoyed" check** — FEATURE — value 3 — effort S — risk low — category: impact
  Why: wild; every JARVIS complaint came from a change that was correct in Foreman but broke a consumer's habit. Before a task is dispatched, a child would list the downstream workflows the change touches (commands, refusals, UI states) using usage data and consumer sessions, and attach that list to the brief as acceptance probes.
  Done when: a brief for a guard change lists at least one real replayed consumer command it could affect.

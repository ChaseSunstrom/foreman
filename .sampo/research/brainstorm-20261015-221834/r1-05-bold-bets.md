# Brainstorm — lens: bold bets

- **Ship a portable "playbook pack" that travels in git and self-heals** — FEATURE — value 5 — effort L — risk med — category: learning
  Why: the user asked that fixes work for any project and travel with git (project fixes in the repo, machine-wide ones in Foreman state); T-1032 shipped hints, but the pack is not yet a versioned, mergeable unit.
  Done when: `fm pack export` in repo A writes `.foreman/pack/` and a fresh clone of A, with no Foreman state, offers a recorded fix on the same obstacle, and a conflicting merge of two packs resolves by confidence.

- **Resume any stopped agent from a durable run manifest** — FEATURE — value 5 — effort M — risk low — category: resume
  Why: the first request is easy resume of stopped worktree agents (T-1028 is only planned). Assumption: each spawn can write a manifest (task, brief, branch, worktree, last tool call, step) before it starts.
  Done when: after `kill -9` on a builder session, `fm resume` lists it with its brief and branch, and picking it up continues in the same worktree with the brief re-injected and no step repeated.

- **Auto-route repeat obstacles to the known fix before the model tries anything** — FEATURE — value 5 — effort M — risk med — category: self-improvement
  Why: the user asked why Foreman doesn't "detect an issue and automatically go that path next time". Offering a fix is weaker than applying it. Assumption: fixes carry a signature (error regex plus command) and a safe replay.
  Done when: a seeded error signature triggers the stored fix automatically in a test, the ledger records "applied, passed", and a failed apply demotes the fix's confidence.

- **Score Foreman's own improvement per week** — FEATURE — value 4 — effort M — risk low — category: self-measurement
  Why: the user asked "why have you not really improved all that much?" and there is no number to answer with. Assumption: the ledger already holds first-pass rate, retries, time to close and repeat-obstacle counts.
  Done when: `fm trend` prints week-over-week first-pass rate, repeat-obstacle rate and median close time, and the pane shows one sparkline of it.

- **Add a recursion governor to the super-brainstorm loop** — FEATURE — value 4 — effort M — risk med — category: orchestration
  Why: the user wants build, review, brainstorm, repeat "until dry", and T-0829 (drop lenses that run dry) is deferred. Without a stop rule, rounds waste money. The budget line in this pack ($25) suggests a cap is needed.
  Done when: a loop run ends on its own when a round's accepted-idea rate falls below a set threshold or the budget is spent, and prints which lenses went dry.

- **Rank backlog by evidence, not by age** — FIX — value 4 — effort M — risk low — category: backlog
  Why: Open Work holds about 30 "Later from T-07xx/08xx" deferrals with no due date. Assumption: failures, user asks and ledger hits can be linked to tasks.
  Done when: `fm next` shows each deferred item's evidence count, and an item with three linked recurrences is promoted automatically.

- **Share learned fixes between machines with a trust handshake** — SECURITY — value 4 — effort M — risk high — category: sharing
  Why: the user wants other sessions, clones and teammates to use fixes. Auto-applied fixes from a clone are a prompt-injection and supply-chain route (T-0791 is deferred). Assumption: packs can be signed.
  Done when: an unsigned or modified pack's fix is shown but not auto-applied, and a test shows a poisoned hint is refused.

- **Wild: Add a "sleep mode" where Foreman works the queue overnight in worktrees and leaves a morning receipt** — FEATURE — value 5 — effort L — risk high — category: autonomy
  Why: wild; builds on T-0793 (overnight work), resume and the ledger. The morning receipt lists what closed with proof, what stalled and what needs you.
  Done when: a queued task set run with a time box produces one summary file with per-task proof, and a killed run resumes from the manifest.

- **Wild: Replay old failures as a regression suite for Foreman itself** — FEATURE — value 4 — effort L — risk med — category: evals
  Why: wild; T-0035 (`fm eval capture`) is deferred. Every past obstacle becomes a case, so a new rule or card must not regress the old ones. This is also the proof that "genuinely improving" is real.
  Done when: `fm eval run` replays at least 20 captured failures against the current rules and reports which ones are still caught.

- **Wild: Hand off a running worktree agent between machines with a git ref** — FEATURE — value 3 — effort L — risk med — category: portability
  Why: wild; resume plus git travel. Pushing `refs/foreman/run/T-xxxx` carries the manifest, brief and branch, so a laptop can pick up a desktop's stopped builder.
  Done when: on a second clone, `fm resume --from origin` restores the brief and branch of a run created on the first.

- **Wild: Let the user vote on a fix with one keypress in the pane** — FEATURE — value 3 — effort S — risk low — category: feedback
  Why: wild; confidence in learned fixes (T-0217) needs a human signal that costs almost nothing. Assumption: the pane takes key events.
  Done when: pressing a key on an offered fix records up or down in the ledger and changes its confidence, shown in the pane.

- **Detect a stalled agent and resume it before you notice** — FIX — value 4 — effort M — risk med — category: reliability
  Why: the pack's own incidents include harness stalls at the folder-trust prompt and the Stop hook driving a screenshot session into the queue. Assumption: a heartbeat file per agent exists or can be added.
  Done when: an agent with no tool call for N minutes is flagged in the pane, and with `--auto` it is restarted from its manifest once, then escalated.

- **Retire a fix when it stops working** — FIX — value 3 — effort S — risk low — category: learning
  Why: fixes learned once will go stale as tools change (for example, `claude` found through `~/.local/bin`). Assumption: the ledger tracks applied-then-failed.
  Done when: a fix that fails twice in a row after being applied is marked stale and no longer auto-applied, and `fm doctor` lists it.

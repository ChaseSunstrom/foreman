# Brainstorm — lens: user value

- **Keep one warm hook daemon** — PERFORMANCE — value 4 — effort M — risk med — category: performance
  Why: every tool call pays process start for the hooks. `bench_hooks.py` exists, T-2605 caught a waiting hook, and T-0832 (shell prefilter) is deferred. Assumption: Python startup dominates p95.
  Done when: `bench_hooks.py --runs 20` shows PreToolUse p95 at least 40% lower with the daemon up, and hooks give identical verdicts with the daemon killed (fallback to cold start).

- **Run only impacted tests in the ship gate, full suite nightly** — PERFORMANCE — value 4 — effort M — risk med — category: speed
  Why: every push goes through `fm ship` gated by the full suite, with 404 test files under `plugin/tests`. The map already holds a tests→src relation.
  Done when: a one-file change runs under 20% of the suite in `fm ship`, and a nightly full run flags any failure the impacted set missed, with the miss rate shown in `fm doctor`.

- **Cache prove results by tree hash** — PERFORMANCE — value 3 — effort S — risk med — category: speed
  Why: re-proving after a no-op amend or rebase reruns the same commands. Assumption: the run record stores the command and exit code.
  Done when: a second `fm task prove` on an identical tree prints "reused run <id>, N min old" and runs nothing. Any changed file reruns it, and the receipt still links the original run.

- **Show Foreman in the editor status bar** — FEATURE — value 4 — effort M — risk low — category: devices
  Why: the pane and mod live only in the Claude Code terminal, while the README says IDE users exist and Codex, Gemini and opencode users have no pane. Assumption: a state file or `fm status --json` can be polled.
  Done when: a VS Code extension shows the current task, stage and guard-block count, and clicking a task id opens its receipt.

- **Spike two approaches in parallel lanes and keep the smaller proof** — FEATURE — value 4 — effort M — risk med — category: agents
  Why: the Genesis rule says a failed spike gets 2+ different approaches, and T-0792 (fleet lanes) is deferred. The 30+ "Later from" deferrals are mostly unspiked.
  Done when: `fm spike T-xxxx --approaches 2` runs both in separate worktrees and prints a side-by-side of proof pass, diff size and cost. The loser is archived with its reason and only the winner touches main.

- **Rehearse tonight's plan before the user leaves** — FEATURE — value 4 — effort M — risk low — category: agents
  Why: `fm night` runs unattended, and the standing rules say never block on the user and wait out limits. The user approves outcomes only after the fact. Assumption: the night tick can run with dry-run semantics.
  Done when: `fm night --rehearse` prints the ordered tasks, the expected cost and the three riskiest steps from a scratch clone. The approved list is what the real tick runs, and the tick refuses anything not on it.

- **Cap interruptions per day** — FEATURE — value 3 — effort S — risk low — category: simplicity
  Why: `fm ask`, Foreman-filed inbox items and doctor warnings all compete for the user's attention. The steers show repeated pushback on noise (the round-first hold, the pasted-key skip).
  Done when: a daily interrupt budget (default 5) holds non-urgent asks into one digest. `fm doctor` shows asked vs held, and an urgent item still passes.

- **Let `fm doctor --fix` apply the safe repairs** — FEATURE — value 3 — effort M — risk med — category: developer experience
  Why: doctor names many problems (missing steer checks, stale timers, version skew), and the user then types each fix by hand. Assumption: most warnings map to one known command.
  Done when: `--fix` runs only repairs tagged reversible, prints each command before running it, and a second doctor run is greener. Anything irreversible is listed, not run.

- **Quiz the user on a big diff (wild)** — FEATURE — value 3 — effort M — risk low — category: understanding
  Why: assumption: with agents landing 2,600+ tasks, the user's grasp of their own repo erodes silently. The user model and sealed predictions already show interest in modeling the human.
  Done when: after any task over 200 changed lines, `fm quiz` asks 3 questions drawn from the diff. The score is logged, and a streak of misses prompts a walkthrough task.

- **Probe each blocked task against today's world (wild)** — FEATURE — value 3 — effort S — risk low — category: unblock
  Why: T-0325 needs libappindicator, T-0335 to T-0337 wait on adapters and T-0418 on a version bump. Some blockers may have cleared since they were filed.
  Done when: a nightly probe re-tests each blocker's stated condition (package present, CLI version, release exists) and moves any cleared task to ready with the evidence line.

- **Open the whole queue as one offline HTML file (wild)** — FEATURE — value 3 — effort S — risk low — category: devices
  Why: assumption: the user checks progress from a phone. A synced folder (Syncthing, Dropbox) needs no server, no port and no cloud API.
  Done when: `fm export brief --html <dir>` writes a single self-contained file with queue, morning brief, open asks and last-night receipts. The file works in a phone browser with no network, and `fm night` refreshes it.

- **Meter the ceremony tax per task** — FEATURE — value 4 — effort S — risk low — category: value
  Why: T-1231 (beat Claude Code on the duel), T-1266 (ceremony profile per task kind) and T-0795 (seconds/tokens at close) are all deferred, so the user can't see what Foreman's process costs. Foreman's pitch is discipline, and a visible price lets the user judge it.
  Done when: each finish receipt shows plan, prove and review as minutes and tokens beside the edit time, and `fm doctor` ranks task kinds by tax so ceremony can be dropped where it never caught anything.

- **Rebuild `fm map` incrementally** — PERFORMANCE — value 2 — effort S — risk low — category: speed
  Why: the map reads "2117 files, as of an older HEAD", so it goes stale and a full rebuild is costly. Assumption: file hashes are cheap to compare.
  Done when: a one-file change re-maps in under a second and the map's HEAD matches the working tree.

Next question: Which of Foreman's per-call or per-task costs (hook latency, ceremony minutes, interruptions) does the user actually notice, and is there any measurement of it from their side?
Next question: Which Foreman surfaces does the user open daily, and which do they only run because a task told them to?

# Brainstorm — lens: bold bets

- **Verify the verifier with mutation proof** — FEATURE — value 5 — effort L — risk med — category: verification
  Why: A criterion's verify used `-k a or b`, which run.py ignores, so it ran no tests yet counted as checked (T-0342). Evidence is only as good as the check behind it.
  Done when: `fm task done` mutates the task's diff (flips conditions, drops lines) and fails any criterion whose verify command still passes on a mutant. A test with a no-op verify is rejected.

- **Compile criteria into red-first executable checks** — FEATURE — value 5 — effort L — risk med — category: verification
  Why: `fm oracle` already derives behaviour examples from the spec alone, and PR output reports red→green. Joining them lets the criteria become tests before any code exists.
  Done when: a task with acceptance criteria cannot leave planning until each has a generated check that fails on the pre-change tree. The brief records the red output.

- **Race competing builder lanes on L tasks** — FEATURE — value 4 — effort L — risk med — category: orchestration
  Why: Lanes in git worktrees already exist, and L items sit deferred (T-0034, T-0035). Assumption: sampling several approaches beats one plan on hard tasks.
  Done when: `fm lane race T-x --n 3` starts three lanes with different approach briefs. A judge scores gates, diff size and review verdicts, and merges one winner. The other lanes are archived with their reasons.

- **Sweep leftovers after every task** — FEATURE — value 4 — effort M — risk low — category: hygiene
  Why: The user steered that cleanup requests (dead code, docs, briefs, replaced functionality) never got done. Nothing creates the work.
  Done when: after `done`, `fm sweep` lists symbols, docs and briefs orphaned by the diff and queues a cleanup task for each. A seeded replaced function shows up in the next sweep.

- **Run a shadow CI daemon on every edit** — FEATURE — value 4 — effort M — risk low — category: feedback speed
  Why: T-0214 (edit-time test sentinel) is deferred, and `fm map` already links tests to source. Assumption: failures caught at edit time cost fewer turns than failures caught at the gate.
  Done when: after an Edit, the linked tests run in the background and a failure is injected into the next turn's context within the bench-measured latency budget. Hook overhead stays inside `bench_hooks.py` limits.

- **Ship a one-command release train** — FEATURE — value 4 — effort M — risk med — category: release
  Why: Releases 1.2.8 to 1.2.16 were each a separate request to push to GitHub main and JARVIS. The steps are identical every time.
  Done when: `fm release` bumps the version, writes the changelog from merged tasks, runs the gates, tags, pushes to the configured targets and installs into the downstream project. It asks once before the push.

- **Detect scope drift against the brief** — FEATURE — value 3 — effort M — risk low — category: focus
  Why: Foreman's core promise is staying on the current task. Today the guard checks commands, not whether the diff matches the brief.
  Done when: before commit, hunks unrelated to the brief's files and goal are flagged and offered as captured inbox items. A test diff with an unrelated edit produces a capture.

- **Plan the day against usage pace and learned task cost** — FEATURE — value 4 — effort M — risk low — category: scheduling
  Why: The user cares about pace, with budget limits inactive until 75% usage and subagents never capped by tokens. `fm cost` already has per-task history. Assumption: effort and cost are predictable from type, size and touched files.
  Done when: `fm drive` orders the queue by predicted cost against remaining pace and shows the estimate. Predicted versus actual error is reported by `fm digest`.

- **Replay whole task runs deterministically and fork them** (wild) — FEATURE — value 4 — effort L — risk high — category: time travel
  Why: wild. Transcripts, ledger events and checkpoints exist, but a bad plan at step 2 means redoing everything. Forking from a recorded step with a revised plan would make it cheap.
  Done when: `fm fork T-x --at step 2` restores the tree and context from the checkpoint into a lane and continues with a new plan. The original run stays intact.

- **Judge risky commands by running them in a sandbox** (wild) — SECURITY — value 4 — effort L — risk high — category: guard
  Why: wild. Guard refusals on parse alone are the user's repeated JARVIS complaints (symlink `rm`, `fm focus ;` chains). T-0275 wants the guard to read what scripts run.
  Done when: an ambiguous command runs in an overlay-filesystem namespace and the guard allows or blocks it on the observed writes. A seeded `rm` of a symlink is allowed, and a script that deletes outside the repo is blocked.

- **Red-team the guard nightly with an adversary agent** (wild) — SECURITY — value 4 — effort M — risk med — category: guard
  Why: wild. Real bypasses (`bash -lc`, braces hiding writes, `python -c`) keep surfacing from field use. `fm night` and the real-bash differential tests are already there.
  Done when: a night job generates 500 bypass candidates, diffs the guard's verdict against real bash effects, and files each divergence as a FIX task with a failing test.

- **Pre-answer questions from a taste model while the user sleeps** (wild) — FEATURE — value 3 — effort L — risk med — category: autonomy
  Why: wild. `fm taste` already holds kept, dropped and steered choices, and `fm ask` grants are mid-run stops. Assumption: many asks repeat and can be predicted.
  Done when: `fm night` replays the day's asks and proposes standing yeses ranked by predicted acceptance. The user approves them in one batch. Accepted ones stop prompting afterward.

- **Dispatch lanes across machines with queue leases** — FEATURE — value 4 — effort L — risk high — category: multi-machine
  Why: `fm serve`, `fm projects` and `fm session` handle this device only. The user asked for multi-machine work in the ambition, and the drive idled with 20+ queued tasks.
  Done when: a second host claims a lease on a queued task, works it in a lane, and returns the branch and evidence. The primary merges it. A dead lease expires and the task returns to the queue.

- **Score lessons by whether recall preceded a clean pass** — FEATURE — value 3 — effort M — risk low — category: learning
  Why: T-0217 is deferred. `fm bench` and `fm evolve` can already prove whether a lesson helps.
  Done when: each lesson carries a confidence that rises when its recall preceded a first-time pass. Low-confidence lessons are flagged for `fm evolve --drop`.

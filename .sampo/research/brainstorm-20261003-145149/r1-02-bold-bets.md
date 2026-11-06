# Brainstorm — lens: bold bets

- **Prove skills and playbooks earn their load with an ablation run** — PERFORMANCE — value 4 — effort M — risk low — category: dead weight
  Why: usage shows 46 of 46 playbooks never read and the skills never invoked (used as rules only). Nothing yet proves that deleting them changes behaviour. Replay 5 canonical tasks with and without each, compare outcome and tokens.
  Done when: `fm ablate` prints a per-file verdict (keep / delete / inline) from paired replays, and at least one never-read playbook is deleted with no change in outcome.

- **Rank context fill by Read and Bash, then enforce a read budget** — PERFORMANCE — value 4 — effort M — risk med — category: token cost
  Why: Read fills 59% and Bash 34% of context, with a 27k median at first reply. Nothing caps ranged reads. Suggest `offset`/`limit` when a Read exceeds N lines and the task scope names a symbol. Assumption: the PreToolUse hook can see the file size cheaply.
  Done when: a replayed session with a large-file Read yields a ranged-read hint, and median first-reply-to-done context on 5 recorded tasks drops by at least 10%.

- **Prove the self-improvement loop with a held-out friction suite** — FEATURE — value 5 — effort L — risk med — category: RSI
  Why: the user asked for recursive self-improvement via subagents, but nothing shows a pass made Foreman better rather than bigger. Freeze past friction events as fixtures, and accept a self-change only if the suite improves and `fm replay` has no verdict change.
  Done when: `fm rsi` rejects a deliberately neutral change and accepts one that fixes a recorded friction, each with a printed score delta.

- **Compile each user complaint into a golden-frame test at capture** — FEATURE — value 5 — effort M — risk low — category: UI regression
  Why: the user repeats UI complaints (unpanelled rows, duplicated dashboard, diff contrast, a `$` not animated) in round after round. Assumption: the mod can render a row to text deterministically. A "looks wrong" capture stores the row type and state as a snapshot case.
  Done when: running the capture command with a complaint adds a failing snapshot, and the fix turns it green in the 59-test mod suite.

- **Stop the drive loop for mod reloads by reloading between turns** — FIX — value 3 — effort M — risk med — category: drive
  Why: friction shows 5 drive stops for mod reloads and 7 for background waits. Defer a reload until the Stop hook fires, carrying a resume token, so the reload never interrupts a turn.
  Done when: a scripted session that installs a new mod build mid-queue continues to the next task with zero manual prompts.

- **Wild: Let a night shift spend leftover weekly quota on speculative replay** — FEATURE — value 4 — effort L — risk high — category: autonomy
  Why: wild. The user is quota-sensitive. A forecast of unused weekly budget could fund read-only agents that pre-plan queued tasks and mine friction, stopping at a hard cap. Assumption: usage is readable from transcripts.
  Done when: with a cap of X tokens, the shift writes plans for at least 2 queued tasks, never edits the tree, and halts at the cap.

- **Wild: Point a two-model adversarial duel at the guard** — SECURITY — value 4 — effort M — risk low — category: guard
  Why: wild. The guard has had a long run of bypass fixes (heredocs, backticks, keywords). One read-only agent writes bypass candidates, a sandbox runs them in bubblewrap, and misses become differential test cases.
  Done when: a run yields N novel candidates, and any bypass found is added to the differential test before the fix lands.

- **Wild: Hand the user a "regret ledger" they can scan in 10 seconds** — FEATURE — value 3 — effort S — risk low — category: trust
  Why: wild. Pushback is the best ground truth (the rm denial, "this doesn't match", and so on). One panel lists what the user rejected or corrected, each with the rule or test it produced, or "no change yet".
  Done when: `fm regret` lists each recorded steer with a linked artifact, and flags those with none.

- **Make time-to-first-useful-action a gated metric** — PERFORMANCE — value 3 — effort M — risk low — category: speed
  Why: the cost split shows the model at 55% of active time and shell at 45%, with python3 at 14%. Measure per turn from the transcript, and fail a self-improvement pass if the median regresses.
  Done when: `fm cost` prints the median and p90 per turn, and a seeded slow change fails the pass.

- **Wild: Show the user a one-image "state of the build" on return** — FEATURE — value 3 — effort M — risk med — category: UI
  Why: wild. The user judges the UI by sight and the mod cannot be screenshot by the agent today. A throwaway tmux renders the mod headlessly and saves a PNG or ANSI dump, which becomes the golden frame source above.
  Done when: `fm snap` writes a frame for each row type without typing into the user's own terminal.

- **Give verify commands a purity and runtime estimate at plan time** — FIX — value 3 — effort S — risk low — category: gates
  Why: the 22 s suite and pass reuse show gate time matters. Record each verify command's median runtime and show the plan's total in the brief, so slow plans get trimmed before execution. Assumption: runtimes are already in the ledger.
  Done when: a brief lists an estimated gate time per criterion, within 30% of the measured value on 5 past tasks.

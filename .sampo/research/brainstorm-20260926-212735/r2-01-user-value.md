# Brainstorm — lens: user value

- **Write a plain-language outcome report at task done** — FEATURE — value 5 — effort S — risk low
  Why: the user never runs commands and doesn't read diffs, but the pack only surfaces evidence to gates, not to the person. Assumption: today they see raw Stop-hook output.
  Done when: `fm task done` writes `report.md` of ≤10 lines (what changed, how it was verified, what to eyeball, tokens spent, unverified assumptions), and the Stop hook prints it once.

- **Checkpoint at focus and offer a one-yes/no `fm undo`** — FEATURE — value 5 — effort M — risk med
  Why: full autonomy with yes/no-only consent needs a cheap safety net. The guard blocks dangerous commands but nothing reverts a bad but allowed task. Assumption: the project is usually a git repo; fall back to a file snapshot of scope globs otherwise.
  Done when: after an edit in scope, `fm undo` restores the tree to the focus-time checkpoint (out-of-scope files untouched) and the test passes with and without git.

- **Record each task's read/edit set and seed the next related task with "Start here" files** — PERFORMANCE — value 4 — effort M — risk low
  Why: recall gives related briefs, not the files that mattered, so the ground step re-explores each time. The pack names tokens burned as the top complaint. Assumption: PostToolUse can see Read/Edit paths.
  Done when: at focus, a task with a recall hit lists ≤5 files with outlines. A replay test shows fewer Read calls in grounding than without seeding.

- **Learn standing approvals from repeated yes answers** — FEATURE — value 4 — effort M — risk med
  Why: consent is yes/no prompts, and repeated identical approvals are turns and interruptions. Assumption: approvals are logged by category.
  Done when: after 3 identical yeses, Foreman asks once "always allow X in this project?". A yes stores a scoped standing rule, which `fm doctor` lists and can revoke. Standing rules never cover the guard's dangerous-command list.

- **Re-run finished tasks' verify commands as a regression sentinel** — FIX — value 4 — effort M — risk low
  Why: the pack already matches recurring failures to finished tasks, but only after the user hits them. Each done task holds machine-runnable criteria that could catch it earlier. Assumption: verify commands are stored structured.
  Done when: `fm check --sentinel` runs the criteria of the last N done tasks (cached by tree hash, timed). Breaking one flags "task X's criterion Y regressed" at the next SessionStart in ≤1 line.

- **Make injected prefixes byte-stable to hit the prompt cache** — PERFORMANCE — value 4 — effort S — risk low
  Why: SessionStart text and per-turn notes may embed volatile data (times, counts, reordered queue) that breaks caching. Assumption: unverified, but cheap to test.
  Done when: a test renders SessionStart twice with no state change and gets identical bytes. Volatile fields go after the stable block, and `fm doctor` reports the stable-prefix length.

- **Batch queued tasks by scope overlap in `fm run`** — PERFORMANCE — value 3 — effort M — risk med
  Why: each headless task starts a fresh `claude -p` and re-reads the same files. Tasks with overlapping scope globs could share a warm session and one audit read. Assumption: overlapping tasks are common in a queue.
  Done when: two tasks touching the same files run in one session and `fm cost` shows lower combined tokens than separate runs. Each task still keeps its own gates and evidence.

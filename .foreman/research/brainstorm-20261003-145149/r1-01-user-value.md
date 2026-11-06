# Brainstorm — lens: user value

- **Make the 46 never-read playbooks load on demand through `fm next`** — FIX — value 4 — effort S — risk low — category: playbooks
  Why: usage shows 46 of 46 playbooks never read and skills never invoked, so that text is dead weight. Inject a playbook's single relevant line only when its task type and step match, then count whether it was followed.
  Done when: a FIX task at step "reproduce" has `fm next` output naming one playbook line, and `fm usage` shows a nonzero read count for it.

- **Cap Read output at focus with a "start here" outline** — PERFORMANCE — value 5 — effort M — risk med — category: tokens
  Why: Read fills 59% of context and the median first-reply context is 27k tokens, while the user is usage-sensitive (a 20% weekly burn once). Offer symbol outlines with line ranges for large files before a full read.
  Done when: on a replayed session, a >800-line file read drops to an outline plus a range read, and `fm cost` shows lower Read tokens on the same task.

- **Add `fm cost --budget` that warns mid-session at a user-set weekly share** — FEATURE — value 5 — effort M — risk low — category: usage
  Why: the user burned 20% of their weekly quota in one session and asked for "token efficient"; drive mode keeps going with no brake. Warn once at 50% and 80% of a per-session share and let drive pause at the cap.
  Done when: with a 1k-token test cap, drive stops with one "budget reached" line and `fm status` shows the cap and the usage so far.

- **Turn each user complaint into a mod render regression fixture** — FEATURE — value 4 — effort M — risk low — category: ui-quality
  Why: the user repeatedly says things "aren't in panels", "duplicated", "don't match". Capture the complained-about frame as a fixture on `fm capture` and fail the mod tests if any row type lacks a panel owner.
  Done when: a test enumerating every row type fails when one is rendered unpanelled, and passes on the current mod.

- **Lead each finished task with a one-line "what changed for you" chip** — FEATURE — value 3 — effort S — risk low — category: communication
  Why: the user wants quiet replies and a clean look. `fm task finish` already has the audit, lesson and commit, so derive a single outcome line from them and have the reply panel show it first.
  Done when: finish output starts with one line under 100 chars, and the reply panel renders it above the details.

- **Attach the complaint text to every self-improvement fix and score whether it recurs** — FEATURE — value 4 — effort M — risk low — category: self-improvement
  Why: the user wants recursive self-improvement with a measurable "better", and the loop now waits at least 2 h between passes. Link each fix to its source friction event and let `fm friction` show recurrence after N sessions.
  Done when: `fm friction` lists each fix with "recurred: yes/no since commit X".

- **Auto-resume drive after a mod reload or background wait without a stop** — FIX — value 4 — effort M — risk med — category: drive
  Why: drive stops 5 times for mod reloads and 7 times for background waits since the last pass. Have the Stop hook detect a pending reload or background job and return a short wait-and-resume instead of ending the turn.
  Done when: a simulated reload and a background completion each produce zero drive stops in the hook test.

- **Wild: Add a "Foreman rewind" that replays a finished task as a 15-second panel animation** — FEATURE — value 3 — effort L — risk low — category: delight
  Why: wild; the user cares about animation and the look. The ledger already has timestamps, steps and evidence, so a replay can show each step landing with its ✓ or ✗.
  Done when: `fm replay-task T-NNNN` draws steps and evidence in order within 15 s and exits cleanly.

- **Wild: Let a "fresh eyes" subagent screenshot the mod in tmux and file looks-wrong tasks** — FEATURE — value 4 — effort L — risk med — category: ui-quality
  Why: wild; the user's complaints are visual and the mod tests are not. A read-only agent in its own tmux captures the frames, lists the unpanelled or duplicated regions and queues briefs. The user's terminal is never touched.
  Done when: a run on a deliberately broken mod build files at least one brief naming the broken region.

- **Wild: Hold a nightly "regret court" that re-judges the day's guard blocks and user "no" answers** — FEATURE — value 3 — effort M — risk med — category: guard
  Why: wild; `fm friction` already rechecks past blocks with today's guard. Extend it to classify each no or block as true-block, false-positive or taste, and propose a rewrite hint only for false positives, never loosening the guard on its own.
  Done when: the nightly report lists each block's class, and no guard rule changes without a replay pass.

- **Fold `fm cost`'s time split into a per-task "where it went" line at finish** — FEATURE — value 3 — effort S — risk low — category: speed
  Why: cost now shows model 55% and shell 45% (python3 14%, fm task 7%). The user wants faster, so print the top two sinks for that task at finish and flag when `fm` commands exceed 15%.
  Done when: finish output includes "time: model X%, shell Y% (top: …)" and the flag appears in a test with a slow fm command.

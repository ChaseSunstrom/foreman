# Brainstorm — lens: user value

- **Run only affected tests while iterating** — PERFORMANCE — value 5 — effort M — risk med
  Why: the ~100 s full suite runs after every small change, and `fm impact` plus the test↔source map already exist. Mechanism: `fm check --affected` runs the mapped tests for the changed files. The full suite runs once, at the close gate.
  Done when: a one-file change runs a strict subset of tests, and `fm done` still refuses to close without a full-suite pass.

- **Skip subagent review for low-risk work** — PERFORMANCE — value 5 — effort S — risk med
  Why: each review costs 50-100k tokens. Mechanism: a deterministic pre-audit that checks criteria evidence, diff size and whether hot files or gates are touched. An S-tier task with a clean pre-audit skips the subagent, and it escalates on a size or hot-file threshold.
  Done when: an S-tier task with a small diff closes with zero subagent spawns, and a diff touching a gate file still triggers the review.

- **Give the reviewer a diff packet, not the repo** — PERFORMANCE — value 4 — effort M — risk low
  Why: reviewers re-read whole files. Mechanism: `fm audit --packet` emits ≤6k chars of diff hunks, criteria with their evidence and the related lessons. The reviewer prompt says to open files only for a specific doubt.
  Done when: measured reviewer tokens drop ≥40% on three comparable audits, with no new missed findings on a seeded-bug fixture.

- **Auto-record evidence in the Stop hook instead of nudging** — PERFORMANCE — value 4 — effort M — risk med
  Why: the evidence-gate nudge forces an extra model turn. Mechanism: when the criteria's verify commands are known, the hook runs `fm check` itself (bounded by a timeout) and records the result. It blocks only on real failure.
  Done when: a task with unrecorded but passing criteria closes with no extra turn, and a failing one is still blocked with the failure output.

- **Add `fm cost` to measure where tokens go** — FEATURE — value 4 — effort M — risk low
  Why: the user's complaint is 20% of weekly usage, and the token sinks in the pack are anecdotal ("observed this session"). Mechanism: hooks log the chars Foreman injects per event. Assumption: transcript JSONL has usage fields that `fm cost` can read for per-task tokens. It prints the top 3 sinks per task.
  Done when: `fm cost` on a finished task prints injected chars by hook and the top 3 sinks. Later rounds can cite before and after numbers.

- **Guard large reads with `fm outline` and summarized output** — PERFORMANCE — value 4 — effort M — risk low
  Why: whole-file reads and large tool outputs are named token sinks. Mechanism: `fm outline FILE` lists symbols with line ranges. A hook nudge fires for files over N lines. Test and command output through `fm check` is cut to failures plus a tail.
  Done when: reading a 2000-line file via outline plus a targeted range costs <15% of the chars, and passing-suite output is ≤10 lines.

- **Inject deltas only, not the same state every turn** — PERFORMANCE — value 3 — effort S — risk low
  Why: the per-turn "Next" (≤400 chars) and SessionStart (≤2k chars) repeat unchanged content. Mechanism: hash the injected block and skip it when unchanged since the last turn. SessionStart omits sections already covered by the always-on rules.
  Done when: two consecutive turns with no state change inject 0 chars the second time, and post-compaction resume still injects the full brief.

- **Add a fixed-format close-out summary** — FEATURE — value 3 — effort S — risk low
  Why: verbose status replies are a named sink. Mechanism: `fm done` prints a ≤6-line summary (outcome, evidence, lesson) that the rules tell Claude to relay as-is.
  Done when: the final reply on a closed task is ≤6 lines and includes the lesson for M/L tasks.

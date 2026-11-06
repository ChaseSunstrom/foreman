# Brainstorm — lens: invented: the session that can read its own map

- **Slice the map to the open task** — FEATURE — value 5 — effort M — risk low — category: context
  Why: The pack lists SessionStart injecting 2,733 characters twice, and "Map (2358 files)" is global, not task-shaped. The map already holds tests→src, gates and stack cards, so `sampo map --for T-id` can cut them down to one task. Injecting that at task pickup instead of session start moves the cost to where it is used. Assumption: task pickup runs through a path that can emit context.
  Done when: Starting T-xxxx on a fixture repo emits a slice under 600 characters that names the gate command and the tests for the files in the task's brief, and SessionStart itself emits only a pointer.

- **Rewrite an oversized Read into the matching section** — FIX — value 5 — effort M — risk med — category: context
  Why: MASTER.md is 75,758 tokens and Read refuses it, so the session wanders. "Guide with an outline" only helps after the refusal. A PreToolUse hook could instead return updated input (offset/limit) for the best-matching shard, using the anchors and the session's last query.
  Done when: With MASTER.md sharded, a Read of the whole file by a test session is turned into a Read of one section of at most 8k tokens, and the ledger records the rewrite.

- **Mine wandering into map lines** — FEATURE — value 4 — effort M — risk low — category: map telemetry
  Why: Assumption: a run of 4 or more Read/Grep calls with no edit before the first useful hit means the map failed. Log (query, final path) pairs in the hook ledger. Promote a pair to a map line only if it recurs across sessions, and evict the map lines that never shortened a search. This is evidence-driven and grows the map by exception.
  Done when: Replaying 20 recorded sessions yields a ranked list of at most 10 promote/evict candidates, each with its count of wasted calls.

- **Recall from my own pre-compaction transcript** — FEATURE — value 4 — effort S — risk low — category: continuity
  Why: After compaction a session re-runs a 4-minute test because it lost the output. The transcript is still on disk, and the pack lists cross-session recall but not this-session recall. `sampo recall --here "failing test"` would return the exact lines, with the turn number.
  Done when: In a session compacted after a failing `pytest`, the verb returns the failure lines verbatim and the session does not re-run the suite.

- **Resume with bookmarks, not a re-read** — FEATURE — value 4 — effort M — risk low — category: resume
  Why: T-2900 closes the work a dead process left open, but the new process starts blind. At Stop, write the (file, section, reason) set the session had narrowed to. On `source=resume`, inject those pointers only.
  Done when: A killed-and-resumed fixture session opens with at most 5 bookmark lines and edits the same file without a MASTER or map read.

- **Preview the Ward rules for this repo before they bite** — SECURITY — value 4 — effort S — risk low — category: guard
  Why: "Teach at the block" explains only after a denial. `sampo ward here` would list the rules that could fire given the cwd, protected paths and the repo's remotes, in at most 5 lines. This keeps the guard visible while the prose shrinks.
  Done when: In a repo with a protected path, the verb prints the rule that would block a write there, and a test confirms the actual Ward blocks it for that same reason.

- **Resolve the map per worktree and commit** — FIX — value 3 — effort S — risk low — category: correctness
  Why: Lanes run in worktrees on other trees. Assumption: the map cache is keyed by repo, so a lane may read a map of another HEAD. `sampo map --at <rev>` plus a key of (worktree, HEAD) would fix that and make the map reproducible.
  Done when: Two worktrees on different commits with a file renamed between them each print a map that matches their own `ls`.

- **Sign every map claim with the check that earned it** — CLEAN — value 3 — effort M — risk low — category: trust
  Why: The mission says "every claim checked on the machine". Give each map and injection line an optional `verify:` command that ship runs, with the result stored as `checked-at`. A line that fails is dropped from the injection and listed in `doctor`.
  Done when: Breaking a path named in the map makes `sampo doctor` red and removes that line from the next SessionStart output.

- **Run the cartographer lane** (wild) — FEATURE — value 4 — effort L — risk med — category: agents
  Why: Wild. An unattended sub-agent holds only the injected map and gets 20 navigation questions ("where does the drive count running agents?"). Ground truth comes from grep. It scores steps-to-answer, then proposes map patches that a second child verifies. It acts as the exam for the lean-vs-useful tradeoff: cut a map line and see whether the score drops.
  Done when: One run prints a score per question, and removing a known-critical map line lowers the score.

- **Answer "where is X" from a local map oracle** (wild) — FEATURE — value 3 — effort M — risk med — category: privacy, local
  Why: Wild. A local model (qwen3.8-27b) answers location questions from an index of anchors and symbols, so cloud context never carries the lookup. Every answer must come back as file:line, and a grep must confirm it before it is returned. Assumption: the model switch cost of about 3 minutes is paid once, so the oracle stays warm.
  Done when: 10 location questions return confirmed file:lines with zero Claude tokens spent on the lookup, and an unverifiable answer is returned as "not found".

- **Show a session minimap with a you-are-here dot** (wild) — FEATURE — value 3 — effort M — risk low — category: delight, UI
  Why: Wild. Render one status-line strip of the repo's layout (plugin/skills, tests, lib, site) as cells. Cells light up where this session read or edited, and the dot marks the current file's area. Cold cells with a co-changer edited nearby blink faintly. It shows context spend as geography instead of a number.
  Done when: The strip renders at 80 columns, respects reduced motion and NO_COLOR, and updates after a tool call in a recorded session.

- **Print a map-version stamp the model can echo** — CLEAN — value 2 — effort S — risk low — category: continuity
  Why: After compaction the session cannot tell whether its remembered map is current. A 6-character hash in the per-turn line (replacing the 48 to 76 characters now sent) lets the model detect staleness and re-pull only when it changes.
  Done when: Changing a map input changes the hash on the next turn, and the unchanged per-turn line is shorter than today's.

Next question: Which of the map's lines have ever been followed by a tool call that touched the path they named, and what does the answer say about what the session actually needs?
Next question: When the map and the Ward's rules both shrink, what is the smallest guard-plus-map card from which a cold session can still reach every verb?

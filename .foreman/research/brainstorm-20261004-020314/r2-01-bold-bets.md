# Brainstorm — lens: bold bets

- **Compile the brief into a proof-carrying done-claim** — FEATURE — value 5 — effort M — risk med — category: trust
  Why: assumption: the "done report" is prose today. Every review pass found real issues the model's own report missed. Make `fm done` emit a machine-checked manifest (criterion → run id → file hashes → diff hunks). The closer can only cite entries that exist, and any claim without a manifest line is stripped.
  Done when: a done report citing a criterion with no matching ledger run is rejected by `fm done`, and a unittest covers it.

- **Add a negative-space check: what the diff did not touch** — FEATURE — value 4 — effort M — risk low — category: review
  Why: the first adversary pass missed the whole git exec-channel class. Reviewers read what changed, not siblings that should have. Using the repo map, list sibling parsers, handlers and tables beside each edited symbol (same module, same call pattern) and have the reviewer say per sibling "needs the same change, or why not".
  Done when: editing one of two parallel handlers in a fixture repo makes `fm audit` list the untouched sibling with a verdict line.

- **Teach the guard by differential replay against git's own manual** — SECURITY — value 4 — effort M — risk low — category: guard
  Why: pass 1 found exec channels by hand, one class at a time. A generator that walks `git help -a` and each command's option list to flag options taking paths or commands turns that into an enumerated, tested surface, and flags new options after a git upgrade.
  Done when: `fm doctor` reports the count of git options classified read/write/exec and fails on an unclassified option from the installed git.

- **Make verification adversarial to itself with verify-command mutation** — FEATURE — value 4 — effort M — risk med — category: evidence
  Why: the guard tests passed for the wrong reason, and a verify command can be a silent no-op. After a criterion goes green, revert or mutate the touched code in a scratch copy and require the verify to go red. If it stays green, the criterion is marked "vacuous".
  Done when: a criterion whose verify is `true` or tests unrelated code is flagged vacuous in `fm check`, and one with a real test is not.

- **Wild: Run a persistent "opposing counsel" that argues against each brief before the first edit** — FEATURE — value 4 — effort M — risk med — category: planning
  Why: wild; the review findings are almost all edge cases and premises. A tool-less child gets only the request and criteria and must write three concrete inputs where the criteria pass while the user's intent fails. The inputs become candidate oracle cases the user can accept with one word.
  Done when: `fm task new` on a fixture request stores at least one counter-input, and accepting it adds a criterion with a verify command.

- **Wild: Offer a time-boxed "walk away" contract** — FEATURE — value 5 — effort L — risk high — category: autonomy
  Why: wild; the user keeps asking for multiple recursive passes and the drive waits are the main interruption. `fm away 3h --budget $8` freezes the grants, scope and risk categories in force, runs the queue, parks every real decision with a default, and writes a single return note. It will not cross the guard, push or publish.
  Done when: a dry-run of `fm away` on a fixture queue ends with every task closed or parked, a return note, and zero outward actions in the ledger.

- **Wild: Let Foreman learn the user's taste from the diffs they hand-edit afterwards** — FEATURE — value 4 — effort L — risk med — category: preference
  Why: wild; the user's steers are already data, but the stronger signal is what they change after Foreman finishes. Diff the closed commit against the later working tree, cluster the edits (naming, comment density, error style) and propose a one-line rule each, which the user accepts or declines. Accepted rules become bench judge rubric lines.
  Done when: a fixture where a file is hand-edited after close yields a proposed rule that cites the diff hunk.

- **Add a pass-over-pass duplicate collapse for brainstorms** — CLEAN — value 3 — effort S — risk low — category: ideas
  Why: the "ideas so far" list repeats the same ten themes (flaky gates, atomic state, MCP server, research cache) in many wordings. Embed titles with the existing BM25, cluster, and pass children only a cluster label plus the best title. This cuts prompt size and forces new ground.
  Done when: running the collapse on the pack's idea list gives under 60 clusters, and each pass prompt contains one line per cluster.

- **Wild: Keep a cheap "tripwire twin" that re-runs the last N finished tasks' verify commands at session start** — FEATURE — value 4 — effort M — risk low — category: regression
  Why: wild; a crash broke `git diff` and `fm doctor` passed, so nothing checks that finished work still holds. The sentinel in the inbox is the same idea. Sample several finished tasks, rerun their verify commands under the budget, and show a one-line pane card on drift. I'd merge sentinel into this and cut the separate item.
  Done when: breaking a file a finished task depended on makes session start print that task's ID with its failing criterion.

- **Cut or merge three inbox items into the proof-and-judge pipeline** — CLEAN — value 3 — effort S — risk low — category: inbox
  Why: the inbox overlaps heavily. Merge bench judge, debate-pair review and shadow plan review into one "second opinion" step with a model and rubric parameter. Merge the second-Foreman daily review into the tripwire twin. Cut the skill duels (the skill-adoption trial covers them).
  Done when: the inbox lists the merged items with reasons, and no two open items share a done-when check.

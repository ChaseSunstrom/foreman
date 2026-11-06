# Brainstorm — lens: unspoken needs

- **Cache gate results by tree hash** — PERFORMANCE — value 5 — effort M — risk low — category: gates
  Why: gates cost 18.8 hours, and one project's `cargo test` runs ~8 min about once per task. Many runs re-test an identical tree (retries, reverts, audit fixes that touch only docs).
  Done when: a second `fm check` on an unchanged tree (same git tree hash plus gate command) returns the cached pass in under 1 s and says "cached @<hash>"; any file change forces a re-run.

- **Run only affected tests first, full suite once at close** — PERFORMANCE — value 5 — effort M — risk med — category: gates
  Why: the user said "it takes hours". Per-task `cargo test` at 8 min is the biggest measured block. Assumption: the changed-file-to-test mapping can be derived per project (cargo `-p`, pytest `--testmon`, or a configured command).
  Done when: a task's mid-flight check runs a scoped command in under 25% of the full-suite time, and `fm task finish` still requires one full pass recorded for the final tree.

- **Run gates in the background while the next step starts** — PERFORMANCE — value 4 — effort M — risk med — category: concurrency
  Why: close-out takes 42 of 125 hours. Gates and audit reviewers are serial waits, though reviewers are read-only and could overlap with tests. Assumption: the gate does not mutate the tree.
  Done when: on a task with a slow gate, audits and gate start together, and wall time for close-out is at most max(gate, audit) plus 5 s on a measured sample.

- **Show a "where did the hours go" receipt per task** — FEATURE — value 4 — effort S — risk low — category: transparency
  Why: the user keeps saying Foreman is slow, but they can't see why. The measurement exists only as a one-off analysis. A per-task receipt turns it into a habit. Assumption: the ledger has timestamps for each stage.
  Done when: `fm task finish` prints one line like "2h10m: plan 6m · exec 1h20m · gates 38m · audit 20m · bookkeeping 2m", and the dashboard shows the same.

- **Detect stale docs from the diff and propose the edit** — FEATURE — value 4 — effort M — risk low — category: freshness
  Why: the user asked that long sessions avoid "out of date information, documentation", and the compaction work covers only context. Assumption: docs name code symbols, paths or flags that can be matched against the diff.
  Done when: finishing a task that renames a flag or file referenced in README or docs lists those exact lines as "docs now stale" and adds a pre-filled doc-fix step to the plan.

- **Stamp remembered facts with a source and re-check them on resume** — FEATURE — value 4 — effort M — risk med — category: freshness
  Why: "context rot" in multi-day sessions often means a stale claim, for example "test X fails" or "file Y has function Z". Assumption: facts are recorded as text without references today.
  Done when: after a compact or resume, any fact tied to a path or command whose file hash changed is flagged "unverified" and re-checked by a cheap fm-scout lookup before being relied on.

- **Learn the user's taste profile for brainstorming** — FEATURE — value 4 — effort M — risk low — category: brainstorming
  Why: the user says brainstorms miss "things I want but don't know how to say". Their history of accepted, rejected and edited ideas is untapped signal. Assumption: accept and reject outcomes can be read from the inbox and brief history.
  Done when: a brainstorm pack includes a "you usually accept / skip" summary derived from past outcomes, and a second brainstorm shows a measurable shift in category mix toward past accepts.

- **Replay the user's pushback as regression checks (wild)** — FEATURE — value 3 — effort M — risk med — category: learning
  Why: assumption: the user corrects the same things repeatedly (quiet output, no handed commands, size words instead of letters). Those corrections currently live as prose rules. Turn each into a tiny executable check run in `fm check`, such as a lint on reply format or on the banned "L/T/M" strings in UI output.
  Done when: adding the correction "no bare S/M/L in output" creates a check that fails on a fixture containing it and passes on the current UI snapshot.

- **Dry-run the plan on a git worktree before touching the user's tree (wild)** — FEATURE — value 3 — effort L — risk med — category: safety
  Why: assumption: risky tasks like the protected core require a "yes" per task, and a throwaway worktree attempt would let the user see the diff and test result first. It would also let two independent tasks run truly in parallel.
  Done when: `fm task try` runs the plan in a temporary worktree, reports the diff and gate result, and applies it to the main tree only on approval.

- **Add a "morning after" digest for multi-day unattended runs (wild)** — FEATURE — value 4 — effort S — risk low — category: reporting
  Why: sessions last days (a 5-day Volt session) and the user is usage-sensitive but wants autonomy. On return they need what shipped, what's blocked on them, what was burned and what's next, in about 10 lines.
  Done when: the first prompt after 30 or more minutes idle shows a digest of tasks closed, decisions awaiting the user, token usage and the next three queue items, with no commands needed to see it.

- **Budget tokens per task and downshift models automatically (wild)** — FEATURE — value 4 — effort M — risk med — category: cost
  Why: "more playbooks/subagents without burning a crap ton of tokens". Fixed lookups already go to Haiku. A per-task budget estimated from history could route bookkeeping, scouting and the first audit pass to cheap models and escalate only on disagreement. Assumption: usage per task is observable via session usage.
  Done when: the ledger records tokens by role per task, and a configured budget visibly reroutes low-stakes subagents to Haiku, with a one-line note when the budget is hit.

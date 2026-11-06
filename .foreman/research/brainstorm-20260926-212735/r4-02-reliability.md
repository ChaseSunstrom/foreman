# Brainstorm — lens: reliability

- **Bind each yes/no approval to a pending-question id** — SECURITY — value 4 — effort S — risk low
  Why: the UserPromptSubmit hook parses bare yes/no replies, and "park approvals" only defers them. Nothing stops a stale or ambiguous "yes" (or "yes, but skip X") from approving a different, later action. Assumption: approvals are currently matched to the latest pending item.
  Done when: a test shows a "yes" sent after the question expires, or after a different question was posted, is ignored with a one-line re-ask. A hedged reply ("yes but…") is not accepted as consent.

- **Fuzz the task state machine against its invariants** — FIX — value 5 — effort M — risk low
  Why: the gates live in code (`focus`, `done`, queue order, one active task), but the 435 tests are example-based. Random `fm` command sequences in a temp state dir, with a seeded RNG, can catch a path that reaches `done` without evidence, or leaves two active tasks. Assumption: there is no model-based test today.
  Done when: a seeded stdlib fuzz test runs at least 2,000 random sequences and asserts "no done without gates", "≤1 active", and "canonical queue order". Any failure prints a replayable seed.

- **Give derived data a source fingerprint and self-heal it** — FIX — value 4 — effort M — risk low
  Why: the recall BM25 index, `fm map`, test↔source links and cached passes are all derived from briefs or the tree. A stale or corrupt copy silently degrades every later decision. Fsck only detects problems; it doesn't rebuild.
  Done when: each cache stores a hash of its inputs. After deleting or corrupting any cache file, the next read rebuilds it in one call and no hook errors. `fm doctor` reports "rebuilt".

- **Watchdog verify commands with process-group kill** — FIX — value 4 — effort S — risk low
  Why: `fm check` and criterion verify commands are timed but not obviously killed. A hung test server or a child process left behind can stall a gate, `fm run` or the Stop hook. Assumption: no process-group timeout exists.
  Done when: a verify command that sleeps forever is killed, along with its children, at the limit. The gate reports "timeout" (not "fail"), and no orphan processes remain.

- **Keep a last-known-good plugin snapshot with auto-rollback** — FEATURE — value 4 — effort M — risk med
  Why: `improve` merges self-modifications behind evals, but if a merged change breaks hooks in real use, a user who never runs commands can't recover. Existing latency logging and the fail-open self-monitor only detect the problem.
  Done when: after a self-merge, N consecutive hook errors or a failed smoke eval restore the previous snapshot automatically. The next SessionStart states the rollback in one line.

- **Key state to a stable project identity, not the path slug** — FIX — value 3 — effort M — risk med
  Why: state is stored under `projects/<slug>`. Renaming or moving a directory, using git worktrees, or two repos with the same basename can orphan state or merge two projects. Assumption: the slug derives from the path or basename.
  Done when: a moved repo reattaches to its old state via a root-commit or marker id, and two same-named repos never share a queue. `fm doctor` lists orphaned state dirs.

- **Label evidence by provenance and let only hook-captured evidence satisfy gates** — SECURITY — value 4 — effort S — risk low
  Why: `fm task done` demands evidence, but the agent that wants to finish can also write that evidence through `fm`. Only the PostToolUse auto-capture of a verify command's exact run is machine-observed.
  Done when: manually added evidence is stored as `claimed`. A gate requiring `observed` evidence refuses a task with only claimed evidence, and the refusal prints the verify command to run.

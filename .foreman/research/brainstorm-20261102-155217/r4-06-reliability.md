# Brainstorm — lens: reliability

- **Run compound-fault drills in pairs** — FEATURE — value 4 — effort M — risk low — category: drills
  Why: T-2648 and `fm drill` inject one fault at a time (a dropped ledger class, a torn write), but real 3am failures stack (disk full during a clock jump, torn tail plus stale lock). assumption: no pairwise drill exists.
  Done when: `fm drill --pairs` runs every pair from the fault table in a scratch home, and each pair ends with either a named reader report or a recorded "unhandled", never a traceback.

- **Diff every cache against its uncached twin nightly** — TEST — value 4 — effort M — risk low — category: caches
  Why: the slate keeps proposing caches and incremental readers (prove cache by tree hash, cold-read cache, hook verdict cache, memoised pure verbs, verified-up-to cursors, impacted-test selection). Nothing checks that a cache returns what a cold run would.
  Done when: a nightly `fm doctor --nocache-diff` runs the readers and verdicts with all caches off and on over the same ledgers, and a planted stale entry makes it name the cache and the key.

- **Hold tower files in a pending state until their cold read lands** — FIX — value 4 — effort M — risk med — category: genesis
  Why: the standing rules say every tower file gets a cold read when written and nothing is filed on a failure, and `fm genesis live` publishes to main on every tower change. A kill between "written" and "verdict recorded" could publish an unread file or lose one. assumption: no pending marker exists today.
  Done when: killing the writer at each step of write, read and verdict never leaves a published file without a verdict record, and a startup sweep resolves orphans, shown by a kill-point test.

- **Prove every alert channel delivers, and fall back when it doesn't** — FEATURE — value 4 — effort M — risk low — category: notifications
  Why: `fm ask`, the dead-man's switch and usage-limit stops all assume the user hears about them. T-0325 shows the tray is blocked, and notify-send needs a live DBus session. T-0827 covers only mail receipts.
  Done when: a weekly test ping needs an ack, a missing ack walks a ranked fallback list (bell, notify-send, file, mail), and `fm doctor` prints "channel last confirmed N days ago".

- **Make each hook time itself out before the host kills it** — FIX — value 4 — effort S — risk med — category: hooks
  Why: the pack has latency budgets and declared fail-open/closed modes, but when the host kills a slow hook the outcome is the host's choice, not Foreman's. assumption: hooks don't self-time-out today.
  Done when: a hook slowed on purpose emits its declared fail mode and a ledger record at about 80% of the host timeout, and a test asserts the host never has to kill it.

- **Single-flight every scheduled job and record overlaps** — FIX — value 3 — effort S — risk low — category: unattended
  Why: ticks, `fm genesis live` and the drive can fire again while the last run is still going (a long run, a suspend). The open question about unattended paths on a real clock isn't answered for overlap. assumption: only lock files protect against it.
  Done when: a second fire during a running job exits with "skipped: previous running (pid, age)" in the ledger, and `fm doctor` shows the longest-running job.

- **Key project state by repo identity and offer re-attach on move** — FIX — value 3 — effort M — risk med — category: state
  Why: queue, ledgers and lessons per project are likely keyed by path (the memory dir name encodes the path). A moved, renamed or re-cloned repo would look like lost tasks. assumption: keying is by path.
  Done when: after `mv repo repo2`, `fm next` says "state for this repo (root-commit id) found at the old path, re-attach?" and a test covers move, clone and symlink.

- **Run task start, finish and ship through a git-state matrix** — TEST — value 4 — effort M — risk low — category: git
  Why: the verbs are exercised against ordinary clones. Detached HEAD, shallow, sparse, submodule, worktree, `safe.directory` refusal, `commit.gpgsign` needing a pinentry, a repo `core.hooksPath` and an old git version could each hang or fail an unattended run.
  Done when: each case runs with stdin closed and `GIT_TERMINAL_PROMPT=0`, and ends in a pass or a named refusal within a deadline.

- **List ambient override variables at every unattended entry** — FIX — value 3 — effort S — risk low — category: env
  Why: T-2645 added a doctor warning for a pinned `FOREMAN_NOW`. The same trap applies to any test or debug override left in a shell profile or timer unit. assumption: other `FOREMAN_*` knobs exist.
  Done when: any set override that changes behaviour is printed at drive and tick start and in `fm doctor`, and a planted one in a unit file is flagged.

- **Measure the judges against themselves** — FEATURE — value 3 — effort M — risk low — category: cold reads
  Why: the cold-read rule was "made reliable" with a Sonnet tiebreak, but only Haiku/Sonnet agreement is measured. A FAIL that doesn't reproduce on a rerun is noise that blocks filing.
  Done when: a sample of cold reads is rerun, `fm doctor` reports the self-agreement rate per judge, and a judge below a threshold has its FAILs re-read before they block.

- **Wild: rebuild the task index from git history alone** — FEATURE — value 3 — effort M — risk low — category: recovery
  Why: wild. Commit subjects carry `T-####` ids and "Merge T-####" lines, so git is a backup of last resort if the state dir is lost.
  Done when: in a scratch home with no state, `fm rescue --from-git` lists closed task ids and titles that match the ledger's closed set on a fixture repo.

- **Wild: have a Murphy child write the 3am sequences from MASTER.md** — FEATURE — value 3 — effort M — risk low — category: drills
  Why: wild. A tool-less child that sees only the docs writes the 20 likeliest multi-step failure stories. Each becomes a drill, and the ones Foreman survives are scored.
  Done when: at least 5 child-written sequences run as drills in a scratch home with a pass/fail line each.

- **Wild: run a monthly fire drill for the human** — FEATURE — value 3 — effort S — risk low — category: notifications
  Why: wild. A clearly labelled fake incident tests whether the user sees it and knows the one command to run, which covers the open question about the first minute after a silent fail-open.
  Done when: `fm drill --human` raises a fake degraded state, and the ledger records time-to-ack, with "unacked" shown in `fm doctor`.

Next question: which of Foreman's recovery paths have only ever been tested by the process that wrote the state, and never from a cold, different-uid or different-path start?
Next question: when two reliability checks disagree (a doctor row green, a drill red), which does the user trust, and is that written down anywhere?

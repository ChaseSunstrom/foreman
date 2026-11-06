# Brainstorm — lens: reliability

- **Verify the live site after every publish** — FEATURE — value 4 — effort S — risk low — category: deploy
  Why: The last publish was pinned to a commit that a later test fix had moved past, so the check passed against stale code. Assumption: the publish step only checks that the push succeeded.
  Done when: after a publish, the fetched site's build id equals the pushed commit, and the step fails if it doesn't.

- **Run a canary model call before a queue starts** — FEATURE — value 4 — effort M — risk low — category: queue start
  Why: Assumption: a long queue finds auth or usage-limit failures only when task 1 is already half done, after the lock and the edits are in play.
  Done when: with an exhausted usage budget, `fm run` stops within 30 seconds of starting, before any task begins or any lease is taken.

- **Reject malformed brainstorm children and re-run only that lens** — FIX — value 3 — effort S — risk low — category: brainstorm
  Why: Each child must follow an exact format (10–15 ideas, a "Done when" line on each, ≤900 words). Assumption: the merge accepts whatever a child returns, so one bad child can quietly thin the slate.
  Done when: a child whose output lacks a "Done when" line is rejected at merge, and only that lens is re-run.

- **Write the backlog and journal atomically** — FIX — value 4 — effort S — risk low — category: state
  Why: Assumption: the open-work list and the run journal are rewritten in place, so a crash mid-write could leave a truncated file and lose track of open work.
  Done when: killing the process between write and rename leaves the previous file intact and readable.

- **Make `fm status` and `fm why` read without the gate lock** — FIX — value 4 — effort S — risk low — category: status
  Why: Status and explain paths queue behind the machine-wide gate lock, and a hung check in another project held it for over 40 minutes.
  Done when: `fm status` returns in under 1 second while a full `fm check` holds the gate.

- **Kill the whole process group when a check hits its deadline** — FIX — value 4 — effort S — risk low — category: process control
  Why: A hung check kept the gate held for 40+ minutes. Assumption: a deadline kills the direct child, so grandchild processes can outlive it and keep the lock.
  Done when: a check that spawns a sleeping grandchild leaves no process alive after its deadline.

- **Record reruns that pass as flakes in a ledger** — FEATURE — value 3 — effort S — risk low — category: test health
  Why: The hook bench p95 moved from about 266 ms to about 310 ms between runs on the same machine. A test that passes only on retry is currently invisible.
  Done when: a test that passes only after a rerun appears in `fm check` output with its flake count for the past 30 days.

- **Make doc-parsing tests read one generated index, not raw Markdown rows** — CLEAN — value 3 — effort S — risk low — category: tests
  Why: `test_followups` hit an IndexError when a plugin/lib row was split into a module list, and `test_help` broke when a help position shifted. Both tests read the document layout directly.
  Done when: adding or splitting a table row fails no test, and a layout change regenerates the index with no test edits.

- **Bisect a broken main automatically** — FEATURE — value 3 — effort M — risk low — category: triage
  Why: Main broke from a doc change and a snapshot test (`test_session_care`), and each was found by hand. Assumption: nothing narrows a red main to the commit that broke it.
  Done when: `fm bisect` names the first bad commit for a seeded regression within a logarithmic number of gate runs.

- **Run a nightly gate in a clean clone with an empty environment** — FEATURE — value 4 — effort M — risk low — category: CI
  Why: Local passes depend on machine state: an inherited Claude Code env var broke 10 bench tests (T-1791), and the bench depends on load. Assumption: a clean-room result is the only trustworthy one.
  Done when: each night a clean clone of main runs the gate with an empty environment, and a failure opens a task with the log attached.

- **Wild: a rollback that restores the last good site build in one command** — FEATURE — value 4 — effort S — risk low — category: deploy
  Why: Each publish replaces the live site, and recovering a bad one means a manual rebuild. Assumption: the previous build is discarded at publish time.
  Done when: `fm site rollback` restores the previous build in under 60 seconds, and the restored site's build id matches the stored one.

- **Wild: time-travel the gate over the last 30 days of commits** — FEATURE — value 3 — effort L — risk med — category: regression hunt
  Why: Some guarantees (the rules budget, the hook latency) can break quietly across many commits. Assumption: today's checks are only ever run against today's tree.
  Done when: a weekly job reruns the current checks on each of the last 30 days' commits and reports the first day any check that passed later failed.

- **Wild: a pre-mortem before each queue, with a check for each predicted failure** — FEATURE — value 4 — effort M — risk low — category: queue start
  Why: A queue fails in ways the user has already hit (lease outliving its run, gate waits, usage limits). Assumption: each failure is found by running into it, not by asking what could fail.
  Done when: before a queue starts, Foreman lists the likely failures for its tasks, and each one has a named check that runs first and blocks the start if it fails.

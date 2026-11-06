# Brainstorm — lens: bold bets

- **Fork the session at any ledger point** — FEATURE — value 5 — effort L — risk med — category: time travel
  Why: assumption: the ledger is hash-chained and lanes are worktrees, so the state needed to branch exists. Tier extreme, domain version control and physics (many-worlds). `fm fork <ledger-id>` rebuilds worktree, task state and injected context at that point and runs a different approach beside the original. Prior art: git branches and Cursor checkpoints cover files only, not agent state. Cheapest experiment: fork one closed task from its midpoint, and see if the replay reaches the same pre-edit state.
  Done when: a forked run starts from a byte-identical tree and task state as recorded at the chosen ledger entry, verified by hash.

- **Cap each close at a reviewable size** — FEATURE — value 5 — effort M — risk low — category: user value
  Why: assumption: the user's time reading diffs is the scarcest resource, and no listed idea prices it (only "charge attention" as a wild idea). Tier xhigh, domain cognitive load. A close whose diff or proof exceeds a reading budget (say 5 minutes) is split into stacked commits, each with its own proof and a one-paragraph why. Prior art: stacked-PR tools split by hand, none by reading time. Cheapest experiment: measure how many past closes exceed the budget.
  Done when: a synthetic 900-line task lands as three commits, each under the budget with a passing proof.

- **Score proofs by mutation** — FEATURE — value 4 — effort M — risk med — category: verification
  Why: the pack lists proof kinds and "null-distribution check", but not whether a proof fails when the changed code is broken. Tier high, domain manufacturing (test-fixture gauge R&R). `fm prove` mutates the diff's lines and records the share of mutants the proof catches as the stored grade. Prior art: mutmut and Stryker exist, but none feed a close gate. Cheapest experiment: run it on 20 past closes and see how many proofs catch under half the mutants.
  Done when: a planted vacuous proof grades "weak" and a real one grades "strong" in the receipt.

- **Run the user-from-the-README tester** — FEATURE — value 4 — effort M — risk low — category: docs and delight
  Why: docs and delight are listed as thin. Tier high, domain usability science. Before each release a fresh-context agent with no repo knowledge installs and uses Foreman using only the README and site, recording every point it got stuck. Prior art: usability testing with humans, none with agents as the test subject. Cheapest experiment: run it once on the current README.
  Done when: the run writes a stuck-points list, and fixing the top item makes the same agent finish the quick-start without it.

- **Declare a living intent spec and flag drift** — FEATURE — value 5 — effort L — risk med — category: user value
  Why: assumption: a user's high-level goal erodes across many small closes, and per-task briefs cannot see that. Tier xhigh, domain law (a constitution with judicial review). The goal sentence becomes a short spec; a sentinel reads each landed diff against it and reports contradictions. Prior art: none found for coding agents. Cheapest experiment: seed a spec, plant a contradicting commit, and see if it's flagged.
  Done when: a planted contradicting commit is flagged within one run, and an unrelated commit is not.

- **Undo a day with dependency order** — FEATURE — value 4 — effort M — risk med — category: reliability
  Why: assumption: warranties and drills cover failure detection, but the pack shows no single-command recovery. `fm undo --since 09:00` reverts Foreman's landed commits in reverse dependency order and runs the proofs of what remains. Prior art: git revert works one commit at a time, with no proof check. Cheapest experiment: try it on a scratch repo with three dependent commits.
  Done when: the tree after undo equals the tree before the window, and `fm doctor` is clean.

- **Pocket-approve from phone or watch** — FEATURE — value 4 — effort M — risk med — category: devices
  Why: devices are thin, and the pack has a web UI only. Tier high. A signed push shows the one-line why, proof status and blast radius, with Approve, Defer or Stop buttons; answers are logged as ledger decisions. Prior art: CI approval bots. Cheapest experiment: send the same card to a local notification and measure response time.
  Done when: a blocked task unblocks from a phone-sized page with no terminal, and the ledger records who approved.

- **Draw a blast-radius map before each task** — FEATURE — value 4 — effort M — risk low — category: security
  Why: it answers the earlier question about which spawned processes inherit authority. Before the first edit, the brief lists the files, commands and credentials it may touch, and edits outside that footprint pause the lane. Prior art: allowlists in tool configs, but none derived per task. Cheapest experiment: compute footprints for 30 past tasks and count how many stayed inside.
  Done when: a lane that edits a file outside its declared footprint stops and names the file.

- **Keep fossil tests of every fixed bug** — FEATURE — value 3 — effort M — risk low — category: reliability
  Why: assumption: the fixed-bug history is rich and unused as a regression corpus. Tier medium, domain paleontology. Each fix leaves a minimal reproduction, and a nightly run replays all of them against HEAD. Prior art: regression tests exist per fix, but not as a fast replayable corpus with age and recurrence stats. Cheapest experiment: extract reproductions from 20 past fixes.
  Done when: the nightly run lists reproductions run, with a planted old bug reintroduced and caught.

- **Wild: dream consolidation** — FEATURE — value 3 — effort M — risk low — category: learning
  Why: wild. Tier high, domain neuroscience (sleep replay). Idle quota replays the day's ledger, merges duplicate lessons, drops ones contradicted by later closes and writes a "morning note" of three changes. Prior art: memory consolidation in agent papers. Cheapest experiment: run it on one week of ledger and see if the lesson count drops with no check regressing.
  Done when: a morning note lists merged and dropped lessons, and a later session's injected context shrinks.

- **Wild: take over an open-source maintainer's inbox** — FEATURE — value 5 — effort L — risk high — category: massive scope
  Why: wild. Tier massive, domain public health triage. Foreman reads new issues, reproduces each, labels it, and opens a proven PR for the clear cases while holding the rest for the human. Prior art: GitHub bots do labels only. Cheapest experiment: replay 50 closed issues of a small repo and count reproductions.
  Done when: on a replayed set, it reproduces at least a third of the bugs and opens PRs whose proofs pass.

- **Wild: dependency upgrade autopilot** — FEATURE — value 4 — effort L — risk med — category: massive scope
  Why: wild. Tier massive, domain infrastructure maintenance. It bumps each dependency in its own lane, reads the changelog for breaking notes, fixes call sites, and lands only with passing proofs and a warranty. Prior art: Dependabot and Renovate bump without repairing. Cheapest experiment: run it on one major bump in a test fixture.
  Done when: a major-version bump in the fixture lands with call sites fixed and every gate green.

- **Wild: talk to the daily standup by voice** — FEATURE — value 3 — effort M — risk low — category: devices
  Why: wild. Tier high. A spoken two-minute briefing on what closed, what is stuck and what costs money, with a spoken reply ("defer that one") turned into a ledger action. Prior art: none found for coding harnesses. Cheapest experiment: text-to-speech of the existing digest.
  Done when: one spoken command changes a task's state and the ledger shows it.

Next question: which of Foreman's closes does the user later quietly rework by hand, and what do those share?
Next question: what would the user need to see in ten seconds to trust an unattended night run without opening a terminal?

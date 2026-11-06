# Brainstorm — lens: reliability

- **Checkpoint deliberation per stage** — FEATURE — value 4 — effort M — risk low — category: resume
  Why: assumption: a killed or usage-limited session loses readings, options and race results, because only the cell *fill* has an "atomic and resumable" idea. The standing rule is to wait out limits and resume where stopped.
  Done when: killing a session between the options and race stages, then restarting, resumes at the race, with the readings and options file byte-identical and no child re-spawned for finished stages.

- **Declare "inconclusive" when a race has fewer than two finishers** — FIX — value 5 — effort S — risk low — category: race verdict
  Why: assumption: with usage-limit pauses and capped `claude -p` children (T-0831), one surviving lane could "win" by default. That is first instinct dressed as evidence.
  Done when: a race with a planted dead lane records `inconclusive` and a depth downgrade note, and `fm task finish` does not cite it as a race win.

- **Hash-bind the race winner to the merged patch** — SECURITY — value 4 — effort S — risk low — category: integrity
  Why: assumption: no check ties the diff that was verified in the lane to the diff that lands. A rebase or hand edit between the two silently voids the evidence.
  Done when: changing one byte of the winner's patch after the verdict makes merge refuse, naming both hashes.

- **Give each race lane a private port, temp, HOME and DB namespace** — FIX — value 4 — effort M — risk med — category: lane isolation
  Why: parallel builder lanes (Missions 5-8) and an `/run/user` tmpfs children dir are in the pack. Shared ports or files are the classic source of flaky verdicts that look like a candidate's fault.
  Done when: two lanes started together, each binding the same default port and writing the same temp filename, both pass. A preflight also refuses fan-out when the tmpfs free space is under the estimate.

- **Add a lock and a concurrent-writer test for the decision and plan ledgers** — FIX — value 4 — effort S — risk low — category: concurrency
  Why: parallel lanes append to `decisions.md` and the plan/bet ledgers. Assumption: appends are not serialized, so torn lines are possible.
  Done when: 8 processes each append 200 rows to the ledger and every row parses, with none lost or interleaved.

- **Check that the picker is deterministic and order-invariant** — FIX — value 3 — effort S — risk low — category: metamorphic
  Why: assumption: the minimax-regret or rubric picker has never been fed shuffled or renamed candidates. A winner that depends on lane order is a coin flip.
  Done when: a test replays stored race results under 20 shuffles and relabelings and always gets the same winner and fragility score.

- **Check that the tier is stable under paraphrase** — FIX — value 4 — effort M — risk low — category: plan gate
  Why: the plan gate scales depth by tier, and T-2341 had to be re-scoped because of two readings of one request. Assumption: the same ask, reworded, can land in S or L and pay very different deliberation.
  Done when: 10 paraphrases of each of 12 fixture requests keep the same tier and depth for at least 11 of 12 fixtures. Each miss is listed.

- **Cache `fm graph blast` by tree hash with a timeout and an "unknown" result** — PERFORMANCE — value 3 — effort M — risk low — category: blast radius
  Why: the repo has 2072 files. Assumption: a slow or failing graph call stalls the plan gate, or worse, is read as "no blast radius".
  Done when: a second call on the same tree is under 100 ms, and a forced 30 s hang returns `unknown` within the timeout and the gate treats it as at least M risk.

- **Name the deliberation depth actually reached on the receipt** — FEATURE — value 4 — effort S — risk low — category: honesty
  Why: assumption: when budget, timeout or a dead child cuts a stage, the task still reads as "exhaustively thought". The cell fill needs a truthful field per cell.
  Done when: every closed M or L task prints `depth: asked=L reached=M (race skipped: budget)` and a test forces each cut-short path.

- **Wild: Run a metamorphic day: the host CLI updates, the canary trap task re-runs** — FEATURE — value 3 — effort M — risk low — category: drift
  Why: wild. A tool-less child writes a task whose obvious fix is wrong, and `fm night` re-runs it when the host's version string changes. This turns a host update into a measured pass or fail for the deliberation machinery.
  Done when: bumping a faked host version triggers one run, and the result lands in `fm doctor` as held or missed.

- **Wild: Hold a degraded-mode drill that cuts the network and has a child return garbage** — FEATURE — value 3 — effort M — risk low — category: chaos
  Why: wild. One scripted run per release drops the network, makes children emit truncated JSON and kills one lane. It then records the exact message the user would see at each stage.
  Done when: the drill prints a table of stage, failure and user-visible line, and no row reads "silent".

- **Wild: Run an N-version picker: two independent implementations vote on race winners** — FEATURE — value 2 — effort M — risk med — category: redundancy
  Why: wild. The picker is the single point that turns evidence into a choice. A second, simpler one (a plain pass-count tie-break) runs in shadow, and disagreement becomes the "uncertain" flag.
  Done when: on 30 stored races, disagreements are listed and each one produces a visible "pick is fragile" line.

- **Fail when a deliberation child answers with a different model than requested** — SECURITY — value 3 — effort S — risk low — category: provenance
  Why: assumption: a retired alias or fallback can swap the model with no trace. That quietly breaks "cold read by a different model" and the rival-planner separation.
  Done when: a stub child reporting a different model ID makes the stage fail and log the requested and actual IDs.

Next question: Which deliberation stages have no recorded timeout, and what does the user see when each one hits its limit?
Next question: If two lanes finish the same cell fill with different content, which one wins, and where is that written down?

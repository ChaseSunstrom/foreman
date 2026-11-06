# Brainstorm — lens: grid

**Grid used.** Surfaces are CLI (`fm`/`sampo`), hooks (session and drive paths), web UI and pane, Smith TUI, and the site. Actors are the user, the builder agent, other lanes, and the unattended drive.

- **Ideas 1–3, 5–6:** the evidence is the flat 0/6, the resume fixes, and the repeated running-set fixes.
- **Idea 4 and ideas 7–10, 12:** assumptions drawn from the rename, the local-model push and the tray ticket.
- **Ideas 11 and 13:** wild.

- **Trace the done-gate on each of the six false dones** — FIX — value 5 — effort S — risk low — category: done-gate
  Why: 6 false dones unchanged since gen 2 despite new mechanisms. Cell: hooks × agent × wrong. Assumption: nobody has checked whether the gate even fires in those runs.
  Done when: each of the 6 scenarios prints one line: gate ran y/n, clauses seen, verdict, and the first scenario where "ran: n" is named.

- **Score the long tier by clauses met, not only true/false done** — FEATURE — 4 — M — low — measurement
  Why: the binary 0/6 has not moved for two generations, so progress is invisible. Cell: CLI × user × unclear.
  Done when: `fm exam long` prints met/total clauses per scenario. A planted partial improvement raises that number while true-done stays 0.

- **Check that resuming a finished goal changes nothing** — FIX — 4 — S — low — resume
  Why: resume needed later fixes in 2 of 6 cases, and T-2900 shows resume can act on a dead session's leftovers. Cell: hooks × agent × wrong.
  Done when: a test resumes a closed goal; the ledger diff is empty, no task reopens, and nothing is spawned.

- **Carry an in-flight goal across the Foreman→Sampo migration** — FIX — 5 — M — med — migration
  Why: steers say the rename moves state with backup and undo, and a multi-day goal can span it. Assumption: the migration test fixtures hold no open goal or lease. Cell: CLI × unattended × wrong.
  Done when: start a goal under `fm`, run the migration mid-goal, resume under `sampo`. Clauses, evidence and lease are intact, and `undo` restores them.

- **Give each hook event one owner across the shim and real plugin** — FIX — 4 — S — low — hooks
  Why: the thin `foreman` and `foreman-ui` shims list `sampo` as a dependency. Assumption: both can be installed and both register Stop and PostToolUse. Cell: hooks × agent × wrong (a double fire).
  Done when: with both installed, one Stop produces one gate run and one evidence record, keyed by event id.

- **Replay real engine shapes through the drive's running-set function** — FIX — 4 — M — low — drive
  Why: T-0575, T-0115, T-2873 and T-2901 were four separate fixes to the same count. Cell: hooks × unattended × wrong and slow.
  Done when: a table of recorded `background_tasks` and event-tail samples, with expected running sets, is a test, and every past misread is a row.

- **Bisect a once-proven clause with `fm goal bisect <clause>`** — FEATURE — 3 — M — low — regression
  Why: evidence is bound to commits, so a clause that was green and is now red can be searched like a bug. Assumption: evidence commands are re-runnable. Cell: CLI × user × unclear.
  Done when: against a planted breaking commit, the verb names that commit by running the clause's own proof.

- **Constrain local builders to a grammar of goal verbs** — FEATURE — 3 — M — med — local models
  Why: the user wants local models used heavily, and qwen-class builders will mistype `fm evidence` syntax. Cell: Smith TUI × agent × wrong.
  Done when: in `sampo smith` with a local profile, a goal-verb call is decoded against a grammar and a malformed call can't be emitted. A mutation-test run shows zero parse failures.

- **Pin ambiguous goal words in a glossary every lane reads** — FEATURE — 3 — S — low — lanes
  Why: parallel lanes can read a vague goal differently. Cell: other agents × wrong.
  Done when: intake writes `glossary` entries (word → chosen reading), the lane brief includes them, and a test shows two lanes receive identical readings.

- **Run a five-sample local-model jury on every done claim** — FEATURE (wild) — 4 — M — low — verification
  Why: the free arm costs $0 against a $200 cap. Votes are cheap, and only dissent escalates to a cold Sonnet read. Cell: hooks × agent × wrong.
  Done when: against the six false dones, the jury flags at least as many as a single cold read, at zero API tokens.

- **Add a kill-and-compaction variant to `roundtrip.py`** — FEATURE — 4 — M — low — ship gate
  Why: `roundtrip.py` is already a gate, but nothing in the gate list kills or compacts mid-goal. Cell: CLI × unattended × wrong.
  Done when: the gate kills the run at each step and injects a compaction; the final ledger equals the uninterrupted run.

- **Run ambient chaos in dogfood** — FEATURE (wild) — 4 — S — med — resilience
  Why: crash handling is only exercised on drill days. Assumption: the tower's own sessions are safe to jostle. Cell: hooks × unattended × wrong.
  Done when: with `SAMPO_CHAOS=1`, about 1% of tool boundaries in the tower's own sessions SIGKILL the process. Over a week the log shows every kill resumed cleanly or filed a task.

- **Show a finish-without-you colour in the tray and pane** — FEATURE (wild) — 3 — M — low — glanceable
  Why: T-0325 blocks the tray icon. Clause progress, budget and blockers can drive one green/amber/red signal answering whether the goal will finish without the user. Cell: tray/pane × user × unclear.
  Done when: the colour is computed from the ledger alone. Backtested on 10 closed goals, red precedes the stalls.

**Cells left empty**
- Web UI × unattended: nobody is looking, so the finding belongs to the drive receipt.
- Site × agent: agents don't read the site mid-goal.
- Smith × other lanes, and every "unsafe" cell on the read-only pane: nothing new beyond the listed safety ideas.

Next question: which of the six false dones happened with the gate firing, and which with it never reached?
Next question: does a goal that spans a plugin upgrade or rename keep its lease, evidence and checkpoint, and has anyone ever run one?

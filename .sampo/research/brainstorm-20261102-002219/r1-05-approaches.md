# Brainstorm — lens: approaches

- **Triage each cell as existing, gap or n/a before writing prose** — CLEAN — value 5 — effort S — risk low — category: coverage
  Why: earlier missions found most of #2, #3, #11 and #12 already built. Assumption: Goal to finish has many built paths (goal plan, baton, ledger, finish audit) that the grid never cited.
  Done when: all 58 cells carry a tag plus a grep or file:line proof, and only the gap-tagged cells need new writing.

- **Fill cells from a kill-and-resume drill** — FEATURE — value 5 — effort M — risk med — category: durability
  Why: the capability promises survival across crashes and compactions. A cell filled from observed resume behavior is grounded, not described. Trade-off: costs session time, but the drill runs with zero tokens if it uses a scripted stub agent. Assumption: the baton and ledger can be inspected after a kill.
  Done when: a script kills a seeded goal at each stage, restarts it, and the cell cites a pass or a recorded failure.

- **Run a done-detector exam with premature-finish traps** — FEATURE — value 5 — effort M — risk med — category: exam
  Why: "knows when it's actually done rather than merely stopped" is the least provable clause. Plant goals with one silently missing contents row and check that the finish refuses. Trade-off: scenarios must come from the blind tool-less child, per the standing rule.
  Done when: a held-out set of 6 or more goals shows finish refusing every planted-incomplete goal and accepting the complete ones.

- **Do less: write columns as rules and cells as exceptions** — CLEAN — value 4 — effort S — risk med — category: coverage
  Why: the pack's templating rule bans cells with the same words and the area swapped. A per-stage rule with a per-surface exception avoids this only if each exception names a concrete path. Assumption: many web-UI cells have no separate path from the CLI. Trade-off: the rule must not be gamed into hidden templates.
  Done when: the linter passes the grid with no shingle overlap above its threshold, and every n/a has a recorded counterexample search.

- **Fill by replaying closed goals** — FEATURE — value 4 — effort M — risk low — category: backtest
  Why: the user's history of closed tasks is a signal Foreman didn't author. Replay the last 20 goals and mark which cells each one exercised. Unexercised cells become probes or are marked unreached with an expiry.
  Done when: each cell is tagged exercised, unexercised or n/a, with the task ids as evidence.

- **Drift-after-days drill for multi-day goals** — FEATURE — value 4 — effort M — risk med — category: staleness
  Why: "carries the plan over days" implies the repo changes underneath. Fake-age the goal, move HEAD, rename a cited file, then check that resume flags the stale rows instead of trusting them. Assumption: there is no staleness check on goal rows today.
  Done when: a resumed goal on a changed tree lists the rows whose cited files moved.

- **Reuse the rivals' plan formats as the contents source** — FEATURE — value 3 — effort M — risk low — category: capability map
  Why: "what a finished, best-in-class version contains" needs an outside reference. Import the structure of Spec Kit, Kiro and Devin plans as a checklist to compare against. Trade-off: it risks borrowing structure that doesn't fit Foreman.
  Done when: a vague goal's generated contents covers the rival checklist's categories, or the gap is recorded.

- **Two blind fillers, with disagreement counted as the gap** — CLEAN — value 3 — effort M — risk low — category: coverage
  Why: the standing rules favor cold reads by a different model. Where two fillers differ, the cell is probably ungrounded. Trade-off: doubles the cost, but Haiku is cheap.
  Done when: the disagreement list is filed as gap tasks, and agreeing cells pass the cold read.

- **Make goal state a harness-neutral file** — FEATURE — value 4 — effort M — risk med — category: harnesses
  Why: the standing rule says Foreman isn't Claude-specific, but hook-based resume may only work in Claude Code. Assumption: this is unproven for codex, gemini and opencode. A plain goal file readable by a prompt works everywhere.
  Done when: a second harness resumes a seeded goal from the file alone and reports the same next row.

- **Wild: sabotage-the-goal lane** — FEATURE — value 3 — effort M — risk med — category: exam
  Why: wild. A lane quietly deletes one contents row, one test, or the baton mid-goal. Score whether Foreman notices, rebuilds, or claims done anyway.
  Done when: 5 sabotage kinds each end in either a detected-and-repaired status or a recorded miss.

- **Wild: goal autopsy from git and ledger alone** — FEATURE — value 3 — effort L — risk med — category: recovery
  Why: wild. Delete all goal state in a scratch copy and rebuild the plan from commits, task ledger and decisions. If it reconstructs, the "crash survival" cells are provably redundant. Trade-off: heuristic, so it needs a backtest bar stated first.
  Done when: on 5 past goals, the rebuilt contents list matches at least a pre-stated fraction of the original rows.

- **Wild: a "finished?" court with a blind prosecutor** — FEATURE — value 4 — effort M — risk med — category: done-detection
  Why: wild. Before finish, a tool-less child sees only the goal text and the diff summary and lists what a best-in-class version would still have. Any item the plan lacks blocks finish unless waived with a reason.
  Done when: on 3 seeded incomplete goals the court names the missing piece; on 3 complete ones it passes with no blocking item.

- **Add a web UI goal board with stale and done states** — FEATURE — value 3 — effort M — risk low — category: web UI
  Why: web UI is the only surface in this run, so the stage-by-surface columns need a real page to point to. Show rows, last proof, and an age stamp, with empty, loading and error states.
  Done when: a screenshot shows a seeded goal's rows, a stale banner, and a done state.

Next question: Which of the 58 cells name a stage (plan, resume, finish) that has no session path calling it today, so that a filled cell would describe code nobody runs?
Next question: Does the goal state survive a harness switch mid-goal, and who would notice if it silently didn't?

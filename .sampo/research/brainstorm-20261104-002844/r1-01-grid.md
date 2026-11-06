# Brainstorm — lens: grid

Cells are written surface × actor × failure mode. Surfaces are the CLI, hooks (SessionStart, Stop, PreCompact), lanes and worktrees, the pane and web UI, and the site. Actors are the user, the agent, other agents and the unattended drive.

- **Resolve state from the git common dir in worktrees** — FIX — value 5 — effort S — risk low — category: reliability
  Why: cell CLI × lane agent × missing. The pack says evidence and lease commands fail inside the builder worktree the harness put the agent in, so state is probably found from cwd.
  Done when: `fm evidence` and `fm lease` run from a fresh `git worktree add` directory and write to the main repo's state, and a test fails on the old resolution.

- **Check a done claim against goal clauses, not task text** — FEATURE — value 5 — effort M — risk med — category: done-gate
  Why: cell Stop hook × agent × wrong. Long tier shows 0/6 true done with 6 false dones unchanged since gen 2, so the gate trusts the agent's summary. Intake splits the goal into numbered clauses, and each clause needs a receipt from a command run after the last edit.
  Done when: on a replayed long-tier scenario with one clause unmet, Stop refuses done and names that clause.

- **Replay planted faults on a scratch goal nightly** — FEATURE — value 4 — effort M — risk low — category: resume
  Why: cell unattended × unattended × wrong. Resume is the worst area (2 of 6 needed a later fix). A scratch goal gets a SIGKILL at each journal write, a forced compaction and a usage-limit pause, then the run must reach the same clause state.
  Done when: the drill prints one pass/fail line per fault and fails when a resume step is removed.

- **Rebuild the goal capsule after compaction under a line budget** — FEATURE — value 5 — effort M — risk med — category: resume
  Why: cell PreCompact/SessionStart hooks × agent × missing. A multi-day goal loses its clause state at each compaction. The capsule holds clauses with status, the last evidence ids, and the next command, capped at about 25 lines.
  Done when: after a forced compaction the first agent turn can name the open clauses, checked by a test reading the injected text.

- **Fence leases with a token that goes stale on crash** — SECURITY — value 4 — effort M — risk med — category: lanes
  Why: cell lanes × other agents × unsafe. A dead lane's lease can still be held, or a resumed session could write evidence under it. A monotonic fence token is checked on every evidence write.
  Done when: a killed lane's old token is rejected after another lane takes over, and the rejection is a visible block.

- **Make a cold different-model child list unmet clauses before done** — FEATURE — value 4 — effort M — risk med — category: done-gate
  Why: cell other agents × agent × wrong. The standing rules say signals Foreman didn't author count. The child sees only the goal text, the final diff and the evidence list.
  Done when: on the six known false dones it flags at least four, and the recall is reported per scenario.

- **Show clause status in the pane as proven, unproven or unmeasured** — FEATURE — value 4 — effort M — risk low — category: ui
  Why: cell pane × user × unclear. The user can't tell "done" from "agent said done". Each clause shows the evidence age, and unmeasured is not drawn green.
  Done when: a goal with one stale receipt renders that clause as unproven, covered by a UI test.

- **Mark guessed clauses and let the user strike them** — FEATURE — value 4 — effort S — risk low — category: intake
  Why: cell CLI × user × unclear. A vague goal forces assumptions that stay silent. Each assumption becomes a clause tagged `assumed`, and the user's edit wins. This differs from the earlier "ask at most three questions" idea because it asks nothing.
  Done when: a goal given as one vague sentence prints its assumed clauses, and striking one removes it from the done-gate.

- **Flag a stalled goal by clause movement** — FEATURE — value 3 — effort S — risk low — category: unattended
  Why: cell drive × unattended × slow. Days of spend can pass with no clause changing state. After N ticks with no clause change, the drive re-plans or asks once.
  Done when: a goal with a frozen clause for N ticks triggers the re-plan path in a test.

- **Mark an unreadable evidence record as "could not run"** — FIX — value 3 — effort S — risk low — category: reliability
  Why: cell hooks × agent × wrong. A failed evidence command, as in the worktree failure, can read as absent or as pass. It needs a third state that blocks done.
  Done when: an evidence call that errors leaves its clause unmeasured and a done attempt is refused.

- **Run a saboteur against the finished goal** — FEATURE — wild — value 4 — effort L — risk med — category: done-gate
  Why: wild; cell other agents × agent × unsafe. A hostile lane has a fixed budget to break the delivered behaviour with a user-like scenario, and done stands only if it fails.
  Done when: the saboteur finds a seeded defect in a planted case and passes a clean one.

- **Write a one-line will before each risky step** — FEATURE — wild — value 3 — effort S — risk low — category: resume
  Why: wild; cell journal × agent × unclear. Before a migration, push or long run, the agent writes what it intends and how to check it landed. Crash recovery reads the last will first.
  Done when: killing a run mid-step leaves a will that resume uses to verify or redo that step.

- **Send a daily goal pulse to the phone** — FEATURE — wild — value 3 — effort M — risk low — category: devices
  Why: wild; cell notifications × user × missing. A multi-day goal gives the user no signal, so each day sends "day 3, 7 of 9 proven, blocked on X".
  Done when: a mail or push test shows the message from a scratch goal with the right counts.

Cells I left empty:
- **Site × unattended and web UI × other agents:** no goal state flows through either, and the existing Genesis site publish already covers them.
- **Smith TUI × all actors:** the pack gives no evidence of a goal flow there. Wait for a failure.
- **Slow × user in the CLI:** the cost is in the drive's tick, not in what the user types.

Next question: Which of the six false dones were missed clauses, and which were clauses the agent never knew existed?
Next question: After a real compaction, what does the agent re-read first, and does the capsule beat that?

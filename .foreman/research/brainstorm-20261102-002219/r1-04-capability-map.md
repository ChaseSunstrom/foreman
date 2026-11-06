# Brainstorm — lens: capability map

- **Make "done" a re-runnable fingerprint** — FEATURE — value 5 — effort M — risk med — category: done-ness
  Why: assumption: the pack shows Goal to finish must "know when it's actually done rather than merely stopped", but no idea ties a goal's done state to something re-checkable. A Bazel-style fingerprint stores each goal row's acceptance probe plus the tree hash it passed on, so "done" goes stale when the tree moves.
  Done when: editing a file a done row's probe covers flips `fm goal status` to "stale: re-verify" for that row, and an untouched row stays done.

- **Replay the goal journal after a crash** — FEATURE — value 5 — effort M — risk med — category: durability
  Why: assumption: Temporal-style durable execution is the best-in-class model for "carries the plan over days, across crashes and compactions". An append-only step journal means resume re-reads what ran and never repeats a completed step.
  Done when: a test kills a session mid-goal at three step boundaries, and the resumed run skips every journaled step and finishes with no duplicate commits.

- **Draw a burn-up with a scope line** — FEATURE — value 4 — effort M — risk low — category: progress
  Why: assumption: Linear, Jira and Shape Up all separate "work done" from "scope grew". The pack shows no way to tell a goal that is stuck from one whose scope keeps growing. Each row added after the plan was accepted is logged with its reason.
  Done when: `fm goal status` prints done, total and scope-added counts, and adding a row after acceptance raises the scope-added count by one.

- **Cut an MVP slice with an explicit "not in this cut" list** — FEATURE — value 4 — effort M — risk low — category: planning
  Why: assumption: a plan covering a full best-in-class version needs a cut line, as Shape Up's appetite and Taskmaster's priorities do. Foreman's "complete plan" otherwise has no way to ship the first usable slice.
  Done when: a goal can be finished at a named cut, and the rows below the cut are listed as deferred in the report rather than left open.

- **Flag a goal row that has no probe** — FIX — value 4 — effort S — risk low — category: planning
  Why: assumption: Kiro and Spec Kit both require acceptance criteria per task. A plan row that no command could falsify is the main way a goal ends up "stopped" rather than done.
  Done when: `fm goal accept` refuses a plan whose row has no verify command or recorded "unprovable" reason, and the refusal names the row.

- **Compute the critical path and next unblocked row** — FEATURE — value 4 — effort M — risk low — category: ordering
  Why: assumption: "decomposed and ordered" implies a dependency DAG, and Jira and Make-style tools surface the longest chain. This lets the drive pick the row that unblocks the most work.
  Done when: given a fixture goal with a known DAG, `fm goal next` returns the row on the longest chain, and a cycle is rejected at plan time.

- **Detect goal drift against the repo** — FEATURE — value 3 — effort M — risk med — category: drift
  Why: assumption: over days, other commits or the user's hand edits can make plan rows moot or contradict them. Related ideas (flag open tasks a commit made moot) cover tasks, not goal-level rows.
  Done when: a fixture where a commit implements a planned row marks that row "possibly done" with the commit named, without closing it.

- **Declare a stuck goal, with the evidence** — FEATURE — value 4 — effort S — risk low — category: stuck
  Why: assumption: "stopped" versus "done" needs a third state. After N attempts at the same row with the same failing probe, the goal parks the row, writes the blocker to not-yet.md and moves to the next unblocked one.
  Done when: a test with a row whose probe always fails parks it after the set number of attempts and continues with an independent row.

- **Import and export goal plans as Spec Kit or Kiro files** — FEATURE — value 3 — effort M — risk low — category: interop
  Why: assumption: the goal plan is Foreman-only, yet Foreman is "the discipline layer for coding agents" across harnesses. A plain-file export lets a hookless harness follow the same plan.
  Done when: a goal round-trips through export and import with identical rows, order and probes.

- **Hand a goal off between harnesses mid-flight** — FEATURE — value 3 — effort M — risk med — category: portability
  Why: assumption: the standing rule says Foreman is not specific to Claude Code, but the pack gives no path for a goal that starts in Claude Code and continues in Codex. A baton file with done rows, current row and the next probe covers it.
  Done when: a fixture goal started under one harness's transcript shape resumes under another and reports the same next row.

- **Wild: Run a "stranger's finish line" check** — FEATURE — value 4 — effort M — risk med — category: done-ness
  Why: wild. A tool-less child that sees only the goal text and the final repo file list writes what it thinks is still missing, and the diff against the plan shows what the plan forgot.
  Done when: the check lists at least one gap on a fixture goal whose plan has a deliberately removed row.

- **Wild: Replay the goal as a ten-second timelapse** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: wild. The journal plus the burn-up already hold the whole story. A web UI page can scrub through it, showing rows lighting up and scope lines moving.
  Done when: the page renders a fixture goal's journal in order, with a scrub control and a reduced-motion fallback.

- **Wild: Make the goal's final report a claim the user can contest** — FEATURE — value 3 — effort S — risk low — category: trust
  Why: wild. The finish report lists each row's probe, tree hash and result with a one-command "contest" that re-runs just that row.
  Done when: `fm goal contest ROW` re-runs the row's probe and either confirms it or reopens the row.

- **Budget a goal in days and dollars up front** — FEATURE — value 3 — effort S — risk low — category: budget
  Why: assumption: a multi-day goal needs an estimate so the user can tell "slow" from "off the rails". The standing rule against stopping for budget means this shows cost, never halts the work.
  Done when: a goal shows a start estimate and a running actual, and exceeding the estimate by a set factor adds a note without stopping.

Next question: Which goal-plan rows do users actually edit by hand after acceptance, and does that edit stream tell us which plan fields are wrong?
Next question: When a goal's rows were all done and the user still asked for more, what did they ask for, and which plan step should have caught it?

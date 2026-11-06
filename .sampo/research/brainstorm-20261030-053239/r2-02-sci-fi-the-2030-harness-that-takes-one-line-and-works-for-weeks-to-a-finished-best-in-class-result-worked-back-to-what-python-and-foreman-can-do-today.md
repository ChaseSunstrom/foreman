# Brainstorm — lens: sci-fi: the 2030 harness that takes one line and works for weeks to a finished best-in-class result, worked back to what Python and Foreman can do today

- **Run a genie test on every done-when** — FEATURE — value 5 — effort M — risk low — category: plan quality
  Why: acceptance criteria are model-written and each is tied to a verify command, but nothing checks that a lazy implementation can't pass them. Both session arms in the last Mission "closed no scenario" while believing they were done. assumption: some criteria pass on a stub today.
  Done when: `fm goal lint` runs each criterion's verify command against an empty or stub tree, flags every one that exits 0, and a planted vacuous criterion in a fixture is flagged.

- **Compile the goal into one verify command** — FEATURE — value 5 — effort M — risk low — category: done verdict
  Why: the gap map wants a done-vs-stopped verdict and Stop-hook clauses. Today "done" is spread over briefs, the ledger and the model's say-so. One executable `fm goal verify` with exit codes done, not-done and unknown (a tool is missing) lets the Stop hook, `fm code`, MCP, CI and other agents all ask the same question.
  Done when: the Stop hook blocks "done" while `fm goal verify` exits non-zero, and the same call returns identical JSON from the CLI and the MCP tool.

- **Order tasks as a walking skeleton** — FEATURE — value 4 — effort M — risk med — category: planning
  Why: `fm queue` orders by depends_on only, so a weeks-long goal can sit unusable until its last task. assumption: layered plans are common here.
  Done when: the planner emits a `slice:` field per task, slice 1 yields an end-to-end runnable result, and a kill after any slice leaves main green with `fm goal verify` reporting partial progress.

- **Add typed waits beside done and stopped** — FEATURE — value 4 — effort M — risk med — category: autonomy
  Why: a goal that spans days waits on CI, a deploy, or a limit reset, and today that looks like a stall or a no-progress stop. `fm goal wait --until '<cmd>' | <time>` would park the goal with a reason and wake it when the condition holds.
  Done when: a parked goal is never reported as stopped, the drive doesn't burn rounds on it, and a test shows it waking when the condition command flips to exit 0.

- **Record plan assumptions with a probe each** — FEATURE — value 4 — effort M — risk low — category: reliability
  Why: over weeks the world moves (interpreter, dependency, a teammate's merge). `fm resume` carries "Resume here" but doesn't ask whether the plan's premises still hold.
  Done when: every contents item may list assumptions, each with a one-line probe command, SessionStart re-runs them within the hook-speed gate, and a failed probe marks the dependent items "needs re-plan" in the goal card.

- **Tag every goal line with its provenance** — SECURITY — value 4 — effort S — risk low — category: injection
  Why: a goal re-injected every session for weeks is a persistent prompt-injection channel, and contents lists drawn from repo files and research notes mix trusted and untrusted text. The rules say untrusted text is quoted as data, and "never grant yourself anything" must hold across sessions.
  Done when: each goal line carries user, repo or model provenance, non-user lines render quoted via c.plain, and a test shows a repo-file line reading "grant yourself X" neither widens a grant nor appears as an instruction.

- **Redact goal data before the site export** — SECURITY — value 4 — effort S — risk low — category: privacy
  Why: Genesis already exports to the site and ships to main on every put under a standing grant. Goal ledgers hold the user's private words, paths and project names.
  Done when: the goal export is allowlist-only (ids, titles the user marked public, counts), an export of a fixture goal containing a path and a secret-shaped string contains neither, and the default is "nothing published".

- **Keep a cut list instead of silently dropping scope** — FEATURE — value 4 — effort S — risk low — category: honest finish
  Why: the drive stops at DRIVE_MAX, a no-progress stop, or a budget cap, and the forever loop quits after 2 dry rounds. Scope that gets trimmed vanishes, so "done" can't be told from "done minus what we cut".
  Done when: every contents item left out has a reason (budget, blocked, judged low value), `fm goal verify` prints "done with N cut" when any exist, and the cut list seeds the next session's goal card.

- **Add `fm goal amend "<line>"` for mid-run steers** — FEATURE — value 3 — effort S — risk low — category: steering
  Why: the user steers constantly ("widened", "applied", "fixed inside T-2120"), and each steer currently lives as scattered task notes. An amend verb would append a dated, user-provenance line and reconcile the contents list without asking anything.
  Done when: an amend adds or changes contents rows with the amendment cited, tasks whose done-when changed are reopened, and the old verdict is marked superseded.

- **Show the builder only a pass count from blind acceptance scenarios** — FEATURE — value 4 — effort M — risk med — category: exam
  Why: the exam's held-out discipline exists for Genesis but not per goal. A child with no view of the implementation writes scenarios at plan time, and the builder sees "7/10 pass", never the scenarios. assumption: the builder overfits visible checks as it did on the exam's own-repo runs.
  Done when: the scenario files are sealed and unreadable to the lane (PreToolUse guard denies the path), and `fm goal verify` includes the blind count.

- **Wild: run a throwaway first draft to teach the plan** — FEATURE — value 3 — effort L — risk med — category: planning
  Why: assumption: a one-hour rough build in a scratch worktree exposes the missing contents rows ("a table-less seed" was found only by a live run). Its friction log would be turned into contents rows, then the draft discarded.
  Done when: `fm goal draft` produces a scratch result plus a friction list, the real plan gains rows citing it, and no draft file reaches the user's tree.

- **Wild: hold a plan tournament** — FEATURE — value 3 — effort L — risk high — category: approaches
  Why: when two decompositions are plausible, build the thinnest slice of each in a worktree, score both on the blind scenarios and pick by `fm decide`. It spends budget to buy certainty before the big spend. assumption: only worth it above a cost threshold.
  Done when: the loser's worktree is archived with its score, and a test shows the pick is the higher blind score.

- **Wild: print a finish-line poster** — FEATURE — value 2 — effort M — risk low — category: delight
  Why: at done, render the capability × verb × surface grid as one SVG or terminal poster, each cell linking to its evidence. The user gets a single artifact showing finished rather than stopped, and it works as the site page for the goal.
  Done when: the poster has exactly one cell per ledger row, any unproven cell renders visibly empty, and the poster can't be produced while `fm goal verify` is not done.

- **Teardown best-in-class references with citations, under a grant** — FEATURE — value 4 — effort M — risk med — category: grounding
  Why: the gap map says contents lists are model boilerplate. A user-pointed folder of docs or READMEs (or a fetch granted per URL) would become contents rows, each citing a source line.
  Done when: a row with no citation or user-words link is labeled "model-suggested" and excluded from the denominator, and no fetch happens without a grant.

Next question: when two sessions or agents advance the same goal on different surfaces at once, who owns the ledger write, and what happens to the loser's evidence?
Next question: what is the goal's honest unit of progress (tasks, contents rows, blind scenarios passed), and does the user trust a percentage built on it?

# Brainstorm — lens: approaches

Answering two earlier questions through this lens. A bad learned rule can be vetoed in one line if every plan line carries a `fm decide --check` steer, so the user's word beats statistics. The baton size limit is only known by measuring a cold-resume exam per model tier. It shouldn't be assumed.

- **Run a goal as a one-Mission tower** — FEATURE — value 5 — effort M — risk med — category: reuse
  Why: Genesis already has `step` (next action from files, resumable after any kill), `check` (coverage grid plus not-yet ledger), `put` with a cold read, `seal`, and `sweep`. Those are the planner, crash-survival and done-detector this request asks for, proven on gen 1. Trade-off: the ceremony is heavy for small goals, so add a lite profile and use it only above a size threshold.
  Done when: `fm goal "<vague line>"` creates a tower with a spec, a grid and a Mission, and `fm goal step` after `kill -9` returns the same next action as before.

- **Plan with rolling-wave fog of war** — FEATURE — value 4 — effort M — risk low — category: planning
  Why: assumption: a full plan up front is wrong for vague goals, and the "reopen" and "missed line" ideas already show plans going stale. Only the next horizon is detailed, and the rest are named fog regions, each with a spike task that must resolve it. Trade-off: the ETA is soft until the fog clears. "Done" means no fog regions and no open rows.
  Done when: a goal card lists N fog regions, and closing a spike replaces its region with concrete rows or a logged cut.

- **Do less: the plan is a task DAG plus gates** — CLEAN — value 3 — effort S — risk low — category: simplicity
  Why: `fm task` with `depends_on` and `fm check` already exist. This approach adds only a `fm goal` view that rolls up task state, and "done" means all tasks are closed and the gates are green. Trade-off: it has no completeness judgement, so it's the baseline every fancier approach must beat on the exam.
  Done when: the exam has a plain-DAG arm, and its reopen rate is reported next to the full planner's.

- **Interview with defaults and a timer** — FEATURE — value 4 — effort S — risk low — category: intake
  Why: the user's goals are vague by nature, and clarifying costs them only seconds. Ask at most 5 multiple-choice questions, each with a pre-selected default, and apply the defaults after a timeout, marked as assumptions so a later steer can overturn them. Trade-off: it interrupts an unattended run, so skip it when no one is present.
  Done when: an unanswered interview produces a plan whose assumption rows all carry "default, unconfirmed".

- **Keep the plan as an orphan git branch** — FEATURE — value 3 — effort M — risk med — category: durability
  Why: crash survival is a hard requirement. Each ledger event becomes a commit on `foreman/goals`, so the log, diffs and `blame` come free, and a resume is a checkout. This works on any harness that has git. Trade-off: commit noise, and no benefit in a non-git tree (assumption: most targets are git repos).
  Done when: deleting the state dir and running `fm goal restore` rebuilds the open goal from the branch.

- **Hand planning to the host's native plan mode and only audit it** — FEATURE — value 3 — effort M — risk med — category: reuse
  Why: Claude Code plan mode and todo lists already exist, so Foreman would only snapshot them into the ledger and gate "done" on them. Trade-off: it's host-specific, which conflicts with the harness-neutral steer, and each host's plan format drifts.
  Done when: a Claude plan-mode exit is captured as contents rows with source "host plan", and Stop blocks if those rows are open.

- **Retrieve a skeleton from finished-goal shapes** — FEATURE — value 4 — effort M — risk low — category: planning
  Why: Foreman holds a growing history of closed goals. Embed-free retrieval by tags such as new verb, new surface or migration returns the nearest finished goal's final list as the skeleton, and the model edits it rather than inventing one. Trade-off: it needs a corpus, so it's weak on the first dozen goals.
  Done when: planning a goal shaped like a finished one pre-fills at least 70% of the final rows, measured by replay on past goals.

- **Replace the plan with a greedy frontier and a dry-round stop** — FEATURE — value 3 — effort S — risk med — category: approaches
  Why: some goals ("make it best-in-class") have no knowable end. Each round runs `fm find` plus a one-lens brainstorm, takes the top-ranked item, and finishes when K consecutive rounds yield nothing proven. Trade-off: it gives no ordering or ETA, and "dry" may only mean the finders are weak.
  Done when: the loop stops after K empty rounds and the goal card shows "done by exhaustion, K=3", not "done".

- **Edit the plan on a web canvas with cut lines** — FEATURE — value 4 — effort M — risk low — category: ui
  Why: the user steers by short sentences, and direct manipulation is faster. Drag rows between "must", "later" and "cut", and each move is written as a `fm decide`. Trade-off: it's a new UI to build, and it must stay in sync with the ledger.
  Done when: moving a row in the web UI appears in `fm goal show` within 2 seconds, with a decision logged.

- **Wild: Play the goal as a stub-model dry run to find the fog** — FEATURE — value 3 — effort M — risk low — category: wild
  Why: `fm code` can run on a stub model with no claude binary (T-2173). A zero-cost pass that only simulates the loop over the draft plan exposes missing dependencies, such as a row with no verify command. Trade-off: it catches structural holes, not semantic ones.
  Done when: a plan with an unverifiable row fails the dry run with that row named.

- **Wild: Let the user's past steers write the plan's veto rules** — FEATURE — value 4 — effort M — risk med — category: wild
  Why: "Every user steer is a standing rule plus an automatic check" is already asked for. Run the draft plan against those checks before sealing it, so it can't propose what the user already banned. Trade-off: stale steers may over-block, so show which steer blocked which row.
  Done when: a draft containing a row that violates a standing rule is rejected with that rule's id.

- **Wild: Trade the plan between two vendors' models as a handshake** — FEATURE — value 2 — effort L — risk high — category: wild
  Why: assumption: a plan one model wrote and a different model can restate correctly is a better test of "complete and unambiguous" than self-review. Done when both restatements match the contents rows, otherwise it's returned for rewording. Trade-off: it costs two model calls, and the models need to be comparable.
  Done when: a deliberately ambiguous row fails the handshake and a clear one passes.

Next question: Which approach wins on the long-horizon exam tier (replayed real repos), and what reopen rate does the do-less DAG baseline set for the others to beat?
Next question: At what goal size does the tower-as-goal ceremony cost more in tokens and user minutes than the reopens it prevents?

# Brainstorm — lens: agents of agents

- **Run a standing agent court for every finished task** — FEATURE — value 5 — effort L — risk med — category: orchestration
  Why: T-0034 (`fm audit`) is deferred and `fm night` mentions a "court"; `fm audit`/`second` exist but are manual. Assumption: the court is today a single second read.
  Done when: finishing a task in a fixture repo spawns ≥3 read-only lens reviewers (correctness, security, scope-creep), each writes a structured findings file, and `fm task done` refuses while any unresolved high-severity finding lacks a rebuttal or fix.

- **Dispatch the queue as a dependency DAG across parallel builder lanes** — FEATURE — value 5 — effort L — risk high — category: orchestration
  Why: JARVIS idled with 20+ queued tasks; `fm relate` already derives build-on links, `fm lane` has worktrees, and lane merge beside dirty main was just fixed (T-0403). Nothing schedules lanes automatically.
  Done when: with 6 queued tasks (two dependent), `fm run --lanes 3` starts only independent ones concurrently, merges each after gates, and starts the dependent task only after its prerequisite lands, shown in the ledger.

- **Add an adversarial tester agent that tries to break each change** — FEATURE — value 5 — effort M — risk med — category: verification
  Why: Verification relies on recorded evidence from the same agent that built it (criterion 1 of a task ran no tests because of a bad `-k`, T-0342 context). Assumption: builders write their own verify commands.
  Done when: for a task with a seeded off-by-one bug that passes its own verify, the red-team agent produces a failing test and the task cannot close until it passes.

- **Audit the verifiers: a meta-agent checks that each criterion's verify command can actually fail** — FEATURE — value 5 — effort M — risk low — category: verification
  Why: the `-k 'a or b'` verify ran no tests and passed anyway; a checked criterion can't be edited. Mutation-style check is a natural guard.
  Done when: `fm task` refuses a criterion whose verify exits 0 both on the current tree and on a tree with the changed files reverted (or on zero tests collected), with a message naming the criterion.

- **Spawn a planner/critic/executor tournament for L-sized plans** — FEATURE — value 4 — effort M — risk med — category: planning
  Why: L plans currently ask the user; `fm second plan` uses one other model. Full autonomy mode "never asks mid-run", so plan quality becomes the only safeguard. Assumption: plans are single-author today.
  Done when: in full autonomy, an L task produces 3 independent plans, a judge agent picks or merges one with a recorded rationale in decisions.md, and the chosen plan's step list is what the brief carries.

- **Run a supervisor agent that watches live sessions and intervenes on drift** — FEATURE — value 4 — effort L — risk med — category: supervision
  Why: Foreman's core pitch is staying on task, but enforcement is hooks per session; `fm claude` can list every session and `fm session` can message them. Assumption: no cross-session watcher exists.
  Done when: a session editing files unrelated to its focused task for N turns receives an injected correction from the supervisor, and the ledger records the intervention.

- **Fork-and-race hard tasks across models and keep the gate winner** — FEATURE — value 4 — effort L — risk med — category: orchestration
  Why: adapters for codex, gemini, opencode exist (`fm agents`) and `fm bench` can compare outputs; nothing races them on real work. Assumption: budgets allow it (pace limits only bite at 75%).
  Done when: `fm race T-XXXX` runs the task in two lanes on different agents, runs gates on each, and merges only the one passing, with the other's diff archived and cost logged.

- **Make the cleanup agent a recurring janitor with proof of deletion safety** — FEATURE — value 4 — effort M — risk med — category: maintenance
  Why: the steered note says cleanup requests (dead code, replaced functionality, docs) never got done. Existing `fm docs`, `tidy` only report. Assumption: the failure is that cleanup has no owner or verification.
  Done when: after a task that replaces a function, a janitor lane deletes the now-unreferenced old code, the full gate suite plus `fm impact` shows no dependents, and a cleanup task is auto-created if it can't prove safety.

- **Let agents negotiate a shared contract before parallel lanes start (wild)** — FEATURE — value 4 — effort L — risk high — category: coordination
  Why: wild; parallel lanes editing related modules collide at merge. Assumption: conflicts are a real cost, as the lane-merge dirty-checkout fixes suggest.
  Done when: two lanes touching a shared interface first write a contract file (signatures, ownership of files); a merge-time check fails if either lane violates it, and a seeded conflicting pair is caught before merge.

- **Grow a self-writing eval from every user steer (wild)** — FEATURE — value 4 — effort M — risk low — category: learning
  Why: wild; the user's drops/steers (budget doesn't block until 75%, cleanups never done) are recorded in `fm taste`, and `fm evals`/`bench` exist. An agent could turn each correction into a regression case automatically.
  Done when: recording a steer spawns an agent that drafts a replayable eval capturing the failure; `fm bench` runs it and fails against the plugin version before the fix.

- **Run a user-simulator agent that uses the product like the user (wild)** — FEATURE — value 5 — effort L — risk med — category: product verification
  Why: wild; "Foreman checks the product the way its user uses it" and `fm smoke` runs a headless browser, but with scripted checks. An agent persona given the task's intent could explore, then report confusing flows.
  Done when: on a drained queue, the simulator runs against the built web UI for a fixture app, files at least one captured task for a seeded broken flow, and attaches screenshots.

- **Run a swarm of agents on Foreman's own friction log overnight (wild)** — FEATURE — value 4 — effort M — risk med — category: self-improvement
  Why: wild; `fm friction --every 3` does one subagent pass, and `fm evolve` ablates instruction files bench-gated. A swarm could propose several candidate instruction changes in parallel and let `fm bench` pick.
  Done when: `fm night` spawns N evolve branches from distinct friction themes, benches each, and leaves only the ones that beat baseline as ready-to-merge branches with reports.

- **Add an agent budget broker that schedules by pace, not caps** — FEATURE — value 3 — effort M — risk low — category: budget
  Why: T-0320 and the steer say limits shouldn't block until 75% usage; with many parallel agents someone must queue starts. Assumption: `fm budget` has no admission control for agents.
  Done when: with usage under 75%, ten agent spawns all start immediately; above it, new spawns queue by task priority, and the ledger shows the wait reason.

- **Give agents persistent role memory (reviewer, builder, scout) distilled from past verdicts** — FEATURE — value 3 — effort M — risk low — category: learning
  Why: T-0217 wants lesson confidence; reviewers start from zero each time. Assumption: verdicts are stored in ledger/briefs.
  Done when: a spawned reviewer's brief includes the top 5 lessons from earlier reviews of the same files, ranked by past hit rate, and a test confirms they appear.

# Brainstorm — lens: deepen: orchestration

- **Build a durable lane scheduler** — FEATURE — value 5 — effort L — risk med — category: orchestration
  Why: lanes, races, budgets, preemption and DAG dispatch are each separate ideas, and the drive idled with 20+ tasks queued. One scheduler with leases, heartbeats and a persisted job graph lets them compose.
  Done when: killing a lane process mid-task makes the scheduler reclaim the lease and restart the lane at its recorded step, with no manual command.

- **Test a speculative merge train** — FEATURE — value 5 — effort L — risk med — category: merge
  Why: `fm lane merge` refused dirty checkouts (T-0403). Lanes that each pass alone can still break together. Gate the merge of lane N on a synthetic tree containing lanes 1..N-1, and bisect when it fails.
  Done when: two lanes that pass alone but fail together are caught by `fm lane train`, and the culprit lane is named without a human.

- **Publish contracts before building** — FEATURE — value 4 — effort M — risk med — category: dependency
  Why: `fm relate` already finds which tasks build on which. A lane could first commit a contract (signatures, schema, CLI flags) plus stubs, so dependent lanes start in parallel against it.
  Done when: a task that depends on another starts in a lane before the dependency finishes, and a contract change flags it as stale.

- **Canary releases on downstream projects** — FEATURE — value 5 — effort M — risk low — category: release
  Why: nearly every release request ends "to GitHub main and JARVIS", and JARVIS surfaces most guard bugs. Before tagging, `fm replay` and `fm sentinel` run against each registered downstream project's recent sessions, and the release blocks on new refusals.
  Done when: `fm release` lists the downstream guard verdicts that changed and refuses to tag if any newly block a previously allowed command.

- **Release by flow, not by request** — FEATURE — value 4 — effort M — risk low — category: release
  Why: "Release 1.2.13" through "1.2.16" were asked one by one. Chain gates, bench, changelog, version bump, tag, push, installer smoke and downstream canary into one resumable flow.
  Done when: `fm release patch` ends at a pushed tag with a ledger entry per step, and resumes at the failed step after an interruption.

- **Turn downstream friction into briefs** — FEATURE — value 4 — effort M — risk med — category: intake
  Why: T-0403, T-0404, T-0408, T-0409 and T-0423 all start as hand-relayed JARVIS refusals. A `guard_block` event now keeps the offending command part, so a captured brief can include the repro automatically, with the guard verdict as its failing test.
  Done when: a refusal in a registered project yields a captured brief with the command and a red replay case, deduplicated against existing briefs.

- **Pair every builder with a saboteur** — FEATURE — value 4 — effort L — risk med — category: verification
  Why: reviewers read diffs, but a second lane that tries to break the change with new tests, fuzzed inputs or differential runs gives stronger evidence. The done-gate would require the saboteur to fail within its budget.
  Done when: a seeded bug in a lane's diff is caught by its saboteur lane in an eval case, and a clean diff passes.

- **Pool human interrupts across lanes** — FEATURE — value 4 — effort M — risk low — category: attention
  Why: `fm ask` grants, L-plan approvals and `?` items each interrupt separately, and the user steered toward fewer blocks. One digest with a priority order, sent when the user is present, can unblock many lanes with a single reply.
  Done when: three lanes blocked on approvals produce one combined prompt, and one reply releases all three.

- **Tune scheduling policy with bench** — FEATURE — value 4 — effort L — risk med — category: learning
  Why: `fm evolve` already ablates instruction files against `fm bench`. Log every scheduler decision (lane count, race or not, model choice, preemption) and replay them under candidate policies against finished-task outcomes and cost.
  Done when: `fm evolve --sched` proposes a policy change with a measured delta in cost or time on the replayed task set.

- **Fuzz the guard continuously (wild)** — FEATURE — value 4 — effort M — risk low — category: security
  Why: wild. The guard has real-bash differential tests and T-0275 and T-0414 show gaps keep appearing. A nightly red-team lane generates evasions, runs them against real bash, and files each divergence as a SECURITY brief with a failing case. This fits `fm night`.
  Done when: a night run files at least one reproducible divergence brief, or reports N generated cases with none.

- **Rehearse the next task while idle (wild)** — FEATURE — value 3 — effort M — risk low — category: autonomy
  Why: wild. The user hated idle sessions. A throwaway lane drafts the plan, finds the files and writes the failing test for the next queued task, then discards the code and keeps the plan, impact map and red test.
  Done when: starting a rehearsed task begins from a stored plan and red test, and the discarded lane leaves no commits on main.

- **Fork lanes from transcript checkpoints (wild)** — FEATURE — value 3 — effort L — risk high — category: time-travel
  Why: wild. Sessions resume at the exact step after `/compact`. The same checkpoint could start a "what if" lane with a different approach from that step, keeping the common prefix, and merge back the better branch.
  Done when: `fm lane fork T-x --at step 3` starts a lane that reuses steps 1-2, with ledger lineage showing the parent.

- **Auction budget to lanes by expected value (wild)** — FEATURE — value 3 — effort M — risk med — category: budget
  Why: wild. Budgets cascade and the user wants pace limits only past 75% usage. Lanes could bid for the remaining pace headroom, with bids set from task type, `fm taste` weights and past first-pass rates, so scarce usage goes to work the user values.
  Done when: with limited headroom, a high-value S task preempts a low-value L task and the ledger records the allocation reason.

- **Reconcile lane intent at merge time** — FEATURE — value 4 — effort L — risk high — category: merge
  Why: a textual conflict between two lanes can be resolved by a small agent given both briefs, both gates and the conflicting hunks. It accepts only when both gates pass on the result, otherwise it hands the conflict to the user.
  Done when: a seeded conflict between two lanes resolves with both lanes' gates green, and an unresolvable one is escalated with the briefs attached.

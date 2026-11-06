# Brainstorm — lens: bold bets

- **Compile Plans into Workflow Scripts** — FEATURE — value 5 — effort L — risk med — category: orchestration
  Why: Workflow gives deterministic multi-agent scripts, and Foreman has 0 references to it. The user asked for "orchestration of orchestrators" and for reordering related work into one task. Foreman's plan, steps, lane and batch data already describe a DAG. The constraint is real: Workflow needs the user's words each time, or a named saved workflow they ask for. So the bold form is a one-time request, "save this as a workflow", with later runs launching the saved one by name.
  Done when: `fm plan --emit-workflow T-xxxx` writes a workflow script for a 3-step batched task, and running it by its saved name executes the steps in dependency order with each step's verify result recorded in the task file.

- **Make Idle Time Impossible with a Work-Conserving Scheduler** — FEATURE — value 5 — effort M — risk med — category: autonomy
  Why: T-0758 ("make sure it doesnt sit idle like it is") is a live complaint. Earlier ideas swap the wake mechanism. This one is a policy: whenever the main thread is waiting (on a background agent, a gate, CI), Foreman picks the next queue item that has no dependency on the wait and starts it. It must use a worktree or a disjoint file set so the two lines of work can't collide. A Stop hook that finds an idle gap and a non-empty queue refuses to stop and names the item to start.
  Done when: in a test with one 60s background gate and two queued independent tasks, the transcript shows the second task started before the gate returned, and no two tasks touched the same file.

- **Bind Every Tool Call to a Step Receipt** — FIX — value 4 — effort M — risk low — category: integrity
  Why: T-0759 reports that it starts work on other steps without updating the step. Earlier ideas block drift. This one makes the step state a derived value: PostToolUse writes a receipt (step id, files touched, command) and the band shows the step inferred from the receipts. When the model's declared step and the inferred step disagree, the next prompt gets a one-line correction.
  Done when: editing a file that belongs to step 3 while step 2 is marked active changes the active step in `fm status` to 3 (or flags the mismatch) within one tool call, and a unit test covers it.

- **Add a Claude Code Release Differ That Writes Integration Tasks** — FEATURE — value 4 — effort M — risk low — category: self-maintenance
  Why: the whole request is "integrate better with new CC features", and the pack's list of unused features came from a manual grep. Nothing keeps it current. `fm doctor` would compare the live tool list and hook event list with a recorded manifest and capture a task for each new or unused item, with the capability, what Foreman does today, and a stub test. This is a durable answer to the request, not a one-off pass.
  Done when: removing one entry from the recorded manifest makes `fm doctor` report it as new and create exactly one captured task, and the second run creates no duplicate.

- **Pay for Review with a Debate Between Cheap Models** — FEATURE — value 4 — effort M — risk med — category: cost
  Why: T-0755 asks for lower-model agents, and the earlier "model ladder" ideas route by step. This one changes the review itself. Two haiku-tier reviewers with different lens prompts review the diff independently. Only the disagreements and the union of their findings go to one sonnet adjudicator. The repo already has reviewer precision tracking (T-0752) to check whether this beats a single sonnet pass.
  Done when: `fm bench` reports review cost and precision for single-sonnet vs. the debate arm on the same 20 recorded diffs, and the arm is enabled only if precision is no worse and cost is lower.

- **Keep a Warm Standby Session That Takes Over on Crash or Limit** — FEATURE — value 4 — effort L — risk med — category: resilience
  Why: the repo already has opt-in usage-limit failover (T-0751) and resume at the exact step. The bold step is a second session kept idle, with the plan and beliefs already loaded, that takes over when the primary hits a limit, hangs or dies. It would use SendMessage to be told, and a heartbeat file to detect the failure. The aim is no cold start and no lost time.
  Done when: killing the primary session mid-step makes the standby continue the same task at the same step within 60s, and the ledger shows one handoff entry.

- **Let the Phone Be the Approval Surface for Guard Asks** — FEATURE — value 4 — effort M — risk high — category: remote control
  Why: `fm ask` grants and guard blocks stop an unattended night run, and the user never wants to be handed commands. A PushNotification carries the ask, and the answer returns through an Artifact page or SendMessage. The risk is high because the guard is a security boundary: replies must be bound to one specific ask id with an expiry, and never carry broader grants.
  Done when: a blocked command triggers a push, a reply approves only that exact command once, and a reply to a different or expired ask id is rejected and logged.

- **Make Hook Cost a Budget the Hooks Spend Down** — PERFORMANCE — value 3 — effort M — risk low — category: latency
  Why: `bench_hooks.py` gates latency, but only at test time. At run time, each hook would read a per-turn millisecond budget and skip its optional work (secondary scans, advisory notes) when the budget is spent, always keeping the blocking guard checks. The band shows the spend.
  Done when: with a simulated slow disk, the optional checks are skipped and logged while the guard still blocks `rm -rf ~`, and p95 hook time stays under the existing bench threshold.

- **Ask the Last Hundred Tasks What to Build Next (wild)** — FEATURE — value 4 — effort M — risk low — category: self-improvement
  Why: the pack shows self-improvement machinery (eval inbox, give-up mining, burden metrics) that looks at failures. Nothing mines for repeated manual steps that could become a skill or hook. A scan of finished tasks would cluster repeated command sequences and user corrections, then draft a skill with a test, and queue it for review.
  Done when: running it on the task history produces at least one drafted skill with a replay test, and the draft is not installed until it is approved.

- **Run a Red-Team Twin Against Every Release (wild)** — SECURITY — value 4 — effort M — risk low — category: guard
  Why: the guard has had many hardening rounds (pipe-to-shell, heredoc writes, `python -c` imports), each found by hand. A nightly agent would try to bypass the current guard with new obfuscations, such as encodings, env tricks and symlinks, in a sandbox directory. Every bypass found becomes a captured SECURITY task with a failing test.
  Done when: seeded with a known-bypassable guard build, the twin finds the bypass and writes a failing test for it, and against the current build it writes a report listing the number of attempts.

- **Hand the Morning to a Voice or Text Briefing Artifact (wild)** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: `fm night` runs unattended, and the user reads results from a terminal. A short page, or a spoken summary through push, says what shipped, what is blocked and what needs one decision, with each decision as a single reply. It builds on the existing ledger.
  Done when: after a night run, one briefing under 200 words lists shipped, blocked and decision items, each linked to its task id, and the decision items can be answered from the page.

- **Price Every Plan in Tokens and Minutes Before Starting** — FEATURE — value 4 — effort M — risk low — category: planning
  Why: Frontier 13 asks for a "priced plan", and the repo has a budget-fit queue (T-0751) and per-model lesions. Pricing would use the history of similar tasks (same tier, same files) to show a token and wall-time range for the plan, and warn when it won't fit the remaining usage window.
  Done when: `fm plan` prints an estimate range for a new M task, and after the task closes the actual cost is recorded and compared against the estimate in `fm bench`.

- **Fork a Task into Competing Attempts and Let the Verifier Pick (wild)** — FEATURE — value 4 — effort L — risk med — category: parallelism
  Why: worktree lanes and isolated agents exist, and verification records evidence. For hard FIX tasks with a failing repro, two or three builders on different models would try in separate worktrees. The one whose repro passes with the smallest diff and the full gates green is merged, and the others are discarded.
  Done when: on a seeded failing-test task, three lanes run, exactly one winning diff is merged, and the ledger records each lane's result and cost.

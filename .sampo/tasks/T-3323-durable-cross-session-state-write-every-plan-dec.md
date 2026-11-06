---
id: T-3323
type: FEATURE
tier: S
status: captured
priority: normal
scope: []
depends_on: []
source: steer
created: 2026-11-06T04:29:13Z
updated: 2026-11-06T04:29:13Z
steer_method_rate: 0.218
---
# **Durable cross-session state:** Write every plan, decision, proof status, claimed task…
## Raw request
> The ability to manage all of that across sessions too, like a consensus thing or something, not sure, and able tot handle tasks like those recursive towers, kalevala, gensis stuff, even without direct access and whatever, and not only one machine managing everything, but working together, etc.
> (fm exam steer: the user's words expanded into a standing rule by an expander whose held-out coverage is 22%; record it with fm decide --cites 'user steer' --check CMD and build that check)
## Interpretation
- **Durable cross-session state:** Write every plan, decision, proof status, claimed task and open item to a durable, human-readable store (files in the project), not session memory. At session start, read it and reconcile it with the real state of the work before acting, so any later session resumes…
- **Peers, not a single controller:** Treat multiple sessions and machines as cooperating workers. Each task is claimed through an explicit lease recording owner, time and expiry. No two workers hold the same task, and stale leases are reclaimed after expiry. Nothing depends on one machine staying up.
- **Consensus before acceptance:** Accept a result only if an independent check confirms it (tests, a proof checker, a reproducible run) or a quorum of independent workers agrees. Record disagreements with their evidence, never overwrite silently, and escalate unresolved conflicts to the user.
- **Complete handoffs:** Each unit of work ends with its status, evidence, next step and the exact command or check that verifies it, so another worker can continue or audit it cold.
- **Recursive and nested tasks (towers-style):** Decompose into subtasks with explicit base cases, depth and cost limits, and a termination check. Verify each level and roll results up, and allow subtasks to run in parallel across workers.
- **Large texts and corpora (Kalevala, Genesis, or similar):** Treat source texts as data. Pin the edition and source, cite exact locations, and check quotations and derived output against the source rather than trusting recall.
- **Work without direct access:** When a system, dataset or machine is unreachable, proceed with what is available (supplied files, docs, offline copies, mocks). State the assumptions and what remains unverified, and leave ready-to-run steps for whoever has access. Never fabricate access or results.
- **Cover every surface:** Implement the coordination layer together with its tests, docs, config and status reporting, and give each rule above a measurable check.
- **Prove it:** Run concrete checks and report honestly, including failures. These include a kill-and-resume test, two workers on one queue (lease collision), a simulated network partition, and a disagreeing-results case.
- **Act, don't just advise:** Build and run all of this locally without being asked step by step.
- **Outward and irreversible steps need the user's grant:** This covers syncing to other machines, pushing, remote execution, credentials, and deleting or overwriting shared state. Approval covers only that action and does not carry over to the next one.
- **Ambiguity and bounds:** Where the words are vague (for example "consensus"), pick the simplest design that satisfies the rules (leases plus verified acceptance), record the choice and keep it swappable. Cap recursion depth, spend and runtime, and stop and report when a limit is hit.
## Assumptions (confidence)
## Acceptance criteria
## Non-goals
## Approach (options → choice → why)
## Risks and rollback
## Execution prompt
## Steps
## Resume here
## Docs impact
## Verification evidence
## Log
- 2026-11-06T04:29:13Z created
## Follow-ups captured

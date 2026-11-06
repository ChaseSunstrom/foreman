# Brainstorm — lens: user value

- **Continue a task on another agent when usage runs out** — FEATURE — value 5 — effort L — risk med — category: continuity
  Why: Foreman already has resume points, budget pace, and Codex/Gemini/opencode adapters, but nothing joins them. When Claude hits a limit mid-task, work stops until the window resets.
  Done when: with Claude usage forced to exhausted, `fm run` hands the active task's brief and resume point to a configured second agent. That agent finishes the next step and records evidence, and the ledger shows the handoff.

- **Tell the user's edits from the agent's** — FEATURE — value 5 — effort M — risk med — category: collaboration
  Why: `fm lane merge` refused any dirty main checkout while the user (or main thread) was mid-task (T-0403). Foreman has no idea who changed what, so it can only be conservative.
  Done when: with a user-edited file in the working tree, the agent's attempts to edit, revert, or stash it are refused with a message naming the file as the user's. A lane merge touching other files still lands, and the task diff excludes the user's lines.

- **Give decisions tripwires that reopen them** — FEATURE — value 4 — effort M — risk low — category: decisions
  Why: the user's drops are mostly "YAGNI, see fm decide" (e.g. the `--focus && <edit>` refusal). Nothing notices when the condition for revisiting arrives, such as the same refusal recurring.
  Done when: `fm decide --revisit "3 more guard refusals of kind X"` stores a counter over the ledger. When the counter trips, a brief is auto-captured citing the decision and the matching events.

- **Turn plain-language policy statements into tested settings** — FEATURE — value 4 — effort M — risk med — category: configuration
  Why: "budget/pace limits shouldn't block anything until 75% usage" and "subagents never capped by token count" were policy steers that had to be hand-built. They are the user's most frequent kind of correction.
  Done when: a message stating a policy yields a proposed config change, a decision entry, and a generated test. The change applies only after the user confirms, and the test fails when the change is reverted.

- **Attribute wall-clock time and show the critical path** — FEATURE — value 4 — effort M — risk low — category: observability
  Why: cost causality is covered, but time isn't. The user's complaints are about idleness and waiting (JARVIS idling with 20+ queued, foreground wait loops). Nobody can see where hours actually go.
  Done when: `fm digest --time` splits a task's elapsed time into thinking, gates, waiting on background jobs, waiting on the user, and refusals/retries. It names the single largest avoidable block.

- **Turn the claims in MASTER.md into executable checks** — CLEAN — value 4 — effort L — risk low — category: docs-truth
  Why: `fm docs` only reports drift in markdown. MASTER.md makes behavioral promises ("resumes at the exact step", "blocks in bypass mode") with no link to a test. The user's cleanup requests also silently failed.
  Done when: each tagged claim in MASTER.md maps to a test ID. `fm doctor` fails when a claim has no passing test, and the claim count is shown.

- **Adopt an existing repo with a baseline health scan** — FEATURE — value 4 — effort M — risk low — category: onboarding
  Why: Foreman is being rolled to other projects (JARVIS, others), and `fm init` only registers them. Gates and conventions are discovered later, through friction.
  Done when: `fm adopt` runs the inferred gates, records which are red or flaky at baseline, and writes a first backlog of at most 10 evidence-backed tasks. A second run on an unchanged repo is idempotent.

- **Triage public GitHub issues into reproduced briefs** — FEATURE — value 4 — effort L — risk med — category: intake
  Why: the repo is public with a one-line installer, so outside users hit installer and platform failures. Intake today is the user relaying them.
  Done when: a new issue becomes a captured brief carrying an attempted repro, with its outcome (reproduced, not reproduced, or needs info) and the evidence. Nothing is posted publicly without the user's approval.

- **Rehearse the "ask" before interrupting the user** — FEATURE — value 3 — effort M — risk low — category: autonomy
  Why: the user steers toward fewer blocks (budget at 75%, "never asks mid-run"). Many asks are still avoidable if Foreman can first search past decisions, vetoes, and standing yeses for an answer.
  Done when: before any `fm ask`, a search of earlier answers runs. When it finds a match, the action proceeds with a ledger line citing that answer. Asks that fire anyway show what was searched.

- **Wild: Interview the user daily to build a living product vision** — FEATURE — value 3 — effort M — risk low — category: intent
  Why: wild. The user's requests are one-liners ("Foreman checks the product the way its user uses it"), so the intent behind them sits only in their head. One sharp question a day, with answers filed as research and used to rank the queue, would tell Foreman what "better" means for each product.
  Done when: a daily prompt asks one question. The answer is saved, and `fm next` cites the vision doc when it ranks a task.

- **Wild: Distil the discipline into a cheap local model's training set** — FEATURE — value 3 — effort L — risk med — category: portability
  Why: wild. The bench, ledger, and evolve flows hold thousands of verified plan/evidence/verdict trajectories. They could power a small model that runs Foreman's routine steps (classify, brief, checkpoint) offline and for free.
  Done when: `fm bench --export-sft` writes a redacted trajectory set. A small model fed it matches the frontier model's classification and brief-quality scores on held-out tasks within a stated margin.

- **Wild: Open a regression shop where users bet against the gates** — FEATURE — value 2 — effort M — risk low — category: trust
  Why: wild. Someone, human or agent, is paid in credits or recognition for each way they break a "done" task that the gates passed. Each win becomes a permanent eval case.
  Done when: submitting a failing scenario against a finished task creates a captured eval. The gate that missed it is named, and the eval fails on the old commit.

- **Hold a one-keystroke "why did you do that?" on any action** — FEATURE — value 3 — effort M — risk low — category: explainability
  Why: `fm why` explains a file, but the user's repeated puzzlement is about behaviours (the guard refusing, the drive going idle). They have had to trace them by hand.
  Done when: `fm why --last` explains the last refusal, nudge, or stop in one screen. It names the rule, the ledger events, and the brief step that caused it.

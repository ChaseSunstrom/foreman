# Brainstorm — lens: bold bets

- **Race hypotheses in parallel worktrees** — FEATURE — value 5 — effort L — risk med
  Why: the pack notes planning has no hypotheses and no "cheapest experiment first"; `fm run` and the improve skill already build worktree candidates.
  Done when: `fm race TASK --n 3` builds 3 candidates from different hypotheses, runs `fm check --affected` on each, and keeps the passing one with the smallest diff. The others are logged as ruled-out approaches.

- **Shape reads with a PreToolUse outline-first guard** — PERFORMANCE — value 5 — effort M — risk low
  Why: the user burned 20% of weekly usage, and `fm outline` and `fm map` exist, but nothing stops whole-file reads of big files.
  Done when: a full `Read` of a file over N lines with no offset gets a one-line hint (outline plus symbol ranges). A measured task shows fewer bytes read, with hook p95 under 150 ms.

- **Cache audits by hunk hash** — PERFORMANCE — value 4 — effort M — risk med
  Why: every reviewer pass re-reads large diffs, and `fm audit prep` already freezes the diff.
  Done when: after a passing audit, a one-line change makes `fm audit prep` include only the changed hunks plus their `fm impact` callers. A test asserts that unchanged hunks are absent from the brief.

- **Quote cost and success before focus** — FEATURE — value 4 — effort M — risk low
  Why: `fm cost` and BM25 recall over past briefs exist, but nobody sees a forecast. Assumption: enough history exists for nearest-neighbour estimates.
  Done when: `fm focus` writes "similar tasks: median X tokens, Y% needed rework" into the brief. Above a threshold it asks a single yes/no about splitting the task or using a cheaper model.

- **Lock behavior for CLEAN tasks with characterization snapshots** — FEATURE — value 4 — effort M — risk med
  Why: red→green covers FIX only, and CLEAN has no proof that behavior is unchanged.
  Done when: at focus, `fm snapshot` records outputs of the touched functions or CLI paths on sample inputs. `task done` for CLEAN fails if the snapshots differ, and a test shows a deliberate behavior change being caught.

- **Mine user corrections into durable preferences** — FEATURE — value 4 — effort M — risk med
  Why: the user never runs commands and wants everything smarter, but nothing learns from "no, don't do X" turns. Assumption: transcripts are readable locally.
  Done when: UserPromptSubmit flags correction-like prompts, and `fm prefs` stores each as a scoped one-line rule. Later matching tasks inject it (≤100 chars) and a repeat correction rate is tracked. Privacy filter and retire-unused apply as with lessons.

- **Queue idle-time pre-verified CLEAN patches for one yes/no merge** — FEATURE — value 3 — effort L — risk med
  Why: `fm repeats`, TODO scans, and `fm run` headless sessions exist, and the user wants autonomy with yes/no consent only.
  Done when: `fm run --idle` produces a worktree branch per small CLEAN item, each with gates green and the audit done. SessionStart shows "3 ready patches" and a single yes merges one.

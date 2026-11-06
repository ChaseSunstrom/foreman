# Brainstorm — lens: deepen: self-improvement

- **Log playbook reads and outcomes per task** — FEATURE — value 5 — effort S — risk low — category: self-improvement
  Why: the pack says playbooks "are not measured (no record of which were read or whether they helped)". A PostToolUse hook already sees Read calls, and `fm task done` knows first-pass status. Record `playbooks_read` and `first_pass` in the brief's front matter, which gives the foundation for scoring everything else below.
  Done when: after a task that read `playbooks/perf/profiling.md` is finished, its brief lists that path and `fm friction` prints a per-playbook read-count and first-pass-rate table.

- **Retire or demote playbooks that never get read** — CLEAN — value 4 — effort S — risk low — category: self-improvement
  Why: the pack lists ~40 ported ECC files with no usage data. Once reads are logged, `fm improve` can propose pruning from the 84-line index any playbook unread across N tasks, which cuts the cost of the index as context.
  Done when: `fm friction` lists playbooks with 0 reads over the last 30 tasks, and `fm tidy` can drop their index lines after the user's yes.

- **Route `fm next` by measured playbook lift** — FEATURE — value 4 — effort M — risk med — category: self-improvement
  Why: STAGE_REFERENCE in fmcore.py is a static one-per-task-type map. With read and pass data, `fm next` could pick the better-performing of two candidate references per task type, and name an installed skill (such as `/security-review` for SECURITY) when its history is good. Assumption: enough tasks accumulate per type to rank.
  Done when: for a task type with two candidate references and recorded outcomes, `fm next` names the one with the higher pass rate, and a test covers the tie and no-data fallback to the static map.

- **Draft playbooks from repeated recipes and solved tasks, one merged flow** — FEATURE — value 4 — effort M — risk med — category: self-improvement
  Why: `fm repeats` finds repeated manual work and lessons exist per task, which are two sources feeding one need. Merge them into a single `fm playbook draft` queue: a candidate is written to a staging file, never into ~/.claude (guarded `plugin` category), and promoted only by the user's yes/no.
  Done when: `fm playbook draft` writes a staged markdown file with trigger, steps and a source-task link, and promotion only happens after consent.

- **Mine eval cases from finished tasks, with a variance floor** — FEATURE — value 4 — effort M — risk med — category: self-improvement
  Why: only 5 eval cases exist, and the pack notes that single runs are noisy. Turn a finished task's acceptance criteria and verify commands into an eval case, then run candidates as paired repeats (k≥3) and report a verdict only if the delta exceeds the observed run-to-run spread.
  Done when: `fm eval grow TASK` emits a case file, and an A/B whose delta is inside the spread reports "inconclusive" instead of win or lose.

- **Wild: Replay old tasks against a candidate change** — FEATURE — value 4 — effort L — risk med — category: self-improvement (wild)
  Why: `fm replay` already replays real shell commands through the guard. Extending that idea, `/foreman:improve` could re-run the first prompts of past briefs in a temp HOME with the candidate plugin and compare gate-pass and turn counts against the recorded baseline. This is regression testing for Foreman itself, using real workloads instead of 5 synthetic cases. Cost is the concern, so cap it at 3 sampled tasks.
  Done when: `fm improve --replay 3` prints baseline vs candidate turns and tokens for 3 sampled past tasks.

- **Make the improvement loop stop on its own evidence** — FIX — value 3 — effort S — risk low — category: self-improvement
  Why: the user said "don't stop" and "recursive", but the last probe went dry (1/40 grounded) and they are usage-sensitive. Track yield per improvement round (grounded ideas ÷ proposed) and per lens in `ideas.md`, and have the super-mode loop stop after two consecutive rounds under a threshold, then widen to a different lens set before halting.
  Done when: a simulated run with two low-yield rounds stops and prints the yield trend, and a lens with 0 yield over three runs is flagged for retirement.

- **Wild: Let friction items auto-close when the fix lands** — FEATURE — value 3 — effort M — risk low — category: self-improvement (wild)
  Why: `fm friction` already shows trend and rechecks guard blocks. Link each friction pattern (e.g. the 21× drive-ended-to-wait item) to the task that claimed to fix it, then verify later digests show the count falling. A fix that doesn't move the number gets reopened automatically.
  Done when: a friction pattern tied to a finished task shows "fixed, down from 21 to N" or reopens as a capture when the count has not dropped.

- **Score lessons by whether recall changed an outcome** — FEATURE — value 3 — effort M — risk low — category: self-improvement
  Why: `fm recall` and `fm why` surface past lessons by BM25, with no feedback signal. Log which recalled lessons preceded a first-pass task, boost those in ranking, and flag lessons that were recalled many times and never helped.
  Done when: `fm recall` ranking changes after a lesson is marked helpful in the log, and a stale-lesson list is available from `fm tidy`.

- **Wild: Hold a research tournament over source-ranking rules** — FEATURE — value 3 — effort L — risk med — category: self-improvement (wild)
  Why: the user asked for better research and web search, and fm-recon currently has no source ranking. Run two or three ranking heuristics (official docs first, recency, corroboration count) over the same past research questions and let the user's accepted/rejected answers pick the winner. Assumption: enough accepted research exists to judge.
  Done when: `fm research tournament` replays N saved questions under 2 heuristics and reports which one's citations the user's past accepts agree with more often.

- **Tag every self-change with a reversible changelog entry and a rollback check** — CLEAN — value 3 — effort S — risk low — category: self-improvement
  Why: super mode builds many self-modifications unattended, and `/foreman:improve` works in a worktree. A per-change record (what changed, which metric it targeted, the baseline) enables `fm improve revert ID` when a later digest shows the metric worsened.
  Done when: `fm improve revert ID` restores the prior state in the worktree and a test shows a regressed metric surfaces the revert suggestion.

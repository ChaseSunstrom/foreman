# Brainstorm — lens: user value

- **Keep every captured message verbatim** — FIX — value 4 — effort S — risk low — category: capture
  Why: T-0756 is stored as "also, the …" and its remainder is unrecoverable, so a real request was lost.
  Done when: `fm task new` from a 2,000-character message stores the full text, `fm task show` prints it, and a test covers a message that is truncated in the title.

- **Coalesce message bursts into one ordered milestone** — FEATURE — value 5 — effort M — risk med — category: intake
  Why: T-0756 to T-0759 are fragments of one thought ("and reordering of operations… put them into one task"). Fragments ending in "also," are held briefly and merged with the next message instead of becoming tasks.
  Done when: replaying those four messages yields one batch with ordered steps and no truncated task.

- **Explain idleness and refuse it** — FEATURE — value 5 — effort M — risk med — category: autonomy
  Why: the user said "make sure it doesn't sit idle like it is". This is not about wake mechanics. At every stop, `fm why-idle` records a reason (queue empty, awaiting the user, blocked, paused, forgot to continue). Only the first three allow stopping.
  Done when: a test with a non-empty runnable queue and no ask pending makes Stop continue, and a measured idle-minutes figure appears in `fm status`.

- **Put a "do this instead" in every guard refusal** — FEATURE — value 4 — effort S — risk low — category: guard UX
  Why: five recent drops were "working as intended" guard refusals. Each cost a task plus a decision record. The block message should carry the sanctioned alternative and the matching `fm decide` id, and a refusal matching a decision should not be offered for capture.
  Done when: each refusal in the guard test corpus prints a next step, and a repeat of a decided refusal creates no new task.

- **Replay new detectors over closed-task history before they activate** — FIX — value 4 — effort M — risk low — category: detector quality
  Why: the debug-scaffolding scan flagged docs (T-0695) and string literals (T-0746), and the check track record and catch-rate parsers missed '✗ exit N' (T-0749, T-0750). The class is a detector shipped without a corpus.
  Done when: `fm doctor` reports a hit and false-positive rate per detector from past closes, and a detector with unlabeled hits is held in shadow mode.

- **Require a baseline measurement before savings features are built** — FEATURE — value 4 — effort S — risk low — category: planning
  Why: delta reads were built, then dropped once measurement showed 109 tokens in 30 days. T-0757 was "already built". A FEATURE task claiming speed or token savings must first record a baseline number, or a pointer to the existing capability it duplicates.
  Done when: a savings-claiming task cannot reach plan approval without a baseline field, and the check passes on a task that has one.

- **Ship releases with one word** — FEATURE — value 4 — effort M — risk med — category: release
  Why: seven recent requests share one shape ("Release Foreman 1.2.N (T-… to T-…) to GitHub main and JARVIS"). `fm ship` would take the tasks closed since the last tag, bump the version, draft the changelog and the milestone summary, run the gates, and push to both targets after one confirmation.
  Done when: in a fixture repo, `fm ship --dry-run` prints the task range, the changelog entry and the push targets exactly as the manual release would produce.

- **Generate the PR description from the evidence ledger** — FEATURE — value 3 — effort S — risk low — category: handoff
  Why: Foreman records criteria, run results and review findings per task, but the user still writes the PR text by hand. Assumption: they open PRs for some work.
  Done when: `fm task pr T-xxxx` prints a body with criteria, their evidence and the review verdicts, with secrets redacted.

- **Cap how much context Foreman itself injects** — PERFORMANCE — value 4 — effort M — risk med — category: token cost
  Why: the user keeps asking for token savings, and Foreman ships 73 skills, 14 hooks and reminders. Measure the Foreman-attributable tokens per session and set a budget that `fm doctor` fails when exceeded.
  Done when: `fm doctor` prints injected tokens per session start and per prompt, and a test fails when the default exceeds the stated budget.

- **Wild: pre-draft the next request from your habits** — FEATURE — value 3 — effort M — risk med — category: prediction
  Why: wild. The history is repetitive (release after a milestone, fix a scanner false positive after a close, update MASTER.md when a command is added). After a close, Foreman queues a captured task, marked as predicted, with a plan.
  Done when: closing a task that adds an `fm` command produces a predicted "MASTER.md names it" task, and the user can discard it with one command.

- **Wild: ask whether the work is worth doing before planning** — FEATURE — value 3 — effort S — risk low — category: planning
  Why: wild. This is a cheap "do less" agent. It reads the open task and checks for an existing built-in, a prior `fm decide`, and a dropped twin, and it argues for deletion when the evidence supports it. The user's drops are mostly YAGNI verdicts reached late.
  Done when: capturing a task that duplicates a dropped one shows the drop reason before any planning begins.

- **Wild: split a "while you were away" report by the decision it needs** — FEATURE — value 4 — effort M — risk low — category: reporting
  Why: wild. Blocked items such as T-0325 (needs sudo), T-0335 to T-0337 and T-0352 wait on the human with no deadline. Return a short list of exactly the human-only steps. Each item has a default Foreman will take after N days if there is no answer, and each can be dropped with one reply.
  Done when: `fm needs-you` lists every blocked task with its one question and default, and a lapsed default is applied and logged.

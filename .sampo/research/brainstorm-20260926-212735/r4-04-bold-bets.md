# Brainstorm — lens: bold bets

- **Run verification in the background on every edit** — FEATURE — value 5 — effort M — risk med
  Why: verification only happens at `fm check` or done, so a broken step costs several turns before anyone sees it. `fm impact` already links tests to source files, and a hook has a 30 ms budget.
  Done when: PostToolUse spawns a detached `--affected` run, and after an edit that breaks a linked test, the next turn's note names that test within one turn, with hook p50 still ≤ 30 ms.

- **Compile repeated tasks into replayable recipes** — PERFORMANCE — value 5 — effort L — risk med
  Why: `fm repeats` and recall show recurring task shapes (add an `fm` subcommand, add a hook, add a playbook), yet each one is re-derived by the model. Assumption: diffs of the same shape share a structure that can be parameterized.
  Done when: `fm recipe learn` extracts a template from 3 similar finished tasks, and a fourth is applied with zero model edit turns and passes its verify commands.

- **Score risk per path from outcomes** — FEATURE — value 4 — effort M — risk low
  Why: tier calibration works per task, but failures, reversals, and post-done recurrences cluster in hot files. `fm map` already tracks hot files, and recurring failures are matched to finished tasks.
  Done when: `fm focus` on a task touching a high-risk path raises the audit depth and shows a one-line reason. On seeded history, a file with 3 past regressions outranks a clean file.

- **Autopsy the weekly token sinks and propose guards** — PERFORMANCE — value 5 — effort M — risk low
  Why: the user reports 20% of weekly usage burned in one session. `fm cost` measures per task but does not attribute waste (re-reads, oversized tool output, retries, repeated reviewer passes).
  Done when: `fm cost --autopsy` ranks the top 5 waste patterns from transcripts with token counts. Each one comes with a concrete proposed guard or rule change, ready for the `improve` skill's yes/no.

- **Track brainstorm lens yield and drop losing lenses** — PERFORMANCE — value 3 — effort S — risk low
  Why: `fm ideas` runs many tool-less `claude -p` lenses over multiple rounds, but nothing records which lenses produced ideas that were implemented and passed.
  Done when: each idea keeps its lens tag through to done. `fm ideas` skips lenses with a lower-than-threshold accepted rate over at least 10 samples, and prints the token saving.

- **Allocate the weekly budget across projects** — FEATURE — value 4 — effort M — risk med
  Why: throttling is per session and state is per project (`state/projects/<slug>`), but the weekly limit is shared across all of them. Assumption: the user works in several projects.
  Done when: `fm run` refuses or defers low-value tasks in project B when the shared remaining budget is under a floor reserved for a higher-value queue in project A. The decision is logged with numbers.

- **Bisect a newly red gate across finished tasks** — FEATURE — value 3 — effort M — risk med
  Why: a recurring failure is matched to a finished task by text only. Task checkpoints plus cached passes keyed on a tree hash could pin the culprit mechanically. Assumption: checkpoints exist per task.
  Done when: `fm bisect GATE` finds the first task checkpoint where the gate flips red, and in a seeded 6-task history it names the injected breaking task in ≤ 3 gate runs.

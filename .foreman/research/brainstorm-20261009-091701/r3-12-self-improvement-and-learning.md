# Brainstorm — lens: self-improvement and learning

- **Promote repeatedly broken rules from prose to enforcement** — FEATURE — value 5 — effort M — risk med — category: self-improvement
  Why: assumption: the same instruction gets ignored across sessions, and fixes keep arriving as new guard patches (T-0404, T-0409, T-0414). Nothing measures which prose rules are actually obeyed. Scan transcripts for each injected rule's violation rate. A rule violated past a threshold becomes a candidate hook or guard check, with a draft and a regression test. A guard check that never fires across N sessions becomes a candidate to demote to prose or delete.
  Done when: `fm rules --compliance` lists each rule with its violation count and a promote/demote recommendation. A fixture transcript with a seeded violation produces a promotion draft that has a failing test.

- **Pre-register self-experiments before changing Foreman** — FEATURE — value 5 — effort M — risk low — category: experiments
  Why: `fm friction --every 3` ships fixes, but nothing records what each fix was expected to change or whether it did. Each friction fix first records a hypothesis, a metric (e.g. refusals per task, idle minutes), a threshold and a review date. After N tasks, `fm friction` scores the hypothesis and flags failed ones for revert or rework. This also stops moving the goalposts afterwards.
  Done when: a fix cannot be merged by the friction pass without a hypothesis record. A seeded hypothesis that fails its metric appears as "unproven" in the next digest.

- **Detect rework to grade past "done" claims** — FEATURE — value 4 — effort M — risk low — category: learning
  Why: assumption: the real measure of quality is whether the same lines get touched again soon. Recent history shows many follow-up fixes (T-0404, T-0408, T-0409, T-0414). Use git blame plus the ledger to mark a finished task as reworked when a later task or manual commit edits its lines within 14 days. Rework feeds back to the lessons, the review lens and the tier of the original task.
  Done when: `fm digest` shows a rework rate per task type. A fixture repo where task B edits task A's lines within the window marks A as reworked and links B.

- **Keep a dead-end registry checked at plan time** — FEATURE — value 4 — effort M — risk low — category: memory
  Why: the dropped items (a `-k` verify that ran no tests, loosening the brief gate, the `--focus &&` combination) show approaches rediscovered and re-rejected. Store each abandoned approach with the reason and the code area. Planning matches a new plan against the registry and says "tried, failed because…" before work starts. This is separate from the FIX-only hypothesis ledger.
  Done when: planning a task whose approach matches a registered dead end prints that entry. Entries expire when the files they cover change substantially.

- **Learn the user's vocabulary into a project glossary** — FEATURE — value 4 — effort M — risk low — category: intake
  Why: requests are terse and loaded with private names ("the band", "JARVIS lane", "the drive", "the court"). Mine briefs, steers and corrections for terms the user uses, and resolve each to a file, command or project. Record intake reclassifications (the user changing type or tier) as training pairs for the classifier. Terse intake then resolves without a clarifying question.
  Done when: `fm intake "fix the band stuck"` resolves "the band" to the right module in the brief. Reclassifying a task twice in the same way changes the classifier's default for that phrase.

- **Schedule self-improvement passes by marginal yield** — FEATURE — value 3 — effort S — risk low — category: scheduling
  Why: `--every 3` is a fixed cadence. Track how many actionable findings each pass produced and their cost. Lengthen the interval when yield is falling and shorten it after a burst of corrections or refusals. Passes also stop making instruction edits beyond a weekly churn budget, so the instruction files stay stable.
  Done when: `fm friction` reports the next pass trigger and why. After three empty passes the interval visibly lengthens in a fixture ledger.

- **Run a model-upgrade exam from the failure museum** — FEATURE — value 4 — effort L — risk med — category: evals
  Why: T-0316 and T-0336 are blocked on re-checking behaviour after a Claude Code update, and `fm bench` already replays finished tasks. Curate the worst historical failures into a fixed exam. On a new model or Claude Code version, run the exam and the instruction-ablation set together and report which crutches the new model no longer needs and which new regressions appeared.
  Done when: `fm bench --exam` runs the museum against the installed `claude` and writes a pass/fail table per case. The table is diffable against the previous version's run.

- **Wild: Hold a mirror session where Foreman interviews its own transcripts** — FEATURE — value 3 — effort L — risk med — category: introspection
  Why: wild. A read-only agent reads a week of full transcripts and answers one question: where did the main thread lose its way, and what did it say to itself at that point? It cites turn numbers. Output feeds friction briefs with the model's own wording of why it deviated.
  Done when: a seeded transcript with a known wrong turn gets that turn cited with a reason in the report.

- **Wild: Let rival lessons compete and keep the survivor** — FEATURE — value 3 — effort M — risk med — category: learning
  Why: wild. Contradictory lessons or rules are only detected today. Instead, when two rules conflict, run each as a variant in alternate tasks (or replay both in `fm bench`) and keep the one with better first-pass and rework outcomes. The loser is archived with the evidence.
  Done when: two contradictory seeded lessons are tested against a bench set, one is retired, and `fm recall` shows the verdict and numbers.

- **Wild: Write a changelog from the future as a steering device** — FEATURE — value 2 — effort S — risk low — category: planning
  Why: wild. Each month Foreman drafts "Foreman 2.0 release notes" from the taste model, open tasks and friction trends, as if the best version shipped. The user strikes lines they don't want, and the survivors become queue seeds. Struck lines become vetoes.
  Done when: `fm mission --future` writes a draft. Striking one line records a veto and keeping one creates a captured brief.

- **Wild: Keep a learning journal of questions the model couldn't answer without asking** — FEATURE — value 3 — effort S — risk low — category: memory
  Why: wild. Every `fm ask` and every mid-task read of a file the map didn't predict is a gap in Foreman's knowledge. Log them as "knowledge gaps". A weekly pass turns the most repeated gaps into map entries, glossary terms or MASTER.md sections, so the same question isn't asked twice.
  Done when: after the same ask recurs three times, `fm doctor` flags it as a gap. Resolving the gap marks the entry closed.

- **Mine abandoned and reverted work for lessons** — FEATURE — value 3 — effort M — risk low — category: learning
  Why: assumption: lessons come from finished tasks, but reverted commits, deleted lanes (`fm lane rm`) and tasks dropped mid-way hold the stronger signal. Capture a one-line cause for each at the moment of revert or drop, defaulting to the diff summary when none is given. Feed these into the dead-end registry and the friction digest.
  Done when: `fm lane rm` on a lane with unmerged commits asks for or infers a reason and writes a recall-visible entry.

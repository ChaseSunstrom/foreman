# Brainstorm — lens: problem solving and debugging under uncertainty

- **Route stages to installed skills from a capability registry** — FEATURE — value 5 — effort M — risk low — category: plugin compat
  Why: the pack states `fm next` names only Foreman's own procedures. A SECURITY task never surfaces `/security-review`, CLEAN never surfaces `/ponytail-audit`, and a UI task never surfaces frontend-design. The static MASTER.md §7 table is prose only. Make it a data table keyed by (task type, stage), filtered to skills actually installed (read from skill frontmatter), and let `next_action` append one line naming the skill.
  Done when: with security-review installed, `fm next` on a SECURITY task in the verify stage names `/security-review`; with it absent, no mention appears.

- **Print a hypothesis ledger at each failed verify** — FEATURE — value 4 — effort M — risk low — category: debugging
  Why: the pack's rule is "3 failed attempts → block with diagnosis", which is a count, not a method. Store `fm hypo add "claim" --test CMD` and `fm hypo rule-out`. A failing verify prompts for one entry before a retry, and the block message lists the ruled-out entries. Unlike the thrash and ruled-out-handoff ideas already listed, this gives each hypothesis a discriminating test command up front. Assumption: Claude will fill it in cheaply if the prompt is one line.
  Done when: after a failed `fm check`, `fm next` asks for a hypothesis. A third failure's block text lists the recorded hypotheses and their outcomes.

- **Classify the unknown before debugging: known-unknown vs. unknown-unknown** — FEATURE — value 3 — effort S — risk low — category: debugging
  Why: assumption: much of the friction comes from guessing at causes without first reproducing the issue. At intake for FIX tasks, require a "reproduced? y/n + command" field. If n, the first step is forced to be "make it reproducible", and the type can't leave plan until a repro command exists.
  Done when: a FIX brief without a repro command or an explicit "not reproducible: reason" cannot pass the plan gate.

- **Rank competing causes by cheap discriminating probes** — FEATURE — value 3 — effort M — risk med — category: debugging
  Why: the pack shows `fm why`, `fm recall`, and recon, but nothing that picks the cheapest next observation. A helper takes the hypothesis list and the git-co-change/impact map (fmmap) and proposes the single read or command that splits the most hypotheses, such as a log grep or a one-line print. Aimed at saving tokens versus broad reading.
  Done when: given 3 hypotheses on a fixture repo, `fm probe` outputs one command that distinguishes at least two of them.

- **Quarantine pre-existing failures at focus** — FIX — value 4 — effort M — risk low — category: test gates
  Why: the pack's failure triage idea is listed, but nothing records a baseline of red tests before the task starts. Run the affected tests at focus, store the red set, and at done report only new failures as the task's fault. This avoids both spurious blocks and the "fix unrelated bug" detours.
  Done when: with one pre-existing failing test, a task that doesn't touch it can reach done, and the evidence names that test as baseline-red.

- **Treat inconclusive evidence as a distinct state** — FIX — value 3 — effort S — risk low — category: verification
  Why: the pack mentions timeouts and environment failures being indistinguishable (a listed idea), and the criterion-1 steer ("old one matched PASS and WARN alike"). Add a tri-state PASS / FAIL / INCONCLUSIVE (timeout, missing tool, network) to `fm check`. INCONCLUSIVE can't satisfy a gate and is never counted as an attempt toward the 3-failure block.
  Done when: a verify command killed by timeout records INCONCLUSIVE, doesn't increment the attempt counter, and `fm next` advises a retry or an alternative check.

- **Wild: Keep a "surprise log" and mine it for model-of-the-code errors** — FEATURE — value 3 — effort M — risk low — category: learning
  Why: wild. Whenever a result contradicts what Claude predicted (a test passed that was expected to fail, or the reverse), one line is written automatically from the evidence. At reflect, the surprises are clustered by file, and files with repeated surprises get a tripwire lesson, because misprediction marks where the mental model is wrong.
  Done when: running a test that was predicted to fail and passes appends a surprise record, and a file with 2 records shows up in `fm why FILE`.

- **Wild: Run a "premortem fork" that argues the root cause is wrong** — FEATURE — value 3 — effort M — risk med — category: debugging
  Why: wild. Before a FIX is declared done, a single `claude -p` child with no tools, given only the symptom, diff, and evidence, is asked for the best alternative explanation that the evidence doesn't rule out. This catches fixes that mask a symptom. Bounded to one call, only for L or security FIX tasks, so usage stays low.
  Done when: for a L FIX task, `fm task done` records an "alternative cause considered" line, with a skip reason when the budget is in economy mode.

- **Wild: Replay a failing session as a minimal repro by delta-debugging the transcript's commands** — FEATURE — value 3 — effort L — risk med — category: debugging
  Why: wild. Pasted-error intake exists as an idea, but nothing shrinks a long multi-command failure to its few essential steps. Using the recorded shell commands (the source fmreplay already reads), bisect the sequence to the smallest subset that still reproduces the error.
  Done when: a fixture session of 12 commands with 3 relevant ones shrinks to those 3 and prints them as a script.

- **Wild: Add a "rubber duck" mode that answers from the brief alone** — FEATURE — value 2 — effort S — risk low — category: debugging
  Why: wild. When stuck, a Haiku child gets only the brief, the failing output, and ruled-out hypotheses, with no code access, and must ask the one question it would ask. Fresh context often exposes a wrong assumption cheaply, and complements the already-listed fresh-context consult by forcing a question rather than an answer.
  Done when: `fm stuck` returns exactly one question, and its input contains no file contents beyond the failing output.

- **Record "assumed vs. verified" tags on every fact in the brief's evidence section** — CLEAN — value 3 — effort S — risk low — category: uncertainty
  Why: assumption: under uncertainty, most wasted turns come from treating an unverified claim as established. The pack lists a stale-fact tripwire and provenance labels, but not the explicit tag. At focus, any "assumed" fact that a step depends on gets a one-command check as the step's first action.
  Done when: a brief with an assumed fact the first step depends on shows a check as step 1 in `fm next`, and marking it verified removes it.

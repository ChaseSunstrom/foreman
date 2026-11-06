# Brainstorm — lens: user value

- **Wrap noisy commands so only failures reach context** — FEATURE — value 5 — effort M — risk med
  Why: tool output is usually the biggest context item, and the pack has no output-side trimming (only read-shaping). Mechanism: PreToolUse rewrites known verbose test/build/install commands to `fm quiet -- <cmd>`, which prints the exit code, failing tests, the last 30 lines and a log path. Full output is saved to state. Evidence matching keys on the original command. Assumption: PreToolUse can rewrite the command.
  Done when: a 500-line passing test run injects ≤ 15 lines, a failing run still shows every failure name, and the criterion's verify command is still auto-recorded as evidence.

- **Throttle ceremony as the weekly budget drains** — FEATURE — value 5 — effort M — risk low
  Why: the user burned 20% of their weekly usage in one session, and the per-stage ledger measures tasks, not the week. Mechanism: `fm cost` totals transcript tokens per week against a cap the user sets once, via a yes/no prompt with a sensible default. At 60% / 85% the governor lowers brainstorm rounds to 1, skips optional M audits, routes `fm run` to cheaper models and defers PERF/RESEARCH tasks. SessionStart shows one line saying so.
  Done when: with a fake ledger at 90%, `fm ideas` runs one round and `fm audit prep` omits the optional lens, and both say why.

- **Treat mid-task replies as amendments, not inbox items** — FEATURE — value 4 — effort M — risk med
  Why: new requests go to the inbox, but a user who never runs commands steers in prose ("no, make it blue", "also handle empty input"). Mechanism: UserPromptSubmit classifies a prompt during an active task by scope/keyword overlap with the brief. Corrections append or revise criteria and mark affected steps stale, so they need fresh evidence. Ambiguous cases become one yes/no.
  Done when: a test prompt refining the active task edits its criteria and invalidates the touched step's evidence, while an unrelated prompt still lands in the inbox.

- **Move to a fresh session at task boundaries when context is heavy** — PERFORMANCE — value 5 — effort M — risk med
  Why: every turn re-reads the whole session, and finished-task history is dead weight. Mechanism: the Stop hook estimates transcript size. Past a threshold, at a task boundary with a written resume note, the drive loop hands the next queued task to `fm run` rather than continuing in-session. Assumption: headless runs can meet the yes/no consent constraint via pre-approved standing answers.
  Done when: after a simulated 300k-token session, task done launches the next task in a new session, whose SessionStart shows the resume note, and per-turn token cost drops in `fm cost`.

- **Ledger assumptions and review them in one batch at done** — FEATURE — value 4 — effort S — risk low
  Why: mid-task questions cost turns, and the user only gives yes/no. Mechanism: the brief gets an `assumptions:` list, filled from past preferences whenever intake is ambiguous instead of asking. `fm task done` prints them in the plain-language report as a single "keep these?" yes/no, and a "no" reopens only the dependent steps.
  Done when: a task with 2 assumptions shows both in the done report, and answering "no" reopens exactly the steps that cite them.

- **Short-circuit requests that are already done** — FEATURE — value 3 — effort S — risk low
  Why: recall already runs BM25 over past briefs, and finished tasks have verify commands. Mechanism: at capture, a top hit above a score threshold triggers running that task's verify commands. If they pass and the tree hasn't changed in the scope, ask one yes/no: "This looks already done in task X — close it?"
  Done when: re-requesting a completed feature produces the prompt with no new brief planned, and a changed scope skips the shortcut.

- **Auto-onboard unfamiliar repos with a 600-char project card** — FEATURE — value 4 — effort S — risk low
  Why: `fm map` exists but nothing says it runs unprompted. Assumption: a first session in a new project pays for exploration greps. Mechanism: the first SessionStart in an unmapped project runs `fm map` and stores a card (gates, entry points, hot files, conventions) that later SessionStarts reference by pointer.
  Done when: a fresh repo's first turn shows the card, and the count of exploratory Grep/Glob calls in its first task falls versus baseline.

- **Re-ground queued briefs by scope delta at focus** — FIX — value 3 — effort S — risk low
  Why: resume preflight covers only the active task, so queued briefs go stale as other work changes their scope. Mechanism: record a scope tree hash at planning. At `fm focus`, if it differs, `fm` lists changed files and re-runs ground only on that delta.
  Done when: editing a queued task's scope file makes focus print the delta and mark the plan "needs re-ground", and an unchanged scope focuses silently.

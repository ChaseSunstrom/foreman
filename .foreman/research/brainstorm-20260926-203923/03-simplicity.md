# Brainstorm — lens: simplicity

- **Script the audit, and call a reviewer only when the script flags something** — PERFORMANCE — value 5 — effort M — risk med
  Why: subagent reviews cost ~50-100k tokens each, the biggest item in the pack. Most of what they check is mechanical.
  Done when: `fm audit` on an S/M task with every criterion evidenced, gates green and the diff inside the mapped files finishes with no subagent and prints pass/fail. A seeded discrepancy (an unevidenced criterion, or an edit outside the brief) triggers the reviewer path.

- **Run only the impacted tests during work, and the full suite once at close** — PERFORMANCE — value 5 — effort S — risk med
  Why: the full suite (~100 s) runs after every small change. `fm map` and `fm impact` already have the test↔source mapping.
  Done when: `fm check --changed` runs only the mapped tests and falls back to the full suite if a file has no mapping. `fm done` requires one full green run, and a session's wall time on a 5-edit task drops by at least 50%.

- **Collapse the Stop-hook nudges into one message that fires at most once per task state** — CLEAN — value 4 — effort S — risk low
  Why: the evidence-gate and question nudges each force an extra model turn. They may stack or repeat.
  Done when: a test simulating both conditions shows one combined nudge and no repeat while state is unchanged. Extra turns per task are ≤1, as counted from the transcript.

- **Cap every `fm` output and write the full text to a file** — PERFORMANCE — value 4 — effort S — risk low
  Why: large tool outputs are a listed cost. Only failing lines matter to the model.
  Done when: `fm check`, `fm map` and `fm impact` print ≤40 lines or ≤2k chars, ending with a `full: <path>` line. The failing test name and assertion are always in the printed part.

- **Inject "Next" and SessionStart only when state changed, and shrink SessionStart to a pointer** — PERFORMANCE — value 4 — effort S — risk low
  Why: the "Next" injection (≤400 chars) runs every turn, SessionStart is ≤2k chars, and another plugin already adds 5.7k.
  Done when: an unchanged-state turn injects 0 chars, SessionStart is ≤800 chars, and hook p50 stays ~30 ms.

- **Add `fm ledger`, a per-hook count of injected chars and extra turns, and delete what doesn't pay** — CLEAN — value 4 — effort M — risk low
  Why: the user burned 20% of weekly usage and the pack's cost breakdown is observed rather than measured. Rounds 1-4 only added features.
  Done when: `fm ledger` prints chars injected per hook and turns added per session. At least one feature is either justified with numbers or removed in the same change.

- **Make tier S a one-line brief with no steps, one criterion, and no Related lookup** — CLEAN — value 3 — effort S — risk low
  Why: assumption: small tasks pay the full brief and recall overhead. Recall matters most for M/L.
  Done when: an S focus writes ≤3 lines and skips BM25. M/L output is unchanged, and the tier hint still upgrades to M when the Related lookup finds a matching failure.

- **Have `fm done` print the final report, and make replying with it the rule** — PERFORMANCE — value 3 — effort S — risk low
  Why: verbose status replies are a listed cost. The evidence and lesson are already in state.
  Done when: `fm done` emits a ≤5-line summary (outcome, evidence, lesson) and the closing reply averages ≤80 words across 5 sample tasks.

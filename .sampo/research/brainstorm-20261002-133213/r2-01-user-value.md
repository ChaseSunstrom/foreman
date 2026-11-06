# Brainstorm — lens: user value

- **Add a one-keystroke "capture inbox triage" dialog** — FEATURE — value 4 — effort M — risk low
  Why: the inbox holds self-found items (T-0074…T-0081) and "captures instead of chasing" means it grows silently. Nothing lets the user promote, merge, defer or drop items quickly. Mod Pane with Select and Buttons calling `fm` via `$.process.run` fits.
  Done when: opening the dialog lists inbox items and pressing a hotkey promotes, defers or drops one, with `fm state --json` showing the change.

- **Auto-dedupe and cluster inbox captures** — FEATURE — value 3 — effort M — risk low
  Why: T-0075/T-0076/T-0080 are all "state doesn't round-trip", and T-0078/T-0079 are both scope bugs. Both clusters were hand-spotted. assumption: the inbox has no similarity check on capture.
  Done when: capturing a near-duplicate prints "similar to T-00xx" and offers merge. A test with two similar titles asserts one cluster.

- **Show a "why was I blocked" explainer on gate refusals** — FEATURE — value 4 — effort M — risk low
  Why: gates refuse "done" without evidence, and the guard blocks commands, but the model only sees terse text. Users see the model apologise with no cause. A ToolResult/InfoNotice renderer could show the failed gate, the missing evidence and the exact fix. `fm why` exists, so this wires it into the UI.
  Done when: a refused `fm task done` renders a notice naming the unmet criterion and fix. A mod UI test asserts the text.

- **Add a per-task time-travel replay from the ledger** — FEATURE — value 3 — effort M — risk low
  Why: the ledger and event history exist, and `fm digest`/`fm pr` summarise, but nothing lets you scrub a finished task's stages, evidence and tool calls. This helps audits and debugging of Foreman's own decisions.
  Done when: `fm replay T-0082` (and a Pane view) steps through stage transitions with timestamps and evidence, with output matching the ledger in a test.

- **Learn per-user effort and cost estimates from history** — FEATURE — value 4 — effort M — risk low
  Why: briefs carry size tags (M, L), and `fm cost` records actuals. The user is usage-sensitive, yet estimates are static. Predicting tokens and time per size, and warning before a drive run exceeds a budget, serves token economy directly.
  Done when: `fm task new` shows "est ~N tokens (p50 from K similar tasks)". `fm run --budget` stops the queue when the budget is hit, covered by a test with seeded history.

- **Add a drive-mode kill switch and live budget guard** — SECURITY — value 4 — effort S — risk med
  Why: "full autonomy" plus `$.prompt.submit` waking idle sessions means unattended runs could loop. Nothing in the pack caps turns, spend, or consecutive failures. assumption: only `fm run` has limits.
  Done when: drive stops after N consecutive failed verifications or a spend cap. An AbovePrompt band shows "paused: reason", and a test simulates three failures.

- **Make planning a conversational "plan card" the user can edit in place** — FEATURE — value 3 — effort L — risk med
  Why: planning friction is a known limitation (exact section names, several `fm` calls). Rather than only adding buttons, render the plan as editable Input/Select fields with steps reorderable, writing back once. This goes past the existing "one-click approve" and "single plan call" ideas by letting the user change the plan.
  Done when: editing a step title in the card and confirming updates the brief via one `fm` call, and the round-trip is lossless.

- **Run a mod/classic parity test harness** — CLEAN — value 3 — effort M — risk low
  Why: classic hooks must still work where mods are absent, but the mod will diverge over time. A replay of recorded event fixtures through both paths, asserting identical `fm state` and ledger results, prevents silent drift.
  Done when: CI replays one fixture through both paths and fails on any difference in final state.

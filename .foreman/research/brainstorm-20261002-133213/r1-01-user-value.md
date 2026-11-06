# Brainstorm — lens: user value

- **Ship a Foreman mod with a docked live-task Pane** — FEATURE — value 5 — effort L — risk med
  Why: the user asked for a mods-integrated UI; `fm watch` needs a second terminal and the statusline is one non-interactive line. Mods offer docked Panes and AbovePrompt bands. The mod would call `fm state --json` and `fm queue --json` through `$.process.run`, and show the task, steps, stage bar, queue and inbox. Classic hooks stay as the fallback.
  Done when: `claude plugin test` mounts the Pane on terminal, shows T-id, stage and step N/M from a mocked `fm` result, and `claude plugin validate` passes.

- **Replace "Next:" hint text with in-process tool.call gates** — FEATURE — value 5 — effort M — risk med
  Why: hints can be ignored and only gates are enforced; the Python hook costs about 29 ms per event. A mod `tool.call` handler can deny or rewrite in-process, and can also see Bash edits that the Edit/Write hooks miss. Classic hooks remain the fallback, and the mod must not double-fire them.
  Done when: a mod test shows a Bash `sed -i` on an out-of-scope file is denied or flagged, and the classic path still works under `claude -p`.

- **Add one-click approve/execute buttons in the planning dialog** — FEATURE — value 4 — effort M — risk low
  Why: planning friction (several `fm` calls, exact section names) is a known limitation. A focusable dialog could show the brief's Approach and Acceptance criteria with Approve, Edit and Capture buttons, and hand the result to `fm task set`. Assumption: mod dialogs can pass input back via `$.prompt.submit`.
  Done when: a mod test presses Approve and `$.process.run` is called with the expected `fm task set/step` argv.

- **Fix `fm task show --json` to include criteria, steps and depends (T-0076)** — FIX — value 4 — effort S — risk low
  Why: it is an open inbox item, and any mod UI needs this data to render criteria and steps without parsing markdown. It blocks the Pane and dialog ideas above.
  Done when: the JSON output contains `criteria[]` with evidence links, `steps[]` and `depends[]`, and a unit test asserts the keys.

- **Add a `fm task set` section-alias fix and evidence-link preservation (T-0075, T-0080)** — FIX — value 4 — effort S — risk low
  Why: `--section Approach` creates a duplicate section, and `--section 'Acceptance criteria'` drops the evidence↔criterion link. Both are inbox items that cause rework for every planning pass.
  Done when: tests show `--section Approach` fills the existing "Approach (options → choice → why)" section and criterion evidence survives a section rewrite.

- **Use `$.model.complete` Haiku for smart capture and intent classification** — FEATURE — value 4 — effort M — risk med
  Why: the user wants it "way smarter", and a prompt.submit mod could classify a message as new request, follow-up or question, then capture it automatically. Cost is a concern for this usage-sensitive user, so it needs a budget cap and an `fm cost` entry. Assumption: classification beats the current heuristics.
  Done when: a labeled sample of 20 prompts is classified at ≥90% accuracy with a mocked model, and each call is recorded in the cost ledger.

- **Render tool timeline and hook latency as Raster sparklines in CommandOutput** — FEATURE — value 3 — effort M — risk low
  Why: `fm watch` already has tool latencies, hook latency and files touched, but only as curses in a second terminal. A `/fm` slash command and a CommandOutput renderer would put them inline.
  Done when: a mod test runs `/fm` and the tree output contains the queue, the tool timeline and a sparkline row.

- **Fix scope and security audit to the task's own diff (T-0078, T-0079)** — FIX — value 3 — effort M — risk low
  Why: scope checks and audit triggers currently look at the whole tree, which produces false gates and wastes audit tokens. Scoping them to the task's own changes is a precondition for trusting mod-level gating.
  Done when: a test with unrelated dirty files elsewhere in the tree does not trigger the security audit or a scope-drift flag.

# Brainstorm — lens: simplicity

- **Cap the stage machine at five visible stages** — CLEAN — value 4 — effort M — risk med
  Why: the pack lists seven stages (captured→planning→ready→executing→verifying→auditing→closing) plus eight steps (capture…record). Two overlapping vocabularies show up in the statusline, the output style and `Next:` text. Every UI surface has to teach both.
  Done when: `fm state --json` exposes one `phase` field drawn from ≤5 values, and the statusline, the Pane and the output style all read it. A test fails if any of them prints a different name.

- **Make planning a single fillable template file** — FEATURE — value 5 — effort M — risk low
  Why: the pack names planning friction as a known limitation. Sections need several `fm` calls with exact names, and T-0075 and T-0080 are bugs of exactly this kind. Earlier ideas fixed the bugs or added a `fm task plan` call, but neither removes the exact-name problem.
  Done when: `fm task plan T-x` writes a skeleton brief and the model edits it with Edit. `fm task ready` parses it, rejects unknown or missing headings with the exact heading names, and keeps the evidence links.

- **Delete the ~62 always-on rule lines that a gate already enforces** — CLEAN — value 4 — effort M — risk med
  Why: the pack says a gate enforces a rule while a hint can be ignored, and user is usage-sensitive. A rule that has both costs tokens twice.
  Done when: a script maps each rule line to the gate or hook that enforces it. The unmapped rules are listed and the mapped duplicates are removed. Always-on text drops by ≥25% and the e2e roundtrip still passes.

- **Retire per-event Python hooks for pure-observe events** — PERFORMANCE — value 3 — effort S — risk low
  Why: 13 classic hooks each cost a ~29 ms Python process. Several (MessageDisplay, Notification, SubagentStart/Stop, PostToolUse) only record events. assumption: they never block or inject.
  Done when: observe-only events append to the ledger through one tiny shell or a batched writer. The hook bench shows ≥50% less total hook time per tool call, and `fm doctor` passes.

- **Define one `fm ui` JSON view model that every surface renders** — CLEAN — value 4 — effort M — risk low
  Why: the pack has the statusline, `fm watch`, the output style and the mod, and earlier ideas treat the mod as a renderer. None names a single versioned view-model with per-surface size budgets (one line, band, Pane). `fm state --json` is a snapshot, not a layout contract.
  Done when: `fm ui --json --width N` returns the same fields for all consumers. A golden test covers widths 40, 80 and 160, and the statusline and `fm watch` consume it with no private formatting code.

- **Add `fm mode` as one switch for autonomy and quiet levels** — FEATURE — value 3 — effort S — risk low
  Why: the pack shows "full auto" in the statusline plus separate `fm quiet`, `fm run`, `fm notify` and "drive" behaviours. assumption: they are configured independently.
  Done when: `fm mode manual|guided|auto` sets all of them. The statusline shows the mode, and a test verifies each mode's resulting gate, notify and quiet settings.

- **Gate subcommand sprawl behind `fm help` tiers** — CLEAN — value 3 — effort S — risk low
  Why: ~45 subcommands, and the model has to choose among them correctly. assumption: the model gets the list from the rule text or `--help`.
  Done when: `fm help` shows ≤10 core commands, and the rest sit under `fm help --all`. Rule text references only core commands.

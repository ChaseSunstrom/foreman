# Brainstorm — lens: simplicity

- **Derive the tier instead of asking for it** — FEATURE — value 4 — effort M — risk med — category: ceremony
  Why: pass 1 had to add a rule telling an S task that touches 3+ code files to re-tier, so the declared tier is often wrong. Compute it from the impact map (files, importers, guard/state paths touched) and let the brief state only an override reason.
  Done when: a brief with no tier gets one computed from `fmmap` impact, and a replay of the last 50 finished tasks shows the computed tier matches the final tier at least as often as the declared one did.

- **Fold every evidence kind into one event type** — CLEAN — value 4 — effort L — risk med — category: ledger
  Why: the last day added inconclusive runs, assumed/verified facts, surprises, hypotheses, oracle examples, and revisit triggers, each with its own verb, store and UI card. One `evidence` event with a `kind` field, one reader and one card renderer would make the next kind a row, not a feature.
  Done when: all existing kinds read and write through one function, the old verbs still work as aliases, and adding a test-only kind needs zero changes outside a kind table.

- **Run all child-spawning through one runner** — CLEAN — value 4 — effort M — risk low — category: architecture
  Why: `fmideas`, `fmresearch`, `fmbench`, `fmevolve` and the reviewer each spawn children, and the budget caps, shared prefix and tool-less mode were added piecemeal. A single `spawn_child(role, prefix, cap)` gives one place for caps, caching and the spend ledger. (assumption: they don't already share one.)
  Done when: grep shows one subprocess call site for model children, and a test shows a cap violation aborts every role the same way.

- **Collapse the brainstorm pack to clusters with status** — PERFORMANCE — value 3 — effort S — risk low — category: tokens
  Why: the "ideas so far" list repeats the same idea 5–8 times (flaky, atomic state, guard receipts, bench ablation), spending child tokens on dedup rather than thought. Send ~25 cluster headlines, each tagged shipped, open or cut, with counts.
  Done when: the same pack builds at under 40% of its current size and a child given it proposes no idea whose cluster is tagged shipped.

- **Cap the open inbox with an expiry rule** — FEATURE — value 3 — effort S — risk low — category: backlog
  Why: about 17 items stay interleaved across families and keep reappearing as re-proposals. Cap open items at 8, and an item not pulled in 3 passes is archived with a one-line reason and can be revived by one command.
  Done when: adding a 9th item shows which one it displaces, and archived items show in `fm friction` with their reasons.

- **Give every fm verb one default line and a `--json` flag** — CLEAN — value 3 — effort M — risk low — category: CLI
  Why: the UI view model (`fmwatch`) and the CLI each format the same facts separately, and every new feature added a bespoke print path. One formatter table keeps the CLI to one line by default and gives the UI and MCP server the same data.
  Done when: a suite test fails if a verb lacks `--json`, and the pane and CLI agree on the same fixture.

- **Wild: Make features switchable modules that double as ablation** — FEATURE — value 5 — effort L — risk high — category: modularity
  Why: the pack wants ablation by leave-one-out bench, calm mode and a smaller surface, and these are the same need. Declare each feature (hooks, nudges, verbs, cards) as a module in one manifest. Then a profile turns modules on, and `fm bench` can turn one off to measure its value. wild.
  Done when: `fm bench --without <module>` runs a case with that module's hooks disabled, and a "minimal" profile enables only the edit-needs-brief, evidence-on-done and guard modules.

- **Wild: Project all state from one append-only event log** — CLEAN — value 4 — effort L — risk high — category: state
  Why: a crash left truncated brief/state JSON and zero-byte objects, and the fix so far has been detection (doctor). If the briefs, queue and state are views over a single log, recovery means replaying it, and rewind and time travel become free. wild.
  Done when: deleting the derived state files and running `fm doctor --repair` rebuilds identical state from the log on a fixture project.

- **Wild: Require one deletion per feature** — CLEAN — value 3 — effort S — risk low — category: discipline
  Why: 704 tests, dozens of modules and an always-on rules file capped at 120 lines mean every addition competes for attention. A `fm task close` check on FEATURE briefs asks which verb, rule line, or hint the change replaced, and accepts "none, because…" as a recorded answer. wild.
  Done when: closing a FEATURE brief without a replaced-item entry or a stated reason is refused, and the answers are listed by `fm friction`.

- **Wild: Let `fm` with no arguments be the whole interface** — FEATURE — value 4 — effort M — risk low — category: UX
  Why: the user asks for ever more features, and the stranger test is queued to find where newcomers stall. Bare `fm` prints one sentence on where things stand and the single command to run next, with everything else behind `fm help <topic>`. wild.
  Done when: in a fresh toy repo, a session that sees only the output of bare `fm` reaches a closed task within 5 commands.

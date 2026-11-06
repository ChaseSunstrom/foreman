# Brainstorm — lens: simplicity

- **Hard-cap the always-on rules at 2 KB with a CI check** — CLEAN — value 4 — effort S — risk low — category: rules
  Why: rules/foreman.md is ≈5.7 KB loaded every turn, and the user is usage-sensitive. Prior ideas say "trim" or "delete" but none sets a ceiling that fails the build.
  Done when: `fm check` fails if plugin/rules/foreman.md exceeds the byte cap, and passes after the file is trimmed under it.

- **Make guard false positives self-explaining with a single rewrite line** — FIX — value 5 — effort M — risk low — category: guard
  Why: most recent friction is guard false positives on Claude's own edit/probe commands, each costing a rewrite. Block messages should name the one safe form.
  Done when: every block category prints "Instead: <command form>", and a test asserts that form is allowed by the guard.

- **Freeze the guard: new rules need a real-command replay failure first** — CLEAN — value 4 — effort M — risk med — category: guard
  Why: the last ~12 commits are all guard patches (backticks, keywords, heredocs, $'…'), each fixing a bypass found by chance. Assumption: a replay corpus can be built from ledger commands.
  Done when: a guard change is rejected by `fm check` unless a corpus case that fails before it and passes after is added in the same commit.

- **Render every Foreman surface from one function, `view(state) -> sections`** — CLEAN — value 4 — effort M — risk med — category: ui
  Why: the user complained that the dashboard top, AC and audits, buttons and panels don't match, and that it is duplicated at the bottom of the chat. Duplication points to several render paths.
  Done when: the dashboard, band and chat summary all call the same function, and a test shows no section is rendered twice.

- **Remove the dashboard from the chat when the pane is open** — FIX — value 4 — effort S — risk low — category: ui
  Why: the user said "the dashboard is duplicated at the bottom of the chat even though there's a panel on the top right".
  Done when: with the pane open, a turn's output contains the dashboard zero times, and with it closed, once.

- **Collapse self-improvement into `fm task finish` output** — CLEAN — value 3 — effort S — risk low — category: loop
  Why: the friction digest, the 2 h wait and the 3-task cadence are three triggers for one loop. Assumption: one rule ("on finish, if friction exists and the last pass is over 2 h old") covers all three.
  Done when: the cadence counter is deleted, and a test shows a pass triggers only from finish.

- **Delete guard categories that have never fired for real** — CLEAN — value 3 — effort S — risk med — category: guard
  Why: the guard has many categories (system, remote, plugin…) and is admittedly "a speed bump, not a sandbox". Unused rules add false-positive surface. Assumption: the ledger records which categories blocked.
  Done when: a report lists per-category real fires, and categories with zero fires in N tasks are removed with the tests still green.

- **Wild: "Boring mode" that prints one line per turn unless blocked** — FEATURE — value 3 — effort M — risk low — category: quiet
  Why: wild. The user wants quiet, Foreman-styled replies and cares about token economy, so the default would be a single status line, with panels only on a block.
  Done when: with boring mode on, a normal turn shows ≤1 Foreman line, and a gate block shows the full panel.

- **Wild: Keep a 20-line budget for the whole dashboard** — FEATURE — value 3 — effort M — risk low — category: ui
  Why: wild. The dashboard has many sections (queue, inbox, gates, activity, subagents, files) and "not everything is shown" was a complaint, so a hard budget forces priority.
  Done when: at any state the dashboard renders in ≤20 lines, and overflow becomes a "+N more" row.

- **Wild: Make a "would anyone miss it" report that proposes deleting unused commands** — CLEAN — value 3 — effort M — risk med — category: pruning
  Why: wild. 45 subcommands are listed in the ideas already, yet nothing measures use. Assumption: ledger events record the commands invoked.
  Done when: `fm doctor --usage` lists commands unused in the last 30 days, and one flagged command is removed by a task.

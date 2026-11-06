# Brainstorm — lens: capability map

- **Add `fm watch` that reruns affected checks on save** — FEATURE — value 4 — effort M — risk low — category: live feedback
  Why: `fm check --affected` exists, but a model or person has to remember to run it after each edit. Assumption: the watcher reuses the content-hash memo, so unchanged files cost nothing.
  Done when: saving a file in `plugin/tests/fixtures/instruments/repo/app.py` prints one verdict line within 2 s.

- **Add shell completion for verbs, task ids and playbook names** — FEATURE — value 4 — effort S — risk low — category: shell ergonomics
  Why: the top-level verb surface is large and task ids like T-1802 are hard to type. No completion exists in the pack.
  Done when: `fm task <TAB>` lists verbs and open task ids in bash, zsh and fish, and a test covers each shell's script.

- **Give tasks `depends-on` edges and skip dependents in the queue** — FEATURE — value 4 — effort M — risk med — category: queue planning
  Why: blocked items such as T-0325 and T-0335 carry their reasons as prose only, so the queue cannot route around them.
  Done when: a task whose dependency is not closed is skipped by the queue, and `fm status` names the edge that holds it.

- **Sync the backlog two ways with Linear or Jira** — FEATURE — value 3 — effort L — risk med — category: tracker sync
  Why: the backlog lives only in local files. Assumption: the user's team tracks work in an external tracker.
  Done when: a local backlog item creates an issue, and closing that issue closes the task on the next sync.

- **Post run-state events to any webhook (Slack, Discord, Matrix, ntfy)** — FEATURE — value 4 — effort S — risk low — category: notifications
  Why: the ideas so far cover phone approval and lock-screen mirrors, but no generic delivery channel. Outbound messages leave the machine, so the payload must stay minimal.
  Done when: a needs-you event posts once to a configured URL, with the task id and title only and no transcript text.

- **Fan one change out across N files, each with its own gate** — FEATURE — value 3 — effort L — risk med — category: batch changes
  Why: codemod learning exists, but nothing applies a change to many files and proves each one separately. Assumption: a partial pass is useful, so partial results are kept.
  Done when: a rename applied to 40 files reports which files passed their gate and which were reverted, with the failing check for each.

- **Let a gate be a manifest-defined runner in any language** — FEATURE — value 3 — effort M — risk med — category: extensibility
  Why: gates are tied to the stacks in the lib cards (python, tailwind), so a Go or Rust project needs code changes in Foreman.
  Done when: a Go gate declared in a manifest runs under `fm check` and its verdict lands in the journal.

- **Ask the journal a question in plain English** — FEATURE — value 3 — effort M — risk low — category: history search
  Why: `fm code why` explains one run, but nothing answers questions across history, such as when the gate lock last held over five minutes.
  Done when: "when did the gate lock last hold over 5 minutes" returns the matching journal events with their ids, using only local data.

- **Load receipt and UI strings from locale files** — FEATURE — value 2 — effort M — risk low — category: localization
  Why: assumption: some users will not read English. Every string is currently hard-coded.
  Done when: a locale file replaces the receipt strings, and a test fails when a key is missing from any locale.

- **Wild: speak a one-line summary aloud when a run needs you** — FEATURE — value 2 — effort M — risk low — category: voice output
  Why (wild): the user looks away while work runs, and a spoken twelve-word summary of the blocked question would reach them without a screen.
  Done when: a needs-you event is spoken through the system text-to-speech, and it stays silent while the pane is focused.

- **Wild: keep refused commands in a dead-letter office and retry them when the rules change** — FEATURE — value 2 — effort S — risk med — category: guard memory
  Why (wild): every guard refusal is lost once the run moves on, though a rule change could make the same command safe.
  Done when: a refused command is listed with the rule that stopped it, and it re-runs through the guard after that rule changes.

- **Wild: serve the status screen as a text door on localhost** — FEATURE — value 1 — effort S — risk low — category: retro interface
  Why (wild): a bulletin-board style door costs little and would delight the people who like the terminal's old style.
  Done when: `nc localhost <port>` shows the status screen and closes cleanly.

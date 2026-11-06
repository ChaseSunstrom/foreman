# Brainstorm — lens: simplicity

- **Cap the top-level fm surface at twelve verbs** — CLEAN — value 4 — effort S — risk low — category: command surface
  Why: `fm dojo` and another command share help position 306, so `test_help` fails. A flat list of verbs is what makes the next collision likely.
  Done when: a test fails if `fm --help` lists more than twelve top-level verbs, and the current help passes it.

- **Collapse task states to three: queued, running, needs you** — CLEAN — value 4 — effort M — risk med — category: task states
  Why: the open work mixes `deferred`, `blocked` and `open` as separate states. A deferral that comes back at midnight (T-1802) is a state the user had to reason about.
  Done when: `fm status` prints only those three headings, and every existing state maps onto one of them in a test.

- **Make the rules file the only place a setting can live** — CLEAN — value 4 — effort M — risk med — category: settings
  Why: T-1611 added run, project and everywhere scopes plus repo policy pins in one commit. Four places answer "where does this come from?"
  Done when: `fm config explain <key>` prints one effective value and its single source, and no key resolves from more than one file.

- **Cut the usage burn to one budget knob** — CLEAN — value 3 — effort S — risk low — category: usage budget
  Why: T-1796 added a compact threshold, a builder model choice and a watchdog. Each is a separate knob, and the user has to know all three to keep burn down.
  Done when: `fm budget` prints the one resolved value, and a test shows each old knob maps to it.

- **Give each task a slug as well as its T-number** — FEATURE — value 3 — effort S — risk low — category: task naming
  Why: the user refers to work by content ("the defer --until bug"), while the pack lists only T-1802 and similar IDs.
  Done when: `fm task show <slug>` and `fm task show T-1802` return the same task.

- **Answer the stalled card with enter or any other key** — FEATURE — value 3 — effort S — risk low — category: stall handling
  Why: T-1373 gave the stalled card `w`, `k` and `m`. Three keys to remember is more than a stall needs.
  Done when: a test sends enter and sends an unrelated key to the card and gets continue and stop respectively.

- **Generate the command reference from the command table** — CLEAN — value 3 — effort M — risk low — category: docs drift
  Why: `MASTER.md` and the site copy hand-written command lists, and the pack shows them describing bench variants that have moved.
  Done when: the docs' command section is built from the registry, and the build fails when a documented command is missing from it.

- **Send brainstorm children two fields per idea: value and effort** — CLEAN — value 3 — effort S — risk low — category: brainstorm format
  Why: each idea carries seven fields, and the ideas-so-far list runs to about 300 entries that nobody reads in full.
  Done when: the parser accepts the two-field form, and a child output in that form round-trips through it.

- **Drop the ideas-so-far list from each round's pack** — CLEAN — value 4 — effort S — risk low — category: context size
  Why: the pack's ideas-so-far list is the largest part of every child's input, and the children are only asked to avoid repeats. Keeping just the newest round's titles would do most of that job.
  Done when: a pack built for a new round is under a fixed character cap, and a test checks that the list holds at most one round.

- **Uninstall with one command that removes what install wrote** — FEATURE — value 3 — effort S — risk low — category: install lifecycle
  Why: `fm install-user` writes a symlink, settings and hooks, and nothing records them for removal. Users cannot cleanly back out.
  Done when: install writes a manifest, and `fm uninstall` leaves no file from the manifest on disk in a test.

- **Wild: hold every default command's output to one 24-row screen** — CLEAN — value 2 — effort S — risk low — category: output size
  Why: assumption: long output is what makes a terminal feel busy. A screen-height cap forces detail behind a flag.
  Done when: each default fm command, run in a 24-row pty, fits its output on one screen.

- **Wild: lint user-facing output against a short jargon list** — CLEAN — value 2 — effort S — risk low — category: plain language
  Why: wild: "lens", "ceremony" and "burn" appear in the pack as product words. A list of banned internal words in output forces plain names.
  Done when: a test fails when `fm status` or a close receipt contains a listed word.

# Brainstorm — lens: simplicity

- **Compile one prompt tree into every injected surface** — CLEAN — value 4 — effort M — risk med — category: footprint
  Why: the rules (1k words), SessionStart context, per-turn hints and skill stubs are written separately, and the pack shows each trimmed on its own. Keep one `prompt/` source of short atoms with a token cost on each. Build the rules, the SessionStart text and the stubs from it, and print the cost per surface in `fm doctor`. This differs from the existing cap ideas because there is one source and the surfaces are derived from it.
  Done when: editing one atom changes the rules file and the SessionStart text in a rebuild, and CI prints a per-surface token total that fails over a budget.

- **Add `fm nope` to silence a message class for good** — FEATURE — value 4 — effort S — risk low — category: noise
  Why: assumption: users tire of repeated notes (close warnings, "Next:" hints, step nudges) and now have to go edit settings. Making the user the pruner is cheaper than measuring ignored notes. Every note carries a short class id, and `fm nope <id>` mutes it for this project. `fm nope --list` shows what is muted and can undo it. Safety-class messages cannot be muted.
  Done when: after `fm nope tier-drift`, the next triggering task prints no tier-drift line, `--list` shows it, and a guard block id is refused with an explanation.

- **Give the CLI a noun-verb grammar with a forwarding table** — CLEAN — value 4 — effort M — risk med — category: cli
  Why: 108 verbs, a 231-line `--help` and 46 verbs never run in 11 days. Merging into `inspect` and `stats` helps, but without a rule it regrows. A test requires every verb to be `fm <noun> <verb>`, with the nouns task, queue, lane, state, guard, inspect, stats. Old names stay as one-line forwards that print the new form once.
  Done when: a test fails on any verb outside the grammar, and an old verb still works and prints its replacement.

- **Show the 20 deny rules as three named presets** — FEATURE — value 4 — effort S — risk low — category: install trust
  Why: newcomer evidence item 2 says the install sets bypass mode and 20 deny rules with only "asks you to confirm once". Naming presets such as `minimal`, `standard` and `paranoid` makes the trust ask legible. `fm guard preset` shows the active one and its rules, and the installer shows the name plus a one-line description.
  Done when: the install output names the preset, `fm guard preset paranoid` switches it, and `fm doctor` reports which preset is active.

- **Require a 12-word purpose sentence per module** — CLEAN — value 3 — effort S — risk low — category: footprint
  Why: the audit found overlapping modules: three child launchers, seven git helpers, a fmwatch that duplicates state. A module that can't state one purpose in 12 words is a merge or delete candidate. A lint extracts each module's first docstring line, and `fm map` lists the modules with their sentences and flags overlaps.
  Done when: the lint fails on a module with no purpose line or one over 12 words, and the map shows 48 sentences.

- **Make `fm task new` adopt the matching capture** — FIX — value 4 — effort S — risk low — category: newcomer
  Why: evidence item 6 says capture followed by `task new` duplicates, and `--help` lists no valid values or example. When a recent open capture matches, `task new` offers to adopt it. If there is no match it infers the type. The help ends with the valid types and tiers and one worked example.
  Done when: capture then `task new` with the same words leaves one item, and `--help` shows the values and the example.

- **Wild: Run an annual "defend or delete" report** — CLEAN — value 3 — effort M — risk low — category: footprint — wild
  Why: assumption: features outlive their use because no one is asked. Each quarter `fm labs` lists every verb and module with its fire count and age, then drafts one deletion diff for the least-used cluster (the self-improvement stack is the likely first target). The user answers keep or cut, and a kept item is exempt for a year.
  Done when: the report lists the bottom cluster with counts, and answering "cut" produces a diff that passes the test suite.

- **Wild: Add `fm one` as the whole interface for week one** — FEATURE — value 4 — effort M — risk med — category: newcomer — wild
  Why: A5/A9 show newcomers hit a wall of verbs. `fm one` infers the one next action (init, capture, check, finish) and prints it plus its own command line. It teaches the real verbs by example and goes away after the third task.
  Done when: on a fresh project three runs of `fm one` walk init, the first gate and the first finish, each printing the underlying `fm` command it ran.

- **Wild: Start new projects in observe-only mode** — FEATURE — value 4 — effort M — risk med — category: trust — wild
  Why: rival plugins add commands without rewriting `~/.claude`, and Foreman asks for a large trust grant on day one. For the first N tasks Foreman only records and says what the gate would have done. Enforcement is switched on after N tasks, or earlier by one command.
  Done when: a new project's first task records "would have blocked" lines without blocking, and enforcement starts at task N+1.

- **Wild: Print a diff of the user's own verb habits** — FEATURE — value 2 — effort S — risk low — category: delight — wild
  Why: assumption: `fm repeats` suggests single test modules as every-task gates, which is bad advice. Instead, once a week print a three-line note of the verbs they use and the ones a shorter form would cover. Suggest only whole-suite gates.
  Done when: the note appears once a week, and `fm repeats` never proposes a single test module as a gate.

- **Unify the three result shapes for `fm status`, `fm task show` and `fm digest` into one view model** — CLEAN — value 3 — effort M — risk med — category: output
  Why: the newcomer's `fm status` prints an unexplained STATE doc ("Drive: on"), and `fm digest` shows 159 "ungraded" folded tasks. One view model, with folded tasks rolled up under their parent, feeds all three, and each field has a one-line gloss.
  Done when: all three verbs render from one function, folded tasks show under their parent, and every status field has a gloss.

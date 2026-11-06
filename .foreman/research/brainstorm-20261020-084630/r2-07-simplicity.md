# Brainstorm — lens: simplicity

- **Deploy the site on every push to main** — CLEAN — value 4 — effort S — risk low — category: release
  Why: the user had to ask "Release Foreman 1.2.36 so the feature pages deploy", then asked for 1.2.38, 1.2.39 and 1.2.40 for page fixes. A version bump is the only way to publish a typo fix.
  Done when: a commit that touches only `site/` updates the live Pages site within CI time, with no version change.

- **Write each guard rule as one data row with its own examples** — CLEAN — value 4 — effort M — risk med — category: guard
  Why: the guard must never weaken, and the measured corpora are 24 dangerous and 25 everyday commands, held apart from the rules. Each row would hold the pattern, one command it must stop and one it must allow. A new rule without both examples would be refused by `fm doctor`.
  Done when: `fm guard rules` prints every rule beside its two examples, and deleting a rule's example fails the doctor.

- **Merge lessons, hints, fixes and cards into one "note" kind** — CLEAN — value 4 — effort L — risk med — category: concepts
  Why: the pack shows cards (`fm lib`), lessons with confidence (T-0217), and a long ideas list of hints, fixes, standing orders and playbooks. That is many stores with overlapping jobs. Assumption: today they differ mostly by file location, not by behaviour.
  Done when: one reader serves recall for all four, and the old file kinds load through a one-time migration.

- **Delete brief fields that no decision reads** — CLEAN — value 3 — effort S — risk low — category: briefs
  Why: briefs carry type, effort, risk, status and origin. Assumption: some of them (risk, for one) change nothing about what Foreman does. A grep of the readers would show which.
  Done when: a report lists each field with its readers, and the unread ones are removed from `fm task new` and the stored format.

- **Make the install a single command with no questions and no leftovers on removal** — FEATURE — value 4 — effort M — risk low — category: onboarding
  Why: T-0418 (update the installed foreman-ui) and the first-run ladders T-0862/T-0863 show setup is still several steps. The install is split across the plugin, the mod and `fm doctor`.
  Done when: one command on a fresh HOME yields a passing `fm doctor`, and the reverse command leaves `~/.claude` byte-identical to before.

- **Show three verbs after install and hide the rest until used** — FEATURE — value 3 — effort S — risk low — category: help
  Why: `fm` has dozens of verbs, and `fm usage --prune` exists because many go unused. Revealing a verb on first need would keep the help short without deleting anything.
  Done when: a new HOME's `fm help` lists at most three verbs plus "more", and using a verb adds it to the list.

- **Replace the settings pile with measured defaults and one override file** — CLEAN — value 3 — effort M — risk med — category: config
  Why: the pack mentions an escape-hatch flag set, the `CLAUDE_CODE_AUTO_COMPACT_WINDOW` tuning and per-feature flags. Assumption: most of them have never been set to a non-default value by the user.
  Done when: a usage count shows each flag's non-default rate, and every flag below 1% is removed.

- **Wild: `fm once "request"` — a stateless run that writes nothing to disk** — FEATURE — value 3 — effort M — risk low — category: ephemeral
  Why: wild. The first-task-per-session ceremony costs turns (the "fewer turns spent on Foreman itself" request). A run with the guard and proof habit but no task file, ledger or lessons would be the cheapest trial for a skeptical newcomer.
  Done when: after `fm once`, `git status` and `~/.foreman` are unchanged, and the guard and prove-before-done still fire.

- **Wild: Print the whole product as one screen of text on bare `fm`** — FEATURE — value 3 — effort S — risk low — category: help
  Why: wild. It would give 12 lines covering what Foreman is doing now, what it will do next and the one command that matters. Everything else sits behind `fm help`.
  Done when: bare `fm` output is at most 12 lines at 80 columns and a snapshot test pins it.

- **Wild: Make Foreman's injected text a single file a user can read in two minutes** — CLEAN — value 4 — effort M — risk med — category: transparency
  Why: wild. The cost parity goal (T-1231) is about what Foreman adds each turn. Collecting every hook note, skill listing and compaction message into one file with sizes would make the tax readable and arguable by a person.
  Done when: `fm tax` prints each injected string with its byte count, and the total matches a recorded session's measured added context.

- **Retire the blocked Codex, Gemini and opencode trio into an `adapters/` branch** — CLEAN — value 3 — effort S — risk low — category: scope
  Why: T-0335, T-0336 and T-0337 are blocked, T-0794 already lists "retire adapters", and `fm code --worker` (T-1214) now covers other CLIs by template. Assumption: nobody runs the adapters today. A usage count would confirm it.
  Done when: the adapters are gone from the main tree, the three briefs are closed with a revive condition, and the gates stay green.

- **Cut the skill count by merging skills that share a trigger** — CLEAN — value 3 — effort M — risk med — category: context cost
  Why: 15 skills take about 3,200 of 9,600 listing characters, re-sent after every compaction in 2.1.304. Skills that are always loaded together could be one. This is narrower than a single router skill.
  Done when: the Foreman share of the skill listing drops by at least a third, and the e2e roundtrip passes unchanged.

- **Make one "reason" flag replace the escape-hatch flags** — CLEAN — value 2 — effort S — risk low — category: CLI
  Why: `--reason` was added recently for fewer turns, which suggests it can absorb the rest. Assumption: the other bypass flags exist only to make a refusal go quiet.
  Done when: every skip path accepts only `--reason TEXT`, and the old flags print a one-line migration note for one release.

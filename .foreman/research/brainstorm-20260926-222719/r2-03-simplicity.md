# Brainstorm — lens: simplicity

The remaining simplicity ideas are mostly marginal. About 30 of the ~200 already cover pruning, profiles, single renderers and gate consolidation. Here are five that go beyond them.

- **Route command parsing through one shared module** — CLEAN — value 3 — effort M — risk med
  Why: assumption: the guard (dangerous commands), evidence auto-capture (exact verify match), verify lint (pipe hides exit, not on PATH), `fm quiet`, and the cached-pass key each parse Bash strings separately. That means several near-duplicate shlex and regex paths that can disagree.
  Done when: one `cmdparse` module is the only place that splits or normalizes commands. A table-driven test feeds the same 40 command strings to guard, lint and evidence capture and shows consistent classification.

- **Generate the command list from one registry and fail tests on drift** — CLEAN — value 3 — effort M — risk low
  Why: the CLI has 30+ commands, and the rules, `fm help`, skills, `fm docs` and the playbooks all name them. Ideas so far trim these lists but none makes them derived. Assumption: they are hand-maintained today.
  Done when: rules, help and skill stubs read a single command registry (name, one-line purpose, tier of visibility). A test fails if any text names a command that isn't registered, or a registered command has no purpose line.

- **Replace free-form verify shell with a tiny check vocabulary** — CLEAN — value 4 — effort M — risk med
  Why: the recent verify-command lint (not on PATH, can't fail, pipe hides exit) is code that polices a free-form field. If criteria are one of `run CMD exits 0`, `test NAME passes`, `file P contains S` or `file P absent`, the malformed cases can't be written. Free shell remains only as an explicit `run` kind.
  Done when: `fm task plan` rejects criteria outside the vocabulary. The three lint rules are deleted or reduced to the `run` kind. Existing briefs still load.

- **Keep one bounded "state of play" block per task instead of separate checkpoint, resume note and handoff** — CLEAN — value 3 — effort M — risk med
  Why: PreCompact checkpoints, resume notes, "ruled out:" lines and failure carry-over are all described as separate mechanisms that read and write different places. Assumption: they hold overlapping content.
  Done when: one ≤600-char block is rewritten in place. SessionStart, PreCompact and `resume` all read and write only that block, and the old writers are removed. A compaction-then-resume replay test still recovers step, next action and ruled-out approaches.

- **Give every new gate, command and note a sunset date in the registry** — CLEAN — value 3 — effort S — risk low
  Why: usage counts and gate-yield ledgers are proposed separately, but nothing forces a decision. The candidate build alone adds ~25 features with no proof of value. Combined with the registry above, this makes removal the default.
  Done when: each registry entry carries `since` and `review_after`. `fm doctor` lists entries past review with zero uses or catches and queues one removal task per entry, awaiting a yes/no.

**Marginal:** verb-noun renaming (`fm task done`, `fm sentinel`, `fm gates` and so on) is worth under a value of 2 without real user friction. I'd skip it.

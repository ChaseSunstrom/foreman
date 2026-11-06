# Brainstorm — lens: approaches

- **Delta-debug the product to find what's safe to delete** — CLEAN — value 5 — effort M — risk med — category: subtraction
  Why: the pack has 1,388 skill files, 30+ deferred "Later from" tasks and a lean row that waits on measurement (T-2503). Earlier ideas rank by usage; none finds the minimal set that still passes. Run ddmin (delta debugging) over verbs, skills and hooks in a scratch copy against the zero-token exam arms and the suite. The surviving minimal set is the evidence, and the rest become removal candidates.
  Done when: `fm tidy --ddmin` prints a minimal feature set and a removable list, and a scratch copy with that list removed passes the suite and the zero-token arms.

- **Keep one footprint file that ship checks** — FEATURE — value 4 — effort M — risk low — category: lean gate
  Why: the pack already has separate ideas for line ratchets, token counts, cold-start and ledger caps, but no single place that holds them. Put verbs, skill files, injected tokens, hook p95, state MB and non-stdlib imports in one committed `footprint.json`. `fm ship` prints the delta, and growth needs a paired shrink or a recorded reason.
  Done when: a task that adds a verb with no deletion fails `fm ship` and names the number that grew. A paired deletion passes.

- **Move candidate-dead code to an attic before deleting it** — CLEAN — value 4 — effort S — risk low — category: reversible subtraction
  Why: the user's dropped ideas show caution about irreversible removal (the drop notes say "mostly built"). Move unused code to `plugin/attic/`, off the import path and still tested by one smoke test. Delete it for good only after 30 days with no restore.
  Done when: `fm tidy --attic NAME` moves a module and the suite stays green. `fm tidy --restore NAME` brings it back, and the permanent delete is refused before 30 days.

- **Use off-the-shelf dead-code finders as a zero-token lean pass** — FEATURE — value 4 — effort S — risk low — category: reuse
  Why: standing rule #1 says detection comes from the ecosystem's own tools found via manifests. Python (vulture, ruff F401/F811) and the TS mods (knip, ts-prune) already cover unused code. Run them when `fm find` runs and file CLEAN captures. Tool output only nominates; the ddmin and attic steps decide.
  Done when: `fm find --lean` on this repo lists at least one tool-flagged unused symbol per language, each with the tool's name. A missing tool queues an install through #5 instead of failing.

- **Check imports against an allowlist across all of `plugin/lib`** — SECURITY — value 4 — effort S — risk low — category: supply chain
  Why: the ideas list holds goal modules to the standard library. The same test over the whole 133-file lib is not listed, and Foreman runs in bypass-mode sessions. A static AST test with an explicit allowlist makes a new dependency a visible, reviewed change.
  Done when: a test fails when a lib module imports a non-allowlisted name, and the allowlist change is the only way to make it pass.

- **Keep an exec manifest of every binary Foreman may spawn** — SECURITY — value 4 — effort M — risk low — category: attack surface
  Why: the unattended paths (drive, tick, lanes) run commands. A static scan of `subprocess` calls produces a committed list of binaries with their call sites. A new binary needs a manifest line, and `fm doctor` flags one that isn't there.
  Done when: adding `subprocess.run(["curl", ...])` to a lib file fails the manifest test until a line is added.

- **Compile guard rules into Claude Code's native deny rules** — SECURITY — value 3 — effort M — risk med — category: defence in depth
  Why: the pack says the guard is a hook, and its liveness and crash modes are open questions (hook fail-open, "probe guard liveness"). Generated `permissions.deny` entries survive a dead hook. Trade-off: native patterns are cruder, so this covers only the clear-cut rules, and the hook stays the precise layer.
  Done when: with the hook disabled, `rm -rf ~` is still denied by the generated settings. `fm doctor` flags drift between the rule table and the settings.

- **Find near-duplicate skill files by content similarity** — CLEAN — value 3 — effort S — risk low — category: skill bloat
  Why: skills are 1,388 of 2,125 files. Unused skills were already proposed, but duplication was not. A stdlib shingle-hash pass lists pairs above 80% similarity as merge candidates, at zero tokens.
  Done when: `fm tidy --skills` lists the similar pairs with their scores, and a seeded duplicate appears in the output.

- **Print a lean receipt on every closed task** — FEATURE — value 3 — effort S — risk low — category: legibility
  Why: the sweep's lean row only counts growth in aggregate. A close-time line such as "+212 lines, +1 verb, −3 files, +180 injected tokens" ties growth to the task that caused it. It reuses footprint data and adds no new gauge.
  Done when: `fm task finish` prints the delta line, and a task with no change prints "no footprint change".

- **Plant a dead-weight canary verb (wild)** — FEATURE — value 3 — effort S — risk low — category: self-test
  Why: assumption: nobody knows whether the subtraction pipeline works. Each release carries one deliberately useless verb, `fm canary-N`. If the usage-prune and tidy flow doesn't propose it within 60 days, the pipeline is broken. Trade-off: it adds a verb, so it must retire itself on detection.
  Done when: the canary appears in the prune list within 60 days of zero use. If it doesn't, `fm doctor` goes red.

- **Hold a nightly code-golf match against each verb (wild)** — PERFORMANCE — value 3 — effort L — risk med — category: shrink
  Why: assumption: the cheapest overnight work is a Haiku child trying to rewrite one verb's module in half the lines while keeping its tests green. A smaller green version becomes a proposal and is never auto-merged. It converts idle budget into subtraction.
  Done when: a nightly run produces at least one smaller candidate that passes the module's tests, with the line counts before and after.

- **Run a mass-extinction rehearsal in a scratch home (wild)** — SECURITY — value 3 — effort M — risk low — category: resilience
  Why: the drill exists for ledger deletion. The same pattern across code, with random 20% of non-core verbs and skills removed, shows which failures are loud and which are silent. A silent failure means a removed part was doing hidden work, or a reader hides its own absence.
  Done when: a drill run prints, per removed item, whether anything noticed, and it lists the silent cases.

Next question: which of Foreman's own protections would still work if the Python lib failed to import at all, and does anything outside it say so?
Next question: what is the smallest set of capabilities the user's actual week of sessions touched, and how does it compare with what ships?

# Brainstorm — lens: docs against code

- **Turn code comments that say never/always/only into checked assertions** — FEATURE — value 4 — effort M — risk low — category: docs-vs-code
  Why: assumption: the code's own comments ("never blocks", "only called from the drive") are claims no gate reads; the doc sweeps in the list cover MASTER, README and the site, not comments. This is cheap to extract with a grep and an AST pass.
  Done when: a scan lists every comment with an absolute word beside the test that guards it, and an unguarded one is printed as unproven, with a planted false comment caught in a fixture.

- **Give each gen-0 MUST and NEVER a falsifier command** — FEATURE — value 5 — effort M — risk med — category: proof
  Why: the cold-read rule judges seeds "against gen-0's MUSTs and NEVERs", but the pack shows no per-clause runnable check on the product itself (Mission 4: "meaning is the largest unproven class").
  Done when: `fm genesis check` prints one row per clause with a command and its last result, and a clause with no command is shown as unproven.

- **Test that every old name still works as promised** — FIX — value 4 — effort S — risk low — category: rename
  Why: the steers say "every old name keeps working" (the `fm` shim, `/foreman:`, `foreman@foreman`, `FOREMAN_*`), and the plugin ids, shims and renames map just moved. No listed idea checks the promise itself.
  Done when: a test iterates the renames map, the verb aliases and the old env names, runs each in a scratch home, and fails on any that does not resolve.

- **Diff documented defaults against the code's defaults** — FIX — value 3 — effort S — risk low — category: docs-vs-code
  Why: assumption: docs quote defaults (stall limits, the pace flag, MOONS_LOCAL's profile) that live in argparse and constants. T-2893 already shows a default leaking a user's endpoint name, a case where code and docs disagreed.
  Done when: a script extracts defaults from argparse and the LIMITS-style constants, finds the same names in MASTER.md, and exits non-zero on a mismatch.

- **Replay the README demo's commands and compare them with the SVG** — FIX — value 4 — effort M — risk med — category: demo
  Why: the README alt text bakes in "Claude Code 2.1.301" and a literal session, which conflicts with the rule to name the orchestrator only as any agent. The anchor `#the-Ward` also looks case-mismatched with a lowercase GitHub slug (assumption: the heading is "The Ward").
  Done when: the commands behind `demo/live.svg` re-run in a scratch repo and their output matches the frames' text, and every in-page anchor resolves case-sensitively.

- **Feed every blocked command shown in the docs to the Ward** — FEATURE — value 4 — effort S — risk low — category: guard
  Why: the README says the Ward stops "the commands you'd never want run". Each example block in the docs is a claim about guard behaviour, and the guard can be asked without running anything.
  Done when: every documented refused command gets a verdict from the guard, a doc example that is allowed fails the check, and a "refuses" line with no example is listed.

- **Lint relative-time words in docs** — CLEAN — value 2 — effort S — risk low — category: docs
  Why: assumption: with around 2,350 files and daily commits, words like "now", "new", "currently" and "recently" go stale. A date or a version would make them checkable.
  Done when: the lint flags those words in MASTER.md, README and the site, and an allowlist records the accepted ones with a reason.

- **Compare docstrings with real signatures and raises** — CLEAN — value 3 — effort M — risk low — category: docs-vs-code
  Why: `plugin/lib/sampo/` was just moved from the `fm*.py` shims, and the stale cold-read list in the dropped items shows paths drifting.
  Done when: an AST pass reports docstring parameters that don't match the signature or exceptions that are never raised, and a fixture with a planted mismatch is caught.

- **Make tests cite the doc claim they prove** — FEATURE — value 4 — effort M — risk low — category: proof
  Why: the list has claim ids pointing down at code. The reverse direction is missing: a `# proves: MASTER.md#anchor` tag in tests, so a changed test or a deleted test moves the claim's status.
  Done when: a reverse index lists tests per claim, and a claim whose only tagged test was removed shows as unproven in `fm doctor`.

- **Probe the failure paths that docs describe** — FEATURE — value 3 — effort M — risk med — category: verbs
  Why: docs say what happens with no `claude` on PATH, a missing ledger or a refused input (the standing rule: install and the task loop work with no `claude`). These are the least-run paths.
  Done when: a scratch-home test runs each documented failure (no agent on PATH, empty state, read-only plugin dir) and compares exit code and `Next:` line with the docs.

- **Wild: Make a child try to falsify each "cannot" and "refuses" sentence** — FEATURE — value 4 — effort L — risk med — category: red team
  Why: negative-capability claims ("never pushes without a grant", "installs nothing") sound safe and are the hardest to prove by example; assumption: no current exam targets them as a class.
  Done when: a sandboxed child gets one such sentence and a goal of making it false, and each claim leaves a "held" or "broken with repro" record.

- **Wild: Have a child write the doc sentence the diff implies, then diff it** — FEATURE — value 3 — effort M — risk low — category: docs
  Why: a tool-less child sees only a commit's diff and writes the sentence a reader should now find in MASTER.md. A missing or contradicted sentence is a docs gap found with no claim extractor.
  Done when: for 10 recent commits, the child's sentences are matched against the docs by search, and the misses are listed.

- **Wild: Check out the commit when each claim was written and test whether it was ever true** — FEATURE — value 3 — effort L — risk med — category: docs history
  Why: this is the reverse of replaying old claims on today's code. A claim false from day one is an aspiration, not drift, and should be labelled differently.
  Done when: for 20 sampled claims, a worktree at the introducing commit runs the claim's probe, and each result is recorded as "true then", "never true" or "can't tell".

Next question: which doc claims were read most often by sessions, via hook-logged reads of MASTER.md sections, so unproven ones can be ranked by exposure?
Next question: does a doc edit made by the user's own hand count as a proof of intent, or is it just as likely to drift?

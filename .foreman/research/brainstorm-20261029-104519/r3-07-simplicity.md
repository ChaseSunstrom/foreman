# Brainstorm — lens: simplicity

- **Delete the ambient test runner** — CLEAN — value 5 — effort M — risk med — category: deletion
  Why: four recent commits (T-1967, T-1974, T-1984, T-1987) patch overlap between ambient runs, `fm check` and `fm ship`. Each patch adds a new "skip if X is running" rule. Removing the background run removes the whole bug class, instead of guarding each pair of launchers.
  Done when: no code path starts tests except `fm check`, `fm ship` and an explicit `run.py` call, and a test greps the lib to prove it.

- **Replace the intake mini-language with plain markdown** — CLEAN — value 4 — effort M — risk med — category: intake
  Why: T-1989, T-1992 and the title-cut fixes all come from parsing `@path>`, `DONE-WHEN:` and block lines out of free text. A heading plus bullet format, with `@path` only inside a `Files:` line, leaves far fewer edge cases. Assumption: the old syntax stays readable for a release.
  Done when: a task pasted in the new format round-trips through `parse_intake` unchanged, and the old format still imports with a one-line deprecation note.

- **Accept PERF and PERFORMANCE as one task kind** — FIX — value 3 — effort S — risk low — category: vocabulary
  Why: the user typed "PERF:" in the T-1994 request, but the queue's kind is PERFORMANCE. Making the user remember the exact word is needless friction.
  Done when: `PERF:`, `PERFORMANCE:`, `FEATURE:` and `FEAT:` each capture a task with the canonical kind, and a test covers the alias table.

- **Show eight commands by default** — FEATURE — value 4 — effort S — risk low — category: help
  Why: the repo has 1248 skill files and a command surface that the open backlog admits is too big (T-0794 Slim Foreman, T-1909 `fm help task` refused). Progressive disclosure costs one list and deletes nothing.
  Done when: `fm help` prints at most 8 commands plus "fm help all", and `fm help all` lists every command with none missing.

- **Delete settings that nobody has ever changed** — CLEAN — value 3 — effort M — risk med — category: config
  Why: assumption. Many settings exist as escape hatches that the user never touched, and each one adds a branch to test. A local scan of the project's own config history would show which ones are safe to delete.
  Done when: `fm doctor --unused-settings` lists settings still at their defaults across all recorded state, and one listed setting is removed with its tests.

- **Stay silent when an upstream skill source changes but no used skill did** — FIX — value 3 — effort S — risk low — category: noise
  Why: the dropped item "Source anthropic-skills moved to ca45fc49: +1 −0 ~0" shows a notice about a bundle entry that grouped skills already seen. The user spent a decision on a non-event.
  Done when: a source bump that changes no skill the project has loaded produces no capture, and one that does names the skill.

- **Write commit subjects as one short line** — CLEAN — value 2 — effort S — risk low — category: history
  Why: recent subjects run past 150 characters and chain ids, such as "(T-2001: T-1998, T-1999, T-2000)". The detail already lives in the task record, so the subject can stay short.
  Done when: `fm ship` produces a subject of 72 characters or fewer with the task ids in the body, and a test enforces the limit.

- **Delete tests that cover nothing unique** — PERFORMANCE — value 4 — effort M — risk med — category: tests
  Why: `plugin/tests/` has 385 files, and the user keeps fixing the cost of running too much (T-1994). Per-test coverage would show the ones whose lines are fully covered by other tests. Assumption: coverage data is cheap to collect once.
  Done when: a report lists tests whose coverage is a strict subset of others, and removing one such batch keeps the mutation or fixture checks green.

- **Infer every gate and ask nothing on first run** — FEATURE — value 4 — effort M — risk med — category: onboarding
  Why: the map already finds gates (`fm doctor`, `roundtrip.py`, `bench_hooks.py`), and T-0862/T-0863 defer a tutorial. A start that needs no questions is simpler than a tour.
  Done when: in a fresh repo with a test command in CI, the first task runs with gates inferred and zero prompts.

- **Wild: Fail any release whose changelog needs more than one sentence** — CLEAN — value 2 — effort S — risk low — category: discipline
  Why: wild. A release that cannot be summarised in a sentence is two releases, which pushes against the "super ultimate improve in all ways" drift.
  Done when: the release script refuses a changelog entry over 200 characters and prints the split it suggests.

- **Wild: Keep a one-page kernel spec that the full tool must pass** — FEATURE — value 3 — effort M — risk low — category: spec
  Why: wild. Ten sentences define plan before edit, proof by an executed command, one task at a time, and the guard. Each has a black-box test. Any new feature that breaks one fails. This also anchors a Lite profile later.
  Done when: `fm kernel-check` runs ten scenarios against the installed build and prints ten passes.

- **Wild: Have Foreman describe itself in ten lines from its own code** — FEATURE — value 2 — effort M — risk med — category: legibility
  Why: wild. A generated summary of the real task lifecycle (states, gates, hooks) exposes complexity. If it cannot fit in ten lines, `fm doctor` says which part grew.
  Done when: `fm explain-self` prints at most 10 lines derived from code, and a test fails when a lifecycle state is missing from the output.

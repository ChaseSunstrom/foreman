# Brainstorm — lens: bold bets

Most of the remaining space is marginal. These are the few gaps I see that the ~200 earlier ideas don't cover.

- **Diff the public surface and entry-point behavior at done** — SECURITY/FIX/FEATURE guard — value 4 — effort M — risk low
  Why: assumption: `fm map` already knows entry points, but done only checks tests and criteria. Nothing reports what a change did to exported symbols, CLI flags, config keys or output shapes. Snapshot the surface with `ast` plus regex, and run a few smoke invocations on the start and end trees. List every difference and grep for its consumers. Unexpected drift outside the brief's scope becomes a gate finding.
  Done when: a task that renames an exported function used elsewhere makes `fm task done` list the removed name and its callers, and a purely internal change reports "surface unchanged".

- **Verify in a clean-room copy before done** — FEATURE — value 4 — effort M — risk med
  Why: assumption: gates run in the live tree, so a pass can depend on untracked files, gitignored build output or stale caches. Only red→green proof (`fm task prove`) uses a second tree, and it covers the start tree, not a clean copy of the result. Export HEAD plus the task's diff to a temp dir, then run the criteria and gates there.
  Done when: a criterion that passes only because of an untracked helper file fails the clean-room run and names the file.

- **Mirror CI: derive gates from the project's CI config and flag the gap** — FEATURE — value 4 — effort M — risk low
  Why: assumption: `fm map` finds gates from local files, but CI often runs extra steps (lint, typecheck, matrix versions). Green locally can still be red in CI. Parse `.github/workflows` and similar files for `run:` commands, and diff them against `fm check`'s gate set. Add the missing runnable ones and list the ones that can't run here.
  Done when: in a fixture repo whose workflow runs `ruff` and local gates don't, `fm check` reports "CI-only gate: ruff" and runs it when it is available.

- **Model cross-repo tasks with linked projects** — FEATURE — value 3 — effort L — risk med
  Why: assumption: state is keyed per project and a task has one scope. Changing a library and its consumer today means two unrelated tasks with no contract between them. Add `fm link PATH`, so a surface diff in one repo queues a pre-scoped follow-up brief in the linked repo, with the changed symbols as evidence.
  Done when: a surface change in repo A creates a queued brief in linked repo B naming the changed symbols, and unlinking stops it.

- **Audit with a different model than the executor** — SECURITY — value 3 — effort S — risk low
  Why: audits run through `claude -p`, and the pack doesn't say the model is varied. A reviewer sharing the executor's blind spots misses the same class of error. Pick the audit model per lens, using a different family or tier for the adversary and security lenses, and record which model reviewed. `--models` already exists for `fm run`.
  Done when: the audit record for a security-sensitive task names a reviewer model different from the executor's.

- **Harvest inline TODO/FIXME into ranked queued briefs** — FEATURE — value 2 — effort S — risk low
  Why: brainstorms treat TODOs as evidence, but nothing turns them into work. Scan comments during idle time or `fm doctor`, and dedupe against the queue and finished tasks. Rank by age from `git blame` and by hot files, then write pre-scoped brief stubs to the inbox.
  Done when: a repo with three TODOs yields three inbox stubs with file:line evidence, and a second run creates no duplicates.

- **Calibrate estimates against actuals** — FEATURE — value 2 — effort M — risk low
  Why: quote-before-focus and step ETAs exist, but nothing compares them to reality. Record predicted against actual tokens, turns and tier per task, then shrink or widen future quotes by type and tier. Warn when a running task passes 2× its quote.
  Done when: after five finished tasks, the quote for a similar task cites the measured ratio, and an overrun triggers exactly one note.

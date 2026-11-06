# Brainstorm — lens: bold bets

Most of the surface is already covered. These six are the ones I think are new and worth building; anything beyond them looks marginal.

- **Classify every failure as env, dependency, flaky, pre-existing, test-bug or regression, and say so in one line** — FEATURE — value 4 — effort M — risk low
  Why: the pack has a flaky rerun, a pre-existing label, a same-failure-3× thrash note and recurring-failure matching, but nothing that names the failure class on first sight (port down, missing module, permissions, stale build). Assumption: pattern rules over exit code and output cover most cases.
  Done when: a fixture set of 10 failure outputs gets the expected class and a diagnosis note of ≤200 chars on first occurrence, with no model call.

- **Detect generated and vendored files and keep both edits and reads away from them** — SECURITY — value 3 — effort S — risk low
  Why: the guard covers dangerous commands and protected paths, and the outline note fires on whole Reads of large files. Neither recognizes "@generated", "DO NOT EDIT", vendored dirs, minified files or snapshots, which are common token sinks and wrong-place edits. Assumption: header and path heuristics are enough.
  Done when: an edit to a file with a generated header is denied with the generator command (or "edit the source"), and a Read of a lockfile or minified file gets an outline or skip note.

- **Serve a diff instead of a full re-read when a file changed since Claude last read it** — PERFORMANCE — value 3 — effort M — risk med
  Why: the ideas so far deny re-reads of unchanged files only. A changed file still costs the full file again after every own or external edit. Assumption: a PreToolUse deny reason can carry a bounded hunk.
  Done when: after a one-line change, re-Reading the file is denied with just that hunk (≤2 KB). After a compaction or clear the full Read is allowed again.

- **Add stateless `fm ci` that runs the mechanical pre-audit and gates on any PR diff** — FEATURE — value 3 — effort M — risk low
  Why: the pre-audit (weakened tests, dangling names, missing companion edits), the CI-command map and `fm pr` exist only inside sessions. Assumption: they can run from a diff and the repo alone, without the state dir.
  Done when: `fm ci --base main` on a fixture branch that weakens a test exits nonzero and names the finding, from a clean checkout with no `~/.claude/foreman`.

- **Add `fm splice FILE:SYMBOL` to replace a whole function or class by name** — PERFORMANCE — value 3 — effort M — risk med
  Why: Edit needs the old text quoted, which costs output tokens on every large change. `ast` and the symbol index already exist, and `fm refactor` covers only renames, moves and signature changes. Assumption: the guard's scope and active-task checks can be applied to this Bash command.
  Done when: splicing a 60-line function takes one call with no old text, runs a syntax check, and refuses an out-of-scope path or a missing task.

- **Scaffold a new test from the nearest sibling test** — FEATURE — value 3 — effort M — risk low
  Why: the pack has "lint against sibling conventions" and test↔source links, but nothing that generates the boilerplate. Claude currently writes imports, fixtures and naming from scratch and can drift from them. Assumption: the sibling is found via the test↔source map.
  Done when: `fm scaffold test PATH:SYMBOL` writes a skeleton that reuses the sibling's imports, fixtures and naming, is collected by the runner, and fails until the assertions are filled in.

I considered per-function return-value invariants and stage-based thinking-effort routing. Both overlap the existing runtime-trace-diff and per-tier model routing ideas, so I left them out.

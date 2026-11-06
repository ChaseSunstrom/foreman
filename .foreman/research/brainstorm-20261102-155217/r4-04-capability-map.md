# Brainstorm — lens: capability map

- **Run tasks from `fm:` comments in source** — FEATURE — value 3 — effort M — risk med — category: intake
  Why: assumption: Aider's watch-files mode lets a user drop `# fm: make this async` in an editor and have it picked up. The pack shows many intake routes (mail, Matrix, voice, TODO harvest) but none that starts from a comment the user typed in their editor.
  Done when: a file containing `// fm: <ask>` makes `fm next` list a task quoting the ask and its file:line, and removing the comment closes the task as withdrawn.

- **Pin legacy behaviour with characterization tests before editing** — FEATURE — value 4 — effort M — risk low — category: proof
  Why: assumption: the pack has differential-run proofs for "no behaviour change" and mutation scoring, but nothing that creates a safety net for untested code before the first edit. Legacy-code workflows (Feathers-style golden master) do this first.
  Done when: for a task touching a function with no covering test, `fm task start` writes a golden-output test, and the test passes before the edit and is named in the receipt.

- **Write tests for surviving mutants** — FEATURE — value 4 — effort M — risk low — category: proof
  Why: the pack has "Score proofs by mutation" and "Validate with mutation testing", which find weak proofs but do not repair them. Closing the loop is the missing half, as in Stryker plus an LLM test writer.
  Done when: given a seeded surviving mutant, a lane adds a test that kills it and re-running the mutation pass shows it dead.

- **Attach a debugger-evidence lane (DAP)** — FEATURE — value 3 — effort L — risk med — category: debugging
  Why: assumption: the pack has hypothesis ledgers, `rr` traces and LSP (T-0788, deferred), but no way for an agent to set a breakpoint and record real runtime values as evidence. Cursor and Cline-class tools lack this too, so it would be ahead of them.
  Done when: for a failing test in a fixture repo, `fm debug` stops at a named line and writes the variable values to the task's evidence file.

- **Detect stuck loops from tool-call n-grams** — FIX — value 4 — effort S — risk low — category: reliability
  Why: assumption: models repeat the same failing command or edit. The pack has "refuse a retry that repeats a failed approach" at the plan level and a stall stop by dollars, but no cheap live detector in the hook stream.
  Done when: a replayed transcript where the same command fails 4 times in a row makes the hook print a nudge naming the repeated command, with zero model calls.

- **Check `.env.example`, config reads and docs for drift** — FEATURE — value 3 — effort S — risk low — category: proof
  Why: the pack has "docs against code" token checks and the ban on secrets in goal files, but no check that the env vars and config keys the code reads match the example file and the docs.
  Done when: adding `os.environ["NEW_VAR"]` to a fixture project makes `fm check` report it missing from `.env.example` and the README.

- **Janitor lane worktrees, branches and stashes** — CLEAN — value 3 — effort S — risk low — category: hygiene
  Why: Foreman runs many lanes, merges in scratch worktrees and spikes in parallel, and the pack shows no owner for the leftovers. It has "protect goal state from git clean" but no reaper for orphaned lane directories and merged branches.
  Done when: `fm tidy --git` lists orphan worktrees, merged `fm/*` branches and stale stashes with the command to remove each, and removes nothing without the flag.

- **Learn a repo's change-completeness conventions** — FEATURE — value 3 — effort M — risk med — category: conventions
  Why: assumption: the pack has co-change hints and review-comment lessons. Mining the last 30 merged commits for "every behaviour change also touches CHANGELOG, docs or a snapshot" and checking the diff against that is a separate capability, like Danger.js rules learned rather than written.
  Done when: on a fixture repo whose history always updates `CHANGELOG.md` with `src/`, a diff touching only `src/` is flagged at finish with the history that justifies it.

- **Lint the user project's UI strings for terminology and tone** — FEATURE — value 2 — effort M — risk low — category: quality
  Why: the pack has a glossary lint for Foreman's own vocabulary and i18n rows for goals. Nothing applies a term list to the user's product strings (button labels, error messages) and flags inconsistencies such as "sign in" vs "log in".
  Done when: a fixture app using both "sign in" and "log in" gets one finding listing each occurrence.

- **Stand up a local offline forge for review** — FEATURE — value 3 — effort L — risk med — category: collaboration
  Why: assumption: the pack has PR bots, forge-side enforcement and Git-native team mode, all needing a hosted forge. A local bare remote plus a small review page would give review, comments and merge-with-proof to users with no GitHub.
  Done when: `fm forge serve` hosts a bare remote and a review page, and a lane's branch can be reviewed and merged with its receipt shown.

- **Wild: Render an architecture diagram diff on every finish card** — FEATURE — value 3 — effort M — risk low — category: delight
  Why: wild. The pack has blast-radius maps and layering checks as text. A module-dependency graph, before and after, with new edges drawn in colour gives a reviewer the shape of a change in one glance.
  Done when: finish on a fixture task that adds an import writes an SVG with the new edge highlighted and the receipt links it.

- **Wild: Map bus factor and queue the docs tasks** — FEATURE — value 2 — effort S — risk low — category: initiative
  Why: wild. Files touched by a single author or by an agent only, mined from git history, are knowledge-loss risks. `fm find` is the free first pass, and this adds one more finder that files "document X" tasks.
  Done when: on a repo with a file edited by one author across 20 commits, `fm find --bus` lists it with a ready-to-file task.

- **Wild: Offer a pair-programming handback with "I'll watch"** — FEATURE — value 3 — effort M — risk med — category: interaction
  Why: wild. When the user edits mid-task, the pack only detects it and says the hand wins. A mode where the user types `fm pair`, edits freely, then `fm resume` makes Foreman read the diff of the user's edits, state its understanding, and continue the plan.
  Done when: after hand edits during `fm pair`, `fm resume` prints a summary of the user's diff and the updated plan row before any further edit.

- **Wild: Run the user's project under network and clock chaos during a proof** — FEATURE — value 3 — effort M — risk med — category: proof
  Why: wild. The pack has chaos shots for screens and time-travel flows with an injected clock. A proof kind that runs the project's own tests under added latency, dropped connections and a skewed clock would catch the retry and timeout bugs normal proofs miss.
  Done when: a fixture service with a missing timeout passes `fm prove` normally and fails under `fm prove --chaos net`, with the failing step named.

- **Extend `fm doctor` with a toolchain-manager check (mise, asdf, nvm, pyenv)** — FEATURE — value 2 — effort S — risk low — category: environment
  Why: assumption: proofs fail confusingly when the shell uses a different tool version than the repo pins (`.tool-versions`, `.nvmrc`). The pack covers bootstrap and a prover lockfile but not pins declared by the user's version manager.
  Done when: in a fixture repo whose `.nvmrc` disagrees with the active node, `fm doctor` prints one row naming both versions and the command to align them.

Next question: Which of these capabilities would the user reach for in their first week, and would the user's own shell history, editor setup and installed tools show it before we build anything?
Next question: Which of the best-in-class tools the user already runs (pre-commit, Renovate, mise, act) could Foreman delegate to instead of rebuilding, and does the pack record which are installed?

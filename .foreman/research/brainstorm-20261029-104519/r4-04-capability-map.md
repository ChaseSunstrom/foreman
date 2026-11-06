# Brainstorm — lens: capability map

- **Gate on diff coverage** — FEATURE — value 4 — effort M — risk low — category: verification
  Why: assumption: gates prove a named test fails without the change, but nothing shows that the changed lines were executed by any test. Test selection from coverage is already listed; a gate on coverage of the diff is not.
  Done when: closing a task whose added lines no test executes is refused, with the uncovered `file:line` ranges named. A task whose lines are all covered closes.

- **Pre-list the files a task will need from co-change history** — FEATURE — value 4 — effort M — risk low — category: prediction
  Why: recent asks were fixes for docs-impact and scope blockers that appeared only at close ("rules/foreman.md → plugin/rules/foreman.md"). The history of which files change together (a new command → README, CHANGELOG, MASTER, completion) can predict them at task start.
  Done when: `fm task start` on a task that adds a command lists the co-changing files from the last N closes. Closing without touching or waiving them is flagged at start, not at close.

- **Shard a codemod across files with `fm sweep`** — FEATURE — value 4 — effort L — risk med — category: refactor
  Why: assumption: Sourcegraph Batch Changes, Codemod and OpenRewrite do one transformation across many files. Foreman has "sweep for sibling gaps" (finding them) but nothing that applies one proven change as N sharded tasks.
  Done when: `fm sweep "<transform>" <glob>` creates one task per shard, each with its own proof, and a failing shard blocks only itself.

- **Route models by step** — PERFORMANCE — value 4 — effort M — risk med — category: cost
  Why: Aider's architect/editor split is the proven pattern: a strong model plans and a cheap one applies edits. Foreman has per-kind ceremony profiles deferred (T-1266) and a usage-runway concern, but no per-step model choice.
  Done when: a config maps plan, edit, review and chore steps to models. A duel run shows the same pass count at lower cost on at least one task kind.

- **Gate on project performance budgets** — FEATURE — value 3 — effort M — risk low — category: verification
  Why: Foreman tracks its own hook latency (`bench_hooks.py`), but the projects it works on have no baseline-and-budget gate. A PERFORMANCE task like T-1994 is proven only by anecdote.
  Done when: a PERFORMANCE task records a before and after benchmark, and closing is refused if after is not better than before by the task's stated margin.

- **Narrate the diff in reading order** — FEATURE — value 3 — effort M — risk low — category: review
  Why: the user ships many one-line-ask tasks and "ranks closed tasks by review need" is listed. Reordering hunks into a story (test, then fix, then docs) with one sentence each is not.
  Done when: `fm task review Tn` prints hunks grouped as intent, test, change and docs. Every hunk in the diff appears exactly once.

- **Split a task's diff into atomic commits** — FEATURE — value 3 — effort M — risk med — category: git
  Why: recent commits bundle sub-tasks ("T-2001: T-1998, T-1999, T-2000"), so a bisect lands on a bundle. Assumption: a revert of one sub-task is currently manual.
  Done when: shipping a multi-subtask task yields one commit per subtask, each of which passes its own proof. `git revert` of one leaves the others green.

- **Auto-author a skill from a repeated procedure** — FEATURE — value 3 — effort M — risk med — category: learning
  Why: there are 1248 skill files, and hiding unused ones is already listed. The reverse direction, noticing the same multi-step procedure three times in transcripts and drafting a `SKILL.md`, is not.
  Done when: after three similar procedures, `fm skill propose` outputs a draft that passes the cc-skill-descriptions card. Nothing is installed without approval.

- **Detect hook conflicts with other plugins** — FIX — value 3 — effort S — risk low — category: compatibility
  Why: Foreman installs guard, ambient and done-gate hooks plus a UI mod. Hooks from other plugins can deny, rewrite or double-fire the same events. `fm doctor` is not shown checking for this.
  Done when: `fm doctor` lists every other plugin's hook on the same events and flags an overlapping matcher. A fixture with a conflicting hook produces the warning.

- **Add a hotfix mode with a ceremony-debt ledger** — FEATURE — value 3 — effort M — risk med — category: workflow
  Why: assumption: sometimes the user wants a prod fix now, and Foreman's full ceremony slows it. Skipping it silently erodes the guarantees, so the skipped steps need recording and repaying.
  Done when: `fm hotfix` skips named gates. It records a debt task for each skipped gate, and `fm status` shows the debt until each is paid.

- **Wild: ask the repo questions with citations that are checked** — FEATURE — value 4 — effort M — risk low — category: understanding
  Why: wild. Cody and Cursor answer codebase questions, but their citations are unchecked. Foreman's theme is proof, so each cited `file:line` should be verified against the text before the answer is shown.
  Done when: `fm ask-repo "<q>"` returns an answer whose every citation resolves to real text. Any citation that does not is dropped or flagged.

- **Wild: record a manual session and turn it into a DONE-WHEN** — FEATURE — value 4 — effort M — risk med — category: capture
  Why: wild. The user writes precise DONE-WHEN lines by hand every time (visible in every recent ask). `fm record` could watch them reproduce a bug once in a shell and emit the repro command plus a failing-test stub.
  Done when: `fm record` captures a shell session and writes a DONE-WHEN command that exits non-zero on the buggy build and zero on the fixed one.

- **Wild: review other people's PRs with Foreman's proof rules** — FEATURE — value 3 — effort L — risk med — category: CI
  Why: wild. This extends beyond "re-run recorded proofs in CI". A GitHub Action could read a PR's claims, check that each named test fails without the change, and comment pass or fail.
  Done when: opening a PR on a fixture repo triggers the action. It comments one verdict per claim, and a PR with a test that passes without the change is marked unproven.

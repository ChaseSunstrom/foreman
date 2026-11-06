# Brainstorm — lens: capability map

- **Open a pull request for each closed task, with the proof in the body** — FEATURE — value 5 — effort M — risk med — category: code review
  Why: Closed tasks already carry commands and exit codes, but nothing sends that proof to review. Assumption: the user reviews changes through GitHub PRs.
  Done when: `fm task close --pr` opens a draft PR (tested against a stubbed `gh`) whose body lists each proof command and its exit code.

- **Import a GitHub issue as a task whose first step is a failing test** — FEATURE — value 4 — effort M — risk low — category: intake
  Why: The open work and user requests come from issues and asks, and the pack has a "prove it" rule that needs a red test first. Assumption: issues often include a repro.
  Done when: `fm task from-issue N` creates a task, and `fm task prove` shows the first step failing before any fix is applied.

- **Run the Foreman gate as a required GitHub check** — FEATURE — value 4 — effort M — risk low — category: CI
  Why: `fm check` and the e2e roundtrip are the project's gates, but they only run locally. Assumption: the repo runs GitHub Actions, as the README badge shows.
  Done when: a generated workflow fails a PR whose seeded change turns `fm check` red, and passes on the clean branch.

- **Answer review comments as tasks** — FEATURE — value 4 — effort M — risk med — category: code review
  Why: Reviewers' comments currently go back to the chat by hand. Assumption: comments map to file and line.
  Done when: a comment on a line creates a task scoped to that file, and its close updates the thread with the commit that resolved it.

- **Redact secrets from journals and receipts before they are written** — SECURITY — value 4 — effort S — risk low — category: privacy
  Why: Journals and receipts store commands and tool output, which can contain tokens. Assumption: some output includes credentials.
  Done when: a seeded fake API key printed by a command is absent from the journal, the receipt and the events file.

- **Set a performance budget on named hot paths, not just hooks** — PERFORMANCE — value 4 — effort M — risk low — category: benchmarks
  Why: The hook bench is noisy (p95 over budget on a loaded machine, under budget on a quiet one). Assumption: other paths like `fm status` and the TUI draw also matter.
  Done when: a seeded 2x slowdown of a registered path fails the check, while ordinary noise under the confidence band passes.

- **Run one queue across several repos** — FEATURE — value 4 — effort L — risk med — category: multi-repo
  Why: The gate lock and leases are already per project, and the user runs several projects. Assumption: work spans repos in some cases.
  Done when: one queue file holds tasks from two repos, each runs in its own worktree, and `fm status` lists both.

- **Give each lane its own git worktree and remove it on close** — FEATURE — value 4 — effort M — risk med — category: isolation
  Why: Lanes that share a working tree make edit leases and gate runs collide. Assumption: git is available in every project.
  Done when: two lanes editing the same file never share a directory, and closing either one removes its worktree.

- **Fail the gate when a doc names a command or file that no longer exists** — FIX — value 3 — effort M — risk low — category: docs
  Why: Docs are listed as thin, and renamed commands leave stale references. Assumption: docs reference `fm` subcommands and repo paths.
  Done when: renaming a command mentioned in a README makes `fm check` fail, naming the file and line.

- **Send a finished change to its CODEOWNERS reviewer with the receipt** — FEATURE — value 3 — effort S — risk low — category: review routing
  Why: Ownership is known from the repo, and the receipt already holds the proof. Assumption: the repo has a CODEOWNERS file.
  Done when: a change that touches an owned path requests a review from the named owner in the PR created by the close step.

- **Export each run as OpenTelemetry spans to a local file** — FEATURE — value 3 — effort M — risk low — category: observability
  Why: Runs and gates have timings and outcomes, but they can only be read in Foreman's own views. Assumption: the user has or wants a trace viewer.
  Done when: `fm run` writes one span per task and gate with the task id and result to a local OTLP JSON file.

- **Run a dependency bump as its own lane, proven by the suite** — FEATURE — value 3 — effort M — risk med — category: maintenance
  Why: Routine upgrades are a common job that the gates already handle well. Assumption: the project has a lockfile and a test suite.
  Done when: a bump that breaks one seeded test closes as failed and leaves the lockfile unchanged.

- **Wild: scrub a run's file state step by step, like a time machine** — FEATURE — value 3 — effort L — risk med — category: replay
  Why: wild; the journal already orders each edit, so any step's file state can be rebuilt. Assumption: edits are journaled with before and after content.
  Done when: `fm replay <id> --step 4` restores the working files to step 4 in a copy directory, and the copy matches the journal's hash for that step.

- **Wild: a sticker book of closed tasks, earned per verified fix** — FEATURE — value 2 — effort S — risk low — category: delight
  Why: wild; closed tasks with passing proof are a natural collectible, and the zine and vase exports show the user likes small rewards.
  Done when: each closed task with a passing proof adds one sticker to a local page, and a task that closes without proof adds none.

- **Wild: a receipt bot that replies on the issue with the proof** — FEATURE — value 2 — effort M — risk med — category: outward-facing
  Why: wild; closing a task could post its receipt to the linked issue. Assumption: some issues are linked to tasks. This is outward-facing, so it needs explicit opt-in before any post.
  Done when: with the opt-in set, closing a task from an issue posts one comment with the receipt, and without it nothing is posted.

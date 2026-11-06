# Brainstorm — lens: capability map

- **Mutation-check the proof tests** — FEATURE — value 5 — effort M — risk low — category: verification
  Why: `fm task prove` shows a test fails without the change, but not that the test would catch a nearby wrong change. T-1996/T-2001 show CLI-test fixes landing with `-k` filters that matched nothing (`core_integrity` vs `CoreIntegrity`). Mutmut and Stryker are the reference tools here.
  Done when: `fm task prove --mutate` flips 3 operators in the changed lines, reruns the task's tests, and reports how many mutants survived. A fixture with a weak test reports at least one survivor.

- **Detect flaky tests and quarantine them** — FEATURE — value 4 — effort M — risk low — category: gates
  Why: assumption: with 385 test files and overlapping ambient/ship runs (T-1967, T-1984), flakes will look like task failures. Pytest-rerunfailures and Buildkite flaky analytics do this.
  Done when: a gate failure that passes on an automatic rerun is recorded as "flaky" in the ledger. `fm doctor` lists tests flaky 3 or more times.

- **Bisect a red gate to the task that broke it** — FEATURE — value 4 — effort M — risk low — category: recovery
  Why: the history is many small per-task commits (T-1998, T-2000, T-2001), which suits `git bisect run` well. Assumption: nothing automates this today.
  Done when: `fm bisect <gate>` names the first bad commit and its task id. A seeded regression across 10 commits is found in at most 4 gate runs.

- **Checkpoint and undo per task** — FEATURE — value 4 — effort M — risk med — category: recovery
  Why: the user steers and drops work often, e.g. a scope-ownership fix that needed `_theirs` in several places. Cline and Cursor both offer checkpoint restore. Assumption: Foreman has no per-task rewind.
  Done when: `fm task undo T-n` restores the pre-task tree for that task's files only. Another task's dirty files are untouched, and the undo is itself logged.

- **Post a per-task cost and time ledger** — FEATURE — value 4 — effort S — risk low — category: observability
  Why: the open items cover budgets and "close-out legibility" (T-0795) and the duel on cost (T-1231), but the pack shows no per-task spend record. Aider and Claude Code `/cost` report spend per session.
  Done when: `fm task finish` prints seconds, tokens and dollars. `fm stats` ranks the 5 priciest tasks of the week.

- **Generate a PR body from the task record** — FEATURE — value 3 — effort S — risk low — category: shipping
  Why: every task has DONE-WHEN, proof output and gate results, and `fm ship` exists. Danger and Copilot PR summaries are the reference. Assumption: ship does not write the body.
  Done when: `fm ship --pr` opens a draft PR whose body lists the DONE-WHEN, the proof command and its output, and the files touched.

- **Add policy-as-code for the guard hook** — FEATURE — value 4 — effort M — risk med — category: safety
  Why: the guard blocks commands you'd never want run, and injection defenses are deferred (T-0791). OPA and Claude Code permission rules show the model: a declarative, testable allow/deny file.
  Done when: `.foreman/guard.yml` rules are unit-testable via `fm guard test`. A rule table of 20 command cases passes, and a denied command names its rule.

- **Run a secrets and dependency scan as a gate** — SECURITY — value 3 — effort S — risk low — category: gates
  Why: assumption: no scanner appears among the gates (`fm doctor`, roundtrip, bench_hooks). Gitleaks and osv-scanner are drop-in tools.
  Done when: a diff that adds a fake API key fails `fm task done` with the file and line. A clean diff adds under 2s.

- **Compute test-impact selection from the dependency map** — PERFORMANCE — value 4 — effort M — risk med — category: speed
  Why: T-1994 and T-1996 were about running too many tests. `fm map` already holds a tests-to-src mapping, and Bazel and pytest-testmon pick tests by changed code.
  Done when: editing one lib file runs only the tests that map to it, plus an escape-hatch full run at ship. Selection beats the full module in time on a benchmark task without missing a seeded failure.

- **Rank the open queue by dependencies and value** — FEATURE — value 3 — effort M — risk low — category: planning
  Why: about 40 deferred or blocked items ("Later from T-0760"…) sit unordered. Linear and Jira show a blocker graph and critical path.
  Done when: `fm queue --next` returns one task with the reason (unblocks N others, S effort). Blocked items name their blocker.

- **Wild: Run an adversary agent against every closed task** — FEATURE — value 5 — effort L — risk med — category: agents — wild
  Why: assumption: closing relies on the author agent's own proof. A separate read-only agent tries for N minutes to find an input or edge case the DONE-WHEN missed. This extends the deferred `fm audit` (T-0034).
  Done when: a closed task with a seeded hole (an unhandled empty input) gets a filed counter-example task. A correct task gets "no finding" in under the budget.

- **Wild: Replay past failures as a regression eval suite** — FEATURE — value 5 — effort L — risk low — category: evals — wild
  Why: builds on T-0035 (eval capture) and the duel (T-1231). The user's steers and drops are labeled real failures: the `-k` mismatch, the overlapping suites, the dry-streak miscount.
  Done when: `fm eval replay` re-creates 5 historical failure scenarios and scores whether the current Foreman avoids each. The score is stored per release.

- **Wild: Send a phone notification and approve from there** — FEATURE — value 3 — effort M — risk med — category: surfaces — wild
  Why: the forever loop runs unattended, and the user asked it not to sit idle (T-0401). A blocked task could ping, with approve or deny and a one-line diff summary. Assumption: only the web UI and terminal exist today.
  Done when: a blocked-on-user event delivers a push with a diff summary and two buttons. Tapping one resumes or parks the task, and the choice is logged.

- **Wild: Dream mode for idle budget** — FEATURE — value 3 — effort L — risk low — category: loop — wild
  Why: the loop already has dry-round accounting and optional-work budgets. Spare budget could rehearse the code: mutate-test the weakest modules, probe `fm doctor` warnings, and write findings as captures only.
  Done when: with spare budget and an empty queue, a round produces at least one ranked capture with evidence and edits no tracked file.

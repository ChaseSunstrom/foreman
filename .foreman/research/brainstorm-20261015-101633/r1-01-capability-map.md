# Brainstorm — lens: capability map

- **Grade each task's evidence by strength** — FEATURE — value 5 — effort M — risk low — category: proof
  Why: `fm task prove` already records a red run, and `check` has a track record, but done is still pass/fail. The "held-rate" and "ungraded work" ideas need a per-task grade to count.
  Done when: `fm task show` prints a strength grade built from red-before, flake-free, diff coverage and mutation kill, and a task with a hollow check grades lower than one with a proven check.

- **Rerun red gates to catch flaky checks** — FEATURE — value 4 — effort S — risk low — category: reliability
  Why: assumption: a red gate on an unchanged tree is sometimes noise. Nothing in the pack separates flaky from really red, and it pollutes the check track record and prove.
  Done when: a failing gate reruns N times on the same tree hash, a mixed result is labelled `flaky` and excluded from the track record, and a test using a seeded flaky test shows it.

- **Require coverage on changed lines** — FEATURE — value 4 — effort M — risk med — category: gates
  Why: `fm check --affected` picks tests, but no step checks that the diff itself is exercised. The test map knows which tests link to which source files.
  Done when: closing a FEATURE or FIX with an untested changed hunk prints those `file:line` ranges, and a fixture task covering every hunk closes with no warning.

- **Mutation-probe the fix on a throwaway lane** — FEATURE — value 4 — effort M — risk med — category: proof
  Why: prove shows the test fails before the fix, but not that it fails when the fix is subtly wrong. Lanes are already throwaway worktrees.
  Done when: for a changed line, `fm task probe` applies N small mutations in a lane and reports how many the linked tests catch, with a surviving mutant shown as a diff.

- **Ratchet warnings against the start tree** — FEATURE — value 3 — effort S — risk low — category: gates
  Why: assumption: lint and type warnings are a common done-quality gap. `prove` already runs the start tree, so a baseline is cheap to take.
  Done when: close fails or warns if the lint/type count rose versus the start tree, and a task that fixes warnings lowers the baseline.

- **Bisect a regression from its red test** — FEATURE — value 4 — effort S — risk low — category: debugging
  Why: FIX tasks often name a regression, and the red test is a ready predicate. Lanes allow bisecting without touching the user's tree.
  Done when: `fm task bisect` runs `git bisect` in a lane with the task's red command and prints the first bad commit and its task id, and a seeded fixture repo finds the planted commit.

- **Turn production errors into FIX tasks** — FEATURE — value 4 — effort M — risk med — category: ingest
  Why: intake covers messages, issues and CI, but not a stack trace or error log. A stack trace maps to files through `fm map`.
  Done when: `fm capture --trace <file|->` creates a FIX with the top frames linked to files and a first-draft failing test, and a pasted fixture traceback yields that task.

- **Ingest PR review comments as steps** — FEATURE — value 4 — effort M — risk med — category: collaboration
  Why: the pack has "babysit PR until CI green" and issue sync, but nothing for a human reviewer's inline comments. Each should become a step closed with evidence or a stated reason.
  Done when: `fm pr comments <n>` creates one step per unresolved thread, and the close-out lists each thread with its commit or reply text.

- **Install a git hook so humans get the gates too** — FEATURE — value 3 — effort S — risk low — category: reach
  Why: Foreman only acts inside Claude sessions, so the user's own commits skip the guard and gates. Rivals win on visible artifacts, and a pre-push check is one.
  Done when: `fm hook git` installs a pre-push that runs `check --affected` and the guard's secret scan, `--remove` restores the prior hook, and a hand-made commit with a seeded red test is blocked.

- **Fan a repo-wide migration into verified shards** — FEATURE — value 4 — effort L — risk med — category: scale
  Why: lanes and `fm night` exist, but each task is one unit. Codemod-style work (rename an API across 200 files) needs sharded lanes with a checkpoint after each shard.
  Done when: `fm migrate` splits a pattern into shards by directory, runs each in its own lane with the repo gate, merges green shards and parks red ones, and an interrupted run resumes at the first unmerged shard.

- **Answer "why is this line here?" from the ledger** — FEATURE — value 3 — effort S — risk low — category: memory
  Why: assumption: the ledger holds the task, evidence and decisions behind each commit but is only searched by task id. Blame plus ledger gives the reason.
  Done when: `fm why src/x.py:42` prints the commit, its task, its request in the user's words and its evidence line, and says so plainly when no task exists.

- **Wild: Rerun closed tasks' evidence nightly against HEAD** — FEATURE — value 4 — effort M — risk low — category: durability
  Why: wild; "closed" is only true at close time. Verify commands are stored, and the pack proposes testing that they can still run but not that they still pass.
  Done when: a nightly job reruns each recent closed task's check on HEAD, and an intentionally broken old fix reopens that task with the first red line.

- **Wild: Turn a screenshot into a failing test** — FEATURE — value 3 — effort L — risk high — category: ingest
  Why: wild; users paste UI bug screenshots, and the pack already has web-UI smoke checks but no capture path from an image.
  Done when: `fm capture --image bug.png` produces a FIX whose brief quotes the visible text and a browser-driven check that fails on the unfixed seeded page.

- **Wild: Let one task span two repos with linked lanes** — FEATURE — value 3 — effort L — risk high — category: scale
  Why: wild; the pack's key is repo identity and lanes are per repo, so a change to a library and its consumer cannot close as one unit.
  Done when: a task can name a second repo, each side gets a lane with its own gate, and close is refused unless both are green and merged.

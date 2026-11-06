# Brainstorm — lens: user value

- **Cache gate results by tree hash** — PERFORMANCE — value 5 — effort M — risk med — category: speed
  Why: gates are 18.8 of 125 hours; one project's `cargo test` takes a median of 8 min and runs about once per task. Many reruns see an unchanged tree or only docs changed.
  Done when: running `fm check` twice on an identical tree hash returns the recorded result with a "cached" label in under 1 s, and any file change in the tree forces a rerun.

- **Run only the tests affected by the diff, full suite at queue end** — PERFORMANCE — value 5 — effort L — risk med — category: speed
  Why: an 8-minute suite per task dominates wall time. Assumption: the project can map changed files to test targets (cargo/pytest selection), with a fallback to the full suite.
  Done when: a one-file change runs a subset in at least 3x less time, and the queue close-out runs the full suite once and records it.

- **Pipeline the next task's planning while gates run** — PERFORMANCE — value 4 — effort M — risk med — category: speed
  Why: close-out is 42 hours and planning is the next biggest call count, yet both wait on each other serially. Assumption: the next task's plan is read-only and independent of the current task's files.
  Done when: in drive mode, a plan for the next ready task exists before the current task's gate finishes, and it is discarded if the files overlap.

- **Batch bookkeeping into one transactional `fm apply` call** — PERFORMANCE — value 4 — effort M — risk low — category: overhead
  Why: median 18 fm calls per task, and close-out is already one call. Planning, steps and evidence can take the same path.
  Done when: a median task makes 6 or fewer fm calls in a replay of the recorded sessions, and a failed batch leaves the record unchanged.

- **Add a "what I'd want" inbox mining pass** — FEATURE — value 4 — effort M — risk low — category: brainstorm
  Why: the user says brainstorming misses "things I want but don't know how to say". Their past requests, corrections and rejected plans are untapped signal. Assumption: the ledger keeps rejections and edits.
  Done when: `fm ideas --mine` returns at least 5 ideas, each citing the specific past user message or correction behind it.

- **Detect stale documentation at task close** — FEATURE — value 4 — effort M — risk low — category: freshness
  Why: the user asked for no context rot or outdated docs. Assumption: docs mention symbols and paths that the task's diff renamed or removed.
  Done when: closing a task that renames a function referenced in README or docs raises a named stale-reference finding with file and line, and a clean diff raises none.

- **Print a per-task usage receipt and weekly budget forecast** — FEATURE — value 4 — effort M — risk low — category: cost
  Why: the user is usage-sensitive and wants more subagents "without burning tokens". Assumption: usage data is available per task through the session API.
  Done when: each closed task records tokens by phase (plan, execute, audit), and `fm usage` shows a ranked list with a projected weekly total.

- **Run tiered audits that scale lens count with risk** — FEATURE — value 3 — effort S — risk low — category: cost
  Why: audits cost tokens on every task, small ones included. Assumption: the diff size and touched paths already produce a risk signal.
  Done when: a docs-only change runs 1 cheap lens, a protected-core change runs all lenses, and the choice is shown with its reason.

- **Let Foreman run overnight with a morning digest (wild)** — FEATURE — value 4 — effort L — risk high — category: autonomy
  Why: wild. The user wants full autonomy and hours-long tasks, so a budgeted unattended run could end with one readable summary of what shipped, what was blocked and what needs a yes.
  Done when: a run with a set time and token cap stops at the cap and writes a digest listing shipped, blocked and awaiting-approval items.

- **Replay old failures as regression tests for Foreman itself (wild)** — CLEAN — value 3 — effort M — risk low — category: reliability
  Why: wild. Real bugs such as the drive stopping on "Next: starting with T-0176" were found by the user. Turning each into a recorded-session test stops them returning.
  Done when: a fixture of that session transcript fails on the old drive logic and passes on the current one.

- **Hold a standing "challenge my request" Haiku pass (wild)** — FEATURE — value 3 — effort S — risk low — category: brainstorm
  Why: wild. A cheap pass can restate what the user probably meant behind a terse request, then offer one sharper variant in the capture, so vague asks like "make it smarter" turn into measurable tasks.
  Done when: a vague capture gains a proposed measurable criterion that the user can accept or ignore without an extra prompt.

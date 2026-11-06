# Brainstorm — lens: bold bets

- **Canary every new Claude Code release** — FEATURE — value 5 — effort M — risk low — category: reliability
  Why: Foreman patches and hooks into Claude Code internals (the foreman-ui mod, the pane background fight in T-1217, the stale install in T-0418, the demo pinned to 2.1.301), so an upstream update can break it silently. Assumption: new releases can be installed into a scratch dir.
  Done when: a nightly job installs the newest Claude Code in a sandbox, runs `roundtrip.py` and `bench_hooks.py`, and files a task naming the first broken hook or mod patch.

- **Isolate every task in its own worktree** — FEATURE — value 5 — effort L — risk med — category: architecture
  Why: recent fixes are one class of bug: the `_theirs` dirty-file gap in scope and sensitive-file checks, two suites at once, and ambient runs beside `fm ship`. Giving each task its own tree removes the class instead of patching instances.
  Done when: two tasks edit the same file at once and each task's `fm check` and close sees only its own diff, with no `_theirs` filtering involved.

- **Fuzz the guard hook against a real sandbox** — SECURITY — value 4 — effort M — risk med — category: guard
  Why: the guard's cwd tracking (`_DCWD`) and shell parsing already needed audits. Assumption: a no-network sandbox (bwrap or landlock) is available. Generate shell commands (nesting, `cd`, subshells, quoting, `eval`), predict the guard's verdict, then run them in the sandbox and compare what they actually touched.
  Done when: a fuzz run of 10k generated commands reports zero cases where the guard allows a command whose sandbox trace deleted or wrote outside the allowed paths.

- **Gate the docs by running them** — FEATURE — value 3 — effort S — risk low — category: docs
  Why: docs-impact only checks that doc paths exist (T-1995, T-1996). README and skill command blocks can still be wrong, and the project's bugs are mostly wrong-message and wrong-name bugs.
  Done when: `fm check` runs each tagged command block in the README and rules docs against a fixture project, and a doc example with a wrong flag fails the gate.

- **Schedule gates by catch rate per second** — PERFORMANCE — value 4 — effort M — risk med — category: gates
  Why: `fm gates` already names why-not-caught, and the commit log shows constant work to avoid duplicate suites and keep per-step checks fast. Rank gates by historical catches divided by seconds, run the best first, and stop early on red.
  Done when: on recorded history, the learned order reaches the first red result at least 30% sooner than the fixed order, with no catch lost.

- **Draft a full task from a pasted observation** — FEATURE — value 4 — effort M — risk low — category: intake
  Why: the user's requests are long, spec-shaped items ("FIX: … @path> DONE-WHEN: …"), usually after seeing a message misbehave. Paste a terminal excerpt and Foreman proposes the title, `@paths` and DONE-WHEN, with the failing command and output already attached.
  Done when: pasting the `no test matches test_doctor with -k core_integrity` output yields a draft with the right path to `run.py` and a runnable DONE-WHEN, accepted unedited in a test.

- **Quote a queue before running it** — FEATURE — value 4 — effort M — risk low — category: planning
  Why: the loop has risk and usage budgets that stop it mid-round, which is why the "dry round" miscount (T-1992) existed. Estimate time and cost per open task from similar closed tasks, then say what fits before the loop starts.
  Done when: `fm quote` lists the open tasks with a range and a stop point, and its estimates fall within 2× of actuals on the last 50 closed tasks.

- **Model-check the task lifecycle** — CLEAN — value 3 — effort M — risk low — category: correctness
  Why: bugs cluster at state transitions (close while another task is dirty, an edit during a gate run, a budget-limited round counted as dry). Write the states (open, focused, gating, shipping, closed) and their locks as a small explicit model, and enumerate all interleavings in a test.
  Done when: the model test explores every transition pair and fails on a deliberately reintroduced overlap bug.

- **Split the biggest modules by co-change** — CLEAN — value 3 — effort M — risk med — category: maintainability
  Why: T-0166 (`register.tsx`) is deferred and `fmmcp.py` and `fmcore.py` are very large. Mine git history for symbol groups that always change together, and propose cut lines.
  Done when: `fm map --split fmmcp.py` prints candidate modules with the co-change evidence, and one is extracted with the suite green.

- **Wild: Set an away envelope** — FEATURE — value 5 — effort L — risk high — category: autonomy
  Why: the user wants the loop to keep going and never sit idle, but unattended work needs authorization. The user says "away until 18:00, $5, these paths, no pushes", and Foreman tightens the guard to exactly that envelope, runs the queue, and leaves a digest. Wild.
  Done when: a run with an envelope refuses an out-of-envelope edit, a push and an overspend, and writes a digest of what shipped.

- **Wild: Narrate the day as a short local audio standup** — FEATURE — value 2 — effort M — risk low — category: delight
  Why: assumption: a local TTS engine is present. Commits and tasks are already rich text ("T-2001: T-1998, T-1999…"), and a 60-second spoken recap suits walking away from the desk. Wild.
  Done when: `fm standup --speak` produces an audio file under 90 seconds from the day's closed tasks, with no network call.

- **Wild: Grow a bug garden** — FEATURE — value 2 — effort M — risk low — category: web UI
  Why: fix clusters on one module are invisible in a task list. A web UI view draws each bug class as a plant that grows with every sibling fix and wilts when a guard test is added. Wild.
  Done when: the web UI renders one plant per cluster from task history, and clicking one lists its tasks.

- **Wild: Host a live public sandbox on the site** — FEATURE — value 3 — effort L — risk high — category: demo
  Why: the hero is a recorded SVG (`demo/live.svg`) of one session. Let a visitor type a request and watch the real loop fix a toy repo in a disposable container, with strict budget and no secrets. Assumption: budget and abuse controls can be built. Wild.
  Done when: a visitor's request on `site/index.html` streams a real session and fix, and the container is destroyed within 10 minutes.

# Brainstorm — lens: user value

- **Answer "is Foreman worth its weight?" in one command** — FEATURE — value 5 — effort M — risk low — category: lean value
  Why: Measured now: context averages 387k per reply, SessionStart note ~2k chars ×89, hook p95 278 ms, yet nothing tells the user what Foreman costs against what it saved. Many ideas above count weight; none gives the user the bottom line.
  Done when: `fm weigh` prints, for the last 7 days, bytes and ms Foreman added, guard blocks and reopens avoided, as one verdict line, and a test fixture with known inputs yields the exact line.

- **Fill the 61 empty cells from probes the user can re-run** — FEATURE — value 5 — effort L — risk med — category: coverage
  Why: The mission request itself; steer says a cell counts only if it names a concrete file or real gap and no phrasing is reused. User value: a grid they can trust, each cell with a rerunnable command.
  Done when: `fm genesis sweep` reports 0 empty, 0 templated, 0 duplicated cells for #12, and each cell lists a command that exits 0 or a recorded n/a with reason.

- **Fix the two brief-guard false positives and pin them as a corpus** — FIX — value 4 — effort S — risk low — category: guard
  Why: Pack: 2 false positives read a dict key and a `.join(` call as written paths. Each false block costs the user a retry and erodes trust in the guard.
  Done when: Both inputs pass the brief guard in a red-first test, and a corpus file of real blocked/allowed briefs runs in `fm check`.

- **Make every guard block say the safe command to run instead** — FEATURE — value 4 — effort M — risk low — category: guard UX
  Why: `core:interpreter-code-driving-foreman` blocked 42× in 7 days; repeated blocks mean the message doesn't teach. assumption: block text currently lacks an alternative.
  Done when: Each deny rule has a non-empty `instead:` line; a test asserts it for every rule; repeat-block rate for that rule drops in the next weekly `fm friction`.

- **Inject the SessionStart note once, then deltas** — PERFORMANCE — value 4 — effort M — risk med — category: context
  Why: ~2k chars × 89 sessions ≈ 180k chars of mostly identical text.
  Done when: The second session on an unchanged repo injects ≤ 300 chars (hash plus delta); a test compares bytes and verifies the full note is still retrievable by `fm note`.

- **Attribute per-reply context to its source** — FEATURE — value 4 — effort M — risk low — category: context
  Why: 387k per reply is reported but not broken down, so the user can't tell if Foreman, MCP schemas or the transcript is the cause.
  Done when: `fm cost --by-source` splits a session's average reply into Foreman injections, tool schemas, transcript and files, summing to within 2% of the total.

- **Shelve unused stack cards to a cold index** — CLEAN — value 3 — effort S — risk low — category: dead weight
  Why: 5 of 1219 cards used; the dropped-task note says to wait for session evidence, so shelve rather than delete.
  Done when: Cards unused for 90 days move to a cold index, `fm lib show NAME` still finds them, and install size drops by a measured amount.

- **Show a weekly "what the guard stopped" note in plain words** — FEATURE — value 3 — effort S — risk low — category: trust
  Why: Guard blocks are invisible wins; 42 blocks in a week are never shown as value. assumption: the user wants to see them.
  Done when: `fm doctor --week` lists blocks by command class in one sentence each, from the real log, and a test checks the wording on a fixture log.

- **Add a deletion receipt to every task that adds a verb** — FEATURE — value 3 — effort M — risk med — category: subtraction
  Why: gen-0 §6 says each generation removes at least as much as it adds, and the lean row marks growth "pending", so the debt is never paid. Make the pairing per task.
  Done when: `fm task finish` on a task adding a verb refuses unless it names a removed or merged verb, or a recorded measured-exemption, with a test for each path.

- **Run `fm doctor` in a hostile headless box and report honestly** — FIX — value 3 — effort M — risk med — category: headless
  Why: Headless/server is one of the empty-cell surfaces; standing rule says Foreman works with no `claude` on PATH. assumption: no hostile-env test exists.
  Done when: A test runs `fm doctor` with read-only home, no TTY, no network and no claude, and it exits with named findings instead of a traceback.

- **Wild: Plant a harmless forbidden command weekly to prove the guard is alive** — FEATURE — value 4 — effort M — risk med — category: guard liveness
  Why: wild; a silent hook failure looks identical to a quiet week.
  Done when: A weekly canary is blocked and logged on each host, and a disabled hook turns `fm doctor` red within a day.

- **Wild: Lean twin: run a task with Foreman off and on, and show the difference** — FEATURE — value 4 — effort L — risk med — category: proof of value
  Why: wild; the user's own evidence for "does this earn its keep" beats any exam number.
  Done when: `fm twin TASK` runs both arms on a scratch copy and prints cost, time and pass state side by side, with the tree untouched afterwards.

- **Wild: A diet week that disables one optional hook per day** — FEATURE — value 3 — effort M — risk med — category: subtraction
  Why: wild; discovers which hooks nobody notices missing, using the user's own work.
  Done when: Day-by-day results land in a table naming each hook, its bytes saved and any reopen or friction increase, with the guard excluded by a test.

Next question: What does the user do in the first five minutes after a guard block, and is that path shorter than just bypassing it?
Next question: Which of Foreman's injected blocks has the user ever read or quoted back, as opposed to the model?

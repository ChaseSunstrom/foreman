# Brainstorm — lens: reliability

- **Make every cell fill resumable and idempotent** — FIX — value 4 — effort M — risk low — category: fill reliability
  Why: 58 cells filled by child lanes; a killed or rate-limited writer mid-batch leaves a half-written coverage.md (assumption: writes aren't atomic). The pack's own "Run the fill twice and diff" idea is unbuilt.
  Done when: killing the filler at every write boundary (test harness) then re-running yields a coverage.md byte-identical to an uninterrupted run, with no duplicated or lost cell.

- **Count a cell only after a recorded cold read** — FIX — value 4 — effort S — risk low — category: coverage integrity
  Why: Steer: "a cell counts only when it names a concrete capability grounded in a file"; Haiku-then-Sonnet cold read rule. A dead or silent cold-read child must not equal a pass.
  Done when: a cell whose reader child timed out, crashed, or returned empty shows as "unread" and is excluded from the filled count; test with a stubbed dying child.

- **Verify each cell's citation still resolves at sweep time** — FIX — value 4 — effort S — risk low — category: rot detection
  Why: Cells cite files/symbols; refactors (e.g. T-0166 register.tsx move) silently break them. "Cells rot" is a known failure class here.
  Done when: renaming a cited function in a scratch copy turns exactly that cell red in `fm genesis sweep`, naming the missing symbol.

- **Table every deliberation component's failure mode, tested by crashing it** — FEATURE — value 4 — effort M — risk med — category: fail-safe
  Why: Gen-2 plan gate, race, blast-radius, readings all run via hooks/children; T-2532 showed a non-tool hook silently switching off. Assumption: not every deliberation stage has a crash test.
  Done when: for each stage (readings, options, blast, race, plan lint) a test injects an exception/timeout and asserts fail-closed or a logged named degradation, never silent pass.

- **Log every silent fallback in one degradation ledger** — FEATURE — value 4 — effort M — risk low — category: observability
  Why: T-2532 fix logged one fallback; earlier "Ideas" list the pattern but no ledger exists in the pack. Unattended lanes leave no trace when killed.
  Done when: `fm doctor` prints a count of named degradation events per component for the last 7 days, and a forced fallback in a test appears in it.

- **Fail visibly when a deliberation child answers with a different model than requested** — FIX — value 3 — effort S — risk low — category: model integrity
  Why: Cold-read and brainstorm children run on pinned tiers (Haiku first, Sonnet decides); a silent downgrade or auth-expired fallback would corrupt verdicts. Assumption: model identity isn't checked on return.
  Done when: a stub child reporting the wrong model ID makes the stage return "invalid" and the cell/read isn't counted.

- **Void a race whose verify command is flaky** — FIX — value 4 — effort M — risk low — category: race validity
  Why: Races "choose by evidence"; a flaky verify picks a winner by chance. Pack has T-2526 flaky-suite refusal but nothing for race verifies.
  Done when: the race runs the frozen verify twice on the baseline; disagreement yields "inconclusive" and no winner is recorded.

- **Run a nightly "tick can still run" self-test** — FEATURE — value 4 — effort S — risk low — category: unattended
  Why: Open question: which unattended failures leave no trace (logged-out session, expired auth, dead interpreter). `fm night` is the dispatcher but nothing proves it can spawn work.
  Done when: the tick writes a beat file with a self-test result; `fm doctor` and SessionStart WARN when the beat is older than 3 intervals or the self-test failed.

- **Cap an S task's deliberation by test** — PERFORMANCE — value 3 — effort S — risk low — category: cost bound
  Why: Capability #2 says "an S task doesn't pay an L task's cost"; no test pins it (assumption).
  Done when: a fixture S task completes the plan stage with under N child spawns and M seconds, asserted in the suite.

- **Sweep orphaned deliberation children and tmp dirs at session start** — FIX — value 3 — effort S — risk low — category: resource leak
  Why: Children run under /run/user/…/fm-children (tmpfs); killed lanes leave scratch that fills RAM-backed storage (assumption).
  Done when: planting a stale child dir older than TTL and starting a session removes it and logs one line.

- **Wild: Hold a silent-failure day** — FEATURE — value 3 — effort M — risk med — category: chaos drill
  Why: wild — kill one component per hour in a scratch copy (tick, cold-read child, hook import, ledger writer) and record which one the user-facing surfaces noticed within an hour.
  Done when: a report lists each killed component and time-to-notice; any "never noticed" row files a fix task.

- **Wild: Plant a canary plan with a known-wrong obvious answer** — FEATURE — value 3 — effort M — risk low — category: gate liveness
  Why: wild — a fixture task whose first-instinct approach fails; run weekly through the real plan gate and race to prove deliberation still beats the obvious.
  Done when: the canary's chosen approach is the non-obvious one in the weekly run; a regression turns `fm doctor` red.

- **Wild: Idempotent re-run proof for the whole fill** — TEST-style FEATURE — value 3 — effort M — risk low — category: determinism
  Why: wild — run the entire 58-cell fill twice on a frozen repo snapshot with a stub model and diff; any nondeterminism outside model text (ordering, ids, timestamps) is a bug.
  Done when: the two runs differ only in allow-listed fields.

Next question: Which of the 58 cells depend on a live session or a model call to stay true, and which can be proven by a zero-token probe the sweep re-runs?
Next question: When a cold-read child and the writer disagree repeatedly on the same cell, is that a reliability signal about the cell or about the reader?

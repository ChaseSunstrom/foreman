# Brainstorm — lens: reliability

- **Make cell fills atomic and resumable** — FIX — value 4 — effort M — risk low — category: genesis state
  Why: assumption: 58 cells filled by parallel S/M lanes with cold reads (steer: Haiku first, Sonnet decides) can be killed mid-batch (usage limit, OS kill). A half-written `coverage.md` or a filed-but-unread cell breaks "a cell counts only when read".
  Done when: killing the fill at each boundary (before write, after write, before cold read) leaves `coverage.md` valid, and rerunning resumes with no duplicate or lost cell, shown by a test.

- **Count a cell only after a cold read, else mark it "unread"** — FIX — value 4 — effort S — risk low — category: coverage integrity
  Why: assumption: when Haiku/Sonnet is unavailable (usage limit, auth expiry), a writer can still file cells. The steer says nothing is filed on a failed read, and silence must not count as a pass.
  Done when: with the reader stubbed to time out, the sweep reports N cells "unread", not filled, and the empty-cell count doesn't drop.

- **Run the fill twice and diff the cells** — FEATURE — value 3 — effort M — risk low — category: nondeterminism
  Why: assumption: tool-less children vary run to run. A cell that changes concept on a second authoring is probably templated or ungrounded, which the coverage rule forbids.
  Done when: `fm genesis check` flags a cell whose two independent fills name different files or capabilities, listing both.

- **Fail visibly when a deliberation child dies** — FIX — value 5 — effort M — risk med — category: gate failure modes
  Why: the idea list has rival planners, races and devil's advocates, but none says what the plan gate does when the child returns empty, truncated or times out. A silent pass defeats "choose by evidence".
  Done when: killing the rival child makes the plan gate record "unrivalled" on the plan and in `fm status`, never a plain pass, shown by a test per failure type.

- **Corrupt-output corpus for every deliberation parser** — FIX — value 4 — effort M — risk low — category: parser robustness
  Why: the idea, cold-read and race parsers read child text. T-0831 (salvaging partial results from capped children) is still deferred, which suggests truncated output is a real, known class.
  Done when: a fixture set (truncated, duplicated sections, injected "ignore the above", wrong format) goes through each parser. Each ends in a salvage or an explicit refusal, never a crash or a wrong accept.

- **Void a race whose verify is flaky** — FIX — value 4 — effort S — risk low — category: race validity
  Why: a race's winner is only as good as its verify command. A command that passes once and fails once picks winners by luck.
  Done when: the winner's and runner-up's verify run 3 times each, and any inconsistency marks the race "void: flaky verify" and falls back to the cheaper approach with that noted.

- **Count plan-gate bypasses by harness** — FEATURE — value 5 — effort M — risk low — category: harness parity
  Why: T-0335, T-0337 and T-0336 show Codex, Gemini and opencode lack some gates. The discipline-layer claim holds only if exhaustive thinking actually ran, so each session needs a counted "deliberation ran / skipped / unsupported".
  Done when: `fm doctor` prints per-harness deliberation-ran rates over the last 50 tasks, and an unsupported harness shows as such, not as green.

- **Add a plan-gate canary corpus to `fm doctor`** — FEATURE — value 4 — effort S — risk low — category: gate liveness
  Why: the guard has liveness ideas, but the plan gate doesn't. A refactor that quietly makes the gate accept paraphrased options would pass every unit test that feeds it good plans.
  Done when: 10 planted-bad plans (one idea in three costumes, no falsifier, a "none" blast radius) must all be refused. `fm doctor` goes red on any acceptance, at zero tokens.

- **Stale-plan check at merge, against the blast radius** — FIX — value 3 — effort M — risk med — category: concurrency
  Why: assumption: parallel builder lanes (the Mission 5-8 steer) can edit files a sibling's plan named as safe. Confidence decays in the existing ideas, but nothing re-checks the plan's blast radius at merge time.
  Done when: merging lane B after lane A touched B's neighbour files makes B's finish rerun `fm graph blast` and refuse on a new overlap, shown by a two-lane fixture.

- **Cap an S task's deliberation by test** — PERFORMANCE — value 3 — effort S — risk low — category: scaling
  Why: the capability text says an S task must not pay an L task's cost. Nothing in the pack measures it. "Alarm when deliberation outweighs the work" is idea-level only.
  Done when: a test runs S fixtures and asserts deliberation tokens/seconds stay under a stated cap, failing when a gate change raises it.

- **Wild: Chaos deliberation day** — FEATURE — value 3 — effort M — risk low — category: fault injection — wild
  Why: assumption: one scheduled run injects clock jumps, empty replies, auth expiry and a read-only state dir into a replayed task through the real plan gate and race path. It shows which failures leave no trace.
  Done when: the run emits a table of injected fault versus visible symptom, and any row reading "none" files a task.

- **Wild: Idempotent re-run proof for the whole fill** — FEATURE — value 3 — effort M — risk low — category: determinism — wild
  Why: assumption: the tower advances itself and may restart mid-generation. Running `fm genesis step` twice on the same state should be a no-op, and a restart should never change what was already filled.
  Done when: running the fill, then killing and re-running it, gives a byte-identical `coverage.md` and the same task ids.

- **Wild: A morning page for dead deliberation** — FEATURE — value 3 — effort M — risk low — category: observability — wild
  Why: the earlier questions ask how the user learns a trigger died and what no-session failures leave behind. That applies to unattended fills, races and cold reads that never ran.
  Done when: after a night with one killed child and one rate-limit pause, a single file lists both with cause and resume state, even with no session open.

Next question: Which standing steers have a check that only runs inside an interactive session, so an unattended fill never trips it?
Next question: When two parallel lanes write the same coverage row or decision record, which one wins, and where is that recorded?

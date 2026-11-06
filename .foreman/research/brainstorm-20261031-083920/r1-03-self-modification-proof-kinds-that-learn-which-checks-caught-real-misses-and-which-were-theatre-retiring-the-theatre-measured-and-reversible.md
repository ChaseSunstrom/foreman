# Brainstorm — lens: self-modification: proof kinds that learn which checks caught real misses and which were theatre, retiring the theatre, measured and reversible

- **Score every proof kind by catch rate against later reopens** — FEATURE — value 5 — effort M — risk low — category: proof ledger
  Why: Mission 7 has built several proof kinds (`--bench`, `--migration`, `fm shot`, `fm flow`, typed evidence, unproven rollup) with no record of which ones ever flagged a defect that a later FIX, revert or reopen confirmed. Assumption: close, reopen and revert events are in the ledger with task ids.
  Done when: `fm proof stats` prints, per proof kind, runs, fails, fails later confirmed by a reopen or FIX, and runs on tasks that were later reopened anyway (a miss), computed from fixture history with a known answer.

- **Mutation-test each proof kind with planted faults** — FEATURE — value 5 — effort L — risk med — category: proof validity
  Why: The standing rule says to use signals Foreman didn't author. A proof that passes on a planted regression is theatre by construction. Assumption: a seeded-fault harness for the instrument fixtures (`plugin/tests/fixtures/instruments/repo/app.py`) can be extended per kind.
  Done when: for each proof kind a fixture fault (slower bench, broken down-migration, shifted layout) makes the kind fail, and `fm proof stats` shows a "detects planted faults: N/M" column.

- **Retire a proof kind to advisory after N consecutive no-signal runs, reversibly** — FEATURE — value 4 — effort M — risk med — category: self-tuning
  Why: Lean ratchet exists for footprint but not for ceremony; the duel task (T-1231) and T-1266 profiles want less ceremony where it buys nothing. Assumption: demotion state lives in a small, user-readable file.
  Done when: a kind with 0 catches over N runs and 0 planted-fault detections is demoted to "advisory" and shown as such on the receipt; `fm proof restore KIND` reverts it in one command, and both actions are logged.

- **Never auto-retire without a user-owned tripwire** — SECURITY — value 4 — effort S — risk low — category: guard
  Why: Following the T-2252 pattern (`fm mandate set` is the user's), a model deciding its own checks are theatre is a writer-judge loop with no user check. Done when: retirement and restoration verbs are in USER_ONLY_FM, and an agent session invoking them is refused by the guard in a test.

- **Run shadow mode before retirement** — FEATURE — value 4 — effort M — risk low — category: measurement
  Why: A check that is skipped can never show it would have caught something. Assumption: running it silently costs little. Done when: a demoted kind still runs, its result is recorded but not enforced, and the first shadow fail on a task that later reopens raises a "retired too early" alert in `fm doctor`.

- **Report theatre cost in seconds and tokens** — PERFORMANCE — value 3 — effort S — risk low — category: observability
  Why: Hook p50 and footprint are tracked; proof runtime isn't tied to catch value. Done when: `fm proof stats` shows total wall time per kind and a time-per-catch figure, and a kind with zero catches ranks first for review.

- **Track which criteria were typed evidence and later wrong** — FIX — value 4 — effort M — risk low — category: unproven rollup
  Why: T-2273 counts typed or inconclusive evidence but nothing checks how often it was false. Done when: the unproven rollup shows a "typed evidence later contradicted" rate, and a test with a reopened typed-evidence task raises it.

- **Escalate a kind that is missing catches** — FEATURE — value 4 — effort M — risk med — category: self-tuning
  Why: The same data that retires theatre shows where tasks reopen after passing. Assumption: reopen reasons can be tagged with the proof they should have had. Done when: a reopen tagged "visual" on three tasks makes `fm task finish` require `fm shot` for that scope, with the rule stored and visible.

- **Version every proof-policy change in a diffable file** — CLEAN — value 3 — effort S — risk low — category: reversibility
  Why: "Measured and reversible" needs a history. Done when: each demotion, promotion or restore is a dated entry in one file, and `fm proof policy --at DATE` shows the policy then.

- **Wild: Hire a saboteur lane that breaks the code and sees which proofs notice** — FEATURE — value 4 — effort L — risk med — category: agents
  Why: wild; fuzzing the checkers with real diffs beats fixed fixtures. Done when: a nightly lane applies a model-written plausible bug to a throwaway worktree and records which proof kinds failed, with none caught listed as a gap.

- **Wild: Replay old closed tasks with the proof removed** — FEATURE — value 4 — effort L — risk med — category: counterfactual
  Why: wild; the repo history holds the answer to "would this check have mattered". Done when: for a sample of closed tasks, `fm proof replay` reruns each proof on the pre-fix tree and reports whether it would have failed.

- **Wild: Give each proof kind a visible "trust" badge on the receipt** — FEATURE — value 3 — effort S — risk low — category: delight
  Why: wild; the user sees "bench ✓ (caught 4 of 5 planted faults)" rather than a bare tick. Done when: the finish receipt prints each kind's detection rate beside its result.

- **Cold-read the policy file for metric-gaming** — SECURITY — value 3 — effort S — risk low — category: anti-gaming
  Why: The standing rule requires a cold Haiku read of every tower file; retiring checks is the easiest way to "improve" a pass rate. Done when: any policy change that raises the pass rate while lowering coverage is flagged by a cold read and blocked until the user accepts it.

Next question: Which proof kinds have never failed once across the ledger's history, and is that because they're sound or because nothing exercises them?
Next question: Who owns the reopen-cause labels that this learning depends on, and can an agent be wrong about them without anyone noticing?

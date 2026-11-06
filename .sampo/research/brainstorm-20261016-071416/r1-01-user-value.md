# Brainstorm — lens: user value

- **Auto-record reviewer findings from the review workflow** — FEATURE — value 5 — effort S — risk low — category: feedback loop
  Why: the pack says defect-class feed "starves unless someone remembers" `fm task finding`; every builder branch needed 2-6 fixes.
  Done when: a test runs the review workflow on a fixture diff with two reviewer findings and `fm lane brief` lists both defect classes without any manual `fm task finding` call.

- **Make bare `fm` inside a lane resolve to the lane's own copy** — FIX — value 5 — effort S — risk med — category: builder DX
  Why: builders can't run their own new flags; bare `fm` hits the main checkout, forcing `python3 plugin/bin/fm`.
  Done when: in a lane worktree, `fm <new-flag>` added on that branch runs and succeeds, and outside a lane the main copy is still used.

- **Show refusal commands in the friction digest** — FEATURE — value 4 — effort S — risk low — category: guard
  Why: the digest counts refusals but never the commands; a hand-written miner was needed twice and two premises were false only after mining.
  Done when: `fm friction` lists the top refused full commands with their verdict from `fm guard try`, and a test with three seeded refusals shows all three.

- **Alias the common guessed verbs** — FIX — value 4 — effort S — risk low — category: CLI forgiveness
  Why: weak agents guess `fm task list`; the nearest-name suggestion exists but the guess could just work.
  Done when: a test runs `fm task list` and gets the same output as the real verb, and the aliases come from mined unknown-command ledger entries.

- **Let the autonomous drive run review and ideas workflows** — FEATURE — value 5 — effort M — risk med — category: autonomy
  Why: /foreman:review and /foreman:ideas only run when the user types them, but the user is AFK and wants recursive self-improvement.
  Done when: a drive test with a fake clock invokes review after a lane merge without user input and records the result in the ledger.

- **Add `fm release` that does the eight-step ritual** — FEATURE — value 4 — effort M — risk med — category: release
  Why: the pack lists a manual 8-step release (3 version fields, heading, gates, release-check, temp worktree merge, push); T-1173 is open now.
  Done when: `fm release --dry-run` on a fixture prints and verifies every step, and the real run stops before push unless a push grant exists.

- **Measure the builder self-review and defect classes** — FEATURE — value 4 — effort M — risk low — category: measurement
  Why: "T-1147 and T-1164 are new and unmeasured"; assumption: review-round defect counts per branch are in the ledger.
  Done when: `fm lane stats` shows defects per branch before and after those features and a test seeds both periods.

- **Fix the guard's "it could be" path guess** — FIX — value 3 — effort S — risk low — category: guard
  Why: the guess shows glued paths like `/repo/cd/w.out`.
  Done when: a test with `cd w && cmd > w.out` yields a suggestion that is a real resolved path or none.

- **Park the 11 externally blocked briefs with a recheck trigger** — CLEAN — value 3 — effort S — risk low — category: backlog
  Why: 11 deferred briefs wait on Claude Code features or evidence; the mission pack still lists them.
  Done when: each has a named trigger (version, file, count) that `fm next` checks, and the pack excludes untriggered ones.

- **Wild: Premise-check sandwich — run a mined replay before any guard task is accepted** — FEATURE — value 4 — effort M — risk low — category: grounding
  Why: wild; two guard premises were false only after transcript mining (data-only writes, literal variables).
  Done when: capturing a guard task auto-attaches the replay count of matching refusals and a task with zero matches is flagged before queueing.

- **Wild: "Ask me nothing" ledger the user can audit on return** — FEATURE — value 4 — effort M — risk low — category: autonomy trust
  Why: wild; the user is AFK and forbids asking, so assumptions made in their place need one reviewable list with a one-keystroke reverse.
  Done when: `fm away` lists every parked assumption with an undo command, and undoing one reverts its effect in a test.

- **Wild: Self-diff the release against round 2 as a "what got better" page** — FEATURE — value 3 — effort M — risk low — category: proof of progress
  Why: wild; round 4 is "improve past everything shipped" but no artifact shows round-over-round change.
  Done when: a generated page shows per-round metrics (hook ms, friction count, held rate) with deltas, and a test builds it from two seeded ledgers.

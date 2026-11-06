# Brainstorm — lens: self-improvement and learning

- **Grow the bench harder when it saturates** — FEATURE — value 4 — effort M — risk low — category: bench
  Why: `fm bench` replays finished tasks and `fm evolve` promotes on bench wins, but a bench that Foreman passes 95% of the time can no longer tell a good instruction change from a bad one. Assumption: pass rates on replayed cases climb over time.
  Done when: a bench run whose pass rate exceeds a set threshold auto-generates harder variants of those cases (brief hints removed, distractor files added, vaguer wording), and a test shows the harder set scores lower on the same plugin version.

- **Embargo born-from lessons during replay** — FIX — value 4 — effort M — risk low — category: bench integrity
  Why: assumption: a replayed case can recall a lesson that was written because of that very case, so bench scores leak the answer. T-0217 and recall make this plausible.
  Done when: `fm bench` replay runs with a memory view that hides every lesson, decision and research note created at or after the case's task, and a test shows a case that scores green with the leak scores red without its own lesson.

- **Learn from every interrupt** — FEATURE — value 4 — effort M — risk med — category: taste learning
  Why: the user's steers ("cleanup never got done", "shouldn't block until 75%") are the strongest labels, and `fm taste` reads kept/dropped/steered but not the moment a user hit Esc or rejected a tool call. Assumption: transcripts record rejections and interrupts.
  Done when: a labelled corpus of (action, context, user reaction) is built from transcripts, and a pre-action check flags a proposed action whose nearest past neighbours were mostly interrupted. Replay on held-out sessions shows the flag fires on a stated minimum share of real interrupts.

- **Teach running sessions new lessons mid-flight** — FEATURE — value 3 — effort S — risk low — category: lessons
  Why: lessons and rules are injected at SessionStart, so a long session or a parallel lane never sees a lesson written an hour ago. Assumption: the UserPromptSubmit hook can inject deltas cheaply.
  Done when: after a lesson is saved in one session, a second already-running session shows it in its next prompt context exactly once, and a test confirms no repeat injection.

- **Tune Foreman's own dials as a bandit** — FEATURE — value 4 — effort L — risk med — category: meta-learning
  Why: review lens count, plan depth, oracle on/off and second-read frequency are fixed settings, while `fm evolve` only ablates instruction files. Assumption: finished tasks give a usable reward of first-pass, rework and cost.
  Done when: for one chosen dial, `fm` assigns values to live tasks within guardrails (never loosening safety gates), logs the arm and outcome, and `fm digest` shows a per-arm result with a confidence interval.

- **Track whether friction fixes stay fixed** — FEATURE — value 3 — effort S — risk low — category: self-improvement
  Why: `fm friction --every 3` ships fixes, but nothing checks that the friction signal it fixed stays gone (T-0424 refined one such signal).
  Done when: each friction-born task records its triggering signature, and a later run that re-matches it auto-reopens or links a task, shown by a test that replays a recurring signature.

- **Plan from solved look-alikes** — FEATURE — value 4 — effort M — risk low — category: planning
  Why: `fm recall` returns related past work, but plans are written from scratch. Assumption: first-time-pass tasks have plans worth reusing.
  Done when: planning a new task shows the nearest first-time-pass plan skeleton as a worked example with the differences from this brief called out, and `fm bench` shows no loss in pass rate and fewer plan edits.

- **Quiz each lesson with a cold agent** — FEATURE — value 3 — effort S — risk low — category: lessons
  Why: assumption: some lessons are too vague or too tied to their incident to change behaviour for someone who wasn't there.
  Done when: a new lesson is saved only if a tool-less child that sees just the lesson text answers an incident-derived question correctly, and an intentionally vague lesson fails the check in a test.

- **Mine the loser–winner delta of a race** — FEATURE — value 3 — effort M — risk low — category: cross-model learning
  Why: assumption: Foreman runs races or second reads across models (`fm second`, agents on codex/gemini), and the difference between the failing and passing attempt is currently discarded.
  Done when: when two attempts on one task end with different gate results, a candidate lesson is drafted from the first point where their plans diverged and queued for review, with the divergence step cited.

- **Wild: Practice on a new repo before touching it** — FEATURE — value 4 — effort L — risk med — category: onboarding
  Why: wild — `fm init` registers a project cold. Foreman could fix seeded bugs in a throwaway copy of the repo, harvesting which gates are slow or flaky, what's non-obvious and which edits break tests, so lessons exist before the first real task.
  Done when: running `fm init --practice` on a fixture repo produces at least N verified lessons and a gate-timing profile, and the user's working tree stays untouched.

- **Wild: Reverse-derive the brief from the diff** — FEATURE — value 3 — effort M — risk low — category: intent quality
  Why: wild — a tool-less child sees only a finished diff and writes the request that produced it. The gap between that and the actual brief measures how underspecified, drifted or over-delivered the task was, and feeds the user's request-style coaching.
  Done when: `fm` closes a task with a similarity score between the derived and real brief, and a seeded task with extra unrelated changes scores visibly lower.

- **Wild: Stage lessons in probation, then promote in sleep** — FEATURE — value 3 — effort M — risk low — category: memory
  Why: wild — new lessons enter as session-scoped and expire in a day. `fm night` consolidates the ones whose recall preceded clean passes into durable memory, as sleep does, instead of every lesson being permanent on arrival.
  Done when: a lesson unconfirmed after a set number of tasks disappears from recall, a confirmed one is promoted by `fm night`, and both transitions are visible in the ledger.

- **Wild: Hold a yearly "fresh model, old tasks" bake-off** — FEATURE — value 3 — effort M — risk low — category: model change
  Why: wild — when a new Claude model ID ships, Foreman replays a sample of the user's own past tasks with every lesson and rule switched off, then with them on. It reports which parts of itself the new model no longer needs, using the user's work rather than a generic benchmark.
  Done when: running the bake-off against two model IDs produces a table of rules by uplift per model, and rules with zero uplift get a removal task queued.

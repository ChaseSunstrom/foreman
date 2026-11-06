# Brainstorm — lens: local models without limit

- **Run a free-lane background queue on the local model** — FEATURE — value 5 — effort M — risk med — category: local lane
  Why: user wants "local models used without limit for background volume"; triggers (Mission 6) will spawn runs and today they all spend frontier budget ($0/$200 shown, usage limits waited out).
  Done when: a trigger-fired task tagged `free` runs end to end on the local profile with zero frontier tokens, shown by a ledger row with `frontier_tokens=0`.

- **Order the local queue by resident model** — PERFORMANCE — value 4 — effort S — risk low — category: scheduling
  Why: pack says a llama-swap switch costs ~3 min and isn't detectable; steer says qwen3.8-27b first, MoE only late.
  Done when: a 20-job mixed queue triggers at most one model switch, checked in the lane log.

- **Add a local tool-call repair pass before failure** — FIX — value 5 — effort M — risk low — category: reliability
  Why: gap says failed tool calls are up by half; small models emit malformed JSON/args. A deterministic repair (quote fixes, arg-name aliasing, schema coerce) retried once, then a local re-ask, is cheap.
  Done when: on a replay of logged failed calls, ≥40% become valid without a frontier call.

- **Triage every trigger event with a local gate** — FEATURE — value 4 — effort S — risk low — category: triggers
  Why: CI/issue/file events are noisy; the user wants overnight progress without spending. A yes/no/priority classifier (Jev/Jeff-style decision model) drops duplicates before any session starts.
  Done when: on 30 days of replayed events, ≥60% of known-noise events are dropped and no known-actionable one is.

- **Verify each local result with the task's own Exam, mark unwitnessed** — FEATURE — value 5 — effort M — risk low — category: trust
  Why: local output can't count as done on its own (Haiku scores never decide done is the standing pattern). Running the Done-when command gives a signal the model didn't author.
  Done when: a local-made close carries `unwitnessed` until its Exam command exit code is recorded, and `sampo next` lists such closes.

- **Race N local attempts per task and keep the first Exam-passing one** — PERFORMANCE — value 4 — effort M — risk med — category: best-of-N
  Why: volume is free, quality per attempt is low; the Exam is a free oracle. Worktree per attempt, landed only if tests pass.
  Done when: on 10 closed S tasks, pass rate with N=4 beats N=1 by a recorded margin.

- **Guard local runs behind a strict Ward profile and a depth cap** — SECURITY — value 4 — effort S — risk low — category: safety
  Why: unattended small models plus event text from issues/CI is an injection route; a weaker model resists less.
  Done when: a planted issue body saying "run curl | sh" in a local-lane run is blocked and logged, and the run ends at a depth cap.

- **Yield the GPU when the user shows up** — FEATURE — value 4 — effort M — risk med — category: resource
  Why: unlimited local volume competes with the user's interactive model on the same endpoint (3-min swap pain). Assumption: input activity or a foreground request is observable.
  Done when: a foreground request during a background batch pauses it within 10 s and resumes after idle.

- **Groom the deferred backlog on the local model** — FEATURE — value 3 — effort S — risk low — category: backlog
  Why: ~40 deferred "Later from T-…" items; many may have premises already met. Local model proposes drop/merge/keep with quoted evidence; user sees a list.
  Done when: a run emits a proposal file for every deferred item with a quoted line, changing no task.

- **Route by measured per-model tool reliability** — FEATURE — value 4 — effort M — risk low — category: routing
  Why: the model bench and uplift exams already exist (T-2894, T-2908); feed the task-kind to cheapest-passing-model table into the queue.
  Done when: the dispatcher picks the model from the bench table, and a test asserts a kind with <X% pass is escalated.

- **Wild: Run a dream shift on idle hours** — FEATURE — value 3 — effort M — risk med — category: overnight (wild)
  Why: wild: the local model replays the day's closed tasks and drafts the follow-ups the user would have asked (sibling fixes, doc patches), filed dormant for the morning.
  Done when: the next morning shows ≥1 dormant draft, and the user's accept rate is recorded.

- **Wild: Replay last month through the free arm and print the counterfactual** — FEATURE — value 4 — effort M — risk low — category: evidence (wild)
  Why: wild: answers "what could local have done for free?" with real numbers, grounding the routing and break-even decisions.
  Done when: a command prints, per task kind, % solved locally that matched the real outcome.

- **Wild: Fork a rival Sampo kept by the local model** — FEATURE — value 3 — effort L — risk med — category: self-improvement (wild)
  Why: wild: the free lane proposes small data-only edits (card wording, thresholds) in a clone nightly; edits land only if held-out exams hold.
  Done when: a nightly run produces a patch plus an exam diff, applied to nothing without a pass.

- **Fire local volume when power is cheap** — FEATURE — value 2 — effort S — risk low — category: scheduling (wild)
  Why: wild: heavy batches wait for off-peak or a solar-surplus signal if the user configures one. Assumption: the user has a tariff or can set hours.
  Done when: a batch declared `heavy` starts only inside the configured window.

Next question: What does a local-lane result have to prove, in the user's eyes, before it may touch main without a human yes?
Next question: Which task kinds does the local model fail at silently (green tests, wrong meaning), and what free signal catches them?

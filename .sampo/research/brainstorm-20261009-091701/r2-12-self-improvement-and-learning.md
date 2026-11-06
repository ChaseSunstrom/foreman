# Brainstorm — lens: self-improvement and learning

- **Hold out a secret bench set evolve never sees** — SECURITY — value 5 — effort M — risk low — category: self-eval
  Why: `fm evolve` and `fm friction` revise instructions against `fm bench`, so they can overfit to the cases they train on. The pack's list of ideas has no guard against this. Assumption: bench cases are currently one pool.
  Done when: `fm bench --holdout` scores a candidate on cases that `fm evolve` and `fm friction` can't read, and evolve refuses a candidate that wins on train cases but loses on holdout.

- **Track a release scorecard and make it evolve's objective** — FEATURE — value 5 — effort M — risk low — category: metrics
  Why: the pack has many measurements (digest, cost, grades, friction) but no single trend. Score each release on first-time-pass rate, user corrections per task, idle minutes, refusals per task and tokens per finished task. Assumption: these can be derived from the ledger and transcripts.
  Done when: `fm score` prints these five numbers per release with deltas, and evolve's accept rule reads them.

- **Examine Foreman on any repo's git history** — FEATURE — value 5 — effort L — risk med — category: benchmark
  Why: `fm bench` only replays Foreman's own finished tasks. For any commit that has a test change, check out the parent, give Foreman the commit message as the brief, and compare its result and tests with the real commit. Assumption: enough project commits have tests attached.
  Done when: `fm bench --history N` builds N cases from a project's past commits and reports pass rate against the real diff.

- **Profile where each task's time and tokens went** — FEATURE — value 4 — effort M — risk low — category: friction
  Why: `fm friction` digests events, but nothing attributes wall-clock and tokens to causes such as refusals, re-reads, retried gates, waiting and replanning. The JARVIS complaints (idle sessions, repeated refusals) were all found by hand.
  Done when: `fm friction --waste` ranks causes by minutes and tokens across the last N tasks, and the top cause becomes a brief in the next self-improvement pass.

- **Delete instruction crutches when a new model arrives** — FEATURE — value 4 — effort M — risk med — category: model-adaptation
  Why: many rules exist to compensate for past model weaknesses. A stronger model (the pack's environment lists the Claude 5 family) may not need them, and each one costs tokens. Assumption: rules can be ablated one at a time via bench.
  Done when: `fm evolve --model <id>` ablates each rule and proposes deleting those whose removal doesn't lower the bench score on that model.

- **Tune instructions per harness and model** — FEATURE — value 4 — effort L — risk med — category: multi-agent
  Why: Codex, Gemini CLI and opencode adapters exist (T-0335/6/7 are blocked, and Gemini's AfterAgent behaves differently). One shared wording is unlikely to be optimal for all of them. Assumption: bench can run on a non-Claude harness.
  Done when: `fm agents install codex` ships a variant selected by bench for that harness, and `fm bench --compare` shows it beating the shared wording.

- **Pin lessons to code and expire them when it changes** — FEATURE — value 4 — effort M — risk low — category: lessons
  Why: T-0217 scores lessons by outcome, but a lesson about `fmguard.py` goes stale when that function is rewritten. `fm why` already links lines to tasks, so lessons can carry file anchors.
  Done when: after a diff touches a lesson's anchored lines, `fm recall` marks the lesson "re-verify" and a lesson can't be injected until it is re-confirmed or retired.

- **Run candidate instructions in shadow on live tasks** — FEATURE — value 4 — effort M — risk low — category: online-eval
  Why: bench is offline, on past tasks. A headless plan-only session with the candidate instructions, run beside each real task's plan, gives live evidence at small cost. Assumption: plan-only runs are cheap and the budget broker allows them.
  Done when: `fm evolve --shadow` records candidate and live plans side by side for N tasks and reports where they disagree, with no repo writes.

- **Turn repeated procedures into generated project tools** — FEATURE — value 4 — effort L — risk med — category: automation
  Why: `fm repeats` only reports what a project repeats. Close the loop: write the script, add a test, register it as a project gate or verb, and prove by replay that it replaces the manual steps.
  Done when: `fm repeats --build 1` creates a script plus a passing test, and a replay of the old sequence calls the tool instead.

- **Interview the user weekly where the taste model is unsure** — FEATURE — value 3 — effort S — risk low — category: taste
  Why: `fm taste` learns from choices passively. Active learning would ask the 3 questions with the highest disagreement among predicted answers, which is cheaper than being wrong later. Assumption: the user will answer short questions.
  Done when: `fm taste --interview` asks at most 3 questions drawn from the highest-uncertainty predictions, and the answers are saved as vetoes or preferences.

- **Wild: Hold an adversarial curriculum between a teacher and Foreman** — FEATURE — value 4 — effort L — risk high — category: self-play
  Why: red-teaming the guard is listed, but nothing attacks planning, resume or verification discipline. A teacher agent writes tasks designed to make Foreman skip evidence, drift or claim done early, and the winning tasks become permanent bench cases. Wild.
  Done when: one overnight run adds at least one reproducible failing case outside the guard to the bench, with the failure shown.

- **Wild: Let Foreman write its own letter to next week's Foreman** — FEATURE — value 3 — effort S — risk low — category: memory
  Why: after each friction pass, Foreman writes a 10-line "what I wish I'd known" note, and the next pass is scored on whether it acted on the last note. This gives self-improvement a memory of its own failures. Wild.
  Done when: each pass opens with the previous note and closes with a per-line verdict (acted on, ignored, outdated).

- **Wild: Breed rival Foremen and let the user pick the survivor** — FEATURE — value 3 — effort L — risk high — category: evolution
  Why: `fm evolve` changes one instruction file at a time. Run two whole-config variants on alternate tasks for a week, then show the user a one-screen comparison of the scorecard, taste fit and cost. Wild.
  Done when: `fm evolve --duel` alternates variants A and B by task and ends with a report the user can accept to make one the default.

# Brainstorm — lens: capability map

- **Compile machine-readable specs into conformance checks** — FEATURE — value 4 — effort M — risk low — category: spec intake
  Why: assumption: the pack shows spec-kit/Kiro import and "compile acceptance criteria into red-first checks", but nothing that reads OpenAPI, GraphQL, protobuf or JSON Schema files. Those contain exact, checkable claims about a project.
  Done when: `fm spec check api/openapi.yaml` (stdlib parser, YAML subset) generates failing conformance checks for 3 seeded endpoint mismatches in a fixture repo, and they go green after the fix.

- **Manage the local model server's lifecycle** — FEATURE — value 4 — effort M — risk med — category: local models
  Why: the pack covers detecting runners, advising which model fits, probing context, and LAN discovery. It never covers starting a llama.cpp/ollama server when the queue needs it, freeing VRAM when a different runner needs the GPU, and stopping it when idle. Assumption: the user has one GPU shared with other work.
  Done when: with a fake server binary, queuing a local-runner task starts it, a second GPU-claiming task evicts it, and 5 idle minutes stops it, all logged in the run journal.

- **Score the test suite's real strength overnight** — FEATURE — value 4 — effort M — risk low — category: user value
  Why: the pack has per-diff mutation proof and coverage-on-changed-lines. It has no whole-project figure, so "the gates pass" can't be told apart from "the gates are weak". A night job sampling mutants per module gives a ranked weak-spot list that the queue can draw tasks from.
  Done when: `fm strength` on a fixture with one untested module ranks that module worst and files a queued brief to cover it.

- **Check design tokens against code** — FEATURE — value 3 — effort M — risk low — category: ui
  Why: assumption: the pack covers screenshot diffs, accessibility gates and "imitate a reference app", but not importing a token export (Figma/Tokens Studio JSON, CSS variables) as the source of truth. UI work then drifts from the design's colors and spacing with nothing flagging it.
  Done when: a fixture with a hard-coded `#3b82f6` that disagrees with the token file fails `fm check`, and the fix replaces it with the token reference.

- **Generate synthetic fixture data from schemas, never from production** — FEATURE — value 3 — effort M — risk low — category: privacy
  Why: the pack covers redaction and synthetic repo shapes, but not test data for the user's database. Agents tend to copy real rows into fixtures. A schema-driven generator, plus a guard that refuses to read a configured production DSN, removes that temptation.
  Done when: `fm fixtures gen schema.sql` produces seeded, reproducible rows that satisfy the schema's constraints, and a task that reads the configured prod DSN is refused with a pointer to the generator.

- **Answer read-only questions by runner quorum** — FEATURE — value 3 — effort S — risk low — category: agents
  Why: assumption: the pack has cross-examining a diff and a "second opinion" button, but questions about the code ("where is X handled?") run on one runner and are trusted. Asking two runners and showing only the disagreements, each with file:line citations, catches confident wrong answers cheaply.
  Done when: `fm code ask --quorum` on a seeded repo whose two runners (fakes) disagree prints both answers with citations and flags the disagreement. It prints one answer when they agree.

- **Explain which rules apply at a path** — FEATURE — value 3 — effort S — risk low — category: simplicity
  Why: the pack reads every harness's rule files and has `fm config explain`, but monorepos nest instruction files and policy layers. Nothing answers "what governs an edit to `services/api/x.py`?".
  Done when: `fm rules at PATH` lists each applicable rule or config source in precedence order, with its file and line, and a fixture with nested overrides shows the winning one.

- **Queue the decisions from a meeting transcript** — FEATURE — value 3 — effort M — risk med — category: intake
  Why: assumption: the pack has dictation, pasted chat-history mining and email capture, but not a recorded or transcribed meeting file as a source. Commitments made out loud ("we'll drop the v1 endpoint") are exactly what gets lost between a call and the queue.
  Done when: `fm capture --transcript call.txt` produces candidate briefs, each quoting the sentence it came from and each marked unconfirmed until the user accepts it.

- **Wild: Add hardware-in-the-loop evidence** — FEATURE — value 3 — effort L — risk med — category: evidence
  Why: wild; assumption: some users build firmware, Android/iOS apps or robots. The pack's "products that aren't web UIs" covers CLIs, not devices. An evidence adapter that runs a serial/adb/simulator script and records its output would let those projects get the same red-to-green proof.
  Done when: a fake serial device script (a recorded transcript) is accepted as a `device` evidence kind, and the criterion fails when the transcript contains the seeded fault line.

- **Wild: Bind physical controls to verbs** — FEATURE — value 2 — effort S — risk low — category: devices
  Why: wild; the pack has a single physical kill switch and approve button, but no general mapping. A small bindings file (MIDI, Stream Deck, gamepad or any command that emits a line) mapped to guarded verbs such as approve, pause or next gives hands-off control, and it reuses the typed exit codes.
  Done when: piping the line `btn3` into `fm bind listen` runs the bound `fm ask --yes` for the pending ask, and a binding to a human-only verb is refused.

- **Wild: Hold a bounty board for the guard's blind spots** — SECURITY — value 3 — effort M — risk low — category: security
  Why: wild; the pack has nightly adversary agents and fuzzers. This adds a persistent board where each confirmed bypass becomes a permanent, labelled regression row with the discovering runner credited, and the board reports which model families keep finding bypasses.
  Done when: a seeded bypass logged through `fm guard bounty add` appears in the guard corpus and fails the suite until the rule is fixed, and the board lists its finder.

- **Hold approvals to a time-of-day quiet window per device** — FEATURE — value 3 — effort S — risk low — category: devices
  Why: assumption: the pack has push-notification budgets, quiet hours and a watch glyph grammar, but not routing a pending ask to the device the user is actually near. One rule table (laptop awake, phone only, wait for morning) keyed on recent activity would fit that.
  Done when: with simulated laptop idle for 30 minutes, a pending ask is sent to the phone channel only, and `fm ask --default` applies the stored default after its deadline.

# Brainstorm — lens: understanding the user

- **Account for every clause of a multi-part message** — FEATURE — value 5 — effort M — risk low — category: intake
  Why: The user pastes long lists ("C022 … C101", "I like almost all of those, continue") and says cleanup requests "never got done". Nothing shows each clause landing somewhere.
  Done when: after a 5-clause test message, `fm inbox` shows each clause mapped to a task, an explicit drop with reason, or a question. An unmapped clause fails the intake check.

- **Generalize each steer into a principle and sweep for siblings** — FEATURE — value 5 — effort M — risk med — category: steers
  Why: "Budget/pace limits shouldn't block until 75%" and "subagents never capped by a token count" were fixed one limit at a time. Assumption: the user means a principle ("don't block me early"), not one gate. On a steer, Foreman writes the principle in one line and lists every other place it applies (limits, gates, asks). It queues the violations as tasks or confirms they're fine.
  Done when: replaying the 75% steer on a fixture repo with 3 other limiters yields a sweep list naming all 3 with a verdict each.

- **Read the latitude a phrase grants** — FEATURE — value 4 — effort M — risk med — category: autonomy
  Why: "feel free to continue", "exactly this", "I was more thinking…" and "build it in Tauri" carry different discretion. Intake records a per-task latitude (narrow, normal, wide) with the quoted words behind it, and Drive's ask/proceed threshold follows it.
  Done when: two briefs from "do exactly X" and "feel free to continue with those" get different recorded latitudes, and the narrow one blocks an unrequested side task that the wide one allows.

- **Resolve "those", "it" and "the above" and echo the result** — FIX — value 4 — effort S — risk low — category: intake
  Why: Recent requests lean on referents ("those", "all of it", "the second brainstorm"). Assumption: a wrong referent is a cheap, common misread. The brief opens with a line like `"those" = C022..C101 (17 items, from your last message)`.
  Done when: a test conversation with an ambiguous referent produces a brief with an explicit referent line. When two candidate lists exist, it asks one question instead of guessing.

- **Expand verbs into the obligations they imply** — FEATURE — value 4 — effort M — risk low — category: planning
  Why: "Replace", "remove", "rename" and "cleanup" imply deleting the old thing, updating docs and removing dead references. The user's cleanup complaint shows these were never done. A verb→obligations table seeds acceptance criteria with verify commands (grep for the old name, doc mentions).
  Done when: `FIX: rename X to Y` gets generated criteria that fail while any `X` reference remains.

- **Classify each misreading and add the matching intake probe** — FEATURE — value 4 — effort M — risk low — category: self-improvement
  Why: Corrections are logged, but not typed. Assumption: misreads cluster into referent, scope, goal, constraint and priority. `fm friction` counts them per type, and the top type gets a targeted intake question or check.
  Done when: 10 sample corrections get typed, and friction output shows a per-type count with a proposed probe for the top one.

- **Rehearse the user's acceptance glance** — FEATURE — value 4 — effort M — risk med — category: verification
  Why: Users judge by looking at one thing first, such as a screen, a command's output or a number. Intake names that one artifact ("the user will open the Sessions view and look for X") and done runs it, in addition to the criteria. Assumption: the gap between "criteria pass" and "user is happy" is mostly this first look.
  Done when: a UI task's close-out includes the captured first-look artifact, and a brief without a named glance is flagged.

- **Tune report length and depth by what the user acts on** — FEATURE — value 3 — effort M — risk low — category: communication
  Why: The user's replies are terse and act on conclusions. Foreman tracks which parts of past reports were followed up on or ignored per area, then shortens or expands close-outs accordingly. Assumption: that signal is recoverable from the transcripts.
  Done when: after replaying 20 sessions, `fm report-profile` shows per-area verbosity and the next close-out in a "never-read" area is at most 3 lines.

- **Separate question, command, venting and delegation at intake** — FEATURE — value 4 — effort S — risk low — category: intake
  Why: "Trace why X never got done" is a causal investigation, not an edit. "Feel free to continue" delegates judgement. Both are treated like any other FIX or FEATURE today. Intake labels the speech act and routes: a why-question gets a recon/debugger report first, and a venting message gets a friction capture rather than a code change.
  Done when: five sample messages, one per class, route to different first steps in a dry-run classification test.

- **Wild: Mirror back the need they keep not saying** — FEATURE — value 4 — effort M — risk med — category: unspoken needs
  Why: wild. Across steers ("don't block until 75%", "never capped", "cleanup never done") a theme runs: trust that Foreman won't get in the way yet will finish. Weekly, Foreman clusters the user's last 30 requests into 2–3 named recurring needs, with quotes and the tasks that served each. It asks "is this right?" and stores the confirmed ones as the lens for ranking the queue.
  Done when: `fm mirror` prints at least 2 themes, each with 3 or more quoted requests, and a confirmed theme appears in the next brainstorm mission.

- **Wild: Show the interpretation as a version history** — FEATURE — value 3 — effort M — risk low — category: transparency
  Why: wild. The brief's reading of a goal drifts through steers and assumptions, but only the final text survives. Keep each interpretation as a diffable revision ("v1 literal → v2 after your 75% steer → v3"), shown in the pane as a thin timeline you can click to revert to an earlier reading.
  Done when: a task with two steers shows three interpretation revisions, and reverting to v1 restores that criteria set.

- **Wild: Let Foreman argue the user's side in its own plan review** — FEATURE — value 3 — effort M — risk med — category: plan critique
  Why: wild. A `fm-reviewer` lens built only from the user's quoted words, vetoes and steers (no code) reads each L plan and objects in the user's voice ("you said never block early; this gate blocks at 60%"). It is cheap and tool-less. Assumption: quotes are enough to catch contradictions that the code-side lenses miss.
  Done when: a seeded plan that contradicts a stored steer is flagged by this lens with the quote, and a clean plan passes silently.

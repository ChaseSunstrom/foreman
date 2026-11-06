# Brainstorm — lens: unspoken needs

- **Turn each dropped result into a failing test the redo must turn green** — FEATURE — value 5 — effort M — risk low — category: user value
  Why: the drop list repeats (T-1796 "recreated", the push-to-main "redo", the CI "false alarm"), and nothing turns a drop into a check, so the same miss comes back.
  Done when: a dropped task writes a test that fails on the dropped commit and passes on the redo, and the redo can't close while that test fails.

- **Scope each outward grant to its commit and expire it** — SECURITY — value 5 — effort S — risk med — category: trust
  Why: "push foreman/build to main" was approved, but its acceptance criterion stayed pinned to 235932b8 after e021641f moved the build, so the grant outlived the state it approved.
  Done when: a push or site publish whose branch head differs from the approved SHA is refused, and the refusal names the SHA it expected.

- **Pin the evidence the user pasted with a dropped request** — FEATURE — value 4 — effort S — risk low — category: user value
  Why: drop entries record outcomes ("false alarm", "recreated") but not the failure the user actually saw. Assumption: pasted logs and screenshots are in the session.
  Done when: the redo's first recorded step reproduces the pinned evidence before any edit is made.

- **Read "go" back in one line, then start after three seconds unless the user types a word** — FEATURE — value 4 — effort S — risk low — category: unspoken needs. (wild)
  Why: the user says "just go, full force" and "don't ask me", so they want speed with no questions, but a clear view of what will run. Assumption: a veto window is not a question.
  Done when: a "go" with no veto starts after exactly 3 s, and the readback lists every standing grant it will use.

- **Hold the dropped area untouched until its redo lands** — FEATURE — value 3 — effort S — risk med — category: performance
  Why: T-1796 was redone on top of work that had already moved the same code. Assumption: this is a common cause of re-drops.
  Done when: a queue that touches a dropped task's files waits for the redo, and the wait is shown on the queue line.

- **Make a redo's receipt answer the user's last question first** — CLEAN — value 3 — effort S — risk low — category: user value
  Why: the user's messages are short and pointed, and receipts lead with the work log, so the answer comes last. Assumption: the user reads the top line first.
  Done when: when the last user message ends in a question, the receipt's first line answers it, and the work log follows below.

- **Show a redo's diff against the dropped attempt, not against main** — FEATURE — value 3 — effort S — risk low — category: user value
  Why: the user has to judge what changed since the drop, and a diff against main hides that. Assumption: the dropped commit is still in the repo.
  Done when: the redo's receipt shows the diff from the dropped commit as its first diff.

- **Write a redo's commit message in the user's own words from the drop** — FEATURE — value 3 — effort S — risk low — category: delight. (wild)
  Why: the history should read as the user's request, not Foreman's paraphrase. Assumption: the user's wording is in the pack.
  Done when: the redo's commit subject reuses the dropped request's key nouns and verbs, and the commit body quotes the user's words.

- **Learn the user's own stop word and map it to a control, once confirmed** — FEATURE — value 3 — effort S — risk low — category: user value
  Why: the user has their own words for "stop" and "don't ask", and a glossary of nouns doesn't cover controls. Assumption: the words repeat across sessions.
  Done when: after the user's stop word is confirmed once, the next use halts the current step with a receipt and nothing else.

- **At each usage reset, rerun every dropped task's failing test and list the still-red ones in one line** — FEATURE — value 4 — effort S — risk low — category: user value. (wild)
  Why: dropped work fades from view once the next task starts, and the reset is the moment the user's budget refreshes. Assumption: the reset time is known to Foreman.
  Done when: at the reset, a single line lists the dropped tasks whose tests still fail, and an empty list prints nothing.

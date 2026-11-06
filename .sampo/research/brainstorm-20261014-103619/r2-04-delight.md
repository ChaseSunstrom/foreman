# Brainstorm — lens: delight

- **Make the terminal title a one-glyph heartbeat of the run** — FEATURE — value 3 — effort S — risk low — category: ambient status
  Why: assumption: the title bar is unused by the band and statusline; users with many tmux panes/terminal tabs can't tell which session needs them (T-0758 "doesn't sit idle" shows idleness is noticed late). The title is set by an OSC sequence from the existing statusline/Notification hooks, no new tool needed.
  Done when: a test drives hook events (working, waiting-on-user, idle, done) and asserts the emitted OSC title string carries a distinct glyph plus the task id for each state.

- **Greet the user's return with a "while you were away" one-liner as the first message of a resumed session** — FEATURE — value 4 — effort S — risk low — category: resume
  Why: resume at exact step after /compact exists, but the user's words show repeated release/close-out asks and a step-tracking complaint (T-0759); a human-readable first line ("3 tasks closed, 1 needs you: T-0762, step 4/6") makes resuming feel like a colleague handing over. assumption: SessionStart hook can inject a first-line summary.
  Done when: starting a fixture session with ledger events since last end prints a single line naming counts of closed, blocked and ask-pending tasks, and a session with no events prints nothing.

- **Write each task's close-out as a three-line "receipt" in plain language** — FEATURE — value 4 — effort S — risk low — category: close-out
  Why: pack shows many Release-N asks and doctor-style checks; users glance at close-outs, and verbose evidence is for the ledger, not the reader. Receipt = what changed (one sentence), proof (the command and its result), what you might want next. Full evidence stays linked.
  Done when: `fm task finish` output for a fixture task is at most three lines before the evidence link, and the receipt includes the actual verify command that passed.

- **Name each lane and subagent after the work, shown in the band** — FEATURE — value 3 — effort S — risk low — category: fleet legibility
  Why: pack's fleet deck and SubagentStart/Stop hooks exist, but lanes are known by id; "fixing login timeout" beats "lane-7" in a glance. Derive the name from the brief's title verb phrase, truncated.
  Done when: SubagentStart for a lane with a brief produces a band entry whose label is the shortened brief title, and a test covers truncation and a missing brief.

- **Say "nothing to do" with a reason and the best next thing** — FEATURE — value 4 — effort S — risk low — category: idle states
  Why: user's T-0758 "make sure it doesnt sit idle like it is" suggests silent idleness is felt. When the drive stops, print why (queue empty / waiting on ask T-xxxx / blocked on usage limit until HH:MM / paused) and one suggested next action drawn from deferred tasks.
  Done when: each of four idle causes in a fixture produces a distinct reason line, and none ends with empty output.

- **Make step transitions visible with a tiny "step N of M ✓" tick in the statusline** — FEATURE — value 3 — effort S — risk low — category: progress feedback
  Why: T-0759 reports work starting on different steps without the step being updated; a visible tick that changes on update makes drift obvious to the user at a glance, and a missing tick becomes the user's own detector.
  Done when: updating the step via the fm CLI changes the statusline segment in the next render, and an edit under a stale step shows a visibly different "step?" marker.

- **Celebrate a first-time-green with a one-time quiet flourish** — FEATURE — value 2 — effort S — risk low — category: micro-delight
  Why: the pack tracks first-time-pass rate and lessons; marking it ("first-try pass") rewards the discipline users value and gives them something to show. Appears once per qualifying task in the close-out, never as noise on failures.
  Done when: a task finished with no failed verify attempts carries the marker in its receipt, and a task with one failure does not.

- **Wild: Publish a "night reel" Artifact, a scrollable morning story of what the overnight run did** — FEATURE — value 4 — effort M — risk med — category: morning return
  Why: wild; Artifact is unused (0 references), and `fm night` exists with no good way to read its result. Each chapter is one task: brief, the one surprising moment (a refused command, a replan), the receipt. assumption: Artifact publishing works from a hook or CLI call.
  Done when: after a fixture night run, an Artifact HTML file is generated with one chapter per finished task and a chapter for each blocked task including its ask.

- **Wild: Give the guard a "close call" ledger and show the user one save a week** — FEATURE — value 3 — effort M — risk low — category: trust moments
  Why: wild; guard blocks (e.g. `echo 'rm -rf ~' | bash`) are invisible wins; the eval inbox already lists blocks. A weekly "the guard stopped this" line with the command, defanged, turns invisible protection into something the user remembers and shows others.
  Done when: `fm guard saves` lists the top blocked commands of the last 7 days with a one-line reason each, redacted, and prints a friendly empty message when there are none.

- **Wild: Let the user type one-key reactions on a close-out and learn from them** — FEATURE — value 4 — effort M — risk med — category: feedback loop
  Why: wild; the user's steers and drops are the richest taste signal, yet they only show up as long sentences. A `+`/`-`/`?` reply on a receipt gets recorded as an outcome label without parsing prose. assumption: UserPromptSubmit can recognise a bare single-character reply right after a receipt.
  Done when: a bare `-` after a receipt appends a negative outcome event to that task in the ledger, and the same character with no preceding receipt is treated as normal input.

- **Wild: Speak the plan back as a "tabletop narration" before the first edit on L tasks** — FEATURE — value 3 — effort M — risk low — category: plan legibility
  Why: wild; users steer when they feel a plan is wrong, but plan tables are hard to skim. Narrating in four sentences ("first I'll…, the risky part is…, I'll know it worked when…") invites a quick correction when it matters.
  Done when: creating an L plan emits a narration of at most four sentences that names the riskiest step and the observable done-signal taken from the plan data.

- **Show "why am I waiting" on every pending ask with a countdown to its default** — FEATURE — value 3 — effort S — risk low — category: asks
  Why: the pack's `fm ask` and a user who never wants to hand commands imply asks should resolve themselves gracefully; a visible default plus time left keeps the user in control without feeling nagged.
  Done when: `fm ask` pending entries display their default action and remaining time, and a fixture ask past its deadline resolves to the default and says so in the next greeting.

- **Add a live "why did you do that?" one-liner for the last guard block or replan** — FEATURE — value 3 — effort S — risk low — category: explainability
  Why: refusals and mid-task replans are the moments the user is most likely to be puzzled; a single command that prints the triggering rule, the evidence, and the allowed alternative removes the need to scroll the ledger.
  Done when: `fm why` after a fixture block prints the rule name, the matched fragment, and an allowed rewrite, and after no event prints a clear "nothing recent to explain".

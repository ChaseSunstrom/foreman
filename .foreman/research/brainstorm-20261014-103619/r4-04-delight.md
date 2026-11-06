# Brainstorm — lens: delight

- **Open every session with a one-line "last time" greeting that types itself in** — FEATURE — value 3 — effort S — risk low — category: session start
  Why: the user returns after compaction/new sessions often (resume is core); the pack shows SessionStart and MessageDisplay hooks already used but no greeting line that names the step and the one thing that changed while away. Assumption: MessageDisplay can render a single line without a model turn.
  Done when: a fresh session in a project with an open task shows "T-id · step N of M · <last evidence line>" as its first visible line, with zero model tokens spent (hook log shows no API call).

- **Tick a "step N of M ✓" mark in the terminal title and OSC 9;4 progress bar** — FEATURE — value 4 — effort S — risk low — category: ambient progress
  Why: the user complained that "it will start working on different steps without updating the step" (T-0759) and that it "sits idle" (T-0758); a progress bar in the terminal chrome makes drift and stalls visible at a glance. Assumption: terminal supports OSC 9;4 (degrades silently otherwise).
  Done when: advancing a step via `fm task` changes the terminal title and progress percent within one second, and an idle-while-queued state turns the indicator to a distinct "stalled" state.

- **Write each close-out as a three-line receipt a stranger could screenshot** — FEATURE — value 4 — effort S — risk low — category: close-out
  Why: the user's own words show they read releases and close-outs constantly ("Release 1.2.27 …"); jargon-heavy ledger text is the thing they relay. Assumption: closing text is generated in one place (`fm task finish`).
  Done when: `fm task finish` prints exactly three lines (what changed in plain words, proof with the real command and result, what's next), and a lint test fails if any line exceeds ~100 chars or uses an unexplained T-id.

- **Name lanes and subagents after their work in the band** — FEATURE — value 3 — effort S — risk low — category: fleet legibility
  Why: the fleet deck exists, but lanes are shown by id and the user wants to see which cheap model does what (T-0755 asks about lower-model agents). Assumption: SubagentStart payload carries the description string.
  Done when: the band shows "scout·haiku: mapping login flow" instead of an id for a running subagent, and it clears when SubagentStop fires.

- **Say "queue is empty" with a reason and the best next thing** — FEATURE — value 3 — effort S — risk low — category: empty states
  Why: the user hates idling and silence; the end of a run currently risks a bare stop. Assumption: the drive already knows when the queue is exhausted.
  Done when: finishing the last task prints "Queue clear: N done, M blocked (why) — next best: <deferred T-id, one line>", and with blocked-only items it names the single unblocker.

- **Show a one-time quiet flourish the first time a check goes red-to-green** — FEATURE — value 2 — effort S — risk low — category: micro-delight
  Why: the pack's verification machinery records failing→passing transitions; marking the moment makes proof feel earned rather than asserted. Assumption: the evidence ledger distinguishes a first-time pass.
  Done when: the first red→green of a criterion appends a "✓ was red, now green" line to the band exactly once per criterion, and repeats never show it.

- **Mint a morning "while you were away" Artifact with comment-to-queue steering** — FEATURE — value 5 — effort M — risk med — category: return screen
  Why: Artifact is unused (0 references) and the user runs long unattended stretches; the earlier ideas sketched a cockpit, but a *return page* is a smaller, more joyful slice: timeline of what finished, what's blocked, one-tap approve on pending asks. Assumption: Artifact data is private to the user's account, and the projection sends only ids and titles.
  Done when: after a night run, `fm return` publishes a page whose comment on a task card appears in the inbox as a captured request within one minute.

- **Keep one phone notification that updates in place instead of many pings** — FEATURE — value 4 — effort S — risk low — category: notifications
  Why: PushNotification is unused; the user doesn't want to be handed commands or spammed. One living notification ("T-0760 step 3/5 · 2 asks waiting") is calmer than a stream. Assumption: PushNotification supports replace-by-tag; otherwise suppress after the first.
  Done when: over a 6-step task exactly one notification thread exists on the device and its text reflects the current step, and it becomes a distinct "needs you" state only for an ask.

- **Greet blocked asks with a countdown to their default** — FEATURE — value 3 — effort S — risk low — category: asks
  Why: the pack shows `fm ask` and the user's habit of answering identically; showing "defaults to X in 10 min" in the band tells them waiting is safe and idle is deliberate. Assumption: asks already store a default.
  Done when: a pending ask renders "↳ default <X> in 09:41" in the band, ticking down, and the default is applied and logged when it hits zero.

- **Wild: Publish a night-reel Artifact — a scrubbable 20-second time-lapse of the overnight run** — FEATURE — value 4 — effort L — risk med — category: story
  Why: wild. Assumption: ledger events carry timestamps and file paths enough to animate steps as a timeline with diff counts and red→green flips.
  Done when: opening the page plays a timeline with one frame per ledger event and a scrub bar, and frame count equals the ledger event count for that run.

- **Wild: Let the user type one key on a close-out to teach taste** — FEATURE — value 4 — effort M — risk low — category: taste
  Why: wild. The pack shows heavy mining of the user's steers; a one-keystroke reaction (👍 too long / 👍 just right / ✂ too much) after each close-out gives clean labels without a question being asked. Assumption: the band can capture a single keypress without stealing the prompt.
  Done when: pressing `l` after a close-out stores a "too long" label tied to the T-id, and the next three close-outs for that request type are measurably shorter in words.

- **Wild: Give the guard a "close call" reel — show one real save per week** — FEATURE — value 3 — effort M — risk low — category: trust
  Why: wild. The guard blocks dangerous commands silently in bypass mode, so the user never feels its value; surfacing "this week it stopped `rm -rf ~` piped into bash" makes the invisible visible. Assumption: guard decisions are logged with the original command.
  Done when: `fm doctor` and the Monday greeting show the highest-severity block from the last 7 days with its command redacted and the rule that fired, or "no close calls" when none.

- **Wild: Speak the plan back as a short tabletop narration before the first edit on L tasks** — FEATURE — value 3 — effort S — risk low — category: planning feel
  Why: wild. The user reads plans quickly; a four-sentence "first I'll…, then…, the risky bit is…, you'll see…" story is easier to veto than a table. Assumption: the plan review already holds a pivot table to narrate from.
  Done when: starting an L task prints a narration of at most four sentences whose named steps match the plan's step titles one-to-one.

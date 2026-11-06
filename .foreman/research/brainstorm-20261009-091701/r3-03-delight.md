# Brainstorm — lens: delight

- **Run a walk-away check before the user leaves** — FEATURE — value 5 — effort M — risk med — category: autonomy UX
  Why: the user keeps reporting idle or blocked sessions (JARVIS "nothing else to do", refusals mid-run, `fm ask` waits). Assumption: most overnight stalls are asks that could have been predicted from the queue. `fm walkaway` dry-walks the queue, lists the guard categories, grants and `?` items it will probably hit, and collects one batched yes/no. It then prints "safe to leave for ~N hours, will block on X".
  Done when: on a fixture queue needing two known grants, `fm walkaway` lists both, one answer resolves them, and a following unattended `fm run` finishes without an ask event.

- **Hang plaques on files in the desktop tree** — FEATURE — value 4 — effort M — risk low — category: desktop
  Why: Foreman already records `fm why`, `surprise`, lessons and vetoes per file, but they surface only through commands. Hovering a file in Foreman Desktop shows small plaques: "T-0278 made this strict", "surprise: expected X, got Y", "veto: never use Z". Assumption: the desktop app has a file or outline view to hang them on.
  Done when: a fixture file with one lesson, one surprise and one veto shows three plaques in the UI, each linking to its source task or decision.

- **Interrogate the project's memory in plain language** — FEATURE — value 4 — effort M — risk low — category: recall
  Why: `recall`, `why` and `decide` need the user to know the file or keyword. Typical questions are "why is the guard so strict about python -c?" or "did we ever try X?". `fm ask-past` answers from briefs, ledger, decisions and drops, with citations and "no record" when there is none.
  Done when: a question about a known dropped idea returns the drop reason and its task id, and a question with no record answers "no record" rather than inventing history.

- **Capture from any selected text, with the excerpt attached** — FEATURE — value 4 — effort S — risk low — category: capture
  Why: users relay bug feedback from other projects by hand (T-0317 "new bug feedback", JARVIS relays). In the desktop or web terminal pane, selecting an error and pressing a key creates `FIX:` with the excerpt, source session and timestamp stored as the brief's first evidence.
  Done when: selecting a stack trace in a session view creates a captured brief containing the trace verbatim and a link back to that session.

- **Show a ghost pace marker on every progress bar** — FEATURE — value 3 — effort M — risk low — category: motion
  Why: the band stuck on step 1/5 was a complaint, so progress legibility matters to this user. A faint "ghost" marker on the step bar shows where the median of similar past tasks (same type and size) would be by now. Assumption: ledger timestamps are enough to compute this. It stays hidden with fewer than 5 comparable tasks.
  Done when: with seeded history, the band renders a ghost position, and it is absent when history is under the threshold.

- **Add a rubber-duck shaping mode for vague ideas** — FEATURE — value 4 — effort M — risk low — category: intake
  Why: the user gives terse requests, and intake leaves ambiguity for the model to resolve silently. `fm duck "something about idle sessions"` asks at most 3 questions, each grounded in repo and ledger evidence, then writes a classified brief. Questions it could answer itself are skipped.
  Done when: a vague input produces ≤3 questions that each cite a repo or ledger fact, and the resulting brief passes the intake validator.

- **Approve asks from the notification itself** — FEATURE — value 4 — effort M — risk med — category: notifications
  Why: `fm notify` only announces, while `fm ask` waits for the next message. Notifications carry Allow-once, Deny and Open buttons that resolve the ask via the existing grant path. Assumption: desktop and phone notification actions can call back to the local server. This is security-sensitive, so it should reuse the content-hash binding idea already proposed.
  Done when: tapping Allow on a test notification grants exactly the asked category for that task once, and a replayed tap is rejected.

- **Run a heads-down mode that goes silent while the user types** — FEATURE — value 3 — effort S — risk low — category: attention
  Why: the user wants budget limits to stay out of the way until 75%, which suggests a preference for quiet. While the user is actively prompting, the band, pane and statusline collapse to one glyph. Non-urgent events queue into a single "while you were typing" line.
  Done when: with an active-typing signal, non-blocking events don't render, and they appear as one summary line after 30 s idle.

- **Put a wall-display mode on a spare screen** — FEATURE — value 3 — effort S — risk low — category: dashboard
  Why: `fm watch` and the web UI exist, but neither is built for glancing across a room. A kiosk route shows lanes, queue depth and the next action in large type, with an ambient colour for healthy, waiting-on-you or blocked. It follows reduced-motion settings.
  Done when: the kiosk route renders at 1080p and 4K with no scrolling, and its colour changes within 2 s of a block event.

- **Wild: Publish a monthly project yearbook** — FEATURE — value 3 — effort M — risk low — category: reflection
  Why: assumption: the user enjoys shipping and reviewing (frequent releases, taste portrait ideas). A generated one-page recap gives superlatives: biggest deletion, most-corrected assumption, longest-running lane, best guard save and a lesson that proved itself. It is static HTML, shareable, and built only from ledger data.
  Done when: `fm yearbook --month` produces a page whose every superlative links to a real task id, and a month with no data says so instead of inventing awards.

- **Wild: Render a day as a 20-second time-lapse** — FEATURE — value 3 — effort L — risk low — category: replay
  Why: a replay and timeline scrubber is already proposed, but nothing exports a shareable clip. This is a gource-style animation of files touched, lanes spawning and merging, and gates flashing red then green, rendered from ledger events to an MP4 or GIF. Assumption: events carry file paths and timestamps.
  Done when: `fm timelapse --day` writes a ≤30 s file from a fixture ledger, and lane merge events visibly connect to their branches.

- **Wild: Capture tasks by voice, transcribed locally** — FEATURE — value 3 — effort M — risk med — category: voice
  Why: assumption: ideas arrive away from the keyboard, and a local-first stance is preferred. Push-to-talk in the phone or desktop app runs a local speech model and reads back the classified brief ("FIX, login timeout — correct?"). Audio is deleted after transcription, and nothing leaves the device.
  Done when: a recorded sentence becomes a captured brief after one confirmation, and no network call is made during the flow.

- **Wild: Open a "near-miss reel" of saves** — FEATURE — value 3 — effort S — risk low — category: reflection
  Why: guard blocks and gate failures are logged, but the user only sees refusals as friction. Each week, Foreman picks the three catches that would have mattered, such as a blocked `rm` of a real directory or a gate that caught a regression, and shows each as a before/after pair with the command that was stopped. This counterbalances the refusal complaints in the user's words.
  Done when: `fm digest` includes a "caught" section with up to three entries, each pointing to a real guard_block or failed-gate event that was later fixed.

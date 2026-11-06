# Brainstorm — lens: delight

- **Show a one-line "since you left" recap on every resume** — FEATURE — value 5 — effort S — risk low — category: resume
  Why: Foreman resumes at the exact step after `/compact` or a new session, but the user sees only the step; they said "make sure it doesnt sit idle" and complained about step drift, so they check state by hand. assumption: SessionStart can print one line from the ledger.
  Done when: starting a new session on a task with 3 finished steps prints a single line naming steps done, step now, and the last evidence, in under 120 chars.

- **Narrate the queue as a progress sentence in the statusline** — FEATURE — value 4 — effort S — risk low — category: statusline
  Why: statusline and band exist, but "it sits idle" suggests the user can't tell working from stuck. assumption: the band can take a computed phrase like "step 3/5 · tests running 41s · next: T-0759".
  Done when: during a gate run the statusline shows elapsed time that ticks, and shows "idle Ns" in a distinct color after 20s with no tool call.

- **Celebrate a close-out with a one-screen receipt** — FEATURE — value 4 — effort S — risk low — category: close-out
  Why: Each release and task ends with evidence, review and ledger entries scattered across files; the user keeps asking for "Release X (T-… to T-…)". assumption: fm task finish knows steps, evidence, tokens and time.
  Done when: `fm task finish` prints a boxed receipt with steps passed, tests run, review findings fixed, wall time and tokens, and the same text is saved in the ledger.

- **Name the model and effort on every subagent in the band** — FEATURE — value 3 — effort S — risk low — category: transparency
  Why: User asked "can foreman spawn agents of lower models?"; they will want to see that it did, and what it saved. assumption: SubagentStart payload includes the model.
  Done when: while two lanes run, the band shows "scout·haiku, builder·sonnet" and the close-out receipt reports the tokens saved against an all-default run.

- **Offer a one-keystroke "why did it do that" on any guard block** — FEATURE — value 4 — effort M — risk low — category: guard UX
  Why: Many dropped items were guard refusals the user had to read as "working as intended" after long analysis; the refusal message itself could carry the reason and the narrow safe rewrite. assumption: guard decisions already have a rule id.
  Done when: a refused command prints the rule name, one sentence of why, and a concrete allowed alternative, and a test asserts every rule has all three.

- **Auto-batch lookalike captured requests into one task with a "merged" toast** — FEATURE — value 4 — effort M — risk med — category: capture
  Why: T-0755 to T-0760 are six captured fragments, one truncated; the user asked to "put them into one task/milestone". assumption: fm batch exists and similarity can be judged cheaply.
  Done when: capturing three requests in one prompt yields one batch task with three steps and a single line "merged 3 requests → T-0761".

- **Play a quiet completion cue and a distinct needs-you cue** — FEATURE — value 3 — effort S — risk low — category: sound
  Why: Notification hook and fm notify exist but only run a shell command; the user leaves it running unattended. assumption: terminal bell or a local audio player is available.
  Done when: finishing a queue rings a short single cue, and a blocked ask rings a different double cue, both off by a setting.

- **Make `fm doctor` print a green-board with a streak** — FEATURE — value 2 — effort S — risk low — category: health
  Why: fm doctor gates are frequent (self-docs check failed once); a streak of clean days rewards upkeep. assumption: doctor results can be stored per day.
  Done when: `fm doctor` ends with "all 14 checks green · 9 days running" and a red check resets it.

- **Wild: Foreman Postcards — a shareable one-page HTML of a finished milestone** — FEATURE — value 3 — effort M — risk low — category: sharing
  Why: wild. The user ships numbered releases to GitHub and JARVIS; a clean static page with the timeline, diffs-at-a-glance and evidence is a thing people show others. assumption: local file only, no upload.
  Done when: `fm postcard 1.2.27` writes a self-contained HTML file that opens offline and lists each task, its evidence and the gates passed.

- **Wild: A "pair-play" replay that animates a task's steps in the terminal** — FEATURE — value 3 — effort M — risk low — category: replay
  Why: wild. Journals and transcripts already exist; replaying at 20x with step transitions makes debugging and demoing Foreman a pleasure. assumption: the event log has timestamps.
  Done when: `fm replay T-0752 --speed 20` plays the step changes, tool calls and evidence lines in order and ends on the receipt.

- **Wild: Give Foreman a mood meter that reflects the burden score** — FEATURE — value 2 — effort S — risk low — category: personality
  Why: wild. The flywheel measures Foreman's own burden (Frontier 12); a tiny glyph in the band (calm, busy, struggling) turns a metric into something glanceable. assumption: burden is a single number.
  Done when: the band shows one of three glyphs derived from the last 20 tasks' retries and blocks, and the mapping is documented.

- **Show a "what I skipped on purpose" list at close-out** — FEATURE — value 4 — effort S — risk low — category: trust
  Why: The user watches for drift and has dropped items as YAGNI or by design; listing captured-not-chased requests and declined fixes at the end shows discipline instead of hiding it. assumption: captures and drops are already recorded with reasons.
  Done when: the receipt lists each request captured during the task and each drop with its one-line reason, or "none".

- **Preview the next three queue items with estimated time on pause** — FEATURE — value 3 — effort S — risk low — category: queue
  Why: "keeps going through the queue until it's done or needs you" leaves the user guessing what's next when it pauses. assumption: size tags S/M/L map to historical durations.
  Done when: on pause, Foreman prints the next three tasks with a minutes estimate drawn from past same-size tasks.
